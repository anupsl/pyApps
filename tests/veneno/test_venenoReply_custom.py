import pytest, time
from src.Constant.constant import constant
from src.utilities.logger import Logger
from src.modules.iris.authorize import authorize
from src.modules.iris.message import campaignMessage
from src.utilities.utils import Utils
from src.modules.iris.dbCallsAuthorize import dbCallsAuthorize
from src.utilities.assertion import Assertion
from src.modules.veneno.venenoHelper import VenenoHelper

@pytest.mark.run(order=10)
@pytest.mark.skipif(constant.config['cluster'] not in ['nightly'], reason='cron for monitor status more 10mins')
class Test_VenenoReply_CUSTOM():

    def setup_class(self):
        self.Details = {}
        self.listOfReplyMessage = constant.listOfReplyMessage
        self.first = True
        self.testConfig = constant.testConfig
        self.testControlType = 'custom'
        campaignDict = VenenoHelper.preRequisitesForVenenoReply(testControlType=self.testControlType)
        self.campaignId = campaignDict['campaignId']
        constant.config['campaignId'] = self.campaignId
        self.listId = campaignDict['listId']
        self.strategy = campaignDict['strategy']
        self.programeId = campaignDict['programeId']
        self.allocationStrategyId = campaignDict['allocationStrategyId']
        self.expiryStrategyId = campaignDict['expiryStrategyId']
        self.bucketId = campaignDict['bucketId']
        self.groupVersionResult = campaignDict['groupVersionResult']
        for replyType, errorConfig in zip(self.listOfReplyMessage, self.testConfig):

            errorConfig[1].update({'description' : replyType})
            self.voucherId = VenenoHelper.createCouponLuci(self,errorConfig[1])
            self.Details[replyType] = {'voucherId' : self.voucherId}
            if self.first:
                self.mutualIds = '[' + str(self.voucherId) + ']'
                self.first = False
            if replyType == 'COUPON_PRESENT_IN_MUTUAL_EXCLUSIVE_SERIES':
                errorConfig[1].update({'mutual_exclusive_series_ids' : self.mutualIds})
            if replyType == 'COUPON_EXPIRED':
                errorConfig[1].update({'fixedExpiryDate' : Utils.getTime(days=-1, milliSeconds=True)})
            Logger.log('Campaign Details : ', errorConfig[0], errorConfig[1])
            VenenoHelper.constructReplyCampaignDetails(self, replyType, errorConfig[0], errorConfig[1])

    def setup_method(self, method):
        Logger.logMethodName(str(method.__name__))


    @pytest.mark.parametrize('description, couponConfig, skippedReason, configChange', [('COUPONS_EXHAUSTED', {'client_handling_type': 'DISC_CODE_PIN'}, ['COUPONS_EXHAUSTED', 'coupons exhausted'] ,{'client_handling_type': 'DISC_CODE'})])
    def test_veneno_replyMessage_CUSTOM_Sanity(self, description, couponConfig, skippedReason, configChange):
        couponConfig.update({'description' : description})
        self.voucherId = VenenoHelper.createCouponLuci(self,couponConfig)
        communicationDetailsId, communicationDetailBucketId, communicationDetailExpectedCount = VenenoHelper.messageAuthorize(self, skippedError=skippedReason, isSkippedMessage=True)
        VenenoHelper.couponConfigChange(self, configChange)
        time.sleep(2)
        self.commDetailsId = communicationDetailsId
        authorize.dbAssertionInSkippedReplyTables(communicationDetailsId)
        campaignMessage.replyMessage(self)
        time.sleep(10)
        campaignReplyStats = dbCallsAuthorize.getVenenoReplyStats(communicationDetailsId)
        Assertion.constructAssertion(len(campaignReplyStats) != 0, 'Campaign Reply Stats update status {}'.format(len(campaignReplyStats)))
        authorize.assertUserPresenceInNsAdminTable(communicationDetailsId, communicationDetailBucketId, int(communicationDetailExpectedCount), verify=False, waitForInboxMsg=True)
        communcationDetailsDict = dbCallsAuthorize.getCommunicationDetailsWithId(communicationDetailsId)
        Assertion.constructAssertion(communcationDetailsDict['state'] == 'REPLAYED', 'Communication Details MessageId state is Actual: {} and Expected: {}'.format(communcationDetailsDict['state'], 'REPLAYED'))
        Assertion.constructAssertion(communcationDetailsDict['expected_delivery_count'] == int(communicationDetailExpectedCount), 'Communication Details Expected Delivery count Actual: {} and Expected: {}'.format(communcationDetailsDict['expected_delivery_count'] , int(communicationDetailExpectedCount)))
        Assertion.constructAssertion(communcationDetailsDict['message_queue_id'] != 0, 'Communication Details Message Queue Id is not 0 Actual: {}'.format(communcationDetailsDict['message_queue_id']))

    @pytest.mark.parametrize('description, changeCouponConfig', [
        ('COUPON_ALREADY_ISSUED', {'do_not_resend_existing_voucher': False}),
        ('MAX_COUPON_ISSUAL_PER_USER_EXCEEDED', {'do_not_resend_existing_voucher': False}),
        ('DAYS_BETWEEN_ISSUAL_LESS_THAN_MIN_DAYS_CONFIGURED', {'do_not_resend_existing_voucher': True, 'min_days_between_vouchers' :-1}),
        ('MAX_COUPON_ISSUAL_PER_SERIES_EXCEEDED', {'max_create' :-1}),
        ('REDEMPTION_VALID_START_DATE_AFTER_SERIES_EXPIRY', {'redemption_valid_after_days' : 0}),
        ('INVALID_ISSUAL_STORE_ID', {'store_ids_json' : '[-1]'}),
        ('COUPONS_EXHAUSTED', {'client_handling_type' : 'DISC_CODE'}),
        ('COUPON_PRESENT_IN_MUTUAL_EXCLUSIVE_SERIES', {'mutual_exclusive_series_ids' : '[-1]'}),
        ('COUPON_EXPIRED', {}),
        ])
    def test_veneno_replyMessage_CUSTOM_allErrorTypes(self, description, changeCouponConfig):
        Logger.log(self.Details[description])
        if description == 'COUPON_EXPIRED':
            changeCouponConfig.update({'fixedExpiryDate' : Utils.getTime(days=2, milliSeconds=True)})
        self.voucherId = self.Details[description]['voucherId']
        self.commDetailsId = self.Details[description]['communicationDetailsId']
        VenenoHelper.couponConfigChange(self, changeCouponConfig)
        time.sleep(70)
        authorize.dbAssertionInSkippedReplyTables(self.commDetailsId)
        campaignMessage.replyMessage(self)
        time.sleep(10)
        campaignReplyStats = dbCallsAuthorize.getVenenoReplyStats(self.Details[description]['communicationDetailsId'])
        Assertion.constructAssertion(len(campaignReplyStats) != 0, 'Campaign Reply Stats update status {}'.format(len(campaignReplyStats)))
        authorize.assertUserPresenceInNsAdminTable(self.Details[description]['communicationDetailsId'], self.Details[description]['communicationDetailBucketId'], int(self.Details[description]['communicationDetailExpectedCount']), verify=False, waitForInboxMsg=True)
        communcationDetailsDict = dbCallsAuthorize.getCommunicationDetailsWithId(self.Details[description]['communicationDetailsId']);
        Assertion.constructAssertion(communcationDetailsDict['state'] == 'REPLAYED', 'Communication Details MessageId state is Actual: {} and Expected: {}'.format(communcationDetailsDict['state'], 'REPLAYED'))
        Assertion.constructAssertion(communcationDetailsDict['expected_delivery_count'] == int(self.Details[description]['communicationDetailExpectedCount']), 'Communication Details Expected Delivery count Actual: {} and Expected: {}'.format(communcationDetailsDict['expected_delivery_count'], int(self.Details[description]['communicationDetailExpectedCount'])))
        Assertion.constructAssertion(communcationDetailsDict['message_queue_id'] != 0, 'Communication Details Message Queue Id is not 0 Actual: {}'.format(communcationDetailsDict['message_queue_id']))