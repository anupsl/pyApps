from src.Constant.constant import constant
from src.utilities.dbhelper import dbHelper
from src.utilities.logger import Logger
from random import randint
import json

class social_info():

	def __init__(self,groupVersionid=None,messageId=None,socialAudienceList=False,socialAdsetInfo=False,aggregationDetail=False,venenoInfo=False,venenoDataDetailsInfo=False,socialOffer=False):
		self.groupVersionid = groupVersionid
		self.messageId = messageId
		self.socialInfo = dict()
		if venenoInfo:self.venenoInfo()
		if venenoDataDetailsInfo:self.venenoDataDetailsInfo()
		if socialAudienceList :self.socialAudienceList()
		if socialAdsetInfo :self.socialAdsetInfo()
		if aggregationDetail:self.aggregationDetail()
		if socialOffer:
			self.socialOfferInfo()
			self.socialCouponUploadInfo()

	def socialAudienceList(self):
		if self.groupVersionid is None : 
			raise Exception('Group Version Id is not Passed')
		else:
			query = 'select type,account_id,remote_list_id,name,description,approximate_count,message_id from social_audience_list where org_id = {} and recipient_list_id = {} and message_id = {}'.format(constant.config['orgId'],self.groupVersionid,self.messageId)
	        result = dbHelper.queryDB(query, 'veneno')[0]
	        self.socialInfo.update({
	        	'audienceList':{
		        	'type' : result[0],
		        	'account_id' : result[1],
		        	'remote_list_id' : result[2],
		        	'name': result[3],
		        	'description' : result[4],
		        	'approximate_count' : result[5],
		        	'message_id':result[6]
	    		}
	        })

	def socialAdsetInfo(self):
		if self.messageId is None :
			raise Exception('Message Id Not Passed')
		else:
			query = 'select name,remote_adset_id,remote_campaign_id,remote_offer_id,custom_audience_id,message_id from social_adset_info where org_id = {} and message_id = {} and message_version = {}'.format(constant.config['orgId'],self.messageId,0)
	    	result = dbHelper.queryDB(query, 'veneno')[0]
	    	self.socialInfo.update({
	    		'adsetInfo':{
	    			'name':result[0],
	    			'remote_adset_id':result[1],
	    			'remote_campaign_id':result[2],
	    			'remote_offer_id':result[3],
	    			'custom_audience_id':result[4],
	    			'message_id':result[5]
	    		}
	    	})

   	def aggregationDetail(self):
   		if self.messageId is None :
   			raise Exception('Message Id Not Passed')
   		else:
   			query = "select job_type,batch_start_id,job_status from aggregation_details where org_id = {} and message_id = {}".format(constant.config['orgId'],self.messageId)
   			result = dbHelper.queryDB(query, 'veneno')
   			buildresult = dict()
   			for eachResult in result:
   				buildresult[eachResult[0]] = {'batch_start_id':eachResult[1],'job_status':eachResult[2]}
   			self.socialInfo.update({
   				'aggregationDetails': buildresult
   			})
   			 
   	def venenoInfo(self):
   		if self.messageId is None :
   			raise Exception('Message Id Not Passed')
   		else:
   			self.socialInfo.update({
   				'veneno' : {
   					'monitoringStatus':self.veneno_monitoringStatus(),
   					'communicationDetail':self.veneno_communicationDetails(),
   					'serviceDetail':self.veneno_serviceDetails(),
   					'batchDetail':self.veneno_venenoBatchDetails(),
   					'summaryReport':self.veneno_summaryReportVeneno()
   				}
   			})

	def veneno_monitoringStatus(self):
		query = "select message_version,processed_status,service_status from veneno_monitor_status where message_id = {}".format(self.messageId)
		result = dbHelper.queryDB(query, 'veneno')[0]
		return {
			'message_version':result[0],
			'processed_status':result[1],
			'service_status':result[2]
		}

	def veneno_communicationDetails(self):
		query = "select guid,message_queue_id,bucket_id,campaign_id,recipient_list_id,recipient_list_name,target_type,communication_type,expected_delivery_count,overall_recipient_count,subject,message_body,state from communication_details where org_id = {} and id = {}".format(constant.config['orgId'],self.messageId)
		result = dbHelper.queryDB(query, 'veneno')[0]
		return {
			'guid':result[0],
			'message_queue_id':result[1],
			'bucket_id':result[2],
			'campaign_id':result[3],
			'recipient_list_id':result[4],
			'recipient_list_name':result[5],
			'target_type':result[6],
			'communication_type':result[7],
			'expected_delivery_count':result[8],
			'overall_recipient_count':result[9],
			'subject':result[10],
			'message_body':result[11],
			'state':result[12]
		}

	def veneno_serviceDetails(self):
		query = 'select id,batch_type,processed_count,batches_processed,message_version from service_details where communication_message_id ={}'.format(self.messageId)
		serviceDetailResult = {}
		statusServiceDetail = True
		for numberOfTries in range(5):
		    result = dbHelper.queryDB(query, 'veneno')
		    if len(result) >= 3:
		        for eachBatchType in result:
		            serviceDetailResult[eachBatchType[1]] = {
		            	'id':eachBatchType[0], 
		            	'processed_count':eachBatchType[2], 
		            	'batches_processed':eachBatchType[3], 
		            	'message_version' : eachBatchType[4]
		            	}
		        break
		    else:
		    	time.sleep(15)
		return serviceDetailResult

	def veneno_venenoBatchDetails(self):
		query = 'select id,batch_type,status,message_version,batch_id from veneno_batch_details where message_id = {}'.format(self.messageId)
		result = dbHelper.queryDB(query, 'veneno')
		venenoBatchResult = {}
		for eachBatchType in result:
		    venenoBatchResult[eachBatchType[1]] = {'id':eachBatchType[0], 'status':eachBatchType[2], 'message_version' : eachBatchType[3], 'batch_id' : eachBatchType[4]}
		return venenoBatchResult

	def veneno_summaryReportVeneno(self):
		query = 'select id,report_type,sub_type,count,message_version from summary_report_veneno where msg_id ={}'.format(self.messageId)
		result = dbHelper.queryDB(query, 'veneno')
		venenoReportResult = {}
		for eachRowBasedOnDeliveryStatusId in result:
		    venenoReportResult[eachRowBasedOnDeliveryStatusId[1]] = {'id':eachRowBasedOnDeliveryStatusId[0], 'sub_type':eachRowBasedOnDeliveryStatusId[2], 'count':eachRowBasedOnDeliveryStatusId[3], 'message_version' : eachRowBasedOnDeliveryStatusId[4]}
		return venenoReportResult

	def venenoDataDetailsInfo(self):
		if 'veneno' in self.socialInfo:
			self.socialInfo['veneno'].update({
				'dataDetail': {
					'inboxes':self.venenoDataDetails_inboxes(),
					'skipped':self.venenoDataDetails_skippedRecipients()
				}
			})
		else:
			raise Exception('VenenoInfo Not Passed , Enable VenenoInfo In Params')

	def venenoDataDetails_inboxes(self):
		query = "select recipient_id from inboxes_{} where message_id = {}".format(self.socialInfo['veneno']['communicationDetail']['bucket_id'], self.messageId)
		result = dbHelper.queryDB(query, 'veneno_data_details')
		return result

	def venenoDataDetails_skippedRecipients(self):
		query = "select recipient_id,target_value from skipped_recipients_{} where message_id = {}".format(self.socialInfo['veneno']['communicationDetail']['bucket_id'], self.messageId)
		result = dbHelper.queryDB(query, 'veneno_data_details')
		return result
		
	def socialOfferInfo(self):
		query = 'select voucher_series_id,remote_offer_id,org_id from social_offer_info where message_id = {}'.format(self.messageId)
		result = dbHelper.queryDB(query, 'veneno')[0]
		self.socialInfo.update({
				'socialOfferInfo':{
					'voucher_series_id':result[0],
					'remote_offer_id':result[1],
					'org_id':result[2]
				}
			})

	def socialCouponUploadInfo(self):
		query = 'select s3_key from social_coupon_upload_info where message_id = {}'.format(self.messageId)
		self.socialInfo.update({
			'socialCouponUploadInfo':{
				's3_key': dbHelper.queryDB(query, 'veneno')[0][0]
				}
			}) 

