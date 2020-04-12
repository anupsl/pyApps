import time, random,pytest
from src.Constant.constant import constant
from src.modules.luci.luciDBHelper import LuciDBHelper
from src.modules.luci.dracarysHelper import DracarysHelper
from src.modules.luci.dracarysObject import DracarysObject
from src.utilities.logger import Logger
from src.utilities.assertion import Assertion
from src.utilities.utils import Utils
from src.modules.luci.luciHelper import LuciHelper
from src.modules.luci.luciObject import LuciObject

class Test_RedeemCouponDiscCode():

    def setup_class(self):
        Logger.logSuiteName(str(self).split('.')[-1])
        self.constructObj = LuciObject()
        self.DracarysObj = DracarysObject()
        self.userId = constant.config['usersInfo'][0]['userId']
        self.tillId = constant.config['tillIds'][0]
        self.billId = Utils.getTime(milliSeconds=True)

    def setup_method(self, method):
        self.connObj = LuciHelper.getConnObj(newConnection=True)
        self.DracraysConnObj = DracarysHelper.getConnObj(newConnection=True)
        Logger.logMethodName(method.__name__)
        constant.config['uploadedFileName'] = method.__name__
        constant.config['requestId'] = 'luci_auto_'+str(random.randint(11111, 99999))
        self.userId = constant.config['usersInfo'][0]['userId']
        
    @pytest.mark.parametrize('description, uploadType', [
        ('redeem Coupons & upload users type is userId', 'USER_ID'),
        ('redeem Coupons & upload users type is Mobile', 'MOBILE')
    ])
    def test_LUCI_RC_DC_011_sanity(self, description, uploadType):
        #Save Coupon Config
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self)
        time.sleep(2)
        createdCouponCount = LuciDBHelper.getCouponsCreated_Count(couponSeriesId)
        Assertion.constructAssertion(createdCouponCount != 0, 'Coupon Code Pumped to Queue')

        couponCode = LuciHelper.uploadCouponAndAssertions(self,couponSeriesId,self.constructObj.importType[uploadType],dracraysUpload={'userOnly' : True})['coupons'][0]
        LuciHelper.getCouponConfigAndAssertion(self, couponSeriesId, 1, 0)

        LuciHelper.redeemCouponAndAssertions(self, couponSeriesId, couponCode)
        LuciHelper.redemptionDBAssertion(self, couponSeriesId)

        couponDetailsRequest = {'onlyActive': True, 'couponCodeFilter': [couponCode]}
        LuciHelper.getCouponDetailsAndAssertion(self,couponSeriesId,couponCode,couponDetailsRequest)
        couponDetailsRequest.update({'couponSeriesRequired' : True})
        LuciHelper.getCouponDetailsAndAssertion(self,couponSeriesId,couponCode,couponDetailsRequest)

    @pytest.mark.parametrize('description', [('redeem Coupons(Disc Code) direct issue')])
    def test_LUCI_RC_DC_012_sanity(self,description):
        #Save Coupon Config
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self)
        LuciHelper.queuePumpWait(self, couponSeriesId)
        LuciHelper.couponPumpAssertion(self, couponSeriesId)
        # issue coupon Code
        couponCode = LuciHelper.issueCouponAndAssertions(self,couponSeriesId)[0]
        # CouponConfigAssertion
        LuciHelper.getCouponConfigAndAssertion(self,couponSeriesId, 1, 0)
        # redeem Coupon and Assertion.constructAssertion(on)
        LuciHelper.redeemCouponAndAssertions(self, couponSeriesId, couponCode)
        LuciHelper.redemptionDBAssertion(self, couponSeriesId)
        LuciHelper.getCouponConfigAndAssertion(self,couponSeriesId, 1, 1)
        # GetCoupon Details and Assertion.constructAssertion(on)
        couponDetailsRequest = {'onlyActive': True, 'couponCodeFilter': [couponCode]}
        LuciHelper.getCouponDetailsAndAssertion(self,couponSeriesId,couponCode,couponDetailsRequest)

    @pytest.mark.parametrize('description', [('Redeem case sentive coupon')])
    def test_LUCI_DC_013_sanity_smoke(self, description):
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self,couponConfigReq={'client_handling_type' : 'DISC_CODE' , 'any_user' : True, 'min_bill_amount' : 1500 , 'max_bill_amount' : 999999999})
        time.sleep(2)
        couponCode = LuciHelper.issueCouponAndAssertions(self, couponSeriesId)[0]
        couponCode = couponCode.lower()
        # CouponDetails Request
        LuciHelper.redeemCouponAndAssertions(self, couponSeriesId, couponCode, error=[900, 'bill amount less than the minimum limit set'])

        couponConfigObj.update({'min_bill_amount': 900})
        LuciHelper.saveCouponConfigAndAssertions(self, couponConfigReq=couponConfigObj)
        LuciHelper.redeemCouponAndAssertions(self, couponSeriesId, couponCode)

    @pytest.mark.parametrize('description', [('Redeem same coupon by different users Config Multiple use: True, any user: True')])
    def test_LUCI_RC_DC_014(self,description):
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self, couponConfigReq={'multiple_use' : True, 'any_user' : True})
        LuciHelper.queuePumpWait(self, couponSeriesId)
        LuciHelper.couponPumpAssertion(self, couponSeriesId)

        #issueCode and Doing Assertion.constructAssertion(on)
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
    def test_LUCI_RC_DC_015(self,description, couponConfig, expectedError):
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self, couponConfigReq=couponConfig)
        LuciHelper.queuePumpWait(self, couponSeriesId)
        LuciHelper.couponPumpAssertion(self, couponSeriesId)
        couponCode = LuciHelper.issueCouponAndAssertions(self, couponSeriesId)[0]
        #Coupon Redemption
        self.userId = constant.config['usersInfo'][1]['userId']
        LuciHelper.redeemCouponAndAssertions(self, couponSeriesId, couponCode, error=expectedError)

    @pytest.mark.parametrize('description, couponConfig, expectedError', [
        ('Redeem coupon Multiple time Config Multiple use: False, same_user_multiple_redeem: True', {'same_user_multiple_redeem' : True}, [constant.MULTIPLE_REDEMPTION_FOR_COUPON_NOT_ALLOWED, 'multiple coupon redemptions not allowed']),
        ('Redeem coupon Multiple time Config Multiple use: True, same_user_multiple_redeem: False', {'multiple_use' : True}, [constant.MULTIPLE_REDEMPTION_FOR_USER_AND_COUPON_NOT_ALLOWED, 'multiple redemptions for user not allowed']),
        ('Redeem coupon Multiple time Config Multiple use: True, same_user_multiple_redeem: False, redemption Gap: 1', {'multiple_use' : True, 'same_user_multiple_redeem' : True, 'min_days_between_redemption' : 1}, [constant.REDEMPTION_GAP_LOWER_THAN_EXPECTED, 'redemption gap of user is lesser than the config redemption gap'])
    ])
    def test_LUCI_RC_DC_016(self,description, couponConfig, expectedError):
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self, couponConfigReq=couponConfig)
        LuciHelper.queuePumpWait(self, couponSeriesId)
        LuciHelper.couponPumpAssertion(self, couponSeriesId)
        couponCode = LuciHelper.issueCouponAndAssertions(self, couponSeriesId)[0]
        #Coupon Redemption
        LuciHelper.redeemCouponAndAssertions(self, couponSeriesId, couponCode)
        LuciHelper.redeemCouponAndAssertions(self, couponSeriesId, couponCode, error=expectedError)
        LuciHelper.redemptionDBAssertion(self, couponSeriesId)

    @pytest.mark.parametrize('description, couponConfig, noOfRedeem', [
        ('Redeem coupon Multiple time Config Multiple use: True, same_user_multiple_redeem: True', {'multiple_use' : True, 'same_user_multiple_redeem' : True}, 3)
    ])
    def test_LUCI_RC_DC_017(self,description, couponConfig, noOfRedeem):
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self, couponConfigReq=couponConfig)
        LuciHelper.queuePumpWait(self, couponSeriesId)
        LuciHelper.couponPumpAssertion(self, couponSeriesId)
        couponCode = LuciHelper.issueCouponAndAssertions(self, couponSeriesId)[0]
        #Coupon Redemption
        for _ in range(noOfRedeem):
            LuciHelper.redeemCouponAndAssertions(self, couponSeriesId, couponCode)
        LuciHelper.redemptionDBAssertion(self, couponSeriesId, noOfRedeem)

    @pytest.mark.parametrize('description, couponConfig, noOfRedeem, expectedError', [
        ('Redeem coupon Multiple time Config Multiple use: True, same_user_multiple_redeem: True, redemption limit per user: 2', {'multiple_use' : True, 'same_user_multiple_redeem' : True, 'max_redemptions_in_series_per_user' : 2}, 2, [constant.MAX_REDEMPTION_PER_USER_EXCEEDED, 'multiple redemptions per user exceeded the limit']),
        ('Redeem coupon Multiple time Config Multiple use: True, same_user_multiple_redeem: True, redemption series limit: 2', {'multiple_use' : True, 'same_user_multiple_redeem' : True, 'max_redeem' : 2}, 2, [constant.MAX_REDEMPTION_FOR_SERIES_EXCEEDED, 'max redeem for series exceeded'])
    ])
    def test_LUCI_RC_DC_018(self,description, couponConfig, noOfRedeem, expectedError):
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self, couponConfigReq=couponConfig)
        LuciHelper.queuePumpWait(self, couponSeriesId)
        LuciHelper.couponPumpAssertion(self, couponSeriesId)
        couponCode = LuciHelper.issueCouponAndAssertions(self, couponSeriesId)[0]
        #Coupon Redemption
        for _ in range(noOfRedeem):
            LuciHelper.redeemCouponAndAssertions(self, couponSeriesId, couponCode)
        LuciHelper.redeemCouponAndAssertions(self, couponSeriesId, couponCode, error=expectedError)
        LuciHelper.redemptionDBAssertion(self, couponSeriesId, noOfRedeem)

    @pytest.mark.parametrize('description', [('isRedeem call commit: False')])
    def test_LUCI_RC_DCP_019(self,description):
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self,)
        LuciHelper.queuePumpWait(self, couponSeriesId)
        LuciHelper.couponPumpAssertion(self, couponSeriesId)
        couponCode = LuciHelper.issueCouponAndAssertions(self, couponSeriesId)[0]
        LuciHelper.redeemCouponAndAssertions(self, couponSeriesId, couponCode, isRedeem=False)
        LuciHelper.getCouponConfigAndAssertion(self, couponSeriesId, 1, 0)

    @pytest.mark.parametrize('description', [('Redemption After Days')])
    def test_LUCI_RC_DC_020(self,description):
        #Save Coupon Config
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self,couponConfigReq={'redemption_valid_after_days' : 1, 'redemption_valid_from' : None})
        LuciHelper.queuePumpWait(self, couponSeriesId)
        couponCode, couponDetails = LuciHelper.issueCouponAndAssertions(self, couponSeriesId)
        changeDate = Utils.getTime(days=-1, minutes=5,milliSeconds=True)
        self.connObj.changeCouponIssuedDate(couponDetails['id'], changeDate)
        #redeem Coupon and Assertion.constructAssertion(on)
        LuciHelper.redeemCouponAndAssertions(self, couponSeriesId, couponCode)
        LuciHelper.redemptionDBAssertion(self, couponSeriesId)

    @pytest.mark.parametrize('description, couponConfig, expectedError', [
        ('Redeem same coupon by different users Config Multiple use: False, any user: True', {'multiple_use': False, 'any_user': True}, [constant.MULTIPLE_REDEMPTION_FOR_COUPON_NOT_ALLOWED, 'multiple coupon redemptions not allowed'])
    ])
    def test_LUCI_RC_DC_021(self,description, couponConfig, expectedError):
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self, couponConfigReq=couponConfig)
        LuciHelper.queuePumpWait(self, couponSeriesId)
        LuciHelper.couponPumpAssertion(self, couponSeriesId)
        couponCode = LuciHelper.issueCouponAndAssertions(self, couponSeriesId)[0]
        #Coupon Redemption
        LuciHelper.redeemCouponAndAssertions(self, couponSeriesId, couponCode)
        self.userId = constant.config['usersInfo'][1]['userId']
        LuciHelper.redeemCouponAndAssertions(self, couponSeriesId, couponCode, error=expectedError)
        self.userId = constant.config['usersInfo'][0]['userId']
        LuciHelper.redemptionDBAssertion(self, couponSeriesId)
