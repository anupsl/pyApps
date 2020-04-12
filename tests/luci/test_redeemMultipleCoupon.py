import time, random,pytest
from src.Constant.constant import constant
from src.modules.luci.luciDBHelper import LuciDBHelper
from src.utilities.logger import Logger
from src.utilities.assertion import Assertion
from src.utilities.utils import Utils
from src.modules.luci.luciHelper import LuciHelper
from src.modules.luci.luciObject import LuciObject
from src.modules.luci.dracarysHelper import DracarysHelper
from src.modules.luci.dracarysObject import DracarysObject

class Test_RedeemMultipleCoupon():
    def setup_class(self):
        Logger.logSuiteName(str(self).split('.')[-1])
        self.constructObj = LuciObject()
        self.DracarysObj = DracarysObject()
        self.userId = constant.config['usersInfo'][0]['userId']
        self.tillId = constant.config['tillIds'][0]
        self.billId = Utils.getTime(milliSeconds=True)

    def setup_method(self, method):
        self.connObj = LuciHelper.getConnObj(newConnection=True)
        Logger.logMethodName(method.__name__)
        constant.config['uploadedFileName'] = method.__name__
        self.DracraysConnObj = DracarysHelper.getConnObj(newConnection=True)
        constant.config['requestId'] = 'luci_auto_rmc_'+str(random.randint(11111, 99999))
        self.userId = constant.config['usersInfo'][0]['userId']

    def redeemCouponsRequest(self, redeemCouponRequestDetails):
        redeemList = []
        tmpDict = {'couponCode': '', 'userId': 1, 'billId': 1, 'storeUnitId': 1}
        for redeemReq in redeemCouponRequestDetails:
            tmpDict.update(redeemReq)
            redeemList.append(LuciObject.redeemCoupon(tmpDict))
        tmpRedeemCouponRequest = {'couponSeriesRequired': False, 'commit': True, 'redeemCoupons': redeemList}
        return LuciObject.redeemCouponsRequest(tmpRedeemCouponRequest)

    @pytest.mark.parametrize('description, redeemCoupons', [('Redeem valid 2 Coupon', 2),
                                                            ('Redeem valid 5 Coupon', 5)])
    def test_LUCI_MCR_01_sanity(self,description, redeemCoupons):
        couponSeriesIdList = list()
        couponCodeList = list()
        for _ in range(redeemCoupons):
            couponSeriesIdList.append(LuciHelper.saveCouponConfigAndAssertions(self)[1])

        for couponSeriesId in couponSeriesIdList:
            couponCodeList.append(LuciHelper.issueCouponAndAssertions(self, couponSeriesId)[0])

        LuciHelper.redeemCouponAndAssertions(self, couponSeriesIdList, couponCodeList)
        couponSeriesIds = ','.join(map(str,couponSeriesIdList))
        redeemedCouponCount = LuciDBHelper.getRedeemCouponCount(couponSeriesId=couponSeriesIds, conditionList=[self.userId, self.billId, constant.config['tillIds'][0]])
        Assertion.constructAssertion(redeemCoupons == redeemedCouponCount, 'Mismatch Redemption details in voucher_redemptions & coupon_redemptions Actual: {} and Expected: {}'.format(redeemCoupons, redeemedCouponCount))
        for couponSeriesId in couponSeriesIdList:
            LuciHelper.getCouponConfigAndAssertion(self, couponSeriesId, 1, 1)

    @pytest.mark.parametrize('description', ['Redeem Coupon more than max limit'])
    def test_LUCI_MCR_02(self,description):
        try:
            couponSeriesIdList = list()
            couponCodeList = list()
            for _ in range(6):
                couponSeriesIdList.append(LuciHelper.saveCouponConfigAndAssertions(self)[1])

            for couponSeriesId in couponSeriesIdList:
                couponCodeList.append(LuciHelper.issueCouponAndAssertions(self, couponSeriesId)[0])

            LuciHelper.redeemCouponAndAssertions(self, couponSeriesIdList, couponCodeList)
        except Exception, luciExp:
            luciExp = luciExp.__dict__
            Assertion.constructAssertion(luciExp['errorCode'] == constant.INVALID_INPUT, 'Luci Exception error code Actual: {} and Expected: {}'.format(luciExp['errorCode'], constant.INVALID_INPUT))
            Assertion.constructAssertion(luciExp['errorMsg'] == 'can not redeem more than 5 coupons in the same request', 'Luci Exception Error Msg Actual : {}'.format(luciExp['errorMsg']))

    @pytest.mark.parametrize('description', ['Different Bill ids and valid coupon redeem'])
    def test_LUCI_MCR_03(self, description):
        redeemRequestList = []
        couponConfig, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self)
        couponConfig1, couponSeriesId1 = LuciHelper.saveCouponConfigAndAssertions(self)

        couponCode = LuciHelper.issueCouponAndAssertions(self, couponSeriesId)[0]
        couponCode1 = LuciHelper.issueCouponAndAssertions(self, couponSeriesId1)[0]

        redeemRequestList.append({'couponCode': couponCode, 'userId': constant.config['usersInfo'][0]['userId'], 'billId': self.billId, 'storeUnitId': constant.config['tillIds'][0]})
        redeemRequestList.append({'couponCode': couponCode1, 'userId': constant.config['usersInfo'][0]['userId'], 'billId': Utils.getTime(milliSeconds=True), 'storeUnitId': constant.config['tillIds'][1]})

        LuciHelper.redeemCouponAndAssertions(self,[couponSeriesId,couponSeriesId1],[couponCode,couponCode1],redeemCouponRequestList=self.redeemCouponsRequest(redeemRequestList))
        redeemedCouponCount = LuciDBHelper.getRedeemCouponCount(couponSeriesId=(str(couponSeriesId) + ',' + str(couponSeriesId1)), conditionList=[self.userId, self.billId, constant.config['tillIds'][0]])
        Assertion.constructAssertion(len(redeemRequestList) == redeemedCouponCount, 'Mismatch Redemption details in voucher_redemptions & coupon_redemptions Actual: {} and Expected: {}'.format(len(redeemRequestList), redeemedCouponCount))

    @pytest.mark.parametrize('description, redeemCoupons, invalidCoupon', [('Redeem valid 4 Coupon and 1 Invalid Coupon', 4, 'INVCR12')])
    def test_LUCI_MCR_04(self,description, redeemCoupons,invalidCoupon):
        couponSeriesIdList = list()
        couponCodeList = list()
        for _ in range(redeemCoupons):
            couponSeriesIdList.append(LuciHelper.saveCouponConfigAndAssertions(self)[1])

        for couponSeriesId in couponSeriesIdList:
            couponCodeList.append(LuciHelper.issueCouponAndAssertions(self, couponSeriesId)[0])
        couponCodeList.append(invalidCoupon)
        expectedError = {'errorCode' : [645,633] , 'errorMsg' : ['there are some failed redemption exists','invalid coupon code']}
        LuciHelper.redeemCouponAndAssertions(self, couponSeriesIdList, couponCodeList, error=expectedError)

        couponSeriesIds = ','.join(map(str, couponSeriesIdList))
        redeemedCouponCount = LuciDBHelper.getRedeemCouponCount(couponSeriesId=couponSeriesIds, conditionList=[self.userId, self.billId, constant.config['tillIds'][0]])
        Assertion.constructAssertion(redeemedCouponCount == 0 , 'Mismatch Redemption details in voucher_redemptions & coupon_redemptions Actual: {} and Expected: 0'.format(redeemedCouponCount))

    @pytest.mark.parametrize('description, redeemCoupons', [('Redeem valid 4 Coupon and 1 Expiry Coupon', 4)])
    def test_LUCI_MCR_05(self, description, redeemCoupons):
        couponSeriesIdList = list()
        couponCodeList = list()
        for _ in range(redeemCoupons):
            couponSeriesIdList.append(LuciHelper.saveCouponConfigAndAssertions(self)[1])

        for couponSeriesId in couponSeriesIdList:
            couponCodeList.append(LuciHelper.issueCouponAndAssertions(self, couponSeriesId)[0])

        couponSeriesIdExpired = LuciHelper.saveCouponConfigAndAssertions(self, couponConfigReq={'expiry_strategy_value' : 1})[1]
        expiredCouponCode, expiredcouponDetails = LuciHelper.issueCouponAndAssertions(self, couponSeriesIdExpired)

        changeDate = Utils.getTime(days=-3, minutes=5,milliSeconds=True)
        self.connObj.changeCouponIssuedDate(expiredcouponDetails['id'], changeDate)

        couponSeriesIdList.append(couponSeriesIdExpired)
        couponCodeList.append(expiredCouponCode)
        expectedError = {'errorCode': [645, 601], 'errorMsg': ['there are some failed redemption exists', 'coupon already expired']}
        LuciHelper.redeemCouponAndAssertions(self, couponSeriesIdList, couponCodeList, error=expectedError)

        couponSeriesIds = ','.join(map(str, couponSeriesIdList))
        redeemedCouponCount = LuciDBHelper.getRedeemCouponCount(couponSeriesId=couponSeriesIds, conditionList=[self.userId, self.billId, constant.config['tillIds'][0]])
        Assertion.constructAssertion(redeemedCouponCount == 0, 'Mismatch Redemption details in voucher_redemptions & coupon_redemptions Actual: {} and Expected: 0'.format(redeemedCouponCount))

    @pytest.mark.parametrize('description, redeemCoupons', [('Redeem valid 3 Coupon & 1 redeemed Coupon', 3)])
    def test_LUCI_MCR_06(self, description, redeemCoupons):
        couponSeriesIdList = list()
        couponCodeList = list()
        for _ in range(redeemCoupons):
            couponSeriesIdList.append(LuciHelper.saveCouponConfigAndAssertions(self)[1])

        for couponSeriesId in couponSeriesIdList:
            couponCodeList.append(LuciHelper.issueCouponAndAssertions(self, couponSeriesId)[0])

        couponSeriesIdUser2 = LuciHelper.saveCouponConfigAndAssertions(self)[1]
        redeemedCouponCode = LuciHelper.issueCouponAndAssertions(self, couponSeriesIdUser2)[0]

        LuciHelper.redeemCouponAndAssertions(self,couponSeriesIdUser2,redeemedCouponCode)

        couponSeriesIdList.append(couponSeriesIdUser2)
        couponCodeList.append(redeemedCouponCode)
        expectedError = {'errorCode': [645, 604], 'errorMsg': ['there are some failed redemption exists', 'multiple redemptions for user not allowed']}
        LuciHelper.redeemCouponAndAssertions(self, couponSeriesIdList, couponCodeList, error=expectedError)

        couponSeriesIds = ','.join(map(str, couponSeriesIdList))
        redeemedCouponCount = LuciDBHelper.getRedeemCouponCount(couponSeriesId=couponSeriesIds, conditionList=[self.userId, self.billId, constant.config['tillIds'][0]])
        Assertion.constructAssertion(redeemedCouponCount == 1, 'Mismatch Redemption details in voucher_redemptions & coupon_redemptions Actual: {} and Expected: 0'.format(redeemedCouponCount))

    @pytest.mark.parametrize('description, redeemCoupons', [('Redeem valid 3 Coupon & 1 coupon redeemed by another user', 3)])
    def test_LUCI_MCR_07(self, description, redeemCoupons):
        couponSeriesIdList = list()
        couponCodeList = list()
        for _ in range(redeemCoupons):
            couponSeriesIdList.append(LuciHelper.saveCouponConfigAndAssertions(self)[1])

        for couponSeriesId in couponSeriesIdList:
            couponCodeList.append(LuciHelper.issueCouponAndAssertions(self, couponSeriesId)[0])

        couponSeriesIdUser2 = LuciHelper.saveCouponConfigAndAssertions(self)[1]
        self.userId = constant.config['usersInfo'][1]['userId']
        redeemedCouponCode = LuciHelper.issueCouponAndAssertions(self, couponSeriesIdUser2)[0]

        LuciHelper.redeemCouponAndAssertions(self,couponSeriesIdUser2,redeemedCouponCode)
        self.userId = constant.config['usersInfo'][0]['userId']

        couponSeriesIdList.append(couponSeriesIdUser2)
        couponCodeList.append(redeemedCouponCode)
        expectedError = {'errorCode': [645, 625], 'errorMsg': ['there are some failed redemption exists', 'coupon not issued to this user redemption failed']}
        LuciHelper.redeemCouponAndAssertions(self, couponSeriesIdList, couponCodeList, error=expectedError)

        couponSeriesIds = ','.join(map(str, couponSeriesIdList))
        redeemedCouponCount = LuciDBHelper.getRedeemCouponCount(couponSeriesId=couponSeriesIds, conditionList=[self.userId, self.billId, constant.config['tillIds'][0]])
        Assertion.constructAssertion(redeemedCouponCount == 0, 'Mismatch Redemption details in voucher_redemptions & coupon_redemptions Actual: {} and Expected: 0'.format(redeemedCouponCount))


    @pytest.mark.parametrize('description, redeemCoupons', [('Redeem valid 3 Coupon & 1 redeemed Coupon & 1 coupon issued to another user', 3)])
    def test_LUCI_MCR_08(self, description, redeemCoupons):
        couponSeriesIdList = list()
        couponCodeList = list()
        for _ in range(redeemCoupons):
            couponSeriesIdList.append(LuciHelper.saveCouponConfigAndAssertions(self)[1])

        for couponSeriesId in couponSeriesIdList:
            couponCodeList.append(LuciHelper.issueCouponAndAssertions(self, couponSeriesId)[0])

        couponSeriesIdUser2 = LuciHelper.saveCouponConfigAndAssertions(self)[1]
        self.userId = constant.config['usersInfo'][2]['userId']
        user2CouponCode = LuciHelper.issueCouponAndAssertions(self, couponSeriesIdUser2)[0]
        self.userId = constant.config['usersInfo'][1]['userId']
        redeemedCouponCode = LuciHelper.issueCouponAndAssertions(self, couponSeriesIdUser2)[0]

        LuciHelper.redeemCouponAndAssertions(self,couponSeriesIdUser2,redeemedCouponCode)
        self.userId = constant.config['usersInfo'][0]['userId']

        couponSeriesIdList.append(couponSeriesIdUser2)
        couponCodeList.append(user2CouponCode)
        couponCodeList.append(redeemedCouponCode)
        expectedError = {'errorCode': [645, 625,625], 'errorMsg': ['there are some failed redemption exists', 'coupon not issued to this user redemption failed' , 'coupon not issued to this user redemption failed']}
        LuciHelper.redeemCouponAndAssertions(self, couponSeriesIdList, couponCodeList, error=expectedError)

        couponSeriesIds = ','.join(map(str, couponSeriesIdList))
        redeemedCouponCount = LuciDBHelper.getRedeemCouponCount(couponSeriesId=couponSeriesIds, conditionList=[self.userId, self.billId, constant.config['tillIds'][0]])
        Assertion.constructAssertion(redeemedCouponCount == 0, 'Mismatch Redemption details in voucher_redemptions & coupon_redemptions Actual: {} and Expected: 0'.format(redeemedCouponCount))

    @pytest.mark.parametrize('description', ['Different userIds & same Coupon series'])
    def test_LUCI_MCR_09(self, description):
        try:
            redeemRequestList = []
            couponConfig, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self)

            couponCode = LuciHelper.issueCouponAndAssertions(self, couponSeriesId)[0]
            self.userId = constant.config['usersInfo'][1]['userId']
            couponCode1 = LuciHelper.issueCouponAndAssertions(self, couponSeriesId)[0]

            redeemRequestList.append({'couponCode': couponCode, 'userId': constant.config['usersInfo'][0]['userId'], 'billId': Utils.getTime(milliSeconds=True), 'storeUnitId': constant.config['tillIds'][0]})
            redeemRequestList.append({'couponCode': couponCode1, 'userId': constant.config['usersInfo'][1]['userId'], 'billId': Utils.getTime(milliSeconds=True), 'storeUnitId': constant.config['tillIds'][1]})

            self.connObj.redeemCoupons(self.redeemCouponsRequest(redeemRequestList))
        except Exception, luciExp:
            luciExp = luciExp.__dict__
            Assertion.constructAssertion(luciExp['errorCode'] == constant.INVALID_INPUT, 'Luci Exception error code Actual: {} and Expected: {}'.format(luciExp['errorCode'], constant.INVALID_INPUT))
            Assertion.constructAssertion(luciExp['errorMsg'] == 'all user ids are not same', 'Luci Exception Error Msg Actual : {}'.format(luciExp['errorMsg']))

    @pytest.mark.parametrize('description', ['Different userIds & different Coupon series'])
    def test_LUCI_MCR_10(self, description):
        try:
            redeemRequestList = []
            couponConfig, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self)
            couponConfig1, couponSeriesId1 = LuciHelper.saveCouponConfigAndAssertions(self)

            couponCode = LuciHelper.issueCouponAndAssertions(self, couponSeriesId)[0]
            self.userId = constant.config['usersInfo'][1]['userId']
            couponCode1 = LuciHelper.issueCouponAndAssertions(self, couponSeriesId1)[0]
            self.userId = constant.config['usersInfo'][0]['userId']

            redeemRequestList.append({'couponCode': couponCode, 'userId': self.userId, 'billId': Utils.getTime(milliSeconds=True), 'storeUnitId': constant.config['tillIds'][0]})
            redeemRequestList.append({'couponCode': couponCode1, 'userId': constant.config['usersInfo'][1]['userId'], 'billId': Utils.getTime(milliSeconds=True), 'storeUnitId': constant.config['tillIds'][1]})

            self.connObj.redeemCoupons(self.redeemCouponsRequest(redeemRequestList))
        except Exception, luciExp:
            luciExp = luciExp.__dict__
            Assertion.constructAssertion(luciExp['errorCode'] == constant.INVALID_INPUT, 'Luci Exception error code Actual: {} and Expected: {}'.format(luciExp['errorCode'], constant.INVALID_INPUT))
            Assertion.constructAssertion(luciExp['errorMsg'] == 'all user ids are not same', 'Luci Exception Error Msg Actual : {}'.format(luciExp['errorMsg']))

    @pytest.mark.parametrize('description', ['Same userIds & coupon code not mapped to the user'])
    def test_LUCI_MCR_11(self, description):
        try:
            req = []
            couponConfig, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self)
            couponConfig1, couponSeriesId1 = LuciHelper.saveCouponConfigAndAssertions(self)

            couponCode = LuciHelper.issueCouponAndAssertions(self, couponSeriesId)[0]
            self.userId = constant.config['usersInfo'][1]['userId']
            couponCode1 = LuciHelper.issueCouponAndAssertions(self, couponSeriesId1)[0]

            req.append({'couponCode': couponCode, 'userId': self.userId, 'billId': Utils.getTime(milliSeconds=True), 'storeUnitId': constant.config['tillIds'][0]})
            req.append({'couponCode': couponCode1, 'userId': constant.config['usersInfo'][1]['userId'], 'billId': Utils.getTime(milliSeconds=True), 'storeUnitId': constant.config['tillIds'][1]})

            self.connObj.redeemCoupons(self.redeemCouponsRequest(req))
        except Exception, luciExp:
            luciExp = luciExp.__dict__
            Assertion.constructAssertion(luciExp['errorCode'] == constant.INVALID_INPUT, 'Luci Exception error code Actual: {} and Expected: {}'.format(luciExp['errorCode'], constant.INVALID_INPUT))
            Assertion.constructAssertion(luciExp['errorMsg'] == 'all user ids are not same', 'Luci Exception Error Msg Actual : {}'.format(luciExp['errorMsg']))

    @pytest.mark.parametrize('description, redeemCoupons, configRequest, redeemCount, expectedError', [
        ('Valid min & max amount and issued to user2 anyUser True ', 2, {'min_bill_amount' : 100, 'max_bill_amount' : 12500}, 4, []),
        ('Bill amount less than min amount and issued to user2 anyUser True ', 2, {'min_bill_amount' : 9999, 'max_bill_amount' : 12500}, 0, {'errorCode': [645, 900], 'errorMsg': ['there are some failed redemption exists', 'bill amount less than the minimum limit set']}),
        ('Bill amount more than max amount and issued to user2 anyUser True ', 2, {'min_bill_amount' : 100, 'max_bill_amount' : 500}, 0, {'errorCode': [645, 901], 'errorMsg': ['there are some failed redemption exists', 'bill amount more than the maximum limit set']}),
    ])
    def test_LUCI_MCR_12(self, description, redeemCoupons, configRequest, redeemCount, expectedError):
        couponSeriesIdList = list()
        couponCodeList = list()
        configOne = True
        for _ in range(redeemCoupons):
            if not configOne:
                couponSeriesIdList.append(LuciHelper.saveCouponConfigAndAssertions(self)[1])
            else:
                couponSeriesIdList.append(LuciHelper.saveCouponConfigAndAssertions(self, couponConfigReq=configRequest)[1])
                configOne=False

        for couponSeriesId in couponSeriesIdList:
            couponCodeList.append(LuciHelper.issueCouponAndAssertions(self, couponSeriesId)[0])

        couponSeriesIdUser2 = LuciHelper.saveCouponConfigAndAssertions(self, couponConfigReq={'any_user' : True})[1]
        couponCodeList.append(LuciHelper.issueCouponAndAssertions(self, couponSeriesIdUser2)[0])
        self.userId = constant.config['usersInfo'][1]['userId']
        couponCodeList.append(LuciHelper.issueCouponAndAssertions(self, couponSeriesIdUser2)[0])

        self.userId = constant.config['usersInfo'][0]['userId']

        couponSeriesIdList.append(couponSeriesIdUser2)
        couponSeriesIdList.append(couponSeriesIdUser2)
        LuciHelper.redeemCouponAndAssertions(self, couponSeriesIdList, couponCodeList, couponIssuedTo=[constant.config['usersInfo'][0]['userId'], constant.config['usersInfo'][1]['userId']], error=expectedError)

        couponSeriesIds = ','.join(map(str, couponSeriesIdList))
        redeemedCouponCount = LuciDBHelper.getRedeemCouponCount(couponSeriesId=couponSeriesIds, conditionList=[self.userId, self.billId, constant.config['tillIds'][0]])
        Assertion.constructAssertion(redeemedCouponCount == redeemCount, 'Mismatch Redemption details in voucher_redemptions & coupon_redemptions Actual: {} and Expected: {}'.format(redeemedCouponCount,redeemCount))


    @pytest.mark.parametrize('description', ['Same Coupon Code & UserId in the redeemList'])
    def test_LUCI_MCR_13(self,description):
        couponConfig, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self)
        couponCode1 = LuciHelper.issueCouponAndAssertions(self,couponSeriesId)[0]

        try:
            LuciHelper.redeemCouponAndAssertions(self, couponSeriesId, [couponCode1, couponCode1])
        except Exception, luciExp:
            luciExp = luciExp.__dict__
            Assertion.constructAssertion(luciExp['errorCode'] == constant.INVALID_INPUT, 'Luci Exception error code Actual: {} and Expected: {}'.format(luciExp['errorCode'], constant.INVALID_INPUT))
            Assertion.constructAssertion(luciExp['errorMsg'] == 'same coupon codes can not be sent multiple times in the same request', 'Luci Exception Error Msg Actual : {}'.format(luciExp['errorMsg']))

    @pytest.mark.parametrize('description', ['Combined same & different coupon code in the redeemList'])
    def test_LUCI_MCR_14(self,description):
        couponConfig, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self)
        couponConfig1, couponSeriesId1 = LuciHelper.saveCouponConfigAndAssertions(self)

        couponCode = LuciHelper.issueCouponAndAssertions(self,couponSeriesId)[0]
        couponCode1 = LuciHelper.issueCouponAndAssertions(self, couponSeriesId1)[0]

        try:
            LuciHelper.redeemCouponAndAssertions(self, couponSeriesId, [couponCode, couponCode1, couponCode1])
        except Exception, luciExp:
            luciExp = luciExp.__dict__
            Assertion.constructAssertion(luciExp['errorCode'] == constant.INVALID_INPUT, 'Luci Exception error code Actual: {} and Expected: {}'.format(luciExp['errorCode'], constant.INVALID_INPUT))
            Assertion.constructAssertion(luciExp['errorMsg'] == 'same coupon codes can not be sent multiple times in the same request', 'Luci Exception Error Msg Actual : {}'.format(luciExp['errorMsg']))

    @pytest.mark.parametrize('description, redeemCoupons, configRequest, redeemCount, expectedError', [
        ('Multiple redeem True and redeem same coupon with valid coupon', 3, {'same_user_multiple_redeem' : True, 'multiple_use' : True}, 5, []),
        ('Multiple redeem True and redemption limit in series per user 2', 3, {'same_user_multiple_redeem': True, 'multiple_use': True, 'max_redemptions_in_series_per_user': 2}, 5, []),
        ('Multiple redeem for same user False and redeem same coupon with valid coupon', 3, {'same_user_multiple_redeem' : False, 'multiple_use' : True}, 1, {'errorCode': [645, 604], 'errorMsg': ['there are some failed redemption exists', 'multiple redemptions for user not allowed']}),
        ('Multiple redeem True and min days between redemption', 3, {'same_user_multiple_redeem' : True, 'multiple_use' : True, 'min_days_between_redemption' : 2}, 1, {'errorCode': [645, 622], 'errorMsg': ['there are some failed redemption exists', 'redemption gap of user is lesser than the config redemption gap']}),
        ('Multiple redeem True and redemption limit in series per user 1', 3, {'same_user_multiple_redeem' : True, 'multiple_use' : True, 'max_redemptions_in_series_per_user' : 1}, 1, {'errorCode': [645, 600], 'errorMsg': ['there are some failed redemption exists', 'multiple redemptions per user exceeded the limit']}),
        ('Multiple redeem True and redemption limit in series', 3, {'same_user_multiple_redeem' : True, 'multiple_use' : True, 'max_redeem' : 1}, 1, {'errorCode': [645, 605], 'errorMsg': ['there are some failed redemption exists', 'max redeem for series exceeded']}),
        ('Multiple use False and redemption limit in series', 3, {'same_user_multiple_redeem' : True, 'multiple_use' : False}, 1, {'errorCode': [645, 603], 'errorMsg': ['there are some failed redemption exists', 'multiple coupon redemptions not allowed']})
    ])
    def test_LUCI_MCR_15(self, description, redeemCoupons, configRequest,redeemCount,expectedError):
        couponSeriesIdList = list()
        couponCodeList = list()
        for _ in range(redeemCoupons):
            couponSeriesIdList.append(LuciHelper.saveCouponConfigAndAssertions(self)[1])

        for couponSeriesId in couponSeriesIdList:
            couponCodeList.append(LuciHelper.issueCouponAndAssertions(self, couponSeriesId)[0])

        couponSeriesIdUser2 = LuciHelper.saveCouponConfigAndAssertions(self, couponConfigReq=configRequest)[1]
        user2CouponCode = LuciHelper.issueCouponAndAssertions(self, couponSeriesIdUser2)[0]

        LuciHelper.redeemCouponAndAssertions(self,couponSeriesIdUser2,user2CouponCode)

        couponSeriesIdList.append(couponSeriesIdUser2)
        couponCodeList.append(user2CouponCode)
        LuciHelper.redeemCouponAndAssertions(self, couponSeriesIdList, couponCodeList, error=expectedError)

        couponSeriesIds = ','.join(map(str, couponSeriesIdList))
        redeemedCouponCount = LuciDBHelper.getRedeemCouponCount(couponSeriesId=couponSeriesIds, conditionList=[self.userId, self.billId, constant.config['tillIds'][0]])
        Assertion.constructAssertion(redeemedCouponCount == redeemCount, 'Mismatch Redemption details in voucher_redemptions & coupon_redemptions Actual: {} and Expected: {}'.format(redeemedCouponCount, redeemCount))

    @pytest.mark.parametrize('description, redeemCoupons, configRequest, redeemCount, expectedError', [
        ('valid Redeem at store', 3, {'redeem_at_store' : 0}, 3, {}),
        ('Invalid Redeem at store', 3, {'redeem_at_store' : 1}, 0, {'errorCode': [645, 624], 'errorMsg': ['there are some failed redemption exists', 'current store is not configured for redemption']}),
        ('Redemption valid from 1 day ahead', 3, {'valid_till_date' : Utils.getTime(days=3,milliSeconds=True), 'redemption_valid_from' : Utils.getTime(days=1,milliSeconds=True)}, 0, {'errorCode': [645, 628], 'errorMsg': ['there are some failed redemption exists', 'event date is lesser than redemption validity date']}),
        ('Redemption valid after days 1 day ahead', 3, {'valid_till_date' : Utils.getTime(days=3,milliSeconds=True), 'redemption_valid_from' : None, 'redemption_valid_after_days' : 1}, 0, {'errorCode': [645, 628], 'errorMsg': ['there are some failed redemption exists', 'event date is lesser than redemption validity date']}),
        ('Redemption Range 1 day ahead', 3, {'valid_till_date' : Utils.getTime(days=3,milliSeconds=True), 'redemption_range' : '{"dom":["' + str(constant.config['dateTime']['day'] + 1) + '"],"dow":[],"hours":["3"]}'}, 0, {'errorCode': [645, 623], 'errorMsg': ['there are some failed redemption exists', 'redemption outside the defined range']}),
    ])
    def test_LUCI_MCR_16(self, description, redeemCoupons, configRequest,redeemCount, expectedError):
        couponSeriesIdList = list()
        couponCodeList = list()
        configOne = True
        if 'redeem_at_store' in configRequest:
            configRequest.update({'redeem_at_store' : '[' + str(constant.config['tillIds'][configRequest['redeem_at_store']]) + ']'})
        for _ in range(redeemCoupons):
            if not configOne:
                couponSeriesIdList.append(LuciHelper.saveCouponConfigAndAssertions(self)[1])
            else:
                couponSeriesIdList.append(LuciHelper.saveCouponConfigAndAssertions(self, couponConfigReq=configRequest)[1])
                configOne = False

        for couponSeriesId in couponSeriesIdList:
            couponCodeList.append(LuciHelper.issueCouponAndAssertions(self, couponSeriesId)[0])

        LuciHelper.redeemCouponAndAssertions(self, couponSeriesIdList, couponCodeList, error=expectedError)
        couponSeriesIds = ','.join(map(str, couponSeriesIdList))
        redeemedCouponCount = LuciDBHelper.getRedeemCouponCount(couponSeriesId=couponSeriesIds, conditionList=[self.userId, self.billId, constant.config['tillIds'][0]])
        Assertion.constructAssertion(redeemedCouponCount == redeemCount, 'Mismatch Redemption details in voucher_redemptions & coupon_redemptions Actual: {} and Expected: {}'.format(redeemedCouponCount, redeemCount))

    @pytest.mark.parametrize('description, redeemCoupons, configRequest, redeemCount, expectedError', [
        ('Invalid Allow Multiple voucher & redeem limit 1', 3, {'do_not_resend_existing_voucher' : True, 'allow_multiple_vouchers_per_user' : True, 'max_redeem' : 1}, 0, {'errorCode' : [645, 605, 605], 'errorMsg' : ['there are some failed redemption exists', 'max redeem for series exceeded', 'max redeem for series exceeded']}),
        ('Invalid Redeem at store', 3, {'do_not_resend_existing_voucher' : True, 'allow_multiple_vouchers_per_user' : True, 'redeem_at_store': 1}, 0, {'errorCode': [645, 624, 624, 624], 'errorMsg': ['there are some failed redemption exists', 'current store is not configured for redemption', 'current store is not configured for redemption' , 'current store is not configured for redemption']}),
        ('Invalid Redemption valid from 1 day ahead', 3, {'do_not_resend_existing_voucher' : True, 'allow_multiple_vouchers_per_user' : True, 'valid_till_date': Utils.getTime(days=3, milliSeconds=True), 'redemption_valid_from': Utils.getTime(days=1, milliSeconds=True)}, 0, {'errorCode': [645, 628, 628, 628], 'errorMsg': ['there are some failed redemption exists', 'event date is lesser than redemption validity date', 'event date is lesser than redemption validity date', 'event date is lesser than redemption validity date']}),
        ('Invalid Redemption valid after days 1 day ahead', 3, {'do_not_resend_existing_voucher' : True, 'allow_multiple_vouchers_per_user' : True, 'valid_till_date': Utils.getTime(days=3, milliSeconds=True), 'redemption_valid_from': None, 'redemption_valid_after_days': 1}, 0, {'errorCode': [645, 628, 628, 628], 'errorMsg': ['there are some failed redemption exists', 'event date is lesser than redemption validity date', 'event date is lesser than redemption validity date', 'event date is lesser than redemption validity date']}),
        ('Invalid Redemption Range 1 day ahead', 3, {'do_not_resend_existing_voucher' : True, 'allow_multiple_vouchers_per_user' : True, 'valid_till_date': Utils.getTime(days=3, milliSeconds=True), 'redemption_range': '{"dom":["' + str(constant.config['dateTime']['day'] + 1) + '"],"dow":[],"hours":["3"]}'}, 0, {'errorCode': [645, 623, 623,623], 'errorMsg': ['there are some failed redemption exists', 'redemption outside the defined range', 'redemption outside the defined range', 'redemption outside the defined range']}),
        ('Invalid Bill amount more than max amount and issued to user2 anyUser True ', 3, {'do_not_resend_existing_voucher' : True, 'allow_multiple_vouchers_per_user' : True, 'min_bill_amount': 100, 'max_bill_amount': 500}, 0, {'errorCode': [645, 901, 901, 901], 'errorMsg': ['there are some failed redemption exists', 'bill amount more than the maximum limit set', 'bill amount more than the maximum limit set', 'bill amount more than the maximum limit set']}),
        ('Invalid Multiple redeem True and min days between redemption', 3, {'do_not_resend_existing_voucher' : True, 'allow_multiple_vouchers_per_user' : True, 'same_user_multiple_redeem': True, 'multiple_use': True, 'min_days_between_redemption': 2}, 0, {'errorCode': [645, 622,622], 'errorMsg': ['there are some failed redemption exists', 'redemption gap of user is lesser than the config redemption gap', 'redemption gap of user is lesser than the config redemption gap']})
    ])
    def test_LUCI_MCR_17(self, description, redeemCoupons, configRequest,redeemCount, expectedError):
        couponSeriesIdList = list()
        couponCodeList = list()
        configOne = True
        if 'redeem_at_store' in configRequest:
            configRequest.update({'redeem_at_store' : '[' + str(constant.config['tillIds'][configRequest['redeem_at_store']]) + ']'})
        for _ in range(redeemCoupons):
            if not configOne:
                couponSeriesIdList.append(LuciHelper.saveCouponConfigAndAssertions(self)[1])
            else:
                couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self, couponConfigReq=configRequest)[1]
                couponSeriesIdList.append(couponSeriesId)
                couponSeriesIdList.append(couponSeriesId)
                couponSeriesIdList.append(couponSeriesId)
                configOne = False

        for couponSeriesId in couponSeriesIdList:
            couponCodeList.append(LuciHelper.issueCouponAndAssertions(self, couponSeriesId)[0])

        LuciHelper.redeemCouponAndAssertions(self, couponSeriesIdList, couponCodeList, error=expectedError)
        couponSeriesIds = ','.join(map(str, couponSeriesIdList))
        redeemedCouponCount = LuciDBHelper.getRedeemCouponCount(couponSeriesId=couponSeriesIds, conditionList=[self.userId, self.billId, constant.config['tillIds'][0]])
        Assertion.constructAssertion(redeemedCouponCount == redeemCount, 'Mismatch Redemption details in voucher_redemptions & coupon_redemptions Actual: {} and Expected: {}'.format(redeemedCouponCount, redeemCount))

    @pytest.mark.parametrize('description, redeemCoupons, configRequest, redeemCount, expectedError', [
        ('Anyone can redeem -Allow Multiple voucher & redeem No limit', 3, {'any_user' : True, 'do_not_resend_existing_voucher' : True, 'allow_multiple_vouchers_per_user' : True}, 4, {}),
        ('Anyone can redeem -Allow Multiple voucher & redeem limit 1', 3, {'any_user' : True, 'do_not_resend_existing_voucher' : True, 'allow_multiple_vouchers_per_user' : True, 'max_redeem' : 1}, 0, {'errorCode' : [645, 605], 'errorMsg' : ['there are some failed redemption exists', 'max redeem for series exceeded']})
    ])
    def test_LUCI_MCR_18(self, description, redeemCoupons, configRequest,redeemCount, expectedError):
        couponSeriesIdList = list()
        couponCodeList = list()
        for _ in range(redeemCoupons):
                couponSeriesIdList.append(LuciHelper.saveCouponConfigAndAssertions(self, couponConfigReq=configRequest)[1])

        couponSeriesIdList.append(couponSeriesIdList[0])
        for couponSeriesId in couponSeriesIdList:
            couponCodeList.append(LuciHelper.issueCouponAndAssertions(self, couponSeriesId)[0])

        self.userId = constant.config['usersInfo'][1]['userId']
        LuciHelper.redeemCouponAndAssertions(self, couponSeriesIdList, couponCodeList, couponIssuedTo=[constant.config['usersInfo'][0]['userId']], error=expectedError)
        couponSeriesIds = ','.join(map(str, couponSeriesIdList))
        redeemedCouponCount = LuciDBHelper.getRedeemCouponCount(couponSeriesId=couponSeriesIds, conditionList=[self.userId, self.billId, constant.config['tillIds'][0]])
        Assertion.constructAssertion(redeemedCouponCount == redeemCount, 'Mismatch Redemption details in voucher_redemptions & coupon_redemptions Actual: {} and Expected: {}'.format(redeemedCouponCount, redeemCount))

    @pytest.mark.parametrize('description, redeemCoupons, configRequest, changeConfigRequest, redeemCount, expectedError', [
        ('Redeem expired coupon series valid till date None & updated date', 3, {'valid_till_date' : None ,'owner_id' : constant.config['campaignId'], 'ownerValidity' : Utils.getTime(days=2,milliSeconds=True), 'owned_by' : 2} ,{'fixedExpiryDate' : Utils.getTime(days=-1, milliSeconds=True)}, 0, {'errorCode' : [645, 635], 'errorMsg' : ['there are some failed redemption exists', 'coupon series already expired']}),
        ('Redeem expired coupon series set valid till date & updated date', 3, {'owner_id' : constant.config['campaignId'], 'ownerValidity' : Utils.getTime(days=2,milliSeconds=True), 'owned_by' : 2} ,{'fixedExpiryDate' : Utils.getTime(days=-1, milliSeconds=True)}, 0, {'errorCode' : [645, 635], 'errorMsg' : ['there are some failed redemption exists', 'coupon series already expired']}),
        ('Redeem expired coupon series valid till date None & ownerValidity Expired', 3, {'valid_till_date' : None,'owner_id' : constant.config['campaignId'], 'ownerValidity' : Utils.getTime(days=2,milliSeconds=True), 'owned_by' : 2} ,{'ownerValidity' : Utils.getTime(days=-1, milliSeconds=True)}, 0, {'errorCode' : [645, 635], 'errorMsg' : ['there are some failed redemption exists', 'coupon series already expired']}),
        ('Redeem expired coupon series valid till date & ownerValidity Expired', 3, {'owner_id' : constant.config['campaignId'], 'ownerValidity' : Utils.getTime(days=2,milliSeconds=True), 'owned_by' : 2} ,{'ownerValidity' : Utils.getTime(days=-1, milliSeconds=True)}, 0, {'errorCode' : [645, 635], 'errorMsg' : ['there are some failed redemption exists', 'coupon series already expired']}),
    ])
    def test_LUCI_MCR_19(self, description, redeemCoupons, configRequest, changeConfigRequest, redeemCount, expectedError):
        couponSeriesIdList = list()
        couponCodeList = list()
        configOne = True
        for _ in range(redeemCoupons):
            if not configOne:
                couponSeriesIdList.append(LuciHelper.saveCouponConfigAndAssertions(self)[1])
            else:
                couponConfig, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self, couponConfigReq=configRequest)
                couponSeriesIdList.append(couponSeriesId)
                configOne = False

        for couponSeriesId in couponSeriesIdList:
            couponCodeList.append(LuciHelper.issueCouponAndAssertions(self, couponSeriesId)[0])

        couponConfig.update(changeConfigRequest)
        LuciHelper.saveCouponConfigAndAssertions(self,couponConfigReq=couponConfig)
        LuciHelper.redeemCouponAndAssertions(self, couponSeriesIdList, couponCodeList, couponIssuedTo=[constant.config['usersInfo'][0]['userId']], error=expectedError)
        couponSeriesIds = ','.join(map(str, couponSeriesIdList))
        redeemedCouponCount = LuciDBHelper.getRedeemCouponCount(couponSeriesId=couponSeriesIds, conditionList=[self.userId, self.billId, constant.config['tillIds'][0]])
        Assertion.constructAssertion(redeemedCouponCount == redeemCount, 'Mismatch Redemption details in voucher_redemptions & coupon_redemptions Actual: {} and Expected: {}'.format(redeemedCouponCount, redeemCount))

    @pytest.mark.parametrize('description, orgId', [
        ('Invalid org_id ' , -1),
        ('Invalid org_id ' , 99999)
    ])
    def test_LUCI_MCR_20(self, description, orgId):
        try:
            redeemRequestList = []
            couponConfig, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self)
            couponConfig1, couponSeriesId1 = LuciHelper.saveCouponConfigAndAssertions(self)

            couponCode = LuciHelper.issueCouponAndAssertions(self, couponSeriesId)[0]
            couponCode1 = LuciHelper.issueCouponAndAssertions(self, couponSeriesId1)[0]

            redeemRequestList.append({'orgId': orgId, 'couponCode': couponCode, 'userId': constant.config['usersInfo'][0]['userId'], 'billId': self.billId, 'storeUnitId': constant.config['tillIds'][0]})
            redeemRequestList.append({'couponCode': couponCode1, 'userId': constant.config['usersInfo'][0]['userId'], 'billId': Utils.getTime(milliSeconds=True), 'storeUnitId': constant.config['tillIds'][1]})

            LuciHelper.redeemCouponAndAssertions(self, [couponSeriesId, couponSeriesId1], [couponCode, couponCode1], redeemCouponRequestList=self.redeemCouponsRequest(redeemRequestList))
            redeemedCouponCount = LuciDBHelper.getRedeemCouponCount(couponSeriesId=(str(couponSeriesId) + ',' + str(couponSeriesId1)), conditionList=[self.userId, self.billId, constant.config['tillIds'][0]])
            Assertion.constructAssertion(redeemedCouponCount == 0, 'Mismatch Redemption details in voucher_redemptions & coupon_redemptions Actual: {} and Expected: {}'.format(redeemedCouponCount, 0))
        except Exception, luciExp:
            luciExp = luciExp.__dict__
            Assertion.constructAssertion(luciExp['errorCode'] == constant.INVALID_ORG_ID, 'Luci Exception error code Actual: {} and Expected: {}'.format(luciExp['errorCode'], constant.INVALID_ORG_ID))
            Assertion.constructAssertion(luciExp['errorMsg'] == 'coupon level org id is not same as request org id', 'Luci Exception Error Msg Actual : {}'.format(luciExp['errorMsg']))


    @pytest.mark.parametrize('description, redeemCoupons, configRequest, redeemCount', [
        ('Multiple redeem True and today current hour redemption range', 3, {'same_user_multiple_redeem': True, 'multiple_use': True, 'redemption_range' : '{"dom":["' + str(constant.config['dateTime']['day']) + '"],"dow":[],"hours":["' + str(constant.config['dateTime']['hour']) + ',' + str(constant.config['dateTime']['hour']+1) + '"]}'}, 5 ),
        ('Redemption valid from current day', 3, {'valid_till_date': Utils.getTime(days=3, milliSeconds=True), 'redemption_valid_from': Utils.getTime(milliSeconds=True)}, 4),
        ('Redemption valid after days current day', 3, {'valid_till_date': Utils.getTime(days=3, milliSeconds=True), 'redemption_valid_from': None, 'redemption_valid_after_days': 0}, 4),
    ])
    def test_LUCI_MCR_21(self, description, redeemCoupons, configRequest, redeemCount):
        couponSeriesIdList = list()
        couponCodeList = list()
        for _ in range(redeemCoupons):
            couponSeriesIdList.append(LuciHelper.saveCouponConfigAndAssertions(self)[1])

        for couponSeriesId in couponSeriesIdList:
            couponCodeList.append(LuciHelper.issueCouponAndAssertions(self, couponSeriesId)[0])

        couponSeriesIdUser2 = LuciHelper.saveCouponConfigAndAssertions(self, couponConfigReq=configRequest)[1]
        user2CouponCode= LuciHelper.issueCouponAndAssertions(self, couponSeriesIdUser2)[0]

        if 'multiple_use' in configRequest:
            LuciHelper.redeemCouponAndAssertions(self, couponSeriesIdUser2, user2CouponCode)

        couponSeriesIdList.append(couponSeriesIdUser2)
        couponCodeList.append(user2CouponCode)
        LuciHelper.redeemCouponAndAssertions(self, couponSeriesIdList, couponCodeList)

        couponSeriesIds = ','.join(map(str, couponSeriesIdList))
        redeemedCouponCount = LuciDBHelper.getRedeemCouponCount(couponSeriesId=couponSeriesIds, conditionList=[self.userId, self.billId, constant.config['tillIds'][0]])
        Assertion.constructAssertion(redeemedCouponCount == redeemCount, 'Mismatch Redemption details in voucher_redemptions & coupon_redemptions Actual: {} and Expected: {}'.format(redeemedCouponCount, redeemCount))

    @pytest.mark.parametrize('description, redeemCoupons, configRequest, redeemCount', [
        ('Valid Allow Multiple voucher & redeem No limit ', 3, {'do_not_resend_existing_voucher' : True, 'allow_multiple_vouchers_per_user' : True}, 4),
        ('Valid Allow Multiple voucher & redeem limit 2', 3, {'do_not_resend_existing_voucher' : True, 'allow_multiple_vouchers_per_user' : True, 'max_redeem' : 2}, 4),
        ('Valid Allow Multiple voucher & redemptions in series per user limit 2', 3, {'do_not_resend_existing_voucher' : True, 'allow_multiple_vouchers_per_user' : True, 'max_redemptions_in_series_per_user' : 2}, 4),
        ('Valid Redeem at store', 3, {'do_not_resend_existing_voucher' : True, 'allow_multiple_vouchers_per_user' : True, 'redeem_at_store': 0}, 4),
        ('Valid Redemption valid from current day', 3, {'do_not_resend_existing_voucher' : True, 'allow_multiple_vouchers_per_user' : True, 'valid_till_date': Utils.getTime(days=3, milliSeconds=True), 'redemption_valid_from': Utils.getTime(milliSeconds=True)}, 4),
        ('Valid Redemption valid after 0 day ', 3, {'do_not_resend_existing_voucher' : True, 'allow_multiple_vouchers_per_user' : True, 'valid_till_date': Utils.getTime(days=3, milliSeconds=True), 'redemption_valid_from': None, 'redemption_valid_after_days': 0}, 4),
        ('Valid Redemption Range current day current hour', 3, {'do_not_resend_existing_voucher' : True, 'allow_multiple_vouchers_per_user' : True, 'valid_till_date': Utils.getTime(days=3, milliSeconds=True), 'redemption_range': '{"dom":["' + str(constant.config['dateTime']['day']) + '"],"dow":[],"hours":["' + str(constant.config['dateTime']['hour']) + ',' + str(constant.config['dateTime']['hour']+1) + '"]}'},4),
        ('Valid Bill amount min & Max', 3, {'do_not_resend_existing_voucher' : True, 'allow_multiple_vouchers_per_user' : True, 'min_bill_amount': 100, 'max_bill_amount': 5000}, 4)
    ])
    def test_LUCI_MCR_22(self, description, redeemCoupons, configRequest,redeemCount):
        couponSeriesIdList = list()
        couponCodeList = list()
        couponSeries = None
        configOne = True
        if 'redeem_at_store' in configRequest:
            configRequest.update({'redeem_at_store' : '[' + str(constant.config['tillIds'][configRequest['redeem_at_store']]) + ']'})
        for _ in range(redeemCoupons):
            if not configOne:
                couponSeriesIdList.append(LuciHelper.saveCouponConfigAndAssertions(self)[1])
            else:
                couponSeries = LuciHelper.saveCouponConfigAndAssertions(self, couponConfigReq=configRequest)[1]
                couponSeriesIdList.append(couponSeries)
                couponSeriesIdList.append(couponSeries)
                configOne = False

        Logger.log('coupon Series list : ', couponSeriesIdList)
        for couponSeriesId in couponSeriesIdList:
            couponCodeList.append(LuciHelper.issueCouponAndAssertions(self, couponSeriesId)[0])


        LuciHelper.redeemCouponAndAssertions(self, couponSeriesIdList, couponCodeList)
        couponSeriesIds = ','.join(map(str, couponSeriesIdList))
        redeemedCouponCount = LuciDBHelper.getRedeemCouponCount(couponSeriesId=couponSeriesIds, conditionList=[self.userId, self.billId, constant.config['tillIds'][0]])
        Assertion.constructAssertion(redeemedCouponCount == redeemCount, 'Mismatch Redemption details in voucher_redemptions & coupon_redemptions Actual: {} and Expected: {}'.format(redeemedCouponCount, redeemCount))
        for couponSeriesId in couponSeriesIdList:
            if couponSeriesId == couponSeries:
                LuciHelper.getCouponConfigAndAssertion(self, couponSeriesId, 2, 2)
            else:
                LuciHelper.getCouponConfigAndAssertion(self, couponSeriesId, 1, 1)


    @pytest.mark.parametrize('description, redeemCoupons, configRequest', [
        ('Partnel coupon issue & redeem', 1, {'source_org_id' : 0 , 'any_user' : True})
    ])
    def test_LUCI_MCR_26(self, description, redeemCoupons, configRequest):
        couponSeriesIdList = list()
        for _ in range(redeemCoupons):
            couponSeriesIdList.append(LuciHelper.saveCouponConfigAndAssertions(self, couponConfigReq=configRequest)[1])

        partnerObj = LuciObject.issuePartnerCouponRequest({'couponSeriesId' : couponSeriesIdList[0], 'clusterAdminUserId' : 4, 'partnerOrgId' : 0 , 'partnerIssuedById' : 4})
        couponDetails = self.connObj.issuePartnerCoupon(partnerObj)[0].__dict__
        couponCode = couponDetails['couponCode']
        LuciHelper.redeemCouponAndAssertions(self, couponSeriesIdList, couponCode, couponIssuedTo=[-1])

    @pytest.mark.parametrize('description, redeemCoupons', [('Redeem valid 2 Coupon', 4)])
    def test_LUCI_MCR_27_sanity(self,description, redeemCoupons):
        couponSeriesIdList = list()
        couponCodeList = list()

        externalCSId = LuciHelper.saveCouponConfigAndAssertions(self, couponConfigReq={'client_handling_type' : 'DISC_CODE_PIN' , 'any_user' : True, 'isExternalIssual' : True})[1]
        couponSeriesIdList.append(externalCSId)
        exCouponCode = LuciHelper.generateCouponCode().lower()
        exCouponCode = LuciHelper.uploadCouponAndAssertions(self, externalCSId, self.constructObj.importType['NONE'], noOfCouponsToBeUpload=1, couponCode=exCouponCode, dracraysUpload={'couponCodeCAPS' : False})['coupons'][0]
        couponCodeList.append(exCouponCode)


        dcpCSId = LuciHelper.saveCouponConfigAndAssertions(self, couponConfigReq={'client_handling_type': 'DISC_CODE_PIN'})[1]
        couponSeriesIdList.append(dcpCSId)
        dcpCouponCode = LuciHelper.generateCouponCode().lower()
        dcpCouponCode = LuciHelper.uploadCouponAndAssertions(self, dcpCSId, self.constructObj.importType['NONE'], couponCode=dcpCouponCode, dracraysUpload={'couponCodeCAPS' : False})['coupons'][0]
        couponCodeList.append(dcpCouponCode)
        LuciHelper.issueCouponAndAssertions(self, dcpCSId)[0]

        DCCSId = LuciHelper.saveCouponConfigAndAssertions(self,couponConfigReq={'client_handling_type' : 'DISC_CODE'})[1]
        couponSeriesIdList.append(DCCSId)
        time.sleep(2)

        DCCouponCode = LuciHelper.issueCouponAndAssertions(self, DCCSId)[0]
        couponCodeList.append(DCCouponCode.lower())

        GenericCouponCode = LuciHelper.generateCouponCode().lower()
        GencouponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self, couponConfigReq={'client_handling_type': 'GENERIC', 'genericCode': GenericCouponCode})[1]
        couponSeriesIdList.append(GencouponSeriesId)
        couponCodeList.append(GenericCouponCode)
        LuciHelper.issueCouponAndAssertions(self, GencouponSeriesId)[0]


        LuciHelper.redeemCouponAndAssertions(self, couponSeriesIdList, couponCodeList, couponIssuedTo=[self.userId, -1])
        couponSeriesIds = ','.join(map(str,couponSeriesIdList))
        redeemedCouponCount = LuciDBHelper.getRedeemCouponCount(couponSeriesId=couponSeriesIds, conditionList=[self.userId, self.billId, constant.config['tillIds'][0]])
        Assertion.constructAssertion(redeemCoupons == redeemedCouponCount, 'Mismatch Redemption details in voucher_redemptions & coupon_redemptions Actual: {} and Expected: {}'.format(redeemCoupons, redeemedCouponCount))
        for couponSeriesId in couponSeriesIdList:
            LuciHelper.getCouponConfigAndAssertion(self, couponSeriesId, 1, 1)

    @pytest.mark.parametrize('description, redeemCoupons', [('Redeem valid 2 Coupon', 0)])
    def test_LUCI_MCR_28_sanity(self,description, redeemCoupons):
        couponSeriesIdList = list()
        couponCodeList = list()

        externalCSId = LuciHelper.saveCouponConfigAndAssertions(self, couponConfigReq={'client_handling_type' : 'DISC_CODE_PIN' , 'any_user' : True, 'isExternalIssual' : True, 'min_bill_amount' : 9999 , 'max_bill_amount' : 999999999})[1]
        couponSeriesIdList.append(externalCSId)
        exCouponCode = LuciHelper.generateCouponCode().lower()
        exCouponCode = LuciHelper.uploadCouponAndAssertions(self, externalCSId, self.constructObj.importType['NONE'], noOfCouponsToBeUpload=1, couponCode=exCouponCode, dracraysUpload={'couponCodeCAPS' : False})['coupons'][0]
        couponCodeList.append(exCouponCode)

        dcpCSId = LuciHelper.saveCouponConfigAndAssertions(self, couponConfigReq={'client_handling_type': 'DISC_CODE_PIN'})[1]
        couponSeriesIdList.append(dcpCSId)
        dcpCouponCode = LuciHelper.generateCouponCode().lower()
        dcpCouponCode = LuciHelper.uploadCouponAndAssertions(self, dcpCSId, self.constructObj.importType['NONE'], couponCode=dcpCouponCode, dracraysUpload={'couponCodeCAPS' : False})['coupons'][0]
        couponCodeList.append(dcpCouponCode)
        LuciHelper.issueCouponAndAssertions(self, dcpCSId)[0]

        DCCSId = LuciHelper.saveCouponConfigAndAssertions(self,couponConfigReq={'client_handling_type' : 'DISC_CODE'})[1]
        couponSeriesIdList.append(DCCSId)
        time.sleep(2)

        DCCouponCode = LuciHelper.issueCouponAndAssertions(self, DCCSId)[0]
        DCCouponCode = DCCouponCode.lower()
        couponCodeList.append(DCCouponCode)

        GenericCouponCode = LuciHelper.generateCouponCode().lower()
        GencouponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self, couponConfigReq={'client_handling_type': 'GENERIC', 'genericCode': GenericCouponCode})[1]
        couponSeriesIdList.append(GencouponSeriesId)
        couponCodeList.append(GenericCouponCode)
        LuciHelper.issueCouponAndAssertions(self, GencouponSeriesId)[0]


        LuciHelper.redeemCouponAndAssertions(self, couponSeriesIdList, couponCodeList, couponIssuedTo=[self.userId, -1], error={'errorCode': [645, 900], 'errorMsg': ['there are some failed redemption exists', 'bill amount less than the minimum limit set']})
        couponSeriesIds = ','.join(map(str,couponSeriesIdList))
        redeemedCouponCount = LuciDBHelper.getRedeemCouponCount(couponSeriesId=couponSeriesIds, conditionList=[self.userId, self.billId, constant.config['tillIds'][0]])
        Assertion.constructAssertion(redeemCoupons == redeemedCouponCount, 'Mismatch Redemption details in voucher_redemptions & coupon_redemptions Actual: {} and Expected: {}'.format(redeemedCouponCount, redeemCoupons))
        for couponSeriesId in couponSeriesIdList:
            LuciHelper.getCouponConfigAndAssertion(self, couponSeriesId, 1, 0)

    @pytest.mark.parametrize('description, redeemCoupons, configRequest, redeemCount, expectedError', [
        ('Anyone can redeem -Allow Multiple voucher & redemptions in series per user limit 1', 3, {'any_user' : True,'do_not_resend_existing_voucher' : True, 'allow_multiple_vouchers_per_user' : True, 'max_redemptions_in_series_per_user' : 1}, 4, {'errorCode' : [645, 600], 'errorMsg' : ['there are some failed redemption exists', 'multiple redemptions per user exceeded the limit']}),
    ])
    def test_LUCI_MCR_29_sanity(self, description, redeemCoupons, configRequest,redeemCount, expectedError):
        couponSeriesIdList = list()
        couponCodeList1 = list()
        couponCodeList2 = list()
        for _ in range(redeemCoupons):
                couponSeriesIdList.append(LuciHelper.saveCouponConfigAndAssertions(self, couponConfigReq=configRequest)[1])

        couponSeriesIdList.append(couponSeriesIdList[0])
        for couponSeriesId in couponSeriesIdList:
            couponCodeList1.append(LuciHelper.issueCouponAndAssertions(self, couponSeriesId)[0])
            couponCodeList2.append(LuciHelper.issueCouponAndAssertions(self, couponSeriesId)[0])
        couponCodeList2.append(couponCodeList1[0])

        self.userId = constant.config['usersInfo'][1]['userId']
        LuciHelper.redeemCouponAndAssertions(self, couponSeriesIdList, couponCodeList1, couponIssuedTo=[constant.config['usersInfo'][0]['userId']])
        LuciHelper.redeemCouponAndAssertions(self, couponSeriesIdList, couponCodeList2, couponIssuedTo=[constant.config['usersInfo'][0]['userId']], error=expectedError, isRedeem=False)
        couponSeriesIds = ','.join(map(str, couponSeriesIdList))
        redeemedCouponCount = LuciDBHelper.getRedeemCouponCount(couponSeriesId=couponSeriesIds, conditionList=[self.userId, self.billId, constant.config['tillIds'][0]])
        Assertion.constructAssertion(redeemedCouponCount == redeemCount, 'Mismatch Redemption details in voucher_redemptions & coupon_redemptions Actual: {} and Expected: {}'.format(redeemedCouponCount, redeemCount))