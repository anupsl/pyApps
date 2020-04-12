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

class Test_MessageStatusStop_EditApprove():

    def setup_method(self, method):
        Logger.logMethodName(method.__name__)

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'LOYALTY', 'MOBILE',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def irisv2_message_Sanity_create_stop_edit_approve_filter_mobile_Recurring_plain(self, campaignType, testControlType,
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
        editInfo = CreateMessage.edit(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                      messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'])
        CreateMessage.assertResponse(editInfo['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(editInfo['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION', version=1)
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                  messageCreateResponse=editInfo)
        AuthorizeMessage.assertResponse(approveRespone, 200)
        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        AuthorizeMessageDBAssertion(campaignId, editInfo['RESPONSE'], editInfo['PAYLOAD'],
                                    testControlType, version=1).check()

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
    def irisv2_message_create_stop_edit_approve_filter_mobile_Recurring_plain(self, campaignType, testControlType,
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
        editInfo = CreateMessage.edit(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                      messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'])
        CreateMessage.assertResponse(editInfo['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(editInfo['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION', version=1)
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                  messageCreateResponse=editInfo)
        AuthorizeMessage.assertResponse(approveRespone, 200)
        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        AuthorizeMessageDBAssertion(campaignId, editInfo['RESPONSE'], editInfo['PAYLOAD'],
                                    testControlType, version=1).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'LOYALTY', 'MOBILE',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': True, 'encryptUrl': False, 'skipRateLimit': True}),
    ])
    def irisv2_message_create_stop_edit_approve_filter_mobile_Recurring_plain_UsingTinyURL(self, campaignType,
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
        editInfo = CreateMessage.edit(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                      messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'])
        CreateMessage.assertResponse(editInfo['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(editInfo['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION', version=1)
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                  messageCreateResponse=editInfo)
        AuthorizeMessage.assertResponse(approveRespone, 200)
        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        AuthorizeMessageDBAssertion(campaignId, editInfo['RESPONSE'], editInfo['PAYLOAD'],
                                    testControlType, version=1).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'LOYALTY', 'MOBILE',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': True, 'skipRateLimit': True}),
    ])
    def irisv2_message_create_stop_edit_approve_filter_mobile_Recurring_plain_UsingEncryptURL(self, campaignType,
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
        editInfo = CreateMessage.edit(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                      messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'])
        CreateMessage.assertResponse(editInfo['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(editInfo['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION', version=1)
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                  messageCreateResponse=editInfo)
        AuthorizeMessage.assertResponse(approveRespone, 200)
        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        AuthorizeMessageDBAssertion(campaignId, editInfo['RESPONSE'], editInfo['PAYLOAD'],
                                    testControlType, version=1).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'LOYALTY', 'MOBILE',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': False}),
    ])
    def irisv2_message_create_stop_edit_approve_filter_mobile_Recurring_plain_UsingRateLimit(self, campaignType,
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
        editInfo = CreateMessage.edit(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                      messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'])
        CreateMessage.assertResponse(editInfo['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(editInfo['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION', version=1)
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                  messageCreateResponse=editInfo)
        AuthorizeMessage.assertResponse(approveRespone, 200)
        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        AuthorizeMessageDBAssertion(campaignId, editInfo['RESPONSE'], editInfo['PAYLOAD'],
                                    testControlType, version=1).check()

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
    def irisv2_message_create_stop_edit_approve_filter_mobile_Recurring_coupon(self, campaignType, testControlType, listType,
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
        editInfo = CreateMessage.edit(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                      messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'])
        CreateMessage.assertResponse(editInfo['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(editInfo['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION', version=1)
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                  messageCreateResponse=editInfo)
        AuthorizeMessage.assertResponse(approveRespone, 200)
        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        AuthorizeMessageDBAssertion(campaignId, editInfo['RESPONSE'], editInfo['PAYLOAD'],
                                    testControlType, version=1).check()

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
    def irisv2_message_create_stop_edit_approve_filter_mobile_Recurring_points(self, campaignType, testControlType, listType,
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
        editInfo = CreateMessage.edit(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                      messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'])
        CreateMessage.assertResponse(editInfo['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(editInfo['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION', version=1)
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                  messageCreateResponse=editInfo)
        AuthorizeMessage.assertResponse(approveRespone, 200)
        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        AuthorizeMessageDBAssertion(campaignId, editInfo['RESPONSE'], editInfo['PAYLOAD'],
                                    testControlType, version=1).check()

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
    def irisv2_message_create_stop_edit_approve_filter_email_Recurring_plain(self, campaignType, testControlType,
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
        editInfo = CreateMessage.edit(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                      messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'])
        CreateMessage.assertResponse(editInfo['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(editInfo['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION', version=1)
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                  messageCreateResponse=editInfo)
        AuthorizeMessage.assertResponse(approveRespone, 200)
        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        AuthorizeMessageDBAssertion(campaignId, editInfo['RESPONSE'], editInfo['PAYLOAD'],
                                    testControlType, version=1).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'LOYALTY', 'EMAIL',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': True, 'encryptUrl': False, 'skipRateLimit': True}),
    ])
    def irisv2_message_create_stop_edit_approve_filter_email_Recurring_plain_UsingTinyURL(self, campaignType,
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
        editInfo = CreateMessage.edit(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                      messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'])
        CreateMessage.assertResponse(editInfo['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(editInfo['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION', version=1)
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                  messageCreateResponse=editInfo)
        AuthorizeMessage.assertResponse(approveRespone, 200)
        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        AuthorizeMessageDBAssertion(campaignId, editInfo['RESPONSE'], editInfo['PAYLOAD'],
                                    testControlType, version=1).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'LOYALTY', 'EMAIL',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': True, 'skipRateLimit': True}),
    ])
    def irisv2_message_create_stop_edit_approve_filter_email_Recurring_plain_UsingEncryptURL(self, campaignType,
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
        editInfo = CreateMessage.edit(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                      messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'])
        CreateMessage.assertResponse(editInfo['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(editInfo['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION', version=1)
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                  messageCreateResponse=editInfo)
        AuthorizeMessage.assertResponse(approveRespone, 200)
        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        AuthorizeMessageDBAssertion(campaignId, editInfo['RESPONSE'], editInfo['PAYLOAD'],
                                    testControlType, version=1).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'LOYALTY', 'EMAIL',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': False}),
    ])
    def irisv2_message_create_stop_edit_approve_filter_email_Recurring_plain_UsingRateLimit(self, campaignType,
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
        editInfo = CreateMessage.edit(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                      messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'])
        CreateMessage.assertResponse(editInfo['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(editInfo['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION', version=1)
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                  messageCreateResponse=editInfo)
        AuthorizeMessage.assertResponse(approveRespone, 200)
        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        AuthorizeMessageDBAssertion(campaignId, editInfo['RESPONSE'], editInfo['PAYLOAD'],
                                    testControlType, version=1).check()

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
    def irisv2_message_create_stop_edit_approve_filter_email_Recurring_coupon(self, campaignType, testControlType, listType,
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
        editInfo = CreateMessage.edit(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                      messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'])
        CreateMessage.assertResponse(editInfo['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(editInfo['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION', version=1)
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                  messageCreateResponse=editInfo)
        AuthorizeMessage.assertResponse(approveRespone, 200)
        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        AuthorizeMessageDBAssertion(campaignId, editInfo['RESPONSE'], editInfo['PAYLOAD'],
                                    testControlType, version=1).check()

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
    def irisv2_message_create_stop_edit_approve_filter_email_Recurring_points(self, campaignType, testControlType, listType,
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
        editInfo = CreateMessage.edit(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                      messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'])
        CreateMessage.assertResponse(editInfo['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(editInfo['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION', version=1)
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                  messageCreateResponse=editInfo)
        AuthorizeMessage.assertResponse(approveRespone, 200)
        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        AuthorizeMessageDBAssertion(campaignId, editInfo['RESPONSE'], editInfo['PAYLOAD'],
                                    testControlType, version=1).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
    ])
    def irisv2_message_create_stop_edit_approve_messagewith2minute_upload_mobile_particularDate_plain(self, campaignType,
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
        editInfo = CreateMessage.edit(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                      messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'])
        CreateMessage.assertResponse(editInfo['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(editInfo['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION', version=1)
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                  messageCreateResponse=editInfo)
        AuthorizeMessage.assertResponse(approveRespone, 200)
        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        AuthorizeMessageDBAssertion(campaignId, editInfo['RESPONSE'], editInfo['PAYLOAD'],
                                    testControlType, version=1).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'EMAIL',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
    ])
    def irisv2_message_create_stop_edit_approve_messagewith2minute_upload_email_particularDate_plain(self, campaignType,
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
        editInfo = CreateMessage.edit(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                      messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'])
        CreateMessage.assertResponse(editInfo['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(editInfo['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION', version=1)
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                  messageCreateResponse=editInfo)
        AuthorizeMessage.assertResponse(approveRespone, 200)
        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        AuthorizeMessageDBAssertion(campaignId, editInfo['RESPONSE'], editInfo['PAYLOAD'],
                                    testControlType, version=1).check()