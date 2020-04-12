# -*- coding: utf-8 -*-

import pytest, time, json

from src.Constant.constant import constant
from src.utilities.logger import Logger
from src.modules.nsadmin.nsadminObject import NSAdminObject
from src.modules.nsadmin.nsadminHelper import NSAdminHelper
from src.utilities.assertion import Assertion
from src.utilities.randValues import randValues
from src.utilities.dbhelper import dbHelper


class Test_sendMessage_VoiceCall():

    def setup_class(self):
        Logger.logSuiteName(str(self).split('.')[-1])
        self.orgId = constant.config['orgId']
        self.cluster = constant.config['cluster']

    def setup_method(self, method):      
        self.nsObj = NSAdminHelper.getConnObj(newConnection=True)
        self.nsadminHelper = NSAdminHelper(self.orgId, 'VOICECALL')
        self.nsadminHelper.disableDomainPropertiesGatewayMap()        
        Logger.logMethodName(method.__name__)


    @pytest.mark.parametrize('priority, gateway', [
                    ('HIGH', 'tbpvoicecall'),
                    ('BULK', 'tbpvoicecall')])        
    def est_sendMessage_VoiceCall_Sanity(self, priority, gateway):
        self.nsadminHelper.configureGateway(priority, gateway)
        msgDict = {"messageClass" : "VOICECALL", "priority" : priority, "message" : "test message with priority "+priority}
        msgId = self.nsadminHelper.createAndSendMessage(msgDict)
        Assertion.constructAssertion(type(msgId) == int, 'sendMessage output')
        resp = self.nsadminHelper.assertWithWaitUntil(msgId, ['RECEIVED_IN_QUEUE', 'SENT'], 'Messages status ACK', 10)
        Assertion.constructAssertion(resp.gateway == gateway, 'gateway used for  sending')
        Assertion.constructAssertion(resp.priority == priority, 'priority')

    