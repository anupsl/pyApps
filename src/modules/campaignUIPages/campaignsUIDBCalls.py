from src.Constant.constant import constant
from src.utilities.dbhelper import dbHelper
from src.utilities.logger import Logger
from src.utilities.mongoHelper import MongoHelper
import json, time

class DBCallsCampaigns():
    
    @staticmethod
    def getLoyaltyUserInfo(numberOfUsers):
        query = "select u.id,u.firstname,u.lastname,u.mobile,u.email,l.external_id from users u,loyalty l where u.id=l.user_id and u.email like 'iris_automation%' and u.org_id = " + str(constant.config['orgId']) + " and l.publisher_id = " + str(constant.config['orgId']) + " order by u.id desc limit " + str(numberOfUsers)
        if constant.config['os'] == 'windows':
            result = dbHelper.queryAPITester(query, 'user_management', constant.config['apiTesterDB'][constant.config['shard']])
        else:
            result = dbHelper.queryDB(query, 'user_management')
        return result
    
    @staticmethod
    def getShardGettingUsed():
        query = 'select name from shard where id = (select shard_id from org_shard_mapping where org_id = {} and policy_id =2)'.format(constant.config['orgId'])
        if constant.config['os'] == 'windows':
            result = dbHelper.queryAPITester(query, 'shard_manager', constant.config['apiTesterDB']['meta'])
        else:
            result = dbHelper.queryDB(query, 'shard_manager')
        return 'shard{}'.format(result[0][0])

    @staticmethod
    def getCampaignIdFromCampaignName(campaignName):
        query = "select id from campaigns_base where name ='" + str(campaignName) + "'"
        if constant.config['os'] == 'windows':
            result = dbHelper.queryAPITester(query, 'campaigns', constant.config['apiTesterDB'][constant.config['shard']])[0]
        else:
            result = dbHelper.queryDB(query, 'campaigns')[0]
        return str(result[0])

    @staticmethod
    def getGroupDetail(campaignId, listName):
        query = "select id from group_details where org_id ={} and campaign_id={} and group_label='{}'".format(constant.config['orgId'], campaignId, listName)
        result = dbHelper.queryAPITester(query, 'campaign_meta_details', constant.config['apiTesterDB']['campaign_shard'])[0]
        return str(result[0])
    
    @staticmethod
    def getGroupVersionDetail(campaignId, groupId,versionNumber=0):
        query = "select id,target_type from group_version_details where org_id={} and campaign_id={} and group_id={} and version_number = {}".format(constant.config['orgId'], campaignId, groupId,versionNumber)
        result = dbHelper.queryAPITester(query, 'campaign_meta_details', constant.config['apiTesterDB']['campaign_shard'])
        return result
        
    @staticmethod
    def getCommunicationDetailsWithListDetails(campaignId, groupVersionId):
        query = "select state,message_queue_id from communication_details where org_id={} and campaign_id={} and recipient_list_id={} order by id desc limit 1".format(constant.config['orgId'], campaignId, groupVersionId)
        result = None
        for numberOfTries in range(5):
            time.sleep(5)
            result = dbHelper.queryAPITester(query, 'veneno', constant.config['apiTesterDB']['campaign_shard'])[0]
            if str(result[0]) == 'CLOSED':
                break
        return { 'state' : str(result[0]) , 'message_queue_id' : str(result[1]) }
    
    @staticmethod
    def getCommunicationDetails(campaignId):
        query = "select id,bucket_id,target_type,expected_delivery_count,overall_recipient_count,state from communication_details where org_id={} and campaign_id={} order by id desc limit 1".format(constant.config['orgId'], campaignId)
        time.sleep(5)
        result = dbHelper.queryDB(query, 'veneno')
        return result[0]
    
    @staticmethod
    def getCommunicationDetailsForPreviewAndTest(channel='SMS'):
        query = "select state,message_queue_id from communication_details where org_id = {} and campaign_id = -30 and communication_type = '{}' order by id desc limit 1".format(constant.config['orgId'], channel.upper())
        result = None
        for numberOfTries in range(5):
            time.sleep(5)
            result = dbHelper.queryAPITester(query, 'veneno', constant.config['apiTesterDB']['campaign_shard'])[0]
            if str(result[0]) == 'CLOSED':
                break
        return {'state' :str(result[0]), 'message_queue_id' : str(result[1])}
    
    @staticmethod
    def getTemplateDetails(channel, templateName):
        port = constant.config['INTOUCH_DB_MONGO_MASTER']
        if channel.lower() == 'wechat': 
            query = {'name':{'$regex':'.*' + templateName + '.*'}, 'isActive':True, 'type':channel.upper()}
        else:
            query = {'name':templateName, 'isActive':True, 'type':channel.upper()}
        return MongoHelper.findDocuments('creatives_mongo', 'templates', port, query, limit=2)
        
    @staticmethod
    def getTimelineDB(timelineName):
        query = "select database_name,campaign_id,org_config_id from sharding_config where org_id = {} and org_config_name = '{}'".format(constant.config['orgId'], timelineName)
        if constant.config['os'] == 'windows':
            result = dbHelper.queryAPITester(query, 'temporal_engine_bootstrap', constant.config['apiTesterDB']['timeline'])
        else:
            result = dbHelper.queryDB(query, 'temporal_engine_bootstrap')
        return result[0]
        
    @staticmethod
    def getUserInitializedInTimeline(timelineDB):
        query = "select count(*) from user_initialization_history"
        if constant.config['os'] == 'windows':
            result = dbHelper.queryAPITester(query, timelineDB, constant.config['apiTesterDB']['timeline'])
        else:
            result = dbHelper.query(query, timelineDB, constant.config['TIMELINE_DB_MYSQL'][0])
        return result[0][0]
    
    @staticmethod
    def getActivityContextHistory(timelineDB, milestoneId='2'):
        query = "select user_id,status,status_context from activity_context_history where milestone_id = {}".format(milestoneId)
        if constant.config['os'] == 'windows':
            result = dbHelper.queryAPITester(query, timelineDB, constant.config['apiTesterDB']['timeline'])
        else:
            result = dbHelper.query(query, timelineDB, constant.config['TIMELINE_DB_MYSQL'][0])
        return result
    
    @staticmethod
    def getCurrentMilestoneContext(timelineDB, milestoneId='2'):
        query = "select user_id from current_milestone_contexts where milestone_id ={} and status = 'ERROR';".format(milestoneId)
        if constant.config['os'] == 'windows':
            result = dbHelper.queryAPITester(query, timelineDB, constant.config['apiTesterDB']['timeline'])
        else:
            result = dbHelper.query(query, timelineDB, constant.config['TIMELINE_DB_MYSQL'][0])
        return result
    
    @staticmethod
    def markCampaignAsInactive(org_config_id):
        query = "update sharding_config set status = 'INACTIVE' where org_id ={} and org_config_id = {}".format(constant.config['orgId'],org_config_id)
        dbHelper.query(query, 'temporal_engine_bootstrap', constant.config['TIMELINE_DB_MYSQL'][0])
        
    @staticmethod
    def getInboxDetails(bucketId, messageId):
        query = "select recipient_id,nsadmin_id from inboxes_{} where message_id = {}".format(bucketId, messageId)
        if constant.config['os'] == 'windows':
            result = dbHelper.queryAPITester(query, 'veneno_data_details', constant.config['apiTesterDB']['campaign_shard'])
        else:
            result = dbHelper.queryDB(query, 'veneno_data_details')
        return result
    
    @staticmethod
    def getSkippedDetails(bucketId, messageId):
        query = "select recipient_id,error_description from skipped_recipients_{} where message_id = {}".format(bucketId, messageId)
        if constant.config['os'] == 'windows':
            result = dbHelper.queryAPITester(query, 'veneno_data_details', constant.config['apiTesterDB']['campaign_shard'])
        else:
            result = dbHelper.queryDB(query, 'veneno_data_details')
        return result

    @staticmethod
    def getOTP():
        query = 'SELECT otp from otp_history where loggable_user_id = ' + constant.config['userId'] + ' order by id desc limit 1'
        result = dbHelper.queryDB(query, "authentication")[0]
        if len(result) != 0:
            return result[0]
        else:
            Logger.log('OTP Not Generated')