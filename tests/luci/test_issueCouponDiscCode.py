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

class Test_IssueCouponDiscCode():

    def setup_class(self):
        Logger.logSuiteName(str(self).split('.')[-1])
        self.constructObj = LuciObject()
        self.DracarysObj = DracarysObject()
        self.userId = constant.config['usersInfo'][0]['userId']
        self.tillId = constant.config['tillIds'][0]
        self.orgDefaultValue = LuciDBHelper.orgDefaultValues()

    def setup_method(self, method):
        self.connObj = LuciHelper.getConnObj(newConnection=True)
        Logger.logMethodName(method.__name__)
        constant.config['uploadedFileName'] = method.__name__
        self.DracraysConnObj = DracarysHelper.getConnObj(newConnection=True)
        constant.config['requestId'] = 'luci_auto_'+str(random.randint(11111, 99999))

    @pytest.mark.parametrize('description', [('Issue DC with valid params')])
    def test_LUCI_IC_DC_011(self, description):
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self)
        LuciHelper.queuePumpWait(self,couponSeriesId)
        LuciHelper.issueCouponAndAssertions(self,couponSeriesId)

    @pytest.mark.parametrize('description', [('Validate Coupon Org Config isNumeric-AlphaNumeric-&-CodeLength')])
    def test_LUCI_IC_DC_012(self, description):
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self)
        LuciHelper.queuePumpWait(self, couponSeriesId)
        createdCouponCount = LuciDBHelper.getCouponsCreated_Count(couponSeriesId, 1)
        Assertion.constructAssertion(createdCouponCount != 0, 'Coupon codes are created for DC')
        Assertion.constructAssertion(self.connObj.getQueueSize(constant.config['orgId'], couponSeriesId, constant.config['requestId']) != 0, 'Coupon codes pumped to queue')

        # upload the coupon code
        LuciHelper.uploadCouponAndAssertions(self, couponSeriesId, self.constructObj.importType['USER_ID'], issuedTo=self.userId, dracraysUpload={'userOnly' : True})

        couponCode = LuciHelper.issueCouponAndAssertions(self, couponSeriesId, issueCouponParamObj={'storeUnitId' : constant.config['adminId']})[0]
        Assertion.constructAssertion(not LuciHelper.isNumeric(couponCode), 'Upload & issued Alpha-Numeric coupon')


        self.userId = constant.config['usersInfo'][1]['userId']
        couponCode2 = LuciHelper.issueCouponAndAssertions(self, couponSeriesId, issueCouponParamObj={'storeUnitId' : constant.config['adminId']})[0]
        Assertion.constructAssertion(len(str(couponCode2)) == int(self.orgDefaultValue['random_code_length']), 'Coupon Org Config Length is: {} Actual Coupon Lenght : {}'.format(len(str(couponCode2)), self.orgDefaultValue['random_code_length']))
        if not self.orgDefaultValue['is_alpha_numeric']:
            Assertion.constructAssertion(LuciHelper.isNumeric(couponCode2), 'Org Config is Numeric Generated Coupon: {}'.format(couponCode2))
        elif self.orgDefaultValue['is_alpha_numeric']:
            Assertion.constructAssertion(not LuciHelper.isNumeric(couponCode2), 'Org Config is AlphaNumeric Generated Coupon: {}'.format(couponCode2))
        self.userId = constant.config['usersInfo'][0]['userId']


    @pytest.mark.parametrize('description', [('Issue same coupon code with config Do not resend existing voucher false & allow multiple voucher false')])
    def test_LUCI_IC_DC_013(self, description):
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self)
        LuciHelper.queuePumpWait(self, couponSeriesId)
        createdCouponCount = LuciDBHelper.getCouponsCreated_Count(couponSeriesId, 1)
        Assertion.constructAssertion(createdCouponCount != 0, 'Coupon codes are created for DC')
        Assertion.constructAssertion(self.connObj.getQueueSize(constant.config['orgId'], couponSeriesId, constant.config['requestId']) != 0, 'Coupon codes pumped to queue')

        # upload the coupon code
        LuciHelper.uploadCouponAndAssertions(self, couponSeriesId, self.constructObj.importType['USER_ID'], issuedTo=self.userId,dracraysUpload={'userOnly' : True})

        LuciHelper.issueCouponAndAssertions(self, couponSeriesId, issueCouponParamObj={'storeUnitId' : constant.config['adminId']})
        LuciHelper.issueCouponAndAssertions(self, couponSeriesId, issueCouponParamObj={'storeUnitId' : constant.config['adminId']}, couponIssuedCount=2)

    @pytest.mark.parametrize('description', [
        ('Issue same coupon code with config Do not resend existing voucher True & allow multiple voucher True')])
    def test_LUCI_IC_DC_014(self, description):
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self, {'do_not_resend_existing_voucher' : True, 'allow_multiple_vouchers_per_user' : True, 'max_vouchers_per_user' : 3})
        LuciHelper.queuePumpWait(self, couponSeriesId)
        createdCouponCount = LuciDBHelper.getCouponsCreated_Count(couponSeriesId, 1)
        Assertion.constructAssertion(createdCouponCount != 0, 'Coupon codes are created for DC')
        Assertion.constructAssertion(self.connObj.getQueueSize(constant.config['orgId'], couponSeriesId, constant.config['requestId']) != 0, 'Coupon codes pumped to queue')

        # upload the coupon code
        LuciHelper.uploadCouponAndAssertions(self, couponSeriesId, self.constructObj.importType['USER_ID'], issuedTo=self.userId, dracraysUpload={'userOnly' : True})

        couponCode1 = LuciHelper.issueCouponAndAssertions(self, couponSeriesId, issueCouponParamObj={'storeUnitId': constant.config['adminId']})[0]
        couponCode2 = LuciHelper.issueCouponAndAssertions(self, couponSeriesId, issueCouponParamObj={'storeUnitId': constant.config['adminId']})[0]

        Assertion.constructAssertion(len(str(couponCode2)) == int(self.orgDefaultValue['random_code_length']), 'Coupon Org Config Length is: {} Actual Coupon Lenght : {}'.format(len(str(couponCode2)), int(self.orgDefaultValue['random_code_length'])))
        if not self.orgDefaultValue['is_alpha_numeric']:
            Assertion.constructAssertion(LuciHelper.isNumeric(couponCode2), 'Org Config is Numeric Generated Coupon: {}'.format(couponCode2))
        elif self.orgDefaultValue['is_alpha_numeric']:
            Assertion.constructAssertion(not LuciHelper.isNumeric(couponCode2), 'Org Config is AlphaNumeric Generated Coupon: {}'.format(couponCode2))
        luciExp = LuciHelper.issueCouponAndAssertions(self, couponSeriesId, expectException=True)
        Assertion.constructAssertion(luciExp['errorCode'] == constant.MAX_COUPON_ISSUAL_PER_USER_EXCEEDED, 'Luci Exception error code Actual: {} and Expected: {}'.format(luciExp['errorCode'], constant.MAX_COUPON_ISSUAL_PER_USER_EXCEEDED))
        Assertion.constructAssertion(luciExp['errorMsg'] == 'max coupon per user exceeded', 'Luci Exception Error Msg Actual : {}'.format(luciExp['errorMsg']))

    @pytest.mark.parametrize('description', [
        ('Issue same coupon code with config Do not resend existing voucher True & allow multiple voucher False')])
    def test_LUCI_IC_DC_015(self, description):
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self, {'do_not_resend_existing_voucher': True, 'allow_multiple_vouchers_per_user': False})
        LuciHelper.queuePumpWait(self, couponSeriesId)
        createdCouponCount = LuciDBHelper.getCouponsCreated_Count(couponSeriesId, 1)
        Assertion.constructAssertion(createdCouponCount != 0, 'Coupon codes are created for DC')
        Assertion.constructAssertion(self.connObj.getQueueSize(constant.config['orgId'], couponSeriesId, constant.config['requestId']) != 0, 'Coupon codes pumped to queue')

        # upload the coupon code
        LuciHelper.uploadCouponAndAssertions(self, couponSeriesId, self.constructObj.importType['USER_ID'], issuedTo=self.userId, dracraysUpload={'userOnly' : True})

        luciExp = LuciHelper.issueCouponAndAssertions(self, couponSeriesId, expectException=True)
        Assertion.constructAssertion(luciExp['errorCode'] == constant.COUPON_ALREADY_ISSUED, 'Luci Exception error code Actual: {} and Expected: {}'.format(luciExp['errorCode'], constant.COUPON_ALREADY_ISSUED))
        Assertion.constructAssertion(luciExp['errorMsg'] == 'user already has a coupon', 'Luci Exception Error Msg Actual : {}'.format(luciExp['errorMsg']))

    @pytest.mark.parametrize('description', [
        ('Issue same coupon code with config Do not resend existing voucher False & allow multiple voucher True')])
    def test_LUCI_IC_DC_016(self, description):
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self, {'do_not_resend_existing_voucher': False, 'allow_multiple_vouchers_per_user': True})
        LuciHelper.queuePumpWait(self, couponSeriesId)
        createdCouponCount = LuciDBHelper.getCouponsCreated_Count(couponSeriesId, 1)
        Assertion.constructAssertion(createdCouponCount != 0, 'Coupon codes are created for DC')
        Assertion.constructAssertion(self.connObj.getQueueSize(constant.config['orgId'], couponSeriesId, constant.config['requestId']) != 0, 'Coupon codes pumped to queue')

        # upload the coupon code
        couponCode =  LuciHelper.uploadCouponAndAssertions(self, couponSeriesId, self.constructObj.importType['USER_ID'], issuedTo=self.userId, dracraysUpload={'userOnly' : True})['coupons'][0]
        couponCode1 = LuciHelper.issueCouponAndAssertions(self, couponSeriesId, issueCouponParamObj={'storeUnitId': constant.config['adminId']})[0]
        Assertion.constructAssertion(couponCode.upper() == couponCode1, 'Resend coupon  code resend Actual : {} & Expected : {}'.format(couponCode,couponCode1))
        couponCode2 = LuciHelper.issueCouponAndAssertions(self, couponSeriesId,couponIssuedCount = 2 , issueCouponParamObj={'storeUnitId': constant.config['adminId']})[0]
        Assertion.constructAssertion(couponCode1 == couponCode2, 'Resend coupon  code resend Actual : {} & Expected : {}'.format(couponCode1,couponCode2))

    @pytest.mark.parametrize('description', [
        ('Issue coupon codes to Multiple users')])
    def test_LUCI_IC_DC_017(self, description):
        actualUserId = self.userId
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self)
        LuciHelper.queuePumpWait(self, couponSeriesId)
        createdCouponCount = LuciDBHelper.getCouponsCreated_Count(couponSeriesId, 1)
        Assertion.constructAssertion(createdCouponCount != 0, 'Coupon codes are created for DC')
        Assertion.constructAssertion(self.connObj.getQueueSize(constant.config['orgId'], couponSeriesId, constant.config['requestId']) != 0, 'Coupon codes pumped to queue')

        LuciHelper.issueCouponAndAssertions(self, couponSeriesId)
        self.userId = constant.config['usersInfo'][1]['userId']
        LuciHelper.issueCouponAndAssertions(self, couponSeriesId)
        self.userId = actualUserId

    @pytest.mark.parametrize('description', [('set max create 1 and issue 2 coupons')])
    def test_LUCI_IC_DC_018(self, description):
        actualUserId = self.userId
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self, {'max_create': 1})
        time.sleep(2)
        createdCouponCount = LuciDBHelper.getCouponsCreated_Count(couponSeriesId, 1)
        Assertion.constructAssertion(createdCouponCount != 0, 'Coupons are created for DC')
        Assertion.constructAssertion(self.connObj.getQueueSize(constant.config['orgId'], couponSeriesId, constant.config['requestId']) != 0, 'Coupon codes pumped to queue')

        LuciHelper.issueCouponAndAssertions(self, couponSeriesId)
        self.userId = constant.config['usersInfo'][1]['userId']
        luciExp = LuciHelper.issueCouponAndAssertions(self, couponSeriesId, expectException=True)
        Assertion.constructAssertion(luciExp['errorCode'] == constant.MAX_COUPON_ISSUAL_PER_SERIES_EXCEEDED, 'Luci Exception error code Actual: {} and Expected: {}'.format(luciExp['errorCode'], constant.MAX_COUPON_ISSUAL_PER_SERIES_EXCEEDED))
        Assertion.constructAssertion(luciExp['errorMsg'] == 'max create for series exceeded', 'Luci Exception Error Msg Actual : {}'.format(luciExp['errorMsg']))
        self.userId = actualUserId

    @pytest.mark.parametrize('description, invalidInput, expected', [
        ('Issue coupon with Invalid orgId', {'orgId': 9999}, [constant.INVALID_ORG_ID, 'invalid org id']),
        ('Issue coupon with Negative orgId', {'orgId': -1}, [constant.INVALID_ORG_ID, 'invalid org id -1']),
        ('Issue coupon with Invalid CouponSeries Id', {'couponSeriesId': -1}, [constant.INVALID_COUPON_SERIES_ID, 'invalid series id -1']),
        ('Issue coupon with Invalid storeUnit Id', {'storeUnitId': -1}, [constant.INVALID_ISSUAL_STORE_ID, 'invalid store id -1']),
        ('Issue coupon with Invalid userId', {'userId': -1}, [constant.INVALID_USER_ID, 'invalid user id -1'])])
    def test_LUCI_IC_DC_019(self, description, invalidInput, expected):
        try:
            couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self)
            LuciHelper.issueCouponAndAssertions(self, couponSeriesId, issueCouponParamObj=invalidInput)
        except Exception, luciExp:
            luciExp = luciExp.__dict__;
            Assertion.constructAssertion(luciExp['errorCode'] == expected[0], 'Luci Exception error code Actual: {} and Expected: {}'.format(luciExp['errorCode'], expected[0]))
            Assertion.constructAssertion(luciExp['errorMsg'] == expected[1], 'Luci Exception Error Msg Actual : {}'.format(luciExp['errorMsg']))

    @pytest.mark.parametrize('description', [('mutually exclusive coupon series and customer lock verifications')])
    def test_LUCI_IC_DC_020_sanity(self, description):
        couponSeriesList = []
        couponConfigObjList = []
        for i in range(4):
            if i % 2:
                mutualCouponSeriesId = '[{}]'.format(couponSeriesList[i-1])
                couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self,couponConfigReq={'mutual_exclusive_series_ids': mutualCouponSeriesId})
                couponConfigObjList.append(couponConfigObj)
                couponSeriesList.append(couponSeriesId)
            else:
                couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self)
                couponConfigObjList.append(couponConfigObj)
                couponSeriesList.append(couponSeriesId)

            LuciHelper.queuePumpWait(self, couponSeriesId)
            createdCouponCount = LuciDBHelper.getCouponsCreated_Count(couponSeriesId)
            Assertion.constructAssertion(createdCouponCount != 0, 'Coupon Code Pumped to Queue')
            Assertion.constructAssertion(self.connObj.getQueueSize(constant.config['orgId'], couponSeriesId,constant.config['requestId']) != 0, 'Coupon Code Pumped to Queue')
            if not i % 2:
                LuciHelper.issueCouponAndAssertions(self,couponSeriesList[i])
            else:
                mutualExclusiveExp = LuciHelper.issueCouponAndAssertions(self, couponSeriesList[i], expectException=True)
                Assertion.constructAssertion(mutualExclusiveExp['errorCode'] == constant.COUPON_PRESENT_MUTUAL_EXCLUSIVE_SERIES, 'Luci Exception error code Actual: {} and Expected: {}'.format(mutualExclusiveExp['errorCode'], constant.COUPON_PRESENT_MUTUAL_EXCLUSIVE_SERIES))
                Assertion.constructAssertion(mutualExclusiveExp['errorMsg'] == 'coupon present in mutually exclusive series id ', 'Luci Exception Error Msg Actual : {}'.format(mutualExclusiveExp['errorMsg']))

    @pytest.mark.parametrize('description', [('Min Days Between issual with Diff TimeZone')])
    def test_LUCI_DCP_DTZ(self, description):
        try:
            self.tillId = LuciDBHelper.getTillDiffTimeZone()
            couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self, couponConfigReq={'client_handling_type' : 'DISC_CODE_PIN' , 'min_days_between_vouchers' : 1, 'do_not_resend_existing_voucher' : True, 'allow_multiple_vouchers_per_user' : True})
            LuciHelper.uploadCouponAndAssertions(self, couponSeriesId, self.constructObj.importType['NONE'], noOfCouponsToBeUpload=10)
            LuciHelper.issueCouponAndAssertions(self,couponSeriesId)
            luciExp = LuciHelper.issueCouponAndAssertions(self, couponSeriesId, issueCouponParamObj={'eventTimeInMillis' : Utils.getTime(days= -1, milliSeconds=True)}, expectException=True)
            Assertion.constructAssertion(luciExp['errorCode'] == constant.DAYS_BETWEEN_ISSUAL_FOR_USER_LOWER_MIN_DAYS, 'Luci Exception error code Actual: {} and Expected: {}'.format(luciExp['errorCode'], constant.DAYS_BETWEEN_ISSUAL_FOR_USER_LOWER_MIN_DAYS))
            Assertion.constructAssertion(luciExp['errorMsg'] == 'days between consecutive issuals for a user less than min days between issuals', 'Luci Exception Error Msg Actual : {}'.format(luciExp['errorMsg']))
        finally:
            self.tillId = constant.config['tillIds'][0]