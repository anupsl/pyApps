import time, random,pytest
from src.Constant.constant import constant
from src.modules.luci.luciDBHelper import LuciDBHelper
from src.utilities.logger import Logger
from src.utilities.assertion import Assertion
from src.utilities.utils import Utils
from src.modules.luci.luciHelper import LuciHelper
from src.modules.luci.luciObject import LuciObject

class Test_CouponSearch():

    def setup_class(self):
        Logger.logSuiteName(str(self).split('.')[-1])
        self.constructObj = LuciObject()
        self.userId = constant.config['usersInfo'][0]['userId']
        self.tillId = constant.config['tillIds'][0]
        self.storeId = constant.config['storeIds'][0]
        self.billId = Utils.getTime(milliSeconds=True)


    def setup_method(self, method):
        self.connObj = LuciHelper.getConnObj(newConnection=True)
        Logger.logMethodName(method.__name__)
        constant.config['requestId'] = 'luci_auto_'+str(random.randint(11111, 99999))

    # description = "Issual Filtes:Get coupon details by providing transaction id,org id and user id"
    def test_LUCI_GCD_011_sanity(self):
        #Save Coupon Config
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self)

        #Checking Coupon Created Count
        LuciHelper.queuePumpWait(self,couponSeriesId)
        createdCouponCount = LuciDBHelper.getCouponsCreated_Count(couponSeriesId)
        Assertion.constructAssertion(createdCouponCount != 0, 'Coupon Code Pumped to Queue')

        # change the coupon config
        couponConfigObj.update({'do_not_resend_existing_voucher' : True, 'allow_multiple_vouchers_per_user' : True})
        LuciHelper.saveCouponConfigAndAssertions(self,couponConfigObj)

        transactionId1 = Utils.getTime(milliSeconds=True);
        time.sleep(1)
        transactionId2 = Utils.getTime(milliSeconds=True);

        #Construct Obj and Issue Coupon Code
        issueCouponObj ={'couponSeriesRequired': True, 'billId' : transactionId1}
        couponCode1 = LuciHelper.issueCouponAndAssertions(self,couponSeriesId,issueCouponObj)[0]

        #Change Issue obj billId and Issue one more coupon
        issueCouponObj = {'couponSeriesRequired': True, 'billId': transactionId2}
        couponCode2 = LuciHelper.issueCouponAndAssertions(self,couponSeriesId, issueCouponObj)[0]

        # Added Issue Filter & Search Coupon 1
        issualFilterObj = LuciObject.issualFilters({'transactionId' : [transactionId1]})
        issualFilterObj = {'issualFilters': issualFilterObj}
        LuciHelper.couponSearchAndAssertion(self, [couponSeriesId],issualFilterObj ,[couponCode1])

        #Added Issue Filter & Search Coupon 2
        issualFilterObj = LuciObject.issualFilters({'transactionId': [transactionId2]})
        issualFilterObj = {'issualFilters': issualFilterObj}
        LuciHelper.couponSearchAndAssertion(self, [couponSeriesId], issualFilterObj, [couponCode2])

        # Added Issue Filter & Search Coupon 3
        issualFilterObj = LuciObject.issualFilters({'transactionId': [transactionId1 , transactionId2]})
        issualFilterObj = {'issualFilters': issualFilterObj}
        LuciHelper.couponSearchAndAssertion(self, [couponSeriesId],issualFilterObj, [couponCode1,couponCode2])

    # description = "Issual Filters: Get coupon details by providing redeemableAtStoreId,org id, coupon series id and user id"
    def test_LUCI_GCD_012(self):
        # Save Coupon Config
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self)

        couponConfigObj.update({'redeem_at_store' : str([self.tillId])})
        LuciHelper.saveCouponConfigAndAssertions(self,couponConfigObj)

        couponCode = LuciHelper.issueCouponAndAssertions(self,couponSeriesId)[0]
        # Added Issue Filter
        issualFilterObj = LuciObject.issualFilters({'redeemableAtStoreId': [self.storeId]})
        issualFilterObj = {'issualFilters': issualFilterObj}
        #coupon Search and Assertion
        LuciHelper.couponSearchAndAssertion(self, [couponSeriesId], issualFilterObj, [couponCode])

    # description = "Issual Filters:Get coupon details by providing issual date range,org id and user id"
    def test_LUCI_GCD_013(self):
        # Save Coupon Config
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self)

        couponConfigObj.update({'allow_multiple_vouchers_per_user' : True, 'do_not_resend_existing_voucher' : True})
        LuciHelper.saveCouponConfigAndAssertions(self,couponConfigObj)

        couponCode1, detailsDict = LuciHelper.issueCouponAndAssertions(self,couponSeriesId)
        issualStartTime1 = detailsDict['issuedDate']
        issualEndTime1 = issualStartTime1 + 4000

        # coupon Search and Assertion
        issualFilterObj = LuciObject.issualFilters({'issualDateStart': (issualStartTime1 - 2000), 'issualDateEnd' : (issualEndTime1 + 2000)})
        issualFilterObj = {'issualFilters': issualFilterObj}
        LuciHelper.couponSearchAndAssertion(self, [couponSeriesId], issualFilterObj, [couponCode1])

        time.sleep(4)
        couponCode2, detailsDict = LuciHelper.issueCouponAndAssertions(self,couponSeriesId)
        issualStartTime2 = detailsDict['issuedDate']
        issualEndTime2 = issualStartTime2 + 4000

        # coupon Search and Assertion
        issualFilterObj = LuciObject.issualFilters({'issualDateStart': (issualStartTime2-2000), 'issualDateEnd' : (issualEndTime2 + 2000)})
        issualFilterObj = {'issualFilters': issualFilterObj}
        LuciHelper.couponSearchAndAssertion(self, [couponSeriesId], issualFilterObj, [couponCode2])


        # coupon Search and Assertion
        issualFilterObj = LuciObject.issualFilters({'issualDateStart': (issualStartTime1-2000), 'issualDateEnd' : (issualEndTime2 + 2000)})
        issualFilterObj = {'issualFilters': issualFilterObj}
        LuciHelper.couponSearchAndAssertion(self, [couponSeriesId], issualFilterObj, [couponCode1,couponCode2])

    # description = "RedemptionFilters: Get coupon details by providing redemption transaction id,org id and user id"
    def test_LUCI_GCD_014(self):
        # Save Coupon Config
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self)

        couponConfigObj.update({'allow_multiple_vouchers_per_user' : True, 'do_not_resend_existing_voucher' : True,
                                'same_user_multiple_redeem' : True,'multiple_use' : True})
        LuciHelper.saveCouponConfigAndAssertions(self,couponConfigObj)


        couponCode1 = LuciHelper.issueCouponAndAssertions(self,couponSeriesId)[0]
        couponCode2 = LuciHelper.issueCouponAndAssertions(self,couponSeriesId)[0]

        tempBill1 = self.billId
        LuciHelper.redeemCouponAndAssertions(self, couponSeriesId, couponCode1)
        tempBill2 = self.billId = Utils.getTime(milliSeconds=True)
        LuciHelper.redeemCouponAndAssertions(self, couponSeriesId, couponCode2)

        # coupon Search and Assertion
        redemptionFiltersObj = LuciObject.redemptionFilters({'transactionId' : [tempBill1]})
        redemptionFiltersObj = {'redemptionFilters' : redemptionFiltersObj}
        LuciHelper.couponSearchAndAssertion(self, [couponSeriesId], redemptionFiltersObj, [couponCode1])

        redemptionFiltersObj = LuciObject.redemptionFilters({'transactionId' : [tempBill2]})
        redemptionFiltersObj = {'redemptionFilters' : redemptionFiltersObj}
        LuciHelper.couponSearchAndAssertion(self, [couponSeriesId], redemptionFiltersObj, [couponCode2])

        redemptionFiltersObj = LuciObject.redemptionFilters({'transactionId' : [tempBill1,tempBill2]})
        redemptionFiltersObj = {'redemptionFilters' : redemptionFiltersObj}
        LuciHelper.couponSearchAndAssertion(self, [couponSeriesId], redemptionFiltersObj, [couponCode1, couponCode2])

    # description = "RedemptionFilters: Get coupon details by providing redemption transaction number,org id and user id"
    def test_LUCI_GCD_015(self):
        # Save Coupon Config
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self)

        couponConfigObj.update({'allow_multiple_vouchers_per_user' : True, 'do_not_resend_existing_voucher' : True,
                                'same_user_multiple_redeem' : True,'multiple_use' : True})
        LuciHelper.saveCouponConfigAndAssertions(self,couponConfigObj)

        couponCode1 = LuciHelper.issueCouponAndAssertions(self,couponSeriesId)[0]
        couponCode2 = LuciHelper.issueCouponAndAssertions(self,couponSeriesId)[0]

        transNum1 = LuciHelper.redeemCouponAndAssertions(self, couponSeriesId, couponCode1)['transactionNumber']
        time.sleep(1)
        self.billId = Utils.getTime(milliSeconds=True)
        transNum2 = LuciHelper.redeemCouponAndAssertions(self, couponSeriesId, couponCode2)['transactionNumber']

        time.sleep(1)
        # coupon Search and Assertion
        redemptionFiltersObj = LuciObject.redemptionFilters({'transactionNumber' : [transNum1]})
        redemptionFiltersObj = {'redemptionFilters' : redemptionFiltersObj}
        LuciHelper.couponSearchAndAssertion(self, [couponSeriesId], redemptionFiltersObj, [couponCode1])

        redemptionFiltersObj = LuciObject.redemptionFilters({'transactionNumber' : [transNum2]})
        redemptionFiltersObj = {'redemptionFilters' : redemptionFiltersObj}
        LuciHelper.couponSearchAndAssertion(self, [couponSeriesId], redemptionFiltersObj, [couponCode2])

        redemptionFiltersObj = LuciObject.redemptionFilters({'transactionNumber' : [transNum1,transNum2]})
        redemptionFiltersObj = {'redemptionFilters' : redemptionFiltersObj}
        LuciHelper.couponSearchAndAssertion(self, [couponSeriesId], redemptionFiltersObj, [couponCode1, couponCode2])

    # description = "Redemption Filters:Get coupon details by providing redemption date range,org id and user id"
    def test_LUCI_GCD_016(self):
        # Save Coupon Config
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self)

        couponConfigObj.update({'allow_multiple_vouchers_per_user': True, 'do_not_resend_existing_voucher': True,
                                'same_user_multiple_redeem': True, 'multiple_use': True})
        LuciHelper.saveCouponConfigAndAssertions(self,couponConfigObj)

        couponCode1 = LuciHelper.issueCouponAndAssertions(self,couponSeriesId)[0]
        couponCode2 = LuciHelper.issueCouponAndAssertions(self,couponSeriesId)[0]

        redeemedDate1 = LuciHelper.redeemCouponAndAssertions(self, couponSeriesId, couponCode1)['redemptionDate']
        time.sleep(2)
        self.billId = Utils.getTime(milliSeconds=True)
        redeemedDate2 = LuciHelper.redeemCouponAndAssertions(self, couponSeriesId, couponCode2)['redemptionDate']

        # coupon Search and Assertion
        redemptionFiltersObj = LuciObject.redemptionFilters({'redemptionDateStart': (redeemedDate1 - 1000),'redemptionDateEnd': (redeemedDate1 + 1000)})
        redemptionFiltersObj = {'redemptionFilters': redemptionFiltersObj}
        LuciHelper.couponSearchAndAssertion(self, [couponSeriesId], redemptionFiltersObj, [couponCode1])

        redemptionFiltersObj = LuciObject.redemptionFilters({'redemptionDateStart': (redeemedDate2 - 1000),'redemptionDateEnd': (redeemedDate2 + 1000)})
        redemptionFiltersObj = {'redemptionFilters': redemptionFiltersObj}
        LuciHelper.couponSearchAndAssertion(self, [couponSeriesId], redemptionFiltersObj, [couponCode2])

        redemptionFiltersObj = LuciObject.redemptionFilters({'redemptionDateStart': (redeemedDate1 - 1000),'redemptionDateEnd': (redeemedDate2 + 1000)})
        redemptionFiltersObj = {'redemptionFilters': redemptionFiltersObj}
        LuciHelper.couponSearchAndAssertion(self, [couponSeriesId], redemptionFiltersObj, [couponCode1, couponCode2])

    # description = "Coupoun Status: Get EXPIRED coupon details by providing org id, coupon series id and user id"
    def test_LUCI_GCD_017(self):
        # Save Coupon Config
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self)

        couponConfigObj.update({'allow_multiple_vouchers_per_user': True, 'do_not_resend_existing_voucher': True,
                                'same_user_multiple_redeem': True, 'multiple_use': True,'valid_days_from_create' : -1,
                                'expiry_strategy_value' : -1})
        LuciHelper.saveCouponConfigAndAssertions(self,couponConfigObj)

        couponCode1 = LuciHelper.issueCouponAndAssertions(self,couponSeriesId)[0]
        time.sleep(1)
        couponCode2 = LuciHelper.issueCouponAndAssertions(self,couponSeriesId)[0]

        LuciHelper.couponSearchAndAssertion(self, [couponSeriesId], {'couponStatus' : [self.constructObj.couponStatus['EXPIRED']],
                                'sort' : self.constructObj.sort['DESC']}, [couponCode2, couponCode1])

    # description = "Coupoun Status: Get ACTIVE coupon details by providing org id, coupon series id and user id"
    def test_LUCI_GCD_018(self):
        # Save Coupon Config
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self)

        couponConfigObj.update({'allow_multiple_vouchers_per_user': True, 'do_not_resend_existing_voucher': True,
                                'same_user_multiple_redeem': True, 'multiple_use': True,})
        LuciHelper.saveCouponConfigAndAssertions(self,couponConfigObj)

        couponCode1 = LuciHelper.issueCouponAndAssertions(self,couponSeriesId)[0]
        time.sleep(2)
        couponCode2 = LuciHelper.issueCouponAndAssertions(self,couponSeriesId)[0]

        LuciHelper.couponSearchAndAssertion(self, [couponSeriesId],{'couponStatus': [self.constructObj.couponStatus['ACTIVE']],
                                          'sort': self.constructObj.sort['DESC']}, [couponCode2, couponCode1])

    # description = "Coupoun Status: Get REDEEMED coupon details by providing org id, coupon series id and user id"
    def test_LUCI_GCD_019(self):
        # Save Coupon Config
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self)

        couponConfigObj.update({'allow_multiple_vouchers_per_user': True, 'do_not_resend_existing_voucher': True,
                                'same_user_multiple_redeem': True, 'multiple_use': True, })
        LuciHelper.saveCouponConfigAndAssertions(self,couponConfigObj)

        #issue and redeem the coupon code
        couponCode = LuciHelper.issueCouponAndAssertions(self,couponSeriesId)[0]
        LuciHelper.redeemCouponAndAssertions(self, couponSeriesId, couponCode)

        LuciHelper.couponSearchAndAssertion(self, [couponSeriesId],{'couponStatus': [self.constructObj.couponStatus['REDEEMED']],
                                          'sort': self.constructObj.sort['DESC']}, [couponCode])

    # description = "Coupoun Status: Get UNREDEEMED coupon details by providing org id, coupon series id and user id"
    def test_LUCI_GCD_020(self):
        # Save Coupon Config
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self)

        couponConfigObj.update({'allow_multiple_vouchers_per_user': True, 'do_not_resend_existing_voucher': True,
                                'same_user_multiple_redeem': True, 'multiple_use': True, })
        LuciHelper.saveCouponConfigAndAssertions(self,couponConfigObj)

        # issue and redeem the coupon code
        couponCode1 = LuciHelper.issueCouponAndAssertions(self,couponSeriesId)[0]
        couponCode2 = LuciHelper.issueCouponAndAssertions(self,couponSeriesId)[0]
        LuciHelper.redeemCouponAndAssertions(self, couponSeriesId, couponCode1)

        LuciHelper.couponSearchAndAssertion(self, [couponSeriesId], {'couponStatus': [self.constructObj.couponStatus['UNREDEEMED']],
                                                       'sort': self.constructObj.sort['DESC']}, [couponCode2])

    # description = "Issual & Redemption Filters:Get coupon details by providing issual date range,org id and user id"
    def test_LUCI_GCD_021(self):
        # Save Coupon Config
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self)

        couponConfigObj.update({'allow_multiple_vouchers_per_user': True, 'do_not_resend_existing_voucher': True})
        LuciHelper.saveCouponConfigAndAssertions(self,couponConfigObj)

        couponCode1, detailsDict = LuciHelper.issueCouponAndAssertions(self,couponSeriesId)
        issualStartTime1 = detailsDict['issuedDate']
        issualEndTime1 = issualStartTime1 + 4000
        Logger.log('Issued Date and Time : {} , EndTime : {}'.format(issualStartTime1,issualEndTime1))


        # coupon Search and Assertion
        time.sleep(4)
        couponCode2, detailsDict = LuciHelper.issueCouponAndAssertions(self,couponSeriesId)
        issualStartTime2 = detailsDict['issuedDate']
        issualEndTime2 = issualStartTime2 + 4000

        redeemedDate1 = LuciHelper.redeemCouponAndAssertions(self, couponSeriesId, couponCode1)['redemptionDate']
        time.sleep(4)
        self.billId = Utils.getTime(milliSeconds=True)
        redeemedDate2 = LuciHelper.redeemCouponAndAssertions(self, couponSeriesId, couponCode2)['redemptionDate']

        # coupon Search and Assertion
        redemptionFiltersObj = LuciObject.redemptionFilters({'redemptionDateStart': (redeemedDate1 - 1000),'redemptionDateEnd': (redeemedDate1 + 1000)})
        issualFilterObj = LuciObject.issualFilters({'issualDateStart': (issualStartTime1 - 1000), 'issualDateEnd': (issualEndTime1 + 1000)})
        couponSearchRequest = {'redemptionFilters': redemptionFiltersObj, 'issualFilters': issualFilterObj}
        LuciHelper.couponSearchAndAssertion(self, [couponSeriesId], couponSearchRequest, [couponCode1])

        redemptionFiltersObj = LuciObject.redemptionFilters({'redemptionDateStart': (redeemedDate2 - 1000),'redemptionDateEnd': (redeemedDate2 + 1000)})
        issualFilterObj = LuciObject.issualFilters({'issualDateStart': (issualStartTime2 - 1000), 'issualDateEnd': (issualEndTime2 + 1000)})
        couponSearchRequest = {'redemptionFilters': redemptionFiltersObj, 'issualFilters': issualFilterObj}
        LuciHelper.couponSearchAndAssertion(self, [couponSeriesId], couponSearchRequest, [couponCode2])

        redemptionFiltersObj = LuciObject.redemptionFilters({'redemptionDateStart': (redeemedDate1 - 1000),'redemptionDateEnd': (redeemedDate2 + 1000)})
        issualFilterObj = LuciObject.issualFilters({'issualDateStart': (issualStartTime1 - 1000), 'issualDateEnd': (issualEndTime2 + 1000)})
        couponSearchRequest = {'redemptionFilters': redemptionFiltersObj, 'issualFilters': issualFilterObj}
        LuciHelper.couponSearchAndAssertion(self, [couponSeriesId], couponSearchRequest, [couponCode1, couponCode2])

    # description = "Issual Filters, RedemptionFilters: Get coupon details by providing issual date start, issual date end, redemption transaction id,org id and user id"
    def test_LUCI_GCD_022(self):
        # Save Coupon Config
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self)

        couponConfigObj.update({'allow_multiple_vouchers_per_user': True, 'do_not_resend_existing_voucher': True})
        LuciHelper.saveCouponConfigAndAssertions(self,couponConfigObj)

        couponCode1, detailsDict = LuciHelper.issueCouponAndAssertions(self,couponSeriesId)
        issualStartTime1 = detailsDict['issuedDate']
        issualEndTime1 = issualStartTime1 + 1000

        # coupon Search and Assertion
        time.sleep(4)
        couponCode2, detailsDict = LuciHelper.issueCouponAndAssertions(self,couponSeriesId)
        issualStartTime2 = detailsDict['issuedDate']
        issualEndTime2 = issualStartTime2 + 1000

        transNum1 = LuciHelper.redeemCouponAndAssertions(self, couponSeriesId, couponCode1)['transactionNumber']
        self.billId = Utils.getTime(milliSeconds=True)
        transNum2 = LuciHelper.redeemCouponAndAssertions(self, couponSeriesId, couponCode2)['transactionNumber']

        # coupon Search and Assertion
        redemptionFiltersObj = LuciObject.redemptionFilters({'transactionNumber' : [transNum1]})
        issualFilterObj = LuciObject.issualFilters({'issualDateStart': (issualStartTime1), 'issualDateEnd': (issualEndTime1)})
        couponSearchRequest = {'redemptionFilters': redemptionFiltersObj, 'issualFilters': issualFilterObj}
        LuciHelper.couponSearchAndAssertion(self, [couponSeriesId], couponSearchRequest, [couponCode1])

        redemptionFiltersObj = LuciObject.redemptionFilters({'transactionNumber' : [transNum2]})
        issualFilterObj = LuciObject.issualFilters({'issualDateStart': (issualStartTime2), 'issualDateEnd': (issualEndTime2)})
        couponSearchRequest = {'redemptionFilters': redemptionFiltersObj, 'issualFilters': issualFilterObj}
        LuciHelper.couponSearchAndAssertion(self, [couponSeriesId], couponSearchRequest, [couponCode2])

        redemptionFiltersObj = LuciObject.redemptionFilters({'transactionNumber' : [transNum1,transNum2]})
        issualFilterObj = LuciObject.issualFilters({'issualDateStart': (issualStartTime1), 'issualDateEnd': (issualEndTime2)})
        couponSearchRequest = {'redemptionFilters': redemptionFiltersObj, 'issualFilters': issualFilterObj}
        LuciHelper.couponSearchAndAssertion(self, [couponSeriesId], couponSearchRequest, [couponCode1, couponCode2])

    # description = "Issual Filetrs, Redemption filters: Get coupon details by providing transaction id,redeem date start and end,org id and user id"
    def test_LUCI_GCD_023(self):
        # Save Coupon Config
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self)

        couponConfigObj.update({'allow_multiple_vouchers_per_user': True, 'do_not_resend_existing_voucher': True})
        LuciHelper.saveCouponConfigAndAssertions(self,couponConfigObj)

        transactionId1 = Utils.getTime(milliSeconds=True);
        time.sleep(2)
        transactionId2 = Utils.getTime(milliSeconds=True);

        # Construct Obj and Issue Coupon Code
        issueCouponObj = {'couponSeriesRequired': True, 'billId': transactionId1}
        couponCode1 = LuciHelper.issueCouponAndAssertions(self,couponSeriesId, issueCouponObj)[0]

        # Change Issue obj billId and Issue one more coupon
        issueCouponObj = {'couponSeriesRequired': True, 'billId': transactionId2}
        couponCode2 = LuciHelper.issueCouponAndAssertions(self,couponSeriesId, issueCouponObj)[0]

        redeemedDate1 = LuciHelper.redeemCouponAndAssertions(self, couponSeriesId, couponCode1)['redemptionDate']
        time.sleep(4)
        self.billId = Utils.getTime(milliSeconds=True)
        redeemedDate2 = LuciHelper.redeemCouponAndAssertions(self, couponSeriesId, couponCode2)['redemptionDate']

        # coupon Search and Assertion
        redemptionFiltersObj = LuciObject.redemptionFilters({'redemptionDateStart': (redeemedDate1 - 1000), 'redemptionDateEnd': (redeemedDate1 + 1000)})
        issualFilterObj = LuciObject.issualFilters({'transactionId': [transactionId1]})
        couponSearchRequest = {'redemptionFilters': redemptionFiltersObj, 'issualFilters': issualFilterObj}
        LuciHelper.couponSearchAndAssertion(self, [couponSeriesId], couponSearchRequest, [couponCode1])

        redemptionFiltersObj = LuciObject.redemptionFilters({'redemptionDateStart': (redeemedDate2 - 1000), 'redemptionDateEnd': (redeemedDate2 + 1000)})
        issualFilterObj = LuciObject.issualFilters({'transactionId': [transactionId2]})
        couponSearchRequest = {'redemptionFilters': redemptionFiltersObj, 'issualFilters': issualFilterObj}
        LuciHelper.couponSearchAndAssertion(self, [couponSeriesId], couponSearchRequest, [couponCode2])

        redemptionFiltersObj = LuciObject.redemptionFilters({'redemptionDateStart': (redeemedDate1 - 1000), 'redemptionDateEnd': (redeemedDate2 + 1000)})
        issualFilterObj = LuciObject.issualFilters({'transactionId': [transactionId1, transactionId2]})
        couponSearchRequest = {'redemptionFilters': redemptionFiltersObj, 'issualFilters': issualFilterObj}
        LuciHelper.couponSearchAndAssertion(self, [couponSeriesId], couponSearchRequest, [couponCode1, couponCode2])

    # description = "Issual Filetrs, Redemption filters: Get coupon details by providing issual transaction id,redemption transaction id,org id and user id"
    def test_LUCI_GCD_024(self):
        # Save Coupon Config
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self)

        couponConfigObj.update({'allow_multiple_vouchers_per_user': True, 'do_not_resend_existing_voucher': True})
        LuciHelper.saveCouponConfigAndAssertions(self,couponConfigObj)

        transactionId1 = Utils.getTime(milliSeconds=True);
        time.sleep(2)
        transactionId2 = Utils.getTime(milliSeconds=True);

        # Construct Obj and Issue Coupon Code
        issueCouponObj = {'couponSeriesRequired': True, 'billId': transactionId1}
        couponCode1 = LuciHelper.issueCouponAndAssertions(self,couponSeriesId, issueCouponObj)[0]

        # Change Issue obj billId and Issue one more coupon
        issueCouponObj = {'couponSeriesRequired': True, 'billId': transactionId2}
        couponCode2 = LuciHelper.issueCouponAndAssertions(self,couponSeriesId, issueCouponObj)[0]

        tempBill1 = self.billId
        LuciHelper.redeemCouponAndAssertions(self, couponSeriesId, couponCode1)
        tempBill2 = self.billId = Utils.getTime(milliSeconds=True)
        LuciHelper.redeemCouponAndAssertions(self, couponSeriesId, couponCode2)

        # coupon Search and Assertion
        redemptionFiltersObj = LuciObject.redemptionFilters({'transactionId' : [tempBill1]})
        issualFilterObj = LuciObject.issualFilters({'transactionId': [transactionId1]})
        couponSearchRequest = {'redemptionFilters': redemptionFiltersObj, 'issualFilters': issualFilterObj}
        LuciHelper.couponSearchAndAssertion(self, [couponSeriesId], couponSearchRequest, [couponCode1])

        redemptionFiltersObj = LuciObject.redemptionFilters({'transactionId' : [tempBill2]})
        issualFilterObj = LuciObject.issualFilters({'transactionId': [transactionId2]})
        couponSearchRequest = {'redemptionFilters': redemptionFiltersObj, 'issualFilters': issualFilterObj}
        LuciHelper.couponSearchAndAssertion(self, [couponSeriesId], couponSearchRequest, [couponCode2])

        redemptionFiltersObj = LuciObject.redemptionFilters({'transactionId' : [tempBill1,tempBill2]})
        issualFilterObj = LuciObject.issualFilters({'transactionId': [transactionId1, transactionId2]})
        couponSearchRequest = {'redemptionFilters': redemptionFiltersObj, 'issualFilters': issualFilterObj}
        LuciHelper.couponSearchAndAssertion(self, [couponSeriesId], couponSearchRequest, [couponCode1, couponCode2])

    # description = "Issual Filters,Redeemption Filters: Get coupon details by providing redeemableAtStoreId,redemption transaction number,org id, coupon series id and user id"
    def test_LUCI_GCD_025(self):
        # Save Coupon Config
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self)

        couponConfigObj.update({'allow_multiple_vouchers_per_user': True, 'do_not_resend_existing_voucher': True, 'redeem_at_store' : str([self.tillId])})
        LuciHelper.saveCouponConfigAndAssertions(self,couponConfigObj)

        couponCode1 = LuciHelper.issueCouponAndAssertions(self,couponSeriesId)[0]
        couponCode2 = LuciHelper.issueCouponAndAssertions(self,couponSeriesId)[0]

        transNum1 = LuciHelper.redeemCouponAndAssertions(self, couponSeriesId, couponCode1)['transactionNumber']
        time.sleep(1)
        self.billId = Utils.getTime(milliSeconds=True)
        transNum2 = LuciHelper.redeemCouponAndAssertions(self, couponSeriesId, couponCode2)['transactionNumber']

        # coupon Search and Assertion
        redemptionFiltersObj = LuciObject.redemptionFilters({'transactionNumber': [transNum1]})
        issualFilterObj = LuciObject.issualFilters({'redeemableAtStoreId': [self.storeId]})
        couponSearchRequest = {'redemptionFilters': redemptionFiltersObj, 'issualFilters': issualFilterObj}
        LuciHelper.couponSearchAndAssertion(self, [couponSeriesId], couponSearchRequest, [couponCode1])

        redemptionFiltersObj = LuciObject.redemptionFilters({'transactionNumber': [transNum2]})
        issualFilterObj = LuciObject.issualFilters({'redeemableAtStoreId': [self.storeId]})
        couponSearchRequest = {'redemptionFilters': redemptionFiltersObj, 'issualFilters': issualFilterObj}
        LuciHelper.couponSearchAndAssertion(self, [couponSeriesId], couponSearchRequest, [couponCode2])

        redemptionFiltersObj = LuciObject.redemptionFilters({'transactionNumber': [transNum1, transNum2]})
        issualFilterObj = LuciObject.issualFilters({'redeemableAtStoreId': [self.storeId]})
        couponSearchRequest = {'redemptionFilters': redemptionFiltersObj, 'issualFilters': issualFilterObj}
        LuciHelper.couponSearchAndAssertion(self, [couponSeriesId], couponSearchRequest, [couponCode1, couponCode2])

    # description = "Get coupon details by providing Offset,Limit,org id, coupon series id and user id"
    def test_LUCI_GCD_026(self):
        # Save Coupon Config
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self)

        couponConfigObj.update({'allow_multiple_vouchers_per_user': True, 'do_not_resend_existing_voucher': True, 'redeem_at_store' : str([self.tillId])})
        LuciHelper.saveCouponConfigAndAssertions(self,couponConfigObj)

        couponCode1 = LuciHelper.issueCouponAndAssertions(self,couponSeriesId)[0]
        time.sleep(2)
        couponCode2 = LuciHelper.issueCouponAndAssertions(self,couponSeriesId)[0]
        time.sleep(2)
        couponCode3 = LuciHelper.issueCouponAndAssertions(self,couponSeriesId)[0]
        time.sleep(2)
        couponCode4 = LuciHelper.issueCouponAndAssertions(self,couponSeriesId)[0]
        time.sleep(2)
        couponCode5 = LuciHelper.issueCouponAndAssertions(self,couponSeriesId)[0]

        couponSearchRequest = {'offset' : 2, 'limit' : 2, 'sort' : self.constructObj.sort['DESC']}
        LuciHelper.couponSearchAndAssertion(self, [couponSeriesId], couponSearchRequest, [couponCode3,couponCode2])

        couponSearchRequest = {'offset': 1}
        LuciHelper.couponSearchAndAssertion(self, [couponSeriesId], couponSearchRequest, [couponCode2, couponCode3,couponCode4,couponCode5])

        couponSearchRequest = {'limit': 3}
        LuciHelper.couponSearchAndAssertion(self, [couponSeriesId], couponSearchRequest, [couponCode1, couponCode2,couponCode3])

    # description = "Get coupon details by providing sortBy, coupon series id and user id"
    def test_LUCI_GCD_027(self):
        # Save Coupon Config
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self)

        couponConfigObj.update({'allow_multiple_vouchers_per_user': True, 'do_not_resend_existing_voucher': True, 'redeem_at_store' : str([self.tillId])})
        LuciHelper.saveCouponConfigAndAssertions(self,couponConfigObj)

        couponCode1 = LuciHelper.issueCouponAndAssertions(self,couponSeriesId)[0]
        time.sleep(2)
        couponCode2 = LuciHelper.issueCouponAndAssertions(self,couponSeriesId)[0]
        time.sleep(2)
        couponCode3 = LuciHelper.issueCouponAndAssertions(self,couponSeriesId)[0]
        time.sleep(2)
        couponCode4 = LuciHelper.issueCouponAndAssertions(self,couponSeriesId)[0]
        time.sleep(2)
        couponCode5 = LuciHelper.issueCouponAndAssertions(self,couponSeriesId)[0]

        couponSearchRequest = {'sort' : self.constructObj.sort['ASC']}
        LuciHelper.couponSearchAndAssertion(self, [couponSeriesId], couponSearchRequest, [couponCode1,couponCode2,couponCode3,couponCode4, couponCode5])

        couponSearchRequest = {'sort': self.constructObj.sort['DESC']}
        LuciHelper.couponSearchAndAssertion(self, [couponSeriesId], couponSearchRequest, [couponCode5, couponCode4, couponCode3,couponCode2,couponCode1])

    # description = "Get coupon details by providing OrderBy, coupon series id and user id"
    def test_LUCI_GCD_028(self):
        # Save Coupon Config
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self)

        couponConfigObj.update({'allow_multiple_vouchers_per_user': True, 'do_not_resend_existing_voucher': True, 'redeem_at_store' : str([self.tillId])})
        LuciHelper.saveCouponConfigAndAssertions(self,couponConfigObj)

        couponCode1 = LuciHelper.issueCouponAndAssertions(self,couponSeriesId,{'storeUnitId' : constant.config['tillIds'][2]})[0]
        time.sleep(2)
        couponCode2 = LuciHelper.issueCouponAndAssertions(self,couponSeriesId)[0]
        time.sleep(2)
        couponCode3 = LuciHelper.issueCouponAndAssertions(self,couponSeriesId,{'storeUnitId' : constant.config['tillIds'][1]})[0]

        couponSearchRequest = {'orderBy' : self.constructObj.orderBy['ISSUED_TILL']}
        LuciHelper.couponSearchAndAssertion(self, [couponSeriesId], couponSearchRequest, [couponCode2,couponCode3,couponCode1])

        couponSearchRequest = {'orderBy': self.constructObj.orderBy['CREATED_DATE']}
        LuciHelper.couponSearchAndAssertion(self, [couponSeriesId], couponSearchRequest, [couponCode1, couponCode2, couponCode3])

    # description = "Get coupon details by providing coupoun series as 'Campaig','DVS'Goodwill',org id, coupon series id and user id"
    def test_LUCI_GCD_029(self):
        # Save Coupon Config
        try:
            couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self)

            couponConfigObj.update({'allow_multiple_vouchers_per_user': True, 'do_not_resend_existing_voucher': True, 'redeem_at_store': str([self.tillId])})
            couponConfigObj = LuciHelper.saveCouponConfigAndAssertions(self, couponConfigObj)[0]

            couponCode1 = LuciHelper.issueCouponAndAssertions(self, couponSeriesId)[0]
            couponSearchRequest = {'sort': self.constructObj.sort['DESC'], 'couponSeriesType': self.constructObj.couponSeriesType['CAMPAIGN']}
            LuciHelper.couponSearchAndAssertion(self, [couponSeriesId], couponSearchRequest, [couponCode1])
            time.sleep(2)

            couponConfigObj.update({'series_type': 'DVS'})
            couponConfigObj = LuciHelper.saveCouponConfigAndAssertions(self, couponConfigReq=couponConfigObj)[0]
            couponCode2 = LuciHelper.issueCouponAndAssertions(self, couponSeriesId)[0]
            couponSearchRequest = {'sort': self.constructObj.sort['DESC'], 'couponSeriesType': self.constructObj.couponSeriesType['DVS']}
            LuciHelper.couponSearchAndAssertion(self, [couponSeriesId], couponSearchRequest, [couponCode2, couponCode1])
            time.sleep(2)

            couponConfigObj.update({'series_type': 'GOODWILL'})
            LuciHelper.saveCouponConfigAndAssertions(self, couponConfigReq=couponConfigObj)
            couponCode3 = LuciHelper.issueCouponAndAssertions(self, couponSeriesId)[0]
            couponSearchRequest = {'sort': self.constructObj.sort['DESC'], 'couponSeriesType': self.constructObj.couponSeriesType['GOODWILL']}
            LuciHelper.couponSearchAndAssertion(self, [couponSeriesId], couponSearchRequest, [couponCode3, couponCode2, couponCode1])
        except Exception, luciExp:
            Logger.log('Luci Exception : ' , luciExp)
            luciExp = luciExp.__dict__
            Assertion.constructAssertion(luciExp['errorCode'] == constant.INVALID_INPUT, 'Luci Exception error code Actual: {} and Expected: {}'.format(luciExp['errorCode'], constant.INVALID_INPUT))
            Assertion.constructAssertion(luciExp['errorMsg'] == 'series type and owned by should be same', 'Luci Exception Error Msg Actual : {}'.format(luciExp['errorMsg']))

        # description = "Redemption Filters:Get coupon details by providing redemption date range,org id and user id"

    def test_LUCI_GCD_030(self):
        # Save Coupon Config
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self)

        couponConfigObj.update({'allow_multiple_vouchers_per_user': True, 'do_not_resend_existing_voucher': True,
                                'same_user_multiple_redeem': True, 'multiple_use': True})
        LuciHelper.saveCouponConfigAndAssertions(self,couponConfigObj)

        couponCode1 = LuciHelper.issueCouponAndAssertions(self,couponSeriesId)[0]
        couponCode2 = LuciHelper.issueCouponAndAssertions(self,couponSeriesId)[0]

        LuciHelper.redeemCouponAndAssertions(self, couponSeriesId, couponCode1)
        LuciHelper.redeemCouponAndAssertions(self, couponSeriesId, couponCode1)
        LuciHelper.redeemCouponAndAssertions(self, couponSeriesId, couponCode1)

        time.sleep(2)
        self.billId = Utils.getTime(milliSeconds=True)
        LuciHelper.redeemCouponAndAssertions(self, couponSeriesId, couponCode2)

        # coupon Search and Assertion
        LuciHelper.couponSearchAndAssertion(self, [couponSeriesId],  {'includeRedemptions' : True}, [couponCode1, couponCode2], [3,1])

    # description = "Get coupon details by providing OrderBy expiry date with different expiry days coupon series id and user id"
    def test_LUCI_GCD_031(self):
        # Save Coupon Config
        couponSeriesId1 = LuciHelper.saveCouponConfigAndAssertions(self, couponConfigReq={'expiry_strategy_value' : 2, 'valid_till_date' : Utils.getTime(days=2, milliSeconds=True)})[1]
        couponSeriesId2 = LuciHelper.saveCouponConfigAndAssertions(self, couponConfigReq={'expiry_strategy_value' : 3, 'valid_till_date' : Utils.getTime(days=4, milliSeconds=True)})[1]
        couponSeriesId3 = LuciHelper.saveCouponConfigAndAssertions(self, couponConfigReq={'expiry_strategy_value' : 1, 'valid_till_date' : Utils.getTime(days=1, milliSeconds=True)})[1]


        couponCode1 = LuciHelper.issueCouponAndAssertions(self, couponSeriesId1)[0]
        couponCode2 = LuciHelper.issueCouponAndAssertions(self, couponSeriesId2)[0]
        couponCode3 = LuciHelper.issueCouponAndAssertions(self, couponSeriesId3)[0]

        couponSearchRequest = {'orderBy': self.constructObj.orderBy['EXPIRY_DATE'],'sort' : self.constructObj.sort['DESC']}
        LuciHelper.couponSearchAndAssertion(self, [couponSeriesId1,couponSeriesId2,couponSeriesId3], couponSearchRequest, [couponCode2, couponCode1, couponCode3])

        couponSearchRequest = {'orderBy': self.constructObj.orderBy['EXPIRY_DATE'], 'sort': self.constructObj.sort['ASC']}
        LuciHelper.couponSearchAndAssertion(self, [couponSeriesId1, couponSeriesId2, couponSeriesId3], couponSearchRequest, [couponCode3, couponCode1, couponCode2])

        couponSearchRequest = {'orderBy': self.constructObj.orderBy['EXPIRY_DATE'], 'sort': self.constructObj.sort['ASC'], 'limit': 2}
        LuciHelper.couponSearchAndAssertion(self, [couponSeriesId1, couponSeriesId2, couponSeriesId3], couponSearchRequest, [couponCode3, couponCode1])

    # description = "Get coupon details by providing OrderBy expiry date with different expiry strategy type coupon series id and user id"
    def test_LUCI_GCD_032(self):
        # Save Coupon Config
        couponSeriesId1 = LuciHelper.saveCouponConfigAndAssertions(self, couponConfigReq={'expiry_strategy_value': 5, 'expiry_strategy_type' : 'DAYS' , 'valid_till_date': Utils.getTime(days=5, milliSeconds=True)})[1]
        couponSeriesId2 = LuciHelper.saveCouponConfigAndAssertions(self, couponConfigReq={'expiry_strategy_value': 1, 'expiry_strategy_type' : 'MONTHS' , 'valid_till_date': Utils.getTime(days=30, milliSeconds=True)})[1]
        couponSeriesId3 = LuciHelper.saveCouponConfigAndAssertions(self, couponConfigReq={'expiry_strategy_value': 2, 'expiry_strategy_type': 'MONTHS_END', 'valid_till_date': Utils.getTime(days=40, milliSeconds=True)})[1]
        couponSeriesId4 = LuciHelper.saveCouponConfigAndAssertions(self, couponConfigReq={'expiry_strategy_value': 1, 'expiry_strategy_type' : 'SERIES_EXPIRY' , 'valid_till_date': Utils.getTime(days=3, milliSeconds=True)})[1]

        couponCode1 = LuciHelper.issueCouponAndAssertions(self, couponSeriesId1)[0]
        couponCode2 = LuciHelper.issueCouponAndAssertions(self, couponSeriesId2)[0]
        couponCode3 = LuciHelper.issueCouponAndAssertions(self, couponSeriesId3)[0]
        couponCode4 = LuciHelper.issueCouponAndAssertions(self, couponSeriesId4)[0]

        couponSearchRequest = {'orderBy': self.constructObj.orderBy['EXPIRY_DATE'], 'sort': self.constructObj.sort['DESC']}
        LuciHelper.couponSearchAndAssertion(self, [couponSeriesId1, couponSeriesId2, couponSeriesId3, couponSeriesId4], couponSearchRequest, [couponCode3, couponCode2, couponCode1, couponCode4])

        couponSearchRequest = {'orderBy': self.constructObj.orderBy['EXPIRY_DATE'], 'sort': self.constructObj.sort['ASC']}
        LuciHelper.couponSearchAndAssertion(self, [couponSeriesId1, couponSeriesId2, couponSeriesId3, couponSeriesId4], couponSearchRequest, [couponCode4, couponCode1, couponCode2, couponCode3])

    # description = "Get coupon details by providing OrderBy expiry date with different valid_days_from_create and valid till coupon series id and user id"
    def test_LUCI_GCD_033(self):
        # Save Coupon Config
        couponSeriesId1 = LuciHelper.saveCouponConfigAndAssertions(self, couponConfigReq={'valid_days_from_create': 5, 'valid_till_date': Utils.getTime(days=10, milliSeconds=True)})[1]
        couponSeriesId2 = LuciHelper.saveCouponConfigAndAssertions(self, couponConfigReq={'valid_days_from_create': 6, 'valid_till_date': Utils.getTime(days=10, milliSeconds=True)})[1]
        couponSeriesId3 = LuciHelper.saveCouponConfigAndAssertions(self, couponConfigReq={'valid_days_from_create': 2, 'valid_till_date': Utils.getTime(days=10, milliSeconds=True)})[1]

        couponCode1 = LuciHelper.issueCouponAndAssertions(self, couponSeriesId1)[0]
        couponCode2 = LuciHelper.issueCouponAndAssertions(self, couponSeriesId2)[0]
        couponCode3 = LuciHelper.issueCouponAndAssertions(self, couponSeriesId3)[0]

        couponSearchRequest = {'orderBy': self.constructObj.orderBy['EXPIRY_DATE'], 'sort': self.constructObj.sort['DESC']}
        LuciHelper.couponSearchAndAssertion(self, [couponSeriesId1, couponSeriesId2, couponSeriesId3], couponSearchRequest, [couponCode2, couponCode1, couponCode3])

        couponSearchRequest = {'orderBy': self.constructObj.orderBy['EXPIRY_DATE'], 'sort': self.constructObj.sort['ASC']}
        LuciHelper.couponSearchAndAssertion(self, [couponSeriesId1, couponSeriesId2, couponSeriesId3], couponSearchRequest, [couponCode3, couponCode1, couponCode2])

    # description = "Get coupon details by providing OrderBy expiry date with different valid_days_from_create and valid till coupon series id and user id"
    def test_LUCI_GCD_034(self):
        # Save Coupon Config
        couponSeriesId1 = LuciHelper.saveCouponConfigAndAssertions(self, couponConfigReq={'valid_days_from_create': 10, 'valid_till_date': Utils.getTime(days=5, milliSeconds=True)})[1]
        couponSeriesId2 = LuciHelper.saveCouponConfigAndAssertions(self, couponConfigReq={'valid_days_from_create': 10, 'valid_till_date': Utils.getTime(days=6, milliSeconds=True)})[1]
        couponSeriesId3 = LuciHelper.saveCouponConfigAndAssertions(self, couponConfigReq={'valid_days_from_create': 10, 'valid_till_date': Utils.getTime(days=2, milliSeconds=True)})[1]

        couponCode1 = LuciHelper.issueCouponAndAssertions(self, couponSeriesId1)[0]
        couponCode2 = LuciHelper.issueCouponAndAssertions(self, couponSeriesId2)[0]
        couponCode3 = LuciHelper.issueCouponAndAssertions(self, couponSeriesId3)[0]

        couponSearchRequest = {'orderBy': self.constructObj.orderBy['EXPIRY_DATE'], 'sort': self.constructObj.sort['DESC']}
        LuciHelper.couponSearchAndAssertion(self, [couponSeriesId1, couponSeriesId2, couponSeriesId3], couponSearchRequest, [couponCode2, couponCode1, couponCode3])

        couponSearchRequest = {'orderBy': self.constructObj.orderBy['EXPIRY_DATE'], 'sort': self.constructObj.sort['ASC']}
        LuciHelper.couponSearchAndAssertion(self, [couponSeriesId1, couponSeriesId2, couponSeriesId3], couponSearchRequest, [couponCode3, couponCode1, couponCode2])

    # description = "Get coupon details by providing OrderBy expiry date after the coupons redeemed coupon series id and user id"
    def test_LUCI_GCD_035(self):
        # Save Coupon Config
        couponSeriesId1 = LuciHelper.saveCouponConfigAndAssertions(self, couponConfigReq={'expiry_strategy_value' : 2, 'valid_till_date' : Utils.getTime(days=2, milliSeconds=True)})[1]
        couponSeriesId2 = LuciHelper.saveCouponConfigAndAssertions(self, couponConfigReq={'expiry_strategy_value' : 3, 'valid_till_date' : Utils.getTime(days=4, milliSeconds=True)})[1]
        couponSeriesId3 = LuciHelper.saveCouponConfigAndAssertions(self, couponConfigReq={'expiry_strategy_value' : 1, 'valid_till_date' : Utils.getTime(days=1, milliSeconds=True)})[1]


        couponCode1 = LuciHelper.issueCouponAndAssertions(self, couponSeriesId1)[0]
        couponCode2 = LuciHelper.issueCouponAndAssertions(self, couponSeriesId2)[0]
        couponCode3 = LuciHelper.issueCouponAndAssertions(self, couponSeriesId3)[0]

        LuciHelper.redeemCouponAndAssertions(self, couponSeriesId1, couponCode1)
        LuciHelper.redeemCouponAndAssertions(self, couponSeriesId2, couponCode2)
        LuciHelper.redeemCouponAndAssertions(self, couponSeriesId3, couponCode3)

        couponSearchRequest = {'orderBy': self.constructObj.orderBy['EXPIRY_DATE'], 'sort' : self.constructObj.sort['DESC'], 'includeRedemptions' : True}
        LuciHelper.couponSearchAndAssertion(self, [couponSeriesId1,couponSeriesId2,couponSeriesId3], couponSearchRequest, [couponCode2, couponCode1, couponCode3], [1,1,1])

        couponSearchRequest = {'orderBy': self.constructObj.orderBy['EXPIRY_DATE'], 'sort': self.constructObj.sort['ASC'], 'includeRedemptions' : True}
        LuciHelper.couponSearchAndAssertion(self, [couponSeriesId1, couponSeriesId2, couponSeriesId3], couponSearchRequest, [couponCode3, couponCode1, couponCode2], [1,1,1])

    # description = "Get coupon details by providing OrderBy expiry date search more than one userIds"
    def test_LUCI_GCD_036(self):
        try:
            # Save Coupon Config
            couponSeriesId1 = LuciHelper.saveCouponConfigAndAssertions(self, couponConfigReq={'expiry_strategy_value': 2, 'valid_till_date': Utils.getTime(days=2, milliSeconds=True)})[1]
            couponSeriesId2 = LuciHelper.saveCouponConfigAndAssertions(self, couponConfigReq={'expiry_strategy_value': 3, 'valid_till_date': Utils.getTime(days=4, milliSeconds=True)})[1]

            customerIds = [self.userId]
            couponCode1 = LuciHelper.issueCouponAndAssertions(self, couponSeriesId1)[0]
            self.userId = constant.config['usersInfo'][1]['userId']
            customerIds.append(self.userId)
            couponCode2 = LuciHelper.issueCouponAndAssertions(self, couponSeriesId2)[0]

            couponSearchRequest = {'orderBy': self.constructObj.orderBy['EXPIRY_DATE'], 'customerIds': customerIds}
            LuciHelper.couponSearchAndAssertion(self, [couponSeriesId1, couponSeriesId2], couponSearchRequest, [couponCode2, couponCode1])
        except Exception, exp:
            LuciException = exp.__dict__
            Assertion.constructAssertion(LuciException['errorCode'] == 807, 'Invalid Customers list Error Code Actual : {} and Expected : {}'.format(LuciException['errorCode'],807))
            Assertion.constructAssertion(LuciException['errorMsg'] == 'only one customer id should be mentioned in the customer id list', 'Invalid Customers list Error Message Actual : {}'.format(LuciException['errorMsg']))
        finally:
            self.userId = constant.config['usersInfo'][0]['userId']

    # description = "Get coupon details by providing OrderBy expiry date with offsets and limits coupon series id and user id"
    def test_LUCI_GCD_037(self):
        # Save Coupon Config
        couponSeriesId1 = LuciHelper.saveCouponConfigAndAssertions(self, couponConfigReq={'expiry_strategy_value' : 3, 'valid_till_date' : Utils.getTime(days=2, milliSeconds=True)})[1]
        couponSeriesId2 = LuciHelper.saveCouponConfigAndAssertions(self, couponConfigReq={'expiry_strategy_value' : 4, 'valid_till_date' : Utils.getTime(days=4, milliSeconds=True)})[1]
        couponSeriesId3 = LuciHelper.saveCouponConfigAndAssertions(self, couponConfigReq={'expiry_strategy_value' : 2, 'valid_till_date' : Utils.getTime(days=3, milliSeconds=True)})[1]
        couponSeriesId4 = LuciHelper.saveCouponConfigAndAssertions(self, couponConfigReq={'expiry_strategy_value' : 1, 'valid_till_date' : Utils.getTime(days=1, milliSeconds=True)})[1]


        couponCode1 = LuciHelper.issueCouponAndAssertions(self, couponSeriesId1)[0]
        couponCode2 = LuciHelper.issueCouponAndAssertions(self, couponSeriesId2)[0]
        couponCode3 = LuciHelper.issueCouponAndAssertions(self, couponSeriesId3)[0]
        couponCode4 = LuciHelper.issueCouponAndAssertions(self, couponSeriesId4)[0]

        couponSearchRequest = {'offset' : 1, 'orderBy': self.constructObj.orderBy['EXPIRY_DATE'], 'sort': self.constructObj.sort['ASC'], 'limit': 2}
        LuciHelper.couponSearchAndAssertion(self, [couponSeriesId1, couponSeriesId2, couponSeriesId3,couponSeriesId4], couponSearchRequest, [couponCode1, couponCode3])

        couponSearchRequest = {'offset': 2, 'orderBy': self.constructObj.orderBy['EXPIRY_DATE'], 'sort': self.constructObj.sort['ASC'], 'limit': 2}
        LuciHelper.couponSearchAndAssertion(self, [couponSeriesId1, couponSeriesId2, couponSeriesId3,couponSeriesId4], couponSearchRequest, [couponCode3, couponCode2])

    @pytest.mark.parametrize('description', ['Redeem store id -1 and apply filter couponSearch'])
    def test_LUCI_GCD_038_sanity_smoke(self,description):
        # Save Coupon Config
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self)

        couponCode = LuciHelper.issueCouponAndAssertions(self,couponSeriesId)[0]
        # Added Issue Filter
        issualFilterObj = LuciObject.issualFilters({'redeemableAtStoreId': [self.storeId]})
        issualFilterObj = {'issualFilters': issualFilterObj}
        #coupon Search and Assertion
        LuciHelper.couponSearchAndAssertion(self, [couponSeriesId], issualFilterObj, [couponCode])