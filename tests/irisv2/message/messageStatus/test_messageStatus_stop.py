import pytest,copy
import time
from src.utilities.logger import Logger
from src.dbCalls.messageInfo import message_calls
from src.modules.irisv2.list.createAudience import CreateAudience
from src.Constant.constant import constant
from src.modules.irisv2.message.createMessage import CreateMessage
from src.modules.irisv2.message.createMessageDbAssertion import CreateMessageDBAssertion
from src.modules.irisv2.message.authorizeMessage import AuthorizeMessage
from src.modules.irisv2.message.authorizeMessageDbAssertion import AuthorizeMessageDBAssertion
from src.modules.irisv2.campaigns.createCampaign import CreateCampaign
from src.utilities.assertion import Assertion
from src.modules.irisv2.helper.irisHelper import IrisHelper
from src.utilities.utils import Utils

class Test_MessageStatus_Stop():

    def setup_method(self, method):
        Logger.logMethodName(method.__name__)

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'LOYALTY', 'MOBILE',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def irisv2_message_Sanity_create_stop_filter_mobile_Recurring_plain(self, campaignType, testControlType,
                                                                      listType,
                                                                      channel, messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'], 'VARIANT_CREATION')
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                  messageCreateResponse=messageDetails)
        AuthorizeMessage.assertResponse(approveRespone, 200)
        stopResponse = CreateMessage.stop(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                            approveRespone['json']['entity']['messageId'])
        CreateMessage.assertResponse(stopResponse, 200)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],
                                 reject={'status': 'CLOSED'},approved='STOPPED').check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'CUSTOM', 'LOYALTY', 'MOBILE',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'SKIP', 'LOYALTY', 'MOBILE',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'ORG', 'LOYALTY', 'MOBILE',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'CUSTOM', 'LOYALTY', 'MOBILE',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'SKIP', 'LOYALTY', 'MOBILE',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def irisv2_message_create_stop_filter_mobile_Recurring_plain(self, campaignType, testControlType,
                                                                             listType,
                                                                             channel, messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'], 'VARIANT_CREATION')
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                  messageCreateResponse=messageDetails)
        AuthorizeMessage.assertResponse(approveRespone, 200)
        stopResponse = CreateMessage.stop(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                            approveRespone['json']['entity']['messageId'])
        CreateMessage.assertResponse(stopResponse, 200)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],
                                 reject={'status': 'CLOSED'},approved='STOPPED').check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'LOYALTY', 'MOBILE',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': True, 'encryptUrl': False, 'skipRateLimit': True}),
    ])
    def irisv2_message_create_stop_filter_mobile_Recurring_plain_UsingTinyURL(self, campaignType,
                                                                                   testControlType,
                                                                                   listType, channel, messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'], 'VARIANT_CREATION')
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                  messageCreateResponse=messageDetails)
        AuthorizeMessage.assertResponse(approveRespone, 200)
        stopResponse = CreateMessage.stop(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                            approveRespone['json']['entity']['messageId'])
        CreateMessage.assertResponse(stopResponse, 200)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],
                                 reject={'status': 'CLOSED'},approved='STOPPED').check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'LOYALTY', 'MOBILE',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': True, 'skipRateLimit': True}),
    ])
    def irisv2_message_create_stop_filter_mobile_Recurring_plain_UsingEncryptURL(self, campaignType,
                                                                                      testControlType,
                                                                                      listType, channel, messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'], 'VARIANT_CREATION')
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                  messageCreateResponse=messageDetails)
        AuthorizeMessage.assertResponse(approveRespone, 200)
        stopResponse = CreateMessage.stop(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                            approveRespone['json']['entity']['messageId'])
        CreateMessage.assertResponse(stopResponse, 200)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],
                                 reject={'status': 'CLOSED'},approved='STOPPED').check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'LOYALTY', 'MOBILE',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': False}),
    ])
    def irisv2_message_create_stop_filter_mobile_Recurring_plain_UsingRateLimit(self, campaignType,
                                                                                     testControlType,
                                                                                     listType, channel, messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'], 'VARIANT_CREATION')
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                  messageCreateResponse=messageDetails)
        AuthorizeMessage.assertResponse(approveRespone, 200)
        stopResponse = CreateMessage.stop(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                            approveRespone['json']['entity']['messageId'])
        CreateMessage.assertResponse(stopResponse, 200)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],
                                 reject={'status': 'CLOSED'},approved='STOPPED').check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'LOYALTY', 'MOBILE',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'CUSTOM', 'LOYALTY', 'MOBILE',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'SKIP', 'LOYALTY', 'MOBILE',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'ORG', 'LOYALTY', 'MOBILE',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'CUSTOM', 'LOYALTY', 'MOBILE',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'SKIP', 'LOYALTY', 'MOBILE',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def irisv2_message_create_stop_filter_mobile_Recurring_coupon(self, campaignType, testControlType, listType,
                                                                       channel, messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'], 'VARIANT_CREATION')
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                  messageCreateResponse=messageDetails)
        AuthorizeMessage.assertResponse(approveRespone, 200)
        stopResponse = CreateMessage.stop(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                            approveRespone['json']['entity']['messageId'])
        CreateMessage.assertResponse(stopResponse, 200)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],
                                 reject={'status': 'CLOSED'},approved='STOPPED').check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'LOYALTY', 'MOBILE',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'CUSTOM', 'LOYALTY', 'MOBILE',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'SKIP', 'LOYALTY', 'MOBILE',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'ORG', 'LOYALTY', 'MOBILE',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'CUSTOM', 'LOYALTY', 'MOBILE',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'SKIP', 'LOYALTY', 'MOBILE',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def irisv2_message_create_stop_filter_mobile_Recurring_points(self, campaignType, testControlType, listType,
                                                                       channel, messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'], 'VARIANT_CREATION')
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                  messageCreateResponse=messageDetails)
        AuthorizeMessage.assertResponse(approveRespone, 200)
        stopResponse = CreateMessage.stop(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                            approveRespone['json']['entity']['messageId'])
        CreateMessage.assertResponse(stopResponse, 200)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],
                                 reject={'status': 'CLOSED'},approved='STOPPED').check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'LOYALTY', 'EMAIL',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'CUSTOM', 'LOYALTY', 'EMAIL',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'SKIP', 'LOYALTY', 'EMAIL',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'ORG', 'LOYALTY', 'EMAIL',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'CUSTOM', 'LOYALTY', 'EMAIL',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'SKIP', 'LOYALTY', 'EMAIL',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def irisv2_message_create_stop_filter_email_Recurring_plain(self, campaignType, testControlType,
                                                                     listType,
                                                                     channel, messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'], 'VARIANT_CREATION')
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                  messageCreateResponse=messageDetails)
        AuthorizeMessage.assertResponse(approveRespone, 200)
        stopResponse = CreateMessage.stop(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                            approveRespone['json']['entity']['messageId'])
        CreateMessage.assertResponse(stopResponse, 200)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],
                                 reject={'status': 'CLOSED'},approved='STOPPED').check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'LOYALTY', 'EMAIL',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': True, 'encryptUrl': False, 'skipRateLimit': True}),
    ])
    def irisv2_message_create_stop_filter_email_Recurring_plain_UsingTinyURL(self, campaignType,
                                                                                  testControlType,
                                                                                  listType, channel, messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'], 'VARIANT_CREATION')
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                  messageCreateResponse=messageDetails)
        AuthorizeMessage.assertResponse(approveRespone, 200)
        stopResponse = CreateMessage.stop(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                            approveRespone['json']['entity']['messageId'])
        CreateMessage.assertResponse(stopResponse, 200)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],
                                 reject={'status': 'CLOSED'},approved='STOPPED').check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'LOYALTY', 'EMAIL',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': True, 'skipRateLimit': True}),
    ])
    def irisv2_message_create_stop_filter_email_Recurring_plain_UsingEncryptURL(self, campaignType,
                                                                                     testControlType,
                                                                                     listType, channel, messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'], 'VARIANT_CREATION')
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                  messageCreateResponse=messageDetails)
        AuthorizeMessage.assertResponse(approveRespone, 200)
        stopResponse = CreateMessage.stop(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                            approveRespone['json']['entity']['messageId'])
        CreateMessage.assertResponse(stopResponse, 200)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],
                                 reject={'status': 'CLOSED'},approved='STOPPED').check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'LOYALTY', 'EMAIL',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': False}),
    ])
    def irisv2_message_create_stop_filter_email_Recurring_plain_UsingRateLimit(self, campaignType,
                                                                                    testControlType,
                                                                                    listType, channel, messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'], 'VARIANT_CREATION')
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                  messageCreateResponse=messageDetails)
        AuthorizeMessage.assertResponse(approveRespone, 200)
        stopResponse = CreateMessage.stop(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                            approveRespone['json']['entity']['messageId'])
        CreateMessage.assertResponse(stopResponse, 200)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],
                                 reject={'status': 'CLOSED'},approved='STOPPED').check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'LOYALTY', 'EMAIL',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'CUSTOM', 'LOYALTY', 'EMAIL',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'SKIP', 'LOYALTY', 'EMAIL',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'ORG', 'LOYALTY', 'EMAIL',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'CUSTOM', 'LOYALTY', 'EMAIL',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'SKIP', 'LOYALTY', 'EMAIL',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def irisv2_message_create_stop_filter_email_Recurring_coupon(self, campaignType, testControlType, listType,
                                                                      channel, messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'], 'VARIANT_CREATION')
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                  messageCreateResponse=messageDetails)
        AuthorizeMessage.assertResponse(approveRespone, 200)
        stopResponse = CreateMessage.stop(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                            approveRespone['json']['entity']['messageId'])
        CreateMessage.assertResponse(stopResponse, 200)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],
                                 reject={'status': 'CLOSED'},approved='STOPPED').check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'LOYALTY', 'EMAIL',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'CUSTOM', 'LOYALTY', 'EMAIL',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'SKIP', 'LOYALTY', 'EMAIL',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'ORG', 'LOYALTY', 'EMAIL',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'CUSTOM', 'LOYALTY', 'EMAIL',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'SKIP', 'LOYALTY', 'EMAIL',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def irisv2_message_create_stop_filter_email_Recurring_points(self, campaignType, testControlType, listType,
                                                                      channel, messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'], 'VARIANT_CREATION')
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                  messageCreateResponse=messageDetails)
        AuthorizeMessage.assertResponse(approveRespone, 200)
        stopResponse = CreateMessage.stop(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                            approveRespone['json']['entity']['messageId'])
        CreateMessage.assertResponse(stopResponse, 200)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],
                                 reject={'status': 'CLOSED'},approved='STOPPED').check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
    ])
    def irisv2_message_create_stop_messagewith2hours_upload_mobile_particularDate_plain(self, campaignType,
                                                                                                   testControlType,
                                                                                                   listType,
                                                                                                   channel,
                                                                                                   messageInfo):
        self.listInfo = CreateAudience.uploadList('LIVE', 'ORG')
        payload = copy.deepcopy(constant.payload['createMessagev2'])
        payload['targetAudience'].update({'include': [self.listInfo['ID']]})
        payload['schedule']['scheduleType'] = 'PARTICULAR_DATE'
        payload['schedule']['scheduledDate'] = int(time.time() * 1000) + 2 * 60 * 60 * 1000 + 2 * 60 * 1000
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              payload=payload,updateNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'], 'VARIANT_CREATION')
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                  messageCreateResponse=messageDetails)
        AuthorizeMessage.assertResponse(approveRespone, 200)
        stopResponse = CreateMessage.stop(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                            approveRespone['json']['entity']['messageId'])
        CreateMessage.assertResponse(stopResponse, 200)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],
                                 reject={'status': 'CLOSED'},approved='STOPPED').check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'EMAIL',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
    ])
    def irisv2_message_create_stop_messagewith2hours_upload_email_particularDate_plain(self, campaignType,
                                                                                                 testControlType,
                                                                                                 listType,
                                                                                                 channel,
                                                                                                 messageInfo):
        self.listInfo = CreateAudience.uploadList('LIVE', 'ORG')
        payload = copy.deepcopy(constant.payload['createMessagev2'])
        payload['targetAudience'].update({'include': [self.listInfo['ID']]})
        payload['schedule']['scheduleType'] = 'PARTICULAR_DATE'
        payload['schedule']['scheduledDate'] = int(time.time() * 1000) + 2 * 60 * 60 * 1000 + 2 * 60 * 1000
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              payload=payload, updateNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'], 'VARIANT_CREATION')
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                  messageCreateResponse=messageDetails)
        AuthorizeMessage.assertResponse(approveRespone, 200)
        stopResponse = CreateMessage.stop(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                          approveRespone['json']['entity']['messageId'])
        CreateMessage.assertResponse(stopResponse, 200)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],
                                 reject={'status': 'CLOSED'},approved='STOPPED').check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
    ])
    def irisv2_message_create_stop_messagewith2minute_upload_mobile_particularDate_plain(self, campaignType,
                                                                                                 testControlType,
                                                                                                 listType,
                                                                                                 channel,
                                                                                                 messageInfo):
        self.listInfo = CreateAudience.uploadList('LIVE', 'ORG')
        payload = copy.deepcopy(constant.payload['createMessagev2'])
        payload['targetAudience'].update({'include': [self.listInfo['ID']]})
        payload['schedule']['scheduleType'] = 'PARTICULAR_DATE'
        payload['schedule']['scheduledDate'] = int(time.time() * 1000) + 3 * 60 * 1000
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              payload=payload, updateNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'], 'VARIANT_CREATION')
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                  messageCreateResponse=messageDetails)
        AuthorizeMessage.assertResponse(approveRespone, 200)
        time.sleep(5)
        stopResponse = CreateMessage.stop(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                            approveRespone['json']['entity']['messageId'])
        CreateMessage.assertResponse(stopResponse, 200)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],
                                 reject={'status': 'CLOSED'},approved='STOPPED').check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'EMAIL',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
    ])
    def irisv2_message_create_stop_messagewith2minute_upload_email_particularDate_plain(self, campaignType,
                                                                                                  testControlType,
                                                                                                  listType,
                                                                                                  channel,
                                                                                                  messageInfo):
        self.listInfo = CreateAudience.uploadList('LIVE', 'ORG')
        payload = copy.deepcopy(constant.payload['createMessagev2'])
        payload['targetAudience'].update({'include': [self.listInfo['ID']]})
        payload['schedule']['scheduleType'] = 'PARTICULAR_DATE'
        payload['schedule']['scheduledDate'] = int(time.time() * 1000) + 3 * 60 * 1000
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              payload=payload, updateNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'], 'VARIANT_CREATION')
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                  messageCreateResponse=messageDetails)
        AuthorizeMessage.assertResponse(approveRespone, 200)
        time.sleep(5)
        stopResponse = CreateMessage.stop(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                          approveRespone['json']['entity']['messageId'])
        CreateMessage.assertResponse(stopResponse, 200)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],
                                 reject={'status': 'CLOSED'},approved='STOPPED').check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo,editInfo, statusCode, errorCode, errorDescription', [
        ('LIVE', 'ORG', 'LOYALTY', 'MOBILE',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True},
         {'endDate': Utils.getTime(minutes=1, milliSeconds=True)}, 400, 3036, 'Campaign expired')
    ])
    def irisv2_stopMessage_mobile_afterCampaignExpires(self, campaignType, testControlType,
                                                       listType,
                                                       channel, messageInfo, editInfo, statusCode, errorCode,
                                                       errorDescription):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True, lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION')
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                  messageCreateResponse=messageDetails)
        campaignInfo = constant.config['node'][campaignType][testControlType]['CAMPAIGN']
        editInfo = CreateCampaign.edit(campaignInfo, editInfo)
        time.sleep(60)
        stopResponse = CreateMessage.stop(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                              messageDetails['RESPONSE']['json']['entity']['id'])
        CreateMessage.assertResponse(stopResponse, 400, expectedErrorCode=[errorCode],
                                     expectedErrorMessage=errorDescription)

    @pytest.mark.parametrize('campaignType,testControlType,channel,messageInfo,statusCode,errorCode,errorDescription', [
        ('LIVE', 'ORG', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}, 400, 3057,
         'Message is not approved'),
    ])
    def irisv2_message_create_stop_filter_mobile_particularDate_plain_beforeApproving(self, campaignType,
                                                                                           testControlType,
                                                                                           channel, messageInfo,
                                                                                           statusCode, errorCode,
                                                                                           errorDescription):
        self.listInfo = CreateAudience.uploadList('LIVE', 'ORG')
        payload = copy.deepcopy(constant.payload['createMessagev2'])
        payload['targetAudience'].update({'include': [self.listInfo['ID']]})
        payload['schedule']['scheduleType'] = 'PARTICULAR_DATE'
        payload['schedule']['scheduledDate'] = int(time.time() * 1000) + 4 * 60 * 60 * 1000 + 2 * 60 * 1000
        messageDetails = CreateMessage.create(campaignType, testControlType, 'LOYALTY', channel, messageInfo,
                                              payload=payload, updateNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'], 'VARIANT_CREATION')
        stopResponse = CreateMessage.stop(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                            messageDetails['RESPONSE']['json']['entity']['id'])
        Assertion.constructAssertion(stopResponse['statusCode'] == statusCode,
                                     'Actual Status Code :{} and Expected : {}'.format(
                                         stopResponse['statusCode'], statusCode))
        Assertion.constructAssertion(stopResponse['json']['errors'][0]['code'] == errorCode,
                                     'Actual Error Code :{} and Expected : {}'.format(
                                         stopResponse['json']['errors'][0]['code'], errorCode))
        Assertion.constructAssertion(errorDescription.format(messageDetails['RESPONSE']['json']['entity']['id']) ==
                                     stopResponse['json']['errors'][0]['message'],
                                     'Actual Error Code :{} and Expected : {}'.format(
                                         stopResponse['json']['errors'][0]['message'], errorDescription))

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo,statusCode,errorCode,errorDescription', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}, 400, 3038,
             'Invalid Schedule : Message scheduled date is in past.'),
    ])
    def irisv2_message_create_messagewith2minute_execute_stop_upload_mobile_particularDate_plain(self, campaignType,
                                                                                                 testControlType,
                                                                                                 listType,
                                                                                                 channel,
                                                                                                 messageInfo,statusCode,errorCode,errorDescription):
        self.listInfo = CreateAudience.uploadList('LIVE', 'ORG')
        payload = copy.deepcopy(constant.payload['createMessagev2'])
        payload['targetAudience'].update({'include': [self.listInfo['ID']]})
        payload['schedule']['scheduleType'] = 'PARTICULAR_DATE'
        payload['schedule']['scheduledDate'] = int(time.time() * 1000) + 1 * 60 * 1000
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              payload=payload, updateNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'], 'VARIANT_CREATION')
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                  messageCreateResponse=messageDetails)
        AuthorizeMessage.assertResponse(approveRespone, 200)
        time.sleep(55)
        stopResponse = CreateMessage.stop(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                            approveRespone['json']['entity']['messageId'])
        Assertion.constructAssertion(stopResponse['statusCode'] == statusCode,
                                     'Actual Status Code :{} and Expected : {}'.format(
                                         stopResponse['statusCode'], statusCode))
        Assertion.constructAssertion(stopResponse['json']['errors'][0]['code'] == errorCode,
                                     'Actual Error Code :{} and Expected : {}'.format(
                                         stopResponse['json']['errors'][0]['code'], errorCode))
        Assertion.constructAssertion(errorDescription.format(messageDetails['RESPONSE']['json']['entity']['id']) ==
                                     stopResponse['json']['errors'][0]['message'],
                                     'Actual Error Code :{} and Expected : {}'.format(
                                         stopResponse['json']['errors'][0]['message'], errorDescription))

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo,statusCode,errorCode,errorDescription', [
        ('LIVE', 'ORG', 'LOYALTY', 'MOBILE',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}, 400, 3057,
             'Message is not approved')
    ])
    def irisv2_message_create_stop_filter_mobile_Recurring_plain_beforeApproving(self, campaignType, testControlType,
                                                                             listType,
                                                                             channel, messageInfo,statusCode,errorCode,errorDescription):
        messageDetails = CreateMessage.create(campaignType, testControlType, 'LOYALTY', channel, messageInfo,
                                              updateNode=True, lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'], 'VARIANT_CREATION')
        stopResponse = CreateMessage.stop(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                            messageDetails['RESPONSE']['json']['entity']['id'])
        Assertion.constructAssertion(stopResponse['statusCode'] == statusCode,
                                     'Actual Status Code :{} and Expected : {}'.format(
                                         stopResponse['statusCode'], statusCode))
        Assertion.constructAssertion(stopResponse['json']['errors'][0]['code'] == errorCode,
                                     'Actual Error Code :{} and Expected : {}'.format(
                                         stopResponse['json']['errors'][0]['code'], errorCode))
        Assertion.constructAssertion(errorDescription.format(messageDetails['RESPONSE']['json']['entity']['id']) ==
                                     stopResponse['json']['errors'][0]['message'],
                                     'Actual Error Code :{} and Expected : {}'.format(
                                         stopResponse['json']['errors'][0]['message'], errorDescription))

    @pytest.mark.parametrize('campaignType,testControlType,channel,messageInfo,statusCode,errorCode,errorDescription', [
        ('LIVE', 'ORG', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}, 400, 3038,
             'Invalid Schedule : IMMEDIATE')
    ])
    def irisv2_message_create_stop_filter_mobile_immediate_plain_beforeAprroving(self, campaignType, testControlType,
                                                                      channel, messageInfo,statusCode,errorCode,errorDescription):
        messageDetails = CreateMessage.create(campaignType, testControlType, 'LOYALTY', channel, messageInfo,
                                              updateNode=True, lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        stopResponse = CreateMessage.stop(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                            messageDetails['RESPONSE']['json']['entity']['id'])
        Assertion.constructAssertion(stopResponse['statusCode'] == statusCode,
                                     'Actual Status Code :{} and Expected : {}'.format(
                                         stopResponse['statusCode'], statusCode))
        Assertion.constructAssertion(stopResponse['json']['errors'][0]['code'] == errorCode,
                                     'Actual Error Code :{} and Expected : {}'.format(
                                         stopResponse['json']['errors'][0]['code'], errorCode))
        Assertion.constructAssertion(errorDescription.format(messageDetails['RESPONSE']['json']['entity']['id']) ==
                                     stopResponse['json']['errors'][0]['message'],
                                     'Actual Error Code :{} and Expected : {}'.format(
                                         stopResponse['json']['errors'][0]['message'], errorDescription))

    @pytest.mark.parametrize('campaignType,testControlType,channel,messageInfo,statusCode,errorCode,errorDescription', [
        ('LIVE', 'ORG', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}, 400, 3038,
         'Invalid Schedule : IMMEDIATE')
    ])
    def irisv2_message_create_stop_filter_mobile_immediate_plain_afterAprroving(self, campaignType,
                                                                                      testControlType,
                                                                                      channel, messageInfo, statusCode,
                                                                                      errorCode, errorDescription):
        messageDetails = CreateMessage.create(campaignType, testControlType, 'LOYALTY', channel, messageInfo,
                                              updateNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, 'LOYALTY', channel, messageInfo,
                                                  messageCreateResponse=messageDetails)
        AuthorizeMessage.assertResponse(approveRespone, 200)
        stopResponse = CreateMessage.stop(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                            approveRespone['json']['entity']['messageId'])
        Assertion.constructAssertion(stopResponse['statusCode'] == statusCode,
                                     'Actual Status Code :{} and Expected : {}'.format(
                                         stopResponse['statusCode'], statusCode))
        Assertion.constructAssertion(stopResponse['json']['errors'][0]['code'] == errorCode,
                                     'Actual Error Code :{} and Expected : {}'.format(
                                         stopResponse['json']['errors'][0]['code'], errorCode))
        Assertion.constructAssertion(errorDescription.format(messageDetails['RESPONSE']['json']['entity']['id']) ==
                                     stopResponse['json']['errors'][0]['message'],
                                     'Actual Error Code :{} and Expected : {}'.format(
                                         stopResponse['json']['errors'][0]['message'], errorDescription))

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo,statusCode,errorCode,errorDescription', [
        ('LIVE', 'ORG', 'LOYALTY', 'MOBILE',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}, 400, 3023,
         'Message with message id {} does not exists')
    ])
    def irisv2_stopMessage_mobile_with_campaignId_of_another_campaign(self, campaignType, testControlType,
                                                                    listType,
                                                                    channel, messageInfo, statusCode, errorCode,
                                                                    errorDescription):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True, lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        campaignInfo = CreateCampaign.create(campaignType, testControlType, updateNode=True)
        stopResponse = CreateMessage.stop(
            campaignInfo['ID'], messageDetails['RESPONSE']['json']['entity']['id'])
        Assertion.constructAssertion(stopResponse['statusCode'] == statusCode,
                                     'Actual Status Code :{} and Expected : {}'.format(
                                         stopResponse['statusCode'], statusCode))
        Assertion.constructAssertion(stopResponse['json']['errors'][0]['code'] == errorCode,
                                     'Actual Error Code :{} and Expected : {}'.format(
                                         stopResponse['json']['errors'][0]['code'], errorCode))
        Assertion.constructAssertion(errorDescription.format(messageDetails['RESPONSE']['json']['entity']['id']) ==
                                     stopResponse['json']['errors'][0]['message'],
                                     'Actual Error Code :{} and Expected : {}'.format(
                                         stopResponse['json']['errors'][0]['message'], errorDescription))

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo,statusCode,errorCode,errorDescription', [
        ('LIVE', 'ORG', 'LOYALTY', 'MOBILE',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}, 400, 3023,
         'Message with message id {} does not exists')
    ])
    def irisv2_stopMessage_mobile_with_invalid_campaignId(self, campaignType, testControlType,
                                                        listType,
                                                        channel, messageInfo, statusCode, errorCode, errorDescription):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True, lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        stopResponse = CreateMessage.stop(
            3453553, messageDetails['RESPONSE']['json']['entity']['id'])
        Assertion.constructAssertion(stopResponse['statusCode'] == statusCode,
                                     'Actual Status Code :{} and Expected : {}'.format(
                                         stopResponse['statusCode'], statusCode))
        Assertion.constructAssertion(stopResponse['json']['errors'][0]['code'] == errorCode,
                                     'Actual Error Code :{} and Expected : {}'.format(
                                         stopResponse['json']['errors'][0]['code'], errorCode))
        Assertion.constructAssertion(errorDescription.format(messageDetails['RESPONSE']['json']['entity']['id']) ==
                                     stopResponse['json']['errors'][0]['message'],
                                     'Actual Error Code :{} and Expected : {}'.format(
                                         stopResponse['json']['errors'][0]['message'], errorDescription))

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo,statusCode,errorCode,errorDescription', [
        ('LIVE', 'ORG', 'LOYALTY', 'MOBILE',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}, 400, 3023,
         'Message with message id 1231342 does not exists')
    ])
    def irisv2_stopMessage_mobile_with_invalid_messageId(self, campaignType, testControlType,
                                                       listType,
                                                       channel, messageInfo, statusCode, errorCode, errorDescription):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True, lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        stopResponse = CreateMessage.stop(
            constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'], '1231342')
        Assertion.constructAssertion(stopResponse['statusCode'] == statusCode,
                                     'Actual Status Code :{} and Expected : {}'.format(
                                         stopResponse['statusCode'], statusCode))
        Assertion.constructAssertion(stopResponse['json']['errors'][0]['code'] == errorCode,
                                     'Actual Error Code :{} and Expected : {}'.format(
                                         stopResponse['json']['errors'][0]['code'], errorCode))
        Assertion.constructAssertion(errorDescription ==
                                     stopResponse['json']['errors'][0]['message'],
                                     'Actual Error Code :{} and Expected : {}'.format(
                                         stopResponse['json']['errors'][0]['message'], errorDescription))

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo,statusCode,errorCode,errorDescription', [
        ('LIVE', 'ORG', 'LOYALTY', 'MOBILE',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}, 400, 102,
         'Invalid request : CampaignId must be greater than or equal to 1')
    ])
    def irisv2_stopMessage_mobile_with_negative_campaignId(self, campaignType, testControlType,
                                                         listType,
                                                         channel, messageInfo, statusCode, errorCode,
                                                         errorDescription):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True, lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        stopResponse = CreateMessage.stop(
            -1234, messageDetails['RESPONSE']['json']['entity']['id'])
        Assertion.constructAssertion(stopResponse['statusCode'] == statusCode,
                                     'Actual Status Code :{} and Expected : {}'.format(
                                         stopResponse['statusCode'], statusCode))
        Assertion.constructAssertion(stopResponse['json']['errors'][0]['code'] == errorCode,
                                     'Actual Error Code :{} and Expected : {}'.format(
                                         stopResponse['json']['errors'][0]['code'], errorCode))
        Assertion.constructAssertion(errorDescription.format(messageDetails['RESPONSE']['json']['entity']['id']) ==
                                     stopResponse['json']['errors'][0]['message'],
                                     'Actual Error Code :{} and Expected : {}'.format(
                                         stopResponse['json']['errors'][0]['message'], errorDescription))

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo,statusCode,errorCode,errorDescription', [
        ('LIVE', 'ORG', 'LOYALTY', 'MOBILE',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}, 400, 3023,
         'Message with message id -1231342 does not exists')
    ])
    def irisv2_stopMessage_mobile_with_negative_messageId(self, campaignType, testControlType,
                                                        listType,
                                                        channel, messageInfo, statusCode, errorCode, errorDescription):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True, lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        stopResponse = CreateMessage.stop(
            constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'], '-1231342')
        Assertion.constructAssertion(stopResponse['statusCode'] == statusCode,
                                     'Actual Status Code :{} and Expected : {}'.format(
                                         stopResponse['statusCode'], statusCode))
        Assertion.constructAssertion(stopResponse['json']['errors'][0]['code'] == errorCode,
                                     'Actual Error Code :{} and Expected : {}'.format(
                                         stopResponse['json']['errors'][0]['code'], errorCode))
        Assertion.constructAssertion(errorDescription ==
                                     stopResponse['json']['errors'][0]['message'],
                                     'Actual Error Code :{} and Expected : {}'.format(
                                         stopResponse['json']['errors'][0]['message'], errorDescription))

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo,statusCode,errorCode,errorDescription', [
        ('LIVE', 'ORG', 'LOYALTY', 'MOBILE',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}, 500, 101,
         'Generic error: HTTP 401 Unauthorized')
    ])
    def irisv2_stopMessage_mobile_with_invalid_orgId(self, campaignType, testControlType,
                                                   listType,
                                                   channel, messageInfo, statusCode, errorCode,
                                                   errorDescription):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True, lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        actualOrgId = constant.config['orgId']
        try:
            constant.config['orgId'] = 999999
            stopResponse = CreateMessage.stop(
                constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                messageDetails['RESPONSE']['json']['entity']['id'])
            Assertion.constructAssertion(stopResponse['statusCode'] == statusCode,
                                         'Actual Status Code :{} and Expected : {}'.format(
                                             stopResponse['statusCode'], statusCode))
            Assertion.constructAssertion(stopResponse['json']['errors'][0]['code'] == errorCode,
                                         'Actual Error Code :{} and Expected : {}'.format(
                                             stopResponse['json']['errors'][0]['code'], errorCode))
            Assertion.constructAssertion(errorDescription ==
                                         stopResponse['json']['errors'][0]['message'],
                                         'Actual Error Code :{} and Expected : {}'.format(
                                             stopResponse['json']['errors'][0]['message'], errorDescription))
        finally:
            constant.config['orgId'] = actualOrgId

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo,statusCode,errorCode,errorDescription', [
        ('LIVE', 'ORG', 'LOYALTY', 'MOBILE',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}, 401,
         999999,
         'Invalid org id')
    ])
    def irisv2_stopMessage_mobile_with_negative_orgId(self, campaignType, testControlType,
                                                    listType,
                                                    channel, messageInfo, statusCode, errorCode,
                                                    errorDescription):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True, lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        actualOrgId = constant.config['orgId']
        try:
            constant.config['orgId'] = -999999
            stopResponse = CreateMessage.stop(
                constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                messageDetails['RESPONSE']['json']['entity']['id'])
            Assertion.constructAssertion(stopResponse['statusCode'] == statusCode,
                                         'Actual Status Code :{} and Expected : {}'.format(
                                             stopResponse['statusCode'], statusCode))
            Assertion.constructAssertion(stopResponse['json']['errors'][0]['code'] == errorCode,
                                         'Actual Error Code :{} and Expected : {}'.format(
                                             stopResponse['json']['errors'][0]['code'], errorCode))
            Assertion.constructAssertion(errorDescription ==
                                         stopResponse['json']['errors'][0]['message'],
                                         'Actual Error Code :{} and Expected : {}'.format(
                                             stopResponse['json']['errors'][0]['message'], errorDescription))
        finally:
            constant.config['orgId'] = actualOrgId

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo,statusCode,errorCode,errorDescription', [
        ('LIVE', 'ORG', 'LOYALTY', 'MOBILE',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}, 401,
         999999,
         'Unauthorized'),
    ])
    def irisv2_stopMessage_mobile_with_wrongAuth(self, campaignType, testControlType,
                                               listType,
                                               channel, messageInfo, statusCode, errorCode,
                                               errorDescription):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True, lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        previousUserName = None
        try:
            previousUserName = IrisHelper.updateUserName('WrongName')
            stopResponse = CreateMessage.stop(
                constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                messageDetails['RESPONSE']['json']['entity']['id'])
            Assertion.constructAssertion(stopResponse['statusCode'] == statusCode,
                                         'Actual Status Code :{} and Expected : {}'.format(
                                             stopResponse['statusCode'], statusCode))
            Assertion.constructAssertion(stopResponse['json']['errors'][0]['code'] == errorCode,
                                         'Actual Error Code :{} and Expected : {}'.format(
                                             stopResponse['json']['errors'][0]['code'], errorCode))
            Assertion.constructAssertion(errorDescription ==
                                         stopResponse['json']['errors'][0]['message'],
                                         'Actual Error Code :{} and Expected : {}'.format(
                                             stopResponse['json']['errors'][0]['message'], errorDescription))
        finally:
            if previousUserName is not None: IrisHelper.updateUserName(previousUserName)
