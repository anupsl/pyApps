import pytest

from src.Constant.constant import constant
from src.modules.irisv2.helper.irisHelper import IrisHelper
from src.modules.irisv2.message.authorizeMessage import AuthorizeMessage
from src.modules.irisv2.message.authorizeMessageDbAssertion import AuthorizeMessageDBAssertion
from src.utilities.logger import Logger

@pytest.mark.run(order=56)
class Test_ExecuteMessage_MobilePush_PayloadVariation():
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
                                                                                                   "enable": True,
                                                                                                   "value": [['Send',
                                                                                                              'DEEP_LINK',
                                                                                                              'Auto Link'],
                                                                                                             ['Reply',
                                                                                                              'DEEP_LINK',
                                                                                                              'Auto Link']]},
                                                                                               "primary_cta": {
                                                                                                   "enable": False,
                                                                                                   "value": None},
                                                                                               "custom": False},
                                                                                           "ios": {
                                                                                               "contentType": "IMAGE",
                                                                                               "secondary_cta": {
                                                                                                   "enable": False,
                                                                                                   "value": None},
                                                                                               "primary_cta": {
                                                                                                   "enable": True,
                                                                                                   "value": [
                                                                                                       'EXTERNAL_URL',
                                                                                                       'https://www.capillarytech.com']},
                                                                                               "custom": False}},
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def test_irisv2_message_Sanity_execute_mobilePush_android_text_ios_image_secondCTA_DeepLink_PrimaryCTA_ExternalURL_customTrue(self, campaignType,
                                                                                         testControlType,
                                                                                         listType,
                                                                                         channel, messageInfo):
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                  updateNode=True)
        AuthorizeMessage.assertResponse(approveRespone, 200)

        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        response = constant.config['node'][campaignType][testControlType]['LIST'][listType][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['RESPONSE']
        payload = constant.config['node'][campaignType][testControlType]['LIST'][listType][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['PAYLOAD']

        AuthorizeMessageDBAssertion(campaignId, response, payload, testControlType).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT',
                                                                                           "android": {
                                                                                               "contentType": "IMAGE",
                                                                                               "secondary_cta": {
                                                                                                   "enable": True,
                                                                                                   "value": [['Send',
                                                                                                              'DEEP_LINK',
                                                                                                              'Auto Link'],
                                                                                                             ['Reply',
                                                                                                              'DEEP_LINK',
                                                                                                              'Auto Link']]},
                                                                                               "primary_cta": {
                                                                                                   "enable": True,
                                                                                                   "value": [
                                                                                                       'EXTERNAL_URL',
                                                                                                       'https://www.capillarytech.com']},
                                                                                               "custom": True},
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
    def test_irisv2_message_execute_mobilePush_android_image_secondCTA_Multiplevalue_primaryCTAEmable_IOS_Text(self, campaignType, testControlType,
                                                                                    listType,
                                                                                    channel, messageInfo):
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                  updateNode=True)
        AuthorizeMessage.assertResponse(approveRespone, 200)

        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        response = constant.config['node'][campaignType][testControlType]['LIST'][listType][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['RESPONSE']
        payload = constant.config['node'][campaignType][testControlType]['LIST'][listType][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['PAYLOAD']

        AuthorizeMessageDBAssertion(campaignId, response, payload, testControlType).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT',
                                                                                           "ios": {
                                                                                               "contentType": "TEXT",
                                                                                               "secondary_cta": {
                                                                                                   "enable": False,
                                                                                                   "value": None},
                                                                                               "primary_cta": {
                                                                                                   "enable": False,
                                                                                                   "value": None},
                                                                                               "custom": True}},
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def test_irisv2_message_execute_mobilePush_ContentType_OnlyIOS(
            self,
            campaignType,
            testControlType,
            listType,
            channel,
            messageInfo):
        constant.config['mobilepush']['channels'] = ['ios']
        try:
            approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                      updateNode=True)
            AuthorizeMessage.assertResponse(approveRespone, 200)

            campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
            response = constant.config['node'][campaignType][testControlType]['LIST'][listType][channel]['MESSAGE'][
                messageInfo['scheduleType']['type']][messageInfo['offerType']]['RESPONSE']
            payload = constant.config['node'][campaignType][testControlType]['LIST'][listType][channel]['MESSAGE'][
                messageInfo['scheduleType']['type']][messageInfo['offerType']]['PAYLOAD']

            AuthorizeMessageDBAssertion(campaignId, response, payload, testControlType).check()
        finally:
            constant.config['mobilepush']['channels'] = ['android','ios']

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
                                                                                               "custom": True}},
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def test_irisv2_message_execute_mobilePush_ContentType_OnlyAndroid(
            self,
            campaignType,
            testControlType,
            listType,
            channel,
            messageInfo):
        constant.config['mobilepush']['channels'] = ['android']
        try:
            approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                      updateNode=True)
            AuthorizeMessage.assertResponse(approveRespone, 200)

            campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
            response = constant.config['node'][campaignType][testControlType]['LIST'][listType][channel]['MESSAGE'][
                messageInfo['scheduleType']['type']][messageInfo['offerType']]['RESPONSE']
            payload = constant.config['node'][campaignType][testControlType]['LIST'][listType][channel]['MESSAGE'][
                messageInfo['scheduleType']['type']][messageInfo['offerType']]['PAYLOAD']

            AuthorizeMessageDBAssertion(campaignId, response, payload, testControlType).check()
        finally:
            constant.config['mobilepush']['channels'] = ['android','ios']