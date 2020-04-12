import pytest, time, datetime
from src.Constant.constant import constant
from src.modules.irisv2.monitoringDetails.getMonitoringDetails import GetMonitoringDetails
from src.modules.irisv2.message.authorizeMessage import AuthorizeMessage
from src.utilities.assertion import Assertion
from src.utilities.awsHelper import AWSHelper
from src.utilities.logger import Logger
from src.dbCalls.messageInfo import message_calls
from src.modules.irisv2.campaigns.createCampaign import CreateCampaign
from src.modules.irisv2.message.createMessage import CreateMessage
from src.modules.irisv2.message.createMessageDbAssertion import CreateMessageDBAssertion
from src.modules.irisv2.message.authorizeMessageDbAssertion import AuthorizeMessageDBAssertion

class Test_getMonitorByCampaignId():

    def setup_class(self):
        Logger.log('Getting uploaded User list by filters')
        constant.config['totalUserCount'] = (filter(None, AWSHelper.readFileFromS3(bucketName=constant.orgDetails[constant.config['cluster']][constant.config['orgId']]['s3BucketName'],
                                                   keyName=constant.orgDetails[constant.config['cluster']][constant.config['orgId']]['s3KeyName'])))

    def setup_method(self, method):
        Logger.logMethodName(method.__name__)

    @pytest.mark.parametrize('campaignType,testControlType,channel,messageInfo,queryParam', [
        ('LIVE', 'ORG', 'MOBILE',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True},
         [('monitoring', 'true'), ('details', 'true'), ('deliveryBreakup', 'true')])
    ])
    def test_irisv2_getStatusBy_messageId_Sanity(self, campaignType, testControlType,
                                                                       channel, messageInfo, queryParam):
        messageDetails = CreateMessage.create(campaignType, testControlType, 'LOYALTY', channel, messageInfo,
                                              updateNode=True, lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION')
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, 'LOYALTY', channel, messageInfo,
                                                  messageCreateResponse=messageDetails)
        AuthorizeMessage.assertResponse(approveRespone, 200)
        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        AuthorizeMessageDBAssertion(campaignId, messageDetails['RESPONSE'], messageDetails['PAYLOAD'],
                                    testControlType).check()
        response = GetMonitoringDetails.getByMessageId(campaignId, messageDetails['RESPONSE']['json']['entity']['id'], queryParam)
        actualResponse, expectedResponse = GetMonitoringDetails.formatingMonitorDetails(response,isScheduledMsg=True,isDeliveryBreakEnabled=True)
        Assertion.constructAssertion(actualResponse == expectedResponse, 'Monitoring Details response Matched Actual: {} and Expected: {}'.format(actualResponse, expectedResponse))

    @pytest.mark.parametrize('campaignType,testControlType,channel,messageInfo,queryParam', [
        ('LIVE', 'ORG', 'EMAIL',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True},
         [('monitoring', 'true'), ('details', 'false'), ('deliveryBreakup', 'true')])
    ])
    def test_irisv2_getStatusBy_campaignId_Sanity(self, campaignType, testControlType,
                                                  channel, messageInfo, queryParam):
        campaignInfo = CreateCampaign.create(campaignType, testControlType, updateNode=True, lockNode=True)
        Logger.log('campaign id is',campaignInfo['ID'])
        messageDetails = CreateMessage.create(campaignType, testControlType, 'LOYALTY', channel, messageInfo,
                                              campaignId=campaignInfo['ID'],
                                              updateNode=True, lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION')
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, 'LOYALTY', channel, messageInfo,
                                                  messageCreateResponse=messageDetails,campaignId=campaignInfo['ID'])
        AuthorizeMessage.assertResponse(approveRespone, 200)
        messageDetails = CreateMessage.create(campaignType, testControlType, 'LOYALTY', channel, messageInfo,
                                              campaignId=campaignInfo['ID'],
                                              updateNode=True, lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION')
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, 'LOYALTY', channel, messageInfo,
                                                  messageCreateResponse=messageDetails,campaignId=campaignInfo['ID'])
        AuthorizeMessage.assertResponse(approveRespone, 200)
        time.sleep(150)
        message_calls().getCommunicationDetailsWithOnlyMessageId(approveRespone['json']['entity']['messageId'])
        response = GetMonitoringDetails.getByCampaignId(campaignInfo['ID'], queryParam)
        actualResponse, expectedResponse = GetMonitoringDetails.formatingMonitorDetails(response, isScheduledMsg=False,
                                                                                        isDeliveryBreakEnabled=True)
        Assertion.constructAssertion(actualResponse == expectedResponse,
                                     'Monitoring Details response Matched Actual: {} and Expected: {}'.format(
                                         actualResponse, expectedResponse))

    @pytest.mark.parametrize('campaignType,testControlType,channel,messageInfo,queryParam', [
        ('LIVE', 'ORG', 'EMAIL',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True},
         [('monitoring', 'true'), ('details', 'false'), ('deliveryBreakup', 'true')])
    ])
    def test_irisv2_getStatusBy_messageId_All_User_Skipp(self, campaignType, testControlType,
                                                 channel, messageInfo, queryParam):
        messageDetails = CreateMessage.create(campaignType, testControlType, 'UPLOAD', channel, messageInfo,
                                              updateNode=True, lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION')
        messageDetails['PAYLOAD']['messageContent']['message_content_id_1'][
            'emailBody'] = '{{unsubscribe}},{{last_transacted_store_external_id_2}}'
        editInfo = CreateMessage.edit(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                      messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'])
        CreateMessage.assertResponse(editInfo['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(editInfo['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION', version=1)
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, 'UPLOAD', channel, messageInfo,
                                                  messageCreateResponse=editInfo)
        AuthorizeMessage.assertResponse(approveRespone, 200)
        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        AuthorizeMessageDBAssertion(campaignId, editInfo['RESPONSE'], editInfo['PAYLOAD'],
                                    testControlType, version=1, skippedReason=['No entry for last shopped store present']).check()
        response = GetMonitoringDetails.getByMessageId(
            constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
            editInfo['RESPONSE']['json']['entity']['id'], queryParam)
        actualResponse, expectedResponse = GetMonitoringDetails.formatingMonitorDetails(response, isScheduledMsg=False,
                                                                                       isDeliveryBreakEnabled=True)
        Assertion.constructAssertion(actualResponse == expectedResponse,
                                     'Monitoring Details response Matched Actual: {} and Expected: {}'.format(
                                         actualResponse, expectedResponse))

    def test_irisv2_monitoring_partial_skippedReasons(self):
        listInfo = GetMonitoringDetails.createSkippedPartialList()
        messageInfo = {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}
        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE', messageInfo,listInfo=listInfo,
                                              updateNode=True, lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION')
        approveRespone = AuthorizeMessage.approve('LIVE', 'ORG', 'UPLOAD', 'MOBILE', messageInfo,
                                                  messageCreateResponse=messageDetails)
        AuthorizeMessage.assertResponse(approveRespone, 200)
        time.sleep(150)
        queryParam = [('monitoring', 'true'), ('details', 'false'), ('deliveryBreakup', 'true')]
        response = GetMonitoringDetails.getByMessageId(constant.config['node']['LIVE']['ORG']['CAMPAIGN']['ID'], messageDetails['RESPONSE']['json']['entity']['id'], queryParam)
        actualResponse, expectedResponse = GetMonitoringDetails.formatingMonitorDetails(response, isScheduledMsg=False,
                                                                                        isDeliveryBreakEnabled=True)
        Assertion.constructAssertion(actualResponse == expectedResponse,
                                     'Monitoring Details response Matched Actual: {} and Expected: {}'.format(
                                         actualResponse, expectedResponse))

    @pytest.mark.parametrize('campaignType,testControlType,channel,messageInfo,queryParam', [
        ('LIVE', 'ORG', 'EMAIL',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True},
         [('monitoring', 'true'), ('details', 'false'), ('deliveryBreakup', 'true')])
    ])
    def test_irisv2_getStatusBy_messageId_Yet_to_go(self, campaignType, testControlType,
                                                         channel, messageInfo, queryParam):
        messageDetails = CreateMessage.create(campaignType, testControlType, 'LOYALTY', channel, messageInfo,
                                              updateNode=True, lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION')
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, 'LOYALTY', channel, messageInfo,
                                                  messageCreateResponse=messageDetails)
        response = GetMonitoringDetails.getByMessageId(
            constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
            messageDetails['RESPONSE']['json']['entity']['id'], queryParam)
        actualResponse, expectedResponse = GetMonitoringDetails.formatingMonitorDetails(response, isScheduledMsg=True,
                                                                                        isDeliveryBreakEnabled=False,forceUpdate=True)
        Assertion.constructAssertion(actualResponse == expectedResponse,
                                     'Monitoring Details response Matched Actual: {} and Expected: {}'.format(
                                         actualResponse, expectedResponse))

    @pytest.mark.parametrize('campaignType,testControlType,channel,messageInfo', [
        ('LIVE', 'ORG', 'MOBILE',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def test_irisv2_getStatusBy_orgId_yesterday_to_tomorrow(self, campaignType, testControlType,
                                                 channel, messageInfo):
        queryParam = [('startDate', (datetime.datetime.today() - datetime.timedelta(days=1) - datetime.datetime.utcfromtimestamp(0)).days),
                      ('endDate', (datetime.datetime.today() + datetime.timedelta(days=1) - datetime.datetime.utcfromtimestamp(0)).days),
                      ('limit',1)]
        response = GetMonitoringDetails.getByOrgId(queryParam,entity=True)
        actualResponse, expectedResponse = GetMonitoringDetails.formatingMonitorDetails(response, isScheduledMsg=False,
                                                                                        isDeliveryBreakEnabled=False)
        Assertion.constructAssertion(actualResponse == expectedResponse,
                                     'Monitoring Details response Matched Actual: {} and Expected: {}'.format(
                                         actualResponse, expectedResponse))

    @pytest.mark.parametrize('campaignType,testControlType,channel,messageInfo', [
        ('LIVE', 'ORG', 'MOBILE',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def test_irisv2_getStatusBy_orgId_today_to_tomorrow(self, campaignType, testControlType,
                                                            channel, messageInfo):
        queryParam = [('startDate', (datetime.datetime.today() - datetime.datetime.utcfromtimestamp(0)).days),
                      ('endDate', (datetime.datetime.today() + datetime.timedelta(days=1) - datetime.datetime.utcfromtimestamp(0)).days),
                      ('limit',1)]
        response = GetMonitoringDetails.getByOrgId(queryParam,entity=True)
        actualResponse, expectedResponse = GetMonitoringDetails.formatingMonitorDetails(response, isScheduledMsg=False,
                                                                                        isDeliveryBreakEnabled=False)
        Assertion.constructAssertion(actualResponse == expectedResponse,
                                     'Monitoring Details response Matched Actual: {} and Expected: {}'.format(
                                         actualResponse, expectedResponse))

    @pytest.mark.parametrize('campaignType,testControlType,channel,messageInfo', [
        ('LIVE', 'ORG', 'MOBILE',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def test_irisv2_getStatusBy_orgId_yesterday_to_today(self, campaignType, testControlType,
                                                        channel, messageInfo):
        queryParam = [('startDate', (datetime.datetime.today() - datetime.timedelta(days=1) - datetime.datetime.utcfromtimestamp(0)).days),
                      ('endDate', (datetime.datetime.today() - datetime.datetime.utcfromtimestamp(0)).days),
                      ('limit',1)]
        response = GetMonitoringDetails.getByOrgId(queryParam,entity=True)
        actualResponse, expectedResponse = GetMonitoringDetails.formatingMonitorDetails(response, isScheduledMsg=False,
                                                                                        isDeliveryBreakEnabled=False)
        Assertion.constructAssertion(actualResponse == expectedResponse,
                                     'Monitoring Details response Matched Actual: {} and Expected: {}'.format(
                                         actualResponse, expectedResponse))

    @pytest.mark.parametrize('campaignType,testControlType,channel,messageInfo', [
        ('LIVE', 'ORG', 'MOBILE',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def test_irisv2_getStatusBy_orgId(self, campaignType, testControlType,
                                                         channel, messageInfo):
        queryParam = [('limit',1)]
        response = GetMonitoringDetails.getByOrgId(queryParam,entity=True)
        actualResponse, expectedResponse = GetMonitoringDetails.formatingMonitorDetails(response, isScheduledMsg=False,
                                                                                        isDeliveryBreakEnabled=False)
        Assertion.constructAssertion(actualResponse == expectedResponse,
                                     'Monitoring Details response Matched Actual: {} and Expected: {}'.format(
                                         actualResponse, expectedResponse))

    @pytest.mark.parametrize('campaignType,testControlType,channel,messageInfo', [
        ('LIVE', 'ORG', 'MOBILE',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def test_irisv2_getStatusBy_orgId_past(self, campaignType, testControlType,
                                                         channel, messageInfo):
        queryParam = [('startDate', (datetime.datetime.today() - datetime.timedelta(days=10) - datetime.datetime.utcfromtimestamp(0)).days),
                      ('endDate', (datetime.datetime.today() - datetime.timedelta(days=7) - datetime.datetime.utcfromtimestamp(0)).days),
                      ('limit',2)]
        response = GetMonitoringDetails.getByOrgId(queryParam,entity=True)
        actualResponse, expectedResponse = GetMonitoringDetails.formatingMonitorDetails(response, isScheduledMsg=False,
                                                                                        isDeliveryBreakEnabled=False)
        Assertion.constructAssertion(actualResponse == expectedResponse,
                                     'Monitoring Details response Matched Actual: {} and Expected: {}'.format(
                                         actualResponse, expectedResponse))

    @pytest.mark.parametrize('campaignType,testControlType,channel,messageInfo', [
        ('LIVE', 'ORG', 'MOBILE',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def test_irisv2_getStatusBy_orgId_future(self, campaignType, testControlType,
                                                        channel, messageInfo):
        queryParam = [('startDate', (datetime.datetime.today() + datetime.timedelta(days=1) - datetime.datetime.utcfromtimestamp(0)).days),
                      ('endDate', (datetime.datetime.today() + datetime.timedelta(days=4) - datetime.datetime.utcfromtimestamp(0)).days),
                      ('limit',1)]
        response = GetMonitoringDetails.getByOrgId(queryParam,entity=True)
        actualResponse, expectedResponse = GetMonitoringDetails.formatingMonitorDetails(response, isScheduledMsg=False,
                                                                                        isDeliveryBreakEnabled=False)
        Assertion.constructAssertion(actualResponse == expectedResponse,
                                     'Monitoring Details response Matched Actual: {} and Expected: {}'.format(
                                         actualResponse, expectedResponse))
