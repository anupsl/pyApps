import time, random,pytest
from src.Constant.constant import constant
from src.modules.luci.luciDBHelper import LuciDBHelper
from src.utilities.logger import Logger
from src.utilities.assertion import Assertion
from src.modules.luci.luciHelper import LuciHelper
from src.modules.luci.luciObject import LuciObject
from src.modules.luci.dracarysHelper import DracarysHelper
from src.modules.luci.dracarysObject import DracarysObject

class Test_IssueMultipleCouponsDiscCodePin():

    def setup_class(self):
        Logger.logSuiteName(str(self).split('.')[-1])
        self.constructObj = LuciObject()
        self.userIds = []
        self.bulkUserIds = []
        self.DracarysObj = DracarysObject()
        for i in range(len(constant.config['usersInfo'])):
            self.userIds.append(constant.config['usersInfo'][i]['userId'])
        self.tillId = constant.config['tillIds'][0]


    def setup_method(self, method):
        self.connObj = LuciHelper.getConnObj(newConnection=True)
        Logger.logMethodName(method.__name__)
        constant.config['uploadedFileName'] = method.__name__
        self.DracraysConnObj = DracarysHelper.getConnObj(newConnection=True)
        constant.config['requestId'] = 'luci_auto_'+str(random.randint(11111, 99999))

    @pytest.mark.parametrize('description' , ['With all the valid parameters'])
    def test_LUCI_IMC_DCP_011_sanity_smoke(self, description):
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self, couponConfigReq={'client_handling_type' : 'DISC_CODE_PIN'})
        LuciHelper.couponPumpAssertion(self,couponSeriesId,False)
        noOfCouponUpload = 10

        LuciHelper.uploadCouponAndAssertions(self,couponSeriesId, self.constructObj.importType['NONE'], noOfCouponsToBeUpload=noOfCouponUpload)

        time.sleep(2)
        LuciHelper.couponPumpAssertion(self,couponSeriesId,isDiscCode=False, DiscCodePinCouponUploaded=noOfCouponUpload)

        LuciHelper.issueMultipleCoupon(self,couponSeriesId,self.userIds)

        # Check the queue size after coupon issued
        Assertion.constructAssertion(self.connObj.getQueueSize(constant.config['orgId'], couponSeriesId, constant.config['requestId']) == 0, 'Coupon Queue count deducted with No. of Issued Coupons')

        couponIssuedList = LuciDBHelper.getCouponsIssuedList(couponSeriesId)
        Assertion.constructAssertion(couponIssuedList != [], 'Issued Coupon Code recorded in Coupons_issued table')
        Assertion.constructAssertion(len(couponIssuedList) == noOfCouponUpload, 'Issued Coupons are recorded in coupons_issued')

        # couponSentHistoryList = LuciDBHelper.getCouponSentHistoryList(couponSeriesId)
        # Assertion.constructAssertion(couponSentHistoryList != [], 'Issued Coupon details recorded in Coupon_sent_history')
        # Assertion.constructAssertion(len(couponSentHistoryList) == noOfCouponUpload, 'Coupon_sent_history Count of records')

    @pytest.mark.parametrize('description' , ['Upload 100 Coupon and Issue coupon to 120 users'])
    def test_LUCI_IMC_DCP_012(self, description):
        try:
            couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self, couponConfigReq={'client_handling_type': 'DISC_CODE_PIN'})
            LuciHelper.couponPumpAssertion(self, couponSeriesId, False)
            noOfCouponUpload = 100
            noOfCouponToBeIssue = 120

            LuciHelper.uploadCouponAndAssertions(self, couponSeriesId, self.constructObj.importType['NONE'], noOfCouponsToBeUpload=noOfCouponUpload)

            time.sleep(2)
            createdCouponCount = LuciDBHelper.getCouponsCreated_Count(couponSeriesId, 1)
            Assertion.constructAssertion(createdCouponCount == noOfCouponUpload, 'Uploaded coupon & Valid coupon in DB count Mismatch Actual : {} and Expected : {}'.format(createdCouponCount, noOfCouponUpload))
            queueCount = self.connObj.getQueueSize(constant.config['orgId'], couponSeriesId, constant.config['requestId']);
            Assertion.constructAssertion(queueCount == noOfCouponUpload, 'Uploaded coupon and Queued Coupon count is Mismatch Actual : {} and Expected : {}'.format(queueCount, noOfCouponUpload))

            LuciDBHelper.getUsers(noOfCouponToBeIssue)
            for i in range(len(constant.config['usersInfo'])):
                self.bulkUserIds.append(constant.config['usersInfo'][i]['userId'])
            exceptionList = LuciHelper.issueMultipleCoupon(self, couponSeriesId, self.bulkUserIds, expectResponseException=[True, 'coupons exhausted'])
            Assertion.constructAssertion((noOfCouponToBeIssue - noOfCouponUpload) == len(exceptionList), 'Uploaded and Issued Coupons : {} and Coupon Exhausted Exception : {}'.format(noOfCouponUpload, len(exceptionList)))
        finally:
            del constant.config['usersInfo'][10:]

    @pytest.mark.parametrize('description', [('Issue same coupon twice with config Do not resend existing voucher false & allow multiple voucher false')])
    def test_LUCI_IMC_DCP_013(self, description):
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self, {'client_handling_type' : 'DISC_CODE_PIN', })
        LuciHelper.couponPumpAssertion(self,couponSeriesId,isDiscCode=False)
        noOfCouponUpload = 10

        LuciHelper.uploadCouponAndAssertions(self, couponSeriesId, self.constructObj.importType['NONE'], noOfCouponsToBeUpload=noOfCouponUpload)

        time.sleep(2)
        LuciHelper.couponPumpAssertion(self,couponSeriesId,isDiscCode=False, DiscCodePinCouponUploaded=noOfCouponUpload)

        LuciHelper.issueMultipleCoupon(self, couponSeriesId, self.userIds)

        # Check the queue size after coupon issued
        Assertion.constructAssertion(self.connObj.getQueueSize(constant.config['orgId'], couponSeriesId, constant.config['requestId']) == 0, 'Coupon Queue count deducted with No. of Issued Coupons')

        couponIssuedList = LuciDBHelper.getCouponsIssuedList(couponSeriesId)
        Assertion.constructAssertion(couponIssuedList != [], 'Issued Coupon Code recorded in Coupons_issued table')
        Assertion.constructAssertion(len(couponIssuedList) == noOfCouponUpload, 'Issued Coupons are recorded in coupons_issued')

        LuciHelper.issueMultipleCoupon(self, couponSeriesId, self.userIds)
        # couponSentHistoryList = LuciDBHelper.getCouponSentHistoryList(couponSeriesId)
        # Assertion.constructAssertion(couponSentHistoryList != [], 'Issued Coupon details recorded in Coupon_sent_history')
        # Assertion.constructAssertion(len(couponSentHistoryList) == (noOfCouponUpload * 2), 'Coupon_sent_history Count of records')

    @pytest.mark.parametrize('description', [('Issue multiple coupons per user with the max coupon limits')])
    def test_LUCI_IMC_DCP_014(self, description):
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self, {'client_handling_type' : 'DISC_CODE_PIN', 'do_not_resend_existing_voucher' : True, 'allow_multiple_vouchers_per_user' : True, 'max_vouchers_per_user' : 2})
        LuciHelper.couponPumpAssertion(self, couponSeriesId, isDiscCode=False)
        # upload the coupon code
        LuciHelper.uploadCouponAndAssertions(self,couponSeriesId, self.constructObj.importType['NONE'], noOfCouponsToBeUpload = 20)

        LuciHelper.issueMultipleCoupon(self, couponSeriesId, self.userIds)
        LuciHelper.issueMultipleCoupon(self, couponSeriesId, self.userIds)
        maxCouponLimitExceed = LuciHelper.issueMultipleCoupon(self, couponSeriesId, self.userIds, expectResponseException=[True,'max coupon per user exceeded'])
        Assertion.constructAssertion(len(maxCouponLimitExceed) == len(self.userIds), 'Max Coupon per user Exceeded with limit 2')

    @pytest.mark.parametrize('description', [('Issue same coupon twice with config Do not resend existing voucher True & allow multiple voucher false')])
    def test_LUCI_IMC_DCP_015(self, description):
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self, {'client_handling_type' : 'DISC_CODE_PIN', 'do_not_resend_existing_voucher' : True, 'allow_multiple_vouchers_per_user' : False})
        LuciHelper.couponPumpAssertion(self, couponSeriesId, isDiscCode=False)
        # upload the coupon code
        LuciHelper.uploadCouponAndAssertions(self,couponSeriesId, self.constructObj.importType['NONE'], noOfCouponsToBeUpload = 10)

        LuciHelper.issueMultipleCoupon(self, couponSeriesId, self.userIds)
        couponAlreadyIssued = LuciHelper.issueMultipleCoupon(self, couponSeriesId, self.userIds, expectResponseException=[True,'user already has a coupon'])
        Assertion.constructAssertion(len(couponAlreadyIssued) == len(self.userIds), 'Coupon Already issued to List of users Sent')

    @pytest.mark.parametrize('description', [('Issue same coupon twice with config Do not resend existing voucher false & allow multiple voucher True')])
    def test_LUCI_IMC_DCP_016(self, description):
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self, {'client_handling_type' : 'DISC_CODE_PIN', 'do_not_resend_existing_voucher' : False, 'allow_multiple_vouchers_per_user' : True})
        LuciHelper.couponPumpAssertion(self, couponSeriesId, isDiscCode=False)

        # upload the coupon code
        LuciHelper.uploadCouponAndAssertions(self, couponSeriesId, self.constructObj.importType['NONE'], noOfCouponsToBeUpload=10)

        LuciHelper.issueMultipleCoupon(self, couponSeriesId, self.userIds)
        LuciHelper.issueMultipleCoupon(self, couponSeriesId, self.userIds)
        # couponSentHistoryList = LuciDBHelper.getCouponSentHistoryList(couponSeriesId);
        # Assertion.constructAssertion(couponSentHistoryList[0]['notes'] == 'ISSUED', 'Coupon_sent_history Notes Actual : {} and Expected : ISSUED'.format(couponSentHistoryList[0]['notes']))
        # Assertion.constructAssertion(couponSentHistoryList[1]['notes'] == 'RESENT', 'Coupon_sent_history Notes Actual : {} and Expected : RESENT'.format(couponSentHistoryList[1]['notes']))

    @pytest.mark.parametrize('description', [('Issue coupon without upload coupons')])
    def test_LUCI_IMC_DCP_017(self, description):
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self, {'client_handling_type' : 'DISC_CODE_PIN'})
        LuciHelper.couponPumpAssertion(self, couponSeriesId, isDiscCode=False)

        exceptionList = LuciHelper.issueMultipleCoupon(self, couponSeriesId, self.userIds, expectResponseException=[True, 'coupons exhausted'])
        Assertion.constructAssertion(len(self.userIds) == len(exceptionList), 'Uploaded and Issued Coupons : {} and Coupon Exhausted Exception : {}'.format(len(self.userIds), len(exceptionList)))

    @pytest.mark.parametrize('description', [('set max create 5 and issue 10 coupons')])
    def test_LUCI_IMC_DCP_018(self, description):
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self, {'client_handling_type': 'DISC_CODE_PIN', 'max_create': 5})
        LuciHelper.couponPumpAssertion(self, couponSeriesId, isDiscCode=False)
        noOfCouponUpload = 5
        # upload the coupon code
        LuciHelper.uploadCouponAndAssertions(self, couponSeriesId, self.constructObj.importType['NONE'], noOfCouponsToBeUpload = noOfCouponUpload)

        maxCouponSeries = LuciHelper.issueMultipleCoupon(self, couponSeriesId, self.userIds, expectResponseException=[True, 'max create for series exceeded'])
        Assertion.constructAssertion(len(maxCouponSeries) == noOfCouponUpload, 'Max Create for series Exceeded Exception for Users')

    @pytest.mark.parametrize('description, invalidInput, expected', [
        ('Issue coupon with Invalid orgId', {'orgId' : 9999}, [constant.INVALID_ORG_ID, 'invalid org id']),
        ('Issue coupon with Negative orgId', {'orgId' : -1}, [constant.INVALID_ORG_ID, 'invalid org id -1']),
        ('Issue coupon with Invalid CouponSeries Id', {'couponSeriesId' : -1}, [constant.INVALID_COUPON_SERIES_ID, 'invalid series id -1']),
        ('Issue coupon with Invalid storeUnit Id', {'storeUnitId' : -1}, [constant.INVALID_ISSUAL_STORE_ID, 'invalid store id -1']),
        ('Issue coupon with Invalid userId', {'userIds' : [-1]}, [constant.INVALID_USER_ID, 'user id is not valid']),
        ('Issue coupon with Invalid userId', None, [constant.DUPLICATE_USER_ID, 'duplicate user id for the customer {}'])])
    def test_LUCI_IMC_DCP_019(self, description, invalidInput, expected):
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self, {'client_handling_type': 'DISC_CODE_PIN'})
        # upload the coupon code
        LuciHelper.uploadCouponAndAssertions(self, couponSeriesId, self.constructObj.importType['NONE'])
        if invalidInput == None:
            invalidInput = {'userIds' : [constant.config['usersInfo'][0]['userId'],constant.config['usersInfo'][0]['userId']]}
            expected[1] = expected[1].format(constant.config['usersInfo'][0]['userId'])
        try:
            LuciHelper.issueMultipleCoupon(self, couponSeriesId, self.userIds, issueCouponParamObj=invalidInput)
        except Exception, luciExp:
            Logger.log('Exception : ' , luciExp)
            luciExp = luciExp.__dict__;
            Assertion.constructAssertion(luciExp['errorCode'] == expected[0], 'Luci Exception error code Actual: {} and Expected: {}'.format(luciExp['errorCode'], expected[0]))
            Assertion.constructAssertion(luciExp['errorMsg'] == expected[1], 'Luci Exception Error Msg Actual : {}'.format(luciExp['errorMsg']))