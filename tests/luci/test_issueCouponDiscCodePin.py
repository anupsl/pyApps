import time, random, pytest
from src.Constant.constant import constant
from src.modules.luci.luciDBHelper import LuciDBHelper
from src.utilities.logger import Logger
from src.utilities.assertion import Assertion
from src.utilities.utils import Utils
from src.modules.luci.luciHelper import LuciHelper
from src.modules.luci.luciObject import LuciObject
from src.modules.luci.dracarysHelper import DracarysHelper
from src.modules.luci.dracarysObject import DracarysObject

class Test_IssueCouponDiscCodePin():

    def setup_class(self):
        Logger.logSuiteName(str(self).split('.')[-1])
        self.constructObj = LuciObject()
        self.DracarysObj = DracarysObject()
        self.userId = constant.config['usersInfo'][0]['userId']
        self.tillId = constant.config['tillIds'][0]


    def setup_method(self, method):
        self.connObj = LuciHelper.getConnObj(newConnection=True)
        Logger.logMethodName(method.__name__)
        constant.config['uploadedFileName'] = method.__name__
        self.DracraysConnObj = DracarysHelper.getConnObj(newConnection=True)
        constant.config['requestId'] = 'luci_auto_'+str(random.randint(11111, 99999))


    @pytest.mark.parametrize('description', [('Issue DCP with Valid Params')])
    def test_LUCI_IC_DCP_011(self, description):
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self)
        LuciHelper.queuePumpWait(self, couponSeriesId)

        # Checking Coupon Created Count
        createdCouponCount = LuciDBHelper.getCouponsCreated_Count(couponSeriesId, 1)
        Assertion.constructAssertion(createdCouponCount != 0, 'Coupon Code Pumped to Queue')
        Assertion.constructAssertion(self.connObj.getQueueSize(constant.config['orgId'], couponSeriesId, constant.config['requestId']) != 0, 'Coupon Code Pumped to Queue')

        #Update the coupon series from DC -> DCP
        couponConfigObj.update({'client_handling_type' : 'DISC_CODE_PIN'})
        LuciHelper.saveCouponConfigAndAssertions(self,couponConfigReq=couponConfigObj)

        #Checking Queue count and coupons_created count once update DC -> DCP
        createdCouponCount = LuciDBHelper.getCouponsCreated_Count(couponSeriesId,1)
        Assertion.constructAssertion(createdCouponCount == 0, 'Disc Code Marked as Invalid')

        Assertion.constructAssertion(self.connObj.getQueueSize(constant.config['orgId'], couponSeriesId, constant.config['requestId']) == 0, 'Coupon codes are cleared from queue')

        # upload the coupon code
        LuciHelper.uploadCouponAndAssertions(self, couponSeriesId, self.constructObj.importType['NONE'])

        # Checking Coupon Count once DCP uploaded +1
        time.sleep(2)
        createdCouponCount = LuciDBHelper.getCouponsCreated_Count(couponSeriesId, 1)
        Assertion.constructAssertion(createdCouponCount == 1, 'Uploaded coupons are recorded in coupons_created')
        Assertion.constructAssertion(self.connObj.getQueueSize(constant.config['orgId'], couponSeriesId, constant.config['requestId']) == 1, 'Coupon Code Pumped to Queue')

        LuciHelper.issueCouponAndAssertions(self,couponSeriesId)
        Assertion.constructAssertion(self.connObj.getQueueSize(constant.config['orgId'], couponSeriesId, constant.config['requestId']) == 0, 'All DCP Coupons are issued')

    @pytest.mark.parametrize('description', [('Upload one coupon and Issue two different users')])
    def test_LUCI_IC_DCP_012(self, description):
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self)
        LuciHelper.queuePumpWait(self, couponSeriesId)

        # Checking Coupon Created Count
        createdCouponCount = LuciDBHelper.getCouponsCreated_Count(couponSeriesId, 1)
        Assertion.constructAssertion(createdCouponCount != 0, 'Coupon Code Pumped to Queue')
        Assertion.constructAssertion(self.connObj.getQueueSize(constant.config['orgId'], couponSeriesId, constant.config['requestId']) != 0, 'Coupon Code Pumped to Queue')

        #Update the coupon series from DC -> DCP
        couponConfigObj.update({'client_handling_type' : 'DISC_CODE_PIN'})
        LuciHelper.saveCouponConfigAndAssertions(self,couponConfigReq=couponConfigObj)

        #Checking Queue count and coupons_created count once update DC -> DCP
        time.sleep(2)
        createdCouponCount = LuciDBHelper.getCouponsCreated_Count(couponSeriesId,1)
        Assertion.constructAssertion(createdCouponCount == 0, 'Disc Code Marked as Invalid')
        Assertion.constructAssertion(self.connObj.getQueueSize(constant.config['orgId'], couponSeriesId, constant.config['requestId']) == 0, 'Coupon codes are cleared from queue')

        # upload the coupon code
        LuciHelper.uploadCouponAndAssertions(self,couponSeriesId, self.constructObj.importType['NONE'])

        # Checking Coupon Count once DCP uploaded +1
        time.sleep(2)
        createdCouponCount = LuciDBHelper.getCouponsCreated_Count(couponSeriesId, 1)
        Assertion.constructAssertion(createdCouponCount == 1, 'Uploaded coupons are recorded in coupons_created')
        Assertion.constructAssertion(self.connObj.getQueueSize(constant.config['orgId'], couponSeriesId, constant.config['requestId']) == 1, 'Coupon Code Pumped to Queue')

        LuciHelper.issueCouponAndAssertions(self,couponSeriesId)
        luciExp = LuciHelper.issueCouponAndAssertions(self, couponSeriesId, {'userId': constant.config['usersInfo'][1]['userId']}, expectException=True)
        Assertion.constructAssertion(luciExp['errorCode'] == constant.COUPONS_EXHAUSTED, 'Luci Exception error code Actual: {} and Expected: {}'.format(luciExp['errorCode'], constant.COUPONS_EXHAUSTED))
        Assertion.constructAssertion(luciExp['errorMsg'] ==  'coupons exhausted', 'Luci Exception Error Msg Actual : {}'.format(luciExp['errorMsg']))

    @pytest.mark.parametrize('description', [('Issue same coupon twice with config Do not resend existing voucher false & allow multiple voucher false')])
    def test_LUCI_IC_DCP_013(self, description):
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self, {'client_handling_type' : 'DISC_CODE_PIN', })

        createdCouponCount = LuciDBHelper.getCouponsCreated_Count(couponSeriesId,1)
        Assertion.constructAssertion(createdCouponCount == 0, 'Coupons are created for DCP')
        Assertion.constructAssertion(self.connObj.getQueueSize(constant.config['orgId'], couponSeriesId, constant.config['requestId']) == 0, 'Coupons not pumped to queue')

        # upload the coupon code
        LuciHelper.uploadCouponAndAssertions(self,couponSeriesId, self.constructObj.importType['NONE'])

        LuciHelper.issueCouponAndAssertions(self,couponSeriesId)
        LuciHelper.issueCouponAndAssertions(self, couponSeriesId, couponIssuedCount=2)
        # couponSentHistoryList = LuciDBHelper.getCouponSentHistoryList(couponSeriesId);
        # Assertion.constructAssertion(couponSentHistoryList[1]['notes'] == 'RESENT', 'Coupon_sent_history Notes Actual : {} and Expected : RESENT'.format(couponSentHistoryList[1]['notes']))

    @pytest.mark.parametrize('description', [('Issue multiple coupons per user with the max coupon limits')])
    def test_LUCI_IC_DCP_014(self, description):
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self, {'client_handling_type' : 'DISC_CODE_PIN', 'do_not_resend_existing_voucher' : True, 'allow_multiple_vouchers_per_user' : True, 'max_vouchers_per_user' : 3})

        createdCouponCount = LuciDBHelper.getCouponsCreated_Count(couponSeriesId,1)
        Assertion.constructAssertion(createdCouponCount == 0, 'Coupons are created for DCP')
        Assertion.constructAssertion(self.connObj.getQueueSize(constant.config['orgId'], couponSeriesId, constant.config['requestId']) == 0, 'Coupons not pumped to queue')

        # upload the coupon code
        LuciHelper.uploadCouponAndAssertions(self,couponSeriesId, self.constructObj.importType['NONE'], noOfCouponsToBeUpload = 3)

        LuciHelper.issueCouponAndAssertions(self,couponSeriesId)
        LuciHelper.issueCouponAndAssertions(self,couponSeriesId)
        LuciHelper.issueCouponAndAssertions(self,couponSeriesId)
        luciExp = LuciHelper.issueCouponAndAssertions(self, couponSeriesId, expectException=True)
        Assertion.constructAssertion(luciExp['errorCode'] == constant.MAX_COUPON_ISSUAL_PER_USER_EXCEEDED, 'Luci Exception error code Actual: {} and Expected: {}'.format(luciExp['errorCode'], constant.MAX_COUPON_ISSUAL_PER_USER_EXCEEDED))
        Assertion.constructAssertion(luciExp['errorMsg'] == 'max coupon per user exceeded', 'Luci Exception Error Msg Actual : {}'.format(luciExp['errorMsg']))

    @pytest.mark.parametrize('description', [('Issue same coupon twice with config Do not resend existing voucher True & allow multiple voucher false')])
    def test_LUCI_IC_DCP_015(self, description):
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self, {'client_handling_type' : 'DISC_CODE_PIN', 'do_not_resend_existing_voucher' : True, 'allow_multiple_vouchers_per_user' : False})

        createdCouponCount = LuciDBHelper.getCouponsCreated_Count(couponSeriesId,1)
        Assertion.constructAssertion(createdCouponCount == 0, 'Coupons are created for DCP')
        Assertion.constructAssertion(self.connObj.getQueueSize(constant.config['orgId'], couponSeriesId, constant.config['requestId']) == 0, 'Coupons not pumped to queue')

        # upload the coupon code
        LuciHelper.uploadCouponAndAssertions(self,couponSeriesId, self.constructObj.importType['NONE'])

        LuciHelper.issueCouponAndAssertions(self,couponSeriesId)
        luciExp = LuciHelper.issueCouponAndAssertions(self, couponSeriesId, expectException=True)
        Assertion.constructAssertion(luciExp['errorCode'] == constant.COUPON_ALREADY_ISSUED, 'Luci Exception error code Actual: {} and Expected: {}'.format(luciExp['errorCode'], constant.COUPON_ALREADY_ISSUED))
        Assertion.constructAssertion(luciExp['errorMsg'] == 'user already has a coupon', 'Luci Exception Error Msg Actual : {}'.format(luciExp['errorMsg']))

    @pytest.mark.parametrize('description', [('Issue same coupon twice with config Do not resend existing voucher false & allow multiple voucher True')])
    def test_LUCI_IC_DCP_016(self, description):
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self, {'client_handling_type' : 'DISC_CODE_PIN', 'do_not_resend_existing_voucher' : False, 'allow_multiple_vouchers_per_user' : True})

        createdCouponCount = LuciDBHelper.getCouponsCreated_Count(couponSeriesId,1)
        Assertion.constructAssertion(createdCouponCount == 0, 'Coupons are created for DCP')
        Assertion.constructAssertion(self.connObj.getQueueSize(constant.config['orgId'], couponSeriesId, constant.config['requestId']) == 0, 'Coupons not pumped to queue')

        # upload the coupon code
        LuciHelper.uploadCouponAndAssertions(self,couponSeriesId, self.constructObj.importType['NONE'])

        LuciHelper.issueCouponAndAssertions(self,couponSeriesId)
        LuciHelper.issueCouponAndAssertions(self, couponSeriesId, couponIssuedCount=2)
        # couponSentHistoryList = LuciDBHelper.getCouponSentHistoryList(couponSeriesId);
        # Assertion.constructAssertion(couponSentHistoryList[1]['notes'] == 'RESENT', 'Coupon_sent_history Notes Actual : {} and Expected : RESENT'.format(couponSentHistoryList[1]['notes']))

    @pytest.mark.parametrize('description', [('Issue coupon without upload coupons')])
    def test_LUCI_IC_DCP_017(self, description):
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self, {'client_handling_type' : 'DISC_CODE_PIN'})
        createdCouponCount = LuciDBHelper.getCouponsCreated_Count(couponSeriesId,1)
        Assertion.constructAssertion(createdCouponCount == 0, 'Coupons are created for DCP')
        Assertion.constructAssertion(self.connObj.getQueueSize(constant.config['orgId'], couponSeriesId, constant.config['requestId']) == 0, 'Coupons not pumped to queue')

        luciExp = LuciHelper.issueCouponAndAssertions(self, couponSeriesId, expectException=True)
        Assertion.constructAssertion(luciExp['errorCode'] == constant.COUPONS_EXHAUSTED, 'Luci Exception error code Actual: {} and Expected: {}'.format(luciExp['errorCode'], constant.COUPONS_EXHAUSTED))
        Assertion.constructAssertion(luciExp['errorMsg'] == 'coupons exhausted', 'Luci Exception Error Msg Actual : {}'.format(luciExp['errorMsg']))

    @pytest.mark.parametrize('description', [('set max create 1 and issue 2 coupons')])
    def test_LUCI_IC_DCP_018(self, description):
        actualUserId = self.userId
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self, {'client_handling_type': 'DISC_CODE_PIN', 'max_create': 1})

        createdCouponCount = LuciDBHelper.getCouponsCreated_Count(couponSeriesId, 1)
        Assertion.constructAssertion(createdCouponCount == 0, 'Coupons are created for DCP')
        Assertion.constructAssertion(self.connObj.getQueueSize(constant.config['orgId'], couponSeriesId, constant.config['requestId']) == 0, 'Coupons not pumped to queue')

        # upload the coupon code
        LuciHelper.uploadCouponAndAssertions(self, couponSeriesId, self.constructObj.importType['NONE'], noOfCouponsToBeUpload = 1)

        LuciHelper.issueCouponAndAssertions(self, couponSeriesId)
        self.userId = constant.config['usersInfo'][1]['userId']
        luciExp = LuciHelper.issueCouponAndAssertions(self, couponSeriesId, expectException=True)
        Assertion.constructAssertion(luciExp['errorCode'] == constant.MAX_COUPON_ISSUAL_PER_SERIES_EXCEEDED, 'Luci Exception error code Actual: {} and Expected: {}'.format(luciExp['errorCode'], constant.MAX_COUPON_ISSUAL_PER_SERIES_EXCEEDED))
        Assertion.constructAssertion(luciExp['errorMsg'] == 'max create for series exceeded', 'Luci Exception Error Msg Actual : {}'.format(luciExp['errorMsg']))
        self.userId = actualUserId

    @pytest.mark.parametrize('description, invalidInput, expected', [
        ('Issue coupon with Invalid orgId', {'orgId' : 9999}, [constant.INVALID_ORG_ID, 'invalid org id']),
        ('Issue coupon with Negative orgId', {'orgId' : -1}, [constant.INVALID_ORG_ID, 'invalid org id -1']),
        ('Issue coupon with Invalid CouponSeries Id', {'couponSeriesId' : -1}, [constant.INVALID_COUPON_SERIES_ID, 'invalid series id -1']),
        ('Issue coupon with Invalid storeUnit Id', {'storeUnitId' : -1}, [constant.INVALID_ISSUAL_STORE_ID, 'invalid store id -1']),
        ('Issue coupon with Invalid userId', {'userId' : -1}, [constant.INVALID_USER_ID, 'invalid user id -1'])])
    def test_LUCI_IC_DCP_020(self, description, invalidInput, expected):
        try:
            couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self, {'client_handling_type': 'DISC_CODE_PIN'})
            # upload the coupon code
            LuciHelper.uploadCouponAndAssertions(self, couponSeriesId, self.constructObj.importType['NONE'])

            LuciHelper.issueCouponAndAssertions(self, couponSeriesId, issueCouponParamObj=invalidInput)
        except Exception, luciExp:
            luciExp = luciExp.__dict__;
            Assertion.constructAssertion(luciExp['errorCode'] == expected[0], 'Luci Exception error code Actual: {} and Expected: {}'.format(luciExp['errorCode'], expected[0]))
            Assertion.constructAssertion(luciExp['errorMsg'] == expected[1], 'Luci Exception Error Msg Actual : {}'.format(luciExp['errorMsg']))

    @pytest.mark.parametrize('description', [('Queue Size checking while create & update coupon series and after issual coupon')])
    def test_LUCI_IC_DCP_025_sanity(self, description):
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self, couponConfigReq = {'client_handling_type' : 'DISC_CODE_PIN'})
        time.sleep(2)
        LuciHelper.couponPumpAssertion(self,couponSeriesId,isDiscCode=False)
        LuciHelper.uploadCouponAndAssertions(self,couponSeriesId,self.constructObj.importType['NONE'])

        time.sleep(2)
        createdCouponCount = LuciDBHelper.getCouponsCreated_Count(couponSeriesId,1)
        Assertion.constructAssertion(createdCouponCount == 1, 'Uploaded coupons are recorded in coupons_created')
        Assertion.constructAssertion(self.connObj.getQueueSize(constant.config['orgId'], couponSeriesId,constant.config['requestId']) == 1, 'Coupon Code Pumped to Queue')

        #Update Coupon series & issue coupon check queue size
        LuciHelper.saveCouponConfigAndAssertions(self, couponConfigReq=couponConfigObj)
        Assertion.constructAssertion(self.connObj.getQueueSize(constant.config['orgId'], couponSeriesId,constant.config['requestId']) == 1, 'Coupon Code Pumped to Queue')
        LuciHelper.issueCouponAndAssertions(self, couponSeriesId)
        Assertion.constructAssertion(self.connObj.getQueueSize(constant.config['orgId'], couponSeriesId, constant.config['requestId']) == 0, 'Coupon Queue count deducted with No. of Issued Coupons')