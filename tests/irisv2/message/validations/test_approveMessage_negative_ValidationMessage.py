import time

import pytest

from src.Constant.constant import constant
from src.modules.irisv2.campaigns.createCampaign import CreateCampaign
from src.modules.irisv2.helper.irisHelper import IrisHelper
from src.modules.irisv2.message.authorizeMessage import AuthorizeMessage
from src.modules.irisv2.message.createMessage import CreateMessage
from src.utilities.assertion import Assertion
from src.utilities.logger import Logger


class Test_approveMessage_Negative_ValildationMessage():
    def setup_method(self, method):
        Logger.logMethodName(method.__name__)

    def setup_class(self):
        messageInfo = {
            'scheduleType': {'type': 'IMMEDIATE'},
            'offerType': 'PLAIN',
            'messageStrategy': {'type': 'DEFAULT'},
            'channels': ['SMS', 'EMAIL'],
            'useTinyUrl': False,
            'encryptUrl': False,
            'skipRateLimit': True
        }
        self.campaignInfo = CreateCampaign.create('LIVE', 'ORG')
        self.messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'EMAIL', messageInfo)

    @pytest.mark.parametrize('messageId,response,errorCode,errorMessage', [
        ('messageId', 400, 3023, 'Message with message id messageId does not exists'),
        ('$$$####', 405, 108, 'INVALID REQUEST METHOD : HTTP 405 Method Not Allowed'),
        ('9999999', 400, 3023, 'Message with message id 9999999 does not exists'),
        ('-999999', 400, 3023, 'Message with message id -999999 does not exists')
    ])
    def test_approveMessage_negative_validationMessage_wrongMessageId(self, messageId, response, errorCode,
                                                                      errorMessage):
        responseAuthorize = AuthorizeMessage.approveWithCampaignAndMessageId(self.campaignInfo['ID'], messageId)
        AuthorizeMessage.assertResponse(responseAuthorize, response, expectedErrorCode=errorCode,
                                        expectedErrorMessage=errorMessage
                                        )

    @pytest.mark.parametrize('campaignId,response,errorCode,errorMessage', [
        ('campaignId', 400, 103, 'Invalid value for path param: campaignId'),
        ('$$$####', 405, 108, 'INVALID REQUEST METHOD : HTTP 405 Method Not Allowed'),
        ('-999999', 400, 102, 'Invalid request : must be greater than or equal to 1')
    ])
    def test_approveMessage_negative_validationMessage_wrongcampaignId(self, campaignId, response, errorCode,
                                                                       errorMessage):
        responseAuthorize = AuthorizeMessage.approveWithCampaignAndMessageId(campaignId,
                                                                             self.messageDetails['RESPONSE']['json'][
                                                                                 'entity']['id'])
        AuthorizeMessage.assertResponse(responseAuthorize, response, expectedErrorCode=errorCode,
                                        expectedErrorMessage=errorMessage)



    @pytest.mark.parametrize('campaignId,response,errorCode,errorMessage', [
        ('9999999', 400, [3034, 3024,3023], ['Invalid campaign id: 9,999,999','Message does not belong to the campaign','Message with message id {} does not exists'])
    ])
    def test_approveMessage_negative_validationMessage_wrongcampaignIdMessage(self, campaignId, response, errorCode,
                                                                          errorMessage):


        responseAuthorize = AuthorizeMessage.approveWithCampaignAndMessageId(campaignId,
                                                                             self.messageDetails['RESPONSE']['json'][
                                                                                 'entity']['id'])
        Assertion.constructAssertion(responseAuthorize['statusCode'] == response, 'Actual code :{} and Expected:{}'.format(responseAuthorize['statusCode'],response))


        for errors in responseAuthorize['json']['errors']:
            Assertion.constructAssertion(errors['code'] in errorCode,
                                         'Actual Error Code :{} and Expected :{}'.format(
                                             errors['code'], errorCode))

            Assertion.constructAssertion(errors['message'] in errorMessage[2].format(self.messageDetails['RESPONSE']['json']['entity']['id']),
                                         'Actual Error message :{} and Expected :{}'.format(
                                             errors['message'], errorMessage[2].format(self.messageDetails['RESPONSE']['json']['entity']['id'])))



    def test_approveMessage_negative_validationMessage_different_campaignId(self):

        campaignInfo = CreateCampaign.create('LIVE', 'CUSTOM')
        diffId = campaignInfo['ID']
        responseAuthorize = AuthorizeMessage.approveWithCampaignAndMessageId(diffId,
                                                                             self.messageDetails['RESPONSE']['json'][
                                                                                 'entity']['id'])

        messageId= self.messageDetails['RESPONSE']['json']['entity']['id']

        AuthorizeMessage.assertResponse(responseAuthorize, 400, expectedErrorCode=3023,
                                        expectedErrorMessage=['Message with message id {} does not exists'.format(messageId)])

    def test_approveMessage_negative_validationMessage_wrongAuth(self):
        previousUser = IrisHelper.updateUserName('XXXX')
        try:
            responseAuthorize = AuthorizeMessage.approveWithCampaignAndMessageId(self.campaignInfo['ID'],
                                                                                 self.messageDetails['RESPONSE'][
                                                                                     'json'][
                                                                                     'entity']['id'])
            AuthorizeMessage.assertResponse(responseAuthorize, 401, expectedErrorCode=999999,
                                            expectedErrorMessage='Unauthorized')
        except Exception, exp:
            Assertion.constructAssertion(False, 'Exception Occured :{}'.format(exp))
        finally:
            IrisHelper.updateUserName(previousUser)

    def test_approveMessage_negative_validationMessage_wrongOrgId(self):
        previousOrg = IrisHelper.updateOrgId(-1)
        Logger.log(constant.config['orgId'])
        try:
            responseAuthorize = AuthorizeMessage.approveWithCampaignAndMessageId(self.campaignInfo['ID'],
                                                                                 self.messageDetails['RESPONSE'][
                                                                                     'json'][
                                                                                     'entity']['id'])
            AuthorizeMessage.assertResponse(responseAuthorize, 401, expectedErrorCode=999999,
                                            expectedErrorMessage='Invalid org id')
        except Exception, exp:
            Assertion.constructAssertion(False, 'Exception Occured :{}'.format(exp))
        finally:
            IrisHelper.updateOrgId(previousOrg)

    def test_approveMessage_negative_validationMessage_particularDate_ApproveAfterSchedulle(self):
        messageInfo = {
            'scheduleType': {
                'type': 'PARTICULARDATE'

            },
            'offerType': 'PLAIN',
            'messageStrategy': {
                'type': 'DEFAULT'
            },
            'channels': ['SMS', 'EMAIL'],
            'useTinyUrl': False,
            'encryptUrl': False,
            'skipRateLimit': True
        }
        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE', messageInfo)
        time.sleep(120)
        responseAuthorize = AuthorizeMessage.approveWithCampaignAndMessageId(self.campaignInfo['ID'],
                                                                             messageDetails['RESPONSE']['json'][
                                                                                 'entity']['id'])
        AuthorizeMessage.assertResponse(responseAuthorize, 400,expectedErrorCode=3023,
        expectedErrorMessage = "Message with message id {} does not exists".format(messageDetails['RESPONSE']['json'][
                                                                                 'entity']['id']) )

    def test_approveMessage_negative_validationMessage_immediate_ApprovingAlreadyApprovedMessage(self):
        messageInfo = {
            'scheduleType': {
                'type': 'IMMEDIATE'
            },
            'offerType': 'PLAIN',
            'messageStrategy': {
                'type': 'DEFAULT'
            },
            'channels': ['SMS', 'EMAIL'],
            'useTinyUrl': False,
            'encryptUrl': False,
            'skipRateLimit': True
        }
        campaignType = 'LIVE'
        testControlType = 'ORG'
        listType = 'UPLOAD'
        channel = 'MOBILE'
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo)
        AuthorizeMessage.assertResponse(approveRespone, 200)
        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        responseAuthorize = AuthorizeMessage.approveWithCampaignAndMessageId(campaignId,
                                                                             approveRespone['json'][
                                                                                 'entity']['messageId'])
        AuthorizeMessage.assertResponse(responseAuthorize, 400, expectedErrorCode=3022,
                                        expectedErrorMessage='Message is already approved')


    def test_irisv2_approve_message_after_7_days(self):
        responseAuthorize = AuthorizeMessage.approveWithCampaignAndMessageId('760905','5d878d854f0c41f1325c22d1')
        AuthorizeMessage.assertResponse(responseAuthorize, 400, expectedErrorCode=3070,
                                        expectedErrorMessage='Message cannot be approved beyond allowed period of 7 Days : Message cannot be approved 5d878d854f0c41f1325c22d1')


