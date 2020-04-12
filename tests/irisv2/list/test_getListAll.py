import pytest, pytest_ordering, time
from src.utilities.logger import Logger
from src.modules.irisv2.list.getAudienceAll import GetAudienceAll

@pytest.mark.run(order=13)
class Test_GetAudienceAll():
    
    def setup_method(self, method):
        Logger.logMethodName(method.__name__)
    
    @pytest.mark.parametrize('description,queryParam,maxIdsCheck', [
        ('Without Any Query Param ', [], 20),
    ])

    def test_irisV2_getListAll_limit_Sanity(self, description, queryParam, maxIdsCheck):
        groupIds = GetAudienceAll.getGroupIdAsPerQueryParam(queryParam)
        response = GetAudienceAll.getAll(queryParam)
        GetAudienceAll.assertResponse(response, 200)
        GetAudienceAll.assertGetByAll(queryParam, response, maxIdsCheck=maxIdsCheck, actualGroupId=groupIds)

    @pytest.mark.parametrize('description,queryParam,maxIdsCheck', [

        ('With Limit Lower Value', [('limit', 1)], 1),
        ('With Limit Higher Value', [('limit', 20)], 1)
    ])
    def test_irisV2_getListAll_limit(self, description, queryParam, maxIdsCheck):
        groupIds = GetAudienceAll.getGroupIdAsPerQueryParam(queryParam)
        response = GetAudienceAll.getAll(queryParam)
        GetAudienceAll.assertResponse(response, 200)
        GetAudienceAll.assertGetByAll(queryParam, response, maxIdsCheck=maxIdsCheck, actualGroupId=groupIds)

    @pytest.mark.parametrize('description,queryParam,maxIdsCheck', [
        ('With Limit Lower Value', [('offset', 1)], 2),
        ('With Limit Higher Value', [('offset', 20)], 2)
        ])
    def test_irisV2_getListAll_Offset(self, description, queryParam, maxIdsCheck):
        response = GetAudienceAll.getAll(queryParam)
        GetAudienceAll.assertResponse(response, 200)
        GetAudienceAll.assertGetByAll(queryParam, response, maxIdsCheck=maxIdsCheck)
    
    @pytest.mark.parametrize('description,queryParam,maxIdsCheck', [
        ('With Sort Value 1 : auto_updated_time', [('sort', 1)], 2),
        ])
    def test_irisV2_getListAll_sort(self, description, queryParam, maxIdsCheck):
        response = GetAudienceAll.getAll(queryParam)
        GetAudienceAll.assertResponse(response, 200)
        GetAudienceAll.assertGetByAll(queryParam, response, maxIdsCheck=maxIdsCheck)
       
    @pytest.mark.parametrize('description,queryParam,maxIdsCheck', [
        ('With Search Value As : Auto', [('search', 'Auto')], 2),
        ])
    def test_irisV2_getListAll_search(self, description, queryParam, maxIdsCheck):
        groupIds = GetAudienceAll.getGroupIdAsPerQueryParam(queryParam)
        response = GetAudienceAll.getAll(queryParam)
        GetAudienceAll.assertResponse(response, 200)
        GetAudienceAll.assertGetByAll(queryParam, response, maxIdsCheck=maxIdsCheck, actualGroupId=groupIds)
    
    @pytest.mark.parametrize('queryParam,maxIdsCheck', [
        ([('limit', 5), ('offset', 0), ('sort', 1), ('search', 'Auto')], 5),
        ([('limit', 5), ('offset', 5), ('sort', 1), ('search', 'campaignUI')], 5),
        ([('limit', 5), ('offset', 10), ('sort', 1), ('search', 'Auto')], 5),
        ([('limit', 1), ('offset', 1), ('sort', 1), ('search', 'Auto')], 5),
        ([('limit', 5), ('offset', 2), ('sort', 1), ('search', 'Timeline')], 5),
        ([('limit', 1), ('sort', 1), ('search', 'Auto')], 5),
        ([('offset', 5), ('sort', 1), ('search', 'campaign')], 5),
        ([('offset', 5), ('sort', 1), ('type', 'ORG_USERS')], 5),
        ])
    def test_irisV2_getListAll_variation_WithCombinationOfQueryParam(self, queryParam, maxIdsCheck):
        groupIds = GetAudienceAll.getGroupIdAsPerQueryParam(queryParam)
        response = GetAudienceAll.getAll(queryParam)
        GetAudienceAll.assertResponse(response, 200)
        GetAudienceAll.assertGetByAll(queryParam, response, maxIdsCheck=maxIdsCheck, actualGroupId=groupIds)

    @pytest.mark.parametrize('queryParam,statusCode,errorCode,errorDescription', [
        ([('limit', -1)], 400, 102, 'Invalid request : Limit should be greater than 1'),
        ([('limit', 0)], 400, 102, 'Invalid request : Limit should be greater than 1'),
        ([('limit', 21)], 400, 102, 'Invalid request : Maximum 20 groups allowed in singe request'),
        ([('limit', 999)], 400, 102, 'Invalid request : Maximum 20 groups allowed in singe request')
        ])   
    def test_irisV2_getListAll_limit_BoundaryValue(self, queryParam, statusCode, errorCode, errorDescription):
        response = GetAudienceAll.getAll(queryParam)
        GetAudienceAll.assertResponse(response, statusCode, errorCode, errorDescription)
    
    @pytest.mark.parametrize('queryParam,statusCode,errorCode,errorDescription', [
        ([('offset', -1)], 400, 102, 'Invalid request : Offset cannot be negative'),
        ]) 
    def test_irisV2_getListAll_OffsetBoundaryValue(self, queryParam, statusCode, errorCode, errorDescription):
        response = GetAudienceAll.getAll(queryParam)
        GetAudienceAll.assertResponse(response, statusCode, errorCode, errorDescription)
       
    @pytest.mark.parametrize('queryParam,statusCode,errorCode,errorDescription', [
        ([('offset', 0), ('limit', 0)], 400, 102, 'Invalid request : Limit should be greater than 1'),
        ([('offset', 0), ('limit', -1)], 400, 102, 'Invalid request : Limit should be greater than 1'),
        ([('offset', -1), ('limit', 1)], 400, 102, 'Invalid request : Offset cannot be negative'),
        ]) 
    def test_irisV2_getListAll_OffsetAndLimitInvalid(self, queryParam, statusCode, errorCode, errorDescription):
        response = GetAudienceAll.getAll(queryParam)
        GetAudienceAll.assertResponse(response, statusCode, errorCode, errorDescription)
       
    @pytest.mark.parametrize('queryParam,statusCode,errorCode,errorDescription', [
        ([('sort', 2)], 400, 5005, 'invalid request : invalid audience group sort'),
        ])
    def test_irisV2_getListAll_sort_UnknownSortValue(self, queryParam, statusCode, errorCode, errorDescription):
        response = GetAudienceAll.getAll(queryParam)
        GetAudienceAll.assertResponse(response, statusCode, errorCode, errorDescription)
       
    @pytest.mark.parametrize('queryParam,statusCode', [
        ([('search', 'ThereisNoSuchListWithThisName')], 200),
        ])
    def test_irisV2_getListAll_search_WithNoSuchList(self, queryParam, statusCode):
        response = GetAudienceAll.getAll(queryParam)
        GetAudienceAll.assertResponse(response, statusCode)
    
    @pytest.mark.parametrize('queryParam,maxIdsCheck', [
        ([('limit', 5), ('offet', 0), ('sort', 1), ('search', 'Auto')], 5),
        ([('limit', 5), ('offset', 5), ('sorting', 1), ('search', 'campaignUI')], 5),
        ([('limit', 5), ('offset', 5), ('sort', 1), ('like', 'campaignUI')], 5),
        ])
    def test_irisV2_getListAll_variation_InvalidParams(self, queryParam, maxIdsCheck):
        groupIds = GetAudienceAll.getGroupIdAsPerQueryParam(queryParam)
        response = GetAudienceAll.getAll(queryParam)
        GetAudienceAll.assertResponse(response, 200)
        GetAudienceAll.assertGetByAll(queryParam, response, maxIdsCheck=maxIdsCheck, actualGroupId=groupIds)

