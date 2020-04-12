import pytest, random
from src.Constant.constant import constant
from src.modules.luci.luciDBHelper import LuciDBHelper
from src.utilities.logger import Logger
from src.utilities.assertion import Assertion
from src.utilities.randValues import randValues
from src.utilities.utils import Utils
from src.modules.luci.luciHelper import LuciHelper
from src.modules.luci.luciObject import LuciObject

class Test_brandCategorySKU():

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

    @pytest.mark.parametrize('description', ['Add productIds in Thrift call'])
    def test_LUCI_BCSKU_001_sanity(self,description):
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self)
        prodInfo = LuciObject.productInfo({'productIds' : [9926522, 9926523, 15972]})
        couponConfigObj.update({'productInfo' : [prodInfo]})
        couponConfigObj,couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self,couponConfigObj,{'includeProductInfo' : True})
        LuciHelper.queuePumpWait(self, couponSeriesId)
        Assertion.constructAssertion( LuciDBHelper.getCouponsCreated_Count(couponSeriesId) != 0 , 'Coupon Code Pumped to Queue')
        configRequest = LuciObject.getCouponConfigRequest({'couponSeriesId' : couponSeriesId})
        couponConfigList = self.connObj.getCouponConfiguration(configRequest)
        productInfo = couponConfigList[0].__dict__
        productInfo = productInfo['productInfo']
        productIds = []
        productIds2 = []
        voucherProductDataValuesList = LuciDBHelper.getVoucherProductDataValues(couponSeriesId)
        for k in productInfo:
            k = k.__dict__
            Assertion.constructAssertion( (k['productType'] == self.constructObj.productType['BRAND'] ) or (k['productType'] == self.constructObj.productType['CATEGORY']),'PRODUCT TYPE IS MISMATCH')
            productIds += k['productIds']
        for k in voucherProductDataValuesList:
            productIds2.append(k['product_id'])
        Assertion.constructAssertion(len(voucherProductDataValuesList) == len(productIds) , 'PRODUCT IDs COUNT IS MISMATCH')
        Assertion.constructAssertion(set(productIds) == set(productIds2), 'PRODUCT IDs ARE MISMATCH IN DB AND THRIFT RESPONSE')

    @pytest.mark.parametrize('description',['Update productIds in Thrift call'])
    def test_LUCI_BCSKU_002_sanity(self,description):
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self)
        prodInfo = LuciObject.productInfo({'productIds' : [9926522, 9926523, 15972]})
        couponConfigObj.update({'productInfo' : [prodInfo]})
        couponConfigObj,couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self,couponConfigObj,{'includeProductInfo' : True})
        prodInfo = LuciObject.productInfo({'productType' : 0, 'productIds': [1243]})
        couponConfigObj.update({'productInfo': [prodInfo]})
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self, couponConfigObj, {'includeProductInfo': True})
        LuciHelper.queuePumpWait(self, couponSeriesId)
        Assertion.constructAssertion( LuciDBHelper.getCouponsCreated_Count(couponSeriesId) != 0 , 'Coupon Code Pumped to Queue')
        configRequest = LuciObject.getCouponConfigRequest({'couponSeriesId' : couponSeriesId})
        couponConfigList = self.connObj.getCouponConfiguration(configRequest)
        productInfo = couponConfigList[0].__dict__
        productInfo = productInfo['productInfo']
        productIds = []
        productIds2 = []
        voucherProductDataValuesList = LuciDBHelper.getVoucherProductDataValues(couponSeriesId)
        for k in productInfo:
            k = k.__dict__
            Assertion.constructAssertion( (k['productType'] == self.constructObj.productType['BRAND'] ) or (k['productType'] == self.constructObj.productType['CATEGORY']),'PRODUCT TYPE IS MISMATCH')
            productIds += k['productIds']
        for k in voucherProductDataValuesList:
            productIds2.append(k['product_id'])
        Assertion.constructAssertion(len(voucherProductDataValuesList) == len(productIds) , 'PRODUCT IDs COUNT IS MISMATCH')
        Assertion.constructAssertion(set(productIds) == set(productIds2), 'PRODUCT IDs ARE MISMATCH IN DB AND THRIFT RESPONSE')


    @pytest.mark.parametrize('description', ['Merge user and getMerge user Id'])
    def test_LUCI_MU_001(self, description):
        toUserId = randValues.randomInteger(digits=6)
        actualUserId = self.userId
        try:
            couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self)
            LuciHelper.queuePumpWait(self, couponSeriesId)
            couponCode = LuciHelper.issueCouponAndAssertions(self, couponSeriesId)[0]

            mergeUserResponse = self.connObj.mergeUsers(fromUserId=self.userId, toUserId=toUserId, mergedbyTillId=self.tillId).__dict__
            Assertion.constructAssertion(mergeUserResponse['fromUserId'] == self.userId, 'Merge From userId is Matched Actual: {} & Expected: {}'.format(mergeUserResponse['fromUserId'], self.userId))
            Assertion.constructAssertion(mergeUserResponse['toUserId'] == toUserId, 'Merge to userId is Matched Actual: {} & Expected: {}'.format(mergeUserResponse['toUserId'], toUserId))
            mergeStatus = mergeUserResponse['status'].__dict__
            Assertion.constructAssertion(mergeStatus['message'] == 'customer merge was successfull', 'Merge status Msg Actual: {} & Expected: {}'.format(mergeStatus['message'], 'customer merge was successfull'))
            Assertion.constructAssertion(mergeStatus['statusCode'] == constant.MERGE_SUCCESSFUL, 'Merge status code Actual: {} & Expected: {}'.format(mergeStatus['statusCode'], constant.MERGE_SUCCESSFUL))
            mergeStatus = self.connObj.getMergeStatus(fromUserId=self.userId, toUserId=toUserId).__dict__
            Assertion.constructAssertion(mergeStatus['message'] == 'customer is already merged', 'Merge status Msg Actual: {} & Expected: {}'.format(mergeStatus['message'], 'customer is already merged'))
            Assertion.constructAssertion(mergeStatus['statusCode'] == constant.MERGED_ALREADY_DONE, 'Merge status code Actual: {} & Expected: {}'.format(mergeStatus['statusCode'], constant.MERGED_ALREADY_DONE))
            LuciHelper.redeemCouponAndAssertions(self, [couponSeriesId], [couponCode], error=[625, 'coupon not issued to this user redemption failed'])
            self.userId = toUserId
            LuciHelper.redeemCouponAndAssertions(self, [couponSeriesId], [couponCode])
        finally:
            self.userId = actualUserId