import time
import pytest
from src.Constant.constant import constant
from src.modules.irisv2.campaigns.createCampaign import CreateCampaign
from src.modules.irisv2.message.authorizeMessage import AuthorizeMessage
from src.modules.irisv2.message.authorizeMessageDbAssertion import AuthorizeMessageDBAssertion
from src.modules.irisv2.message.getMessage import GetMessage
from src.modules.irisv2.message.createMessageDbAssertion import CreateMessageDBAssertion
from src.modules.irisv2.message.createMessage import CreateMessage
from src.utilities.logger import Logger

@pytest.mark.run(order=35)
class Test_getMessage_derived_Derived():
    def setup_method(self, method):
        Logger.logMethodName(method.__name__)

    @pytest.mark.parametrize('campaignType,testControlType,channel,messageInfo', [
        ('LIVE', 'ORG', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),

    ])
    def irisv2_message_Sanity_create_execute_get_derived_derived_SMS_include_excludelist_immediate_plain(self,
                                                                                                         campaignType,
                                                                                                         testControlType,
                                                                                                         channel,
                                                                                                         messageInfo):
        CreateMessage.create(campaignType, testControlType, 'DERIVED', channel, messageInfo,
                             derivedListInfo={'includedGroups' : ['UPLOAD', 'LOYALTY', 'DERIVED'],'excludedGroup' : ['UPLOADOLD'], 'derived' : ['UPLOADOLD','UPLOAD','LOYALTY'],'noOfUserUpload' : 5})
        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        messageId = constant.config['node'][campaignType][testControlType]['LIST']['DERIVED'][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['RESPONSE']['json']['entity']['id']
        getMessageResponse = GetMessage.getMessageById(campaignId, messageId)
        GetMessage.assertResponse(getMessageResponse, 200)
        CreateMessageDBAssertion(campaignId, messageId, getMessageResponse['json']['entity']).check()

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
    def irisv2_message_create_execute_get_derived_derived_SMS_include_excludelist_immediate_plain(self,
                                                                                                              campaignType,
                                                                                                              testControlType,
                                                                                                              channel,
                                                                                                              messageInfo):
        CreateMessage.create(campaignType, testControlType, 'DERIVED', channel, messageInfo,
                             derivedListInfo={'includedGroups': ['UPLOAD', 'LOYALTY', 'DERIVED'],
                                              'excludedGroup': ['UPLOADOLD'],
                                              'derived': ['UPLOADOLD', 'UPLOAD', 'LOYALTY'], 'noOfUserUpload': 5})
        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        messageId = constant.config['node'][campaignType][testControlType]['LIST']['DERIVED'][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['RESPONSE']['json']['entity']['id']
        getMessageResponse = GetMessage.getMessageById(campaignId, messageId)
        GetMessage.assertResponse(getMessageResponse, 200)
        CreateMessageDBAssertion(campaignId, messageId, getMessageResponse['json']['entity']).check()

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
    def irisv2_message_create_execute_get_derived_derived_EMAIL_include_excludelist_immediate_plain(self,
                                                                                                           campaignType,
                                                                                                           testControlType,
                                                                                                           channel,
                                                                                                           messageInfo):
        CreateMessage.create(campaignType, testControlType, 'DERIVED', channel, messageInfo,
                             derivedListInfo={'includedGroups' : ['UPLOAD', 'LOYALTY', 'DERIVED'],'excludedGroup' : ['UPLOADOLD'], 'derived' : ['UPLOADOLD','UPLOAD','LOYALTY'],'noOfUserUpload' : 5})
        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        messageId = constant.config['node'][campaignType][testControlType]['LIST']['DERIVED'][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['RESPONSE']['json']['entity']['id']
        getMessageResponse = GetMessage.getMessageById(campaignId, messageId)
        GetMessage.assertResponse(getMessageResponse, 200)
        CreateMessageDBAssertion(campaignId, messageId, getMessageResponse['json']['entity']).check()

    @pytest.mark.parametrize('campaignType,testControlType,channel,messageInfo', [
        ('LIVE', 'ORG', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': True, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def irisv2_message_create_execute_get_derived_derived_SMS_immediate_plain_additionalProperties_UsingTinyURL(self,
                                                                                                                campaignType,
                                                                                                                testControlType,
                                                                                                                channel,
                                                                                                                messageInfo):
        CreateMessage.create(campaignType, testControlType, 'DERIVED', channel, messageInfo,
                             derivedListInfo={'includedGroups' : ['UPLOAD', 'LOYALTY', 'DERIVED'],'excludedGroup' : ['UPLOADOLD'], 'derived' : ['UPLOADOLD','UPLOAD','LOYALTY'],'noOfUserUpload' : 5})
        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        messageId = constant.config['node'][campaignType][testControlType]['LIST']['DERIVED'][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['RESPONSE']['json']['entity']['id']
        getMessageResponse = GetMessage.getMessageById(campaignId, messageId)
        GetMessage.assertResponse(getMessageResponse, 200)
        CreateMessageDBAssertion(campaignId, messageId, getMessageResponse['json']['entity']).check()

    @pytest.mark.parametrize('campaignType,testControlType,channel,messageInfo', [
        ('LIVE', 'ORG', 'EMAIL',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': True, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def irisv2_message_create_execute_get_derived_derived_EMAIL_immediate_plain_additionalProperties_UsingTinyURL(self,
                                                                                                                  campaignType,
                                                                                                                  testControlType,
                                                                                                                  channel,
                                                                                                                  messageInfo):
        CreateMessage.create(campaignType, testControlType, 'DERIVED', channel, messageInfo,
                             derivedListInfo={'includedGroups' : ['UPLOAD', 'LOYALTY', 'DERIVED'],'excludedGroup' : ['UPLOADOLD'], 'derived' : ['UPLOADOLD','UPLOAD','LOYALTY'],'noOfUserUpload' : 5})
        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        messageId = constant.config['node'][campaignType][testControlType]['LIST']['DERIVED'][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['RESPONSE']['json']['entity']['id']
        getMessageResponse = GetMessage.getMessageById(campaignId, messageId)
        GetMessage.assertResponse(getMessageResponse, 200)
        CreateMessageDBAssertion(campaignId, messageId, getMessageResponse['json']['entity']).check()

    @pytest.mark.parametrize('campaignType,testControlType,channel,messageInfo', [
        ('LIVE', 'ORG', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': True, 'skipRateLimit': True}),
    ])
    def irisv2_message_create_execute_get_derived_derived_SMS_immediate_plain_additionalProperties_UsingEncryptURL(self,
                                                                                                                   campaignType,
                                                                                                                   testControlType,
                                                                                                                   channel,
                                                                                                                   messageInfo):
        CreateMessage.create(campaignType, testControlType, 'DERIVED', channel, messageInfo,
                             derivedListInfo={'includedGroups' : ['UPLOAD', 'LOYALTY', 'DERIVED'],'excludedGroup' : ['UPLOADOLD'], 'derived' : ['UPLOADOLD','UPLOAD','LOYALTY'],'noOfUserUpload' : 5})
        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        messageId = constant.config['node'][campaignType][testControlType]['LIST']['DERIVED'][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['RESPONSE']['json']['entity']['id']
        getMessageResponse = GetMessage.getMessageById(campaignId, messageId)
        GetMessage.assertResponse(getMessageResponse, 200)
        CreateMessageDBAssertion(campaignId, messageId, getMessageResponse['json']['entity']).check()

    @pytest.mark.parametrize('campaignType,testControlType,channel,messageInfo', [
        ('LIVE', 'ORG', 'EMAIL',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': True, 'skipRateLimit': True}),
    ])
    def irisv2_message_create_execute_get_derived_derived_EMAIL_immediate_plain_additionalProperties_UsingEncryptURL(
            self,
            campaignType,
            testControlType,
            channel,
            messageInfo):
        CreateMessage.create(campaignType, testControlType, 'DERIVED', channel, messageInfo,
                             derivedListInfo={'includedGroups' : ['UPLOAD', 'LOYALTY', 'DERIVED'],'excludedGroup' : ['UPLOADOLD'], 'derived' : ['UPLOADOLD','UPLOAD','LOYALTY'],'noOfUserUpload' : 5})
        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        messageId = constant.config['node'][campaignType][testControlType]['LIST']['DERIVED'][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['RESPONSE']['json']['entity']['id']
        getMessageResponse = GetMessage.getMessageById(campaignId, messageId)
        GetMessage.assertResponse(getMessageResponse, 200)
        CreateMessageDBAssertion(campaignId, messageId, getMessageResponse['json']['entity']).check()

    @pytest.mark.parametrize('campaignType,testControlType,channel,messageInfo', [
        ('LIVE', 'ORG', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': False}),
    ])
    def irisv2_message_create_execute_get_derived_derived_SMS_immediate_plain_additionalProperties_UsingRateLimit(self,
                                                                                                                  campaignType,
                                                                                                                  testControlType,
                                                                                                                  channel,
                                                                                                                  messageInfo):
        CreateMessage.create(campaignType, testControlType, 'DERIVED', channel, messageInfo,
                             derivedListInfo={'includedGroups' : ['UPLOAD', 'LOYALTY', 'DERIVED'],'excludedGroup' : ['UPLOADOLD'], 'derived' : ['UPLOADOLD','UPLOAD','LOYALTY'],'noOfUserUpload' : 5})
        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        messageId = constant.config['node'][campaignType][testControlType]['LIST']['DERIVED'][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['RESPONSE']['json']['entity']['id']
        getMessageResponse = GetMessage.getMessageById(campaignId, messageId)
        GetMessage.assertResponse(getMessageResponse, 200)
        CreateMessageDBAssertion(campaignId, messageId, getMessageResponse['json']['entity']).check()

    @pytest.mark.parametrize('campaignType,testControlType,channel,messageInfo', [
        ('LIVE', 'ORG', 'EMAIL',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': False}),
    ])
    def irisv2_message_create_execute_get_derived_derived_EMAIL_immediate_plain_additionalProperties_UsingRateLimit(
            self,
            campaignType,
            testControlType,
            channel,
            messageInfo):
        CreateMessage.create(campaignType, testControlType, 'DERIVED', channel, messageInfo,
                             derivedListInfo={'includedGroups' : ['UPLOAD', 'LOYALTY', 'DERIVED'],'excludedGroup' : ['UPLOADOLD'], 'derived' : ['UPLOADOLD','UPLOAD','LOYALTY'],'noOfUserUpload' : 5})
        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        messageId = constant.config['node'][campaignType][testControlType]['LIST']['DERIVED'][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['RESPONSE']['json']['entity']['id']
        getMessageResponse = GetMessage.getMessageById(campaignId, messageId)
        GetMessage.assertResponse(getMessageResponse, 200)
        CreateMessageDBAssertion(campaignId, messageId, getMessageResponse['json']['entity']).check()

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
    def irisv2_message_create_execute_get_derived_derived_SMS_immediate_coupon(self, campaignType,
                                                                                      testControlType,
                                                                                      channel, messageInfo):
        CreateMessage.create(campaignType, testControlType, 'DERIVED', channel, messageInfo,
                             derivedListInfo={'includedGroups' : ['UPLOAD', 'LOYALTY', 'DERIVED'],'excludedGroup' : ['UPLOADOLD'], 'derived' : ['UPLOADOLD','UPLOAD','LOYALTY'],'noOfUserUpload' : 5})
        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        messageId = constant.config['node'][campaignType][testControlType]['LIST']['DERIVED'][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['RESPONSE']['json']['entity']['id']
        getMessageResponse = GetMessage.getMessageById(campaignId, messageId)
        GetMessage.assertResponse(getMessageResponse, 200)
        CreateMessageDBAssertion(campaignId, messageId, getMessageResponse['json']['entity']).check()

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
    def irisv2_message_create_execute_get_derived_derived_EMAIL_immediate_coupon(self, campaignType,
                                                                                        testControlType,
                                                                                        channel, messageInfo):
        CreateMessage.create(campaignType, testControlType, 'DERIVED', channel, messageInfo,
                             derivedListInfo={'includedGroups' : ['UPLOAD', 'LOYALTY', 'DERIVED'],'excludedGroup' : ['UPLOADOLD'], 'derived' : ['UPLOADOLD','UPLOAD','LOYALTY'],'noOfUserUpload' : 5})
        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        messageId = constant.config['node'][campaignType][testControlType]['LIST']['DERIVED'][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['RESPONSE']['json']['entity']['id']
        getMessageResponse = GetMessage.getMessageById(campaignId, messageId)
        GetMessage.assertResponse(getMessageResponse, 200)
        CreateMessageDBAssertion(campaignId, messageId, getMessageResponse['json']['entity']).check()

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
    def irisv2_message_create_execute_get_derived_derived_SMS_immediate_points(self, campaignType, testControlType,
                                                                               channel, messageInfo):
        CreateMessage.create(campaignType, testControlType, 'DERIVED', channel, messageInfo,
                             derivedListInfo={'includedGroups' : ['UPLOAD', 'LOYALTY', 'DERIVED'],'excludedGroup' : ['UPLOADOLD'], 'derived' : ['UPLOADOLD','UPLOAD','LOYALTY'],'noOfUserUpload' : 5})
        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        messageId = constant.config['node'][campaignType][testControlType]['LIST']['DERIVED'][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['RESPONSE']['json']['entity']['id']
        getMessageResponse = GetMessage.getMessageById(campaignId, messageId)
        GetMessage.assertResponse(getMessageResponse, 200)
        CreateMessageDBAssertion(campaignId, messageId, getMessageResponse['json']['entity']).check()

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
    def irisv2_message_create_execute_get_derived_derived_EMAIL_immediate_points(self, campaignType, testControlType,
                                                                                 channel, messageInfo):
        CreateMessage.create(campaignType, testControlType, 'DERIVED', channel, messageInfo,
                             derivedListInfo={'includedGroups' : ['UPLOAD', 'LOYALTY', 'DERIVED'],'excludedGroup' : ['UPLOADOLD'], 'derived' : ['UPLOADOLD','UPLOAD','LOYALTY'],'noOfUserUpload' : 5})
        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        messageId = constant.config['node'][campaignType][testControlType]['LIST']['DERIVED'][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['RESPONSE']['json']['entity']['id']
        getMessageResponse = GetMessage.getMessageById(campaignId, messageId)
        GetMessage.assertResponse(getMessageResponse, 200)
        CreateMessageDBAssertion(campaignId, messageId, getMessageResponse['json']['entity']).check()

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
    def irisv2_message_create_execute_get_derived_derived_SMS_particularDate_plain(self, campaignType,
                                                                                          testControlType,
                                                                                          channel, messageInfo):
        CreateMessage.create(campaignType, testControlType, 'DERIVED', channel, messageInfo,
                             derivedListInfo={'includedGroups' : ['UPLOAD', 'LOYALTY', 'DERIVED'],'excludedGroup' : ['UPLOADOLD'], 'derived' : ['UPLOADOLD','UPLOAD','LOYALTY'],'noOfUserUpload' : 5})
        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        messageId = constant.config['node'][campaignType][testControlType]['LIST']['DERIVED'][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['RESPONSE']['json']['entity']['id']
        getMessageResponse = GetMessage.getMessageById(campaignId, messageId)
        GetMessage.assertResponse(getMessageResponse, 200)
        CreateMessageDBAssertion(campaignId, messageId, getMessageResponse['json']['entity']).check()

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
    def irisv2_message_create_execute_get_derived_derived_EMAIL_particularDate_plain(self, campaignType,
                                                                                            testControlType,
                                                                                            channel, messageInfo):
        CreateMessage.create(campaignType, testControlType, 'DERIVED', channel, messageInfo,
                             derivedListInfo={'includedGroups' : ['UPLOAD', 'LOYALTY', 'DERIVED'],'excludedGroup' : ['UPLOADOLD'], 'derived' : ['UPLOADOLD','UPLOAD','LOYALTY'],'noOfUserUpload' : 5})
        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        messageId = constant.config['node'][campaignType][testControlType]['LIST']['DERIVED'][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['RESPONSE']['json']['entity']['id']
        getMessageResponse = GetMessage.getMessageById(campaignId, messageId)
        GetMessage.assertResponse(getMessageResponse, 200)
        CreateMessageDBAssertion(campaignId, messageId, getMessageResponse['json']['entity']).check()

    @pytest.mark.parametrize('campaignType,testControlType,channel,messageInfo', [
        ('LIVE', 'ORG', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': True, 'encryptUrl': False, 'skipRateLimit': True}),
    ])
    def irisv2_message_create_execute_get_derived_Derived_SMS_particularDate_plain_UsingTinyURL(self, campaignType,
                                                                                                testControlType,
                                                                                                channel, messageInfo):
        CreateMessage.create(campaignType, testControlType, 'DERIVED', channel, messageInfo,
                             derivedListInfo={'includedGroups' : ['UPLOAD', 'LOYALTY', 'DERIVED'],'excludedGroup' : ['UPLOADOLD'], 'derived' : ['UPLOADOLD','UPLOAD','LOYALTY'],'noOfUserUpload' : 5})
        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        messageId = constant.config['node'][campaignType][testControlType]['LIST']['DERIVED'][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['RESPONSE']['json']['entity']['id']
        getMessageResponse = GetMessage.getMessageById(campaignId, messageId)
        GetMessage.assertResponse(getMessageResponse, 200)
        CreateMessageDBAssertion(campaignId, messageId, getMessageResponse['json']['entity']).check()

    @pytest.mark.parametrize('campaignType,testControlType,channel,messageInfo', [
        ('LIVE', 'ORG', 'EMAIL',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': True, 'encryptUrl': False, 'skipRateLimit': True}),
    ])
    def irisv2_message_create_execute_get_derived_Derived_EMAIL_particularDate_plain_UsingTinyURL(self, campaignType,
                                                                                                  testControlType,
                                                                                                  channel, messageInfo):
        CreateMessage.create(campaignType, testControlType, 'DERIVED', channel, messageInfo,
                             derivedListInfo={'includedGroups' : ['UPLOAD', 'LOYALTY', 'DERIVED'],'excludedGroup' : ['UPLOADOLD'], 'derived' : ['UPLOADOLD','UPLOAD','LOYALTY'],'noOfUserUpload' : 5})
        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        messageId = constant.config['node'][campaignType][testControlType]['LIST']['DERIVED'][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['RESPONSE']['json']['entity']['id']
        getMessageResponse = GetMessage.getMessageById(campaignId, messageId)
        GetMessage.assertResponse(getMessageResponse, 200)
        CreateMessageDBAssertion(campaignId, messageId, getMessageResponse['json']['entity']).check()

    @pytest.mark.parametrize('campaignType,testControlType,channel,messageInfo', [
        ('LIVE', 'ORG', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': True, 'skipRateLimit': True}),
    ])
    def irisv2_message_create_execute_get_derived_derived_SMS_particularDate_plain_UsingEncryptURL(self, campaignType,
                                                                                                   testControlType,
                                                                                                   channel,
                                                                                                   messageInfo):
        CreateMessage.create(campaignType, testControlType, 'DERIVED', channel, messageInfo,
                             derivedListInfo={'includedGroups' : ['UPLOAD', 'LOYALTY', 'DERIVED'],'excludedGroup' : ['UPLOADOLD'], 'derived' : ['UPLOADOLD','UPLOAD','LOYALTY'],'noOfUserUpload' : 5})
        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        messageId = constant.config['node'][campaignType][testControlType]['LIST']['DERIVED'][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['RESPONSE']['json']['entity']['id']
        getMessageResponse = GetMessage.getMessageById(campaignId, messageId)
        GetMessage.assertResponse(getMessageResponse, 200)
        CreateMessageDBAssertion(campaignId, messageId, getMessageResponse['json']['entity']).check()

    @pytest.mark.parametrize('campaignType,testControlType,channel,messageInfo', [
        ('LIVE', 'ORG', 'EMAIL',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': True, 'skipRateLimit': True}),
    ])
    def irisv2_message_create_execute_get_derived_derived_EMAIL_particularDate_plain_UsingEncryptURL(self, campaignType,
                                                                                                     testControlType,
                                                                                                     channel,
                                                                                                     messageInfo):
        CreateMessage.create(campaignType, testControlType, 'DERIVED', channel, messageInfo,
                             derivedListInfo={'includedGroups' : ['UPLOAD', 'LOYALTY', 'DERIVED'],'excludedGroup' : ['UPLOADOLD'], 'derived' : ['UPLOADOLD','UPLOAD','LOYALTY'],'noOfUserUpload' : 5})
        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        messageId = constant.config['node'][campaignType][testControlType]['LIST']['DERIVED'][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['RESPONSE']['json']['entity']['id']
        getMessageResponse = GetMessage.getMessageById(campaignId, messageId)
        GetMessage.assertResponse(getMessageResponse, 200)
        CreateMessageDBAssertion(campaignId, messageId, getMessageResponse['json']['entity']).check()

    @pytest.mark.parametrize('campaignType,testControlType,channel,messageInfo', [
        ('LIVE', 'ORG', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': False}),
    ])
    def irisv2_message_create_execute_get_derived_derived_SMS_particularDate_plain_UsingRateLimit(self, campaignType,
                                                                                                  testControlType,
                                                                                                  channel, messageInfo):
        CreateMessage.create(campaignType, testControlType, 'DERIVED', channel, messageInfo,
                             derivedListInfo={'includedGroups' : ['UPLOAD', 'LOYALTY', 'DERIVED'],'excludedGroup' : ['UPLOADOLD'], 'derived' : ['UPLOADOLD','UPLOAD','LOYALTY'],'noOfUserUpload' : 5})
        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        messageId = constant.config['node'][campaignType][testControlType]['LIST']['DERIVED'][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['RESPONSE']['json']['entity']['id']
        getMessageResponse = GetMessage.getMessageById(campaignId, messageId)
        GetMessage.assertResponse(getMessageResponse, 200)
        CreateMessageDBAssertion(campaignId, messageId, getMessageResponse['json']['entity']).check()

    @pytest.mark.parametrize('campaignType,testControlType,channel,messageInfo', [
        ('LIVE', 'ORG', 'EMAIL',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': False}),
    ])
    def irisv2_message_create_execute_get_derived_derived_EMAIL_particularDate_plain_UsingRateLimit(self, campaignType,
                                                                                                    testControlType,
                                                                                                    channel,
                                                                                                    messageInfo):
        CreateMessage.create(campaignType, testControlType, 'DERIVED', channel, messageInfo,
                             derivedListInfo={'includedGroups' : ['UPLOAD', 'LOYALTY', 'DERIVED'],'excludedGroup' : ['UPLOADOLD'], 'derived' : ['UPLOADOLD','UPLOAD','LOYALTY'],'noOfUserUpload' : 5})
        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        messageId = constant.config['node'][campaignType][testControlType]['LIST']['DERIVED'][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['RESPONSE']['json']['entity']['id']
        getMessageResponse = GetMessage.getMessageById(campaignId, messageId)
        GetMessage.assertResponse(getMessageResponse, 200)
        CreateMessageDBAssertion(campaignId, messageId, getMessageResponse['json']['entity']).check()

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
    def irisv2_message_create_execute_get_derived_derived_SMS_particularDate_coupon(self, campaignType,
                                                                                           testControlType,
                                                                                           channel, messageInfo):
        CreateMessage.create(campaignType, testControlType, 'DERIVED', channel, messageInfo,
                             derivedListInfo={'includedGroups' : ['UPLOAD', 'LOYALTY', 'DERIVED'],'excludedGroup' : ['UPLOADOLD'], 'derived' : ['UPLOADOLD','UPLOAD','LOYALTY'],'noOfUserUpload' : 5})
        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        messageId = constant.config['node'][campaignType][testControlType]['LIST']['DERIVED'][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['RESPONSE']['json']['entity']['id']
        getMessageResponse = GetMessage.getMessageById(campaignId, messageId)
        GetMessage.assertResponse(getMessageResponse, 200)
        CreateMessageDBAssertion(campaignId, messageId, getMessageResponse['json']['entity']).check()

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
    def irisv2_message_create_execute_get_derived_derived_EMAIL_particularDate_coupon(self, campaignType,
                                                                                             testControlType,
                                                                                             channel, messageInfo):
        CreateMessage.create(campaignType, testControlType, 'DERIVED', channel, messageInfo,
                             derivedListInfo={'includedGroups' : ['UPLOAD', 'LOYALTY', 'DERIVED'],'excludedGroup' : ['UPLOADOLD'], 'derived' : ['UPLOADOLD','UPLOAD','LOYALTY'],'noOfUserUpload' : 5})
        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        messageId = constant.config['node'][campaignType][testControlType]['LIST']['DERIVED'][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['RESPONSE']['json']['entity']['id']
        getMessageResponse = GetMessage.getMessageById(campaignId, messageId)
        GetMessage.assertResponse(getMessageResponse, 200)
        CreateMessageDBAssertion(campaignId, messageId, getMessageResponse['json']['entity']).check()

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
    def est_irisv2_message_create_execute_get_derived_derived_SMS_particularDate_points(self, campaignType, testControlType,
                                                                                   channel, messageInfo):
        CreateMessage.create(campaignType, testControlType, 'DERIVED', channel, messageInfo,
                             derivedListInfo={'includedGroups' : ['UPLOAD', 'LOYALTY', 'DERIVED'],'excludedGroup' : ['UPLOADOLD'], 'derived' : ['UPLOADOLD','UPLOAD','LOYALTY'],'noOfUserUpload' : 5})
        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        messageId = constant.config['node'][campaignType][testControlType]['LIST']['DERIVED'][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['RESPONSE']['json']['entity']['id']
        getMessageResponse = GetMessage.getMessageById(campaignId, messageId)
        GetMessage.assertResponse(getMessageResponse, 200)
        CreateMessageDBAssertion(campaignId, messageId, getMessageResponse['json']['entity']).check()

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
    def est_irisv2_message_create_execute_get_derived_derived_EMAIL_particularDate_points(self, campaignType,
                                                                                     testControlType,
                                                                                     channel, messageInfo):
        CreateMessage.create(campaignType, testControlType, 'DERIVED', channel, messageInfo,
                             derivedListInfo={'includedGroups' : ['UPLOAD', 'LOYALTY', 'DERIVED'],'excludedGroup' : ['UPLOADOLD'], 'derived' : ['UPLOADOLD','UPLOAD','LOYALTY'],'noOfUserUpload' : 5})
        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        messageId = constant.config['node'][campaignType][testControlType]['LIST']['DERIVED'][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['RESPONSE']['json']['entity']['id']
        getMessageResponse = GetMessage.getMessageById(campaignId, messageId)
        GetMessage.assertResponse(getMessageResponse, 200)
        CreateMessageDBAssertion(campaignId, messageId, getMessageResponse['json']['entity']).check()