import pytest, time, json, pytest_ordering, copy
from src.Constant.constant import constant
from src.utilities.logger import Logger
from src.modules.iris.construct import construct
from src.modules.social.socialObject import SocialObject
from src.modules.social.socialHelper import SocialHelper

@pytest.mark.run(order=3)
class Test_Social_Thrift_CreateCampaign():

	def setup_class(self):
		self.campaigns = SocialHelper.createCampaignsForSocialThrift()

	def setup_method(self, method):
		self.connObj = SocialHelper.getConnObj(newConnection=True)
		Logger.logMethodName(method.__name__)

	@pytest.mark.parametrize('socialStatus', [
    	('ACTIVE'),
        ('PAUSED')
        ])
	def test_socialThrift_createCampaign_Sanity(self,socialStatus):
		SocialCampaign = self.connObj.createCampaign(
			constant.config['orgId'],
			SocialObject().SocialChannel['facebook'],
			SocialObject.SocialCampaign(
					'SocialCampaign_{}'.format(int(time.time()*1000)),
					constant.config['orgId'],
					self.campaigns['ORG'],
					socialCampaignStatus=socialStatus
				),
			'requestId_automationthriftCall_{}'.format(int(time.time()*1000))
		)
		SocialHelper.assertCreateCampaignForSocial(self.campaigns['ORG'],SocialCampaign)