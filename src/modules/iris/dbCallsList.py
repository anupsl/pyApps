import time

from src.Constant.constant import constant
from src.utilities.dbhelper import dbHelper
from src.utilities.logger import Logger
import json

class dbCallsList():
    @staticmethod
    def getGroupDetailsWithListId(list_id):
        Logger.log('Getting Group Details with list Id:', list_id)
        query = 'select group_label,type,group_tags,custom_tag_count,id,uuid,is_visible,group_label,description from group_details where id = ' + str(
            list_id)
        result = dbHelper.queryDB(query, 'campaign_meta_details')[0]
        return {'group_label': result[0], 'type': result[1], 'group_tags': result[2], 'custom_tag_count': result[3],
                'id': result[4], 'uuId': result[5], 'is_visible': result[6], 'label': result[7],
                'orgId': constant.config['orgId'], 'description':result[8]}

    @staticmethod
    def getGroupDetailsWithListName(listName, uuid):
        Logger.log('Getting Group Details with list Name:', listName)
        query = "select id,type,group_tags,custom_tag_count from group_details where group_label = '{}' and uuid = '{}'".format(
            listName, uuid)
        result = dbHelper.queryDB(query, 'campaign_meta_details')[0]
        return {'id': result[0], 'type': result[1], 'group_tags': result[2], 'custom_tag_count': result[3]}

    @staticmethod
    def getGroupDetailsOfInvisibleList():
        Logger.log("Getting Group Details of invisible list")
        query = "select id from group_details where org_id ={} and is_visible = 0 order by id desc limit 1".format(
            constant.config['orgId'])
        result = dbHelper.queryDB(query, 'campaign_meta_details')[0]
        return result

    @staticmethod
    def getGroupVersionDetailsWithGroupId(group_id,expectedStatus='ACTIVE'):
        for each in range(10):
            Logger.log('Getting Group Version with list Id :', group_id)
            query = 'select id,params,target_type,customer_count,bucket_id,status from group_version_details where group_id = ' + str(
                group_id)
            result = dbHelper.queryDB(query, 'campaign_meta_details')
            constructResult = {}
            for eachRow in result:
                constructResult[eachRow[2]] = {'id': eachRow[0], 'bucket_id': eachRow[4], 'params': eachRow[1],
                                               'customer_count': eachRow[3], 'status': eachRow[5]}
            Logger.log('Constructed Result of Group Version Detail :', constructResult)
            if constructResult['TEST']['status'] == expectedStatus: break
            time.sleep(10)
        return constructResult

    @staticmethod
    def getGroupVersionDetailWithGroupVersionId(group_version_id):
        Logger.log('Getting Group Version Detail for group version id :{}'.format(group_version_id))
        query = 'select id,params,target_type,customer_count,bucket_id,campaign_id from group_version_details where id = {}'.format(
            group_version_id)
        result = dbHelper.queryDB(query, 'campaign_meta_details')[0]
        return {'id': result[0], 'bucket_id': result[4], 'params': result[1], 'customer_count': result[3],
                'campaign_id': result[4]}

    @staticmethod
    def getTestControlBasedOnSecreta(userType='mobile', data='', module='iris'):
        Logger.log('Getting Test Control Based on Secreta with Data :', data)
        query = 'select ' + str(userType).lower() + ',secreta from users where ' + str(
            userType) + ' in (' + data + ') and org_id = ' + str(constant.config['orgId'])
        result = dbHelper.queryDB(query, 'user_management')
        buildResult = {'test': [], 'control': []}
        for eachResult in result:
            if int(eachResult[1]) <= 90:
                buildResult['test'].append(eachResult[0])
            else:
                buildResult['control'].append(eachResult[0])
        Logger.log('Constructed Result for Test Control From Secreta :', buildResult)
        return buildResult

    @staticmethod
    def getInvalidUsersFromDarknight(listOfusers):
        if len(listOfusers) == 0: return 0
        query = "select count(*) from email_status where email in ('{}') and status='INVALID'".format(
            "','".join(listOfusers))
        return dbHelper.queryDB(query, 'darknight')[0][0]

    @staticmethod
    def getSecretA(userType, data):
        if userType.lower() == 'externalid':
            query = 'select u.secreta from users u,loyalty l where u.id=l.user_id and u.org_id = {} and l.publisher_id={} and l.external_id in ({})'.format(
                constant.config['orgId'], constant.config['orgId'], data)
            result = dbHelper.queryDB(query, 'user_management')
            return result
        elif userType.lower() == 'userid':
            query = 'select u.secreta from users u,loyalty l where u.id=l.user_id and u.org_id = {} and l.publisher_id={} and u.id in ({})'.format(
                constant.config['orgId'], constant.config['orgId'], data)
            result = dbHelper.queryDB(query, 'user_management')
            return result
        elif userType.lower() == 'mobile':
            query = 'select u.secreta from users u,loyalty l where u.id=l.user_id and u.org_id = {} and l.publisher_id={} and u.mobile in ({})'.format(
                constant.config['orgId'], constant.config['orgId'], data)
            result = dbHelper.queryDB(query, 'user_management')
            return result
        elif userType.lower() == 'email':
            query = 'select u.secreta from users u,loyalty l where u.id=l.user_id and u.org_id = {} and l.publisher_id={} and u.email in ({})'.format(
                constant.config['orgId'], constant.config['orgId'], data)
            result = dbHelper.queryDB(query, 'user_management')
            return result

    @staticmethod
    def getEmailListFromUserId(listOfUsers):
        if len(listOfUsers) == 0: return []
        query = "select email from users where org_id = {} and id in ({})".format(constant.config['orgId'],
                                                                                  ','.join(map(str, listOfUsers)))
        result = dbHelper.queryDB(query, 'user_management')
        constructResult = list()
        if len(result) != 0:
            for each in result:
                constructResult.append(each[0])
            return constructResult
        else:
            return []

    @staticmethod
    def getHashLookUp(module='iris'):
        Logger.log('Getting Hash look Up')
        query = 'select id,lookup_string from campaign_hash_lookup where org_id =' + str(constant.config['orgId'])
        result = dbHelper.queryDB(query, 'campaign_meta_details')
        buildResult = {}
        for eachResult in result:
            buildResult[eachResult[1]] = eachResult[0]

        Logger.log('Constructed Hash Lookup :', buildResult)
        return buildResult

    @staticmethod
    def getCampaignGroupRecipient(bucketId, groupVersionId, hashId):
        Logger.log(
            'Getting Campaign Group Recipient with bucketId :{} , groupVersionId :{}  and hashId :{}'.format(bucketId,
                                                                                                             groupVersionId,
                                                                                                             hashId))
        query = 'select hash_id,reachability_type_id,count(*) as userCount from campaign_group_recipients__' + str(
            bucketId) + ' where group_version_id = ' + str(groupVersionId) + ' and org_id = ' + str(constant.config['orgId']) + ' group by hash_id'
        buildResult = {}

        for numberOfTries in range(10):
            time.sleep(10)
            result = dbHelper.queryDB(query, 'campaign_data_details')
            if len(result) > 0:
                for eachResult in result:
                    buildResult[eachResult[0]] = {'reachability_type_id': eachResult[1], 'userCount': eachResult[2]}
                if buildResult[hashId]['reachability_type_id'] != -1:
                    break

        Logger.log('Result Getting Returned for CGR : {}', buildResult)
        return buildResult

    @staticmethod
    def getContorlUsersFromCGR(bucketId, groupVersionId, hashId, listOfUsers=[]):
        Logger.log('ListOfUsers :{}'.format(listOfUsers))
        query = "select user_id,reachability_type_id from campaign_group_recipients__{} where org_id = {} and group_version_id = {} and test_control=0 and hash_id = {}".format(
            bucketId, constant.config['orgId'], groupVersionId, hashId)
        result = dbHelper.queryDB(query, 'campaign_data_details')
        dictOfUserBasedOnReachablity = dict()
        for each in result:
            if len(listOfUsers) == 0:
                if each[1] not in dictOfUserBasedOnReachablity:
                    dictOfUserBasedOnReachablity[each[1]] = [each[0]]
                else:
                    dictOfUserBasedOnReachablity[each[1]].append(each[0])
            else:
                if each[0] in listOfUsers:
                    if each[1] not in dictOfUserBasedOnReachablity:
                        dictOfUserBasedOnReachablity[each[1]] = [each[0]]
                    else:
                        dictOfUserBasedOnReachablity[each[1]].append(each[0])
        return dictOfUserBasedOnReachablity

    @staticmethod
    def getCampaignGroupRecipientTestControlCount(bucketId, groupVersionId, hashId):
        Logger.log(
            'Getting Campaign Group Recipient with bucketId :{} , groupVersionId :{}  and hashId :{}'.format(bucketId,
                                                                                                             groupVersionId,
                                                                                                             hashId))
        query = 'select test_control,count(*) as userCount from campaign_group_recipients__' + str(
            bucketId) + ' where group_version_id = ' + str(
            groupVersionId) + ' and org_id = ' + str(constant.config['orgId']) + ' and  hash_id = {} group by test_control'.format(hashId)
        buildResult = {}

        for numberOfTries in range(10):
            time.sleep(10)
            result = dbHelper.queryDB(query, 'campaign_data_details')
            if len(result) > 0:
                for eachResult in result:
                    buildResult[eachResult[0]] = eachResult[1]
                break
        return buildResult

    @staticmethod
    def getHashIdAsPerChannel(channel,gvdId=None):
        if channel.lower() == 'sms': channel = 'mobile'
        channel = channel.upper()
        if channel.lower() == 'wechat':
            if gvdId is None: raise Exception('GVD Required For HashLookup Of Wechat')
            allParams = json.loads(dbCallsList.getGroupVersionDetailWithGroupVersionId(gvdId)['params'])
            for eachParam in allParams:
                if 'wechat' in eachParam and allParams[eachParam]>0:
                    channel = 'WECHAT__'+eachParam.split('wechat_')[1]+'__WECHAT'
        query = "select id from campaign_hash_lookup where org_id = {} and lookup_string  like '%INSTORE%{}%'".format(
            constant.config['orgId'], channel)
        result = dbHelper.queryDB(query, 'campaign_meta_details')
        if len(result) == 0:
            Logger.log('No Hash Id Found ')
            return None
        return result[0][0]

    @staticmethod
    def getUsersFromCampaignGroupRecipient(bucketId, groupVersionId, channel='sms', testControl=None,
                                           reachabilityCalculated=False):
        hashId = dbCallsList.getHashIdAsPerChannel(channel,groupVersionId)
        query = 'select distinct(user_id) from campaign_data_details.campaign_group_recipients__{} where group_version_id={} and org_id ={}'.format(
            bucketId, groupVersionId, constant.config['orgId'])
        if hashId is not None:
            query = query + ' and hash_id = {}'.format(hashId)
        else:
            Logger.log('HashId Not Found , so querying without using HashID')  # TODO: Temporary Solution
        if testControl is not None: query = query + ' and test_control = {}'.format(
            str(testControl))
        if reachabilityCalculated: query = query + ' and reachability_type_id IN ( -1,4,13,14,27,28,30,32,33,34,35,40,1,15,18,20,22,37,2 )'

        result = dbHelper.queryDB(query, 'campaign_data_details')
        listOfUsers = []
        for eachUser in result:
            listOfUsers.append(eachUser[0])
        return listOfUsers

    @staticmethod
    def getAllUsersFromCampaignGroupRecipient(bucketId, groupVersionId):
        query = 'select distinct(user_id) from campaign_group_recipients__' + str(
            bucketId) + ' where group_version_id = ' + str(groupVersionId) + ' and org_id = ' + str(
            constant.config['orgId'])
        userList = []
        for numberOfTries in range(5):
            time.sleep(5)
            result = dbHelper.queryDB(query, 'campaign_data_details')
            if len(result) > 0:
                for eachUser in result:
                    userList.append(eachUser[0])
                break
        return userList

    @staticmethod
    def getCampaignGroupRecipientForCustomTags(bucketId, groupVersionId):
        Logger.log('Getting Campaign Group Recipient for Custom Tags with bucket Id :', bucketId,
                   ' and groupVersionId :', groupVersionId)
        query = 'select distinct(custom_tags),count(*) from campaign_group_recipients_custom_tags__' + str(
            bucketId) + ' where group_version_id = ' + str(groupVersionId) + ' and org_id = ' + str(constant.config['orgId'])
        for i in range(0, 5):
            result = result = dbHelper.queryDB(query, 'campaign_data_details')
            time.sleep(5)
            if len(result) > 0:
                break
        return result

    @staticmethod
    def getReachabilityStatus(id):
        Logger.log('Getting reachability status with id :', id)
        query = 'select ss_status from reachability_status_mapping where id = ' + str(id)
        result = dbHelper.queryDB(query, 'campaign_meta_details')[0][0]
        return result

    @staticmethod
    def updateReachabilityJobs():
        if constant.config['cluster'].lower() == 'nightly' or constant.config['cluster'].lower() == 'staging':
            Logger.log('Updating reachability jobs')

            getOpenIdQuery = "select id from reachability_job_details where status != 'CLOSED' and org_id = " + str(
                constant.config['orgId'])
            listOfIds = dbHelper.queryDB(getOpenIdQuery, 'campaign_meta_details')
            ids = ''
            for eachId in listOfIds:
                ids = ids + str(eachId[0]) + ','
            Logger.log('All Ids which are not in Closed state : {}'.format(ids))

            queryToUpdateReachablityjob = "update reachability_job_details set status = 'CLOSED' where status != 'CLOSED' and org_id = " + str(
                constant.config['orgId'])
            queryToUpdateReachablityjobBatch = "update reachability_batch_details set status = 'CLOSED' where job_id in (" + ids + ")"
            jobResult = dbHelper.queryDB(queryToUpdateReachablityjob, 'campaign_meta_details')
            if ids != '':
                batchResult = dbHelper.queryDB(queryToUpdateReachablityjobBatch, 'campaign_meta_details')
                Logger.log('Update Job Result :{} and batch Result :{}'.format(jobResult, batchResult))
        else:
            assert False, 'WARNING :There was a call To Update Reachability in cluster :{} , Fix This'.format(
                constant.config['cluster'].lower())

    @staticmethod
    def getSkippedErrorTypes():
        query = 'select id,error_type from skipped_error_types'
        result = dbHelper.queryDB(query, 'veneno')
        skippedErrorTypes = {}
        for k in result:
            skippedErrorTypes.update({k[1]: k[0]})
        return skippedErrorTypes

    @staticmethod
    def updateRowCountOfBucket(rows_count):
        query = 'select id from bucket_details order by id desc limit 1'
        selectResult = dbHelper.queryDB(query, 'campaign_meta_details')[0]
        if constant.config['cluster'] == 'nightly':
            query = 'update bucket_details set rows_count = {} where id = {}'.format(rows_count, selectResult[0])
            result = dbHelper.queryDB(query, 'campaign_meta_details')
            return {'oldBucket': int(selectResult[0]), 'newBucket': int(selectResult[0]) + 1}
        else:
            raise Exception('Warning : Warning : Warning : updateBucketIdRowCount getting called for Other clusters ')
