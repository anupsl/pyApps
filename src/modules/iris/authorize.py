import json, time, re
from src.Constant.constant import constant
from src.utilities.logger import Logger
from src.utilities.assertion import Assertion
from src.modules.iris.construct import construct
from src.modules.iris.message import campaignMessage
from src.modules.iris.dbCallsMessage import dbCallsMessage
from src.modules.iris.dbCallsCampaign import dbCallsCampaign
from src.modules.iris.dbCallsAuthorize import dbCallsAuthorize
from src.modules.iris.dbCallsList import dbCallsList
from src.utilities.utils import Utils

class authorize():

    @staticmethod
    def authorizeCampaign(self, messageInfo, usePreCreatedMessages=False):
        if usePreCreatedMessages:
            Logger.log('Message Object Found Update so Getting Message Details To Make Authorize Request')
            messageObjectDetailsForMessageInfo = authorize.getMessageDetailsFromObject(messageInfo)
            Logger.log('Recieved Message Object :', messageObjectDetailsForMessageInfo)
            if messageObjectDetailsForMessageInfo == {} :
                Logger.log('As Message Object is Empty Creating a New Message to Authorize')
                return authorize.authorizeCampaign(self, messageInfo, False)
            authorizeResponse = authorize.makeAuthorizeRequest(messageObjectDetailsForMessageInfo['campaignId'], messageObjectDetailsForMessageInfo['messageId'])
            messageObjectDetailsForMessageInfo.update({'authorizeResponse':authorizeResponse})
            Logger.log('Authorized Succesfully and constructed MessageDefault Info Object as :', messageObjectDetailsForMessageInfo)
            return messageObjectDetailsForMessageInfo
        else:
            Logger.log('Creating a New Message And Authorizing')
            messageResponse, messagePayload = campaignMessage.createMessage(self, messageInfo=messageInfo)
            Logger.log('Message Created for Authorize with Id :{}'.format(messageResponse['json']['entity']['messageId']))
            campaignMessage.assertCreateMessage(messageResponse, 200)
            Logger.log('Making Authorize Post Request')
            authorizeResponse = authorize.makeAuthorizeRequest(str(self.campaignId), str(messageResponse['json']['entity']['messageId']))
            messageObjectDetailsForMessageInfo = {'campaignId':self.campaignId, 'listId':self.listId, 'groupVersionResult':self.groupVersionResult , 'bucketId':self.bucketId, 'voucherId':self.voucherId, 'strategy':self.strategy, 'messageInfo':messageInfo, 'payload':messagePayload, 'messageId':str(messageResponse['json']['entity']['messageId']), 'authorizeResponse':authorizeResponse}
            Logger.log('Authorized Succesfully and constructed MessageDefault Info Object as :', messageObjectDetailsForMessageInfo)
            return messageObjectDetailsForMessageInfo

    @staticmethod
    def makeAuthorizeRequest(campaignId, messageId):
        authorizeConstructedEndPoint = construct.constructUrl('authorize').replace('{campaignId}', str(campaignId)).replace('{messageId}', str(messageId))
        response = Utils.makeRequest(url=authorizeConstructedEndPoint, data='', auth=construct.constructAuthenticate(), headers=construct.constructHeaders(), method='POST')
        return construct.constructResponse(response)

    @staticmethod
    def getMessageDetailsFromObject(messageInfo):
        messageObjectDetailsForMessageInfo = {}
        Logger.log('Forming a Message Default Object , check messaage Object Detail as Pre Step')
        if not authorize.checkMessageInfoRequirementInMessageDetailJsonObject(messageInfo):
            return messageObjectDetailsForMessageInfo

        try:
            messageDetails = constant.messagesDefault[messageInfo[0]][messageInfo[1][0]][messageInfo[2][0]][messageInfo[3]]
            messageObjectDetailsForMessageInfo.update({
                'campaignId' : constant.messagesDefault['campaignId'],
                'listId' :constant.messagesDefault['listId'] ,
                'voucherId': constant.messagesDefault['voucherId'] ,
                'strategy': constant.messagesDefault['strategy'],
                'bucketId':constant.messagesDefault['bucketId'],
                'groupVersionResult':constant.messagesDefault['groupVersionResult'],
                'messageInfo': messageDetails['messageInfo'],
                'payload': messageDetails['payload'],
                'messageId': messageDetails['msgId']
                })
        except Exception, exp:
            Logger.log('Exception :{} while getting details from messageDefault Json'.format(exp))
        Logger.log('returning Message Object as :', messageObjectDetailsForMessageInfo)
        return messageObjectDetailsForMessageInfo

    @staticmethod
    def checkMessageInfoRequirementInMessageDetailJsonObject(messageInfo):
        Logger.log('Checking Message Default Value Can Be used or Not For Message Info :', messageInfo)
        if constant.messagesDefault['campaignId'] == -1 :
            Logger.log('CampaignId Not Found in Message Defaults')
            return False
        elif constant.messagesDefault['listId'] == -1 :
            Logger.log('listId Not Found in Message Defaults')
            return False
        elif constant.messagesDefault['voucherId'] == -1 :
            Logger.log('VoucherId Not Found in Message Defaults')
            return False
        elif constant.messagesDefault['strategy'] == {} :
            Logger.log('Strategy Not Found in Message Defaults')
            return False
        elif constant.messagesDefault[messageInfo[0]][messageInfo[1][0]][messageInfo[2][0]][messageInfo[3]] == {} :
            Logger.log('Message Info Found empty in Message Defaults')
            return False
        elif 'msgId' not in constant.messagesDefault[messageInfo[0]][messageInfo[1][0]][messageInfo[2][0]][messageInfo[3]] :
            Logger.log('MessageId Not Found in Message Defaults')
            return False
        elif 'messageInfo' not in constant.messagesDefault[messageInfo[0]][messageInfo[1][0]][messageInfo[2][0]][messageInfo[3]] :
            Logger.log('MessageInfo Not Found in Message Defaults')
            return False
        elif 'payload' not in constant.messagesDefault[messageInfo[0]][messageInfo[1][0]][messageInfo[2][0]][messageInfo[3]] :
            Logger.log('Message payload Not Found in Message Defaults')
            return False
        else :
            Logger.log('All Info Checked Sucessfully')
            return True

    @staticmethod
    def assertAuthorize(response, expectedStatusCode, expectedErrorCode=999999, expectedErrorMessage=''):
        Logger.log('Response sent to be asserted :', response)
        if response['constructed'].lower() == 'pass':
            if expectedStatusCode >= 200 and expectedStatusCode <= 300:
                Assertion.constructAssertion(response['statusCode'] == int(expectedStatusCode), 'Matching statusCode actual :{},expected :{}'.format(response['statusCode'], expectedStatusCode))
                if len(response['json']['warnings']) > 0:
                    Logger.log('There was a Warning while Creating Campaign :', response['json']['warning'])
            else:
                Logger.log('loop for each error')
                for errorReturned in response['json']['errors']:
                    Logger.log('Status Code :{} and error :{}', response['statusCode'], errorReturned)
                    Assertion.constructAssertion(response['statusCode'] == int(expectedStatusCode), 'Matching statusCode actual :{},expected :{}'.format(response['statusCode'], expectedStatusCode))
                    Assertion.constructAssertion(errorReturned['code'] == expectedErrorCode, 'Matching Error Code ,actual:{} and expected:{}'.format(errorReturned['code'], expectedErrorCode))
                    Assertion.constructAssertion(errorReturned['status'] == False, 'Checking for Error Status as False')
                    Assertion.constructAssertion(errorReturned['message'] in expectedErrorMessage, 'Matching Error Message ,actual:{} and expected'.format(errorReturned['message'], expectedErrorMessage))
        else:
            Assertion.constructAssertion(False, 'Constructed Body has Failed due to Exception so no Validation')

    @staticmethod
    def assertMessageQueueAndGetCommunicationDetailsForReferenceMessageQueueId(campaignId,groupVersionId,messageId):
        messageQueueDetails = dbCallsMessage.getMessageQueueFromMessageId(messageId)
        Logger.log('Message Queue Validation Started with MessageQueueDetails as:', messageQueueDetails)
        Assertion.constructAssertion(str(messageQueueDetails['Approved']) == '1', 'Approved in Message Queue :{} and Expecting :1'.format(messageQueueDetails['Approved']),verify=True)
        Assertion.constructAssertion(messageQueueDetails['status'] == 'SENT', 'Status in Message Queue :{} and expected is : SENT'.format(messageQueueDetails['status']))
        communicationDetails = dbCallsAuthorize.getCommunicationDetails(campaignId, groupVersionId, messageQueueDetails['guid'])
        Assertion.constructAssertion(int(communicationDetails['message_queue_id'])==int(messageId),'Communication Details id of Message Queue :{} and in communicationDetails :{}'.format(messageId,communicationDetails['message_queue_id']))
        return communicationDetails['id'],communicationDetails['bucket_id'],communicationDetails['expected_delivery_count']
    
    @staticmethod
    def dbAssertAuthorize(messageObjectDetailsForMessageInfo, checkSkippedUsers=False, errorType=99999, errorDescription='', healthDashboardCheck=True):
        Logger.log('Validatng Message Queue and Communication Details with Message Information :', messageObjectDetailsForMessageInfo)
        messageQueueGuid = authorize.dbAssertAuthorize_MessageQueue(messageObjectDetailsForMessageInfo)
        communicationDetailId, communicationDetailBucketId = authorize.dbAssertAuthorize_CommunicationDetail(messageObjectDetailsForMessageInfo, messageQueueGuid, checkSkippedUsers, errorType, errorDescription)
        authorize.dbAssertAuthorize_bulk_sms_campaign(messageObjectDetailsForMessageInfo['campaignId'], messageObjectDetailsForMessageInfo['messageId'])
        if healthDashboardCheck : authorize.dbAssertAuthorize_HealthDashboardNotification(messageObjectDetailsForMessageInfo['campaignId'], channel=messageObjectDetailsForMessageInfo['payload']['channel'])
        return communicationDetailId, communicationDetailBucketId

    @staticmethod
    def dbAssertAuthorize_MessageQueue(messageObjectDetail):
        messageQueueDetails = dbCallsMessage.getMessageQueueFromMessageId(messageObjectDetail['messageId'])
        Logger.log('Message Queue Validation Started with MessageQueueDetails as:', messageQueueDetails)
        Assertion.constructAssertion(str(messageQueueDetails['Approved']) == '1', 'Approved in Message Queue :{} and Expecting :1'.format(messageQueueDetails['Approved']))
        if messageObjectDetail['payload']['schedule']['type'] is 'IMMEDIATELY' :
            Assertion.constructAssertion(messageQueueDetails['status'] == 'SENT', 'Status in Message Queue :{} and expected is : SENT'.format(messageQueueDetails['status']))
        else:
            Assertion.constructAssertion(messageQueueDetails['status'] == 'OPEN', 'Status in Message Queue :{} and expected is : OPEN'.format(messageQueueDetails['status']))
        return messageQueueDetails['guid']

    @staticmethod
    def dbAssertAuthorize_CommunicationDetail(messageObjectDetail, messageQueueGuid, checkSkippedUsers, errorType, errorDescription):
        nonImmediate = False
        if messageObjectDetail['payload']['schedule']['type'] is not 'IMMEDIATELY':
            nonImmediate = True
        channelTypeMapping = {'sms':'mobile', 'email':'email'}
        communicationDetails = dbCallsAuthorize.getCommunicationDetails(messageObjectDetail['campaignId'], messageObjectDetail['groupVersionResult']['TEST']['id'], messageQueueGuid , nonImmediate)
        Logger.log('Veneno DB  Validation Started with CommunicationDetail Information as:', communicationDetails)
        Assertion.constructAssertion(str(messageObjectDetail['messageId']) == str(communicationDetails['message_queue_id']), 'Message Queue Id :{} and in CD message_queue_id :{}'.format(messageObjectDetail['messageId'], communicationDetails['message_queue_id']))
        Assertion.constructAssertion(communicationDetails['expected_delivery_count'] != 0, 'Veneno not able processed because Expected Delivery Count is : {}'.format(communicationDetails['expected_delivery_count']))
        authorize.assertCommunicationDetail(communicationDetails, messageObjectDetail['groupVersionResult'], messageObjectDetail['payload'])
        batchTypeNSAdminPresent = authorize.assertServiceDetails(communicationDetails['id'], communicationDetails['bucket_id'], messageObjectDetail['payload'], json.loads(messageObjectDetail['groupVersionResult']['TEST']['params'])[channelTypeMapping[communicationDetails['communication_type'].lower()]], checkSkippedUsers, errorType, errorDescription)
        authorize.assertVenenoBatchDetails(communicationDetails['id'], batchTypeNSAdminPresent)
        return communicationDetails['id'], communicationDetails['bucket_id']

    @staticmethod
    def assertCommunicationDetail(communicationDetails, groupVersionResult, messagePayload):
        Logger.log('Validating Communication Details with CD Result:{} and GroupVersionResult:{} and Message payload:{}'.format(communicationDetails, groupVersionResult, messagePayload))
        Assertion.constructAssertion(communicationDetails['communication_type'] == messagePayload['channel'], 'Communication Type in CD :{} and in Message payload :{}'.format(communicationDetails['communication_type'], messagePayload['channel']))
        Assertion.constructAssertion(communicationDetails['state'] == 'CLOSED', 'State of Communication Details is :{}'.format(communicationDetails['state']))
        Assertion.constructAssertion(int(communicationDetails['overall_recipient_count']) == int(groupVersionResult['TEST']['customer_count']), 'Overall Count in CD :{} and in GroupVersion is :'.format(communicationDetails['overall_recipient_count'], groupVersionResult['TEST']['customer_count']))
        if messagePayload['channel'].lower() == 'sms' : Assertion.constructAssertion(int(communicationDetails['expected_delivery_count']) == int(json.loads(groupVersionResult['TEST']['params'])['mobile']), 'Overall Count in CD :{} and in GroupVersion is :'.format(communicationDetails['overall_recipient_count'], int(json.loads(groupVersionResult['TEST']['params'])['mobile'])))
        if messagePayload['channel'].lower() == 'email' : Assertion.constructAssertion(int(communicationDetails['expected_delivery_count']) == int(json.loads(groupVersionResult['TEST']['params'])['email']), 'Overall Count in CD :{} and in GroupVersion is :'.format(communicationDetails['overall_recipient_count'], int(json.loads(groupVersionResult['TEST']['params'])['email'])))
        Assertion.constructAssertion(int(communicationDetails['recipient_list_id']) == int(groupVersionResult['TEST']['id']), 'Recipient List id in CD :{} and in GroupVersionDetails :{}'.format(communicationDetails['recipient_list_id'], groupVersionResult['TEST']['id']))
        Assertion.constructAssertion(communicationDetails['message_body'] == messagePayload['message'], 'Payload in CD :{} and in Create message Payload :{}'.format(communicationDetails['message_body'] , messagePayload['message']))

    @staticmethod
    def assertServiceDetails(msgId, bucketId, messagePayload, numberOfTestUsers, checkSkippedUsers, errorType, errorDescription):
        BatchTypeNSAdminPresent = True
        serviceDetails = dbCallsAuthorize.getServiceDetails(msgId, numberOfTestUsers)
        Logger.log('Validating Service Details with Information :', serviceDetails)
        Assertion.constructAssertion(len(serviceDetails) >= 3, 'Validating length of Service Details is greater than or Equal To 3')
        if 'DELIVERY_SERVER' not in serviceDetails and 'FEEDER' not in serviceDetails and 'NSADMIN' not in serviceDetails:
            Assertion.constructAssertion(False, 'All Batch Type [DELIVERY_SERVER,FEEDER,NSADMIN] Not Found in serviceDetails Result')
        Assertion.constructAssertion(int(serviceDetails['DELIVERY_SERVER']['processed_count']) == int(numberOfTestUsers) , 'Processed Count is :{} and numberOftestUsers :{}'.format(serviceDetails['DELIVERY_SERVER'], numberOfTestUsers))
        Assertion.constructAssertion(serviceDetails['DELIVERY_SERVER']['message_version'] == 0, 'Message Version Id : {} for DELIVERY_SERVER'.format(serviceDetails['DELIVERY_SERVER']['message_version']))
        Assertion.constructAssertion(int(serviceDetails['FEEDER']['processed_count']) == int(numberOfTestUsers) , 'Processed Count is :{} and numberOftestUsers :{}'.format(serviceDetails['FEEDER'], numberOfTestUsers))
        Assertion.constructAssertion(serviceDetails['FEEDER']['message_version'] == 0, 'Message Version Id : {} for FEEDER'.format(serviceDetails['FEEDER']['message_version']))
        if 'SKIPPED' in serviceDetails :
            totalProcessedCount = int(serviceDetails['SKIPPED']['processed_count'])
            Assertion.constructAssertion(serviceDetails['SKIPPED']['message_version'] == 0, 'Message Version Id : {} for SKIPPED'.format(serviceDetails['SKIPPED']['message_version']))
            if 'NSADMIN' in serviceDetails :
                totalProcessedCount = totalProcessedCount + int(serviceDetails['NSADMIN']['processed_count'])
                Assertion.constructAssertion(serviceDetails['NSADMIN']['message_version'] == 0, 'Message Version Id : {} for NSADMIN'.format(serviceDetails['NSADMIN']['message_version']))
                authorize.dbAssertAuthorize_VenenoDataDetails(bucketId, msgId, messagePayload['message'], checkSkippedUsers=checkSkippedUsers, errorType=errorType, errorDescription=errorDescription)
            else:
                BatchTypeNSAdminPresent = False
                Assertion.constructAssertion(False, 'All Users are Skipped , No NSADMIN Entry Found in Service Details', verify=True)
            authorize.dbAssertAuthorize_VenenoDataDetails(bucketId, msgId, messagePayload['message'], table='skipped', checkSkippedUsers=checkSkippedUsers, errorType=errorType, errorDescription=errorDescription)
            Assertion.constructAssertion(totalProcessedCount == int(numberOfTestUsers) , 'Processed Count of NSADMIN and SKIPPED:{} and numberOftestUsers :{}'.format(totalProcessedCount, numberOfTestUsers))
            authorize.assertSummaryReportVeneno(msgId, serviceDetails['SKIPPED']['processed_count'])
        else:
            Assertion.constructAssertion(int(serviceDetails['NSADMIN']['processed_count']) == int(numberOfTestUsers) , 'Processed Count is :{} and numberOftestUsers :{}'.format(serviceDetails['NSADMIN'], numberOfTestUsers))
            Assertion.constructAssertion(serviceDetails['NSADMIN']['message_version'] == 0, 'Message Version Id : {} for NSADMIN'.format(serviceDetails['NSADMIN']['message_version']))
            authorize.dbAssertAuthorize_VenenoDataDetails(bucketId, msgId, messagePayload['message'], checkSkippedUsers=checkSkippedUsers, errorType=errorType, errorDescription=errorDescription)
            authorize.assertSummaryReportNsadmin(msgId, serviceDetails['NSADMIN']['processed_count'])
        return BatchTypeNSAdminPresent

    @staticmethod
    def assertVenenoBatchDetails(msgId, batchTypeNSAdminPresent):
        venenoBatchDetail = dbCallsAuthorize.getVenenoBatchDetail(msgId)
        Logger.log('Validating Veneno Batch Details with Information :', venenoBatchDetail)
        Assertion.constructAssertion(len(venenoBatchDetail) >= 3, 'Validating Length of venenoBatchDetails is 5')
        if 'FEEDER' not in venenoBatchDetail and 'TAG_RESOLVER' not in venenoBatchDetail and 'DELIVERY_SERVER' not in venenoBatchDetail :
            Assertion.constructAssertion(False, 'Batch Type [FEEDER,TAG_RESOLVER,DELIVERY_SERVER] Not Found in serviceDetails Result')
        if batchTypeNSAdminPresent :
            Assertion.constructAssertion('INBOX_CONSUMER' in venenoBatchDetail , 'Batch Type [INBOX_CONSUMER] check in venenoBatchDetails ')
            Assertion.constructAssertion('NSADMIN_SERVER' not in venenoBatchDetail, 'Batch Type NSADMIN_SERVER not in venenoBatchDetails')

        for eachbatchType in venenoBatchDetail:
            Assertion.constructAssertion(venenoBatchDetail[eachbatchType]['status'] == 'CLOSED', 'Status is :{} for batchType:{}'.format(venenoBatchDetail[eachbatchType]['status'], eachbatchType))
            Assertion.constructAssertion(venenoBatchDetail[eachbatchType]['message_version'] == 0, 'Message version of Batch : {} is {}'.format(eachbatchType, venenoBatchDetail[eachbatchType]['message_version']))

    @staticmethod
    def assertSummaryReportVeneno(msgId, numberOfSkippedUsers):
        summaryReportVeneno = dbCallsAuthorize.getSummaryReportVeneno(msgId)
        Logger.log('Validating SummaryReportVeneno with Information :', summaryReportVeneno)
        countOfSkippedUsers = 0
        for eachSubType in summaryReportVeneno:
            countOfSkippedUsers = countOfSkippedUsers + int(summaryReportVeneno[eachSubType]['count'])
            Assertion.constructAssertion(summaryReportVeneno[eachSubType]['message_version'] == 0, 'Message Version for Batch :{} is :{}'.format(eachSubType, summaryReportVeneno[eachSubType]['message_version']))
        Assertion.constructAssertion(numberOfSkippedUsers == countOfSkippedUsers, 'Matching Number of Skipped Users in ServiceDetails :{} and in summaryVeneno :{}'.format(numberOfSkippedUsers, countOfSkippedUsers))

    @staticmethod
    def assertSummaryReportNsadmin(msgId, numberOfTestUsers):
        summaryReportNsadmin = dbCallsAuthorize.getSummaryReportNsadmin(msgId)
        Logger.log('Validating in Summary report Nsadmin :', summaryReportNsadmin)
        totalCountInTable = 0
        for eachDeliveryId in summaryReportNsadmin:
            totalCountInTable = totalCountInTable + int(summaryReportNsadmin[eachDeliveryId]['count'])
        Assertion.constructAssertion(int(numberOfTestUsers) == totalCountInTable , 'NumberOfTestUsers :{} and count in SummaryReportNsadmin is :{}'.format(numberOfTestUsers , totalCountInTable))

    @staticmethod
    def dbAssertAuthorize_VenenoDataDetails(bucketId, messageId, message, table='inbox', checkSkippedUsers=False, errorType=99999, errorDescription=''):
        if table is 'inbox':
            inboxDetailWithUserIds = dbCallsAuthorize.getInboxDetail(bucketId, messageId)
            listOfAllTagsInMessageBody = re.findall(r"\{{(.*?)\}}", message)
            listOfAllTagsInMessageBody.remove('optout')
            Logger.log('InboxDetails :{} getting validated with listOfAllTagsInMessageBody :{}'.format(inboxDetailWithUserIds, listOfAllTagsInMessageBody))
            for eachuser in inboxDetailWithUserIds:
                authorize.ResolvedTagsForEachUser(inboxDetailWithUserIds[eachuser]['id'], inboxDetailWithUserIds[eachuser]['resolved_tags'], listOfAllTagsInMessageBody)
        else:
            skippedDetailWithUserIds = dbCallsAuthorize.getSkippedDetail(bucketId, messageId)
            for eachUserId in skippedDetailWithUserIds:
                Logger.log('UserId : {} , got Skipped due to errorTypeId:{} and errorDescription:{}'.format(eachUserId, skippedDetailWithUserIds[eachUserId]['error_type_id'], skippedDetailWithUserIds[eachUserId]['error_description']))
                if checkSkippedUsers : authorize.dbAssertSkippedUsers(eachUserId, skippedDetailWithUserIds[eachUserId]['error_type_id'], skippedDetailWithUserIds[eachUserId]['error_description'], skippedDetailWithUserIds[eachUserId]['message_version'], errorType, errorDescription)

    @staticmethod
    def ResolvedTagsForEachUser(userId, resolvedTags, listOfAllTagsInMessageBody):
        Logger.log('List of All tags In Message :{}'.format(listOfAllTagsInMessageBody))
        for eachTag in listOfAllTagsInMessageBody:
            Assertion.constructAssertion(eachTag in resolvedTags, 'Checking Tag :{} which we passed in message Body in Resolved Tags :{} For UserId:{}'.format(eachTag, resolvedTags, userId))

    @staticmethod
    def dbAssertSkippedUsers(userId, actualErrorType, actualErrorReason, actualMessageVersion, expectedErrorType, expectedErrorReason):
        Assertion.constructAssertion(int(actualErrorType) == int(expectedErrorType), 'errorType why user got Skipped in DB :{} and expected :{} for userId :{}'.format(actualErrorType, expectedErrorType, userId))
        Assertion.constructAssertion(str(actualErrorReason) == str(expectedErrorReason), 'Reason why user got Skipped in DB :{} and expected :{} for userId :{}'.format(actualErrorReason, expectedErrorReason, userId))
        Assertion.constructAssertion(actualMessageVersion == 0, 'Skipped message_version : {}  matched'.format(actualMessageVersion))

    @staticmethod
    def assertUserPresenceInSkippedTable(messageId, bucketId, errorType, errorMessage):
        listOfErrorType = []
        listOfErrorDescription = []
        skippedDetailWithUserIds = dbCallsAuthorize.getSkippedDetail(bucketId, messageId)
        for eachUserId in skippedDetailWithUserIds:
            listOfErrorType.append(skippedDetailWithUserIds[eachUserId]['error_type_id'])
            listOfErrorDescription.append(skippedDetailWithUserIds[eachUserId]['error_description'])
        Assertion.constructAssertion(errorType in listOfErrorType, 'ErrorType :{} Present in Skipped table'.format(errorType))
        Assertion.constructAssertion(errorMessage in listOfErrorDescription, 'ErrorMessage :{} Present in Skipped table'.format(errorMessage))

    @staticmethod
    def assertUserPresenceInNsAdminTable(messageId, bucketId, numberOfUsers,testControlType='org', verify=True, waitForInboxMsg = False,groupVersionId=0,channel=None):
        if testControlType == 'custom':
            numberOfUsers = 0
            groupVersionResult = dbCallsList.getGroupVersionDetailWithGroupVersionId(groupVersionId)
            listOfUsers = dbCallsList.getUsersFromCampaignGroupRecipient(groupVersionResult['bucket_id'],groupVersionId,channel=channel)
            bound = (90 * 128)/100
            key = authorize.randomize(int(groupVersionResult['campaign_id']))
            for eachuser in listOfUsers:
                significant_bit = eachuser & 127
                significant_bit = authorize.randomize(significant_bit)
                bucket_position_of_input = (significant_bit ^ key) & 127
                if bucket_position_of_input > bound:
                    Logger.log('userid :{} is counted as Control')
                else:
                    numberOfUsers = numberOfUsers + 1
                    Logger.log('userid :{} is counted as Test')
        inboxDetailWithUserIds = dbCallsAuthorize.getInboxDetail(bucketId, messageId,waitForInboxMsg=waitForInboxMsg)
        Assertion.constructAssertion(len(inboxDetailWithUserIds) == numberOfUsers, 'Number Of Users sent :{} and present in Inbox is:{}'.format(numberOfUsers, len(inboxDetailWithUserIds)), verify=verify)

    @staticmethod
    def randomize(key):
        return (key ^ (key << 5) ^ (key << 2))

    @staticmethod
    def dbAssertAuthorize_HealthDashboardNotification(campaignId, refId=None, ExpectedMsg=['Messages sent'] , channel='SMS'):
        if refId is None:
            refId = campaignId
        notificationDetails = dbCallsAuthorize.getHealthDashBoardNotifications(refId)
        Assertion.constructAssertion(notificationDetails.has_key(channel), 'Notification Causes matched actual : {} and expected : {}'.format(notificationDetails.keys(), channel) , verify=True)
        Assertion.constructAssertion(str(notificationDetails[channel][0]) in ExpectedMsg, 'Notification Message actual : {}  and expected : {}'.format(notificationDetails[channel], ExpectedMsg), verify=True)

    @staticmethod
    def dbAssertAuthorize_bulk_sms_campaign(campaignId, messageId):
        bulk_sms_campaign = dbCallsAuthorize.getBulkSMS_Campaigns(campaignId, messageId)
        Assertion.constructAssertion((len(bulk_sms_campaign) != 0), 'Bulk SMS Message queued in the DB')

    @staticmethod
    def dbAssertionInSkippedReplyTables(messageId):
        batchDetails = dbCallsAuthorize.getVenenoBatchDetail(messageId)
        batchIds = list()
        for k, v in batchDetails.iteritems():
            batchIds.append(v['batch_id'])
        batchIds = list(set(batchIds))
        listOfReplyBatch = dbCallsAuthorize.getVenenoReplyBatchDetail(messageId)
        for actual, expected in zip(listOfReplyBatch,batchIds):
            Assertion.constructAssertion(expected in actual['batch_id'] , 'Batch Ids Mismatch in Reply and Batch Details Actual: {} and Expected: {}'.format(actual['batch_id'], expected))
        listOfMonitorStatus = dbCallsAuthorize.getVenenoMonitorStatus(messageId)
        Assertion.constructAssertion(len(listOfReplyBatch) != 0, 'No of Message Batches : {} Skipped & captured'.format(str(len(listOfReplyBatch))))
        Assertion.constructAssertion(len(listOfMonitorStatus) != 0, 'Monitor status updated for MessageId : {}'.format(str(messageId)))
        for version, status in listOfMonitorStatus.items():
            Assertion.constructAssertion(status['status'] == 1, 'Monitor status MessageId : {} and Message version: {} and Processed status: {}'.format(str(messageId), str(version), str(status['status'])))

    @staticmethod
    def dbAssertRateLimitStats(listOfUsers, expectedResultForEachUser, channel='SMS'):
        Logger.log(listOfUsers)
        listOfUsers = tuple(listOfUsers)
        Logger.log(listOfUsers)
        dictOfUserStats = dbCallsAuthorize.getRateLimitStats(listOfUsers, channel)
        for eachUserStats in dictOfUserStats:
            Assertion.constructAssertion(dictOfUserStats[eachUserStats] == expectedResultForEachUser, 'Expected Data is stats for user :{} is :{} and constructed From DB :{}'.format(eachUserStats, expectedResultForEachUser, dictOfUserStats[eachUserStats]))
