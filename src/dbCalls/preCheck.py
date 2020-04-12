import time

from src.Constant.constant import constant
from  src.utilities.dbhelper import dbHelper
from src.utilities.logger import Logger


class precheck_calls():
    def __init__(self, event=None):
        self.event = event

    def getJobDetailFromPreExecutionJobStatus(self, camaignId, messageId, jobType):
        query = 'select campaign_id,job_status,error_description,params from pre_execution_job_status where org_id ={} and campaign_id = {} and message_id = "{}" and job_type = "{}"  and event_type = "{}" order by id desc limit 1'.format(
            constant.config['orgId'], camaignId, messageId, jobType,self.event)
        for _ in range(25):
            result = dbHelper.queryDB(query, 'veneno')
            if len(result) == 0 or result[0][1] in ('OPEN', 'PROCESSING'):
                time.sleep(10)
            else:
                break

        if len(result) == 0:
            Logger.log('Retiral 15 Times with each 10 secs Gap , but No Data Found')
            raise Exception('NoEntryInPreExecutionJobStatusForMessageId:{},JobType:{}'.format(messageId, jobType))
        return {
            'campaign_id': result[0][0],
            'job_status': result[0][1],
            'error_description': result[0][2],
            'params': result[0][3]
        }

    def getMsgDetailFromPreExecutionMessageStatus(self, camaignId, messageId, jobType):
        query = 'select status from pre_execution_msg_status where org_id = {} and campaign_id = {} and message_id = "{}" and event_type="{}"'.format(
            constant.config['orgId'], camaignId, messageId, jobType)
        for _ in range(15):
            result = dbHelper.queryDB(query, 'veneno')
            if len(result) == 0 or result[0][1] in ('OPEN', 'PROCESSING', 'SUBMITTED'):
                time.sleep(10)
            else:
                break

        if len(result) == 0:
            Logger.log('Retiral 15 Times with each 10 secs Gap , but No Data Found')
            raise Exception('NoEntryInPreExecutionMsgStatusForMessageId:{},EventType:{}'.format(messageId, jobType))
        return {
            'status': result[0][0]
        }

    def getVariantExecutionStatus(self, camaignId, messageId):
        query = 'select message_variant_id,status from variant_execution_status where org_id = {} and campaign_id = {} and message_id = "{}"'.format(
            constant.config['orgId'], camaignId, messageId)
        for _ in range(15):
            result = dbHelper.queryDB(query, 'veneno')
            if len(result) == 0:
                time.sleep(10)
            else:
                break
        if len(result) == 0:
            Logger.log('Retiral 15 Times with each 10 secs Gap , but No Data Found')
            raise Exception('NoEntryInPreExecutionVariantStatusForMessageId:{}'.format(messageId))
        actualResult = dict()
        for each in result:
            actualResult.update({each[0]: each[1]})
        return actualResult
