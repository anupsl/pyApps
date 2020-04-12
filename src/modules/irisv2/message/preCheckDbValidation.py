import time

from src.dbCalls.messageInfo import message_calls
from src.dbCalls.messageInfo import message_info
from src.dbCalls.preCheck import precheck_calls
from src.utilities.assertion import Assertion
from src.utilities.logger import Logger


class PreCheckDBValidation():
    def __init__(self, campaignId, messageId, messageType, cronStatus, messageVersion=0, remindCheck=True,
                 executeCheck=True, variantCheck=True, basicCheckStatus=None,
                 basicRecurringCheck=None, reloadCheck=None, precheck=None, basicExecuteCheck=None, cdDetail=None,
                 messageStatus_remind=None, messageStatus_execute=None, variantStatus='SUCCESS', messageDBDetails=None,
                 byPassPrecheckValidation=False):
        Logger.log(
            'Initializing Precheck Validation for campaign Id :{} and MessageId :{}'.format(campaignId, messageId))
        self.campaignId = campaignId
        self.messageID = messageId
        self.messageType = messageType
        self.cronStatus = cronStatus
        self.version = messageVersion
        self.remindCheck = remindCheck
        self.executeCheck = executeCheck
        self.variantCheck = variantCheck
        self.basicCheckStatus = basicCheckStatus
        self.basicRecurringCheck = basicRecurringCheck
        self.reloadCheck = reloadCheck
        self.precheck = precheck
        self.basicExecuteCheck = basicExecuteCheck
        self.cdDetail = cdDetail
        self.messageStatus_remind = messageStatus_remind
        self.messageStatus_execute = messageStatus_execute
        self.varaintStatus = variantStatus
        self.messageDbDetails = messageDBDetails
        self.byPassPrecheckValidation = byPassPrecheckValidation

    def validateMessageFlow(self):
        self.getMessageDBDetails()
        CronValidator(self.messageDbDetails, self.cronStatus).validateCronInfo()
        if self.remindCheck: ReminderValidator(self.campaignId, self.messageID, self.messageType,
                                               basicCheckStatus=self.basicCheckStatus,
                                               reloadCheck=self.reloadCheck,
                                               precheck=self.precheck,
                                               messageStatus=self.messageStatus_remind,
                                               byPassPrecheckValidation=self.byPassPrecheckValidation).validate()
        if self.executeCheck: ExecutionValidator(self.campaignId, self.messageID, self.messageType,
                                                 basicExecuteCheck=self.basicExecuteCheck,
                                                 basicRecurringCheck=self.basicRecurringCheck,
                                                 precheck=self.precheck, cdDetail=self.cdDetail,
                                                 messageStatus_execute=self.messageStatus_execute).validate()
        if self.variantCheck: self.validateVariantStatus()

    def getMessageDBDetails(self):
        self.messageDbDetails = message_info(self.messageID,
                                             version=self.version).messageDbDetail if self.messageDbDetails is None else self.messageDbDetails

    def validateVariantStatus(self):
        dictOfVariantsInDB = precheck_calls().getVariantExecutionStatus(self.campaignId, self.messageID)
        for eachJobDetails in self.messageDbDetails['messageJobDetails_collection']['VARIANT_CREATION']:
            for varient in eachJobDetails['variant_detail']:
                Assertion.constructAssertion(varient['_id'] in dictOfVariantsInDB,
                                             'Varient ID :{} found in PrecheckVariantStatus DB :{}'.format(
                                                 varient['_id'], dictOfVariantsInDB))
                Assertion.constructAssertion(dictOfVariantsInDB[varient['_id']] == self.varaintStatus,
                                             'For VariantId :{} , status :{} and expected :{}'.format(varient['_id'],
                                                                                                      dictOfVariantsInDB[
                                                                                                          varient[
                                                                                                              '_id']],
                                                                                                      self.varaintStatus))


