
from src.modules.irisv2.helper.irisHelper import IrisHelper
from src.utilities.logger import Logger
from src.utilities.assertion import Assertion
from src.utilities.utils import Utils
from src.Constant.constant import constant
from src.dbCalls.campaignInfo import campaign_calls
from src.dbCalls.messageInfo import pocMetaInfo
import copy

class CampaignSetting():


    @staticmethod
    def settings(self, settingInfo={},popField=None):
        Logger.log('Setting Info :', settingInfo)
        campaignSettingsEndpoint = IrisHelper.constructUrl('campaignSettings')
        payload = CampaignSetting.constructPayloadSetting(settingInfo,popField)
        response = Utils.makeRequest(url=campaignSettingsEndpoint, data=payload, auth=IrisHelper.constructAuthenticate(),
                                     headers=IrisHelper.constructHeaders(), method='POST')

        return {'RESPONSE' : IrisHelper.constructResponse(response),
                'PAYLOAD' : payload}

    @staticmethod
    def constructPayloadSetting(settingInfo,popField=None):

        payload = copy.deepcopy(constant.payload['campaignsetting'])
        payload["messageSettings"].update({'enableLinkTracking': settingInfo['enableLinkTracking']})
        metaInfo = pocMetaInfo().pocMetaData
        listOfIds = list()
        for eachPoc in ['orgPocs','capPocs']:
            listOfIds = listOfIds + metaInfo[eachPoc].keys()
        count = settingInfo['summary']['count']
        for numberOfUsersRequired in range(count):
            payload['reportsSettings']['summaryReportReceivers'].append({
                'userId':listOfIds[numberOfUsersRequired],
                'subscribedChannels':settingInfo['summary']['channels']
            })

        count = settingInfo['credit']['count']
        for numberOfUsersRequired in range(count):
            payload["reportsSettings"]["creditReportReceivers"].append({'userId':listOfIds[numberOfUsersRequired],
                'subscribedChannels':settingInfo['credit']['channels']
            })
        count = settingInfo['failure']['count']
        for numberOfUsersRequired in range(count):
            payload["alertsSettings"]["failureReceivers"].append({'userId': listOfIds[numberOfUsersRequired],
                                                                       'subscribedChannels': settingInfo['failure'][
                                                                           'channels']
                                                                       })
        count = settingInfo['lowDelivery']['count']
        for numberOfUsersRequired in range(count):
            payload["alertsSettings"]["lowDeliveryReceivers"].append({'userId': listOfIds[numberOfUsersRequired],
                                                                  'subscribedChannels': settingInfo['failure'][
                                                                      'channels']
                                                                  })
        if popField!=None:
            payload.pop(popField)
        return payload


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

    @staticmethod
    def updateSettings(self,updateInfo={}):
        campaignSettingsEndpoint = IrisHelper.constructUrl('campaignSettings')
        payload = CampaignSetting.constructUploadPayload(updateInfo)
        response = Utils.makeRequest(url=campaignSettingsEndpoint,
                                     data=payload,
                                     auth=IrisHelper.constructAuthenticate(),
                                     headers=IrisHelper.constructHeadersPatch(), method='PATCH')
        return {'RESPONSE' : IrisHelper.constructResponse(response),
                'PAYLOAD' : payload}

    @staticmethod
    def constructUploadPayload(updateInfo):

        payload = copy.deepcopy(constant.payload['campaignsetting'])
        metaInfo = pocMetaInfo().pocMetaData
        listOfIds = list()
        for eachPoc in ['orgPocs', 'capPocs']:
            listOfIds = listOfIds + metaInfo[eachPoc].keys()

        if 'enableLinkTracking'in updateInfo:
                 payload ["messageSettings"].update({'enableLinkTracking': updateInfo['enableLinkTracking']})
        if 'summary' in updateInfo:
                 count = updateInfo['summary']['count']
                 # listOfIds = campaign_calls().getUserId(count)
                 for numberOfUsersRequired in range(count):
                        payload['reportsSettings']['summaryReportReceivers'].append({
                            'userId': listOfIds[numberOfUsersRequired],
                            'subscribedChannels': updateInfo['summary']['channels']
                        })
        if 'credit' in updateInfo:

                count = updateInfo['credit']['count']
                # listOfIds = campaign_calls().getUserId(count)
                for numberOfUsersRequired in range(count):
                        payload["reportsSettings"]["creditReportReceivers"].append({'userId': listOfIds[numberOfUsersRequired],
                                                                                    'subscribedChannels': updateInfo['credit'][
                                                                                        'channels']})
        if 'failure' in updateInfo:
                count = updateInfo['failure']['count']
                # listOfIds = campaign_calls().getUserId(count)

                for numberOfUsersRequired in range(count):
                    payload["alertsSettings"]["failureReceivers"].append({'userId': listOfIds[numberOfUsersRequired],
                                                                          'subscribedChannels': updateInfo['failure'][
                                                                              'channels']
                                                                          })
        if 'lowDelivery' in updateInfo:

                count = updateInfo['lowDelivery']['count']
                # listOfIds = campaign_calls().getUserId(count)
                for numberOfUsersRequired in range(count):
                    payload["alertsSettings"]["lowDeliveryReceivers"].append({'userId': listOfIds[numberOfUsersRequired],
                                                                              'subscribedChannels': updateInfo['failure'][
                                                                                  'channels']
                                                                              })

        return payload


    @staticmethod
    def getSettings():
        campaignSettingsEndpoint = IrisHelper.constructUrl('campaignSettings')

        response = Utils.makeRequest(url=campaignSettingsEndpoint,data='',
                                     auth=IrisHelper.constructAuthenticate(),
                                     headers=IrisHelper.constructHeaders(), method='GET')
        return {'RESPONSE' : IrisHelper.constructResponse(response)}

