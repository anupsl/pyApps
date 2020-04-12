import time

import pytest

from src.Constant.constant import constant
from src.modules.irisv2.campaigns.createCampaign import CreateCampaign
from src.modules.irisv2.message.createMessage import CreateMessage
from src.modules.irisv2.message.createMessageDbAssertion import CreateMessageDBAssertion
from src.utilities.logger import Logger


@pytest.mark.run(order=21)
class Test_CreateMessage_UploadList_Mobile():
    def setup_method(self, method):
        Logger.logMethodName(method.__name__)

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),

    ])
    def test_irisv2_message_Sanity_create_upload_mobile_immediate_plain(self, campaignType, testControlType, listType,
                                                                        channel, messageInfo):
        listInfo = CreateAudience.uploadList(campaignType, testControlType, schemaIdentifier=schemaIdentifier,numberOfUsers=1000000,
                                         campaignCheck=False, updateNode=True, lockNode=True)
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,listInfo=listInfo)

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
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
    def irisv2_message_create_upload_mobile_immediate_plain(self, campaignType, testControlType, listType,
                                                                        channel, messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,updateNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD']).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LAPSED', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LAPSED', 'CUSTOM', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LAPSED', 'SKIP', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def irisv2_message_create_upload_mobile_immediate_plain_lapsed(self, campaignType, testControlType, listType,
                                                                        channel, messageInfo):
        CreateCampaign.create(campaignType, testControlType, endDate=int(
            time.time() * 1000) + 5 * 60 * 1000)  # Extending Campaign for 5 Mins to set message
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD']).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': True, 'encryptUrl': False, 'skipRateLimit': True}),
    ])
    def irisv2_message_create_upload_mobile_immediate_plain_additionalProperties_UsingTinyURL(self, campaignType,
                                                                                                   testControlType,
                                                                                                   listType, channel,
                                                                                                   messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD']).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': True, 'skipRateLimit': True}),
    ])
    def irisv2_message_create_upload_mobile_immediate_plain_additionalProperties_UsingEncryptURL(self,
                                                                                                      campaignType,
                                                                                                      testControlType,
                                                                                                      listType, channel,
                                                                                                      messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD']).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': False}),
    ])
    def irisv2_message_create_upload_mobile_immediate_plain_additionalProperties_UsingRateLimit(self, campaignType,
                                                                                                     testControlType,
                                                                                                     listType, channel,
                                                                                                     messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD']).check()

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
    def irisv2_message_create_upload_mobile_immediate_coupon(self, campaignType, testControlType, listType,
                                                                  channel, messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],
                                 offer=True).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LAPSED', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LAPSED', 'CUSTOM', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LAPSED', 'SKIP', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def irisv2_message_create_upload_mobile_immediate_coupon_lapsed(self, campaignType, testControlType, listType,
                                                                         channel, messageInfo):
        CreateCampaign.create(campaignType, testControlType, endDate=int(
            time.time() * 1000) + 5 * 60 * 1000)
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD']).check()

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
    def irisv2_message_create_upload_mobile_immediate_points(self, campaignType, testControlType, listType,
                                                                 channel, messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],
                                 offer=True).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LAPSED', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LAPSED', 'CUSTOM', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LAPSED', 'SKIP', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def irisv2_message_create_upload_mobile_immediate_points_lapsed(self, campaignType, testControlType, listType,
                                                                       channel, messageInfo):
        CreateCampaign.create(campaignType, testControlType, endDate=int(
            time.time() * 1000) + 5 * 60 * 1000)
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD']).check()


    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'CUSTOM', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'SKIP', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'CUSTOM', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'SKIP', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def irisv2_message_create_upload_mobile_particularDate_plain(self, campaignType, testControlType,
                                                                             listType,
                                                                             channel, messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD']).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LAPSED', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LAPSED', 'CUSTOM', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LAPSED', 'SKIP', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def irisv2_message_create_upload_mobile_particularDate_plain_lapsed(self, campaignType, testControlType,
                                                                             listType,
                                                                             channel, messageInfo):
        CreateCampaign.create(campaignType, testControlType, endDate=int(
            time.time() * 1000) + 5 * 60 * 1000)
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD']).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': True, 'encryptUrl': False, 'skipRateLimit': True}),
    ])
    def irisv2_message_create_upload_mobile_particularDate_plain_UsingTinyURL(self, campaignType, testControlType,
                                                                                   listType, channel, messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD']).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': True, 'skipRateLimit': True}),
    ])
    def irisv2_message_create_upload_mobile_particularDate_plain_UsingEncryptURL(self, campaignType,
                                                                                      testControlType,
                                                                                      listType, channel, messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD']).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': False}),
    ])
    def irisv2_message_create_upload_mobile_particularDate_plain_UsingRateLimit(self, campaignType,
                                                                                     testControlType,
                                                                                     listType, channel, messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD']).check()

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
    def irisv2_message_create_upload_mobile_particularDate_coupon(self, campaignType, testControlType,
                                                                           listType,
                                                                           channel, messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],
                                 offer=True).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LAPSED', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LAPSED', 'CUSTOM', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LAPSED', 'SKIP', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def irisv2_message_create_upload_mobile_particularDate_coupon_lapsed(self, campaignType, testControlType,
                                                                              listType,
                                                                              channel, messageInfo):
        CreateCampaign.create(campaignType, testControlType, endDate=int(
            time.time() * 1000) + 5 * 60 * 1000)
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD']).check()

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
    def irisv2_message_create_upload_mobile_particularDate_points(self, campaignType, testControlType, listType,
                                                                      channel, messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],
                                 offer=True).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LAPSED', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LAPSED', 'CUSTOM', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LAPSED', 'SKIP', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def irisv2_message_create_upload_mobile_particularDate_points_lapsed(self, campaignType, testControlType,
                                                                             listType,
                                                                             channel, messageInfo):
        CreateCampaign.create(campaignType, testControlType, endDate=int(
            time.time() * 1000) + 5 * 60 * 1000)
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD']).check()












