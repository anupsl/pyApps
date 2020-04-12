import pytest

from src.Constant.constant import constant
from src.modules.irisv2.helper.irisHelper import IrisHelper
from src.modules.irisv2.message.authorizeMessage import AuthorizeMessage
from src.modules.irisv2.message.createMessage import CreateMessage
from src.modules.irisv2.message.preCheckDbValidation import PreCheckDBValidation
from src.modules.irisv2.message.preCheckDbValidation import Precheck_calls
from src.utilities.assertion import Assertion
from src.utilities.logger import Logger
from src.utilities.utils import Utils

@pytest.mark.skipif(constant.config['cluster'] not in ['nightly'], reason='Precheck Credit Tests Authorized Only For Nightly')
class Test_Precheck_Flow():
    def setup_method(self, method):
        Logger.logMethodName(method.__name__)

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),

    ])
    def test_irisv2_message_execute_flow_precheck_immediate_Sanity(self, campaignType, testControlType, listType,
                                                                   channel,
                                                                   messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True, lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                  messageCreateResponse=messageDetails)
        AuthorizeMessage.assertResponse(approveRespone, 200)
        PreCheckDBValidation(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                             messageDetails['RESPONSE']['json']['entity']['id'], messageInfo['scheduleType']['type'],
                             ['REMINDED', 'EXECUTING', 'OPENED'], remindCheck=False).validateMessageFlow()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),

    ])
    def test_irisv2_message_execute_flow_precheck_failed_immediate_CreditUnavialable(self, campaignType,
                                                                                     testControlType,
                                                                                     listType,
                                                                                     channel,
                                                                                     messageInfo):
        preCheckError = {'status': 'TEMPORARY_FAILURE', 'errorDescription': 'BULK_CREDITS_NOT_AVAILABLE'}
        try:
            messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                                  updateNode=True, lockNode=True)
            CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
            IrisHelper.updateCredit(0, channel)
            approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                      messageCreateResponse=messageDetails)
            AuthorizeMessage.assertResponse(approveRespone, 200)
            PreCheckDBValidation(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'],
                                 messageInfo['scheduleType']['type'],
                                 ['OPENED'], remindCheck=False,
                                 precheck=preCheckError, variantCheck=False).validateMessageFlow()
        finally:
            IrisHelper.updateCredit(99999, channel)

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),

    ])
    def test_irisv2_message_execute_flow_precheck_particularDate_Sanity(self, campaignType, testControlType, listType,
                                                                        channel,
                                                                        messageInfo):
        preCheckError = {
            'create': {'status': 'TEMPORARY_FAILURE', 'errorDescription': 'CAMPAIGN_NOT_AUTHORIZED'}
        }
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True, lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        PreCheckDBValidation(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                             messageDetails['RESPONSE']['json']['entity']['id'], messageInfo['scheduleType']['type'],
                             ['REMINDED', 'OPENED'], executeCheck=False, precheck=preCheckError['create'],
                             variantCheck=False).validateMessageFlow()
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                  messageCreateResponse=messageDetails)
        AuthorizeMessage.assertResponse(approveRespone, 200)

        Precheck_calls().waitForJobTypeUpdate(
            constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
            messageDetails['RESPONSE']['json']['entity']['id'], 'REMIND', 'PRECHECK', 'SUCCESS')

        PreCheckDBValidation(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                             messageDetails['RESPONSE']['json']['entity']['id'], messageInfo['scheduleType']['type'],
                             ['REMINDED', 'OPENED']).validateMessageFlow()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),

    ])
    def test_irisv2_message_execute_flow_precheck_failed_particularDate_CreditUnavialable_remind_execute_success(self,
                                                                                                                 campaignType,
                                                                                                                 testControlType,
                                                                                                                 listType,
                                                                                                                 channel,
                                                                                                                 messageInfo):
        preCheckError = {
            'create': {'status': 'TEMPORARY_FAILURE',
                       'errorDescription': 'CAMPAIGN_NOT_AUTHORIZED,BULK_CREDITS_NOT_AVAILABLE'}
        }
        try:
            IrisHelper.updateCredit(0, channel)
            messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                                  updateNode=True, lockNode=True)
            CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
            PreCheckDBValidation(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'],
                                 messageInfo['scheduleType']['type'],
                                 ['REMINDED', 'OPENED'], executeCheck=False, precheck=preCheckError['create'],
                                 variantCheck=False).validateMessageFlow()
            IrisHelper.updateCredit(100, channel)
            approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                      messageCreateResponse=messageDetails)
            AuthorizeMessage.assertResponse(approveRespone, 200)

            Precheck_calls().waitForJobTypeUpdate(
                constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                messageDetails['RESPONSE']['json']['entity']['id'], 'REMIND', 'PRECHECK', 'SUCCESS')

            PreCheckDBValidation(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'],
                                 messageInfo['scheduleType']['type'],
                                 ['REMINDED', 'OPENED']).validateMessageFlow()
        finally:
            IrisHelper.updateCredit(99999, channel)

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),

    ])
    def test_irisv2_message_execute_flow_precheck_particularDate_NotAuthorized_remind_retrail_remind_CreditUnavialable(
            self,
            campaignType,
            testControlType,
            listType,
            channel,
            messageInfo):
        preCheckError = {
            'create': {'status': 'TEMPORARY_FAILURE',
                       'errorDescription': 'CAMPAIGN_NOT_AUTHORIZED'},
            'execute': {'status': 'TEMPORARY_FAILURE',
                        'errorDescription': 'BULK_CREDITS_NOT_AVAILABLE'}
        }
        try:
            messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                                  updateNode=True, lockNode=True)
            CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
            PreCheckDBValidation(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'],
                                 messageInfo['scheduleType']['type'],
                                 ['REMINDED', 'OPENED'], executeCheck=False, precheck=preCheckError['create'],
                                 variantCheck=False).validateMessageFlow()
            IrisHelper.updateCredit(0, channel)
            approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                      messageCreateResponse=messageDetails)
            AuthorizeMessage.assertResponse(approveRespone, 200)

            Precheck_calls().waitForJobTypeUpdate(
                constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                messageDetails['RESPONSE']['json']['entity']['id'], 'REMIND', 'PRECHECK', 'TEMPORARY_FAILURE',
                expectedError='BULK_CREDITS_NOT_AVAILABLE')

            PreCheckDBValidation(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'],
                                 messageInfo['scheduleType']['type'],
                                 ['REMINDED', 'OPENED'], executeCheck=False, precheck=preCheckError['execute'],
                                 variantCheck=False).validateMessageFlow()
        except AssertionError, exp:
            Assertion.constructAssertion(False, 'Reason :{}'.format(exp))
        finally:
            IrisHelper.updateCredit(99999, channel)

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),

    ])
    def test_irisv2_message_execute_flow_precheck_particularDate_remind_success_approve_creditNotAvialable(self,
                                                                                                           campaignType,
                                                                                                           testControlType,
                                                                                                           listType,
                                                                                                           channel,
                                                                                                           messageInfo):
        try:
            precheckError = {'status': 'TEMPORARY_FAILURE',
                             'errorDescription': 'CAMPAIGN_NOT_AUTHORIZED'}
            messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                                  updateNode=True, lockNode=True)
            CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
            PreCheckDBValidation(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'],
                                 messageInfo['scheduleType']['type'],
                                 ['REMINDED', 'OPENED'], executeCheck=False,
                                 variantCheck=False, precheck=precheckError).validateMessageFlow()
            approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                      messageCreateResponse=messageDetails)
            AuthorizeMessage.assertResponse(approveRespone, 200)
            Precheck_calls().waitForJobTypeUpdate(
                constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                messageDetails['RESPONSE']['json']['entity']['id'], 'REMIND', 'PRECHECK', 'SUCCESS')

            PreCheckDBValidation(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'],
                                 messageInfo['scheduleType']['type'],
                                 ['REMINDED', 'OPENED']).validateMessageFlow()
        finally:
            IrisHelper.updateCredit(99999, channel)

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),

    ])
    def test_irisv2_message_execute_flow_precheck_particularDate_passed_with2MinsInterval(self,
                                                                                          campaignType,
                                                                                          testControlType,
                                                                                          listType,
                                                                                          channel,
                                                                                          messageInfo):
        precheckError = {
            'remind': {'status': 'TEMPORARY_FAILURE',
                       'errorDescription': 'CAMPAIGN_NOT_AUTHORIZED'}
        }
        scheduleType = {
            'scheduleType': 'PARTICULAR_DATE',
            'scheduledDate': Utils.getTime(minutes=2, seconds=00, milliSeconds=True)
        }
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              scheduleType=scheduleType, updateNode=True, lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        PreCheckDBValidation(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                             messageDetails['RESPONSE']['json']['entity']['id'],
                             messageInfo['scheduleType']['type'],
                             ['REMINDED', 'OPENED'], executeCheck=False,
                             variantCheck=False, precheck=precheckError['remind']).validateMessageFlow()
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                  messageCreateResponse=messageDetails)
        AuthorizeMessage.assertResponse(approveRespone, 200)

        Precheck_calls().waitForJobTypeUpdate(
            constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
            messageDetails['RESPONSE']['json']['entity']['id'], 'REMIND', 'PRECHECK', 'SUCCESS')

        PreCheckDBValidation(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                             messageDetails['RESPONSE']['json']['entity']['id'],
                             messageInfo['scheduleType']['type'],
                             ['REMINDED', 'OPENED']).validateMessageFlow()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),

    ])
    def test_irisv2_message_execute_flow_precheck_particularDate_with2HoursInterval_RemindCheck(self,
                                                                                                campaignType,
                                                                                                testControlType,
                                                                                                listType,
                                                                                                channel,
                                                                                                messageInfo):
        scheduleType = {
            'scheduleType': 'PARTICULAR_DATE',
            'scheduledDate': Utils.getTime(hours=2, minutes=1, seconds=30, milliSeconds=True)
        }
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              scheduleType=scheduleType, updateNode=True, lockNode=True)
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                  messageCreateResponse=messageDetails)
        AuthorizeMessage.assertResponse(approveRespone, 200)

        Precheck_calls().waitForJobTypeUpdate(
            constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
            messageDetails['RESPONSE']['json']['entity']['id'], 'REMIND', 'PRECHECK', 'SUCCESS')

        PreCheckDBValidation(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                             messageDetails['RESPONSE']['json']['entity']['id'],
                             messageInfo['scheduleType']['type'],
                             ['REMINDED', 'OPENED'],
                             executeCheck=False, variantCheck=False).validateMessageFlow()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'LOYALTY', 'MOBILE',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),

    ])
    def test_irisv2_message_execute_flow_precheck_recurring__RemindCheck(self,
                                                                         campaignType,
                                                                         testControlType,
                                                                         listType,
                                                                         channel,
                                                                         messageInfo):
        try:
            precheckError = {
                'remind': {'status': 'TEMPORARY_FAILURE',
                           'errorDescription': 'CAMPAIGN_NOT_AUTHORIZED'},
                'execute': {'status': 'TEMPORARY_FAILURE',
                            'errorDescription': 'BULK_CREDITS_NOT_AVAILABLE'}
            }

            messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                                  updateNode=True, lockNode=True)
            CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
            PreCheckDBValidation(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'],
                                 messageInfo['scheduleType']['type'],
                                 ['REMINDED', 'OPENED'], executeCheck=False,
                                 variantCheck=False, precheck=precheckError['remind'],
                                 reloadCheck={'GROUP_RELOAD_NFS': 'SUCCESS',
                                              'GROUP_RELOAD_CREATE_AUDIENCE': 'SUBMITTED'},
                                 byPassPrecheckValidation=True
                                 ).validateMessageFlow()
            IrisHelper.updateCredit(0, channel)
            approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                      messageCreateResponse=messageDetails)
            AuthorizeMessage.assertResponse(approveRespone, 200)
            Precheck_calls().waitForJobTypeUpdate(
                constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                messageDetails['RESPONSE']['json']['entity']['id'], 'REMIND', 'PRECHECK', 'TEMPORARY_FAILURE',
                expectedError='BULK_CREDITS_NOT_AVAILABLE')

            PreCheckDBValidation(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'],
                                 messageInfo['scheduleType']['type'],
                                 ['REMINDED', 'OPENED'], executeCheck=False, variantCheck=False,
                                 precheck=precheckError['execute']).validateMessageFlow()
        finally:
            IrisHelper.updateCredit(99999, channel)

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'LOYALTY', 'MOBILE',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),

    ])
    def test_irisv2_message_execute_flow_precheck_recurring__RemindCheckFailure_CreditUnavialable_ExecuteSuccess(self,
                                                                                                                 campaignType,
                                                                                                                 testControlType,
                                                                                                                 listType,
                                                                                                                 channel,
                                                                                                                 messageInfo):
        try:
            precheckError = {
                'remind': {'status': 'TEMPORARY_FAILURE',
                           'errorDescription': 'CAMPAIGN_NOT_AUTHORIZED,BULK_CREDITS_NOT_AVAILABLE'}
            }
            IrisHelper.updateCredit(0, channel)
            messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                                  updateNode=True, lockNode=True)
            CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
            PreCheckDBValidation(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'],
                                 messageInfo['scheduleType']['type'],
                                 ['REMINDED', 'OPENED'], executeCheck=False,
                                 variantCheck=False, precheck=precheckError['remind'],
                                 reloadCheck={'GROUP_RELOAD_NFS': 'SUCCESS',
                                              'GROUP_RELOAD_CREATE_AUDIENCE': 'SUBMITTED'},
                                 byPassPrecheckValidation=True).validateMessageFlow()
            IrisHelper.updateCredit(99999, channel)
            approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                      messageCreateResponse=messageDetails)
            AuthorizeMessage.assertResponse(approveRespone, 200)
            Precheck_calls().waitForJobTypeUpdate(
                constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                messageDetails['RESPONSE']['json']['entity']['id'], 'REMIND', 'PRECHECK', 'SUCCESS')

            PreCheckDBValidation(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'],
                                 messageInfo['scheduleType']['type'],
                                 ['REMINDED', 'OPENED']).validateMessageFlow()
        finally:
            IrisHelper.updateCredit(99999, channel)
