import pytest, time, json

from src.Constant.constant import constant
from src.utilities.logger import Logger
from src.modules.nsadmin.nsadminObject import NSAdminObject
from src.modules.nsadmin.nsadminHelper import NSAdminHelper
from src.utilities.assertion import Assertion
from src.utilities.randValues import randValues


class Test_TagGateway():

    def setup_class(self):
        Logger.logSuiteName(str(self).split('.')[-1])
        self.orgId = constant.config['orgId']
        self.cluster = constant.config['cluster']

    def setup_method(self, method):
        messageClass = 'SMS'
        if 'EMAIL' in method.__name__:
            messageClass = 'EMAIL'      
        self.nsObj = NSAdminHelper.getConnObj(newConnection=True)
        self.nsadminHelper = NSAdminHelper(self.orgId, messageClass)
        self.nsadminHelper.disableDomainPropertiesGatewayMap()
        Logger.logMethodName(method.__name__)

    def test_sendMessage_SMS_HIGH_NoGateway(self):
        msgDict = {"messageClass" : "SMS", "priority" : "HIGH", 
            "message" : "test message No gateway" ,"tags":["otp"]}
        msgId  = self.nsadminHelper.createAndSendMessage(msgDict)
        self.nsadminHelper.assertWithWaitUntil(msgId, ['GTW_NOT_FOUND'], 'Messages status', 10)
    
    def test_sendMessage_SMS_HIGH_DefaultNoTagGateway(self):
        self.nsadminHelper.configureGateway("HIGH", "cardboardfishmock")
        msgDict = {"messageClass" : "SMS", "priority" : "HIGH", 
            "message" : "test message No gateway" ,"tags":["otp"]}
        msgId  = self.nsadminHelper.createAndSendMessage(msgDict)
        self.nsadminHelper.assertWithWaitUntil(msgId, ['GTW_NOT_FOUND'], 'Messages status', 10)

    def test_sendMessage_SMS_HIGH_DefaultAndTagGateway(self):
        self.nsadminHelper.configureGateway("HIGH", "cardboardfishmock")
        self.nsadminHelper.configureGateway("HIGH", "cardboardfishmock", False, ["otp"])
        msgDict = {"messageClass" : "SMS", "priority" : "HIGH", 
            "message" : "test message No gateway" ,"tags":["otp"]}
        msgId  = self.nsadminHelper.createAndSendMessage(msgDict)
        resp = self.nsadminHelper.assertWithWaitUntil(msgId, ['RECEIVED_IN_QUEUE', 'SENT'], 'Messages status ACK', 10)
        Assertion.constructAssertion(resp.gateway ==  constant.config['orgName']+"cardboardfishmock", 'Messages gateway')

    def test_sendMessage_SMS_HIGH_DefaultAndMultipleTagGateway(self):
        self.nsadminHelper.configureGateway("HIGH", "cardboardfishmock")
        self.nsadminHelper.configureGateway("HIGH", "cardboardfishmock1", False, ["otp"], {}, 2)
        self.nsadminHelper.configureGateway("HIGH", "cardboardfishmock2", False, ["otp"], {}, 3)
        self.nsadminHelper.configureGateway("HIGH", "cardboardfishmock3", False, ["otp"], {}, 4)
        msgDict = {"messageClass" : "SMS", "priority" : "HIGH", 
            "message" : "test message No gateway" ,"tags":["otp"]}
        msgId  = self.nsadminHelper.createAndSendMessage(msgDict)
        resp = self.nsadminHelper.assertWithWaitUntil(msgId, ['RECEIVED_IN_QUEUE', 'SENT'], 'Messages status ACK', 10)
        Assertion.constructAssertion(resp.gateway ==  constant.config['orgName']+"cardboardfishmock1", 'Messages gateway')

    def test_sendMessage_SMS_HIGH_ExpiredTagGateway(self):
        self.nsadminHelper.configureGateway("HIGH", "cardboardfishmock", False, ["otp"], 
            {"startTimestamp": int(time.time() - 18000)*1000,
            "endTimestamp" : int(time.time() + 5)*1000})
        time.sleep(5)
        msgDict = {"messageClass" : "SMS", "priority" : "HIGH", 
            "message" : "test message No gateway" ,"tags":["otp"]}
        msgId = self.nsadminHelper.createAndSendMessage(msgDict)
        self.nsadminHelper.assertWithWaitUntil(msgId, ['GTW_NOT_FOUND'], 'Messages status', 10)

    def test_sendMessage_SMS_HIGH_DifferentTag(self):
        self.nsadminHelper.configureGateway("HIGH", "cardboardfishmock", False, ["otp"])
        msgDict = {"messageClass" : "SMS", "priority" : "HIGH", 
            "message" : "test message No gateway" ,"tags":["highvolttrans"]}
        msgId = self.nsadminHelper.createAndSendMessage(msgDict)
        self.nsadminHelper.assertWithWaitUntil(msgId, ['GTW_NOT_FOUND'], 'Messages status', 10)

    def test_sendMessage_EMAIL_HIGH_NoTagGateways(self): # Should fall back to Capillary org Gateway
        msgDict = {"messageClass" : "EMAIL", "priority" : "HIGH", "body" : "test body",
            "message" : "test message No gateway" ,"tags":["otp"]}
        msgId = self.nsadminHelper.createAndSendMessage(msgDict)
        resp = self.nsadminHelper.assertWithWaitUntil(msgId, ['RECEIVED_IN_QUEUE', 'SENT'], 'Messages status ACK', 10)
        Assertion.constructAssertion(resp.gateway ==  "localmail_HIGH", 'Messages gateway')


    def test_sendMessage_Email_HIGH_DefaultAndTagGateway(self): # Will go from Default gateway. Tag no effect in EMAIL     
        self.nsadminHelper.configureGateway("HIGH", "localmail_HIGH")
        self.nsadminHelper.configureGateway("HIGH", "localmail_HIGH2", False, ["otp"])
        msgDict = {"messageClass" : "EMAIL", "priority" : "HIGH", "body" : "test body",
            "message" : "test message No gateway" ,"tags":["otp"]}
        msgId = self.nsadminHelper.createAndSendMessage(msgDict)
        resp = self.nsadminHelper.assertWithWaitUntil(msgId, ['RECEIVED_IN_QUEUE', 'SENT'], 'Messages status ACK', 10)
        Assertion.constructAssertion(resp.gateway == "localmail_HIGH", 'Messages gateway')


    ## capillary tag
    @pytest.mark.parametrize('priority, gateway, tags', [
            ('HIGH', 'cardboardfishmock',["capillary", "otp"]),
            ('BULK', 'valuefirstmock',["capillary", "campaigns"])])    
    def test_sendMessage_SMS_NoGateways_withCapillaryMsgTag(self, priority, gateway, tags): # Should not fall back to Capillary org Gateway
        self.nsadminHelper.configureGateway(priority, gateway)
        msgDict = {"messageClass" : "SMS", "priority" : priority,"tags": tags,
            "message" : "test message without tag gateway with capillary tag"}
        msgId = self.nsadminHelper.createAndSendMessage(msgDict)
        self.nsadminHelper.assertWithWaitUntil(msgId, ['GTW_NOT_FOUND'], 'Messages status', 10)

    def test_sendMessage_SMS_HIGH_CapillaryTag(self):
        self.nsadminHelper.configureGateway("HIGH", "cardboardfishmock1", False, ["capillary"], {}, 1)
        msgDict = {"messageClass" : "SMS", "priority" : "HIGH", 
            "message" : "test message capillary tag" ,"tags":["otp"]}
        msgId = self.nsadminHelper.createAndSendMessage(msgDict)
        self.nsadminHelper.assertWithWaitUntil(msgId, ['GTW_NOT_FOUND'], 'Messages status', 10)

        msgDict = {"messageClass" : "SMS", "priority" : "HIGH", 
            "message" : "test message and gateway with capillary tag","tags":["capillary"]}
        msgId = self.nsadminHelper.createAndSendMessage(msgDict)
        self.nsadminHelper.assertWithWaitUntil(msgId, ['RECEIVED_IN_QUEUE', 'SENT'], 'Messages status ACK', 10)

    @pytest.mark.parametrize('priority, tags', [
            ('HIGH', ["capillary", "report"]),
            ('BULK', ["capillary", "campaigns"])])
    def test_sendMessage_EMAIL_NoGateways_withCapillaryMsgTag(self, priority, tags): # Should not fall back to Capillary org Gateway
        msgDict = {"messageClass" : "EMAIL", "priority" : priority, "body" : "test body",
            "message" : "test message No gateway" ,"tags": tags}
        msgId = self.nsadminHelper.createAndSendMessage(msgDict)
        self.nsadminHelper.assertWithWaitUntil(msgId, ['GTW_NOT_FOUND'], 'Messages status', 10)

    @pytest.mark.parametrize('priority, gateway, tags', [
            ('HIGH', 'localmail_HIGH',["capillary", "otp"]),
            ('BULK', 'localmail_BULK',["capillary", "campaigns"])]) 
    def test_sendMessage_EMAIL_DefaultAndCapillaryTagGateway(self, priority, gateway, tags): # Will go from capillary tag gateway.
        self.nsadminHelper.configureGateway(priority, gateway)
        self.nsadminHelper.configureGateway(priority, gateway+'_2', False, tags)
        msgDict = {"messageClass" : "EMAIL", "priority" : priority, "body" : "test body",
            "message" : "test message No gateway" ,"tags": tags}
        msgId = self.nsadminHelper.createAndSendMessage(msgDict)
        resp = self.nsadminHelper.assertWithWaitUntil(msgId, ['RECEIVED_IN_QUEUE', 'SENT'], 'Messages status ACK', 10)
        Assertion.constructAssertion(gateway+'_2' in resp.gateway, 'Messages gateway')       


    @pytest.mark.parametrize('priority, gateway, tags', [
            ('HIGH', 'localmail_HIGH',["capillary", "otp123"]),
            ('BULK', 'localmail_BULK',["capillary", "campaigns123"])]) 
    def test_sendMessage_EMAIL_RandomTagDefaultAndCapillaryTagGateway(self, priority, gateway, tags): # Will go from capillary tag gateway.
        self.nsadminHelper.configureGateway(priority, gateway)
        self.nsadminHelper.configureGateway(priority, gateway+'_2', False, tags)
        msgDict = {"messageClass" : "EMAIL", "priority" : priority, "body" : "test body",
            "message" : "test message No gateway" ,"tags": tags}
        msgId = self.nsadminHelper.createAndSendMessage(msgDict)
        resp = self.nsadminHelper.assertWithWaitUntil(msgId, ['RECEIVED_IN_QUEUE', 'SENT'], 'Messages status ACK', 10)
        Assertion.constructAssertion(gateway+'_2' in resp.gateway, 'Messages gateway')   

    @pytest.mark.parametrize('priority, gateway, tags, msgTag', [
            ('HIGH', 'localmail_HIGH',["capillary", "otp"], ["otp"]),
            ('BULK', 'localmail_BULK',["capillary", "campaigns"], ["campaigns"])]) 
    def test_sendMessage_EMAIL_OTPFromCapillaryTagGateway(self, priority, gateway, tags, msgTag): # send regular messages from capillary tag gateway.
        self.nsadminHelper.configureGateway(priority, gateway+'_2', False, tags)
        msgDict = {"messageClass" : "EMAIL", "priority" : priority, "body" : "test body",
            "message" : "test message No gateway" ,"tags": msgTag}
        msgId = self.nsadminHelper.createAndSendMessage(msgDict)
        resp = self.nsadminHelper.assertWithWaitUntil(msgId, ['RECEIVED_IN_QUEUE', 'SENT'], 'Messages status ACK', 10)
        Assertion.constructAssertion(gateway+'_2' in resp.gateway, 'Messages gateway')


    def test_sendMessage_EMAIL_HIGH_DefaultAndFallbackTagGateway(self): # should fallback to Org 0 tag gateway
        self.nsadminHelper.configureGateway("HIGH", "localmail_HIGH")
        self.nsadminHelper.configureGateway("HIGH", "localmail_HIGH2", False, ["capillary", "report"])
        msgDict = {"messageClass" : "EMAIL", "priority" : "HIGH", "body" : "test body",
            "message" : "test message No gateway" ,"tags":["capillary", "otp"]}
        msgId = self.nsadminHelper.createAndSendMessage(msgDict)
        resp = self.nsadminHelper.assertWithWaitUntil(msgId, ['RECEIVED_IN_QUEUE', 'SENT'], 'Messages status ACK', 10)
        Assertion.constructAssertion(resp.gateway == "localmail_HIGH_OTP", 'Messages gateway')                


    def test_sendMessage_EMAIL_BULK_DefaultAndFallbackTagGateway(self): # should not fallback to Org 0 
        self.nsadminHelper.configureGateway("BULK", "localmail_BULK")
        self.nsadminHelper.configureGateway("BULK", "localmail_BULK2", False, ["capillary", "otp"])
        msgDict = {"messageClass" : "EMAIL", "priority" : "BULK", "body" : "test body",
            "message" : "test message No gateway" ,"tags":["capillary", "report"]}
        msgId = self.nsadminHelper.createAndSendMessage(msgDict)
        self.nsadminHelper.assertWithWaitUntil(msgId, ['GTW_NOT_FOUND'], 'Messages status', 10)