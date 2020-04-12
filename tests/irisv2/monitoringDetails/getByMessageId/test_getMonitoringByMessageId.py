import pytest, time
from src.Constant.constant import constant
from src.utilities.awsHelper import AWSHelper
from src.modules.irisv2.monitoringDetails.getMonitoringDetails import GetMonitoringDetails
from src.modules.irisv2.message.authorizeMessage import AuthorizeMessage
from src.utilities.assertion import Assertion
from src.utilities.logger import Logger

class Test_getMonitorByMessageId():

    def setup_class(self):
        Logger.log('Getting uploadeded User list by filters')
        constant.config['totalUserCount'] = (filter(None, AWSHelper.readFileFromS3(bucketName=constant.orgDetails[constant.config['cluster']][constant.config['orgId']]['s3BucketName'],
                                                   keyName=constant.orgDetails[constant.config['cluster']][constant.config['orgId']]['s3KeyName'])))

    def setup_method(self, method):
        Logger.logMethodName(method.__name__)

    @pytest.mark.parametrize('campaignType,testControlType,channel,messageInfo', [
        ('LIVE', 'ORG', 'MOBILE', {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def est_irisv2_getStatusBy_messageId_Sanity(self, campaignType, testControlType,
                                                                       channel, messageInfo):
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, 'LOYALTY', channel, messageInfo)
        AuthorizeMessage.assertResponse(approveRespone, 200)

        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        messageId = constant.config['node'][campaignType][testControlType]['LIST']['LOYALTY'][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['RESPONSE']['json']['entity']['id']

        response = GetMonitoringDetails.getByMessageId(campaignId,messageId, queryParam=[('monitoring', 'true'), ('details' , 'false'), ('deliveryBreakup' , 'false')])

        actualResponse, expectedResponse = GetMonitoringDetails.formatingMonitorDetails(response, isScheduledMsg=True)
        Assertion.constructAssertion(actualResponse == expectedResponse, 'Monitoring Details response Matched Actual: {} and Expected: {}'.format(actualResponse, expectedResponse))

        time.sleep(150)
        response = GetMonitoringDetails.getByMessageId(campaignId, messageId, queryParam=[('monitoring', 'true'), ('details', 'false'), ('deliveryBreakup', 'true')])

        actualResponse, expectedResponse = GetMonitoringDetails.formatingMonitorDetails(response,isDeliveryBreakEnabled=True)
        Assertion.constructAssertion(actualResponse == expectedResponse, 'Monitoring Details response Matched Actual: {} and Expected: {}'.format(actualResponse, expectedResponse))


    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG','LOYALTY','MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'CUSTOM','LOYALTY', 'MOBILE',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'SKIP','LOYALTY' ,'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def test_irisv2_getStatusBy_messageId_withDeliveryBreakUp(self, campaignType, testControlType,listType,
                                                                       channel, messageInfo):
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo)
        AuthorizeMessage.assertResponse(approveRespone, 200)

        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        messageId = constant.config['node'][campaignType][testControlType]['LIST'][listType][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['RESPONSE']['json']['entity']['id']

        time.sleep(150)
        response = GetMonitoringDetails.getByMessageId(campaignId, messageId, queryParam=[('monitoring', 'true'), ('details', 'false'), ('deliveryBreakup', 'true')])

        actualResponse, expectedResponse = GetMonitoringDetails.formatingMonitorDetails(response,isDeliveryBreakEnabled=True)
        Assertion.constructAssertion(actualResponse == expectedResponse, 'Monitoring Details response Matched Actual: {} and Expected: {}'.format(actualResponse, expectedResponse))


    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'LOYALTY', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'CUSTOM', 'LOYALTY', 'MOBILE',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'SKIP', 'LOYALTY', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def test_irisv2_getStatusBy_messageId_withoutDeliveryBreakup(self, campaignType, testControlType, listType,
                                                                        channel, messageInfo):
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo)
        AuthorizeMessage.assertResponse(approveRespone, 200)

        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        messageId = constant.config['node'][campaignType][testControlType]['LIST'][listType][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['RESPONSE']['json']['entity']['id']

        time.sleep(150)
        response = GetMonitoringDetails.getByMessageId(campaignId, messageId, queryParam=[('monitoring', 'true'), ('details', 'false'), ('deliveryBreakup', 'false')])

        actualResponse, expectedResponse = GetMonitoringDetails.formatingMonitorDetails(response,isDeliveryBreakEnabled=False)
        Assertion.constructAssertion(actualResponse == expectedResponse, 'Monitoring Details response Matched Actual: {} and Expected: {}'.format(actualResponse, expectedResponse))

