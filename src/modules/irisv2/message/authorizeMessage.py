from src.Constant.constant import constant
from src.dbCalls.messageInfo import message_calls
from src.modules.irisv2.helper.irisHelper import IrisHelper
from src.modules.irisv2.message.createMessage import CreateMessage
from src.utilities.assertion import Assertion
from src.utilities.logger import Logger
from src.utilities.utils import Utils


class AuthorizeMessage():
    def __init__(self):
        pass

    @staticmethod
    def approve(campaignType, testControlType, listType, channel, messageInfo={}, messageCreateResponse=None,
                listInfo=None, campaignId=None,
                newUser=True, messageType='OUTBOUND', payload=None, targetAudience=None, scheduleType=None,
                messageStrategy=None, messageContent=None, updateNode=False, lockNode=False,
                storeType='REGISTERED_STORE', derivedListInfo=None,couponSeriesId=None):
        messageCreateResponse = CreateMessage.create(campaignType, testControlType, listType, channel,
                                                     messageInfo=messageInfo,
                                                     listInfo=listInfo, campaignId=campaignId,
                                                     newUser=newUser, messageType=messageType, payload=payload,
                                                     targetAudience=targetAudience, scheduleType=scheduleType,
                                                     messageStrategy=messageStrategy, messageContent=messageContent,
                                                     updateNode=updateNode, lockNode=lockNode,
                                                     storeType=storeType,
                                                     derivedListInfo=derivedListInfo, couponSeriesId=couponSeriesId) if messageCreateResponse is None else messageCreateResponse

        if messageCreateResponse['RESPONSE']['statusCode'] == 200:
            campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'] if campaignId is None else campaignId
            messageId = constant.config['node'][campaignType][testControlType]['LIST'][listType][channel]['MESSAGE'][
                messageInfo['scheduleType']['type']][messageInfo['offerType']]['RESPONSE']['json']['entity'][
                'id'] if messageCreateResponse is None else messageCreateResponse['RESPONSE']['json']['entity']['id']

            Logger.log(
                'Message Execution for CampaignType :{} , testsControlType :{} , listType :{} , channel :{} , SchedulleType :{} , offerType :{} with CampaignId :{} and messageId :{}'.format(
                    campaignType,
                    testControlType,
                    listType,
                    channel,
                    messageInfo['scheduleType'],
                    messageInfo['offerType'],
                    campaignId,
                    messageId)
            )
            variantJobName = 'PERSONALIZED_VARIANT_CREATION' if messageInfo['messageStrategy']['type'] == 'PERSONALISATION' else 'VARIANT_CREATION'
            if not message_calls().waitForJobDetailsStatusToClose(messageId, variantJobName):
                raise Exception('VariantNotCreatedException')

            endPoint = IrisHelper.constructUrl('approvemessage').replace('{campaignId}', str(campaignId)).replace(
                '{msgId}',
                messageId)
            response = IrisHelper.constructResponse(
                Utils.makeRequest(url=endPoint, data=payload, auth=IrisHelper.constructAuthenticate(),
                                  headers=IrisHelper.constructHeaders(), method='POST')
            )
            if response['statusCode']== 200 and messageCreateResponse is None :
                constant.config['node'][campaignType][testControlType]['LIST'][listType][channel]['MESSAGE'][
                    messageInfo['scheduleType']['type']][messageInfo['offerType']]['RESPONSE']['EXECUTED'] = True
            return response
        else:
            raise Exception('Failed To Create Message Exception')

    @staticmethod
    def approveWithCampaignAndMessageId(campaignId, messageId):
        endPoint = IrisHelper.constructUrl('approvemessage').replace('{campaignId}', str(campaignId)).replace(
            '{msgId}', messageId)
        return IrisHelper.constructResponse(
            Utils.makeRequest(url=endPoint, data=None, auth=IrisHelper.constructAuthenticate(),
                              headers=IrisHelper.constructHeaders(), method='POST')
        )

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
