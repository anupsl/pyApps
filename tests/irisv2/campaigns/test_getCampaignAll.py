import pytest
from src.modules.irisv2.campaigns.getCampaignMessageStatsDBAssertion import GetCampaignMessageStatsDBAssertion
from src.modules.irisv2.campaigns.getCampaignMessageStatsDBAssertion import GetCampaignPerformanceStatsDBAssertion
from src.modules.irisv2.campaigns.getCampaignAll import GetCampaignAll
from src.utilities.logger import Logger
from src.Constant.constant import constant

@pytest.mark.run(order=4)
class Test_getCampaignsAll():
    def setup_method(self, method):
        Logger.logMethodName(method.__name__)

    @pytest.mark.parametrize('description,queryParam,maxIdsCheck', [
        ('Without Any Query Param ', [], 20)
    ])
    def test_irisV2_getCampaignAll_limit_Sanity(self, description, queryParam, maxIdsCheck):
        response = GetCampaignAll.getAll(queryParam)
        GetCampaignAll.assertResponse(response, 200)
        GetCampaignAll.assertGetByAll(queryParam, response, maxIdsCheck)

    @pytest.mark.parametrize('description,queryParam,maxIdsCheck', [

        ('With Limit Lower Value', [('limit', 1)], 1),
        ('With Limit Higher Value', [('limit', 20)], 1)
    ])
    def test_irisV2_getCampaignAll_limit(self, description, queryParam, maxIdsCheck):
        response = GetCampaignAll.getAll(queryParam)
        GetCampaignAll.assertResponse(response, 200)
        GetCampaignAll.assertGetByAll(queryParam, response, maxIdsCheck)

    @pytest.mark.parametrize('description,queryParam,maxIdsCheck', [
        ('With Limit Lower Value', [('offset', 1)], 2),
        ('With Limit Higher Value', [('offset', 20)], 2)
    ])
    def test_irisV2_getCampaignAll_Offset(self, description, queryParam, maxIdsCheck):
        response = GetCampaignAll.getAll(queryParam)
        GetCampaignAll.assertResponse(response, 200)
        GetCampaignAll.assertGetByAll(queryParam, response, maxIdsCheck)

    @pytest.mark.parametrize('description,queryParam,maxIdsCheck', [
        ('With Sort Value 1 : auto_updated_time', [('sort', 1)], 2),
    ])
    def test_irisV2_getCampaignAll_sort(self, description, queryParam, maxIdsCheck):
        response = GetCampaignAll.getAll(queryParam)
        GetCampaignAll.assertResponse(response, 200)
        GetCampaignAll.assertGetByAll(queryParam, response, maxIdsCheck)

    @pytest.mark.parametrize('description,queryParam,maxIdsCheck', [
        ('With Search Value As : Auto', [('search', 'Auto')], 2),
    ])
    def test_irisV2_getCampaignAll_search(self, description, queryParam, maxIdsCheck):
        response = GetCampaignAll.getAll(queryParam)
        GetCampaignAll.assertResponse(response, 200)
        GetCampaignAll.assertGetByAll(queryParam, response, maxIdsCheck)

    @pytest.mark.parametrize('queryParam,maxIdsCheck', [
        ([('limit', 5), ('offset', 0), ('sort', 1), ('search', 'Auto')], 5),
        ([('limit', 5), ('offset', 5), ('sort', 1), ('search', 'campaignUI')], 5),
        ([('limit', 5), ('offset', 10), ('sort', 1), ('search', 'Auto')], 5),
        ([('limit', 1), ('offset', 1), ('sort', 1), ('search', 'Auto')], 5),
        ([('limit', 5), ('offset', 2), ('sort', 1), ('search', 'Timeline')], 5),
        ([('limit', 1), ('sort', 1), ('search', 'Auto')], 5),
        ([('offset', 5), ('sort', 1), ('search', 'ampaign')], 5),
    ])
    def test_irisV2_getCampaignAll_variation_WithCombinationOfQueryParam(self, queryParam, maxIdsCheck):
        response = GetCampaignAll.getAll(queryParam)
        GetCampaignAll.assertResponse(response, 200)
        GetCampaignAll.assertGetByAll(queryParam, response, maxIdsCheck)

    @pytest.mark.parametrize('queryParam,statusCode,errorCode,errorDescription', [
        ([('limit', -1)], 400, 102, 'Invalid request : Limit minimum should be 1.'),
        ([('limit', 0)], 400, 102, 'Invalid request : Limit minimum should be 1.'),
        ([('limit', 21)], 400, 102, 'Invalid request : Limit maximum can be 20.'),
        ([('limit', 999)], 400, 102, 'Invalid request : Limit maximum can be 20.')
    ])
    def test_irisV2_getCampaignAll_limit_BoundaryValue(self, queryParam, statusCode, errorCode, errorDescription):
        response = GetCampaignAll.getAll(queryParam)
        GetCampaignAll.assertResponse(response, statusCode, errorCode, errorDescription)

    @pytest.mark.parametrize('queryParam,statusCode,errorCode,errorDescription', [
        ([('offset', -1)], 500, 1001, 'Unexpected error : Page index must not be less than zero!'),
    ])
    def test_irisV2_getCampaignAll_OffsetBoundaryValue(self, queryParam, statusCode, errorCode, errorDescription):
        response = GetCampaignAll.getAll(queryParam)
        GetCampaignAll.assertResponse(response, statusCode, errorCode, errorDescription)

    @pytest.mark.parametrize('queryParam,statusCode,errorCode,errorDescription', [
        ([('offset', 0), ('limit', 0)], 400, 102, 'Invalid request : Limit minimum should be 1.'),
        ([('offset', 0), ('limit', -1)], 400, 102, 'Invalid request : Limit minimum should be 1.'),
        ([('offset', -1), ('limit', 1)], 500, 1001, 'Unexpected error : Page index must not be less than zero!'),
    ])
    def test_irisV2_getCampaignAll_OffsetAndLimitInvalid(self, queryParam, statusCode, errorCode, errorDescription):
        response = GetCampaignAll.getAll(queryParam)
        GetCampaignAll.assertResponse(response, statusCode, errorCode, errorDescription)

    @pytest.mark.parametrize('queryParam,statusCode', [
        ([('search', 'ThereisNoSuchListWithThisName')], 200),
    ])
    def test_irisV2_getCampaignAll_search_WithNoSuchList(self, queryParam, statusCode):
        response = GetCampaignAll.getAll(queryParam)
        GetCampaignAll.assertResponse(response, statusCode)

    @pytest.mark.parametrize('queryParam', [
        ([('limit', 5), ('offet', 0), ('sort', 1), ('search', 'Auto')]),
        ([('limit', 5), ('offset', 5), ('sorting', 1), ('search', 'campaignUI')]),
        ([('limit', 5), ('offset', 5), ('sort', 1), ('like', 'campaignUI')]),
    ])
    def test_irisV2_getCampaignAll_variation_InvalidParams(self, queryParam):
        response = GetCampaignAll.getAll(queryParam)
        GetCampaignAll.assertResponse(response, 200)

    @pytest.mark.parametrize('queryParam', [
        ([('messageStats','True')])
    ])
    def test_irisV2_getCampaign_messageStats(self,queryParam):
        response = GetCampaignAll.getAll(queryParam)
        GetCampaignAll.assertResponse(response, 200)
        GetCampaignMessageStatsDBAssertion.check(self,response)

    @pytest.mark.parametrize('queryParam', [
        ([('performanceStats', 'True'),('search',constant.config['performanceStats']['name'])])
    ])
    def test_irisV2_getCampaign_performanceStats(self, queryParam):

        response = GetCampaignAll.getAll(queryParam)
        GetCampaignAll.assertResponse(response, 200)



