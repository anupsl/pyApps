# -*- coding: utf-8 -*-
import time,pytest, random
from datetime import datetime
from src.Constant.constant import constant
from src.modules.luci.luciDBHelper import LuciDBHelper
from src.utilities.logger import Logger
from src.utilities.assertion import Assertion
from src.utilities.utils import Utils
from src.modules.luci.dracarysHelper import DracarysHelper
from src.modules.luci.luciHelper import LuciHelper
from src.modules.luci.dracarysObject import DracarysObject

class Test_Dracarys_SaveCouponReminder():

    def setup_class(self):
        Logger.logSuiteName(str(self).split('.')[-1])
        self.connObj = LuciHelper.getConnObj()
        self.DracraysConnObj = DracarysHelper.getConnObj()
        self.constructObj = DracarysObject()
        self.userId = constant.config['usersInfo'][0]['userId']
        self.tillId = constant.config['tillIds'][0]
        self.storeId = constant.config['storeIds'][0]

    def teardown_class(self):
        self.connObj = ''

    def setup_method(self, method):
        Logger.logMethodName(method.__name__)
        constant.config['requestId'] = 'dracarys_auto_'+str(random.randint(11111, 99999))
        self.couponConfig, self.couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self,couponConfigReq={"valid_days_from_create": 1,"expiry_strategy_value": 1, 'do_not_resend_existing_voucher' : 1, 'allow_multiple_vouchers_per_user' : 1})
        LuciHelper.issueCouponAndAssertions(self,self.couponSeriesId)

    @pytest.mark.parametrize('description, couponReminder, updateScheduler', [
        ('Save and update CouponReminder with SMS', [[1,constant.config['dateTime']['hour'],constant.config['dateTime']['mins'], [{'type' : 0, 'message' : {'message' : 'Test🇷 reminder Msg😁'}}]]],[[19,15,13,['update msg']], [5,9,37]]),
        ('Save and update CouponReminder with Email', [[1,constant.config['dateTime']['hour'],constant.config['dateTime']['mins'], [{'type' : 1, 'message' : {'subject' : 'Test reminder♜ MsgⓅⓡⓔⓥⓘⓔⓦ Ⓣⓔⓧⓣ', 'emailBody' : 'Voucher message for 🅿️🌱🎗✅🎐🎗🔱  🌴🎗❎🌴reminder＠'}}]]],[[19,15,13], [5,9,37]]),
        ('Save and update CouponReminder with Wechat', [[1,constant.config['dateTime']['hour'],constant.config['dateTime']['mins'], [{'type' : 2, 'message' : {}}]]],[[19, 15, 13], [5, 9, 37]]),
        ('Save and update CouponReminder with MobilePush', [[1,constant.config['dateTime']['hour'],constant.config['dateTime']['mins'], [{'type' : 3, 'message' : {}}]]],[[19, 15, 13], [5, 9, 37]])])
    def test_dracarys_SCR_01(self, description,couponReminder,updateScheduler):
        saveCouponReminderResponse = DracarysHelper.saveCouponExpiryReminder(self, reminderInfoList=couponReminder)[0]
        DracarysHelper.saveExpiryReminderAssertion(self,saveCouponReminderResponse,couponReminder)
        reminderMsgDB = LuciDBHelper.getCouponReminderMessages(self.couponSeriesId)
        Assertion.constructAssertion(reminderMsgDB != [], 'Reminder Message Update an DB Entry')

        updatedCouponReminderResponse = DracarysHelper.saveCouponExpiryReminder(self,isConfigupdate=True, updateConfigScheduler = {'couponReminderDetails' : saveCouponReminderResponse, 'updateScheduler' : updateScheduler})[0]
        DracarysHelper.saveExpiryReminderAssertion(self, updatedCouponReminderResponse, updateScheduler)
        getCouponReminder = DracarysHelper.getCouponReminder(self)
        Assertion.constructAssertion(getCouponReminder != [], 'Get CouponReminder call Returns the Saved CouponReminder Details')

    @pytest.mark.parametrize('description, couponReminder', [
        ('Send Expiry Reminder via SMS ', [[1,constant.config['dateTime']['hour'],constant.config['dateTime']['mins'], [{'type' : 0, 'message' : {'message' : "Hi {{first_name}} {{last_name}}, name: {{fullname}}, Coupon Code: {{voucher}}, {{valid_days_from_create}},{{valid_till_date.FORMAT_1}},{{valid_till_date.FORMAT_2}},{{valid_till_date.FORMAT_3}},{{valid_till_date.FORMAT_4}},{{valid_till_date.FORMAT_5}},{{valid_till_date.FORMAT_6}},{{valid_till_date.FORMAT_7}},{{valid_till_date.FORMAT_8}}, {{optout}}"}}]]]),
        ('Send Expiry Reminder via EMAIL', [[1,constant.config['dateTime']['hour'],constant.config['dateTime']['mins'], [{'type' : 1, 'message' : {'subject' : 'Expiry reminder Email', 'emailBody' : 'Hi {{first_name}} {{last_name}}, name: {{fullname}}, Coupon Code: {{voucher}}, {{valid_days_from_create}},{{valid_till_date.FORMAT_1}},{{valid_till_date.FORMAT_2}},{{valid_till_date.FORMAT_3}},{{valid_till_date.FORMAT_4}},{{valid_till_date.FORMAT_5}},{{valid_till_date.FORMAT_6}},{{valid_till_date.FORMAT_7}},{{valid_till_date.FORMAT_8}}, {{unsubscribe}}'}}]]]),
        ('Send Expiry Reminder via SMS & EMAIL', [[1,constant.config['dateTime']['hour'],constant.config['dateTime']['mins'], [{'type' : 1, 'message' : {'subject' : 'Expiry reminder Email', 'emailBody' : 'Hi {{first_name}} {{last_name}}, name: {{fullname}}, Coupon Code: {{voucher}}, {{valid_days_from_create}},{{valid_till_date.FORMAT_1}},{{valid_till_date.FORMAT_2}},{{valid_till_date.FORMAT_3}},{{valid_till_date.FORMAT_4}},{{valid_till_date.FORMAT_5}},{{valid_till_date.FORMAT_6}},{{valid_till_date.FORMAT_7}},{{valid_till_date.FORMAT_8}}, {{unsubscribe}}'}}, {'type' : 0, 'message' : {'message' : "Hi {{first_name}} {{last_name}}, name: {{fullname}}, Coupon Code: {{voucher}}, {{valid_days_from_create}},{{valid_till_date.FORMAT_1}},{{valid_till_date.FORMAT_2}},{{valid_till_date.FORMAT_3}},{{valid_till_date.FORMAT_4}},{{valid_till_date.FORMAT_5}},{{valid_till_date.FORMAT_6}},{{valid_till_date.FORMAT_7}},{{valid_till_date.FORMAT_8}}, {{optout}}"}}]]])])
    def test_dracarys_SCR_02(self, description,couponReminder):
        tmpDate = DracarysHelper.getValueOfDay(minsToAdd=2)
        couponReminder[0][1:3] = [tmpDate['hour'],tmpDate['mins']]
        response,reminderIds,messageIds = DracarysHelper.saveCouponExpiryReminder(self, reminderInfoList=couponReminder)
        DracarysHelper.saveExpiryReminderAssertion(self, response, couponReminder)
        for _ in range(15):
            if couponReminder[0][2] > DracarysHelper.getValueOfDay()['mins']:
                Logger.log('Waiting (15s) for Schduler Hour : {} & Minute: {} and Current Minute : {}'.format(couponReminder[0][1], couponReminder[0][2], DracarysHelper.getValueOfDay()['mins']))
                time.sleep(15)
            else:
                Logger.log('Waiting for Expiry Reminder cron execution')
                time.sleep(10)
                break
        for ids in reminderIds:
            status = LuciDBHelper.getReminderExecutionLog(self.couponSeriesId, ids)
            cronStatus = LuciDBHelper.getCronStatus(LuciDBHelper.getCouponReminder(self.couponSeriesId, reminderId=ids)[0]['cronId'])
            Assertion.constructAssertion(status in ['QUEUED', 'RUNNING', 'COMPLETED'], 'Published Messages updated on Execution logs and status : {}'.format(status))
            Assertion.constructAssertion(cronStatus in ['REMINDED', 'OPENED'], 'Cron status is Mismatch Actual: {} and Expected: {}'.format(cronStatus, ['REMINDED', 'OPENED']))
        for ids in messageIds:
            nsAdminId = LuciDBHelper.getSentReminderMessageId(self.couponSeriesId, ids)
            Assertion.constructAssertion(nsAdminId != [], ' Message Sent to the users NsAdmin-Id : {}'.format(nsAdminId))


    @pytest.mark.parametrize('description, couponReminder', [
        ('Save Reminder with all supportted tags SMS & EMAIL', [[1,constant.config['dateTime']['hour'],constant.config['dateTime']['mins'], [{'type' : 0, 'message' : {'message' : "{{first_name}},{{last_name}},{{fullname}},{{custom_field.age_group}},{{custom_field.anniversary}},{{custom_field.birthday}},{{custom_field.chchar}},{{custom_field.chinesecharacter}},{{custom_field.gender}},{{custom_field.pincode}},{{voucher}},{{valid_days_from_create}},{{valid_till_date.FORMAT_1}},{{valid_till_date.FORMAT_2}},{{valid_till_date.FORMAT_3}},{{valid_till_date.FORMAT_4}},{{valid_till_date.FORMAT_5}},{{valid_till_date.FORMAT_6}},{{valid_till_date.FORMAT_7}},{{valid_till_date.FORMAT_8}}, {{optout}}"}},{'type' : 1, 'message' : {'subject' : "{{first_name}},{{last_name}},{{fullname}},{{custom_field.age_group}},{{custom_field.anniversary}},{{custom_field.birthday}},{{custom_field.chchar}},{{custom_field.chinesecharacter}},{{custom_field.gender}},{{custom_field.pincode}},{{voucher}},{{valid_days_from_create}},{{valid_till_date.FORMAT_1}},{{valid_till_date.FORMAT_2}},{{valid_till_date.FORMAT_3}},{{valid_till_date.FORMAT_4}},{{valid_till_date.FORMAT_5}},{{valid_till_date.FORMAT_6}},{{valid_till_date.FORMAT_7}},{{valid_till_date.FORMAT_8}}", 'emailBody' : "{{first_name}},{{last_name}},{{fullname}},{{custom_field.age_group}},{{custom_field.anniversary}},{{custom_field.birthday}},{{custom_field.chchar}},{{custom_field.chinesecharacter}},{{custom_field.gender}},{{custom_field.pincode}},{{voucher}},{{valid_days_from_create}},{{valid_till_date.FORMAT_1}},{{valid_till_date.FORMAT_2}},{{valid_till_date.FORMAT_3}},{{valid_till_date.FORMAT_4}},{{valid_till_date.FORMAT_5}},{{valid_till_date.FORMAT_6}},{{valid_till_date.FORMAT_7}},{{valid_till_date.FORMAT_8}}, {{unsubscribe}}"}}]]]),
        ('Save Reminder with all supportted tags EMAIL', [[1,constant.config['dateTime']['hour'],constant.config['dateTime']['mins'], [{'type' : 1, 'message' : {'subject' : '{{first_name}},{{last_name}},{{fullname}},{{custom_field.age_group}},{{custom_field.anniversary}},{{custom_field.birthday}},{{custom_field.chchar}},{{custom_field.chinesecharacter}},{{custom_field.gender}},{{custom_field.pincode}},{{voucher}},{{valid_days_from_create}},{{valid_till_date.FORMAT_1}},{{valid_till_date.FORMAT_2}},{{valid_till_date.FORMAT_3}},{{valid_till_date.FORMAT_4}},{{valid_till_date.FORMAT_5}},{{valid_till_date.FORMAT_6}},{{valid_till_date.FORMAT_7}},{{valid_till_date.FORMAT_8}}', 'emailBody' : '{{first_name}},{{last_name}},{{fullname}},{{custom_field.age_group}},{{custom_field.anniversary}},{{custom_field.birthday}},{{custom_field.chchar}},{{custom_field.chinesecharacter}},{{custom_field.gender}},{{custom_field.pincode}},{{voucher}},{{valid_days_from_create}},{{valid_till_date.FORMAT_1}},{{valid_till_date.FORMAT_2}},{{valid_till_date.FORMAT_3}},{{valid_till_date.FORMAT_4}},{{valid_till_date.FORMAT_5}},{{valid_till_date.FORMAT_6}},{{valid_till_date.FORMAT_7}},{{valid_till_date.FORMAT_8}}, {{unsubscribe}}'}}]]]),
        ('Save Reminder with all supportted tags WECHAT', [[1,constant.config['dateTime']['hour'],constant.config['dateTime']['mins'], [{'type' : 2, 'message' : {'template': "{{first_name}},{{last_name}},{{fullname}},{{custom_field.age_group}},{{custom_field.anniversary}},{{custom_field.birthday}},{{custom_field.chchar}},{{custom_field.chinesecharacter}},{{custom_field.gender}},{{custom_field.pincode}},{{voucher}},{{valid_days_from_create}},{{valid_till_date.FORMAT_1}},{{valid_till_date.FORMAT_2}},{{valid_till_date.FORMAT_3}},{{valid_till_date.FORMAT_4}},{{valid_till_date.FORMAT_5}},{{valid_till_date.FORMAT_6}},{{valid_till_date.FORMAT_7}},{{valid_till_date.FORMAT_8}}, {{optout}}"}}]]]),
        ('Save Reminder with all supportted tags MOBILEPUSH', [[1,constant.config['dateTime']['hour'],constant.config['dateTime']['mins'], [{'type' : 3, 'message' : {}}]]])])
    def test_dracarys_SCR_03(self, description,couponReminder):
        if 'MOBILEPUSH' in description:
            couponReminder[0][3] = [{'type' : 3, 'message' : {'androidMessageDetails' : DracarysObject.mobilePushDetails({'title' : "{{first_name}},{{last_name}},{{fullname}},{{custom_field.age_group}},{{custom_field.anniversary}},{{custom_field.birthday}},{{custom_field.chchar}},{{custom_field.chinesecharacter}},{{custom_field.gender}},{{custom_field.pincode}},{{voucher}},{{valid_days_from_create}},{{valid_till_date.FORMAT_1}},{{valid_till_date.FORMAT_2}},{{valid_till_date.FORMAT_3}},{{valid_till_date.FORMAT_4}},{{valid_till_date.FORMAT_5}},{{valid_till_date.FORMAT_6}},{{valid_till_date.FORMAT_7}},{{valid_till_date.FORMAT_8}}", 'messageBlob' : "{{first_name}},{{last_name}},{{fullname}},{{custom_field.age_group}},{{custom_field.anniversary}},{{custom_field.birthday}},{{custom_field.chchar}},{{custom_field.chinesecharacter}},{{custom_field.gender}},{{custom_field.pincode}},{{voucher}},{{valid_days_from_create}},{{valid_till_date.FORMAT_1}},{{valid_till_date.FORMAT_2}},{{valid_till_date.FORMAT_3}},{{valid_till_date.FORMAT_4}},{{valid_till_date.FORMAT_5}},{{valid_till_date.FORMAT_6}},{{valid_till_date.FORMAT_7}},{{valid_till_date.FORMAT_8}}"})}}]
        response,reminderIds,messageIds = DracarysHelper.saveCouponExpiryReminder(self, reminderInfoList=couponReminder)
        DracarysHelper.saveExpiryReminderAssertion(self, response, couponReminder)
        reminderMsgDB = LuciDBHelper.getCouponReminderMessages(self.couponSeriesId)
        Assertion.constructAssertion(reminderMsgDB != [], 'Reminder Message Update an DB Entry')


    @pytest.mark.parametrize('description, couponReminder, updateScheduler, expected', [
        ('Reminder Msg Invalidate SMS and Added SMS', [[1,constant.config['dateTime']['hour'],constant.config['dateTime']['mins'], [{'type' : 0 ,'message' : {'message' : 'Test🇷 reminder Msg😁'}}]]],[{'type' : 0, 'typeObj' : 'smsMessage', 'message' : {'message' : 'updated SMS Test🇷 reminder Msg😁'}}], ['SMS', 'SMS']),
        ('Reminder Msg Invalidate SMS and Added Email', [[1,constant.config['dateTime']['hour'],constant.config['dateTime']['mins'], [{'type' : 0 ,'message' : {'message' : 'Test🇷 reminder Msg😁'}}]]],[{'type' : 1, 'typeObj' : 'emailMessage', 'message' : {'subject' : 'Updated to SMS to EMail' ,'emailBody' : 'Updated Test🇷 reminder Msg😁'}}], ['SMS', 'EMAIL']),
        ('Reminder Msg Invalidate Email and Added SMS', [[1,constant.config['dateTime']['hour'],constant.config['dateTime']['mins'], [{'type' : 1, 'message' : {'subject' : 'Test reminder♜ MsgⓅⓡⓔⓥⓘⓔⓦ Ⓣⓔⓧⓣ', 'emailBody' : 'Voucher message for 🅿️🌱🎗✅🎐🎗🔱  🌴🎗❎🌴reminder＠'}}]]],[{'type' : 0, 'typeObj' : 'smsMessage' , 'message' : {'message' : 'Test🇷 reminder Msg😁'}}], ['EMAIL', 'SMS']),
        ('Reminder Msg Invalidate WECHAT and Added Email', [[1,constant.config['dateTime']['hour'],constant.config['dateTime']['mins'], [{'type' : 2, 'message' : {}}]]],[{'type' : 1, 'typeObj' : 'emailMessage' ,'message' : {'subject' : 'Updated to Wechat to EMail' ,'emailBody' : 'Updated Test🇷 reminder Msg😁'}}], ['WECHAT', 'EMAIL']),
        ('Reminder Msg Invalidate Mobile_Push and Added SMS', [[1,constant.config['dateTime']['hour'],constant.config['dateTime']['mins'], [{'type' : 3, 'message' : {}}]]],[{'type' : 0, 'typeObj' : 'smsMessage' ,'message' : {'message' : 'Test🇷 reminder Msg😁'}}], ['MOBILE_PUSH', 'SMS'])])
    def test_dracarys_SCR_04(self, description,couponReminder,updateScheduler,expected):
        saveCouponReminderResponse = DracarysHelper.saveCouponExpiryReminder(self, reminderInfoList=couponReminder)[0]
        DracarysHelper.saveExpiryReminderAssertion(self, saveCouponReminderResponse, couponReminder)
        reminderMsgDB = LuciDBHelper.getCouponReminderMessages(self.couponSeriesId)
        Assertion.constructAssertion(reminderMsgDB != [], 'Reminder Message Update an DB Entry')
        Assertion.constructAssertion(reminderMsgDB[0]['type'] == expected[0], 'Reminder Message Type added Correctly')
        if updateScheduler[0]['typeObj'] == 'emailMessage':
            updateReminderMsg = {updateScheduler[0]['typeObj'] : DracarysObject.emailMessage(updateScheduler[0]['message'])}
        elif updateScheduler[0]['typeObj'] == 'smsMessage':
            updateReminderMsg = {updateScheduler[0]['typeObj'] : DracarysObject.smsMessage(updateScheduler[0]['message'])}
        updateReminderMsg.update({'type' : updateScheduler[0]['type']})
        reminderMsgDetailObj = DracarysObject.CouponReminderMessageDetails({'reminderMessage' : DracarysObject.reminderMessage(updateReminderMsg)})
        saveCouponReminderResponse[0]['reminderMessages'][0] = reminderMsgDetailObj

        saveCouponReminderRequest = DracarysObject.SaveCouponReminderRequest({'couponSeriesId': self.couponSeriesId, 'couponReminderDetails': [DracarysObject.CouponReminderDetails(saveCouponReminderResponse[0])]})
        self.DracraysConnObj.saveCouponReminder(saveCouponReminderRequest)
        reminderMsgDB = LuciDBHelper.getCouponReminderMessages(self.couponSeriesId)
        Assertion.constructAssertion(reminderMsgDB != [], 'Reminder Message Update an DB Entry')
        Assertion.constructAssertion(len(reminderMsgDB) == 1, 'Old Reminder Message Type Marked as invalid')
        Assertion.constructAssertion(reminderMsgDB[0]['type'] == expected[1], 'Updated Reminder Message Type Updated')

    @pytest.mark.parametrize('description, couponReminder, updateScheduler, expected', [
        ('Update Reminder Message Type SMS to Email', [[1,constant.config['dateTime']['hour'],constant.config['dateTime']['mins'], [{'type' : 0, 'message' : {'message' : 'Test🇷 reminder Msg😁'}}]]],[{'type' : 1, 'typeObj' : 'emailMessage','message' : {'subject' : 'Updated to SMS to EMail' ,'emailBody' : 'Updated Test🇷 reminder Msg😁'}}],['SMS', 'EMAIL']),
        ('Update Reminder Message Type Email to SMS', [[1,constant.config['dateTime']['hour'],constant.config['dateTime']['mins'], [{'type' : 1, 'message' : {'subject' : 'Test reminder♜ MsgⓅⓡⓔⓥⓘⓔⓦ Ⓣⓔⓧⓣ', 'emailBody' : 'Voucher message for 🅿️🌱🎗✅🎐🎗🔱  🌴🎗❎🌴reminder＠'}}]]],[{'type' : 0, 'typeObj' : 'smsMessage' ,'message' : {'message' : 'Test🇷 reminder Msg😁'}}],['EMAIL', 'SMS']),
        ('Update Reminder Message Type WECHAT to Email', [[1,constant.config['dateTime']['hour'],constant.config['dateTime']['mins'], [{'type' : 2, 'message' : {}}]]],[{'type' : 1, 'typeObj' : 'emailMessage','message' : {'subject' : 'Updated to SMS to EMail' ,'emailBody' : 'Updated Test🇷 reminder Msg😁'}}],['WECHAT', 'EMAIL']),
        ('Update Reminder Message Type MOBILE_PUSH to SMS', [[1,constant.config['dateTime']['hour'],constant.config['dateTime']['mins'], [{'type' : 3, 'message' : {}}]]],[{'type' : 0, 'typeObj' : 'smsMessage' ,'message' : {'message' : 'Test🇷 reminder Msg😁'}}],['MOBILE_PUSH', 'SMS'])])
    def test_dracarys_SCR_05(self, description,couponReminder,updateScheduler, expected):
        saveCouponReminderResponse = DracarysHelper.saveCouponExpiryReminder(self, reminderInfoList=couponReminder)[0]
        DracarysHelper.saveExpiryReminderAssertion(self, saveCouponReminderResponse, couponReminder)
        reminderMsgDB = LuciDBHelper.getCouponReminderMessages(self.couponSeriesId)
        Assertion.constructAssertion(reminderMsgDB != [], 'Reminder Message Update an DB Entry')
        reminderMsgId = reminderMsgDB[0]['id']
        id = (saveCouponReminderResponse[0]['reminderMessages'][0].__dict__)['id']
        if updateScheduler[0]['typeObj'] == 'emailMessage':
            updateReminderMsg = {updateScheduler[0]['typeObj'] : DracarysObject.emailMessage(updateScheduler[0]['message'])}
        elif updateScheduler[0]['typeObj'] == 'smsMessage':
            updateReminderMsg = {updateScheduler[0]['typeObj'] : DracarysObject.smsMessage(updateScheduler[0]['message'])}
        updateReminderMsg.update({'type' : updateScheduler[0]['type']})
        reminderMsgDetailObj = DracarysObject.CouponReminderMessageDetails({'reminderMessage' : DracarysObject.reminderMessage(updateReminderMsg), 'id' : id})
        saveCouponReminderResponse[0]['reminderMessages'][0] = reminderMsgDetailObj

        saveCouponReminderRequest = DracarysObject.SaveCouponReminderRequest({'couponSeriesId': self.couponSeriesId, 'couponReminderDetails': [DracarysObject.CouponReminderDetails(saveCouponReminderResponse[0])]})
        self.DracraysConnObj.saveCouponReminder(saveCouponReminderRequest)
        reminderMsgDB = LuciDBHelper.getCouponReminderMessages(self.couponSeriesId)
        Assertion.constructAssertion(reminderMsgDB != [], 'Reminder Message Update an DB Entry')
        Assertion.constructAssertion(len(reminderMsgDB) == 1, 'Old Reminder Message Type Marked as invalid')
        Assertion.constructAssertion(reminderMsgDB[0]['id'] == reminderMsgId, 'Update the Message Type with Existing Id Actual : {} and Expected : {}'.format(reminderMsgDB[0]['id'],reminderMsgId))
        Assertion.constructAssertion(reminderMsgDB[0]['type'] == expected[1], 'Updated Reminder Message Type Updated')

    @pytest.mark.parametrize('description, couponReminder, updateScheduler', [
        ('Invalidate CouponReminder SMS & add new reminder EMAIL', [[1,constant.config['dateTime']['hour'],constant.config['dateTime']['mins'], [{'type' : 0, 'message' : {'message' : 'Test🇷 reminder Msg😁'}}]]],[ {'type' : 1, 'typeObj': 'emailMessage', 'message' : {'subject' : 'Updated to SMS to EMail' ,'emailBody' : 'Updated Test🇷 reminder Msg😁'}}]),
        ('Invalidate CouponReminder Email & add new reminder SMS', [[1, constant.config['dateTime']['hour'], constant.config['dateTime']['mins'], [{'type': 1, 'message': {'subject': 'Test reminder♜ MsgⓅⓡⓔⓥⓘⓔⓦ Ⓣⓔⓧⓣ', 'emailBody': 'Voucher message for 🅿️🌱🎗✅🎐🎗🔱  🌴🎗❎🌴reminder＠'}}]]], [{'type': 0, 'typeObj': 'smsMessage', 'message': {'message': 'Test🇷 reminder Msg😁'}}]),
        ('Invalidate CouponReminder Wechat & add new reminder Email', [[1, constant.config['dateTime']['hour'], constant.config['dateTime']['mins'], [{'type': 2, 'message': {}}]]], [{'type': 1, 'typeObj': 'emailMessage', 'message': {'subject': 'Updated to SMS to EMail', 'emailBody': 'Updated Test🇷 reminder Msg😁'}}]),
        ('Invalidate CouponReminder Mobile_Push & add new reminder SMS', [[1, constant.config['dateTime']['hour'], constant.config['dateTime']['mins'], [{'type': 3, 'message': {}}]]], [{'type': 0, 'typeObj': 'smsMessage', 'message': {'message': 'Test🇷 reminder Msg😁'}}])])
    def test_dracarys_SCR_06(self, description,couponReminder,updateScheduler):
        saveCouponReminderResponse = DracarysHelper.saveCouponExpiryReminder(self, reminderInfoList=couponReminder)[0]
        DracarysHelper.saveExpiryReminderAssertion(self, saveCouponReminderResponse, couponReminder)
        couponReainderDB = LuciDBHelper.getCouponReminder(self.couponSeriesId)
        Assertion.constructAssertion(couponReainderDB != [], 'Coupon Reminder Added in DB')
        couponReminderId = couponReainderDB[0]['id']
        if updateScheduler[0]['typeObj'] == 'emailMessage':
            updateReminderMsg = {updateScheduler[0]['typeObj'] : DracarysObject.emailMessage(updateScheduler[0]['message'])}
        elif updateScheduler[0]['typeObj'] == 'smsMessage':
            updateReminderMsg = {updateScheduler[0]['typeObj'] : DracarysObject.smsMessage(updateScheduler[0]['message'])}
        updateReminderMsg.update({'type' : updateScheduler[0]['type']})
        reminderMsgDetailObj = DracarysObject.CouponReminderMessageDetails({'reminderMessage' : DracarysObject.reminderMessage(updateReminderMsg)})
        saveCouponReminderResponse[0]['reminderMessages'][0] = reminderMsgDetailObj
        saveCouponReminderResponse[0]['id'] = 0

        saveCouponReminderRequest = DracarysObject.SaveCouponReminderRequest({'couponSeriesId': self.couponSeriesId, 'couponReminderDetails': [DracarysObject.CouponReminderDetails(saveCouponReminderResponse[0])]})
        self.DracraysConnObj.saveCouponReminder(saveCouponReminderRequest)
        couponReainderDB = LuciDBHelper.getCouponReminder(self.couponSeriesId, is_active = 0)
        Assertion.constructAssertion(couponReainderDB != [], 'Coupon Reminder Added in DB')
        Assertion.constructAssertion(len(couponReainderDB) == 1, 'Previous Coupon Reminder Marked as InActive')
        Assertion.constructAssertion(couponReainderDB[0]['id'] == couponReminderId, 'Marked InActive previous coupon reminder Actual : {} and Expected : {}'.format(couponReainderDB[0]['id'], couponReminderId))

    @pytest.mark.parametrize('description, couponReminder', [
        ('Add Reminder past time', [[1,(constant.config['dateTime']['hour'] - 1),constant.config['dateTime']['mins'], [{'type' : 0, 'message' : {'message' : 'Test🇷 reminder Msg😁'}}]]])])
    def test_dracarys_SCR_07(self, description,couponReminder):
        DracarysHelper.saveCouponExpiryReminder(self, reminderInfoList=couponReminder)
        couponReainderDB = LuciDBHelper.getCouponReminder(self.couponSeriesId)
        datevalue = datetime.strptime(couponReainderDB[0]['next_scheduled_on'], '%Y-%m-%d %H:%M:%S')
        Assertion.constructAssertion(couponReainderDB != [], 'Coupon Reminder Added in DB')
        Assertion.constructAssertion(datevalue.year == constant.config['dateTime']['year'], 'Updated Next Schedule On Year Actual : {} and Expected : {}'.format(datevalue.year, constant.config['dateTime']['year']))
        Assertion.constructAssertion(datevalue.month == constant.config['dateTime']['month'], 'Updated Next Schedule On Month Actual : {} and Expected : {}'.format(datevalue.month, constant.config['dateTime']['month']))
        Assertion.constructAssertion(datevalue.day == (constant.config['dateTime']['day'] + 1), 'Updated Next Schedule On Date Actual : {} and Expected : {}'.format(datevalue.day , (constant.config['dateTime']['day'] + 1)))
        Assertion.constructAssertion(datevalue.hour == (constant.config['dateTime']['hour'] - 1), 'Updated Next Schedule On Hour Actual : {} and Expected : {}'.format(datevalue.hour , (constant.config['dateTime']['hour'] - 1)))


    @pytest.mark.parametrize('description, couponReminder,expectedException', [
        ('Save CouponReminder with Negative Hour', [[1,-24,constant.config['dateTime']['mins']]],[629,'invalid hour of day -24']),
        ('Save CouponReminder with Negative Minutes', [[1,12,-67]],[629,'invalid mminute of hour -67']),
        ('Save CouponReminder with Negative Hour & Minutes', [[1,-24,-67]],[629,'invalid hour of day -24']),
        ('Save CouponReminder with Invalid Hour', [[1,36,26]],[629,'invalid hour of day 36']),
        ('Save CouponReminder with Invalid Minutes', [[1,17,90]],[400,'Value 90 for minuteOfHour must be in the range [0,59]']),
        ('Save CouponReminder with Invalid Hour & Minutes', [[1,28,75]],[629,'invalid hour of day 28'])])
    def test_dracarys_SCR_08(self, description,couponReminder,expectedException):
        try:
            DracarysHelper.saveCouponExpiryReminder(self, reminderInfoList=couponReminder)
        except Exception, dracarysExp:
            dracarysExp = dracarysExp.__dict__
            Assertion.constructAssertion(dracarysExp['errorCode'] == expectedException[0], 'Dracarys Error Code Actual : {} and Expected : {}'.format(dracarysExp['errorCode'] , expectedException[0]))
            Assertion.constructAssertion(dracarysExp['errorMsg'] == expectedException[1], 'Dracarys Error Message Actual : {} and Expected : {}'.format(dracarysExp['errorMsg'] , expectedException[1]))

    @pytest.mark.parametrize('description, couponReminder, invalidData,expectedException', [
        ('Save CouponReminder with Negative orgId', [[1,-24,constant.config['dateTime']['mins']]], [-1,0] ,[500,'invalid org id -1']),
        ('Save CouponReminder with Negative CouponSeriesId', [[1,12,-67]],[0,-1],[501,'invalid coupon series id -1'])])
    def test_dracarys_SCR_09(self, description,couponReminder,invalidData,expectedException):
        actualOrgId = constant.config['orgId']
        actualCouponSeriesId = self.couponSeriesId
        try:
            if invalidData[0] != 0:
                constant.config['orgId'] = invalidData[0]
            if invalidData[1] != 0:
                self.couponSeriesId = invalidData[1]
            DracarysHelper.saveCouponExpiryReminder(self, reminderInfoList=couponReminder)
        except Exception, dracarysExp:
            dracarysExp = dracarysExp.__dict__
            Assertion.constructAssertion(dracarysExp['errorCode'] == expectedException[0], 'Dracarys Error Code Actual : {} and Expected : {}'.format(dracarysExp['errorCode'] , expectedException[0]))
            Assertion.constructAssertion(dracarysExp['errorMsg'] == expectedException[1], 'Dracarys Error Message Actual : {} and Expected : {}'.format(dracarysExp['errorMsg'] , expectedException[1]))
        finally:
            constant.config['orgId'] = actualOrgId
            self.couponSeriesId = actualCouponSeriesId

    @pytest.mark.parametrize('description, inputData, expectedException', [
        ('Get CouponReminder Invalid OrgId', {'orgId' : -1},[500,'invalid org id -1']),
        ('Get CouponReminder Invalid CouponSeriesId', {'couponSeriesId': -1},[501,'invalid coupon series id -1'])])
    def test_dracarys_SCR_10(self, description, inputData,expectedException):
        try:
            tmpDict = {'couponSeriesId': self.couponSeriesId}
            tmpDict.update(inputData)
            getCouponReminderRequest = DracarysObject.GetCouponReminderRequest(tmpDict)
            self.DracraysConnObj.getCouponReminders(getCouponReminderRequest)
        except Exception, dracarysExp:
            dracarysExp = dracarysExp.__dict__
            Assertion.constructAssertion(dracarysExp['errorCode'] == expectedException[0], 'Dracarys Error Code Actual : {} and Expected : {}'.format(dracarysExp['errorCode'], expectedException[0]))
            Assertion.constructAssertion(dracarysExp['errorMsg'] == expectedException[1], 'Dracarys Error Message Actual : {} and Expected : {}'.format(dracarysExp['errorMsg'], expectedException[1]))

    @pytest.mark.skipif(constant.config['cluster'] not in ['nightly'], reason='Wechat Configured only in nightly')
    @pytest.mark.parametrize('description, couponReminder', [
        ('Publish with Simple WECHAT', [[1, constant.config['dateTime']['hour'], constant.config['dateTime']['mins'], [{'type': 2, 'message': {"template":"{\"template_id\":\"Nc9fDFlKRMWdaoxZtjzSkNo_teR1Cw8CH1TNXhlf0jc\",\"Title\":\"订阅模板消息\",\"Tag\":[\"content\"],\"url\":\"nbhjkj\",\"TopColor\":\"#000000\",\"data\":{\"content\":{\"value\":\"ihuhkj\",\"color\":\"#00000\"}, {{first_name}},{{last_name}},{{fullname}}, voucher : {{voucher}},{{valid_days_from_create}},{{valid_till_date.FORMAT_1}},{{valid_till_date.FORMAT_2}},{{valid_till_date.FORMAT_3}},{{valid_till_date.FORMAT_4}},{{valid_till_date.FORMAT_5}},{{valid_till_date.FORMAT_6}},{{valid_till_date.FORMAT_7}},{{valid_till_date.FORMAT_8}}, {{optout}}},\"preview\":\"\",\"BrandId\":\"f\",\"OriginalId\":\"gh_b5e131178808\",\"isInternalUrl\":\"\",\"creative_template_id\":\"5aa769497462373a5f0792b8\"}","originalId":"gh_b5e131178808","brandId":"f","wechatId":"5aa769497462373a5f0792b8"}}]]])])
    def test_dracarys_Wechat(self, description, couponReminder):
        actualOrgId = constant.config['orgId']
        tmpDate = DracarysHelper.getValueOfDay(minsToAdd=2)
        couponReminder[0][1:3] = [tmpDate['hour'], tmpDate['mins']]
        try:
            constant.config['orgId'] = 780
            self.couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self, couponConfigReq={"valid_days_from_create": 1, "expiry_strategy_value": 1})[1]
            self.userId = 313229998
            LuciHelper.issueCouponAndAssertions(self, self.couponSeriesId)
            response, reminderIds, messageIds = DracarysHelper.saveCouponExpiryReminder(self, reminderInfoList=couponReminder)
            for _ in range(15):
                if couponReminder[0][2] > DracarysHelper.getValueOfDay()['mins']:
                    Logger.log('Waiting (15s) for Schduler Hour : {} & Minute: {} and Current Minute : {}'.format(couponReminder[0][1], couponReminder[0][2], DracarysHelper.getValueOfDay()['mins']))
                    time.sleep(15)
                else:
                    Logger.log('Waiting for Expiry Reminder cron execution')
                    time.sleep(10)
                    break
            for ids in reminderIds:
                status = LuciDBHelper.getReminderExecutionLog(self.couponSeriesId, ids)
                Assertion.constructAssertion(status in ['QUEUED', 'RUNNING', 'COMPLETED'], 'Published Messages updated on Execution logs and status : {}'.format(status))
            for ids in messageIds:
                nsAdminId = LuciDBHelper.getSentReminderMessageId(self.couponSeriesId, ids)
                Assertion.constructAssertion(nsAdminId != [], ' Message Sent to the users NsAdmin-Id : {}'.format(nsAdminId))
        finally:
            constant.config['orgId'] = actualOrgId

    @pytest.mark.skip(reason='Bulk SMS expiry Reminder Message')
    @pytest.mark.parametrize('description, couponReminder', [
        ('Bulk Expiry Reminder SMS', [[1, constant.config['dateTime']['hour'], constant.config['dateTime']['mins'], [{'type' : 0, 'message' : {'message' : "Test Msg for Reminder"}},{'type' : 1, 'message' : {'subject' : "Test Msg Subject", 'emailBody' : "Test Msg Email Body"}}]]])])
    def test_dracarys_SCR_012(self, description,couponReminder):
        LuciDBHelper.getUsers(3000)
        self.userIds = []
        for i in range(len(constant.config['usersInfo'])):
            self.userIds.append(constant.config['usersInfo'][i]['userId'])
        for _ in range(20):
            LuciHelper.issueMultipleCoupon(self,self.couponSeriesId,userList=self.userIds)
        response,reminderIds,messageIds = DracarysHelper.saveCouponExpiryReminder(self, reminderInfoList=couponReminder)

    @pytest.mark.parametrize('description, couponReminder', [
        ('Cron status ', [[1,constant.config['dateTime']['hour'],constant.config['dateTime']['mins'], [{'type' : 0, 'message' : {'message' : "Hi {{first_name}} {{last_name}}, name: {{fullname}}, Coupon Code: {{voucher}}, {{valid_days_from_create}},{{valid_till_date.FORMAT_1}},{{valid_till_date.FORMAT_2}},{{valid_till_date.FORMAT_3}},{{valid_till_date.FORMAT_4}},{{valid_till_date.FORMAT_5}},{{valid_till_date.FORMAT_6}},{{valid_till_date.FORMAT_7}},{{valid_till_date.FORMAT_8}}, {{optout}}"}}]]])])
    def test_dracarys_SCR_13_sanity_smoke(self, description,couponReminder):
        tmpDate = DracarysHelper.getValueOfDay(minsToAdd=2)
        couponReminder[0][1:3] = [tmpDate['hour'],tmpDate['mins']]
        response,reminderIds,messageIds = DracarysHelper.saveCouponExpiryReminder(self, reminderInfoList=couponReminder)
        DracarysHelper.saveExpiryReminderAssertion(self, response, couponReminder)
        self.couponConfig.update({'fixedExpiryDate': Utils.getTime(days=-1, milliSeconds=True)})
        LuciHelper.saveCouponConfigAndAssertions(self, couponConfigReq=self.couponConfig)
        for _ in range(15):
            if couponReminder[0][2] > DracarysHelper.getValueOfDay()['mins']:
                Logger.log('Waiting (15s) for Schduler Hour : {} & Minute: {} and Current Minute : {}'.format(couponReminder[0][1], couponReminder[0][2], DracarysHelper.getValueOfDay()['mins']))
                time.sleep(15)
            else:
                Logger.log('Waiting for Expiry Reminder cron execution')
                time.sleep(10)
                break
        cronTaskId = LuciDBHelper.getCouponReminder(self.couponSeriesId, reminderId=reminderIds[0])[0]['cronId']
        cronStatus = LuciDBHelper.getCronStatus(cronTaskId)
        Assertion.constructAssertion(cronStatus == 'CLOSED', 'Coupon series Expired  & Cron status is Mismatch Actual: {} and Expected: {}'.format(cronStatus, 'CLOSED'))

        self.couponConfig.update({'description' : 'Cron scheduler update'})
        LuciHelper.saveCouponConfigAndAssertions(self,couponConfigReq=self.couponConfig)
        tmpDate = DracarysHelper.getValueOfDay()
        couponReminder[0][1:3] = [tmpDate['hour'], tmpDate['mins']]
        updatedCouponReminderResponse = DracarysHelper.saveCouponExpiryReminder(self, isConfigupdate=True, updateConfigScheduler={'couponReminderDetails': response, 'updateScheduler': couponReminder})[0]
        DracarysHelper.saveExpiryReminderAssertion(self, updatedCouponReminderResponse, couponReminder)

        cronStatus = LuciDBHelper.getCronStatus(cronTaskId)
        Assertion.constructAssertion(cronStatus == 'CLOSED', 'Updated Coupon Config & Cron status is Mismatch Actual: {} and Expected: {}'.format(cronStatus, 'CLOSED'))

        self.couponConfig.update({'fixedExpiryDate': Utils.getTime(days=1, milliSeconds=True)})
        LuciHelper.saveCouponConfigAndAssertions(self, couponConfigReq=self.couponConfig)
        tmpDate = DracarysHelper.getValueOfDay()
        couponReminder[0][1:3] = [tmpDate['hour'], tmpDate['mins']]
        DracarysHelper.saveCouponExpiryReminder(self, isConfigupdate=True, updateConfigScheduler={'couponReminderDetails': updatedCouponReminderResponse, 'updateScheduler': couponReminder})
        cronStatus = LuciDBHelper.getCronStatus(LuciDBHelper.getCouponReminder(self.couponSeriesId, reminderId=reminderIds[0])[0]['cronId'])
        Assertion.constructAssertion(cronStatus in ['REMINDED', 'OPENED'], 'Extened Coupon series Expiry date & Cron status is Mismatch Actual: {} and Expected: {}'.format(cronStatus, ['REMINDED', 'OPENED']))

    @pytest.mark.parametrize('description, couponReminder', [
        ('Send Expiry Reminder via SMS valid_till_date None ', [[1,constant.config['dateTime']['hour'],constant.config['dateTime']['mins'], [{'type' : 0, 'message' : {'message' : "Hi {{first_name}} {{last_name}}, name: {{fullname}}, Coupon Code: {{voucher}}, {{valid_days_from_create}},{{valid_till_date.FORMAT_1}},{{valid_till_date.FORMAT_2}},{{valid_till_date.FORMAT_3}},{{valid_till_date.FORMAT_4}},{{valid_till_date.FORMAT_5}},{{valid_till_date.FORMAT_6}},{{valid_till_date.FORMAT_7}},{{valid_till_date.FORMAT_8}}, {{optout}}"}}]]])
        ])
    def test_dracarys_SCR_14(self, description,couponReminder):
        self.couponConfig, self.couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self, couponConfigReq={"valid_till_date": None, "valid_days_from_create": 1, "expiry_strategy_value": 1, 'do_not_resend_existing_voucher': 1, 'allow_multiple_vouchers_per_user': 1, 'owned_by': 2, 'owner_id': constant.config['campaignId'], 'ownerValidity': Utils.getTime(days=2, milliSeconds=True)});
        LuciHelper.issueCouponAndAssertions(self, self.couponSeriesId)
        tmpDate = DracarysHelper.getValueOfDay(minsToAdd=2)
        couponReminder[0][1:3] = [tmpDate['hour'],tmpDate['mins']]
        response,reminderIds,messageIds = DracarysHelper.saveCouponExpiryReminder(self, reminderInfoList=couponReminder)
        DracarysHelper.saveExpiryReminderAssertion(self, response, couponReminder)
        for _ in range(15):
            if couponReminder[0][2] > DracarysHelper.getValueOfDay()['mins']:
                Logger.log('Waiting (15s) for Schduler Hour : {} & Minute: {} and Current Minute : {}'.format(couponReminder[0][1], couponReminder[0][2], DracarysHelper.getValueOfDay()['mins']))
                time.sleep(15)
            else:
                Logger.log('Waiting for Expiry Reminder cron execution')
                time.sleep(10)
                break
        for ids in reminderIds:
            status = LuciDBHelper.getReminderExecutionLog(self.couponSeriesId, ids)
            cronStatus = LuciDBHelper.getCronStatus(LuciDBHelper.getCouponReminder(self.couponSeriesId, reminderId=ids)[0]['cronId'])
            Assertion.constructAssertion(status in ['QUEUED', 'RUNNING', 'COMPLETED'], 'Published Messages updated on Execution logs and status : {}'.format(status))
            Assertion.constructAssertion(cronStatus in ['REMINDED', 'OPENED'], 'Cron status is Mismatch Actual: {} and Expected: {}'.format(cronStatus, ['REMINDED', 'OPENED']))
        for ids in messageIds:
            nsAdminId = LuciDBHelper.getSentReminderMessageId(self.couponSeriesId, ids)
            Assertion.constructAssertion(nsAdminId != [], ' Message Sent to the users NsAdmin-Id : {}'.format(nsAdminId))

    @pytest.mark.parametrize('description, couponReminder', [
        ('Send Expiry Reminder via SMS ', [[1,constant.config['dateTime']['hour'],constant.config['dateTime']['mins'], [{'type' : 0, 'message' : {'message' : "Hi {{first_name}} {{last_name}}, name: {{fullname}}, Coupon Code: {{voucher}}, {{valid_days_from_create}},{{valid_till_date.FORMAT_1}},{{valid_till_date.FORMAT_2}},{{valid_till_date.FORMAT_3}},{{valid_till_date.FORMAT_4}},{{valid_till_date.FORMAT_5}},{{valid_till_date.FORMAT_6}},{{valid_till_date.FORMAT_7}},{{valid_till_date.FORMAT_8}}, {{optout}}"}}]]])
        ])
    def test_dracarys_SCR_15_sanity(self, description,couponReminder):
        for _ in range(10):
            LuciHelper.issueCouponAndAssertions(self, self.couponSeriesId)
        issuedCount = LuciDBHelper.getCouponsIssued_Count(self.couponSeriesId)
        tmpDate = DracarysHelper.getValueOfDay(minsToAdd=2)
        couponReminder[0][1:3] = [tmpDate['hour'],tmpDate['mins']]
        response,reminderIds,messageIds = DracarysHelper.saveCouponExpiryReminder(self, reminderInfoList=couponReminder)
        DracarysHelper.saveExpiryReminderAssertion(self, response, couponReminder)
        for _ in range(15):
            if couponReminder[0][2] > DracarysHelper.getValueOfDay()['mins']:
                Logger.log('Waiting (15s) for Schduler Hour : {} & Minute: {} and Current Minute : {}'.format(couponReminder[0][1], couponReminder[0][2], DracarysHelper.getValueOfDay()['mins']))
                time.sleep(15)
            else:
                Logger.log('Waiting for Expiry Reminder cron execution')
                time.sleep(10)
                break
        for ids in reminderIds:
            status = LuciDBHelper.getReminderExecutionLog(self.couponSeriesId, ids)
            cronStatus = LuciDBHelper.getCronStatus(LuciDBHelper.getCouponReminder(self.couponSeriesId, reminderId=ids)[0]['cronId'])
            Assertion.constructAssertion(status in ['QUEUED', 'RUNNING', 'COMPLETED'], 'Published Messages updated on Execution logs and status : {}'.format(status))
            Assertion.constructAssertion(cronStatus in ['REMINDED', 'OPENED'], 'Cron status is Mismatch Actual: {} and Expected: {}'.format(cronStatus, ['REMINDED', 'OPENED']))
        for ids in messageIds:
            nsAdminIdsCount = LuciDBHelper.getSentReminderMessageId(self.couponSeriesId, ids, isCount=True)
            Assertion.constructAssertion(nsAdminIdsCount == issuedCount, ' Reminder Message sent all issuedCoupons Actual: {} Expected: {}'.format(nsAdminIdsCount,issuedCount))