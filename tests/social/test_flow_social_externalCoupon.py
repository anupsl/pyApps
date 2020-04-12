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
from src.modules.luci.luciHelper import LuciHelper
from src.modules.luci.luciObject import LuciObject
from src.modules.luci.dracarysObject import DracarysObject
from src.modules.luci.dracarysHelper import DracarysHelper
from src.modules.social.socialDBAssertion import SocialDBAssertion
from src.dbCalls.socialInfo import social_user_calls
from src.modules.social.socialRemoteObjectAssertion import SocialRemoteObjectAssertion

@pytest.mark.run(order=9)
class Test_Flow_Social_ExternalCoupon():

	def setup_class(self):
		self.numberOfUsers = 20
		self.constructObj = LuciObject()
		self.DracarysObj = DracarysObject()
		self.DracraysConnObj = DracarysHelper.getConnObj(newConnection=True)
		self.campaigns = SocialHelper.createCampaignsForSocialThrift(testControlType=['ORG'])
		self.groupVersionid,self.groupName = SocialHelper.createListForSocial(self.campaigns,'ORG',numberOfUsers=self.numberOfUsers,newUser=True)
		self.remoteCampaignId = SocialHelper.createRemoteCampaignsForSocialThrift(self.campaigns['ORG'])
		SocialHelper.updateRemoteCampaignIdInCampaignsBase(self.campaigns['ORG'],self.remoteCampaignId)
		self.voucherSeriesId = coupons.createCoupons(campaignId=self.campaigns['ORG'],payloadData={'couponLimit':{'limit':0, 'type':'UNLIMITED'}, 'discountOn':'BILL', 'discountType':'ABS', 'discountValue':10})[0]['json']['entity']['voucherSeriesId']
		SocialHelper.couponConfigChange({'client_handling_type':'EXTERNAL_ISSUAL','any_user':True},self.campaigns['ORG'],self.voucherSeriesId)
			
	def setup_method(self, method):
		self.connObj = VenenoHelper.getConnObj(newConnection=True)
		constant.config['uploadedFileName'] = method.__name__
		Logger.logMethodName(method.__name__)

	def est_flow_social_negative_withExternalCoupon(self):
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
			    "use_existing_adset":False,
			    "adset_name": 'AutoAdset_{}'.format(int(time.time()*1000))
	   		}
	   	}
		communicationDetailObject = VenenoObject.communicationDetail(cdDetailsBody,extraParams=extraParams)
		communicationId = self.connObj.addMessageForRecipients(communicationDetailObject)
		SocialHelper.assertCommunicationDetailInErrorState(self.groupVersionid,communicationId)
		SocialHelper.assertAggregationDetailAndAudienceListCreated(self.groupVersionid,communicationId)

	def est_flow_social_positive_withExternalCoupon_Sanity(self):
		couponsused = LuciHelper.uploadCouponAndAssertions(self, self.voucherSeriesId, 2,noOfCouponsToBeUpload = 20)['coupons']
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
			    "use_existing_adset":False,
			    "adset_name": 'AutoAdset_{}'.format(int(time.time()*1000))
	   		}
	   	}
		communicationDetailObject = VenenoObject.communicationDetail(cdDetailsBody,extraParams=extraParams)
		communicationId = self.connObj.addMessageForRecipients(communicationDetailObject)
		remoteCampaignId,remoteListId,remoteAdsetId,remoteOfferid = SocialDBAssertion(self.campaigns['ORG'],self.groupVersionid,communicationId,self.numberOfUsers,couponUsed=True,couponUsedExteranal=True,socialOffer=True,externalOfferList=couponsused).check()
		SocialRemoteObjectAssertion(self.campaigns['ORG'],remoteCampaignId,remoteListId,remoteAdsetId)

	def est_flow_social_positive_withExternalCoupon_CreateAdsetAsFalse(self):
		couponsused = LuciHelper.uploadCouponAndAssertions(self, self.voucherSeriesId, 2,noOfCouponsToBeUpload = 20)['coupons']
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
		SocialDBAssertion(self.campaigns['ORG'],self.groupVersionid,communicationId,self.numberOfUsers,couponUsed=True,couponUsedExteranal=True,socialOffer=False,externalOfferList=couponsused,socialAdsetInfo=False,aggregationDetail=False,venenoDataDetailsInfo=False).check()
		
	def est_flow_social_positive_withExternalCoupon_CreateAdsetAndUseExistingAsTrue(self):
		couponsused = LuciHelper.uploadCouponAndAssertions(self, self.voucherSeriesId, 2,noOfCouponsToBeUpload = 20)['coupons']
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
		SocialDBAssertion(self.campaigns['ORG'],self.groupVersionid,communicationId,self.numberOfUsers,couponUsed=True,couponUsedExteranal=True,socialOffer=True,externalOfferList=couponsused,socialAdsetInfo=True,aggregationDetail=True).check()
		