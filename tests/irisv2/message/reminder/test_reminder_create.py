import pytest

from src.Constant.constant import constant
from src.modules.irisv2.message.authorizeMessage import AuthorizeMessage
from src.modules.irisv2.message.authorizeMessageDbAssertion import AuthorizeMessageDBAssertion
from src.modules.irisv2.message.createMessage import CreateMessage
from src.dbCalls.messageInfo import message_calls

class Test_Reminder_Create():
    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'REMIND', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
    ])
    def test_reminder_create_plain_transactionType_All_Sanity(self, campaignType, testControlType, listType, channel,
                                                       messageInfo):
        remindParams = {
            'reminderStrategy': 'ALL',
            'parentMessageId': constant.config['reminder']['plain']['messageId']
        }
        campaignId = constant.config['reminder']['plain']['campaignId']
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              listInfo='', campaignId=campaignId, remindParams=remindParams,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'], 'VARIANT_CREATION',sleepTime=20)
        approveRespone = AuthorizeMessage.approveWithCampaignAndMessageId(campaignId,
                                                                          messageDetails['RESPONSE']['json']['entity']['id'])
        AuthorizeMessage.assertResponse(approveRespone, 200)
        AuthorizeMessageDBAssertion(campaignId, messageDetails['RESPONSE'], messageDetails['PAYLOAD'],
                                    testControlType).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'REMIND', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
    ])
    def test_reminder_create_plain_transactionType_All_ParticularDate(self, campaignType, testControlType, listType, channel,
                                                              messageInfo):
        remindParams = {
            'reminderStrategy': 'ALL',
            'parentMessageId': constant.config['reminder']['plain']['messageId']
        }
        campaignId = constant.config['reminder']['plain']['campaignId']
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              listInfo='', campaignId=campaignId, remindParams=remindParams,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION')
        approveRespone = AuthorizeMessage.approveWithCampaignAndMessageId(campaignId,
                                                                          messageDetails['RESPONSE']['json']['entity'][
                                                                              'id'])
        AuthorizeMessage.assertResponse(approveRespone, 200)
        AuthorizeMessageDBAssertion(campaignId, messageDetails['RESPONSE'], messageDetails['PAYLOAD'],
                                    testControlType).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'REMIND', 'EMAIL',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
    ])
    def test_reminder_create_sms_coupon_email_particulardate_nonResponders_Coupon_appoved(self, campaignType, testControlType, listType,
                                                                      channel,
                                                                      messageInfo):
        remindParams = {
            'reminderStrategy': 'COUPON_NOT_REDEEMED',
            'parentMessageId': constant.config['reminder']['coupon']['messageId']
        }
        campaignId = constant.config['reminder']['coupon']['campaignId']
        constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'] = campaignId
        messageContent = CreateMessage.constructMessageContent(campaignType, testControlType,
                                              messageInfo['messageStrategy'],
                                              messageInfo['offerType'],
                                              channel)
        messageContent['message_content_id_1']['offers'] = []
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              listInfo='', campaignId=campaignId, remindParams=remindParams,
                                              lockNode=True,messageContent=messageContent)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION')
        approveRespone = AuthorizeMessage.approveWithCampaignAndMessageId(campaignId,
                                                                          messageDetails['RESPONSE']['json']['entity'][
                                                                              'id'])
        AuthorizeMessage.assertResponse(approveRespone, 200)
        AuthorizeMessageDBAssertion(campaignId, messageDetails['RESPONSE'], messageDetails['PAYLOAD'],
                                    testControlType).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'REMIND', 'EMAIL',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
    ])
    def test_reminder_create_sms_coupon_email_particulardate_nonResponders_Coupon_appoved(self, campaignType,
                                                                                          testControlType, listType,
                                                                                          channel,
                                                                                          messageInfo):
        remindParams = {
            'reminderStrategy': 'COUPON_NOT_REDEEMED',
            'parentMessageId': constant.config['reminder']['coupon']['messageId']
        }
        campaignId = constant.config['reminder']['coupon']['campaignId']
        constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'] = campaignId
        messageContent = CreateMessage.constructMessageContent(campaignType, testControlType,
                                                               messageInfo['messageStrategy'],
                                                               messageInfo['offerType'],
                                                               channel)
        messageContent['message_content_id_1']['offers'] = []
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              listInfo='', campaignId=campaignId, remindParams=remindParams,
                                              lockNode=True, messageContent=messageContent)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION')
        approveRespone = AuthorizeMessage.approveWithCampaignAndMessageId(campaignId,
                                                                          messageDetails['RESPONSE']['json']['entity'][
                                                                              'id'])
        AuthorizeMessage.assertResponse(approveRespone, 200)
        AuthorizeMessageDBAssertion(campaignId, messageDetails['RESPONSE'], messageDetails['PAYLOAD'],
                                    testControlType).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'REMIND', 'EMAIL',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
    ])
    def test_reminder_create_sms_coupon_email_particulardate_nonRedeemers_Coupon_appoved(self, campaignType,
                                                                                          testControlType, listType,
                                                                                          channel,
                                                                                          messageInfo):
        remindParams = {
            'reminderStrategy': 'NOT_TRANSACTED',
            'parentMessageId': constant.config['reminder']['coupon']['messageId']
        }
        campaignId = constant.config['reminder']['coupon']['campaignId']
        constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'] = campaignId
        messageContent = CreateMessage.constructMessageContent(campaignType, testControlType,
                                                               messageInfo['messageStrategy'],
                                                               messageInfo['offerType'],
                                                               channel)
        messageContent['message_content_id_1']['offers'] = []
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              listInfo='', campaignId=campaignId, remindParams=remindParams,
                                              lockNode=True, messageContent=messageContent)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION')
        approveRespone = AuthorizeMessage.approveWithCampaignAndMessageId(campaignId,
                                                                          messageDetails['RESPONSE']['json']['entity'][
                                                                              'id'])
        AuthorizeMessage.assertResponse(approveRespone, 200)
        AuthorizeMessageDBAssertion(campaignId, messageDetails['RESPONSE'], messageDetails['PAYLOAD'],
                                    testControlType).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'REMIND', 'EMAIL',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
    ])
    def test_reminder_create_sms_coupon_email_particulardate_nonRedeemers_Plain_appoved(self, campaignType,
                                                                                         testControlType, listType,
                                                                                         channel,
                                                                                         messageInfo):
        remindParams = {
            'reminderStrategy': 'NOT_TRANSACTED',
            'parentMessageId': constant.config['reminder']['plain']['messageId']
        }
        campaignId = constant.config['reminder']['plain']['campaignId']
        constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'] = campaignId
        messageContent = CreateMessage.constructMessageContent(campaignType, testControlType,
                                                               messageInfo['messageStrategy'],
                                                               messageInfo['offerType'],
                                                               channel)
        messageContent['message_content_id_1']['offers'] = []
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              listInfo='', campaignId=campaignId, remindParams=remindParams,
                                              lockNode=True, messageContent=messageContent)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION')
        approveRespone = AuthorizeMessage.approveWithCampaignAndMessageId(campaignId,
                                                                          messageDetails['RESPONSE']['json']['entity'][
                                                                              'id'])
        AuthorizeMessage.assertResponse(approveRespone, 200)
        AuthorizeMessageDBAssertion(campaignId, messageDetails['RESPONSE'], messageDetails['PAYLOAD'],
                                    testControlType).check()
