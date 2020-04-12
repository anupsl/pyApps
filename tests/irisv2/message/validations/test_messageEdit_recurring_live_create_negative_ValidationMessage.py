import pytest,time
import copy

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

class Test_MessageEdit_NegativeCase_Recurring_Live_Create():
    def setup_method(self, method):
        Logger.logMethodName(method.__name__)

    def setup_class(self):
        Logger.logSuiteName(str(self).split('.')[-1])
        self.listInfo = CreateAudience.uploadList('LIVE', 'ORG')
        self.listInfoFilter = CreateAudience.FilterList('LIVE', 'ORG')
        constant.config['FilterListID'] = CreateAudience.FilterList('LIVE', 'ORG', campaignCheck=False)['ID']
        CreateAudience.getPocUsers()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo,editInfo,statusCode,errorCode,errorDescription', [
        ('LIVE', 'ORG', 'LOYALTY', 'MOBILE',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True},
         {'schedule': {'scheduleType': 'RECURRIN', 'startDate': Utils.getTime(minutes=10, milliSeconds=True),
                       'endDate': Utils.getTime(minutes=40, milliSeconds=True), 'repeatOn': [1], 'hour': 10,
                       'repeatType': 'DAILY', 'minute': 10}}, 400, 104,
         'Invalid request : invalid data type of field schedule')
    ])
    def test_irisv2_message_edit_recurring_live_create_plain_mobile_negativeCases(self, campaignType,
                                                                                  testControlType, listType,
                                                                                  channel, messageInfo,
                                                                                  editInfo, statusCode, errorCode,
                                                                                  errorDescription):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True, lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        editInfo = CreateMessage.edit(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                      messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],
                                      editInfo)
        CreateMessage.assertResponse(editInfo['RESPONSE'], 400, expectedErrorCode=[errorCode],
                                     expectedErrorMessage=errorDescription)

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo,field,fieldValue,statusCode, errorCode,errorDescription', [
        ('LIVE', 'ORG', 'LOYALTY', 'MOBILE',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True},
         'storeType', 'REGISTERED_STOR', 400, 104,
         'Invalid request : storeType , Unknown value REGISTERED_STOR, allowed values are [REGISTERED_STORE, LAST_TRANSACTED_AT]'),
        ('LIVE', 'ORG', 'LOYALTY', 'MOBILE',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}, 'messageBody',
         '', 400, 102, 'Invalid request : Message body is required in message content.'),
        ('LIVE', 'ORG', 'LOYALTY', 'MOBILE',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}, 'messageBody',
         'no optout tag', 400, 3066, 'Invalid message content : Optout tag must be present in message.'),
        ('LIVE', 'ORG', 'LOYALTY', 'MOBILE',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}, 'messageBody',
         'invalid tag {{anup}} {{optout}}', 400, 3067, 'Unsupported Tag {{anup}}'),
        ('LIVE', 'ORG', 'LOYALTY', 'MOBILE',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}, 'channel',
         'SMSS', 400, 104, 'Invalid request : channel , Unknown value SMSS, allowed values are [SMS, EMAIL, MOBILEPUSH, CALL_TASK, WECHAT]'),
        ('LIVE', 'ORG', 'LOYALTY', 'MOBILE',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}, 'messageBody',
         'invalid tag {{voucher}} {{optout}}', 400, 3067, 'Coupon offer should be attached to use voucher tag'),
        ('LIVE', 'ORG', 'LOYALTY', 'MOBILE',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}, 'messageBody',
         'invalid tag {{promotion_points}} {{optout}}', 400, 3067, 'Points offer should be attached to use points tags'),
        ('LIVE', 'ORG', 'LOYALTY', 'MOBILE',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}, 'messageBody',
         'invalid tag {{promotion_points}} {{optout}}', 400, 3067, 'Points offer should be attached to use points tags'),
        ('LIVE', 'ORG', 'LOYALTY', 'MOBILE',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}, 'messageBody',
         'invalid tag {{voucher}} {{optout}}', 400, 3067, 'Invalid coupon series id is used while using coupon tags')
    ])
    def test_irisv2_message_edit_recurring_live_create_plain_mobile_messageContent_negativeCases(self, campaignType,
                                                                                  testControlType, listType,
                                                                                  channel, messageInfo, field, fieldValue,
                                                                                  statusCode, errorCode,
                                                                                  errorDescription):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True, lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        messageDetails['PAYLOAD']['messageContent']['message_content_id_1'][field] = fieldValue
        editInfo = CreateMessage.edit(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                      messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'])
        CreateMessage.assertResponse(editInfo['RESPONSE'], 400, expectedErrorCode=[errorCode],
                                     expectedErrorMessage=errorDescription)

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo,statusCode, errorCode,errorDescription,', [
        ('LIVE', 'ORG', 'LOYALTY', 'MOBILE',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}, 400, 3050, 'Target Audience is not filter based : {}.')
    ])
    def test_irisv2_message_edit_recurring_live_create_plain_mobile_targetAudience_negativeCase(self, campaignType,
                                                                                        testControlType, listType,
                                                                                        channel, messageInfo,statusCode, errorCode,errorDescription):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True, lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        messageDetails['PAYLOAD']['targetAudience']['include'] = [self.listInfo['ID']]
        editInfo = CreateMessage.edit(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                      messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'])
        CreateMessage.assertResponse(editInfo['RESPONSE'], 400, expectedErrorCode=[errorCode],
                                     expectedErrorMessage=errorDescription.format(self.listInfo['ID']))

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo,statusCode,errorCode,errorDescription', [
        ('LIVE', 'ORG', 'LOYALTY', 'MOBILE',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}, 400, 3023,
         'Message with message id {} does not exists')
    ])
    def test_irisv2_message_edit_recurring_live_create_plain_mobile_editMessage_with_campaignId_of_another_campaign(self, campaignType, testControlType,
                                                                      listType,
                                                                      channel, messageInfo, statusCode, errorCode,
                                                                      errorDescription):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True, lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION')
        campaignInfo = CreateCampaign.create(campaignType, testControlType, updateNode=True)
        editInfo = CreateMessage.edit(campaignInfo['ID'],
                                      messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'])
        CreateMessage.assertResponse(editInfo['RESPONSE'], 400, expectedErrorCode=[errorCode],
                                     expectedErrorMessage=errorDescription.format(messageDetails['RESPONSE']['json']['entity']['id']))

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo,statusCode,errorCode,errorDescription', [
        ('LIVE', 'ORG', 'LOYALTY', 'MOBILE',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}, 400, 3023,
         'Message with message id {} does not exists')
    ])
    def test_irisv2_message_edit_recurring_live_create_plain_mobile_editMessage_with_invalid_campaignId(self, campaignType, testControlType,
                                                          listType,
                                                          channel, messageInfo, statusCode, errorCode,
                                                          errorDescription):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True, lockNode=True)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION')
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        editInfo = CreateMessage.edit(12345678,
                                      messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'])
        CreateMessage.assertResponse(editInfo['RESPONSE'], 400, expectedErrorCode=[errorCode],
                                     expectedErrorMessage=errorDescription.format(messageDetails['RESPONSE']['json']['entity']['id']))

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo,statusCode,errorCode,errorDescription', [
        ('LIVE', 'ORG', 'LOYALTY', 'MOBILE',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}, 400, 3023,
         'Message with message id hjsdgf7823jsd72v does not exists')
    ])
    def test_irisv2_message_edit_recurring_live_create_plain_mobile_editMessage_with_invalid_messageId(self, campaignType, testControlType,
                                                         listType,
                                                         channel, messageInfo, statusCode, errorCode, errorDescription):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True, lockNode=True)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION')
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        editInfo = CreateMessage.edit(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                      'hjsdgf7823jsd72v',messageDetails['PAYLOAD'])
        CreateMessage.assertResponse(editInfo['RESPONSE'], 400, expectedErrorCode=[errorCode],
                                     expectedErrorMessage=errorDescription.format(messageDetails['RESPONSE']['json']['entity']['id']))

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo,statusCode,errorCode,errorDescription', [
        ('LIVE', 'ORG', 'LOYALTY', 'MOBILE',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}, 400, 102,
         'Invalid request : must be greater than or equal to 1')
    ])
    def test_irisv2_message_edit_recurring_live_create_plain_mobile_editMessage_with_negative_campaignId(self, campaignType, testControlType,
                                                           listType,
                                                           channel, messageInfo, statusCode, errorCode,
                                                           errorDescription):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True, lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION')
        editInfo = CreateMessage.edit(-1234,
                                      messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'])
        CreateMessage.assertResponse(editInfo['RESPONSE'], 400, expectedErrorCode=[errorCode],
                                     expectedErrorMessage=errorDescription)

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo,statusCode,errorCode,errorDescription', [
        ('LIVE', 'ORG', 'LOYALTY', 'MOBILE',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}, 400, 3023,
         'Message with message id -1234 does not exists')
    ])
    def test_irisv2_message_edit_recurring_live_create_plain_mobile_editMessage_with_negative_messageId(self, campaignType, testControlType,
                                                          listType,
                                                          channel, messageInfo, statusCode, errorCode,
                                                          errorDescription):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True, lockNode=True)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION')
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        editInfo = CreateMessage.edit(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                      '-1234', messageDetails['PAYLOAD'])
        CreateMessage.assertResponse(editInfo['RESPONSE'], 400, expectedErrorCode=[errorCode],
                                     expectedErrorMessage=errorDescription)

    @pytest.mark.parametrize('description,campaignType,testControlType,channel,messageInfo,statusCode,errorCode,errorDescription', [
        ('Edit end date', 'LIVE', 'ORG', 'MOBILE',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}, 400, [3036,3038],
         ['Campaign expired','Invalid Schedule : Message cannot end after campaign.'])
    ])
    def test_irisV2_message_edit_recurring_live_create_plain_mobile_editMessage_afterCampaign_expires(self, description,
                                                                                                      campaignType,
                                                                                                      testControlType,
                                                                                                      channel,
                                                                                                      messageInfo,
                                                                                                      statusCode,
                                                                                                      errorCode,
                                                                                                      errorDescription):
        messageDetails = CreateMessage.create(campaignType, testControlType, 'LOYALTY', channel, messageInfo,
                                              updateNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        campaignInfo = constant.config['node'][campaignType][testControlType]['CAMPAIGN']
        editInfo = {'endDate': Utils.getTime(minutes=1, milliSeconds=True)}
        editInfo = CreateCampaign.edit(campaignInfo, editInfo)
        time.sleep(61)
        editInfo = CreateMessage.edit(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                      messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'])
        CreateMessage.assertResponse(editInfo['RESPONSE'], 400, expectedErrorCode=errorCode,
                                     expectedErrorMessage=errorDescription)