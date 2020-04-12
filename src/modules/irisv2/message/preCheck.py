from src.dbCalls.messageInfo import message_calls
from src.modules.irisv2.helper.irisHelper import IrisHelper
from src.utilities.assertion import Assertion
from src.utilities.logger import Logger
from src.utilities.utils import Utils
from src.Constant.constant import constant
import json

class PreCheck():
    @staticmethod
    def executePrecheck(campaignId, messageId, checkVariant=True):
        if checkVariant: PreCheck.checkVariantIsClosed(messageId)
        endpoint = IrisHelper.constructUrl('precheck').replace('{campaignId}',
                                                               str(campaignId)).replace('{messageId}', messageId)
        response = Utils.makeRequest(url=endpoint, data='', auth=IrisHelper.constructAuthenticate(),
                                     headers=IrisHelper.constructHeaders(), method='GET')
        return IrisHelper.constructResponse(response)

    @staticmethod
    def checkVariantIsClosed(messageId):
        message_calls().getVariantIdByMessageId(messageId)

    @staticmethod
    def assertPreCheckResponse(response, expectedStatusCode, expectedErrorCode=999999, expectedErrorMessage=''):
        if response['constructed'].lower() == 'pass':
            if expectedStatusCode >= 200 and expectedStatusCode <= 300:
                Assertion.constructAssertion(response['statusCode'] == int(expectedStatusCode),
                                             'Matching statusCode actual :{},expected :{}'.format(
                                                 response['statusCode'], expectedStatusCode))
                if len(response['json']['warnings']) > 0:
                    Logger.log('There was a Warning while Creating Campaign :', response['json']['warning'])
            else:
                Assertion.constructAssertion(len(response['json']['errors']) != 0,
                                             'Expected Status Code :{} and Errors in Response is Empty'.format(
                                                 expectedStatusCode))
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
    def assertPrecheckStatus(preCheckResponse, precheckErrors):
        Assertion.constructAssertion(preCheckResponse['json']['entity']['precheckStatus']['precheckStatus'] == 'CLOSED',
                                     'PrecheckStatus is :{} and expected is :CLOSED'.format(
                                         preCheckResponse['json']['entity']['precheckStatus']['precheckStatus']))
        for eachPrecheckError in preCheckResponse['json']['entity']['precheckStatus']['precheckErrors']:
            Assertion.constructAssertion(eachPrecheckError in precheckErrors,
                                         'Actual Error :{} found in Expected list :{}'.format(eachPrecheckError,
                                                                                              precheckErrors))

    @staticmethod
    def updateCronWithoutMessageId(messageId,cronStatus):
        if constant.config['cluster'] == 'nightly':
            cronDetails = message_calls().getCronIdWithVariantId(messageId, cronStatus)
            params = json.loads(['params'])
            params.pop('messageId')
            message_calls().updateParamsInCron(messageId)

        else:
            raise Exception('UpdateCronNotPermittedInCluster')