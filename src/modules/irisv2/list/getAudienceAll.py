from src.dbCalls.campaignShard import list_Calls
from src.modules.irisv2.helper.irisHelper import IrisHelper
from src.modules.irisv2.list.getListDBAssertion import GetListDBAssertion
from src.utilities.assertion import Assertion
from src.utilities.logger import Logger
from src.utilities.utils import Utils


class GetAudienceAll():

    @staticmethod
    def getAll(queryParam):
        endpoint = IrisHelper.constructUrl('getById', queryParam=queryParam).replace('{group_id}', '')
        response = Utils.makeRequest(url=endpoint, data='', auth=IrisHelper.constructAuthenticate(),
                                     headers=IrisHelper.constructHeaders(), method='GET')
        return IrisHelper.constructResponse(response)

    @staticmethod
    def assertResponse(response, expectedStatusCode, expectedErrorCode=999999, expectedErrorMessage=''):
        if response['constructed'].lower() == 'pass':
            if expectedStatusCode >= 200 and expectedStatusCode <= 300:
                Assertion.constructAssertion(response['statusCode'] == int(expectedStatusCode),
                                             'Matching statusCode actual :{},expected :{}'.format(
                                                 response['statusCode'], expectedStatusCode))
            else:
                for errorReturned in response['json']['errors']:
                    Logger.log('Status Code :{} and error :{}', response['statusCode'], errorReturned)
                    Assertion.constructAssertion(response['statusCode'] == int(expectedStatusCode),
                                                 'Matching statusCode actual :{},expected :{}'.format(
                                                     response['statusCode'], expectedStatusCode))
                    Assertion.constructAssertion(errorReturned['code'] == expectedErrorCode,
                                                 'Matching Error Code ,actual:{} and expected:{}'.format(
                                                     errorReturned['code'], expectedErrorCode))
                    Assertion.constructAssertion(errorReturned['status'] == False, 'Checking for Error Status as False')
                    Assertion.constructAssertion(errorReturned['message'] == expectedErrorMessage,
                                                 'Matching Error Message ,actual:{} and expected'.format(
                                                     errorReturned['message'], expectedErrorMessage))
        else:
            Assertion.constructAssertion(False, 'Constructed Body has Failed due to Exception so no Validation')

    @staticmethod
    def assertGetByAll(queryParam, response, maxIdsCheck=20, actualGroupId = None):
        if 'data' not in response['json']: Assertion.constructAssertion(False,
                                                                        'No Entity Found In JSON Response from GetById')
        actualListOfGroupIds = GetAudienceAll.getGroupIdAsPerQueryParam(queryParam) if actualGroupId is None else actualGroupId
        Logger.log(actualListOfGroupIds)
        Assertion.constructAssertion(len(actualListOfGroupIds) == len(response['json']['data']),
                                     'Lenght of ActualEntities :{} and Expected :{}'.format(len(actualListOfGroupIds),
                                                                                            len(response['json'][
                                                                                                    'data'])))
        for eachEntity in response['json']['data']:
            if maxIdsCheck == 0:
                break
            else:
                maxIdsCheck = maxIdsCheck - 1
            Assertion.constructAssertion(str(eachEntity['id']) in actualListOfGroupIds,
                                         'GroupId :{} present in Expected List :{}'.format(eachEntity['id'],
                                                                                           actualListOfGroupIds))
            GetListDBAssertion(eachEntity['id'], {'json': {'entity': eachEntity}}, reachabilityCheck=False,
                               createAudienceJob=False, campaignGroupRecipients=False, listAllCheck=True).check()

    @staticmethod
    def getGroupIdAsPerQueryParam(queryParam):
        sortMap = {1: 'created_date'}
        offset = 0
        limit = 10
        sort = 'created_date'
        search = None
        if len(queryParam) == 0:
            return list_Calls().getAllGroupIds(limit, offset, sort, search)
        else:
            for each in queryParam:
                if 'offset' in each: offset = each[1]
                if 'limit' in each: limit = each[1]
                if 'sort' in each: sort = sortMap[each[1]]
                if 'search' in each: search = each[1]
                if 'type' in each:
                    type = each[1]
                    return  list_Calls().getAllGroupDetails(limit,offset,sort, groupType=type, onlyIds=True)
            return list_Calls().getAllGroupIds(limit, offset, sort, search)
