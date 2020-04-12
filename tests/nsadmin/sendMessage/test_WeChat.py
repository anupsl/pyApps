# -*- coding: utf-8 -*-

import pytest, time, json

from src.Constant.constant import constant
from src.utilities.logger import Logger
from src.modules.nsadmin.nsadminObject import NSAdminObject
from src.modules.nsadmin.nsadminHelper import NSAdminHelper
from src.utilities.assertion import Assertion
from src.utilities.randValues import randValues
from src.utilities.dbhelper import dbHelper


class Test_sendMessage_WECHAT():

    def setup_class(self):
        Logger.logSuiteName(str(self).split('.')[-1])
        self.cluster = constant.config['cluster']

    def setup_method(self, method):      
        self.nsObj = NSAdminHelper.getConnObj(newConnection=True)
        if self.cluster in ['nightly']:
            self.orgId = 780
        elif self.cluster == 'china':
            self.orgId = 200017        
        self.nsadminHelper = NSAdminHelper(self.orgId, 'WECHAT')       
        Logger.logMethodName(method.__name__)


    @pytest.mark.parametrize('priority, tags, gateway', [
            ('HIGH', ['transaction'], 'wecrmwechat_HIGH'),
            ('BULK', ['campaign'], 'wecrmwechat_BULK')])        
    def test_sendMessage_Wechat_China_Prod_Sanity(self, priority, tags, gateway):
        if self.cluster in ['nightly']:
            wechatTemplateId = "L_9kbOkFR2MAwDgNL-KRcoCxea7E_dE0-vT44UwZKIQ"
            wechatOriginalId = "wxbfceb2b8ab553715"
            wechatUrl = "https://nightly.capillary.in/"
        elif self.cluster == 'china':
            wechatTemplateId = "Nc9fDFlKRMWdaoxZtjzSkNo_teR1Cw8CH1TNXhlf0jc"
            wechatOriginalId = "gh_923969206326" 
            wechatUrl = "http://we.capillarytech-cn.com/"
        receiver = 'oduTN1Tn2q6x0IfpHEwbF8Znb1fI'
        message = json.dumps({
            "template_id": wechatTemplateId,
            "touser": receiver,
            "OriginalId": wechatOriginalId,
            "Title": "订阅模板消息",
            "BrandId": "eGdQY2VQTCUyYjUlMmJaSE1SN2hwWFNkdGRYMEtSbXJOSUFZ",
            "url": wechatUrl,
            "TopColor": "#000000",
            "data": {   
                "first": {"Value": "WeChatTest", "color": "#00000"},
                "cardNumber": {"Value": "Your customerId ", "color": "#00000"},
                "type": {"Value": "Your slab name End Tier", "color": "#00000"},
                "address": {"Value": "Your store address mgroad, ropenaagarasjdnf","color": "#00000"},
                "VIPName": {"Value": "Your number ","color": "#00000"},
                "VIPPhone": {"Value": "Your Number ","color": "#00000"},
                "expDate": {"Value": "Your's slab expire date ","color": "#00000"},
                "remark": {"Value": "Additional information provided","color": "#00000"}
            }})
        additionalHeaders = {"APP_ID":"wxc7bf989decc7e35b", 
            "APP_SECRET":"eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJ6aG91cGluZyIsImlsIjp0cnVlLCJleHAiOjQ2NjU5ODI3MjksImlhdCI6MTUxMDMwOTEyOTAwOSwianRpIjozfQ.zGgmGaz89ReL1WgeuBj3sdgsHvkbvrXmSvggU-cm4UClnOObAhSlVQwMV9jjJRXkEA6MXjrHLtEFQdJgNQ424Q"}
        msgDict= {'messageClass': 'WECHAT', 'sendingOrgId': self.orgId, 'receiver' : receiver, 
        'priority' : priority, 'tags' : tags,
        'message' : message, 'truncate' : False, 'additionalHeaders' : additionalHeaders}
        resp  = self.nsadminHelper.createAndSendMessage(msgDict)
        Assertion.constructAssertion(resp > 0, 'sendMessage output')
        resp = self.nsObj.getMessagesById([resp])[0]
        Assertion.constructAssertion(resp.status in ['RECEIVED_IN_QUEUE', 'SENT'], 'Messages status')
        Assertion.constructAssertion(resp.gateway == gateway, 'gateway used for  sending')
        Assertion.constructAssertion(resp.priority == priority, 'priority')

    