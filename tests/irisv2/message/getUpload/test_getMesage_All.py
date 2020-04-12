import pytest

from src.modules.irisv2.message.getMessage import GetMessage
from src.utilities.assertion import Assertion
from src.utilities.logger import Logger

@pytest.mark.run(order=40)
class Test_GetMessage_All():
    def setup_method(self, method):
        Logger.logMethodName(method.__name__)

    @pytest.mark.parametrize('campaignType,testControlType', [
        ('LIVE', 'ORG'),

    ])
    def test_irisv2_getMessage_All_Sanity_Campaign_Variations(self, campaignType, testControlType):
        campaignId = GetMessage.getCampaignID(campaignType, testControlType)
        getMessageAllResponse = GetMessage.getMessageAll(campaignId)
        GetMessage.assertResponse(getMessageAllResponse, 200)
        GetMessage.validateGetAll(getMessageAllResponse['json']['data'], campaignId)

    @pytest.mark.parametrize('campaignType,testControlType', [
        ('LIVE', 'CUSTOM'),
        ('UPCOMING', 'ORG'),
        ('UPCOMING', 'SKIP'),
        ('LAPSED', 'CUSTOM'),
        ('LAPSED', 'SKIP')
    ])
    def test_irisv2_getMessage_All_Campaign_Variations(self, campaignType, testControlType):
        campaignId = GetMessage.getCampaignID(campaignType, testControlType)
        getMessageAllResponse = GetMessage.getMessageAll(campaignId)
        GetMessage.assertResponse(getMessageAllResponse, 200)
        GetMessage.validateGetAll(getMessageAllResponse['json']['data'], campaignId)

    @pytest.mark.parametrize('campaignType,testControlType', [
        ('LIVE', 'ORG'),
        ('UPCOMING', 'ORG'),
        ('UPCOMING', 'CUSTOM'),
        ('LAPSED', 'CUSTOM'),
        ('LAPSED', 'SKIP')
    ])
    def test_irisv2_getMessage_All_WithQueryParam_targetAudience(self, campaignType, testControlType):
        campaignId = GetMessage.getCampaignID(campaignType, testControlType)
        getMessageAllResponse = GetMessage.getMessageAll(campaignId, queryParam=[('includeAudience', 'true')])
        GetMessage.assertResponse(getMessageAllResponse, 200)
        GetMessage.validateGetAllAudienceInclude(getMessageAllResponse['json']['data'], campaignId)

    @pytest.mark.parametrize('campaignType,testControlType', [
        ('LIVE', 'ORG'),
        ('LIVE', 'CUSTOM'),
        ('LIVE', 'SKIP'),
        ('UPCOMING', 'ORG'),
        ('UPCOMING', 'CUSTOM'),
        ('UPCOMING', 'SKIP'),
        ('LAPSED', 'ORG'),
        ('LAPSED', 'CUSTOM'),
        ('LAPSED', 'SKIP')
    ])
    def test_irisv2_getMessage_All_WithQueryParam_Variant(self, campaignType, testControlType):
        campaignId = GetMessage.getCampaignID(campaignType, testControlType)
        getMessageAllResponse = GetMessage.getMessageAll(campaignId, queryParam=[('includeVariant', 'true')])
        GetMessage.assertResponse(getMessageAllResponse, 200)
        GetMessage.validateGetAllVaraintsInclude(getMessageAllResponse['json']['data'], campaignId)

    @pytest.mark.parametrize('campaignType,testControlType', [
        ('LIVE', 'ORG'),
        ('UPCOMING', 'ORG'),
        ('UPCOMING', 'CUSTOM'),
        ('LAPSED', 'ORG')
    ])
    def test_irisv2_getMessage_All_WithQueryParam_targetAudience_Variant(self, campaignType, testControlType):
        campaignId = GetMessage.getCampaignID(campaignType, testControlType)
        getMessageAllResponse = GetMessage.getMessageAll(campaignId, queryParam=[('includeVariant', 'true'),
                                                                                 ('includeAudience', 'true')])
        GetMessage.assertResponse(getMessageAllResponse, 200)
        GetMessage.validateGetAll(getMessageAllResponse['json']['data'], campaignId)
        GetMessage.validateGetAllAudienceInclude(getMessageAllResponse['json']['data'], campaignId)
        GetMessage.validateGetAllVaraintsInclude(getMessageAllResponse['json']['data'], campaignId)

    @pytest.mark.parametrize('campaignType,testControlType', [
        ('LIVE', 'ORG'),
        ('LAPSED', 'SKIP')
    ])
    def test_irisv2_getMessage_All_WithQueryParam_targetAudience_Variant_False(self, campaignType,
                                                                                      testControlType):
        campaignId = GetMessage.getCampaignID(campaignType, testControlType)
        getMessageAllResponse = GetMessage.getMessageAll(campaignId, queryParam=[('includeVariant', 'false'),
                                                                                 ('includeAudience', 'false')])
        GetMessage.assertResponse(getMessageAllResponse, 200)
        GetMessage.validateGetAll(getMessageAllResponse['json']['data'], campaignId)
        GetMessage.validateGetAllIncludeVariantAndAudienceAsFalse(response=getMessageAllResponse['json']['data'])

    def test_irisv2_getMessage_All_WhenNoMessageInCampaign(self):
        campaignId = GetMessage.getCampaignIDHavingNoMessage('LIVE', 'ORG')
        getMessageAllResponse = GetMessage.getMessageAll(campaignId)
        GetMessage.assertResponse(getMessageAllResponse, 200)
        Assertion.constructAssertion(len(getMessageAllResponse['json']['data']) == 0,
                                     'Lenght Of getMessage Array is :{}'.format(
                                         len(getMessageAllResponse['json']['data'])))
