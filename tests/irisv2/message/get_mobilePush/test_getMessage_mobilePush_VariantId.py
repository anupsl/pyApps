import time

import pytest

from src.Constant.constant import constant
from src.dbCalls.messageInfo import message_calls
from src.modules.irisv2.campaigns.createCampaign import CreateCampaign
from src.modules.irisv2.helper.irisHelper import IrisHelper
from src.modules.irisv2.message.createMessage import CreateMessage
from src.modules.irisv2.message.createMessageDbAssertion import CreateMessageDBAssertion
from src.modules.irisv2.message.getMessage import GetMessage
from src.modules.irisv2.message.variantDbAssertion import VariantDBAssertion
from src.utilities.assertion import Assertion
from src.utilities.logger import Logger


@pytest.mark.run(order=54)
class Test_GetMessage_MobilePush_VariantById():
    def setup_class(self):
        self.actualOrgId = IrisHelper.updateOrgId(constant.config['mobilepush']['orgId'])
        self.actualOrgName = IrisHelper.updateOrgName(constant.config['mobilepush']['orgName'])

    def teardown_class(self):
        IrisHelper.updateOrgId(self.actualOrgId)
        IrisHelper.updateOrgName(self.actualOrgName)

    def setup_method(self, method):
        Logger.logMethodName(method.__name__)

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT',
                                                                                           "android": {
                                                                                               "contentType": "TEXT",
                                                                                               "secondary_cta": {
                                                                                                   "enable": False,
                                                                                                   "value": None},
                                                                                               "primary_cta": {
                                                                                                   "enable": False,
                                                                                                   "value": None},
                                                                                               "custom": False},
                                                                                           "ios": {
                                                                                               "contentType": "TEXT",
                                                                                               "secondary_cta": {
                                                                                                   "enable": False,
                                                                                                   "value": None},
                                                                                               "primary_cta": {
                                                                                                   "enable": False,
                                                                                                   "value": None},
                                                                                               "custom": False}},
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
    ])
    def test_irisv2_getMessageVariant_create_mobilepush_immediate_plain(self, campaignType, testControlType,
                                                                        listType,
                                                                        channel, messageInfo):
        CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo)

        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        messageId = constant.config['node'][campaignType][testControlType]['LIST'][listType][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['RESPONSE']['json']['entity']['id']

        for eachType in ['MESSAGE_TARGET_AUDIENCE', 'VARIANT_CREATION']:
            status = message_calls().waitForJobDetailsStatusToClose(messageId, eachType, maxNumberOfAttempts=20)

        if status:
            getMessageResponse = GetMessage.getMessageVariantById(campaignId,
                                                                  message_calls().getVariantIdByMessageId(messageId))
            GetMessage.assertResponse(getMessageResponse, 200)
            VariantDBAssertion(campaignId, messageId, [getMessageResponse['json']['entity']]).check()
        else:
            Assertion.constructAssertion(False, 'Variant_Creation is Not Closed in Specified time')

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT',
                                                                                           "android": {
                                                                                               "contentType": "TEXT",
                                                                                               "secondary_cta": {
                                                                                                   "enable": False,
                                                                                                   "value": None},
                                                                                               "primary_cta": {
                                                                                                   "enable": False,
                                                                                                   "value": None},
                                                                                               "custom": False},
                                                                                           "ios": {
                                                                                               "contentType": "TEXT",
                                                                                               "secondary_cta": {
                                                                                                   "enable": False,
                                                                                                   "value": None},
                                                                                               "primary_cta": {
                                                                                                   "enable": False,
                                                                                                   "value": None},
                                                                                               "custom": False}},
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),

    ])
    def test_irisv2_getMessageVariant_Sanity_create_mobilepush_immediate_plain(self, campaignType, testControlType,
                                                                               listType,
                                                                               channel, messageInfo):
        CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo)

        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        messageId = constant.config['node'][campaignType][testControlType]['LIST'][listType][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['RESPONSE']['json']['entity']['id']

        for eachType in ['MESSAGE_TARGET_AUDIENCE', 'VARIANT_CREATION']:
            status = message_calls().waitForJobDetailsStatusToClose(messageId, eachType, maxNumberOfAttempts=20)

        if status:
            getMessageResponse = GetMessage.getMessageVariantById(campaignId,
                                                                  message_calls().getVariantIdByMessageId(messageId))
            GetMessage.assertResponse(getMessageResponse, 200)
            VariantDBAssertion(campaignId, messageId, [getMessageResponse['json']['entity']]).check()
        else:
            Assertion.constructAssertion(False, 'Variant_Creation is Not Closed in Specified time')

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LAPSED', 'SKIP', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT',
                                                                                           "android": {
                                                                                               "contentType": "TEXT",
                                                                                               "secondary_cta": {
                                                                                                   "enable": False,
                                                                                                   "value": None},
                                                                                               "primary_cta": {
                                                                                                   "enable": False,
                                                                                                   "value": None},
                                                                                               "custom": False},
                                                                                           "ios": {
                                                                                               "contentType": "TEXT",
                                                                                               "secondary_cta": {
                                                                                                   "enable": False,
                                                                                                   "value": None},
                                                                                               "primary_cta": {
                                                                                                   "enable": False,
                                                                                                   "value": None},
                                                                                               "custom": False}},
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def test_irisv2_getMessageVariant_create_mobilepush_immediate_plain_lapsed(self, campaignType, testControlType,
                                                                               listType,
                                                                               channel, messageInfo):
        CreateCampaign.create(campaignType, testControlType, endDate=int(
            time.time() * 1000) + 5 * 60 * 1000)  # Extending Campaign for 5 Mins to set message
        CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo)
        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        messageId = constant.config['node'][campaignType][testControlType]['LIST'][listType][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['RESPONSE']['json']['entity']['id']

        for eachType in ['MESSAGE_TARGET_AUDIENCE', 'VARIANT_CREATION']:
            status = message_calls().waitForJobDetailsStatusToClose(messageId, eachType, maxNumberOfAttempts=20)

        if status:
            getMessageResponse = GetMessage.getMessageVariantById(campaignId,
                                                                  message_calls().getVariantIdByMessageId(messageId))
            GetMessage.assertResponse(getMessageResponse, 200)
            VariantDBAssertion(campaignId, messageId, [getMessageResponse['json']['entity']]).check()
        else:
            Assertion.constructAssertion(False, 'Variant_Creation is Not Closed in Specified time')

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT',
                                                                                           "android": {
                                                                                               "contentType": "TEXT",
                                                                                               "secondary_cta": {
                                                                                                   "enable": False,
                                                                                                   "value": None},
                                                                                               "primary_cta": {
                                                                                                   "enable": False,
                                                                                                   "value": None},
                                                                                               "custom": False},
                                                                                           "ios": {
                                                                                               "contentType": "TEXT",
                                                                                               "secondary_cta": {
                                                                                                   "enable": False,
                                                                                                   "value": None},
                                                                                               "primary_cta": {
                                                                                                   "enable": False,
                                                                                                   "value": None},
                                                                                               "custom": False}},
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': True, 'encryptUrl': False, 'skipRateLimit': True}),
    ])
    def test_irisv2_getMessageVariant_create_mobilepush_immediate_plain_additionalProperties_UsingTinyURL(self,
                                                                                                          campaignType,
                                                                                                          testControlType,
                                                                                                          listType,
                                                                                                          channel,
                                                                                                          messageInfo):
        messageInfo = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                           updateNode=True,
                                           lockNode=True)
        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        messageId = messageInfo['RESPONSE']['json']['entity']['id']

        getMessageResponse = GetMessage.getMessageVariantById(campaignId,
                                                              message_calls().getVariantIdByMessageId(messageId))
        GetMessage.assertResponse(getMessageResponse, 200)
        VariantDBAssertion(campaignId, messageId, [getMessageResponse['json']['entity']]).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'CUSTOM', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT',
                                                                                            "android": {
                                                                                                "contentType": "TEXT",
                                                                                                "secondary_cta": {
                                                                                                    "enable": False,
                                                                                                    "value": None},
                                                                                                "primary_cta": {
                                                                                                    "enable": False,
                                                                                                    "value": None},
                                                                                                "custom": False},
                                                                                            "ios": {
                                                                                                "contentType": "TEXT",
                                                                                                "secondary_cta": {
                                                                                                    "enable": False,
                                                                                                    "value": None},
                                                                                                "primary_cta": {
                                                                                                    "enable": False,
                                                                                                    "value": None},
                                                                                                "custom": False}},
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'SKIP', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT',
                                                                                            "android": {
                                                                                                "contentType": "TEXT",
                                                                                                "secondary_cta": {
                                                                                                    "enable": False,
                                                                                                    "value": None},
                                                                                                "primary_cta": {
                                                                                                    "enable": False,
                                                                                                    "value": None},
                                                                                                "custom": False},
                                                                                            "ios": {
                                                                                                "contentType": "TEXT",
                                                                                                "secondary_cta": {
                                                                                                    "enable": False,
                                                                                                    "value": None},
                                                                                                "primary_cta": {
                                                                                                    "enable": False,
                                                                                                    "value": None},
                                                                                                "custom": False}},
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def test_irisv2_getMessageVariant_create_mobilepush_immediate_coupon(self, campaignType, testControlType, listType,
                                                                         channel, messageInfo):
        CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo)
        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        messageId = constant.config['node'][campaignType][testControlType]['LIST'][listType][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['RESPONSE']['json']['entity']['id']

        getMessageResponse = GetMessage.getMessageVariantById(campaignId,
                                                              message_calls().getVariantIdByMessageId(messageId))
        GetMessage.assertResponse(getMessageResponse, 200)
        VariantDBAssertion(campaignId, messageId, [getMessageResponse['json']['entity']]).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LAPSED', 'CUSTOM', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT',
                                                                                            "android": {
                                                                                                "contentType": "TEXT",
                                                                                                "secondary_cta": {
                                                                                                    "enable": False,
                                                                                                    "value": None},
                                                                                                "primary_cta": {
                                                                                                    "enable": False,
                                                                                                    "value": None},
                                                                                                "custom": False},
                                                                                            "ios": {
                                                                                                "contentType": "TEXT",
                                                                                                "secondary_cta": {
                                                                                                    "enable": False,
                                                                                                    "value": None},
                                                                                                "primary_cta": {
                                                                                                    "enable": False,
                                                                                                    "value": None},
                                                                                                "custom": False}},
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
    ])
    def test_irisv2_getMessageVariant_create_mobilepush_immediate_coupon_lapsed(self, campaignType, testControlType,
                                                                                listType,
                                                                                channel, messageInfo):
        CreateCampaign.create(campaignType, testControlType, endDate=int(
            time.time() * 1000) + 5 * 60 * 1000)
        CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo)
        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        messageId = constant.config['node'][campaignType][testControlType]['LIST'][listType][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['RESPONSE']['json']['entity']['id']

        getMessageResponse = GetMessage.getMessageVariantById(campaignId,
                                                              message_calls().getVariantIdByMessageId(messageId))
        GetMessage.assertResponse(getMessageResponse, 200)
        VariantDBAssertion(campaignId, messageId, [getMessageResponse['json']['entity']]).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('UPCOMING', 'ORG', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT',
                                                                                                "android": {
                                                                                                    "contentType": "TEXT",
                                                                                                    "secondary_cta": {
                                                                                                        "enable": False,
                                                                                                        "value": None},
                                                                                                    "primary_cta": {
                                                                                                        "enable": False,
                                                                                                        "value": None},
                                                                                                    "custom": False},
                                                                                                "ios": {
                                                                                                    "contentType": "TEXT",
                                                                                                    "secondary_cta": {
                                                                                                        "enable": False,
                                                                                                        "value": None},
                                                                                                    "primary_cta": {
                                                                                                        "enable": False,
                                                                                                        "value": None},
                                                                                                    "custom": False}},
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def test_irisv2_getMessageVariant_create_mobilepush_particularDate_plain(self, campaignType, testControlType,
                                                                             listType,
                                                                             channel, messageInfo):
        CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo)
        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        messageId = constant.config['node'][campaignType][testControlType]['LIST'][listType][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['RESPONSE']['json']['entity']['id']

        for eachType in ['MESSAGE_TARGET_AUDIENCE', 'VARIANT_CREATION']:
            status = message_calls().waitForJobDetailsStatusToClose(messageId, eachType, maxNumberOfAttempts=20)

        if status:
            getMessageResponse = GetMessage.getMessageById(campaignId, messageId, [('includeVariant', 'true')])
            GetMessage.assertResponse(getMessageResponse, 200)
            CreateMessageDBAssertion(campaignId, messageId, getMessageResponse['json']['entity']).check()
            VariantDBAssertion(campaignId, messageId,
                               getMessageResponse['json']['entity']['messageVariantList']).check()
        else:
            Assertion.constructAssertion(False, 'Variant_Creation is Not Closed in Specified time')

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LAPSED', 'SKIP', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT',
                                                                                                "android": {
                                                                                                    "contentType": "TEXT",
                                                                                                    "secondary_cta": {
                                                                                                        "enable": False,
                                                                                                        "value": None},
                                                                                                    "primary_cta": {
                                                                                                        "enable": False,
                                                                                                        "value": None},
                                                                                                    "custom": False},
                                                                                                "ios": {
                                                                                                    "contentType": "TEXT",
                                                                                                    "secondary_cta": {
                                                                                                        "enable": False,
                                                                                                        "value": None},
                                                                                                    "primary_cta": {
                                                                                                        "enable": False,
                                                                                                        "value": None},
                                                                                                    "custom": False}},
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def test_irisv2_getMessageVariant_create_mobilepush_particularDate_plain_lapsed(self, campaignType, testControlType,
                                                                                    listType,
                                                                                    channel, messageInfo):
        CreateCampaign.create(campaignType, testControlType, endDate=int(
            time.time() * 1000) + 5 * 60 * 1000)
        CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo)
        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        messageId = constant.config['node'][campaignType][testControlType]['LIST'][listType][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['RESPONSE']['json']['entity']['id']

        for eachType in ['MESSAGE_TARGET_AUDIENCE', 'VARIANT_CREATION']:
            status = message_calls().waitForJobDetailsStatusToClose(messageId, eachType, maxNumberOfAttempts=20)

        if status:
            getMessageResponse = GetMessage.getMessageById(campaignId, messageId, [('includeVariant', 'true')])
            GetMessage.assertResponse(getMessageResponse, 200)
            CreateMessageDBAssertion(campaignId, messageId, getMessageResponse['json']['entity']).check()
            VariantDBAssertion(campaignId, messageId,
                               getMessageResponse['json']['entity']['messageVariantList']).check()
        else:
            Assertion.constructAssertion(False, 'Variant_Creation is Not Closed in Specified time')

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT',
                                                                                                "android": {
                                                                                                    "contentType": "TEXT",
                                                                                                    "secondary_cta": {
                                                                                                        "enable": False,
                                                                                                        "value": None},
                                                                                                    "primary_cta": {
                                                                                                        "enable": False,
                                                                                                        "value": None},
                                                                                                    "custom": False},
                                                                                                "ios": {
                                                                                                    "contentType": "TEXT",
                                                                                                    "secondary_cta": {
                                                                                                        "enable": False,
                                                                                                        "value": None},
                                                                                                    "primary_cta": {
                                                                                                        "enable": False,
                                                                                                        "value": None},
                                                                                                    "custom": False}},
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': True, 'skipRateLimit': True}),
    ])
    def test_irisv2_getMessageVariant_create_mobilepush_particularDate_plain_UsingEncryptURL(self, campaignType,
                                                                                             testControlType,
                                                                                             listType, channel,
                                                                                             messageInfo):
        messageInfo = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                           updateNode=True,
                                           lockNode=True)
        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        messageId = messageInfo['RESPONSE']['json']['entity']['id']

        for eachType in ['MESSAGE_TARGET_AUDIENCE', 'VARIANT_CREATION']:
            status = message_calls().waitForJobDetailsStatusToClose(messageId, eachType, maxNumberOfAttempts=20)

        if status:
            getMessageResponse = GetMessage.getMessageById(campaignId, messageId, [('includeVariant', 'true')])
            GetMessage.assertResponse(getMessageResponse, 200)
            CreateMessageDBAssertion(campaignId, messageId, getMessageResponse['json']['entity']).check()
            VariantDBAssertion(campaignId, messageId,
                               getMessageResponse['json']['entity']['messageVariantList']).check()
        else:
            Assertion.constructAssertion(False, 'Variant_Creation is Not Closed in Specified time')

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'SKIP', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT',
                                                                                                 "android": {
                                                                                                     "contentType": "TEXT",
                                                                                                     "secondary_cta": {
                                                                                                         "enable": False,
                                                                                                         "value": None},
                                                                                                     "primary_cta": {
                                                                                                         "enable": False,
                                                                                                         "value": None},
                                                                                                     "custom": False},
                                                                                                 "ios": {
                                                                                                     "contentType": "TEXT",
                                                                                                     "secondary_cta": {
                                                                                                         "enable": False,
                                                                                                         "value": None},
                                                                                                     "primary_cta": {
                                                                                                         "enable": False,
                                                                                                         "value": None},
                                                                                                     "custom": False}},
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'CUSTOM', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT',
                                                                                                 "android": {
                                                                                                     "contentType": "TEXT",
                                                                                                     "secondary_cta": {
                                                                                                         "enable": False,
                                                                                                         "value": None},
                                                                                                     "primary_cta": {
                                                                                                         "enable": False,
                                                                                                         "value": None},
                                                                                                     "custom": False},
                                                                                                 "ios": {
                                                                                                     "contentType": "TEXT",
                                                                                                     "secondary_cta": {
                                                                                                         "enable": False,
                                                                                                         "value": None},
                                                                                                     "primary_cta": {
                                                                                                         "enable": False,
                                                                                                         "value": None},
                                                                                                     "custom": False}},
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
    ])
    def test_irisv2_getMessageVariant_create_mobilepush_particularDate_coupon(self, campaignType, testControlType,
                                                                              listType,
                                                                              channel, messageInfo):
        CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo)
        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        messageId = constant.config['node'][campaignType][testControlType]['LIST'][listType][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['RESPONSE']['json']['entity']['id']

        for eachType in ['MESSAGE_TARGET_AUDIENCE', 'VARIANT_CREATION']:
            status = message_calls().waitForJobDetailsStatusToClose(messageId, eachType, maxNumberOfAttempts=20)

        if status:
            getMessageResponse = GetMessage.getMessageById(campaignId, messageId, [('includeVariant', 'true')])
            GetMessage.assertResponse(getMessageResponse, 200)
            CreateMessageDBAssertion(campaignId, messageId, getMessageResponse['json']['entity']).check()
            VariantDBAssertion(campaignId, messageId,
                               getMessageResponse['json']['entity']['messageVariantList']).check()
        else:
            Assertion.constructAssertion(False, 'Variant_Creation is Not Closed in Specified time')

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LAPSED', 'SKIP', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT',
                                                                                                 "android": {
                                                                                                     "contentType": "TEXT",
                                                                                                     "secondary_cta": {
                                                                                                         "enable": False,
                                                                                                         "value": None},
                                                                                                     "primary_cta": {
                                                                                                         "enable": False,
                                                                                                         "value": None},
                                                                                                     "custom": False},
                                                                                                 "ios": {
                                                                                                     "contentType": "TEXT",
                                                                                                     "secondary_cta": {
                                                                                                         "enable": False,
                                                                                                         "value": None},
                                                                                                     "primary_cta": {
                                                                                                         "enable": False,
                                                                                                         "value": None},
                                                                                                     "custom": False}},
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def test_irisv2_getMessageVariant_create_mobilepush_particularDate_coupon_lapsed(self, campaignType,
                                                                                     testControlType,
                                                                                     listType,
                                                                                     channel, messageInfo):
        CreateCampaign.create(campaignType, testControlType, endDate=int(
            time.time() * 1000) + 5 * 60 * 1000)
        CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo)
        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        messageId = constant.config['node'][campaignType][testControlType]['LIST'][listType][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['RESPONSE']['json']['entity']['id']

        for eachType in ['MESSAGE_TARGET_AUDIENCE', 'VARIANT_CREATION']:
            status = message_calls().waitForJobDetailsStatusToClose(messageId, eachType, maxNumberOfAttempts=20)

        if status:
            getMessageResponse = GetMessage.getMessageById(campaignId, messageId, [('includeVariant', 'true')])
            GetMessage.assertResponse(getMessageResponse, 200)
            CreateMessageDBAssertion(campaignId, messageId, getMessageResponse['json']['entity']).check()
            VariantDBAssertion(campaignId, messageId,
                               getMessageResponse['json']['entity']['messageVariantList']).check()
        else:
            Assertion.constructAssertion(False, 'Variant_Creation is Not Closed in Specified time')

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT',
                                                                                                 "android": {
                                                                                                     "contentType": "TEXT",
                                                                                                     "secondary_cta": {
                                                                                                         "enable": False,
                                                                                                         "value": None},
                                                                                                     "primary_cta": {
                                                                                                         "enable": False,
                                                                                                         "value": None},
                                                                                                     "custom": False},
                                                                                                 "ios": {
                                                                                                     "contentType": "TEXT",
                                                                                                     "secondary_cta": {
                                                                                                         "enable": False,
                                                                                                         "value": None},
                                                                                                     "primary_cta": {
                                                                                                         "enable": False,
                                                                                                         "value": None},
                                                                                                     "custom": False}},
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'CUSTOM', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT',
                                                                                                 "android": {
                                                                                                     "contentType": "TEXT",
                                                                                                     "secondary_cta": {
                                                                                                         "enable": False,
                                                                                                         "value": None},
                                                                                                     "primary_cta": {
                                                                                                         "enable": False,
                                                                                                         "value": None},
                                                                                                     "custom": False},
                                                                                                 "ios": {
                                                                                                     "contentType": "TEXT",
                                                                                                     "secondary_cta": {
                                                                                                         "enable": False,
                                                                                                         "value": None},
                                                                                                     "primary_cta": {
                                                                                                         "enable": False,
                                                                                                         "value": None},
                                                                                                     "custom": False}},
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def test_irisv2_getMessageVariant_create_mobilepush_particularDate_points(self, campaignType, testControlType,
                                                                              listType,
                                                                              channel, messageInfo):
        CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo)

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LAPSED', 'SKIP', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT',
                                                                                                 "android": {
                                                                                                     "contentType": "TEXT",
                                                                                                     "secondary_cta": {
                                                                                                         "enable": False,
                                                                                                         "value": None},
                                                                                                     "primary_cta": {
                                                                                                         "enable": False,
                                                                                                         "value": None},
                                                                                                     "custom": False},
                                                                                                 "ios": {
                                                                                                     "contentType": "TEXT",
                                                                                                     "secondary_cta": {
                                                                                                         "enable": False,
                                                                                                         "value": None},
                                                                                                     "primary_cta": {
                                                                                                         "enable": False,
                                                                                                         "value": None},
                                                                                                     "custom": False}},
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def test_irisv2_getMessageVariant_create_mobilepush_particularDate_coupon_lapsed(self, campaignType,
                                                                                     testControlType,
                                                                                     listType,
                                                                                     channel, messageInfo):
        CreateCampaign.create(campaignType, testControlType, endDate=int(
            time.time() * 1000) + 5 * 60 * 1000)
        CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo)
        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        messageId = constant.config['node'][campaignType][testControlType]['LIST'][listType][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['RESPONSE']['json']['entity']['id']

        for eachType in ['MESSAGE_TARGET_AUDIENCE', 'VARIANT_CREATION']:
            status = message_calls().waitForJobDetailsStatusToClose(messageId, eachType, maxNumberOfAttempts=20)

        if status:
            getMessageResponse = GetMessage.getMessageById(campaignId, messageId, [('includeVariant', 'true')])
            GetMessage.assertResponse(getMessageResponse, 200)
            CreateMessageDBAssertion(campaignId, messageId, getMessageResponse['json']['entity']).check()
            VariantDBAssertion(campaignId, messageId,
                               getMessageResponse['json']['entity']['messageVariantList']).check()
        else:
            Assertion.constructAssertion(False, 'Variant_Creation is Not Closed in Specified time')

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT',
                                                                                            "android": {
                                                                                                "contentType": "TEXT",
                                                                                                "secondary_cta": {
                                                                                                    "enable": False,
                                                                                                    "value": None},
                                                                                                "primary_cta": {
                                                                                                    "enable": False,
                                                                                                    "value": None},
                                                                                                "custom": False},
                                                                                            "ios": {
                                                                                                "contentType": "TEXT",
                                                                                                "secondary_cta": {
                                                                                                    "enable": False,
                                                                                                    "value": None},
                                                                                                "primary_cta": {
                                                                                                    "enable": False,
                                                                                                    "value": None},
                                                                                                "custom": False}},
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
    ])
    def test_irisv2_getMessageVariant_create_mobilepush_Recurring_coupon(self, campaignType, testControlType, listType,
                                                                         channel, messageInfo):
        CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo)
        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        messageId = constant.config['node'][campaignType][testControlType]['LIST'][listType][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['RESPONSE']['json']['entity']['id']

        for eachType in ['MESSAGE_TARGET_AUDIENCE', 'VARIANT_CREATION']:
            status = message_calls().waitForJobDetailsStatusToClose(messageId, eachType, maxNumberOfAttempts=20)

        if status:
            getMessageResponse = GetMessage.getMessageById(campaignId, messageId, [('includeVariant', 'true')])
            GetMessage.assertResponse(getMessageResponse, 200)
            CreateMessageDBAssertion(campaignId, messageId, getMessageResponse['json']['entity']).check()
            VariantDBAssertion(campaignId, messageId,
                               getMessageResponse['json']['entity']['messageVariantList']).check()
        else:
            Assertion.constructAssertion(False, 'Variant_Creation is Not Closed in Specified time')
