from src.dbCalls.campaignInfo import campaign_calls
from src.modules.irisv2.campaigns.getCampaignDBAssertion import GetCampaignDBAssertion
from src.modules.irisv2.helper.irisHelper import IrisHelper
from src.utilities.assertion import Assertion
from src.utilities.logger import Logger
from src.utilities.utils import Utils


class GetCampaignAll():
    @staticmethod
    def getAll(queryParam=[]):
        endpoint = IrisHelper.constructUrl('getcampaignbyid', queryParam=queryParam).replace('{campaignId}', '')
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
    def assertGetByAll(queryParam, response, maxIdsCheck=20):
        if 'data' not in response['json']: Assertion.constructAssertion(False,
                                                                        'No Entity Found In JSON Response from GetById')
        actualListOfCampaignIds = GetCampaignAll.getCampaignIdAsPerQueryParam(queryParam)
        Logger.log(actualListOfCampaignIds)
        Assertion.constructAssertion(len(actualListOfCampaignIds) == len(response['json']['data']),
                                     'Lenght of ActualEntities :{} and Expected :{}'.format(
                                         len(actualListOfCampaignIds),
                                         len(response['json'][
                                                 'data'])))
        for eachEntity in response['json']['data']:
            if maxIdsCheck == 0:
                break
            else:
                maxIdsCheck = maxIdsCheck - 1
            Assertion.constructAssertion(eachEntity['campaignId'] in actualListOfCampaignIds,
                                         'GroupId :{} present in Expected List :{}'.format(eachEntity['campaignId'],
                                                                                           actualListOfCampaignIds))
            GetCampaignDBAssertion(eachEntity['campaignId'], {'json': {'entity': eachEntity}}).check()

    @staticmethod
    def getCampaignIdAsPerQueryParam(queryParam):
        offset = 0
        limit = 10
        search = ''
        if len(queryParam) == 0:
            return campaign_calls().getCampaignIdAsPerQueryParam(limit, offset, search)
        else:
            for each in queryParam:
                if 'offset' in each: offset = each[1]
                if 'limit' in each: limit = each[1]
                if 'search' in each: search = each[1]
            return campaign_calls().getCampaignIdAsPerQueryParam(limit, offset, search)
