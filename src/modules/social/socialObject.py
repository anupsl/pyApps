import time
from src.Constant.constant import constant
from src.initializer.generateThrift import facebook
from src.utilities.randValues import randValues
from src.utilities.utils import Utils

class SocialObject():

	def __init__(self):
		self.SocialChannel = {'none': 0,'facebook':1,'google':2,'twitter':3}
		self.GatewayResponseType = {'success':0,'sent':1, 'blocked':2, 'failed':3, 'invalidContent':4, 'policyViolation':5}
		self.SocialStatus = {'ACTIVE':0, 'PAUSED':1, 'DELETED':2, 'ARCHIVED':3}
		self.SocialCouponType = { 'generic':0,'csv_file':1 }
		self.OfferType = {'percentage_off':0, 'cash_discount':1}
		self.AdSetStatus= {'ACTIVE':0, 'PAUSED':1, 'DELETED':2, 'ARCHIVED':3}
		self.OfferLocationType = {'online':0, 'offline':1, 'both':3}

	@staticmethod
	def UpdateAdsetRequest(remoteAdsetId,customAudienceId=None,remoteOfferId=None):
		tmpDict = {
			'remoteAdsetId' : remoteAdsetId
		}
		if customAudienceId is not None : tmpDict['customAudienceId'] = customAudienceId
		if remoteOfferId is not None : tmpDict['remoteOfferId'] = remoteOfferId
		return facebook.UpdateAdsetRequest(**tmpDict)

	@staticmethod
	def SocialAdsetInfo(adsetName,remoteCampaignId,startTime,endTime,socialAdsetStatus,dailyBudget,customAudienceId=None,remoteOfferId=None,remoteAdsetId=None):
		tmpDict = {
			'adsetName':adsetName,
			'remoteCampaignId':remoteCampaignId,
			'startTime':startTime,
			'endTime':endTime,
			'socialAdsetStatus':socialAdsetStatus,
			'dailyBudget':dailyBudget
		}
		scObj = SocialObject()
		tmpDict['socialAdsetStatus'] = scObj.SocialStatus[tmpDict['socialAdsetStatus'].upper()]
		if customAudienceId is not None : tmpDict['customAudienceId'] = customAudienceId
		if remoteOfferId is not None : tmpDict['remoteOfferId'] = remoteOfferId
		if remoteAdsetId is not None : tmpDict['remoteAdsetId'] = remoteAdsetId
		return facebook.SocialAdsetInfo(**tmpDict)

	@staticmethod
	def SocialOffer(socialDiscount,pageId,offerLocationType,overviewDetails,expirationTime,socialCouponType,remoteOfferId=None):
		tmpDict = {
			'socialDiscount':socialDiscount,
			'pageId':pageId,
			'offerLocationType':offerLocationType,
			'overviewDetails':overviewDetails,
			'expirationTime':expirationTime,
			'socialCouponType':socialCouponType
		}
		scObj = SocialObject()
		tmpDict['socialDiscount'] = SocialObject.SocialDiscount(socialDiscount['offerType'],socialDiscount['offerText'],socialDiscount['offerValue'],socialDiscount['socialOfferCouponsCsvFileInfo'],socialDiscount['redemptionCode'])
		tmpDict['socialCouponType'] = scObj.SocialCouponType[tmpDict['socialCouponType'].lower()]
		if remoteOfferId is not None : tmpDict['socialDiscount'] = socialDiscount
		return facebook.SocialOffer(**tmpDict)

	@staticmethod
	def SocialDiscount(offerType,offerText,offerValue,socialOfferCouponsCsvFileInfo=None,redemptionCode=None):
		tmpDict = {
			'offerType':offerType,
			'offerText':offerText,
			'offerValue':offerValue
		}
		scObj = SocialObject()
		tmpDict['offerType'] = scObj.OfferType[tmpDict['offerType'].lower()]
		if socialOfferCouponsCsvFileInfo is not None:
			tmpDict['socialOfferCouponsCsvFileInfo'] = SocialObject.SocialOfferCouponsCsvFileInfo(socialOfferCouponsCsvFileInfo['couponsCsvFileS3Path'],socialOfferCouponsCsvFileInfo['couponsUploaded'],socialOfferCouponsCsvFileInfo['couponsUploadStatus'])
		if 'redemptionCode' is not None :  tmpDict['redemptionCode'] = redemptionCode
		return facebook.SocialDiscount(**tmpDict)

	@staticmethod
	def SocialOfferCouponsCsvFileInfo(couponsCsvFileS3Path,couponsUploaded=None,couponsUploadStatus=None):
		tmpDict = {
			'couponsCsvFileS3Path':couponsCsvFileS3Path
		}
		if couponsUploaded is not None : tmpDict['couponsUploaded']=couponsUploaded
		if couponsUploadStatus is not None : tmpDict['couponsUploadStatus']=couponsUploadStatus
		return facebook.SocialOfferCouponsCsvFileInfo(**tmpDict)

	@staticmethod
	def SocialCampaign(name,orgId,campaignId,accountId=None,socialCampaignStatus=None,remoteCampaignId=None):
		tmpDict = {
			'name':name,
			'orgId':orgId,
			'campaignId':campaignId,

		}
		if remoteCampaignId is not None: tmpDict['remoteCampaignId']=remoteCampaignId
		if accountId is not None : tmpDict['accountId']=accountId
		if socialCampaignStatus is not None :
			tmpDict['socialCampaignStatus'] = socialCampaignStatus
			scObj = SocialObject()
			tmpDict['socialCampaignStatus'] = scObj.SocialStatus[tmpDict['socialCampaignStatus'].upper()]
		return facebook.SocialCampaign(**tmpDict)

	@staticmethod
	def AdInsight(orgId,socialChannel,adsetId,insights,cachedon):
		tmpDict ={
			'orgId':orgId,
			'socialChannel':socialChannel,
			'adsetId':adsetId,
			'insights':insights,
			'cachedon':cachedon

		}
		scObj = SocialObject()
		tmpDict['socialChannel'] = scObj.SocialChannel[tmpDict['socialChannel'].lower()]
		return facebook.AdInsight(**tmpDict)

	@staticmethod
	def SocialAdSet(id,name,campaignId,startTime,endTime,status):
		tmpDict = {
			'id':id,
			'name':name,
			'campaignId':campaignId,
			'startTime':startTime,
			'endTime':endTime,
			'status':status
		}
		scObj = SocialObject()
		tmpDict['status'] = scObj.AdSetStatus[tmpDict['status'].upper()]
		return facebook.SocialAdSet(**tmpDict)

	@staticmethod
	def GetCustomAudienceListsResponse(response,message,customAudienceLists):
		tmpDict = {
			'response':response,
			'message':message,
			'customAudienceLists':customAudienceLists
		}
		scObj = SocialObject()
		tmpDict['response'] =  scObj.GatewayResponseType[tmpDict['response'].lower()]
		listOfConstructerCustomAudience = list()
		for eachcustomAudienceLists in tmpDict['customAudienceLists']:
			listOfConstructerCustomAudience.append(SocialObject.CustomAudienceList(eachcustomAudienceLists['orgId'],eachcustomAudienceLists['socialChannel'],eachcustomAudienceLists['adsAccountId'],eachcustomAudienceLists['recepientlistId'],eachcustomAudienceLists['remoteListId'],eachcustomAudienceLists['name'],eachcustomAudienceLists['description'],eachcustomAudienceLists['approximateCount'],eachcustomAudienceLists['contentUpdatedTime'],eachcustomAudienceLists['createdTime']))
		tmpDict['customAudienceLists'] = listOfConstructerCustomAudience
		return facebook.GetCustomAudienceListsResponse(**tmpDict)

	@staticmethod
	def CustomAudienceList(orgId,socialChannel,adsAccountId,recepientlistId,remoteListId,name,description,approximateCount,contentUpdatedTime,createdTime):
		tmpDict = {
			'orgId':orgId,
			'socialChannel':socialChannel,
			'adsAccountId':adsAccountId,
			'recepientlistId':recepientlistId,
			'remoteListId':remoteListId,
			'name':name,
			'description':description,
			'approximateCount':approximateCount,
			'contentUpdatedTime':contentUpdatedTime,
			'createdTime':createdTime,
			'cachedOn':cachedOn

		}
		scObj = SocialObject()
		tmpDict['socialChannel'] =  scObj.SocialChannel[tmpDict['socialChannel'].lower()]
		return facebook.CustomAudienceList(**tmpDict)


	@staticmethod
	def SocialAccountDetails(channel):
		tmpDict = {
			'channel':channel
		}
		scObj = SocialObject()
		tmpDict['channel'] =  scObj.SocialChannel[tmpDict['channel'].lower()]
		return facebook.SocialAccountDetails(**tmpDict)

	@staticmethod
	def CustomAudienceListDetails(name,description,messageId):
		tmpDict ={
			'name':name,
			'description':description,
			'messageId':int(messageId)
		}
		return facebook.CustomAudienceListDetails(**tmpDict)

	@staticmethod
	def UserDetails(email=None,mobile=None):
		tmpDict ={}
		if email is not None : tmpDict['email'] = email
		if mobile is not None : tmpDict['mobile'] = mobile
		return facebook.UserDetails(**tmpDict)

	@staticmethod
	def CreateCustomAudienceListResponse(listid,message,response):
		tmpDict = {
			'listid':listid,
			'message':message,
			'response':response
		}
		scObj = SocialObject()
		tmpDict['response'] =  scObj.GatewayResponseType[tmpDict['response'].lower()]
		return facebook.CreateCustomAudienceListResponse(**tmpDict)