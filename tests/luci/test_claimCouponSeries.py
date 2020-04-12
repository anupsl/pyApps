import time,pytest, random
from src.Constant.constant import constant
from src.modules.luci.luciDBHelper import LuciDBHelper
from src.utilities.logger import Logger
from src.utilities.assertion import Assertion
from src.utilities.utils import Utils
from src.modules.luci.luciHelper import LuciHelper
from src.modules.luci.luciObject import LuciObject

class Test_ClaimCouponSeries():

    def setup_class(self):
        Logger.logSuiteName(str(self).split('.')[-1])
        self.constructObj = LuciObject()
        self.userId = constant.config['usersInfo'][0]['userId']
        self.tillId = constant.config['tillIds'][0]
        self.storeId = constant.config['storeIds'][0]
        self.billId = Utils.getTime(milliSeconds=True)

    def teardown_class(self):
        self.connObj = '' 

    def setup_method(self, method):
        self.connObj = LuciHelper.getConnObj(newConnection=True)
        Logger.logMethodName(method.__name__)
        constant.config['requestId'] = 'luci_auto_'+str(random.randint(11111, 99999))

    @pytest.mark.parametrize('description, couponConfig, expected', [
        ('Create CS with campaign_Id and without claim by', {'discount_type' : 'PERC', 'discount_upto': 5}, ['OUTBOUND', constant.config['campaignId'], '5.00']),
        ('Create CS with claim by None', {'discount_type' : 'PERC', 'discount_upto': 10.0, 'series_type': 'UNDEFINED', 'campaign_id': -1, 'owned_by': 0}, ['NONE', -1, '10.00']),
        ('Create CS with claim by Loyalty', {'discount_type' : 'PERC','discount_upto': 7.5, 'series_type': 'LOYALTY', 'campaign_id': -1, 'owned_by': 1, 'owner_id': 123}, ['LOYALTY', 123, '7.50']),
        ('Create CS with claim by Goodwill', {'discount_type' : 'PERC', 'discount_upto': 12.6, 'series_type': 'GOODWILL', 'campaign_id': -1, 'owned_by': 3}, ['GOODWILL','','12.60']),
        ('Create CS without claim by Goodwill', {'discount_type' : 'PERC', 'discount_upto': 100.12, 'series_type': 'GOODWILL', 'campaign_id': -1}, ['GOODWILL','', '100.12']),
        ('Create CS with claim by campaigns', {'discount_type' : 'PERC', 'discount_upto': 78.0, 'campaign_id': -1, 'owned_by': 2, 'owner_id': constant.config['campaignId']}, ['OUTBOUND', constant.config['campaignId'], '78.00']),
        ('Create CS with claim by Timeline', {'discount_type' : 'PERC', 'discount_upto': 46.0, 'series_type' : 'TIMELINE' ,'campaign_id': -1, 'owned_by': 5, 'owner_id': 512}, ['TIMELINE', 512, '46.00']),
        ('Create CS with claim by Referral', {'discount_type' : 'PERC', 'discount_upto': 55.0, 'series_type': 'REFERRAL' ,'campaign_id': -1, 'owned_by': 6, 'owner_id': 612}, ['REFERRAL', 612, '55.00'])])
    def test_LUCI_CF_001(self,description,couponConfig, expected):
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self,couponConfig)
        Assertion.constructAssertion(couponConfigObj['discount_upto'] == couponConfig['discount_upto'],'Discount upto value set Actual {} and Expected : {}'.format(couponConfigObj['discount_upto'], couponConfig['discount_upto']))
        ownedInfo = LuciDBHelper.getOwnerInfo(couponSeriesId)
        Assertion.constructAssertion(ownedInfo['owned_by'] == expected[0], 'Owned by Actual: {} and Expected: {}'.format(ownedInfo['owned_by'],expected[0]))
        if couponConfigObj['series_type'] in ['OUTBOUND','LOYALTY'] or couponConfigObj['owned_by'] in [2,1]:
            Assertion.constructAssertion(ownedInfo['owner_id'] == expected[1], 'Owner Id Actual: {} and Expected: {}'.format(ownedInfo['owner_id'],expected[1]))
        discount_upto = LuciDBHelper.getCouponConfigKeyValues(couponSeriesId, 4)
        Assertion.constructAssertion(discount_upto == expected[2], 'Discount upto Actual: {} and Expected: {}'.format(discount_upto, expected[2]))

    @pytest.mark.parametrize('description, couponConfig, expected', [
        ('CS_Type_Loyalty_and_owned_by_NONE', {'valid_till_date' : None, 'series_type': 'LOYALTY', 'campaign_id': -1, 'owned_by': 0}, [629,'series type and owned by should be same']),
        ('CS_Type_Campaign_and_owned_by_NONE', {'valid_till_date': None, 'campaign_id': constant.config['campaignId'], 'owned_by': 0}, [629, 'owned by should be outbound when series type is campaign']),
        ('CS_Type_Undefined_and_ownerId_CampaignId', {'valid_till_date': None, 'series_type': 'UNDEFINED', 'owned_by': 2, 'owner_id': constant.config['campaignId']}, [629, 'campaign id should be -1 when series type is undefined']),
        ('CS_Type_Loyalty_and_owned_by_OUTBOUND', {'valid_till_date' : None, 'series_type': 'LOYALTY', 'campaign_id': -1, 'owned_by': 2, 'owner_id' : constant.config['campaignId']}, [629,'series type and owned by should be same']),
        ('CS_Type_TIMELINE_and_owned_by_OUTBOUND', {'valid_till_date' : None, 'series_type': 'TIMELINE', 'campaign_id': -1, 'owned_by': 2, 'owner_id' : constant.config['campaignId']}, [629,'series type and owned by should be same']),
        ('CS_Type_REFERRAL_and_owned_by_OUTBOUND', {'valid_till_date' : None, 'series_type': 'REFERRAL', 'campaign_id': -1, 'owned_by': 2, 'owner_id' : constant.config['campaignId']}, [629,'series type and owned by should be same'])])
    def test_LUCI_CF_002(self,description,couponConfig, expected):
        try:
            couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self, couponConfig)
        except Exception, luciExp:
            luciExp = luciExp.__dict__
            Assertion.constructAssertion(luciExp['errorCode'] == expected[0], 'Luci Exception error code Actual: {} and Expected: {}'.format(luciExp['errorCode'], expected[0]))
            Assertion.constructAssertion(luciExp['errorMsg'] == expected[1], 'Luci Exception Error Msg Actual : {}'.format(luciExp['errorMsg']))

    @pytest.mark.parametrize('description, couponConfig, claimObject', [
        ('Claim_by_LOYALTY_using_Claim_call', {'valid_till_date': None,'campaign_id': -1, 'series_type': 'UNDEFINED', 'owned_by': 0},[1, 123, 'LOYALTY']),
        ('Claim_by_OUTBOUND_using_Claim_call', {'valid_till_date': None, 'campaign_id': -1, 'series_type': 'UNDEFINED', 'owned_by': 0}, [2, constant.config['campaignId'], 'CAMPAIGN']),
        ('Claim_by_GOODWILL_using_Claim_call', {'valid_till_date': None, 'campaign_id': -1, 'series_type': 'UNDEFINED', 'owned_by': 0}, [3, -1, 'GOODWILL']),
        ('Claim_by_DVS_using_Claim_call', {'valid_till_date': None, 'campaign_id': -1, 'series_type': 'UNDEFINED', 'owned_by': 0}, [4, constant.config['campaignId'], 'DVS']),
        ('Claim_by_TIMELINE_using_Claim_call', {'valid_till_date': None, 'campaign_id': -1, 'series_type': 'UNDEFINED', 'owned_by': 0}, [5, constant.config['campaignId'], 'TIMELINE']),
        ('Claim_by_REFERRAL_using_Claim_call', {'valid_till_date': None, 'campaign_id': -1, 'series_type': 'UNDEFINED', 'owned_by': 0}, [6, constant.config['campaignId'], 'REFERRAL'])])
    def test_LUCI_CF_003(self, description, couponConfig,claimObject):
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self, couponConfig)
        voucherType = LuciDBHelper.getCouponSeriesType(couponSeriesId)['seriesType']
        Assertion.constructAssertion(voucherType == couponConfig['series_type'], 'Coupon Series Type in voucher_series Actual : {} and Expected : {}'.format(voucherType,couponConfig['series_type']))
        Assertion.constructAssertion(self.connObj.getQueueSize(constant.config['orgId'], couponSeriesId, constant.config['requestId']) == 0, 'Coupons Not Pumped to Queue')
        LuciHelper.claimCouponSeries(self, couponSeriesId, claimObject)

    @pytest.mark.parametrize('description, couponConfig, claimObject, updateClaim,  expected', [
        ('ReClaim_LOYALTY', {'valid_till_date': None,'campaign_id': -1, 'series_type': 'UNDEFINED', 'owned_by': 0},[1, 123,'LOYALTY'], [2, constant.config['campaignId'], 'LOYALTY'], [640, 'can not change owned by, once it is set, already claimed by : LOYALTY']),
        ('ReClaim_OUTBOUND', {'valid_till_date': None, 'campaign_id': -1, 'series_type': 'UNDEFINED', 'owned_by': 0}, [2, constant.config['campaignId'],'CAMPAIGN'], [3, -1, 'CAMPAIGN'] ,  [640, 'can not change owned by, once it is set, already claimed by : OUTBOUND']),
        ('ReClaim_GOODWILL', {'valid_till_date': None, 'campaign_id': -1, 'series_type': 'UNDEFINED', 'owned_by': 0}, [3, -1, 'GOODWILL'], [4, constant.config['campaignId'], 'GOODWILL'] ,[640, 'can not change owned by, once it is set, already claimed by : GOODWILL']),
        ('ReClaim_DVS', {'valid_till_date': None, 'campaign_id': -1, 'series_type': 'UNDEFINED', 'owned_by': 0}, [4, constant.config['campaignId'], 'DVS'], [1, 123, 'DVS'] , [640, 'can not change owned by, once it is set, already claimed by : DVS']),
        ('ReClaim_TIMELINE', {'valid_till_date': None, 'campaign_id': -1, 'series_type': 'UNDEFINED', 'owned_by': 0}, [5, 512, 'TIMELINE'], [4, constant.config['campaignId'], 'TIMELINE'] ,[640, 'coupon series already claimed by campaign id : 512']),
        ('ReClaim_REFERRAL', {'valid_till_date': None, 'campaign_id': -1, 'series_type': 'UNDEFINED', 'owned_by': 0}, [6, 612, 'REFERRAL'], [4, constant.config['campaignId'], 'REFERRAL'] ,[640, 'coupon series already claimed by campaign id : 612'])])
    def test_LUCI_CF_004(self, description, couponConfig,claimObject, updateClaim, expected):
            couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self, couponConfig)
            LuciHelper.claimCouponSeries(self, couponSeriesId, claimObject)
            #Re-claim with Diff owners
            LuciHelper.claimCouponSeries(self, couponSeriesId, updateClaim, expectedErrors = expected, claimResult=False)


    @pytest.mark.parametrize('description, couponConfig, claimObject, updateClaim, expected', [
        ('Claim_by_Negative_org_id', {'valid_till_date': None,'campaign_id': -1, 'series_type': 'UNDEFINED', 'owned_by': 0},[1, 123,'LOYALTY'], {'orgId' : -1}, [500, 'invalid org id -1']),
        ('Claim_by_Negative_Campaign_id', {'valid_till_date': None, 'campaign_id': -1, 'series_type': 'UNDEFINED', 'owned_by': 0}, [2, constant.config['campaignId'],'CAMPAIGN'], {'ownerId': -123}, [629, 'invalid value given for owner id']),
        ('Claim_by_Invalid_Goodwill_Id', {'valid_till_date': None, 'campaign_id': -1, 'series_type': 'UNDEFINED', 'owned_by': 0}, [3, -1, 'GOODWILL'], {'ownerId': constant.config['campaignId']}, [629, 'owner id should not be set when owned by is none or goodwill']),
        ('Claim_by_None_using_Claim_call', {'valid_till_date': None, 'campaign_id': -1, 'series_type': 'UNDEFINED', 'owned_by': 0}, [0, -1, 'NONE'], {}, [629, 'owned by can not be none']),
        ('Claim_by_Negative_Loyalty_id', {'valid_till_date': None, 'campaign_id': -1, 'series_type': 'UNDEFINED', 'owned_by': 0}, [1, 123, 'LOYALTY'], {'ownerId': -123}, [629,'invalid value given for owner id'])])
    def test_LUCI_CF_005(self, description, couponConfig,claimObject, updateClaim, expected):
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self, couponConfig)
        tmpDict = {'couponSeriesId': couponSeriesId, 'ownedBy': claimObject[0], 'ownerId': claimObject[1], 'ownerValidity': Utils.getTime(days=2, milliSeconds=True)}
        tmpDict.update(updateClaim)
        claimObj = LuciObject.claimCouponConfigRequest(tmpDict)
        result = self.connObj.claimCouponConfig(claimObj).__dict__
        Assertion.constructAssertion(not result['success'], 'Re-claim Coupon Series by {}'.format(updateClaim))
        luciExp = result['ex'].__dict__
        Assertion.constructAssertion(luciExp['errorCode'] == expected[0], 'Luci Exception error code Actual: {} and Expected: {}'.format(luciExp['errorCode'], expected[0]))
        Assertion.constructAssertion(luciExp['errorMsg'] == expected[1], 'Luci Exception Error Msg Actual : {}'.format(luciExp['errorMsg']))

    @pytest.mark.parametrize('description' , [('Update_ownerId_by_saveCouponConfig')])
    def test_LUCI_CF_006(self, description):
        #Save Coupon Config
        try:
            couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self)
            couponConfigObj.update({'owned_by': 1, 'owner_id': 123})
            LuciHelper.saveCouponConfigAndAssertions(self, couponConfigObj)
        except Exception, luciExp:
            luciExp = luciExp.__dict__
            Assertion.constructAssertion(luciExp['errorCode'] == constant.INVALID_INPUT, 'Luci Exception error code Actual: {} and Expected: {}'.format(luciExp['errorCode'], constant.INVALID_INPUT))
            Assertion.constructAssertion(luciExp['errorMsg'] == 'owned by should be outbound when series type is campaign', 'Luci Exception Error Msg Actual : {}'.format(luciExp['errorMsg']))

    @pytest.mark.parametrize('description' , [('Get_Config_And_Get_All_Coupon_Config')])
    def test_LUCI_CF_007(self, description):
        try:
            couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self)
            LuciHelper.getCouponConfigAndAssertion(self,couponSeriesId,0,0)
            getAllCouponConfig = self.connObj.getAllCouponConfigurations(LuciObject.getAllCouponConfigRequest({'couponSeriesIds' : [couponSeriesId]}))[0].__dict__
            Assertion.constructAssertion('owned_by' in getAllCouponConfig, 'Getting Details Owned by in CouponConfig')
            Assertion.constructAssertion('owner_id' in getAllCouponConfig, 'Getting Details Owner id in CouponConfig')
        except Exception, luciExp:
            luciExp = luciExp.__dict__
            Assertion.constructAssertion(luciExp['errorCode'] == constant.INVALID_INPUT, 'Luci Exception error code Actual: {} and Expected: {}'.format(luciExp['errorCode'], constant.INVALID_INPUT))
            Assertion.constructAssertion(luciExp['errorMsg'] == 'owned by should be outbound when series type is campaign', 'Luci Exception Error Msg Actual : {}'.format(luciExp['errorMsg']))

    @pytest.mark.parametrize('description, params, expected' , [
        ('Issue_And_Redeemed_change_Owned_and_OwnerId', {'owned_by': 1, 'owner_id': 123},[629, 'owned by should be outbound when series type is campaign']),
        ('Issue_And_Redeemed_change_CampaignId', {'campaign_id' : 12345}, [629, 'campaign id and owner id should be same when owned by is campaign'])])
    def test_LUCI_CF_008(self, description, params, expected):
        #Save Coupon Config
        try:
            couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self)
            couponCode = LuciHelper.issueCouponAndAssertions(self,couponSeriesId)[0]
            LuciHelper.redeemCouponAndAssertions(self, couponSeriesId, couponCode)
            couponConfigObj.update(params)
            LuciHelper.saveCouponConfigAndAssertions(self, couponConfigObj)
        except Exception, luciExp:
            luciExp = luciExp.__dict__
            Logger.log('Luci Exception : ' , luciExp)
            Assertion.constructAssertion(luciExp['errorCode'] == expected[0], 'Luci Exception error code Actual: {} and Expected: {}'.format(luciExp['errorCode'], expected[0]))
            Assertion.constructAssertion(luciExp['errorMsg'] == expected[1], 'Luci Exception Error Msg Actual : {}'.format(luciExp['errorMsg']))

    @pytest.mark.parametrize('description, couponConfig,  expected', [
        ('Issue_Coupon_when_valid_till_date_None', {'valid_till_date': None, 'campaign_id': -1, 'series_type': 'UNDEFINED', 'owned_by': 0}, [641, 'coupon series valid till date is not configured'])])
    def test_LUCI_CF_009(self, description, couponConfig, expected):
        try:
            couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self, couponConfig)
            LuciHelper.issueCouponAndAssertions(self,couponSeriesId)
        except Exception, luciExp:
            luciExp = luciExp.__dict__
            Assertion.constructAssertion(luciExp['errorCode'] == expected[0], 'Luci Exception error code Actual: {} and Expected: {}'.format(luciExp['errorCode'], expected[0]))
            Assertion.constructAssertion(luciExp['errorMsg'] == expected[1], 'Luci Exception Error Msg Actual : {}'.format(luciExp['errorMsg']))

    @pytest.mark.parametrize('description, couponConfig,  expected', [
        ('Issue_Coupon_when_valid_till_date_None', {'valid_till_date': None, 'campaign_id': -1, 'series_type': 'UNDEFINED', 'owned_by': 0}, [641, 'coupon series valid till date is not configured'])])
    def test_LUCI_CF_010(self, description, couponConfig, expected):
        try:
            couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self, couponConfig)
            userList = []
            for tmpDict in constant.config['usersInfo']:
                userList.append(tmpDict['userId'])
            LuciHelper.issueMultipleCoupon(self,couponSeriesId, userList)
        except Exception, luciExp:
            luciExp = luciExp.__dict__
            Assertion.constructAssertion(luciExp['errorCode'] == expected[0], 'Luci Exception error code Actual: {} and Expected: {}'.format(luciExp['errorCode'], expected[0]))
            Assertion.constructAssertion(luciExp['errorMsg'] == expected[1], 'Luci Exception Error Msg Actual : {}'.format(luciExp['errorMsg']))

    @pytest.mark.parametrize('description, couponConfig, claimObject, updateClaim,  expected', [
        ('CS_Type_LOYALTY_Revoke_CS_And_Re-Claim_by_Campaign', {'valid_till_date': None,'campaign_id': -1, 'series_type': 'UNDEFINED', 'owned_by': 0},[1, 123,'LOYALTY'], [2, constant.config['campaignId'], 'LOYALTY'], [640, 'can not change owned by, once it is set, already claimed by : LOYALTY'])])
    def test_LUCI_CF_011(self, description, couponConfig,claimObject, updateClaim, expected):
            couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self, couponConfig)
            LuciHelper.claimCouponSeries(self, couponSeriesId, claimObject)
            LuciHelper.invalidateCouponAndAssertions(self,couponSeriesId,numRevoked=0)
            LuciHelper.claimCouponSeries(self, couponSeriesId, updateClaim, expected, claimResult = False)

    @pytest.mark.parametrize('description, couponConfig, expected', [
        ('Discount_upto Negative value', {'discount_type' : 'PERC', 'discount_upto': -100}, [629,'discount_upto cannot be negative']),
        ('Discount_upto Negative value', {'discount_upto':  5}, [629, 'discount_upto cannot be used with discount type abs']),
        ('Discount_upto Invalid value', {'discount_type' : 'PERC', 'discount_upto': 9999999999}, ['OUTBOUND', constant.config['campaignId'], '9999999999.00'])])
    def test_LUCI_CF_012(self,description,couponConfig, expected):
        try:
            couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self, couponConfig)
            discount_upto = LuciDBHelper.getCouponConfigKeyValues(couponSeriesId, 4)
            Assertion.constructAssertion(discount_upto == expected[2], 'Discount upto Actual: {} and Expected: {}'.format(discount_upto, expected[2]))
        except Exception, luciExp:
            luciExp = luciExp.__dict__
            Assertion.constructAssertion(luciExp['errorCode'] == expected[0], 'Luci Exception error code Actual: {} and Expected: {}'.format(luciExp['errorCode'], expected[0]))
            Assertion.constructAssertion(luciExp['errorMsg'] == expected[1], 'Luci Exception Error Msg Actual : {}'.format(luciExp['errorMsg']))



    @pytest.mark.parametrize('description, couponConfig, expected', [
        ('Discount upto Validate GetCouponConfig', {'discount_type' : 'PERC', 'discount_upto': 5.12}, ['OUTBOUND', constant.config['campaignId'], '5.12'])])
    def test_LUCI_CF_013(self,description,couponConfig, expected):
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self,couponConfig)
        ownedInfo = LuciDBHelper.getOwnerInfo(couponSeriesId)
        Assertion.constructAssertion(ownedInfo['owned_by'] == expected[0], 'Owned by Actual: {} and Expected: {}'.format(ownedInfo['owned_by'],expected[0]))
        if couponConfigObj['series_type'] in ['OUTBOUND','LOYALTY'] or couponConfigObj['owned_by'] in [2,1]:
            Assertion.constructAssertion(ownedInfo['owner_id'] == expected[1], 'Owner Id Actual: {} and Expected: {}'.format(ownedInfo['owner_id'],expected[1]))
        discount_upto = LuciDBHelper.getCouponConfigKeyValues(couponSeriesId, 4)
        Assertion.constructAssertion(discount_upto == expected[2], 'Discount upto Actual: {} and Expected: {}'.format(discount_upto, expected[2]))
        getCouponConfig = LuciHelper.getCouponConfigAndAssertion(self,couponSeriesId,0,0)
        Assertion.constructAssertion(getCouponConfig['discount_upto'] == couponConfig['discount_upto'], 'Discount upto value set Actual {} and Expected : {}'.format(getCouponConfig['discount_upto'], couponConfig['discount_upto']))

    @pytest.mark.parametrize('description, couponConfig, expected', [
        ('Redemption Org Entity as Zone', {'redemption_org_entity_type' : 0}, ['ZONE']),
        ('Redemption Org Entity as Concept', {'redemption_org_entity_type' : 1}, ['CONCEPT']),
        ('Redemption Org Entity as Store', {'redemption_org_entity_type' : 2}, ['STORE']),
        ('Redemption Org Entity as Till', {'redemption_org_entity_type' : 3}, ['TILL'])])
    def test_LUCI_CF_014(self,description,couponConfig, expected):
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self,couponConfig)
        Assertion.constructAssertion(couponConfigObj['redemption_org_entity_type'] == couponConfig['redemption_org_entity_type'], 'Redemption Org Entity Type in API call Actual {} and Expected : {}'.format(couponConfigObj['redemption_org_entity_type'], couponConfig['redemption_org_entity_type']))
        redemptionEntityType = LuciDBHelper.getCouponConfigKeyValues(couponSeriesId, 3)
        Assertion.constructAssertion(redemptionEntityType == expected[0], 'Redemption Org Entity Type in DB Actual: {} and Expected: {}'.format(redemptionEntityType, expected[0]))
        getCouponConfig = LuciHelper.getCouponConfigAndAssertion(self, couponSeriesId, 0, 0)
        Assertion.constructAssertion(getCouponConfig['redemption_org_entity_type'] == couponConfig['redemption_org_entity_type'], 'Redemption Org Entity Type in GetCouponConfig Actual {} and Expected : {}'.format(getCouponConfig['redemption_org_entity_type'], couponConfig['redemption_org_entity_type']))

    @pytest.mark.parametrize('description, couponConfig, claimObject , validTillDay', [
        ('Set OwnerValidity as 2 and Update Valid Till date as 1', {'valid_till_date': None,'campaign_id': -1, 'series_type': 'UNDEFINED', 'owned_by': 0},[2, constant.config['campaignId'], 'CAMPAIGN'], 1),
        ('Set OwnerValidity as 2 and Update Valid Till date as 4', {'valid_till_date': None, 'campaign_id': -1, 'series_type': 'UNDEFINED', 'owned_by': 0}, [2, constant.config['campaignId'], 'CAMPAIGN'], 4)])
    def test_LUCI_CF_015(self, description, couponConfig, claimObject, validTillDay):
            couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self, couponConfig)
            LuciHelper.claimCouponSeries(self, couponSeriesId, claimObject)
            couponConfigObj = LuciHelper.getCouponConfigAndAssertion(self,couponSeriesId,0,0)
            Assertion.constructAssertion(long(couponConfigObj['ownerValidity']) > 0, 'Owner Validity is set Actual: {}'.format(couponConfigObj['ownerValidity']))
            couponConfigObj.update({'valid_till_date': Utils.getTime(days=validTillDay,milliSeconds=True)})
            LuciHelper.saveCouponConfigAndAssertions(self, couponConfigObj)
            couponConfigObj = LuciHelper.getCouponConfigAndAssertion(self, couponSeriesId, 0, 0)
            Assertion.constructAssertion(long(couponConfigObj['valid_till_date']) > 0, 'valid_till_date is set Actual: {}'.format(couponConfigObj['valid_till_date']))
            Assertion.constructAssertion(long(couponConfigObj['ownerValidity']) > 0, 'Owner Validity is set Actual: {}'.format(couponConfigObj['ownerValidity']))


    @pytest.mark.parametrize('description, couponConfig, claimObject', [
        ('GetCouponConfig by ownerBy & ownedId LOYALTY', {'valid_till_date': None,'campaign_id': -1, 'series_type': 'UNDEFINED', 'owned_by': 0},[1, 123, 'LOYALTY']),
        ('GetCouponConfig by ownerBy & ownedId OUTBOUND', {'valid_till_date': None, 'campaign_id': -1, 'series_type': 'UNDEFINED', 'owned_by': 0}, [2, constant.config['campaignId'], 'CAMPAIGN']),
        ('GetCouponConfig by ownerBy & ownedId GOODWILL', {'valid_till_date': None, 'campaign_id': -1, 'series_type': 'UNDEFINED', 'owned_by': 0}, [3, -1, 'GOODWILL']),
        ('GetCouponConfig by ownerBy & ownedId DVS', {'valid_till_date': None, 'campaign_id': -1, 'series_type': 'UNDEFINED', 'owned_by': 0}, [4, constant.config['campaignId'], 'DVS']),
        ('GetCouponConfig by ownerBy & ownedId GOODWILL', {'valid_till_date': None, 'campaign_id': -1, 'series_type': 'UNDEFINED', 'owned_by': 0}, [5, 512, 'TIMELINE']),
        ('GetCouponConfig by ownerBy & ownedId GOODWILL', {'valid_till_date': None, 'campaign_id': -1, 'series_type': 'UNDEFINED', 'owned_by': 0}, [6, 612, 'REFERRAL'])])
    def test_LUCI_CF_016(self, description, couponConfig,claimObject):
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self, couponConfig)
        LuciHelper.claimCouponSeries(self, couponSeriesId, claimObject)
        LuciHelper.getCouponConfigAndAssertion(self,couponSeriesId,0,0,{'ownedBy' : claimObject[0]})
        LuciHelper.getCouponConfigAndAssertion(self,couponSeriesId,0,0,{'ownerId' : claimObject[1]})
        LuciHelper.getCouponConfigAndAssertion(self,couponSeriesId,0,0,{'ownedBy' : claimObject[0], 'ownerId' : claimObject[1]})

    @pytest.mark.parametrize('description, couponConfig, expected', [
        ('Set ownedby None and OwnerValidity -1', {'valid_till_date': None, 'campaign_id': -1, 'series_type': 'UNDEFINED', 'owned_by': 0, 'ownerValidity': -1}, [629, 'invalid value given for owner validity']),
        ('Not set ownedby None and OwnerValidity -1', {'valid_till_date': None, 'campaign_id': -1, 'series_type': 'UNDEFINED', 'owned_by': 0, 'ownerValidity' : Utils.getTime(days=2, milliSeconds=True)}, [629, 'owner validity should not be set when owned by is NONE'])])
    def test_LUCI_CF_017(self, description, couponConfig, expected):
        try:
            couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self, couponConfig)
        except Exception, luciExp:
            luciExp = luciExp.__dict__
            Assertion.constructAssertion(luciExp['errorCode'] == expected[0], 'Luci Exception error code Actual: {} and Expected: {}'.format(luciExp['errorCode'], expected[0]))
            Assertion.constructAssertion(luciExp['errorMsg'] == expected[1], 'Luci Exception Error Msg Actual : {}'.format(luciExp['errorMsg']))


    @pytest.mark.parametrize('description, couponConfig, claimObject , validTillDay', [
        ('Set OwnerValidity as 2 and Update Valid Till & OwnerValidity date as 1', {'valid_till_date': None,'campaign_id': -1, 'series_type': 'UNDEFINED', 'owned_by': 0},[2, constant.config['campaignId'], 'CAMPAIGN'], 1),
        ('Set OwnerValidity as 2 and Update Valid Till & OwnerValidity date as 4', {'valid_till_date': None, 'campaign_id': -1, 'series_type': 'UNDEFINED', 'owned_by': 0}, [2, constant.config['campaignId'], 'CAMPAIGN'], 4)])
    def test_LUCI_CF_018(self, description, couponConfig, claimObject, validTillDay):
            couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self, couponConfig)
            LuciHelper.claimCouponSeries(self, couponSeriesId, claimObject)
            couponConfigObj = LuciHelper.getCouponConfigAndAssertion(self,couponSeriesId,0,0)
            Assertion.constructAssertion(long(couponConfigObj['ownerValidity']) > 0, 'Owner Validity is set Actual: {}'.format(couponConfigObj['ownerValidity']))
            couponConfigObj.update({'valid_till_date': Utils.getTime(days=validTillDay,milliSeconds=True), 'ownerValidity' : Utils.getTime(days=validTillDay,milliSeconds=True)})
            LuciHelper.saveCouponConfigAndAssertions(self, couponConfigObj)
            couponConfigObj = LuciHelper.getCouponConfigAndAssertion(self, couponSeriesId, 0, 0)
            Assertion.constructAssertion(long(couponConfigObj['valid_till_date']) > 0, 'valid_till_date is set Actual: {}'.format(couponConfigObj['valid_till_date']))
            Assertion.constructAssertion(long(couponConfigObj['ownerValidity']) > 0, 'Owner Validity is set Actual: {}'.format(couponConfigObj['ownerValidity']))

    @pytest.mark.parametrize('description, ownerValues', [
        ('GetCouponConfig and GetAllCouponConfig by ownerBy & ownedId', [1, 123])])
    def test_LUCI_CF_019(self, description,ownerValues):
        configRequest = LuciObject.getCouponConfigRequest({'ownedBy' : ownerValues[0]})
        couponConfigList = self.connObj.getCouponConfiguration(configRequest)
        Assertion.constructAssertion(couponConfigList != None, 'Retrieved couponConfig from GetCouponConfig by OwnedBy')
        configRequest = LuciObject.getCouponConfigRequest({'ownerId': ownerValues[1]})
        couponConfigList = self.connObj.getCouponConfiguration(configRequest)
        Assertion.constructAssertion(couponConfigList != None, 'Retrieved couponConfig from GetCouponConfig by OwnedId')

    # description = "Get coupon details by providing OrderBy expiry date with different expiry strategy type coupon series id and user id"
    def test_LUCI_CF_SC_020(self):
        # Save Coupon Config
        couponSeriesId1 = LuciHelper.saveCouponConfigAndAssertions(self, couponConfigReq={'valid_till_date': None, 'expiry_strategy_value': 5, 'expiry_strategy_type' : 'DAYS', 'campaign_id': -1, 'series_type': 'UNDEFINED', 'owned_by': 0})[1]
        LuciHelper.claimCouponSeries(self, couponSeriesId1, [2, constant.config['campaignId'], 'CAMPAIGN'], ownerValidityDays=1)
        couponSeriesId2 = LuciHelper.saveCouponConfigAndAssertions(self, couponConfigReq={'valid_till_date': None, 'expiry_strategy_value': 5, 'expiry_strategy_type' : 'DAYS', 'campaign_id': -1, 'series_type': 'UNDEFINED', 'owned_by': 0})[1]
        LuciHelper.claimCouponSeries(self, couponSeriesId2, [2, constant.config['campaignId'], 'CAMPAIGN'], ownerValidityDays=2)
        couponSeriesId3 = LuciHelper.saveCouponConfigAndAssertions(self, couponConfigReq={'valid_till_date': None, 'expiry_strategy_value': 5, 'expiry_strategy_type': 'DAYS', 'campaign_id': -1, 'series_type': 'UNDEFINED', 'owned_by': 0})[1]
        LuciHelper.claimCouponSeries(self, couponSeriesId3, [2, constant.config['campaignId'], 'CAMPAIGN'], ownerValidityDays=3)
        couponSeriesId4 = LuciHelper.saveCouponConfigAndAssertions(self, couponConfigReq={'valid_till_date': None, 'expiry_strategy_value': 5, 'expiry_strategy_type' : 'DAYS','campaign_id': -1, 'series_type': 'UNDEFINED', 'owned_by': 0})[1]
        LuciHelper.claimCouponSeries(self, couponSeriesId4, [2, constant.config['campaignId'], 'CAMPAIGN'], ownerValidityDays=4)

        couponCode1 = LuciHelper.issueCouponAndAssertions(self, couponSeriesId1)[0]
        couponCode2 = LuciHelper.issueCouponAndAssertions(self, couponSeriesId2)[0]
        couponCode3 = LuciHelper.issueCouponAndAssertions(self, couponSeriesId3)[0]
        couponCode4 = LuciHelper.issueCouponAndAssertions(self, couponSeriesId4)[0]

        couponSearchRequest = {'orderBy': self.constructObj.orderBy['EXPIRY_DATE'], 'sort': self.constructObj.sort['DESC']}
        LuciHelper.couponSearchAndAssertion(self, [couponSeriesId1, couponSeriesId2, couponSeriesId3, couponSeriesId4], couponSearchRequest, [couponCode4, couponCode3, couponCode2, couponCode1])

        couponSearchRequest = {'orderBy': self.constructObj.orderBy['EXPIRY_DATE'], 'sort': self.constructObj.sort['ASC']}
        LuciHelper.couponSearchAndAssertion(self, [couponSeriesId1, couponSeriesId2, couponSeriesId3, couponSeriesId4], couponSearchRequest, [couponCode1, couponCode2, couponCode3, couponCode4])

