import pytest

from src.Constant.constant import constant
from src.dbCalls.messageInfo import message_calls
from src.modules.irisv2.helper.irisHelper import IrisHelper
from src.modules.irisv2.list.createAudience import CreateAudience
from src.modules.irisv2.message.authorizeMessage import AuthorizeMessage
from src.modules.irisv2.message.createMessage import CreateMessage
from src.modules.irisv2.message.createMessageDbAssertion import CreateMessageDBAssertion
from src.utilities.logger import Logger
from src.modules.irisv2.campaigns.createCampaign import CreateCampaign

import req

class Test_MessageStatus_pair_Stop_reject():
    def setup_method(self, method):
        Logger.logMethodName(method.__name__)

    def setup_class(self):
        CreateAudience.getPocUsers()
        constant.config['FilterListID'] = CreateAudience.FilterList('LAPSED', 'ORG', campaignCheck=False)['ID']

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
    ])
    def test_irisv2_messageStatus_upload_mobile_immediate_plain_notApproved_Reject(self, campaignType, testControlType,
                                                                                   listType,
                                                                                   channel, messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True, lockNode=True)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION')
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        rejectResponse = CreateMessage.reject(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                              messageDetails['RESPONSE']['json']['entity']['id'])
        CreateMessage.assertResponse(rejectResponse, 200)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],
                                 approved='REJECTED').check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('UPCOMING', 'ORG', 'UPLOAD', 'EMAIL',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
    ])
    def test_irisv2_messageStatus_upload_email_particulardate_point_notApproved_Reject(self, campaignType,
                                                                                       testControlType,
                                                                                       listType,
                                                                                       channel, messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True, lockNode=True)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION')
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        rejectResponse = CreateMessage.reject(
            constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
            messageDetails['RESPONSE']['json']['entity']['id'])
        CreateMessage.assertResponse(rejectResponse, 200)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],
                                 reject={'status': 'CLOSED'}, approved='REJECTED').check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('UPCOMING', 'SKIP', 'UPLOAD', 'MOBILE_PUSH',
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
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': True, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'SKIP', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'MULTICOUPONS', 'messageStrategy': {'type': 'DEFAULT',
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
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': True, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def test_irisv2_messageStatus_push_recurring_coupon_notApproved_Reject(self, campaignType, testControlType,
                                                                           listType,
                                                                           channel, messageInfo):
        try:
            actualOrgId = IrisHelper.updateOrgId(constant.config['mobilepush']['orgId'])
            actualOrgName = IrisHelper.updateOrgName(constant.config['mobilepush']['orgName'])

            messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                                  updateNode=True, lockNode=True)
            message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'],
                                                           'VARIANT_CREATION')
            CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
            rejectResponse = CreateMessage.reject(
                constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                messageDetails['RESPONSE']['json']['entity']['id'])
            CreateMessage.assertResponse(rejectResponse, 200)
            CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                     messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],
                                     reject={'status': 'CLOSED'}, approved='REJECTED').check()
        finally:
            IrisHelper.updateOrgId(actualOrgId)
            IrisHelper.updateOrgName(actualOrgName)

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'LOYALTY', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'ORG', 'LOYALTY', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'MULTICOUPONS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'ORG', 'LOYALTY', 'EMAIL',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
    ])
    def test_irisv2_messageStatus_sms_email_push_particulardate_Approved_Stopt(self, campaignType, testControlType,
                                                                               listType,
                                                                               channel, messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION')
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                  messageCreateResponse=messageDetails)
        AuthorizeMessage.assertResponse(approveRespone, 200)
        stopResponse = CreateMessage.stop(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                          approveRespone['json']['entity']['messageId'])
        CreateMessage.assertResponse(stopResponse, 200)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],
                                 reject={'status': 'CLOSED'}, approved='STOPPED').check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('UPCOMING', 'ORG', 'LOYALTY', 'MOBILE_PUSH',
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
    def test_irisv2_messageStatus_push_particulardate_Approved_Stopt(self, campaignType, testControlType,
                                                                     listType,
                                                                     channel, messageInfo):
        try:
            actualOrgId = IrisHelper.updateOrgId(constant.config['mobilepush']['orgId'])
            actualOrgName = IrisHelper.updateOrgName(constant.config['mobilepush']['orgName'])
            campaignInfo = CreateCampaign.create(campaignType, testControlType,updateNode=True,lockNode=True)

            messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                                  campaignId=campaignInfo['ID'],updateNode = True)
            CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
            message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'],
                                                           'VARIANT_CREATION')
            approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,campaignId=campaignInfo['ID'],
                                                      messageCreateResponse=messageDetails)
            AuthorizeMessage.assertResponse(approveRespone, 200)
            stopResponse = CreateMessage.stop(campaignInfo['ID'],
                                              approveRespone['json']['entity']['messageId'])
            CreateMessage.assertResponse(stopResponse, 200)
            CreateMessageDBAssertion(campaignInfo['ID'],
                                     messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],
                                     reject={'status': 'CLOSED'}, approved='STOPPED').check()
        finally:
            IrisHelper.updateOrgId(actualOrgId)
            IrisHelper.updateOrgName(actualOrgName)

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'LOYALTY', 'MOBILE',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def test_irisv2_messageStatus_sms_recurring_points_Approved_Stop(self, campaignType, testControlType,
                                                                     listType,
                                                                     channel, messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION')
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                  messageCreateResponse=messageDetails)
        AuthorizeMessage.assertResponse(approveRespone, 200)
        stopResponse = CreateMessage.stop(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                          approveRespone['json']['entity']['messageId'])
        CreateMessage.assertResponse(stopResponse, 200)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],
                                 reject={'status': 'CLOSED'}, approved='STOPPED').check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'CUSTOM', 'ORG_USERS', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def test_irisv2_messageStatus_stickylist_sms_recurring_points_Approved_Stop(self, campaignType, testControlType,
                                                                                listType,
                                                                                channel, messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, 'ORG_USERS', channel, messageInfo,
                                              derivedListInfo={'excludeUsers': [], 'includeUsers': ':1'})

        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION')
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                  messageCreateResponse=messageDetails)
        AuthorizeMessage.assertResponse(approveRespone, 200)
        stopResponse = CreateMessage.stop(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                          approveRespone['json']['entity']['messageId'])
        CreateMessage.assertResponse(stopResponse, 200)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],
                                 reject={'status': 'CLOSED'}, approved='STOPPED').check()
