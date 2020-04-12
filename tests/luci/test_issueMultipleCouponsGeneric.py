import time, random,pytest
from src.Constant.constant import constant
from src.modules.luci.luciDBHelper import LuciDBHelper
from src.utilities.logger import Logger
from src.utilities.assertion import Assertion
from src.utilities.randValues import randValues
from src.utilities.utils import Utils
from src.modules.luci.luciHelper import LuciHelper
from src.modules.luci.luciObject import LuciObject
from src.modules.luci.dracarysHelper import DracarysHelper
from src.modules.luci.dracarysObject import DracarysObject

class Test_IssueMultipleCouponsDiscCode():

    def setup_class(self):
        Logger.logSuiteName(str(self).split('.')[-1])
        self.connObj = LuciHelper.getConnObj()
        self.constructObj = LuciObject()
        self.userIds = []
        self.bulkUserIds = []
        self.DracarysObj = DracarysObject()
        for i in range(len(constant.config['usersInfo'])):
            self.userIds.append(constant.config['usersInfo'][i]['userId'])
        self.tillId = constant.config['tillIds'][0]

    def teardown_class(self):
        self.connObj = ''

    def setup_method(self, method):
        Logger.logMethodName(method.__name__)
        constant.config['uploadedFileName'] = method.__name__
        self.DracraysConnObj = DracarysHelper.getConnObj(newConnection=True)
        constant.config['requestId'] = 'luci_auto_'+str(random.randint(11111, 99999))

    @pytest.mark.parametrize('description' , ['Issue multiple Generic Coupons'])
    def test_LUCI_IMC_GC_01(self, description):
        couponCode = LuciHelper.generateCouponCode()
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self,couponConfigReq={'client_handling_type' : 'GENERIC', 'genericCode' : couponCode})

        LuciHelper.issueMultipleCoupon(self,couponSeriesId,self.userIds)

        couponIssuedList = LuciDBHelper.getCouponsIssuedList(couponSeriesId)
        Assertion.constructAssertion(couponIssuedList != [], 'Issued Coupon Code recorded in Coupons_issued table')
        Assertion.constructAssertion(len(couponIssuedList) == len(self.userIds), 'Issued Coupons are recorded in coupons_issued')

        # couponSentHistoryList = LuciDBHelper.getCouponSentHistoryList(couponSeriesId)
        # Assertion.constructAssertion(couponSentHistoryList != [], 'Issued Coupon details recorded in Coupon_sent_history')
        # Assertion.constructAssertion(len(couponSentHistoryList) == len(self.userIds), 'Coupon_sent_history Count of records')

    @pytest.mark.parametrize('description, couponConfig, expectedErrorMsg, sentHistoryCount' , [
        ('Issue Multiple coupons per user & config multiple voucher False', {'do_not_resend_existing_voucher' : True}, 'user already has a coupon', 10),
        ('Issue Multiple coupons per user & config multiple voucher True', {'allow_multiple_vouchers_per_user' : True, 'do_not_resend_existing_voucher' : True}, 'user already has a valid generic coupon', 10),
        ('Issue Multiple coupons per user & config multiple voucher True', {'allow_multiple_vouchers_per_user' : False, 'do_not_resend_existing_voucher' : True}, 'user already has a coupon', 10)
    ])
    def test_LUCI_IMC_GC_02(self, description, couponConfig, expectedErrorMsg, sentHistoryCount):
        couponCode = LuciHelper.generateCouponCode()
        couponConfig.update({'client_handling_type' : 'GENERIC', 'genericCode' : couponCode})
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self,couponConfigReq=couponConfig)
        LuciHelper.issueMultipleCoupon(self, couponSeriesId, self.userIds)


        exceptionList = LuciHelper.issueMultipleCoupon(self, couponSeriesId, self.userIds, expectResponseException=[True, expectedErrorMsg])
        Assertion.constructAssertion(len(exceptionList) == len(self.userIds), 'Requested issual {}'.format(expectedErrorMsg))
        # couponSentHistoryList = LuciDBHelper.getCouponSentHistoryList(couponSeriesId)
        # Assertion.constructAssertion(len(couponSentHistoryList) == sentHistoryCount, 'Coupon_sent_history Count of records')

    @pytest.mark.parametrize('description', [('Issue same coupon twice with config Do not resend existing voucher false & allow multiple voucher True')])
    def test_LUCI_IMC_GC_03(self, description):
        couponCode = LuciHelper.generateCouponCode()
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self, {'client_handling_type' : 'GENERIC', 'genericCode' : couponCode, 'do_not_resend_existing_voucher' : False, 'allow_multiple_vouchers_per_user' : True})

        LuciHelper.issueMultipleCoupon(self, couponSeriesId, self.userIds)
        LuciHelper.issueMultipleCoupon(self, couponSeriesId, self.userIds)
        # couponSentHistoryList = LuciDBHelper.getCouponSentHistoryList(couponSeriesId);
        # issued, resent = 0, 0
        # for sentHistory in couponSentHistoryList:
        #     if sentHistory['notes'] == 'ISSUED': issued += 1
        #     if sentHistory['notes'] == 'RESENT': resent += 1
        # Assertion.constructAssertion(issued == len(self.userIds), 'Sent History Issued count Mismatch Actual: {} & Expected: {}'.format(issued, len(self.userIds)))
        # Assertion.constructAssertion(resent == len(self.userIds), 'Sent History resent count Mismatch Actual: {} & Expected: {}'.format(resent, len(self.userIds)))

    @pytest.mark.parametrize('description', [('Issue same coupon twice with config Do not resend existing voucher false & allow multiple voucher False')])
    def test_LUCI_IMC_GC_04(self, description):
        couponCode = LuciHelper.generateCouponCode()
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self, {'client_handling_type': 'GENERIC', 'genericCode': couponCode, 'do_not_resend_existing_voucher': False, 'allow_multiple_vouchers_per_user': False})

        LuciHelper.issueMultipleCoupon(self, couponSeriesId, self.userIds)
        LuciHelper.issueMultipleCoupon(self, couponSeriesId, self.userIds)
        # couponSentHistoryList = LuciDBHelper.getCouponSentHistoryList(couponSeriesId);
        # issued, resent = 0, 0
        # for sentHistory in couponSentHistoryList:
        #     if sentHistory['notes'] == 'ISSUED': issued += 1
        #     if sentHistory['notes'] == 'RESENT': resent += 1
        # Assertion.constructAssertion(issued == len(self.userIds), 'Sent History Issued count Mismatch Actual: {} & Expected: {}'.format(issued, len(self.userIds)))
        # Assertion.constructAssertion(resent == len(self.userIds), 'Sent History resent count Mismatch Actual: {} & Expected: {}'.format(resent, len(self.userIds)))

    @pytest.mark.parametrize('description', [('Expiry issued coupons and issue for same users with config Do not resend existing voucher True & allow multiple voucher True')])
    def test_LUCI_IMC_GC_05(self, description):
        couponCode = LuciHelper.generateCouponCode()
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self, {'client_handling_type' : 'GENERIC', 'genericCode' : couponCode, 'do_not_resend_existing_voucher' : True, 'allow_multiple_vouchers_per_user' : True , 'valid_days_from_create' : 1})

        couponDetailsList = LuciHelper.issueMultipleCoupon(self, couponSeriesId, self.userIds)
        for couponDetails in couponDetailsList:
            couponDetails = couponDetails.__dict__
            self.connObj.changeCouponIssuedDate(couponDetails['id'], Utils.getTime(days=-2, minutes=5,milliSeconds=True))

        LuciHelper.uploadCouponAndAssertions(self, couponSeriesId, self.constructObj.importType['USER_ID'], self.userIds, noOfCouponsToBeUpload=10, dracraysUpload={'userOnly': True})
        couponAlreadyIssued = LuciHelper.issueMultipleCoupon(self, couponSeriesId, self.userIds, expectResponseException=[True,'user already has a valid generic coupon'])
        Assertion.constructAssertion(len(couponAlreadyIssued) == len(self.userIds), 'Coupon Already issued to List of users Sent')

        couponIssuedList = LuciDBHelper.getCouponsIssuedList(couponSeriesId)
        Assertion.constructAssertion(couponIssuedList != [], 'Issued Coupon Code recorded in Coupons_issued table')
        Assertion.constructAssertion(len(couponIssuedList) == len(self.userIds)*2, 'Issued Coupons are recorded in coupons_issued')

        # couponSentHistoryList = LuciDBHelper.getCouponSentHistoryList(couponSeriesId)
        # Assertion.constructAssertion(couponSentHistoryList != [], 'Issued Coupon details recorded in Coupon_sent_history')
        # Assertion.constructAssertion(len(couponSentHistoryList) == len(self.userIds), 'Coupon_sent_history Count of records')

    @pytest.mark.parametrize('description', [pytest.param('Expiry issued coupons and issue for same users with config Do not resend existing voucher False & allow multiple voucher True', marks=pytest.mark.xfail)])
    def test_LUCI_IMC_GC_06(self, description):
        couponCode = LuciHelper.generateCouponCode()
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self, {'client_handling_type' : 'GENERIC', 'genericCode' : couponCode, 'do_not_resend_existing_voucher' : False, 'allow_multiple_vouchers_per_user' : True , 'valid_days_from_create' : 1})

        couponDetailsList = LuciHelper.issueMultipleCoupon(self, couponSeriesId, self.userIds)
        for couponDetails in couponDetailsList:
            couponDetails = couponDetails.__dict__
            self.connObj.changeCouponIssuedDate(couponDetails['id'], Utils.getTime(days=-2, minutes=5,milliSeconds=True))

        LuciHelper.uploadCouponAndAssertions(self, couponSeriesId, self.constructObj.importType['USER_ID'], self.userIds, noOfCouponsToBeUpload=10, dracraysUpload={'userOnly': True})
        couponAlreadyIssued = LuciHelper.issueMultipleCoupon(self, couponSeriesId, self.userIds, expectResponseException=[True,'user already has a valid generic coupon'])
        Assertion.constructAssertion(len(couponAlreadyIssued) == len(self.userIds), 'Coupon Already issued to List of users Sent')

        couponIssuedList = LuciDBHelper.getCouponsIssuedList(couponSeriesId)
        Assertion.constructAssertion(couponIssuedList != [], 'Issued Coupon Code recorded in Coupons_issued table')
        Assertion.constructAssertion(len(couponIssuedList) == len(self.userIds)*2, 'Issued Coupons are recorded in coupons_issued')

        # couponSentHistoryList = LuciDBHelper.getCouponSentHistoryList(couponSeriesId)
        # Assertion.constructAssertion(couponSentHistoryList != [], 'Issued Coupon details recorded in Coupon_sent_history')
        # Assertion.constructAssertion(len(couponSentHistoryList) == len(self.userIds)*2, 'Coupon_sent_history Count of records')
        # issued, resent = 0, 0
        # for sentHistory in couponSentHistoryList:
        #     if sentHistory['notes'] == 'ISSUED': issued += 1
        #     if sentHistory['notes'] == 'RESENT': resent += 1
        # Assertion.constructAssertion(issued == len(self.userIds), 'Sent History Issued count Mismatch Actual: {} & Expected: {}'.format(issued, len(self.userIds)));
        # Assertion.constructAssertion(resent == len(self.userIds), 'Sent History resent count Mismatch Actual: {} & Expected: {}'.format(resent, len(self.userIds)))

    @pytest.mark.parametrize('description', [('Expiry issued coupons and issue for same users with config Do not resend existing voucher True & allow multiple voucher False')])
    def test_LUCI_IMC_GC_07(self, description):
        couponCode = LuciHelper.generateCouponCode()
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self, {'client_handling_type' : 'GENERIC', 'genericCode' : couponCode, 'do_not_resend_existing_voucher' : True, 'allow_multiple_vouchers_per_user' : False , 'valid_days_from_create' : 1})

        couponDetailsList = LuciHelper.issueMultipleCoupon(self, couponSeriesId, self.userIds)
        for couponDetails in couponDetailsList:
            couponDetails = couponDetails.__dict__
            self.connObj.changeCouponIssuedDate(couponDetails['id'], Utils.getTime(days=-2, minutes=5,milliSeconds=True))

        couponAlreadyIssued = LuciHelper.issueMultipleCoupon(self, couponSeriesId, self.userIds, expectResponseException=[True,'user already has a coupon'])
        Assertion.constructAssertion(len(couponAlreadyIssued) == len(self.userIds), 'Coupon Already issued to List of users Sent')

        couponIssuedList = LuciDBHelper.getCouponsIssuedList(couponSeriesId)
        Assertion.constructAssertion(couponIssuedList != [], 'Issued Coupon Code recorded in Coupons_issued table')
        Assertion.constructAssertion(len(couponIssuedList) == len(self.userIds), 'Issued Coupons are recorded in coupons_issued')

        # couponSentHistoryList = LuciDBHelper.getCouponSentHistoryList(couponSeriesId)
        # Assertion.constructAssertion(couponSentHistoryList != [], 'Issued Coupon details recorded in Coupon_sent_history')
        # Assertion.constructAssertion(len(couponSentHistoryList) == len(self.userIds), 'Coupon_sent_history Count of records')


    @pytest.mark.parametrize('description', [('Expiry issued coupons and issue for same users with config Do not resend existing voucher False & allow multiple voucher False')])
    def test_LUCI_IMC_GC_08(self, description):
        couponCode = LuciHelper.generateCouponCode()
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self, {'client_handling_type' : 'GENERIC', 'genericCode' : couponCode, 'do_not_resend_existing_voucher' : False, 'allow_multiple_vouchers_per_user' : False , 'valid_days_from_create' : 1})

        couponDetailsList = LuciHelper.issueMultipleCoupon(self, couponSeriesId, self.userIds)
        for couponDetails in couponDetailsList:
            couponDetails = couponDetails.__dict__
            self.connObj.changeCouponIssuedDate(couponDetails['id'], Utils.getTime(days=-2, minutes=5,milliSeconds=True))

        LuciHelper.issueMultipleCoupon(self, couponSeriesId, self.userIds)

        couponIssuedList = LuciDBHelper.getCouponsIssuedList(couponSeriesId)
        Assertion.constructAssertion(couponIssuedList != [], 'Issued Coupon Code recorded in Coupons_issued table')
        Assertion.constructAssertion(len(couponIssuedList) == len(self.userIds), 'Issued Coupons are recorded in coupons_issued')

        # couponSentHistoryList = LuciDBHelper.getCouponSentHistoryList(couponSeriesId)
        # Assertion.constructAssertion(couponSentHistoryList != [], 'Issued Coupon details recorded in Coupon_sent_history')
        # Assertion.constructAssertion(len(couponSentHistoryList) == len(self.userIds)*2, 'Coupon_sent_history Count of records')
        # issued, resent = 0,0
        # for sentHistory in couponSentHistoryList:
        #     if sentHistory['notes'] == 'ISSUED' : issued += 1
        #     if sentHistory['notes'] == 'RESENT' : resent += 1
        # Assertion.constructAssertion(issued == len(self.userIds), 'Sent History Issued count Mismatch Actual: {} & Expected: {}'.format(issued,len(self.userIds)))
        # Assertion.constructAssertion(resent == len(self.userIds), 'Sent History resent count Mismatch Actual: {} & Expected: {}'.format(resent,len(self.userIds)))

    @pytest.mark.parametrize('description', [('Issue for same users with config Do not resend existing voucher False & allow multiple voucher False')])
    def test_LUCI_IMC_GC_09(self, description):
        couponCode = LuciHelper.generateCouponCode()
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self, {'client_handling_type' : 'GENERIC', 'genericCode' : couponCode, 'do_not_resend_existing_voucher' : False, 'allow_multiple_vouchers_per_user' : False , 'valid_days_from_create' : 1})

        couponDetailsList = LuciHelper.issueMultipleCoupon(self, couponSeriesId, self.userIds)
        LuciHelper.issueMultipleCoupon(self, couponSeriesId, self.userIds)

        couponIssuedList = LuciDBHelper.getCouponsIssuedList(couponSeriesId)
        Assertion.constructAssertion(couponIssuedList != [], 'Issued Coupon Code recorded in Coupons_issued table')
        Assertion.constructAssertion(len(couponIssuedList) == len(self.userIds), 'Issued Coupons are recorded in coupons_issued')

        # couponSentHistoryList = LuciDBHelper.getCouponSentHistoryList(couponSeriesId)
        # Assertion.constructAssertion(couponSentHistoryList != [], 'Issued Coupon details recorded in Coupon_sent_history')
        # Assertion.constructAssertion(len(couponSentHistoryList) == len(self.userIds)*2, 'Coupon_sent_history Count of records')
        # issued, resent = 0,0
        # for sentHistory in couponSentHistoryList:
        #     if sentHistory['notes'] == 'ISSUED' : issued += 1
        #     if sentHistory['notes'] == 'RESENT' : resent += 1
        # Assertion.constructAssertion(issued == len(self.userIds), 'Sent History Issued count Mismatch Actual: {} & Expected: {}'.format(issued,len(self.userIds)))
        # Assertion.constructAssertion(resent == len(self.userIds), 'Sent History resent count Mismatch Actual: {} & Expected: {}'.format(resent,len(self.userIds)))

    @pytest.mark.parametrize('description, couponConfig' , [
        ('Issue Multiple coupons per user & config multiple voucher False', {'valid_till_date' : Utils.getTime(days=-1,milliSeconds=True), 'do_not_resend_existing_voucher' : True, 'allow_multiple_vouchers_per_user' : False}),
    ])
    def test_LUCI_IMC_GC_10(self, description, couponConfig):
        couponCode = LuciHelper.generateCouponCode()
        couponConfig.update({'client_handling_type': 'GENERIC', 'genericCode': couponCode})
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self, couponConfigReq=couponConfig)
        LuciHelper.issueMultipleCoupon(self, couponSeriesId, self.userIds, expectResponseException=[True,'coupon series expired'])