class social_user_calls():

	def __init__(self):
		pass

	def getUsersInformation(self,numberOfUsers,identifier):
	    query = "select u.id,u.firstname,u.lastname,u.mobile,u.email,l.external_id from users u,loyalty l where u.id=l.user_id and u.email like 'iris_automation%' and u.org_id = " + str(constant.config['orgId']) + " and l.publisher_id = " + str(constant.config['orgId']) + " and l.type = 'loyalty' order by u.id desc limit " + str(numberOfUsers)
	    result = dbHelper.queryDB(query, 'user_management')
	    buildresult = []
	    for eachUserDetail in result:
	    	if identifier == 'mobile' :
	    		buildresult.append(eachUserDetail[3])
	    	else:
	    		buildresult.append(eachUserDetail[4])
	    return buildresult

	def getCustomAudienceListsWithRecipientListId(self,groupVersionid,name):
		query = "select remote_list_id,name from social_audience_list where recipient_list_id = {} and name = '{}'".format(groupVersionid,name)
		result = dbHelper.queryDB(query, 'veneno')[0]
		return result[0],result[1]

	def getCampaignDetails(self,campaignId):
		query = 'select additional_properties from campaigns_base where id ={}'.format(campaignId)
		result = dbHelper.queryDB(query, 'campaigns')[0]
		return result[0]

	def updateCampaignsBaseAdditionalInfo(self,campaignId,remoteId):
		query = "update campaigns_base set additional_properties = '{}' where id = {}".format(json.dumps({'social_campaign_id':remoteId}),campaignId)
		result = dbHelper.queryDB(query, 'campaigns')

	def getNumberOfUsersInCGUH(self,campaignId,messageId):
		query = 'select count(*) from control_group_users_history where org_id ={} and campaign_id = {} and message_id = {}'.format(constant.config['orgId'],campaignId,messageId)
		result = dbHelper.queryDB(query, 'veneno_data_details')
		return result

	def getValidKeyIdForFacebookAccount(self):
		query = "select ckv.id from config_keys ck , config_key_values ckv where ck.name='FB_ADS_ACCOUNT_ID' and ck.id = ckv.key_id and ckv.is_valid = 1 and ckv.org_id={}".format(constant.config['orgId'])
		result = dbHelper.queryDB(query, 'masters')
		return result[0][0]

	def updateConfigKeyValue(self,ckvId,valid=1):
		query = "update config_key_values set is_valid={} where id ={}".format(valid,ckvId)
		result = dbHelper.queryDB(query, 'masters')

	def getCampaignIdWithRemoteId(self):
		query = "select id from campaigns_base where org_id = 786 and additional_properties like '%social_campaign_id%' order by id desc limit 1"
		result = dbHelper.queryDB(query, 'campaigns')
		return result[0][0]

	def getRemoteAdset(self):
		query = "select remote_adset_id from social_adset_info where remote_adset_id is not null and remote_campaign_id is not null order by id desc limit 1"
		result = dbHelper.queryDB(query, 'veneno')
		return result[0][0]

	def getRemoteListId(self):
		query = "select remote_list_id from social_audience_list where account_id = {} order by id desc limit 5".format(constant.config['facebook']['accountId'])
		result = dbHelper.queryDB(query, 'veneno')
		if len(result) == 0: raise Exception('NoRemoteListFoundForAccount:{}'.format(constant.config['facebook']['accountId']))
		return result[randint(0,5)][0]

	def getJobDetail(self,message_id):
		query = "select job_status from aggregation_details where message_id = {} and job_type = 'SOCIAL_ADSET'".format(message_id)
		result = dbHelper.queryDB(query, 'veneno')
		return result[0][0]
