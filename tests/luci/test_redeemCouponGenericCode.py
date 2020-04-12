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

class Test_RedeemCouponGenericCode():

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
        constant.config['requestId'] = 'luci_auto_'+str(random.randint(11111, 99999))
        self.userId = constant.config['usersInfo'][0]['userId']

    @pytest.mark.parametrize('description, uploadType', [
        ('redeem Coupons & upload users type is userId', 'USER_ID'),
        ('redeem Coupons & upload users type is Mobile', 'MOBILE')
    ])
    def test_LUCI_RC_GC_011_sanity(self,description, uploadType):
        #Save Coupon Config
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self)
        LuciHelper.queuePumpWait(self, couponSeriesId)
        LuciHelper.couponPumpAssertion(self, couponSeriesId)

        #Update the coupon series from DC -> Generic
        couponCode = LuciHelper.generateCouponCode()
        couponConfigObj.update({'client_handling_type' : 'GENERIC','genericCode' : couponCode})
        LuciHelper.saveCouponConfigAndAssertions(self, couponConfigReq=couponConfigObj)

        # upload coupon Code
        LuciHelper.uploadCouponAndAssertions(self,couponSeriesId, self.constructObj.importType[uploadType],self.userId, couponCode=couponCode,dracraysUpload={'userOnly' : True,})
        couponIssued = LuciDBHelper.getCouponsIssued(couponSeriesId, self.userId, couponCode)
        Assertion.constructAssertion(couponIssued != {}, 'Issued Coupons are recorded in coupons_issued ')
        Assertion.constructAssertion(couponIssued['issuedBy'] == constant.config['adminId'], 'Coupon Issued by userId')

        # CouponConfigAssertion
        LuciHelper.getCouponConfigAndAssertion(self,couponSeriesId, 1, 0)
        # GetCoupon Details and Assertion.constructAssertion(on)
        couponDetailsRequest = {'onlyActive': True, 'couponCodeFilter': [couponCode]}
        LuciHelper.getCouponDetailsAndAssertion(self,couponSeriesId, couponCode, couponDetailsRequest)

        # redeem Coupon and Assertion.constructAssertion(on)
        LuciHelper.redeemCouponAndAssertions(self, couponSeriesId, couponCode)
        LuciHelper.redemptionDBAssertion(self,couponSeriesId)
        # CouponConfigAssertion
        LuciHelper.getCouponConfigAndAssertion(self, couponSeriesId, 1, 1)

    @pytest.mark.parametrize('description', [('redeem Coupons(Generic) direct issue')])
    def test_LUCI_RC_GC_012_sanity(self,description):
        couponCode = LuciHelper.generateCouponCode()
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self, couponConfigReq={'client_handling_type' : 'GENERIC','genericCode' : couponCode})

        #issue coupon code to user
        couponCode = LuciHelper.issueCouponAndAssertions(self,couponSeriesId)[0]

        # CouponConfigAssertion
        LuciHelper.getCouponConfigAndAssertion(self,couponSeriesId, 1, 0)

        # redeem Coupon and Assertion.constructAssertion(on)
        LuciHelper.redeemCouponAndAssertions(self, couponSeriesId, couponCode)
        LuciHelper.redemptionDBAssertion(self,couponSeriesId)
        # CouponConfigAssertion
        LuciHelper.getCouponConfigAndAssertion(self,couponSeriesId, 1, 1)

    @pytest.mark.parametrize('description', [('Redeem case sentive coupon')])
    def test_LUCI_RC_GC_013_sanity(self,description):
        couponCode = LuciHelper.generateCouponCode().lower()
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self,couponConfigReq={'client_handling_type' : 'GENERIC','genericCode' : couponCode, 'any_user' : True, 'min_bill_amount' : 1500 , 'max_bill_amount' : 999999999})
        LuciHelper.issueCouponAndAssertions(self, couponSeriesId)[0]
        # CouponDetails Request
        LuciHelper.redeemCouponAndAssertions(self, couponSeriesId, couponCode, error=[900, 'bill amount less than the minimum limit set'])
        couponConfigObj.update({'min_bill_amount': 900})
        LuciHelper.saveCouponConfigAndAssertions(self, couponConfigReq=couponConfigObj)
        LuciHelper.redeemCouponAndAssertions(self, couponSeriesId, couponCode)

    @pytest.mark.parametrize('description', [('Redeem same coupon by different users Config Multiple use: True, any user: True')])
    def test_LUCI_RC_GC_014(self,description):
        couponCode = LuciHelper.generateCouponCode()
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self, couponConfigReq={'client_handling_type' : 'GENERIC','genericCode' : couponCode, 'multiple_use' : True, 'any_user' : True})

        couponCode = LuciHelper.issueCouponAndAssertions(self, couponSeriesId)[0]
        LuciHelper.getCouponConfigAndAssertion(self, couponSeriesId, 1, 0)
        LuciHelper.getCouponDetailsAndAssertion(self,couponSeriesId,couponCode, couponDetailsRequest={'onlyActive': True, 'couponCodeFilter': [couponCode]})
        #Coupon Redemption
        redeemedIds = [self.userId]
        LuciHelper.redeemCouponAndAssertions(self, couponSeriesId, couponCode, couponIssuedTo=[constant.config['usersInfo'][0]['userId']])
        self.userId = constant.config['usersInfo'][1]['userId']
        redeemedIds.append(self.userId)
        LuciHelper.redeemCouponAndAssertions(self, couponSeriesId, couponCode, couponIssuedTo=[constant.config['usersInfo'][0]['userId']])
        self.userId = constant.config['usersInfo'][2]['userId']
        redeemedIds.append(self.userId)
        LuciHelper.redeemCouponAndAssertions(self, couponSeriesId, couponCode, couponIssuedTo=[constant.config['usersInfo'][0]['userId']])
        LuciHelper.redemptionDBAssertion(self,couponSeriesId, numRedeemed=3, redeemedBy=redeemedIds)
        LuciHelper.getCouponConfigAndAssertion(self,couponSeriesId,1,3)

    @pytest.mark.parametrize('description, couponConfig, expectedError', [
        ('Redeem same coupon by different users Config Multiple use: True, any user: False', {'multiple_use' : True, 'any_user' : False}, [constant.REDEMPTION_FAILED_FOR_USER, 'coupon not issued to this user redemption failed']),
        ('Redeem coupon when redemption start date not reached', {'redemption_valid_from' : Utils.getTime(days=1, milliSeconds=True)}, [constant.REDEMPTION_VALIDITY_DATE_NOT_REACHED, 'event date is lesser than redemption validity date']),
        ('Redeem coupon Bill amount less than min_bill_amount : 1500', {'min_bill_amount' : 1500 , 'max_bill_amount' : 999999999}, [constant.BILL_AMOUNT_TOO_LOW, 'bill amount less than the minimum limit set']),
        ('Redeem coupon Bill amount more than max_bill_amount : 500', {'min_bill_amount' : 10 , 'max_bill_amount' : 500}, [constant.BILL_AMOUNT_TOO_HIGH, 'bill amount more than the maximum limit set'])
    ])
    def test_LUCI_RC_GC_015(self,description, couponConfig, expectedError):
        couponCode = LuciHelper.generateCouponCode()
        couponConfig.update({'client_handling_type' : 'GENERIC','genericCode' : couponCode})
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self, couponConfigReq=couponConfig)
        couponCode = LuciHelper.issueCouponAndAssertions(self, couponSeriesId)[0]
        #Coupon Redemption
        self.userId = constant.config['usersInfo'][1]['userId']
        LuciHelper.redeemCouponAndAssertions(self, couponSeriesId, couponCode, error=expectedError)

    @pytest.mark.parametrize('description, couponConfig, expectedError', [
        ('Redeem coupon Multiple time Config Multiple use: False, same_user_multiple_redeem: True', {'same_user_multiple_redeem' : True}, [constant.MULTIPLE_REDEMPTION_FOR_COUPON_NOT_ALLOWED, 'multiple coupon redemptions not allowed']),
        ('Redeem coupon Multiple time Config Multiple use: True, same_user_multiple_redeem: False', {'multiple_use' : True}, [constant.MULTIPLE_REDEMPTION_FOR_USER_AND_COUPON_NOT_ALLOWED, 'multiple redemptions for user not allowed']),
        ('Redeem coupon Multiple time Config Multiple use: True, same_user_multiple_redeem: False, redemption Gap: 1', {'multiple_use' : True, 'same_user_multiple_redeem' : True, 'min_days_between_redemption' : 1}, [constant.REDEMPTION_GAP_LOWER_THAN_EXPECTED, 'redemption gap of user is lesser than the config redemption gap'])
    ])
    def test_LUCI_RC_GC_016(self,description, couponConfig, expectedError):
        couponCode = LuciHelper.generateCouponCode()
        couponConfig.update({'client_handling_type': 'GENERIC', 'genericCode': couponCode})
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self, couponConfigReq=couponConfig)
        couponCode = LuciHelper.issueCouponAndAssertions(self, couponSeriesId)[0]
        #Coupon Redemption
        LuciHelper.redeemCouponAndAssertions(self, couponSeriesId, couponCode)
        LuciHelper.redeemCouponAndAssertions(self, couponSeriesId, couponCode, error=expectedError)
        LuciHelper.redemptionDBAssertion(self, couponSeriesId)

    @pytest.mark.parametrize('description, couponConfig, noOfRedeem', [
        ('Redeem coupon Multiple time Config Multiple use: True, same_user_multiple_redeem: True', {'multiple_use' : True, 'same_user_multiple_redeem' : True}, 3)
    ])
    def test_LUCI_RC_GC_017(self,description, couponConfig, noOfRedeem):
        couponCode = LuciHelper.generateCouponCode()
        couponConfig.update({'client_handling_type': 'GENERIC', 'genericCode': couponCode})
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self, couponConfigReq=couponConfig)
        couponCode = LuciHelper.issueCouponAndAssertions(self, couponSeriesId)[0]
        #Coupon Redemption
        for _ in range(noOfRedeem):
            LuciHelper.redeemCouponAndAssertions(self, couponSeriesId, couponCode)
        LuciHelper.redemptionDBAssertion(self, couponSeriesId, noOfRedeem)

    @pytest.mark.parametrize('description, couponConfig, noOfRedeem, expectedError', [
        ('Redeem coupon Multiple time Config Multiple use: True, same_user_multiple_redeem: True, redemption limit per user: 2', {'multiple_use' : True, 'same_user_multiple_redeem' : True, 'max_redemptions_in_series_per_user' : 2}, 2, [constant.MAX_REDEMPTION_PER_USER_EXCEEDED, 'multiple redemptions per user exceeded the limit']),
        ('Redeem coupon Multiple time Config Multiple use: True, same_user_multiple_redeem: True, redemption series limit: 2', {'multiple_use' : True, 'same_user_multiple_redeem' : True, 'max_redeem' : 2}, 2, [constant.MAX_REDEMPTION_FOR_SERIES_EXCEEDED, 'max redeem for series exceeded'])
    ])
    def test_LUCI_RC_GC_018(self,description, couponConfig, noOfRedeem, expectedError):
        couponCode = LuciHelper.generateCouponCode()
        couponConfig.update({'client_handling_type': 'GENERIC', 'genericCode': couponCode})
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self, couponConfigReq=couponConfig)
        couponCode = LuciHelper.issueCouponAndAssertions(self, couponSeriesId)[0]
        #Coupon Redemption
        for _ in range(noOfRedeem):
            LuciHelper.redeemCouponAndAssertions(self, couponSeriesId, couponCode)
        LuciHelper.redeemCouponAndAssertions(self, couponSeriesId, couponCode, error=expectedError)
        LuciHelper.redemptionDBAssertion(self, couponSeriesId, noOfRedeem)

    @pytest.mark.parametrize('description', [('isRedeem call commit: False')])
    def test_LUCI_RC_GC_019(self,description):
        couponCode = LuciHelper.generateCouponCode()
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self,couponConfigReq={'client_handling_type' : 'GENERIC','genericCode' : couponCode})
        couponCode = LuciHelper.issueCouponAndAssertions(self, couponSeriesId)[0]
        LuciHelper.redeemCouponAndAssertions(self, couponSeriesId, couponCode, isRedeem=False)
        LuciHelper.getCouponConfigAndAssertion(self, couponSeriesId, 1, 0)