class CronValidator():
    def __init__(self, messageDBDetails, cronStatus):
        Logger.log('Initializing Cron Validation with CronStatus :{}'.format(cronStatus))
        self.cronStatus = cronStatus
        self.messageDBDetails = messageDBDetails

    def getCronInfoWithVariants(self):
        mapOfVariantWithCron = dict()
        for eachJobDetails in self.messageDBDetails['messageJobDetails_collection']['VARIANT_CREATION']:
            for varient in eachJobDetails['variant_detail']:
                cronInfo = message_calls().getCronIdWithVariantId(varient['_id'], self.cronStatus)
                if cronInfo is None: raise Exception('NoCronEntryFoundForVariantId :{}'.format(varient))
                mapOfVariantWithCron.update({varient['_id']: cronInfo})
        return mapOfVariantWithCron

    def validateCronInfo(self):
        mapOfVariantWithCron = self.getCronInfoWithVariants()
        Logger.log('MapOfVariantWithStatus :{}'.format(mapOfVariantWithCron))
        for eachVariant in mapOfVariantWithCron:
            if mapOfVariantWithCron[eachVariant] is None:
                Assertion.addValidationMessage('For VariantId :{} cronInfo not Found'.format(eachVariant))

            Assertion.constructAssertion(mapOfVariantWithCron[eachVariant]['status'] in self.cronStatus,
                                         'Actual CronStatus is {} for varient :{} and expected :{}'.format(
                                             mapOfVariantWithCron[eachVariant]['status'], eachVariant, self.cronStatus))


class ReminderValidator():
    def __init__(self, campaignId, messageId, messageType, basicCheckStatus=None,
                 reloadCheck=None, precheck=None, messageStatus=None, byPassPrecheckValidation=False):
        Logger.log('Remnder Validation Initialized with campaignId :{} and MessageId :{}'.format(campaignId, messageId))
        self.campaignId = campaignId
        self.messageId = messageId
        self.messageType = messageType
        self.byPassPrecheckValidation = byPassPrecheckValidation
        self.basicCheckStatus = 'SUCCESS' if basicCheckStatus is None else basicCheckStatus
        self.reloadCheck = {'GROUP_RELOAD_NFS': 'SUCCESS',
                            'GROUP_RELOAD_CREATE_AUDIENCE': 'SUCCESS'} if reloadCheck is None else reloadCheck
        self.precheck = {'status': 'SUCCESS', 'errorDescription': None} if precheck is None else precheck
        self.messageStatus = 'SUCCESS' if messageStatus is None else messageStatus

    def validate(self):
        self.validateBasicCheck()
        if self.messageType.upper() == 'RECURRING':
            self.validateAudienceGroupReload()
        if self.messageType.upper() != 'IMMEDIATE': self.validatePrecheck()

    def validateBasicCheck(self):
        basicRemindCheck = precheck_calls('REMIND').getJobDetailFromPreExecutionJobStatus(self.campaignId,
                                                                                          self.messageId,
                                                                                          'BASIC_REMIND_CHECKS')
        Assertion.constructAssertion(basicRemindCheck['job_status'] == self.basicCheckStatus,
                                     'For BasicCheck actual Status :{} and expected Status :{}'.format(
                                         basicRemindCheck['job_status'], self.basicCheckStatus))

    def validateAudienceGroupReload(self):
        for eachJobType in ['GROUP_RELOAD_NFS', 'GROUP_RELOAD_CREATE_AUDIENCE']:
            reloadCheck = precheck_calls('REMIND').getJobDetailFromPreExecutionJobStatus(self.campaignId,
                                                                                         self.messageId,
                                                                                         eachJobType)
            Assertion.constructAssertion(reloadCheck['job_status'] == self.reloadCheck[eachJobType],
                                         'For ReloadCheck actual Status :{} and expected Status :{}'.format(
                                             reloadCheck['job_status'], self.reloadCheck[eachJobType]))

    def validatePrecheck(self):
        if self.byPassPrecheckValidation: return
        preCheck = precheck_calls('REMIND').getJobDetailFromPreExecutionJobStatus(self.campaignId, self.messageId,
                                                                                  'PRECHECK')
        Assertion.constructAssertion(preCheck['job_status'] == self.precheck['status'],
                                     'For precheck actual Status :{} and expected Status :{}'.format(
                                         preCheck['job_status'], self.precheck['status']))

        if self.precheck['errorDescription'] is not None:
            Assertion.constructAssertion(sorted(preCheck['error_description'].split(',')) == sorted(
                self.precheck['errorDescription'].split(',')),
                                         'For precheck actual errorDescription :{} and expected Status :{}'.format(
                                             preCheck['error_description'], self.precheck['errorDescription']))

    def validateMessageStatus(self):
        eventStatus = precheck_calls('REMIND').getMsgDetailFromPreExecutionMessageStatus(self.campaignId,
                                                                                         self.messageId,
                                                                                         'REMIND')
        Assertion.constructAssertion(eventStatus['status'] == self.messageStatus,
                                     'For Event REMIND in preCheckMessageStatus status is :{} and expected is :{}'.format(
                                         eventStatus['status'], self.messageStatus))


