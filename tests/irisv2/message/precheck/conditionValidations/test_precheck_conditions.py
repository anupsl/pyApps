import pytest

from src.Constant.constant import constant
from src.modules.irisv2.message.createMessage import CreateMessage
from src.modules.irisv2.message.preCheck import PreCheck
from src.modules.irisv2.helper.irisHelper import IrisHelper
from src.utilities.assertion import Assertion
from src.dbCalls.campaignShard import list_Calls

@pytest.mark.skipif(constant.config['cluster'] not in ['nightly'], reason='Precheck Credit Tests Authorized Only For Nightly')
class Test_Precheck_Conditions():
    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo,precheckErrors', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True},
         [{'errorType': 'CAMPAIGN_NOT_AUTHORIZED', 'parameters': {}}]),
        ('UPCOMING', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True},
         [{'errorType': 'CAMPAIGN_NOT_AUTHORIZED', 'parameters': {}}])
    ])
    def test_irisv2_message_precheck_create_upload_mobile_immediate_NotAuthorized(self, campaignType, testControlType,
                                                                                  listType, channel, messageInfo,
                                                                                  precheckErrors):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True, lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        preCheckResponse = PreCheck.executePrecheck(
            constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
            messageDetails['RESPONSE']['json']['entity']['id'])
        PreCheck.assertPreCheckResponse(preCheckResponse, 200)
        PreCheck.assertPrecheckStatus(preCheckResponse, precheckErrors)

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo,precheckErrors', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True},
         [{'errorType': 'CAMPAIGN_NOT_AUTHORIZED', 'parameters': {}}]),
        ('UPCOMING', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True},
         [{'errorType': 'CAMPAIGN_NOT_AUTHORIZED', 'parameters': {}}])
    ])
    def test_irisv2_message_precheck_create_upload_mobile_particularDate_NotAuthorized(self, campaignType,
                                                                                       testControlType, listType,
                                                                                       channel, messageInfo,
                                                                                       precheckErrors):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True, lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        preCheckResponse = PreCheck.executePrecheck(
            constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
            messageDetails['RESPONSE']['json']['entity']['id'])
        PreCheck.assertPreCheckResponse(preCheckResponse, 200)
        PreCheck.assertPrecheckStatus(preCheckResponse, precheckErrors)

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo,precheckErrors', [
        ('LIVE', 'ORG', 'LOYALTY', 'MOBILE',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True},
         [{'errorType': 'CAMPAIGN_NOT_AUTHORIZED', 'parameters': {}}]),
        ('UPCOMING', 'ORG', 'LOYALTY', 'MOBILE',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True},
         [{'errorType': 'CAMPAIGN_NOT_AUTHORIZED', 'parameters': {}}])
    ])
    def est_irisv2_message_precheck_create_filter_mobile_Recurring_NotAuthorized(self, campaignType,
                                                                                 testControlType,
                                                                                 listType,
                                                                                 channel, messageInfo,
                                                                                 precheckErrors):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True, lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        preCheckResponse = PreCheck.executePrecheck(
            constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
            messageDetails['RESPONSE']['json']['entity']['id'])
        PreCheck.assertPreCheckResponse(preCheckResponse, 200)
        PreCheck.assertPrecheckStatus(preCheckResponse, precheckErrors)

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo,precheckErrors', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True},
         [{'errorType': 'CAMPAIGN_NOT_AUTHORIZED', 'parameters': {}},
          {'errorType': 'BULK_CREDITS_NOT_AVAILABLE',
           'parameters': {'availableCredits': 0, 'balanceRequiredCredits': 10}}]),
        ('UPCOMING', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True},
         [{'errorType': 'CAMPAIGN_NOT_AUTHORIZED', 'parameters': {}},
          {'errorType': 'BULK_CREDITS_NOT_AVAILABLE',
           'parameters': {'availableCredits': 0, 'balanceRequiredCredits': 10}}])
    ])
    def test_irisv2_message_precheck_create_upload_mobile_immediate_CreditAvialable(self, campaignType,
                                                                                    testControlType,
                                                                                    listType,
                                                                                    channel, messageInfo,
                                                                                    precheckErrors):
        try:
            messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                                  updateNode=True, lockNode=True)
            precheckErrors[1]['parameters']['balanceRequiredCredits'] = int(list_Calls().getCustomerCountInGVD(
                messageDetails['PAYLOAD']['targetAudience']['include'][0]))
            CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
            IrisHelper.updateCredit(0, channel)
            preCheckResponse = PreCheck.executePrecheck(
                constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                messageDetails['RESPONSE']['json']['entity']['id'])
            PreCheck.assertPreCheckResponse(preCheckResponse, 200)
            PreCheck.assertPrecheckStatus(preCheckResponse,precheckErrors)
        except Exception, exp:
            Assertion.constructAssertion(False, 'Failure Due to Exception :{}'.format(exp))
        finally:
            IrisHelper.updateCredit(99999, channel)

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo,precheckErrors', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True},
         [{'errorType': 'CAMPAIGN_NOT_AUTHORIZED', 'parameters': {}},
          {'errorType': 'BULK_CREDITS_NOT_AVAILABLE',
           'parameters': {'availableCredits': 0, 'balanceRequiredCredits': 10}}]),
        ('UPCOMING', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True},
         [{'errorType': 'CAMPAIGN_NOT_AUTHORIZED', 'parameters': {}},
          {'errorType': 'BULK_CREDITS_NOT_AVAILABLE',
           'parameters': {'availableCredits': 0, 'balanceRequiredCredits': 10}}])
    ])
    def test_irisv2_message_precheck_create_upload_mobile_particularDate_CreditAvialable(self, campaignType,
                                                                                                testControlType,
                                                                                                listType,
                                                                                                channel, messageInfo,
                                                                                         precheckErrors):
        try:
            messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                                  updateNode=True, lockNode=True)
            precheckErrors[1]['parameters']['balanceRequiredCredits'] = int(list_Calls().getCustomerCountInGVD(
                messageDetails['PAYLOAD']['targetAudience']['include'][0]))
            CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
            IrisHelper.updateCredit(0, channel)
            preCheckResponse = PreCheck.executePrecheck(
                constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                messageDetails['RESPONSE']['json']['entity']['id'])
            PreCheck.assertPreCheckResponse(preCheckResponse, 200)
            PreCheck.assertPrecheckStatus(preCheckResponse,precheckErrors)
        except Exception, exp:
            Assertion.constructAssertion(False, 'Failure Due to Exception :{}'.format(exp))
        finally:
            IrisHelper.updateCredit(99999, channel)

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo,precheckErrors', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True},
         [{'errorType': 'CAMPAIGN_NOT_AUTHORIZED', 'parameters': {}},
          {'errorType': 'BULK_CREDITS_NOT_AVAILABLE',
           'parameters': {'availableCredits': 1, 'balanceRequiredCredits': 9}}]),
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True},
         [{'errorType': 'CAMPAIGN_NOT_AUTHORIZED', 'parameters': {}},
          {'errorType': 'BULK_CREDITS_NOT_AVAILABLE',
           'parameters': {'availableCredits': 7, 'balanceRequiredCredits': 3}}]),
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True},
         [{'errorType': 'CAMPAIGN_NOT_AUTHORIZED', 'parameters': {}},
          {'errorType': 'BULK_CREDITS_NOT_AVAILABLE',
           'parameters': {'availableCredits': 9, 'balanceRequiredCredits': 1}}])
    ])
    def test_irisv2_message_precheck_create_upload_mobile_particularDate_CreditAvialable_CheckAvialable_BalanceRequiredCredit_Count(
            self, campaignType,
            testControlType,
            listType,
            channel, messageInfo,
            precheckErrors):
        try:
            messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                                  updateNode=True, lockNode=True)
            precheckErrors[1]['parameters']['balanceRequiredCredits'] = int(list_Calls().getCustomerCountInGVD(
                messageDetails['PAYLOAD']['targetAudience']['include'][0])) - precheckErrors[1]['parameters'][
                                                                               'availableCredits']

            CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
            IrisHelper.updateCredit(0, channel)
            IrisHelper.updateCredit(precheckErrors[1]['parameters']['availableCredits'], channel)
            preCheckResponse = PreCheck.executePrecheck(
                constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                messageDetails['RESPONSE']['json']['entity']['id'])
            PreCheck.assertPreCheckResponse(preCheckResponse, 200)
            PreCheck.assertPrecheckStatus(preCheckResponse,precheckErrors)
        except Exception, exp:
            Assertion.constructAssertion(False, 'Failure Due to Exception :{}'.format(exp))
        finally:
            IrisHelper.updateCredit(99999, channel)

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo,precheckErrors', [
        ('LIVE', 'ORG', 'LOYALTY', 'MOBILE',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True},
         [{'errorType': 'CAMPAIGN_NOT_AUTHORIZED', 'parameters': {}},
          {'errorType': 'BULK_CREDITS_NOT_AVAILABLE',
           'parameters': {'availableCredits': 0, 'balanceRequiredCredits': 10}}])

    ])
    def test_irisv2_message_precheck_create_filter_mobile_recurring_CreditAvialable(self, campaignType,
                                                                                    testControlType,
                                                                                    listType,
                                                                                    channel, messageInfo,
                                                                                    precheckErrors):
        try:
            messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                                  updateNode=True, lockNode=True)
            precheckErrors[1]['parameters']['balanceRequiredCredits'] = list_Calls().getCustomerCountInGVD(
                messageDetails['PAYLOAD']['targetAudience']['include'][0])

            CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
            IrisHelper.updateCredit(0, channel)
            preCheckResponse = PreCheck.executePrecheck(
                constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                messageDetails['RESPONSE']['json']['entity']['id'])
            PreCheck.assertPreCheckResponse(preCheckResponse, 200)
            PreCheck.assertPrecheckStatus(preCheckResponse,precheckErrors)
        except Exception, exp:
            Assertion.constructAssertion(False, 'Failure Due to Exception :{}'.format(exp))
        finally:
            IrisHelper.updateCredit(99999, channel)

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo,precheckErrors', [
        ('LIVE', 'ORG', 'LOYALTY', 'MOBILE',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True},
         [{'errorType': 'CAMPAIGN_NOT_AUTHORIZED', 'parameters': {}},
          {'errorType': 'MAX_USER_LIMIT_EXCEEDED', 'parameters': {'totalCustomerCount': 22, 'maxUsersAllowed': 1}}]),
        ('LIVE', 'CUSTOM', 'LOYALTY', 'MOBILE',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True},
         [{'errorType': 'CAMPAIGN_NOT_AUTHORIZED', 'parameters': {}},
          {'errorType': 'MAX_USER_LIMIT_EXCEEDED', 'parameters': {'totalCustomerCount': 22, 'maxUsersAllowed': 1}}])

    ])
    def test_irisv2_message_precheck_create_filter_mobile_Recurring_MaxUser(self, campaignType,
                                                                            testControlType,
                                                                            listType,
                                                                            channel, messageInfo,
                                                                            precheckErrors):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True, lockNode=True, maxUser=[1])
        precheckErrors[1]['parameters']['totalCustomerCount'] = list_Calls().getCustomerCountInGVD(
            messageDetails['PAYLOAD']['targetAudience']['include'][0])
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        preCheckResponse = PreCheck.executePrecheck(
            constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
            messageDetails['RESPONSE']['json']['entity']['id'])
        PreCheck.assertPreCheckResponse(preCheckResponse, 200)
        PreCheck.assertPrecheckStatus(preCheckResponse,precheckErrors)

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo,precheckErrors', [
        ('LIVE', 'ORG', 'UPLOAD', 'EMAIL',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True},
         [{'errorType': 'CAMPAIGN_NOT_AUTHORIZED', 'parameters': {}}]),
        ('UPCOMING', 'ORG', 'UPLOAD', 'EMAIL',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True},
         [{'errorType': 'CAMPAIGN_NOT_AUTHORIZED', 'parameters': {}}]),
        ('LIVE', 'CUSTOM', 'UPLOAD', 'EMAIL',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True},
         [{'errorType': 'CAMPAIGN_NOT_AUTHORIZED', 'parameters': {}}])
    ])
    def test_irisv2_message_precheck_create_upload_email_immediate_NotAuthorized(self, campaignType,
                                                                                 testControlType,
                                                                                 listType,
                                                                                 channel, messageInfo,
                                                                                 precheckErrors):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True, lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        preCheckResponse = PreCheck.executePrecheck(
            constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
            messageDetails['RESPONSE']['json']['entity']['id'])
        PreCheck.assertPreCheckResponse(preCheckResponse, 200)
        PreCheck.assertPrecheckStatus(preCheckResponse,precheckErrors)

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo,precheckErrors', [
        ('LIVE', 'ORG', 'LOYALTY', 'EMAIL',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True},
         [{'errorType': 'CAMPAIGN_NOT_AUTHORIZED', 'parameters': {}}]),
        ('LIVE', 'CUSTOM', 'LOYALTY', 'EMAIL',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True},
         [{'errorType': 'CAMPAIGN_NOT_AUTHORIZED', 'parameters': {}}]),
        ('UPCOMING', 'ORG', 'LOYALTY', 'EMAIL',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True},
         [{'errorType': 'CAMPAIGN_NOT_AUTHORIZED', 'parameters': {}}])
    ])
    def test_irisv2_message_precheck_create_filter_email_Recurring_NotAuthorized(self, campaignType,
                                                                                 testControlType,
                                                                                 listType,
                                                                                 channel, messageInfo,
                                                                                 precheckErrors):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True, lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        preCheckResponse = PreCheck.executePrecheck(
            constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
            messageDetails['RESPONSE']['json']['entity']['id'])
        PreCheck.assertPreCheckResponse(preCheckResponse, 200)
        PreCheck.assertPrecheckStatus(preCheckResponse,precheckErrors)

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo,precheckErrors', [
        ('LIVE', 'ORG', 'LOYALTY', 'EMAIL',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True},
         [{'errorType': 'CAMPAIGN_NOT_AUTHORIZED', 'parameters': {}},
          {'errorType': 'MAX_USER_LIMIT_EXCEEDED', 'parameters': {'totalCustomerCount': 22, 'maxUsersAllowed': 1}}])
    ])
    def test_irisv2_message_precheck_create_filter_email_Recurring_MaxUser(self, campaignType,
                                                                           testControlType,
                                                                           listType,
                                                                           channel, messageInfo,
                                                                           precheckErrors):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True, lockNode=True, maxUser=[1])
        precheckErrors[1]['parameters']['totalCustomerCount'] = list_Calls().getCustomerCountInGVD(
            messageDetails['PAYLOAD']['targetAudience']['include'][0])
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        preCheckResponse = PreCheck.executePrecheck(
            constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
            messageDetails['RESPONSE']['json']['entity']['id'])
        PreCheck.assertPreCheckResponse(preCheckResponse, 200)
        PreCheck.assertPrecheckStatus(preCheckResponse,precheckErrors)