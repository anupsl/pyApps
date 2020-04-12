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
from src.modules.irisv2.message.authorizeMessageDbAssertion import AuthorizeMessageDBAssertion

class Test_MessageEdit_Immediate_Live_Execute():
    def setup_method(self, method):
        Logger.logMethodName(method.__name__)

    def setup_class(self):
        Logger.logSuiteName(str(self).split('.')[-1])
        self.listInfo = CreateAudience.uploadList('LIVE', 'ORG')
        self.listInfoFilter = CreateAudience.FilterList('LIVE', 'ORG')
        constant.config['FilterListID'] = CreateAudience.FilterList('LIVE', 'ORG', campaignCheck=False)['ID']
        CreateAudience.getPocUsers()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def irisv2_message_edit_immediate_live_execute_plain_mobile_schedulle_body_Sanity(self, campaignType, testControlType, listType,
                                                                        channel, messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True, lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION')
        messageDetails['PAYLOAD'].update({
            'schedule':{
                'scheduleType': 'PARTICULAR_DATE',
                'scheduledDate': int(time.time() * 1000) + 2 * 60 * 1000
            }
        })
        editInfo = CreateMessage.edit(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                      messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'])
        CreateMessage.assertResponse(editInfo['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(editInfo['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION', version=1)
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                  messageCreateResponse=editInfo)
        AuthorizeMessage.assertResponse(approveRespone, 200)
        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        AuthorizeMessageDBAssertion(campaignId, editInfo['RESPONSE'], editInfo['PAYLOAD'],
                                    testControlType, version=1,).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'CUSTOM', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'SKIP', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def irisv2_message_edit_immediate_live_execute_plain_mobile_targetAudience_Sanity_body(self, campaignType,
                                                                                               testControlType,
                                                                                               listType,
                                                                                               channel, messageInfo):

        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True, lockNode=True)
        messageDetails['PAYLOAD']['targetAudience']['include'] = [self.listInfoFilter['ID']]
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION')
        editInfo = CreateMessage.edit(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                      messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'])
        CreateMessage.assertResponse(editInfo['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(editInfo['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION', version=1)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 editInfo['RESPONSE']['json']['entity']['id'], editInfo['PAYLOAD'], version=1).check()
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                  messageCreateResponse=editInfo)
        AuthorizeMessage.assertResponse(approveRespone, 200)
        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        AuthorizeMessageDBAssertion(campaignId, editInfo['RESPONSE'], editInfo['PAYLOAD'],
                                    testControlType, version=1, ).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def irisv2_message_edit_immediate_live_execute_plain_mobile_schedulle_particualrDate_coupon_body(self, campaignType,
                                                                                          testControlType, listType,
                                                                                          channel, messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True, lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION')
        messageDetails['PAYLOAD'].update({
            'schedule': {
                'scheduleType': 'PARTICULAR_DATE',
                'scheduledDate': int(time.time() * 1000) + 2 * 60 * 1000
            }
        })
        editInfo = CreateMessage.edit(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                      messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'])
        CreateMessage.assertResponse(editInfo['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(editInfo['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION', version=1)
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                  messageCreateResponse=editInfo)
        AuthorizeMessage.assertResponse(approveRespone, 200)
        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        AuthorizeMessageDBAssertion(campaignId, editInfo['RESPONSE'], editInfo['PAYLOAD'],
                                    testControlType, version=1).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'LOYALTY', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def irisv2_message_edit_immediate_live_execute_plain_mobile_schedulle_particualrDate_points_body(self, campaignType,
                                                                                                     testControlType,
                                                                                                     listType,
                                                                                                     channel,
                                                                                                     messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True, lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION')
        messageDetails['PAYLOAD'].update({
            'schedule': {
                'scheduleType': 'PARTICULAR_DATE',
                'scheduledDate': int(time.time() * 1000) + 2 * 60 * 1000
            }
        })
        editInfo = CreateMessage.edit(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                      messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'])
        CreateMessage.assertResponse(editInfo['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(editInfo['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION', version=1)
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                  messageCreateResponse=editInfo)
        AuthorizeMessage.assertResponse(approveRespone, 200)
        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        AuthorizeMessageDBAssertion(campaignId, editInfo['RESPONSE'], editInfo['PAYLOAD'],
                                    testControlType, version=1).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'LOYALTY', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def irisv2_message_edit_immediate_live_execute_plain_mobile_schedulle_recurring_plain_body(self, campaignType,
                                                                                    testControlType, listType,
                                                                                    channel, messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True, lockNode=True)

        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION')
        dateTime = Utils.getTime(hours=5, minutes=32, dateTimeFormat=True)
        messageDetails['PAYLOAD'].update({
            'schedule': {
                'startDate': Utils.getTime(seconds=30, milliSeconds=True),
                'endDate': Utils.getTime(minutes=40, milliSeconds=True),
                'repeatOn': [1],
                'repeatType': 'DAILY',
                'scheduleType': 'RECURRING',
                'hour': int(dateTime[11:13]),
                'minute': int(dateTime[14:16])
            }
        })
        editInfo = CreateMessage.edit(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                      messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'])
        CreateMessage.assertResponse(editInfo['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(editInfo['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION', version=1)
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                  messageCreateResponse=editInfo)
        AuthorizeMessage.assertResponse(approveRespone, 200)
        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        AuthorizeMessageDBAssertion(campaignId, editInfo['RESPONSE'], editInfo['PAYLOAD'],
                                    testControlType, version=1).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'LOYALTY', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def irisv2_message_edit_immediate_live_execute_plain_mobile_schedulle_recurring_coupon_body(self, campaignType,
                                                                                                    testControlType,
                                                                                                    listType,
                                                                                                    channel,
                                                                                                    messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True, lockNode=True)

        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION')
        dateTime = Utils.getTime(hours=5, minutes=32, dateTimeFormat=True)
        messageDetails['PAYLOAD'].update({
            'schedule': {
                'startDate': Utils.getTime(seconds=30, milliSeconds=True),
                'endDate': Utils.getTime(minutes=40, milliSeconds=True),
                'repeatOn': [1],
                'repeatType': 'DAILY',
                'scheduleType': 'RECURRING',
                'hour': int(dateTime[11:13]),
                'minute': int(dateTime[14:16])
            }
        })
        editInfo = CreateMessage.edit(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                      messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'])
        CreateMessage.assertResponse(editInfo['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(editInfo['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION', version=1)
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                  messageCreateResponse=editInfo)
        AuthorizeMessage.assertResponse(approveRespone, 200)
        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        AuthorizeMessageDBAssertion(campaignId, editInfo['RESPONSE'], editInfo['PAYLOAD'],
                                    testControlType, version=1).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'LOYALTY', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def irisv2_message_edit_immediate_live_execute_plain_mobile_schedulle_recurring_points_body(self, campaignType,
                                                                                                     testControlType,
                                                                                                     listType,
                                                                                                     channel,
                                                                                                     messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True, lockNode=True)

        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION')
        dateTime = Utils.getTime(hours=5, minutes=32, dateTimeFormat=True)
        messageDetails['PAYLOAD'].update({
            'schedule': {
                'startDate': Utils.getTime(seconds=30, milliSeconds=True),
                'endDate': Utils.getTime(minutes=40, milliSeconds=True),
                'repeatOn': [1],
                'repeatType': 'DAILY',
                'scheduleType': 'RECURRING',
                'hour': int(dateTime[11:13]),
                'minute': int(dateTime[14:16])
            }
        })
        editInfo = CreateMessage.edit(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                      messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'])
        CreateMessage.assertResponse(editInfo['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(editInfo['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION', version=1)
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                  messageCreateResponse=editInfo)
        AuthorizeMessage.assertResponse(approveRespone, 200)
        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        AuthorizeMessageDBAssertion(campaignId, editInfo['RESPONSE'], editInfo['PAYLOAD'],
                                    testControlType, version=1).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'EMAIL',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def irisv2_message_edit_immediate_live_execute_plain_email_schedulle_body_Sanity(self, campaignType,
                                                                                          testControlType, listType,
                                                                                          channel, messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True, lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION')
        messageDetails['PAYLOAD'].update({
            'schedule': {
                'scheduleType': 'PARTICULAR_DATE',
                'scheduledDate': int(time.time() * 1000) + 2 * 60 * 1000
            }
        })
        editInfo = CreateMessage.edit(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                      messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'])
        CreateMessage.assertResponse(editInfo['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(editInfo['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION', version=1)
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                  messageCreateResponse=editInfo)
        AuthorizeMessage.assertResponse(approveRespone, 200)
        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        AuthorizeMessageDBAssertion(campaignId, editInfo['RESPONSE'], editInfo['PAYLOAD'],
                                    testControlType, version=1).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'EMAIL',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def irisv2_message_edit_immediate_live_execute_plain_email_schedulle_particualrDate_coupon_body(self,
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
        messageDetails['PAYLOAD'].update({
            'schedule': {
                'scheduleType': 'PARTICULAR_DATE',
                'scheduledDate': int(time.time() * 1000) + 2 * 60 * 1000
            }
        })
        editInfo = CreateMessage.edit(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                      messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'])
        CreateMessage.assertResponse(editInfo['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(editInfo['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION', version=1)
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                  messageCreateResponse=editInfo)
        AuthorizeMessage.assertResponse(approveRespone, 200)
        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        AuthorizeMessageDBAssertion(campaignId, editInfo['RESPONSE'], editInfo['PAYLOAD'],
                                    testControlType, version=1).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'LOYALTY', 'EMAIL',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def irisv2_message_edit_immediate_live_execute_plain_email_schedulle_particualrDate_points_body(self,
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
        messageDetails['PAYLOAD'].update({
            'schedule': {
                'scheduleType': 'PARTICULAR_DATE',
                'scheduledDate': int(time.time() * 1000) + 2 * 60 * 1000
            }
        })
        editInfo = CreateMessage.edit(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                      messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'])
        CreateMessage.assertResponse(editInfo['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(editInfo['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION', version=1)
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                  messageCreateResponse=editInfo)
        AuthorizeMessage.assertResponse(approveRespone, 200)
        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        AuthorizeMessageDBAssertion(campaignId, editInfo['RESPONSE'], editInfo['PAYLOAD'],
                                    testControlType, version=1).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'LOYALTY', 'EMAIL',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def irisv2_message_edit_immediate_live_execute_plain_email_schedulle_recurring_plain_body(self, campaignType,
                                                                                                   testControlType,
                                                                                                   listType,
                                                                                                   channel,
                                                                                                   messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True, lockNode=True)

        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION')
        dateTime = Utils.getTime(hours=5, minutes=32, dateTimeFormat=True)
        messageDetails['PAYLOAD'].update({
            'schedule': {
                'startDate': Utils.getTime(seconds=30, milliSeconds=True),
                'endDate': Utils.getTime(minutes=40, milliSeconds=True),
                'repeatOn': [1],
                'repeatType': 'DAILY',
                'scheduleType': 'RECURRING',
                'hour': int(dateTime[11:13]),
                'minute': int(dateTime[14:16])
            }
        })
        editInfo = CreateMessage.edit(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                      messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'])
        CreateMessage.assertResponse(editInfo['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(editInfo['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION', version=1)
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                  messageCreateResponse=editInfo)
        AuthorizeMessage.assertResponse(approveRespone, 200)
        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        AuthorizeMessageDBAssertion(campaignId, editInfo['RESPONSE'], editInfo['PAYLOAD'],
                                    testControlType, version=1).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'LOYALTY', 'EMAIL',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def irisv2_message_edit_immediate_live_execute_plain_email_schedulle_recurring_coupon_body(self, campaignType,
                                                                                                    testControlType,
                                                                                                    listType,
                                                                                                    channel,
                                                                                                    messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True, lockNode=True)

        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION')
        dateTime = Utils.getTime(hours=5, minutes=32, dateTimeFormat=True)
        messageDetails['PAYLOAD'].update({
            'schedule': {
                'startDate': Utils.getTime(seconds=30, milliSeconds=True),
                'endDate': Utils.getTime(minutes=40, milliSeconds=True),
                'repeatOn': [1],
                'repeatType': 'DAILY',
                'scheduleType': 'RECURRING',
                'hour': int(dateTime[11:13]),
                'minute': int(dateTime[14:16])
            }
        })
        editInfo = CreateMessage.edit(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                      messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'])
        CreateMessage.assertResponse(editInfo['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(editInfo['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION', version=1)
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                  messageCreateResponse=editInfo)
        AuthorizeMessage.assertResponse(approveRespone, 200)
        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        AuthorizeMessageDBAssertion(campaignId, editInfo['RESPONSE'], editInfo['PAYLOAD'],
                                    testControlType, version=1).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'LOYALTY', 'EMAIL',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def irisv2_message_edit_immediate_live_execute_plain_email_schedulle_recurring_points_body(self, campaignType,
                                                                                                    testControlType,
                                                                                                    listType,
                                                                                                    channel,
                                                                                                    messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True, lockNode=True)

        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION')
        dateTime = Utils.getTime(hours=5, minutes=32, dateTimeFormat=True)
        messageDetails['PAYLOAD'].update({
            'schedule': {
                'startDate': Utils.getTime(seconds=30, milliSeconds=True),
                'endDate': Utils.getTime(minutes=40, milliSeconds=True),
                'repeatOn': [1],
                'repeatType': 'DAILY',
                'scheduleType': 'RECURRING',
                'hour': int(dateTime[11:13]),
                'minute': int(dateTime[14:16])
            }
        })
        editInfo = CreateMessage.edit(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                      messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'])
        CreateMessage.assertResponse(editInfo['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(editInfo['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION', version=1)
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                  messageCreateResponse=editInfo)
        AuthorizeMessage.assertResponse(approveRespone, 200)
        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        AuthorizeMessageDBAssertion(campaignId, editInfo['RESPONSE'], editInfo['PAYLOAD'],
                                    testControlType, version=1).check()

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
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def irisv2_message_edit_immediate_live_execute_plain_mobilePush_schedulle_body_Sanity(self, campaignType,
                                                                                         testControlType, listType,
                                                                                         channel, messageInfo):
        actualOrgId = IrisHelper.updateOrgId(constant.config['mobilepush']['orgId'])
        try:
            campaignInfo = CreateCampaign.create(campaignType, testControlType,updateNode=True,lockNode=True)
            messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,campaignId=campaignInfo['ID'],
                                              updateNode=True, lockNode=True)
            CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
            message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'],
                                                           'VARIANT_CREATION')
            messageDetails['PAYLOAD'].update({
                'schedule': {
                    'scheduleType': 'PARTICULAR_DATE',
                    'scheduledDate': int(time.time() * 1000) + 2 * 60 * 1000
                }
            })
            editInfo = CreateMessage.edit(campaignInfo['ID'],
                                      messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'])
            CreateMessage.assertResponse(editInfo['RESPONSE'], 200)
            message_calls().waitForJobDetailsStatusToClose(editInfo['RESPONSE']['json']['entity']['id'],
                                                           'VARIANT_CREATION', version=1)
            approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                      messageCreateResponse=editInfo,campaignId=campaignInfo['ID'])
            AuthorizeMessage.assertResponse(approveRespone, 200)
            AuthorizeMessageDBAssertion(campaignInfo['ID'], editInfo['RESPONSE'], editInfo['PAYLOAD'],
                                        testControlType, version=1).check()
        finally:
            IrisHelper.updateOrgId(actualOrgId)

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'ORG', 'LOYALTY', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
         'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def irisv2_message_edit_immediate_live_execute_plain_mobile_targetAudience_body(self, campaignType,
                                                                                          testControlType, listType,
                                                                                          channel, messageInfo):

        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True, lockNode=True)
        messageDetails['PAYLOAD']['targetAudience']['include']=[self.listInfoFilter['ID']]
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION')
        editInfo = CreateMessage.edit(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                      messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'])
        CreateMessage.assertResponse(editInfo['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(editInfo['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION', version=1)
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                  messageCreateResponse=editInfo)
        AuthorizeMessage.assertResponse(approveRespone, 200)
        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        AuthorizeMessageDBAssertion(campaignId, editInfo['RESPONSE'], editInfo['PAYLOAD'],
                                    testControlType, version=1).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo,keys', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}, 'useTinyUrl'),
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': True, 'encryptUrl': False, 'skipRateLimit': True}, 'useTinyUrl'),
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}, 'skipRateLimit'),
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': True, 'encryptUrl': False, 'skipRateLimit': False}, 'skipRateLimit'),
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True},
         'encryptUrl'),
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': True, 'encryptUrl': True, 'skipRateLimit': False},
         'encryptUrl')
    ])
    def irisv2_message_edit_immediate_live_execute_plain_mobile_additionalSettings_body(self, campaignType,
                                                                                               testControlType,
                                                                                               listType,
                                                                                               channel, messageInfo,
                                                                                               keys):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True, lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        messageDetails['PAYLOAD']['deliverySetting']['additionalSetting'][keys] = not messageDetails['PAYLOAD']['deliverySetting']['additionalSetting'][keys]
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION')
        editInfo = CreateMessage.edit(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                      messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'])
        CreateMessage.assertResponse(editInfo['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(editInfo['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION', version=1)
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                  messageCreateResponse=editInfo)
        AuthorizeMessage.assertResponse(approveRespone, 200)
        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        AuthorizeMessageDBAssertion(campaignId, editInfo['RESPONSE'], editInfo['PAYLOAD'],
                                    testControlType, version=1).check()

    @pytest.mark.skipif(constant.config['cluster'] not in ['nightly'],
                        reason='Channel Setting update Only Set for Nightly Cluster')
    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'ORG', 'LOYALTY', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def irisv2_message_edit_immediate_live_execute_plain_mobile_channleSetting_body(self, campaignType, testControlType, listType,
                                                                        channel, messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True, lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION')
        messageDetails['PAYLOAD']['deliverySetting']['channelSetting'] = constant.config['channelSetting']
        editInfo = CreateMessage.edit(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                      messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'])
        CreateMessage.assertResponse(editInfo['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(editInfo['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION', version=1)
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                  messageCreateResponse=editInfo)
        AuthorizeMessage.assertResponse(approveRespone, 200)
        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        AuthorizeMessageDBAssertion(campaignId, editInfo['RESPONSE'], editInfo['PAYLOAD'],
                                    testControlType, version=1).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'ORG', 'LOYALTY', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def irisv2_message_edit_immediate_live_execute_plain_mobile_storeType_body(self, campaignType,
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
        CreateMessage.assertResponse(editInfo['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(editInfo['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION', version=1)
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                  messageCreateResponse=editInfo)
        AuthorizeMessage.assertResponse(approveRespone, 200)
        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        AuthorizeMessageDBAssertion(campaignId, editInfo['RESPONSE'], editInfo['PAYLOAD'],
                                    testControlType, version=1).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'ORG', 'LOYALTY', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def irisv2_message_edit_immediate_live_execute_plain_mobile_messageBody_body(self, campaignType,
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
        CreateMessage.assertResponse(editInfo['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(editInfo['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION', version=1)
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                  messageCreateResponse=editInfo)
        AuthorizeMessage.assertResponse(approveRespone, 200)
        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        AuthorizeMessageDBAssertion(campaignId, editInfo['RESPONSE'], editInfo['PAYLOAD'],
                                    testControlType, version=1).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'LOYALTY', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'ORG', 'LOYALTY', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'ORG', 'LOYALTY', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def irisv2_message_edit_immediate_live_execute_plain_mobile_channel_body(self, campaignType,
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
        CreateMessage.assertResponse(editInfo['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(editInfo['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION', version=1)
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                  messageCreateResponse=editInfo)
        AuthorizeMessage.assertResponse(approveRespone, 200)
        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        AuthorizeMessageDBAssertion(campaignId, editInfo['RESPONSE'], editInfo['PAYLOAD'],
                                    testControlType, version=1).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'ORG', 'LOYALTY', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def irisv2_message_edit_immediate_live_execute_plain_mobile_sms_to_mobilePush_body(self, campaignType,
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
            CreateMessage.assertResponse(editInfo['RESPONSE'], 200)
            message_calls().waitForJobDetailsStatusToClose(editInfo['RESPONSE']['json']['entity']['id'],
                                                           'VARIANT_CREATION', version=1)
            approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                      messageCreateResponse=editInfo,campaignId=campaignInfo['ID'])
            AuthorizeMessage.assertResponse(approveRespone, 200)
            AuthorizeMessageDBAssertion(campaignInfo['ID'], editInfo['RESPONSE'], editInfo['PAYLOAD'],
                                        testControlType, version=1).check()
        finally:
            IrisHelper.updateOrgId(actualOrgId)

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def irisv2_message_edit_immediate_live_execute_plain_mobile_coupon_sms_to_mobilePush_body(self, campaignType,
                                                                                            testControlType, listType,
                                                                                            channel, messageInfo):
        actualOrgId = IrisHelper.updateOrgId(constant.config['mobilepush']['orgId'])
        try:
            campaignInfo = CreateCampaign.create(campaignType, testControlType, updateNode=True, lockNode=True)
            couponSeriesId =CreateMessage.getCouponSeriesId(campaignInfo['ID'])
            listInfo = CreateAudience.uploadList(campaignType, testControlType, schemaIdentifier=['USER_ID'],
                                                 schemaData=['USER_ID'], newUser=False, updateNode=True, lockNode=True,
                                                 campaignCheck=False, mobilePush=True)
            messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                                  listInfo=listInfo,
                                                  campaignId=campaignInfo['ID'],
                                                  updateNode=True, lockNode=True,couponSeriesId=couponSeriesId)
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
            CreateMessage.assertResponse(editInfo['RESPONSE'], 200)
            message_calls().waitForJobDetailsStatusToClose(editInfo['RESPONSE']['json']['entity']['id'],
                                                           'VARIANT_CREATION', version=1)
            approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                      messageCreateResponse=editInfo, campaignId=campaignInfo['ID'])
            AuthorizeMessage.assertResponse(approveRespone, 200)
            AuthorizeMessageDBAssertion(campaignInfo['ID'], editInfo['RESPONSE'], editInfo['PAYLOAD'],
                                        testControlType, version=1).check()
        finally:
            IrisHelper.updateOrgId(actualOrgId)

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'ORG', 'LOYALTY', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def irisv2_message_edit_immediate_live_execute_plain_mobile_plain_points_message_to_couponMessage(self, campaignType,
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
        CreateMessage.assertResponse(editInfo['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(editInfo['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION', version=1)
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                  messageCreateResponse=editInfo)
        AuthorizeMessage.assertResponse(approveRespone, 200)
        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        AuthorizeMessageDBAssertion(campaignId, editInfo['RESPONSE'], editInfo['PAYLOAD'],
                                    testControlType, version=1).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'LOYALTY', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'ORG', 'LOYALTY', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def irisv2_message_edit_immediate_live_execute_plain_mobile_plain_coupon_message_to_pointsMessage(self,
                                                                                                          campaignType,
                                                                                                          testControlType,
                                                                                                          listType,
                                                                                                          channel,
                                                                                                          messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True, lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
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
        CreateMessage.assertResponse(editInfo['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(editInfo['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION', version=1)
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                  messageCreateResponse=editInfo)
        AuthorizeMessage.assertResponse(approveRespone, 200)
        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        AuthorizeMessageDBAssertion(campaignId, editInfo['RESPONSE'], editInfo['PAYLOAD'],
                                    testControlType, version=1).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'LOYALTY', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def irisv2_message_edit_immediate_live_execute_plain_mobile_points_coupon_message_to_plainMessage(self,
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
        CreateMessage.assertResponse(editInfo['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(editInfo['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION', version=1)
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                  messageCreateResponse=editInfo)
        AuthorizeMessage.assertResponse(approveRespone, 200)
        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        AuthorizeMessageDBAssertion(campaignId, editInfo['RESPONSE'], editInfo['PAYLOAD'],
                                    testControlType, version=1).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def irisv2_message_edit_immediate_live_execute_plain_mobile_editMessage_withouChanging_body(self, campaignType,
                                                                                        testControlType, listType,
                                                                                        channel, messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True, lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION')
        editInfo = CreateMessage.edit(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                      messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'])
        CreateMessage.assertResponse(editInfo['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(editInfo['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION', version=1)
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                  messageCreateResponse=editInfo)
        AuthorizeMessage.assertResponse(approveRespone, 200)
        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        AuthorizeMessageDBAssertion(campaignId, editInfo['RESPONSE'], editInfo['PAYLOAD'],
                                    testControlType, version=1).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def irisv2_message_edit_immediate_live_execute_plain_mobile_editMessage_multipleTimes_body(self, campaignType,
                                                                                                   testControlType,
                                                                                                   listType,
                                                                                                   channel,
                                                                                                   messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True, lockNode=True)
        messageDetails['PAYLOAD']['targetAudience']['include'] = [self.listInfoFilter['ID']]
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
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
        CreateMessage.assertResponse(editInfo['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(editInfo['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION', version=1)
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                  messageCreateResponse=editInfo)
        AuthorizeMessage.assertResponse(approveRespone, 200)
        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        AuthorizeMessageDBAssertion(campaignId, editInfo['RESPONSE'], editInfo['PAYLOAD'],
                                    testControlType, version=3).check()

    @pytest.mark.parametrize('campaignType,testControlType,channel,messageInfo', [
        ('LIVE', 'ORG', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def irisv2_message_edit_immediate_live_create_plain_mobile_editStickyListMessage_particularDate(self, campaignType,
                                                                                          testControlType,
                                                                                          channel, messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, 'ORG_USERS', channel, messageInfo,
                                              derivedListInfo={'excludeUsers': [], 'includeUsers': ':1'})
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION')
        messageDetails['PAYLOAD'].update({
            'schedule': {
                'scheduleType': 'PARTICULAR_DATE',
                'scheduledDate': int(time.time() * 1000) + 2 * 60 * 1000
            }
        })
        editInfo = CreateMessage.edit(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                      messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'])
        CreateMessage.assertResponse(editInfo['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(editInfo['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION', version=1)
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, 'ORG_USERS', channel, messageInfo,
                                                  messageCreateResponse=editInfo)
        AuthorizeMessage.assertResponse(approveRespone, 200)
        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        AuthorizeMessageDBAssertion(campaignId, editInfo['RESPONSE'], editInfo['PAYLOAD'],
                                    testControlType, version=1).check()

    @pytest.mark.parametrize('campaignType,testControlType,channel,messageInfo', [
        ('LIVE', 'ORG', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def irisv2_message_edit_immediate_live_create_plain_mobile_editStickyListMessage_recurring(self,
                                                                                                         campaignType,
                                                                                                         testControlType,
                                                                                                         channel,
                                                                                                         messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, 'ORG_USERS', channel, messageInfo,
                                              derivedListInfo={'excludeUsers': [], 'includeUsers': ':1'})
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION')
        dateTime = Utils.getTime(hours=5, minutes=32, dateTimeFormat=True)
        messageDetails['PAYLOAD'].update({
            'schedule': {
                'startDate': Utils.getTime(seconds=30, milliSeconds=True),
                'endDate': Utils.getTime(minutes=40, milliSeconds=True),
                'repeatOn': [1],
                'repeatType': 'DAILY',
                'scheduleType': 'RECURRING',
                'hour': int(dateTime[11:13]),
                'minute': int(dateTime[14:16])
            }
        })
        editInfo = CreateMessage.edit(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                      messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'])
        CreateMessage.assertResponse(editInfo['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(editInfo['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION', version=1)
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, 'ORG_USERS', channel, messageInfo,
                                                  messageCreateResponse=editInfo)
        AuthorizeMessage.assertResponse(approveRespone, 200)
        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        AuthorizeMessageDBAssertion(campaignId, editInfo['RESPONSE'], editInfo['PAYLOAD'],
                                    testControlType, version=1).check()

    @pytest.mark.parametrize('campaignType,testControlType,channel,messageInfo', [
        ('LIVE', 'ORG', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def irisv2_message_edit_immediate_live_execute_plain_mobile_editStickyListMessage_targetAudience(self,
                                                                                                         campaignType,
                                                                                                         testControlType,
                                                                                                         channel,
                                                                                                         messageInfo):

        messageDetails = CreateMessage.create(campaignType, testControlType, 'ORG_USERS', channel, messageInfo,
                                              derivedListInfo={'excludeUsers': [], 'includeUsers': ':1'})
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        messageDetails['PAYLOAD'].pop('targetAudience')
        messageDetails['PAYLOAD'].update({
            'targetAudience': {
                'include': [self.listInfoFilter['ID']]
            }
        })
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION')
        editInfo = CreateMessage.edit(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                      messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'])
        CreateMessage.assertResponse(editInfo['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(editInfo['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION', version=1)
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, 'LOYALTY', channel, messageInfo,
                                                  messageCreateResponse=editInfo)
        AuthorizeMessage.assertResponse(approveRespone, 200)
        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        AuthorizeMessageDBAssertion(campaignId, editInfo['RESPONSE'], editInfo['PAYLOAD'],
                                    testControlType, version=1).check()









