import pytest

from src.utilities.logger import Logger
from src.modules.irisv2.campaigns.campaignSetting import CampaignSetting
from src.dbCalls.campaignInfo import campaign_calls
from src.modules.irisv2.campaigns.getCampaignSettingDBAssertion import GetCampaignSettingDBAssertion

@pytest.mark.run(order=6)
class Test_getCampaignSettings():

    def setup_method(self, method):
        Logger.logMethodName(method.__name__)


    def test_irisV2_getCampaignSettings_Sanity(self):

        get = CampaignSetting.getSettings()
        CampaignSetting.assertResponse(get['RESPONSE'], 200)
        response = get['RESPONSE']['json']['entity']
        GetCampaignSettingDBAssertion(response).check()

