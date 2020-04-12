# -*- coding: utf-8 -*-

import pytest, time, json

from src.Constant.constant import constant
from src.utilities.logger import Logger
from src.modules.nsadmin.nsadminObject import NSAdminObject
from src.modules.nsadmin.nsadminHelper import NSAdminHelper
from src.utilities.assertion import Assertion
from src.utilities.randValues import randValues
from src.utilities.dbhelper import dbHelper


class Test_sendMessage_LINE():

    def setup_class(self):
        Logger.logSuiteName(str(self).split('.')[-1])
        self.orgId = constant.config['orgId']
        self.cluster = constant.config['cluster']

    def setup_method(self, method):      
        self.nsObj = NSAdminHelper.getConnObj(newConnection=True)
        self.nsadminHelper = NSAdminHelper(self.orgId, 'LINE')
        self.nsadminHelper.disableDomainPropertiesGatewayMap()        
        Logger.logMethodName(method.__name__)

    ## 2019-02-11-17:25:51.518 [Camel (camel-ce) thread #1258 - RabbitMQConsumer] [1619] [85e72289-d6c0-4458-a147-bdb2e82e3ea5] [-1] [-1] [LINE] [line] [1548959588713] in.capillary.service.impl.IntouchAPIService:105 ERROR - error during fetching channel configs from intouch : 


    @pytest.mark.parametrize('priority, gateway', [
                    ('HIGH', 'cardboardfishmock'),
                    ('BULK', 'valuefirstmock')])        
    def est_sendMessage_LINE(self, priority, gateway):
        self.nsadminHelper.configureGateway(priority, gateway)
        message = {"to": receiver, "messages": [{ "type" : "text", "text": "Hi, this is a test bulk message"}]}
        msgDict = {"messageClass" : "SMS", "priority" : priority, 
        "message" : "test message with priority "+priority, 'receiver' : 'U1895436c12d420347a53ce25a3b7fad5' }
        msgId = self.nsadminHelper.createAndSendMessage(msgDict)
        Assertion.constructAssertion(type(msgId) == int, 'sendMessage output')
        resp = self.nsadminHelper.assertWithWaitUntil(msgId, ['RECEIVED_IN_QUEUE', 'SENT'], 'Messages status ACK', 10)
        Assertion.constructAssertion(resp.gateway == gateway, 'gateway used for  sending')
        Assertion.constructAssertion(resp.priority == priority, 'priority')

    