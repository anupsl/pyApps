import pytest, time

from src.Constant.constant import constant
from src.utilities.logger import Logger
from src.modules.nsadmin.nsadminObject import NSAdminObject
from src.modules.nsadmin.nsadminHelper import NSAdminHelper
from src.utilities.assertion import Assertion
from src.utilities.randValues import randValues
from src.utilities.dbhelper import dbHelper
from src.modules.nsadmin.deliveryReceipt import DeliveryReceipt
from src.utilities.utils import Utils


class Test_DeliveryReceipt_SMS():      

    def setup_class(self):
        Logger.logSuiteName(str(self).split('.')[-1])
        self.orgId = constant.config['orgId']
        self.cluster = constant.config['cluster']
        self.nsObj = NSAdminHelper.getConnObj(newConnection=True)
        self.nsadminHelper = NSAdminHelper(self.orgId, 'SMS')
        self.nsadminHelper.disableDomainPropertiesGatewayMap()
        self.nsadminHelper.configureGateway('HIGH', 'cardboardfishmock')
        self.nsadminHelper.configureGateway('BULK', 'valuefirstmock')
        self.DR = DeliveryReceipt()

    def setup_method(self, method):      
        Logger.logMethodName(method.__name__)


    @pytest.mark.parametrize('priority', [('HIGH'),('BULK')])      
    def test_sendMessage_Delivered(self, priority):
        msgDict = {"messageClass" : "SMS", "priority" : priority, "message" : "test message with priority "+priority}
        msgId  = self.nsadminHelper.createAndSendMessage(msgDict)
        Assertion.constructAssertion(type(msgId) == int, 'sendMessage output')
        self.nsadminHelper.assertWithWaitUntil(msgId, ['RECEIVED_IN_QUEUE', 'SENT'], 'Messages status ACK', 10)
        deliveredTime = Utils.getTime(dateTimeFormat=True)
        data = {"delivered_time": deliveredTime, "msgid": str(msgId), "status":"DELIVRD"}
        self.DR.solutionsinfini(data)
        self.nsadminHelper.assertWithWaitUntil(msgId, ['DELIVERED'], 'Messages status after DLR update', 10)
        resp = self.nsObj.isMessageDelivered(msgId)
        Assertion.constructAssertion(resp == True, 'isMessageDelivered response')
        

    def test_sendMessage_PartialResponse_To_DELIVERED(self):
        msgDict = {"messageClass" : "SMS", "priority" : 'HIGH', "message" : "test message for DLR"}
        msgId  = self.nsadminHelper.createAndSendMessage(msgDict)
        self.nsadminHelper.assertWithWaitUntil(msgId, ['RECEIVED_IN_QUEUE', 'SENT'], 'Messages status ACK', 10)
        deliveredTime = Utils.getTime(dateTimeFormat=True)
        data = {"delivered_time": deliveredTime, "msgid": str(msgId), "status":"UNDELIV"}
        self.DR.solutionsinfini(data)
        self.nsadminHelper.assertWithWaitUntil(msgId, ['NOT_DELIVERED'], 'Messages status after DLR update', 10)
        resp = self.nsObj.isMessageDelivered(msgId)
        Assertion.constructAssertion(resp == False, 'isMessageDelivered response')

    def test_sendMessage_NOT_DELIVERED_To_DELIVERED(self):
        msgDict = {"messageClass" : "SMS", "priority" : 'HIGH', "message" : "test message for DLR"}
        msgId  = self.nsadminHelper.createAndSendMessage(msgDict)
        self.nsadminHelper.assertWithWaitUntil(msgId, ['RECEIVED_IN_QUEUE', 'SENT'], 'Messages status ACK', 10)
        deliveredTime = Utils.getTime(dateTimeFormat=True)
        data = {"delivered_time": deliveredTime, "msgid": str(msgId), "status":"UNDELIV"}
        self.DR.solutionsinfini(data)
        self.nsadminHelper.assertWithWaitUntil(msgId, ['NOT_DELIVERED'], 'Messages status after DLR update', 10)
        deliveredTime = Utils.getTime(dateTimeFormat=True)
        data = {"delivered_time": deliveredTime, "msgid": str(msgId), "status":"DELIVRD"}
        self.DR.solutionsinfini(data)
        self.nsadminHelper.assertWithWaitUntil(msgId, ['DELIVERED'], 'Messages status after DLR update', 10)
        
    def test_sendMessage_DELIVERED_To_NOT_DELIVERED(self):
        msgDict = {"messageClass" : "SMS", "priority" : 'HIGH', "message" : "test message for DLR"}
        msgId  = self.nsadminHelper.createAndSendMessage(msgDict)
        self.nsadminHelper.assertWithWaitUntil(msgId, ['RECEIVED_IN_QUEUE', 'SENT'], 'Messages status ACK', 10)
        deliveredTime = Utils.getTime(dateTimeFormat=True)
        data = {"delivered_time": deliveredTime, "msgid": str(msgId), "status":"DELIVRD"}
        self.DR.solutionsinfini(data)
        self.nsadminHelper.assertWithWaitUntil(msgId, ['DELIVERED'], 'Messages status after DLR update', 10)
        deliveredTime = Utils.getTime(dateTimeFormat=True)
        data = {"delivered_time": deliveredTime, "msgid": str(msgId), "status":"UNDELIV"}
        self.DR.solutionsinfini(data)
        self.nsadminHelper.assertWithWaitUntil(msgId, ['DELIVERED'], 'Messages status after DLR update', 10)
        
        
    def test_sendMessage_InvalidDLR(self):
        msgDict = {"messageClass" : "SMS", "priority" : 'HIGH', "message" : "test message for DLR"}
        msgId  = self.nsadminHelper.createAndSendMessage(msgDict)
        self.nsadminHelper.assertWithWaitUntil(msgId, ['RECEIVED_IN_QUEUE', 'SENT'], 'Messages status ACK', 10)
        deliveredTime = Utils.getTime(dateTimeFormat=True)
        data = {"delivered_time": deliveredTime, "msgid": str(msgId), "status":"INVALID"}
        self.DR.solutionsinfini(data)
        self.nsadminHelper.assertWithWaitUntil(msgId, ['NOT_DELIVERED'], 'Messages status after DLR update', 10)

    def test_sendMessage_TIMEOUT(self):
        msgDict = {"messageClass" : "SMS", "priority" : 'HIGH', "message" : "SLEEP91"}
        msgId  = self.nsadminHelper.createAndSendMessage(msgDict)
        Assertion.constructAssertion(type(msgId) == int, 'sendMessage output')
        Utils.sleep(95)
        self.nsadminHelper.assertWithWaitUntil(msgId, ['TIMEOUT'], 'Messages status ACK', 10)

    def test_sendMessage_TIMEOUT_To_DELIVERED(self):
        msgDict = {"messageClass" : "SMS", "priority" : 'HIGH', "message" : "SLEEP91"}
        msgId  = self.nsadminHelper.createAndSendMessage(msgDict)
        Assertion.constructAssertion(type(msgId) == int, 'sendMessage output')
        Utils.sleep(95)
        self.nsadminHelper.assertWithWaitUntil(msgId, ['TIMEOUT'], 'Messages status ACK', 10)
        deliveredTime = Utils.getTime(dateTimeFormat=True)
        data = {"delivered_time": deliveredTime, "msgid": str(msgId), "status":"DELIVRD"}
        self.DR.solutionsinfini(data)
        self.nsadminHelper.assertWithWaitUntil(msgId, ['DELIVERED'], 'Messages status after DLR update', 10)

    def test_sendMessage_PARTIAL_RESPONSE(self):
        msgDict = {"messageClass" : "SMS", "priority" : 'HIGH', "message" : "PARTIAL_RESPONSE"}
        msgId  = self.nsadminHelper.createAndSendMessage(msgDict)
        Assertion.constructAssertion(type(msgId) == int, 'sendMessage output')
        Utils.sleep(5)
        self.nsadminHelper.assertWithWaitUntil(msgId, ['PARTIAL_RESPONSE'], 'Messages status ACK', 10)

    def test_sendMessage_PARTIAL_RESPONSE_To_DELIVERED(self):
        msgDict = {"messageClass" : "SMS", "priority" : 'HIGH', "message" : "PARTIAL_RESPONSE"}
        msgId  = self.nsadminHelper.createAndSendMessage(msgDict)
        Assertion.constructAssertion(type(msgId) == int, 'sendMessage output')
        Utils.sleep(5)
        self.nsadminHelper.assertWithWaitUntil(msgId, ['PARTIAL_RESPONSE'], 'Messages status ACK', 10)
        deliveredTime = Utils.getTime(dateTimeFormat=True)
        data = {"delivered_time": deliveredTime, "msgid": str(msgId), "status":"DELIVRD"}
        self.DR.solutionsinfini(data)
        self.nsadminHelper.assertWithWaitUntil(msgId, ['DELIVERED'], 'Messages status after DLR update', 10)
        
    def test_sendMessage_GatewayDelay(self):
        msgDict = {"messageClass" : "SMS", "priority" : 'HIGH', "message" : "SLEEP21"}
        msgId  = self.nsadminHelper.createAndSendMessage(msgDict)
        Assertion.constructAssertion(type(msgId) == int, 'sendMessage output')
        Utils.sleep(5)
        self.nsadminHelper.assertWithWaitUntil(msgId, ['RECEIVED_IN_QUEUE', 'SENT'], 'Messages status ACK', 10)
        Utils.sleep(20)
        deliveredTime = Utils.getTime(dateTimeFormat=True)
        data = {"delivered_time": deliveredTime, "msgid": str(msgId), "status":"DELIVRD"}
        self.DR.solutionsinfini(data)
        self.nsadminHelper.assertWithWaitUntil(msgId, ['DELIVERED'], 'Messages status after DLR update', 10)

    def test_sendMessage_DELAYED_SCHEDULED_To_DELIVERED(self):
        scheduledTimestamp = int(time.time() + 180) * 1000 # 3 mins delay
        msgDict = {"messageClass" : "SMS", "priority" : 'HIGH', 
        "scheduledTimestamp" : scheduledTimestamp, "message" : "test message for DLR"}
        msgId  = self.nsadminHelper.createAndSendMessage(msgDict)
        self.nsadminHelper.assertWithWaitUntil(msgId, ['DELAYED_SCHEDULED'], 'Messages status DELAYED_SCHEDULED', 10)
        Utils.sleep(185)
        self.nsadminHelper.assertWithWaitUntil(msgId, ['RECEIVED_IN_QUEUE', 'SENT', 'READ'], 'Messages status ACK', 10)
        deliveredTime = Utils.getTime(dateTimeFormat=True)
        data = {"delivered_time": deliveredTime, "msgid": str(msgId), "status":"DELIVRD"}
        self.DR.solutionsinfini(data)
        self.nsadminHelper.assertWithWaitUntil(msgId, ['DELIVERED'], 'Messages status after DLR update', 10)
        

    def test_DLR_Endpoints(self):
        endpoints = [
            'airtelbulk',
            'bizup',
            'bouncedemail',
            'descentebulk',
            'descentetrans',
            'falconide',
            'gmtsms',
            'gupshupxml',
            'harleydavidsonbulk',
            'icsxml',
            'infoblip',
            'ismartbulk',
            'mailchimp',
            'netcore',
            'octane',
            'onewaysms',
            'ooredoobulk',
            'ooredootrans',
            'plivobulk',
            'plivotrans',
            'puxunbulk',
            'puxuntrans',
            'qxun/broadcast',
            'qxun/template',
            'redirectedreceipts',
            'routemobilebulk',
            'routemobilenewbulk',
            'sendgrid',
            'silverstreetbulk',
            'silverstreettrans',
            'solutionsbulk',
            'solutionsinfini',
            'solutionstrans',
            'sslpushbulk',
            'sslpushtrans',
            "timestrans",
            "timesbulk",
            'tbpbulksms',
            'tbptranssms',
            'tbpvoicecall',
            'tingli/report',
            'tobeprecisebulk',
            'tobeprecisehttp',
            'unicell',
            'valuefirst',
            'vectramind',
            'vectramindbulkupgrade',
            'vectramindtransupgrade',
            'wecrm/template'
        ]
        for hostName in endpoints:
            r = self.DR.testEndpoint(hostName)
            if r.status_code != 200:
                Assertion.constructAssertion(r.status_code == 200, 'Endpoint response for '+hostName)
        Assertion.constructAssertion(1, 'Verified all the endpoints response')
