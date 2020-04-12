from src.dbCalls.campaignInfo import campaign_calls
from src.dbCalls.messageInfo import message_calls
from src.modules.irisv2.helper.irisHelper import IrisHelper
from src.modules.irisv2.list.getListDBAssertion import GetListDBAssertion
from src.modules.irisv2.message.createMessageDbAssertion import CreateMessageDBAssertion
from src.modules.irisv2.message.variantDbAssertion import VariantDBAssertion
from src.utilities.assertion import Assertion
from src.utilities.logger import Logger
from src.utilities.utils import Utils


class GetMessage():
    @staticmethod
    def getMessageById(campaignId, messageId, queryParam=[]):
        endpoint = IrisHelper.constructUrl('getmessage', queryParam=queryParam).replace('{campaignId}',
                                                                                        str(campaignId)).replace(
            '{messageId}',
            messageId)
        response = Utils.makeRequest(url=endpoint, data='', auth=IrisHelper.constructAuthenticate(),
                                     headers=IrisHelper.constructHeaders(), method='GET')
        return IrisHelper.constructResponse(response)

    @staticmethod
    def getMessageAll(campaignId, queryParam=[]):
        endpoint = IrisHelper.constructUrl('getmessage', queryParam=queryParam).replace('{campaignId}',
                                                                                        str(campaignId)).replace(
            '{messageId}',
            '')
        response = Utils.makeRequest(url=endpoint, data='', auth=IrisHelper.constructAuthenticate(),
                                     headers=IrisHelper.constructHeaders(), method='GET')
        return IrisHelper.constructResponse(response)

    @staticmethod
    def getMessageVariantById(campaignId, variantId):
        endpoint = IrisHelper.constructUrl('getmessagevariant').replace('{campaignId}', str(campaignId)).replace(
            '{variantId}',
            variantId)
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
    def getCampaignID(campaignType, testControlType):
        campaigns = campaign_calls().getCampaignId(campaignType, testControlType)
        campaignId = None
        for each in campaigns:
            Logger.log('Checking Message for Campaign :{}'.format(each['campaignId']))
            campaignId = each['campaignId']
            if message_calls().checkCampaignHaveMessage(campaignId): break
        Logger.log('For GetCall CampaignId Finally Getting Used is :{}'.format(campaignId))
        return campaignId

    @staticmethod
    def getCampaignIDHavingNoMessage(campaignType, testControlType):
        campaigns = campaign_calls().getCampaignId(campaignType, testControlType)
        campaignId = None
        for each in campaigns:
            campaignId = each['campaignId']
            if not message_calls().checkCampaignHaveMessage(campaignId): break
        return campaignId

    @staticmethod
    def validateGetAll(response, campaignId):
        numberOfMessageInCampaign = message_calls().getNumberOfMessagesInCampaign(campaignId)
        Assertion.constructAssertion(numberOfMessageInCampaign == len(response),
                                     'NumberOf Messages In Db :{} and in response :{}'.format(numberOfMessageInCampaign,
                                                                                              len(response)))
        for eachMessage in response:
            messageResponse = eachMessage
            CreateMessageDBAssertion(campaignId, messageResponse['messageId'], messageResponse, getAllTest=True).check()

    @staticmethod
    def validateGetAllAudienceInclude(response, campaignId):
        for eachMessage in response:
            GetListDBAssertion(
                eachMessage['targetAudience']['includeAudienceGroupInfo'][0]['id'],
                {'json':
                    {
                        'entity': eachMessage['targetAudience']['includeAudienceGroupInfo'][0]
                    }
                },
                campaignHashLookUp=False, createAudienceJob=False, reachabilityCheck=False,
                campaignGroupRecipients=False
            ).check()

    @staticmethod
    def validateGetAllVaraintsInclude(response, campaignId):
        for eachMessage in response:
            if 'messageVariantList' in eachMessage:
                VariantDBAssertion(campaignId, eachMessage['messageId'],
                                   eachMessage['messageVariantList']).check()
            else:
                Assertion.constructAssertion(False, 'messageVariantList Not Found for MessageId :{}'.format(
                    eachMessage['messageId']), verify=True)

    @staticmethod
    def validateGetAllIncludeVariantAndAudienceAsFalse(response):
        for eachEntity in response:
            Assertion.constructAssertion('messageVariantList' not in eachEntity,
                                         ' Found in Message Entity :{}'.format(eachEntity))
            Assertion.constructAssertion('includeAudienceGroupInfo' not in eachEntity['targetAudience'],
                                         'includeAudienceGroupInfo Found in Message Entity :{}'.format(eachEntity))
