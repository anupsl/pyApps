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

class Test_UploadCouponsDiscCodeMobile():

    def setup_class(self):
        Logger.logSuiteName(str(self).split('.')[-1])
        self.constructObj = LuciObject()
        self.DracarysObj = DracarysObject()
        self.uploadTypeList = ['USER_ID', 'MOBILE', 'EMAIL', 'EXTERNAL_ID']
        self.userId = constant.config['usersInfo'][0]['userId']
        self.userIds = list()
        self.tillId = constant.config['tillIds'][0]


    def setup_method(self, method):
        self.connObj = LuciHelper.getConnObj(newConnection=True)
        self.DracraysConnObj = DracarysHelper.getConnObj(newConnection=True)
        Logger.logMethodName(method.__name__)
        constant.config['uploadedFileName'] = method.__name__
        constant.config['requestId'] = 'luci_auto_'+str(random.randint(11111, 99999))
        self.userId = constant.config['usersInfo'][0]['userId']

    @pytest.mark.parametrize('description, couponConfig, uploadType, dracarysUploadInput', [
        ('Upload UserId DiscCode', {'client_handling_type': 'DISC_CODE'}, 'USER_ID', {'userOnly' : True}),
        ('Upload Mobile DiscCode', {'client_handling_type': 'DISC_CODE'}, 'MOBILE', {'userOnly' : True}),
        ('Upload Email DiscCode', {'client_handling_type': 'DISC_CODE'}, 'EMAIL', {'userOnly' : True}),
        ('Upload ExtId DiscCode', {'client_handling_type': 'DISC_CODE'}, 'EXTERNAL_ID', {'userOnly' : True}),
    ])
    def test_LUCI_UC_01(self,description, couponConfig, uploadType, dracarysUploadInput):
        #Save Coupon Config
        for i in range(5):
            self.userIds.append(constant.config['usersInfo'][i]['userId'])
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self)
        time.sleep(2)
        couponCodeList = LuciHelper.uploadCouponAndAssertions(self,couponSeriesId, self.constructObj.importType[uploadType],noOfCouponsToBeUpload=5, dracraysUpload=dracarysUploadInput)['coupons']
        Logger.log('Coupon Code list : ', couponCodeList)
        for couponCode, self.userId in zip(couponCodeList,self.userIds):
            LuciHelper.getCouponDetailsAndAssertion(self,couponSeriesId,couponCode, couponDetailsRequest={'onlyActive': True, 'couponCodeFilter': [couponCode]})
        LuciHelper.getCouponConfigAndAssertion(self,couponSeriesId,5,0)


    @pytest.mark.parametrize('description, uploadType', [
        ('Upload duplicate userId and one valid userId', 'USER_ID'),
        ('Upload duplicate Mobile and one valid Mobile', 'MOBILE'),
        ('Upload duplicate Email and one valid Email', 'EMAIL'),
        ('Upload duplicate ExtId and one valid ExtId', 'EXTERNAL_ID')
    ])
    def test_LUCI_UC_02_sanity(self, description, uploadType):
        #Save Coupon Config
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self, couponConfigReq={'client_handling_type': 'DISC_CODE_PIN'})
        # upload coupon Code to user1
        response = LuciHelper.uploadCouponAndAssertions(self,couponSeriesId, self.constructObj.importType[uploadType],self.userId, noOfCouponsToBeUpload=2, dracraysUpload={'errorCount' : 2, 'invalidCase' : [True, False]})
        for errorMsg in response['errors']:
            Assertion.constructAssertion(errorMsg['ErrorMsg'] == 'duplicate users provided in the same file', 'Error Message is Mismatch Actual : {} and Expected: {}'.format(errorMsg['ErrorMsg'], 'duplicate users provided in the same file'))
            Assertion.constructAssertion(errorMsg['UserId'] == self.userId, 'UserId is Mismatch Actual : {} and Expected: {}'.format(errorMsg['UserId'], self.userId))
        LuciHelper.getCouponConfigAndAssertion(self,couponSeriesId,1,0)


    @pytest.mark.parametrize('description, couponConfig, expectedErrorMsg', [
        ('Upload with Max issual limit series', {'client_handling_type': 'DISC_CODE_PIN', 'max_create' : 1, 'do_not_resend_existing_voucher' : True, 'allow_multiple_vouchers_per_user' : True}, 'coupon max issual limit exceeded'),
        ('Upload with Max issual limit per user', {'client_handling_type': 'DISC_CODE_PIN', 'max_vouchers_per_user' : 1, 'do_not_resend_existing_voucher' : True, 'allow_multiple_vouchers_per_user' : True}, 'coupon max issual limit per customer exceeded'),
        ('Upload with Min days between issual', {'client_handling_type': 'DISC_CODE_PIN', 'min_days_between_vouchers' : 2, 'do_not_resend_existing_voucher' : True, 'allow_multiple_vouchers_per_user' : True}, 'coupon already issued within min days between issual limit'),
        ('Upload with Min days between issual', {'client_handling_type': 'DISC_CODE_PIN', 'do_not_resend_existing_voucher' : False, 'allow_multiple_vouchers_per_user' : False}, 'coupon already issued not uploading again as per resend config')
    ])
    def test_LUCI_UC_03(self, description, couponConfig, expectedErrorMsg):
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self, couponConfigReq=couponConfig)
        LuciHelper.uploadCouponAndAssertions(self, couponSeriesId, self.constructObj.importType['USER_ID'], self.userId, noOfCouponsToBeUpload=1)
        for uploadType in self.uploadTypeList:
            response = LuciHelper.uploadCouponAndAssertions(self,couponSeriesId, self.constructObj.importType[uploadType],self.userId, noOfCouponsToBeUpload=1, dracraysUpload={'errorCount' : 1})
            for errorMsg in response['errors']:
                Assertion.constructAssertion(errorMsg['ErrorMsg'] == expectedErrorMsg, 'Error Message is Mismatch Actual : {} and Expected: {}'.format(errorMsg['ErrorMsg'], expectedErrorMsg))
                Assertion.constructAssertion(errorMsg['UserId'] == self.userId, 'UserId is Mismatch Actual : {} and Expected: {}'.format(errorMsg['UserId'], self.userId))
        LuciHelper.getCouponConfigAndAssertion(self,couponSeriesId,1,0)

    @pytest.mark.parametrize('description, uploadType', [('Upload duplicate Coupon Code', 'NONE')])
    def test_LUCI_UC_04(self, description, uploadType):
        #Save Coupon Config
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self, couponConfigReq={'client_handling_type': 'DISC_CODE_PIN'})
        # upload coupon Code to user1
        response = LuciHelper.uploadCouponAndAssertions(self,couponSeriesId, self.constructObj.importType[uploadType],self.userId, noOfCouponsToBeUpload=2, dracraysUpload={'errorCount' : 2, 'invalidCase' : [True, False]})
        for errorMsg in response['errors']:
            Assertion.constructAssertion(errorMsg['ErrorMsg'] == 'duplicate coupons provided in the same file', 'Error Message is Mismatch Actual : {} and Expected: {}'.format(errorMsg['ErrorMsg'], 'duplicate coupons provided in the same file'))
        LuciHelper.getCouponConfigAndAssertion(self,couponSeriesId,0,0)
        createdCouponCount = LuciDBHelper.getCouponsCreated_Count(couponSeriesId, 1)
        Assertion.constructAssertion(createdCouponCount == 1, 'Uploaded coupons are recorded in coupons_created');
        Assertion.constructAssertion(self.connObj.getQueueSize(constant.config['orgId'], couponSeriesId, constant.config['requestId']) == 1, 'Coupon Code Pumped to Queue')

    @pytest.mark.parametrize('description, uploadType, expectedErrorMsg', [
        ('Upload Invalid user id', 'USER_ID', 'userid is not valid or is inactive'),
        pytest.param('Upload Invalid Coupon Code', 'MOBILE', 'user does not exist with the provided mobile', marks=pytest.mark.xfail),
        pytest.param('Upload Invalid Coupon Code', 'EMAIL', 'User does not with the provided email', marks=pytest.mark.xfail),
        pytest.param('Upload Invalid Coupon Code', 'EXTERNAL_ID', 'user does not exist with the provided external id', marks=pytest.mark.xfail),
    ])
    def test_LUCI_UC_05(self, description, uploadType, expectedErrorMsg):
        #Save Coupon Config
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self, couponConfigReq={'client_handling_type': 'DISC_CODE'})
        response = LuciHelper.uploadCouponAndAssertions(self,couponSeriesId, self.constructObj.importType[uploadType],self.userId, noOfCouponsToBeUpload=2, dracraysUpload={'errorCount' : 1, 'userOnly' : True, 'invalidCase' : [False, True]})
        for errorMsg in response['errors']:
            Assertion.constructAssertion(errorMsg['ErrorMsg'] == expectedErrorMsg, 'Error Message is Mismatch Actual : {} and Expected: {}'.format(errorMsg['ErrorMsg'], expectedErrorMsg))
        LuciHelper.getCouponConfigAndAssertion(self,couponSeriesId,2,0)

    @pytest.mark.parametrize('description, uploadType, expectedErrorMsg', [
        ('Upload duplicate Coupon Code', 'NONE', 'userid is not valid or is inactive')
    ])
    def test_LUCI_UC_06(self, description, uploadType, expectedErrorMsg):
        #Save Coupon Config
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self, couponConfigReq={'client_handling_type': 'DISC_CODE_PIN'})
        response = LuciHelper.uploadCouponAndAssertions(self,couponSeriesId, self.constructObj.importType[uploadType],self.userId, noOfCouponsToBeUpload=2, dracraysUpload={'errorCount' : 3, 'invalidCase' : [False, True]})
        for errorMsg in response['errors']:
            Assertion.constructAssertion(errorMsg['ErrorMsg'] == expectedErrorMsg, 'Error Message is Mismatch Actual : {} and Expected: {}'.format(errorMsg['ErrorMsg'], expectedErrorMsg))
        LuciHelper.getCouponConfigAndAssertion(self,couponSeriesId,0,0)
        LuciHelper.couponPumpAssertion(self,couponSeriesId,isDiscCode = False)

    @pytest.mark.parametrize('description, uploadType, expectedErrorMsg', [
        ('Upload duplicate Coupon Code', 'NONE', 'coupon code already used in this org - duplicate coupons created entry')
    ])
    def test_LUCI_UC_07(self, description, uploadType, expectedErrorMsg):
        #Save Coupon Config
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self, couponConfigReq={'client_handling_type': 'DISC_CODE_PIN'})
        LuciHelper.uploadCouponAndAssertions(self,couponSeriesId, self.constructObj.importType[uploadType],self.userId, noOfCouponsToBeUpload=2)
        LuciHelper.getCouponConfigAndAssertion(self,couponSeriesId,0,0)
        LuciHelper.couponPumpAssertion(self,couponSeriesId,isDiscCode=False,DiscCodePinCouponUploaded=2)
        response = LuciHelper.uploadCouponAndAssertions(self, couponSeriesId, self.constructObj.importType[uploadType], self.userId, noOfCouponsToBeUpload=2, dracraysUpload={'errorCount': 2, 'invalidCase': [True, True]})
        for errorMsg in response['errors']:
            Assertion.constructAssertion(errorMsg['ErrorMsg'] == expectedErrorMsg, 'Error Message is Mismatch Actual : {} and Expected: {}'.format(errorMsg['ErrorMsg'], expectedErrorMsg))

    @pytest.mark.parametrize('description, uploadType, expectedErrorMsg', [
        ('Upload duplicate Coupon Code', 'USER_ID', 'Coupon code is already used in this org')
    ])
    def test_LUCI_UC_08(self, description, uploadType, expectedErrorMsg):
        #Save Coupon Config
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self, couponConfigReq={'client_handling_type': 'DISC_CODE_PIN'})

        LuciHelper.uploadCouponAndAssertions(self,couponSeriesId, self.constructObj.importType[uploadType],self.userId, noOfCouponsToBeUpload=2)
        LuciHelper.getCouponConfigAndAssertion(self,couponSeriesId,2,0)
        response = LuciHelper.uploadCouponAndAssertions(self, couponSeriesId, self.constructObj.importType[uploadType], self.userId, noOfCouponsToBeUpload=2, dracraysUpload={'errorCount': 2, 'invalidCase': [True, True]})
        for errorMsg in response['errors']:
            Assertion.constructAssertion(errorMsg['ErrorMsg'] == expectedErrorMsg, 'Error Message is Mismatch Actual : {} and Expected: {}'.format(errorMsg['ErrorMsg'], expectedErrorMsg))

    @pytest.mark.parametrize('description, uploadType, expectedErrorMsg', [
        ('Upload Coupon with Mutual Exclusive series', 'USER_ID', 'Coupon exists for mutual exclusive series')
    ])
    def test_LUCI_UC_09(self, description, uploadType, expectedErrorMsg):
        #Save Coupon Config
        mutualCouponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self, couponConfigReq={'client_handling_type': 'DISC_CODE_PIN'})[1]

        LuciHelper.uploadCouponAndAssertions(self,mutualCouponSeriesId, self.constructObj.importType[uploadType],self.userId, noOfCouponsToBeUpload=2)
        LuciHelper.getCouponConfigAndAssertion(self,mutualCouponSeriesId,2,0)
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self, couponConfigReq={'client_handling_type': 'DISC_CODE_PIN', 'mutual_exclusive_series_ids' : '[' + str(mutualCouponSeriesId) + ']'})
        response = LuciHelper.uploadCouponAndAssertions(self, couponSeriesId, self.constructObj.importType[uploadType], self.userId, noOfCouponsToBeUpload=2, dracraysUpload={'errorCount': 2})
        for errorMsg in response['errors']:
            Assertion.constructAssertion(errorMsg['ErrorMsg'] == expectedErrorMsg, 'Error Message is Mismatch Actual : {} and Expected: {}'.format(errorMsg['ErrorMsg'], expectedErrorMsg))