class ExecutionValidator():
    def __init__(self, campaignId, messageId, messageType, basicExecuteCheck=None, precheck=None, cdDetail=None,
                 basicRecurringCheck=None, messageStatus_execute=None):
        Logger.log(
            'Execution Validator Initialized with campaignId :{} and MessageId :{}'.format(campaignId, messageId))
        self.campaignId = campaignId
        self.messageId = messageId
        self.messageType = messageType
        self.basicRecurringCheck = 'SUCCESS' if basicRecurringCheck is None else basicRecurringCheck
        self.basicExecuteCheck = 'SUCCESS' if basicExecuteCheck is None else basicExecuteCheck
        self.precheck = {'status': 'SUCCESS', 'errorDescription': None} if precheck is None else precheck
        self.cdDetail = 'SUCCESS' if cdDetail is None else cdDetail
        self.messageStatus = 'SUCCESS' if messageStatus_execute is None else messageStatus_execute

    def validate(self):
        self.validateBasicExecuteCheck()
        if self.messageType.upper() == 'RECURRING':
            self.validateBasicRecurringCheck()
        if self.messageType.upper() == 'IMMEDIATE':
            self.validatePrecheck()
        if self.precheck['status'] == 'SUCCESS': self.validateCommunicationDetailsCreation()

    def validateBasicExecuteCheck(self):
        basicExecuteCheck = precheck_calls('EXECUTE').getJobDetailFromPreExecutionJobStatus(self.campaignId,
                                                                                            self.messageId,
                                                                                            'BASIC_EXECUTE_CHECKS')
        Assertion.constructAssertion(basicExecuteCheck['job_status'] == self.basicExecuteCheck,
                                     'For BasicCheck actual Status :{} and expected Status :{}'.format(
                                         basicExecuteCheck['job_status'], self.basicExecuteCheck))

    def validatePrecheck(self):
        preCheck = precheck_calls('EXECUTE').getJobDetailFromPreExecutionJobStatus(self.campaignId, self.messageId,
                                                                                   'PRECHECK')
        Assertion.constructAssertion(preCheck['job_status'] == self.precheck['status'],
                                     'For precheck actual Status :{} and expected Status :{}'.format(
                                         preCheck['job_status'], self.precheck['status']))
        if self.precheck['errorDescription'] is not None:
            Assertion.constructAssertion(sorted(preCheck['error_description'].split(',')) == sorted(
                self.precheck['errorDescription'].split(',')),
                                         'For precheck actual errorDescription :{} and expected Status :{}'.format(
                                             preCheck['error_description'], self.precheck['errorDescription']))

    def validateCommunicationDetailsCreation(self):
        cdDetail = precheck_calls('EXECUTE').getJobDetailFromPreExecutionJobStatus(self.campaignId, self.messageId,
                                                                                   'COMMUNICATION_DETAIL_CREATION')
        Assertion.constructAssertion(cdDetail['job_status'] == self.cdDetail,
                                     'For BasicCheck actual Status :{} and expected Status :{}'.format(
                                         cdDetail['job_status'], self.cdDetail))

    def validateMessageStatus(self):
        eventStatus = precheck_calls('EXECUTE').getMsgDetailFromPreExecutionMessageStatus(self.campaignId,
                                                                                          self.messageId,
                                                                                          'EXECUTE')
        Assertion.constructAssertion(eventStatus['status'] == self.messageStatus,
                                     'For Event EXECUTE in preCheckMessageStatus status is :{} and expected is :{}'.format(
                                         eventStatus['status'], self.messageStatus))

    def validateBasicRecurringCheck(self):
        basicRecurringCheck = precheck_calls('EXECUTE').getJobDetailFromPreExecutionJobStatus(self.campaignId,
                                                                                              self.messageId,
                                                                                              'RECURRING_CHECKS')
        Assertion.constructAssertion(basicRecurringCheck['job_status'] == self.basicRecurringCheck,
                                     'For BasicRecurringCheck actual Status :{} and expected Status :{}'.format(
                                         basicRecurringCheck['job_status'], self.basicRecurringCheck))


class Precheck_calls():
    def waitForJobTypeUpdate(self, campaignId, messageId, event, job, expectedStatus, expectedError=None):
        for _ in range(30):
            jobDetail = precheck_calls(event).getJobDetailFromPreExecutionJobStatus(campaignId, messageId, job)
            status = jobDetail['job_status']
            error = jobDetail['error_description']
            if status == expectedStatus:
                if expectedError is None:
                    break
                elif expectedError == error:
                    break
                else:
                    time.sleep(10)
            else:
                time.sleep(10)
