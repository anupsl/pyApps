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



class Test_DeliveryReceipt_EMAIL():      

    def setup_class(self):
        Logger.logSuiteName(str(self).split('.')[-1])
        self.orgId = constant.config['orgId']
        self.cluster = constant.config['cluster']
        self.nsObj = NSAdminHelper.getConnObj(newConnection=True)
        self.nsadminHelper = NSAdminHelper(self.orgId, 'EMAIL')
        self.nsadminHelper.disableDomainPropertiesGatewayMap()
        self.nsadminHelper.configureGateway('HIGH', 'sendgrid_HIGH')
        self.nsadminHelper.configureGateway('BULK', 'sendgrid_BULK')
        self.DR = DeliveryReceipt()
        self.msgDict = {"messageClass" : "EMAIL", "priority" : 'HIGH', "message" : "test message for DLR"}

    def setup_method(self, method):      
        Logger.logMethodName(method.__name__)

    def getSendGridPayload(self, msgId, event):
        payload = {"event": event, "timestamp": Utils.getTime(), "oid": str(self.orgId), 
                "nid": str(msgId), "email": "test@capillarytech.com", "cluster": "localcluster", 
                "iid": "-1", "cid": "-1"}
        if event == 'DEFERRED':
            payload['response'] = ""
        if event == 'DROPPED':
            payload['reason'] = ""
        return payload

    @pytest.mark.parametrize('priority', [('HIGH'),('BULK')])
    def test_sendMessage_Delivered(self, priority):
        msgDict = {"messageClass" : "EMAIL", "priority" : priority, "message" : "test message for DLR"}
        msgId  = self.nsadminHelper.createAndSendMessage(msgDict)
        self.nsadminHelper.assertWithWaitUntil(msgId, ['RECEIVED_IN_QUEUE', 'SENT'], 'Messages status after ACK', 10)
        data = [self.getSendGridPayload(msgId, 'DELIVERED')]
        self.DR.sendgrid(data)
        self.nsadminHelper.assertWithWaitUntil(msgId, ['DELIVERED'], 'Messages status after DLR update', 10)


    def test_sendMessage_NotDelivered(self):
        msgId  = self.nsadminHelper.createAndSendMessage(self.msgDict)
        self.nsadminHelper.assertWithWaitUntil(msgId, ['RECEIVED_IN_QUEUE', 'SENT'], 'Messages status after ACK', 10)
        data = [self.getSendGridPayload(msgId, 'DROPPED')]
        self.DR.sendgrid(data)
        self.nsadminHelper.assertWithWaitUntil(msgId, ['NOT_DELIVERED'], 'Messages status after DLR update', 10)
        resp = self.nsObj.isMessageDelivered(msgId)
        Assertion.constructAssertion(resp == False, 'isMessageDelivered response')

    def test_sendMessage_PROCESSED(self):
        msgId  = self.nsadminHelper.createAndSendMessage(self.msgDict)
        self.nsadminHelper.assertWithWaitUntil(msgId, ['RECEIVED_IN_QUEUE', 'SENT'], 'Messages status after ACK', 10)
        data = [self.getSendGridPayload(msgId, 'PROCESSED')]
        self.DR.sendgrid(data)
        self.nsadminHelper.assertWithWaitUntil(msgId, ['GTW_PROCESSED'], 'Messages status after DLR update', 10)

    def test_sendMessage_IN_GTW(self):
        msgId  = self.nsadminHelper.createAndSendMessage(self.msgDict)
        self.nsadminHelper.assertWithWaitUntil(msgId, ['RECEIVED_IN_QUEUE', 'SENT'], 'Messages status after ACK', 10)
        data = [self.getSendGridPayload(msgId, 'DEFERRED')]
        self.DR.sendgrid(data)
        self.nsadminHelper.assertWithWaitUntil(msgId, ['IN_GTW'], 'Messages status after DLR update', 10)

    def test_sendMessage_OPEN(self):
        msgId  = self.nsadminHelper.createAndSendMessage(self.msgDict)
        self.nsadminHelper.assertWithWaitUntil(msgId, ['RECEIVED_IN_QUEUE', 'SENT'], 'Messages status after ACK', 10)
        data = [self.getSendGridPayload(msgId, 'OPEN')]
        self.DR.sendgrid(data)
        self.nsadminHelper.assertWithWaitUntil(msgId, ['OPENED'], 'Messages status after DLR update', 10)

    def test_sendMessage_CLICK(self):
        msgId  = self.nsadminHelper.createAndSendMessage(self.msgDict)
        self.nsadminHelper.assertWithWaitUntil(msgId, ['RECEIVED_IN_QUEUE', 'SENT'], 'Messages status after ACK', 10)
        data = [self.getSendGridPayload(msgId, 'CLICK')]
        self.DR.sendgrid(data)
        self.nsadminHelper.assertWithWaitUntil(msgId, ['CLICKED'], 'Messages status after DLR update', 10)

    def test_sendMessage_MARKED_SPAM(self):
        msgId  = self.nsadminHelper.createAndSendMessage(self.msgDict)
        self.nsadminHelper.assertWithWaitUntil(msgId, ['RECEIVED_IN_QUEUE', 'SENT'], 'Messages status after ACK', 10)
        data = [self.getSendGridPayload(msgId, 'SPAMREPORT')]
        self.DR.sendgrid(data)
        self.nsadminHelper.assertWithWaitUntil(msgId, ['MARKED_SPAM'], 'Messages status after DLR update', 10)

    def test_sendMessage_UNSUBSCRIBE(self):
        msgId  = self.nsadminHelper.createAndSendMessage(self.msgDict)
        self.nsadminHelper.assertWithWaitUntil(msgId, ['RECEIVED_IN_QUEUE', 'SENT'], 'Messages status after ACK', 10)        
        data = [self.getSendGridPayload(msgId, 'UNSUBSCRIBE')]
        self.DR.sendgrid(data)
        self.nsadminHelper.assertWithWaitUntil(msgId, ['NOT_DELIVERED'], 'Messages status after DLR update', 10)


    def test_sendMessage_DELAYED_SCHEDULED_To_DELIVERED(self):
        scheduledTimestamp = int(time.time() + 180) * 1000 # 3 mins delay
        msgDict = {"messageClass" : "EMAIL", "priority" : 'HIGH', 
        "scheduledTimestamp" : scheduledTimestamp, "message" : "test message for DLR"}
        msgId  = self.nsadminHelper.createAndSendMessage(msgDict)
        self.nsadminHelper.assertWithWaitUntil(msgId, ['DELAYED_SCHEDULED'], 'Messages status DELAYED_SCHEDULED', 10)
        Utils.sleep(185)
        self.nsadminHelper.assertWithWaitUntil(msgId, ['RECEIVED_IN_QUEUE', 'SENT'], 'Messages status ACK', 10)
        data = [self.getSendGridPayload(msgId, 'DELIVERED')]
        self.DR.sendgrid(data)
        self.nsadminHelper.assertWithWaitUntil(msgId, ['DELIVERED'], 'Messages status after DLR update', 10)


    def test_sendMessage_Batch(self):
        msgId1  = self.nsadminHelper.createAndSendMessage(self.msgDict)
        self.nsadminHelper.assertWithWaitUntil(msgId1, ['RECEIVED_IN_QUEUE', 'SENT'], 'Messages status after ACK', 10)
        msgId2  = self.nsadminHelper.createAndSendMessage(self.msgDict)
        data = [self.getSendGridPayload(msgId1, 'DELIVERED'),
                self.getSendGridPayload(msgId2, 'DROPPED')
            ]
        self.DR.sendgrid(data)
        self.nsadminHelper.assertWithWaitUntil(msgId1, ['DELIVERED'], 'Messages status after DLR update', 10)
        self.nsadminHelper.assertWithWaitUntil(msgId2, ['NOT_DELIVERED'], 'Messages status after DLR update', 10)


    def test_sendMessage_GTWPROCESSED_INGWT_DELIVERED_OPEN_CLICK_MARKEDSPAM(self):
        msgId  = self.nsadminHelper.createAndSendMessage(self.msgDict)
        self.nsadminHelper.assertWithWaitUntil(msgId, ['RECEIVED_IN_QUEUE', 'SENT'], 'Messages status ACK', 10)
        statusDict = [
            ('PROCESSED', 'GTW_PROCESSED'), ('DEFERRED', 'IN_GTW'), ('DELIVERED', 'DELIVERED'), 
            ('OPEN', 'OPENED'), ('CLICK', 'CLICKED'), ('SPAMREPORT', 'MARKED_SPAM')]
        for event, status in statusDict:
            data = [self.getSendGridPayload(msgId, event)]
            self.DR.sendgrid(data)
            self.nsadminHelper.assertWithWaitUntil(msgId, [status], 'Messages status after DLR update', 10)

    def test_sendMessage_shouldNotUpdateAfter_INGWT(self):
        msgId  = self.nsadminHelper.createAndSendMessage(self.msgDict)
        self.nsadminHelper.assertWithWaitUntil(msgId, ['RECEIVED_IN_QUEUE', 'SENT'], 'Messages status ACK', 10)
        statusDict = [
                ('PROCESSED', 'GTW_PROCESSED'), ('DEFERRED', 'IN_GTW'), ('PROCESSED', 'IN_GTW')]
        for event, status in statusDict:
            data = [self.getSendGridPayload(msgId, event)]
            self.DR.sendgrid(data)
            self.nsadminHelper.assertWithWaitUntil(msgId, [status], 'Messages status after DLR update', 10)

    def test_sendMessage_shouldNotUpdateAfter_NOTDELIVERED(self):
        msgId  = self.nsadminHelper.createAndSendMessage(self.msgDict)
        self.nsadminHelper.assertWithWaitUntil(msgId, ['RECEIVED_IN_QUEUE', 'SENT'], 'Messages status ACK', 10)
        statusDict = [
            ('PROCESSED', 'GTW_PROCESSED'), ('DEFERRED', 'IN_GTW'), ('DROPPED', 'NOT_DELIVERED'), 
            ('PROCESSED', 'NOT_DELIVERED'), ('DEFERRED', 'NOT_DELIVERED')]
        for event, status in statusDict:
            data = [self.getSendGridPayload(msgId, event)]
            self.DR.sendgrid(data)
            self.nsadminHelper.assertWithWaitUntil(msgId, [status], 'Messages status after DLR update', 10)

    def test_sendMessage_shouldNotUpdateAfter_DELIVERED(self):
        msgId  = self.nsadminHelper.createAndSendMessage(self.msgDict)
        self.nsadminHelper.assertWithWaitUntil(msgId, ['RECEIVED_IN_QUEUE', 'SENT'], 'Messages status ACK', 10)
        statusDict = [
            ('PROCESSED', 'GTW_PROCESSED'), ('DEFERRED', 'IN_GTW'), ('DELIVERED', 'DELIVERED'), 
            ('PROCESSED', 'DELIVERED'), ('DEFERRED', 'DELIVERED')]
        for event, status in statusDict:
            data = [self.getSendGridPayload(msgId, event)]
            self.DR.sendgrid(data)
            self.nsadminHelper.assertWithWaitUntil(msgId, [status], 'Messages status after DLR update', 10)

    def test_sendMessage_shouldNotUpdateAfter_OPEN(self):
        msgId  = self.nsadminHelper.createAndSendMessage(self.msgDict)
        self.nsadminHelper.assertWithWaitUntil(msgId, ['RECEIVED_IN_QUEUE', 'SENT'], 'Messages status after ACK', 10)
        statusDict = [
            ('OPEN', 'OPENED'), ('PROCESSED', 'OPENED'), ('DEFERRED', 'OPENED'), 
            ('DELIVERED', 'OPENED'), ('DROPPED', 'OPENED')]
        for event, status in statusDict:
            data = [self.getSendGridPayload(msgId, event)]
            self.DR.sendgrid(data)
            self.nsadminHelper.assertWithWaitUntil(msgId, [status], 'Messages status after DLR update', 10)

