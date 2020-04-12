import json
import time

from bson import ObjectId

from src.Constant.constant import constant
from src.utilities.dbhelper import dbHelper
from src.utilities.logger import Logger
from src.utilities.mongoHelper import MongoHelper


class message_info():
    def __init__(self, messageId, messageCollection=True, messageJobDetailsCollection=True,
                 messageVariantsCollection=True, version=0, personalize=False):
        self.messageId = messageId
        self.messageDbDetail = dict()
        self.personalize = personalize
        if messageCollection: self.messageCollection()
        if messageJobDetailsCollection: self.messageJobDetailsCollection()
        if messageVariantsCollection: self.messageVariantsCollection()

    def messageCollection(self):
        query = {'_id': ObjectId(self.messageId)}
        result = MongoHelper.findDocuments('campaigns', 'message', constant.config['CAMPAIGNS_DB_MONGO_MASTER'], query)
        self.messageDbDetail.update({'message_collection': result[0]})
        if 'version' in self.messageDbDetail['message_collection'] :
            self.version = self.messageDbDetail['message_collection']['version']
        else:
            self.version=0
            
    def messageJobDetailsCollection(self):
        self.messageDbDetail['messageJobDetails_collection'] = dict()
        jobType = ['MESSAGE_TARGET_AUDIENCE', 'VARIANT_CREATION'] if not self.personalize  else [
            'MESSAGE_TARGET_AUDIENCE', 'PERSONALIZE_TARGET_AUDIENCE', 'PERSONALIZED_TARGET_AUDIENCE_POLLER',
            'PERSONALIZED_AUDIENCE_GROUP_CREATION', 'PERSONALIZED_AUDIENCE_GROUPS_POLLER',
            'PERSONALIZED_VARIANT_CREATION']
        for eachType in jobType:
            if message_calls().waitForJobDetailsStatusToClose(self.messageId, eachType, version=self.version):
                query = {"messageId": self.messageId, 'type': eachType, 'messageVersion': self.version}
                result = MongoHelper.findDocuments('campaigns', 'messageJobDetails',
                                                   constant.config['CAMPAIGNS_DB_MONGO_MASTER'],
                                                   query, sort='messageVersion')
                self.messageDbDetail['messageJobDetails_collection'].update({eachType: result})
            else:
                raise Exception('Job Details Status For :{} is not yet Closed , check time :{}'.format(eachType, str(
                    int(time.time()))))

    def messageVariantsCollection(self):
        variant_detail = list()
        variant_creation_key = 'VARIANT_CREATION' if not self.personalize else 'PERSONALIZED_VARIANT_CREATION'
        for eachVariant in self.messageDbDetail['messageJobDetails_collection'][variant_creation_key]:
            for eachVariantId in eachVariant['jobContext']['messageVariantIds']:
                query = {'_id': ObjectId(eachVariantId)}
                variant_detail.append(MongoHelper.findDocuments('campaigns', 'messageVariant',
                                                                constant.config['CAMPAIGNS_DB_MONGO_MASTER'],
                                                                query)[0])

            eachVariant.update({'variant_detail': variant_detail})


