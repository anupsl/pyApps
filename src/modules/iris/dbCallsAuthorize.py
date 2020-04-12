import json
import time

from src.Constant.constant import constant
from src.utilities.assertion import Assertion
from src.utilities.dbhelper import dbHelper
from src.utilities.logger import Logger
from src.utilities.mongoHelper import MongoHelper


class dbCallsAuthorize():
    @staticmethod
    def getCommunicationDetails(campaignId, groupVersionId, guid, nonImmediate=False, sleepTime=10, retry=30):
        query = 'select id,recipient_list_id,recipient_list_name,communication_type,expected_delivery_count,overall_recipient_count,subject,state,default_arguments,bucket_id,message_queue_id from communication_details where org_id =' + str(
            constant.config['orgId']) + ' and campaign_id =' + str(campaignId) + ' and recipient_list_id=' + str(
            groupVersionId) + ' and guid =\'' + str(guid) + '\''
        result = None
        if nonImmediate:
            retry = 25
        for numberOfTries in range(retry):
            try:
                result = dbHelper.queryDB(query, 'veneno')[0]
                if result != []:
                    if str(result[7]) == 'CLOSED':
                        break
            except Exception, exp:
                Logger.log('Exception :{} , Try :{} and no Result is:{}'.format(exp, numberOfTries, result))
            Logger.log('For Getting CD Details try:{} with SleepTime:{}'.format(numberOfTries, sleepTime))
            time.sleep(sleepTime)
        if result == None: Assertion.constructAssertion(False,
                                                        'Even After Trying 25 times and waiting 250 second Entry is not present in Communication Detail Table for guid:{}'.format(
                                                            guid))
        return {'id': result[0], 'recipient_list_id': result[1], 'recipient_list_name': result[2],
                'communication_type': result[3], 'expected_delivery_count': result[4],
                'overall_recipient_count': result[5], 'message_body': result[6], 'state': result[7],
                'default_arguments': result[8], 'bucket_id': result[9], 'message_queue_id': result[10]}

    @staticmethod
    def getCommunicationDetailsWithId(cdId):
        query = 'select id,recipient_list_id,recipient_list_name,communication_type,expected_delivery_count,overall_recipient_count,subject,state,default_arguments,bucket_id,message_queue_id,message_body from communication_details where org_id =' + str(
            constant.config['orgId']) + ' and id =' + str(cdId)
        for numberOfTries in range(5):
            result = dbHelper.queryDB(query, 'veneno')[0]
            if str(result[7]) == 'CLOSED':
                break
            time.sleep(10)
        return {'id': result[0], 'recipient_list_id': result[1], 'recipient_list_name': result[2],
                'communication_type': result[3], 'expected_delivery_count': result[4],
                'overall_recipient_count': result[5], 'message_body': result[6], 'state': result[7],
                'default_arguments': result[8], 'bucket_id': result[9], 'message_queue_id': result[10],
                'body': result[11]}

    @staticmethod
    def getHealthDashBoardNotifications(messageId):
        query = 'select message,cause from notifications where org_id = ' + str(
            constant.config['orgId']) + ' and ref_id  = ' + str(messageId) + ' order by added_on desc limit 1'
        Logger.log('For Getting Health Notification for org : {} , MessageQueueId : {}'.format(constant.config['orgId'],
                                                                                               messageId))
        result = dbHelper.queryDB(query, 'health_dashboard')
        resultList = {}
        if result != []:
            for resultValue in result:
                message = json.loads(resultValue[0])['message']
                details = json.loads(resultValue[0])['details']
                cause = resultValue[1]
                if cause in resultList:
                    resultList[cause].append(message)
                else:
                    resultList[cause] = [message]
                resultList.update({'details': json.loads(resultValue[0])['details']})
            return resultList
        else:
            Logger.log('No Result found{}'.format(result))

    @staticmethod
    def getBulkSMS_Campaigns(campaignId, messageId):
        query = 'select * from bulksms_campaign where org_id = ' + str(
            constant.config['orgId']) + ' and campaign_id = ' + str(campaignId) + ' and queue_id  = ' + str(messageId)
        Logger.log('Getting Bulk SMS campaign Details for org : {} , MessageQueueId : {} and campaignId :{}'.format(
            constant.config['orgId'], messageId, campaignId))
        result = dbHelper.queryDB(query, 'msging')
        if result != []:
            return result
        else:
            Logger.log('No Result found{}'.format(result))
            return result

    @staticmethod
    def getSummaryReportNsadmin(msgId):
        query = 'select id,delivery_status_id,count from summary_report_nsadmin where msg_id =' + str(msgId)
        result = dbHelper.queryDB(query, 'veneno')
        summaryReportResult = {}
        for eachRowBasedOnDeliveryStatusId in result:
            summaryReportResult[eachRowBasedOnDeliveryStatusId[1]] = {'id': eachRowBasedOnDeliveryStatusId[0],
                                                                      'count': eachRowBasedOnDeliveryStatusId[2]}
        return summaryReportResult

    @staticmethod
    def getSummaryReportVeneno(msgId):
        query = 'select id,report_type,sub_type,count,message_version from summary_report_veneno where msg_id =' + str(
            msgId)
        result = dbHelper.queryDB(query, 'veneno')
        venenoReportResult = {}
        for eachRowBasedOnDeliveryStatusId in result:
            venenoReportResult[eachRowBasedOnDeliveryStatusId[2]] = {'id': eachRowBasedOnDeliveryStatusId[0],
                                                                     'report_type': eachRowBasedOnDeliveryStatusId[1],
                                                                     'count': eachRowBasedOnDeliveryStatusId[3],
                                                                     'message_version': eachRowBasedOnDeliveryStatusId[
                                                                         4]}
        return venenoReportResult

    @staticmethod
    def getVenenoBatchDetail(msgId):
        query = 'select id,batch_type,status,message_version,batch_id from veneno_batch_details where message_id = ' + str(
            msgId)
        result = dbHelper.queryDB(query, 'veneno')
        venenoBatchResult = {}
        for eachBatchType in result:
            venenoBatchResult[eachBatchType[1]] = {'id': eachBatchType[0], 'status': eachBatchType[2],
                                                   'message_version': eachBatchType[3], 'batch_id': eachBatchType[4]}
        return venenoBatchResult

    @staticmethod
    def getVenenoMonitorStatus(msgId):
        query = 'select message_version,processed_status from veneno_monitor_status where message_id = ' + str(msgId)
        for _ in range(15):
            result = dbHelper.queryDB(query, 'veneno')
            if len(result) != 0:
                break
            time.sleep(5)
        venenoMonitorStatus = {}
        for eachStatus in result:
            venenoMonitorStatus[eachStatus[0]] = {'status': eachStatus[1]}
        return venenoMonitorStatus

    @staticmethod
    def getVenenoReplyBatchDetail(msgId):
        query = 'select message_version,batch_id,s3_key from replay_skipped_batches where org_id = ' + str(
            constant.config['orgId']) + ' and message_id = ' + str(msgId)
        result = dbHelper.queryDB(query, 'veneno')
        venenoReplyBatchResult = []
        for eachBatchType in result:
            venenoReplyBatchResult.append(
                {'message_version': eachBatchType[0], 'batch_id': eachBatchType[1], 's3_key': eachBatchType[2]})
        return venenoReplyBatchResult

    @staticmethod
    def getVenenoReplyStats(msgId):
        query = 'select message_version,skipped_error_csv,skipped_count from campaign_replay_stats where message_id = ' + str(
            msgId)
        result = dbHelper.queryDB(query, 'veneno')
        venenoReplyStats = {}
        for eachStats in result:
            venenoReplyStats[eachStats[0]] = {'skipped_error_csv': eachStats[1], 'skipped_count': eachStats[2]}
        return venenoReplyStats

    @staticmethod
    def getServiceDetails(msgId, numberOfTestUsers):
        query = 'select id,batch_type,processed_count,batches_processed,message_version from service_details where communication_message_id = ' + str(
            msgId)
        serviceDetailResult = {}
        statusServiceDetail = True
        for numberOfTries in range(25):
            result = dbHelper.queryDB(query, 'veneno')
            if len(result) >= 3:
                for eachBatchType in result:
                    if int(eachBatchType[2]) != numberOfTestUsers:
                        statusServiceDetail = False
                    else:
                        statusServiceDetail = True
                    serviceDetailResult[eachBatchType[1]] = {'id': eachBatchType[0],
                                                             'processed_count': eachBatchType[2],
                                                             'batches_processed': eachBatchType[3],
                                                             'message_version': eachBatchType[4]}
                if statusServiceDetail: break
            time.sleep(25)

        return serviceDetailResult

    @staticmethod
    def getInboxDetail(bucketId, msgId, waitForInboxMsg=False):
        query = 'select id,recipient_id,nsadmin_id,resolved_tags from inboxes_{} where message_id={}'.format(bucketId,
                                                                                                             msgId)
        result = dbHelper.queryDB(query, 'veneno_data_details')
        i = 0
        while waitForInboxMsg and len(result) == 0 and i < 10:
            i = i + 1
            time.sleep(3)
            result = dbHelper.queryDB(query, 'veneno_data_details')
        inboxDetailAsUserId = {}
        for eachUserInboxDetail in result:
            inboxDetailAsUserId[eachUserInboxDetail[1]] = {'id': eachUserInboxDetail[0],
                                                           'nsadmin_id': eachUserInboxDetail[2],
                                                           'resolved_tags': eachUserInboxDetail[3]}
        return inboxDetailAsUserId

    @staticmethod
    def getSkippedDetail(bucketId, msgId):
        query = 'select id,recipient_id,error_type_id,error_description,message_version from skipped_recipients_{} where message_id={}'.format(
            bucketId, msgId)
        result = dbHelper.queryDB(query, 'veneno_data_details')
        skippedDetailAsUserId = {}
        for eachSkippedUserDetail in result:
            skippedDetailAsUserId[eachSkippedUserDetail[1]] = {'id': eachSkippedUserDetail[0],
                                                               'error_type_id': eachSkippedUserDetail[2],
                                                               'error_description': eachSkippedUserDetail[3],
                                                               'message_version': eachSkippedUserDetail[4]}
        return skippedDetailAsUserId

    @staticmethod
    def getUserForMobilePush(commChannelType):
        port = constant.config['INTOUCH_DB_MONGO_MASTER']
        query = {'orgId': constant.config['orgId'], 'source': 'WEB_ENGAGE', 'commChannels.type': commChannelType}
        return MongoHelper.findDocuments('multi_profile', 'profileV2', port, query, limit=2)

    @staticmethod
    def configRateLimit(enable, channel):
        if enable:
            query = "update rate_limiting_strategy set is_active = 1 where org_id = {} and  channel = '{}'"
        else:
            Logger.log('Setting is_active of rate_limit_strategy as 0')
            query = "update rate_limiting_strategy set is_active = 0 where org_id = {} and channel = '{}'"
        dbHelper.queryDB(query.format(constant.config['orgId'], channel.upper()), 'veneno')

    @staticmethod
    def setupStrategy(daily=None, weekly=None, monthly=None, channel='SMS'):
        query = "update rate_limiting_strategy set `limit` = {} where org_id = {} and window = '{}' and channel = '{}'"
        if daily is not None:
            dbHelper.queryDB(query.format(daily, constant.config['orgId'], 'DAILY', channel), 'veneno')
        if weekly is not None:
            dbHelper.queryDB(query.format(weekly, constant.config['orgId'], 'WEEKLY', channel), 'veneno')
        if monthly is not None:
            dbHelper.queryDB(query.format(monthly, constant.config['orgId'], 'MONTHLY', channel), 'veneno')

    @staticmethod
    def getRateLimitStats(userIds, channel):
        query = "select user_id,strategy_id,no_of_attempts from rate_limiting_stats where org_id = {} and user_id in {}".format(
            constant.config['orgId'], userIds)
        result = dbHelper.queryDB(query, 'veneno')
        mapOfStrategy = dbCallsAuthorize.getMappingOfStrategyId(channel)
        dictOfuserStats = dict()
        for eachUserPerStrategyStats in result:
            if eachUserPerStrategyStats[0] not in dictOfuserStats:
                dictOfuserStats[eachUserPerStrategyStats[0]] = {
                    mapOfStrategy[int(eachUserPerStrategyStats[1])]: eachUserPerStrategyStats[2]}
            else:
                dictOfuserStats[eachUserPerStrategyStats[0]].update(
                    {mapOfStrategy[int(eachUserPerStrategyStats[1])]: eachUserPerStrategyStats[2]})
        return dictOfuserStats

    @staticmethod
    def getMappingOfStrategyId(channel):
        query = "select id,window from rate_limiting_strategy where org_id = {} and channel='{}'".format(
            constant.config['orgId'], channel.upper())
        result = dbHelper.queryDB(query, 'veneno')
        dictOfMap = dict()
        for each in result:
            dictOfMap[int(each[0])] = each[1]
        return dictOfMap

    @staticmethod
    def getStrategyId(window, channel):
        query = "select id from rate_limiting_strategy where org_id = {} and window = '{}' and channel = '{}'".format(
            constant.config['orgId'], window.upper(), channel.upper())
        result = dbHelper.queryDB(query, 'veneno')[0]
        return result[0]

    @staticmethod
    def updateWindowValueToByPassStrategy(userIds, strategyId):
        query = "update rate_limiting_stats set window_value = window_value-1 where user_id in {} and strategy_id = {}".format(
            userIds, strategyId)
        result = dbHelper.queryDB(query, 'veneno')

    @staticmethod
    def updateStartegyForRateLimit():
        if constant.config['cluster'] == 'nightly':
            Logger.log('Setting is_active of rate_limit_strategy as 0')
            query = "update rate_limiting_strategy set is_active=0"
            result = dbHelper.queryDB(query, 'veneno')
        else:
            Logger.log('Update Strategy only Works for Nightly Cluster')

    @staticmethod
    def getUserFromCGUH(campaign_id, message_id):
        query = "select user_id from control_group_users_history where org_id = {} and campaign_id = {} and message_id = {}".format(
            constant.config['orgId'], campaign_id, message_id)
        result = dbHelper.queryDB(query, 'veneno_data_details')
        listOfusers = []
        for each in result:
            listOfusers.append(each[0])
        return listOfusers

    @staticmethod
    def getListType(gvdId):
        query = "select gd.type from group_version_details gvd,group_details gd where gvd.id = {} and gvd.group_id = gd.id".format(gvdId)
        return dbHelper.queryDB(query, 'campaign_meta_details')[0][0]