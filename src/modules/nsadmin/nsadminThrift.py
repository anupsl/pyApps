from src.Constant.constant import constant
from src.initializer.generateThrift import nsadmin
from src.utilities.logger import Logger
from thriftpy.rpc import make_client



class NSAdminThrift(object):

    def __init__(self, port, timeout=60000):
        self.conn = make_client(nsadmin.NSAdminService, '127.0.0.1', port, timeout=timeout)

    def close(self):
        self.conn.close()

    def log(self, output):
        Logger.log(output)
        return output

    def isAlive(self):
        return self.log(self.conn.isAlive())

    def getStatus(self):
        return self.log(self.conn.getStatus())

    def isMaster(self):
        return self.log(self.conn.isMaster())        

    def sendMessage(self, message):
        Logger.log(message)
        return self.log(self.conn.sendMessage(message))

    def sendMultipleMessages(self, messageList):
        Logger.log(messageList)
        return self.log(self.conn.sendMultipleMessages(messageList))

    def getMessagesById(self, idList):
        Logger.log(idList)
        return self.log(self.conn.getMessagesById(idList))

    def getMessageLogs(self, orgId, messageClass, receiver):
        Logger.log(orgId, ' - ',messageClass,' - ',receiver)
        return self.log(self.conn.getMessageLogs(orgId, messageClass, receiver))

    def getMessageSendError(self, messageId):
        Logger.log(messageId)
        return self.log(self.conn.getMessageSendError(messageId))

    def getMessagesByReceiver(self, orgId, receiver):
        Logger.log('orgId ',orgId,' receiver ',receiver)
        return self.log(self.conn.getMessagesByReceiver(orgId, receiver))

    def getMessagesByUserOrReciever(self, orgId, userId, receiver):
        Logger.log('orgId ',orgId,' userId ',userId,' receiver ',receiver)
        return self.log(self.conn.getMessagesByUserOrReciever(orgId, userId, receiver))  

    def whitelistEmailIds(self, emailIds):
        Logger.log('emailIds ',emailIds)
        return self.log(self.conn.whitelistEmailIds(emailIds))      

    def insertDomainProperties(self,domainProperties):
        Logger.log('Request - ' ,domainProperties)
        return self.log(self.conn.insertDomainProperties(domainProperties))

    def updateDomainProperties(self,domainProperties):
        Logger.log('Request - ' ,domainProperties)
        return self.log(self.conn.updateDomainProperties(domainProperties))

    def getDomainPropertiesByOrg(self,orgId):
        Logger.log('OrgId - ' ,orgId)
        return self.log(self.conn.getDomainPropertiesByOrg(orgId))

    def disableDomainProperties(self, domainPropsId, orgId):
        Logger.log('OrgId - ', orgId, ' - Domain PropId -' , domainPropsId)
        return self.log(self.conn.disableDomainProperties(domainPropsId, orgId))

    def getDomainPropertiesGatewayMapByOrg(self, orgId, messageClass):
        Logger.log('OrgId - ', orgId, ' - MessageClass -' , messageClass)
        return self.log(self.conn.getDomainPropertiesGatewayMapByOrg(orgId,messageClass))

    def getDomainPropertiesByID(self, domainPropertiesId):
        Logger.log('Domain Prop Id - ', domainPropertiesId)
        return self.log(self.conn.getDomainPropertiesByID(domainPropertiesId))

    def getDomainPropertiesGatewayMapByID(self, id):
        Logger.log('Gateway Id - ', id)
        return self.log(self.conn.getDomainPropertiesGatewayMapByID(id))

    def saveDomainPropertiesGatewayMap(self, domainPropertiesGatewayMap):
        Logger.log('Domain Gateway Map - ', domainPropertiesGatewayMap)
        return self.log(self.conn.saveDomainPropertiesGatewayMap(domainPropertiesGatewayMap))

    def validateDomain(self, domainPropGatewayMapId, triggeredBy = -1):
        Logger.log('MapId - ', domainPropGatewayMapId)
        return self.log(self.conn.validateDomain(domainPropGatewayMapId, triggeredBy))

    def disableDomainPropertiesGatewayMap(self, domainPropertiesGatewayMapId):
        Logger.log('Gateway Map Id - ', domainPropertiesGatewayMapId)
        return self.log(self.conn.disableDomainPropertiesGatewayMap(domainPropertiesGatewayMapId))

    def getCreditDetails(self, orgId):
        Logger.log('orgId - ',orgId)
        return self.log(self.conn.getCreditDetails(orgId))

    def addCredits(self, creditDetails):
        Logger.log('creditDetails - ',creditDetails)
        return self.log(self.conn.addCredits(creditDetails))

    def getCreditsLog(self, orgId):
        Logger.log('orgId - ',orgId)
        return self.log(self.conn.getCreditsLog(orgId)) 

    def isMessageDelivered(self, messageId):
        Logger.log('messageId - ', messageId)
        return self.log(self.conn.isMessageDelivered(messageId))       

    def getCreditDetailsByOrgAndChannel(self, orgId, messageClass, requestId = 'test'):
        Logger.log('orgId -',orgId, ' messageClass -', messageClass)
        return self.log(self.conn.getCreditDetailsByOrgAndChannel(orgId, messageClass, requestId))