class message_calls():
    def getDeliverySetting(self, channel):
        query = "select dg.id,ci.type,ci.value from domain_properties_gateway_map dg, contact_info ci where dg.org_id = " \
                "{} and ci.org_id={} and dg.domain_prop_id=ci.domain_prop_id and ci.message_class = '{}' AND dg.is_active = 1 " \
                "and dg.is_validated = 1".format(
            constant.config['orgId'], constant.config['orgId'], channel.upper())
        result = dbHelper.queryDB(query, 'nsadmin')
        domainProp = dict()
        for eachInfo in result:
            domainProp[eachInfo[1]] = eachInfo[2]
        domainProp['mapId'] = result[0][0]
        return domainProp

    def waitForJobDetailsStatusToClose(self, messageId, jodDetailsType, maxNumberOfAttempts=25, version=0,sleepTime=20):
        Logger.log('Waiting For MessageId :{} with JobDetail :{} for MaxAttempts :{} and version :{}'.format(messageId,
                                                                                                             jodDetailsType,
                                                                                                             maxNumberOfAttempts,
                                                                                                             version))
        if jodDetailsType == 'PERSONALIZED_VARIANT_CREATION': maxNumberOfAttempts = 50
        version = \
        message_info(messageId, messageJobDetailsCollection=False, messageVariantsCollection=False).messageDbDetail[
            'message_collection']['version']
        query = {"messageId": messageId, 'type': jodDetailsType, 'messageVersion': version}
        while (True):
            result = MongoHelper.findDocuments('campaigns', 'messageJobDetails',
                                               constant.config['CAMPAIGNS_DB_MONGO_MASTER'],
                                               query)
            if len(result) != 0:
                for eachJobDetailOfTypeTargetAudience in result:
                    status = True if eachJobDetailOfTypeTargetAudience['status'] == 'CLOSED' else False
            else:
                status = False
                Logger.log('Variant Entry Not Yet Created')

            if status or maxNumberOfAttempts == 0:
                Logger.log('Status :{} and MaxAttempts :{}'.format(status, maxNumberOfAttempts))
                if status == False : raise Exception('VariantNotClosedExceptionWithStatus:{}'.format(status))
                break
            else:
                time.sleep(sleepTime)
                maxNumberOfAttempts = maxNumberOfAttempts - 1

        return status

    def getVariantIdByMessageId(self, messageId, numberOfTries=10):
        for _ in range(numberOfTries):
            query = {"messageId": messageId}
            result = MongoHelper.findDocuments('campaigns', 'messageVariant',
                                               constant.config['CAMPAIGNS_DB_MONGO_MASTER'],
                                               query)
            if len(result) == 0:
                time.sleep(10)
            else:
                break
        if len(result) == 0: raise Exception('VariantNotCreatedException')
        return result[0]['_id']

    def getVariantStatusByMessageId(self, messageId, version):
        listOfActiveStatus = list()
        for _ in range(10):
            query = {"messageId": messageId, 'messageVersion': version, 'type': 'VARIANT_CREATION'}
            try:
                result = MongoHelper.findDocuments('campaigns', 'messageJobDetails',
                                                   constant.config['CAMPAIGNS_DB_MONGO_MASTER'],
                                                   query)[0]['jobContext']['messageVariantIds']
                Logger.log(
                    'MessageVariant Ids for Message :{} with version :{} are :{}'.format(messageId, version, result))
                for eachVariant in result:
                    variantInfo = MongoHelper.findDocuments('campaigns', 'messageVariant',
                                                            constant.config['CAMPAIGNS_DB_MONGO_MASTER'],
                                                            {'_id': ObjectId(eachVariant)})[0]
                    listOfActiveStatus.append(variantInfo)
                break
            except Exception, exp:
                Logger.log('Exception fetching getVariantStatusByMessageId :{}'.format(exp))
                time.sleep(10)
        return listOfActiveStatus

        if len(result) == 0: raise Exception('VariantNotCreatedException')
        return result[0]['_id'], result[0]['active']

    def getNUmberOfInactiveVariantForMessage(self, messageId):
        query = {"messageId": messageId, 'active': False}
        result = MongoHelper.findDocuments('campaigns', 'messageVariant',
                                           constant.config['CAMPAIGNS_DB_MONGO_MASTER'],
                                           query, limit=10)
        return len(result)

    def getMapOfVersions(self, messageId, numberOfVersions):
        query = {"messageId": messageId}
        for eachTry in range(10):
            result = MongoHelper.findDocuments('campaigns', 'messageVariant',
                                               constant.config['CAMPAIGNS_DB_MONGO_MASTER'],
                                               query, limit=10)
            if len(result) == numberOfVersions: break
            time.sleep(10)
        if len(result) != numberOfVersions + 1:
            raise Exception('NumberOfVersionRequired:{}AndInMongo:{}'.format(numberOfVersions, len(result)))
        mapOfVesions = dict()
        idx = 0
        for each in result:
            mapOfVesions.update({idx: each['messageVersion']})
            idx = idx + 1
        return mapOfVesions

    def getProgrameId(self):
        query = 'select id from program where org_id = ' + str(
            constant.config['orgId']) + ' and is_active = 1 and is_default = 1 order by id desc limit 1'
        result = dbHelper.queryDB(query, 'warehouse')[0]
        return str(result[0])

    def getAllocationIdForPrograme(self, programeId):
        query = 'select id from strategies where org_id = ' + str(
            constant.config['orgId']) + ' and program_id = ' + str(
            programeId) + " and owner = 'campaign'" + ' and strategy_type_id = 1 order by id asc limit 1'
        result = dbHelper.queryDB(query, 'warehouse')[0]
        return str(result[0])

    def getExpiryIdForPrograme(self, programeId):
        query = 'select id from strategies where org_id = ' + str(
            constant.config['orgId']) + ' and program_id = ' + str(
            programeId) + ' and strategy_type_id = 3 order by id desc limit 1'
        result = dbHelper.queryDB(query, 'warehouse')[0]
        return str(result[0])

    def getExistingMessageNameAndCampaignId(self):
        result = MongoHelper.findDocuments('campaigns', 'message',
                                           constant.config['CAMPAIGNS_DB_MONGO_MASTER'],
                                           {'orgId': constant.config['orgId']})
        return result[0]['name'], result[0]['campaignId']

    def checkCampaignHaveMessage(self, campaignId):
        query = {
            'orgId': constant.config['orgId'],
            'campaignId': campaignId
        }
        result = MongoHelper.findDocuments('campaigns', 'message',
                                           constant.config['CAMPAIGNS_DB_MONGO_MASTER'],
                                           query)
        if len(result) > 0:
            return True
        else:
            return False

    def getNumberOfMessagesInCampaign(self, campaignId):
        query = {
            'orgId': constant.config['orgId'],
            'campaignId': campaignId,
            'test': False
        }
        return len(MongoHelper.findDocuments('campaigns', 'message',
                                             constant.config['CAMPAIGNS_DB_MONGO_MASTER'],
                                             query, limit=50))

    def getCommunicationDetails(self, messageId, messageQueueId):
        self.waitForCommunicationDetailsToBeCreated(messageId, messageQueueId)
        query = 'select id,communication_type,state from communication_details where org_id = {} and message_id= "{}" and message_queue_id = "{}"'.format(
            constant.config['orgId'], messageId, messageQueueId)
        for numberOfTries in range(25):
            result = dbHelper.queryDB(query, 'veneno')
            if len(result) > 0:
                if str(result[0][2]) == 'CLOSED':
                    break
            time.sleep(10)
        return result[0][0], result[0][1]

    def getCommunicationDetailsWithOnlyMessageId(self, messageId):
        query = 'select id,communication_type,state from communication_details where org_id = {} and message_id= "{}"'.format(
            constant.config['orgId'], messageId)
        for numberOfTries in range(25):
            result = dbHelper.queryDB(query, 'veneno')
            if len(result) > 0:
                if str(result[0][2]) == 'CLOSED':
                    break
            time.sleep(10)
        return result[0][0], result[0][1]

    def waitForCommunicationDetailsToBeCreated(self, messageId, messageQueueId):
        query = 'select id,communication_type from communication_details where org_id = {} and message_id= "{}" and message_queue_id = "{}"'.format(
            constant.config['orgId'], messageId, messageQueueId)
        for numberOfTries in range(25):
            result = dbHelper.queryDB(query, 'veneno')
            if len(result) > 0: break
            time.sleep(20)
        if len(result) == 0: raise Exception(
            'No Entry in Communication Detail , message id :{} and messageQueueId :{}'.format(messageId,
                                                                                              messageQueueId))

    def getApproveStatus(self, messageId):
        query = {
            '_id': ObjectId(messageId)
        }
        return MongoHelper.findDocuments('campaigns', 'message',
                                         constant.config['CAMPAIGNS_DB_MONGO_MASTER'],
                                         query)[0]['state']

    def getCronDetails(self, cronId):
        query = 'select component,params,status,cron_pattern from cron_tasks where id = {}'.format(cronId)
        result = dbHelper.queryDB(query, 'scheduler')[0]
        return {
            'component': result[0],
            'params': result[1],
            'status': result[2],
            'cron_pattern': result[3]
        }

    def getCronIdWithVariantId(self, variantId, expectedStatus):
        query = "select id,component,cron_pattern,scheduled_time,status,params from cron_tasks where params like '%{}%'".format(
            variantId)
        for _ in range(10):
            result = dbHelper.queryDB(query, 'scheduler')
            if len(result) == 0 or result[0][4] not in expectedStatus:
                time.sleep(10)
            else:
                break
        if len(result) == 0: return None
        return {
            'id': result[0][0],
            'component': result[0][1],
            'cron_pattern': result[0][2],
            'scheduled_time': result[0][3],
            'status': result[0][4],
            'params': result[0][5]
        }

    def updateParamsInCron(self, params, cronId):
        if constant.config['cluster'] == 'nightly':
            try:
                query = "update cron_tasks set params = '{}' where id = {}".format(params, cronId)
                dbHelper.queryDB(query, 'scheduler')
            except:
                raise Exception('CronNotUpdatedWithId:{}'.format(cronId))
        else:
            raise Exception('UpdateCronNotPermittedInCluster')

    def getStatusOfMessageQueue(self, messageQueueId):
        query = 'select status from message_queue where id = {} and org_id = {}'.format(messageQueueId,
                                                                                        constant.config['orgId'])
        result = dbHelper.queryDB(query, 'msging')
        return result[0][0]

    def getTargetAudienceForTestAndPreview(self, messageId):
        try:
            query = {
                '_id': ObjectId(messageId)
            }
            result = MongoHelper.findDocuments('campaigns', 'message',
                                               constant.config['CAMPAIGNS_DB_MONGO_MASTER'],
                                               query)[0]
            listId = result['targetAudience']['include'][0]
            campaignId = result['campaignId']
        except Exception, exp:
            raise Exception('Exception While Getting Target Audience of test&Preview , exp:{}'.format(exp))
        return listId, campaignId

    def getAccountIdFromMeta(self, accountId):
        query = "select id from org_channel_accounts where org_id = {} and account_name = '{}'".format(
            constant.config['orgId'], accountId)
        port = constant.config['INTOUCH_META_DB_MYSQL'][0]
        accountId = dbHelper.query(query, 'masters', port)[0][0]
        return accountId

    def getKeyOfDeepLink(self):
        query = "select id from  channel_config_keys where label = 'Deep Link'"
        port = constant.config['INTOUCH_META_DB_MYSQL'][0]
        key = dbHelper.query(query, 'masters', port)[0][0]
        return key

    def getDeepLinkvalue(self, accountId, keyId):
        query = "select value from channel_config_key_values where account_id = {} and key_id = {}".format(accountId,
                                                                                                           keyId)
        port = constant.config['INTOUCH_META_DB_MYSQL'][0]
        return json.loads(dbHelper.query(query, 'masters', port)[0][0])

    def getAuditDetails(self, messageId):
        query = "select details,tracked_item,tracked_class from campaign_audit where tracked_class='MessageEntity' and details like '%{}%' order by id desc limit 1".format(
            messageId)
        result = dbHelper.queryDB(query, 'audit_logs')
        if len(result) == 0: return None
        return result[0][0], result[0][1], result[0][2]


