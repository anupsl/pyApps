from src.Constant.constant import constant
from src.utilities.logger import Logger
from src.utilities.assertion import Assertion
from src.utilities.randValues import randValues
from src.modules.iris.construct import construct
from src.modules.iris.campaigns import campaigns
from src.modules.iris.dbCallsCampaign import dbCallsCampaign
from src.modules.iris.dbCallsCoupons import dbCallsCoupons
from src.utilities.utils import Utils
import json, time

class coupons():
    
    @staticmethod
    def createCoupons(payloadData={}, campaignId=None, campaignType=[], process='update', key=True, timeout=5.0):     
        updateDefault = False
        if campaignId == None:    
            if len(campaignType) == 0:
                response, payload = campaigns.createCampaign({'name':'IRIS_COUPON' + randValues.randomString(5) + str(int(time.time() * 100000)), 'goalId':constant.irisGenericValues['goalId'], 'objectiveId':constant.irisGenericValues['objectiveId']})   
            else:
                response, payload = campaigns.createCampaign({}, campaignTypeParams=[campaignType[0], campaignType[1]])   
                updateDefault = True
                
            if response['statusCode'] == 200:
                campaignId = response['json']['entity']['campaignId']
            else:
                Assertion.constructAssertion(False, 'Error : While Creating Campaign , Status Code : {}'.format(response['statusCode']))
               
        Logger.log('CampaignId getting used to create list :', campaignId)
        
        if key:
            createCouponConstructedEndPoint = construct.constructUrl('createcoupon')
            payload = construct.constructBody(payloadData, process, 'createcoupon')
            payload.update({'campaignId':campaignId})
            try:
                response = Utils.makeRequest(url=createCouponConstructedEndPoint, data=payload, auth=construct.constructAuthenticate(),  headers=construct.constructHeaders(), method='POST')
                if updateDefault:
                    constant.campaignDefaultValues[campaignType[0]][campaignType[1]]['Coupon'].update({'response':response, 'payload':payload})
            except:
                return {}, payload, campaignId
            
            return construct.constructResponse(response), payload, campaignId
        else:
            couponResponse = constant.campaignDefaultValues[campaignType[0]][campaignType[1]]['Coupon']['response']
            couponPayload = constant.campaignDefaultValues[campaignType[0]][campaignType[1]]['Coupon']['payload']
            
            if len(couponResponse) == 0 or len(couponPayload) == 0:
                coupons.createCoupons(payloadData, campaignId, campaignType, process, key=True)
            else:
                return couponResponse, couponPayload, campaignId

    @staticmethod
    def assertCreateCoupon(response, expectedStatusCode, expectedErrorCode=2001, expectedErrorMessage='Unexpected error : null'):
        Logger.log('Response sent to be asserted :', response)
        if response['constructed'].lower() == 'pass':
            if expectedStatusCode >= 200 and expectedStatusCode <= 300: 
                Assertion.constructAssertion(response['statusCode'] == int(expectedStatusCode), 'Matching statusCode actual :{},expected :{}'.format(response['statusCode'], expectedStatusCode))
                Assertion.constructAssertion(response['json']['entity']['voucherSeriesId'] > 0, 'voucherSeriesId should always be greater then zero')
                if len(response['json']['warnings']) > 0:
                    Logger.log('There was a Warning while Creating Campaign :', response['json']['warnings'])
            else:
                errorReturned = response['json']['errors'][0]
                Logger.log('Validating Failed Request Data as Expected:', errorReturned)
                Assertion.constructAssertion(response['statusCode'] == int(expectedStatusCode), 'Matching statusCode actual :{},expected :{}'.format(response['statusCode'], int(expectedStatusCode)))
                Assertion.constructAssertion(errorReturned['code'] == expectedErrorCode, 'Matching Error Code ,actual:{} and expected:{}'.format(errorReturned['code'], expectedErrorCode))
                Assertion.constructAssertion(errorReturned['status'] == False, 'Matching error status')
                Assertion.constructAssertion(errorReturned['message'] == expectedErrorMessage, 'Matching Error Message ,actual:{} and expected:{}'.format(errorReturned['message'], expectedErrorMessage))          
        else:
            assert False, 'Constructed Body has Failed due to Exception so no Validation'
            
    @staticmethod
    def assertCreateCouponDbCalls(response, payload, campaignId):
        voucherSeriesInfo = dbCallsCoupons.getVoucherSeriesInfoBasedOnId(response['json']['entity']['voucherSeriesId'])
        Assertion.constructAssertion(int(voucherSeriesInfo['campaign_id']) == int(campaignId), 'Matching Campaign id in Voucher Series')
        Assertion.constructAssertion(voucherSeriesInfo['series_type'] == 'CAMPAIGN' , 'Matching Series Type in DB is set as Campaign')
        Assertion.constructAssertion(voucherSeriesInfo['description'] == payload['couponSeriesTag'] , 'Matching Coupon Name in DB :{} and passed in payalod :{}'.format(voucherSeriesInfo['description'], payload['couponSeriesTag']))
        Assertion.constructAssertion(voucherSeriesInfo['discount_on'] == payload['discountOn'] , 'Matching discountOn in Db :{} and in payalod :{}'.format(voucherSeriesInfo['discount_on'], payload['discountOn']))
        Assertion.constructAssertion(voucherSeriesInfo['discount_type'] == payload['discountType'] , 'Matching Discount Type in DB :{} and passed in Payload :{}'.format(voucherSeriesInfo['discount_type'], payload['discountType']))
        Assertion.constructAssertion(voucherSeriesInfo['discount_value'] == payload['discountValue'] , 'Matching Discount Value in DB :{} and passed :{}'.format(voucherSeriesInfo['discount_value'], payload['discountValue']))
        if 'redeemableTillIds' in payload : Assertion.constructAssertion(voucherSeriesInfo['redeem_store_type'] == 'redeemable_stores' , 'MAtching redeem store type as redeemable_stores')
       
        if payload['couponLimit']['type'] == 'UNLIMITED':
            Assertion.constructAssertion(voucherSeriesInfo['max_create'] == -1 , 'Matching max_create value in Db as -1 as Coupon Limit is Unlimited')
        else:
            Assertion.constructAssertion(voucherSeriesInfo['max_create'] == payload['couponLimit']['limit'] , 'Matching max_create value in Db :{} and passed in payload as limit :{}'.format(voucherSeriesInfo['max_create'], payload['couponLimit']['limit']))
        
        CampaignsInfo = dbCallsCampaign.getCampaignBaseFromCampaignId(campaignId)
        Assertion.constructAssertion(int(CampaignsInfo['voucher_series_id']) == int(response['json']['entity']['voucherSeriesId']), 'Matching Voucher Series ID Set in Campaign is Correct')
        Assertion.constructAssertion(CampaignsInfo['end_date'].split(' ')[0] == voucherSeriesInfo['valid_till_date'], 'Matching Voucher Series ID Set in Campaign is Correct')
        
    @staticmethod
    def getTillFromParentEntity(parentChild, entityId):
        Logger.log('Parent Id :', entityId)
        if entityId not in parentChild:
            return entityId
        else:
            return coupons.getTillFromParentEntity(parentChild, parentChild[entityId].split(',')[0])
        
