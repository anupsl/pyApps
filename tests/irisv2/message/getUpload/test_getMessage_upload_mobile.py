import time

import pytest

from src.Constant.constant import constant
from src.modules.irisv2.campaigns.createCampaign import CreateCampaign
from src.modules.irisv2.message.createMessage import CreateMessage
from src.modules.irisv2.message.createMessageDbAssertion import CreateMessageDBAssertion
from src.modules.irisv2.message.getMessage import GetMessage
from src.utilities.logger import Logger


@pytest.mark.run(order=44)
class Test_GetMessage_UploadList_Mobile():
    def setup_method(self, method):
        Logger.logMethodName(method.__name__)

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),

    ])
    def test_irisv2_getMessage_create_upload_mobile_immediate_plain(self, campaignType, testControlType,
                                                                           listType,
                                                                           channel, messageInfo):
        CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo)

        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        messageId = constant.config['node'][campaignType][testControlType]['LIST'][listType][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['RESPONSE']['json']['entity']['id']

        getMessageResponse = GetMessage.getMessageById(campaignId, messageId)
        GetMessage.assertResponse(getMessageResponse, 200)
        CreateMessageDBAssertion(campaignId, messageId, getMessageResponse['json']['entity']).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'SKIP', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def test_irisv2_getMessage_create_upload_mobile_immediate_plain(self, campaignType, testControlType,
                                                                           listType,
                                                                           channel, messageInfo):
        CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo)

        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        messageId = constant.config['node'][campaignType][testControlType]['LIST'][listType][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['RESPONSE']['json']['entity']['id']

        getMessageResponse = GetMessage.getMessageById(campaignId, messageId)
        GetMessage.assertResponse(getMessageResponse, 200)
        CreateMessageDBAssertion(campaignId,messageId,getMessageResponse['json']['entity']).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': True, 'encryptUrl': False, 'skipRateLimit': True}),
    ])
    def test_irisv2_getMessage_create_upload_mobile_immediate_plain_additionalProperties_UsingTinyURL(self,
                                                                                                      campaignType,
                                                                                                      testControlType,
                                                                                                      listType, channel,
                                                                                                      messageInfo):
        messageInfo = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                             updateNode=True,
                             lockNode=True)
        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        messageId = messageInfo['RESPONSE']['json']['entity']['id']
        
        getMessageResponse = GetMessage.getMessageById(campaignId, messageId)
        GetMessage.assertResponse(getMessageResponse, 200)
        CreateMessageDBAssertion(campaignId,messageId,getMessageResponse['json']['entity']).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'CUSTOM', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'SKIP', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
    ])
    def test_irisv2_getMessage_create_upload_mobile_immediate_coupon(self, campaignType, testControlType, listType,
                                                                     channel, messageInfo):
        CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo)
        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        messageId = constant.config['node'][campaignType][testControlType]['LIST'][listType][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['RESPONSE']['json']['entity']['id']
        
        getMessageResponse = GetMessage.getMessageById(campaignId, messageId)
        GetMessage.assertResponse(getMessageResponse, 200)
        CreateMessageDBAssertion(campaignId,messageId,getMessageResponse['json']['entity'],offer=True).check()


    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('UPCOMING', 'CUSTOM', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'SKIP', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def test_irisv2_getMessage_create_upload_mobile_immediate_points(self, campaignType, testControlType, listType,
                                                                     channel, messageInfo):
        CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo)
        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        messageId = constant.config['node'][campaignType][testControlType]['LIST'][listType][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['RESPONSE']['json']['entity']['id']
        
        getMessageResponse = GetMessage.getMessageById(campaignId, messageId)
        GetMessage.assertResponse(getMessageResponse, 200)
        CreateMessageDBAssertion(campaignId,messageId,getMessageResponse['json']['entity'],offer=True).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('UPCOMING', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
    ])
    def test_irisv2_getMessage_create_upload_mobile_particularDate_plain(self, campaignType, testControlType,
                                                                               listType,
                                                                               channel, messageInfo):
        CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo)
        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        messageId = constant.config['node'][campaignType][testControlType]['LIST'][listType][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['RESPONSE']['json']['entity']['id']
        
        getMessageResponse = GetMessage.getMessageById(campaignId, messageId)
        GetMessage.assertResponse(getMessageResponse, 200)
        CreateMessageDBAssertion(campaignId,messageId,getMessageResponse['json']['entity']).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': True, 'skipRateLimit': True}),
    ])
    def test_irisv2_getMessage_create_upload_mobile_particularDate_plain_UsingEncryptURL(self, campaignType,
                                                                                        testControlType,
                                                                                        listType, channel, messageInfo):
        messageInfo = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                           updateNode=True,
                                           lockNode=True)
        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        messageId = messageInfo['RESPONSE']['json']['entity']['id']
        
        getMessageResponse = GetMessage.getMessageById(campaignId, messageId)
        GetMessage.assertResponse(getMessageResponse, 200)
        CreateMessageDBAssertion(campaignId,messageId,getMessageResponse['json']['entity']).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'SKIP', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def test_irisv2_getMessage_create_upload_mobile_particularDate_coupon(self, campaignType, testControlType, listType,
                                                                         channel, messageInfo):
        CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo)
        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        messageId = constant.config['node'][campaignType][testControlType]['LIST'][listType][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['RESPONSE']['json']['entity']['id']
        
        getMessageResponse = GetMessage.getMessageById(campaignId, messageId)
        GetMessage.assertResponse(getMessageResponse, 200)
        CreateMessageDBAssertion(campaignId,messageId,getMessageResponse['json']['entity']).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'CUSTOM', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
    ])
    def test_irisv2_getMessage_create_upload_mobile_particularDate_points(self, campaignType, testControlType, listType,
                                                                         channel, messageInfo):
        CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo)
        CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo)
        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        messageId = constant.config['node'][campaignType][testControlType]['LIST'][listType][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['RESPONSE']['json']['entity']['id']

        getMessageResponse = GetMessage.getMessageById(campaignId, messageId)
        GetMessage.assertResponse(getMessageResponse, 200)
        CreateMessageDBAssertion(campaignId, messageId, getMessageResponse['json']['entity']).check()