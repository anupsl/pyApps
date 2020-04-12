import time

import pytest

from src.Constant.constant import constant
from src.modules.irisv2.campaigns.createCampaign import CreateCampaign
from src.modules.irisv2.message.createMessage import CreateMessage
from src.modules.irisv2.message.createMessageDbAssertion import CreateMessageDBAssertion
from src.modules.irisv2.message.getMessage import GetMessage
from src.dbCalls.messageInfo import message_calls
from src.modules.irisv2.message.variantDbAssertion import VariantDBAssertion
from src.utilities.assertion import Assertion
from src.utilities.logger import Logger


@pytest.mark.run(order=46)
class Test_GetMessage_VariantById():
    def setup_method(self, method):
        Logger.logMethodName(method.__name__)

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),

    ])
    def test_irisv2_getMessageVariant_Sanity_create_upload_mobile_immediate_plain(self, campaignType, testControlType,
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
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'SKIP', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def test_irisv2_getMessageVariant_create_upload_mobile_immediate_plain(self, campaignType, testControlType,
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
        ('LAPSED', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
    ])
    def test_irisv2_getMessageVariant_create_upload_mobile_immediate_plain_lapsed(self, campaignType, testControlType,
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
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': True, 'encryptUrl': True, 'skipRateLimit': True}),
    ])
    def test_irisv2_getMessageVariant_create_upload_mobile_immediate_plain_additionalProperties_UsingRateLimit(self,
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
        ('UPCOMING', 'CUSTOM', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'SKIP', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def test_irisv2_getMessageVariant_create_upload_mobile_immediate_coupon(self, campaignType, testControlType, listType,
                                                                     channel, messageInfo):
        CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo)
        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        messageId = constant.config['node'][campaignType][testControlType]['LIST'][listType][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['RESPONSE']['json']['entity']['id']

        getMessageResponse = GetMessage.getMessageVariantById(campaignId, message_calls().getVariantIdByMessageId(messageId))
        GetMessage.assertResponse(getMessageResponse, 200)
        VariantDBAssertion(campaignId, messageId,[getMessageResponse['json']['entity']]).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('UPCOMING', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'SKIP', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def test_irisv2_getMessageVariant_create_upload_mobile_immediate_points(self, campaignType, testControlType, listType,
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
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'CUSTOM', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
    ])
    def test_irisv2_getMessageVariant_create_upload_mobile_particularDate_plain(self, campaignType, testControlType,
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
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
    ])
    def test_irisv2_getMessageVariant_create_upload_mobile_particularDate_coupon(self, campaignType, testControlType, listType,
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

