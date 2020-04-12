import pytest

from src.Constant.constant import constant
from src.modules.irisv2.message.reminder import Reminder


class Test_Reminder_Count():
    @pytest.mark.parametrize('campaignType,reminderType,invert,intersection', [
        ('plain', 'ALL',False,False),
        ('plain', 'NOT_TRANSACTED',True,True)
    ])
    def test_reminder_plainMessage_count_Sanity(self, campaignType, reminderType,invert,intersection):
        campaignId = str(constant.config['reminder'][campaignType]['campaignId'])
        messageId = constant.config['reminder'][campaignType]['messageId']
        irisresponse = Reminder.getReminderCount(campaignId, messageId, reminderType)
        nfsResponse = Reminder.getReminderCountFromNFS(messageId,invert=invert,intersection=intersection)
        Reminder.assertResponse(irisresponse, 200)
        Reminder.validateReminderCount(irisresponse,nfsResponse)

    @pytest.mark.parametrize('campaignType,reminderType', [
        ('plain', 'COUPON_NOT_REDEEMED')
    ])
    def test_reminder_plainMessage_count_CouponNotIssued(self, campaignType, reminderType):
        campaignId = str(constant.config['reminder'][campaignType]['campaignId'])
        messageId = constant.config['reminder'][campaignType]['messageId']
        response = Reminder.getReminderCount(campaignId, messageId, reminderType)
        Reminder.assertResponse(response, 400, expectedErrorCode=5004,
                                expectedErrorMessage='Campaign Meta Exception: Invalid parameter Reminder strategy. Cannot fetch reminder filter customer stats as parent message did not issue coupons.')

    @pytest.mark.parametrize('campaignType,reminderType,invert,intersection', [
        ('coupon', 'ALL', False, False),
        ('coupon', 'NOT_TRANSACTED', True, True)
    ])
    def test_reminder_couponMessage_count_Sanity(self, campaignType, reminderType, invert, intersection):
        campaignId = str(constant.config['reminder'][campaignType]['campaignId'])
        messageId = constant.config['reminder'][campaignType]['messageId']
        irisresponse = Reminder.getReminderCount(campaignId, messageId, reminderType)
        nfsResponse = Reminder.getReminderCountFromNFS(messageId, invert=invert, intersection=intersection)
        Reminder.assertResponse(irisresponse, 200)
        Reminder.validateReminderCount(irisresponse, nfsResponse)

    @pytest.mark.parametrize('campaignType,reminderType', [
        ('coupon', 'COUPON_NOT_REDEEMED')
    ])
    def test_reminder_couponMessage_count_CouponNotRedeemed(self, campaignType, reminderType):
        campaignId = str(constant.config['reminder'][campaignType]['campaignId'])
        messageId = constant.config['reminder'][campaignType]['messageId']
        series_id = constant.config['reminder'][campaignType]['series_id']
        irisresponse = Reminder.getReminderCount(campaignId, messageId, reminderType)
        nfsResponse = Reminder.getReminderCountFromNFS(messageId, namev2='couponRedeemed',invert=True, intersection=True,series_id=series_id)
        Reminder.assertResponse(irisresponse, 200)
        Reminder.validateReminderCount(irisresponse, nfsResponse)
