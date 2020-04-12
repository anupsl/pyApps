from src.Constant.constant import constant
from src.utilities.dbhelper import dbHelper
from src.utilities.logger import Logger
import time

class dbCallsCoupons():
    
    @staticmethod
    def getVoucherSeriesInfoBasedOnId(voucherSeriesId):
        query = 'select id,campaign_id,series_type,description,discount_code,discount_on,discount_type,discount_value,redeem_store_type,valid_till_date,max_create from voucher_series where id =' + str(voucherSeriesId)
        result = dbHelper.queryDB(query, 'campaigns')[0]
        return {'id':result[0], 'campaign_id':result[1], 'series_type':result[2], 'description':result[3], 'discount_code':result[4], 'discount_on':result[5], 'discount_type':result[6], 'discount_value':result[7], 'redeem_store_type':result[8], 'valid_till_date':result[9], 'max_create':result[10]}
    
    @staticmethod
    def getVoucherSeriesIdUsingCampaignId(campaignId):
        query = 'select id from voucher_series where campaign_id =' + str(campaignId)
        result = dbHelper.queryDB(query, 'campaigns')[0]
        return str(result[0])
    
    @staticmethod
    def getEntityIdWithType(module='iris'):
        query = 'select id,type from org_entities where org_id =' + str(constant.config['orgId'])
        result = dbHelper.queryDB(query, 'masters')
        dictOfEntityTypeWithIds = {}
        for eachResult in result:
            id = eachResult[0]
            type = eachResult[1]
            if eachResult[1] in dictOfEntityTypeWithIds:
                dictOfEntityTypeWithIds.update({eachResult[1]:str(dictOfEntityTypeWithIds[eachResult[1]]) + ',' + str(eachResult[0])})
            else:
                dictOfEntityTypeWithIds[eachResult[1]] = eachResult[0]
        return dictOfEntityTypeWithIds

    @staticmethod
    def getParentChildRelationOnEntities(module='iris'):
        query = 'select parent_entity_id,child_entity_id from org_entity_relations where org_id =' + str(constant.config['orgId'])
        result = dbHelper.queryDB(query, 'masters')
        dictParentAndChildRelation = {}
        for eachResult in result:
            if str(eachResult[0]) in dictParentAndChildRelation:
                dictParentAndChildRelation.update({str(eachResult[0]):dictParentAndChildRelation[str(eachResult[0])] + ',' + str(eachResult[1])})
            else:
                dictParentAndChildRelation[str(eachResult[0])] = str(eachResult[1])    
        return dictParentAndChildRelation
    
    @staticmethod
    def getCouponCode(coupon_series_id, userId):
        query = 'select coupon_code from coupons_issued where org_id ={} and coupon_series_id = {} and issued_to = {}'.format(constant.config['orgId'], coupon_series_id, userId)
        result = None
        for numberOfTries in range(5):
            time.sleep(5)
            result = dbHelper.queryDB(query, 'luci')
            if len(result) != 0:
                break
        return result[0][0]
        
        
        
        
         
