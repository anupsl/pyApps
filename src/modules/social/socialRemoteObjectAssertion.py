from src.utilities.logger import Logger
from src.Constant.constant import constant
from src.utilities.assertion import Assertion
from src.dbCalls.socialInfo import social_user_calls
from src.modules.social.socialObject import SocialObject
from src.modules.social.socialHelper import SocialHelper
import json,time

class SocialRemoteObjectAssertion():

	def __init__(self,campaignId,remoteCampaignId,remoteListId,remoteAdsetId):
		self.campaignId=campaignId
		self.remoteCampaignId=remoteCampaignId
		self.remoteListId=remoteListId
		self.remoteAdsetId=remoteAdsetId
		self.checkRemoteCampaignIdMapping()
		self.checkRemoteList()
		self.checkRemoteAdset()

	def checkRemoteCampaignIdMapping(self):
		remoteCampaignId = json.loads(social_user_calls().getCampaignDetails(self.campaignId))['social_campaign_id']
		Assertion.constructAssertion(remoteCampaignId == self.remoteCampaignId,'Remote CampaignId , Actual :{} and Expected :{}'.format(remoteCampaignId,self.remoteCampaignId))

	def checkRemoteList(self):
		connObj = SocialHelper.getConnObj(newConnection=True)
		flag=False
		
		GetCustomAudienceListsResponse = connObj.getCustomAudienceLists(
		    constant.config['orgId'],
		    SocialObject().SocialChannel['facebook'],
		    True,
		    'requestId_automationthriftCall_{}'.format(int(time.time()*1000))
		)
		for each in GetCustomAudienceListsResponse.customAudienceLists:
		    if each.remoteListId == self.remoteListId:
		        flag = True
		        break
		Assertion.constructAssertion(flag,'New Created List with Name :{} found in GetCustomAudienceListsResponse'.format(self.remoteListId))

	def checkRemoteAdset(self):
		connObj = SocialHelper.getConnObj(newConnection=True)
		flag = False
		SocialAdSets = connObj.getAdSets(
			SocialObject().SocialChannel['facebook'],
			constant.config['orgId'],
			'requestId_automationthriftCall_{}'.format(int(time.time()*1000))
		)
		
		for SocialAdSet in SocialAdSets:
		    if SocialAdSet.id == self.remoteAdsetId:
		        flag=True
		        break
		Assertion.constructAssertion(flag,'SocialAdsetInfo remoteId found in getSocialAdset')

