import time

from src.Constant.constant import constant
from src.utilities.dbhelper import dbHelper
from src.utilities.logger import Logger
from src.utilities.mongoHelper import MongoHelper


class meta_details():
    def __init__(self, groupId=None, groupDetails=False, groupVersionDetails=False, campaignHashLookUp=False,
                 createAudienceJob=False, reachabilityCheck=False, bucketDetails=False):
        Logger.log('Getting Meta Details for groupId :{}'.format(groupId))
        self.groupId = groupId
        self.metaDetail = {
            'groupId': self.groupId
        }
        if groupDetails: self.groupDetails()
        if groupVersionDetails: self.groupVersionDetails()
        if campaignHashLookUp: self.campaignHashLookUp()
        if createAudienceJob: self.getCreateAudienceJob()
        if reachabilityCheck:
            self.sleepAsPerCluster()
            self.reachabilityJobDetail()
            self.reachabilityBatchDetail()
            self.reachabilityCategoryLabel()
            self.reachabilityChannelType()
            self.reachabilitySummaryReport()
        if bucketDetails: self.bucketDetails()

    def sleepAsPerCluster(self):
        if constant.config['cluster'] in ['nightly', 'staging']:
            time.sleep(10)
        else:
            time.sleep(20)

    def groupDetails(self):
        if self.groupId is None: raise Exception("GroupId is Not Passed to MetaDetails Object")
        query = 'select campaign_id,uuid,group_label,created_date,org_id,type,group_tags,is_reloading,is_visible,custom_tag_count from group_details where id = {}'.format(
            self.groupId)
        result = dbHelper.queryDB(query, 'campaign_meta_details')[0]
        self.metaDetail.update(
            {'groupDetails':
                {
                    'campaign_id': result[0],
                    'uuid': result[1],
                    'group_label': result[2],
                    'created_date': result[3],
                    'org_id': result[4],
                    'type': result[5],
                    'group_tags': result[6],
                    'is_reloading': result[7],
                    'is_visible': result[8],
                    'custom_tag_count': result[9]
                }
            }
        )

    def groupVersionDetails(self):
        if self.groupId is None: raise Exception("GroupId is Not Passed to MetaDetails Object")
        query = 'select id,params,target_type,customer_count,bucket_id,test_control,test_percentage,version_number,is_active from group_version_details where group_id = {} and org_id = {} and is_active=1'.format(
            self.groupId, constant.config['orgId'])
        result = dbHelper.queryDB(query, 'campaign_meta_details')
        constructResult = {}
        for eachRow in result:
            constructResult[eachRow[2]] = {
                'id': eachRow[0],
                'params': eachRow[1],
                'customer_count': eachRow[3],
                'bucket_id': eachRow[4],
                'test_control': eachRow[5],
                'test_percentage': eachRow[6],
                'version_number': eachRow[7],
                'is_active': eachRow[8]
            }
        self.metaDetail.update({'groupVersionDetails': constructResult})

    def campaignHashLookUp(self):
        query = 'select id,lookup_string from campaign_hash_lookup where org_id = {}'.format(constant.config['orgId'])
        result = dbHelper.queryDB(query, 'campaign_meta_details')
        buildResult = {}
        for eachResult in result:
            buildResult[eachResult[1]] = eachResult[0]
        self.metaDetail.update({'hashLookupDetails': buildResult})

    def reachabilityJobDetail(self):
        if 'groupVersionDetails' not in self.metaDetail: raise Exception(
            'GroupVersionDetail is not Enabled in meta_details Object')
        query = 'select id,status,expected_count,processed_count from reachability_job_details where org_id={} and group_id={}'.format(
            constant.config['orgId'], self.metaDetail['groupVersionDetails']['TEST']['id'])
        result = dbHelper.queryDB(query, 'campaign_meta_details')[0]
        self.metaDetail.update(
            {
                'reachabilityJobDetails': {
                    'id': result[0],
                    'status': result[1],
                    'expected_count': result[2],
                    'processed_count': result[3]
                }
            }
        )

    def reachabilityBatchDetail(self):
        query = 'select id,status,expected_count,processed_count,wl_job_id from reachability_batch_details where job_id = {}'.format(
            self.metaDetail['reachabilityJobDetails']['id'])
        result = dbHelper.queryDB(query, 'campaign_meta_details')
        buildResult = {}
        for eachResult in result:
            buildResult[eachResult[4]] = {
                'id': eachResult[0],
                'status': eachResult[1],
                'expected_count': eachResult[2],
                'processed_count': eachResult[3]
            }
        self.metaDetail.update({'reachabilityBatchDetails': buildResult})

    def reachabilityCategoryLabel(self):
        query = 'select id,category from reachability_category_labels'
        result = dbHelper.queryDB(query, 'campaign_meta_details')
        buildResult = {}
        for eachCategory in result:
            buildResult[eachCategory[1]] = eachCategory[0]
        self.metaDetail.update(
            {
                'reachabilityCategoryLabel': buildResult
            }
        )

    def reachabilityChannelType(self):
        # query = 'select id,channel from reachability_channel_types'
        # result = dbHelper.queryDB(query, 'campaign_meta_details')
        # buildResult = {}
        # for eachChannel in result:
        #    buildResult[eachChannel[1]] = eachChannel[0]
        self.metaDetail.update(
            {
                #'reachabilityChannelType': buildResult
                'reachabilityChannelType': {
                    'EMAIL':1,
                    'MOBILE':2,
                    'WECHAT':3,
                    'ANDROID':5,
                    'IOS':6,
                    'LINE':8,
                    'MOBILEPUSH':9
                }
            }
        )

    def reachabilitySummaryReport(self):
        query = 'select channel_id,reachability_label_id,count from reachability_summary_report where group_id= {} and job_id = {} group by channel_id,reachability_label_id'.format(
            self.metaDetail['groupVersionDetails']['TEST']['id'], self.metaDetail['reachabilityJobDetails']['id'])
        result = dbHelper.queryDB(query, 'campaign_meta_details')
        buildResult = {}
        for eachChannel in result:
            if eachChannel[0] not in buildResult:
                buildResult[eachChannel[0]] = [{'reachability_label_id': eachChannel[1], 'count': eachChannel[2]}]
            else:
                buildResult[eachChannel[0]].append({'reachability_label_id': eachChannel[1], 'count': eachChannel[2]})

        self.metaDetail.update(
            {
                'reachabilitySummaryReport': buildResult
            }
        )

    def getCreateAudienceJob(self):
        query = 'select uploaded_file_name,status,total_upload_count,file_url,error_count,error_file_url from create_audience_job where org_id = {} and group_version_id = {}'.format(
            constant.config['orgId'], self.metaDetail['groupVersionDetails']['TEST']['id'])
        result = dbHelper.queryDB(query, 'campaign_meta_details')
        buildResult = {}
        for eachJobFile in result:
            buildResult[eachJobFile[0]] = {
                'status': eachJobFile[1],
                'total_upload_count': eachJobFile[2],
                'file_url': eachJobFile[3],
                'error_count': eachJobFile[4],
                'error_file_url': eachJobFile[5]

            }
        self.metaDetail.update(
            {
                'createAudienceJob': buildResult
            }
        )

    def bucketDetails(self):
        query = 'select rows_count from bucket_details order by id desc limit 1 '
        result = dbHelper.queryDB(query, 'campaign_meta_details')[0]
        self.metaDetail.update({
            'bucketDetails': result
        }
        )


