from src.modules.arya.reminder import NFSReminder
from src.modules.irisv2.helper.irisHelper import IrisHelper
from src.utilities.assertion import Assertion
from src.utilities.logger import Logger
from src.utilities.utils import Utils


class Reminder():
    @staticmethod
    def getReminderCount(campaignId, messageId, reminderType, queryParam=[]):
        endpoint = IrisHelper.constructUrl('remindercount', queryParam=queryParam).replace('{campaignId}',
                                                                                           campaignId).replace(
            '{messageId}', messageId).replace('{reminderType}', reminderType)
        response = Utils.makeRequest(url=endpoint, data='', auth=IrisHelper.constructAuthenticate(),
                                     headers=IrisHelper.constructHeaders(), method='GET', timeout=120)
        return IrisHelper.constructResponse(response)

    @staticmethod
    def getReminderCountFromNFS(msgId, mode='INTERACTIVE', name='contactedCustomerV2', namev2='transaction',
                                invert=False,intersection=False,series_id=None):
        response = NFSReminder.reminder(msgId, mode, name, namev2, invert,intersection=intersection,series_id=series_id)
        return response

    @staticmethod
    def validateReminderCount(iris_response, nfs_response):
        Logger.log('Response From IRIS :{} and From NFS :{}'.format(iris_response, nfs_response))
        Assertion.constructAssertion(
            iris_response['json']['entity']['totalCount'] == nfs_response['json']['response']['data']['totalCount'],
            'IRIS Call , TotalCount :{} and from NFS :{}'.format(iris_response['json']['entity']['totalCount'],
                                                                 nfs_response['json']['response']['data'][
                                                                     'totalCount']))

    @staticmethod
    def assertResponse(response, expectedStatusCode, expectedErrorCode=999999, expectedErrorMessage=[]):
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
                    Assertion.constructAssertion(int(errorReturned['code']) == expectedErrorCode,
                                                 'Matching Error Code ,actual:{} and expected:{}'.format(
                                                     errorReturned['code'], expectedErrorCode))
                    Assertion.constructAssertion(errorReturned['status'] == False, 'Checking for Error Status as False')
                    Assertion.constructAssertion(errorReturned['message'] in expectedErrorMessage,
                                                 'Matching Error Message ,actual:{} in expected:{}'.format(
                                                     errorReturned['message'], expectedErrorMessage))
        else:
            Assertion.constructAssertion(False, 'Constructed Body has Failed due to Exception so no Validation')
