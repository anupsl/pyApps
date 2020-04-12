import pytest, time, datetime, copy, json, sys
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

@pytest.mark.skipif(constant.config['cluster'] not in ['nightly'], reason='RateLimit Configured only in nightly')
@pytest.mark.run(order=8)
class Test_Veneno_RateLimit_EMAIL_CUSTOM():
    
    def setup_class(self):
        Logger.logSuiteName(str(self).split('.')[-1])
        VenenoHelper.configRateLimit(enable=True, channel='EMAIL')
        VenenoHelper.setupStrategy(daily=1, weekly=2, monthly=3, channel='EMAIL')
        self.testObjectForRateLimit = VenenoHelper.preRequisitesForVenenoRateLimit('email',testControl='custom')
        self.campaignId = self.testObjectForRateLimit['campaign']['id']
        VenenoHelper.updateEmailStatus(self.testObjectForRateLimit['list'])
        
    def teardown_class(self):
        Logger.log('Disable Rate Limit Config')
        VenenoHelper.configRateLimit(enable=False, channel='EMAIL')
    
    def setup_method(self, method):
        self.connObj = VenenoHelper.getConnObj(newConnection=True)
        Logger.logMethodName(method.__name__)
    
    @pytest.mark.parametrize('listType', [
        ('upload')
        ])
    def test_veneno_rateLimit_allStrategySatisfied_email_sanity(self, listType):
        self.listId = self.testObjectForRateLimit['list'][listType]['groupDetails']['id']
        cdDetailsBody = {
             'campaignId':self.campaignId,
             'communicationType':'EMAIL',
             'subject':'Automation Generated Body {{unsubscribe}}',
             'recipientListId':self.testObjectForRateLimit['list'][listType]['groupVersionDetails']['TEST']['id'],
             'overallRecipientCount':self.testObjectForRateLimit['list'][listType]['groupVersionDetails']['TEST']['customer_count'],
             'expectedDeliveryCount':self.testObjectForRateLimit['list'][listType]['groupVersionDetails']['TEST']['customer_count'],
             'groupName':self.testObjectForRateLimit['list'][listType]['groupDetails']['group_label']
            }
        communicationDetailObject = VenenoObject.communicationDetail(cdDetailsBody)
        communicationId = self.connObj.addMessageForRecipients(communicationDetailObject)
        authorize.assertUserPresenceInNsAdminTable(communicationId , VenenoHelper.getCommunicationBucketId(communicationId), int(json.loads(self.testObjectForRateLimit['list'][listType]['groupVersionDetails']['TEST']['params'])['test_count']), testControlType='custom', verify=False,groupVersionId=cdDetailsBody['recipientListId'],channel='EMAIL')
        authorize.dbAssertRateLimitStats(self.testObjectForRateLimit['list'][listType]['campaignGroupRecipients']['TEST'], {'DAILY':1, 'WEEKLY':1, 'MONTHLY':1}, channel='EMAIL')
        
    @pytest.mark.parametrize('listType', [
        ('upload')
        ])    
    def test_veneno_rateLimit_dailyLimitExceed(self, listType):
        self.listId = self.testObjectForRateLimit['list'][listType]['groupDetails']['id']
        cdDetailsBody = {
             'campaignId':self.campaignId,
             'communicationType':'EMAIL',
             'subject':'Automation Generated Body {{unsubscribe}}',
             'recipientListId':self.testObjectForRateLimit['list'][listType]['groupVersionDetails']['TEST']['id'],
             'overallRecipientCount':self.testObjectForRateLimit['list'][listType]['groupVersionDetails']['TEST']['customer_count'],
             'expectedDeliveryCount':self.testObjectForRateLimit['list'][listType]['groupVersionDetails']['TEST']['customer_count'],
             'groupName':self.testObjectForRateLimit['list'][listType]['groupDetails']['group_label']
            }
        communicationDetailObject = VenenoObject.communicationDetail(cdDetailsBody)
        communicationId = self.connObj.addMessageForRecipients(communicationDetailObject)
        communicationDetailBucketId = VenenoHelper.getCommunicationBucketId(communicationId)
        authorize.assertUserPresenceInSkippedTable(communicationId , VenenoHelper.getCommunicationBucketId(communicationId), constant.config['skipped_errors']['RATE_LIMIT_ERROR'], 'rate limit crossed for user')
        authorize.dbAssertRateLimitStats(self.testObjectForRateLimit['list'][listType]['campaignGroupRecipients']['TEST'], {'DAILY':1, 'WEEKLY':1, 'MONTHLY':1}, channel='EMAIL')
        
    @pytest.mark.parametrize('listType', [
        ('upload')
        ])
    def test_veneno_rateLimit_weeklyLimitExceed(self, listType):
        VenenoHelper.setupStrategy(daily=2, weekly=1, monthly=3, channel='EMAIL')
        self.listId = self.testObjectForRateLimit['list'][listType]['groupDetails']['id']
        cdDetailsBody = {
             'campaignId':self.campaignId,
             'communicationType':'EMAIL',
             'subject':'Automation Generated Body {{unsubscribe}}',
             'recipientListId':self.testObjectForRateLimit['list'][listType]['groupVersionDetails']['TEST']['id'],
             'overallRecipientCount':self.testObjectForRateLimit['list'][listType]['groupVersionDetails']['TEST']['customer_count'],
             'expectedDeliveryCount':self.testObjectForRateLimit['list'][listType]['groupVersionDetails']['TEST']['customer_count'],
             'groupName':self.testObjectForRateLimit['list'][listType]['groupDetails']['group_label']
            }
        communicationDetailObject = VenenoObject.communicationDetail(cdDetailsBody)
        communicationId = self.connObj.addMessageForRecipients(communicationDetailObject)
        communicationDetailBucketId = VenenoHelper.getCommunicationBucketId(communicationId)
        authorize.assertUserPresenceInSkippedTable(communicationId , VenenoHelper.getCommunicationBucketId(communicationId), constant.config['skipped_errors']['RATE_LIMIT_ERROR'], 'rate limit crossed for user')
        authorize.dbAssertRateLimitStats(self.testObjectForRateLimit['list'][listType]['campaignGroupRecipients']['TEST'], {'DAILY':1, 'WEEKLY':1, 'MONTHLY':1}, channel='EMAIL')
        
    @pytest.mark.parametrize('listType', [
        ('upload')
        ])
    def test_veneno_rateLimit_monthlyLimitExceed(self, listType):
        VenenoHelper.setupStrategy(daily=2, weekly=2, monthly=1, channel='EMAIL')
        self.listId = self.testObjectForRateLimit['list'][listType]['groupDetails']['id']
        cdDetailsBody = {
             'campaignId':self.campaignId,
             'communicationType':'EMAIL',
             'subject':'Automation Generated Body {{unsubscribe}}',
             'recipientListId':self.testObjectForRateLimit['list'][listType]['groupVersionDetails']['TEST']['id'],
             'overallRecipientCount':self.testObjectForRateLimit['list'][listType]['groupVersionDetails']['TEST']['customer_count'],
             'expectedDeliveryCount':self.testObjectForRateLimit['list'][listType]['groupVersionDetails']['TEST']['customer_count'],
             'groupName':self.testObjectForRateLimit['list'][listType]['groupDetails']['group_label']
            }
        communicationDetailObject = VenenoObject.communicationDetail(cdDetailsBody)
        communicationId = self.connObj.addMessageForRecipients(communicationDetailObject)
        communicationDetailBucketId = VenenoHelper.getCommunicationBucketId(communicationId)
        authorize.assertUserPresenceInSkippedTable(communicationId , VenenoHelper.getCommunicationBucketId(communicationId), constant.config['skipped_errors']['RATE_LIMIT_ERROR'], 'rate limit crossed for user')
        authorize.dbAssertRateLimitStats(self.testObjectForRateLimit['list'][listType]['campaignGroupRecipients']['TEST'], {'DAILY':1, 'WEEKLY':1, 'MONTHLY':1}, channel='EMAIL')
        
    @pytest.mark.parametrize('listType', [
        ('upload')
        ])
    def test_veneno_rateLimit_dailyWeeklyMonthlyLimitExceed(self, listType):
        VenenoHelper.setupStrategy(daily=1, weekly=1, monthly=1, channel='EMAIL')
        self.listId = self.testObjectForRateLimit['list'][listType]['groupDetails']['id']
        cdDetailsBody = {
             'campaignId':self.campaignId,
             'communicationType':'EMAIL',
             'subject':'Automation Generated Body {{unsubscribe}}',
             'recipientListId':self.testObjectForRateLimit['list'][listType]['groupVersionDetails']['TEST']['id'],
             'overallRecipientCount':self.testObjectForRateLimit['list'][listType]['groupVersionDetails']['TEST']['customer_count'],
             'expectedDeliveryCount':self.testObjectForRateLimit['list'][listType]['groupVersionDetails']['TEST']['customer_count'],
             'groupName':self.testObjectForRateLimit['list'][listType]['groupDetails']['group_label']
            }
        communicationDetailObject = VenenoObject.communicationDetail(cdDetailsBody)
        communicationId = self.connObj.addMessageForRecipients(communicationDetailObject)
        communicationDetailBucketId = VenenoHelper.getCommunicationBucketId(communicationId)
        authorize.assertUserPresenceInSkippedTable(communicationId , VenenoHelper.getCommunicationBucketId(communicationId), constant.config['skipped_errors']['RATE_LIMIT_ERROR'], 'rate limit crossed for user')
        authorize.dbAssertRateLimitStats(self.testObjectForRateLimit['list'][listType]['campaignGroupRecipients']['TEST'], {'DAILY':1, 'WEEKLY':1, 'MONTHLY':1}, channel='EMAIL')
        
    @pytest.mark.parametrize('listType', [
        ('upload')
        ])
    def test_veneno_rateLimit_reconfig_allStrategySatisified(self, listType):
        VenenoHelper.setupStrategy(daily=2, weekly=2, monthly=2, channel='EMAIL')
        self.listId = self.testObjectForRateLimit['list'][listType]['groupDetails']['id']
        cdDetailsBody = {
             'campaignId':self.campaignId,
             'communicationType':'EMAIL',
             'subject':'Automation Generated Body {{unsubscribe}}',
             'recipientListId':self.testObjectForRateLimit['list'][listType]['groupVersionDetails']['TEST']['id'],
             'overallRecipientCount':self.testObjectForRateLimit['list'][listType]['groupVersionDetails']['TEST']['customer_count'],
             'expectedDeliveryCount':self.testObjectForRateLimit['list'][listType]['groupVersionDetails']['TEST']['customer_count'],
             'groupName':self.testObjectForRateLimit['list'][listType]['groupDetails']['group_label']
            }
        communicationDetailObject = VenenoObject.communicationDetail(cdDetailsBody)
        communicationId = self.connObj.addMessageForRecipients(communicationDetailObject)
        authorize.assertUserPresenceInNsAdminTable(communicationId , VenenoHelper.getCommunicationBucketId(communicationId), int(json.loads(self.testObjectForRateLimit['list'][listType]['groupVersionDetails']['TEST']['params'])['test_count']),testControlType='custom', verify=False,groupVersionId=cdDetailsBody['recipientListId'],channel='EMAIL')
        authorize.dbAssertRateLimitStats(self.testObjectForRateLimit['list'][listType]['campaignGroupRecipients']['TEST'], {'DAILY':2, 'WEEKLY':2, 'MONTHLY':2}, channel='EMAIL')
        
    @pytest.mark.parametrize('listType', [
        ('upload')
        ])
    def test_veneno_rateLimit_reconfig_allStrategySatisified_StatsUpdateCheck(self, listType):
        VenenoHelper.setupStrategy(daily=3, weekly=3, monthly=3, channel='EMAIL')
        self.listId = self.testObjectForRateLimit['list'][listType]['groupDetails']['id']
        cdDetailsBody = {
             'campaignId':self.campaignId,
             'communicationType':'EMAIL',
             'subject':'Automation Generated Body {{unsubscribe}}',
             'recipientListId':self.testObjectForRateLimit['list'][listType]['groupVersionDetails']['TEST']['id'],
             'overallRecipientCount':self.testObjectForRateLimit['list'][listType]['groupVersionDetails']['TEST']['customer_count'],
             'expectedDeliveryCount':self.testObjectForRateLimit['list'][listType]['groupVersionDetails']['TEST']['customer_count'],
             'groupName':self.testObjectForRateLimit['list'][listType]['groupDetails']['group_label']
            }
        communicationDetailObject = VenenoObject.communicationDetail(cdDetailsBody)
        communicationId = self.connObj.addMessageForRecipients(communicationDetailObject)
        authorize.assertUserPresenceInNsAdminTable(communicationId , VenenoHelper.getCommunicationBucketId(communicationId), int(json.loads(self.testObjectForRateLimit['list'][listType]['groupVersionDetails']['TEST']['params'])['test_count']),testControlType='custom', verify=False,groupVersionId=cdDetailsBody['recipientListId'],channel='EMAIL')
        authorize.dbAssertRateLimitStats(self.testObjectForRateLimit['list'][listType]['campaignGroupRecipients']['TEST'], {'DAILY':3, 'WEEKLY':3, 'MONTHLY':3}, channel='EMAIL')
    
    @pytest.mark.parametrize('listType', [
        ('upload')
        ])   
    def test_veneno_rateLimit_dailyByPass(self, listType):
        VenenoHelper.setupStrategy(daily=3, weekly=4, monthly=4, channel='EMAIL')
        VenenoHelper.updateWindowValueToByPassStrategy(self.testObjectForRateLimit['list'][listType]['campaignGroupRecipients']['TEST'], 'DAILY', channel='EMAIL')
        self.listId = self.testObjectForRateLimit['list'][listType]['groupDetails']['id']
        cdDetailsBody = {
             'campaignId':self.campaignId,
             'communicationType':'EMAIL',
             'subject':'Automation Generated Body {{unsubscribe}}',
             'recipientListId':self.testObjectForRateLimit['list'][listType]['groupVersionDetails']['TEST']['id'],
             'overallRecipientCount':self.testObjectForRateLimit['list'][listType]['groupVersionDetails']['TEST']['customer_count'],
             'expectedDeliveryCount':self.testObjectForRateLimit['list'][listType]['groupVersionDetails']['TEST']['customer_count'],
             'groupName':self.testObjectForRateLimit['list'][listType]['groupDetails']['group_label']
            }
        communicationDetailObject = VenenoObject.communicationDetail(cdDetailsBody)
        communicationId = self.connObj.addMessageForRecipients(communicationDetailObject)
        authorize.assertUserPresenceInNsAdminTable(communicationId , VenenoHelper.getCommunicationBucketId(communicationId), int(json.loads(self.testObjectForRateLimit['list'][listType]['groupVersionDetails']['TEST']['params'])['test_count']),testControlType='custom', verify=False,groupVersionId=cdDetailsBody['recipientListId'],channel='EMAIL')
        authorize.dbAssertRateLimitStats(self.testObjectForRateLimit['list'][listType]['campaignGroupRecipients']['TEST'], {'DAILY':1, 'WEEKLY':4, 'MONTHLY':4}, channel='EMAIL')
    
    @pytest.mark.parametrize('listType', [
        ('upload')
        ])   
    def test_veneno_rateLimit_weeklyByPass(self, listType):
        VenenoHelper.setupStrategy(daily=2, weekly=1, monthly=5, channel='EMAIL')
        VenenoHelper.updateWindowValueToByPassStrategy(self.testObjectForRateLimit['list'][listType]['campaignGroupRecipients']['TEST'], 'WEEKLY', channel='EMAIL')
        self.listId = self.testObjectForRateLimit['list'][listType]['groupDetails']['id']
        cdDetailsBody = {
             'campaignId':self.campaignId,
             'communicationType':'EMAIL',
             'subject':'Automation Generated Body {{unsubscribe}}',
             'recipientListId':self.testObjectForRateLimit['list'][listType]['groupVersionDetails']['TEST']['id'],
             'overallRecipientCount':self.testObjectForRateLimit['list'][listType]['groupVersionDetails']['TEST']['customer_count'],
             'expectedDeliveryCount':self.testObjectForRateLimit['list'][listType]['groupVersionDetails']['TEST']['customer_count'],
             'groupName':self.testObjectForRateLimit['list'][listType]['groupDetails']['group_label']
            }
        communicationDetailObject = VenenoObject.communicationDetail(cdDetailsBody)
        communicationId = self.connObj.addMessageForRecipients(communicationDetailObject)
        authorize.assertUserPresenceInNsAdminTable(communicationId , VenenoHelper.getCommunicationBucketId(communicationId), int(json.loads(self.testObjectForRateLimit['list'][listType]['groupVersionDetails']['TEST']['params'])['test_count']),testControlType='custom', verify=False,groupVersionId=cdDetailsBody['recipientListId'],channel='EMAIL')
        authorize.dbAssertRateLimitStats(self.testObjectForRateLimit['list'][listType]['campaignGroupRecipients']['TEST'], {'DAILY':2, 'WEEKLY':1, 'MONTHLY':5}, channel='EMAIL')
    
    @pytest.mark.parametrize('listType', [
        ('upload')
        ])   
    def test_veneno_rateLimit_MonthlyByPass(self, listType):
        VenenoHelper.setupStrategy(daily=3, weekly=2, monthly=1, channel='EMAIL')
        VenenoHelper.updateWindowValueToByPassStrategy(self.testObjectForRateLimit['list'][listType]['campaignGroupRecipients']['TEST'], 'MONTHLY', channel='EMAIL')
        self.listId = self.testObjectForRateLimit['list'][listType]['groupDetails']['id']
        cdDetailsBody = {
             'campaignId':self.campaignId,
             'communicationType':'EMAIL',
             'subject':'Automation Generated Body {{unsubscribe}}',
             'recipientListId':self.testObjectForRateLimit['list'][listType]['groupVersionDetails']['TEST']['id'],
             'overallRecipientCount':self.testObjectForRateLimit['list'][listType]['groupVersionDetails']['TEST']['customer_count'],
             'expectedDeliveryCount':self.testObjectForRateLimit['list'][listType]['groupVersionDetails']['TEST']['customer_count'],
             'groupName':self.testObjectForRateLimit['list'][listType]['groupDetails']['group_label']
            }
        communicationDetailObject = VenenoObject.communicationDetail(cdDetailsBody)
        communicationId = self.connObj.addMessageForRecipients(communicationDetailObject)
        authorize.assertUserPresenceInNsAdminTable(communicationId , VenenoHelper.getCommunicationBucketId(communicationId), int(json.loads(self.testObjectForRateLimit['list'][listType]['groupVersionDetails']['TEST']['params'])['test_count']), testControlType='custom',verify=False,groupVersionId=cdDetailsBody['recipientListId'],channel='EMAIL')
        authorize.dbAssertRateLimitStats(self.testObjectForRateLimit['list'][listType]['campaignGroupRecipients']['TEST'], {'DAILY':3, 'WEEKLY':2, 'MONTHLY':1}, channel='EMAIL')
    
    

