import pytest, time, json, pytest_ordering, copy
from datetime import datetime
from src.Constant.constant import constant
from src.utilities.logger import Logger
from src.modules.iris.construct import construct
from src.modules.iris.coupons import coupons
from src.utilities.assertion import Assertion
from src.modules.veneno.venenoObject import VenenoObject
from src.modules.veneno.venenoHelper import VenenoHelper
from src.modules.social.socialObject import SocialObject
from src.modules.social.socialHelper import SocialHelper
from src.modules.social.socialDBAssertion import SocialDBAssertion
from src.dbCalls.socialInfo import social_user_calls
from src.modules.social.socialRemoteObjectAssertion import SocialRemoteObjectAssertion

@pytest.mark.run(order=10)
class Test_Flow_Social_CUSTOM():

	def setup_class(self):
		self.numberOfUsers = 20
		self.campaigns = SocialHelper.createCampaignsForSocialThrift(testControlType=['CUSTOM'])
		self.groupVersionid,self.groupName = SocialHelper.createListForSocial(self.campaigns,'CUSTOM',numberOfUsers=self.numberOfUsers,newUser=True)
		self.remoteCampaignId = SocialHelper.createRemoteCampaignsForSocialThrift(self.campaigns['CUSTOM'])
		SocialHelper.updateRemoteCampaignIdInCampaignsBase(self.campaigns['CUSTOM'],self.remoteCampaignId)
		self.voucherSeriesId = coupons.createCoupons(campaignId=self.campaigns['CUSTOM'],payloadData={'couponLimit':{'limit':0, 'type':'UNLIMITED'}, 'discountOn':'BILL', 'discountType':'ABS', 'discountValue':10})[0]['json']['entity']['voucherSeriesId']

	def setup_method(self, method):
		self.connObj = VenenoHelper.getConnObj(newConnection=True)
		Logger.logMethodName(method.__name__)

	@pytest.mark.parametrize('campaignType', [
    	('CUSTOM')
        ])
	def test_flow_social_positive_withoutCoupon(self,campaignType):
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
		     'campaignId':self.campaigns['CUSTOM'],
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
		SocialDBAssertion(self.campaigns['CUSTOM'],self.groupVersionid,communicationId,self.numberOfUsers,socialAdsetInfo=False,aggregationDetail=False,venenoDataDetailsInfo=False).check()
		
	def test_flow_social_positive_withoutCoupon_CreateAdsetAndUseExistingAsTrue(self):
		cdDetailsBody = {
		     'campaignId':self.campaigns['CUSTOM'],
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
		SocialDBAssertion(self.campaigns['CUSTOM'],self.groupVersionid,communicationId,self.numberOfUsers,socialAdsetInfo=False,aggregationDetail=False).check()
		
	@pytest.mark.parametrize('campaignType', [
    	('CUSTOM')
        ])
	def test_flow_social_positive_withInternalCoupon(self,campaignType):
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
		     'campaignId':self.campaigns['CUSTOM'],
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
		SocialDBAssertion(self.campaigns['CUSTOM'],self.groupVersionid,communicationId,self.numberOfUsers,couponUsed=True,socialAdsetInfo=False,aggregationDetail=False,venenoDataDetailsInfo=False).check()
		
	def test_flow_social_positive_withInternalCoupon_CreateAdsetAndUseExistingAsTrue(self):
		cdDetailsBody = {
		     'campaignId':self.campaigns['CUSTOM'],
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
		SocialDBAssertion(self.campaigns['CUSTOM'],self.groupVersionid,communicationId,self.numberOfUsers,couponUsed=True,socialAdsetInfo=False,aggregationDetail=False).check()
		
	def test_flow_social_skippedWithCouponExpired(self):
		try:
			SocialHelper.couponConfigChange({'fixedExpiryDate':int(time.time() * 1000 - 24 * 60 * 60 * 1000)},self.campaigns['CUSTOM'],self.voucherSeriesId)
			cdDetailsBody= {
			     'campaignId':self.campaigns['CUSTOM'],
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
			SocialDBAssertion(self.campaigns['CUSTOM'],
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
			SocialHelper.couponConfigChange({'fixedExpiryDate':int(time.time() * 1000 + 24 * 60 * 60 * 1000)},self.campaigns['CUSTOM'],self.voucherSeriesId)
			
	