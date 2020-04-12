# -*- coding: utf-8 -*-

import pytest, time, json
from datetime import datetime

from src.Constant.constant import constant
from src.utilities.logger import Logger
from src.modules.nsadmin.nsadminObject import NSAdminObject
from src.modules.nsadmin.nsadminHelper import NSAdminHelper
from src.utilities.assertion import Assertion
from src.utilities.randValues import randValues
from src.utilities.dbhelper import dbHelper
from src.utilities.utils import Utils
from src.modules.darknight.darknightHelper import DarknightHelper


class Test_sendMessage_SMS():

    def setup_class(self):
        Logger.logSuiteName(str(self).split('.')[-1])
        self.orgId = 1604 #constant.config['orgId']
        self.cluster = constant.config['cluster']

    def setup_method(self, method):      
        self.nsObj = NSAdminHelper.getConnObj(newConnection=True)
        self.nsadminHelper = NSAdminHelper(self.orgId, 'SMS')
        self.nsadminHelper.disableDomainPropertiesGatewayMap()        
        Logger.logMethodName(method.__name__)


    @pytest.mark.parametrize('priority, gateway', [
                    ('HIGH', 'cardboardfishmock'),
                    ('BULK', 'valuefirstmock')])        
    def test_sendMessage_SMS_Sanity(self, priority, gateway):
        self.nsadminHelper.configureGateway(priority, gateway)
        msgDict = {"messageClass" : "SMS", "priority" : priority, "message" : "test message with priority "+priority}
        resp  = self.nsadminHelper.createAndSendMessage(msgDict)
        Assertion.constructAssertion(resp > 0, 'sendMessage output')
        resp = self.nsadminHelper.assertWithWaitUntil(resp, ['RECEIVED_IN_QUEUE', 'SENT'], 'Messages status ACK', 10)
        Assertion.constructAssertion(resp.gateway == gateway, 'gateway used for  sending')
        Assertion.constructAssertion(resp.priority == priority, 'priority')

    def test_sendMessage_DefaultPriority(self):
        self.nsadminHelper.configureGateway("HIGH", "cardboardfishmock")
        msgDict = {"messageClass" : "SMS", "priority" : "DEFAULT", "message" : "test message with priority DEFAULT"}
        msgId = self.nsadminHelper.createAndSendMessage(msgDict)
        resp = self.nsadminHelper.assertWithWaitUntil(msgId, ['RECEIVED_IN_QUEUE', 'SENT'], 'Messages status ACK', 10)
        Assertion.constructAssertion(resp.gateway == "cardboardfishmock", 'gateway used for sending')
        Assertion.constructAssertion(resp.priority == "HIGH", 'priority')


    @pytest.mark.parametrize('priority', [('HIGH'), ('BULK')]) 
    def test_sendMessage_withoutGateway(self, priority):
        msgDict = {"messageClass" : "SMS", "priority" : priority, "message" : "test message without gateway priority "+priority}
        msgId  = self.nsadminHelper.createAndSendMessage(msgDict)
        self.nsadminHelper.assertWithWaitUntil(msgId, ['GTW_NOT_FOUND'], 'Messages status', 10)
        resp = self.nsObj.getMessageSendError(msgId)
        Assertion.constructAssertion("no configs for" in resp, 'Error message without gateway')


    def test_sendMessasge_SMS_InvalidReceiver(self):
        self.nsadminHelper.configureGateway("BULK", "valuefirstmock")
        msgDict = {"receiver": "invalid", "messageClass" : "SMS", "priority" : "BULK", 
                "message" : "test message with receiver invalid"}
        msgId  = self.nsadminHelper.createAndSendMessage(msgDict)
        self.nsadminHelper.assertWithWaitUntil(msgId, ['GTW_NOT_FOUND'], 'Messages status', 10)
        resp = self.nsObj.getMessageSendError(msgId)
        Assertion.constructAssertion("no gw found after checking" in resp, 'Error message without gateway')        

        msgDict = {"receiver": "", "messageClass" : "SMS", "priority" : "BULK", 
                "message" : "test message with empty receiver"}
        resp  = self.nsadminHelper.createAndSendMessage(msgDict)
        Assertion.constructAssertion(resp == -1, 'sendMessage output')

        msgDict = {"messageClass" : "SMS", "priority" : "BULK", "message" : "test message with empty receiver"}           
        msgObj = NSAdminObject.message(msgDict)
        resp = self.nsObj.sendMessage(msgObj)
        Assertion.constructAssertion(resp == -1, 'sendMessage output')

    @pytest.mark.parametrize('priority, gateway', [
                    ('HIGH', 'cardboardfishmock'),
                    ('BULK', 'valuefirstmock')])
    def test_sendMessage_delayScheduledMessage(self, priority, gateway):
        self.nsadminHelper.configureGateway(priority, gateway)
        scheduledTimestamp = int(time.time() + 180) * 1000 # 2 mins delay
        msgDict = {"messageClass" : "SMS", "priority" : priority, "scheduledTimestamp" : scheduledTimestamp,
            "message" : "test message with delayed schedule"}
        msgId  = self.nsadminHelper.createAndSendMessage(msgDict)        
        self.nsadminHelper.assertWithWaitUntil(msgId, ['DELAYED_SCHEDULED'], 'Messages status', 10)
        Utils.sleep(180)
        self.nsadminHelper.assertWithWaitUntil(msgId, ['READ', 'RECEIVED_IN_QUEUE', 'SENT'], 'Messages status after delay', 10)


    def test_sendMultipleMessage(self):
        self.nsadminHelper.configureGateway('HIGH', 'cardboardfishmock')
        self.nsadminHelper.configureGateway('BULK', 'valuefirstmock')
        mobile1 = randValues.getRandomMobileNumber()
        mobile2 = randValues.getRandomMobileNumber()
        mobile3 = randValues.getRandomMobileNumber()
        params = [
            [0, "BULK",  "test message 1", mobile1],
            [1, "BULK",  "test message 2", mobile2],
            [2, "HIGH",  "test message 3", mobile3]
        ]
        msgObjList = []
        for p in params:
            msgObj = NSAdminObject.message({"messageClass" : "SMS", "inboxId" : p[0], "priority" : p[1], "message" : p[2], "receiver" : p[3]})
            msgObjList.append(msgObj)
        resp = self.nsObj.sendMultipleMessages(msgObjList)
        for i in range(0, 3):
            msgId = resp[i]
            msgResp = self.nsObj.getMessagesById([msgId])[0]
            #inboxId = msgResp.inboxId
            msgParams = params[i]
            Assertion.constructAssertion(msgResp.status in ['RECEIVED_IN_QUEUE', 'SENT'], 'Messages status')
            Assertion.constructAssertion(msgResp.priority == msgParams[1], 'Messages priority')
            Assertion.constructAssertion(msgResp.message == msgParams[2], 'Message')
            Assertion.constructAssertion(msgResp.receiver == msgParams[3], 'Messages receiver')
        msg1 = self.nsObj.getMessagesByReceiver(self.orgId, mobile1)[0]
        msg2 = self.nsObj.getMessagesByReceiver(self.orgId, mobile2)[0]
        Assertion.constructAssertion(msg1.message == 'test message 1', 'getMessagesByReceiver Message')
        Assertion.constructAssertion(msg2.message == 'test message 2', 'getMessagesByReceiver Message')



    def test_sendMultipleMessageWithBulkGateway(self):
        self.nsadminHelper.configureGateway('BULK', 'valuefirstmock')
        params = [
            [0, "BULK",  "test message 1", randValues.getRandomMobileNumber(), ['RECEIVED_IN_QUEUE', 'SENT']],
            #[1, "BULK",  "test message 2", randValues.getRandomMobileNumber(), ['RECEIVED_IN_QUEUE', 'SENT']],
            #[2, "HIGH",  "test message 3", randValues.getRandomMobileNumber(), ['GTW_NOT_FOUND']]
        ]
        msgObjList = []
        for p in params:
            msgObj = NSAdminObject.message({"messageClass" : "SMS", "inboxId" : p[0], "priority" : p[1], "message" : p[2], "receiver" : p[3]})
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


    def test_SMScharLimit(self):
        self.nsadminHelper.configureGateway('HIGH', 'cardboardfishmock')
        message160CharSize = "At Capillary, we continuously work to help our clients succeed in rapidly evolving markets through our world-class solutions, services and products -  combining"
        msgDict = {"messageClass" : "SMS", "priority" : "HIGH", 
        "message" : message160CharSize}
        resp  = self.nsadminHelper.createAndSendMessage(msgDict)
        currentMonthTable = NSAdminHelper.getTableName()
        query = 'select status, message_count, message from '+currentMonthTable+' where id='+str(resp)
        resp = dbHelper.queryDB(query, 'nsadmin')
        Assertion.constructAssertion(resp[0][0] in [7, 35], 'Messages status')
        Assertion.constructAssertion(resp[0][2] == message160CharSize, '160 Char limit')
        Assertion.constructAssertion(resp[0][1] == 1, 'Message count')

        message320CharSize = "At Capillary, we continuously work to help our clients succeed in rapidly evolving markets through our world-class solutions, services and products. By combining big data with a robust, cloud-based analytics engine, we optimize the relevance and profitability of discounts and personalized offers to consumers in real time, significantly increasing both loyalty and sales"
        msgDict = {"messageClass" : "SMS", "priority" : "HIGH", 
        "message" : message320CharSize}
        resp  = self.nsadminHelper.createAndSendMessage(msgDict)
        currentMonthTable = NSAdminHelper.getTableName()
        query = 'select status, message_count, message from '+currentMonthTable+' where id='+str(resp)
        resp = dbHelper.queryDB(query, 'nsadmin')
        Assertion.constructAssertion(resp[0][0] in [7, 35], 'Messages status')
        Assertion.constructAssertion(resp[0][1] == 1, 'Message count without truncate')  

        msgDict = {"messageClass" : "SMS", "priority" : "HIGH", "truncate": False,
        "message" : message320CharSize}
        resp  = self.nsadminHelper.createAndSendMessage(msgDict)
        currentMonthTable = NSAdminHelper.getTableName()
        query = 'select status, message_count, message from '+currentMonthTable+' where id='+str(resp)
        resp = dbHelper.queryDB(query, 'nsadmin')
        Assertion.constructAssertion(resp[0][0] in [7, 35], 'Messages status')
        Assertion.constructAssertion(resp[0][2] == message320CharSize, '320 Char limit')
        Assertion.constructAssertion(resp[0][1] == 3, 'Message count')        

    def test_SMSCharUTF8(self):
        self.nsadminHelper.configureGateway('HIGH', 'cardboardfishmock')
        messageArabic = "في شعري ، ونحن نعملمجمو باستمرار لمساعدة العملاء على تحقيق النجاح في الأسواق المتطورة بسرعة من خلال حلول عالمية"
        msgDict = {"messageClass" : "SMS", "priority" : "HIGH", "truncate":False,
        "message" : messageArabic}
        resp  = self.nsadminHelper.createAndSendMessage(msgDict)
        currentMonthTable = NSAdminHelper.getTableName()
        query = 'select status, message_count, message from '+currentMonthTable+' where id='+str(resp)
        resp = dbHelper.queryDB(query, 'nsadmin')
        Assertion.constructAssertion(resp[0][0] in [7, 35], 'Messages status')
        Assertion.constructAssertion(resp[0][2].encode('utf8') == messageArabic, 'Arabic Char')
        Assertion.constructAssertion(resp[0][1] == 2, 'Message count') 

        messageChinese = "在毛細管中，我們不斷努力，以幫助我們的客戶通過我們的世界級解決方案，服務和產品成功在快速發展的市場 - 將合併在毛細管中，我們不斷努力，以以- 將合併在毛細管中，我們不斷努力，以以"
        msgDict = {"messageClass" : "SMS", "priority" : "HIGH", "truncate": False,
        "message" : messageChinese}
        resp  = self.nsadminHelper.createAndSendMessage(msgDict)
        currentMonthTable = NSAdminHelper.getTableName()
        query = 'select status, message_count, message from '+currentMonthTable+' where id='+str(resp)
        resp = dbHelper.queryDB(query, 'nsadmin')
        Assertion.constructAssertion(resp[0][0] in [7, 35], 'Messages status')       
        Assertion.constructAssertion(resp[0][2].encode('utf8') == messageChinese, 'Chinese Char')
        Assertion.constructAssertion(resp[0][1] == 2, 'Message count')               


    @pytest.mark.parametrize('mobileNumber', [
                    ('917976762433'),
                    (randValues.getRandomMobileNumber())])
    def est_ratelimit(self, mobileNumber): # Same number if used will timeout within 24hrs # to be fixed
        self.nsadminHelper.configureGateway('BULK', 'valuefirstmock')        
        msgObjList = []
        for i in range(1, 10):
            msgObj = NSAdminObject.message({"messageClass" : "SMS", "inboxId" : i ,"clientId":113,
                "priority" : "BULK", "message" : "test message "+str(i), "receiver" : mobileNumber})
            msgObjList.append(msgObj)
        self.nsObj.sendMultipleMessages(msgObjList)
        msgObj = NSAdminObject.message({"messageClass" : "SMS", "inboxId" : 10 ,"clientId":113,
        "priority" : "BULK", "message" : "test message 10", "receiver" : mobileNumber})
        nsadminId = self.nsObj.sendMessage(msgObj)
        resp = self.nsadminHelper.waitUntil(nsadminId, ['SENT'])
        if resp:
            Assertion.constructAssertion(resp.requestId != '', 'msg_ref_id is not generated')
        else:
            Assertion.constructAssertion(False, 'Failed to get status SENT')
        msgObj = NSAdminObject.message({"messageClass" : "SMS", "inboxId" : 11,"clientId":113,
        "priority" : "BULK", "message" : "test message 11", "receiver" : mobileNumber})
        nsadminId = self.nsObj.sendMessage(msgObj)
        resp = self.nsadminHelper.waitUntil(nsadminId, ['RATE_LIMIT_EXCEEDED'])
        if resp:
            Assertion.constructAssertion(resp.requestId == '', 'msg_ref_id is generated')
        else:
            Assertion.constructAssertion(False, 'Failed to get status RATE_LIMIT_EXCEEDED')


    def test_getMessagesByUserOrReciever(self):
        mobile = randValues.getRandomMobileNumber()
        testMessage = "test message new"
        msgObj = NSAdminObject.message({"messageClass" : "SMS", "inboxId" : 1, 
        "priority" : "BULK", "message" : testMessage, "receiver" : mobile})
        nsadminId = self.nsObj.sendMessage(msgObj)
        resp = self.nsObj.getMessagesByReceiver(self.orgId, mobile)
        Assertion.constructAssertion(resp[0].message == testMessage, 'getMessagesByReceiver response')
        resp = self.nsObj.getMessagesByUserOrReciever(self.orgId, '', mobile)
        Assertion.constructAssertion(resp[0].message == testMessage, 'getMessagesByUserOrReciever response')


    @pytest.mark.parametrize('priority, gateway', [
                    ('HIGH', 'cardboardfishmock'),
                    ('BULK', 'valuefirstmock')])        
    def test_sendMessage_with_DomainGatewayMapID(self, priority, gateway):
        self.nsadminHelper.configureGateway(priority, gateway)
        dpgmId = self.nsadminHelper.getDomainGatewayMapId(gateway)
        msgDict = {"messageClass" : "SMS", 
                "priority" : priority, "message" : "test message with priority "+priority,
                "additionalHeaders" : {"domain_gateway_map_id": str(dpgmId)}}
        msgId = self.nsadminHelper.createAndSendMessage(msgDict)
        resp = self.nsadminHelper.assertWithWaitUntil(msgId, ['RECEIVED_IN_QUEUE', 'SENT'], 'Messages status ACK', 10)
        Assertion.constructAssertion(resp.gateway == gateway, 'gateway used for  sending')
        Assertion.constructAssertion(resp.priority == priority, 'priority')


    @pytest.mark.parametrize('priority, gateway', [
                    ('HIGH', 'cardboardfishmock'),
                    ('BULK', 'valuefirstmock')])        
    def test_sendMessage_with_InvalidDomainGatewayMapID(self, priority, gateway):
        self.nsadminHelper.configureGateway(priority, gateway)
        dpgmId = self.nsadminHelper.getDomainGatewayMapId(gateway)
        msgDict = {"messageClass" : "SMS", 
                "priority" : priority, "message" : "test message with priority "+priority,
                "additionalHeaders" : {"domain_gateway_map_id": "1"}}
        msgId = self.nsadminHelper.createAndSendMessage(msgDict)
        self.nsadminHelper.assertWithWaitUntil(msgId, ['GTW_NOT_FOUND'], 'Messages status', 10)

    @pytest.mark.parametrize('priority, gateway', [
                    ('HIGH', 'cardboardfishmock'),
                    ('BULK', 'valuefirstmock')])        
    def test_sendMessage_with_DomainID(self, priority, gateway):
        domainId = self.nsadminHelper.addDefaultDomain()
        self.nsadminHelper.configureGateway(priority, gateway)
        msgDict = {"messageClass" : "SMS", 
                "priority" : priority, "message" : "test message with priority "+priority,
                "additionalHeaders" : {"domain_prop_id": str(domainId)}}
        msgId = self.nsadminHelper.createAndSendMessage(msgDict)
        resp = self.nsadminHelper.assertWithWaitUntil(msgId, ['RECEIVED_IN_QUEUE', 'SENT'], 'Messages status ACK', 10)
        Assertion.constructAssertion(resp.gateway == gateway, 'gateway used for  sending')
        Assertion.constructAssertion(resp.priority == priority, 'priority')

    @pytest.mark.parametrize('priority, gateway', [
                    ('HIGH', 'cardboardfishmock'),
                    ('BULK', 'valuefirstmock')])        
    def test_sendMessage_with_InvalidDomainID(self, priority, gateway):
        domainId = self.nsadminHelper.addDefaultDomain()
        self.nsadminHelper.configureGateway(priority, gateway)
        msgDict = {"messageClass" : "SMS", 
                "priority" : priority, "message" : "test message with priority "+priority,
                "additionalHeaders" : {"domain_prop_id": "1"}}
        msgId = self.nsadminHelper.createAndSendMessage(msgDict)
        self.nsadminHelper.assertWithWaitUntil(msgId, ['GTW_NOT_FOUND'], 'Messages status', 10)


    @pytest.mark.parametrize('priority, gateway, status', [
                    ('HIGH', 'cardboardfishmock', ['RECEIVED_IN_QUEUE', 'SENT']),
                    ('BULK', 'valuefirstmock', ['MOBILE_WHITELISTED_BLOCKED'])]) 
    def test_sendMessage_smsWhitelisting(self, priority, gateway, status):
        mobile = '919980142462'
        last_failed_on = datetime.now()
        DarknightHelper.getMongoConnection('whitelisting', 'mobile_status')
        domainId = self.nsadminHelper.addDefaultDomain()
        DarknightHelper.generateSmsWhitelistingData(
                {'not_delivered' : 4, 'last_failed_on' : last_failed_on, 
                "monthly_stats": [{"year": last_failed_on.year, "month": last_failed_on.month, 
                "not_delivered": 4, "total": 4}]}, mobile)        
        self.nsadminHelper.configureGateway(priority, gateway)
        msgDict = {"messageClass" : "SMS", 'receiver' : mobile,
                "priority" : priority, "message" : "test message with is_whitelisting_enabled "+priority,
                "additionalHeaders" : {"is_whitelisting_enabled": "true"}}
        msgId1  = self.nsadminHelper.createAndSendMessage(msgDict)
        msgDict = {"messageClass" : "SMS", 'receiver' : mobile,
                "priority" : priority, "message" : "test message with is_whitelisting_enabled false"+priority,
                "additionalHeaders" : {"is_whitelisting_enabled": "false"}}
        msgId2  = self.nsadminHelper.createAndSendMessage(msgDict)
        self.nsadminHelper.assertWithWaitUntil(msgId1, status, 'Messages status ACK', 10)
        self.nsadminHelper.assertWithWaitUntil(msgId2, ['RECEIVED_IN_QUEUE', 'SENT'], 'Messages status ACK', 10)


    #### Prod ###
    @pytest.mark.parametrize('priority, gateway', [
                    ('HIGH', 'solutionsinfinitrans'),
                    ('BULK', 'solutionsinfinibulk_BULK')])        
    def test_sendMessage_SMS_UseSystemDefaultsGateway_India_More_Prod_Sanity(self, priority, gateway):
        self.nsadminHelper.configureGateway(priority, gateway)
        msgDict = {"messageClass" : "SMS", "receiver" : constant.config['prodMobile1'], "priority" : priority, 
            "message" : "test message priority "+priority+" cluster:"+self.cluster}
        msgObj = NSAdminObject.message(msgDict)
        msgId = self.nsObj.sendMessage(msgObj)
        resp = self.nsadminHelper.assertWithWaitUntil(msgId, ['RECEIVED_IN_QUEUE', 'SENT'], 'Messages status ACK', 10)
        Assertion.constructAssertion(resp.gateway == gateway, 'gateway used for sending')
        Assertion.constructAssertion(resp.priority == priority, 'priority')

    @pytest.mark.parametrize('priority, gateway, username, tags', [
                    ('HIGH', 'puxuntrans', '7171', ['transaction', 'otp']),
                    ('BULK', 'puxunbulk', '7174', ['campaign'])]) 
    def test_sendMessage_SMS_China_Prod_Sanity(self, priority, gateway, username, tags):
        domainPropertiesId = self.nsadminHelper.addDefaultDomain()
        orgName = constant.config['orgName']
        shortName = orgName+gateway
        connectionProperties = json.dumps({
            "account":username,
            "apiKey":"203dfd2c4eb6f8eed0889bef5d7aa646",
            "factory": gateway,
            "dlrUrl": constant.config['dlrUrl']+gateway
        })
        properties = json.dumps({
            "scopes": tags,
            "countries":["86"]
        })
        gatewayOrgConfigs = {
            "orgId": self.orgId,
            "hostName": gateway,
            "shortName": shortName,
            "fullName": shortName,
            "username": username,
            "password": "lfhg@2587",
            "connectionProperties": connectionProperties,
            "serviceIp": "",
            "serviceUrl": "http://202.91.244.252:30001/yqx/v1/sms/multi_send",
            "statusCheckUrl": "http://202.91.244.252:30001/yqx/v1/sms/multi_send",
            "messageClass": "SMS",
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
        msgDict = {"messageClass" : "SMS", "receiver" : constant.config['prodMobile3'], "priority" : priority, 
            "message" : "test message priority "+priority+" cluster:"+self.cluster}
        msgObj = NSAdminObject.message(msgDict)
        msgId = self.nsObj.sendMessage(msgObj)
        resp = self.nsadminHelper.assertWithWaitUntil(msgId, ['RECEIVED_IN_QUEUE', 'SENT', 'DELIVERED'], 'Messages status ACK', 10)
        Assertion.constructAssertion(resp.gateway == shortName, 'gateway used for sending')
        Assertion.constructAssertion(resp.priority == priority, 'priority')


    @pytest.mark.parametrize('priority, gateway ,tags',[
                    ('HIGH', 'solutionsinfiniTrans', ['transaction', 'otp']),
                    ('BULK', 'solutionsinfiniBulk', ['campaign'])]) 
    def test_sendMessage_SMS_Eu_Prod_Sanity(self, priority, gateway, tags):
        domainPropertiesId = self.nsadminHelper.addDefaultDomain()
        orgName = constant.config['orgName']
        shortName = orgName+gateway
        connectionProperties = json.dumps({
            "dlrUrl": constant.config['dlrUrl']+'solutionsinfini'
        })
        properties = json.dumps({
            "scopes": tags,
            "countries":["44"]
        })
        gatewayOrgConfigs = {
            "orgId": self.orgId,
            "hostName": "solutionsinfini",
            "shortName": shortName,
            "fullName": shortName,
            "username": "capintl",
            "password": "gU89a",
            "connectionProperties": connectionProperties,
            "serviceIp": "",
            "serviceUrl": "http://global.sinfini.com/api/v0/xmlapi.php",
            "statusCheckUrl": "http://global.sinfini.com/api/v0/xmlapi.php",
            "messageClass": "SMS",
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
        msgDict = {"messageClass" : "SMS", "receiver" : constant.config['prodMobile4'], "priority" : priority, 
            "message" : "test message priority "+priority+" cluster:"+self.cluster}
        msgObj = NSAdminObject.message(msgDict)
        msgId = self.nsObj.sendMessage(msgObj)
        resp = self.nsadminHelper.assertWithWaitUntil(msgId, ['RECEIVED_IN_QUEUE', 'SENT', 'DELIVERED'], 'Messages status', 10)
        Assertion.constructAssertion(resp.gateway == shortName, 'gateway used for sending')
        Assertion.constructAssertion(resp.priority == priority, 'priority')







