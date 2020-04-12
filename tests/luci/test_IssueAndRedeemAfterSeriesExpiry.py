import random,pytest
from src.Constant.constant import constant
from src.utilities.logger import Logger
from src.utilities.assertion import Assertion
from src.utilities.utils import Utils
from src.modules.luci.luciHelper import LuciHelper
from src.modules.luci.luciObject import LuciObject

class Test_IssueAndRedeemAfterSeriesExpiry():

    def setup_class(self):
        Logger.logSuiteName(str(self).split('.')[-1])
        self.constructObj = LuciObject()
        self.userId = constant.config['usersInfo'][0]['userId']
        self.tillId = constant.config['tillIds'][0]
        self.billId = Utils.getTime(milliSeconds=True)

    def setup_method(self, method):
        self.connObj = LuciHelper.getConnObj(newConnection=True)
        Logger.logMethodName(method.__name__)
        constant.config['requestId'] = 'luci_auto_ase_'+str(random.randint(11111, 99999))
        self.userId = constant.config['usersInfo'][0]['userId']

    @pytest.mark.parametrize('description, couponConfig',[
        (['Redeem valid from is Present date & Redeem after days 0', {'redemption_valid_from' : Utils.getTime(milliSeconds=True) ,'redemption_valid_after_days' : 0}]),
        (['Redeem valid from is Past date & Redeem after days 0', {'redemption_valid_from' : Utils.getTime(days=-1, milliSeconds=True) ,'redemption_valid_after_days' : 0}]),
        (['Redeem valid from is None & Redeem after days -1', {'redemption_valid_from' : None ,'redemption_valid_after_days' : -1}])
    ])
    def test_LUCI_RSD_001(self, description, couponConfig):
        couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self,couponConfig)[1]
        couponCode = LuciHelper.issueCouponAndAssertions(self,couponSeriesId)[0]
        LuciHelper.getCouponConfigAndAssertion(self,couponSeriesId,no_issued=1)
        LuciHelper.redeemCouponAndAssertions(self,couponSeriesId,couponCode)
        LuciHelper.redemptionDBAssertion(self,couponSeriesId,numRedeemed=1)

    @pytest.mark.parametrize('description, couponConfig',[
        (['Redeem valid from as None & Redeem after days 1', {'redemption_valid_from' : None ,'redemption_valid_after_days' : 1}])
    ])
    def test_LUCI_RSD_002(self, description, couponConfig):
        couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self, couponConfig)[1]
        couponCode = LuciHelper.issueCouponAndAssertions(self, couponSeriesId)[0]
        LuciHelper.getCouponConfigAndAssertion(self, couponSeriesId, no_issued=1)
        LuciHelper.redeemCouponAndAssertions(self, couponSeriesId, couponCode, error=[constant.REDEMPTION_VALIDITY_DATE_NOT_REACHED, 'event date is lesser than redemption validity date'])

    @pytest.mark.parametrize('description, createCouponConfig, changeCouponConfig',[
        (['Redeem after days 1 and change config value to 0 & redeem coupon', {'redemption_valid_from' : None ,'redemption_valid_after_days' : 1}, {'redemption_valid_after_days' : 0}])
    ])
    def test_LUCI_RSD_003(self, description, createCouponConfig, changeCouponConfig):
        couponConfig, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self, createCouponConfig)
        couponCode = LuciHelper.issueCouponAndAssertions(self, couponSeriesId)[0]
        LuciHelper.getCouponConfigAndAssertion(self, couponSeriesId, no_issued=1)
        LuciHelper.redeemCouponAndAssertions(self, couponSeriesId, couponCode, error=[constant.REDEMPTION_VALIDITY_DATE_NOT_REACHED, 'event date is lesser than redemption validity date'])
        couponConfig.update(changeCouponConfig)
        LuciHelper.saveCouponConfigAndAssertions(self,couponConfigReq=couponConfig)
        LuciHelper.redeemCouponAndAssertions(self, couponSeriesId, couponCode)
        LuciHelper.redemptionDBAssertion(self,couponSeriesId,numRedeemed=1)

    @pytest.mark.parametrize('description, createCouponConfig, changeCouponConfig',[
        (['Redeem coupon & change redeem valid 1 day ahead & redeem same coupon', {'redemption_valid_from' : None ,'redemption_valid_after_days' : 0, 'multiple_use' : True, 'same_user_multiple_redeem' : True}, {'redemption_valid_from' : Utils.getTime(days=1,milliSeconds=True) ,'redemption_valid_after_days' : 0}])
    ])
    def test_LUCI_RSD_004(self, description, createCouponConfig, changeCouponConfig):
        couponConfig, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self, createCouponConfig)
        couponCode = LuciHelper.issueCouponAndAssertions(self, couponSeriesId)[0]
        LuciHelper.getCouponConfigAndAssertion(self, couponSeriesId, no_issued=1)
        LuciHelper.redeemCouponAndAssertions(self, couponSeriesId, couponCode)
        LuciHelper.redemptionDBAssertion(self,couponSeriesId,numRedeemed=1)
        couponConfig.update(changeCouponConfig)
        LuciHelper.saveCouponConfigAndAssertions(self,couponConfigReq=couponConfig)
        LuciHelper.redeemCouponAndAssertions(self, couponSeriesId, couponCode, error=[constant.REDEMPTION_VALIDITY_DATE_NOT_REACHED, 'event date is lesser than redemption validity date'])

    @pytest.mark.parametrize('description, couponConfig, expectedError',[
        (['Redemption valid date greater than expiry date', {'redemption_valid_from' : None ,'redemption_valid_after_days' : 3}, [constant.REDEMPTION_DATE_AFTER_SERIES_EXPIRY_DATE,'coupon redemption valid start date is after series expiry date']]),
        (['Redemption valid from greater than expiry date', {'redemption_valid_from' : Utils.getTime(days=3, milliSeconds=True) ,'redemption_valid_after_days' : 0}, [constant.REDEMPTION_DATE_AFTER_SERIES_EXPIRY_DATE,'coupon redemption valid start date is after series expiry date']])
    ])
    def test_LUCI_RSD_005(self, description, couponConfig, expectedError):
        couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self, couponConfig)[1]
        luciExp = LuciHelper.issueCouponAndAssertions(self, couponSeriesId, expectException=True)
        Assertion.constructAssertion(luciExp['errorCode'] == expectedError[0], 'Luci Exception error code Actual: {} and Expected: {}'.format(luciExp['errorCode'], expectedError[0]))
        Assertion.constructAssertion(luciExp['errorMsg'] == expectedError[1], 'Luci Exception Error Msg Actual : {}'.format(luciExp['errorMsg']))

    @pytest.mark.parametrize('description, createCouponConfig, changeCouponConfig, expectedError',[
        (['Issue & redeem one coupon and change Redemption valid date greater than expiry date', {'redemption_valid_from' : None ,'redemption_valid_after_days' : 0}, {'redemption_valid_from' : None ,'redemption_valid_after_days' : 3}, [constant.REDEMPTION_DATE_AFTER_SERIES_EXPIRY_DATE,'coupon redemption valid start date is after series expiry date']]),
        (['Issue & redeem one coupon and change Redemption valid from greater than expiry date', {'redemption_valid_from' : Utils.getTime(milliSeconds=True) ,'redemption_valid_after_days' : 0}, {'redemption_valid_from' : Utils.getTime(days=3, milliSeconds=True) ,'redemption_valid_after_days' : 0} , [constant.REDEMPTION_DATE_AFTER_SERIES_EXPIRY_DATE,'coupon redemption valid start date is after series expiry date']])
    ])
    def test_LUCI_RSD_006(self, description, createCouponConfig, changeCouponConfig, expectedError):
        couponConfig, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self, createCouponConfig)
        couponCode = LuciHelper.issueCouponAndAssertions(self, couponSeriesId)[0]
        LuciHelper.redeemCouponAndAssertions(self, couponSeriesId, couponCode)
        couponConfig.update(changeCouponConfig)
        LuciHelper.saveCouponConfigAndAssertions(self,couponConfigReq=couponConfig)
        self.userId = constant.config['usersInfo'][1]['userId']
        luciExp = LuciHelper.issueCouponAndAssertions(self, couponSeriesId, expectException=True)
        Assertion.constructAssertion(luciExp['errorCode'] == expectedError[0], 'Luci Exception error code Actual: {} and Expected: {}'.format(luciExp['errorCode'], expectedError[0]))
        Assertion.constructAssertion(luciExp['errorMsg'] == expectedError[1], 'Luci Exception Error Msg Actual : {}'.format(luciExp['errorMsg']))

    @pytest.mark.parametrize('description, couponConfig',[
        (['Redeem after days 1 and redeem coupon', {'redemption_valid_from' : None ,'redemption_valid_after_days' : 1}])
    ])
    def test_LUCI_RSD_007(self, description, couponConfig):
        couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self,couponConfig)[1]
        couponCode, couponDetails = LuciHelper.issueCouponAndAssertions(self, couponSeriesId)
        changeDate = Utils.getTime(days=-1, hours=-2, milliSeconds=True)
        self.connObj.changeCouponIssuedDate(couponDetails['id'], changeDate)
        LuciHelper.getCouponConfigAndAssertion(self,couponSeriesId,no_issued=1)
        LuciHelper.redeemCouponAndAssertions(self,couponSeriesId,couponCode)
        LuciHelper.redemptionDBAssertion(self,couponSeriesId,numRedeemed=1)