import pytest

from src.Constant.constant import constant
from src.dbCalls.messageInfo import message_calls
from src.modules.irisv2.message.authorizeMessage import AuthorizeMessage
from src.modules.irisv2.message.authorizeMessageDbAssertion import AuthorizeMessageDBAssertion
from src.modules.irisv2.message.createMessage import CreateMessage
from src.utilities.utils import Utils


class Test_Reminder_Edit():
    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'REMIND', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
    ])
    def test_reminder_edit_allToNotRedemers_particularDate_coupons(self, campaignType, testControlType, listType,
                                                                   channel,
                                                                   messageInfo):
        remindParams = {
            'reminderStrategy': 'ALL',
            'parentMessageId': constant.config['reminder']['coupon']['messageId']
        }
        campaignId = constant.config['reminder']['coupon']['campaignId']
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              listInfo='', campaignId=campaignId, remindParams=remindParams,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION')
        editInfo = {
            'messageContent': {
                'message_content_id_1': {
                    "storeType": "REGISTERED_STORE",
                    "offers": [],
                    "messageBody": "Edit Message {{first_name}} {{last_name}} {{fullname}}  {{dynamic_expiry_date_after_1_days.FORMAT_2}} {{voucher}} {{valid_days_from_create}} {{valid_till_date.FORMAT_2}} {{optout}}",
                    "channel":"SMS"
                }
            },
            'targetAudience': {
                "isDef": True,
                "orgUsers": [],
                "includeDefinition": {
                    "parentMessageId": constant.config['reminder']['coupon']['messageId'],
                    "defType": "parentMsgReminder",
                    "reminderStrategy": "COUPON_NOT_REDEEMED"
                }
            },
            'schedule': {'scheduleType': 'PARTICULAR_DATE',
                         'scheduledDate': Utils.getTime(minutes=3, seconds=30, milliSeconds=True)
                         }

        }
        editInfo = CreateMessage.edit(campaignId,
                                      messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],
                                      editInfo)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION',version=1)
        approveRespone = AuthorizeMessage.approveWithCampaignAndMessageId(campaignId,
                                                                          editInfo['RESPONSE']['json']['entity'][
                                                                              'id'])
        AuthorizeMessage.assertResponse(approveRespone, 200)
        AuthorizeMessageDBAssertion(campaignId, editInfo['RESPONSE'], editInfo['PAYLOAD'],
                                    testControlType, version=1).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'REMIND', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
    ])
    def test_reminder_edit_allToNotTransacted_particularDate_coupons(self, campaignType, testControlType, listType,
                                                                   channel,
                                                                   messageInfo):
        remindParams = {
            'reminderStrategy': 'ALL',
            'parentMessageId': constant.config['reminder']['coupon']['messageId']
        }
        campaignId = constant.config['reminder']['coupon']['campaignId']
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              listInfo='', campaignId=campaignId, remindParams=remindParams,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION')
        editInfo = {
            'messageContent': {
                'message_content_id_1': {
                    "storeType": "REGISTERED_STORE",
                    "offers": [],
                    "messageBody": "Edit Message {{first_name}} {{last_name}} {{fullname}}  {{dynamic_expiry_date_after_1_days.FORMAT_2}} {{voucher}} {{valid_days_from_create}} {{valid_till_date.FORMAT_2}} {{optout}}",
                    "channel": "SMS"
                }
            },
            'targetAudience': {
                "isDef": True,
                "orgUsers": [],
                "includeDefinition": {
                    "parentMessageId": constant.config['reminder']['coupon']['messageId'],
                    "defType": "parentMsgReminder",
                    "reminderStrategy": "NOT_TRANSACTED"
                }
            },
            'schedule': {'scheduleType': 'PARTICULAR_DATE',
                         'scheduledDate': Utils.getTime(minutes=3, seconds=30, milliSeconds=True)
                         }

        }
        editInfo = CreateMessage.edit(campaignId,
                                      messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],
                                      editInfo)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION', version=1)
        approveRespone = AuthorizeMessage.approveWithCampaignAndMessageId(campaignId,
                                                                          editInfo['RESPONSE']['json']['entity'][
                                                                              'id'])
        AuthorizeMessage.assertResponse(approveRespone, 200)
        AuthorizeMessageDBAssertion(campaignId, editInfo['RESPONSE'], editInfo['PAYLOAD'],
                                    testControlType, version=1).check()
