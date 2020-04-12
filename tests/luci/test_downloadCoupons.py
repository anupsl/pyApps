import time,pytest, random,requests
from src.Constant.constant import constant
from src.utilities.logger import Logger
from src.utilities.assertion import Assertion
from src.utilities.utils import Utils
from src.utilities.randValues import randValues
from src.modules.luci.dracarysHelper import DracarysHelper
from src.modules.luci.luciHelper import LuciHelper
from src.modules.luci.dracarysObject import DracarysObject
from src.modules.luci.luciObject import LuciObject

class Test_DownloadCoupons():

    def setup_class(self):
        Logger.logSuiteName(str(self).split('.')[-1])
        self.constructObj = LuciObject()
        self.DracarysObj = DracarysObject()
        self.usersInfo = constant.config['usersInfo']
        self.userId = constant.config['usersInfo'][0]['userId']
        self.tillId = constant.config['tillIds'][0]
        self.storeId = constant.config['storeIds'][0]
        self.billId = Utils.getTime(milliSeconds=True)

    def setup_method(self, method):
        self.connObj = LuciHelper.getConnObj(newConnection=True)
        Logger.logMethodName(method.__name__)
        constant.config['uploadedFileName'] = method.__name__
        self.DracraysConnObj = DracarysHelper.getConnObj(newConnection=True)
        constant.config['requestId'] = 'dracarys_auto_'+str(random.randint(11111, 99999))

    @pytest.mark.parametrize('description', [('Download Issued & Redeemed Coupon Codes')])
    def test_downloadCoupon_001_sanity(self,description):
        couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self)[1]
        couponCode = LuciHelper.issueCouponAndAssertions(self,couponSeriesId)[0]
        DracarysHelper.downloadCouponsRequestAndAssertion(self,couponSeriesId,self.DracarysObj.DownloadReportType['ISSUED'],[couponCode])
        LuciHelper.redeemCouponAndAssertions(self, couponSeriesId, couponCode)
        DracarysHelper.downloadCouponsRequestAndAssertion(self, couponSeriesId, self.DracarysObj.DownloadReportType['REDEEMED'], [couponCode])


    @pytest.mark.skipif(True, reason = 'Bulk coupon issual & Download')
    def test_downloadCoupon_002(self):
        self.couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self)[1]
        tmpListOfUsers = []
        for _ in range(2500):
            tmpListOfUsers.append(randValues.randomInteger(7))
        listOfUsers = list(set(tmpListOfUsers))
        limit = 1000
        for i in range(0, len(listOfUsers)):
            if limit > len(listOfUsers):
                limit = len(listOfUsers)
            Logger.log(listOfUsers[i:limit])
            LuciHelper.issueMultipleCoupon(self,self.couponSeriesId,listOfUsers[i:limit], expectResponseException=[True,'coupons exhausted'])
            i = limit
            limit = limit + 1000

        requestObj = DracarysObject.DownloadCouponsRequest({'couponSeriesId' : self.couponSeriesId})
        jobRes = self.DracraysConnObj.downloadCouponsReport(requestObj).__dict__
        requestsStatusObj = DracarysObject.GetDownloadStatus({'couponSeriesId' : self.couponSeriesId, 'jobId' : jobRes['jobId']})
        statusRes = self.DracraysConnObj.getDownloadStatus(requestsStatusObj).__dict__
        for _ in range(10):
            if statusRes['downloadReportJobStatus'] != 2 and statusRes['downloadReportJobStatus'] != 1:
                time.sleep(1)
                statusRes = self.DracraysConnObj.getDownloadStatus(requestsStatusObj).__dict__
            else:
                break

    @pytest.mark.parametrize('description, requestParam, expectedError', [
        ('Invalid CouponSeriesId', {'couponSeriesId' : 123}, [501, 'invalid coupon_series_id for org id']),
        ('Invalid orgId', {'orgId' : 0}, [501, 'invalid coupon_series_id for org id']),
        ('Negative orgId', {'orgId': -1}, [500, 'invalid org id-1'])])
    def test_downloadCoupon_Invalid_001(self,description, requestParam, expectedError):
        try:
            couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self)[1]
            LuciHelper.issueCouponAndAssertions(self, couponSeriesId)
            request = {'couponSeriesId': couponSeriesId, 'downloadReportType': 1}
            request.update(requestParam)
            requestObj = DracarysObject.DownloadCouponsRequest(request)
            self.DracraysConnObj.downloadCouponsReport(requestObj)
        except Exception, luciExp:
            luciExp = luciExp.__dict__
            Assertion.constructAssertion(luciExp['errorCode'] == expectedError[0], 'Error Code Mismatched Actual : {} and Expected : {}'.format(luciExp['errorCode'], expectedError[0]))
            Assertion.constructAssertion(luciExp['errorMsg'] == expectedError[1], 'Error Msg Mismatched Actual : {} and Expected : {}'.format(luciExp['errorMsg'], expectedError[0]))

    @pytest.mark.parametrize('description', [('Download External Coupon Codes')])
    def test_downloadCoupon_External(self,description):
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self,couponConfigReq={'client_handling_type' : 'DISC_CODE_PIN' , 'any_user' : True, 'isExternalIssual' : True})

        couponCode = LuciHelper.uploadCouponAndAssertions(self, couponSeriesId, 2,noOfCouponsToBeUpload = 2)['coupons'][0]
        self.userId = -1
        DracarysHelper.downloadCouponsRequestAndAssertion(self, couponSeriesId, self.DracarysObj.DownloadReportType['ISSUED'], [couponCode, 'DummyCode'])
        self.userId = constant.config['usersInfo'][0]['userId']
        LuciHelper.redeemCouponAndAssertions(self, couponSeriesId, couponCode,  couponIssuedTo=[-1])
        DracarysHelper.downloadCouponsRequestAndAssertion(self, couponSeriesId, self.DracarysObj.DownloadReportType['REDEEMED'], [couponCode])

    @pytest.mark.parametrize('description', [('Download Generic Coupon Codes')])
    def test_downloadCoupon_Generic(self,description):
        try:
            couponCode = LuciHelper.generateCouponCode()
            couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self, {'client_handling_type': 'GENERIC', 'genericCode': couponCode})

            couponCode1 = LuciHelper.issueCouponAndAssertions(self, couponSeriesId)[0]
            self.userId = constant.config['usersInfo'][1]['userId']
            couponCode2 =LuciHelper.issueCouponAndAssertions(self, couponSeriesId)[0]
            DracarysHelper.downloadCouponsRequestAndAssertion(self, couponSeriesId, self.DracarysObj.DownloadReportType['ISSUED'], [couponCode1, couponCode2])
            LuciHelper.redeemCouponAndAssertions(self, couponSeriesId, couponCode)
            DracarysHelper.downloadCouponsRequestAndAssertion(self, couponSeriesId, self.DracarysObj.DownloadReportType['REDEEMED'], [couponCode])
        finally:
            self.userId = constant.config['usersInfo'][0]['userId']

    @pytest.mark.parametrize('description', [('Download DiscCodePin Coupon Codes')])
    def test_downloadCoupon_DCP(self,description):
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self, {'client_handling_type': 'DISC_CODE_PIN'})

        LuciHelper.uploadCouponAndAssertions(self, couponSeriesId, 2, noOfCouponsToBeUpload=2)
        # Issue Coupon Code
        couponCode = LuciHelper.issueCouponAndAssertions(self, couponSeriesId)[0]
        DracarysHelper.downloadCouponsRequestAndAssertion(self, couponSeriesId, self.DracarysObj.DownloadReportType['ISSUED'], [couponCode])
        LuciHelper.redeemCouponAndAssertions(self, couponSeriesId, couponCode)
        DracarysHelper.downloadCouponsRequestAndAssertion(self, couponSeriesId, self.DracarysObj.DownloadReportType['REDEEMED'], [couponCode])

    @pytest.mark.parametrize('description', [('Download coupons issued last 24hr')])
    def test_downloadCoupon_issued_24HR(self,description):
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self, {'client_handling_type': 'DISC_CODE_PIN'})

        LuciHelper.uploadCouponAndAssertions(self, couponSeriesId, 2, noOfCouponsToBeUpload=2)
        # Issue Coupon Code
        couponCode, couponDetails = LuciHelper.issueCouponAndAssertions(self, couponSeriesId)
        changeDate = Utils.getTime(days=-1, minutes=-5,milliSeconds=True)
        self.connObj.changeCouponIssuedDate(couponDetails['id'], changeDate)
        DracarysHelper.downloadCouponsRequestAndAssertion(self, couponSeriesId, self.DracarysObj.DownloadReportType['ISSUED'], [])
        LuciHelper.redeemCouponAndAssertions(self, couponSeriesId, couponCode)
        DracarysHelper.downloadCouponsRequestAndAssertion(self, couponSeriesId, self.DracarysObj.DownloadReportType['REDEEMED'], [couponCode])