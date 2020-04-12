
from src.modules.irisv2.helper.irisHelper import IrisHelper
from src.utilities.logger import Logger
from src.utilities.assertion import Assertion
from src.utilities.utils import Utils
from src.Constant.constant import constant
from src.dbCalls.campaignInfo import orgStatus
from src.dbCalls.messageInfo import pocMetaInfo
import copy

class OrgV2Status():
    @staticmethod
    def getOrgV2Status():
        orgStatusEndpoint = IrisHelper.constructUrl('orgv2status')

        response = Utils.makeRequest(url=orgStatusEndpoint,data='',
                                     auth=IrisHelper.constructAuthenticate(),
                                     headers=IrisHelper.constructHeaders(), method='GET')
        return {'RESPONSE' : IrisHelper.constructResponse(response)}

    @staticmethod
    def getOnboardingStatus(orgId):
        orgOnboardingStatusEndpoint = IrisHelper.constructUrl('orgonboadringstatus').replace('{orgId}',orgId)
        response = Utils.makeRequest(url= orgOnboardingStatusEndpoint, data='',
                                     auth=IrisHelper.constructAuthenticate(),
                                     headers=IrisHelper.constructHeaders(), method='GET')
        return {'RESPONSE': IrisHelper.constructResponse(response)}


    @staticmethod
    def checktheStatus(response):
        value = orgStatus().getOrgStatus()
        if value[0][0] == 2:
            Assertion.constructAssertion(response == True,"The org is already in V2")
        else:
            Assertion.constructAssertion(response == False, "The org is in V1")



    @staticmethod
    def assertResponse(response, expectedStatusCode, expectedErrorCode=102, expectedErrorMessage=[]):
        if response['constructed'].lower() == 'pass':
            if expectedStatusCode >= 200 and expectedStatusCode <= 300:
                Assertion.constructAssertion(response['statusCode'] == int(expectedStatusCode),
                                             'Matching statusCode actual :{},expected :{}'.format(
                                                 response['statusCode'], expectedStatusCode))
                if len(response['json']['warnings']) > 0:
                    Logger.log('There was a Warning while Creating Campaign :', response['json']['warning'])
            else:
                Assertion.constructAssertion(response['statusCode'] == int(expectedStatusCode),
                                             'Matching statusCode actual :{},expected :{}'.format(
                                                 response['statusCode'], expectedStatusCode))
                for errorReturned in response['json']['errors']:
                    Logger.log('Status Code :{} and error :{}', response['statusCode'], errorReturned)
                    Assertion.constructAssertion(errorReturned['code'] == expectedErrorCode,
                                                 'Matching Error Code ,actual:{} and expected:{}'.format(
                                                     errorReturned['code'], expectedErrorCode))
                    Assertion.constructAssertion(errorReturned['status'] == False, 'Checking for Error Status as False')
                    Assertion.constructAssertion(errorReturned['message'] in expectedErrorMessage,
                                                 'Matching Error Message ,actual:{} in expected:{}'.format(
                                                     errorReturned['message'], expectedErrorMessage))
        else:
            Assertion.constructAssertion(False, 'Constructed Body has Failed due to Exception so no Validation')


