import pytest

from src.modules.irisv2.campaigns.createCampaign import CreateCampaign
from src.modules.irisv2.list.checkAvailabilityName import CheckAvailabiltyName
from src.modules.irisv2.campaigns.checkAvailabilityCampaignName import CheckCampaignAvailabilty
from src.modules.irisv2.list.createAudience import CreateAudience
from src.utilities.logger import Logger
from src.utilities.utils import Utils


@pytest.mark.run(order=2)
class Test_checkAvailabilityCampaign():

    def setup_method(self, method):
        Logger.logMethodName(method.__name__)

    @pytest.mark.parametrize('campaignType,testControlType', [
        ('LIVE', 'ORG'),

    ])
    def test_irisV2_checkCampaignAvailability_Sanity(self, campaignType, testControlType):
        campaign = CreateCampaign.create(campaignType, testControlType)
        response = CheckCampaignAvailabilty.checkExists(campaign['NAME'])
        CheckCampaignAvailabilty.assertCheckExists(response, 200)

    @pytest.mark.parametrize('campaignType,testControlType', [

        ('LIVE', 'SKIP'),
        ('LIVE', 'CUSTOM'),
    ])
    def test_irisV2_checkCampaignAvailability(self, campaignType, testControlType):
        campaign = CreateCampaign.create(campaignType, testControlType)
        response = CheckCampaignAvailabilty.checkExists(campaign['NAME'])
        CheckCampaignAvailabilty.assertCheckExists(response, 200)

    @pytest.mark.parametrize('description,campaignName', [
        ('Name With Special Character', 'Name$$$####'),
        ('Name Doesnt Exist', 'NameDoesntExist')
    ])
    def test_irisV2_checkCampaignAvailability_Negative_VariationOfWrongName(self, description, campaignName):
        response = CheckCampaignAvailabilty.checkExists(campaignName)
        CheckCampaignAvailabilty.assertCheckExists(response, 200,isExists=False)

    @pytest.mark.parametrize('campaignType,testControlType,campaignName', [
            ('LIVE', 'ORG', 'test space2'+ str(Utils.getTime(milliSeconds=True)))


        ])
    def test_irisV2_checkCampaignAvailability_nameWithSpace(self, campaignType, testControlType,campaignName):
        campaign = CreateCampaign.create(campaignType, testControlType,
                                         name = campaignName)

        response = CheckCampaignAvailabilty.checkExists(campaign['NAME'])

        CheckCampaignAvailabilty.assertCheckExists(response, 200)

    @pytest.mark.parametrize(
            'campaignType,testControlType,campaignName', [

                ('LIVE', 'SKIP', 'test1234' + str(Utils.getTime(milliSeconds=True)))

    ])

    def test_irisV2_checkCampaignAvailability_nameWithNumericCharatcer(self, campaignType, testControlType, campaignName):
            campaign = CreateCampaign.create(campaignType, testControlType,
                                             name=campaignName)

            response = CheckCampaignAvailabilty.checkExists(campaign['NAME'])

            CheckCampaignAvailabilty.assertCheckExists(response, 200)







