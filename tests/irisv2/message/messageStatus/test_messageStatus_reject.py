import pytest,copy,time
from src.modules.irisv2.list.createAudience import CreateAudience
from src.dbCalls.messageInfo import message_calls
from src.utilities.logger import Logger
from src.Constant.constant import constant
from src.modules.irisv2.message.createMessage import CreateMessage
from src.modules.irisv2.message.createMessageDbAssertion import CreateMessageDBAssertion
from src.modules.irisv2.message.authorizeMessage import AuthorizeMessage
from src.modules.irisv2.message.authorizeMessageDbAssertion import AuthorizeMessageDBAssertion
from src.modules.irisv2.campaigns.createCampaign import CreateCampaign
from src.utilities.assertion import Assertion
from src.modules.irisv2.helper.irisHelper import IrisHelper
from src.utilities.utils import Utils


class Test_MessageStatus_Reject():

    def setup_method(self, method):
        Logger.logMethodName(method.__name__)

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
    ])
    def irisv2_message_Sanity_create_reject_upload_mobile_immediate_plain(self, campaignType, testControlType, listType,
                                                                        channel, messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo, updateNode=True, lockNode=True)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'], 'VARIANT_CREATION')
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        rejectResponse = CreateMessage.reject(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'], messageDetails['RESPONSE']['json']['entity']['id'])
        CreateMessage.assertResponse(rejectResponse, 200)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],approved= 'REJECTED').check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'CUSTOM', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'SKIP', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'CUSTOM', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'SKIP', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def irisv2_message_create_reject_upload_mobile_immediate_plain(self, campaignType, testControlType, listType,
                                                                        channel, messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo, updateNode=True, lockNode=True)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'], 'VARIANT_CREATION')
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        rejectResponse = CreateMessage.reject(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'], messageDetails['RESPONSE']['json']['entity']['id'])
        CreateMessage.assertResponse(rejectResponse, 200)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],approved='REJECTED').check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': True, 'encryptUrl': False, 'skipRateLimit': True}),
    ])
    def irisv2_message_create_reject_upload_mobile_immediate_plain_additionalProperties_UsingTinyURL(self,
                                                                                                          campaignType,
                                                                                                          testControlType,
                                                                                                          listType,
                                                                                                          channel,
                                                                                                          messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True,
                                              lockNode=True)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'], 'VARIANT_CREATION')
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        rejectResponse = CreateMessage.reject(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                              messageDetails['RESPONSE']['json']['entity']['id'])
        CreateMessage.assertResponse(rejectResponse, 200)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],
                                 approved='REJECTED').check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': True, 'skipRateLimit': True}),
    ])
    def irisv2_message_create_reject_upload_mobile_immediate_plain_additionalProperties_UsingEncryptURL(self,
                                                                                                             campaignType,
                                                                                                             testControlType,
                                                                                                             listType,
                                                                                                             channel,
                                                                                                             messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True,
                                              lockNode=True)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'], 'VARIANT_CREATION')
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        rejectResponse = CreateMessage.reject(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                              messageDetails['RESPONSE']['json']['entity']['id'])
        CreateMessage.assertResponse(rejectResponse, 200)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],
                                 approved='REJECTED').check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': False}),
    ])
    def irisv2_message_create_reject_upload_mobile_immediate_plain_additionalProperties_UsingRateLimit(self,
                                                                                                            campaignType,
                                                                                                            testControlType,
                                                                                                            listType,
                                                                                                            channel,
                                                                                                            messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True,
                                              lockNode=True)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'], 'VARIANT_CREATION')
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        rejectResponse = CreateMessage.reject(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                              messageDetails['RESPONSE']['json']['entity']['id'])
        CreateMessage.assertResponse(rejectResponse, 200)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],
                                 approved='REJECTED').check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'CUSTOM', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'SKIP', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'CUSTOM', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'SKIP', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def irisv2_message_create_reject_upload_mobile_immediate_coupon(self, campaignType, testControlType, listType,
                                                                         channel, messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo, updateNode=True, lockNode=True)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'], 'VARIANT_CREATION')
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        rejectResponse = CreateMessage.reject(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                              messageDetails['RESPONSE']['json']['entity']['id'])
        CreateMessage.assertResponse(rejectResponse, 200)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],
                                 approved='REJECTED',
                                 offer=True).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'CUSTOM', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'SKIP', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'CUSTOM', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'SKIP', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def irisv2_message_create_reject_upload_mobile_immediate_points(self, campaignType, testControlType, listType,
                                                                         channel, messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo, updateNode=True, lockNode=True)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'], 'VARIANT_CREATION')
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        rejectResponse = CreateMessage.reject(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                              messageDetails['RESPONSE']['json']['entity']['id'])
        CreateMessage.assertResponse(rejectResponse, 200)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],
                                 approved='REJECTED',
                                 offer=True).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
    ])
    def irisv2_message_create_reject_upload_mobile_particularDate_plain(self, campaignType, testControlType,
                                                                             listType,
                                                                             channel, messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True, lockNode=True)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'], 'VARIANT_CREATION')
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        rejectResponse = CreateMessage.reject(
            constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
            messageDetails['RESPONSE']['json']['entity']['id'])
        CreateMessage.assertResponse(rejectResponse, 200)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],
                                 reject={'status': 'CLOSED'}, approved='REJECTED').check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': True, 'encryptUrl': False, 'skipRateLimit': True}),
    ])
    def irisv2_message_create_reject_upload_mobile_particularDate_plain_UsingTinyURL(self, campaignType,
                                                                                          testControlType,
                                                                                          listType, channel,
                                                                                          messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True,
                                              lockNode=True)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'], 'VARIANT_CREATION')
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        rejectResponse = CreateMessage.reject(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                              messageDetails['RESPONSE']['json']['entity']['id'])
        CreateMessage.assertResponse(rejectResponse, 200)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],
                                 reject={'status': 'CLOSED'}, approved='REJECTED').check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': True, 'skipRateLimit': True}),
    ])
    def irisv2_message_create_reject_upload_mobile_particularDate_plain_UsingEncryptURL(self, campaignType,
                                                                                             testControlType,
                                                                                             listType, channel,
                                                                                             messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True,
                                              lockNode=True)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'], 'VARIANT_CREATION')
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        rejectResponse = CreateMessage.reject(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                              messageDetails['RESPONSE']['json']['entity']['id'])
        CreateMessage.assertResponse(rejectResponse, 200)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],
                                 reject={'status': 'CLOSED'}, approved='REJECTED').check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': False}),
    ])
    def irisv2_message_create_reject_upload_mobile_particularDate_plain_UsingRateLimit(self, campaignType,
                                                                                            testControlType,
                                                                                            listType, channel,
                                                                                            messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True,
                                              lockNode=True)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'], 'VARIANT_CREATION')
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        rejectResponse = CreateMessage.reject(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                              messageDetails['RESPONSE']['json']['entity']['id'])
        CreateMessage.assertResponse(rejectResponse, 200)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],
                                 reject={'status': 'CLOSED'}, approved='REJECTED').check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'CUSTOM', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'SKIP', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'CUSTOM', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'SKIP', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def irisv2_message_create_reject_upload_mobile_particularDate_coupon(self, campaignType, testControlType,
                                                                              listType,
                                                                              channel, messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True, lockNode=True)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'], 'VARIANT_CREATION')
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        rejectResponse = CreateMessage.reject(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                              messageDetails['RESPONSE']['json']['entity']['id'])
        CreateMessage.assertResponse(rejectResponse, 200)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],
                                 reject={'status': 'CLOSED'}, approved='REJECTED',
                                 offer=True).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'CUSTOM', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'SKIP', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'CUSTOM', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'SKIP', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def irisv2_message_create_reject_upload_mobile_particularDate_points(self, campaignType, testControlType,
                                                                              listType,
                                                                              channel, messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True, lockNode=True)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'], 'VARIANT_CREATION')
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        rejectResponse = CreateMessage.reject(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                              messageDetails['RESPONSE']['json']['entity']['id'])
        CreateMessage.assertResponse(rejectResponse, 200)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],
                                 reject={'status': 'CLOSED'}, approved='REJECTED',
                                 offer=True).check()

    @pytest.mark.parametrize('campaignType,testControlType,channel,messageInfo', [
        ('LIVE', 'ORG', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),

    ])
    def irisv2_message_Sanity_create_reject_filter_mobile_immediate_plain(self, campaignType, testControlType,
                                                                        channel, messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, 'LOYALTY', channel, messageInfo, updateNode=True, lockNode=True)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'], 'VARIANT_CREATION')
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        rejectResponse = CreateMessage.reject(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                              messageDetails['RESPONSE']['json']['entity']['id'])
        CreateMessage.assertResponse(rejectResponse, 200)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],
                                 approved='REJECTED').check()

    @pytest.mark.parametrize('campaignType,testControlType,channel,messageInfo', [
        ('LIVE', 'ORG', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'CUSTOM', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'SKIP', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'ORG', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'CUSTOM', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'SKIP', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def irisv2_message_create_reject_filter_mobile_immediate_plain(self, campaignType, testControlType,
                                                                 channel, messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, 'LOYALTY', channel, messageInfo, updateNode=True, lockNode=True)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'], 'VARIANT_CREATION')
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        rejectResponse = CreateMessage.reject(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                              messageDetails['RESPONSE']['json']['entity']['id'])
        CreateMessage.assertResponse(rejectResponse, 200)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'],
                                 messageDetails['PAYLOAD'], approved='REJECTED').check()

    @pytest.mark.parametrize('campaignType,testControlType,channel,messageInfo', [
        ('LIVE', 'ORG', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'CUSTOM', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'SKIP', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'ORG', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'CUSTOM', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'SKIP', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def irisv2_message_create_reject_filter_mobile_particularDate_plain(self, campaignType, testControlType,
                                                                      channel, messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, 'LOYALTY', channel, messageInfo, updateNode=True, lockNode=True)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'], 'VARIANT_CREATION')
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        rejectResponse = CreateMessage.reject(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                              messageDetails['RESPONSE']['json']['entity']['id'])
        CreateMessage.assertResponse(rejectResponse, 200)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],
                                 reject={'status':'CLOSED'},approved='REJECTED').check()

    @pytest.mark.parametrize('campaignType,testControlType,channel,messageInfo', [
        ('LIVE', 'ORG', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'CUSTOM', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'SKIP', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'ORG', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'CUSTOM', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'SKIP', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def irisv2_message_create_reject_filter_mobile_immediate_coupon(self, campaignType, testControlType,
                                                                  channel, messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, 'LOYALTY', channel, messageInfo, updateNode=True, lockNode=True)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'], 'VARIANT_CREATION')
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        rejectResponse = CreateMessage.reject(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                              messageDetails['RESPONSE']['json']['entity']['id'])
        CreateMessage.assertResponse(rejectResponse, 200)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],
                                 approved='REJECTED').check()

    @pytest.mark.parametrize('campaignType,testControlType,channel,messageInfo', [
        ('LIVE', 'ORG', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),

    ])
    def irisv2_message_create_reject_filter_mobile_immediate_coupon(self, campaignType, testControlType,
                                                                  channel, messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, 'LOYALTY', channel, messageInfo)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'], 'VARIANT_CREATION')
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        rejectResponse = CreateMessage.reject(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                              messageDetails['RESPONSE']['json']['entity']['id'])
        CreateMessage.assertResponse(rejectResponse, 200)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],
                                 approved='REJECTED').check()

    @pytest.mark.parametrize('campaignType,testControlType,channel,messageInfo', [
        ('LIVE', 'ORG', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'CUSTOM', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'SKIP', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'ORG', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'CUSTOM', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'SKIP', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def irisv2_message_create_reject_filter_mobile_particularDate_coupon(self, campaignType, testControlType,
                                                                       channel, messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, 'LOYALTY', channel, messageInfo, updateNode=True, lockNode=True)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'], 'VARIANT_CREATION')
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        rejectResponse = CreateMessage.reject(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                              messageDetails['RESPONSE']['json']['entity']['id'])
        CreateMessage.assertResponse(rejectResponse, 200)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],
                                 reject={'status':'CLOSED'},approved='REJECTED').check()

    @pytest.mark.parametrize('campaignType,testControlType,channel,messageInfo', [
        ('LIVE', 'ORG', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'CUSTOM', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'SKIP', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'ORG', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'CUSTOM', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'SKIP', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def irisv2_message_create_reject_filter_mobile_immediate_points(self, campaignType, testControlType,
                                                                         channel, messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, 'LOYALTY', channel, messageInfo, updateNode=True, lockNode=True)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'], 'VARIANT_CREATION')
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        rejectResponse = CreateMessage.reject(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                              messageDetails['RESPONSE']['json']['entity']['id'])
        CreateMessage.assertResponse(rejectResponse, 200)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],
                                 approved='REJECTED', offer=True).check()

    @pytest.mark.parametrize('campaignType,testControlType,channel,messageInfo', [
        ('LIVE', 'ORG', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'CUSTOM', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'SKIP', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'ORG', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'CUSTOM', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'SKIP', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def irisv2_message_create_reject_filter_mobile_particularDate_points(self, campaignType, testControlType,
                                                                              channel, messageInfo, updateNode=True, lockNode=True):
        messageDetails = CreateMessage.create(campaignType, testControlType, 'LOYALTY', channel, messageInfo)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'], 'VARIANT_CREATION')
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        rejectResponse = CreateMessage.reject(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                              messageDetails['RESPONSE']['json']['entity']['id'])
        CreateMessage.assertResponse(rejectResponse, 200)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],
                                 reject={'status':'CLOSED'},approved='REJECTED', offer=True).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'LOYALTY', 'MOBILE',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
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
    def irisv2_message_create_reject_filter_mobile_Recurring_plain(self, campaignType, testControlType,
                                                                        listType,
                                                                        channel, messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo, updateNode=True, lockNode=True)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'], 'VARIANT_CREATION')
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        rejectResponse = CreateMessage.reject(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                              messageDetails['RESPONSE']['json']['entity']['id'])
        CreateMessage.assertResponse(rejectResponse, 200)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'],
                                 messageDetails['PAYLOAD'], reject={'status':'CLOSED'},approved='REJECTED').check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'LOYALTY', 'MOBILE',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': True, 'encryptUrl': False, 'skipRateLimit': True}),
    ])
    def irisv2_message_create_reject_filter_mobile_Recurring_plain_UsingTinyURL(self, campaignType,
                                                                                     testControlType,
                                                                                     listType, channel, messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True,
                                              lockNode=True)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'], 'VARIANT_CREATION')
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        rejectResponse = CreateMessage.reject(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                              messageDetails['RESPONSE']['json']['entity']['id'])
        CreateMessage.assertResponse(rejectResponse, 200)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],
                                 reject={'status':'CLOSED'},approved='REJECTED').check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'LOYALTY', 'MOBILE',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': True, 'skipRateLimit': True}),
    ])
    def irisv2_message_create_reject_filter_mobile_Recurring_plain_UsingEncryptURL(self, campaignType,
                                                                                        testControlType,
                                                                                        listType, channel, messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True,
                                              lockNode=True)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'], 'VARIANT_CREATION')
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        rejectResponse = CreateMessage.reject(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                              messageDetails['RESPONSE']['json']['entity']['id'])
        CreateMessage.assertResponse(rejectResponse, 200)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],
                                 reject={'status':'CLOSED'},approved='REJECTED').check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'LOYALTY', 'MOBILE',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': False}),
    ])
    def irisv2_message_create_reject_filter_mobile_Recurring_plain_UsingRateLimit(self, campaignType,
                                                                                       testControlType,
                                                                                       listType, channel, messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True,
                                              lockNode=True)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'], 'VARIANT_CREATION')
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        rejectResponse = CreateMessage.reject(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                              messageDetails['RESPONSE']['json']['entity']['id'])
        CreateMessage.assertResponse(rejectResponse, 200)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],
                                 reject={'status':'CLOSED'},approved='REJECTED').check()

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
    def irisv2_message_create_reject_filter_mobile_Recurring_coupon(self, campaignType, testControlType, listType,
                                                                         channel, messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo, updateNode=True, lockNode=True)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'], 'VARIANT_CREATION')
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        rejectResponse = CreateMessage.reject(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                              messageDetails['RESPONSE']['json']['entity']['id'])
        CreateMessage.assertResponse(rejectResponse, 200)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],
                                 reject={'status':'CLOSED'},approved='REJECTED', offer=True).check()

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
    def irisv2_message_create_reject_filter_mobile_Recurring_points(self, campaignType, testControlType, listType,
                                                                         channel, messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo, updateNode=True, lockNode=True)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'], 'VARIANT_CREATION')
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        rejectResponse = CreateMessage.reject(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                              messageDetails['RESPONSE']['json']['entity']['id'])
        CreateMessage.assertResponse(rejectResponse, 200)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],
                                 reject={'status':'CLOSED'},approved='REJECTED', offer=True).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'EMAIL',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),

    ])
    def irisv2_message_Sanity_create_reject_upload_email_immediate_plain(self, campaignType, testControlType,
                                                                              listType,
                                                                              channel, messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo, updateNode=True, lockNode=True)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'], 'VARIANT_CREATION')
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        rejectResponse = CreateMessage.reject(
            constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
            messageDetails['RESPONSE']['json']['entity']['id'])
        CreateMessage.assertResponse(rejectResponse, 200)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],
                                 approved='REJECTED').check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'CUSTOM', 'UPLOAD', 'EMAIL',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'SKIP', 'UPLOAD', 'EMAIL',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'ORG', 'UPLOAD', 'EMAIL',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'CUSTOM', 'UPLOAD', 'EMAIL',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'SKIP', 'UPLOAD', 'EMAIL',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def irisv2_message_create_reject_upload_email_immediate_plain(self, campaignType, testControlType,
                                                                       listType,
                                                                       channel, messageInfo, updateNode=True, lockNode=True):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'], 'VARIANT_CREATION')
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        rejectResponse = CreateMessage.reject(
            constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
            messageDetails['RESPONSE']['json']['entity']['id'])
        CreateMessage.assertResponse(rejectResponse, 200)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],
                                 approved='REJECTED').check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'EMAIL',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': True, 'encryptUrl': False, 'skipRateLimit': True}),
    ])
    def irisv2_message_create_reject_upload_email_immediate_plain_additionalProperties_UsingTinyURL(self,
                                                                                                         campaignType,
                                                                                                         testControlType,
                                                                                                         listType,
                                                                                                         channel,
                                                                                                         messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True,
                                              lockNode=True)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'], 'VARIANT_CREATION')
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        rejectResponse = CreateMessage.reject(
            constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
            messageDetails['RESPONSE']['json']['entity']['id'])
        CreateMessage.assertResponse(rejectResponse, 200)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],
                                 approved='REJECTED').check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'EMAIL',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': True, 'skipRateLimit': True}),
    ])
    def irisv2_message_create_reject_upload_email_immediate_plain_additionalProperties_UsingEncryptURL(self,
                                                                                                            campaignType,
                                                                                                            testControlType,
                                                                                                            listType,
                                                                                                            channel,
                                                                                                            messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True,
                                              lockNode=True)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'], 'VARIANT_CREATION')
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        rejectResponse = CreateMessage.reject(
            constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
            messageDetails['RESPONSE']['json']['entity']['id'])
        CreateMessage.assertResponse(rejectResponse, 200)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],
                                 approved='REJECTED').check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'EMAIL',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': False}),
    ])
    def irisv2_message_create_reject_upload_email_immediate_plain_additionalProperties_UsingRateLimit(self,
                                                                                                           campaignType,
                                                                                                           testControlType,
                                                                                                           listType,
                                                                                                           channel,
                                                                                                           messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True,
                                              lockNode=True)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'], 'VARIANT_CREATION')
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        rejectResponse = CreateMessage.reject(
            constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
            messageDetails['RESPONSE']['json']['entity']['id'])
        CreateMessage.assertResponse(rejectResponse, 200)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],
                                 approved='REJECTED').check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'EMAIL',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'CUSTOM', 'UPLOAD', 'EMAIL',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'SKIP', 'UPLOAD', 'EMAIL',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'ORG', 'UPLOAD', 'EMAIL',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'CUSTOM', 'UPLOAD', 'EMAIL',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'SKIP', 'UPLOAD', 'EMAIL',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def irisv2_message_create_reject_upload_email_immediate_coupon(self, campaignType, testControlType,
                                                                        listType,
                                                                        channel, messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo, updateNode=True, lockNode=True)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'], 'VARIANT_CREATION')
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        rejectResponse = CreateMessage.reject(
            constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
            messageDetails['RESPONSE']['json']['entity']['id'])
        CreateMessage.assertResponse(rejectResponse, 200)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],
                                 approved='REJECTED',
                                 offer=True).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'EMAIL',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'CUSTOM', 'UPLOAD', 'EMAIL',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'SKIP', 'UPLOAD', 'EMAIL',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'ORG', 'UPLOAD', 'EMAIL',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'CUSTOM', 'UPLOAD', 'EMAIL',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'SKIP', 'UPLOAD', 'EMAIL',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def irisv2_message_create_reject_upload_email_immediate_points(self, campaignType, testControlType,
                                                                        listType,
                                                                        channel, messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo, updateNode=True, lockNode=True)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'], 'VARIANT_CREATION')
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        rejectResponse = CreateMessage.reject(
            constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
            messageDetails['RESPONSE']['json']['entity']['id'])
        CreateMessage.assertResponse(rejectResponse, 200)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],
                                 approved='REJECTED',
                                 offer=True).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'EMAIL',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),

    ])
    def irisv2_message_create_reject_upload_email_particularDate_plain(self, campaignType, testControlType,
                                                                            listType,
                                                                            channel, messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo, updateNode=True, lockNode=True)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'], 'VARIANT_CREATION')
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        rejectResponse = CreateMessage.reject(
            constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
            messageDetails['RESPONSE']['json']['entity']['id'])
        CreateMessage.assertResponse(rejectResponse, 200)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],
                                 reject={'status':'CLOSED'},approved='REJECTED').check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'EMAIL',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': True, 'encryptUrl': False, 'skipRateLimit': True}),
    ])
    def irisv2_message_create_reject_upload_email_particularDate_plain_UsingTinyURL(self, campaignType,
                                                                                         testControlType,
                                                                                         listType, channel,
                                                                                         messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True,
                                              lockNode=True)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'], 'VARIANT_CREATION')
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        rejectResponse = CreateMessage.reject(
            constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
            messageDetails['RESPONSE']['json']['entity']['id'])
        CreateMessage.assertResponse(rejectResponse, 200)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],
                                 reject={'status':'CLOSED'},approved='REJECTED').check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'EMAIL',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': True, 'skipRateLimit': True}),
    ])
    def irisv2_message_create_reject_upload_email_particularDate_plain_UsingEncryptURL(self, campaignType,
                                                                                            testControlType,
                                                                                            listType, channel,
                                                                                            messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True,
                                              lockNode=True)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'], 'VARIANT_CREATION')
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        rejectResponse = CreateMessage.reject(
            constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
            messageDetails['RESPONSE']['json']['entity']['id'])
        CreateMessage.assertResponse(rejectResponse, 200)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],
                                 reject={'status':'CLOSED'},approved='REJECTED').check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'EMAIL',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': False}),
    ])
    def irisv2_message_create_reject_upload_email_particularDate_plain_UsingRateLimit(self, campaignType,
                                                                                           testControlType,
                                                                                           listType, channel,
                                                                                           messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True,
                                              lockNode=True)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'], 'VARIANT_CREATION')
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        rejectResponse = CreateMessage.reject(
            constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
            messageDetails['RESPONSE']['json']['entity']['id'])
        CreateMessage.assertResponse(rejectResponse, 200)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],
                                 reject={'status':'CLOSED'},approved='REJECTED').check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'EMAIL',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'CUSTOM', 'UPLOAD', 'EMAIL',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'SKIP', 'UPLOAD', 'EMAIL',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'ORG', 'UPLOAD', 'EMAIL',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'CUSTOM', 'UPLOAD', 'EMAIL',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'SKIP', 'UPLOAD', 'EMAIL',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def irisv2_message_create_reject_upload_email_particularDate_coupon(self, campaignType, testControlType,
                                                                             listType,
                                                                             channel, messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo, updateNode=True, lockNode=True)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'], 'VARIANT_CREATION')
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        rejectResponse = CreateMessage.reject(
            constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
            messageDetails['RESPONSE']['json']['entity']['id'])
        CreateMessage.assertResponse(rejectResponse, 200)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],
                                 reject={'status':'CLOSED'},approved='REJECTED',
                                 offer=True).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'EMAIL',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'CUSTOM', 'UPLOAD', 'EMAIL',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'SKIP', 'UPLOAD', 'EMAIL',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'ORG', 'UPLOAD', 'EMAIL',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'CUSTOM', 'UPLOAD', 'EMAIL',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'SKIP', 'UPLOAD', 'EMAIL',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def irisv2_message_create_reject_upload_email_particularDate_points(self, campaignType, testControlType,
                                                                             listType,
                                                                             channel, messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo, updateNode=True, lockNode=True)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'], 'VARIANT_CREATION')
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        rejectResponse = CreateMessage.reject(
            constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
            messageDetails['RESPONSE']['json']['entity']['id'])
        CreateMessage.assertResponse(rejectResponse, 200)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],
                                 reject={'status':'CLOSED'},approved='REJECTED',
                                 offer=True).check()

    @pytest.mark.parametrize('campaignType,testControlType,channel,messageInfo', [
        ('LIVE', 'ORG', 'EMAIL',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),

    ])
    def irisv2_message_Sanity_create_reject_filter_email_immediate_plain(self, campaignType, testControlType,
                                                                              channel, messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, 'LOYALTY', channel, messageInfo, updateNode=True, lockNode=True)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'], 'VARIANT_CREATION')
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        rejectResponse = CreateMessage.reject(
            constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
            messageDetails['RESPONSE']['json']['entity']['id'])
        CreateMessage.assertResponse(rejectResponse, 200)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],
                                 approved='REJECTED').check()

    @pytest.mark.parametrize('campaignType,testControlType,channel,messageInfo', [
        ('LIVE', 'ORG', 'EMAIL',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'CUSTOM', 'EMAIL',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'SKIP', 'EMAIL',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'ORG', 'EMAIL',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'CUSTOM', 'EMAIL',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'SKIP', 'EMAIL',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def irisv2_message_create_reject_filter_email_immediate_plain(self, campaignType, testControlType,
                                                                       channel, messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, 'LOYALTY', channel, messageInfo, updateNode=True, lockNode=True)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'], 'VARIANT_CREATION')
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        rejectResponse = CreateMessage.reject(
            constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
            messageDetails['RESPONSE']['json']['entity']['id'])
        CreateMessage.assertResponse(rejectResponse, 200)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'],
                                 messageDetails['PAYLOAD'], approved='REJECTED').check()

    @pytest.mark.parametrize('campaignType,testControlType,channel,messageInfo', [
        ('LIVE', 'ORG', 'EMAIL',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'CUSTOM', 'EMAIL',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'SKIP', 'EMAIL',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'ORG', 'EMAIL',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'CUSTOM', 'EMAIL',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'SKIP', 'EMAIL',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def irisv2_message_create_reject_filter_email_particularDate_plain(self, campaignType, testControlType,
                                                                            channel, messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, 'LOYALTY', channel, messageInfo, updateNode=True, lockNode=True)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'], 'VARIANT_CREATION')
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        rejectResponse = CreateMessage.reject(
            constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
            messageDetails['RESPONSE']['json']['entity']['id'])
        CreateMessage.assertResponse(rejectResponse, 200)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],
                                 reject={'status':'CLOSED'},approved='REJECTED').check()

    @pytest.mark.parametrize('campaignType,testControlType,channel,messageInfo', [
        ('LIVE', 'ORG', 'EMAIL',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'CUSTOM', 'EMAIL',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'SKIP', 'EMAIL',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'ORG', 'EMAIL',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'CUSTOM', 'EMAIL',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'SKIP', 'EMAIL',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def irisv2_message_create_reject_filter_email_immediate_coupon(self, campaignType, testControlType,
                                                                        channel, messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, 'LOYALTY', channel, messageInfo, updateNode=True, lockNode=True)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'], 'VARIANT_CREATION')
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        rejectResponse = CreateMessage.reject(
            constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
            messageDetails['RESPONSE']['json']['entity']['id'])
        CreateMessage.assertResponse(rejectResponse, 200)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],
                                 approved='REJECTED').check()

    @pytest.mark.parametrize('campaignType,testControlType,channel,messageInfo', [
        ('LIVE', 'ORG', 'EMAIL',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),

    ])
    def irisv2_message_create_reject_filter_email_immediate_coupon(self, campaignType, testControlType,
                                                                        channel, messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, 'LOYALTY', channel, messageInfo)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'], 'VARIANT_CREATION')
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        rejectResponse = CreateMessage.reject(
            constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
            messageDetails['RESPONSE']['json']['entity']['id'])
        CreateMessage.assertResponse(rejectResponse, 200)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],
                                 approved='REJECTED').check()

    @pytest.mark.parametrize('campaignType,testControlType,channel,messageInfo', [
        ('LIVE', 'ORG', 'EMAIL',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'CUSTOM', 'EMAIL',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'SKIP', 'EMAIL',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'ORG', 'EMAIL',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'CUSTOM', 'EMAIL',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'SKIP', 'EMAIL',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def irisv2_message_create_reject_filter_email_particularDate_coupon(self, campaignType, testControlType,
                                                                             channel, messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, 'LOYALTY', channel, messageInfo, updateNode=True, lockNode=True)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'], 'VARIANT_CREATION')
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        rejectResponse = CreateMessage.reject(
            constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
            messageDetails['RESPONSE']['json']['entity']['id'])
        CreateMessage.assertResponse(rejectResponse, 200)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],
                                 reject={'status':'CLOSED'},approved='REJECTED').check()

    @pytest.mark.parametrize('campaignType,testControlType,channel,messageInfo', [
        ('LIVE', 'ORG', 'EMAIL',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'CUSTOM', 'EMAIL',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'SKIP', 'EMAIL',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'ORG', 'EMAIL',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'CUSTOM', 'EMAIL',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'SKIP', 'EMAIL',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def irisv2_message_create_reject_filter_email_immediate_points(self, campaignType, testControlType,
                                                                        channel, messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, 'LOYALTY', channel, messageInfo, updateNode=True, lockNode=True)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'], 'VARIANT_CREATION')
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        rejectResponse = CreateMessage.reject(
            constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
            messageDetails['RESPONSE']['json']['entity']['id'])
        CreateMessage.assertResponse(rejectResponse, 200)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],
                                 approved='REJECTED', offer=True).check()

    @pytest.mark.parametrize('campaignType,testControlType,channel,messageInfo', [
        ('LIVE', 'ORG', 'EMAIL',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'CUSTOM', 'EMAIL',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'SKIP', 'EMAIL',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'ORG', 'EMAIL',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'CUSTOM', 'EMAIL',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'SKIP', 'EMAIL',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def irisv2_message_create_reject_filter_email_particularDate_points(self, campaignType, testControlType,
                                                                             channel, messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, 'LOYALTY', channel, messageInfo, updateNode=True, lockNode=True)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'], 'VARIANT_CREATION')
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        rejectResponse = CreateMessage.reject(
            constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
            messageDetails['RESPONSE']['json']['entity']['id'])
        CreateMessage.assertResponse(rejectResponse, 200)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],
                                 reject={'status':'CLOSED'},approved='REJECTED', offer=True).check()

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
    def irisv2_message_create_reject_filter_email_Recurring_plain(self, campaignType, testControlType,
                                                                       listType,
                                                                       channel, messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo, updateNode=True, lockNode=True)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'], 'VARIANT_CREATION')
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        rejectResponse = CreateMessage.reject(
            constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
            messageDetails['RESPONSE']['json']['entity']['id'])
        CreateMessage.assertResponse(rejectResponse, 200)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'],
                                 messageDetails['PAYLOAD'], reject={'status':'CLOSED'},approved='REJECTED').check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'LOYALTY', 'EMAIL',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': True, 'encryptUrl': False, 'skipRateLimit': True}),
    ])
    def irisv2_message_create_reject_filter_email_Recurring_plain_UsingTinyURL(self, campaignType,
                                                                                    testControlType,
                                                                                    listType, channel, messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True,
                                              lockNode=True)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'], 'VARIANT_CREATION')
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        rejectResponse = CreateMessage.reject(
            constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
            messageDetails['RESPONSE']['json']['entity']['id'])
        CreateMessage.assertResponse(rejectResponse, 200)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],
                                 reject={'status':'CLOSED'},approved='REJECTED').check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'LOYALTY', 'EMAIL',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': True, 'skipRateLimit': True}),
    ])
    def irisv2_message_create_reject_filter_email_Recurring_plain_UsingEncryptURL(self, campaignType,
                                                                                       testControlType,
                                                                                       listType, channel,
                                                                                       messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True,
                                              lockNode=True)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'], 'VARIANT_CREATION')
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        rejectResponse = CreateMessage.reject(
            constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
            messageDetails['RESPONSE']['json']['entity']['id'])
        CreateMessage.assertResponse(rejectResponse, 200)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],
                                 reject={'status':'CLOSED'},approved='REJECTED').check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'LOYALTY', 'EMAIL',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': False}),
    ])
    def irisv2_message_create_reject_filter_email_Recurring_plain_UsingRateLimit(self, campaignType,
                                                                                      testControlType,
                                                                                      listType, channel,
                                                                                      messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True,
                                              lockNode=True)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'], 'VARIANT_CREATION')
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        rejectResponse = CreateMessage.reject(
            constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
            messageDetails['RESPONSE']['json']['entity']['id'])
        CreateMessage.assertResponse(rejectResponse, 200)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],
                                 reject={'status':'CLOSED'},approved='REJECTED').check()

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
    def irisv2_message_create_reject_filter_email_Recurring_coupon(self, campaignType, testControlType,
                                                                        listType,
                                                                        channel, messageInfo, updateNode=True, lockNode=True):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo, updateNode=True, lockNode=True)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'], 'VARIANT_CREATION')
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        rejectResponse = CreateMessage.reject(
            constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
            messageDetails['RESPONSE']['json']['entity']['id'])
        CreateMessage.assertResponse(rejectResponse, 200)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],
                                 reject={'status':'CLOSED'},approved='REJECTED', offer=True).check()

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
    def irisv2_message_create_reject_filter_email_Recurring_points(self, campaignType, testControlType,
                                                                        listType,
                                                                        channel, messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo, updateNode=True, lockNode=True)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'], 'VARIANT_CREATION')
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        rejectResponse = CreateMessage.reject(
            constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
            messageDetails['RESPONSE']['json']['entity']['id'])
        CreateMessage.assertResponse(rejectResponse, 200)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],
                                 reject={'status':'CLOSED'},approved='REJECTED', offer=True).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
    ])
    def irisv2_message_create_reject_messagewith2hours_upload_mobile_particularDate_plain(self, campaignType,
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
                                              payload=payload, updateNode=True, lockNode=True)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'], 'VARIANT_CREATION')
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        rejectResponse = CreateMessage.reject(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                              messageDetails['RESPONSE']['json']['entity']['id'])
        CreateMessage.assertResponse(rejectResponse, 200)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],
                                 approved='REJECTED', reject={'status': 'CLOSED'}).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'LOYALTY', 'MOBILE',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
    ])
    def irisv2_message_create_reject_messagewith2hrs_filter_mobile_Recurring_plain(self, campaignType,
                                                                                        testControlType,
                                                                                        listType,
                                                                                        channel, messageInfo):
        self.listInfoFilter = CreateAudience.FilterList('LIVE', 'ORG')
        dateTime = Utils.getTime(hours=7, minutes=32, dateTimeFormat=True)
        payload = copy.deepcopy(constant.payload['createMessagev2'])
        payload['targetAudience'].update({'include': [self.listInfoFilter['ID']]})
        payload['schedule']['scheduleType'] = 'RECURRING'
        payload['schedule']['repeatType'] = 'DAILY'
        payload['schedule']['startDate'] = (time.time() * 1000) + 20000
        payload['schedule']['endDate'] = (time.time() * 1000) + 20000 + 1000
        payload['schedule']['repeatOn'] = [1]
        payload['schedule']['hour'] = int(dateTime[11:13])
        payload['schedule']['minute'] = int(dateTime[14:16])
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              payload=payload, updateNode=True, lockNode=True)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'], 'VARIANT_CREATION')
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        rejectResponse = CreateMessage.reject(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                              messageDetails['RESPONSE']['json']['entity']['id'])
        CreateMessage.assertResponse(rejectResponse, 200)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'],
                                 messageDetails['PAYLOAD'], reject={'status': 'CLOSED'}, approved='REJECTED').check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo,statusCode,errorCode,errorDescription', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}, 400, 3022,
         ['Message is already approved']),
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}, 400, 3022,
         ['Message is already approved']),
        ('LIVE', 'ORG', 'LOYALTY', 'MOBILE',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}, 400, 3022,
         ['Message is already approved'])
    ])
    def irisv2_rejectMessage_mobile_alreadyApproved(self, campaignType, testControlType,
                                                         listType,
                                                         channel, messageInfo, statusCode, errorCode, errorDescription):
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo)
        AuthorizeMessage.assertResponse(approveRespone, 200)
        rejectResponse = CreateMessage.reject(
            constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
            constant.config['node'][campaignType][testControlType]['LIST'][listType][channel]['MESSAGE'][
                messageInfo['scheduleType']['type']][messageInfo['offerType']]['RESPONSE']['json']['entity']['id'])
        CreateMessage.assertResponse(rejectResponse, 400, expectedErrorCode=[errorCode],
                                     expectedErrorMessage=errorDescription)

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo,editInfo,statusCode,errorCode,errorDescription', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True},
         {'endDate': Utils.getTime(minutes=1, milliSeconds=True)}, 400, 3036, 'Campaign expired')
    ])
    def irisv2_rejectMessage_mobile_afterCampaignExpires(self, campaignType, testControlType,
                                                              listType,
                                                              channel, messageInfo, editInfo, statusCode, errorCode,
                                                              errorDescription):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True, lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION')
        campaignInfo = constant.config['node'][campaignType][testControlType]['CAMPAIGN']
        editInfo = CreateCampaign.edit(campaignInfo, editInfo)
        time.sleep(60)
        rejectResponse = CreateMessage.reject(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                              messageDetails['RESPONSE']['json']['entity']['id'])
        CreateMessage.assertResponse(rejectResponse, 400, expectedErrorCode=[errorCode],
                                     expectedErrorMessage=errorDescription)

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo,statusCode,errorCode,errorDescription', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}, 400, 3023,
         'Message with message id {} does not exists')
    ])
    def irisv2_rejectMessage_mobile_with_campaignId_of_another_campaign(self, campaignType, testControlType,
                                                                             listType,
                                                                             channel, messageInfo, statusCode,
                                                                             errorCode, errorDescription):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True, lockNode=True)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION')
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        campaignInfo = CreateCampaign.create(campaignType, testControlType, updateNode=True)
        rejectResponse = CreateMessage.reject(
            campaignInfo['ID'], messageDetails['RESPONSE']['json']['entity']['id'])
        Assertion.constructAssertion(rejectResponse['statusCode'] == statusCode,
                                     'Actual Status Code :{} and Expected : {}'.format(
                                         rejectResponse['statusCode'], statusCode))
        Assertion.constructAssertion(rejectResponse['json']['errors'][0]['code'] == errorCode,
                                     'Actual Error Code :{} and Expected : {}'.format(
                                         rejectResponse['json']['errors'][0]['code'], errorCode))
        Assertion.constructAssertion(errorDescription.format(messageDetails['RESPONSE']['json']['entity']['id']) ==
                                     rejectResponse['json']['errors'][0]['message'],
                                     'Actual Error Code :{} and Expected : {}'.format(
                                         rejectResponse['json']['errors'][0]['message'], errorDescription))

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo,statusCode,errorCode,errorDescription', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}, 400, 3023,
         'Message with message id {} does not exists')
    ])
    def irisv2_rejectMessage_mobile_with_invalid_campaignId(self, campaignType, testControlType,
                                                                 listType,
                                                                 channel, messageInfo, statusCode, errorCode,
                                                                 errorDescription):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True, lockNode=True)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION')
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        rejectResponse = CreateMessage.reject(
            3453553, messageDetails['RESPONSE']['json']['entity']['id'])
        Assertion.constructAssertion(rejectResponse['statusCode'] == statusCode,
                                     'Actual Status Code :{} and Expected : {}'.format(
                                         rejectResponse['statusCode'], statusCode))
        Assertion.constructAssertion(rejectResponse['json']['errors'][0]['code'] == errorCode,
                                     'Actual Error Code :{} and Expected : {}'.format(
                                         rejectResponse['json']['errors'][0]['code'], errorCode))
        Assertion.constructAssertion(errorDescription.format(messageDetails['RESPONSE']['json']['entity']['id']) ==
                                     rejectResponse['json']['errors'][0]['message'],
                                     'Actual Error Code :{} and Expected : {}'.format(
                                         rejectResponse['json']['errors'][0]['message'], errorDescription))

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo,statusCode,errorCode,errorDescription', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}, 400, 3023,
         'Message with message id 1231342 does not exists')
    ])
    def irisv2_rejectMessage_mobile_with_invalid_messageId(self, campaignType, testControlType,
                                                                listType,
                                                                channel, messageInfo, statusCode, errorCode,
                                                                errorDescription):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True, lockNode=True)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION')
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        rejectResponse = CreateMessage.reject(
            constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'], '1231342')
        Assertion.constructAssertion(rejectResponse['statusCode'] == statusCode,
                                     'Actual Status Code :{} and Expected : {}'.format(
                                         rejectResponse['statusCode'], statusCode))
        Assertion.constructAssertion(rejectResponse['json']['errors'][0]['code'] == errorCode,
                                     'Actual Error Code :{} and Expected : {}'.format(
                                         rejectResponse['json']['errors'][0]['code'], errorCode))
        Assertion.constructAssertion(errorDescription ==
                                     rejectResponse['json']['errors'][0]['message'],
                                     'Actual Error Code :{} and Expected : {}'.format(
                                         rejectResponse['json']['errors'][0]['message'], errorDescription))

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo,statusCode,errorCode,errorDescription', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}, 400, 102,
         'Invalid request : CampaignId must be greater than or equal to 1')
    ])
    def irisv2_rejectMessage_mobile_with_negative_campaignId(self, campaignType, testControlType,
                                                                  listType,
                                                                  channel, messageInfo, statusCode, errorCode,
                                                                  errorDescription):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True, lockNode=True)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION')
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        rejectResponse = CreateMessage.reject(
            -1234, messageDetails['RESPONSE']['json']['entity']['id'])
        Assertion.constructAssertion(rejectResponse['statusCode'] == statusCode,
                                     'Actual Status Code :{} and Expected : {}'.format(
                                         rejectResponse['statusCode'], statusCode))
        Assertion.constructAssertion(rejectResponse['json']['errors'][0]['code'] == errorCode,
                                     'Actual Error Code :{} and Expected : {}'.format(
                                         rejectResponse['json']['errors'][0]['code'], errorCode))
        Assertion.constructAssertion(errorDescription.format(messageDetails['RESPONSE']['json']['entity']['id']) ==
                                     rejectResponse['json']['errors'][0]['message'],
                                     'Actual Error Code :{} and Expected : {}'.format(
                                         rejectResponse['json']['errors'][0]['message'], errorDescription))

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo,statusCode,errorCode,errorDescription', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}, 400, 3023,
         'Message with message id -1231342 does not exists')
    ])
    def irisv2_rejectMessage_mobile_with_negative_messageId(self, campaignType, testControlType,
                                                                 listType,
                                                                 channel, messageInfo, statusCode, errorCode,
                                                                 errorDescription):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True, lockNode=True)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION')
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        rejectResponse = CreateMessage.reject(
            constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'], '-1231342')
        Assertion.constructAssertion(rejectResponse['statusCode'] == statusCode,
                                     'Actual Status Code :{} and Expected : {}'.format(
                                         rejectResponse['statusCode'], statusCode))
        Assertion.constructAssertion(rejectResponse['json']['errors'][0]['code'] == errorCode,
                                     'Actual Error Code :{} and Expected : {}'.format(
                                         rejectResponse['json']['errors'][0]['code'], errorCode))
        Assertion.constructAssertion(errorDescription ==
                                     rejectResponse['json']['errors'][0]['message'],
                                     'Actual Error Code :{} and Expected : {}'.format(
                                         rejectResponse['json']['errors'][0]['message'], errorDescription))

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo,statusCode,errorCode,errorDescription', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}, 500, 101,
         'Generic error: HTTP 401 Unauthorized')
    ])
    def irisv2_rejectMessage_mobile_with_invalid_orgId(self, campaignType, testControlType,
                                                            listType,
                                                            channel, messageInfo, statusCode, errorCode,
                                                            errorDescription):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True, lockNode=True)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION')
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        actualOrgId = constant.config['orgId']
        try:
            constant.config['orgId'] = 999999
            rejectResponse = CreateMessage.reject(
                constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                messageDetails['RESPONSE']['json']['entity']['id'])
            Assertion.constructAssertion(rejectResponse['statusCode'] == statusCode,
                                         'Actual Status Code :{} and Expected : {}'.format(
                                             rejectResponse['statusCode'], statusCode))
            Assertion.constructAssertion(rejectResponse['json']['errors'][0]['code'] == errorCode,
                                         'Actual Error Code :{} and Expected : {}'.format(
                                             rejectResponse['json']['errors'][0]['code'], errorCode))
            Assertion.constructAssertion(errorDescription ==
                                         rejectResponse['json']['errors'][0]['message'],
                                         'Actual Error Code :{} and Expected : {}'.format(
                                             rejectResponse['json']['errors'][0]['message'], errorDescription))
        finally:
            constant.config['orgId'] = actualOrgId

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo,statusCode,errorCode,errorDescription', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}, 401,
         999999,
         'Invalid org id')
    ])
    def irisv2_rejectMessage_mobile_with_negative_orgId(self, campaignType, testControlType,
                                                             listType,
                                                             channel, messageInfo, statusCode, errorCode,
                                                             errorDescription):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True, lockNode=True)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION')
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        actualOrgId = constant.config['orgId']
        try:
            constant.config['orgId'] = -999999
            rejectResponse = CreateMessage.reject(
                constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                messageDetails['RESPONSE']['json']['entity']['id'])
            Assertion.constructAssertion(rejectResponse['statusCode'] == statusCode,
                                         'Actual Status Code :{} and Expected : {}'.format(
                                             rejectResponse['statusCode'], statusCode))
            Assertion.constructAssertion(rejectResponse['json']['errors'][0]['code'] == errorCode,
                                         'Actual Error Code :{} and Expected : {}'.format(
                                             rejectResponse['json']['errors'][0]['code'], errorCode))
            Assertion.constructAssertion(errorDescription ==
                                         rejectResponse['json']['errors'][0]['message'],
                                         'Actual Error Code :{} and Expected : {}'.format(
                                             rejectResponse['json']['errors'][0]['message'], errorDescription))
        finally:
            constant.config['orgId'] = actualOrgId

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo,statusCode,errorCode,errorDescription', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}, 401,
         999999,'Unauthorized')
    ])
    def irisv2_rejectMessage_mobile_with_wrongAuth(self, campaignType, testControlType,
                                                        listType,
                                                        channel, messageInfo, statusCode, errorCode,
                                                        errorDescription):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True, lockNode=True)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION')
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        previousUserName = None
        try:
            previousUserName = IrisHelper.updateUserName('WrongName')
            rejectResponse = CreateMessage.reject(
                constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                messageDetails['RESPONSE']['json']['entity']['id'])
            Assertion.constructAssertion(rejectResponse['statusCode'] == statusCode,
                                         'Actual Status Code :{} and Expected : {}'.format(
                                             rejectResponse['statusCode'], statusCode))
            Assertion.constructAssertion(rejectResponse['json']['errors'][0]['code'] == errorCode,
                                         'Actual Error Code :{} and Expected : {}'.format(
                                             rejectResponse['json']['errors'][0]['code'], errorCode))
            Assertion.constructAssertion(errorDescription ==
                                         rejectResponse['json']['errors'][0]['message'],
                                         'Actual Error Code :{} and Expected : {}'.format(
                                             rejectResponse['json']['errors'][0]['message'], errorDescription))
        finally:
            if previousUserName is not None: IrisHelper.updateUserName(previousUserName)

