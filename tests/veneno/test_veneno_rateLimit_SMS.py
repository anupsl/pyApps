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
@pytest.mark.run(order=5)
class Test_Veneno_RateLimit_SMS_ORG():
    
    def setup_class(self):
        Logger.logSuiteName(str(self).split('.')[-1])
        VenenoHelper.configRateLimit(enable=True, channel='SMS')
        VenenoHelper.setupStrategy(daily=1, weekly=2, monthly=3, channel='SMS')
        self.testObjectForRateLimit = VenenoHelper.preRequisitesForVenenoRateLimit('mobile')
        self.campaignId = self.testObjectForRateLimit['campaign']['id']
    
    def teardown_class(self):
        Logger.log('Disable Rate Limit Config')
        VenenoHelper.configRateLimit(enable=False, channel='SMS')
    
    @pytest.mark.parametrize('listType', [
        ('upload')
        ])
    def test_veneno_rateLimitsss_allStrategySatisified_sms_sanity(self, listType):
        self.listId = self.testObjectForRateLimit['list'][listType]['groupDetails']['id']
        authorizeResult = VenenoHelper.authorizeForRateLimit(self, listType)
        authorize.assertAuthorize(authorizeResult['authorizeResponse'], 200)
        communicationDetailId ,communicationDetailBucketId ,communicationDetailExpectedCount=authorize.assertMessageQueueAndGetCommunicationDetailsForReferenceMessageQueueId(self.campaignId,authorizeResult['groupVersionResult']['TEST']['id'],authorizeResult['messageId'])
        VenenoDBAssertion(self.campaignId, 'SMS', communicationDetailId, authorizeResult['groupVersionResult']['TEST']['customer_count'], authorizeResult['groupVersionResult']['TEST']['id'], authorizeResult['payload']['message']).check()
        authorize.assertUserPresenceInNsAdminTable(communicationDetailId , communicationDetailBucketId, int(communicationDetailExpectedCount))
        authorize.dbAssertRateLimitStats(self.testObjectForRateLimit['list'][listType]['campaignGroupRecipients']['TEST'], {'DAILY':1, 'WEEKLY':1, 'MONTHLY':1})
    
    @pytest.mark.parametrize('listType', [
        ('upload')
        ])    
    def test_veneno_rateLimitsss_dailyLimitExceed(self, listType):
        self.listId = self.testObjectForRateLimit['list'][listType]['groupDetails']['id']
        authorizeResult = VenenoHelper.authorizeForRateLimit(self, listType)
        authorize.assertAuthorize(authorizeResult['authorizeResponse'], 200)
        communicationDetailId ,communicationDetailBucketId, communicationDetailExpectedCount=authorize.assertMessageQueueAndGetCommunicationDetailsForReferenceMessageQueueId(self.campaignId,authorizeResult['groupVersionResult']['TEST']['id'],authorizeResult['messageId'])
        VenenoDBAssertion(self.campaignId, 'SMS', communicationDetailId, authorizeResult['groupVersionResult']['TEST']['customer_count'], authorizeResult['groupVersionResult']['TEST']['id'], authorizeResult['payload']['message'],skippedReasons=['rate limit crossed for user']).check()
        authorize.assertUserPresenceInSkippedTable(communicationDetailId, communicationDetailBucketId, constant.config['skipped_errors']['RATE_LIMIT_ERROR'], 'rate limit crossed for user')
        authorize.dbAssertRateLimitStats(self.testObjectForRateLimit['list'][listType]['campaignGroupRecipients']['TEST'], {'DAILY':1, 'WEEKLY':1, 'MONTHLY':1})
        
    @pytest.mark.parametrize('listType', [
        ('upload')
        ])
    def test_veneno_rateLimitsss_weeklyLimitExceed(self, listType):
        VenenoHelper.setupStrategy(daily=2, weekly=1, monthly=3)
        self.listId = self.testObjectForRateLimit['list'][listType]['groupDetails']['id']
        authorizeResult = VenenoHelper.authorizeForRateLimit(self, listType)
        authorize.assertAuthorize(authorizeResult['authorizeResponse'], 200)
        communicationDetailId ,communicationDetailBucketId, communicationDetailExpectedCount=authorize.assertMessageQueueAndGetCommunicationDetailsForReferenceMessageQueueId(self.campaignId,authorizeResult['groupVersionResult']['TEST']['id'],authorizeResult['messageId'])
        VenenoDBAssertion(self.campaignId, 'SMS', communicationDetailId, authorizeResult['groupVersionResult']['TEST']['customer_count'], authorizeResult['groupVersionResult']['TEST']['id'], authorizeResult['payload']['message'],skippedReasons=['rate limit crossed for user']).check()
        authorize.assertUserPresenceInSkippedTable(communicationDetailId, communicationDetailBucketId, constant.config['skipped_errors']['RATE_LIMIT_ERROR'], 'rate limit crossed for user')
        authorize.dbAssertRateLimitStats(self.testObjectForRateLimit['list'][listType]['campaignGroupRecipients']['TEST'], {'DAILY':1, 'WEEKLY':1, 'MONTHLY':1})
        
    @pytest.mark.parametrize('listType', [
        ('upload')
        ])
    def test_veneno_rateLimitsss_monthlyLimitExceed(self, listType):
        VenenoHelper.setupStrategy(daily=2, weekly=2, monthly=1)
        self.listId = self.testObjectForRateLimit['list'][listType]['groupDetails']['id']
        authorizeResult = VenenoHelper.authorizeForRateLimit(self, listType)
        authorize.assertAuthorize(authorizeResult['authorizeResponse'], 200)
        communicationDetailId ,communicationDetailBucketId, communicationDetailExpectedCount=authorize.assertMessageQueueAndGetCommunicationDetailsForReferenceMessageQueueId(self.campaignId,authorizeResult['groupVersionResult']['TEST']['id'],authorizeResult['messageId'])
        VenenoDBAssertion(self.campaignId, 'SMS', communicationDetailId, authorizeResult['groupVersionResult']['TEST']['customer_count'], authorizeResult['groupVersionResult']['TEST']['id'], authorizeResult['payload']['message'],skippedReasons=['rate limit crossed for user']).check()
        authorize.assertUserPresenceInSkippedTable(communicationDetailId, communicationDetailBucketId, constant.config['skipped_errors']['RATE_LIMIT_ERROR'], 'rate limit crossed for user')
        authorize.dbAssertRateLimitStats(self.testObjectForRateLimit['list'][listType]['campaignGroupRecipients']['TEST'], {'DAILY':1, 'WEEKLY':1, 'MONTHLY':1})
        
    @pytest.mark.parametrize('listType', [
        ('upload')
        ])
    def test_veneno_rateLimit_dailyWeeklyMonthlyLimitExceed(self, listType):
        VenenoHelper.setupStrategy(daily=1, weekly=1, monthly=1)
        self.listId = self.testObjectForRateLimit['list'][listType]['groupDetails']['id']
        authorizeResult = VenenoHelper.authorizeForRateLimit(self, listType)
        authorize.assertAuthorize(authorizeResult['authorizeResponse'], 200)
        communicationDetailId ,communicationDetailBucketId, communicationDetailExpectedCount=authorize.assertMessageQueueAndGetCommunicationDetailsForReferenceMessageQueueId(self.campaignId,authorizeResult['groupVersionResult']['TEST']['id'],authorizeResult['messageId'])
        VenenoDBAssertion(self.campaignId, 'SMS', communicationDetailId, authorizeResult['groupVersionResult']['TEST']['customer_count'], authorizeResult['groupVersionResult']['TEST']['id'], authorizeResult['payload']['message'],skippedReasons=['rate limit crossed for user']).check()
        authorize.assertUserPresenceInSkippedTable(communicationDetailId, communicationDetailBucketId, constant.config['skipped_errors']['RATE_LIMIT_ERROR'], 'rate limit crossed for user')
        authorize.dbAssertRateLimitStats(self.testObjectForRateLimit['list'][listType]['campaignGroupRecipients']['TEST'], {'DAILY':1, 'WEEKLY':1, 'MONTHLY':1})
        
    @pytest.mark.parametrize('listType', [
        ('upload')
        ])
    def test_veneno_rateLimit_reconfig_allStrategySatisified(self, listType):
        VenenoHelper.setupStrategy(daily=2, weekly=2, monthly=2)
        self.listId = self.testObjectForRateLimit['list'][listType]['groupDetails']['id']
        authorizeResult = VenenoHelper.authorizeForRateLimit(self, listType)
        authorize.assertAuthorize(authorizeResult['authorizeResponse'], 200)
        communicationDetailId ,communicationDetailBucketId ,communicationDetailExpectedCount=authorize.assertMessageQueueAndGetCommunicationDetailsForReferenceMessageQueueId(self.campaignId,authorizeResult['groupVersionResult']['TEST']['id'],authorizeResult['messageId'])
        VenenoDBAssertion(self.campaignId, 'SMS', communicationDetailId, authorizeResult['groupVersionResult']['TEST']['customer_count'], authorizeResult['groupVersionResult']['TEST']['id'], authorizeResult['payload']['message']).check()
        authorize.assertUserPresenceInNsAdminTable(communicationDetailId , communicationDetailBucketId, int(communicationDetailExpectedCount))
        authorize.dbAssertRateLimitStats(self.testObjectForRateLimit['list'][listType]['campaignGroupRecipients']['TEST'], {'DAILY':2, 'WEEKLY':2, 'MONTHLY':2})
        
    @pytest.mark.parametrize('listType', [
        ('upload')
        ])
    def test_veneno_rateLimit_reconfig_allStrategySatisified_StatsUpdateCheck(self, listType):
        VenenoHelper.setupStrategy(daily=3, weekly=3, monthly=3)
        self.listId = self.testObjectForRateLimit['list'][listType]['groupDetails']['id']
        authorizeResult = VenenoHelper.authorizeForRateLimit(self, listType)
        communicationDetailId ,communicationDetailBucketId ,communicationDetailExpectedCount=authorize.assertMessageQueueAndGetCommunicationDetailsForReferenceMessageQueueId(self.campaignId,authorizeResult['groupVersionResult']['TEST']['id'],authorizeResult['messageId'])
        VenenoDBAssertion(self.campaignId, 'SMS', communicationDetailId, authorizeResult['groupVersionResult']['TEST']['customer_count'], authorizeResult['groupVersionResult']['TEST']['id'], authorizeResult['payload']['message']).check()
        authorize.assertUserPresenceInNsAdminTable(communicationDetailId , communicationDetailBucketId, int(communicationDetailExpectedCount))
        authorize.dbAssertRateLimitStats(self.testObjectForRateLimit['list'][listType]['campaignGroupRecipients']['TEST'], {'DAILY':3, 'WEEKLY':3, 'MONTHLY':3})
    
    @pytest.mark.parametrize('listType', [
        ('upload')
        ])   
    def test_veneno_rateLimit_dailyByPass(self, listType):
        VenenoHelper.setupStrategy(daily=3, weekly=4, monthly=4)
        VenenoHelper.updateWindowValueToByPassStrategy(self.testObjectForRateLimit['list'][listType]['campaignGroupRecipients']['TEST'], 'DAILY')
        self.listId = self.testObjectForRateLimit['list'][listType]['groupDetails']['id']
        authorizeResult = VenenoHelper.authorizeForRateLimit(self, listType)
        communicationDetailId ,communicationDetailBucketId ,communicationDetailExpectedCount=authorize.assertMessageQueueAndGetCommunicationDetailsForReferenceMessageQueueId(self.campaignId,authorizeResult['groupVersionResult']['TEST']['id'],authorizeResult['messageId'])
        VenenoDBAssertion(self.campaignId, 'SMS', communicationDetailId, authorizeResult['groupVersionResult']['TEST']['customer_count'], authorizeResult['groupVersionResult']['TEST']['id'], authorizeResult['payload']['message']).check()
        authorize.assertUserPresenceInNsAdminTable(communicationDetailId , communicationDetailBucketId, int(communicationDetailExpectedCount))
        authorize.dbAssertRateLimitStats(self.testObjectForRateLimit['list'][listType]['campaignGroupRecipients']['TEST'], {'DAILY':1, 'WEEKLY':4, 'MONTHLY':4})
    
    @pytest.mark.parametrize('listType', [
        ('upload')
        ])   
    def test_veneno_rateLimit_weeklyByPass(self, listType):
        VenenoHelper.setupStrategy(daily=2, weekly=1, monthly=5)
        VenenoHelper.updateWindowValueToByPassStrategy(self.testObjectForRateLimit['list'][listType]['campaignGroupRecipients']['TEST'], 'WEEKLY')
        self.listId = self.testObjectForRateLimit['list'][listType]['groupDetails']['id']
        authorizeResult = VenenoHelper.authorizeForRateLimit(self, listType)
        communicationDetailId ,communicationDetailBucketId ,communicationDetailExpectedCount=authorize.assertMessageQueueAndGetCommunicationDetailsForReferenceMessageQueueId(self.campaignId,authorizeResult['groupVersionResult']['TEST']['id'],authorizeResult['messageId'])
        VenenoDBAssertion(self.campaignId, 'SMS', communicationDetailId, authorizeResult['groupVersionResult']['TEST']['customer_count'], authorizeResult['groupVersionResult']['TEST']['id'], authorizeResult['payload']['message']).check()
        authorize.assertUserPresenceInNsAdminTable(communicationDetailId , communicationDetailBucketId, int(communicationDetailExpectedCount))
        authorize.dbAssertRateLimitStats(self.testObjectForRateLimit['list'][listType]['campaignGroupRecipients']['TEST'], {'DAILY':2, 'WEEKLY':1, 'MONTHLY':5})
    
    @pytest.mark.parametrize('listType', [
        ('upload')
        ])   
    def test_veneno_rateLimit_MonthlyByPass(self, listType):
        VenenoHelper.setupStrategy(daily=3, weekly=2, monthly=1)
        VenenoHelper.updateWindowValueToByPassStrategy(self.testObjectForRateLimit['list'][listType]['campaignGroupRecipients']['TEST'], 'MONTHLY')
        self.listId = self.testObjectForRateLimit['list'][listType]['groupDetails']['id']
        authorizeResult = VenenoHelper.authorizeForRateLimit(self, listType)
        communicationDetailId ,communicationDetailBucketId ,communicationDetailExpectedCount=authorize.assertMessageQueueAndGetCommunicationDetailsForReferenceMessageQueueId(self.campaignId,authorizeResult['groupVersionResult']['TEST']['id'],authorizeResult['messageId'])
        VenenoDBAssertion(self.campaignId, 'SMS', communicationDetailId, authorizeResult['groupVersionResult']['TEST']['customer_count'], authorizeResult['groupVersionResult']['TEST']['id'], authorizeResult['payload']['message']).check()
        authorize.assertUserPresenceInNsAdminTable(communicationDetailId , communicationDetailBucketId, int(communicationDetailExpectedCount))
        authorize.dbAssertRateLimitStats(self.testObjectForRateLimit['list'][listType]['campaignGroupRecipients']['TEST'], {'DAILY':3, 'WEEKLY':2, 'MONTHLY':1})
    
    @pytest.mark.parametrize('listType', [
        ('upload')
        ])   
    def test_veneno_rateLimit_SetZero(self, listType):
        VenenoHelper.setupStrategy(daily=0, weekly=0, monthly=0)
        VenenoHelper.updateWindowValueToByPassStrategy(self.testObjectForRateLimit['list'][listType]['campaignGroupRecipients']['TEST'], 'MONTHLY')
        self.listId = self.testObjectForRateLimit['list'][listType]['groupDetails']['id']
        authorizeResult = VenenoHelper.authorizeForRateLimit(self, listType)
        communicationDetailId ,communicationDetailBucketId, communicationDetailExpectedCount=authorize.assertMessageQueueAndGetCommunicationDetailsForReferenceMessageQueueId(self.campaignId,authorizeResult['groupVersionResult']['TEST']['id'],authorizeResult['messageId'])
        VenenoDBAssertion(self.campaignId, 'SMS', communicationDetailId, authorizeResult['groupVersionResult']['TEST']['customer_count'], authorizeResult['groupVersionResult']['TEST']['id'], authorizeResult['payload']['message'],skippedReasons=['rate limit crossed for user']).check()
        authorize.assertUserPresenceInSkippedTable(communicationDetailId, communicationDetailBucketId, constant.config['skipped_errors']['RATE_LIMIT_ERROR'], 'rate limit crossed for user')
        authorize.dbAssertRateLimitStats(self.testObjectForRateLimit['list'][listType]['campaignGroupRecipients']['TEST'], {'DAILY':3, 'WEEKLY':2, 'MONTHLY':1})
    
    @pytest.mark.parametrize('listType', [
        ('upload')
        ])   
    def test_veneno_rateLimit_SetWithSomeNegativeValue(self, listType):
        VenenoHelper.setupStrategy(daily=-1, weekly=-1, monthly=-1)
        VenenoHelper.updateWindowValueToByPassStrategy(self.testObjectForRateLimit['list'][listType]['campaignGroupRecipients']['TEST'], 'MONTHLY')
        self.listId = self.testObjectForRateLimit['list'][listType]['groupDetails']['id']
        authorizeResult = VenenoHelper.authorizeForRateLimit(self, listType)
        communicationDetailId ,communicationDetailBucketId, communicationDetailExpectedCount=authorize.assertMessageQueueAndGetCommunicationDetailsForReferenceMessageQueueId(self.campaignId,authorizeResult['groupVersionResult']['TEST']['id'],authorizeResult['messageId'])
        VenenoDBAssertion(self.campaignId, 'SMS', communicationDetailId, authorizeResult['groupVersionResult']['TEST']['customer_count'], authorizeResult['groupVersionResult']['TEST']['id'], authorizeResult['payload']['message'],skippedReasons=['rate limit crossed for user']).check()
        authorize.assertUserPresenceInSkippedTable(communicationDetailId, communicationDetailBucketId, constant.config['skipped_errors']['RATE_LIMIT_ERROR'], 'rate limit crossed for user')
        authorize.dbAssertRateLimitStats(self.testObjectForRateLimit['list'][listType]['campaignGroupRecipients']['TEST'], {'DAILY':3, 'WEEKLY':2, 'MONTHLY':1})
    
