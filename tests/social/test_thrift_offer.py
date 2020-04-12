import pytest, time, json, pytest_ordering, copy
from datetime import datetime
from src.Constant.constant import constant
from src.utilities.logger import Logger
from src.modules.iris.construct import construct
from src.modules.social.socialObject import SocialObject
from src.modules.social.socialHelper import SocialHelper

@pytest.mark.run(order=6)
class Test_Social_Thrift_Offer():

	def setup_method(self, method):
	    self.connObj = SocialHelper.getConnObj(newConnection=True)
	    Logger.logMethodName(method.__name__)

	@pytest.mark.parametrize('offerType,offerValue,socialCouponType', [
		('percentage_off',10,'generic'),
    	('cash_discount',10,'generic')
   	])
	def test_thrift_createNativeOffer_without_socialOfferCouponsCsvFileInfo_Sanity(self,offerType,offerValue,socialCouponType):
		SocialOffer = self.connObj.createNativeOffer(
			constant.config['orgId'],
			SocialObject().SocialChannel['facebook'],
			SocialObject.SocialOffer(
					{
							'offerType':offerType,
							'offerText':'offerText_{}'.format(int(time.time())),
							'offerValue':offerValue,
							'socialOfferCouponsCsvFileInfo':None,
							'redemptionCode':'redemptionCode_{}'.format(int(time.time()))
					},
					constant.config['facebook']['pageId'],
					SocialObject().OfferLocationType['offline'],
					'overviewDetails_{}'.format(int(time.time())),
					datetime.fromtimestamp(time.time()+ 25*60*60).strftime('%Y-%m-%dT%H:%M:%S'),
					socialCouponType
				),
			'requestId_automationthriftCall_{}'.format(int(time.time()*1000))
		)
		SocialHelper.assertOfferCreation(SocialOffer)
	