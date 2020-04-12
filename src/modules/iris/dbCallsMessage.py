from src.Constant.constant import constant
from src.utilities.dbhelper import dbHelper
from src.utilities.logger import Logger
import json, time

class dbCallsMessage():
    
    @staticmethod
    def getMessageQueueFromMessageId(message_id, payload={}):
        Logger.log('Getting Message Queue Informtion using message ID:', message_id)
        query = 'select id,type,org_id,campaign_id,group_id,status,scheduled_type,params,Approved,default_arguments,guid from message_queue where id = ' + str(message_id) 
        result = dbHelper.queryDB(query, 'msging')[0]
        param = json.loads(result[7])
        if result[1].lower() == 'wechat' and 'message' in payload:
            param['message'] = json.loads(param['message'])
            if param['message']['isUrlInternal']:
                param['message']['url'] = payload['message']['url']
            param['message'].pop('urlInternal')
        return {'id':result[0], 'type':result[1], 'org_id':result[2], 'campaign_id':result[3], 'group_id':result[4], 'status':result[5], 'scheduled_type':result[6], 'param': param, 'Approved':result[8], 'default_arguments':result[9], 'guid':result[10]}
        
    @staticmethod
    def getMessageQueueId(campaignId, groupVersionId):
        Logger.log('Getting Message Queue Id for OrgId :{} , campaignId :{} and groupVersion :{}'.format(constant.config['orgId'], campaignId, groupVersionId))
        result = []
        for eachTry in range(5):
            query = "select id from message_queue where org_id = {} and campaign_id = {} and group_id = {} order by id desc limit 1".format(constant.config['orgId'], campaignId, groupVersionId)
            result = dbHelper.queryDB(query, 'msging')
            if len(result) > 0:
                break
            else:
                time.sleep(2)
                Logger.log('Retry :{} as result was empty '.format(eachTry))
        return result[0]
    
    @staticmethod
    def getMessageQueueIdForPreviewTest(campaignId):
        Logger.log('Getting Message Queue Id for OrgId :{} , campaignId :{} '.format(constant.config['orgId'], campaignId))
        result = []
        for eachTry in range(5):
            query = "select id from message_queue where org_id = {} and campaign_id = {} order by id desc limit 1".format(constant.config['orgId'], campaignId)
            result = dbHelper.queryDB(query, 'msging')
            if len(result) > 0:
                break
            else:
                time.sleep(2)
                Logger.log('Retry :{} as result was empty '.format(eachTry))
        return result[0]

    @staticmethod
    def getReminderDataFromMessageId(message_id, module):
        Logger.log('Getting Reminder Informtion using message ID:', message_id)
        query = 'select reminder_type,id,group_id,state,frequency from reminder where refrence_id = ' + str(message_id) + ' and org_id = ' + str(constant.config['orgId']);
        result = dbHelper.queryDB(query, 'user_management')
        constructedResult = {}
        for eachIndex in result:
            constructedResult[eachIndex[0]] = {'id':eachIndex[1], 'group_id':eachIndex[2], 'state':eachIndex[3], 'frequency':eachIndex[4]}
        return constructedResult
            
    @staticmethod
    def getCronTableFromReminderId(reminder_id, module):
        Logger.log('Getting Cron Informtion using reminder ID:', reminder_id)
        query = 'select id,cron_pattern from cron_tasks where reference_id = ' + str(reminder_id) + ' and org_id = ' + str(constant.config['orgId']);
        result = dbHelper.queryDB(query, 'scheduler')[0]
        return {'id':result[0], 'cron_pattern':result[1]}
        
    @staticmethod
    def getGenericIncentiveId(message_queue_id):
        query = 'select incentive_type_id,campaign_id from incentive_mapping where message_queue_id = ' + str(message_queue_id)
        result = dbHelper.queryDB(query, 'campaigns')[0]
        return {'incentive_type_id' : result[0], 'campaign_id':result[1]}
        
    @staticmethod
    def getIncentiveMetaDetails():
        Logger.log('Getting Incentive Meta Infomration')
        query = 'select incentive_type,id from incentive_meta_details'
        result = dbHelper.queryDB(query, 'campaigns')
        constructedResult = {}
        for eachIncentive in result:
            constructedResult[eachIncentive[0]] = eachIncentive[1]
        return constructedResult
    
    @staticmethod
    def getUsersInformation(numberOfUsers, module='iris'):
        query = "select u.id,u.firstname,u.lastname,u.mobile,u.email,l.external_id from users u,loyalty l where u.id=l.user_id and u.email like 'iris_automation%' and u.org_id = " + str(constant.config['orgId']) + " and l.publisher_id = " + str(constant.config['orgId']) + " and l.type = 'loyalty' order by u.id desc limit " + str(numberOfUsers * 2)
        result = list(dbHelper.queryDB(query, 'user_management'))
        listOfNDNCIndex = 0
        for idx in range(len(result)):
            query = 'select status from users_ndnc_status where user_id = {}'.format(result[idx][0])
            ndnc_result = dbHelper.queryDB(query, 'user_management')
            if len(ndnc_result) > 0:
                if dbHelper.queryDB(query, 'user_management')[0][0] == 'NDNC':result[idx] = None
        formedResult = filter(None, result)[:numberOfUsers]
        return formedResult
    
    @staticmethod
    def getAllUserInformationFromOrg(loyaltyType='loyalty'):
        query = "select u.firstname,u.lastname,u.mobile from users u,loyalty l where u.id=l.user_id and u.email like 'iris%' and u.org_id = " + str(constant.config['orgId']) + " and l.publisher_id = " + str(constant.config['orgId']) + " and l.type = '{}' order by u.id desc ".format(loyaltyType)
        result = dbHelper.queryDB(query, 'user_management')
        return result
    
    @staticmethod
    def getUsersInformationWithUserId(userId):
        query = "select firstname,lastname,mobile,email from users where id= {} and org_id = {} ".format(userId, str(constant.config['orgId']))
        result = dbHelper.queryDB(query, 'user_management')[0]
        return result
    
    @staticmethod
    def getNDNCUserMobileNumber(numberOfUsers=1):
        query = "select mobile from users_ndnc_status where org_id = {} and status = 'NDNC' limit {}".format(str(constant.config['orgId']), numberOfUsers)
        result = dbHelper.queryDB(query, 'user_management')
        listOfNDNCMobile = []
        for eachNDNCUser in result:
            listOfNDNCMobile.append(eachNDNCUser[0])
        return listOfNDNCMobile
    
    @staticmethod
    def getUserIdsForAlistOfMobileNumbers(mobileNumbers):
        query = "select id,mobile,secretA from users where org_id = {} and mobile in ({}) order by id asc".format(constant.config['orgId'], mobileNumbers)
        result = dbHelper.queryDB(query, 'user_management')
        listOfTestUsersId = []
        listOfControlUserId = []
        for each in result:
            if int(each[2]) <= 90:
                listOfTestUsersId.append({'userId':each[0], 'mobile':each[1]})
            else:
                listOfControlUserId.append({'userId':each[0], 'mobile':each[1]})
        return listOfTestUsersId, listOfControlUserId
            
    @staticmethod
    def getInvalidUserMobileNumber(numberOfUsers=1):
        query = "select mobile from users_ndnc_status where org_id = {} and status = 'INVALID' limit {}".format(str(constant.config['orgId']), numberOfUsers)
        result = dbHelper.queryDB(query, 'user_management')
        listOfInvalidMobile = []
        for eachInvalidUser in result:
            listOfInvalidMobile.append(eachInvalidUser[0])
        return listOfInvalidMobile
    
    @staticmethod    
    def getProgrameId():
        query = 'select id from program where org_id = ' + str(constant.config['orgId']) + ' order by id desc limit 1'
        result = dbHelper.queryDB(query, 'warehouse')[0]
        return str(result[0])
    
    @staticmethod
    def getAllocationIdForPrograme(programeId):
        query = 'select id from strategies where org_id = ' + str(constant.config['orgId']) + ' and program_id = ' + str(programeId) + ' and strategy_type_id = 1 and owner="CAMPAIGN" and property_values like "%FIXED_SLAB%" order by id desc limit 1'
        result = dbHelper.queryDB(query, 'warehouse')[0]
        return str(result[0])
    
    @staticmethod
    def getExpiryIdForPrograme(programeId):
        query = 'select id from strategies where org_id = ' + str(constant.config['orgId']) + ' and program_id = ' + str(programeId) + ' and strategy_type_id = 3 and owner="CAMPAIGN" and property_values like "%expiry_type%" order by id desc limit 1'
        result = dbHelper.queryDB(query, 'warehouse')[0]
        return str(result[0])
    
    
