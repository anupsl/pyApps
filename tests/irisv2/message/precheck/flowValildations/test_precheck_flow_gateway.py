import time

import pytest

from src.Constant.constant import constant
from src.modules.irisv2.helper.irisHelper import IrisHelper
from src.modules.irisv2.message.authorizeMessage import AuthorizeMessage
from src.modules.irisv2.message.createMessage import CreateMessage
from src.modules.irisv2.message.preCheckDbValidation import PreCheckDBValidation
from src.modules.irisv2.message.preCheckDbValidation import Precheck_calls
from src.utilities.assertion import Assertion
from src.utilities.logger import Logger


@pytest.mark.skipif(constant.config['cluster'] not in ['nightly'], reason='Precheck Gateway Tests Authorized Only For Nightly')
class Test_Gateway_Flow_PreCheck():
    def setup_class(self):
        self.actualOrgId = IrisHelper.updateOrgId(constant.config['mobilepush']['orgId'])
        self.actualOrgName = IrisHelper.updateOrgName(constant.config['mobilepush']['orgName'])

    def setup_method(self, method):
        Logger.logMethodName(method.__name__)

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),

    ])
    def test_irisv2_message_execute_flow_precheck_immediate_GatewayUnavialable_remind(self, campaignType,
                                                                                      testControlType,
                                                                                      listType,
                                                                                      channel,
                                                                                      messageInfo):
        preCheckError = {'status': 'TEMPORARY_FAILURE', 'errorDescription': 'GATEWAY_NOT_AVAILABLE'}
        try:
            messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                                  updateNode=True, lockNode=True)
            CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
            IrisHelper.disableDomainGatewayMapId(channel)
            approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                      messageCreateResponse=messageDetails)
            AuthorizeMessage.assertResponse(approveRespone, 200)

            PreCheckDBValidation(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'],
                                 messageInfo['scheduleType']['type'],
                                 ['REMINDED', 'OPENED'], remindCheck=False,
                                 precheck=preCheckError, variantCheck=False).validateMessageFlow()
        except AssertionError, exp:
            Assertion.constructAssertion(False, '{}'.format(exp))
        finally:
            IrisHelper.createNewDummyGateway(channel)

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),

    ])
    def test_irisv2_message_execute_flow_precheck_failed_particularDate_GatewayUnavialable_SuccessAtExecute(self,
                                                                                                            campaignType,
                                                                                                            testControlType,
                                                                                                            listType,
                                                                                                            channel,
                                                                                                            messageInfo):
        preCheckError = {'status': 'TEMPORARY_FAILURE',
                         'errorDescription': 'CAMPAIGN_NOT_AUTHORIZED,GATEWAY_NOT_AVAILABLE'}
        dummyGatewayCreated = False
        try:
            messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                                  updateNode=True, lockNode=True)
            IrisHelper.disableDomainGatewayMapId(channel)
            CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
            PreCheckDBValidation(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'],
                                 messageInfo['scheduleType']['type'],
                                 ['REMINDED', 'OPENED'], executeCheck=False,
                                 precheck=preCheckError, variantCheck=False).validateMessageFlow()
            if IrisHelper.createNewDummyGateway(channel): dummyGatewayCreated = True
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
        except AssertionError, exp:
            Assertion.constructAssertion(False, '{}'.format(exp))
        finally:
            if not dummyGatewayCreated: IrisHelper.createNewDummyGateway(channel)

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),

    ])
    def test_irisv2_message_execute_flow_precheck_particularDate_NotAuthorized_remind_retrail_remind_GatewayUnavialable(
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
                        'errorDescription': 'GATEWAY_NOT_AVAILABLE'}
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
            IrisHelper.disableDomainGatewayMapId(channel)
            approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                      messageCreateResponse=messageDetails)
            AuthorizeMessage.assertResponse(approveRespone, 200)

            Precheck_calls().waitForJobTypeUpdate(
                constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                messageDetails['RESPONSE']['json']['entity']['id'], 'REMIND', 'PRECHECK', 'TEMPORARY_FAILURE',
                expectedError='GATEWAY_NOT_AVAILABLE')

            PreCheckDBValidation(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'],
                                 messageInfo['scheduleType']['type'],
                                 ['REMINDED', 'OPENED'], executeCheck=False, precheck=preCheckError['execute'],
                                 variantCheck=False).validateMessageFlow()
        except AssertionError, exp:
            Assertion.constructAssertion(False, 'Reason :{}'.format(exp))
        finally:
            IrisHelper.createNewDummyGateway(channel)

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),

    ])
    def test_irisv2_message_execute_flow_precheck_failed_particularDate_CreditUnavialable_remind_execute_gatewayNotFound(
            self,
            campaignType,
            testControlType,
            listType,
            channel,
            messageInfo):
        preCheckError = {
            'create': {'status': 'TEMPORARY_FAILURE',
                       'errorDescription': 'CAMPAIGN_NOT_AUTHORIZED,BULK_CREDITS_NOT_AVAILABLE'
                       },
            'execute': {'status': 'TEMPORARY_FAILURE',
                        'errorDescription': 'GATEWAY_NOT_AVAILABLE'
                        }
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
            IrisHelper.disableDomainGatewayMapId(channel)
            approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                      messageCreateResponse=messageDetails)
            AuthorizeMessage.assertResponse(approveRespone, 200)
            Precheck_calls().waitForJobTypeUpdate(
                constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                messageDetails['RESPONSE']['json']['entity']['id'], 'REMIND', 'PRECHECK', 'TEMPORARY_FAILURE',expectedError='GATEWAY_NOT_AVAILABLE')

            PreCheckDBValidation(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'],
                                 messageInfo['scheduleType']['type'],
                                 ['REMINDED', 'OPENED'], executeCheck=False, precheck=preCheckError['execute'],
                                 variantCheck=False).validateMessageFlow()
        except AssertionError, exp:
            Assertion.constructAssertion(False, 'Reason :{}'.format(exp))
        finally:
            IrisHelper.updateCredit(99999, channel)
            IrisHelper.createNewDummyGateway(channel)

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),

    ])
    def test_irisv2_message_execute_flow_precheck_failed_particularDate_gatewayNotAvialable_remind_execute_creditNotAvialable(
            self,
            campaignType,
            testControlType,
            listType,
            channel,
            messageInfo):
        preCheckError = {
            'create': {'status': 'TEMPORARY_FAILURE',
                       'errorDescription': 'CAMPAIGN_NOT_AUTHORIZED,GATEWAY_NOT_AVAILABLE'
                       },
            'execute': {'status': 'TEMPORARY_FAILURE',
                        'errorDescription': 'BULK_CREDITS_NOT_AVAILABLE'
                        }
        }
        dummyGatewayCreated = False
        try:
            messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                                  updateNode=True, lockNode=True)
            IrisHelper.disableDomainGatewayMapId(channel)
            CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
            PreCheckDBValidation(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'],
                                 messageInfo['scheduleType']['type'],
                                 ['REMINDED', 'OPENED'], executeCheck=False, precheck=preCheckError['create'],
                                 variantCheck=False).validateMessageFlow()
            IrisHelper.updateCredit(0, channel)
            if IrisHelper.createNewDummyGateway(channel): dummyGatewayCreated = True
            approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                      messageCreateResponse=messageDetails)
            AuthorizeMessage.assertResponse(approveRespone, 200)
            Precheck_calls().waitForJobTypeUpdate(
                constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                messageDetails['RESPONSE']['json']['entity']['id'], 'REMIND', 'PRECHECK', 'TEMPORARY_FAILURE',expectedError='BULK_CREDITS_NOT_AVAILABLE')

            PreCheckDBValidation(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'],
                                 messageInfo['scheduleType']['type'],
                                 ['REMINDED', 'OPENED'], executeCheck=False, precheck=preCheckError['execute'],
                                 variantCheck=False).validateMessageFlow()
        finally:
            IrisHelper.updateCredit(99999, channel)
            if not dummyGatewayCreated: IrisHelper.createNewDummyGateway(channel)
