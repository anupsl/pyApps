import inspect
import json

from src.Constant.constant import constant
from src.dbCalls.messageInfo import message_calls
from src.dbCalls.messageInfo import message_info
from src.dbCalls.messageInfo import pointsMetaInfo
from src.utilities.assertion import Assertion
from src.utilities.logger import Logger



class CreateMessageDBAssertion():
    def __init__(self, campaignId, messageId, payload, offer=False, draft=False, approved='CREATED', numberOfVariant=1,
                 messageCollection=True,
                 messageJobDetailsCollection=True, messageVariantsCollection=True, getAllTest=False, stickyList=False,
                 cronPattern=None, reject=False, messageSchedulerState='START', version=0):
        Logger.log('Called Method Name: ', inspect.stack()[1][3].lower())
        self.campaignId = campaignId
        self.messageId = messageId
        self.payload = payload
        self.offer = offer
        self.draft = draft
        self.approved = approved
        self.numberOfVariant = numberOfVariant
        self.messageCollection = messageCollection
        self.messageJobDetailsCollection = messageJobDetailsCollection
        self.messageVariantsCollection = messageVariantsCollection
        self.getAllTest = getAllTest
        self.stickyList = stickyList
        self.reject = reject
        self.cronPattern = cronPattern
        self.version = version
        self.messageSchedulerState = messageSchedulerState
        if 'sticky' in inspect.stack()[1][3].lower():
            self.stickyList = True
        self.messageDbDetail = message_info(self.messageId, messageCollection, messageJobDetailsCollection,
                                            messageVariantsCollection, version=version).messageDbDetail

    def check(self):
        self.validateMessageCollection()
        self.validateMessageJobDetailCollection()
        self.validateAuditLogs()
        if self.version > 0:
            mapOfVersions = message_calls().getMapOfVersions(self.messageId,self.version)
            self.validateOlderVersionsMarkedAsInactive(mapOfVersions)
            self.validateNumberOfInactiveVersions()

    def validateMessageCollection(self):
        self.validateBasicInfo()
        self.validateDeliverySetting()
        self.validateMessageContent()
        self.validateSchedule()
        self.validateStrategy()
        self.validateTargetAudience()

    def validateMessageJobDetailCollection(self):
        for eachEntity in ['VARIANT_CREATION', 'MESSAGE_TARGET_AUDIENCE']:
            Assertion.constructAssertion(eachEntity in self.messageDbDetail['messageJobDetails_collection'],
                                         '{} : found in Job Details'.format(eachEntity))
        self.validateJobDetailsForTargetAudience()
        self.actualTargetAudience = self.validateJobDetailsForJobContextInTargetAudience()
        self.validateJobDetailsForVariants()

    def validateOlderVersionsMarkedAsInactive(self,mapOfVersions):
        for version in range(self.version):
            listOfActiveStatus = message_calls().getVariantStatusByMessageId(self.messageId, version=mapOfVersions[version])
            for eachStatus in listOfActiveStatus:
                Assertion.constructAssertion(eachStatus['active'] == False,
                                             'Active Marked in Variant as :{}'.format(eachStatus['active']),verify=True)
                if eachStatus['cronTaskId'] != 0:
                    cronDetail = message_calls().getCronDetails(eachStatus['cronTaskId'])
                    Assertion.constructAssertion(cronDetail['status'] == 'CLOSED',
                                                 'For Older Version of Message where active is :{}, cron Detail have Status :{} and Expected is CLOSED'.format(
                                                     eachStatus['active'], cronDetail['status']),verify=True)

    def validateNumberOfInactiveVersions(self):
        numberOfInactiveVariant = message_calls().getNUmberOfInactiveVariantForMessage(self.messageId)
        Assertion.constructAssertion(numberOfInactiveVariant == self.version,
                                     'Latest Version :{} and numberOfInactiveVersions are :{}'.format(self.version,
                                                                                                      numberOfInactiveVariant),verify=True)

    def validateAuditLogs(self):
        auditTrialDetails, auditTrialTrackedItem, auditTrialTrackedClass = message_calls().getAuditDetails(
            self.messageId)
        if auditTrialDetails is None:
            Assertion.constructAssertion(False,
                                         'No Entry Found in Audit Logs for message Id :{}'.format(self.messageId))
        else:
            auditTrialDetails = json.loads(auditTrialDetails)
            Assertion.constructAssertion(auditTrialTrackedItem == self.messageId,
                                         'For MessageID :{} and Tracked item :{}'.format(self.messageId,
                                                                                         auditTrialTrackedItem))
            Assertion.constructAssertion(auditTrialTrackedClass == 'MessageEntity',
                                         'Tracked Class is  :{}'.format(auditTrialTrackedClass))
            for eachKey in ['orgId', 'campaignId', 'name', 'type']:
                Assertion.constructAssertion(eachKey in auditTrialDetails, 'Key :{} in Audit Trial'.format(eachKey))
                Assertion.constructAssertion(
                    auditTrialDetails[eachKey] == self.messageDbDetail['message_collection'][eachKey],
                    'Audit Log Value of :{} in details :{} and in Mongo :{}'.format(eachKey, auditTrialDetails[eachKey],
                                                                                    self.messageDbDetail[
                                                                                        'message_collection'][eachKey]))
            for eachKey in ['targetAudience', 'strategy', 'messageContent', 'schedule', 'deliverySetting']:
                Assertion.constructAssertion(eachKey in auditTrialDetails, 'Key :{} in Audit Trial'.format(eachKey))

    def validateSchedule(self):
        Assertion.constructAssertion(
            self.messageDbDetail['message_collection']['schedule']['type'] == self.payload['schedule']['scheduleType'],
            'Schedule used in DB :{} and in payoad :{}'.format(
                self.messageDbDetail['message_collection']['schedule']['type'],
                self.payload['schedule']['scheduleType']))
        if self.payload['schedule']['scheduleType'] != 'IMMEDIATE':
            Assertion.constructAssertion(False, 'For Schedulle Type {}, no assertion defined'.format(
                self.payload['schedule']['scheduleType']), verify=True)

    def validateStrategy(self):
        Assertion.constructAssertion(
            self.messageDbDetail['message_collection']['strategy']['type'] == self.payload['messageStrategy']['type'],
            'Strategy used in DB :{} and in payoad :{}'.format(
                self.messageDbDetail['message_collection']['strategy']['type'],
                self.payload['messageStrategy']['type']))

    def validateTargetAudience(self):
        if 'include' in self.payload['targetAudience']: Assertion.constructAssertion(
            sorted(map(int, self.messageDbDetail['message_collection']['targetAudience']['include'])) == sorted(
                map(int, self.payload['targetAudience']['include'])
            ),
            'Target Audience Includes  in DB :{} and expected :{}'.format(
                self.messageDbDetail['message_collection']['targetAudience']['include'],
                self.payload['targetAudience']['include']))
        if 'exclude' in self.payload['targetAudience']: Assertion.constructAssertion(
            sorted(map(int, self.messageDbDetail['message_collection']['targetAudience']['exclude'])) == sorted(
                map(int, self.payload['targetAudience']['exclude'])
            ),
            'Target Audience Includes  in DB :{} and expected :{}'.format(
                self.messageDbDetail['message_collection']['targetAudience']['exclude'],
                self.payload['targetAudience']['exclude']))

    def validateMessageContent(self):
        for eachContent in self.payload['messageContent']:
            Assertion.constructAssertion(eachContent in self.messageDbDetail['message_collection']['messageContent'],
                                         'Content Name : {} found in DB '.format(eachContent))
            if self.messageDbDetail['message_collection']['messageContent'][eachContent]['channel'] == 'SMS':
                Assertion.constructAssertion(
                    self.messageDbDetail['message_collection']['messageContent'][eachContent]['messageBody'] ==
                    self.payload['messageContent'][eachContent]['messageBody'],
                    'Message Body in Db :{} and in payload passed :{}'.format(
                        self.messageDbDetail['message_collection']['messageContent'][eachContent]['messageBody'],
                        self.payload['messageContent'][eachContent]['messageBody']))

                Assertion.constructAssertion(
                    self.messageDbDetail['message_collection']['messageContent'][eachContent]['channel'] ==
                    self.payload['messageContent'][eachContent]['channel'],
                    'Channel Saved in Db :{} and in payload passed :{}'.format(
                        self.messageDbDetail['message_collection']['messageContent'][eachContent]['channel'],
                        self.payload['messageContent'][eachContent]['channel']))
            elif self.messageDbDetail['message_collection']['messageContent'][eachContent]['channel'] == 'EMAIL':
                Assertion.constructAssertion(
                    self.messageDbDetail['message_collection']['messageContent'][eachContent]['emailSubject'] ==
                    self.payload['messageContent'][eachContent]['emailSubject'],
                    'Message Subject in Db :{} and in payload passed :{}'.format(
                        self.messageDbDetail['message_collection']['messageContent'][eachContent]['emailSubject'],
                        self.payload['messageContent'][eachContent]['emailSubject']))

                Assertion.constructAssertion(
                    self.messageDbDetail['message_collection']['messageContent'][eachContent]['emailBody'] ==
                    self.payload['messageContent'][eachContent]['emailBody'],
                    'emailBody Saved in Db :{} and in payload passed :{}'.format(
                        self.messageDbDetail['message_collection']['messageContent'][eachContent]['emailBody'],
                        self.payload['messageContent'][eachContent]['emailBody']))

            if self.offer:
                offer_DB = self.messageDbDetail['message_collection']['messageContent'][eachContent]['offers'][0]
                offer_Payload = self.payload['messageContent'][eachContent]['offers'][0]
                for each in offer_Payload:
                    if each in offer_DB:
                        Assertion.constructAssertion(offer_Payload[each] == offer_DB[each],
                                                     'Offer Key in Payload Passed :{} and in DB :{}'.format(
                                                         offer_Payload[each], offer_DB[each]))
                    else:
                        if each == 'program':
                            Logger.log('Checking for programe')
                            response_programDescription = offer_Payload['program']
                            db_programeDescription = pointsMetaInfo().pointsMeta
                            db_programeDescription[response_programDescription['programId']].pop('tiers')
                            Assertion.constructAssertion(response_programDescription == db_programeDescription[
                                response_programDescription['programId']],
                                                         'From Response Programe Info :{} and in DB :{}'.format(
                                                             response_programDescription, db_programeDescription[
                                                                 response_programDescription['programId']]),
                                                         verify=True)
                        else:
                            Assertion.constructAssertion(False,
                                                         'Offer Validation : Key ->{} is not Present in DB'.format(
                                                             each),
                                                         verify=True)

    def validateDeliverySetting(self):
        for eachSetting in self.payload['deliverySetting']:
            Assertion.constructAssertion(eachSetting in self.messageDbDetail['message_collection']['deliverySetting'],
                                         'Setting :{} found in Db'.format(eachSetting))
            try:
                if eachSetting == 'additionalSetting':
                    Assertion.constructAssertion(
                        self.messageDbDetail['message_collection']['deliverySetting'][eachSetting]['useTinyUrl'] ==
                        self.payload['deliverySetting'][eachSetting]['useTinyUrl'],
                        'UseTinyURL in DB :{} and in payload passed as :{}'.format(
                            self.messageDbDetail['message_collection']['deliverySetting'][eachSetting]['useTinyUrl'],
                            self.payload['deliverySetting'][eachSetting]['useTinyUrl']))

                    Assertion.constructAssertion(
                        self.messageDbDetail['message_collection']['deliverySetting'][eachSetting]['encryptUrl'] ==
                        self.payload['deliverySetting'][eachSetting]['encryptUrl'],
                        'encryptUrl in DB :{} and in payload passed as :{}'.format(
                            self.messageDbDetail['message_collection']['deliverySetting'][eachSetting]['encryptUrl'],
                            self.payload['deliverySetting'][eachSetting]['encryptUrl']))

                    Assertion.constructAssertion(
                        self.messageDbDetail['message_collection']['deliverySetting'][eachSetting]['skipRateLimit'] ==
                        self.payload['deliverySetting'][eachSetting]['skipRateLimit'],
                        'skipRateLimit in DB :{} and in payload passed as :{}'.format(
                            self.messageDbDetail['message_collection']['deliverySetting'][eachSetting]['skipRateLimit'],
                            self.payload['deliverySetting'][eachSetting]['skipRateLimit']))
            except AssertionError, exp:
                Assertion.constructAssertion(False, 'ADditional Setting Check Failed with Exception :{}'.format(exp))
            except Exception, exp:
                Logger.log('While Checking Additional Setting Exception caught as :{}'.format(exp))

            if eachSetting == 'channelSetting':
                if 'SMS' in self.messageDbDetail['message_collection']['deliverySetting'][eachSetting]:
                    Assertion.constructAssertion(
                        self.messageDbDetail['message_collection']['deliverySetting'][eachSetting]['SMS'][
                            'gsmSenderId'] ==
                        self.payload['deliverySetting'][eachSetting]['SMS']['gsmSenderId'],
                        'gsmSenderId in DB :{} and in payload passed as :{}'.format(
                            self.messageDbDetail['message_collection']['deliverySetting'][eachSetting]['SMS'][
                                'gsmSenderId'],
                            self.payload['deliverySetting'][eachSetting]['SMS']['gsmSenderId']))

                    Assertion.constructAssertion(
                        self.messageDbDetail['message_collection']['deliverySetting'][eachSetting]['SMS'][
                            'targetNdnc'] ==
                        self.payload['deliverySetting'][eachSetting]['SMS']['targetNdnc'],
                        'targetNdnc in DB :{} and in payload passed as :{}'.format(
                            self.messageDbDetail['message_collection']['deliverySetting'][eachSetting]['SMS'][
                                'targetNdnc'],
                            self.payload['deliverySetting'][eachSetting]['SMS']['targetNdnc']))

                    Assertion.constructAssertion(
                        self.messageDbDetail['message_collection']['deliverySetting'][eachSetting]['SMS'][
                            'cdmaSenderId'] ==
                        self.payload['deliverySetting'][eachSetting]['SMS']['cdmaSenderId'],
                        'cdmaSenderId in DB :{} and in payload passed as :{}'.format(
                            self.messageDbDetail['message_collection']['deliverySetting'][eachSetting]['SMS'][
                                'cdmaSenderId'],
                            self.payload['deliverySetting'][eachSetting]['SMS']['cdmaSenderId']))

                    Assertion.constructAssertion(
                        self.messageDbDetail['message_collection']['deliverySetting'][eachSetting]['SMS'][
                            'channel'] ==
                        self.payload['deliverySetting'][eachSetting]['SMS']['channel'],
                        'channel in DB :{} and in payload passed as :{}'.format(
                            self.messageDbDetail['message_collection']['deliverySetting'][eachSetting]['SMS'][
                                'channel'],
                            self.payload['deliverySetting'][eachSetting]['SMS']['channel']))
                if 'EMAIL' in self.messageDbDetail['message_collection']['deliverySetting'][eachSetting]:
                    Assertion.constructAssertion(
                        self.messageDbDetail['message_collection']['deliverySetting'][eachSetting]['EMAIL'][
                            'senderReplyTo'] ==
                        self.payload['deliverySetting'][eachSetting]['EMAIL']['senderReplyTo'],
                        'senderReplyTo in DB :{} and in payload passed as :{}'.format(
                            self.messageDbDetail['message_collection']['deliverySetting'][eachSetting]['EMAIL'][
                                'senderReplyTo'],
                            self.payload['deliverySetting'][eachSetting]['EMAIL']['senderReplyTo']))

                    Assertion.constructAssertion(
                        self.messageDbDetail['message_collection']['deliverySetting'][eachSetting]['EMAIL'][
                            'senderLabel'] ==
                        self.payload['deliverySetting'][eachSetting]['EMAIL']['senderLabel'],
                        'senderLabel in DB :{} and in payload passed as :{}'.format(
                            self.messageDbDetail['message_collection']['deliverySetting'][eachSetting]['EMAIL'][
                                'senderLabel'],
                            self.payload['deliverySetting'][eachSetting]['EMAIL']['senderLabel']))

                    Assertion.constructAssertion(
                        self.messageDbDetail['message_collection']['deliverySetting'][eachSetting]['EMAIL'][
                            'senderEmail'] ==
                        self.payload['deliverySetting'][eachSetting]['EMAIL']['senderEmail'],
                        'senderEmail in DB :{} and in payload passed as :{}'.format(
                            self.messageDbDetail['message_collection']['deliverySetting'][eachSetting]['EMAIL'][
                                'senderEmail'],
                            self.payload['deliverySetting'][eachSetting]['EMAIL']['senderEmail']))

                    Assertion.constructAssertion(
                        self.messageDbDetail['message_collection']['deliverySetting'][eachSetting]['EMAIL'][
                            'channel'] ==
                        self.payload['deliverySetting'][eachSetting]['EMAIL']['channel'],
                        'channel in DB :{} and in payload passed as :{}'.format(
                            self.messageDbDetail['message_collection']['deliverySetting'][eachSetting]['EMAIL'][
                                'channel'],
                            self.payload['deliverySetting'][eachSetting]['EMAIL']['channel']))

    def validateBasicInfo(self):
        Assertion.constructAssertion(self.messageDbDetail['message_collection']['_id'] == self.messageId,
                                     'Message Id in DB :{} and expected :{}'.format(
                                         self.messageDbDetail['message_collection']['_id'], self.messageId))

        Assertion.constructAssertion(self.messageDbDetail['message_collection']['campaignId'] == self.campaignId,
                                     'campaignId  in DB :{} and expected :{}'.format(
                                         self.messageDbDetail['message_collection']['campaignId'], self.campaignId))

        Assertion.constructAssertion(self.messageDbDetail['message_collection']['name'] == self.payload['name'],
                                     'Name  in DB :{} and expected :{}'.format(
                                         self.messageDbDetail['message_collection']['name'], self.payload['name']))

        Assertion.constructAssertion(self.messageDbDetail['message_collection']['orgId'] == constant.config['orgId'],
                                     'OrgId  in DB :{} and expected :{}'.format(
                                         self.messageDbDetail['message_collection']['orgId'], constant.config['orgId']))

        Assertion.constructAssertion(self.messageDbDetail['message_collection']['orgUnitId'] == -1,
                                     'orgUnitId  in DB :{} and expected :{}'.format(
                                         self.messageDbDetail['message_collection']['orgUnitId'], -1))

        Assertion.constructAssertion(
            str(self.messageDbDetail['message_collection']['createdBy']) == str(constant.config['userId']),
            'createdBy  in DB :{} and expected :{}'.format(
                self.messageDbDetail['message_collection']['createdBy'], constant.config['userId']))

        # Assertion.constructAssertion(self.messageDbDetail['message_collection']['draft'] == self.draft,
        #                              'Draft  in DB :{} and expected :{}'.format(
        #                                  self.messageDbDetail['message_collection']['draft'], self.draft))

        Assertion.constructAssertion(self.messageDbDetail['message_collection']['type'] == self.payload['type'],
                                     'type  in DB :{} and expected :{}'.format(
                                         self.messageDbDetail['message_collection']['type'], self.payload['type']))
        if not self.getAllTest:
            Assertion.constructAssertion(self.messageDbDetail['message_collection']['state'] == self.approved,
                                         'approved  in DB :{} and expected :{}'.format(
                                             self.messageDbDetail['message_collection']['state'], self.approved))

    def validateJobDetailsForTargetAudience(self):
        Assertion.constructAssertion(
            self.messageDbDetail['messageJobDetails_collection']['MESSAGE_TARGET_AUDIENCE'][0]['_id'] is not None,
            '_id in DB :{} Found'.format(
                self.messageDbDetail['messageJobDetails_collection']['MESSAGE_TARGET_AUDIENCE'][0]['_id']))

        Assertion.constructAssertion(
            self.messageDbDetail['messageJobDetails_collection']['MESSAGE_TARGET_AUDIENCE'][0]['status'] == 'CLOSED',
            'Status Of target Audience is :{} and Expected is : CLOSED'.format(
                self.messageDbDetail['messageJobDetails_collection']['MESSAGE_TARGET_AUDIENCE'][0]['status']))

        Assertion.constructAssertion(
            self.messageDbDetail['messageJobDetails_collection']['MESSAGE_TARGET_AUDIENCE'][0][
                'campaignId'] == self.campaignId,
            'CampaignId in DB :{} and Expected :{}'.format(
                self.messageDbDetail['messageJobDetails_collection']['MESSAGE_TARGET_AUDIENCE'][0]['campaignId'],
                self.campaignId))

        Assertion.constructAssertion(
            self.messageDbDetail['messageJobDetails_collection']['MESSAGE_TARGET_AUDIENCE'][0]['orgId'] ==
            constant.config[
                'orgId'],
            'OrgId in DB :{} and Expected :{}'.format(
                self.messageDbDetail['messageJobDetails_collection']['MESSAGE_TARGET_AUDIENCE'][0]['orgId'],
                constant.config['orgId']))

        Assertion.constructAssertion(
            str(self.messageDbDetail['messageJobDetails_collection']['MESSAGE_TARGET_AUDIENCE'][0]['createdBy']) ==
            str(constant.config['userId']),
            'createdBy in DB :{} and Expected :{}'.format(
                self.messageDbDetail['messageJobDetails_collection']['MESSAGE_TARGET_AUDIENCE'][0]['createdBy'],
                constant.config['userId']))

        Assertion.constructAssertion(
            self.messageDbDetail['messageJobDetails_collection']['MESSAGE_TARGET_AUDIENCE'][0]['reTryCount'] == 0,
            'reTryCount in DB :{} and Expected :{}'.format(
                self.messageDbDetail['messageJobDetails_collection']['MESSAGE_TARGET_AUDIENCE'][0]['reTryCount'], 0),
            verify=True)

        Assertion.constructAssertion(
            self.messageDbDetail['messageJobDetails_collection']['MESSAGE_TARGET_AUDIENCE'][0][
                'type'] == 'MESSAGE_TARGET_AUDIENCE',
            'type in DB :{} and Expected :{}'.format(
                self.messageDbDetail['messageJobDetails_collection']['MESSAGE_TARGET_AUDIENCE'][0]['type'],
                'MESSAGE_TARGET_AUDIENCE'))

    def validateJobDetailsForJobContextInTargetAudience(self):
        Assertion.constructAssertion(
            'targetAudienceId' in self.messageDbDetail['messageJobDetails_collection']['MESSAGE_TARGET_AUDIENCE'][0][
                'jobContext'], 'targetAudienceId present in jobContext')

        return self.messageDbDetail['messageJobDetails_collection']['MESSAGE_TARGET_AUDIENCE'][0][
            'jobContext']['targetAudienceId']

    def validateJobDetailsForVariants(self):
        Assertion.constructAssertion(
            len(self.messageDbDetail['messageJobDetails_collection']['VARIANT_CREATION']) == self.numberOfVariant,
            'Number Of Variants in DB :{} and expected :{}'.format(
                len(self.messageDbDetail['messageJobDetails_collection']['VARIANT_CREATION']), self.numberOfVariant))
        for eachVariant in self.messageDbDetail['messageJobDetails_collection']['VARIANT_CREATION']:
            Assertion.constructAssertion(eachVariant['status'] == 'CLOSED',
                                         'Variant Status is :{}'.format(eachVariant['status']))
            Assertion.constructAssertion(eachVariant['campaignId'] == self.campaignId,
                                         'CampaignId in DB :{} and expected :{}'.format(eachVariant['campaignId'],
                                                                                        self.campaignId))
            Assertion.constructAssertion(eachVariant['orgId'] == constant.config['orgId'],
                                         'CampaignId in DB :{} and expected :{}'.format(eachVariant['orgId'],
                                                                                        constant.config['orgId']))
            Assertion.constructAssertion(str(eachVariant['createdBy']) == str(constant.config['userId']),
                                         'createdBy in DB :{} and expected :{}'.format(eachVariant['createdBy'],
                                                                                       constant.config['userId']))
            Assertion.constructAssertion(eachVariant['messageId'] == self.messageId,
                                         'MessageId in DB :{} and expected :{}'.format(eachVariant['messageId'],
                                                                                       self.messageId))
            Assertion.constructAssertion(eachVariant['type'] == 'VARIANT_CREATION',
                                         'Variant Type in DB :{} and expected :{}'.format(eachVariant['type'],
                                                                                          'VARIANT_CREATION'))
            Assertion.constructAssertion(eachVariant['jobContext']['targetAudienceId'] == self.actualTargetAudience,
                                         'Target Audience Id For variant in db :{} and expected :{}'.format(
                                             eachVariant['jobContext']['targetAudienceId'], self.actualTargetAudience))

            for eachVariantInList in eachVariant['variant_detail']:
                self.validateVariantDetails(eachVariantInList, eachVariantInList['_id'])

    def validateVariantDetails(self, variantDetails, variantId):
        if self.payload['schedule']['scheduleType'] == 'IMMEDIATE':
            if self.messageDbDetail['message_collection']['state'] == 'REJECTED':
                Assertion.constructAssertion(variantDetails['cronTaskId'] == 0,
                                             'For Schedulle Type :{} CrontaskId :{}'.format(
                                                 self.payload['schedule']['scheduleType'],
                                                 variantDetails['cronTaskId']))
                # TODO: Message Varaint Active Should Get Mark as False
            elif self.messageDbDetail['message_collection']['state'] == 'APPROVED':
                Assertion.constructAssertion(variantDetails['cronTaskId'] != 0,
                                             'For Schedulle Type :{} CrontaskId :{}'.format(
                                                 self.payload['schedule']['scheduleType'],
                                                 variantDetails['cronTaskId']))

            else:
                Assertion.constructAssertion(variantDetails['cronTaskId'] == 0,
                                             'For Schedulle Type :{} CrontaskId :{}'.format(
                                                 self.payload['schedule']['scheduleType'],
                                                 variantDetails['cronTaskId']))
        else:
            Assertion.constructAssertion(variantDetails['cronTaskId'] != 0,
                                         'For Schedulle Type :{} CrontaskId :{}'.format(
                                             self.payload['schedule']['scheduleType'], variantDetails['cronTaskId']))
            cronDetail = message_calls().getCronDetails(variantDetails['cronTaskId'])
            if self.cronPattern is not None:
                Assertion.constructAssertion(cronDetail['cron_pattern'] == self.cronPattern,
                                             'CronPattern in DB :{} and expected :{}'.format(cronDetail['cron_pattern'],
                                                                                             self.cronPattern))
            if self.reject is not False:
                Assertion.constructAssertion(cronDetail['status'] == self.reject['status'],
                                             'Message Reject Validation , cron status in DB :{} and expected is :{}'.format(
                                                 cronDetail['status'], self.reject['status']))

        Assertion.constructAssertion(variantDetails['_id'] == variantId,
                                     'Variant Id in DB :{} and Expected :{}'.format(variantDetails['_id'], variantId))
        Assertion.constructAssertion(variantDetails['orgId'] == constant.config['orgId'],
                                     'OrgId in DB :{} and expected :{}'.format(variantDetails['orgId'],
                                                                               constant.config['orgId']))
        Assertion.constructAssertion(str(variantDetails['createdBy']) == str(constant.config['userId']),
                                     'createdBy in DB :{} and expected :{}'.format(variantDetails['createdBy'],
                                                                                   constant.config['userId']))
        Assertion.constructAssertion(variantDetails['messageId'] == self.messageId,
                                     'Message Id set in Variant is :{} and expected :{}'.format(
                                         variantDetails['messageId'], self.messageId))
        Assertion.constructAssertion(variantDetails['campaignId'] == self.campaignId,
                                     'CampaignId in Variant :{} and expected :{}'.format(variantDetails['campaignId'],
                                                                                         self.campaignId))

        if variantDetails['skipTestControl'] and self.stickyList:
            Assertion.constructAssertion(
                variantDetails['audienceId'] == int(self.payload['targetAudience']['orgUsers'][0]),
                'SkipTestControlIs True, In Variant Detail Audience Id :{} and in TargetAudience orgUsers :{}'.format(
                    variantDetails['audienceId'], self.payload['targetAudience']['orgUsers'][0]))
        else:
            Assertion.constructAssertion(variantDetails['audienceId'] == self.actualTargetAudience,
                                         'Audience Id in DB :{} and Expected :{}'.format(variantDetails['audienceId'],
                                                                                         self.actualTargetAudience))
        Assertion.constructAssertion(variantDetails['schedule']['type'] == self.payload['schedule']['scheduleType'],
                                     'Schedulle Type  in DB :{} and Expected :{}'.format(
                                         variantDetails['schedule']['type'],
                                         self.payload['schedule'][
                                             'scheduleType']))

        self.validateChannelSettinginVariant(variantDetails['channelSetting'],
                                             variantDetails['channelSetting']['channel'])

        self.validateDummyEntryInMessageQueue(variantDetails['messageVariantId'])

    def validateChannelSettinginVariant(self, channelSetting, channel):
        if channel == 'SMS':
            Assertion.constructAssertion(
                channelSetting['gsmSenderId'] ==
                self.payload['deliverySetting']['channelSetting']['SMS']['gsmSenderId'],
                'gsmSenderId in DB :{} and in payload passed as :{}'.format(channelSetting['gsmSenderId'],
                                                                            self.payload['deliverySetting'][
                                                                                'channelSetting']['SMS'][
                                                                                'gsmSenderId']))

            Assertion.constructAssertion(
                channelSetting['targetNdnc'] ==
                self.payload['deliverySetting']['channelSetting']['SMS']['targetNdnc'],
                'targetNdnc in DB :{} and in payload passed as :{}'.format(
                    channelSetting['targetNdnc'],
                    self.payload['deliverySetting']['channelSetting']['SMS']['targetNdnc']))

            Assertion.constructAssertion(
                channelSetting['cdmaSenderId'] ==
                self.payload['deliverySetting']['channelSetting']['SMS']['cdmaSenderId'],
                'cdmaSenderId in DB :{} and in payload passed as :{}'.format(
                    channelSetting['cdmaSenderId'],
                    self.payload['deliverySetting']['channelSetting']['SMS']['cdmaSenderId']))

            Assertion.constructAssertion(
                channelSetting['channel'] ==
                self.payload['deliverySetting']['channelSetting']['SMS']['channel'],
                'channel in DB :{} and in payload passed as :{}'.format(
                    channelSetting['channel'],
                    self.payload['deliverySetting']['channelSetting']['SMS']['channel']))
        if channel.upper() == 'EMAIL':
            Assertion.constructAssertion(
                channelSetting['senderReplyTo'] ==
                self.payload['deliverySetting']['channelSetting']['EMAIL']['senderReplyTo'],
                'senderReplyTo in DB :{} and in payload passed as :{}'.format(
                    channelSetting['senderReplyTo'],
                    self.payload['deliverySetting']['channelSetting']['EMAIL']['senderReplyTo']))

            Assertion.constructAssertion(
                channelSetting['senderLabel'] ==
                self.payload['deliverySetting']['channelSetting']['EMAIL']['senderLabel'],
                'senderLabel in DB :{} and in payload passed as :{}'.format(
                    channelSetting['senderLabel'],
                    self.payload['deliverySetting']['channelSetting']['EMAIL']['senderLabel']))

            Assertion.constructAssertion(
                channelSetting['senderEmail'] ==
                self.payload['deliverySetting']['channelSetting']['EMAIL']['senderEmail'],
                'senderEmail in DB :{} and in payload passed as :{}'.format(
                    channelSetting['senderEmail'],
                    self.payload['deliverySetting']['channelSetting']['EMAIL']['senderEmail']))

            Assertion.constructAssertion(
                channelSetting['channel'] ==
                self.payload['deliverySetting']['channelSetting']['EMAIL']['channel'],
                'channel in DB :{} and in payload passed as :{}'.format(
                    channelSetting['channel'],
                    self.payload['deliverySetting']['channelSetting']['EMAIL']['channel']))

    def validateDummyEntryInMessageQueue(self, messageQueueId):
        messageQueueStatus = message_calls().getStatusOfMessageQueue(messageQueueId)
        Assertion.constructAssertion(messageQueueStatus == 'MIGRATED',
                                     'Status of messageQueue Id :{}'.format(messageQueueStatus))




