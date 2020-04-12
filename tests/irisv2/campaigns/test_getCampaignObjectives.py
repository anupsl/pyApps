import pytest

from src.utilities.logger import Logger
from src.modules.irisv2.campaigns.campaignObjectives import CampaignObjectives
from src.modules.irisv2.campaigns.campaignObjectiveDBAssertion import CampaignObjectiveDBAssertion

@pytest.mark.run(order=6)
class Test_getCampaignObjectives():

    def setup_method(self, method):
        Logger.logMethodName(method.__name__)


    def test_irisV2_getObjectives_Sanity(self):

        get = CampaignObjectives.getObjectives()
        CampaignObjectives.assertResponse(get['RESPONSE'], 200)
        CampaignObjectiveDBAssertion(get['RESPONSE']).check()


