import pytest

from src.Constant.constant import constant
from src.dbCalls.messageInfo import message_calls
from src.modules.irisv2.message.createMessage import CreateMessage
from src.utilities.utils import Utils


class Test_Reminder_Validation():
    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'REMIND', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
    ])
    def test_reminder_validation_newCouponSeriesID(self, campaignType, testControlType,
                                                   listType,
                                                   channel,
                                                   messageInfo):
        remindParams = {
            'reminderStrategy': 'ALL',
            'parentMessageId': constant.config['reminder']['coupon']['messageId']
        }
        campaignId = constant.config['reminder']['coupon']['campaignId']
        series_id = constant.config['reminder']['coupon']['series_id']
        constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'] = campaignId
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              listInfo='', campaignId=campaignId, remindParams=remindParams,
                                              lockNode=True, couponSeriesId=series_id)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[3065, 3039],
                                     expectedErrorMessage=[
                                         'Invalid reminder message content : New coupons cannot be issued in a reminder message.',
                                         'Coupon series is claimed : {},{}'.format(str(series_id)[:2],
                                                                                   str(series_id)[2:])])

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'REMIND', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
    ])
    def test_reminder_validation_createWithPoints(self, campaignType, testControlType,
                                                  listType,
                                                  channel,
                                                  messageInfo):
        remindParams = {
            'reminderStrategy': 'ALL',
            'parentMessageId': constant.config['reminder']['coupon']['messageId']
        }
        campaignId = constant.config['reminder']['coupon']['campaignId']
        constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'] = campaignId
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              listInfo='', campaignId=campaignId, remindParams=remindParams,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[3069],
                                     expectedErrorMessage=[
                                         'Promotion Points cannot be added for a Reminder type message: Points should not be added in reminder type message'])

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'REMIND', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
    ])
    def test_reminder_edit_validation_parentMessageID_edit(self, campaignType, testControlType, listType,
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
                    "parentMessageId": constant.config['reminder']['plain']['messageId'],
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
        CreateMessage.assertResponse(editInfo['RESPONSE'], 400, expectedErrorCode=[3060], expectedErrorMessage=[
            'Invalid parent message id specified in target audience include definition for reminder message: Cannot change the parent message id of a reminder message while editing.'])
