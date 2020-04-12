import pytest, time, json, pytest_ordering, copy
from datetime import datetime
from src.Constant.constant import constant
from src.utilities.logger import Logger
from src.modules.iris.construct import construct
from src.modules.social.socialObject import SocialObject
from src.modules.social.socialHelper import SocialHelper
from src.dbCalls.socialInfo import social_user_calls
from src.utilities.assertion import Assertion

@pytest.mark.run(order=5)
class Test_Social_Thrift_AdsetOperation():

	def setup_class(self):
		self.campaignId = SocialHelper.createCampaignsForSocialThrift()
		self.remoteCampaignId = SocialHelper.createRemoteCampaignsForSocialThrift(self.campaignId['ORG'])
		self.remoteListId,self.groupVersionId = SocialHelper.createRemoteListForSocialThrift(self.campaignId)
		self.remoteOfferId = None

	def setup_method(self, method):
		self.connObj = SocialHelper.getConnObj(newConnection=True)
		Logger.logMethodName(method.__name__)

	@pytest.mark.parametrize('socialStatus', [
		('ACTIVE')
	    ])
	def test_socialThrift_Insight_getAdsetInsights_Sanity(self,socialStatus):
		adsetName = 'Auto_AdsetName_{}'.format(int(time.time()*1000))
		adsetId = self.connObj.createSocialAdset(
			constant.config['orgId'],
			SocialObject().SocialChannel['facebook'],
			SocialObject.SocialAdsetInfo(
	    			adsetName,
	    			self.remoteCampaignId,
	    			datetime.fromtimestamp(time.time()).strftime('%Y-%m-%dT%H:%M:%S'),
	    			datetime.fromtimestamp(time.time()+ 25*60*60).strftime('%Y-%m-%dT%H:%M:%S'),
	    			socialStatus,
	    			100000,
	    			customAudienceId=self.remoteListId
				),
			'requestId_automationthriftCall_{}'.format(int(time.time()*1000))
		).remoteAdsetId

		AdInsight = self.connObj.getAdsetInsights(
			SocialObject().SocialChannel['facebook'],
			constant.config['orgId'],
			adsetId,
			self.groupVersionId,
			True,
			'requestId_automationthriftCall_{}'.format(int(time.time()*1000))
		)
		
		SocialHelper.assertGetAdsetInsight(AdInsight,adsetId)

	@pytest.mark.parametrize('socialStatus', [
		('ACTIVE'),
	    ('PAUSED')
	    ])
	def test_socialThrift_getAdset_Sanity(self,socialStatus):
		adsetName = 'Auto_AdsetName_{}'.format(int(time.time()*1000))
		SocialAdsetInfo = self.connObj.createSocialAdset(
			constant.config['orgId'],
			SocialObject().SocialChannel['facebook'],
			SocialObject.SocialAdsetInfo(
	    			adsetName,
	    			self.remoteCampaignId,
	    			datetime.fromtimestamp(time.time()).strftime('%Y-%m-%dT%H:%M:%S'),
	    			datetime.fromtimestamp(time.time()+ 25*60*60).strftime('%Y-%m-%dT%H:%M:%S'),
	    			socialStatus,
	    			100000,
	    			customAudienceId=self.remoteListId
				),
			'requestId_automationthriftCall_{}'.format(int(time.time()*1000))
		)

		SocialAdSets = self.connObj.getAdSets(
			SocialObject().SocialChannel['facebook'],
			constant.config['orgId'],
			'requestId_automationthriftCall_{}'.format(int(time.time()*1000))
		)

		SocialHelper.assertGetAdset(SocialAdSets,SocialAdsetInfo,SocialObject().SocialStatus[socialStatus])

	def test_socialThrift_updateCustomListInAdset_Sanity(self):
		remoteAdsetId = social_user_calls().getRemoteAdset()
		remoteListId = social_user_calls().getRemoteListId()
		SocialAdsetInfo = self.connObj.updateCustomListInAdset(
			constant.config['orgId'],
			SocialObject().SocialChannel['facebook'],
			remoteAdsetId,
			remoteListId,
			'requestId_automationthriftCall_{}'.format(int(time.time()*1000))
			)
		SocialHelper.validateSocialAdsetInfo(SocialAdsetInfo,remoteAdsetId,remoteListId)

	def test_socialThrift_updateCustomListInAdset_WithIncorrectAdsetId(self):
		remoteListId = social_user_calls().getRemoteListId()
		try:
			SocialAdsetInfo = self.connObj.updateCustomListInAdset(
				constant.config['orgId'],
				SocialObject().SocialChannel['facebook'],
				'remoteAdsetId',
				remoteListId,
				'requestId_automationthriftCall_{}'.format(int(time.time()*1000))
				) 
			Assertion.constructAssertion(False,'Wrong Remote AdsetId is Getting Accepted')
		except Exception,exp:
			Logger.log('With Wrong Adset Id , Exception from thrift Call :{}'.format(exp))

	def test_socialThrift_updateCustomListInAdset_WithIncorrectCampaignId(self):
		remoteAdsetId = social_user_calls().getRemoteAdset()
		try:
			SocialAdsetInfo = self.connObj.updateCustomListInAdset(
				constant.config['orgId'],
				SocialObject().SocialChannel['facebook'],
				remoteAdsetId,
				'remoteListId',
				'requestId_automationthriftCall_{}'.format(int(time.time()*1000))
				)
			Assertion.constructAssertion(False,'Wrong Remote CampaignId is Getting Accepted')
		except Exception,exp:
			Logger.log('With Wrong Campaign Id , Exception from thrift Call :{}'.format(exp))
