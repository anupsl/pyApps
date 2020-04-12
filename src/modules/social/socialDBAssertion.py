from src.utilities.logger import Logger
from src.Constant.constant import constant
from src.utilities.assertion import Assertion
from src.dbCalls.socialInfo import social_info
from src.dbCalls.socialInfo import social_user_calls
from src.utilities.awsHelper import AWSHelper
import json,time

class SocialDBAssertion():

	def __init__(self,campaignId,groupVersionId,cdId,listCount,couponUsed=False,couponUsedExteranal=False,skippedUsers=False,skippedReason=[],socialAudienceList=True,socialAdsetInfo=True,aggregationDetail=True,venenoInfo=True,venenoDataDetailsInfo=True,socialOffer=False,externalOfferList=[]):
		Logger.log('Social Db Assertion Initialized for Value ... GroupVersionId :{} and Messageid :{}'.format(groupVersionId,cdId))
		self.campaignId=campaignId
		self.groupVersionId = groupVersionId
		self.messageId = cdId
		self.listCount=listCount
		self.skippedUsers=skippedUsers
		self.skippedReason=skippedReason
		self.couponUsed=couponUsed
		self.couponUsedExteranal=couponUsedExteranal
		self.socialAudienceList=socialAudienceList
		self.socialAdsetInfo=socialAdsetInfo
		self.aggregationDetail=aggregationDetail
		self.venenoInfo=venenoInfo
		self.venenoDataDetailsInfo=venenoDataDetailsInfo
		self.socialOffer=socialOffer
		self.externalOfferList=externalOfferList
		self.waitForSocial()
		self.SocialInfo = social_info(groupVersionid=groupVersionId,messageId=cdId,socialAudienceList=socialAudienceList,socialAdsetInfo=socialAdsetInfo,aggregationDetail=aggregationDetail,venenoInfo=venenoInfo,venenoDataDetailsInfo=venenoDataDetailsInfo,socialOffer=socialOffer).socialInfo

	def waitForSocial(self):
		sleep=35
		if self.socialAdsetInfo : sleep = 100
		if constant.config['cluster'] not in ['nightly','staging']:
			Logger.log('In Prod , Veneno Monitor Status takes 10 mins , so waiting for 1 mins -10 times  to start DB Assertion....')
			sleep = sleep + 70
		for _ in range(15):
			try:
				Logger.log('Checking For Value in SocialAdset Table')
				if self.socialAdsetInfo: 
					social_info(groupVersionid=self.groupVersionId,messageId=self.messageId,socialAdsetInfo=True).socialInfo
				else:
					social_info(groupVersionid=self.groupVersionId,messageId=self.messageId).veneno_monitoringStatus()
					break
			except Exception,exp:
				time.sleep(sleep)

	def check(self):
		if self.venenoInfo:
			self.assertCommunicationDetail()
			self.assertServiceDetail()
			self.assertBatchDetail()
			self.assertSummaryReport()
			self.assertmonitoringStatus()
			self.assertCGUH()
		if self.venenoDataDetailsInfo:
			self.assertInboxes()
			self.assertSkippedRecipient()
		if self.socialAudienceList: 
			self.assertsocialAudienceList()
		if self.aggregationDetail: 
			self.assertAggregationDetail()
		if self.socialOffer:
			self.assertSocialOffer()
		if self.socialAdsetInfo: 
			self.assertAdsetInfo()
			return self.SocialInfo['adsetInfo']['remote_campaign_id'],self.SocialInfo['adsetInfo']['custom_audience_id'],self.SocialInfo['adsetInfo']['remote_adset_id'],self.SocialInfo['adsetInfo']['remote_offer_id']

	def assertCommunicationDetail(self):
		Assertion.constructAssertion(self.SocialInfo['veneno']['communicationDetail']['expected_delivery_count'] <= self.listCount, 'Expected Delivery Count , Actual :{} and Expected :{}'.format(self.SocialInfo['veneno']['communicationDetail']['expected_delivery_count'],self.listCount))
		Assertion.constructAssertion(self.SocialInfo['veneno']['communicationDetail']['overall_recipient_count'] == self.listCount, 'Overall Delivery Count , Actual :{} and Expected :{}'.format(self.SocialInfo['veneno']['communicationDetail']['overall_recipient_count'],self.listCount))
		Assertion.constructAssertion(self.SocialInfo['veneno']['communicationDetail']['recipient_list_id'] == self.groupVersionId, 'RecipientListId , Actual :{} and Expected :{}'.format(self.SocialInfo['veneno']['communicationDetail']['recipient_list_id'],self.groupVersionId))
		Assertion.constructAssertion(self.SocialInfo['veneno']['communicationDetail']['communication_type'] == 'FACEBOOK', 'communication_type , Actual :{} and Expected :{}'.format(self.SocialInfo['veneno']['communicationDetail']['communication_type'],'FACEBOOK'))
		Assertion.constructAssertion(self.SocialInfo['veneno']['communicationDetail']['campaign_id'] == self.campaignId, 'campaign_id , Actual :{} and Expected :{}'.format(self.SocialInfo['veneno']['communicationDetail']['campaign_id'],self.campaignId))
		Assertion.constructAssertion(self.SocialInfo['veneno']['communicationDetail']['target_type'] == 'SOCIAL', 'target_type , Actual :{} and Expected :{}'.format(self.SocialInfo['veneno']['communicationDetail']['target_type'],'SOCIAL'))
		Assertion.constructAssertion(int(self.SocialInfo['veneno']['communicationDetail']['bucket_id']) > 0, 'BucketId , Actual :{} is > 0'.format(self.SocialInfo['veneno']['communicationDetail']['bucket_id']))
		Assertion.constructAssertion(self.SocialInfo['veneno']['communicationDetail']['state'] == 'CLOSED', 'state , Actual :{} and Expected :{}'.format(self.SocialInfo['veneno']['communicationDetail']['state'],'CLOSED'))

	def assertServiceDetail(self):
		Assertion.constructAssertion('DELIVERY_SERVER' in self.SocialInfo['veneno']['serviceDetail'],'Expecting DELIVERY_SERVER in Service Details')
		Assertion.constructAssertion('FEEDER' in self.SocialInfo['veneno']['serviceDetail'],'Expecting FEEDER in Service Details')
		if self.skippedUsers:
			Assertion.constructAssertion('SKIPPED' in self.SocialInfo['veneno']['serviceDetail'],'Expecting SKIPPED in Service Details')
		else:
			Assertion.constructAssertion('FB_GATEWAY' in self.SocialInfo['veneno']['serviceDetail'],'Expecting FB_GATEWAY in Service Details')
		for eachbatch in self.SocialInfo['veneno']['serviceDetail']:
			Logger.log('For Batch :{} , check of Version , batch processed and processed Count'.format(eachbatch))
			Assertion.constructAssertion(int(self.SocialInfo['veneno']['serviceDetail'][eachbatch]['message_version']) == 0, 'Message Version , Actual :{} and Expected :{}'.format(self.SocialInfo['veneno']['serviceDetail'][eachbatch]['message_version'],0))
			Assertion.constructAssertion(int(self.SocialInfo['veneno']['serviceDetail'][eachbatch]['batches_processed']) == 1, 'Message Version , Actual :{} and Expected :{}'.format(self.SocialInfo['veneno']['serviceDetail'][eachbatch]['batches_processed'],1))
			Assertion.constructAssertion(int(self.SocialInfo['veneno']['serviceDetail'][eachbatch]['processed_count']) == self.SocialInfo['veneno']['communicationDetail']['expected_delivery_count'], 'Message Version , Actual :{} and Expected :{}'.format(self.SocialInfo['veneno']['serviceDetail'][eachbatch]['processed_count'],self.SocialInfo['veneno']['communicationDetail']['expected_delivery_count']))

	def assertBatchDetail(self):
		Assertion.constructAssertion('DELIVERY_SERVER' in self.SocialInfo['veneno']['batchDetail'],'Expecting DELIVERY_SERVER in batchDetail')
		Assertion.constructAssertion('TAG_RESOLVER' in self.SocialInfo['veneno']['batchDetail'],'Expecting TAG_RESOLVER in batchDetail')
		Assertion.constructAssertion('FEEDER' in self.SocialInfo['veneno']['batchDetail'],'Expecting FEEDER in batchDetail')
		if not self.skippedUsers: Assertion.constructAssertion('INBOX_CONSUMER' in self.SocialInfo['veneno']['batchDetail'],'Expecting INBOX_CONSUMER in batchDetail')
		
		for eachbatch in self.SocialInfo['veneno']['batchDetail']:
			Logger.log('For Batch :{} , checking message version and status'.format(eachbatch))
			Assertion.constructAssertion(int(self.SocialInfo['veneno']['batchDetail'][eachbatch]['message_version']) == 0,'Expecting Message Version to be 0 for each batch')
			Assertion.constructAssertion(self.SocialInfo['veneno']['batchDetail'][eachbatch]['status'] == 'CLOSED','Expecting Status to be CLOSED for each batch')

	def assertSummaryReport(self):
		reportType = 'SENT_TO_FACEBOOK'
		if self.skippedUsers: reportType = 'SKIPPED'
		Assertion.constructAssertion(reportType in self.SocialInfo['veneno']['summaryReport'],'Expecting {} in summaryReport',format(reportType))
		Assertion.constructAssertion(int(self.SocialInfo['veneno']['summaryReport'][reportType]['count'])==self.SocialInfo['veneno']['communicationDetail']['expected_delivery_count'],'Expecting {} count , Actual :{} and Expected :{}'.format(reportType,self.SocialInfo['veneno']['summaryReport'][reportType]['count'],self.SocialInfo['veneno']['communicationDetail']['expected_delivery_count']))
	
	def assertmonitoringStatus(self):
		Assertion.constructAssertion(self.SocialInfo['veneno']['monitoringStatus']['processed_status'] == 1, 'Monitoring Status processed_status , Actual :{} and Expected :{}'.format(self.SocialInfo['veneno']['monitoringStatus']['processed_status'],1))
		Assertion.constructAssertion(int(self.SocialInfo['veneno']['monitoringStatus']['message_version']) == 0, 'Monitoring Status message_version , Actual :{} and Expected :{}'.format(self.SocialInfo['veneno']['monitoringStatus']['message_version'],0))
		
	def assertInboxes(self):
		self.inboxCount = len(self.SocialInfo['veneno']['dataDetail']['inboxes'])
		if not self.skippedUsers:
			Assertion.constructAssertion(len(self.SocialInfo['veneno']['dataDetail']['inboxes']) == self.SocialInfo['veneno']['communicationDetail']['expected_delivery_count'],'NUmberOfUsers in Inbox , Actual :{} and Expected :{}'.format(len(self.SocialInfo['veneno']['dataDetail']['inboxes']),self.SocialInfo['veneno']['communicationDetail']['expected_delivery_count']))
			
	def assertSkippedRecipient(self):
		self.skippedCount = len(self.SocialInfo['veneno']['dataDetail']['skipped'])
		if self.skippedUsers:
			Assertion.constructAssertion(len(self.SocialInfo['veneno']['dataDetail']['inboxes']) == self.SocialInfo['veneno']['communicationDetail']['expected_delivery_count']-self.skippedCount,'NUmberOfUsers in Inbox , Actual :{} and Expected :{}'.format(len(self.SocialInfo['veneno']['dataDetail']['inboxes']),self.SocialInfo['veneno']['communicationDetail']['expected_delivery_count']-self.skippedCount))
			for eachUserGotSkipped in self.SocialInfo['veneno']['dataDetail']['skipped']:
				Logger.log('User :{} , got Skipped with Error Description :{}'.format(eachUserGotSkipped[0],eachUserGotSkipped[1]))
				Assertion.constructAssertion(eachUserGotSkipped[1] in self.skippedReason,'Skipped Error Description , Actual :{} and Expected :{}'.format(eachUserGotSkipped[1],self.skippedReason))
	
	def assertsocialAudienceList(self):
		Assertion.constructAssertion('List created from capillary for message id {}'.format(self.messageId) in self.SocialInfo['audienceList']['description'], 'Description in Social Audience List :{}'.format(self.SocialInfo['audienceList']['description']))
		Assertion.constructAssertion(int(self.SocialInfo['audienceList']['approximate_count']) == 0 , 'approximate_count in Social Audience List , Actual :{} and Expected :{}'.format(int(self.SocialInfo['audienceList']['approximate_count']),0))
		Assertion.constructAssertion(self.SocialInfo['audienceList']['message_id'] == self.messageId , 'message_id in Social Audience List , Actual :{} and Expected :{}'.format(self.SocialInfo['audienceList']['message_id'], self.messageId))
		Assertion.constructAssertion(int(self.SocialInfo['audienceList']['approximate_count']) == 0 , 'approximate_count in Social Audience List , Actual :{} and Expected :{}'.format(int(self.SocialInfo['audienceList']['approximate_count']),0))
		Assertion.constructAssertion(self.SocialInfo['audienceList']['type'] == 'FACEBOOK' , 'type in Social Audience List , Actual :{} and Expected :{}'.format(self.SocialInfo['audienceList']['type'],'FACEBOOK'))
		Assertion.constructAssertion(self.SocialInfo['audienceList']['remote_list_id'] is not None ,'Remote List is not None')
		Assertion.constructAssertion(str(self.SocialInfo['audienceList']['account_id']) == str(constant.config['facebook']['accountId']) ,'Account Id ,Actual :{} and Expected :{}'.format(self.SocialInfo['audienceList']['account_id'],constant.config['facebook']['accountId']))
		
	def assertAggregationDetail(self):
		Assertion.constructAssertion('LIST_PUBLISHED' in self.SocialInfo['aggregationDetails'],'Expecting LIST_PUBLISHED in aggregationDetails')
		Assertion.constructAssertion('POST_PROCESS' in self.SocialInfo['aggregationDetails'],'Expecting POST_PROCESS in aggregationDetails')
		if self.couponUsed and not self.couponUsedExteranal:
			Assertion.constructAssertion('COUPON_ISSUED' in self.SocialInfo['aggregationDetails'],'Expecting COUPON_ISSUED in aggregationDetails')
		
		for eachJobType in self.SocialInfo['aggregationDetails']:
			Assertion.constructAssertion(self.SocialInfo['aggregationDetails'][eachJobType]['job_status'] == 'DONE','For JobType :{} , job status is :{}'.format(eachJobType,self.SocialInfo['aggregationDetails'][eachJobType]['job_status']))
	
	def assertAdsetInfo(self):
		if self.couponUsedExteranal: Assertion.constructAssertion(self.SocialInfo['adsetInfo']['remote_offer_id'] is not None ,'Remote Offer Id is not None')
		Assertion.constructAssertion(self.SocialInfo['adsetInfo']['remote_campaign_id'] is not None , 'Remote Campaign id is not None')
		Assertion.constructAssertion(self.SocialInfo['adsetInfo']['custom_audience_id'] is not None , 'Custom Audience Id is not None')
		Assertion.constructAssertion(self.SocialInfo['adsetInfo']['remote_adset_id'] is not None , 'Remote AdsetId is not None')

	def assertCGUH(self):
		numberofUserInCGUH = int(social_user_calls().getNumberOfUsersInCGUH(self.campaignId,self.messageId)[0][0])
		Assertion.constructAssertion(numberofUserInCGUH == self.SocialInfo['veneno']['communicationDetail']['overall_recipient_count']-self.SocialInfo['veneno']['communicationDetail']['expected_delivery_count'],'NumberOfusers in CGUH :{} and expected :{}'.format(numberofUserInCGUH ,self.SocialInfo['veneno']['communicationDetail']['overall_recipient_count']-self.SocialInfo['veneno']['communicationDetail']['expected_delivery_count']))

	def assertSocialOffer(self):
		if self.socialOffer:
			Assertion.constructAssertion(self.SocialInfo['socialOfferInfo']['remote_offer_id'] == str(self.SocialInfo['adsetInfo']['remote_offer_id']), 'Social Offer Info -> remote Offer Id , Actual :{} and Expected :{}'.format(self.SocialInfo['socialOfferInfo']['remote_offer_id'],self.SocialInfo['adsetInfo']['remote_offer_id']))
			Assertion.constructAssertion(self.SocialInfo['socialOfferInfo']['org_id'] == constant.config['orgId'],'OrgId Matched in Social Offer Info')

			s3Key = self.SocialInfo['socialCouponUploadInfo']['s3_key']
			Assertion.constructAssertion(s3Key.endswith('.csv'),'s3 Key Extension check for .csv')
			dataFromS3 = AWSHelper.readFileFromS3('campaigns{}'.format(constant.config['cluster']),s3Key)
			
			for each in self.externalOfferList:
				Assertion.constructAssertion('{},'.format(each) in dataFromS3 , 'Coupon Code :{} in s3'.format(each))
			