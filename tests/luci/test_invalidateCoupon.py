import time,pytest, random
from src.Constant.constant import constant
from src.utilities.logger import Logger
from src.utilities.assertion import Assertion
from src.utilities.utils import Utils
from src.utilities.randValues import randValues
from src.modules.luci.luciHelper import LuciHelper
from src.modules.luci.luciObject import LuciObject
from src.modules.luci.luciDBHelper import LuciDBHelper
from src.modules.luci.dracarysHelper import DracarysHelper
from src.modules.luci.dracarysObject import DracarysObject

class Test_InvalidateCoupon():

    def setup_class(self):
        Logger.logSuiteName(str(self).split('.')[-1])
        self.constructObj = LuciObject()
        self.DracarysObj = DracarysObject()
        self.userId = constant.config['usersInfo'][0]['userId']
        self.tillId = constant.config['tillIds'][0]
        self.userIds = list()
        self.billId = Utils.getTime(milliSeconds=True)

    def setup_method(self, method):
        self.connObj = LuciHelper.getConnObj(newConnection=True)
        self.DracraysConnObj = DracarysHelper.getConnObj(newConnection=True)
        Logger.logMethodName(method.__name__)
        self.userId = constant.config['usersInfo'][0]['userId']
        constant.config['uploadedFileName'] = method.__name__
        constant.config['requestId'] = 'luci_auto_'+str(random.randint(11111, 99999))      

    @pytest.mark.parametrize('description',[('Revoke_CouponSeries')])
    def test_LUCI_RVC_001(self,description):
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self)
        LuciHelper.queuePumpWait(self,couponSeriesId)
        # Issue Coupon Code
        LuciHelper.issueCouponAndAssertions(self,couponSeriesId)
        LuciHelper.invalidateCouponAndAssertions(self,couponSeriesId)

    @pytest.mark.parametrize('description',[('Redeem_revoked_couponCode')])
    def test_LUCI_RVC_002(self,description):
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self)
        LuciHelper.queuePumpWait(self,couponSeriesId)
        # Issue Coupon Code
        couponCode = LuciHelper.issueCouponAndAssertions(self,couponSeriesId)[0]
        LuciHelper.invalidateCouponAndAssertions(self,couponSeriesId)
        LuciHelper.redeemCouponAndAssertions(self, couponSeriesId, couponCode, error=[633,'invalid coupon code'])

    @pytest.mark.parametrize('description',[('Revoke_CouponSeries_&_Upload_CouponCode')])
    def test_LUCI_RVC_003_sanity(self,description):
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self)
        LuciHelper.queuePumpWait(self,couponSeriesId)
        # Issue Coupon Code
        LuciHelper.issueCouponAndAssertions(self,couponSeriesId)
        LuciHelper.invalidateCouponAndAssertions(self,couponSeriesId)
        LuciHelper.uploadCouponAndAssertions(self, couponSeriesId, self.constructObj.importType['MOBILE'],constant.config['usersInfo'][0]['mobile'],dracraysUpload={'userOnly' : True})

    @pytest.mark.parametrize('description', [('Revoke_CouponSeries_&_Search_CouponCode')])
    def test_LUCI_RVC_004(self, description):
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self)
        LuciHelper.queuePumpWait(self,couponSeriesId)
        # Issue Coupon Code
        LuciHelper.issueCouponAndAssertions(self, couponSeriesId)
        LuciHelper.invalidateCouponAndAssertions(self,couponSeriesId)
        LuciHelper.couponSearchAndAssertion(self, [couponSeriesId])

    @pytest.mark.parametrize('description', [('Revoke_Issued_CouponCode')])
    def test_LUCI_RVC_005(self, description):
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self)
        LuciHelper.queuePumpWait(self,couponSeriesId)
        # Issue Coupon Code
        couponCode = LuciHelper.issueCouponAndAssertions(self, couponSeriesId)[0]
        LuciHelper.invalidateCouponAndAssertions(self,couponSeriesId,couponCode=couponCode,couponSeriesInfo=[False])

    @pytest.mark.parametrize('description', [('Revoke_Issued_CouponCode_&_Redeem_CouponCode')])
    def test_LUCI_RVC_006(self, description):
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self)
        LuciHelper.queuePumpWait(self,couponSeriesId)
        # Issue Coupon Code
        couponCode = LuciHelper.issueCouponAndAssertions(self, couponSeriesId)[0]
        LuciHelper.invalidateCouponAndAssertions(self,couponSeriesId, couponCode=couponCode, couponSeriesInfo=[False])
        LuciHelper.redeemCouponAndAssertions(self, couponSeriesId, couponCode,  error=[633, 'invalid coupon code'])

    @pytest.mark.parametrize('description', [('Upload_&_Issue_DCP_and_Revoke_CouponCode')])
    def test_LUCI_RVC_007(self, description):
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self,{'client_handling_type' : 'DISC_CODE_PIN'})
        couponCode = LuciHelper.uploadCouponAndAssertions(self,couponSeriesId,self.constructObj.importType['NONE'])['coupons'][0]
        # Issue Coupon Code
        LuciHelper.issueCouponAndAssertions(self, couponSeriesId)
        LuciHelper.invalidateCouponAndAssertions(self,couponSeriesId, couponCode=couponCode, couponSeriesInfo=[False,True])

    @pytest.mark.parametrize('description', [('Upload_&_Issue_DCP_and_Revoke_CouponSeries')])
    def test_LUCI_RVC_008(self, description):
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self,{'client_handling_type' : 'DISC_CODE_PIN'})
        LuciHelper.uploadCouponAndAssertions(self,couponSeriesId,self.constructObj.importType['NONE'], noOfCouponsToBeUpload=10)
        # Issue Coupon Code
        LuciHelper.issueCouponAndAssertions(self, couponSeriesId)
        LuciHelper.invalidateCouponAndAssertions(self,couponSeriesId, couponSeriesInfo=[True])

    @pytest.mark.parametrize('description', [('Revoke_issued_DCP_and_Upload_&_issue_new_CouponCode')])
    def test_LUCI_RVC_009_sanity_smoke(self, description):
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self,{'client_handling_type' : 'DISC_CODE_PIN'})
        LuciHelper.uploadCouponAndAssertions(self,couponSeriesId,self.constructObj.importType['NONE'])
        # Issue Coupon Code
        LuciHelper.issueCouponAndAssertions(self, couponSeriesId)
        LuciHelper.invalidateCouponAndAssertions(self,couponSeriesId, couponSeriesInfo=[True])
        LuciHelper.uploadCouponAndAssertions(self, couponSeriesId, self.constructObj.importType['NONE'])
        LuciHelper.issueCouponAndAssertions(self, couponSeriesId)

    @pytest.mark.parametrize('description', [('Revoke_Generic_CouponSeries')])
    def test_LUCI_RVC_010(self, description):
        couponCode = LuciHelper.generateCouponCode()
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self,{'client_handling_type' : 'GENERIC', 'genericCode' : couponCode})
        userList = []
        for tmpDict in constant.config['usersInfo']:
            userList.append(tmpDict['userId'])

        LuciHelper.issueMultipleCoupon(self,couponSeriesId,userList)
        LuciHelper.invalidateCouponAndAssertions(self,couponSeriesId, numRevoked=len(userList) ,couponSeriesInfo=[True,'GENERIC'])

    @pytest.mark.parametrize('description', [('Revoke_Generic_CouponCode')])
    def test_LUCI_RVC_011(self, description):
        couponCode = LuciHelper.generateCouponCode()
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self,{'client_handling_type' : 'GENERIC', 'genericCode' : couponCode})
        userList = []
        for tmpDict in constant.config['usersInfo']:
            userList.append(tmpDict['userId'])

        LuciHelper.issueMultipleCoupon(self,couponSeriesId,userList)
        LuciHelper.invalidateCouponAndAssertions(self,couponSeriesId, couponCode = couponCode ,couponSeriesInfo=[False, True,'GENERIC'])

    @pytest.mark.parametrize('description', [('Revoke_Generic_CouponCode_and_Redeem')])
    def test_LUCI_RVC_012(self, description):
        couponCode = LuciHelper.generateCouponCode()
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self,{'client_handling_type' : 'GENERIC', 'genericCode' : couponCode})
        userList = []
        for tmpDict in constant.config['usersInfo']:
            userList.append(tmpDict['userId'])

        LuciHelper.issueMultipleCoupon(self,couponSeriesId,userList)
        LuciHelper.invalidateCouponAndAssertions(self,couponSeriesId, couponCode = couponCode ,couponSeriesInfo=[False, True,'GENERIC'])
        LuciHelper.redeemCouponAndAssertions(self, couponSeriesId, couponCode,  error=[625, 'coupon not issued to this user redemption failed'])

    @pytest.mark.parametrize('description', [('Redeem_revoked_and_Redeem_Same_couponCode')])
    def test_LUCI_RVC_013(self, description):
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self,{'same_user_multiple_redeem' : True,'multiple_use' : True,'any_user' : True})
        LuciHelper.queuePumpWait(self,couponSeriesId)
        # Issue Coupon Code
        couponCode = LuciHelper.issueCouponAndAssertions(self, couponSeriesId)[0]
        LuciHelper.redeemCouponAndAssertions(self, couponSeriesId, couponCode)
        LuciHelper.invalidateCouponAndAssertions(self,couponSeriesId, numRevoked=0, couponCode = couponCode ,couponSeriesInfo=[False])
        LuciHelper.issueCouponAndAssertions(self, couponSeriesId,couponIssuedCount=2)
        LuciHelper.redeemCouponAndAssertions(self, couponSeriesId, couponCode)

    @pytest.mark.parametrize('description', [('Revoke_Invalid_CouponSeries')])
    def test_LUCI_RVC_014(self, description):
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self)
        # Issue Coupon Code
        LuciHelper.issueCouponAndAssertions(self, couponSeriesId)
        invalidateCouponRequest = LuciObject.invalidateCouponRequest({'couponSeriesId': (couponSeriesId + 365)})
        Assertion.constructAssertion(self.connObj.invalidateCoupons(invalidateCouponRequest) == False, 'Revoking Invalid Coupon Series')

    @pytest.mark.parametrize('description', [('Revoked_CouponSeries_and_update_CouponConfig')])
    def test_LUCI_RVC_015(self, description):
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self,{'same_user_multiple_redeem' : True,'multiple_use' : True,'any_user' : True})
        LuciHelper.queuePumpWait(self,couponSeriesId)
        # Issue Coupon Code
        couponCode = LuciHelper.issueCouponAndAssertions(self, couponSeriesId)[0]
        LuciHelper.invalidateCouponAndAssertions(self,couponSeriesId, couponSeriesInfo=[True])
        couponConfigObj.update({'same_user_multiple_redeem' : True,'multiple_use' : True,'any_user' : True})
        LuciHelper.saveCouponConfigAndAssertions(self,couponConfigObj)

    @pytest.mark.parametrize('description', [('Revoke_Issued_CouponCode_&_Issue_new_CouponCode')])
    def test_LUCI_RVC_016(self, description):
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self)
        LuciHelper.queuePumpWait(self,couponSeriesId)
        # Issue Coupon Code
        couponCode = LuciHelper.issueCouponAndAssertions(self, couponSeriesId)[0]
        LuciHelper.redeemCouponAndAssertions(self, couponSeriesId, couponCode)
        LuciHelper.invalidateCouponAndAssertions(self,couponSeriesId, numRevoked= 0, couponCode=couponCode, couponSeriesInfo=[False])
        LuciHelper.issueCouponAndAssertions(self, couponSeriesId, couponIssuedCount=2)

    @pytest.mark.parametrize('description', [('Revoke_Redeemed_CouponSeries')])
    def test_LUCI_RVC_017(self, description):
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self)
        LuciHelper.queuePumpWait(self,couponSeriesId)
        # Issue Coupon Code
        couponCode = LuciHelper.issueCouponAndAssertions(self, couponSeriesId)[0]
        LuciHelper.redeemCouponAndAssertions(self, couponSeriesId, couponCode)
        LuciHelper.invalidateCouponAndAssertions(self,couponSeriesId, numRevoked=0, couponSeriesInfo=[True, 'GENERIC'])

    @pytest.mark.parametrize('description', [('Revoke_Redeemed_CouponSeries_and_issue_new_coupon')])
    def test_LUCI_RVC_018(self,description):
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self)
        LuciHelper.queuePumpWait(self,couponSeriesId)
        # Issue Coupon Code
        couponCode = LuciHelper.issueCouponAndAssertions(self, couponSeriesId)[0]
        LuciHelper.redeemCouponAndAssertions(self, couponSeriesId, couponCode)
        LuciHelper.invalidateCouponAndAssertions(self,couponSeriesId, numRevoked=0, couponSeriesInfo=[True, 'GENERIC'])
        LuciHelper.issueCouponAndAssertions(self, couponSeriesId, couponIssuedCount=2)

    @pytest.mark.parametrize('description', [('Resend_Revoke_CouponCode')])
    def test_LUCI_RVC_019(self,description):
        try:
            couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self)
            LuciHelper.queuePumpWait(self,couponSeriesId)
            # Issue Coupon Code
            couponCode = LuciHelper.issueCouponAndAssertions(self, couponSeriesId)[0]
            LuciHelper.invalidateCouponAndAssertions(self,couponSeriesId, couponSeriesInfo=[True])
            resendRequest = LuciObject.resendCouponRequest({'storeUnitId': self.tillId, 'eventTimeInMillis': Utils.getTime(milliSeconds=True), 'couponCode': couponCode, 'userId': self.userId})
            self.connObj.resendCoupon(resendRequest)
        except Exception, luciException:
            luciException = luciException.__dict__
            Assertion.constructAssertion(luciException['errorCode'] == 633, 'Redemption error Code Actual : {} and Expected: {}'.format(luciException['errorCode'], 633))
            Assertion.constructAssertion(luciException['errorMsg'] == 'invalid coupon code', 'Redemption error Message Actual : {} and Expected: {}'.format(luciException['errorMsg'], 'invalid coupon code'))

    @pytest.mark.parametrize('description, couponConfig, uploadType, dracarysUploadInput, invalidateRequest', [
        ('Revoke Type coupon series DC', {'client_handling_type': 'DISC_CODE'}, 'USER_ID', {'userOnly' : True},{'revokeType' : 0, 'commit' : True}),
        ('Revoke Type coupon series GENERIC', {'client_handling_type': 'GENERIC'}, 'USER_ID', {'userOnly' : True},{'revokeType' : 0, 'commit' : True}),
        ('Revoke Type coupon series DCP', {'client_handling_type': 'DISC_CODE_PIN'}, 'USER_ID', {},{'revokeType' : 0, 'commit' : True}),
        ('Revoke Type coupon series EXTERNAL', {'client_handling_type' : 'DISC_CODE_PIN' , 'any_user' : True, 'isExternalIssual' : True}, 'NONE', {}, {'revokeType' : 0, 'commit' : True})
    ])
    def test_LUCI_RVC_NF_020(self,description, couponConfig, uploadType, dracarysUploadInput, invalidateRequest):
        if couponConfig['client_handling_type'] == 'GENERIC':
            couponConfig.update({'genericCode' : LuciHelper.generateCouponCode()})
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self, couponConfigReq=couponConfig)
        if couponConfig['client_handling_type'] == 'DISC_CODE':
            LuciHelper.queuePumpWait(self,couponSeriesId)
        time.sleep(2)
        couponCodeList = LuciHelper.uploadCouponAndAssertions(self,couponSeriesId, self.constructObj.importType[uploadType],noOfCouponsToBeUpload=5, dracraysUpload=dracarysUploadInput)['coupons']
        createdCount = LuciDBHelper.getCouponsCreated_Count(couponSeriesId, 1)
        LuciHelper.revokeCoupon(self,couponSeriesId,couponCodeList,revokeType=invalidateRequest['revokeType'], reqDict=invalidateRequest)
        Assertion.constructAssertion(LuciDBHelper.getCouponsIssued_Count(couponSeriesId, 1) == 0, 'All Coupons Marked as invalid in issued table')
        Assertion.constructAssertion(LuciDBHelper.getCouponsCreated_Count(couponSeriesId, 0) == createdCount, 'All Coupons Marked as invalid in created table')
        if not couponConfigObj['isExternalIssual']:
            LuciHelper.getCouponConfigAndAssertion(self,couponSeriesId,0,0)


    @pytest.mark.parametrize('description, couponConfig, uploadType, dracarysUploadInput, invalidateRequest', [
        ('Revoke Type only unissued DC', {'client_handling_type': 'DISC_CODE'}, 'USER_ID', {'userOnly' : True},{'revokeType' : 1, 'commit' : True, 'reuse' : True}),
    ])
    def test_LUCI_RVC_NF_021(self,description, couponConfig, uploadType, dracarysUploadInput, invalidateRequest):
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self, couponConfigReq=couponConfig)
        LuciHelper.queuePumpWait(self,couponSeriesId)
        couponCodeList = LuciHelper.uploadCouponAndAssertions(self,couponSeriesId, self.constructObj.importType[uploadType],noOfCouponsToBeUpload=5, dracraysUpload=dracarysUploadInput)['coupons']
        createdCount = LuciDBHelper.getCouponsCreated_Count(couponSeriesId, 1)
        LuciHelper.revokeCoupon(self,couponSeriesId,couponCodeList,revokeType=invalidateRequest['revokeType'], reqDict=invalidateRequest)
        Assertion.constructAssertion(LuciDBHelper.getCouponsIssued_Count(couponSeriesId, 0) == 0, 'All Coupons Marked as invalid in issued table')
        Assertion.constructAssertion(LuciDBHelper.getCouponsCreated_Count(couponSeriesId, 0) == (createdCount-5), 'All Coupons Marked as invalid in created table')
        LuciHelper.getCouponConfigAndAssertion(self,couponSeriesId,5,0)


    @pytest.mark.parametrize('description, couponConfig, invalidateRequest', [
        ('Revoke Type only unissued DC', {'client_handling_type': 'DISC_CODE'}, {'revokeType' : 1, 'commit' : True, 'reuse' : True}),
        ('Revoke Type only unissued -DCP', {'client_handling_type': 'DISC_CODE_PIN'},{'revokeType': 1, 'commit': True, 'reuse': True})
    ])
    def test_LUCI_RVC_NF_022(self,description, couponConfig, invalidateRequest):
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self, couponConfigReq=couponConfig)
        couponCodeList = []
        if couponConfig['client_handling_type'] == 'DISC_CODE':
            LuciHelper.queuePumpWait(self, couponSeriesId)
        else:
            couponCodeList = LuciHelper.uploadCouponAndAssertions(self,couponSeriesId, self.constructObj.importType['NONE'],noOfCouponsToBeUpload=10, dracraysUpload={})['coupons']
        createdCount = LuciDBHelper.getCouponsCreated_Count(couponSeriesId, 1)
        LuciHelper.issueCouponAndAssertions(self, couponSeriesId)
        issuedCount = LuciDBHelper.getCouponsIssued_Count(couponSeriesId, 1)
        LuciHelper.revokeCoupon(self,couponSeriesId,couponCodeList,revokeType=invalidateRequest['revokeType'], reqDict=invalidateRequest)
        Assertion.constructAssertion(LuciDBHelper.getCouponsIssued_Count(couponSeriesId, 0) == 0, 'All Coupons Marked as invalid in issued table')
        Assertion.constructAssertion(LuciDBHelper.getCouponsCreated_Count(couponSeriesId, 0) == (createdCount- issuedCount), 'All Coupons Marked as invalid in created table')
        LuciHelper.getCouponConfigAndAssertion(self,couponSeriesId,1,0)

    @pytest.mark.parametrize('description, couponConfig, uploadType, dracarysUploadInput, invalidateRequest', [
        ('Revoke Type only unissued -DCP', {'client_handling_type': 'DISC_CODE_PIN'}, 'USER_ID', {}, {'revokeType': 1, 'commit': True, 'reuse': True})
    ])
    def test_LUCI_RVC_NF_023(self, description, couponConfig, uploadType, dracarysUploadInput, invalidateRequest):
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self, couponConfigReq=couponConfig)
        couponCodeList = LuciHelper.uploadCouponAndAssertions(self, couponSeriesId, self.constructObj.importType[uploadType], noOfCouponsToBeUpload=5, dracraysUpload=dracarysUploadInput)['coupons']
        LuciHelper.revokeCoupon(self, couponSeriesId, couponCodeList, revokeType=invalidateRequest['revokeType'], reqDict=invalidateRequest)
        Assertion.constructAssertion(LuciDBHelper.getCouponsIssued_Count(couponSeriesId, 0) == 0, 'No invalid issued coupons')
        Assertion.constructAssertion(LuciDBHelper.getCouponsCreated_Count(couponSeriesId, 0) == 0, 'Unissued Coupons are Marked as invalid in created table')
        LuciHelper.getCouponConfigAndAssertion(self, couponSeriesId, 5, 0)

    @pytest.mark.parametrize('description, couponConfig, invalidateRequest,isS3Support', [
        ('Revoke Type userId -DC', {'client_handling_type': 'DISC_CODE'}, {'revokeType' : 2, 'commit' : True}, False),
        ('Revoke Type userId -DCP', {'client_handling_type': 'DISC_CODE_PIN'}, {'revokeType': 2, 'commit': True}, False),
        ('Revoke Type userId -GENERIC', {'client_handling_type': 'GENERIC'}, {'revokeType' : 2, 'commit' : True}, False),
        ('s3File Support Revoke Type userId -DC', {'client_handling_type': 'DISC_CODE'}, {'revokeType': 2, 'commit': True}, True),
        ('s3File Support Revoke Type userId -DCP', {'client_handling_type': 'DISC_CODE_PIN'}, {'revokeType': 2, 'commit': True}, True),
        ('s3File Support Revoke Type userId -GENERIC', {'client_handling_type': 'GENERIC'}, {'revokeType': 2, 'commit': True}, True),
    ])
    def test_LUCI_RVC_NF_024(self,description, couponConfig, invalidateRequest,isS3Support):
        userIds = list()
        for i in range(5):
            userIds.append(constant.config['usersInfo'][i]['userId'])
        invalidateCouponDetails = []
        if couponConfig['client_handling_type'] == 'GENERIC':
            couponConfig.update({'genericCode' : LuciHelper.generateCouponCode()})
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self, couponConfigReq=couponConfig)
        if couponConfigObj['client_handling_type'] == 'DISC_CODE':
            LuciHelper.queuePumpWait(self,couponSeriesId)
        elif couponConfigObj['client_handling_type'] == 'DISC_CODE_PIN':
            LuciHelper.uploadCouponAndAssertions(self,couponSeriesId, self.constructObj.importType['NONE'],noOfCouponsToBeUpload=10, dracraysUpload={})
        issuedCouponDetails = LuciHelper.issueMultipleCoupon(self,couponSeriesId, userIds)
        for couponDetails in issuedCouponDetails:
            couponDetails = couponDetails.__dict__
            invalidateCouponDetails.append(couponDetails['issuedToUserId'])
        issuedCount = LuciDBHelper.getCouponsIssued_Count(couponSeriesId, 1)
        if isS3Support:
            invalidateRequest.update(LuciHelper.revokes3FileAndRequestObject(self,couponSeriesId, map(str,invalidateCouponDetails), invalidateRequest['revokeType']))
        LuciHelper.revokeCoupon(self,couponSeriesId,invalidateCouponDetails if not isS3Support else [],revokeType=invalidateRequest['revokeType'], reqDict=invalidateRequest)
        Assertion.constructAssertion(LuciDBHelper.getCouponsIssued_Count(couponSeriesId, 1) == 0, 'All Coupons Marked as invalid in issued table')
        if couponConfigObj['client_handling_type'] != 'GENERIC':
            Assertion.constructAssertion(LuciDBHelper.getCouponsCreated_Count(couponSeriesId, 0) == issuedCount, 'All Coupons Marked as invalid in created table')
        LuciHelper.getCouponConfigAndAssertion(self,couponSeriesId,0,0)


    @pytest.mark.parametrize('description, couponConfig, uploadType, dracarysUploadInput, invalidateRequest,isS3Support', [
        ('Revoke Type Coupon code -DC', {'client_handling_type': 'DISC_CODE'}, 'USER_ID', {'userOnly' : True}, {'revokeType' : 3, 'commit' : True, 'reuse' : True},False),
        ('Revoke Type Coupon code -DCP', {'client_handling_type': 'DISC_CODE_PIN'}, 'USER_ID', {}, {'revokeType': 3, 'commit': True, 'reuse' : True},False),
        ('Revoke Type Coupon code -EXTERNAL', {'client_handling_type' : 'DISC_CODE_PIN' , 'any_user' : True, 'isExternalIssual' : True}, 'NONE', {}, {'revokeType': 3, 'commit': True, 'reuse' : True},False),
        ('s3File Support Revoke Type Coupon code -DC', {'client_handling_type': 'DISC_CODE'}, 'USER_ID', {'userOnly': True}, {'revokeType': 3, 'commit': True, 'reuse': True}, True),
        ('s3File Support Revoke Type Coupon code -DCP', {'client_handling_type': 'DISC_CODE_PIN'}, 'USER_ID', {}, {'revokeType': 3, 'commit': True, 'reuse': True}, True),
        ('s3File Support Revoke Type Coupon code -EXTERNAL', {'client_handling_type': 'DISC_CODE_PIN', 'any_user': True, 'isExternalIssual': True}, 'NONE', {}, {'revokeType': 3, 'commit': True, 'reuse': True}, True)
    ])
    def test_LUCI_RVC_NF_025(self,description, couponConfig, uploadType, dracarysUploadInput, invalidateRequest,isS3Support):
        if couponConfig['client_handling_type'] == 'GENERIC':
            couponConfig.update({'genericCode' : LuciHelper.generateCouponCode()})
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self, couponConfigReq=couponConfig)
        if couponConfigObj['client_handling_type'] == 'DISC_CODE':
            LuciHelper.queuePumpWait(self,couponSeriesId)

        invalidateCouponDetails = LuciHelper.uploadCouponAndAssertions(self,couponSeriesId, self.constructObj.importType[uploadType],noOfCouponsToBeUpload=10, dracraysUpload=dracarysUploadInput)['coupons']
        issuedCount = LuciDBHelper.getCouponsIssued_Count(couponSeriesId, 1)
        if isS3Support:
            invalidateRequest.update(LuciHelper.revokes3FileAndRequestObject(self,couponSeriesId, invalidateCouponDetails, invalidateRequest['revokeType']))
        LuciHelper.revokeCoupon(self,couponSeriesId,invalidateCouponDetails if not isS3Support else [],revokeType=invalidateRequest['revokeType'], reqDict=invalidateRequest)
        Assertion.constructAssertion(LuciDBHelper.getCouponsIssued_Count(couponSeriesId, 1) == 0, 'All Coupons Marked as invalid in issued table')
        if couponConfigObj['client_handling_type'] == 'DISC_CODE':
            Assertion.constructAssertion(LuciDBHelper.getCouponsCreated_Count(couponSeriesId, 0) == issuedCount, 'All Coupons Marked as invalid in created table')
        else:
            Assertion.constructAssertion(LuciDBHelper.getCouponsCreated_Count(couponSeriesId, 0) == 0, 'All Coupons Marked as invalid in created table')
        if not couponConfigObj['isExternalIssual']:
            LuciHelper.getCouponConfigAndAssertion(self,couponSeriesId,0,0)

    @pytest.mark.parametrize('description, couponConfig, uploadType, dracarysUploadInput, invalidateRequest,isS3Support', [
        ('Revoke Type CouponId -DC', {'client_handling_type': 'DISC_CODE'},'NONE', {}, {'revokeType' : 4, 'commit' : True, 'reuse' : True}, False),
        ('Revoke Type CouponId -DCP', {'client_handling_type': 'DISC_CODE_PIN'},'NONE', {}, {'revokeType': 4, 'commit': True, 'reuse' : True}, False),
        ('Revoke Type CouponId -GENERIC', {'client_handling_type': 'GENERIC'},'NONE', {}, {'revokeType' : 4, 'commit' : True, 'reuse' : True}, False),
        ('Revoke Type CouponId -EXTERNAL', {'client_handling_type' : 'DISC_CODE_PIN' , 'any_user' : True, 'isExternalIssual' : True}, 'NONE', {}, {'revokeType': 4, 'commit': True, 'reuse': True}, False),
        ('s3File Support Revoke Type CouponId -DC', {'client_handling_type': 'DISC_CODE'}, 'NONE', {}, {'revokeType': 4, 'commit': True, 'reuse': True}, True),
        ('s3File Support Revoke Type CouponId -DCP', {'client_handling_type': 'DISC_CODE_PIN'}, 'NONE', {}, {'revokeType': 4, 'commit': True, 'reuse': True}, True),
        ('s3File Support Revoke Type CouponId -GENERIC', {'client_handling_type': 'GENERIC'}, 'NONE', {}, {'revokeType': 4, 'commit': True, 'reuse': True}, True),
        ('s3File Support Revoke Type CouponId -EXTERNAL', {'client_handling_type': 'DISC_CODE_PIN', 'any_user': True, 'isExternalIssual': True}, 'NONE', {}, {'revokeType': 4, 'commit': True, 'reuse': True}, True)
    ])
    def test_LUCI_RVC_NF_026(self,description, couponConfig, uploadType, dracarysUploadInput, invalidateRequest,isS3Support):
        userIds = list()
        for i in range(5):
            userIds.append(constant.config['usersInfo'][i]['userId'])
        invalidateCouponDetails = []
        if couponConfig['client_handling_type'] == 'GENERIC':
            couponConfig.update({'genericCode' : LuciHelper.generateCouponCode(size=10)})
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self, couponConfigReq=couponConfig)
        if couponConfigObj['client_handling_type'] == 'DISC_CODE':
            LuciHelper.queuePumpWait(self,couponSeriesId)
        elif couponConfigObj['client_handling_type'] in ['DISC_CODE_PIN'] or couponConfigObj['isExternalIssual']:
            LuciHelper.uploadCouponAndAssertions(self,couponSeriesId, self.constructObj.importType[uploadType],noOfCouponsToBeUpload=10, dracraysUpload=dracarysUploadInput)
        if not couponConfigObj['isExternalIssual']:
            LuciHelper.issueMultipleCoupon(self,couponSeriesId,userIds)
        couponIssuedIdDict = LuciDBHelper.getCouponsIssuedList(couponSeriesId)
        for couponIssuedId in couponIssuedIdDict:
            invalidateCouponDetails.append(couponIssuedId['id'])
        if isS3Support:
            invalidateRequest.update(LuciHelper.revokes3FileAndRequestObject(self,couponSeriesId, map(str,invalidateCouponDetails), invalidateRequest['revokeType']))
        issuedCount = LuciDBHelper.getCouponsIssued_Count(couponSeriesId, 1)
        LuciHelper.revokeCoupon(self,couponSeriesId,invalidateCouponDetails if not isS3Support else [],revokeType=invalidateRequest['revokeType'], reqDict=invalidateRequest)
        Assertion.constructAssertion(LuciDBHelper.getCouponsIssued_Count(couponSeriesId, 1) == 0, 'All Coupons Marked as invalid in issued table')
        if couponConfigObj['client_handling_type'] not in ['GENERIC'] and not couponConfigObj['isExternalIssual']:
            Assertion.constructAssertion(LuciDBHelper.getCouponsCreated_Count(couponSeriesId, 0) == issuedCount, 'All Coupons Marked as invalid in created table')
        if not couponConfigObj['isExternalIssual']:
            LuciHelper.getCouponConfigAndAssertion(self,couponSeriesId,0,0)

    @pytest.mark.parametrize('description, couponConfig, uploadType, dracarysUploadInput, invalidateRequest,isS3Support', [
        ('Revoke Type Coupon and userId -DC', {'client_handling_type': 'DISC_CODE'},'NONE', {}, {'revokeType' : 5, 'commit' : True, 'reuse' : True},False),
        ('Revoke Type Coupon and userId -DCP', {'client_handling_type': 'DISC_CODE_PIN'},'NONE', {}, {'revokeType': 5, 'commit': True, 'reuse' : True},False),
        ('s3File Support Revoke Type Coupon and userId -DC', {'client_handling_type': 'DISC_CODE'}, 'NONE', {}, {'revokeType': 5, 'commit': True, 'reuse': True}, True),
        ('s3File Support Revoke Type Coupon and userId -DCP', {'client_handling_type': 'DISC_CODE_PIN'}, 'NONE', {}, {'revokeType': 5, 'commit': True, 'reuse': True}, True),
    ])
    def test_LUCI_RVC_NF_027(self,description, couponConfig, uploadType, dracarysUploadInput, invalidateRequest,isS3Support):
        userIds = list()
        for i in range(5):
            userIds.append(constant.config['usersInfo'][i]['userId'])
        invalidateCouponDetails = []
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self, couponConfigReq=couponConfig)
        if couponConfig['client_handling_type'] == 'DISC_CODE':
            LuciHelper.queuePumpWait(self,couponSeriesId)
        elif couponConfig['client_handling_type'] in ['DISC_CODE_PIN'] or couponConfig['isExternalIssual']:
            LuciHelper.uploadCouponAndAssertions(self,couponSeriesId, self.constructObj.importType[uploadType],noOfCouponsToBeUpload=10, dracraysUpload=dracarysUploadInput)
        LuciHelper.issueMultipleCoupon(self,couponSeriesId,userIds)
        couponIssuedIdDict = LuciDBHelper.getCouponsIssuedList(couponSeriesId)

        for couponIssuedId in couponIssuedIdDict:
            invalidateCouponDetails.append([couponIssuedId['couponCode'], couponIssuedId['issuedTo']] if not isS3Support else couponIssuedId['couponCode'] +','+ str(couponIssuedId['issuedTo']))
        if isS3Support:
            invalidateRequest.update(LuciHelper.revokes3FileAndRequestObject(self,couponSeriesId, invalidateCouponDetails, invalidateRequest['revokeType']))
        LuciHelper.revokeCoupon(self,couponSeriesId,invalidateCouponDetails if not isS3Support else [],revokeType=invalidateRequest['revokeType'], reqDict=invalidateRequest)
        Assertion.constructAssertion(LuciDBHelper.getCouponsIssued_Count(couponSeriesId, 1) == 0, 'All Coupons Marked as invalid in issued table')


    @pytest.mark.parametrize('description, couponConfig, uploadType, dracarysUploadInput, invalidateRequest', [
        ('Revoke Type coupon series DC', {'client_handling_type': 'DISC_CODE'}, 'USER_ID', {'userOnly' : True},{'revokeType' : 0, 'commit' : True})
    ])
    def test_LUCI_RVC_NF_028(self,description, couponConfig, uploadType, dracarysUploadInput, invalidateRequest):
        userIds = []
        for i in range(10):
            userIds.append(constant.config['usersInfo'][i]['userId'])
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self, couponConfigReq=couponConfig)
        LuciHelper.queuePumpWait(self,couponSeriesId)
        couponCodeList = LuciHelper.uploadCouponAndAssertions(self,couponSeriesId, self.constructObj.importType[uploadType],noOfCouponsToBeUpload=10, dracraysUpload=dracarysUploadInput)['coupons']
        for couponCode, userId in zip(couponCodeList, userIds):
            self.userId = userId
            LuciHelper.redeemCouponAndAssertions(self,couponSeriesId,couponCode)
        LuciHelper.revokeCoupon(self,couponSeriesId,couponCodeList,revokeType=invalidateRequest['revokeType'], reqDict=invalidateRequest)
        Assertion.constructAssertion(LuciDBHelper.getCouponsIssued_Count(couponSeriesId, 1) == 10, 'All Coupons Marked as invalid in issued table')
        revokeHistoryObj = LuciObject.getRevokeHistoryRequest({'couponSeriesId' : couponSeriesId})
        listOfRevoke = self.connObj.getRevokeHistory(revokeHistoryObj)[0].__dict__
        tempDetailsList = LuciDBHelper.getTempTableData(listOfRevoke['tempTableName'])
        Assertion.constructAssertion(len(tempDetailsList) == 10, 'Unrevoked coupon count is Matching Actual: {}'.format(len(tempDetailsList)))
        for tmp in tempDetailsList:
            Assertion.constructAssertion(tmp['errorMsg'] == 'coupon already redeemed', 'Redeemed coupons not revoked Error Message: {}'.format(tmp['errorMsg']))
        LuciHelper.getCouponConfigAndAssertion(self,couponSeriesId,10,10)
        s3OutPut = LuciHelper.downloadFile(self,listOfRevoke['errorFileHandle'])
        for errors in s3OutPut:
            Assertion.constructAssertion(errors['errorMsg'] == 'coupon already redeemed', 'Redeemed coupons not revoked Error Message: {}'.format(errors['errorMsg']))
            Assertion.constructAssertion(errors['couponCode'] in couponCodeList, 'Coupon code is Matched with error report Actual: {} and Expected: {}'.format(errors['couponCode'], couponCodeList))
        LuciHelper.revokeCoupon(self, couponSeriesId, couponCodeList, revokeType=1, reqDict={'revokeType' : 1, 'commit' : True, 'reuse' : True})

    @pytest.mark.parametrize('description, couponConfig, uploadType, dracarysUploadInput, invalidateRequest,isS3Support', [
        ('Invalid Revoke Type customerId DC', {'client_handling_type': 'DISC_CODE_PIN'}, 'NONE', {},{'revokeType' : 2, 'commit' : True},False),
        ('s3File Support Invalid Revoke Type customerId DC', {'client_handling_type': 'DISC_CODE_PIN'}, 'NONE', {},{'revokeType' : 2, 'commit' : True},True)
    ])
    def test_LUCI_RVC_NF_029(self,description, couponConfig, uploadType, dracarysUploadInput, invalidateRequest,isS3Support):
        invalidateCouponDetails = []
        userIds = []
        for i in range(10):
            userIds.append(constant.config['usersInfo'][i]['userId'])
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self, couponConfigReq=couponConfig)
        LuciHelper.uploadCouponAndAssertions(self,couponSeriesId, self.constructObj.importType[uploadType],noOfCouponsToBeUpload=20, dracraysUpload=dracarysUploadInput)
        LuciHelper.issueMultipleCoupon(self, couponSeriesId, userIds)
        couponIssuedIdDict = LuciDBHelper.getCouponsIssuedList(couponSeriesId)
        for couponIssuedId in couponIssuedIdDict:
            invalidateCouponDetails.append(couponIssuedId['id'])
        if isS3Support:
            invalidateRequest.update(LuciHelper.revokes3FileAndRequestObject(self,couponSeriesId, map(str,invalidateCouponDetails), invalidateRequest['revokeType']))
        LuciHelper.revokeCoupon(self,couponSeriesId,invalidateCouponDetails if not isS3Support else [],revokeType=invalidateRequest['revokeType'], reqDict=invalidateRequest)
        Assertion.constructAssertion(LuciDBHelper.getCouponsIssued_Count(couponSeriesId, 1) == 10, 'All Coupons Marked as invalid in issued table')
        revokeHistoryObj = LuciObject.getRevokeHistoryRequest({'couponSeriesId' : couponSeriesId})
        listOfRevoke = self.connObj.getRevokeHistory(revokeHistoryObj)[0].__dict__
        tempDetailsList = LuciDBHelper.getTempTableData(listOfRevoke['tempTableName'])
        Assertion.constructAssertion(len(tempDetailsList) == 10, 'Unrevoked coupon count is Matching Actual: {}'.format(len(tempDetailsList)))
        for tmp in tempDetailsList:
            Assertion.constructAssertion(tmp['errorMsg'] == 'invalid customer id', 'Invalid customerIds sent & coupons not revoked Error Message: {}'.format(tmp['errorMsg']))
        LuciHelper.getCouponConfigAndAssertion(self,couponSeriesId,10,0)
        s3OutPut = LuciHelper.downloadFile(self,listOfRevoke['errorFileHandle'])
        for errors in s3OutPut:
            Assertion.constructAssertion(errors['errorMsg'] == 'invalid customer id', 'Invalid customerIds sent & coupons not revoked Error Message: {}'.format(errors['errorMsg']))
            Assertion.constructAssertion(errors['userId'] in invalidateCouponDetails, 'Invalid userId Id is Matched with error report Actual: {} and Expected: {}'.format(errors['userId'], invalidateCouponDetails))


    @pytest.mark.parametrize('description, couponConfig, uploadType, dracarysUploadInput, invalidateRequest,isS3Support', [
        ('Invalid Revoke Type couponCode DC', {'client_handling_type': 'DISC_CODE_PIN'}, 'NONE', {},{'revokeType' : 3, 'commit' : True},False),
        ('s3File Support Invalid Revoke Type couponCode DC', {'client_handling_type': 'DISC_CODE_PIN'}, 'NONE', {},{'revokeType' : 3, 'commit' : True},True)
    ])
    def test_LUCI_RVC_NF_030(self,description, couponConfig, uploadType, dracarysUploadInput, invalidateRequest,isS3Support):
        invalidateCouponDetails = []
        userIds = []
        for i in range(10):
            userIds.append(constant.config['usersInfo'][i]['userId'])
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self, couponConfigReq=couponConfig)
        LuciHelper.uploadCouponAndAssertions(self,couponSeriesId, self.constructObj.importType[uploadType],noOfCouponsToBeUpload=20, dracraysUpload=dracarysUploadInput)
        LuciHelper.issueMultipleCoupon(self, couponSeriesId, userIds)
        couponIssuedIdDict = LuciDBHelper.getCouponsIssuedList(couponSeriesId)
        for couponIssuedId in couponIssuedIdDict:
            invalidateCouponDetails.append(str(couponIssuedId['id']))
        if isS3Support:
            invalidateRequest.update(LuciHelper.revokes3FileAndRequestObject(self,couponSeriesId, map(str,invalidateCouponDetails), invalidateRequest['revokeType']))
        LuciHelper.revokeCoupon(self,couponSeriesId,invalidateCouponDetails if not isS3Support else [],revokeType=invalidateRequest['revokeType'], reqDict=invalidateRequest)
        Assertion.constructAssertion(LuciDBHelper.getCouponsIssued_Count(couponSeriesId, 1) == 10, 'All Coupons Marked as invalid in issued table')
        revokeHistoryObj = LuciObject.getRevokeHistoryRequest({'couponSeriesId' : couponSeriesId})
        listOfRevoke = self.connObj.getRevokeHistory(revokeHistoryObj)[0].__dict__
        tempDetailsList = LuciDBHelper.getTempTableData(listOfRevoke['tempTableName'])
        Assertion.constructAssertion(len(tempDetailsList) == 10, 'Unrevoked coupon count is Matching Actual: {}'.format(len(tempDetailsList)))
        for tmp in tempDetailsList:
            Assertion.constructAssertion(tmp['errorMsg'] == 'invalid coupon code', 'Invalid coupon Codes sent & coupons not revoked Error Message: {}'.format(tmp['errorMsg']))
        LuciHelper.getCouponConfigAndAssertion(self,couponSeriesId,10,0)
        self.userId = constant.config['usersInfo'][0]['userId']
        s3OutPut = LuciHelper.downloadFile(self,listOfRevoke['errorFileHandle'])
        for errors in s3OutPut:
            Assertion.constructAssertion(errors['errorMsg'] == 'invalid coupon code', 'Invalid coupon Codes sent & coupons not revoked Error Message: {}'.format(errors['errorMsg']))
            Assertion.constructAssertion(errors['couponCode'] in invalidateCouponDetails, 'Invalid Coupon code is Matched with error report Actual: {} and Expected: {}'.format(errors['couponCode'], invalidateCouponDetails))

    @pytest.mark.parametrize('description, couponConfig, uploadType, dracarysUploadInput, invalidateRequest,isS3Support', [
        ('Invalid Revoke Type couponId DC', {'client_handling_type': 'DISC_CODE_PIN'}, 'NONE', {},{'revokeType' : 4, 'commit' : True},False),
        ('s3File Support Invalid Revoke Type couponId DC', {'client_handling_type': 'DISC_CODE_PIN'}, 'NONE', {},{'revokeType' : 4, 'commit' : True},True),
    ])
    def test_LUCI_RVC_NF_031(self,description, couponConfig, uploadType, dracarysUploadInput, invalidateRequest,isS3Support):
        invalidateCouponDetails = []
        for i in range(10):
            invalidateCouponDetails.append(constant.config['usersInfo'][i]['userId'])
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self, couponConfigReq=couponConfig)
        LuciHelper.uploadCouponAndAssertions(self,couponSeriesId, self.constructObj.importType[uploadType],noOfCouponsToBeUpload=20, dracraysUpload=dracarysUploadInput)
        LuciHelper.issueMultipleCoupon(self, couponSeriesId, invalidateCouponDetails)
        if isS3Support:
            invalidateRequest.update(LuciHelper.revokes3FileAndRequestObject(self,couponSeriesId, map(str,invalidateCouponDetails), invalidateRequest['revokeType']))
        LuciHelper.revokeCoupon(self,couponSeriesId,invalidateCouponDetails if not isS3Support else [],revokeType=invalidateRequest['revokeType'], reqDict=invalidateRequest)
        Assertion.constructAssertion(LuciDBHelper.getCouponsIssued_Count(couponSeriesId, 1) == 10, 'All Coupons Marked as invalid in issued table')
        revokeHistoryObj = LuciObject.getRevokeHistoryRequest({'couponSeriesId' : couponSeriesId})
        listOfRevoke = self.connObj.getRevokeHistory(revokeHistoryObj)[0].__dict__
        tempDetailsList = LuciDBHelper.getTempTableData(listOfRevoke['tempTableName'])
        Assertion.constructAssertion(len(tempDetailsList) == 10, 'Unrevoked coupon count is Matching Actual: {}'.format(len(tempDetailsList)))
        for tmp in tempDetailsList:
            Assertion.constructAssertion(tmp['errorMsg'] == 'invalid coupon id', 'Invalid coupon Ids sent & coupons not revoked Error Message: {}'.format(tmp['errorMsg']))
        LuciHelper.getCouponConfigAndAssertion(self,couponSeriesId,10,0)
        self.userId = constant.config['usersInfo'][0]['userId']
        s3OutPut = LuciHelper.downloadFile(self,listOfRevoke['errorFileHandle'])
        for errors in s3OutPut:
            Assertion.constructAssertion(errors['errorMsg'] == 'invalid coupon id', 'Invalid coupon Ids sent & coupons not revoked Error Message: {}'.format(errors['errorMsg']))
            Assertion.constructAssertion(errors['couponId'] in invalidateCouponDetails, 'Coupon issued Id is Matched with error report Actual: {} and Expected: {}'.format(errors['couponId'], invalidateCouponDetails))

    @pytest.mark.parametrize('description, couponConfig, uploadType, dracarysUploadInput, invalidateRequest,isS3Support', [
        ('Invalid Revoke Type coupon and userId DC', {'client_handling_type': 'DISC_CODE_PIN'}, 'NONE', {},{'revokeType' : 5, 'commit' : True}, False),
        ('s3File Support Invalid Revoke Type coupon and userId DC', {'client_handling_type': 'DISC_CODE_PIN'}, 'NONE', {},{'revokeType' : 5, 'commit' : True}, True)
    ])
    def test_LUCI_RVC_NF_032(self,description, couponConfig, uploadType, dracarysUploadInput, invalidateRequest,isS3Support):
        invalidateCouponDetails = []
        userIds = []
        for i in range(10):
            userIds.append(constant.config['usersInfo'][i]['userId'])
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self, couponConfigReq=couponConfig)
        LuciHelper.uploadCouponAndAssertions(self,couponSeriesId, self.constructObj.importType[uploadType],noOfCouponsToBeUpload=20, dracraysUpload=dracarysUploadInput)
        LuciHelper.issueMultipleCoupon(self, couponSeriesId, userIds)
        couponIssuedIdDict = LuciDBHelper.getCouponsIssuedList(couponSeriesId)

        for couponIssuedId in couponIssuedIdDict:
            invalidateCouponDetails.append([couponIssuedId['couponCode'], couponIssuedId['issuedBy']] if not isS3Support else couponIssuedId['couponCode'] + ',' + str(couponIssuedId['issuedBy']))
        if isS3Support:
            invalidateRequest.update(LuciHelper.revokes3FileAndRequestObject(self,couponSeriesId, invalidateCouponDetails, invalidateRequest['revokeType']))
        LuciHelper.revokeCoupon(self,couponSeriesId,invalidateCouponDetails if not isS3Support else [],revokeType=invalidateRequest['revokeType'], reqDict=invalidateRequest)
        Assertion.constructAssertion(LuciDBHelper.getCouponsIssued_Count(couponSeriesId, 1) == 10, 'All Coupons Marked as invalid in issued table')
        revokeHistoryObj = LuciObject.getRevokeHistoryRequest({'couponSeriesId' : couponSeriesId})
        listOfRevoke = self.connObj.getRevokeHistory(revokeHistoryObj)[0].__dict__
        tempDetailsList = LuciDBHelper.getTempTableData(listOfRevoke['tempTableName'])
        Assertion.constructAssertion(len(tempDetailsList) == 10, 'Unrevoked coupon count is Matching Actual: {}'.format(len(tempDetailsList)))
        for tmp in tempDetailsList:
            Assertion.constructAssertion(tmp['errorMsg'] == 'invalid customer id and coupon code', 'Invalid CUSTOMER_AND_COUPON sent & coupons not revoked Error Message: {}'.format(tmp['errorMsg']))
        LuciHelper.getCouponConfigAndAssertion(self,couponSeriesId,10,0)
        self.userId = constant.config['usersInfo'][0]['userId']
        s3OutPut = LuciHelper.downloadFile(self,listOfRevoke['errorFileHandle'])
        for invalidInput, errors in zip(invalidateCouponDetails,s3OutPut):
            Logger.log('Invalidate Data : ', invalidInput)
            if isS3Support:
                invalidInput = invalidInput.split(',')
                invalidInput[1] = int(invalidInput[1])
            Assertion.constructAssertion(errors['errorMsg'] == 'invalid customer id and coupon code', 'Invalid CUSTOMER_AND_COUPON sent & coupons not revoked Error Message: {}'.format(errors['errorMsg']))
            Assertion.constructAssertion(errors['couponCode'] == invalidInput[0], 'Coupon code is Matched with error report Actual: {} and Expected: {}'.format(errors['couponCode'], invalidInput[0]))
            Assertion.constructAssertion(errors['userId'] == invalidInput[1], 'User id is Matched with error report Actual: {} and Expected: {}'.format(errors['userId'], invalidInput[1]))


    @pytest.mark.parametrize('description, couponConfig, invalidateRequest,isS3Support', [
        ('Invalid Revoke Type customerId DC', {'client_handling_type': 'DISC_CODE', 'randomCodeLength' : 18}, {'revokeType' : 4, 'commit' : True, 'reuse' : True}, False),
        ('s3File Support Invalid Revoke Type customerId DC', {'client_handling_type': 'DISC_CODE', 'randomCodeLength' : 18}, {'revokeType' : 4, 'commit' : True, 'reuse' : True}, True)
    ])
    def test_LUCI_RVC_NF_033(self,description, couponConfig, invalidateRequest,isS3Support):
        invalidateCouponDetails = []
        userIds = []
        for i in range(10):
            userIds.append(constant.config['usersInfo'][i]['userId'])
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self, couponConfigReq=couponConfig)
        LuciHelper.queuePumpWait(self,couponSeriesId)
        LuciHelper.issueMultipleCoupon(self, couponSeriesId, userIds)
        couponIssuedIdDict = LuciDBHelper.getCouponsIssuedList(couponSeriesId)
        for couponIssuedId in couponIssuedIdDict:
            invalidateCouponDetails.append(couponIssuedId['id'])
        if isS3Support:
            invalidateRequest.update(LuciHelper.revokes3FileAndRequestObject(self,couponSeriesId, map(str,invalidateCouponDetails), invalidateRequest['revokeType']))
        LuciHelper.revokeCoupon(self,couponSeriesId,invalidateCouponDetails if not isS3Support else [],revokeType=invalidateRequest['revokeType'], reqDict=invalidateRequest)
        Assertion.constructAssertion(LuciDBHelper.getCouponsIssued_Count(couponSeriesId, 1) == 10, 'All Coupons Marked as invalid in issued table')
        revokeHistoryObj = LuciObject.getRevokeHistoryRequest({'couponSeriesId' : couponSeriesId})
        listOfRevoke = self.connObj.getRevokeHistory(revokeHistoryObj)[0].__dict__
        Assertion.constructAssertion(listOfRevoke['status'] == 2, 'Revoke Request status is Finished')
        Assertion.constructAssertion(listOfRevoke['revokeType'] == invalidateRequest['revokeType'], 'RevokeType is Match Actual : {} and Expected : {}'.format(listOfRevoke['revokeType'], invalidateRequest['revokeType']))
        Assertion.constructAssertion(listOfRevoke['unrevokedCount'] == 10, 'UnRevoked coupon count is Match Actual : {} and Expected : {}'.format(listOfRevoke['unrevokedCount'], 10))
        tempDetailsList = LuciDBHelper.getTempTableData(listOfRevoke['tempTableName'])
        Assertion.constructAssertion(len(tempDetailsList) == 10, 'Unrevoked coupon count is Matching Actual: {}'.format(len(tempDetailsList)))
        for tmp in tempDetailsList:
            Assertion.constructAssertion(tmp['errorMsg'] == 'max coupon code length exceeded', 'coupon Code length 18 and resue True revoked Error Message: {}'.format(tmp['errorMsg']))
        LuciHelper.getCouponConfigAndAssertion(self,couponSeriesId,10,0)
        s3OutPut = LuciHelper.downloadFile(self,listOfRevoke['errorFileHandle'])
        for errors in s3OutPut:
            Assertion.constructAssertion(errors['errorMsg'] == 'max coupon code length exceeded', 'coupon Code length 18 and resue True revoked Error Message: {}'.format(errors['errorMsg']))
            Assertion.constructAssertion(errors['couponId'] in invalidateCouponDetails, 'Coupon issued Id is Matched with error report Actual: {} and Expected: {}'.format(errors['couponId'], invalidateCouponDetails))

    @pytest.mark.parametrize('description, couponConfig, uploadType, dracarysUploadInput, invalidateRequest, isS3Support', [
        ('Revoke Type CouponId and upload same coupon codes ', {'client_handling_type': 'DISC_CODE_PIN'},'NONE', {}, {'revokeType': 4, 'commit': True, 'reuse' : True}, False),
        ('s3File support Revoke Type CouponId and upload same coupon codes ', {'client_handling_type': 'DISC_CODE_PIN'},'NONE', {}, {'revokeType': 4, 'commit': True, 'reuse' : True}, True),
        ])
    def test_LUCI_RVC_NF_034(self,description, couponConfig, uploadType, dracarysUploadInput, invalidateRequest, isS3Support):
        userIds = list()
        for i in range(5):
            userIds.append(constant.config['usersInfo'][i]['userId'])
        invalidateCouponDetails = []
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self, couponConfigReq=couponConfig)
        LuciHelper.uploadCouponAndAssertions(self,couponSeriesId, self.constructObj.importType[uploadType],noOfCouponsToBeUpload=5, dracraysUpload=dracarysUploadInput)
        LuciHelper.issueMultipleCoupon(self, couponSeriesId, userIds)
        couponIssuedIdDict = LuciDBHelper.getCouponsIssuedList(couponSeriesId)
        Assertion.constructAssertion(len(couponIssuedIdDict) == 5, 'No of coupons upload and issued count Actual: {} and Expected: {}'.format(len(couponIssuedIdDict), 5))
        for couponIssuedId in couponIssuedIdDict:
            invalidateCouponDetails.append(couponIssuedId['id'])
        if isS3Support:
            invalidateRequest.update(LuciHelper.revokes3FileAndRequestObject(self,couponSeriesId, map(str,invalidateCouponDetails), invalidateRequest['revokeType']))
        LuciHelper.revokeCoupon(self,couponSeriesId,invalidateCouponDetails if not isS3Support else [],revokeType=invalidateRequest['revokeType'], reqDict=invalidateRequest)
        Assertion.constructAssertion(LuciDBHelper.getCouponsIssued_Count(couponSeriesId, 1) == 0, 'All Coupons Marked as invalid in issued table')
        LuciHelper.uploadCouponAndAssertions(self, couponSeriesId, self.constructObj.importType[uploadType], noOfCouponsToBeUpload=5, dracraysUpload={'invalidCase' : [True, True]})

    @pytest.mark.parametrize('description, couponConfig, uploadType, dracarysUploadInput, invalidateRequest,isS3Support', [
        ('Revoke Type CouponId and Redeem coupon code', {'client_handling_type': 'DISC_CODE_PIN'},'NONE', {}, {'revokeType': 4, 'commit': True, 'reuse' : True}, False),
        ('s3File support Revoke Type CouponId and Redeem coupon code', {'client_handling_type': 'DISC_CODE_PIN'},'NONE', {}, {'revokeType': 4, 'commit': True, 'reuse' : True}, True),
        ])
    def test_LUCI_RVC_NF_035(self,description, couponConfig, uploadType, dracarysUploadInput, invalidateRequest,isS3Support):
        invalidateCouponDetails = []
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self, couponConfigReq=couponConfig)
        LuciHelper.uploadCouponAndAssertions(self,couponSeriesId, self.constructObj.importType[uploadType],noOfCouponsToBeUpload=5, dracraysUpload=dracarysUploadInput)
        couponCode = LuciHelper.issueCouponAndAssertions(self,couponSeriesId)[0]
        couponIssuedIdDict = LuciDBHelper.getCouponsIssuedList(couponSeriesId)
        for couponIssuedId in couponIssuedIdDict:
            invalidateCouponDetails.append(couponIssuedId['id'])
        if isS3Support:
            invalidateRequest.update(LuciHelper.revokes3FileAndRequestObject(self,couponSeriesId, map(str,invalidateCouponDetails), invalidateRequest['revokeType']))
        LuciHelper.revokeCoupon(self,couponSeriesId,invalidateCouponDetails if not isS3Support else [],revokeType=invalidateRequest['revokeType'], reqDict=invalidateRequest)
        Assertion.constructAssertion(LuciDBHelper.getCouponsIssued_Count(couponSeriesId, 1) == 0, 'All Coupons Marked as invalid in issued table')
        LuciHelper.redeemCouponAndAssertions(self,couponSeriesId,couponCode,error=[633, 'invalid coupon code'])

    @pytest.mark.parametrize('description, couponConfig, uploadType, dracarysUploadInput, invalidateRequest', [
        ('Bulk Coupon Revoke -DC', {'client_handling_type': 'DISC_CODE'}, 'NONE', {}, {'revokeType': 0, 'commit': True, 'reuse': True})
    ])
    def est_LUCI_RVC_NF_036(self, description, couponConfig, uploadType, dracarysUploadInput, invalidateRequest):
        userIds = list()
        #2k-3sec, 20k-20sec , 1Lakh - more than minute
        noOfUsers = 100000
        invalidateCouponDetails = []
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self, couponConfigReq=couponConfig)
        LuciHelper.queuePumpWait(self, couponSeriesId)

        bulkUserIds = []
        couponCodeList = []
        for _ in range(noOfUsers):
            bulkUserIds.append(randValues.randomInteger(9))
        bulkUserIds = list(set(bulkUserIds))
        limit = 5000
        i = 0
        Logger.log('Actual : ', len(bulkUserIds))
        for _ in range(len(bulkUserIds)):
            if limit > (len(bulkUserIds)):
                limit = len(bulkUserIds)
            issueMultipleCouponsRequest = {'couponSeriesId': couponSeriesId, 'storeUnitId': self.tillId, 'userIds': bulkUserIds[i:(limit)]}
            issueMultipleCouponsRequestObj = LuciObject.issueMultipleCouponsRequest(issueMultipleCouponsRequest)
            couponDetailsList = self.connObj.issueMultipleCoupons(issueMultipleCouponsRequestObj)

            for couponDetails in couponDetailsList:
                couponDetails = couponDetails.__dict__
                couponCodeList.append(couponDetails['couponCode'])
            if limit == len(bulkUserIds):
                break

            i = limit
            limit = limit+5000

        LuciHelper.revokeCoupon(self, couponSeriesId, couponCodeList, revokeType=invalidateRequest['revokeType'], reqDict=invalidateRequest)
        # Assertion.constructAssertion(LuciDBHelper.getCouponsIssued_Count(couponSeriesId, 1) == 0, 'All Coupons Marked as invalid in issued table')

    @pytest.mark.parametrize('description, couponConfig, invalidateRequest', [
        ('Revoke Type only unissued -DCP', {'client_handling_type': 'DISC_CODE_PIN'},{'revokeType': 1, 'commit': True, 'reuse': True})
    ])
    def test_LUCI_RVC_NF_037_sanity(self,description, couponConfig, invalidateRequest):
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self, couponConfigReq=couponConfig)
        couponCodeList = LuciHelper.uploadCouponAndAssertions(self,couponSeriesId, self.constructObj.importType['NONE'],noOfCouponsToBeUpload=2500, dracraysUpload={})['coupons']

        bulkUserIds = LuciHelper.getBulkUsers(650)
        issueMultipleCouponsRequest = {'couponSeriesId': couponSeriesId, 'storeUnitId': self.tillId, 'userIds': bulkUserIds}
        issueMultipleCouponsRequestObj = LuciObject.issueMultipleCouponsRequest(issueMultipleCouponsRequest)
        self.connObj.issueMultipleCoupons(issueMultipleCouponsRequestObj)
        couponCode = LuciHelper.issueCouponAndAssertions(self, couponSeriesId)[0]
        queueCount = LuciHelper.getQueueSize(self,couponSeriesId)
        Assertion.constructAssertion(queueCount != 0, 'Redis Contains remaining coupons After issual count: {}'.format(queueCount))
        LuciHelper.revokeCoupon(self,couponSeriesId,couponCodeList,revokeType=invalidateRequest['revokeType'], reqDict=invalidateRequest)
        LuciHelper.redeemCouponAndAssertions(self, couponSeriesId, couponCode)
        queueCount = LuciHelper.getQueueSize(self,couponSeriesId)
        Assertion.constructAssertion(queueCount == 0, 'Redis queue cleared After revoked count: {}'.format(queueCount))