import time, random,pytest
from src.Constant.constant import constant
from src.modules.luci.luciDBHelper import LuciDBHelper
from src.utilities.logger import Logger
from src.utilities.assertion import Assertion
from src.utilities.randValues import randValues
from src.modules.luci.luciHelper import LuciHelper
from src.modules.luci.luciObject import LuciObject
from src.utilities.utils import Utils
from src.modules.luci.dracarysHelper import DracarysHelper
from src.modules.luci.dracarysObject import DracarysObject

class Test_IssueMultipleCouponsDiscCode():

    def setup_class(self):
        Logger.logSuiteName(str(self).split('.')[-1])
        self.constructObj = LuciObject()
        self.DracarysObj = DracarysObject()
        self.userIds = []
        self.userId = constant.config['usersInfo'][0]['userId']
        self.bulkUserIds = []
        for i in range(len(constant.config['usersInfo'])):
            self.userIds.append(constant.config['usersInfo'][i]['userId'])
        self.tillId = constant.config['tillIds'][0]

    def teardown_class(self):
        self.connObj = ''

    def setup_method(self, method):
        Logger.logMethodName(method.__name__)
        self.connObj = LuciHelper.getConnObj(newConnection=True)
        self.DracraysConnObj = DracarysHelper.getConnObj(newConnection=True)
        constant.config['uploadedFileName'] = method.__name__
        constant.config['requestId'] = 'luci_auto_'+str(random.randint(11111, 99999))

    @pytest.mark.parametrize('description' , ['With all the valid parameters'])
    def test_LUCI_IMC_DC_011(self, description):
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self)
        LuciHelper.queuePumpWait(self,couponSeriesId)
        LuciHelper.couponPumpAssertion(self,couponSeriesId)

        LuciHelper.issueMultipleCoupon(self,couponSeriesId,self.userIds)

        # Check the queue size after coupon issued

        couponIssuedList = LuciDBHelper.getCouponsIssuedList(couponSeriesId)
        Assertion.constructAssertion(couponIssuedList != [], 'Issued Coupon Code recorded in Coupons_issued table')
        Assertion.constructAssertion(len(couponIssuedList) == len(self.userIds), 'Issued Coupons are recorded in coupons_issued')

        # couponSentHistoryList = LuciDBHelper.getCouponSentHistoryList(couponSeriesId)
        # Assertion.constructAssertion(couponSentHistoryList != [], 'Issued Coupon details recorded in Coupon_sent_history')
        # Assertion.constructAssertion(len(couponSentHistoryList) == len(self.userIds), 'Coupon_sent_history Count of records')

    @pytest.mark.parametrize('description' , ['Issue 5 coupons using upload-userIds and Issue 5 coupons in Multiple issue call'])
    def test_LUCI_IMC_DC_012(self, description):
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self)
        LuciHelper.queuePumpWait(self,couponSeriesId)
        LuciHelper.couponPumpAssertion(self,couponSeriesId)

        preIssueQC = self.connObj.getQueueSize(constant.config['orgId'], couponSeriesId,constant.config['requestId'])

        LuciHelper.uploadCouponAndAssertions(self, couponSeriesId, self.constructObj.importType['USER_ID'], self.userIds, noOfCouponsToBeUpload=5,  dracraysUpload={'userOnly' : True})
        LuciHelper.issueMultipleCoupon(self,couponSeriesId,self.userIds[5:])

        postIssueQC = self.connObj.getQueueSize(constant.config['orgId'], couponSeriesId,constant.config['requestId'])

        # Check the queue size after coupon issued
        Assertion.constructAssertion(preIssueQC == (postIssueQC + 5), 'After coupon issued Queue size Mismatch Actual: {} & Expected: {}'.format(preIssueQC,  (postIssueQC + 5)))
        couponIssuedList = LuciDBHelper.getCouponsIssuedList(couponSeriesId)
        Assertion.constructAssertion(couponIssuedList != [], 'Issued Coupon Code recorded in Coupons_issued table')
        Assertion.constructAssertion(len(couponIssuedList) == len(self.userIds), 'Issued Coupons are recorded in coupons_issued Actual: {} and Expected : {}'.format(len(couponIssuedList), len(self.userIds)))

        # couponSentHistoryList = LuciDBHelper.getCouponSentHistoryList(couponSeriesId)
        # Assertion.constructAssertion(couponSentHistoryList != [], 'Issued Coupon details recorded in Coupon_sent_history')
        # Assertion.constructAssertion(len(couponSentHistoryList) == len(self.userIds[5:]), 'Coupon_sent_history Count of records')

    @pytest.mark.parametrize('description', [('Issue same coupon twice with config Do not resend existing voucher false & allow multiple voucher false')])
    def test_LUCI_IMC_DC_013(self, description):
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self)
        LuciHelper.queuePumpWait(self, couponSeriesId)
        LuciHelper.couponPumpAssertion(self, couponSeriesId)

        LuciHelper.issueMultipleCoupon(self, couponSeriesId, self.userIds)

        couponIssuedList = LuciDBHelper.getCouponsIssuedList(couponSeriesId)
        Assertion.constructAssertion(couponIssuedList != [], 'Issued Coupon Code recorded in Coupons_issued table')
        Assertion.constructAssertion(len(couponIssuedList) == len(self.userIds), 'Issued Coupons are recorded in coupons_issued')

        LuciHelper.issueMultipleCoupon(self, couponSeriesId, self.userIds)
        # couponSentHistoryList = LuciDBHelper.getCouponSentHistoryList(couponSeriesId)
        # Assertion.constructAssertion(couponSentHistoryList != [], 'Issued Coupon details recorded in Coupon_sent_history')
        # Assertion.constructAssertion(len(couponSentHistoryList) == (len(self.userIds) * 2), 'Coupon_sent_history Count of records')

    @pytest.mark.parametrize('description', [('Issue multiple coupons per user with the max coupon limits')])
    def test_LUCI_IMC_DC_014(self, description):
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self, { 'do_not_resend_existing_voucher' : True, 'allow_multiple_vouchers_per_user' : True, 'max_vouchers_per_user' : 2})
        LuciHelper.queuePumpWait(self, couponSeriesId)
        LuciHelper.couponPumpAssertion(self, couponSeriesId)

        LuciHelper.issueMultipleCoupon(self, couponSeriesId, self.userIds)
        LuciHelper.issueMultipleCoupon(self, couponSeriesId, self.userIds)
        maxCouponLimitExceed = LuciHelper.issueMultipleCoupon(self, couponSeriesId, self.userIds, expectResponseException=[True,'max coupon per user exceeded'])
        Assertion.constructAssertion(len(maxCouponLimitExceed) == len(self.userIds), 'Max Coupon per user Exceeded with limit 2')

    @pytest.mark.parametrize('description', [('Issue same coupon twice with config Do not resend existing voucher True & allow multiple voucher false')])
    def test_LUCI_IMC_DC_015(self, description):
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self, {'do_not_resend_existing_voucher' : True, 'allow_multiple_vouchers_per_user' : False})
        LuciHelper.queuePumpWait(self, couponSeriesId)
        LuciHelper.couponPumpAssertion(self, couponSeriesId)

        LuciHelper.issueMultipleCoupon(self, couponSeriesId, self.userIds)
        couponAlreadyIssued = LuciHelper.issueMultipleCoupon(self, couponSeriesId, self.userIds, expectResponseException=[True,'user already has a coupon'])
        Assertion.constructAssertion(len(couponAlreadyIssued) == len(self.userIds), 'Coupon Already issued to List of users Sent')

    @pytest.mark.parametrize('description', [('Issue same coupon twice with config Do not resend existing voucher false & allow multiple voucher True')])
    def test_LUCI_IMC_DC_016(self, description):
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self, {'do_not_resend_existing_voucher' : False, 'allow_multiple_vouchers_per_user' : True})
        LuciHelper.queuePumpWait(self, couponSeriesId)
        LuciHelper.couponPumpAssertion(self, couponSeriesId)

        LuciHelper.issueMultipleCoupon(self, couponSeriesId, self.userIds)
        LuciHelper.issueMultipleCoupon(self, couponSeriesId, self.userIds)
        # couponSentHistoryList = LuciDBHelper.getCouponSentHistoryList(couponSeriesId);
        # Assertion.constructAssertion(couponSentHistoryList[0]['notes'] == 'ISSUED', 'Coupon_sent_history Notes Actual : {} and Expected : ISSUED'.format(couponSentHistoryList[0]['notes']))
        # Assertion.constructAssertion(couponSentHistoryList[1]['notes'] == 'RESENT', 'Coupon_sent_history Notes Actual : {} and Expected : RESENT'.format(couponSentHistoryList[1]['notes']))

    @pytest.mark.parametrize('description', [('set max create 5 and issue 10 coupons')])
    def test_LUCI_IMC_DC_017(self, description):
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self, {'max_create': 5})
        LuciHelper.queuePumpWait(self, couponSeriesId)
        LuciHelper.couponPumpAssertion(self, couponSeriesId)

        maxCouponSeries = LuciHelper.issueMultipleCoupon(self, couponSeriesId, self.userIds, expectResponseException=[True, 'max create for series exceeded'])
        Assertion.constructAssertion(len(maxCouponSeries) == 5, 'Max Create for series Exceeded Exception for Users')

    @pytest.mark.parametrize('description' , ['Bulk coupon issual'])
    def est_LUCI_BulkIssual(self, description):
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self, couponConfigReq={"any_user": True})
        couponCodeList = []
        Logger.log('Coupon series Id: ', couponSeriesId )

        bulkUserIds = []
        for _ in range(1000000):
            bulkUserIds.append(randValues.randomInteger(9))
        bulkUserIds = list(set(bulkUserIds))
        limit = 500000
        i = 0
        Logger.log('Actial : ', len(bulkUserIds))
        for _ in range(len(bulkUserIds)):
            if limit > (len(bulkUserIds)):
                limit = len(bulkUserIds)
            issueMultipleCouponsRequest = {'couponSeriesId': couponSeriesId, 'storeUnitId': self.tillId, 'userIds': bulkUserIds[i:(limit)]}
            issueMultipleCouponsRequestObj = LuciObject.issueMultipleCouponsRequest(issueMultipleCouponsRequest)
            couponDetailsList = self.connObj.issueMultipleCoupons(issueMultipleCouponsRequestObj)

            for couponDetails in couponDetailsList:
                couponDetails = couponDetails.__dict__
                couponCodeList.append(couponDetails['couponCode'])
            if limit == len(bulkUserIds):
                break

            i = limit
            limit = limit+1000

        for couponCode, userId in zip(couponCodeList,bulkUserIds):
            couponDetailsList = self.connObj.redeemCoupons(LuciHelper.redeemCouponRequest([couponCode], userId, billId=Utils.getTime(milliSeconds=True)))
            # break
