import time
import pytest

from src.modules.irisv2.helper.irisHelper import IrisHelper
from src.Constant.constant import constant
from src.modules.irisv2.campaigns.createCampaign import CreateCampaign
from src.modules.irisv2.message.authorizeMessage import AuthorizeMessage
from src.modules.irisv2.message.authorizeMessageDbAssertion import AuthorizeMessageDBAssertion
from src.modules.irisv2.message.createMessage import CreateMessage
from src.utilities.logger import Logger

@pytest.mark.run(order=55)
class Test_ExecuteMessage_MobilePush_UploadList():
    def setup_class(self):
        self.actualOrgId = IrisHelper.updateOrgId(constant.config['mobilepush']['orgId'])
        self.actualOrgName = IrisHelper.updateOrgName(constant.config['mobilepush']['orgName'])

    def teardown_class(self):
        IrisHelper.updateOrgId(self.actualOrgId)
        IrisHelper.updateOrgName(self.actualOrgName)

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('UPCOMING', 'SKIP', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT',"android":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False},"ios":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False}},
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': True, 'encryptUrl': False, 'skipRateLimit': True}),
        ('IMMEDIATE', 'CUSTOM', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT',"android":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False},"ios":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False}},
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': True, 'encryptUrl': False, 'skipRateLimit': False})
    ])
    def irisv2_message_execute_mobilePush_immediate_plain(self, campaignType, testControlType, listType,
                                                                        channel, messageInfo):
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo)
        AuthorizeMessage.assertResponse(approveRespone, 200)

        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        response = constant.config['node'][campaignType][testControlType]['LIST'][listType][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['RESPONSE']
        payload = constant.config['node'][campaignType][testControlType]['LIST'][listType][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['PAYLOAD']

        AuthorizeMessageDBAssertion(campaignId, response, payload, testControlType).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'SKIP', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT',
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
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': True, 'encryptUrl': False, 'skipRateLimit': False}),

    ])
    def irisv2_message_Sanity_execute_mobilePush_immediate_plain(self, campaignType, testControlType, listType,
                                                                      channel, messageInfo):
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo)
        AuthorizeMessage.assertResponse(approveRespone, 200)

        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        response = constant.config['node'][campaignType][testControlType]['LIST'][listType][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['RESPONSE']
        payload = constant.config['node'][campaignType][testControlType]['LIST'][listType][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['PAYLOAD']

        AuthorizeMessageDBAssertion(campaignId, response, payload, testControlType).check()

    def setup_method(self, method):
        Logger.logMethodName(method.__name__)

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LAPSED', 'ORG', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT',"android":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False},"ios":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False}},
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
    ])
    def irisv2_message_execute_mobilePush_immediate_plain_lapsed(self, campaignType, testControlType, listType,
                                                                        channel, messageInfo):
        CreateCampaign.create(campaignType, testControlType, endDate=int(
            time.time() * 1000) + 1 * 60 * 1000)
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo)
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                  messageCreateResponse=messageDetails)
        AuthorizeMessage.assertResponse(approveRespone, 400, expectedErrorCode=3036,
                                        expectedErrorMessage=['Campaign expired'])

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT',"android":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False},"ios":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False}},
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': True, 'encryptUrl': False, 'skipRateLimit': True}),
    ])
    def irisv2_message_execute_mobilePush_immediate_plain_additionalProperties_UsingTinyURL(self, campaignType,
                                                                                                   testControlType,
                                                                                                   listType, channel,
                                                                                                   messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True)
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                  messageCreateResponse=messageDetails)
        AuthorizeMessage.assertResponse(approveRespone, 200)

        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        response = constant.config['node'][campaignType][testControlType]['LIST'][listType][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['RESPONSE']
        payload = constant.config['node'][campaignType][testControlType]['LIST'][listType][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['PAYLOAD']

        AuthorizeMessageDBAssertion(campaignId, response, payload, testControlType).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT',"android":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False},"ios":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False}},
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': True, 'skipRateLimit': True}),
    ])
    def irisv2_message_execute_mobilePush_immediate_plain_additionalProperties_UsingEncryptURL(self,
                                                                                                      campaignType,
                                                                                                      testControlType,
                                                                                                      listType, channel,
                                                                                                      messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True)
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                  messageCreateResponse=messageDetails)
        AuthorizeMessage.assertResponse(approveRespone, 200)

        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        response = constant.config['node'][campaignType][testControlType]['LIST'][listType][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['RESPONSE']
        payload = constant.config['node'][campaignType][testControlType]['LIST'][listType][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['PAYLOAD']

        AuthorizeMessageDBAssertion(campaignId, response, payload, testControlType).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT',"android":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False},"ios":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False}},
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': False}),
    ])
    def irisv2_message_execute_mobilePush_immediate_plain_additionalProperties_UsingRateLimit(self, campaignType,
                                                                                                     testControlType,
                                                                                                     listType, channel,
                                                                                                     messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True)
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                  messageCreateResponse=messageDetails)
        AuthorizeMessage.assertResponse(approveRespone, 200)

        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        response = constant.config['node'][campaignType][testControlType]['LIST'][listType][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['RESPONSE']
        payload = constant.config['node'][campaignType][testControlType]['LIST'][listType][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['PAYLOAD']

        AuthorizeMessageDBAssertion(campaignId, response, payload, testControlType).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT',"android":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False},"ios":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False}},
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'CUSTOM', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT',"android":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False},"ios":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False}},
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'SKIP', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT',"android":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False},"ios":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False}},
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'ORG', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT',"android":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False},"ios":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False}},
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'CUSTOM', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT',"android":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False},"ios":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False}},
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'SKIP', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT',"android":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False},"ios":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False}},
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def irisv2_message_execute_mobilePush_immediate_coupon(self, campaignType, testControlType, listType,
                                                                  channel, messageInfo):
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo)
        AuthorizeMessage.assertResponse(approveRespone, 200)

        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        response = constant.config['node'][campaignType][testControlType]['LIST'][listType][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['RESPONSE']
        payload = constant.config['node'][campaignType][testControlType]['LIST'][listType][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['PAYLOAD']

        AuthorizeMessageDBAssertion(campaignId, response, payload, testControlType).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LAPSED', 'ORG', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT',"android":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False},"ios":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False}},
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LAPSED', 'CUSTOM', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT',"android":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False},"ios":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False}},
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LAPSED', 'SKIP', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT',"android":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False},"ios":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False}},
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def irisv2_message_execute_mobilePush_immediate_coupon_lapsed(self, campaignType, testControlType, listType,
                                                                         channel, messageInfo):
        CreateCampaign.create(campaignType, testControlType, endDate=int(
            time.time() * 1000) + 1 * 60 * 1000)
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo)
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                  messageCreateResponse=messageDetails)
        AuthorizeMessage.assertResponse(approveRespone, 400, expectedErrorCode=3036,
                                        expectedErrorMessage=['Campaign expired'])

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT',"android":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False},"ios":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False}},
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'CUSTOM', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT',"android":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False},"ios":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False}},
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'SKIP', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT',"android":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False},"ios":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False}},
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'ORG', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT',"android":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False},"ios":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False}},
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'CUSTOM', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT',"android":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False},"ios":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False}},
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'SKIP', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT',"android":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False},"ios":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False}},
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def irisv2_message_execute_mobilePush_immediate_points(self, campaignType, testControlType, listType,
                                                                 channel, messageInfo):
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo)
        AuthorizeMessage.assertResponse(approveRespone, 200)

        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        response = constant.config['node'][campaignType][testControlType]['LIST'][listType][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['RESPONSE']
        payload = constant.config['node'][campaignType][testControlType]['LIST'][listType][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['PAYLOAD']

        AuthorizeMessageDBAssertion(campaignId, response, payload, testControlType,skippedReason=['Users are not registered in loyalty program']).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LAPSED', 'ORG', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT',"android":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False},"ios":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False}},
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LAPSED', 'CUSTOM', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT',"android":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False},"ios":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False}},
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LAPSED', 'SKIP', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT',"android":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False},"ios":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False}},
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def irisv2_message_execute_mobilePush_immediate_point_lapsed(self, campaignType, testControlType, listType,
                                                                       channel, messageInfo):
        CreateCampaign.create(campaignType, testControlType, endDate=int(
            time.time() * 1000) + 1 * 60 * 1000)
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo)
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                  messageCreateResponse=messageDetails)
        AuthorizeMessage.assertResponse(approveRespone, 400, expectedErrorCode=3036,
                                        expectedErrorMessage=['Campaign expired'])

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT',"android":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False},"ios":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False}},
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'CUSTOM', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT',"android":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False},"ios":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False}},
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'SKIP', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT',"android":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False},"ios":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False}},
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'ORG', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT',"android":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False},"ios":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False}},
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'CUSTOM', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT',"android":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False},"ios":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False}},
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'SKIP', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT',"android":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False},"ios":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False}},
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def irisv2_message_create_mobilePush_particularDate_plain(self, campaignType, testControlType,
                                                                             listType,
                                                                             channel, messageInfo):
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo)
        AuthorizeMessage.assertResponse(approveRespone, 200)

        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        response = constant.config['node'][campaignType][testControlType]['LIST'][listType][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['RESPONSE']
        payload = constant.config['node'][campaignType][testControlType]['LIST'][listType][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['PAYLOAD']

        AuthorizeMessageDBAssertion(campaignId, response, payload, testControlType).check()


    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LAPSED', 'ORG', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT',"android":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False},"ios":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False}},
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LAPSED', 'CUSTOM', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT',"android":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False},"ios":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False}},
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LAPSED', 'SKIP', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT',"android":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False},"ios":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False}},
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def irisv2_message_execute_mobilePush_particularDate_plain_lapsed(self, campaignType, testControlType,
                                                                             listType,
                                                                             channel, messageInfo):
        CreateCampaign.create(campaignType, testControlType, endDate=int(
            time.time() * 1000) + 1 * 60 * 1000)
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo)
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                  messageCreateResponse=messageDetails)

        AuthorizeMessage.assertResponse(approveRespone, 400, expectedErrorCode=3036,
                                        expectedErrorMessage=['Campaign expired'])

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT',"android":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False},"ios":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False}},
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': True, 'encryptUrl': False, 'skipRateLimit': True}),
    ])
    def irisv2_message_execute_mobilePush_particularDate_plain_UsingTinyURL(self, campaignType, testControlType,
                                                                                   listType, channel, messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True)
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                  messageCreateResponse=messageDetails)
        AuthorizeMessage.assertResponse(approveRespone, 200)

        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        response = constant.config['node'][campaignType][testControlType]['LIST'][listType][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['RESPONSE']
        payload = constant.config['node'][campaignType][testControlType]['LIST'][listType][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['PAYLOAD']
        AuthorizeMessageDBAssertion(campaignId, response, payload, testControlType).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT',"android":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False},"ios":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False}},
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': True, 'skipRateLimit': True}),
    ])
    def irisv2_message_execute_mobilePush_particularDate_plain_UsingEncryptURL(self, campaignType,
                                                                                      testControlType,
                                                                                      listType, channel, messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True)
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                  messageCreateResponse=messageDetails)
        AuthorizeMessage.assertResponse(approveRespone, 200)

        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        response = constant.config['node'][campaignType][testControlType]['LIST'][listType][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['RESPONSE']
        payload = constant.config['node'][campaignType][testControlType]['LIST'][listType][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['PAYLOAD']
        AuthorizeMessageDBAssertion(campaignId, response, payload, testControlType).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT',"android":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False},"ios":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False}},
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': False}),
    ])
    def irisv2_message_execute_mobilePush_particularDate_plain_UsingRateLimit(self, campaignType,
                                                                                     testControlType,
                                                                                     listType, channel, messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True)
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                  messageCreateResponse=messageDetails)
        AuthorizeMessage.assertResponse(approveRespone, 200)

        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        response = constant.config['node'][campaignType][testControlType]['LIST'][listType][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['RESPONSE']
        payload = constant.config['node'][campaignType][testControlType]['LIST'][listType][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['PAYLOAD']
        AuthorizeMessageDBAssertion(campaignId, response, payload, testControlType).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT',"android":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False},"ios":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False}},
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'CUSTOM', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT',"android":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False},"ios":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False}},
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'SKIP', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT',"android":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False},"ios":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False}},
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'ORG', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT',"android":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False},"ios":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False}},
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'CUSTOM', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT',"android":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False},"ios":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False}},
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'SKIP', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT',"android":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False},"ios":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False}},
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def irisv2_message_execute_mobilePush_particularDate_coupon(self, campaignType, testControlType,
                                                                       listType,
                                                                       channel, messageInfo):
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo)
        AuthorizeMessage.assertResponse(approveRespone, 200)

        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        response = constant.config['node'][campaignType][testControlType]['LIST'][listType][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['RESPONSE']
        payload = constant.config['node'][campaignType][testControlType]['LIST'][listType][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['PAYLOAD']

        AuthorizeMessageDBAssertion(campaignId, response, payload, testControlType).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LAPSED', 'ORG', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT',"android":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False},"ios":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False}},
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LAPSED', 'CUSTOM', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT',"android":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False},"ios":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False}},
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LAPSED', 'SKIP', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT',"android":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False},"ios":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False}},
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def irisv2_message_execute_mobilePush_particularDate_coupon_lapsed(self, campaignType, testControlType,
                                                                              listType,
                                                                              channel, messageInfo):
        CreateCampaign.create(campaignType, testControlType, endDate=int(
            time.time() * 1000) + 1 * 60 * 1000)
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo)
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                  messageCreateResponse=messageDetails)
        AuthorizeMessage.assertResponse(approveRespone, 400, expectedErrorCode=3036,
                                        expectedErrorMessage=['Campaign expired'])

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT',"android":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False},"ios":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False}},
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'CUSTOM', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT',"android":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False},"ios":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False}},
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'SKIP', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT',"android":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False},"ios":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False}},
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'ORG', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT',"android":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False},"ios":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False}},
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'CUSTOM', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT',"android":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False},"ios":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False}},
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'SKIP', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT',"android":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False},"ios":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False}},
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def irisv2_message_execute_mobilePush_particularDate_points(self, campaignType, testControlType, listType,
                                                                      channel, messageInfo):
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo)
        AuthorizeMessage.assertResponse(approveRespone, 200)

        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        response = constant.config['node'][campaignType][testControlType]['LIST'][listType][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['RESPONSE']
        payload = constant.config['node'][campaignType][testControlType]['LIST'][listType][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['PAYLOAD']

        AuthorizeMessageDBAssertion(campaignId, response, payload, testControlType,skippedReason=['Users are not registered in loyalty program']).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LAPSED', 'ORG', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT',"android":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False},"ios":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False}},
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LAPSED', 'CUSTOM', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT',"android":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False},"ios":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False}},
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LAPSED', 'SKIP', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT',"android":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False},"ios":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False}},
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def irisv2_message_execute_mobilePush_particularDate_point_lapsed(self, campaignType, testControlType,
                                                                             listType,
                                                                             channel, messageInfo):
        CreateCampaign.create(campaignType, testControlType, endDate=int(
            time.time() * 1000) + 1 * 60 * 1000)
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo)
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                  messageCreateResponse=messageDetails)
        AuthorizeMessage.assertResponse(approveRespone, 400, expectedErrorCode=3036,
                                        expectedErrorMessage=['Campaign expired'])

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT',"android":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False},"ios":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False}},
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'CUSTOM', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT',"android":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False},"ios":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False}},
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'SKIP', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT',"android":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False},"ios":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False}},
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'ORG', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT',"android":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False},"ios":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False}},
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'CUSTOM', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT',"android":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False},"ios":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False}},
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'SKIP', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT',"android":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False},"ios":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False}},
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def irisv2_message_create_mobilePush_Recurring_plain(self, campaignType, testControlType,
                                                                       listType,
                                                                       channel, messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)




    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LAPSED', 'ORG', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT',"android":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False},"ios":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False}},
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LAPSED', 'CUSTOM', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT',"android":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False},"ios":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False}},
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LAPSED', 'SKIP', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT',"android":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False},"ios":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False}},
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def irisv2_message_create_mobilePush_Recurring_plain_lapsed(self, campaignType, testControlType,
                                                                       listType,
                                                                       channel, messageInfo):
        CreateCampaign.create(campaignType, testControlType, endDate=int(
            time.time() * 1000) + 5 * 60 * 1000)
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)


    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LAPSED', 'ORG', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT',"android":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False},"ios":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False}},
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': True, 'encryptUrl': False, 'skipRateLimit': True}),
    ])
    def est_irisv2_message_create_mobilePush_Recurring_plain_UsingTinyURL(self, campaignType, testControlType,
                                                                             listType, channel, messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)


    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LAPSED', 'ORG', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT',"android":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False},"ios":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False}},
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': True, 'skipRateLimit': True}),
    ])
    def est_irisv2_message_create_mobilePush_Recurring_plain_UsingEncryptURL(self, campaignType,
                                                                                testControlType,
                                                                                listType, channel, messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)


    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LAPSED', 'ORG', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT',"android":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False},"ios":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False}},
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': False}),
    ])
    def est_irisv2_message_create_mobilePush_Recurring_plain_UsingRateLimit(self, campaignType,
                                                                               testControlType,
                                                                               listType, channel, messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)


    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT',"android":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False},"ios":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False}},
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'CUSTOM', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT',"android":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False},"ios":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False}},
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'SKIP', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT',"android":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False},"ios":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False}},
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'ORG', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT',"android":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False},"ios":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False}},
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'CUSTOM', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT',"android":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False},"ios":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False}},
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'SKIP', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT',"android":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False},"ios":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False}},
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def est_irisv2_message_create_mobilePush_Recurring_coupon(self, campaignType, testControlType, listType,
                                                                 channel, messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)


    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LAPSED', 'ORG', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT',"android":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False},"ios":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False}},
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LAPSED', 'CUSTOM', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT',"android":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False},"ios":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False}},
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LAPSED', 'SKIP', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT',"android":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False},"ios":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False}},
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def est_irisv2_message_create_mobilePush_Recurring_coupon_lapsed(self, campaignType, testControlType,
                                                                        listType,
                                                                        channel, messageInfo):
        CreateCampaign.create(campaignType, testControlType, endDate=int(
            time.time() * 1000) + 5 * 60 * 1000)
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)


    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT',"android":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False},"ios":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False}},
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'CUSTOM', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT',"android":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False},"ios":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False}},
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'SKIP', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT',"android":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False},"ios":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False}},
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'ORG', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT',"android":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False},"ios":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False}},
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'CUSTOM', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT',"android":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False},"ios":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False}},
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'SKIP', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT',"android":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False},"ios":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False}},
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def est_irisv2_message_create_mobilePush_Recurring_points(self, campaignType, testControlType, listType,
                                                                 channel, messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)


    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LAPSED', 'ORG', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT',"android":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False},"ios":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False}},
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LAPSED', 'CUSTOM', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT',"android":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False},"ios":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False}},
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LAPSED', 'SKIP', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT',"android":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False},"ios":{"contentType":"TEXT","secondary_cta":{"enable":False,"value":None},"primary_cta":{"enable":False,"value":None},"custom":False}},
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def est_irisv2_message_create_mobilePush_Recurring_coupon_lapsed(self, campaignType, testControlType,
                                                                        listType,
                                                                        channel, messageInfo):
        CreateCampaign.create(campaignType, testControlType, endDate=int(
            time.time() * 1000) + 5 * 60 * 1000)
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
