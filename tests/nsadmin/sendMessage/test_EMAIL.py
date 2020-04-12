# -*- coding: utf-8 -*-

import pytest, time, json
from src.Constant.constant import constant
from src.utilities.logger import Logger
from src.modules.nsadmin.nsadminObject import NSAdminObject
from src.modules.nsadmin.nsadminHelper import NSAdminHelper
from src.initializer.generateThrift import nsadmin
from src.utilities.assertion import Assertion
from src.utilities.randValues import randValues
from src.utilities.fileHelper import FileHelper
from src.utilities.dbhelper import dbHelper

class Test_sendEMAIL():

    def setup_class(self):
        Logger.logSuiteName(str(self).split('.')[-1])
        self.orgId = constant.config['orgId']
        self.cluster = constant.config['cluster']

    def setup_method(self, method):      
        self.nsObj = NSAdminHelper.getConnObj(newConnection=True)
        self.nsadminHelper = NSAdminHelper(self.orgId, 'EMAIL')
        self.nsadminHelper.disableDomainPropertiesGatewayMap()        
        Logger.logMethodName(method.__name__)
        

    @pytest.mark.parametrize('priority, gateway', [
                    ('HIGH', 'localmail_HIGH'),
                    ('BULK', 'localmail_BULK')])        
    def test_sendMessage_EMAIL_Sanity(self, priority, gateway):
        self.nsadminHelper.configureGateway(priority, gateway)
        msgDict = {"messageClass" : "EMAIL", "priority" : priority, "message" : "test message with priority "+priority}
        resp = self.nsadminHelper.createAndSendMessage(msgDict)
        Assertion.constructAssertion(resp > 0, 'sendMessage output')
        resp = self.nsadminHelper.assertWithWaitUntil(resp, ['RECEIVED_IN_QUEUE', 'SENT'], 'Messages status ACK', 10)
        Assertion.constructAssertion(resp.gateway == gateway, 'gateway used for sending')
        Assertion.constructAssertion(resp.priority == priority, 'priority')  


    @pytest.mark.parametrize('priority, gateway, status', [
                    ('HIGH', 'localmail_HIGH', 'SENT'),
                    ('BULK', 'localmail_BULK', 'GTW_NOT_FOUND')])        
    def test_sendMessage_EMAIL_withoutGateway(self, priority, gateway, status):
        msgDict = {"messageClass" : "EMAIL", "priority" : priority, "message" : "test message with priority "+priority}
        msgId = self.nsadminHelper.createAndSendMessage(msgDict)
        self.nsadminHelper.assertWithWaitUntil(msgId, [status], 'Messages status ACK', 10)


    @pytest.mark.parametrize('priority, gateway, tags', [
                    ('HIGH', 'localmail_HIGH', ['transaction', 'otp']),
                    ('BULK', 'localmail_BULK', ['campaign'])])
    def test_sendMessage_EMAIL_OrgGateway(self, priority, gateway, tags):
        domainPropertiesId = self.nsadminHelper.addDefaultDomain()
        orgName = constant.config['orgName']
        shortName = orgName+gateway
        connectionProperties = json.dumps({})
        properties = json.dumps({
            "scopes": tags
        })
        gatewayOrgConfigs = {
            "orgId": self.orgId,
            "hostName": "localmail",
            "shortName": shortName,
            "fullName": shortName,
            "username": "",
            "password": "",
            "connectionProperties": connectionProperties,
            "serviceIp": "",
            "serviceUrl": "",
            "statusCheckUrl": "",
            "messageClass": "EMAIL",
            "messagePriority": priority,
            "properties": properties
        }
        gatewayOrgConfigs = NSAdminObject.gatewayOrgConfigs(gatewayOrgConfigs)
        domainProperties = self.nsObj.getDomainPropertiesByID(domainPropertiesId)
        domainPropertiesGatewayMap = {
            "orgId" : self.orgId,
            "subDomain" : shortName,            
            "gatewayOrgConfigs" : gatewayOrgConfigs,
            "domainProperties" : domainProperties,
            "domainPropertiesId" : domainPropertiesId,
        }
        domainPropertiesGatewayMap = NSAdminObject.domainPropertiesGatewayMap(domainPropertiesGatewayMap)
        self.nsObj.saveDomainPropertiesGatewayMap(domainPropertiesGatewayMap)
        self.nsadminHelper.domainGatewayValidate()
        msgDict = {"messageClass" : "EMAIL", "priority" : priority, "message" : "test message with priority "+priority}
        msgId = self.nsadminHelper.createAndSendMessage(msgDict)
        resp = self.nsadminHelper.assertWithWaitUntil(msgId, ['RECEIVED_IN_QUEUE', 'SENT'], 'Messages status ACK', 10)
        Assertion.constructAssertion(resp.gateway == shortName, 'gateway used for sending')
        Assertion.constructAssertion(resp.priority == priority, 'priority')  


    def test_sendMultipleMessageEmailWithBulkGateway(self):
        self.nsadminHelper.configureGateway('BULK', 'localmail_BULK')
        params = [
            [0, "BULK",  "test message 1", "autoemail"+randValues.getRandomMobileNumber()+"@gmail.com", ['RECEIVED_IN_QUEUE', 'SENT']],
            [1, "BULK",  "test message 2", "autoemail"+randValues.getRandomMobileNumber()+"@gmail.com", ['RECEIVED_IN_QUEUE', 'SENT']],
            [2, "HIGH",  "test message 3", "autoemail"+randValues.getRandomMobileNumber()+"@gmail.com", ['RECEIVED_IN_QUEUE', 'FAILED']]
        ]
        self.nsObj.whitelistEmailIds([params[0][3], params[1][3], params[2][3]])
        msgObjList = []
        for p in params:
            msgObj = NSAdminObject.message({"messageClass" : "EMAIL", "inboxId" : p[0], 
                    "priority" : p[1], "message" : p[2], "receiver" : p[3], "body" : "test body"})
            msgObjList.append(msgObj)
        resp = self.nsObj.sendMultipleMessages(msgObjList)
        for i in range(0, 3):
            msgId = resp[i]
            msgResp = self.nsObj.getMessagesById([msgId])[0]
            #inboxId = msgResp.inboxId
            msgParams = params[i]
            Assertion.constructAssertion(msgResp.status in msgParams[4], 'Messages status')
            Assertion.constructAssertion(msgResp.priority == msgParams[1], 'Messages priority')
            Assertion.constructAssertion(msgResp.message == msgParams[2], 'Message')
            Assertion.constructAssertion(msgResp.receiver == msgParams[3], 'Messages receiver')  
            currentMonthTable = NSAdminHelper.getDataTableName()        
            query = 'select nsadmin_id from '+currentMonthTable+' where nsadmin_id='+str(msgId)
            dbResp = dbHelper.queryDB(query, 'nsadmin')
            Assertion.constructAssertion(dbResp[0][0] == msgId, 'Messages id') 

        for p in params:
            msg = self.nsObj.getMessagesByReceiver(self.orgId, p[3])
            Assertion.constructAssertion(msg[0].message == p[2], 'Assert getMessagesByReceiver')



     
    def test_sendMessage_EMAIL_withHTMLContentAndAttachment(self):
        filePath = constant.rootPath + '/src/modules/nsadmin/html'
        body = FileHelper.readFile(filePath)
        self.nsadminHelper.configureGateway('BULK', 'localmail_BULK')
        msgDict = {"messageClass" : "EMAIL", "priority" : "BULK", "receiver" : "autoemail8116645500@gmail.com",
            "message" : "test message with html content", "body" : body, "attachmentId" : [23303]}
        msgObj = NSAdminObject.message(msgDict)
        msgId = self.nsObj.sendMessage(msgObj)
        resp = self.nsadminHelper.assertWithWaitUntil(msgId, ['RECEIVED_IN_QUEUE', 'SENT'], 'Messages status ACK', 10)
        currentMonthTable = NSAdminHelper.getDataTableName()        
        query = 'select attachment_id from '+currentMonthTable+' where nsadmin_id='+str(msgId)
        resp = dbHelper.queryDB(query, 'nsadmin')
        Assertion.constructAssertion(resp[0][0] == '23303', 'Messages attachmentId')       

    def test_sendMessasge_EMAIL_InvalidReceiver(self):
        self.nsadminHelper.configureGateway("BULK", "localmail_BULK")
        msgDict = {"receiver": "invalid", "messageClass" : "EMAIL", "priority" : "BULK", 
                "message" : "test message with receiver invalid"}
        msgId  = self.nsadminHelper.createAndSendMessage(msgDict)
        self.nsadminHelper.assertWithWaitUntil(msgId, ['BLOCKED'], 'Messages status ACK', 10)

        msgDict = {"receiver": "", "messageClass" : "EMAIL", "priority" : "BULK", 
                "message" : "test message with empty receiver"}
        resp = self.nsadminHelper.createAndSendMessage(msgDict)
        Assertion.constructAssertion(resp == -1, 'sendMessage output')

        msgDict = {"messageClass" : "EMAIL", "priority" : "BULK", "message" : "test message with empty receiver"}           
        msgObj = NSAdminObject.message(msgDict)
        resp = self.nsObj.sendMessage(msgObj)
        Assertion.constructAssertion(resp == -1, 'sendMessage output')

    def test_sendMessage_EMAIL_without_Body(self):
        self.nsadminHelper.configureGateway('BULK', 'localmail_BULK')
        msgDict = {"messageClass" : "EMAIL", "priority" : "BULK", "receiver" : "autoemail8116645500@gmail.com",
            "message" : "test message without body"}
        msgObj = NSAdminObject.message(msgDict)
        msgId = self.nsObj.sendMessage(msgObj)
        self.nsadminHelper.assertWithWaitUntil(msgId, ['EMAIL_BODY_EMPTY'], 'Messages status ACK', 10)


    def test_sendMessage_EMAIL_without_Message(self):
        self.nsadminHelper.configureGateway('BULK', 'localmail_BULK')
        msgDict = {"messageClass" : "EMAIL", "priority" : "BULK", "receiver" : "autoemail8116645500@gmail.com",
            "body" : "test message without message"}
        msgObj = NSAdminObject.message(msgDict)
        resp = self.nsObj.sendMessage(msgObj)
        Assertion.constructAssertion(resp == -1, 'sendMessage output')


    def test_sendMessage_EMAIL_ScheduledTime(self):
        self.nsadminHelper.configureGateway('BULK', 'localmail_BULK')
        msgDict = {"messageClass" : "EMAIL", "priority" : "BULK", "receiver" : "autoemail8116645500@gmail.com",
            "message" : "test body", "body" : "test message body", "scheduledTimestamp" : int(time.time()+600)*1000}
        msgObj = NSAdminObject.message(msgDict)
        msgId = self.nsObj.sendMessage(msgObj)
        self.nsadminHelper.assertWithWaitUntil(msgId, ['DELAYED_SCHEDULED'], 'Messages status ACK', 10)


    @pytest.mark.parametrize('priority, gateway', [
                    ('HIGH', 'localmail_HIGH'),
                    ('BULK', 'localmail_BULK')])        
    def test_sendMessage_EMAIL_HardSoftBounce_AfterWhitelisting(self, priority, gateway):      
        self.nsadminHelper.configureGateway(priority, gateway)
        emailH = "ComsysAutomation_QAHBA@gmail.com"
        emailS = "ComsysAutomation_QASBA@gmail.com"
        self.nsObj.whitelistEmailIds([emailH, emailS])
        msgDict = {"messageClass" : "EMAIL", "priority" : priority, "receiver" : emailH,
            "message" : "test body", "body" : "test message body", "tags":["hb"]}
        msgObj = NSAdminObject.message(msgDict)
        msgId = self.nsObj.sendMessage(msgObj)
        self.nsadminHelper.assertWithWaitUntil(msgId, ['RECEIVED_IN_QUEUE', 'SENT'], 'Messages status ACK', 10)

        msgDict = {"messageClass" : "EMAIL", "priority" : priority, "receiver" : emailS,
            "message" : "test body", "body" : "test message body", "tags":["sb"]}
        msgObj = NSAdminObject.message(msgDict)
        msgId = self.nsObj.sendMessage(msgObj)
        self.nsadminHelper.assertWithWaitUntil(msgId, ['RECEIVED_IN_QUEUE', 'SENT'], 'Messages status ACK', 10)


    @pytest.mark.parametrize('priority, gateway', [
                    ('HIGH', 'localmail_HIGH'),
                    ('BULK', 'localmail_BULK')])        
    def test_sendMessage_EMAIL_withSoftBounce_lastFailedOnMoreThanMonth(self, priority, gateway):      
        self.nsadminHelper.configureGateway(priority, gateway)
        msgDict = {"messageClass" : "EMAIL", "priority" : priority, "receiver" : "ComsysAutomation_QASB@gmail.com",
            "message" : "test body", "body" : "test message body", "tags":["sb"]}
        msgObj = NSAdminObject.message(msgDict)
        msgId = self.nsObj.sendMessage(msgObj)
        self.nsadminHelper.assertWithWaitUntil(msgId, ['RECEIVED_IN_QUEUE', 'SENT'], 'Messages status ACK', 10)


    @pytest.mark.parametrize('priority, gateway', [
                    ('HIGH', 'localmail_HIGH'),
                    ('BULK', 'localmail_BULK')])        
    def test_sendMessage_EMAIL_ValidSender(self, priority, gateway):
        self.nsadminHelper.configureGateway(priority, gateway)
        msgDict = {"messageClass" : "EMAIL", "priority" : priority, 'sender' : 'test@test.com',
            "message" : "test message with priority "+priority}
        msgId = self.nsadminHelper.createAndSendMessage(msgDict)
        resp = self.nsadminHelper.assertWithWaitUntil(msgId, ['RECEIVED_IN_QUEUE', 'SENT'], 'Messages status ACK', 10)
        currentMonthTable = NSAdminHelper.getDataTableName()
        query = 'select sender from '+currentMonthTable+' where nsadmin_id='+str(msgId)
        resp = dbHelper.queryDB(query, 'nsadmin')        
        Assertion.constructAssertion(resp[0][0] == 'test@test.com', 'sender')
        

    @pytest.mark.parametrize('priority, gateway', [
                    ('HIGH', 'localmail_HIGH'),
                    ('BULK', 'localmail_BULK')])        
    def test_sendMessage_EMAIL_InvalidSender(self, priority, gateway):
        self.nsadminHelper.configureGateway(priority, gateway)
        msgDict = {"messageClass" : "EMAIL", "priority" : priority, 'sender' : '',
            "message" : "test message with priority "+priority}
        msgId = self.nsadminHelper.createAndSendMessage(msgDict)
        resp = self.nsadminHelper.assertWithWaitUntil(msgId, ['RECEIVED_IN_QUEUE', 'SENT'], 'Messages status ACK', 10)
        Assertion.constructAssertion(resp.sender != '', 'sender is not empty')
        # msgObj without sender 
        msgObj = {'inboxId': 1, 'messageId': 1, 'clientId': 111, 'receiverId':111, 'campaignId': 222, 
                'sendingOrgId' : self.orgId, 'messageClass' : 'EMAIL', 'receiver' : 'autoemail8116645500@gmail.com',
                'priority' : priority, 'message' : 'test message with priority '+priority,
                'scheduledTimestamp' : int(time.time())*1000, 'body' : 'test body'}
        msgObj= nsadmin.Message(**msgObj)  
        msgId = self.nsObj.sendMessage(msgObj)
        self.nsadminHelper.assertWithWaitUntil(msgId, ['RECEIVED_IN_QUEUE', 'SENT'], 'Messages status ACK', 10)
        Assertion.constructAssertion(resp.sender != '', 'sender is not empty')


    @pytest.mark.parametrize('priority, gateway, status', [
                    ('HIGH', 'localmail_HIGH', ['RECEIVED_IN_QUEUE', 'SENT']),
                    ('BULK', 'localmail_BULK', ['GTW_NOT_FOUND', 'BLOCKED'])])        
    def test_sendMessage_EMAIL_WhitelistStatus_UNKNOWN_INVALID(self, priority, gateway, status):
        # without gateway
        self.nsadminHelper.resetUnknowInvalidEmails()
        msgDict = {"messageClass" : "EMAIL", "priority" : priority, 'receiver' : 'unknown_email@invalid.com',
            "message" : "test message unknown_email with priority "+priority}
        msgId = self.nsadminHelper.createAndSendMessage(msgDict)
        resp = self.nsadminHelper.assertWithWaitUntil(msgId, status, 'Messages status ACK', 10)
        msgDict = {"messageClass" : "EMAIL", "priority" : priority, 'receiver' : 'invalid_email@invalid.com',
            "message" : "test message invalid_email with priority "+priority}
        msgId = self.nsadminHelper.createAndSendMessage(msgDict)
        resp = self.nsadminHelper.assertWithWaitUntil(msgId, status, 'Messages status ACK', 10)        

        # with gateway
        self.nsadminHelper.resetUnknowInvalidEmails()
        self.nsadminHelper.configureGateway(priority, gateway)
        msgDict = {"messageClass" : "EMAIL", "priority" : priority, 'receiver' : 'unknown_email@invalid.com',
            "message" : "test message unknown_email with priority "+priority}
        msgId = self.nsadminHelper.createAndSendMessage(msgDict)
        resp = self.nsadminHelper.assertWithWaitUntil(msgId, status, 'Messages status ACK', 10)
        msgDict = {"messageClass" : "EMAIL", "priority" : priority, 'receiver' : 'invalid_email@invalid.com',
            "message" : "test message invalid_email with priority "+priority}
        msgId = self.nsadminHelper.createAndSendMessage(msgDict)
        resp = self.nsadminHelper.assertWithWaitUntil(msgId, status, 'Messages status ACK', 10)        

    


    @pytest.mark.parametrize('priority, gateway', [
                    ('HIGH', 'sendgridmail'),
                    ('BULK', 'localmail_BULK')])        
    def test_sendMessage_EMAIL_India_More_Eu_Prod_Sanity(self, priority, gateway):      
        self.nsadminHelper.configureGateway(priority, gateway)
        msgDict = {"messageClass" : "EMAIL", "priority" : priority, "receiver" : constant.config['prodEmail1'],
            "message" : "test message for "+self.cluster+" cluster "+priority, "body" : "test body"}
        msgObj = NSAdminObject.message(msgDict)
        msgId = self.nsObj.sendMessage(msgObj)
        self.nsadminHelper.assertWithWaitUntil(msgId, ['RECEIVED_IN_QUEUE', 'SENT'], 'Messages status ACK', 10)


    def test_sendMultipleMessageEmail_India_More_Prod_Sanity(self):
        if self.cluster == 'india':
            self.nsadminHelper.configureGateway('BULK', 'sendgridmail_BULK')
        else:
            self.nsadminHelper.configureGateway('BULK', 'sendgridapac2_BULK')
        params = [
            [0, "BULK",  "test message 1 for "+self.cluster, constant.config['prodEmail1'], ['RECEIVED_IN_QUEUE', 'SENT']],
            [1, "BULK",  "test message 2 for "+self.cluster, constant.config['prodEmail1'], ['RECEIVED_IN_QUEUE', 'SENT']]
        ]
        msgObjList = []
        for p in params:
            msgObj = NSAdminObject.message({"messageClass" : "EMAIL", "inboxId" : p[0], 
                    "priority" : p[1], "message" : p[2], "receiver" : p[3], "body" : "test body"})
            msgObjList.append(msgObj)
        resp = self.nsObj.sendMultipleMessages(msgObjList)
        for i in range(0, 2):
            msgId = resp[i]
            msgResp = self.nsObj.getMessagesById([msgId])[0]
            msgParams = params[i]
            Assertion.constructAssertion(msgResp.status in msgParams[4], 'Messages status')
            Assertion.constructAssertion(msgResp.priority == msgParams[1], 'Messages priority')
            Assertion.constructAssertion(msgResp.message == msgParams[2], 'Message')
            Assertion.constructAssertion(msgResp.receiver == msgParams[3], 'Messages receiver')  

    @pytest.mark.parametrize('priority, gateway', [
                    ('HIGH', 'sendgridcn'),
                    ('BULK', 'sendgridcn_BULK')])        
    def test_sendMessage_EMAIL_China_Prod_Sanity(self, priority, gateway):      
        self.nsadminHelper.configureGateway(priority, gateway)
        msgDict = {"messageClass" : "EMAIL", "priority" : priority, "receiver" : constant.config['prodEmail1'],
            "message" : "test message for China cluster "+priority, "body" : "test body"}
        msgObj = NSAdminObject.message(msgDict)
        msgId = self.nsObj.sendMessage(msgObj)
        self.nsadminHelper.assertWithWaitUntil(msgId, ['RECEIVED_IN_QUEUE', 'SENT'], 'Messages status ACK', 10)
