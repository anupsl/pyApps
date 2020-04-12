import pytest, time, datetime, copy, json, sys, unicodedata
from src.Constant.constant import constant
from src.modules.iris.list import campaignList
from src.utilities.logger import Logger
from src.utilities.assertion import Assertion
from src.modules.iris.campaigns import campaigns
from src.modules.iris.message import campaignMessage
from src.modules.iris.dbCallsCampaign import dbCallsCampaign
from src.modules.iris.dbCallsMessage import dbCallsMessage
from src.modules.iris.dbCallsCoupons import dbCallsCoupons
from src.modules.iris.dbCallsList import dbCallsList
from src.modules.iris.construct import construct
from src.modules.iris.authorize import authorize
from src.modules.veneno.venenoObject import VenenoObject
from src.modules.veneno.venenoHelper import VenenoHelper
from src.modules.veneno.venenoDBAssertion import VenenoDBAssertion


@pytest.mark.skipif(constant.config['cluster'] not in ['nightly_V'], reason='Wechat Configured only in nightly')
@pytest.mark.run(order=12)
class est_Veneno_RateLimit_WECHAT_ORG():
    
    def setup_class(self):
        Logger.logSuiteName(str(self).split('.')[-1])
        self.actualOrgId = construct.updateOrgId(constant.config['wechat']['orgId'])
        self.actualOrgName = construct.updateOrgName(constant.config['wechat']['orgName'])
        VenenoHelper.configRateLimit(enable=True, channel='WECHAT')
        VenenoHelper.setupStrategy(daily=1, weekly=2, monthly=3, channel='WECHAT')
        self.testObjectForRateLimit = VenenoHelper.preRequisitesForVenenoRateLimit('WECHAT')
        self.campaignId = self.testObjectForRateLimit['campaign']['id']
        
    def teardown_class(self):
        Logger.log('Disable Rate Limit Config')
        VenenoHelper.configRateLimit(enable=False, channel='WECHAT')
        construct.updateOrgId(self.actualOrgId)
        construct.updateOrgName(self.actualOrgName)
        
    def setup_method(self, method):
        self.connObj = VenenoHelper.getConnObj(newConnection=True)
        Logger.logMethodName(method.__name__)
        
    @pytest.mark.parametrize('listType', [
        ('upload')
        ])
    def test_veneno_rateLimit_allStrategySatisfied(self, listType):
        self.listId = self.testObjectForRateLimit['list'][listType]['groupDetails']['id']
        campaignMessage.getWeCRMTemplates()
        subject = {
            "template_id" : unicodedata.normalize('NFKD', constant.config['templateId']).encode('ascii', 'ignore'),
            "touser" : "{{wechat_open_id}}",
            "OriginalId" : constant.config['wechat']['OriginalId'],
            "Title" : "",
            "BrandId" : "f",
            "url" : "http://we.capillarytech-cn.com/web?appid=wxc7bf989decc7e35b&redirect_uri=http://somelink.com/someword?nowAParam=firstParam&second=second.Param&response_type=code&scope=snsapi_base&state=STATE",
            "TopColor" : "#000000",
            "data" : {"productType": {"value": "HakeemProduct", "color": "#00000"}, "name": {"value": "Hakeem {{first_name}} Lukka", "color": "#00000"}, "number": {"value": "898767 skdjnjn", "color": "#00000"}, "expDate": {"value": "look down", "color": "#00000"}, "remark": { "value": "Look up", "color": "#00000"}}
        }
        cdDetailsBody = {
             'campaignId':self.testObjectForRateLimit['campaign']['id'],
             'communicationType':'WECHAT',
             'subject': str(subject),
             'body': 'Thrift Created Automation Wechat Body',
             'recipientListId':self.testObjectForRateLimit['list'][listType]['groupVersionDetails']['TEST']['id'],
             'overallRecipientCount':self.testObjectForRateLimit['list'][listType]['groupVersionDetails']['TEST']['customer_count'],
             'expectedDeliveryCount':self.testObjectForRateLimit['list'][listType]['groupVersionDetails']['TEST']['customer_count'],
             'groupName':self.testObjectForRateLimit['list'][listType]['groupDetails']['group_label']
            }
        communicationDetailObject = VenenoObject.communicationDetail(cdDetailsBody)
        communicationId = self.connObj.addMessageForRecipients(communicationDetailObject)
        VenenoDBAssertion(cdDetailsBody['campaignId'], cdDetailsBody['communicationType'], communicationId, cdDetailsBody['overallRecipientCount'], cdDetailsBody['recipientListId'], cdDetailsBody['subject'], skippedReasons=['Captured OpenId for user seems to be unsubscribed']).check()
        authorize.dbAssertRateLimitStats(self.testObjectForRateLimit['list'][listType]['campaignGroupRecipients']['TEST'], {'DAILY':1, 'WEEKLY':1, 'MONTHLY':1}, channel='WECHAT')
        
    @pytest.mark.parametrize('listType', [
        ('upload')
        ])    
    def test_veneno_rateLimit_dailyLimitExceed(self, listType):
        self.listId = self.testObjectForRateLimit['list'][listType]['groupDetails']['id']
        campaignMessage.getWeCRMTemplates()
        subject = {
            "template_id" : unicodedata.normalize('NFKD', constant.config['templateId']).encode('ascii', 'ignore'),
            "touser" : "{{wechat_open_id}}",
            "OriginalId" : constant.config['wechat']['OriginalId'],
            "Title" : "",
            "BrandId" : "f",
            "url" : "http://we.capillarytech-cn.com/web?appid=wxc7bf989decc7e35b&redirect_uri=http://somelink.com/someword?nowAParam=firstParam&second=second.Param&response_type=code&scope=snsapi_base&state=STATE",
            "TopColor" : "#000000",
            "data" : {"productType": {"value": "HakeemProduct", "color": "#00000"}, "name": {"value": "Hakeem {{first_name}} Lukka", "color": "#00000"}, "number": {"value": "898767 skdjnjn", "color": "#00000"}, "expDate": {"value": "look down", "color": "#00000"}, "remark": { "value": "Look up", "color": "#00000"}}
        }
        cdDetailsBody = {
             'campaignId':self.testObjectForRateLimit['campaign']['id'],
             'communicationType':'WECHAT',
             'subject': str(subject),
             'body': 'Thrift Created Automation Wechat Body',
             'recipientListId':self.testObjectForRateLimit['list'][listType]['groupVersionDetails']['TEST']['id'],
             'overallRecipientCount':self.testObjectForRateLimit['list'][listType]['groupVersionDetails']['TEST']['customer_count'],
             'expectedDeliveryCount':self.testObjectForRateLimit['list'][listType]['groupVersionDetails']['TEST']['customer_count'],
             'groupName':self.testObjectForRateLimit['list'][listType]['groupDetails']['group_label']
            }
        communicationDetailObject = VenenoObject.communicationDetail(cdDetailsBody)
        communicationId = self.connObj.addMessageForRecipients(communicationDetailObject)
        VenenoDBAssertion(cdDetailsBody['campaignId'], cdDetailsBody['communicationType'], communicationId, cdDetailsBody['overallRecipientCount'], cdDetailsBody['recipientListId'], cdDetailsBody['subject'], skippedReasons=['Captured OpenId for user seems to be unsubscribed', 'rate limit crossed for user']).check()
        authorize.dbAssertRateLimitStats(self.testObjectForRateLimit['list'][listType]['campaignGroupRecipients']['TEST'], {'DAILY':1, 'WEEKLY':1, 'MONTHLY':1}, channel='WECHAT')
        
    @pytest.mark.parametrize('listType', [
        ('upload')
        ])
    def test_veneno_rateLimit_weeklyLimitExceed(self, listType):
        VenenoHelper.setupStrategy(daily=2, weekly=1, monthly=3, channel='WECHAT')
        self.listId = self.testObjectForRateLimit['list'][listType]['groupDetails']['id']
        campaignMessage.getWeCRMTemplates()
        subject = {
            "template_id" : unicodedata.normalize('NFKD', constant.config['templateId']).encode('ascii', 'ignore'),
            "touser" : "{{wechat_open_id}}",
            "OriginalId" : constant.config['wechat']['OriginalId'],
            "Title" : "",
            "BrandId" : "f",
            "url" : "http://we.capillarytech-cn.com/web?appid=wxc7bf989decc7e35b&redirect_uri=http://somelink.com/someword?nowAParam=firstParam&second=second.Param&response_type=code&scope=snsapi_base&state=STATE",
            "TopColor" : "#000000",
            "data" : {"productType": {"value": "HakeemProduct", "color": "#00000"}, "name": {"value": "Hakeem {{first_name}} Lukka", "color": "#00000"}, "number": {"value": "898767 skdjnjn", "color": "#00000"}, "expDate": {"value": "look down", "color": "#00000"}, "remark": { "value": "Look up", "color": "#00000"}}
        }
        cdDetailsBody = {
             'campaignId':self.testObjectForRateLimit['campaign']['id'],
             'communicationType':'WECHAT',
             'subject': str(subject),
             'body': 'Thrift Created Automation Wechat Body',
             'recipientListId':self.testObjectForRateLimit['list'][listType]['groupVersionDetails']['TEST']['id'],
             'overallRecipientCount':self.testObjectForRateLimit['list'][listType]['groupVersionDetails']['TEST']['customer_count'],
             'expectedDeliveryCount':self.testObjectForRateLimit['list'][listType]['groupVersionDetails']['TEST']['customer_count'],
             'groupName':self.testObjectForRateLimit['list'][listType]['groupDetails']['group_label']
            }
        communicationDetailObject = VenenoObject.communicationDetail(cdDetailsBody)
        communicationId = self.connObj.addMessageForRecipients(communicationDetailObject)
        VenenoDBAssertion(cdDetailsBody['campaignId'], cdDetailsBody['communicationType'], communicationId, cdDetailsBody['overallRecipientCount'], cdDetailsBody['recipientListId'], cdDetailsBody['subject'], skippedReasons=['Captured OpenId for user seems to be unsubscribed', 'rate limit crossed for user']).check()
        authorize.dbAssertRateLimitStats(self.testObjectForRateLimit['list'][listType]['campaignGroupRecipients']['TEST'], {'DAILY':1, 'WEEKLY':1, 'MONTHLY':1}, channel='WECHAT')
        
    @pytest.mark.parametrize('listType', [
        ('upload')
        ])
    def test_veneno_rateLimit_monthlyLimitExceed(self, listType):
        VenenoHelper.setupStrategy(daily=2, weekly=2, monthly=1, channel='WECHAT')
        self.listId = self.testObjectForRateLimit['list'][listType]['groupDetails']['id']
        campaignMessage.getWeCRMTemplates()
        subject = {
            "template_id" : unicodedata.normalize('NFKD', constant.config['templateId']).encode('ascii', 'ignore'),
            "touser" : "{{wechat_open_id}}",
            "OriginalId" : constant.config['wechat']['OriginalId'],
            "Title" : "",
            "BrandId" : "f",
            "url" : "http://we.capillarytech-cn.com/web?appid=wxc7bf989decc7e35b&redirect_uri=http://somelink.com/someword?nowAParam=firstParam&second=second.Param&response_type=code&scope=snsapi_base&state=STATE",
            "TopColor" : "#000000",
            "data" : {"productType": {"value": "HakeemProduct", "color": "#00000"}, "name": {"value": "Hakeem {{first_name}} Lukka", "color": "#00000"}, "number": {"value": "898767 skdjnjn", "color": "#00000"}, "expDate": {"value": "look down", "color": "#00000"}, "remark": { "value": "Look up", "color": "#00000"}}
        }
        cdDetailsBody = {
             'campaignId':self.testObjectForRateLimit['campaign']['id'],
             'communicationType':'WECHAT',
             'subject': str(subject),
             'body': 'Thrift Created Automation Wechat Body',
             'recipientListId':self.testObjectForRateLimit['list'][listType]['groupVersionDetails']['TEST']['id'],
             'overallRecipientCount':self.testObjectForRateLimit['list'][listType]['groupVersionDetails']['TEST']['customer_count'],
             'expectedDeliveryCount':self.testObjectForRateLimit['list'][listType]['groupVersionDetails']['TEST']['customer_count'],
             'groupName':self.testObjectForRateLimit['list'][listType]['groupDetails']['group_label']
            }
        communicationDetailObject = VenenoObject.communicationDetail(cdDetailsBody)
        communicationId = self.connObj.addMessageForRecipients(communicationDetailObject)
        VenenoDBAssertion(cdDetailsBody['campaignId'], cdDetailsBody['communicationType'], communicationId, cdDetailsBody['overallRecipientCount'], cdDetailsBody['recipientListId'], cdDetailsBody['subject'], skippedReasons=['Captured OpenId for user seems to be unsubscribed', 'rate limit crossed for user']).check()
        authorize.dbAssertRateLimitStats(self.testObjectForRateLimit['list'][listType]['campaignGroupRecipients']['TEST'], {'DAILY':1, 'WEEKLY':1, 'MONTHLY':1}, channel='WECHAT')
        
    @pytest.mark.parametrize('listType', [
        ('upload')
        ])
    def test_veneno_rateLimit_dailyWeeklyMonthlyLimitExceed(self, listType):
        VenenoHelper.setupStrategy(daily=1, weekly=1, monthly=1, channel='WECHAT')
        self.listId = self.testObjectForRateLimit['list'][listType]['groupDetails']['id']
        campaignMessage.getWeCRMTemplates()
        subject = {
            "template_id" : unicodedata.normalize('NFKD', constant.config['templateId']).encode('ascii', 'ignore'),
            "touser" : "{{wechat_open_id}}",
            "OriginalId" : constant.config['wechat']['OriginalId'],
            "Title" : "",
            "BrandId" : "f",
            "url" : "http://we.capillarytech-cn.com/web?appid=wxc7bf989decc7e35b&redirect_uri=http://somelink.com/someword?nowAParam=firstParam&second=second.Param&response_type=code&scope=snsapi_base&state=STATE",
            "TopColor" : "#000000",
            "data" : {"productType": {"value": "HakeemProduct", "color": "#00000"}, "name": {"value": "Hakeem {{first_name}} Lukka", "color": "#00000"}, "number": {"value": "898767 skdjnjn", "color": "#00000"}, "expDate": {"value": "look down", "color": "#00000"}, "remark": { "value": "Look up", "color": "#00000"}}
        }
        cdDetailsBody = {
             'campaignId':self.testObjectForRateLimit['campaign']['id'],
             'communicationType':'WECHAT',
             'subject': str(subject),
             'body': 'Thrift Created Automation Wechat Body',
             'recipientListId':self.testObjectForRateLimit['list'][listType]['groupVersionDetails']['TEST']['id'],
             'overallRecipientCount':self.testObjectForRateLimit['list'][listType]['groupVersionDetails']['TEST']['customer_count'],
             'expectedDeliveryCount':self.testObjectForRateLimit['list'][listType]['groupVersionDetails']['TEST']['customer_count'],
             'groupName':self.testObjectForRateLimit['list'][listType]['groupDetails']['group_label']
            }
        communicationDetailObject = VenenoObject.communicationDetail(cdDetailsBody)
        communicationId = self.connObj.addMessageForRecipients(communicationDetailObject)
        VenenoDBAssertion(cdDetailsBody['campaignId'], cdDetailsBody['communicationType'], communicationId, cdDetailsBody['overallRecipientCount'], cdDetailsBody['recipientListId'], cdDetailsBody['subject'], skippedReasons=['Captured OpenId for user seems to be unsubscribed', 'rate limit crossed for user']).check()
        authorize.dbAssertRateLimitStats(self.testObjectForRateLimit['list'][listType]['campaignGroupRecipients']['TEST'], {'DAILY':1, 'WEEKLY':1, 'MONTHLY':1}, channel='WECHAT')
        
    @pytest.mark.parametrize('listType', [
        ('upload')
        ])
    def test_veneno_rateLimit_reconfig_allStrategySatisified(self, listType):
        VenenoHelper.setupStrategy(daily=2, weekly=2, monthly=2, channel='WECHAT')
        self.listId = self.testObjectForRateLimit['list'][listType]['groupDetails']['id']
        campaignMessage.getWeCRMTemplates()
        subject = {
            "template_id" : unicodedata.normalize('NFKD', constant.config['templateId']).encode('ascii', 'ignore'),
            "touser" : "{{wechat_open_id}}",
            "OriginalId" : constant.config['wechat']['OriginalId'],
            "Title" : "",
            "BrandId" : "f",
            "url" : "http://we.capillarytech-cn.com/web?appid=wxc7bf989decc7e35b&redirect_uri=http://somelink.com/someword?nowAParam=firstParam&second=second.Param&response_type=code&scope=snsapi_base&state=STATE",
            "TopColor" : "#000000",
            "data" : {"productType": {"value": "HakeemProduct", "color": "#00000"}, "name": {"value": "Hakeem {{first_name}} Lukka", "color": "#00000"}, "number": {"value": "898767 skdjnjn", "color": "#00000"}, "expDate": {"value": "look down", "color": "#00000"}, "remark": { "value": "Look up", "color": "#00000"}}
        }
        cdDetailsBody = {
             'campaignId':self.testObjectForRateLimit['campaign']['id'],
             'communicationType':'WECHAT',
             'subject': str(subject),
             'body': 'Thrift Created Automation Wechat Body',
             'recipientListId':self.testObjectForRateLimit['list'][listType]['groupVersionDetails']['TEST']['id'],
             'overallRecipientCount':self.testObjectForRateLimit['list'][listType]['groupVersionDetails']['TEST']['customer_count'],
             'expectedDeliveryCount':self.testObjectForRateLimit['list'][listType]['groupVersionDetails']['TEST']['customer_count'],
             'groupName':self.testObjectForRateLimit['list'][listType]['groupDetails']['group_label']
            }
        communicationDetailObject = VenenoObject.communicationDetail(cdDetailsBody)
        communicationId = self.connObj.addMessageForRecipients(communicationDetailObject)
        VenenoDBAssertion(cdDetailsBody['campaignId'], cdDetailsBody['communicationType'], communicationId, cdDetailsBody['overallRecipientCount'], cdDetailsBody['recipientListId'], cdDetailsBody['subject'], skippedReasons=['Captured OpenId for user seems to be unsubscribed', 'rate limit crossed for user']).check()
        authorize.dbAssertRateLimitStats(self.testObjectForRateLimit['list'][listType]['campaignGroupRecipients']['TEST'], {'DAILY':2, 'WEEKLY':2, 'MONTHLY':2}, channel='WECHAT')
        
    @pytest.mark.parametrize('listType', [
        ('upload')
        ])
    def test_veneno_rateLimit_reconfig_allStrategySatisified_StatsUpdateCheck(self, listType):
        VenenoHelper.setupStrategy(daily=3, weekly=3, monthly=3, channel='WECHAT')
        self.listId = self.testObjectForRateLimit['list'][listType]['groupDetails']['id']
        campaignMessage.getWeCRMTemplates()
        subject = {
            "template_id" : unicodedata.normalize('NFKD', constant.config['templateId']).encode('ascii', 'ignore'),
            "touser" : "{{wechat_open_id}}",
            "OriginalId" : constant.config['wechat']['OriginalId'],
            "Title" : "",
            "BrandId" : "f",
            "url" : "http://we.capillarytech-cn.com/web?appid=wxc7bf989decc7e35b&redirect_uri=http://somelink.com/someword?nowAParam=firstParam&second=second.Param&response_type=code&scope=snsapi_base&state=STATE",
            "TopColor" : "#000000",
            "data" : {"productType": {"value": "HakeemProduct", "color": "#00000"}, "name": {"value": "Hakeem {{first_name}} Lukka", "color": "#00000"}, "number": {"value": "898767 skdjnjn", "color": "#00000"}, "expDate": {"value": "look down", "color": "#00000"}, "remark": { "value": "Look up", "color": "#00000"}}
        }
        cdDetailsBody = {
             'campaignId':self.testObjectForRateLimit['campaign']['id'],
             'communicationType':'WECHAT',
             'subject': str(subject),
             'body': 'Thrift Created Automation Wechat Body',
             'recipientListId':self.testObjectForRateLimit['list'][listType]['groupVersionDetails']['TEST']['id'],
             'overallRecipientCount':self.testObjectForRateLimit['list'][listType]['groupVersionDetails']['TEST']['customer_count'],
             'expectedDeliveryCount':self.testObjectForRateLimit['list'][listType]['groupVersionDetails']['TEST']['customer_count'],
             'groupName':self.testObjectForRateLimit['list'][listType]['groupDetails']['group_label']
            }
        communicationDetailObject = VenenoObject.communicationDetail(cdDetailsBody)
        communicationId = self.connObj.addMessageForRecipients(communicationDetailObject)
        VenenoDBAssertion(cdDetailsBody['campaignId'], cdDetailsBody['communicationType'], communicationId, cdDetailsBody['overallRecipientCount'], cdDetailsBody['recipientListId'], cdDetailsBody['subject'], skippedReasons=['Captured OpenId for user seems to be unsubscribed', 'rate limit crossed for user']).check()
        authorize.dbAssertRateLimitStats(self.testObjectForRateLimit['list'][listType]['campaignGroupRecipients']['TEST'], {'DAILY':3, 'WEEKLY':3, 'MONTHLY':3}, channel='WECHAT')
    
    @pytest.mark.parametrize('listType', [
        ('upload')
        ])   
    def test_veneno_rateLimit_dailyByPass(self, listType):
        VenenoHelper.setupStrategy(daily=3, weekly=4, monthly=4, channel='WECHAT')
        VenenoHelper.updateWindowValueToByPassStrategy(self.testObjectForRateLimit['list'][listType]['campaignGroupRecipients']['TEST'], 'DAILY', channel='WECHAT')
        self.listId = self.testObjectForRateLimit['list'][listType]['groupDetails']['id']
        campaignMessage.getWeCRMTemplates()
        subject = {
            "template_id" : unicodedata.normalize('NFKD', constant.config['templateId']).encode('ascii', 'ignore'),
            "touser" : "{{wechat_open_id}}",
            "OriginalId" : constant.config['wechat']['OriginalId'],
            "Title" : "",
            "BrandId" : "f",
            "url" : "http://we.capillarytech-cn.com/web?appid=wxc7bf989decc7e35b&redirect_uri=http://somelink.com/someword?nowAParam=firstParam&second=second.Param&response_type=code&scope=snsapi_base&state=STATE",
            "TopColor" : "#000000",
            "data" : {"productType": {"value": "HakeemProduct", "color": "#00000"}, "name": {"value": "Hakeem {{first_name}} Lukka", "color": "#00000"}, "number": {"value": "898767 skdjnjn", "color": "#00000"}, "expDate": {"value": "look down", "color": "#00000"}, "remark": { "value": "Look up", "color": "#00000"}}
        }
        cdDetailsBody = {
             'campaignId':self.testObjectForRateLimit['campaign']['id'],
             'communicationType':'WECHAT',
             'subject': str(subject),
             'body': 'Thrift Created Automation Wechat Body',
             'recipientListId':self.testObjectForRateLimit['list'][listType]['groupVersionDetails']['TEST']['id'],
             'overallRecipientCount':self.testObjectForRateLimit['list'][listType]['groupVersionDetails']['TEST']['customer_count'],
             'expectedDeliveryCount':self.testObjectForRateLimit['list'][listType]['groupVersionDetails']['TEST']['customer_count'],
             'groupName':self.testObjectForRateLimit['list'][listType]['groupDetails']['group_label']
            }
        communicationDetailObject = VenenoObject.communicationDetail(cdDetailsBody)
        communicationId = self.connObj.addMessageForRecipients(communicationDetailObject)
        VenenoDBAssertion(cdDetailsBody['campaignId'], cdDetailsBody['communicationType'], communicationId, cdDetailsBody['overallRecipientCount'], cdDetailsBody['recipientListId'], cdDetailsBody['subject'], skippedReasons=['Captured OpenId for user seems to be unsubscribed', 'rate limit crossed for user']).check()
        authorize.dbAssertRateLimitStats(self.testObjectForRateLimit['list'][listType]['campaignGroupRecipients']['TEST'], {'DAILY':1, 'WEEKLY':4, 'MONTHLY':4}, channel='WECHAT')
    
    @pytest.mark.parametrize('listType', [
        ('upload')
        ])   
    def test_veneno_rateLimit_weeklyByPass(self, listType):
        VenenoHelper.setupStrategy(daily=2, weekly=1, monthly=5, channel='WECHAT')
        VenenoHelper.updateWindowValueToByPassStrategy(self.testObjectForRateLimit['list'][listType]['campaignGroupRecipients']['TEST'], 'WEEKLY', channel='WECHAT')
        self.listId = self.testObjectForRateLimit['list'][listType]['groupDetails']['id']
        campaignMessage.getWeCRMTemplates()
        subject = {
            "template_id" : unicodedata.normalize('NFKD', constant.config['templateId']).encode('ascii', 'ignore'),
            "touser" : "{{wechat_open_id}}",
            "OriginalId" : constant.config['wechat']['OriginalId'],
            "Title" : "",
            "BrandId" : "f",
            "url" : "http://we.capillarytech-cn.com/web?appid=wxc7bf989decc7e35b&redirect_uri=http://somelink.com/someword?nowAParam=firstParam&second=second.Param&response_type=code&scope=snsapi_base&state=STATE",
            "TopColor" : "#000000",
            "data" : {"productType": {"value": "HakeemProduct", "color": "#00000"}, "name": {"value": "Hakeem {{first_name}} Lukka", "color": "#00000"}, "number": {"value": "898767 skdjnjn", "color": "#00000"}, "expDate": {"value": "look down", "color": "#00000"}, "remark": { "value": "Look up", "color": "#00000"}}
        }
        cdDetailsBody = {
             'campaignId':self.testObjectForRateLimit['campaign']['id'],
             'communicationType':'WECHAT',
             'subject': str(subject),
             'body': 'Thrift Created Automation Wechat Body',
             'recipientListId':self.testObjectForRateLimit['list'][listType]['groupVersionDetails']['TEST']['id'],
             'overallRecipientCount':self.testObjectForRateLimit['list'][listType]['groupVersionDetails']['TEST']['customer_count'],
             'expectedDeliveryCount':self.testObjectForRateLimit['list'][listType]['groupVersionDetails']['TEST']['customer_count'],
             'groupName':self.testObjectForRateLimit['list'][listType]['groupDetails']['group_label']
            }
        communicationDetailObject = VenenoObject.communicationDetail(cdDetailsBody)
        communicationId = self.connObj.addMessageForRecipients(communicationDetailObject)
        VenenoDBAssertion(cdDetailsBody['campaignId'], cdDetailsBody['communicationType'], communicationId, cdDetailsBody['overallRecipientCount'], cdDetailsBody['recipientListId'], cdDetailsBody['subject'], skippedReasons=['Captured OpenId for user seems to be unsubscribed', 'rate limit crossed for user']).check()
        authorize.dbAssertRateLimitStats(self.testObjectForRateLimit['list'][listType]['campaignGroupRecipients']['TEST'], {'DAILY':2, 'WEEKLY':1, 'MONTHLY':5}, channel='WECHAT')
    
    @pytest.mark.parametrize('listType', [
        ('upload')
        ])   
    def test_veneno_rateLimit_MonthlyByPass(self, listType):
        VenenoHelper.setupStrategy(daily=3, weekly=2, monthly=1, channel='WECHAT')
        VenenoHelper.updateWindowValueToByPassStrategy(self.testObjectForRateLimit['list'][listType]['campaignGroupRecipients']['TEST'], 'MONTHLY', channel='WECHAT')
        self.listId = self.testObjectForRateLimit['list'][listType]['groupDetails']['id']
        campaignMessage.getWeCRMTemplates()
        subject = {
            "template_id" : unicodedata.normalize('NFKD', constant.config['templateId']).encode('ascii', 'ignore'),
            "touser" : "{{wechat_open_id}}",
            "OriginalId" : constant.config['wechat']['OriginalId'],
            "Title" : "",
            "BrandId" : "f",
            "url" : "http://we.capillarytech-cn.com/web?appid=wxc7bf989decc7e35b&redirect_uri=http://somelink.com/someword?nowAParam=firstParam&second=second.Param&response_type=code&scope=snsapi_base&state=STATE",
            "TopColor" : "#000000",
            "data" : {"productType": {"value": "HakeemProduct", "color": "#00000"}, "name": {"value": "Hakeem {{first_name}} Lukka", "color": "#00000"}, "number": {"value": "898767 skdjnjn", "color": "#00000"}, "expDate": {"value": "look down", "color": "#00000"}, "remark": { "value": "Look up", "color": "#00000"}}
        }
        cdDetailsBody = {
             'campaignId':self.testObjectForRateLimit['campaign']['id'],
             'communicationType':'WECHAT',
             'subject': str(subject),
             'body': 'Thrift Created Automation Wechat Body',
             'recipientListId':self.testObjectForRateLimit['list'][listType]['groupVersionDetails']['TEST']['id'],
             'overallRecipientCount':self.testObjectForRateLimit['list'][listType]['groupVersionDetails']['TEST']['customer_count'],
             'expectedDeliveryCount':self.testObjectForRateLimit['list'][listType]['groupVersionDetails']['TEST']['customer_count'],
             'groupName':self.testObjectForRateLimit['list'][listType]['groupDetails']['group_label']
            }
        communicationDetailObject = VenenoObject.communicationDetail(cdDetailsBody)
        communicationId = self.connObj.addMessageForRecipients(communicationDetailObject)
        VenenoDBAssertion(cdDetailsBody['campaignId'], cdDetailsBody['communicationType'], communicationId, cdDetailsBody['overallRecipientCount'], cdDetailsBody['recipientListId'], cdDetailsBody['subject'], skippedReasons=['Captured OpenId for user seems to be unsubscribed', 'rate limit crossed for user']).check()
        authorize.dbAssertRateLimitStats(self.testObjectForRateLimit['list'][listType]['campaignGroupRecipients']['TEST'], {'DAILY':3, 'WEEKLY':2, 'MONTHLY':1}, channel='WECHAT')
