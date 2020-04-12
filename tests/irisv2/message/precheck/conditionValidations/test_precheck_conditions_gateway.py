import pytest

from src.Constant.constant import constant
from src.modules.irisv2.helper.irisHelper import IrisHelper
from src.modules.irisv2.message.createMessage import CreateMessage
from src.modules.irisv2.message.preCheck import PreCheck
from src.utilities.assertion import Assertion
from src.utilities.logger import Logger

@pytest.mark.skipif(constant.config['cluster'] not in ['nightly'], reason='Precheck Gateway Tests Authorized Only For Nightly')
class Test_Gateway_PreCheck():
    def setup_class(self):
        self.actualOrgId = IrisHelper.updateOrgId(constant.config['mobilepush']['orgId'])
        self.actualOrgName = IrisHelper.updateOrgName(constant.config['mobilepush']['orgName'])

    def setup_method(self, method):
        Logger.logMethodName(method.__name__)

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo,preCheckErrorList', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True},
         [{'errorType': 'CAMPAIGN_NOT_AUTHORIZED', 'parameters': {}},
          {'errorType': 'GATEWAY_NOT_AVAILABLE', 'parameters': {}}])
    ])
    def test_irisv2_message_precheck_create_upload_mobile_immediate_GatewayNotAvialable(self, campaignType,
                                                                                               testControlType,
                                                                                               listType,
                                                                                               channel,
                                                                                               messageInfo,
                                                                                               preCheckErrorList):
        try:
            messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                                  updateNode=True, lockNode=True)
            CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
            IrisHelper.disableDomainGatewayMapId(channel)
            preCheckResponse = PreCheck.executePrecheck(
                constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                messageDetails['RESPONSE']['json']['entity']['id'])
            PreCheck.assertPreCheckResponse(preCheckResponse, 200)
            PreCheck.assertPrecheckStatus(preCheckResponse,preCheckErrorList)
        finally:
            IrisHelper.createNewDummyGateway(channel)

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo,preCheckErrorList', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True},
         [{'errorType': 'CAMPAIGN_NOT_AUTHORIZED', 'parameters': {}},
          {'errorType': 'GATEWAY_NOT_AVAILABLE', 'parameters': {}}])
    ])
    def test_irisv2_message_precheck_create_upload_mobile_particularDate_GatewayNotAvialable(self, campaignType,
                                                                                                    testControlType,
                                                                                                    listType,
                                                                                                    channel,
                                                                                                    messageInfo,
                                                                                                    preCheckErrorList):
        try:
            messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                                  updateNode=True, lockNode=True)
            CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
            IrisHelper.disableDomainGatewayMapId(channel)
            preCheckResponse = PreCheck.executePrecheck(
                constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                messageDetails['RESPONSE']['json']['entity']['id'])
            PreCheck.assertPreCheckResponse(preCheckResponse, 200)
            PreCheck.assertPrecheckStatus(preCheckResponse,preCheckErrorList)
        finally:
            IrisHelper.createNewDummyGateway(channel)

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo,preCheckErrorList', [
        ('LIVE', 'ORG', 'UPLOAD', 'EMAIL',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True},
         [{'errorType': 'CAMPAIGN_NOT_AUTHORIZED', 'parameters': {}},
          {'errorType': 'GATEWAY_NOT_AVAILABLE', 'parameters': {}}])
    ])
    def test_irisv2_message_precheck_create_upload_email_immediate_GatewayNotAvialable(self, campaignType,
                                                                                              testControlType,
                                                                                              listType,
                                                                                              channel,
                                                                                              messageInfo,
                                                                                              preCheckErrorList):
        try:
            messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                                  updateNode=True, lockNode=True)
            CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
            IrisHelper.disableDomainGatewayMapId(channel)
            preCheckResponse = PreCheck.executePrecheck(
                constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                messageDetails['RESPONSE']['json']['entity']['id'])
            PreCheck.assertPreCheckResponse(preCheckResponse, 200)
            PreCheck.assertPrecheckStatus(preCheckResponse,preCheckErrorList)
        finally:
            IrisHelper.createNewDummyGateway(channel)

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo,preCheckErrorList', [
        ('LIVE', 'ORG', 'UPLOAD', 'EMAIL',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True},
         [{'errorType': 'CAMPAIGN_NOT_AUTHORIZED', 'parameters': {}},
          {'errorType': 'GATEWAY_NOT_AVAILABLE', 'parameters': {}}])
    ])
    def test_irisv2_message_precheck_create_upload_email_particularDate_GatewayNotAvialable(self, campaignType,
                                                                                                   testControlType,
                                                                                                   listType,
                                                                                                   channel,
                                                                                                   messageInfo,
                                                                                                   preCheckErrorList):
        try:
            messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                                  updateNode=True, lockNode=True)
            CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
            IrisHelper.disableDomainGatewayMapId(channel)
            preCheckResponse = PreCheck.executePrecheck(
                constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                messageDetails['RESPONSE']['json']['entity']['id'])
            PreCheck.assertPreCheckResponse(preCheckResponse, 200)
            PreCheck.assertPrecheckStatus(preCheckResponse,preCheckErrorList)
        finally:
            IrisHelper.createNewDummyGateway(channel)

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo,preCheckErrorList', [
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
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True},
         [{'errorType': 'CAMPAIGN_NOT_AUTHORIZED', 'parameters': {}}])

    ])
    def test_irisv2_message_precheck_create_upload_mobilePush_immediate_NotAuthorized(self, campaignType,
                                                                                             testControlType,
                                                                                             listType,
                                                                                             channel, messageInfo,
                                                                                             preCheckErrorList):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True, lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        preCheckResponse = PreCheck.executePrecheck(
            constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
            messageDetails['RESPONSE']['json']['entity']['id'])
        PreCheck.assertPreCheckResponse(preCheckResponse, 200)
        PreCheck.assertPrecheckStatus(preCheckResponse,preCheckErrorList)

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo,preCheckErrorList', [
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
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True},
         [{'errorType': 'CAMPAIGN_NOT_AUTHORIZED', 'parameters': {}}])

    ])
    def test_irisv2_message_precheck_create_upload_mobilePush_particularDate_NotAuthorized(self, campaignType,
                                                                                                  testControlType,
                                                                                                  listType,
                                                                                                  channel, messageInfo,
                                                                                                  preCheckErrorList):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True, lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        preCheckResponse = PreCheck.executePrecheck(
            constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
            messageDetails['RESPONSE']['json']['entity']['id'])
        PreCheck.assertPreCheckResponse(preCheckResponse, 200)
        PreCheck.assertPrecheckStatus(preCheckResponse,preCheckErrorList)
