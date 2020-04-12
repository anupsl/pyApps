import datetime
from src.utilities.logger import Logger
from src.Constant.constant import constant
from src.utilities.dbhelper import dbHelper

class LuciDBHelper():

    @staticmethod
    def getAdminUserId():
        emailId = constant.config['intouchUsername']
        if emailId == 'ashish':
            emailId = 'cap@coin.com'

        query = 'SELECT ref_id FROM `authentication`.`loggable_users` WHERE `id` = ' \
                '(SELECT ref_id FROM `authentication`.`user_attributes` WHERE ' \
                '`identifier` = \'' + emailId + '\')'
        result = dbHelper.queryDB(query, "authentication")[0]
        if len(result) != 0:
            constant.config['adminId'] = result[0]
        else:
            Logger.log('ADMIN ID NOT FOUND')
            raise ValueError('ADMIN ID NOT FOUND')

    @staticmethod
    def getOTP():
        query = 'SELECT otp from otp_history where loggable_user_id = ' + constant.config['userId'] + ' order by id desc limit 1'
        result = dbHelper.queryDB(query, "authentication")[0]
        if len(result) != 0:
            return result[0]
        else:
            Logger.log('OTP Not found Generated')
            raise ValueError('OTP Not found Generated')

    @staticmethod
    def getCouponsCreated_Count(couponSeriesId, isValid = -1):
        query = 'SELECT count(1) FROM `luci`.`coupons_created` WHERE `org_id` = ' + str(constant.config['orgId']) + \
                ' AND `coupon_series_id` = ' + str(couponSeriesId)
        if isValid >= 0:
            query = query + ' AND is_valid = ' + str(isValid)
        result = dbHelper.queryDB(query, "luci")
        if len(result) == 0:
            Logger.log('No records found')
            return None
        else:
            return result[0][0]

    @staticmethod
    def getTillDiffTimeZone():
        query = "SELECT id FROM  `masters`.`org_entities` WHERE  `org_id` = {} AND `type` = 'STORE' AND `is_active` = 1 and code like 'lucitz1' ORDER BY `org_entities`.`id`".format(constant.config['orgId'])
        result = dbHelper.queryDB(query, "masters")[0]
        if len(result) != 0:
            return result[0]
        else:
            Logger.log('Luci TimeZone till now found')


    @staticmethod
    def getCouponsCreated(couponSeriesId, isValid= -1, couponCode = None):
        couponsCreatedList = []
        query = "SELECT `id`, `coupon_code`, `coupon_series_id`, `series_expiry_date`, `is_valid` " \
                "FROM `luci`.`coupons_created` WHERE `org_id` = " + str(constant.config['orgId']) + \
                " AND `coupon_series_id` = " + str(couponSeriesId)
        if couponCode != None:
            query += " AND `coupon_code` = '" + couponCode + "'"
        if isValid >= 0:
            query = query + " AND is_valid = " + str(isValid)

        result = dbHelper.queryDB(query, "luci")
        if len(result) == 0:
            Logger.log('No records found')
            return couponsCreatedList
        else:
            for k in result:
                couponsCreatedList.append({'id' : k[0], 'couponCode' : k[1], 'coupon_series_id' : k[2],
                                          'series_expiry_date' : k[3], 'is_valid' : k[4]})
            return couponsCreatedList

    @staticmethod
    def getPartnerIssuedCoupons(couponSeriesId):
        query = "SELECT `id`, `partner_org_id`, `coupon_code`, `coupon_series_id`, `issued_by_id`, `requested_by_id`, `issued_on`, `notes`, `last_updated_on`, `is_valid`, `coupon_issued_id` " + \
                "FROM `luci`.`partner_issued_coupons` WHERE `org_id` = " + constant.config[
                    'org_id'] + " AND `coupon_series_id` = " + couponSeriesId
        result = dbHelper.queryDB(query, "luci")
        if len(result) == 0:
            Logger.log('No records found')

    @staticmethod
    def getIssuedCoupons(couponSeriesId):
        query = 'SELECT coupon_code, issued_to FROM luci.coupons_issued WHERE org_id = {} AND coupon_series_id = {} AND active = 1'.format(constant.config['orgId'], couponSeriesId)
        result = dbHelper.queryDB(query, "luci")
        couponsIssued = []
        if len(result) == 0:
            Logger.log('No records found')
            return couponsIssued
        else:
            for k in result:
                couponsIssued.append({'couponCode' : k[0],'issuedTo' : k[1]})
        return couponsIssued

    @staticmethod
    def getCouponsIssued(couponSeriesId, userId, couponCode = None):
        query = 'SELECT id, coupon_code, issued_to, coupon_series_id, issued_by FROM luci.coupons_issued WHERE org_id = {} AND coupon_series_id = {} AND issued_to = {} AND active = 1'.format(constant.config['orgId'], couponSeriesId ,userId)
        if couponCode != None:
            query +=  " AND coupon_code = '{}'".format(couponCode)
        result = dbHelper.queryDB(query, "luci")
        couponsIssued = {}
        if len(result) == 0:
            Logger.log('No records found')
            return couponsIssued
        else:
            for k in result:
                couponsIssued = {'id' : k[0], 'couponCode' : k[1],'issuedTo' : k[2],'couponSeriedId' : k[3], 'issuedBy' : k[4]}
        return couponsIssued

    @staticmethod
    def getCouponsIssuedList(couponSeriesId, dbTimeJustBeforeUpload = None):
        couponsIssuedList = []
        query = "SELECT `id`, `coupon_code`, `issued_to`, `coupon_series_id`, `issued_by` " + \
                "FROM `luci`.`coupons_issued` WHERE `org_id` = " + str(constant.config['orgId']) + \
                " AND `coupon_series_id` = " + str(couponSeriesId)

        if dbTimeJustBeforeUpload is not None:
            query = query + " AND `issued_date` > '" + str(dbTimeJustBeforeUpload) + "'"

        result = dbHelper.queryDB(query, "luci")
        if len(result) == 0:
            Logger.log('No records found')
            return couponsIssuedList
        else:
            for k in result:
                couponsIssuedList.append({'id' : k[0], 'couponCode' : k[1], 'issuedTo' : k[2],
                                          'couponSeriesId' : k[3], 'issuedBy' : k[4]})
            return couponsIssuedList

    @staticmethod
    def getCouponRedemptions(couponIssuedId):
        query = "SELECT * FROM `luci`.`coupon_redemptions` WHERE `coupon_issued_id` = " + couponIssuedId
        result = dbHelper.queryDB(query, "luci")
        if len(result) == 0:
            Logger.log('No records found')

    @staticmethod
    def getCouponRedemptionsListByCouponIssuedId(couponIssuedId):
        query = "SELECT * FROM `luci`.`coupon_redemptions` WHERE `coupon_issued_id` = " + couponIssuedId
        result = dbHelper.queryDB(query, "luci")
        if len(result) == 0:
            Logger.log('No records found')

    @staticmethod
    def getCouponRedemptionsListByCouponSeriesId(couponSeriesId):
        couponRedemptionsList = []
        query = "SELECT * FROM `luci`.`coupon_redemptions` WHERE `org_id` = " + str(constant.config['orgId']) \
                + " AND `coupon_series_id` = " + str(couponSeriesId)
        result = dbHelper.queryDB(query, "luci")
        if len(result) == 0:
            Logger.log('No records found')
            return None
        else:
            for k in result:
                couponRedemptionsList.append({'id' : k[0], 'orgId' : k[1],'couponSeriesId' : k[2], 'couponIssuedId' : k[3],
                                              'redeemedUserId' : k[4], 'redeemedDate' : k[5], 'redeemedAtStore' : k[6],
                                              'billId' : k[7], 'billNumber' : k[8], 'details' : k[9], 'entryType' : k[10],
                                              'validationCodeUsed' : k[11]})
            return  couponRedemptionsList

    @staticmethod
    def getCouponSentHistoryList_ignoring(couponSeriesId, couponIssuedId = 0):
        query = "SELECT *  FROM `luci`.`coupon_sent_history` WHERE `org_id` = " + str(constant.config['orgId']) + \
                " AND `coupon_series_id` = " + str(couponSeriesId)
        if couponIssuedId != 0:
            query = query + " AND `coupon_issued_id` = " + str(couponIssuedId)
        result = dbHelper.queryDB(query, "luci")
        couponSentHistory = []
        if len(result) == 0:
            Logger.log('No records found')
            return couponSentHistory
        else:
            for k in result:
                couponSentHistory.append({'id' : k[0], 'orgId' : k[1], 'couponSeriesId' : k[2], 'couponIssuedId' : k[3],
                                          'sentDate' : k[4], 'sentFromStore' : k[5], 'notes' : k[6], 'autoUpdatedTime' : k[7]})
        return couponSentHistory

    @staticmethod
    def getMergeUserLogList(fromUserId, toUserId):
        query = "SELECT * FROM `merge_user_log` WHERE `org_id` = " + constant.config['orgId'] + \
                " AND `from_user_id` = " + fromUserId + " AND `to_user_id` = " + toUserId
        result = dbHelper.queryDB(query, "luci")
        if len(result) == 0:
            Logger.log('No records found')

    @staticmethod
    def getCouponsIssued_Count(couponSeriesId,active = -1, couponCode = None):
        query = "SELECT count(1) FROM `luci`.`coupons_issued` WHERE `org_id` = " + str(constant.config['orgId']) + " AND `coupon_series_id` = " + \
                str(couponSeriesId)
        if active >= 0:
            query += " AND `active` = " + str(active)
        elif couponCode != None:
            query += " AND `coupon_code` = " + couponCode

        result = dbHelper.queryDB(query, "luci")
        if len(result) == 0:
            Logger.log('No records found')
        else:
            return result[0][0]

    @staticmethod
    def getVoucherProductDataValues(voucherSeriesId, isValid = True):
        query = "SELECT * FROM `campaigns`.`voucher_product_data_values` WHERE `org_id` = " + str(constant.config['orgId']) \
                + " AND `voucher_series_id` = " + str(voucherSeriesId) + " AND is_valid = " + str(isValid)
        result = dbHelper.queryDB(query, "campaigns")
        tmpList =[]
        if len(result) == 0:
            Logger.log('No records found')
            return tmpList
        else:
            for k in result:
                VoucherProductDataValues = {'id': k[0], 'voucher_product_id': k[1], 'org_id': k[2], 'voucher_series_id': k[3],
                           'product_id' : k[4], 'isValid': k[5],'auto_update_time': k[6]}
                tmpList.append(VoucherProductDataValues)
        return tmpList

    @staticmethod
    def getVoucherProductMetaData(productType):
        query = "SELECT * FROM `campaigns`.`voucher_product_meta_data` WHERE " \
				+ "`product_type` = '" + productType + "'"
        result = dbHelper.queryDB(query, "campaigns")
        tmpList =[]
        if len(result) == 0:
            Logger.log('No records found')
            return tmpList
        else:
            for k in result:
                VoucherProductMetaData = {'id': k[0], 'product_type': k[1]}
                tmpList.append(VoucherProductMetaData)
        return tmpList

    @staticmethod
    def getActiveTillIdList():
        Logger.log('Retrieving Active Till Ids')
        query = "SELECT id FROM  `masters`.`org_entities` WHERE  `org_id` = " + str(constant.config['orgId']) + \
				" AND `type` = 'TILL' AND `is_active` = 1 ORDER BY `org_entities`.`id` ASC"
        result = dbHelper.queryDB(query, "masters")
        constant.config['tillIds'] = []
        if len(result) == 0:
            Logger.log('No records found')
        else:
            Logger.log('Retrieved data successfully')
            for k in result:
                constant.config['tillIds'] += k

    @staticmethod
    def getActiveStoreIdList():
        Logger.log('Retrieving Active Store Ids')
        query = "SELECT id FROM  `masters`.`org_entities` WHERE  `org_id` = " + str(constant.config['orgId']) + \
				" AND `type` = 'STORE' AND `is_active` = 1 ORDER BY `org_entities`.`id` ASC"
        result = dbHelper.queryDB(query, "masters")
        constant.config['storeIds'] = []
        if len(result) == 0:
            Logger.log('No records found')
        else:
            Logger.log('Retrieved data successfully')
            for k in result:
                constant.config['storeIds'] += k

    @staticmethod
    def getUsers(limitCount = 10):
        Logger.log('Get users Info')
        query = 'SELECT us.id, us.firstname, us.email, us.mobile, ul.external_id FROM user_management.users us LEFT JOIN user_management.loyalty ul ON us.id = ul.user_id AND us.org_id = ul.publisher_id WHERE us.`email` IS NOT NULL AND us.`mobile` IS NOT NULL and us.is_inactive = 0  AND ul.external_id IS NOT NULL AND us.org_id = ' + str(constant.config['orgId']) + ' LIMIT ' + str(limitCount)
        result = dbHelper.queryDB(query, 'user_management')
        constant.config['usersInfo'] = []
        if len(result) == 0:
            Logger.log('No records found')
        else:
            Logger.log('Retrieved data successfully')
            for k in result:
                users = {'userId' : k[0],'name' : k[1],'email' : k[2], 'mobile' : k[3], 'externalId' : k[4]}
                constant.config['usersInfo'].append(users)

    @staticmethod
    def getCouponConfigKeyValues(couponSeriesId, key):
        query = 'SELECT value FROM `luci`.`coupon_config_key_values` WHERE `coupon_series_id` = ' + str(couponSeriesId) + \
                ' and key_id = ' + str(key) + ' and is_valid = 1'
        result = dbHelper.queryDB(query, "luci")
        if len(result) == 0:
            Logger.log('No records found')
        else:
            Logger.log('Coupon Config Key values : ', result[0][0])
            return result[0][0]

    @staticmethod
    def getOwnerInfo(couponSeriesId):
        query = 'SELECT owned_by, owner_id, expiry_date FROM `luci`.`owner_info` WHERE `coupon_series_id` = ' + str(couponSeriesId) + \
                ' and org_id = ' + str(constant.config['orgId'])
        result = dbHelper.queryDB(query, "luci")
        if len(result) == 0:
            Logger.log('No records found')
        else:
            ownerInfo = {'owned_by' : result[0][0], 'owner_id' :result[0][1], 'expiry_date' : result[0][2]}
            Logger.log('Coupon Config Owner Info : ', ownerInfo)
            return ownerInfo

    @staticmethod
    def getCouponSeriesType(couponSeriesId):
        query = 'select series_type, valid_till_date from voucher_series where org_id = ' + str(constant.config['orgId']) + ' and id = ' + str(couponSeriesId)
        result = dbHelper.queryDB(query, 'campaigns')
        if len(result) == 0:
            Logger.log('No records found')
        else:
            Logger.log('Coupon Config Key values : ', result[0])
            tmpDict = {'seriesType' : result[0][0], 'validTillDate' :result[0][1]}
            return tmpDict

    @staticmethod
    def isExternalCouponSeries(couponSeriesId, client_handling_type = 'DISC_CODE_PIN', isExternal = 'true'):
        query = "select count(1) from campaigns.voucher_series vs LEFT JOIN luci.coupon_config_key_values cv ON vs.id = cv.coupon_series_id AND vs.org_id = cv.org_id WHERE cv.is_valid = 1 AND cv.key_id = 11 AND vs.client_handling_type = '{}' AND cv.value = '{}' and vs.id = {}".format(client_handling_type,isExternal,couponSeriesId)
        result = dbHelper.queryDB(query, 'campaigns')[0][0]
        if result:
            Logger.log('Coupon Series Id: {} client_handling_type is External Issual'.format(couponSeriesId))
            return True
        else:
            Logger.log('Coupon Series Id: {} client_handling_type is not External Issual'.format(couponSeriesId))
            return False

    @staticmethod
    def getRedeemCouponCount(couponSeriesId, conditionList = []):
        query = 'SELECT COUNT(1) FROM luci.coupon_redemptions cr LEFT JOIN campaigns.voucher_redemptions vr ON cr.org_id = vr.org_id and cr.coupon_series_id = vr.voucher_series_id AND  cr.id = vr.id where cr.org_id = ' + str(constant.config['orgId']) + ' AND cr.coupon_series_id IN  (' +  str(couponSeriesId)\
                +') AND cr.redeemed_user_id = ' + str(conditionList[0]) + ' AND cr.bill_id = ' + str(conditionList[1]) +  ' AND cr.redeemed_at_store = '  + str(conditionList[2])
        result = dbHelper.queryDB(query, 'luci')
        if len(result) == 0:
            Logger.log('No records found')
            return None
        else:
            Logger.log('Coupon Redeemed Count in voucher_redemptions & coupon_redemptions : ', result[0][0])
            return result[0][0]


    @staticmethod
    def orgDefaultValues():
        query = 'SELECT property_key, property_value FROM default_properties WHERE org_id = ' +  str(constant.config['orgId']) + ' AND is_valid = 1'
        result = dbHelper.queryDB(query, 'luci')
        defaultValue = {}
        if len(result) == 0:
            Logger.log('No records found')
        else:
            for k in result:
                if k[1].lower() == 'false':
                    k[1] = False
                elif k[1].lower() == 'true':
                    k[1] == True
                defaultValue.update({k[0].lower() : k[1]})
        return defaultValue


    @staticmethod
    def getCouponReminder(couponSeriesId, is_active = 1, reminderId = 0):
        query = 'select num_days_before_expiry, hour_of_day, minute_of_hour, created_by,next_scheduled_on,id, cron_task_id from coupon_reminders where org_id = {} and coupon_series_id = {} and is_active = {}'.format(constant.config['orgId'], couponSeriesId, is_active)
        if reminderId != 0:
            query = query + ' and id = {}'.format(reminderId)
        result = dbHelper.queryDB(query, 'luci')
        couponReminder = []
        if len(result) == 0:
            Logger.log('No records found')
        else:
            Logger.log('Retrieved data successfully')
            for k in result:
                reminders = {'num_days_before_expiry' : k[0],'hour_of_day' : k[1],'minute_of_hour' : k[2], 'created_by' : k[3], 'next_scheduled_on' : k[4], 'id' : k[5], 'cronId' : k[6]}
                couponReminder.append(reminders)
        return couponReminder


    @staticmethod
    def getCouponReminderMessages(couponSeriesId, is_valid  = 1):
        query = 'select id, coupon_reminder_id, type, message_json from coupon_reminder_messages where org_id = {} and coupon_series_id = {} and is_valid = {}'.format(constant.config['orgId'], couponSeriesId, is_valid)
        result = dbHelper.queryDB(query, 'luci')
        couponReminderMessages = []
        if len(result) == 0:
            Logger.log('No records found')
        else:
            Logger.log('Retrieved data successfully')
            for k in result:
                messages = {'id' : k[0],'coupon_reminder_id' : k[1],'type' : k[2], 'message_json' : k[3]}
                couponReminderMessages.append(messages)
        return couponReminderMessages

    @staticmethod
    def getSentReminderMessageId(couponSeriesId, reminderMessageId, isCount = False):
        # Table Issue need to Fix for this Query
        # query = 'select message_id from reminder_messages_sent_{}_{} where org_id = {} and coupon_series_id = {} and reminder_message_id = {}'.format(str(constant.config['dateTime']['year']),str(constant.config['dateTime']['month']),str(constant.config['orgId']), str(couponSeriesId), str(reminderMessageId))

        # Tempory Use of query
        query = 'select message_id from reminder_messages_sent where org_id = {} and coupon_series_id = {} and reminder_message_id = {}'.format(str(constant.config['orgId']), str(couponSeriesId), str(reminderMessageId))
        if isCount:
            query = 'select count(1) from reminder_messages_sent where org_id = {} and coupon_series_id = {} and reminder_message_id = {}'.format(str(constant.config['orgId']), str(couponSeriesId), str(reminderMessageId))
        result = dbHelper.queryDB(query, 'luci')
        if result != []:
            return result[0][0]
        else:
            return result

    @staticmethod
    def getReminderExecutionLog(couponSeriesId, couponReminderId):
        #Table Issue need to Fix for this Query
        # query = 'select id, status from coupon_reminder_execution_log_{}_{} where org_id = {} and coupon_series_id = {} and coupon_reminder_id = {}'.format(,str(constant.config['dateTime']['year']),str(constant.config['dateTime']['month']),str(constant.config['orgId']), str(couponSeriesId), str(couponReminderId))

        #Tempory Use of query
        query = 'select status from coupon_reminder_execution_log where org_id = {} and coupon_series_id = {} and coupon_reminder_id = {}'.format(str(constant.config['orgId']), str(couponSeriesId), str(couponReminderId))
        result = dbHelper.queryDB(query, 'luci')
        if result != []:
            return result[0][0]
        else:
            return result

    @staticmethod
    def getCouponUploadDetails(couponSeriesId, status, totalCount):
        query = 'SELECT error_count, error_file_url FROM luci.coupon_upload WHERE org_id = {} AND coupon_series_id = {} AND status = {} AND total_upload_count = {} AND is_valid = 1'.format(constant.config['orgId'], couponSeriesId, status, totalCount)
        result = dbHelper.queryDB(query, 'luci')
        couponUpload = []
        if len(result) == 0:
            Logger.log('No records found')
        else:
            Logger.log('Retrieved data successfully')
            for k in result:
                messages = {'error_count': k[0], 'error_file_url': k[1]}
                couponUpload.append(messages)
        return couponUpload

    @staticmethod
    def getCronStatus(cronId):
        query = 'select status from scheduler.cron_tasks where org_id = {} and id = {}'.format(constant.config['orgId'], str(cronId))
        result = dbHelper.queryDB(query, 'scheduler')
        if len(result) == 0:
            Logger.log('No records found')
        else:
            Logger.log('CronId : {} and Cron status : {}'.format(cronId, result[0][0]))
            return result[0][0]

    @staticmethod
    def getTempTableData(tempTableName):
        couponRevokeHistory = []
        query = 'select is_valid, is_success, error_code, error_message from Temp.{} where is_success = 0'.format(tempTableName)
        result = dbHelper.queryDB(query, 'Temp')
        if len(result) == 0:
            Logger.log('No records found')
        else:
            for k in result:
                couponRevokeHistory.append({'isValid' : k[0], 'isSuccess' : k[1], 'errorCode' : k[2], 'errorMsg' : k[3]})
        return couponRevokeHistory