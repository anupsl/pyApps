import pytest,time

from src.Constant.constant import constant
from src.Constant.orgDetails import OrgDetails
from src.modules.irisv2.message.createMessage import CreateMessage
from src.modules.irisv2.message.createMessageDbAssertion import CreateMessageDBAssertion
from src.utilities.logger import Logger
from src.utilities.utils import Utils
from src.modules.irisv2.list.createAudience import CreateAudience
from src.modules.irisv2.helper.irisHelper import IrisHelper
from src.modules.irisv2.message.authorizeMessage import AuthorizeMessage
from src.modules.irisv2.campaigns.createCampaign import CreateCampaign
from src.utilities.assertion import Assertion
from src.dbCalls.messageInfo import message_calls

class Test_MessageEdit_ParticularDate_Live_Create():
    def setup_method(self, method):
        Logger.logMethodName(method.__name__)

    def setup_class(self):
        Logger.logSuiteName(str(self).split('.')[-1])
        self.listInfo = CreateAudience.uploadList('LIVE', 'ORG')
        self.listInfoFilter = CreateAudience.FilterList('LIVE', 'ORG')

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo,editInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True},
         {'schedule':{'scheduleType': 'IMMEDIATE'}})
    ])
    def irisv2_message_edit_particularDate_live_create_plain_mobile_schedulle_body_Sanity(self, campaignType, testControlType, listType,
                                                                        channel, messageInfo,editInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True, lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION')
        editInfo = CreateMessage.edit(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                      messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],
                                      editInfo)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 editInfo['RESPONSE']['json']['entity']['id'], editInfo['PAYLOAD'],version=1).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo,editInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True},
         {'schedule': {'scheduleType': 'IMMEDIATE'}}),
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True},
         {'schedule': {'scheduleType': 'IMMEDIATE'}}),
        ('LIVE', 'ORG', 'LOYALTY', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True},
         {'schedule': {'scheduleType': 'RECURRING', 'startDate': Utils.getTime(minutes=10, milliSeconds=True),
                       'endDate': Utils.getTime(minutes=40, milliSeconds=True), 'repeatOn': [1], 'hour': 10,
                       'repeatType': 'DAILY', 'minute': 10}}),
        ('LIVE', 'ORG', 'LOYALTY', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True},
         {'schedule': {'scheduleType': 'RECURRING', 'startDate': Utils.getTime(minutes=10, milliSeconds=True),
                       'endDate': Utils.getTime(minutes=40, milliSeconds=True), 'repeatOn': [1], 'hour': 10,
                       'repeatType': 'DAILY', 'minute': 10}}),
        ('LIVE', 'ORG', 'LOYALTY', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True},
         {'schedule': {'scheduleType': 'RECURRING', 'startDate': Utils.getTime(minutes=10, milliSeconds=True),
                       'endDate': Utils.getTime(minutes=40, milliSeconds=True), 'repeatOn': [1], 'hour': 10,
                       'repeatType': 'DAILY', 'minute': 10}})
    ])
    def irisv2_message_edit_particularDate_live_create_plain_mobile_schedulle_body(self, campaignType,
                                                                                   testControlType, listType,
                                                                                   channel, messageInfo,
                                                                                   editInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True, lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION')
        editInfo = CreateMessage.edit(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                      messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],
                                      editInfo)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 editInfo['RESPONSE']['json']['entity']['id'], editInfo['PAYLOAD'],version=1).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo,editInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'EMAIL',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True},
         {'schedule': {'scheduleType': 'IMMEDIATE'}})
    ])
    def irisv2_message_edit_particularDate_live_create_plain_email_schedulle_body_Sanity(self, campaignType,
                                                                                         testControlType, listType,
                                                                                         channel, messageInfo,
                                                                                         editInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True, lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION')
        editInfo = CreateMessage.edit(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                      messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],
                                      editInfo)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 editInfo['RESPONSE']['json']['entity']['id'], editInfo['PAYLOAD'],version=1).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo,editInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'EMAIL',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True},
         {'schedule': {'scheduleType': 'IMMEDIATE'}}),
        ('LIVE', 'ORG', 'UPLOAD', 'EMAIL',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True},
         {'schedule': {'scheduleType': 'IMMEDIATE'}}),
        ('LIVE', 'ORG', 'LOYALTY', 'EMAIL',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True},
         {'schedule': {'scheduleType': 'RECURRING', 'startDate': Utils.getTime(minutes=10, milliSeconds=True),
                       'endDate': Utils.getTime(minutes=40, milliSeconds=True), 'repeatOn': [1], 'hour': 10,
                       'repeatType': 'DAILY', 'minute': 10}}),
        ('LIVE', 'ORG', 'LOYALTY', 'EMAIL',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True},
         {'schedule': {'scheduleType': 'RECURRING', 'startDate': Utils.getTime(minutes=10, milliSeconds=True),
                       'endDate': Utils.getTime(minutes=40, milliSeconds=True), 'repeatOn': [1], 'hour': 10,
                       'repeatType': 'DAILY', 'minute': 10}}),
        ('LIVE', 'ORG', 'LOYALTY', 'EMAIL',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True},
         {'schedule': {'scheduleType': 'RECURRING', 'startDate': Utils.getTime(minutes=10, milliSeconds=True),
                       'endDate': Utils.getTime(minutes=40, milliSeconds=True), 'repeatOn': [1], 'hour': 10,
                       'repeatType': 'DAILY', 'minute': 10}})
    ])
    def irisv2_message_edit_particularDate_live_create_plain_email_schedulle_body(self, campaignType,
                                                                                  testControlType, listType,
                                                                                  channel, messageInfo,
                                                                                  editInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True, lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION')
        editInfo = CreateMessage.edit(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                      messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],
                                      editInfo)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 editInfo['RESPONSE']['json']['entity']['id'], editInfo['PAYLOAD'],version=1).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo,editInfo', [
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
         {'schedule': {'scheduleType': 'IMMEDIATE'}})
    ])
    def irisv2_message_edit_particularDate_live_create_plain_mobilePush_schedulle_body_Sanity(self, campaignType,
                                                                                              testControlType, listType,
                                                                                              channel, messageInfo,
                                                                                              editInfo):
        actualOrgId = IrisHelper.updateOrgId(constant.config['mobilepush']['orgId'])
        try:
            campaignInfo = CreateCampaign.create(campaignType, testControlType, updateNode=True, lockNode=True)
            messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                                  campaignId=campaignInfo['ID'],
                                                  updateNode=True, lockNode=True)
            CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
            message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'],
                                                           'VARIANT_CREATION')
            editInfo = CreateMessage.edit(campaignInfo['ID'],
                                          messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],
                                          editInfo)
            CreateMessageDBAssertion(campaignInfo['ID'],
                                     editInfo['RESPONSE']['json']['entity']['id'], editInfo['PAYLOAD'],version=1).check()
        finally:
            IrisHelper.updateOrgId(actualOrgId)

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo,editInfo', [
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
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True},
         {'schedule': {'scheduleType': 'IMMEDIATE'}}),
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
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True},
         {'schedule': {'scheduleType': 'IMMEDIATE'}})
    ])
    def irisv2_message_edit_particularDate_live_create_plain_mobilePush_schedulle_body(self, campaignType,
                                                                                       testControlType, listType,
                                                                                       channel, messageInfo,
                                                                                       editInfo):
        actualOrgId = IrisHelper.updateOrgId(constant.config['mobilepush']['orgId'])
        try:
            campaignInfo = CreateCampaign.create(campaignType, testControlType, updateNode=True, lockNode=True)
            messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                                  campaignId=campaignInfo['ID'],
                                                  updateNode=True, lockNode=True)
            CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
            message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'],
                                                           'VARIANT_CREATION')
            editInfo = CreateMessage.edit(campaignInfo['ID'],
                                          messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],
                                          editInfo)
            CreateMessageDBAssertion(campaignInfo['ID'],
                                     editInfo['RESPONSE']['json']['entity']['id'], editInfo['PAYLOAD'],version=1).check()
        finally:
            IrisHelper.updateOrgId(actualOrgId)

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [

        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def irisv2_message_edit_particularDate_live_create_plain_mobile_targetAudience_body(self, campaignType,
                                                                                        testControlType, listType,
                                                                                        channel, messageInfo):

        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True, lockNode=True)
        messageDetails['PAYLOAD']['targetAudience']['include'] = [self.listInfoFilter['ID']]
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION')
        editInfo = CreateMessage.edit(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                      messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'])
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 editInfo['RESPONSE']['json']['entity']['id'], editInfo['PAYLOAD'],version=1).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo,keys', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}, 'useTinyUrl'),
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': True, 'encryptUrl': False, 'skipRateLimit': True}, 'useTinyUrl'),
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True},
         'skipRateLimit'),
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': True, 'encryptUrl': False, 'skipRateLimit': False},
         'skipRateLimit'),
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True},
         'encryptUrl'),
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': True, 'encryptUrl': True, 'skipRateLimit': False},
         'encryptUrl'),

    ])
    def irisv2_message_edit_particularDate_live_create_plain_mobile_additionalSettings_body(self, campaignType,
                                                                                            testControlType,
                                                                                            listType,
                                                                                            channel, messageInfo,
                                                                                            keys):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True, lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION')
        messageDetails['PAYLOAD']['deliverySetting']['additionalSetting'][keys] = not messageDetails['PAYLOAD']['deliverySetting']['additionalSetting'][keys]

        editInfo = CreateMessage.edit(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                      messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'])
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 editInfo['RESPONSE']['json']['entity']['id'], editInfo['PAYLOAD'],version=1).check()

    @pytest.mark.skipif(constant.config['cluster'] not in ['nightly'],
                        reason='Channel Setting update Only Set for Nightly Cluster')
    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def irisv2_message_edit_particularDate_live_create_plain_mobile_channleSetting_body(self, campaignType,
                                                                                        testControlType, listType,
                                                                                        channel, messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True, lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION')
        messageDetails['PAYLOAD']['deliverySetting']['channelSetting'] = constant.config['channelSetting']
        editInfo = CreateMessage.edit(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                      messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'])
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 editInfo['RESPONSE']['json']['entity']['id'], editInfo['PAYLOAD'],version=1).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def irisv2_message_edit_particularDate_live_create_plain_mobile_storeType_body(self, campaignType,
                                                                                   testControlType, listType,
                                                                                   channel, messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True, lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION')
        messageDetails['PAYLOAD']['messageContent']['message_content_id_1']['storeType'] = 'LAST_TRANSACTED_AT'
        editInfo = CreateMessage.edit(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                      messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'])
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 editInfo['RESPONSE']['json']['entity']['id'], editInfo['PAYLOAD'],version=1).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def irisv2_message_edit_particularDate_live_create_plain_mobile_messageBody_body(self, campaignType,
                                                                                   testControlType, listType,
                                                                                   channel, messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True, lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION')
        messageDetails['PAYLOAD']['messageContent']['message_content_id_1'][
            'messageBody'] = 'updated message body {{first_name}} {{last_name}} {{fullname}} {{optout}}'
        editInfo = CreateMessage.edit(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                      messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'])
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 editInfo['RESPONSE']['json']['entity']['id'], editInfo['PAYLOAD'],version=1).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def irisv2_message_edit_particularDate_live_create_plain_mobile_channel_body(self, campaignType,
                                                                                     testControlType, listType,
                                                                                     channel, messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True, lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION')
        messageDetails['PAYLOAD']['messageContent']['message_content_id_1'][
            'channel'] = 'EMAIL'
        messageDetails['PAYLOAD']['messageContent']['message_content_id_1'].pop('messageBody')
        messageDetails['PAYLOAD']['messageContent']['message_content_id_1']['emailBody'] = 'sms to email change {{unsubscribe}}'
        messageDetails['PAYLOAD']['messageContent']['message_content_id_1'][
            'emailSubject'] = 'email subject'
        editInfo = CreateMessage.edit(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                      messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'])
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 editInfo['RESPONSE']['json']['entity']['id'], editInfo['PAYLOAD'],version=1).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def irisv2_message_edit_particularDate_live_create_plain_mobile_sms_to_mobilePush_body(self, campaignType,
                                                                                 testControlType, listType,
                                                                                 channel, messageInfo):
        actualOrgId = IrisHelper.updateOrgId(constant.config['mobilepush']['orgId'])
        try:
            campaignInfo = CreateCampaign.create(campaignType, testControlType, updateNode=True, lockNode=True)
            listInfo = CreateAudience.uploadList(campaignType, testControlType, schemaIdentifier=['USER_ID'],
                                                 schemaData=['USER_ID'], newUser=False, updateNode=True, lockNode=True,
                                                 campaignCheck=False, mobilePush=True)
            messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                                  listInfo=listInfo,
                                                  campaignId=campaignInfo['ID'],
                                                  updateNode=True, lockNode=True)
            CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
            message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'],
                                                           'VARIANT_CREATION')
            messageDetails['PAYLOAD']['messageContent'] = CreateMessage.constructMessageContent(campaignType,
                                                                                                testControlType,
                                                                                                {'type': 'DEFAULT',
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
                                                                                                messageInfo[
                                                                                                    'offerType'],
                                                                                                'MOBILE_PUSH',
                                                                                                storeType='REGISTERED_STORE',
                                                                                                numberOfCustomTag=0)
            messageDetails['PAYLOAD']['deliverySetting'] = CreateMessage.constructDeliverySetting(['MOBILE_PUSH'],
                                                                                                  messageInfo[
                                                                                                      'useTinyUrl'],
                                                                                                  messageInfo[
                                                                                                      'encryptUrl'],
                                                                                                  messageInfo[
                                                                                                      'skipRateLimit'],
                                                                                                  maxUsers=[])
            editInfo = CreateMessage.edit(campaignInfo['ID'], messageDetails['RESPONSE']['json']['entity']['id'],
                                          messageDetails['PAYLOAD'])
            CreateMessageDBAssertion(campaignInfo['ID'], editInfo['RESPONSE']['json']['entity']['id'],
                                     editInfo['PAYLOAD'], version=1).check()
        finally:
            IrisHelper.updateOrgId(actualOrgId)

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
    ])
    def irisv2_message_edit_particularDate_live_create_plain_mobile_coupon_sms_to_mobilePush_body(self, campaignType,
                                                                                                testControlType,
                                                                                                listType,
                                                                                                channel, messageInfo):
        actualOrgId = IrisHelper.updateOrgId(constant.config['mobilepush']['orgId'])
        try:
            campaignInfo = CreateCampaign.create(campaignType, testControlType, updateNode=True, lockNode=True)
            couponSeriesId = CreateMessage.getCouponSeriesId(campaignInfo['ID'])
            listInfo = CreateAudience.uploadList(campaignType, testControlType, schemaIdentifier=['USER_ID'],
                                                 schemaData=['USER_ID'], newUser=False, updateNode=True, lockNode=True,
                                                 campaignCheck=False, mobilePush=True)
            messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                                  listInfo=listInfo,
                                                  campaignId=campaignInfo['ID'],
                                                  updateNode=True, lockNode=True)
            CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
            message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'],
                                                           'VARIANT_CREATION')
            messageDetails['PAYLOAD']['messageContent'] = CreateMessage.constructMessageContent(campaignType,
                                                                                                testControlType,
                                                                                                {'type': 'DEFAULT',
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
                                                                                                messageInfo[
                                                                                                    'offerType'],
                                                                                                'MOBILE_PUSH',
                                                                                                storeType='REGISTERED_STORE',
                                                                                                numberOfCustomTag=0)
            messageDetails['PAYLOAD']['messageContent']['message_content_id_1']['offers'][0][
                'couponSeriesId'] = couponSeriesId
            messageDetails['PAYLOAD']['deliverySetting'] = CreateMessage.constructDeliverySetting(['MOBILE_PUSH'],
                                                                                                  messageInfo[
                                                                                                      'useTinyUrl'],
                                                                                                  messageInfo[
                                                                                                      'encryptUrl'],
                                                                                                  messageInfo[
                                                                                                      'skipRateLimit'],
                                                                                                  maxUsers=[])
            editInfo = CreateMessage.edit(campaignInfo['ID'], messageDetails['RESPONSE']['json']['entity']['id'],
                                          messageDetails['PAYLOAD'])
            CreateMessageDBAssertion(campaignInfo['ID'], editInfo['RESPONSE']['json']['entity']['id'],
                                     editInfo['PAYLOAD'], version=1).check()
        finally:
            IrisHelper.updateOrgId(actualOrgId)

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def irisv2_message_edit_particularDate_live_create_plain_mobile_plain_points_message_to_couponMessage(self, campaignType,
                                                                                          testControlType, listType,
                                                                                          channel, messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True, lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION')
        messageDetails['PAYLOAD']['messageContent'] = CreateMessage.constructMessageContent(campaignType, testControlType,
                                                                          messageInfo['messageStrategy'],
                                                                          'COUPON',
                                                                          channel,
                                                                          storeType='REGISTERED_STORE',
                                                                          numberOfCustomTag=0)
        editInfo = CreateMessage.edit(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                      messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'])
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 editInfo['RESPONSE']['json']['entity']['id'], editInfo['PAYLOAD'],version=1).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def irisv2_message_edit_particularDate_live_create_plain_mobile_plain_coupon_message_to_pointsMessage(self,
                                                                                                          campaignType,
                                                                                                          testControlType,
                                                                                                          listType,
                                                                                                          channel,
                                                                                                          messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True, lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION')
        messageDetails['PAYLOAD']['messageContent'] = CreateMessage.constructMessageContent(campaignType,
                                                                                            testControlType,
                                                                                            messageInfo[
                                                                                                'messageStrategy'],
                                                                                            'POINTS',
                                                                                            channel,
                                                                                            storeType='REGISTERED_STORE',
                                                                                            numberOfCustomTag=0)
        editInfo = CreateMessage.edit(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                      messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'])
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 editInfo['RESPONSE']['json']['entity']['id'], editInfo['PAYLOAD'],version=1).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def irisv2_message_edit_particularDate_live_create_plain_mobile_points_coupon_message_to_plainMessage(self,
                                                                                                          campaignType,
                                                                                                          testControlType,
                                                                                                          listType,
                                                                                                          channel,
                                                                                                          messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True, lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION')
        messageDetails['PAYLOAD']['messageContent'] = CreateMessage.constructMessageContent(campaignType,
                                                                                            testControlType,
                                                                                            messageInfo[
                                                                                                'messageStrategy'],
                                                                                            'PLAIN',
                                                                                            channel,
                                                                                            storeType='REGISTERED_STORE',
                                                                                            numberOfCustomTag=0)
        editInfo = CreateMessage.edit(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                      messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'])
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 editInfo['RESPONSE']['json']['entity']['id'], editInfo['PAYLOAD'],version=1).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def irisv2_message_edit_particularDate_live_create_plain_mobile_editMessage_withouChanging_body(self, campaignType,
                                                                                        testControlType, listType,
                                                                                        channel, messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True, lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION')
        editInfo = CreateMessage.edit(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                      messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'])
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 editInfo['RESPONSE']['json']['entity']['id'], editInfo['PAYLOAD'],version=1).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def irisv2_message_edit_particularDate_live_create_plain_mobile_editMessage_multipleTimes_body(self, campaignType,
                                                                                                   testControlType,
                                                                                                   listType,
                                                                                                   channel,
                                                                                                   messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True, lockNode=True)
        messageDetails['PAYLOAD']['targetAudience']['include'] = [self.listInfoFilter['ID']]
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION')
        editInfo = CreateMessage.edit(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                      messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'])
        messageDetails['PAYLOAD']['messageContent'] = CreateMessage.constructMessageContent(campaignType,
                                                                                            testControlType,
                                                                                            messageInfo[
                                                                                                'messageStrategy'],
                                                                                            'COUPON',
                                                                                            channel,
                                                                                            storeType='REGISTERED_STORE',
                                                                                            numberOfCustomTag=0)
        editInfo = CreateMessage.edit(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                      messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'])
        messageDetails['PAYLOAD']['messageContent'] = CreateMessage.constructMessageContent(campaignType,
                                                                                            testControlType,
                                                                                            messageInfo[
                                                                                                'messageStrategy'],
                                                                                            'PLAIN',
                                                                                            channel,
                                                                                            storeType='REGISTERED_STORE',
                                                                                            numberOfCustomTag=0)
        editInfo = CreateMessage.edit(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                      messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'])
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 editInfo['RESPONSE']['json']['entity']['id'], editInfo['PAYLOAD'],version=3).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo,editInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True},
         {'schedule': {'scheduleType': 'PARTICULAR_DATE',
                       'scheduledDate': Utils.getTime(hours=2, milliSeconds=True)}})
    ])
    def irisv2_message_edit_particularDate_live_create_plain_mobile_editMessage_alreadyApproved(self,
                                                                                                         campaignType,
                                                                                                         testControlType,
                                                                                                         listType,
                                                                                                         channel,
                                                                                                         messageInfo,
                                                                                                         editInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION')
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                  messageCreateResponse=messageDetails)
        AuthorizeMessage.assertResponse(approveRespone, 200)
        editInfo = CreateMessage.edit(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                      messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],
                                      editInfo)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 editInfo['RESPONSE']['json']['entity']['id'], editInfo['PAYLOAD'],version=1).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo,editInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True},
         {'schedule': {'scheduleType': 'PARTICULAR_DATE',
                       'scheduledDate': Utils.getTime(hours=2, milliSeconds=True)}})
    ])
    def irisv2_message_edit_particularDate_live_create_plain_mobile_editMessage_expireMessageAndEditTime(self,
                                                                                                     campaignType,
                                                                                                     testControlType,
                                                                                                     listType,
                                                                                                     channel,
                                                                                                     messageInfo,
                                                                                                     editInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        time.sleep(121)
        editInfo = CreateMessage.edit(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                      messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],
                                      editInfo)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 editInfo['RESPONSE']['json']['entity']['id'], editInfo['PAYLOAD'],version=1).check()