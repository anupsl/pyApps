import time, random,pytest
from src.Constant.constant import constant
from src.utilities.logger import Logger
from src.utilities.assertion import Assertion
from src.utilities.utils import Utils
from src.modules.luci.luciHelper import LuciHelper
from src.modules.luci.luciObject import LuciObject
from src.modules.luci.luciDBHelper import LuciDBHelper
from src.modules.luci.dracarysHelper import DracarysHelper
from src.modules.luci.dracarysObject import DracarysObject

class Test_ExternalIssual():

    def setup_class(self):
        Logger.logSuiteName(str(self).split('.')[-1])
        self.constructObj = LuciObject()
        self.DracarysObj = DracarysObject()
        self.userId = constant.config['usersInfo'][0]['userId']
        self.tillId = constant.config['tillIds'][0]
        self.userIds = []
        for i in range(len(constant.config['usersInfo'])):
            self.userIds.append(constant.config['usersInfo'][i]['userId'])
        self.billId = Utils.getTime(milliSeconds=True)

    def setup_method(self, method):
        self.connObj = LuciHelper.getConnObj(newConnection=True)
        Logger.logMethodName(method.__name__)
        constant.config['uploadedFileName'] = method.__name__
        self.DracraysConnObj = DracarysHelper.getConnObj(newConnection=True)
        constant.config['requestId'] = 'luci_auto_'+str(random.randint(11111, 99999))

    @pytest.mark.parametrize('description', [('Upload and Redeem External coupon code')])
    def test_LUCI_EI_011_sanity_smoke(self, description):
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self,couponConfigReq={'client_handling_type' : 'DISC_CODE_PIN' , 'any_user' : True, 'isExternalIssual' : True})
        Assertion.constructAssertion(LuciDBHelper.isExternalCouponSeries(couponSeriesId), 'Client handling type isExternal Enabled for coupon series id: {}'.format(couponSeriesId))
        #Checking Queue Count
        Assertion.constructAssertion(self.connObj.getQueueSize(constant.config['orgId'], couponSeriesId, constant.config['requestId']) == 0, 'Coupon codes are cleared from queue')

        couponCode = LuciHelper.uploadCouponAndAssertions(self, couponSeriesId, self.constructObj.importType['NONE'])['coupons'][0]

        #CouponDetails Request
        couponDetailsRequest = {'onlyActive': True, 'couponCodeFilter': [couponCode]}
        self.userId = -1
        LuciHelper.getCouponDetailsAndAssertion(self,couponSeriesId,couponCode,couponDetailsRequest)
        LuciHelper.issuedCouponsDBAssertion(self,couponSeriesId,couponCode)

        self.userId = constant.config['usersInfo'][0]['userId']

        LuciHelper.redeemCouponAndAssertions(self, couponSeriesId, couponCode, couponIssuedTo = [-1])
        LuciHelper.redemptionDBAssertion(self,couponSeriesId)
        #Get Coupon Configuration
        LuciHelper.getCouponConfigAndAssertion(self,couponSeriesId, 1 , 1)

    @pytest.mark.parametrize('description', [('Upload and Redeem External coupon code in lower case')])
    def test_LUCI_EI_012(self,description):
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self,couponConfigReq={'client_handling_type' : 'DISC_CODE_PIN' , 'any_user' : True, 'isExternalIssual' : True, 'min_bill_amount' : 1500 , 'max_bill_amount' : 999999999, 'redemption_valid_after_days' : -1})
        Assertion.constructAssertion(LuciDBHelper.isExternalCouponSeries(couponSeriesId), 'Client handling type isExternal Enabled for coupon series id: {}'.format(couponSeriesId))

        couponCode = LuciHelper.generateCouponCode().lower()
        couponCode =LuciHelper.uploadCouponAndAssertions(self, couponSeriesId, self.constructObj.importType['NONE'], couponCode=couponCode, dracraysUpload={'couponCodeCAPS' : False})['coupons'][0]

        LuciHelper.redeemCouponAndAssertions(self, couponSeriesId, couponCode, couponIssuedTo = [-1], error=[900, 'bill amount less than the minimum limit set'])
        couponConfigObj.update({'min_bill_amount' : 900})
        LuciHelper.saveCouponConfigAndAssertions(self,couponConfigReq=couponConfigObj)
        LuciHelper.redeemCouponAndAssertions(self, couponSeriesId, couponCode, couponIssuedTo=[-1])


    @pytest.mark.parametrize('description, config', [
        ('Create External with type DISC_CODE_PIN', {'client_handling_type' : 'DISC_CODE_PIN' , 'any_user' : True, 'isExternalIssual' : True})
    ])
    def test_LUCI_EI_013(self, description, config):
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self,couponConfigReq=config)
        Assertion.constructAssertion(LuciDBHelper.isExternalCouponSeries(couponSeriesId), 'Client handling type isExternal Enabled for coupon series id: {}'.format(couponSeriesId))
        Assertion.constructAssertion(couponConfigObj['client_handling_type'] == 'DISC_CODE_PIN', 'External coupon series Client handling type Matched Actual: {} and Expected: {}'.format(couponConfigObj['client_handling_type'] ,'DISC_CODE_PIN'))

        couponCodeList =LuciHelper.uploadCouponAndAssertions(self, couponSeriesId, self.constructObj.importType['NONE'], noOfCouponsToBeUpload=10, dracraysUpload={'couponCodeCAPS' : False})['coupons']
        queueSize = LuciHelper.getQueueSize(self, couponSeriesId)
        Assertion.constructAssertion(queueSize == 0, 'External Coupons not pumped to Queue Actual: {}'.format(queueSize))
        issuedCount = LuciDBHelper.getCouponsIssued_Count(couponSeriesId)
        Assertion.constructAssertion(issuedCount == 10, 'Uploaded External Coupons & Issued DB count Matched Actual: {} and Expected: {}'.format(issuedCount, 10))
        LuciHelper.redeemCouponAndAssertions(self, couponSeriesId, couponCodeList[0], couponIssuedTo = [-1])
        couponConfigObj.update({'any_user' : False, 'isExternalIssual' : False})
        LuciHelper.saveCouponConfigAndAssertions(self,couponConfigReq=couponConfigObj)

        LuciHelper.uploadCouponAndAssertions(self, couponSeriesId, self.constructObj.importType['NONE'], noOfCouponsToBeUpload=10, dracraysUpload={'couponCodeCAPS': False})

        queueSize = LuciHelper.getQueueSize(self, couponSeriesId)
        Assertion.constructAssertion(queueSize == 10, 'External Coupons not pumped to Queue Actual: {}'.format(queueSize))

        couponCode, _ = LuciHelper.issueCouponAndAssertions(self, couponSeriesId)
        LuciHelper.redeemCouponAndAssertions(self, couponSeriesId, couponCode)
        queueSize = LuciHelper.getQueueSize(self, couponSeriesId)
        Assertion.constructAssertion(queueSize == 9, 'External Coupons not pumped to Queue Actual: {}'.format(queueSize))

    @pytest.mark.parametrize('description', [('Create External with type DISC_CODE_PIN Part 01', )])
    def test_LUCI_EI_013_01(self, description):
        config = {'client_handling_type' : 'DISC_CODE_PIN' , 'any_user' : True, 'isExternalIssual' : True}
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self,couponConfigReq=config)
        Assertion.constructAssertion(LuciDBHelper.isExternalCouponSeries(couponSeriesId), 'Client handling type isExternal Enabled for coupon series id: {}'.format(couponSeriesId))
        Assertion.constructAssertion(couponConfigObj['client_handling_type'] == 'DISC_CODE_PIN', 'External coupon series Client handling type Matched Actual: {} and Expected: {}'.format(couponConfigObj['client_handling_type'] ,'DISC_CODE_PIN'))

        couponCodeList =LuciHelper.uploadCouponAndAssertions(self, couponSeriesId, self.constructObj.importType['NONE'], noOfCouponsToBeUpload=10, dracraysUpload={'couponCodeCAPS' : False})['coupons']

        time.sleep(2)

        queueSize = LuciHelper.getQueueSize(self, couponSeriesId)
        Assertion.constructAssertion(queueSize == 0, 'External Coupons not pumped to Queue Actual: {}'.format(queueSize))
        issuedCount = LuciDBHelper.getCouponsIssued_Count(couponSeriesId)
        Assertion.constructAssertion(issuedCount == 10, 'Uploaded External Coupons & Issued DB count Matched Actual: {} and Expected: {}'.format(issuedCount, 10))
        LuciHelper.redeemCouponAndAssertions(self, couponSeriesId, couponCodeList[0], couponIssuedTo = [-1])


    @pytest.mark.parametrize('description', [('Create External with type DISC_CODE_PIN Part 02', )])
    def test_LUCI_EI_013_02(self, description):
        config = {'client_handling_type' : 'DISC_CODE_PIN' , 'any_user' : False, 'isExternalIssual' : False}
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self,couponConfigReq=config)
        LuciHelper.uploadCouponAndAssertions(self, couponSeriesId, self.constructObj.importType['NONE'], noOfCouponsToBeUpload=10, dracraysUpload={'couponCodeCAPS': False})

        time.sleep(10)

        queueSize = LuciHelper.getQueueSize(self, couponSeriesId)
        Assertion.constructAssertion(queueSize == 10, 'External Coupons not pumped to Queue Actual: {}'.format(queueSize))

        couponCode, _ = LuciHelper.issueCouponAndAssertions(self, couponSeriesId)
        LuciHelper.redeemCouponAndAssertions(self, couponSeriesId, couponCode)

    @pytest.mark.parametrize('description, config, expectedErrors', [
        ('Create External with type EXTERNAL_ISSUAL', {'client_handling_type' : 'EXTERNAL_ISSUAL' , 'any_user' : False, 'isExternalIssual' : True}, [629, "invalid client handling type"]),
        ('Create External with type DISC_CODE_PIN', {'client_handling_type' : 'DISC_CODE_PIN' , 'any_user' : False, 'isExternalIssual' : True}, [109, "Can anybody use the coupon' must be enabled for client handling type : DISC_CODE_PIN"]),
        ('Create External with type DISC_CODE_PIN', {'client_handling_type' : 'DISC_CODE' , 'any_user' : False, 'isExternalIssual' : True}, [629, "invalid client handling type with isExternalIssual field set to true"]),
        ('Create External with type DISC_CODE_PIN', {'client_handling_type' : 'GENERIC' , 'any_user' : False, 'isExternalIssual' : True}, [629, "invalid client handling type with isExternalIssual field set to true"]),

    ])
    def test_LUCI_EI_014(self, description, config, expectedErrors):
        try:
            if config['client_handling_type'] == 'GENERIC':
                couponCode = LuciHelper.generateCouponCode()
                config.update({'genericCode': couponCode})
            LuciHelper.saveCouponConfigAndAssertions(self, couponConfigReq=config)
            Assertion.constructAssertion(False,'Actual: Coupon series Created Expected: Exceptions', verify=True)
        except Exception, luciExp:
            luciExp = luciExp.__dict__
            Assertion.constructAssertion(luciExp['errorCode'] == expectedErrors[0], 'Luci Exception error code Actual: {} and Expected: {}'.format(luciExp['errorCode'], expectedErrors[0]))
            Assertion.constructAssertion(luciExp['errorMsg'] == expectedErrors[1], 'Luci Exception Error Msg Actual : {}'.format(luciExp['errorMsg']))