class pointsMetaInfo():
    def __init__(self):
        self.pointsMeta = dict()
        self.execute()

    def execute(self):
        self.getProgrameinfo()
        self.getTiersForeachPrograme()
        self.getStrategyForProgramId()

    def getProgrameinfo(self):
        query = "select id,name,points_currency_ratio,is_active,is_default from program where org_id = {}".format(
            constant.config['orgId'])
        result = dbHelper.queryDB(query, 'warehouse')
        for eachProgramDetail in result:
            self.pointsMeta.update({
                eachProgramDetail[0]: {
                    'name': eachProgramDetail[1],
                    'pointsCurrencyRatio': eachProgramDetail[2],
                    'default': bool(eachProgramDetail[4]),
                    'active': bool(eachProgramDetail[3]),
                    'programId': int(eachProgramDetail[0])
                }
            })

    def getTiersForeachPrograme(self):
        for eachProgrameId in self.pointsMeta:
            query = "select id,serial_number,name,description from program_slabs where org_id = {} and program_id = {}".format(
                constant.config['orgId'], eachProgrameId)
            result = dbHelper.queryDB(query, 'warehouse')
            self.pointsMeta[eachProgrameId].update({'tiers': {}})
            for eachTier in result:
                self.pointsMeta[eachProgrameId]['tiers'].update({
                    eachTier[0]: {
                        'serialNumber': eachTier[1],
                        'name': eachTier[2],
                        'description': eachTier[3]
                    }
                })

    def getStrategyForProgramId(self):
        for eachProgrameId in self.pointsMeta:
            query = "select id,name,description,strategy_type_id,property_values from strategies where org_id = {} and program_id = {} and owner = 'CAMPAIGN'".format(
                constant.config['orgId'], eachProgrameId)
            result = dbHelper.queryDB(query, 'warehouse')
            self.pointsMeta[eachProgrameId].update({
                "strategy": {
                    "allocationStrategy": {

                    },
                    "expiryStrategy": {

                    }
                }
            })
            for eachStrategy in result:
                if str(eachStrategy[3]) == '1':
                    self.pointsMeta[eachProgrameId]['strategy']['allocationStrategy'].update({
                        eachStrategy[0]: {
                            'id': eachStrategy[0],
                            'name': eachStrategy[1],
                            'description': eachStrategy[2],
                            'propertyValues': json.loads(eachStrategy[4])
                        }
                    })
                if str(eachStrategy[3]) == '3':
                    self.pointsMeta[eachProgrameId]['strategy']['expiryStrategy'].update({
                        eachStrategy[0]: {
                            'id': eachStrategy[0],
                            'name': eachStrategy[1],
                            'description': eachStrategy[2],
                            'propertyValues': json.loads(eachStrategy[4])
                        }
                    })


