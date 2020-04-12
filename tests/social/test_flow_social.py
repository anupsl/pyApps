import pytest
import time

from src.dbCalls.socialInfo import social_user_calls
from src.modules.iris.coupons import coupons
from src.modules.social.socialDBAssertion import SocialDBAssertion
from src.modules.social.socialHelper import SocialHelper
from src.modules.social.socialRemoteObjectAssertion import SocialRemoteObjectAssertion
from src.modules.veneno.venenoHelper import VenenoHelper
from src.modules.veneno.venenoObject import VenenoObject
from src.utilities.assertion import Assertion
from src.utilities.logger import Logger


@pytest.mark.run(order=8)
class Test_Flow_Social_ORG():

	def setup_class(self):
		self.numberOfUsers = 20
		self.campaigns = SocialHelper.createCampaignsForSocialThrift(testControlType=['ORG'])
		self.groupVersionid,self.groupName = SocialHelper.createListForSocial(self.campaigns,'ORG',numberOfUsers=self.numberOfUsers,newUser=True)
		self.remoteCampaignId = SocialHelper.createRemoteCampaignsForSocialThrift(self.campaigns['ORG'])
		SocialHelper.updateRemoteCampaignIdInCampaignsBase(self.campaigns['ORG'],self.remoteCampaignId)
		self.voucherSeriesId = coupons.createCoupons(campaignId=self.campaigns['ORG'],payloadData={'couponLimit':{'limit':0, 'type':'UNLIMITED'}, 'discountOn':'BILL', 'discountType':'ABS', 'discountValue':10})[0]['json']['entity']['voucherSeriesId']

	def setup_method(self, method):
		self.connObj = VenenoHelper.getConnObj(newConnection=True)
		Logger.logMethodName(method.__name__)

	@pytest.mark.parametrize('campaignType', [
    	('ORG')
        ])
	def test_flow_social_positive_withoutCoupon_Sanity(self,campaignType):
		cdDetailsBody = {
		     'campaignId':self.campaigns[campaignType.upper()],
		     'targetType':'SOCIAL',
		     'communicationType':'FACEBOOK',
		     'subject':'',
		     'recipientListId':self.groupVersionid,
		     'overallRecipientCount':self.numberOfUsers,
		     'expectedDeliveryCount':self.numberOfUsers,
		     'groupName':self.groupName
		    }
	   	extraParams = {
	   		'voucher_series': -1,
	   		'default_argument' : {
	   			"entity_id":-1,
	   			"is_loyalty_checkbox_enabled":"0",
	   			"voucher_series_id":"-1",
	   			"daily_budget":10000,
			    "create_adset":True,
			    "use_existing_adset":False,
			    "adset_name": 'AutoAdset_{}'.format(int(time.time()*1000))
	   		}
	   	}
		communicationDetailObject = VenenoObject.communicationDetail(cdDetailsBody,extraParams=extraParams)
		communicationId = self.connObj.addMessageForRecipients(communicationDetailObject)
		remoteCampaignId,remoteListId,remoteAdsetId,remoteOfferid = SocialDBAssertion(self.campaigns[campaignType.upper()],self.groupVersionid,communicationId,self.numberOfUsers).check()
		SocialRemoteObjectAssertion(self.campaigns[campaignType.upper()],remoteCampaignId,remoteListId,remoteAdsetId)

	def test_flow_social_positive_withoutCoupon_CreateAdsetAsFalse(self):
		cdDetailsBody = {
		     'campaignId':self.campaigns['ORG'],
		     'targetType':'SOCIAL',
		     'communicationType':'FACEBOOK',
		     'subject':'',
		     'recipientListId':self.groupVersionid,
		     'overallRecipientCount':self.numberOfUsers,
		     'expectedDeliveryCount':self.numberOfUsers,
		     'groupName':self.groupName
		    }
	   	extraParams = {
	   		'voucher_series': -1,
	   		'default_argument' : {
	   			"entity_id":-1,
	   			"is_loyalty_checkbox_enabled":"0",
	   			"voucher_series_id":"-1",
	   			"daily_budget":10000,
			    "create_adset":False
	   		}
	   	}
		communicationDetailObject = VenenoObject.communicationDetail(cdDetailsBody,extraParams=extraParams)
		communicationId = self.connObj.addMessageForRecipients(communicationDetailObject)
		SocialDBAssertion(self.campaigns['ORG'],self.groupVersionid,communicationId,self.numberOfUsers,socialAdsetInfo=False,aggregationDetail=False,venenoDataDetailsInfo=False).check()
		
	def test_flow_social_positive_withoutCoupon_CreateAdsetAndUseExistingAsTrue(self):
		cdDetailsBody = {
		     'campaignId':self.campaigns['ORG'],
		     'targetType':'SOCIAL',
		     'communicationType':'FACEBOOK',
		     'subject':'',
		     'recipientListId':self.groupVersionid,
		     'overallRecipientCount':self.numberOfUsers,
		     'expectedDeliveryCount':self.numberOfUsers,
		     'groupName':self.groupName
		    }
	   	extraParams = {
	   		'voucher_series': -1,
	   		'default_argument' : {
	   			"entity_id":-1,
	   			"is_loyalty_checkbox_enabled":"0",
	   			"voucher_series_id":"-1",
	   			"daily_budget":10000,
			    "create_adset":True,
			    "use_existing_adset":True,
			    "adset_id":social_user_calls().getRemoteAdset()
	   		}
	   	}
		communicationDetailObject = VenenoObject.communicationDetail(cdDetailsBody,extraParams=extraParams)
		communicationId = self.connObj.addMessageForRecipients(communicationDetailObject)
		SocialDBAssertion(self.campaigns['ORG'],self.groupVersionid,communicationId,self.numberOfUsers,socialAdsetInfo=False,aggregationDetail=False).check()
		
	@pytest.mark.parametrize('campaignType', [
    	('ORG')
        ])
	def test_flow_social_positive_withInternalCoupon_Sanity(self,campaignType):
		cdDetailsBody = {
		     'campaignId':self.campaigns[campaignType.upper()],
		     'targetType':'SOCIAL',
		     'communicationType':'FACEBOOK',
		     'subject':'',
		     'recipientListId':self.groupVersionid,
		     'overallRecipientCount':self.numberOfUsers,
		     'expectedDeliveryCount':self.numberOfUsers,
		     'groupName':self.groupName
		    }
	   	extraParams = {
	   		'voucher_series': self.voucherSeriesId,
	   		'default_argument' : {
	   			"entity_id":-1,
	   			"is_loyalty_checkbox_enabled":"0",
	   			"voucher_series_id":self.voucherSeriesId,
	   			"daily_budget":10000,
			    "create_adset":True,
			    "use_existing_adset":False,
			    "adset_name": 'AutoAdset_{}'.format(int(time.time()*1000))
	   		}
	   	}
		communicationDetailObject = VenenoObject.communicationDetail(cdDetailsBody,extraParams=extraParams)
		communicationId = self.connObj.addMessageForRecipients(communicationDetailObject)
		remoteCampaignId,remoteListId,remoteAdsetId,remoteOfferid = SocialDBAssertion(self.campaigns[campaignType.upper()],self.groupVersionid,communicationId,self.numberOfUsers,couponUsed=True).check()
		SocialRemoteObjectAssertion(self.campaigns[campaignType.upper()],remoteCampaignId,remoteListId,remoteAdsetId)

	def test_flow_social_positive_withInternalCoupon_CreateAdsetAsFalse(self):
		cdDetailsBody = {
		     'campaignId':self.campaigns['ORG'],
		     'targetType':'SOCIAL',
		     'communicationType':'FACEBOOK',
		     'subject':'',
		     'recipientListId':self.groupVersionid,
		     'overallRecipientCount':self.numberOfUsers,
		     'expectedDeliveryCount':self.numberOfUsers,
		     'groupName':self.groupName
		    }
	   	extraParams = {
	   		'voucher_series': self.voucherSeriesId,
	   		'default_argument' : {
	   			"entity_id":-1,
	   			"is_loyalty_checkbox_enabled":"0",
	   			"voucher_series_id":self.voucherSeriesId,
	   			"daily_budget":10000,
			    "create_adset":False
	   		}
	   	}
		communicationDetailObject = VenenoObject.communicationDetail(cdDetailsBody,extraParams=extraParams)
		communicationId = self.connObj.addMessageForRecipients(communicationDetailObject)
		SocialDBAssertion(self.campaigns['ORG'],self.groupVersionid,communicationId,self.numberOfUsers,couponUsed=True,socialAdsetInfo=False,aggregationDetail=False,venenoDataDetailsInfo=False).check()
		
	def test_flow_social_positive_withInternalCoupon_CreateAdsetAndUseExistingAsTrue(self):
		cdDetailsBody = {
		     'campaignId':self.campaigns['ORG'],
		     'targetType':'SOCIAL',
		     'communicationType':'FACEBOOK',
		     'subject':'',
		     'recipientListId':self.groupVersionid,
		     'overallRecipientCount':self.numberOfUsers,
		     'expectedDeliveryCount':self.numberOfUsers,
		     'groupName':self.groupName
		    }
	   	extraParams = {
	   		'voucher_series': self.voucherSeriesId,
	   		'default_argument' : {
	   			"entity_id":-1,
	   			"is_loyalty_checkbox_enabled":"0",
	   			"voucher_series_id":self.voucherSeriesId,
	   			"daily_budget":10000,
			    "create_adset":True,
			    "use_existing_adset":True,
			    "adset_id":social_user_calls().getRemoteAdset()
	   		}
	   	}
		communicationDetailObject = VenenoObject.communicationDetail(cdDetailsBody,extraParams=extraParams)
		communicationId = self.connObj.addMessageForRecipients(communicationDetailObject)
		SocialDBAssertion(self.campaigns['ORG'],self.groupVersionid,communicationId,self.numberOfUsers,couponUsed=True,socialAdsetInfo=False,aggregationDetail=False).check()
		
	def test_flow_social_skippedWithCouponExpired(self):
		try:
			SocialHelper.couponConfigChange({'fixedExpiryDate':int(time.time() * 1000 - 24 * 60 * 60 * 1000)},self.campaigns['ORG'],self.voucherSeriesId)
			cdDetailsBody= {
			     'campaignId':self.campaigns['ORG'],
			     'targetType':'SOCIAL',
			     'communicationType':'FACEBOOK',
			     'subject':'',
			     'recipientListId':self.groupVersionid,
			     'overallRecipientCount':self.numberOfUsers,
			     'expectedDeliveryCount':self.numberOfUsers,
			     'groupName':self.groupName
		    }
		   	extraParams = {
		   		'voucher_series': self.voucherSeriesId,
		   		'default_argument' : {
		   			"entity_id":-1,
		   			"is_loyalty_checkbox_enabled":"0",
		   			"voucher_series_id":self.voucherSeriesId,
		   			"daily_budget":10000,
				    "create_adset":True,
				    "use_existing_adset":False,
				    "adset_name": 'AutoAdset_{}'.format(int(time.time()*1000))
		   		}
		   	}
			communicationDetailObject = VenenoObject.communicationDetail(cdDetailsBody,extraParams=extraParams)
			communicationId = self.connObj.addMessageForRecipients(communicationDetailObject)
			SocialDBAssertion(self.campaigns['ORG'],
				self.groupVersionid,communicationId,
				self.numberOfUsers,
				couponUsed=True,
				skippedReason=['Coupon Could not be issued'],
				skippedUsers=True,
				socialAudienceList=False,
				socialAdsetInfo=False,
				aggregationDetail=False).check()
		except Exception,exp:
			Assertion.constructAssertion(False,'Failed with Exception :{}'.format(exp))
		finally:
			SocialHelper.couponConfigChange({'fixedExpiryDate':int(time.time() * 1000 + 24 * 60 * 60 * 1000)},self.campaigns['ORG'],self.voucherSeriesId)
			
	