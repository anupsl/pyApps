import time,pytest, random
from src.Constant.constant import constant
from src.utilities.logger import Logger
from src.utilities.assertion import Assertion
from src.utilities.utils import Utils
from src.modules.luci.luciHelper import LuciHelper
from src.modules.luci.luciObject import LuciObject
from src.modules.luci.luciDBHelper import LuciDBHelper

class Test_SaveCouponConfiguration():

    def setup_class(self):
        Logger.logSuiteName(str(self).split('.')[-1])
        self.constructObj = LuciObject()
        self.userId = constant.config['usersInfo'][0]['userId']
        self.tillId = constant.config['tillIds'][0]
        self.billId = Utils.getTime(milliSeconds=True)

    def setup_method(self, method):
        self.connObj = LuciHelper.getConnObj(newConnection=True)
        Logger.logMethodName(method.__name__)
        constant.config['requestId'] = 'luci_auto_'+str(random.randint(11111, 99999))

    @pytest.mark.parametrize('description' , [('DC to DCP and verify Coupon count')])
    def test_LUCI_SCC_031_sanity(self, description):
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self)
        LuciHelper.queuePumpWait(self, couponSeriesId)
        createdCouponCount = LuciDBHelper.getCouponsCreated_Count(couponSeriesId)
        Assertion.constructAssertion(createdCouponCount != 0, 'Coupon Code Pumped to Queue')
        couponConfigObj.update({'description': 'luci testing description changed'})
        couponConfigObj = LuciHelper.saveCouponConfigAndAssertions(self, couponConfigObj)[0]
        couponCode = LuciHelper.issueCouponAndAssertions(self,couponSeriesId)[0]
        LuciHelper.redeemCouponAndAssertions(self,[couponSeriesId],[couponCode])
        LuciHelper.getCouponConfigAndAssertion(self,couponSeriesId,1,1)

        #Changing client-handling-type
        couponConfigObj.update({'client_handling_type': 'DISC_CODE_PIN'})
        LuciHelper.saveCouponConfigAndAssertions(self, couponConfigObj)
        LuciHelper.getCouponConfigAndAssertion(self,couponSeriesId, 1, 1)
        time.sleep(2)
        createdCouponCount = LuciDBHelper.getCouponsCreated_Count(couponSeriesId,1)
        Assertion.constructAssertion(createdCouponCount == 0, 'Config changed as DC to DCP and Coupon codes marked as invalid ')

    @pytest.mark.parametrize('description', [('Pumps Coupon codes for Given count')])
    def test_LUCI_PC_001(self, description):
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self)

        time.sleep(10)
        count = 2500
        createCouponobj = LuciObject.couponCreateRequest({'couponSeriesId' : couponSeriesId, 'count' : count})
        createCouponDict = self.connObj.createCoupons(createCouponobj).__dict__

        Assertion.constructAssertion(createCouponDict['statusCode'] == 1200, 'CREATE COUPON STATUS CODE IS MISMATCH - ' + str(createCouponDict['statusCode']))
        Assertion.constructAssertion(createCouponDict['message'] == 'coupon pump successfully started', 'CREATE COUPON CODE MESSAGE IS WRONG')
        time.sleep(5)

        createdCount = LuciDBHelper.getCouponsCreated_Count(couponSeriesId)
        Assertion.constructAssertion(createdCount >= count, 'COUPON CREATED IS LESS THAN REQUEST COUNTS')