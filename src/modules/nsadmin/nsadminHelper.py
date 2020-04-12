import traceback,random, time, json
from datetime import datetime
from src.utilities.logger import Logger
from src.Constant.constant import constant
from src.Constant.ports import ports
from src.modules.nsadmin.nsadminThrift import NSAdminThrift
from src.modules.nsadmin.nsadminObject import NSAdminObject
from src.utilities.utils import Utils
from src.utilities.randValues import randValues
from datetime import datetime
from src.utilities.assertion import Assertion
from src.utilities.dbhelper import dbHelper

class NSAdminHelper():

    def __init__(self, orgId, messageClass):
        self.orgId = orgId
        self.cluster = constant.config['cluster']
        self.nsObj = NSAdminHelper.getConnObj()
        if constant.config['cluster'] in ['nightly','staging','china', 'eu', 'more', 'india'] : self.nsObjMaster = NSAdminHelper.getMasterConnObj()
        self.messageClass = messageClass
        self.messageClassType = NSAdminObject.MessageClass[messageClass]

    def createAndSendMessage(self, msgDict, unique = False):
        if unique == True:
            if msgDict['messageClass'] in ['SMS', 'VOICECALL'] :
                msgDict['receiver'] = randValues.getRandomMobileNumber()
            elif msgDict['messageClass'] == 'EMAIL':
                msgDict['body'] = "test body"
                msgDict['receiver'] = "a3.nsadmin@capillarytech.com"
        else:
            if msgDict['messageClass'] in ['SMS', 'VOICECALL']:
                if not 'receiver' in msgDict:
                    msgDict['receiver'] = "918116645500"
            elif msgDict['messageClass'] == 'EMAIL':
                msgDict['body'] = "test body"
                if not 'receiver' in msgDict:
                    msgDict['receiver'] = "a3.nsadmin@capillarytech.com"
        msgObj = NSAdminObject.message(msgDict)
        return self.nsObj.sendMessage(msgObj)

    def constructContactInfo(self, messageClass, label, value):
        return { 
            'messageClass' : messageClass, 
            'type' : label, 
            'label' : label, 
            'value' : value, 
            'description' : label, 
            'isValid' : True, 
            'isDefault' : True
        }
    
    def getDefaultContactInfo(self, messageClass, value=''):
        contactInfoObj = []
        if messageClass == 'SMS' or messageClass == 'VOICECALL':
            if value == '':
                value = '919845012345'
            contactInfo = self.constructContactInfo(messageClass, 'gsm_sender_id', value)
            contactInfoObj.append(NSAdminObject.contactInfo(contactInfo))
            contactInfo = self.constructContactInfo(messageClass, 'cdma_sender_id', value)
            contactInfoObj.append(NSAdminObject.contactInfo(contactInfo))
        elif messageClass == 'EMAIL':
            if value == '':
                value = 'automation@gmail.com'
            contactInfo = self.constructContactInfo(messageClass, 'dmarc_id', value)
            contactInfoObj.append(NSAdminObject.contactInfo(contactInfo))
            contactInfo = self.constructContactInfo(messageClass, 'sender_id', value)
            contactInfoObj.append(NSAdminObject.contactInfo(contactInfo))
            contactInfo = self.constructContactInfo(messageClass, 'reply_to_id', value)
            contactInfoObj.append(NSAdminObject.contactInfo(contactInfo))
        return contactInfoObj


    def insertDomainProperties(self, contactInfoList, domainName = False):
        messageClass = contactInfoList[0].messageClass
        if not domainName:
            orgName = constant.orgDetails[self.cluster][self.orgId]['orgName']
            domainName = orgName+'_'+str(self.orgId)+'_'+messageClass
        if messageClass == 'EMAIL' and '.com' not in domainName:
            domainName += '.com'
        DomainProperties = {
            'orgId' : self.orgId,
            'domainName' : domainName,
            'description' : domainName,
            'contactInfo' : contactInfoList
        }
        DomainProperties = NSAdminObject.domainProperties(DomainProperties)
        self.nsObj.insertDomainProperties(DomainProperties)
        domainPropertiesList = self.nsObj.getDomainPropertiesByOrg(self.orgId)
        for k in domainPropertiesList:
            if domainName == k.domainName and len(k.contactInfo) != 0:
                return k       

    def addDefaultDomain(self):
        domainPropertiesList = self.nsObj.getDomainPropertiesByOrg(self.orgId)
        for dp in domainPropertiesList:        
            for ci in dp.contactInfo:
                if ci.messageClass == self.messageClass:
                    return dp.id
        contactInfoList = self.getDefaultContactInfo(self.messageClass)
        dp = self.insertDomainProperties(contactInfoList)
        return dp.id


    def configureGateway(self, messagePriority, shortName, useSystemDefaults=True, tags='', gatewayOrgConfigs={}, priority=1):
        domainPropertiesId = self.addDefaultDomain()
        if useSystemDefaults:
            self.saveDomainPropertiesGatewayMapWithUseSystemDefaults(messagePriority, shortName, domainPropertiesId)
        else:
            orgId = str(self.orgId)
            orgName = constant.config['orgName']
            shortName = orgName+shortName
            shortName = shortName.replace(" ","")
            connectionProperties = json.dumps({})
            properties = json.dumps({
                "scopes": tags,
                "countries":["91"]
            })
            gatewayOrgConfigs.update({"properties": properties})
            self.saveDomainPropertiesGatewayMap(domainPropertiesId, messagePriority, shortName, 
            connectionProperties, gatewayOrgConfigs, priority)
        self.domainGatewayValidate()
        return self.getDomainGatewayMapId(shortName)


    def saveDomainPropertiesGatewayMap(self, domainPropertiesId, messagePriority, shortName, 
            connectionProperties, gatewayOrgConfigs, priority=1):
        serviceUrl = ''
        if self.messageClass == 'SMS' and self.cluster in constant.dummyGatewayIP:
            serviceUrl = "http://"+constant.dummyGatewayIP[self.cluster]+":5000"
        gatewayOrgConfigs.update({
            "orgId": self.orgId,
            "shortName": shortName,
            "fullName": shortName,
            "username": "",
            "password": "",
            "connectionProperties": connectionProperties,
            "serviceIp": "",
            "serviceUrl": serviceUrl,
            "statusCheckUrl": "",
            "messageClass": self.messageClass,
            "messagePriority": messagePriority,
            
        })
        if not 'hostName' in gatewayOrgConfigs:
            if self.messageClass == 'SMS':
                gatewayOrgConfigs['hostName'] = 'valuefirst'
            elif self.messageClass == 'EMAIL':
                gatewayOrgConfigs['hostName'] = 'localmail'
        gatewayOrgConfigs = NSAdminObject.gatewayOrgConfigs(gatewayOrgConfigs)
        domainProperties = self.nsObj.getDomainPropertiesByID(domainPropertiesId)
        domainPropertiesGatewayMap = {
            "orgId" : self.orgId,
            "subDomain" : shortName,
            "gatewayOrgConfigs" : gatewayOrgConfigs,
            "domainProperties" : domainProperties,
            "domainPropertiesId" : domainPropertiesId,
            "priority" : priority
        }
        domainPropertiesGatewayMap = NSAdminObject.domainPropertiesGatewayMap(domainPropertiesGatewayMap)
        self.nsObj.saveDomainPropertiesGatewayMap(domainPropertiesGatewayMap)

    def saveDomainPropertiesGatewayMapWithUseSystemDefaults(self, messagePriority, shortName, domainPropertiesId):
        capOrgDPGMList = self.nsObj.getDomainPropertiesGatewayMapByOrg(0, self.messageClassType)
        for dpgm in capOrgDPGMList:
            if hasattr(dpgm.gatewayOrgConfigs,'messagePriority') and hasattr(dpgm.gatewayOrgConfigs,'shortName'):
                if dpgm.gatewayOrgConfigs.messagePriority == messagePriority and dpgm.gatewayOrgConfigs.shortName == shortName:
                    setattr(dpgm,'domainPropertiesId', domainPropertiesId)
                    setattr(dpgm,'orgId', self.orgId)
                    setattr(dpgm,'id', -1)
                    setattr(dpgm,'useSystemDefaults',1)
                    dpgm.gatewayOrgConfigs.orgId = self.orgId
                    self.nsObj.saveDomainPropertiesGatewayMap(dpgm)
                    return

    def domainGatewayMapping(self, shortName , gatewayID):
        domainId = 0;
        mapGateway = self.nsObj.getDomainPropertiesGatewayMapByOrg(0, self.messageClassType)
        for s in mapGateway:
            gatewayOrgConfigs = getattr(s, "gatewayOrgConfigs")
            if getattr(gatewayOrgConfigs, "shortName") == shortName:
                gatewayOrgConfigs = getattr(s, "gatewayOrgConfigs")
                domainProperties = getattr(s, "domainProperties")
                domainId = getattr(s,"id")
                domainProperties.id = gatewayID
                domainPropertiesGatewayMapByID = self.nsObj.getDomainPropertiesGatewayMapByID(domainId)
                setattr(domainPropertiesGatewayMapByID, 'domainPropertiesId', domainProperties.id)
                setattr(domainPropertiesGatewayMapByID, 'orgId', self.orgId)
                setattr(domainPropertiesGatewayMapByID, 'useSystemDefaults', 1)
                setattr(domainPropertiesGatewayMapByID, 'id', -1)
                gatewayOrgConfigs.orgId = constant.config['orgId']
                setattr(domainPropertiesGatewayMapByID, 'gatewayOrgConfigs', gatewayOrgConfigs)
                self.nsObj.saveDomainPropertiesGatewayMap(domainPropertiesGatewayMapByID)
                return


    def domainGatewayValidate(self):
        DGlist = self.nsObj.getDomainPropertiesGatewayMapByOrg(self.orgId, self.messageClassType)
        for m in DGlist:
            if m.isActive == True and m.isValidated == False:
                if constant.config['cluster'] in ['nightly','staging','china', 'eu','more', 'india'] :
                    self.nsObjMaster.validateDomain(m.id,-1)
                else:
                    self.nsObj.validateDomain(m.id, -1)

    def disableDomainPropertiesGatewayMap(self, shortName = False):
        DGlist = self.nsObj.getDomainPropertiesGatewayMapByOrg(self.orgId, self.messageClassType)
        for m in DGlist:
            if m.isActive == True:
                if shortName:
                    if m.gatewayOrgConfigs.shortName == shortName:
                        self.nsObj.disableDomainPropertiesGatewayMap(m.id)
                else:        
                    self.nsObj.disableDomainPropertiesGatewayMap(m.id)
    
    def getDomainGatewayMapId(self, shortName):
        DGlist = self.nsObj.getDomainPropertiesGatewayMapByOrg(self.orgId, self.messageClassType)
        for m in DGlist:
            if m.isActive == True and m.gatewayOrgConfigs.shortName == shortName:
                return m.id


    def assertWithWaitUntil(self, nsadminId, status, assertMessage, timeOut = 60):
        self.waitUntil(nsadminId, status, timeOut)
        resp = self.getSingleMessageById(nsadminId)
        Assertion.constructAssertion(resp.status in status, assertMessage)
        return resp


    def waitUntil(self, nsadminId, status, timeOut = 60):
        for _ in range(0, timeOut):
            msgResp = self.nsObj.getMessagesById([nsadminId])[0]
            if msgResp.status in status:
                Logger.log('returning ')
                return msgResp
            else:
                time.sleep(1)
        Logger.log('returning false')
        return False

    def getSingleMessageById(self, msgId):
        return self.nsObj.getMessagesById([msgId])[0]

    def resetUnknowInvalidEmails(self):
        now = str(datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
        queryU = "update email_status set status='UNKNOWN',verifier='BRITE',soft_bounce_count=10, last_failed_on='"+now+"' where email = 'unknown_email@invalid.com'"
        queryI = "update email_status set status='INVALID',verifier='BRITE',soft_bounce_count=10, last_failed_on='"+now+"' where email = 'invalid_email@invalid.com'"
        dbHelper.queryDB(queryU, 'darknight')
        dbHelper.queryDB(queryI, 'darknight')
        time.sleep(2)       

    @staticmethod
    def checkCommServerConn(ignoreConnectionError=False):
        for port in constant.config['NSADMIN_THRIFT_SERVICE']:
            for _ in range(0, 3):
                try:
                    nsObj = NSAdminThrift(port, 10000)
                    if nsObj.isAlive():
                        if constant.config['cluster'] in ['nightly','staging','china', 'eu', 'more', 'india']:
                            constant.config['nsMasterPort'] = port
                            constant.config[str(port) + '_obj'] = nsObj
                        else:
                            if nsObj.isMaster():
                                constant.config['nsMasterPort'] = port
                                constant.config[str(port)+'_obj'] = nsObj
                    break
                except Exception as e:
                    Logger.log('Error connecting to port:', port,' .Issuing tunnelrestart.') #(traceback.format_exc())
                    Utils.restartTunnel(port)
        if not ignoreConnectionError and not 'nsMasterPort' in constant.config:
            raise Exception('Master NSAdmin server not found')

    @staticmethod
    def getConnObj(newConnection=False):
        port = constant.config['nsMasterPort']
        connPort = str(port)+'_obj'
        if connPort in constant.config:
            if newConnection:
                constant.config[connPort].close()
                constant.config[connPort] = NSAdminThrift(port)
            return constant.config[connPort]
        else:
            return NSAdminThrift(port)

    @staticmethod
    def getMasterConnObj():
        port = ports.portsUsed[constant.config['cluster']]['COMMENGINE_THRIFT_SERVICE'][0]
        return NSAdminThrift(port)

    @staticmethod
    def getTableName(year=str(datetime.now().year), month=str(datetime.now().month)):
        if len(month) == 1:
            month = '0'+month
        return "messages_"+year+"_"+month 

    @staticmethod
    def getDataTableName(year=str(datetime.now().year), month=str(datetime.now().month)):
        if len(month) == 1:
            month = '0'+month
        return "message_data_"+year+"_"+month         


