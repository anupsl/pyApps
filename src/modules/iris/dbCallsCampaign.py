from src.Constant.constant import constant
from src.utilities.dbhelper import dbHelper

class dbCallsCampaign():
    
    @staticmethod
    def getCampaignBaseFromCampaignId(campaignId):
        query = 'select name,campaign_roi_type_id,description,type,test_control,test_percentage,ga_name,ga_source_name,voucher_series_id,end_date from campaigns_base where id =' + str(campaignId)
        result = dbHelper.queryDB(query, 'campaigns')[0]
        return {'name':result[0], 'campaign_roi_type_id':result[1], 'description':result[2], 'type':result[3], 'test_control':result[4], 'test_percentage':result[5], 'ga_name':result[6], 'ga_source_name':result[7], 'voucher_series_id':result[8], 'end_date':result[9]}
    
    @staticmethod
    def getCampaignIdFromCampaignName(campaignName):
        query = "select id from campaigns_base where name ='" + str(campaignName) + "'"
        result = dbHelper.queryDB(query, 'campaigns')[0]
        return str(result[0])
    
    @staticmethod
    def getLapsedCamapign(orgId, testControlType, test_percentage=90, campaignType='outbound'):
        if testControlType.lower() == 'custom':
            query = ' select * from campaigns_base where type = "' + campaignType + '" and org_id = ' + str(orgId) + ' and end_date < "' + str(constant.config['currentTimestamp']) + '" and test_control = "' + testControlType + '" and test_percentage =' + str(test_percentage) + ' and end_date > start_date order by id desc limit 1'
        else :
            query = ' select * from campaigns_base where type = "' + campaignType + '" and org_id = ' + str(orgId) + ' and end_date < "' + str(constant.config['currentTimestamp']) + '" and test_control = "' + testControlType + '" and end_date > start_date order by id desc limit 1'
        result = dbHelper.queryDB(query, 'campaigns')[0]
        return result[0], {'name':result[1], 'description':result[6], 'org_id':result[7], 'campaignType':result[8], 'start_date':result[9], 'end_date':result[10], 'test_control':result[20], 'test_percentage':result[21]}
        
    @staticmethod
    def getCampaignTagsFromCampaignId(campaignId):
        query = 'select id,tags from campaign_tags where campaign_id =' + str(campaignId)
        result = dbHelper.queryDB(query, 'campaigns')[0]
        return {'id':result[0], 'tags':result[1]}
    
    @staticmethod
    def getObjectiveMappingIdFromCampaignId(campaignId):
        query = 'select id,objective_type_id from objective_mapping where campaign_id=' + str(campaignId)
        result = dbHelper.queryDB(query, 'campaigns')[0]
        return {'id':result[0], 'objective_type_id':result[1]}
    
    @staticmethod
    def getValidGoalId():
        query = 'select id from campaign_roi_types limit 1'
        result = dbHelper.queryDB(query, 'campaigns')[0]
        return str(result[0])
    
    @staticmethod
    def getInvalidGoalId():
        query = 'select max(id) from campaign_roi_types limit 1'
        result = dbHelper.queryDB(query, 'campaigns')[0]
        return {'id':int(result[0]) + 1}
    
    @staticmethod
    def getValidObjectiveId():
        query = 'select id from objective_meta_details limit 1'
        result = dbHelper.queryDB(query, 'campaigns')[0]
        return str(result[0])
    
    @staticmethod
    def getInvalidObjectiveId():
        query = 'select max(id) from objective_meta_details limit 1'
        result = dbHelper.queryDB(query, 'campaigns')[0]
        return {'id':int(result[0]) + 1}
    