class pocMetaInfo():
    def __init__(self):
        self.pocOrgMeta = dict()
        self.pocCapMeta = dict()
        self.pocMetaData = dict()
        self.execute()

    def execute(self):
        self.getOrgPocinfo()
        self.getOrgPocDetails()
        self.getCapPocinfo()
        self.getCapPocDetails()

        self.pocMetaData.update({
            'orgPocs': self.pocOrgMeta,
            'capPocs': self.pocCapMeta
        })

    def getOrgPocinfo(self):
        query = "SELECT admin_user_roles.admin_user_id from admin_user_roles  INNER JOIN org_roles ON admin_user_roles.org_id = org_roles.org_id AND org_roles.id=admin_user_roles.role_id  WHERE role_name = 'ORG_POC' and admin_user_roles.org_id = {}".format(
            constant.config['orgId'])
        result = dbHelper.queryDB(query, 'masters')
        for eachOrgPoc in result:
            self.pocOrgMeta.update({
                eachOrgPoc[0]: {
                    'userId': eachOrgPoc[0]
                }
            })

    def getOrgPocDetails(self):
        for eachPoc in self.pocOrgMeta:
            query = "SELECT first_name,last_name,email,mobile,mobile_validated,email_validated  FROM `admin_users` WHERE `id` = {} AND `org_id` = {}".format(
                eachPoc, constant.config['orgId'])
            result = dbHelper.queryDB(query, 'masters')
            if len(result) != 0:
                result = result[0]
                self.pocOrgMeta[eachPoc].update({
                    'firstName': result[0],
                    'lastName': result[1],
                    'email': result[2],
                    'mobile': result[3],
                    'validMobile': bool(result[4]),
                    'validEmail': bool(result[5])
                })
            else:
                Logger.log('No orgPoc users Found')

    def getCapPocinfo(self):
        query = "SELECT admin_user_roles.admin_user_id from admin_user_roles  INNER JOIN org_roles ON admin_user_roles.org_id = org_roles.org_id AND org_roles.id=admin_user_roles.role_id  WHERE role_name = 'CAP_POC' and admin_user_roles.org_id = {}".format(
            constant.config['orgId'])
        for port in constant.config['INTOUCH_DB_MYSQL_MASTER']:
            result = dbHelper.query(query, 'masters', port)
            if len(result) != 0: break

        for eachCapPoc in result:
            self.pocCapMeta.update({
                eachCapPoc[0]: {
                    'userId': eachCapPoc[0]
                }
            })

    def getCapPocDetails(self):
        for eachPoc in self.pocCapMeta:
            query = "SELECT first_name,last_name,email,mobile,mobile_validated,email_validated  FROM `admin_users` WHERE `id` = {}".format(
                eachPoc)
            for port in constant.config['INTOUCH_DB_MYSQL_MASTER']:
                result = dbHelper.query(query, 'masters', port)
                if len(result) != 0: break
            if len(result) != 0:
                result = result[0]
                self.pocCapMeta[eachPoc].update({
                    'firstName': result[0],
                    'lastName': result[1],
                    'email': result[2],
                    'mobile': result[3],
                    'validMobile': bool(result[4]),
                    'validEmail': bool(result[5])
                })
            else:
                Logger.log('No CapPoc users Found')


