import pytest, time, json, pytest_ordering, copy
from datetime import datetime
from src.Constant.constant import constant
from src.utilities.logger import Logger
from src.modules.iris.construct import construct
from src.utilities.assertion import Assertion
from src.modules.social.socialObject import SocialObject
from src.modules.social.socialHelper import SocialHelper
from src.dbCalls.socialInfo import social_user_calls

@pytest.mark.run(order=4)
class Test_Social_Thrift_Adset():
    
    def setup_class(self):
    	self.campaignId = SocialHelper.createCampaignsForSocialThrift()
        self.remoteCampaignId = SocialHelper.createRemoteCampaignsForSocialThrift(self.campaignId['ORG'])
        self.remoteListId,self.groupVersionId = SocialHelper.createRemoteListForSocialThrift(self.campaignId)
        self.remoteOfferId = None

    def setup_method(self, method):
        self.connObj = SocialHelper.getConnObj(newConnection=True)
        Logger.logMethodName(method.__name__)

    @pytest.mark.parametrize('socialStatus', [
    	('ACTIVE'),
        ('PAUSED')
        ])
    def test_socialThrift_createAdset_withList_withoutCouponAttached_Sanity(self,socialStatus):
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
    	SocialHelper.assertCreateAdsetSocial(SocialAdsetInfo,self.remoteCampaignId,SocialObject().SocialStatus[socialStatus.upper()],adsetName,expectedRemoteListId=self.remoteListId)

    @pytest.mark.parametrize('socialStatus', [
    	('ACTIVE'),
        ('PAUSED')
        ])
    def test_socialThrift_createAdset_withList_withCouponAttached(self,socialStatus):
    	adsetName = 'Auto_AdsetName_{}'.format(int(time.time()*1000))
    	SocialOffer = self.connObj.createNativeOffer(
            constant.config['orgId'],
            SocialObject().SocialChannel['facebook'],
            SocialObject.SocialOffer(
                    {
                            'offerType':'percentage_off',
                            'offerText':'offerText_{}'.format(int(time.time())),
                            'offerValue':10,
                            'socialOfferCouponsCsvFileInfo':None,
                            'redemptionCode':'redemptionCode_{}'.format(int(time.time()))
                    },
                    constant.config['facebook']['pageId'],
                    SocialObject().OfferLocationType['offline'],
                    'overviewDetails_{}'.format(int(time.time())),
                    datetime.fromtimestamp(time.time()+ 25*60*60).strftime('%Y-%m-%dT%H:%M:%S'),
                    'generic'
                ),
            'requestId_automationthriftCall_{}'.format(int(time.time()*1000))
        )
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
	    			customAudienceId=self.remoteListId,
	    			remoteOfferId=SocialOffer.remoteOfferId
    			),
    		'requestId_automationthriftCall_{}'.format(int(time.time()*1000))
    	)
    	SocialHelper.assertCreateAdsetSocial(SocialAdsetInfo,self.remoteCampaignId,SocialObject().SocialStatus[socialStatus.upper()],adsetName,expectedRemoteListId=self.remoteListId)

    def test_socialThrift_getSocialCampaignDetails_Sanity(self):
        campaignId = social_user_calls().getCampaignIdWithRemoteId()
        SocialCampaignDetails = self.connObj.getSocialCampaignDetails(
            constant.config['orgId'],
            campaignId,
            int(constant.config['userId']),
            SocialObject().SocialChannel['facebook'],
            'requestId_automationthriftCall_{}'.format(int(time.time()*1000))
            )
        SocialHelper.validateGetSoicalCampaignDetails(SocialCampaignDetails,campaignId)

    def test_socialThrift_getSocialCampaignDetails_withCampaignNoRemoteId(self):
        try:
            SocialCampaignDetails = self.connObj.getSocialCampaignDetails(
                constant.config['orgId'],
                self.campaignId['ORG'],
                int(constant.config['userId']),
                SocialObject().SocialChannel['facebook'],
                'requestId_automationthriftCall_{}'.format(int(time.time()*1000))
                )
            Assertion.constructAssertion(False,'With Campaign Not mapped with remote Campaign id , also thrift call worked')
        except Exception,exp:
            Logger.log('With Campaign Not mapped with remote Campaign id Exception Caught :{}'.format(exp))
        
    def test_socialThrift_getSocialCampaignDetails_withInvalidUserId(self):
        try:
            SocialCampaignDetails = self.connObj.getSocialCampaignDetails(
                constant.config['orgId'],
                self.campaignId['ORG'],
                99999,
                SocialObject().SocialChannel['facebook'],
                'requestId_automationthriftCall_{}'.format(int(time.time()*1000))
                )
            Assertion.constructAssertion(False,'Thrift Call still working with Invalid UserId')
        except Exception,exp:
            Logger.log('With Invalid User Exception Caught :{}'.format(exp))

