from src.Constant.constant import constant
from src.modules.irisv2.campaigns.createCampaign import CreateCampaign
from src.modules.irisv2.helper.irisHelper import IrisHelper
from src.modules.irisv2.message.createMessage import CreateMessage
from src.utilities.assertion import Assertion
from src.utilities.logger import Logger
from src.utilities.randValues import randValues
from src.utilities.utils import Utils
from src.dbCalls.campaignShard import list_Calls

class TestPreview():
    @staticmethod
    def create(campaignType, testControlType, channel, numberOfIdentifiers, numberOfCustomTag=0, campaignId=None,
               payload=None,
               messageBody=None,
               couponEnabled=None,
               pointsEnabled=None):
        campaignInfo = CreateCampaign.create(campaignType, testControlType)
        campaignId = campaignInfo['ID'] if campaignId is None else campaignId
        endPoint = IrisHelper.constructUrl('testpreview').replace('{campaignId}', str(campaignId))
        payload = TestPreview.createPayload(campaignType, testControlType, channel, numberOfIdentifiers,
                                            numberOfCustomTag=numberOfCustomTag,
                                            messageBody=messageBody,
                                            couponEnabled=couponEnabled,
                                            pointsEnabled=pointsEnabled) if payload is None else payload

        response = IrisHelper.constructResponse(
            Utils.makeRequest(url=endPoint, data=payload, auth=IrisHelper.constructAuthenticate(),
                              headers=IrisHelper.constructHeaders(), method='POST')
        )
        return response, payload

    @staticmethod
    def createPayload(campaignType, testControlType, channel, numberOfIdentifiers, numberOfCustomTag=0,
                      messageBody=None,
                      couponEnabled=False, pointsEnabled=False):
        testPreviewPayload = dict()
        testPreviewPayload.update({
            'messageContent': TestPreview.createMessageContent(campaignType, testControlType, numberOfCustomTag,
                                                               channel=channel,
                                                               messageBody=messageBody, couponEnabled=couponEnabled,
                                                               pointsEnabled=pointsEnabled),
            'testContentOn': TestPreview.createAudience(channel, numberOfIdentifiers, numberOfCustomTag,pointsEnabled=pointsEnabled)
        })
        return testPreviewPayload

    @staticmethod  # Need a Fix
    def createMessageContent(campaignType, testControlType, numberOfCustomTag, channel=None, messageBody=None,
                             couponEnabled=False,
                             pointsEnabled=False):
        messageBodyType = 'plain'
        if couponEnabled: messageBodyType = 'coupon'
        if pointsEnabled: messageBodyType = 'points'
        messageContent = dict()
        messageContent.update({
            'mesage_content_1': {
                'channel': 'SMS' if channel is None else channel,
                'messageBody': constant.irisMessage[channel.lower()][
                    messageBodyType] if messageBody is None else messageBody,
            }
        })
        if channel == 'EMAIL':
            messageContent['mesage_content_1'].update({
                'emailSubject': 'TestAndPreviewAutomation',
                'emailBody': constant.irisMessage[channel.lower()][
                    messageBodyType] if messageBody is None else messageBody
            })
        if couponEnabled:
            messageContent['mesage_content_1'].update({
                'offers': [{
                    'type': 'COUPON',
                    'couponSeriesId': CreateMessage.getCouponSeriesId(
                        constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'])
                }],
            })
        if pointsEnabled:
            pointsIds = CreateMessage.getStrategyIds()
            messageContent['mesage_content_1'].update({
                'offers': [{
                    'type': 'POINTS',
                    'programId': pointsIds['programeId'],
                    'allocationStrategyId': pointsIds['allocationStrategyId'],
                    'expirationStrategyId': pointsIds['expirationStrategyId']
                }],
            })
        if channel == 'EMAIL': messageContent['mesage_content_1'].pop('messageBody')
        if numberOfCustomTag >0:
            if 'messageBody' in messageContent['mesage_content_1']:
                messageContent['mesage_content_1'].update({'messageBody': TestPreview.getCustomTagsAppendedToBody(
                    messageContent['mesage_content_1']['messageBody'],
                    numberOfCustomTag)})
            if 'emailBody' in messageContent['mesage_content_1']:
                messageContent['mesage_content_1'].update({'emailBody': TestPreview.getCustomTagsAppendedToBody(
                    messageContent['mesage_content_1']['emailBody'], numberOfCustomTag)})

        return messageContent

    @staticmethod
    def getCustomTagsAppendedToBody(body, numberoftags):
        for _ in range(1, numberoftags + 1):
            body = body + " {{custom_tag_" + str(_) + "}}"
        return body

    @staticmethod
    def createAudience(channel, numberOfIdentifier, numberOfCustomTag=0,pointsEnabled=False):
        audience = dict()
        identifiers = list()
        for _ in range(numberOfIdentifier):
            if numberOfCustomTag == 0:
                identifiers.append(
                    {
                        "identifier": TestPreview.getIdentiferValue(channel,pointsEnabled),
                        'identifierType':'MOBILE' if channel == 'SMS' else channel
                    }
                )
            else:
                customTagFormation = list()
                for _ in range(numberOfCustomTag):
                    customTagFormation.append(randValues.randomString(10))
                identifiers.append(
                    {
                        "identifier": TestPreview.getIdentiferValue(channel,pointsEnabled),
                        'identifierType': 'MOBILE' if channel == 'SMS' else channel,
                        "customTag": customTagFormation
                    }
                )
        audience.update({
            'testAudiences': identifiers
        })
        return audience

    @staticmethod
    def getIdentiferValue(channel,pointsEnabled):
        if channel.lower() in ['mobile', 'sms']:
            return randValues.getRandomMobileNumber() if not pointsEnabled else list_Calls().getExistingUsers(1)[0][3]
        else:
            return list_Calls().getExistingUsers(1)[0][4]

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
                    Assertion.constructAssertion(errorReturned['code'] == expectedErrorCode,
                                                 'Matching Error Code ,actual:{} and expected:{}'.format(
                                                     errorReturned['code'], expectedErrorCode))
                    Assertion.constructAssertion(errorReturned['status'] == False, 'Checking for Error Status as False')
                    Assertion.constructAssertion(errorReturned['message'] in expectedErrorMessage,
                                                 'Matching Error Message ,actual:{} in expected:{}'.format(
                                                     errorReturned['message'], expectedErrorMessage))
        else:
            Assertion.constructAssertion(False, 'Constructed Body has Failed due to Exception so no Validation')