class monitorStatus_calls():
    def getSummaryReportVeneno(self, msgId):
        query = 'SELECT st.id,rv.sub_type, st.description, rv.count,st.is_replayable FROM veneno.summary_report_veneno rv JOIN veneno.skipped_error_types st ON rv.sub_type = st.error_type where msg_id = {}'.format(
            msgId)
        result = dbHelper.queryDB(query, 'veneno')
        venenoReportResult = []
        if len(result) != 0:
            for venenoReport in result:
                venenoReportResult.append(
                    {'skippedErrorId': venenoReport[0], 'skippedType': venenoReport[1], 'description': venenoReport[2],
                     'count': venenoReport[3], 'replayable': True if venenoReport[4] else False})
        return venenoReportResult

    def getSummaryReportNsadmin(self, msgId):
        query = 'select ns.count, ds.status, ds.description from veneno.summary_report_nsadmin ns LEFT JOIN veneno.delivery_status ds ON ns.delivery_status_id = ds.id where ns.msg_id = {}'.format(
            msgId)
        for _ in range(5):
            result = dbHelper.queryDB(query, 'veneno')
            if len(result) == 0:
                time.sleep(10)
            else:
                break
        venenoReportResult = []
        if len(result) != 0:
            for eachRowBasedOnDeliveryStatusId in result:
                venenoReportResult.append({'status': 'About to send' if eachRowBasedOnDeliveryStatusId[
                                                                            1] == 'SENT_TO_NSADMIN' else (
                    (eachRowBasedOnDeliveryStatusId[1].replace('_', ' ')).lower()).title(),
                                           'category': 'SENT' if eachRowBasedOnDeliveryStatusId[
                                                                     1] != 'SENT_TO_NSADMIN' else 'IN_PROGRESS',
                                           'description': eachRowBasedOnDeliveryStatusId[2],
                                           'count': eachRowBasedOnDeliveryStatusId[0]})
        return venenoReportResult

    def getExecutionJobStatus(self, messageObjId, queryParam=None):
        if queryParam is not None:
            pass
        query = "select error_description,UNIX_TIMESTAMP(start_date),campaign_id from veneno.pre_execution_job_status where org_id = {} and message_id = '{}' and job_status in ('ERROR','PERMANENT_FAILURE') order by id desc limit 1 ".format(
            constant.config['orgId'], messageObjId)
        result = dbHelper.queryDB(query, 'veneno')
        campaignId = None
        executionJobs = []
        if len(result) != 0:
            for execjob in result:
                executionJobs.append({'executionDateHour': execjob[1], 'cause': execjob[0]})
                campaignId = execjob[2]
        return executionJobs, campaignId

    def getMsgId(self, messageObjId):
        query = "select id,communication_type,expected_delivery_count,overall_recipient_count,state,bucket_id,UNIX_TIMESTAMP(last_updated_on),campaign_id from veneno.communication_details where org_id = {} and message_id = '{}'".format(
            constant.config['orgId'], messageObjId)
        Logger.log(query)
        result = dbHelper.queryDB(query, 'veneno')
        if len(result) != 0:
            result = result[0]
            return {'id': result[0], 'communication_type': result[1], 'expected_delivery_count': result[2],
                    'overall_recipient_count': result[3], 'state': result[4], 'bucket_id': result[5],
                    'executionDateHour': result[6], 'campaignId': result[7]}
        else:
            return self.getExecutionJobStatus(messageObjId)


class emailTrack():
    def waitForCommunicationDetailsToBeCreated(self, messageId):
        query = 'select id,communication_type from communication_details where org_id = {} and message_id= "{}"'.format(
            constant.config['orgId'], messageId)
        for numberOfTries in range(10):
            result = dbHelper.queryDB(query, 'veneno')
            if len(result) > 0: break
            time.sleep(10)

    def getMessageBody(self, messageId):
        self.waitForCommunicationDetailsToBeCreated(messageId)
        query = 'select id,message_body,state from communication_details where org_id = {} and message_id= "{}"'.format(
            constant.config['orgId'], messageId)
        for numberOfTries in range(10):
            result = dbHelper.queryDB(query, 'veneno')
            if len(result) > 0:
                if str(result[0][2]) == 'CLOSED':
                    break
            time.sleep(10)
        return result[0][1]

    def getEmailLinkRedirection(self, campaignId):
        query = 'SELECT url,id from email_links_redirection where org_id = {} and campaign_id = "{}"'.format(
            constant.config['orgId'], campaignId)
        result = dbHelper.queryDB(query, 'msging')
        return result