# description = "Get coupon details by providing OrderBy expiry date with different expiry strategy type coupon series id and user id"
    def test_LUCI_CF_SC_021(self):
        # Save Coupon Config
        couponSeriesId1 = LuciHelper.saveCouponConfigAndAssertions(self, couponConfigReq={'valid_till_date': Utils.getTime(days=1, milliSeconds=True), 'expiry_strategy_value': 5, 'expiry_strategy_type' : 'DAYS', 'campaign_id': -1, 'series_type': 'UNDEFINED', 'owned_by': 0})[1]
        LuciHelper.claimCouponSeries(self, couponSeriesId1, [2, constant.config['campaignId'], 'CAMPAIGN'], ownerValidityDays=2)
        couponSeriesId2 = LuciHelper.saveCouponConfigAndAssertions(self, couponConfigReq={'valid_till_date': Utils.getTime(days=2, milliSeconds=True), 'expiry_strategy_value': 5, 'expiry_strategy_type' : 'DAYS', 'campaign_id': -1, 'series_type': 'UNDEFINED', 'owned_by': 0})[1]
        LuciHelper.claimCouponSeries(self, couponSeriesId2, [2, constant.config['campaignId'], 'CAMPAIGN'], ownerValidityDays=3)
        couponSeriesId3 = LuciHelper.saveCouponConfigAndAssertions(self, couponConfigReq={'valid_till_date': None, 'expiry_strategy_value': 5, 'expiry_strategy_type': 'DAYS', 'campaign_id': -1, 'series_type': 'UNDEFINED', 'owned_by': 0})[1]
        LuciHelper.claimCouponSeries(self, couponSeriesId3, [2, constant.config['campaignId'], 'CAMPAIGN'], ownerValidityDays=3)
        couponSeriesId4 = LuciHelper.saveCouponConfigAndAssertions(self, couponConfigReq={'valid_till_date': None, 'expiry_strategy_value': 5, 'expiry_strategy_type' : 'DAYS','campaign_id': -1, 'series_type': 'UNDEFINED', 'owned_by': 0})[1]
        LuciHelper.claimCouponSeries(self, couponSeriesId4, [2, constant.config['campaignId'], 'CAMPAIGN'], ownerValidityDays=4)

        couponCode1 = LuciHelper.issueCouponAndAssertions(self, couponSeriesId1)[0]
        couponCode2 = LuciHelper.issueCouponAndAssertions(self, couponSeriesId2)[0]
        couponCode3 = LuciHelper.issueCouponAndAssertions(self, couponSeriesId3)[0]
        couponCode4 = LuciHelper.issueCouponAndAssertions(self, couponSeriesId4)[0]

        couponSearchRequest = {'orderBy': self.constructObj.orderBy['EXPIRY_DATE'], 'sort': self.constructObj.sort['DESC']}
        LuciHelper.couponSearchAndAssertion(self, [couponSeriesId1, couponSeriesId2, couponSeriesId3, couponSeriesId4], couponSearchRequest, [couponCode4, couponCode3, couponCode2, couponCode1])

        couponSearchRequest = {'orderBy': self.constructObj.orderBy['EXPIRY_DATE'], 'sort': self.constructObj.sort['ASC']}
        LuciHelper.couponSearchAndAssertion(self, [couponSeriesId1, couponSeriesId2, couponSeriesId3, couponSeriesId4], couponSearchRequest, [couponCode1, couponCode2, couponCode3, couponCode4])