class data_details():
    def __init__(self, metaDetails, campaignGroupRecipients=False, campaignGroupRecipientsForCustomTag=False):
        Logger.log('Getting Data Details for groupId : {}'.format(metaDetails['groupId']))
        self.metaDetails = metaDetails
        self.dataDetail = dict()
        if campaignGroupRecipients: self.campaignGroupRecipients()
        if campaignGroupRecipientsForCustomTag: self.campaignGroupRecipientsForCustomTag()

    def campaignGroupRecipients(self):
        if 'groupVersionDetails' not in self.metaDetails: raise Exception(
            'GroupVersionDetail is not Enabled in meta_details Object')
        query = 'select user_id,hash_id,reachability_type_id,test_control from campaign_data_details.campaign_group_recipients__{} where group_version_id = {} and org_id = {}'.format(
            self.metaDetails['groupVersionDetails']['TEST']['bucket_id'],
            self.metaDetails['groupVersionDetails']['TEST']['id'], constant.config['orgId'])
        result = dbHelper.queryDB(query, 'campaign_data_details')
        buildResult = {}
        for eachRecord in result:
            if eachRecord[1] not in buildResult:
                buildResult[eachRecord[1]] = {
                    eachRecord[0]: {
                        'reachability_type_id': eachRecord[2],
                        'test_control': eachRecord[3]
                    }
                }
            else:
                buildResult[eachRecord[1]].update({
                    eachRecord[0]: {
                        'reachability_type_id': eachRecord[2],
                        'test_control': eachRecord[3]
                    }
                })
        self.dataDetail.update({'campaignGroupRecipients': buildResult})

    def campaignGroupRecipientsForCustomTag(self):
        query = 'select user_id,custom_tags from campaign_data_details.campaign_group_recipients_custom_tags__{} where group_version_id = {} and org_id = {}'.format(
            self.metaDetails['groupVersionDetails']['TEST']['bucket_id'],
            self.metaDetails['groupVersionDetails']['TEST']['id'], constant.config['orgId'])
        result = dbHelper.queryDB(query, 'campaign_data_details')
        buildResult = {}
        for eachRecord in result:
            buildResult[eachRecord[0]] = eachRecord[1]
        self.dataDetail.update({'campaignGroupRecipientsForCustomTag': buildResult})


