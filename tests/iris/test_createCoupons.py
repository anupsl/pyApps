import pytest, time, Queue, pytest_ordering
from threading import Thread
from src.Constant.constant import constant
from src.utilities.assertion import Assertion
from src.utilities.logger import Logger
from src.utilities.randValues import randValues
from src.modules.iris.coupons import coupons
from src.modules.iris.campaigns import campaigns
from src.modules.iris.construct import construct
from src.modules.iris.dbCallsCoupons import dbCallsCoupons
from src.modules.iris.dbCallsCampaign import dbCallsCampaign
from src.modules.arya.auth  import auth

@pytest.mark.run(order=2)
class Test_CreateCoupons():

    def setup_method(self, method):
        Logger.logMethodName(method.__name__)
    
    @pytest.mark.parametrize('description,payloadData', [
        ('Unlimited Coupon', {'couponLimit':{'limit':0, 'type':'UNLIMITED'}, 'discountOn':'BILL', 'discountType':'ABS', 'discountValue':10}),
        ('Limited Coupon', {'couponLimit':{'limit':10, 'type':'LIMITED'}, 'discountOn':'BILL', 'discountType':'ABS', 'discountValue':10}),
        ])
    def test_createCoupon_Sanity(self, description, payloadData):
        response, payload, campaignId = coupons.createCoupons(payloadData=payloadData)
        coupons.assertCreateCoupon(response, 200)
        coupons.assertCreateCouponDbCalls(response, payload, campaignId)
    
    @pytest.mark.parametrize('description,payloadData', [
        ('TillIds as None in List', {'couponLimit':{'limit':0, 'type':'UNLIMITED'}, 'discountOn':'BILL', 'discountType':'ABS', 'discountValue':10, 'redeemableTillIds':None, 'issuableTillIds':None}),
        ])    
    def test_createCoupon_TillIds(self, description, payloadData):
        response, payload, campaignId = coupons.createCoupons(payloadData=payloadData)
        coupons.assertCreateCoupon(response, 200)
        coupons.assertCreateCouponDbCalls(response, payload, campaignId)
    
    @pytest.mark.parametrize('description,payloadData', [
        ('Limited Discount On ITEM with ABS', {'couponLimit':{'limit':10, 'type':'LIMITED'}, 'discountOn':'ITEM', 'discountType':'ABS', 'discountValue':10}),
        ('Limited Discount On ITEM with PERC', {'couponLimit':{'limit':10, 'type':'LIMITED'}, 'discountOn':'ITEM', 'discountType':'PERC', 'discountValue':10}),
        ('Limited Discount On BILL with ABS', {'couponLimit':{'limit':10, 'type':'LIMITED'}, 'discountOn':'BILL', 'discountType':'ABS', 'discountValue':10}),
        ('Limited Discount On BILL with PERC', {'couponLimit':{'limit':10, 'type':'LIMITED'}, 'discountOn':'BILL', 'discountType':'PERC', 'discountValue':10}),
        ('Unlimited Discount On ITEM with ABS', {'couponLimit':{'limit':0, 'type':'UNLIMITED'}, 'discountOn':'ITEM', 'discountType':'ABS', 'discountValue':10}),
        ('Unlimited Discount On ITEM with PERC', {'couponLimit':{'limit':0, 'type':'UNLIMITED'}, 'discountOn':'ITEM', 'discountType':'PERC', 'discountValue':10}),
        ('Unlimited Discount On BILL with ABS', {'couponLimit':{'limit':0, 'type':'UNLIMITED'}, 'discountOn':'BILL', 'discountType':'ABS', 'discountValue':10}),
        ('Unlimited Discount On BILL with PERC', {'couponLimit':{'limit':0, 'type':'UNLIMITED'}, 'discountOn':'BILL', 'discountType':'PERC', 'discountValue':10}),
        ('Unlimited Campaign with Limited Numbers ', {'couponLimit':{'limit':10, 'type':'UNLIMITED'}, 'discountOn':'BILL', 'discountType':'ABS', 'discountValue':10}),
        ('Boundary value for Limit ', {'couponLimit':{'limit':99999999, 'type':'LIMITED'}, 'discountOn':'BILL', 'discountType':'ABS', 'discountValue':10})
        ])
    def test_createCoupon_Variation(self, description, payloadData):
        response, payload, campaignId = coupons.createCoupons(payloadData=payloadData)
        coupons.assertCreateCoupon(response, 200)
        coupons.assertCreateCouponDbCalls(response, payload, campaignId)
     
    @pytest.mark.parametrize('description,payloadData', [
        ('Unlimited Coupon with Till Ids', {'couponLimit':{'limit':0, 'type':'UNLIMITED'}, 'discountOn':'BILL', 'discountType':'ABS', 'discountValue':10}),
        ])
    def test_createCoupon_tillIds_all(self, description, payloadData):
        tillIdList = map(int, dbCallsCoupons.getEntityIdWithType()['TILL'].split(','))
        payloadData.update({'issuableTillIds':tillIdList, 'redeemableTillIds':tillIdList})
        Logger.log('PayloadDate Including till list :', payloadData)
        response, payload, campaignId = coupons.createCoupons(payloadData=payloadData)
        coupons.assertCreateCoupon(response, 200)
        coupons.assertCreateCouponDbCalls(response, payload, campaignId)
    
    @pytest.mark.parametrize('description,payloadData', [
        ('Unlimited Coupon with only 1 redeemable id', {'couponLimit':{'limit':0, 'type':'UNLIMITED'}, 'discountOn':'BILL', 'discountType':'ABS', 'discountValue':10}),
        ]) 
    def test_createCoupon_tillIds_lessReedemableTills(self, description, payloadData):
        tillIdList = map(int, dbCallsCoupons.getEntityIdWithType()['TILL'].split(','))
        payloadData.update({'issuableTillIds':tillIdList, 'redeemableTillIds':[tillIdList[0]]})
        Logger.log('PayloadDate Including till list :', payloadData)
        response, payload, campaignId = coupons.createCoupons(payloadData=payloadData)
        coupons.assertCreateCoupon(response, 200)
        coupons.assertCreateCouponDbCalls(response, payload, campaignId)

    @pytest.mark.parametrize('description,payloadData', [
        ('Unlimited Coupon with Different reedem and issuable tills', {'couponLimit':{'limit':0, 'type':'UNLIMITED'}, 'discountOn':'BILL', 'discountType':'ABS', 'discountValue':10}),
        ])
    def test_createCoupon_tillIds_moreReedemableTillsThanIssuableTills(self, description, payloadData):
        tillIdList = map(int, dbCallsCoupons.getEntityIdWithType()['TILL'].split(','))
        payloadData.update({'redeemableTillIds':tillIdList, 'issuableTillIds':[tillIdList[0]]})
        Logger.log('PayloadDate Including till list :', payloadData)
        response, payload, campaignId = coupons.createCoupons(payloadData=payloadData)
        coupons.assertCreateCoupon(response, 200)
        
    @pytest.mark.parametrize('description,payloadData', [
        ('Unlimited Coupon', {'couponLimit':{'limit':0, 'type':'UNLIMITED'}, 'discountOn':'BILL', 'discountType':'ABS', 'discountValue':10}),
        ])
    def test_createCoupon_tillIds_differentIssuableAndReedemableTills(self, description, payloadData):
        tillIdList = map(int, dbCallsCoupons.getEntityIdWithType()['TILL'].split(','))
        payloadData.update({'redeemableTillIds':[tillIdList[1]], 'issuableTillIds':[tillIdList[0]]})
        Logger.log('PayloadDate Including till list :', payloadData)
        response, payload, campaignId = coupons.createCoupons(payloadData=payloadData)
        coupons.assertCreateCoupon(response, 200)

    @pytest.mark.parametrize('description,payloadData', [
        ('Multiple Coupon in Same Campaign', {'couponSeriesTag':'IRIS_COUPON' + str(int(time.time())), 'couponLimit':{'limit':0, 'type':'UNLIMITED'}, 'discountOn':'BILL', 'discountType':'ABS', 'discountValue':10}),
        ])
    def test_createCoupon_MultipleCouponInSameCampaign(self, description, payloadData):
        response, payload, campaignId = coupons.createCoupons(payloadData=payloadData)
        coupons.assertCreateCoupon(response, 200)
        failedResponse, failedCasepayload, campaignId = coupons.createCoupons(payloadData=payloadData, campaignId=campaignId)
        coupons.assertCreateCoupon(failedResponse, 400, 4005, 'Coupon Exists Exception :  Coupon Already Exists for this Campaign ')
        coupons.assertCreateCouponDbCalls(response, payload, campaignId)
        
    @pytest.mark.parametrize('description,payloadData,statusCode,errorCode,errorMessage', [
        ('Empty CouponName', {'couponSeriesTag':'', 'couponLimit':{'limit':0, 'type':'UNLIMITED'}, 'discountOn':'BILL', 'discountType':'ABS', 'discountValue':10}, 400, 100, 'Invalid request : Coupon series tag must have at least one letter.'),
        ('CouponName more than 160 Character', {'couponSeriesTag':'IRIS_COUPON_' + str(randValues.randomInteger(170)), 'couponLimit':{'limit':0, 'type':'UNLIMITED'}, 'discountOn':'BILL', 'discountType':'ABS', 'discountValue':10}, 400, 100, 'Invalid request : Coupon series tag should be less than 160 characters.'),
        ('CouponName with Special Character', {'couponSeriesTag':'#$$%', 'couponLimit':{'limit':0, 'type':'UNLIMITED'}, 'discountOn':'BILL', 'discountType':'ABS', 'discountValue':10}, 400, 100, 'Invalid request : Coupon series tag must have at least one letter.'),
        ('Wrong Coupon Limit Type', {'couponSeriesTag':'IRIS_COUPON_LIMITTYPE_WRONG', 'couponLimit':{'limit':0, 'type':'WRONG'}, 'discountOn':'BILL', 'discountType':'ABS', 'discountValue':10}, 400, 100, 'Invalid request : Valid Coupon limit type is required.'),
        ('Wrong Discount On', {'couponSeriesTag':'IRIS_COUPON_DISCOUNTON_WRONG', 'couponLimit':{'limit':0, 'type':'UNLIMITED'}, 'discountOn':'WRONG', 'discountType':'ABS', 'discountValue':10}, 400, 100, 'Invalid request : Discount on is required.'),
        ('Wrong Discount Type', {'couponSeriesTag':'IRIS_COUPON_DISCOUNTON_WRONG', 'couponLimit':{'limit':0, 'type':'UNLIMITED'}, 'discountOn':'BILL', 'discountType':'WRONG', 'discountValue':10}, 400, 100, 'Invalid request : Discount type is required.'),
        ('Discount Value More than 100 PERC', {'couponSeriesTag':'IRIS_COUPON_MORETHAN1000PERC', 'couponLimit':{'limit':0, 'type':'UNLIMITED'}, 'discountOn':'BILL', 'discountType':'PERC', 'discountValue':999}, 400, 100, 'Invalid request : Invalid Discount Value.')
        ])
    def test_createCoupon_NegativeCases_Variation(self, description, payloadData, statusCode, errorCode, errorMessage):
        response, payload, campaignId = coupons.createCoupons(payloadData=payloadData, campaignType=['LIVE', 'ORG'])
        coupons.assertCreateCoupon(response, statusCode, errorCode, errorMessage)
            
    @pytest.mark.parametrize('description,payloadData', [
        ('Wrong CampaignId ', {'couponSeriesTag':'IRIS_COUPON_WRONG_CAMPAIGNID', 'couponLimit':{'limit':0, 'type':'UNLIMITED'}, 'discountOn':'BILL', 'discountType':'ABS', 'discountValue':10})
        ])
    def test_createCoupon_wrongCampaignId(self, description, payloadData):
        response, payload, campaignId = coupons.createCoupons(payloadData=payloadData, campaignId=0)
        coupons.assertCreateCoupon(response, 400, 100, 'Invalid request : Campaign id should be a positive value.')
        
    def test_createCoupon_campaignIdNotInPassedOrg(self):
        campaignResponse, campaignPayload = campaigns.createCampaign({'name':'IRIS_' + str(int(time.time())), 'goalId':constant.irisGenericValues['goalId'], 'objectiveId':constant.irisGenericValues['objectiveId']})
        previousOrgId = construct.updateOrgId(0)
        try:
            response, payload, campaignId = coupons.createCoupons(campaignId=campaignResponse['json']['entity']['campaignId'])
            coupons.assertCreateCoupon(response, 400, 1007, 'Campaign Id Exception : Invalid Campaign Id Passed {}'.format(campaignId))
        except AssertionError, exp:
            Assertion.constructAssertion(False, exp)
        finally:
            construct.updateOrgId(int(previousOrgId))

    @pytest.mark.parametrize('description,fieldToPop,statusCode,errorCode,errorMessage', [
        ('Poping:couponSeriesTag', 'couponSeriesTag', 400, 100, 'Invalid request : Coupon series tag is required.'),
        ('Poping:couponSeriesTag', 'couponLimit', 400, 100, 'Invalid request : Coupon limit is required.'),
        ('Poping:couponSeriesTag', 'discountOn', 400, 100, 'Invalid request : Discount on is required.'),
        ('Poping:couponSeriesTag', 'discountType', 400, 100, 'Invalid request : Discount type is required.'),
        ('Poping:couponSeriesTag', 'discountValue', 400, 100, 'Invalid request : Discount value is required.')
        ])    
    def test_createCoupon_popMandatoryFields(self, description, fieldToPop, statusCode, errorCode, errorMessage):
        response, payload, campaignId = coupons.createCoupons(fieldToPop, process='pop')
        coupons.assertCreateCoupon(response, statusCode, errorCode, errorMessage)
         
    @pytest.mark.parametrize('description,payloadData', [
        ('Unlimited Coupon Timeout', {'couponLimit':{'limit':0, 'type':'UNLIMITED'}, 'discountOn':'BILL', 'discountType':'ABS', 'discountValue':10}),
        ])
    def test_createCoupon_Timeout(self, description, payloadData):
        response, payload, campaignId = coupons.createCoupons(payloadData=payloadData, timeout=0.0001)
        time.sleep(5)
        campaignsInfo = dbCallsCampaign.getCampaignBaseFromCampaignId(campaignId)
        Assertion.constructAssertion(int(campaignsInfo['voucher_series_id']) != -1, 'Checking Even After Timeout Voucher Series is Created with VoucherSeriesId :{}'.format(campaignsInfo['voucher_series_id']))
    
    @pytest.mark.parametrize('description,payloadData', [
        ('Multiple Coupons in Same Campaign', {'couponLimit':{'limit':0, 'type':'UNLIMITED'}, 'discountOn':'BILL', 'discountType':'ABS', 'discountValue':10}),
        ])    
    def test_createCoupon_SameCampaignSameName(self, description, payloadData):
        response, payload, campaignId = coupons.createCoupons(payloadData=payloadData)
        coupons.assertCreateCoupon(response, 200)
        secondResponse, secondPayload, campaignId = coupons.createCoupons(payloadData=payloadData, campaignId=campaignId)
        coupons.assertCreateCoupon(secondResponse, 400, 4005, 'Coupon Exists Exception :  Coupon Already Exists for this Campaign ')
    
    """ @Different Users """    
    
    @pytest.mark.parametrize('description,payloadData', [
        ('ConceptLevelUser with correct Till Ids', {'couponLimit':{'limit':0, 'type':'UNLIMITED'}, 'discountOn':'BILL', 'discountType':'ABS', 'discountValue':10}),
        ])    
    def test_createCoupon_tillsFromSameConcept_userConceptLevel(self, description, payloadData):
        parentChild = dbCallsCoupons.getParentChildRelationOnEntities()
        Logger.log('Parent and Child Map :', parentChild)
        try:
            if construct.updateAuthenticate('concept') == True:
                conceptId = str(auth.authLogin()['json']['user']['aryaUserRoles']['CONCEPT'][0]['entityId'])
                tillId = coupons.getTillFromParentEntity(parentChild, conceptId)
                payloadData.update({'issuableTillIds':[tillId], 'redeemableTillIds':[tillId]})
                Logger.log('PayloadDate Including till list :', payloadData)
                response, payload, campaignId = coupons.createCoupons(payloadData=payloadData)
                coupons.assertCreateCoupon(response, 200)
                coupons.assertCreateCouponDbCalls(response, payload, campaignId)
            else:
                Assertion.constructAssertion(False, 'Marking as Failed as Authenticate was not Properly Updated')
        except AssertionError, exp:
            Assertion.constructAssertion(False , 'Case Failed Due to :{}'.format(exp))
        finally:
            construct.updateAuthenticate()
            Logger.log('Finally Admin User :{} Set to Authenticate'.format(constant.config['intouchUsername']))
 
        
    @pytest.mark.parametrize('description,payloadData', [
        ('Multiple Coupons in Same Campaign', {'couponLimit':{'limit':0, 'type':'UNLIMITED'}, 'discountOn':'BILL', 'discountType':'ABS', 'discountValue':10}),
        ])    
    def test_createCoupon_wrongIssuableTillId_userConceptLevel(self, description, payloadData):
        parentChild = dbCallsCoupons.getParentChildRelationOnEntities()
        Logger.log('Parent and Child Map :', parentChild)
        try:
            if construct.updateAuthenticate('concept') == True:
                conceptId = str(auth.authLogin()['json']['user']['aryaUserRoles']['CONCEPT'][0]['entityId'])
                tillId = coupons.getTillFromParentEntity(parentChild, conceptId)
                payloadData.update({'issuableTillIds':[conceptId], 'redeemableTillIds':[tillId]})
                Logger.log('PayloadDate Including till list :', payloadData)
                response, payload, campaignId = coupons.createCoupons(payloadData=payloadData)
                coupons.assertCreateCoupon(response, 400, 4004, 'Coupon Request Body Violation Exception :  Invalid set of issuable till ids.')
            else:
                Assertion.constructAssertion(False, 'Marking as Failed as Authenticate was not Properly Updated')
        except AssertionError, exp:
            Assertion.constructAssertion(False , 'Case Failed Due to :{}'.format(exp))
        finally:
            construct.updateAuthenticate()
            Logger.log('Finally Admin User :{} Set to Auth :'.format(constant.config['intouchUsername']))
 
    @pytest.mark.parametrize('description,payloadData', [
        ('Multiple Coupons in Same Campaign', {'couponLimit':{'limit':0, 'type':'UNLIMITED'}, 'discountOn':'BILL', 'discountType':'ABS', 'discountValue':10}),
        ])    
    def test_createCoupon_wrongReddemableTillId_userConceptLevel(self, description, payloadData):
        parentChild = dbCallsCoupons.getParentChildRelationOnEntities()
        Logger.log('Parent and Child Map :', parentChild)
        try:
            if construct.updateAuthenticate('concept') == True:
                conceptId = str(auth.authLogin()['json']['user']['aryaUserRoles']['CONCEPT'][0]['entityId'])
                tillId = coupons.getTillFromParentEntity(parentChild, conceptId)
                payloadData.update({'issuableTillIds':[tillId], 'redeemableTillIds':[conceptId]})
                Logger.log('PayloadDate Including till list :', payloadData)
                response, payload, campaignId = coupons.createCoupons(payloadData=payloadData)
                coupons.assertCreateCoupon(response, 400, 4004, 'Coupon Request Body Violation Exception :  Invalid set of redeemable till ids.')
            else:
                Assertion.constructAssertion(False, 'Marking as Failed as Authenticate was not Properly Updated')
        except AssertionError, exp:
            Assertion.constructAssertion(False , 'Case Failed Due to :{}'.format(exp))
        finally:
            construct.updateAuthenticate()
            Logger.log('Finally Admin User :{} Set to Auth :'.format(constant.config['intouchUsername']))
        
    @pytest.mark.parametrize('description,payloadData', [
        ('Multiple Coupons in Same Campaign', {'couponLimit':{'limit':0, 'type':'UNLIMITED'}, 'discountOn':'BILL', 'discountType':'ABS', 'discountValue':10}),
        ])    
    def test_createCoupon_passingStoreIdInTill_userConceptLevel(self, description, payloadData):
        parentChild = dbCallsCoupons.getParentChildRelationOnEntities()
        Logger.log('Parent and Child Map :', parentChild)
        try:
            if construct.updateAuthenticate('concept') == True:
                conceptId = str(auth.authLogin()['json']['user']['aryaUserRoles']['CONCEPT'][0]['entityId'])
                storeId = parentChild[conceptId].split(',')[0]
                payloadData.update({'issuableTillIds':[storeId], 'redeemableTillIds':[storeId]})
                Logger.log('PayloadDate Including till list :', payloadData)
                response, payload, campaignId = coupons.createCoupons(payloadData=payloadData)
                coupons.assertCreateCoupon(response, 400, 4004, 'Coupon Request Body Violation Exception :  Invalid set of issuable till ids.')
            else:
                Assertion.constructAssertion(False, 'Marking as Failed as Authenticate was not Properly Updated')
        except AssertionError, exp:
            Assertion.constructAssertion(False , 'Case Failed Due to :{}'.format(exp))
        finally:
            construct.updateAuthenticate()
            Logger.log('Finally Admin User :{} Set to Auth :'.format(constant.config['intouchUsername']))
        
    @pytest.mark.parametrize('description,payloadData', [
        ('Multiple Coupons in Same Campaign', {'couponLimit':{'limit':0, 'type':'UNLIMITED'}, 'discountOn':'BILL', 'discountType':'ABS', 'discountValue':10}),
        ])    
    def test_createCoupon_campaignConceptType_CouponOrgType(self, description, payloadData):     
        parentChild = dbCallsCoupons.getParentChildRelationOnEntities()
        Logger.log('Parent and Child Map :', parentChild)
        try:
            if construct.updateAuthenticate('concept') == True:
                conceptId = str(auth.authLogin()['json']['user']['aryaUserRoles']['CONCEPT'][0]['entityId'])
                createCampaignresponse, createCampaignPayload = campaigns.createCampaign({'entityId':conceptId, 'name':'IRIS_' + str(int(time.time())), 'goalId':constant.irisGenericValues['goalId'], 'objectiveId':constant.irisGenericValues['objectiveId']})   
                if construct.updateAuthenticate() == True:
                    Logger.log('PayloadDate Including till list :', payloadData)
                    response, payload, campaignId = coupons.createCoupons(payloadData=payloadData, campaignId=createCampaignresponse['json']['entity']['campaignId'])
                    coupons.assertCreateCoupon(response, 400, 4004, 'Coupon Request Body Violation Exception :  Creation of Coupon for this campaign is not allowed for this user')
            else:
                Assertion.constructAssertion(False, 'Marking as Failed as Authenticate was not Properly Updated')
        except AssertionError, exp:
            Assertion.constructAssertion(False , 'Case Failed Due to :{}'.format(exp))
        finally:
            construct.updateAuthenticate()
            Logger.log('Finally Admin User :{} Set to Auth :'.format(constant.config['intouchUsername']))
        
    
