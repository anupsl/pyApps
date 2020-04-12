import json

from src.Constant.constant import constant
from src.dbCalls.campaignShard import data_details
from src.dbCalls.campaignShard import meta_details
from src.utilities.assertion import Assertion
from src.utilities.awsHelper import AWSHelper
from src.utilities.fileHelper import FileHelper
from src.utilities.logger import Logger


class GetListDBAssertion():
    def __init__(self, groupId, response, errorReasons={}, auditInfo=True, groupDetails=True, groupVersionDetails=True,
                 campaignHashLookUp=True, createAudienceJob=True, reachabilityCheck=True, bucketDetails=False,
                 campaignGroupRecipients=True, customTag=0, listAllCheck=False, bulkCaseSkip=True,bucketUsed='campaigns'):
        self.response = response
        self.errorReasons = errorReasons
        self.auditInfo = auditInfo
        self.createAudienceJob = createAudienceJob
        self.reachabilityCheck = reachabilityCheck
        self.campaignGroupRecipients = campaignGroupRecipients
        self.campaignGroupRecipientsForCustomTag = False
        self.listAllCheck = listAllCheck
        self.bulkCaseSkip = bulkCaseSkip
        self.bucketUsed=bucketUsed
        if int(customTag) > 0:
            self.numberOfCustomTag = customTag
            self.campaignGroupRecipientsForCustomTag = True

        self.metaInfoFromDB = meta_details(groupId=groupId, groupDetails=groupDetails,
                                           groupVersionDetails=groupVersionDetails,
                                           campaignHashLookUp=campaignHashLookUp, createAudienceJob=createAudienceJob,
                                           reachabilityCheck=reachabilityCheck, bucketDetails=bucketDetails).metaDetail
        self.dataInfoFromDB = data_details(self.metaInfoFromDB, campaignGroupRecipients=self.campaignGroupRecipients,
                                           campaignGroupRecipientsForCustomTag=self.campaignGroupRecipientsForCustomTag).dataDetail

    def check(self):
        self.assertBasicInfoOfList(self.metaInfoFromDB, self.response['json']['entity'])
        if self.auditInfo: self.assertAuditInfo(self.metaInfoFromDB, self.response['json']['entity'])
        if self.reachabilityCheck: self.assertReachability(self.metaInfoFromDB, self.response['json']['entity'])
        if self.createAudienceJob: self.assertUploadStatus(self.metaInfoFromDB,
                                                           self.response['json']['entity']['uploadStatus'],
                                                           self.errorReasons)
        if self.campaignGroupRecipients: self.assertDataDetails()

    def assertBasicInfoOfList(self, metaInfoFromDB, entity):
        Assertion.constructAssertion(str(entity['id']) == str(metaInfoFromDB['groupId']),
                                     'Group Id, Actual :{} and Expected :{}'.format(entity['id'],
                                                                                    metaInfoFromDB['groupId']))
        Assertion.constructAssertion(entity['label'] == metaInfoFromDB['groupDetails']['group_label'],
                                     'Group Label, Actual :{} and Expected :{}'.format(entity['label'],
                                                                                       metaInfoFromDB['groupDetails'][
                                                                                           'group_label']))
        Assertion.constructAssertion(entity['type'] == metaInfoFromDB['groupDetails']['type'],
                                     'Group Type, Actual :{} and Expected :{}'.format(entity['type'],
                                                                                      metaInfoFromDB['groupDetails'][
                                                                                          'type']))
        Assertion.constructAssertion(
            entity['customerCount'] == metaInfoFromDB['groupVersionDetails']['TEST']['customer_count'],
            'Group Version Customer Count, Actual :{} and Expected :{}'.format(entity['customerCount'],
                                                                               metaInfoFromDB['groupVersionDetails'][
                                                                                   'TEST']['customer_count']))
        if entity['testCount'] > 0: Assertion.constructAssertion(entity['testCount'] == int(
            json.loads(metaInfoFromDB['groupVersionDetails']['TEST']['params'])['test_count']),
                                                                 'Test Count, Actual :{} and Expected :{}'.format(
                                                                     entity['testCount'], json.loads(
                                                                         metaInfoFromDB['groupVersionDetails']['TEST'][
                                                                             'params'])['test_count']))
        if entity['controlCount'] > 0: Assertion.constructAssertion(entity['controlCount'] == int(
            json.loads(metaInfoFromDB['groupVersionDetails']['TEST']['params'])['control_count']),
                                                                    'Control Count, Actual :{} and Expected :{}'.format(
                                                                        entity['controlCount'], json.loads(
                                                                            metaInfoFromDB['groupVersionDetails'][
                                                                                'TEST']['params'])['control_count']))
        Assertion.constructAssertion(entity['versionId'] == metaInfoFromDB['groupVersionDetails']['TEST']['id'],
                                     'Group Version Id, Actual :{} and Expected :{}'.format(entity['versionId'],
                                                                                            metaInfoFromDB[
                                                                                                'groupVersionDetails'][
                                                                                                'TEST']['id']))
        Assertion.constructAssertion(
            entity['versionNumber'] == metaInfoFromDB['groupVersionDetails']['TEST']['version_number'],
            'Group Version Number, Actual :{} and Expected :{}'.format(entity['versionNumber'],
                                                                       metaInfoFromDB['groupVersionDetails']['TEST'][
                                                                           'version_number']))
        if self.reachabilityCheck:
            if entity['testCount'] > 0:
                Assertion.constructAssertion(entity['reachabilityStatus'] in ['CLOSED','PROCESSING'],
                                             'Status, Actual :{} and Expected CLOSED/PROCESSING'.format(
                                                 entity['reachabilityStatus']))
            else:
                Assertion.constructAssertion(False, 'Reachability Check is Enabled , but getting Test Count as 0 ',
                                             verify=True)

    def assertAuditInfo(self, metaInfoFromDB, entity):
        if 'createdBy' not in entity['auditInfo'] or 'createdOn' not in entity['auditInfo'] or 'lastUpdatedOn' not in \
                entity['auditInfo']:
            Assertion.constructAssertion(False,
                                         'AuditInfo, created_by,created_on,last_updated_by,last_updated_on info present in Audit Info')
        Assertion.constructAssertion(entity['auditInfo']['createdBy']['name'] == constant.config['intouchUsername'],
                                     'List Created By, Actual :{} and Expected :{}'.format(
                                         entity['auditInfo']['createdBy']['name'], constant.config['intouchUsername']),
                                     verify=True)
        Assertion.constructAssertion(str(entity['auditInfo']['createdBy']['id']) == str(constant.config['userId']),
                                     'List Created By, Actual :{} and Expected :{}'.format(
                                         entity['auditInfo']['createdBy']['id'], constant.config['userId']),
                                     verify=True)

    def assertReachability(self, metaInfoFromDB, entity):
        Assertion.constructAssertion(len(entity['reachabilityStats']) == len(metaInfoFromDB['reachabilityChannelType']),
                                     'Number of Reachability Stats, Actual :{} and Expected :{}'.format(
                                         len(entity['reachabilityStats']),
                                         len(metaInfoFromDB['reachabilityChannelType'])))
        for eachReachabilityStats in entity['reachabilityStats']:
            if 'channel' not in eachReachabilityStats: Assertion.constructAssertion(False,
                                                                                    'Channel Information Not Present in Reachability Stats')
            if eachReachabilityStats['channel'] in ['MOBILE', 'EMAIL']:
                Assertion.constructAssertion(len(eachReachabilityStats['accounts']) == 1,
                                             'Account Info For Mobile,Email: lenght Actual :{}'.format(
                                                 len(eachReachabilityStats['accounts'])))
                for eachAccount in eachReachabilityStats['accounts']:
                    '''
                    Task : To Do In DEV 
                    Assertion.constructAssertion(eachAccount['source'] == 'INSTORE', 'Source for Mobile,Email : Actual :{} and Expected :{}'.format(eachAccount['source'], 'INSTORE'), verify=True)
                    Assertion.constructAssertion(eachAccount['accountId'] == 'default', 'Source for Mobile,Email : Actual :{} and Expected :{}'.format(eachAccount['accountId'], 'default'), verify=True)
                    '''
                    overallCount = 0
                    for eachCategory in eachAccount['reachability']:
                        self.assertReachabilityAsPerCategory(metaInfoFromDB, eachReachabilityStats['channel'],
                                                             eachCategory['category'], eachCategory['count'])
                        overallCount = overallCount + eachCategory['count']
                    Assertion.constructAssertion(eachAccount['count'] == overallCount,
                                                 'Overall Count in Account Actual :{} and expected as per Calculation :{}'.format(
                                                     overallCount, eachAccount['count']))
            else:
                Assertion.constructAssertion(len(eachReachabilityStats['accounts']) >= 1,
                                             'Account Info For Wechat,Push,Line: lenght Actual :{}'.format(
                                                 len(eachReachabilityStats['accounts'])))

    def assertReachabilityAsPerCategory(self, metaInfoFromDB, channel, category, expectedCount):
        channelId = metaInfoFromDB['reachabilityChannelType'][channel.upper()]
        categoryId = metaInfoFromDB['reachabilityCategoryLabel'][category.upper()]
        actualCount = None

        for eachReachableRecordOfChannel in metaInfoFromDB['reachabilitySummaryReport'][channelId]:
            if eachReachableRecordOfChannel['reachability_label_id'] == categoryId:
                actualCount = eachReachableRecordOfChannel['count']
                break
        if actualCount is None: Assertion.constructAssertion(False,
                                                             'Reachability with channelId :{} of channel :{} and categoryId :{} of category :{} not found '.format(
                                                                 channelId, channel, categoryId, category))
        Assertion.constructAssertion(actualCount == expectedCount,
                                     'Actual Count :{} and expected Count :{}'.format(actualCount, expectedCount))

    def assertUploadStatus(self, metaInfoFromDB, uploadStatus, errorReasons={}):
        Assertion.constructAssertion(len(uploadStatus) == len(metaInfoFromDB['createAudienceJob']),
                                     'Number of Object is Upload Status :{} and in CreateAudienceJob :{}'.format(
                                         len(uploadStatus), len(metaInfoFromDB['createAudienceJob'])))
        for eachUploadObject in uploadStatus:
            if self.listAllCheck and eachUploadObject['status'] == 'ERROR':
                Assertion.constructAssertion(False,
                                             'ListId :{} have upload status in error state so bypassing the upload status Validation'.format(
                                                 metaInfoFromDB['groupId']), verify=True)
                break

            fileName = eachUploadObject['fileName']
            s3fileUrl = eachUploadObject['fileUrl']
            totalUploadCount = eachUploadObject['totalUploadCount']
            errorCount = eachUploadObject['errorCount']
            status = eachUploadObject['status']
            Assertion.constructAssertion(status != 'ERROR',
                                         's3FileName with File Name :{} in upload Status :{} and in createAudienceJob DB :{} '.format(
                                             fileName, status, metaInfoFromDB['createAudienceJob'][fileName]['status']))
            Assertion.constructAssertion(
                totalUploadCount == self.metaInfoFromDB['groupVersionDetails']['TEST']['customer_count'],
                'Total Upload Count is :{} and expected is :{}'.format(totalUploadCount,
                                                                       self.metaInfoFromDB['groupVersionDetails'][
                                                                           'TEST']['customer_count']), verify=True)
            if status == 'CLOSED':
                Assertion.constructAssertion(s3fileUrl == metaInfoFromDB['createAudienceJob'][fileName]['file_url'],
                                             'FileURL with File Name :{} in upload Status :{} and in createAudienceJob DB :{}'.format(
                                                 fileName, s3fileUrl,
                                                 metaInfoFromDB['createAudienceJob'][fileName]['file_url']))
                Assertion.constructAssertion(
                    totalUploadCount == metaInfoFromDB['createAudienceJob'][fileName]['total_upload_count'],
                    'total_upload_count with File Name :{} in upload Status :{} and in createAudienceJob DB :{}'.format(
                        fileName, totalUploadCount,
                        metaInfoFromDB['createAudienceJob'][fileName]['total_upload_count']))
                Assertion.constructAssertion(errorCount == metaInfoFromDB['createAudienceJob'][fileName]['error_count'],
                                             'error_count with File Name :{} in upload Status :{} and in createAudienceJob DB :{}'.format(
                                                 fileName, errorCount,
                                                 metaInfoFromDB['createAudienceJob'][fileName]['error_count']))
                Assertion.constructAssertion(status == metaInfoFromDB['createAudienceJob'][fileName]['status'],
                                             'status with File Name :{} in upload Status :{} and in createAudienceJob DB :{}'.format(
                                                 fileName, status,
                                                 metaInfoFromDB['createAudienceJob'][fileName]['status']))
                if errorCount == 0:
                    self.assertFileCreatedAndS3File(fileName, s3fileUrl)
                elif errorCount > 0 and self.bulkCaseSkip:
                    s3errorFileUrl = eachUploadObject['errorFileUrl']
                    if len(errorReasons) == 0: Assertion.constructAssertion(False,
                                                                            'Error Reason is not Provided For this Case , but at run time there is some ErrorCount Present , Info : Error Count :{} and errors3FileURL :{} '.format(
                                                                                errorCount,
                                                                                eachUploadObject['errorFileUrl']))
                    Assertion.constructAssertion(s3errorFileUrl is not '',
                                                 's3FileUrl is not empty as errorCount is :{}'.format(errorCount))
                    self.assertErrorFileCreateAndS3File(eachUploadObject, errorReasons)
                
            else:
                Assertion.constructAssertion(False,
                                             'Upload Status is not Validated as status for filename :{} is {} '.format(
                                                 fileName, status), verify=True)

    def assertFileCreatedAndS3File(self, fileName, s3FilePath):
        filePath = constant.autoTempFilePath + fileName
        dataFromS3 = AWSHelper.readFileFromS3('{}{}'.format(self.bucketUsed,constant.config['cluster']), s3FilePath)
        dataFromFile = FileHelper.readFile(filePath).split('\n')

        Assertion.constructAssertion(len(dataFromFile) == len(dataFromS3),
                                     'Data in File :{} and in s3 :{}'.format(dataFromFile, dataFromS3))
        for eachLine in dataFromS3:
            Assertion.constructAssertion(eachLine in dataFromFile,
                                         'line :{} Found in File used to Create List'.format(eachLine))

    def assertErrorFileCreateAndS3File(self, uploadObject, errorReasons):
        fileName = uploadObject['fileName']
        s3fileUrl = uploadObject['fileUrl']
        errorCount = uploadObject['errorCount']
        s3errorFileUrl = uploadObject['errorFileUrl']

        dataFromFile = filter(None, FileHelper.readFile(constant.autoTempFilePath + fileName).split('\n'))
        correctDataFromS3 = filter(None, AWSHelper.readFileFromS3('{}{}'.format(self.bucketUsed,constant.config['cluster']),
                                                                  s3fileUrl))
        errorDataFromoS3 = filter(None, AWSHelper.readFileFromS3('{}{}'.format(self.bucketUsed,constant.config['cluster']),
                                                                 s3errorFileUrl))[1:]

        Logger.log('DataList Of File :{} , Correct Data From s3 :{} and errorDataFroms3 :{}'.format(dataFromFile,
                                                                                                    correctDataFromS3,
                                                                                                    errorDataFromoS3))

        Assertion.constructAssertion(len(dataFromFile) == len(correctDataFromS3),
                                     'Total Error Count :{} and in s3 correct Data :{} , error Data :{}'.format(
                                         len(dataFromFile), len(correctDataFromS3), len(errorDataFromoS3)))
        Assertion.constructAssertion(len(errorDataFromoS3) == errorReasons[fileName]['numberOfUser'],
                                     'In S3 Number Of Error Users are :{} and Expected :{}'.format(
                                         len(errorDataFromoS3), errorReasons[fileName]['numberOfUser']))
        maxLineCheck = 100
        for eachUser in errorDataFromoS3:
            if maxLineCheck == 0: break
            Assertion.constructAssertion(eachUser.split(',')[-1] in errorReasons[fileName]['reason'],
                                         'Error :{} in File for line :{} , is in Expected List :{} '.format(
                                             eachUser.split(',')[-1], eachUser, errorReasons[fileName]))
            maxLineCheck = maxLineCheck - 1

    def assertDataDetails(self):
        params = json.loads(self.metaInfoFromDB['groupVersionDetails']['TEST']['params'])
        for eachHashId in self.dataInfoFromDB['campaignGroupRecipients']:
            Assertion.constructAssertion(
                len(self.dataInfoFromDB['campaignGroupRecipients'][eachHashId]) == int(params['test_count']) + int(
                    params['control_count']), 'Entry in CGR :{} and total test Count :{} and control count :{}'.format(
                    len(self.dataInfoFromDB['campaignGroupRecipients'][eachHashId]), params['test_count'],
                    params['control_count']))

        if self.campaignGroupRecipientsForCustomTag:
            Assertion.constructAssertion(
                len(self.dataInfoFromDB['campaignGroupRecipientsForCustomTag']) == int(params['test_count']) + int(
                    params['control_count']),
                'For CGR Custom Tag , number of test user  :{} and number of control user :{}'.format(
                    len(self.dataInfoFromDB['campaignGroupRecipientsForCustomTag']), int(params['test_count']),
                    int(params['control_count'])))
            Logger.log(self.dataInfoFromDB['campaignGroupRecipientsForCustomTag'])
            for each in self.dataInfoFromDB['campaignGroupRecipientsForCustomTag']:
                Assertion.constructAssertion(len(json.loads(
                    self.dataInfoFromDB['campaignGroupRecipientsForCustomTag'][each])) == self.numberOfCustomTag,
                                             'For User :{} , number Of Custom Tag :{}'.format(each,
                                                                                              self.numberOfCustomTag))