class list_Calls():
    def __init__(self):
        pass

    def getAllGroupIds(self, limit, offset, sort, search=None):
        query = "select gd.id from group_details gd JOIN group_version_details gvd ON gd.org_id = gvd.org_id AND gd.id = gvd.group_id WHERE gd.org_id = {} groupSearch  AND gd.is_visible=1 AND gvd.is_active=1 AND gvd.target_type='TEST' order by gd.{} desc limit {},{}".format(
            constant.config['orgId'], sort, offset, limit)
        if search is None:
            query = query.replace('groupSearch', '')
        else:
            query = query.replace('groupSearch', 'and gd.group_label like "%{}%"'.format(search))
        result = dbHelper.queryDB(query, 'campaign_meta_details')
        buildResult = []
        for each in result:
            buildResult.append(str(each[0]))
        return buildResult

    def getAllGroupDetails(self, limit, offset, sort, search=None, groupType='ORG_USERS', onlyIds = False):
        query = "select gd.id, gd.group_label from group_details gd JOIN group_version_details gvd ON gd.org_id = gvd.org_id AND gd.id = gvd.group_id  where gd.org_id = {} and gd.type = '{}' groupSearch and gd.is_visible=1 and gvd.is_active=1 and gvd.target_type='TEST' order by gd.{} desc limit {},{}".format(
            constant.config['orgId'], groupType, sort, offset, limit)
        if search is None:
            query = query.replace('groupSearch', '')
        else:
            query = query.replace('groupSearch', 'and gd.group_label like "%{}%"'.format(search))
        result = dbHelper.queryDB(query, 'campaign_meta_details')
        buildResult = []
        if not onlyIds:
            for each in result:
                buildResult.append({'gId': str(each[0]), 'gLabel': each[1]})
        else:
            for each in result:
                buildResult.append(str(each[0]))
        return buildResult

    def getExistingUsers(self, numberOfusers, offset=0, mobilePush=False,commChannels=None):
        if mobilePush:
            listOfMobilePushUsers = list()
            commChannels = constant.config['mobilepush']['channels'] if commChannels is None else commChannels
            for commChannelType in commChannels:
                port = constant.config['INTOUCH_DB_MONGO_MASTER']
                query = {'orgId': constant.config['orgId'], 'source': 'WEB_ENGAGE',
                         'commChannels.type': commChannelType}
                userIds = MongoHelper.findDocuments('multi_profile', 'profileV2', port, query, limit=1)[0]['userId']
                listOfMobilePushUsers.append([userIds])
                if constant.config['cluster'] in ['nightly'] and 'android' in constant.config['mobilepush']['channels']:
                    try:
                        query = "select id from users where org_id = {} and mobile = '{}'".format(
                            constant.config['orgId'],
                            constant.config[
                                'mobilepush'][
                                'androidE2E_User'])
                        android_id = dbHelper.queryDB(query, 'user_management')[0]
                        if android_id is not None: listOfMobilePushUsers[0] = android_id
                    except Exception, exp:
                        Logger.log(
                            "Tried Adding Number :{} as Android User in List but failed due to Exception :{}".format(
                                constant.config['mobilepush']['androidE2E_User'], exp))
            Logger.log('List Of Existing Users :{}'.format(listOfMobilePushUsers))
            return listOfMobilePushUsers
        else:
            query = "select u.id,u.firstname,u.lastname,u.mobile,u.email,l.external_id from users u,loyalty l where u.id=l.user_id and u.email like 'iris_automation%' and u.org_id = " + str(
                constant.config['orgId']) + " and l.publisher_id = " + str(
                constant.config['orgId']) + " and l.type = 'loyalty' order by u.id asc limit {},{} ".format(offset,
                                                                                                            numberOfusers)
            result = dbHelper.queryDB(query, 'user_management')
            return result

    def getCustomerCountInGVD(self, groupId):
        query = "select customer_count from group_version_details where group_id = {} and org_id = {} and target_type = 'TEST' and is_active = 1".format(
            groupId, constant.config['orgId'])
        result = dbHelper.queryDB(query, 'campaign_meta_details')
        return result[0][0]

    def getParamsFromGVD(self, groupId):
        query = "select params from group_version_details where group_id = {} and org_id = {} and target_type = 'TEST'".format(
            groupId, constant.config['orgId'])
        result = dbHelper.queryDB(query, 'campaign_meta_details')
        return result[0][0]

    def getIdOfReloadedList(self, testControl):
        query = "select group_id,version_number from group_version_details where org_id={} and version_number>1 and target_type='TEST' and customer_count>0 and test_control='{}' order by id desc limit 1".format(
            constant.config['orgId'], testControl.upper())
        result = dbHelper.queryDB(query, 'campaign_meta_details')
        if len(result) == 0: raise Exception('NoReloadListFoundInOrg:{}'.format(constant.config['orgId']))
        return {'id': result[0][0], 'version': result[0][1]}

    def getIdofOlderList(self, testControl):
        query = "select group_id,version_number from group_version_details where org_id = {} and target_type='TEST' and customer_count>0 and test_control = '{}' and campaign_id>0 order by id desc limit 1;".format(
            constant.config['orgId'], testControl.upper())
        result = dbHelper.queryDB(query, 'campaign_meta_details')
        if len(result) == 0: raise Exception('NoOlderListFoundInOrg:{}'.format(constant.config['orgId']))
        return {'id': result[0][0], 'version': result[0][1]}

    def getNonVisibleList(self, type):
        query = "select id from group_details where org_id = {} and is_visible =0 and type = '{}' order by id desc limit 1".format(
            constant.config['orgId'], type)
        result = dbHelper.queryDB(query, 'campaign_meta_details')
        return {'id': result[0][0]}

    def updateGroupVersionDetailAsInactive(self, groupId):
        query = "update group_version_details set is_active = 0 where org_id = {} and group_id = {}".format(
            constant.config['orgId'], groupId)
        dbHelper.queryDB(query, 'campaign_meta_details')

    def getReachabilityStatus(self, groupId):
        query = "select status from reachability_job_details where org_id = {} and group_id = {}".format(
            constant.config['orgId'], groupId)
        result = dbHelper.queryDB(query, 'campaign_meta_details')
        if len(result) == 0:
            return 'PROCESSING'
        else:
            return result[0][0]

    def getListWithNoUsers(self):
        query = "select group_id from group_version_details  where org_id = {} and customer_count = 0 limit 1".format(
            constant.config['orgId'])
        result = dbHelper.queryDB(query, 'campaign_meta_details')
        if len(result) == 0: raise Exception('NoListFoundWith:{0}UsersException')
        return result[0][0]

    def getGroupVersionId(self, groupId):
        query = "select id from group_version_details where group_id = {} and org_id = {} and target_type = 'TEST'".format(
            groupId, constant.config['orgId'])
        result = dbHelper.queryDB(query, 'campaign_meta_details')
        return result[0][0]

    def getUploadedFileUrl(self, groupId):
        query = "select file_url from create_audience_job where org_id = {} and group_version_id = {}".format(
            constant.config['orgId'], self.getGroupVersionId(groupId))
        result = dbHelper.queryDB(query, 'campaign_meta_details')
        return result[0][0]

    def getGroupLabelById(self, groupId):
        query = "select group_label from group_details where org_id = {} and id = {}".format(constant.config['orgId'],
                                                                                             groupId)
        result = dbHelper.queryDB(query, 'campaign_meta_details')
        return result[0][0]

    def getMaxVersionOfGroup(self, groupId):
        query = 'select max(version_number) from group_version_details where group_id = {}'.format(groupId)
        result = dbHelper.queryDB(query, 'campaign_meta_details')
        return result[0][0]
