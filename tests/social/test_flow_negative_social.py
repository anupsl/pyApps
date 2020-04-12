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
from src.modules.social.socialRemoteObjectAssertion import SocialRemoteObjectAssertion

@pytest.mark.run(order=7)
@pytest.mark.skipif(constant.config['cluster'] not in ['nightly', 'staging'], reason='Negative Cases should run only on Nightly and Staging')
class Test_Flow_Negative_Social():

	def setup_class(self):
		self.numberOfUsers = 20
		self.campaigns = SocialHelper.createCampaignsForSocialThrift(testControlType=['ORG'])
		self.groupVersionid,self.groupName = SocialHelper.createListForSocial(self.campaigns,'ORG',numberOfUsers=self.numberOfUsers,newUser=True)
		self.voucherSeriesId = coupons.createCoupons(campaignId=self.campaigns['ORG'],payloadData={'couponLimit':{'limit':0, 'type':'UNLIMITED'}, 'discountOn':'BILL', 'discountType':'ABS', 'discountValue':10})[0]['json']['entity']['voucherSeriesId']

	def setup_method(self, method):
		self.connObj = VenenoHelper.getConnObj(newConnection=True)
		Logger.logMethodName(method.__name__)

	def test_flow_social_skipped_fbException(self):
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
		SocialHelper.validateAggregationDetailInExceptionCase(communicationId)
			
	def test_flow_social_skipped_accountDetailsWrong(self):
		ckvId = SocialHelper.updateConfigKeyValue(0)
		try:
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
			SocialHelper.assertCommunicationDetailInErrorState(self.groupVersionid,communicationId)
		except Exception,exp:
			Assertion.constructAssertion(False,'Excpetion :{}'.format(exp))
		finally:
			SocialHelper.updateConfigKeyValue(1,ckvId)