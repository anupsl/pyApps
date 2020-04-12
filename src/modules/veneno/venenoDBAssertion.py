import json
import re
import time

from src.Constant.constant import constant
from src.modules.iris.dbCallsAuthorize import dbCallsAuthorize
from src.modules.iris.dbCallsList import dbCallsList
from src.modules.nsadmin.nsadminThrift import NSAdminThrift
from src.utilities.assertion import Assertion
from src.utilities.logger import Logger


class VenenoDBAssertion():
    def __init__(self, campaignId, channel, communicationDetailId, numberOfUsersSent, groupVersionId, messageBody,
                 testControlType='org', skippedReasons=[],cguhVerfiy=False):
        Logger.log(
            "Veneno DB Assertion Initialized for Details : campaignId :{} , channel :{} , communicationDetailId :{}, numberOfUsersSent :{} , groupVersionId :{} , messageBody:{} , testControlType:{} ,skippedReasons :{}".format(
                campaignId, channel, communicationDetailId, numberOfUsersSent, groupVersionId, messageBody,
                testControlType, skippedReasons))
        self.campaignId = campaignId
        self.groupVersionId = groupVersionId
        self.channel = channel
        self.numberOfUsers = numberOfUsersSent
        self.numberOfSkippedUsers = 0
        self.numberOfNsadminUsers = 0
        self.messageBody = messageBody
        self.skippedReason = skippedReasons
        self.communicationDetailId = communicationDetailId
        self.testControlType = testControlType
        self.ratio = 90
        self.cguhVerfiy = cguhVerfiy
        self.sleepAsPerChannel()
        self.getDbInformationForVeneno()
        if not self.initFailureForStickyList : return
        self.getDbInformationForVenenoDataDetails()
        self.reachabilityCheckDone = True if self.checkReachabilityCalculated() else  False
        if self.channel.lower() == 'email':
            reasonToSkip = ['user email is not whitelisted','Captured email whitelisting status is invalid','Captured email not satisfying reachability rules','Unable to determine WL status']
            self.skippedReason = self.skippedReason +reasonToSkip
        self.computeTestControlUsers()
        self.sortReachableFromControlUser()
        self.hashLookUpString = {
            'sms': 'INSTORE__DEFAULT__MOBILE',
            'email': 'INSTORE__DEFAULT__EMAIL'
        }

    def assertionInitCheck(self):
        try:
            if dbCallsAuthorize.getListType(self.groupVersionId) == 'ORG_USERS':
                return True
            else:
                return False
        except Exception,exp:
            Logger.log('Exception While Computing List Type {}'.format(exp))
            return False

    def sleepAsPerChannel(self):
        if self.channel.lower() in ['sms', 'email']: time.sleep(2)
        if self.channel.lower() in ['wechat', 'push', 'call_task', 'line']: time.sleep(5)

    def getDbInformationForVeneno(self):
        self.communicationDetailResult = dbCallsAuthorize.getCommunicationDetailsWithId(self.communicationDetailId)
        if self.communicationDetailResult['expected_delivery_count'] == 0 and self.assertionInitCheck():
            Logger.log('Aborting the Case')
            self.initFailureForStickyList = False
            return False
        else:
            self.initFailureForStickyList = True
            Assertion.constructAssertion(self.communicationDetailResult['expected_delivery_count'] != 0,
                                         'Veneno not able processed because Expected Delivery Count is : {}'.format(
                                             self.communicationDetailResult['expected_delivery_count']))
        self.serviceDetailResult = dbCallsAuthorize.getServiceDetails(self.communicationDetailId,
                                                                      self.communicationDetailResult[
                                                                          'expected_delivery_count'])
        self.venenoBatchDetailResult = dbCallsAuthorize.getVenenoBatchDetail(self.communicationDetailId)
        self.summaryReportVeneno = dbCallsAuthorize.getSummaryReportVeneno(self.communicationDetailId)
        self.summaryReportNsadmin = dbCallsAuthorize.getSummaryReportNsadmin(self.communicationDetailId)

    def checkReachabilityCalculated(self):
        try:
            return bool(json.loads(self.communicationDetailResult['default_arguments'])['is_list_processed_for_reachability'])
        except:
            return True

    def getDbInformationForVenenoDataDetails(self):
        self.inboxes = dbCallsAuthorize.getInboxDetail(self.communicationDetailResult['bucket_id'],
                                                       self.communicationDetailId)
        self.skipped = dbCallsAuthorize.getSkippedDetail(self.communicationDetailResult['bucket_id'],
                                                         self.communicationDetailId)

    def computeTestControlUsers(self):
        self.numberOfControlUsers = 0
        self.controlUsers = []
        self.testUsers = []
        self.groupVersionResult = dbCallsList.getGroupVersionDetailWithGroupVersionId(self.groupVersionId)

        if self.testControlType == 'org':
            self.paramsOfGroupVersion = json.loads(self.groupVersionResult['params'])
            self.numberOfUsers = len(dbCallsList.getUsersFromCampaignGroupRecipient(self.groupVersionResult['bucket_id'],
                                                                                    self.groupVersionId,self.channel, testControl=1,reachabilityCalculated=self.reachabilityCheckDone))

            self.controlUsers = dbCallsList.getUsersFromCampaignGroupRecipient(self.groupVersionResult['bucket_id'],
                                                           self.groupVersionId,self.channel, testControl=0,reachabilityCalculated=self.reachabilityCheckDone)
            if self.channel.lower() == 'email':
                numberOfInvalidControlUsers = dbCallsList.getInvalidUsersFromDarknight(dbCallsList.getEmailListFromUserId(self.controlUsers))
                self.numberOfControlUsers = len(self.controlUsers) -numberOfInvalidControlUsers
            else:
                self.numberOfControlUsers = len(self.controlUsers)
        elif self.testControlType == 'custom':
            listOfUsers = dbCallsList.getUsersFromCampaignGroupRecipient(self.groupVersionResult['bucket_id'],
                                                                         self.groupVersionId,self.channel,reachabilityCalculated=self.reachabilityCheckDone)
            bound = (self.ratio * 128) / 100
            key = self.randomize(int(self.campaignId))
            for eachuser in listOfUsers:
                significant_bit = eachuser & 127
                significant_bit = self.randomize(significant_bit)
                bucket_position_of_input = (significant_bit ^ key) & 127
                if bucket_position_of_input > bound:
                    Logger.log('userid :{} is counted as Control'.format(eachuser))
                    self.controlUsers.append(eachuser)
                    self.numberOfControlUsers = self.numberOfControlUsers + 1
                else:
                    self.testUsers.append(eachuser)
                    Logger.log('userid :{} is counted as Test'.format(eachuser))
            self.numberOfUsers = len(self.testUsers)
            if self.channel.lower() == 'email':
                numberOfInvalidControlUsers = dbCallsList.getInvalidUsersFromDarknight(dbCallsList.getEmailListFromUserId(self.controlUsers))
                self.numberOfControlUsers = len(self.controlUsers) -numberOfInvalidControlUsers
            else:
                self.numberOfControlUsers = len(self.controlUsers)
        elif self.testControlType =='skip':
            listOfUsers = dbCallsList.getUsersFromCampaignGroupRecipient(self.groupVersionResult['bucket_id'],
                                                                         self.groupVersionId,self.channel,
                                                                         reachabilityCalculated=self.reachabilityCheckDone)
            self.numberOfUsers = len(listOfUsers)
            self.numberOfControlUsers = 0
        Logger.log('Number Of Test Users :{} and control :{} after Calculation'.format(self.numberOfUsers,
                                                                                           self.numberOfControlUsers))

    def randomize(self, key):
        return (key ^ (key << 5) ^ (key << 2))

    def sortReachableFromControlUser(self):
        pass

    def check(self):
        self.assertVenenoTables()
        self.assertVenenoDataDetailsTables()
        self.assertCampaignGroupUserHistory(self.cguhVerfiy)
        if self.channel not in ['CALL_TASK']: self.assertDeliveryStatus()

    def assertVenenoTables(self):
        self.assertVeneno_communicationDetails()
        if self.channel == 'WECHAT':
            self.assertVeneno_WechatDetails()
        else:
            self.assertVeneno_serviceDetails()
        self.assertVeneno_batchDetails()
        self.assertVeneno_summaryVeneno()
        self.assertVeneno_summaryNsadmin()

    def assertVenenoDataDetailsTables(self):
        self.assertVenenoDataDetails_inboxes()
        self.assertVenenoDataDetails_skipped()

    def assertVeneno_communicationDetails(self):
        Assertion.constructAssertion(self.communicationDetailResult['communication_type'] == self.channel,
                                     'Communication Type in CD :{} and in Message payload :{}'.format(
                                         self.communicationDetailResult['communication_type'], self.channel))
        Assertion.constructAssertion(self.communicationDetailResult['state'] == 'CLOSED',
                                     'State of Communication Details is :{}'.format(
                                         self.communicationDetailResult['state']))

        Assertion.constructAssertion(self.communicationDetailResult[
                                         'overall_recipient_count'] == self.groupVersionResult['customer_count'],
                                     'Overall Count in CD :{} and in GroupVersion is :{}'.format(
                                         self.communicationDetailResult['overall_recipient_count'],
                                         self.groupVersionResult['customer_count']))

        Assertion.constructAssertion(self.communicationDetailResult['expected_delivery_count'] == self.numberOfUsers,
                                     'Expected Count in CD :{} and in GroupVersion is :{}'.format(
                                         self.communicationDetailResult['expected_delivery_count'], self.numberOfUsers))
        Assertion.constructAssertion(self.communicationDetailResult['recipient_list_id'] == self.groupVersionId,
                                     'Recipient List id in CD :{} and in GroupVersionDetails :{}'.format(
                                         self.communicationDetailResult['recipient_list_id'], self.groupVersionId))
        if self.channel != 'WECHAT': Assertion.constructAssertion(
            self.communicationDetailResult['message_body'] == self.messageBody,
            'Payload in CD :{} and in Create message Payload :{}'.format(self.communicationDetailResult['message_body'],
                                                                         self.messageBody))


    def assertVeneno_serviceDetails(self):
        Assertion.constructAssertion(len(self.serviceDetailResult) >= 3,
                                     'Matching Length Of Service Details greater than 3')
        Assertion.constructAssertion(
            self.serviceDetailResult['DELIVERY_SERVER']['processed_count'] == self.numberOfUsers,
            'Processed Count in DeliveryServer :{} and total numberOfUsers :{}'.format(
                self.serviceDetailResult['DELIVERY_SERVER']['processed_count'], self.numberOfUsers))
        Assertion.constructAssertion(self.serviceDetailResult['DELIVERY_SERVER']['message_version'] == 0,
                                     'Message Version Id : {} for DELIVERY_SERVER'.format(
                                         self.serviceDetailResult['DELIVERY_SERVER']['message_version']))
        Assertion.constructAssertion(self.serviceDetailResult['FEEDER']['processed_count'] == self.numberOfUsers,
                                     'Processed Count in FEEDER :{} and total numberOfUsers :{}'.format(
                                         self.serviceDetailResult['FEEDER']['processed_count'], self.numberOfUsers))
        Assertion.constructAssertion(self.serviceDetailResult['FEEDER']['message_version'] == 0,
                                     'Message Version Id : {} for FEEDER'.format(
                                         self.serviceDetailResult['FEEDER']['message_version']))
        if 'SKIPPED' in self.serviceDetailResult and 'NSADMIN' in self.serviceDetailResult:
            self.numberOfSkippedUsers = self.serviceDetailResult['SKIPPED']['processed_count']
            self.numberOfNsadminUsers = self.serviceDetailResult['NSADMIN']['processed_count']
            Assertion.constructAssertion(self.numberOfSkippedUsers + self.numberOfNsadminUsers == self.numberOfUsers,
                                         'Both NSADMIN and SKIPPED entry Found in Service Details and Addition of Processed Count in Both :{} and totalNumberOfUsers :{}'.format(
                                             self.numberOfSkippedUsers + self.numberOfNsadminUsers, self.numberOfUsers))
            Assertion.constructAssertion(self.serviceDetailResult['SKIPPED']['message_version'] == 0,
                                         'Message Version Id : {} for SKIPPED'.format(
                                             self.serviceDetailResult['SKIPPED']['message_version']))
            Assertion.constructAssertion(self.serviceDetailResult['NSADMIN']['message_version'] == 0,
                                         'Message Version Id : {} for NSADMIN'.format(
                                             self.serviceDetailResult['NSADMIN']['message_version']))
        elif 'SKIPPED' in self.serviceDetailResult and 'CALL_TASK' in self.serviceDetailResult:
            self.numberOfSkippedUsers = self.serviceDetailResult['SKIPPED']['processed_count']
            self.numberOfNsadminUsers = self.serviceDetailResult['CALL_TASK']['processed_count']
            Assertion.constructAssertion(self.numberOfSkippedUsers + self.numberOfNsadminUsers == self.numberOfUsers,
                                         'Both CALL_TASK and SKIPPED entry Found in Service Details and Addition of Processed Count in Both :{} and totalNumberOfUsers :{}'.format(
                                             self.numberOfSkippedUsers + self.numberOfNsadminUsers, self.numberOfUsers))
            Assertion.constructAssertion(self.serviceDetailResult['SKIPPED']['message_version'] == 0,
                                         'Message Version Id : {} for SKIPPED'.format(
                                             self.serviceDetailResult['SKIPPED']['message_version']))
            Assertion.constructAssertion(self.serviceDetailResult['CALL_TASK']['message_version'] == 0,
                                         'Message Version Id : {} for CALL_TASK'.format(
                                             self.serviceDetailResult['CALL_TASK']['message_version']))
        elif 'SKIPPED' in self.serviceDetailResult:
            self.numberOfSkippedUsers = self.serviceDetailResult['SKIPPED']['processed_count']
            self.numberOfNsadminUsers = 0
            Assertion.constructAssertion(self.numberOfSkippedUsers == self.numberOfUsers,
                                         'All Users Got Skipped, Matching proceesed Count For Skipped :{} and numberOfUsers :{}'.format(
                                             self.numberOfSkippedUsers, self.numberOfUsers))
            Assertion.constructAssertion(self.serviceDetailResult['SKIPPED']['message_version'] == 0,
                                         'Message Version Id : {} for SKIPPED'.format(
                                             self.serviceDetailResult['SKIPPED']['message_version']))
        elif 'NSADMIN' in self.serviceDetailResult:
            self.numberOfNsadminUsers = self.serviceDetailResult['NSADMIN']['processed_count']
            self.numberOfSkippedUsers = 0
            Assertion.constructAssertion(self.numberOfNsadminUsers == self.numberOfUsers,
                                         'All Users Went To Nsadmin, Matching proceesed Count For Msadmin :{} and numberOfUsers :{}'.format(
                                             self.numberOfNsadminUsers, self.numberOfUsers))
            Assertion.constructAssertion(self.serviceDetailResult['NSADMIN']['message_version'] == 0,
                                         'Message Version Id : {} for NSADMIN'.format(
                                             self.serviceDetailResult['NSADMIN']['message_version']))
        elif 'CALL_TASK' in self.serviceDetailResult:
            self.numberOfNsadminUsers = self.serviceDetailResult['CALL_TASK']['processed_count']
            self.numberOfSkippedUsers = 0
            Assertion.constructAssertion(self.numberOfNsadminUsers == self.numberOfUsers,
                                         'All Users Went To CALL_TASK, Matching proceesed Count For CALL_TASK :{} and numberOfUsers :{}'.format(
                                             self.numberOfNsadminUsers, self.numberOfUsers))
            Assertion.constructAssertion(self.serviceDetailResult['CALL_TASK']['message_version'] == 0,
                                         'Message Version Id : {} for CALL_TASK'.format(
                                             self.serviceDetailResult['CALL_TASK']['message_version']))

    def assertVeneno_batchDetails(self):
        if 'FEEDER' not in self.venenoBatchDetailResult and 'TAG_RESOLVER' not in self.venenoBatchDetailResult and 'DELIVERY_SERVER' not in self.venenoBatchDetailResult:
            Assertion.constructAssertion(False,
                                         'Batch Type [FEEDER,TAG_RESOLVER,DELIVERY_SERVER] Not Found in serviceDetails Result')
        if self.numberOfNsadminUsers > 0:
            if self.channel == 'CALL_TASK':
                Logger.log('Asserting Only INBOX_CONSUMER is case of Call Task')
                Assertion.constructAssertion('INBOX_CONSUMER' in self.venenoBatchDetailResult,
                                             'Batch Type [INBOX_CONSUMER] check in serviceDetails Result as batchType NSADMIN is present in Service Details and Entries are also there is entry for users in Inboxes Veneno_data_details')
            else:
                Assertion.constructAssertion('INBOX_CONSUMER' in self.venenoBatchDetailResult,
                                             'Batch Type [INBOX_CONSUMER] present in VenenoBatchDetails')
                Assertion.constructAssertion('NSADMIN_SERVER' not in self.venenoBatchDetailResult,
                                             'Batch Type [NSADMIN_SERVER] not in Veneno_batch_details')
        for eachBatchDetails in self.venenoBatchDetailResult:
            Assertion.constructAssertion(self.venenoBatchDetailResult[eachBatchDetails]['message_version'] == 0,
                                         'Message Version for Batch :{} is :{}'.format(eachBatchDetails,
                                                                                       self.venenoBatchDetailResult[
                                                                                           eachBatchDetails][
                                                                                           'message_version']))
            Assertion.constructAssertion(self.venenoBatchDetailResult[eachBatchDetails]['status'] == 'CLOSED',
                                         'Status Of Batch :{} is :{}'.format(eachBatchDetails,
                                                                             self.venenoBatchDetailResult[
                                                                                 eachBatchDetails]['status']))

    def assertVeneno_summaryVeneno(self):
        if self.numberOfSkippedUsers > 0:
            countOfSkippedUsers = 0
            for eachSubType in self.summaryReportVeneno:
                Assertion.constructAssertion(eachSubType != 'NSADMIN_FAILED',
                                             'NSADMIN FAILED Got Observed in Summary Report Veneno Table')
                countOfSkippedUsers = countOfSkippedUsers + int(self.summaryReportVeneno[eachSubType]['count'])
            Assertion.constructAssertion(self.numberOfSkippedUsers == countOfSkippedUsers,
                                         'Matching Number of Skipped Users in ServiceDetails :{} and in summaryVeneno :{}'.format(
                                             self.numberOfSkippedUsers, countOfSkippedUsers))
        else:
            Logger.log('Nothing to Assert in Summary Report Veneno as no user got Skipped')
        for eachSubType in self.summaryReportVeneno:
            Assertion.constructAssertion(self.summaryReportVeneno[eachSubType]['message_version'] == 0,
                                         'Message Version for Batch :{} is :{}'.format(eachSubType,
                                                                                       self.summaryReportVeneno[
                                                                                           eachSubType][
                                                                                           'message_version']))

    def assertVeneno_summaryNsadmin(self):
        if self.numberOfNsadminUsers > 0:
            totalCountInTable = 0
            for eachDeliveryId in self.summaryReportNsadmin:
                totalCountInTable = totalCountInTable + int(self.summaryReportNsadmin[eachDeliveryId]['count'])
            Assertion.constructAssertion(int(self.numberOfNsadminUsers) == totalCountInTable,
                                         'NumberOfTestUsers :{} and count in SummaryReportNsadmin is :{}'.format(
                                             self.numberOfNsadminUsers, totalCountInTable))
        else:
            Logger.log('Nothing To Assert in Summary Report NSADMIN as all users skipped')

    def assertVeneno_WechatDetails(self):
        Assertion.constructAssertion(len(self.serviceDetailResult) >= 2,
                                     'Matching Length Of Service Details greater than 2')
        Assertion.constructAssertion(
            self.serviceDetailResult['DELIVERY_SERVER']['processed_count'] == self.numberOfUsers,
            'Processed Count in DeliveryServer :{} and total numberOfUsers :{}'.format(
                self.serviceDetailResult['DELIVERY_SERVER']['processed_count'], self.numberOfUsers))
        Assertion.constructAssertion(self.serviceDetailResult['FEEDER']['processed_count'] == self.numberOfUsers,
                                     'Processed Count in DeliveryServer :{} and total numberOfUsers :{}'.format(
                                         self.serviceDetailResult['FEEDER']['processed_count'], self.numberOfUsers))
        Assertion.constructAssertion(self.serviceDetailResult['DELIVERY_SERVER']['message_version'] == 0,
                                     'Message Version Id : {} for DELIVERY_SERVER'.format(
                                         self.serviceDetailResult['DELIVERY_SERVER']['message_version']))
        Assertion.constructAssertion(self.serviceDetailResult['FEEDER']['message_version'] == 0,
                                     'Message Version Id : {} for FEEDER'.format(
                                         self.serviceDetailResult['FEEDER']['message_version']))
        if 'SKIPPED' in self.serviceDetailResult:
            self.numberOfSkippedUsers = self.serviceDetailResult['SKIPPED']['processed_count']
            self.numberOfNsadminUsers = self.serviceDetailResult['DELIVERY_SERVER']['processed_count'] - \
                                        self.serviceDetailResult['SKIPPED']['processed_count']
        else:
            self.numberOfNsadminUsers = self.serviceDetailResult['DELIVERY_SERVER']['processed_count']
            self.numberOfSkippedUsers = 0

    def assertVenenoDataDetails_inboxes(self):
        if self.numberOfNsadminUsers > 0:
            listOfAllTagsInMessageBody = re.findall(r"\{{(.*?)\}}", self.messageBody)
            if 'optout' in listOfAllTagsInMessageBody: listOfAllTagsInMessageBody.remove('optout')
            for eachuser in self.inboxes:
                self.ResolvedTagsForEachUser(self.inboxes[eachuser]['id'], self.inboxes[eachuser]['resolved_tags'],
                                             listOfAllTagsInMessageBody)
        else:
            Logger.log('No Assertion in Inboxes as all user got Skipped')

    def ResolvedTagsForEachUser(self, userId, resolvedTags, listOfAllTagsInMessageBody):
        Logger.log('List of All tags In Message :{}'.format(listOfAllTagsInMessageBody))
        for eachTag in listOfAllTagsInMessageBody:
            if len(eachTag) <= 20: Assertion.constructAssertion(eachTag in resolvedTags,
                                                                'Checking Tag :{} which we passed in message Body in Resolved Tags :{} For UserId:{}'.format(
                                                                    eachTag, resolvedTags, userId))

    def assertVenenoDataDetails_skipped(self):
        if self.numberOfSkippedUsers > 0:
            for eachUserId in self.skipped:
                Assertion.constructAssertion(self.skipped[eachUserId]['error_description'] in self.skippedReason,
                                             'Skipped Reason :{}  matched'.format(
                                                 self.skipped[eachUserId]['error_description']))
                Assertion.constructAssertion(self.skipped[eachUserId]['message_version'] == 0,
                                             'Skipped message_version : {}  matched'.format(
                                                 self.skipped[eachUserId]['message_version']))

    def assertDeliveryStatus(self):
        Logger.log('Checking Delivery Status From NSADMIN')
        for eachUser in self.inboxes:
            Logger.log('Checking For NSADMIN id :{}'.format(self.inboxes[eachUser]['nsadmin_id']))
            nsadminIdOfUser = self.inboxes[eachUser]['nsadmin_id']
            nsadminInstance = NSAdminThrift(constant.config['nsMasterPort'])
            status = nsadminInstance.getMessagesById([nsadminIdOfUser])[0].status
            if self.channel.lower() == 'push':
                Assertion.constructAssertion(status in ['SENT', 'DELIVERED', 'NOT_DELIVERED', 'RECEIVED_IN_QUEUE'],
                                             'Status of Message is :{} for nsadmin id :{}'.format(status,
                                                                                                  nsadminIdOfUser))
            else:
                Assertion.constructAssertion(status in ['SENT', 'DELIVERED', 'FAILED', 'RECEIVED_IN_QUEUE'],
                                             'Status of Message is :{} for nsadmin id :{}'.format(status,
                                                                                                  nsadminIdOfUser),verify=True)

    def assertCampaignGroupUserHistory(self,verify=False):
        if self.numberOfControlUsers ==0 : return
        if self.channel.lower() == 'email': verify=True
        if self.channel.lower() in self.hashLookUpString:
            usersInCGUH = dbCallsAuthorize.getUserFromCGUH(self.campaignId, self.communicationDetailResult['id'])
            if self.testControlType == 'org':
                hashLookupDetails = dbCallsList.getHashLookUp()
                hashLookupGettingUsedAsPerChannel = self.hashLookUpString[self.channel.lower()]
                controlUsersInGroup = dbCallsList.getContorlUsersFromCGR(
                    dbCallsList.getGroupVersionDetailWithGroupVersionId(self.groupVersionId)['bucket_id'],
                    self.groupVersionId, hashLookupDetails[hashLookupGettingUsedAsPerChannel])
                for eachReacabilityStatusId in controlUsersInGroup:
                    if dbCallsList.getReachabilityStatus(eachReacabilityStatusId) in ['SUBSCRIBED', None, 'None']:
                        for eachSubscribedUser in controlUsersInGroup[eachReacabilityStatusId]:
                            Assertion.constructAssertion(eachSubscribedUser in usersInCGUH,
                                                         'User :{} is reachable and Control and present in :{}'.format(
                                                             eachSubscribedUser, usersInCGUH),verify=verify)
                    else:
                        for eachSubscribedUser in controlUsersInGroup[eachReacabilityStatusId]:
                            Assertion.constructAssertion(eachSubscribedUser not in usersInCGUH,
                                                         'User :{} is not reachable but Control and not present in :{}'.format(
                                                             eachSubscribedUser, usersInCGUH),verify=verify)
            if self.testControlType == 'custom':
                for eachUser in self.controlUsers:
                    Assertion.constructAssertion(eachUser in usersInCGUH,
                                                 'User :{} is control and in CGUH :{}'.format(eachUser, usersInCGUH),verify=verify)
            elif self.testControlType == 'skip':
                controlUsersInGroup = []
                Assertion.constructAssertion(len(usersInCGUH) == 0,
                                             'Due to testControl Type :{} , usersInCGUH :{}'.format(
                                                 self.testControlType, usersInCGUH))
        else:
            Logger.log("No Check in CHUG due to No infomration of hashLookup ")
