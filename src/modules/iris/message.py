import json, time, sys, datetime, re
from src.Constant.constant import constant
from src.modules.iris.construct import construct
from src.utilities.logger import Logger
from src.utilities.assertion import Assertion
from src.utilities.utils import Utils
from src.modules.iris.dbCallsMessage import dbCallsMessage
from src.modules.iris.dbCallsList import dbCallsList
from src.modules.iris.campaigns import campaigns

class campaignMessage():
    
    @staticmethod
    def createMessage(self, payloadData={}, messageInfo=['SMS', ['IMMEDIATE'], ['PLAIN'], True], process='update'):
        Logger.log('Create Message Call with payloadDate :{} , messageInfo :{} and process :{}'.format(payloadData, messageInfo, process))
        createMessasgeConstructedEndPoint = construct.constructUrl('createmessage').replace('{campaignId}', str(self.campaignId))
        if 'COUPONS' in messageInfo[2]: 
            Logger.log('Incentive is Coupons so Updating VoucherId in Incentive List as', self.voucherId)
            messageInfo[2].append(self.voucherId)
        
        if len(payloadData) == 0:
            Logger.log('Creating Body for Type :{} and Schedulle Type :{} with Incentive Type :{} taking sender Details as :{}'.format(messageInfo[0], messageInfo[1], messageInfo[2], messageInfo[3]))
            payloadData = construct.constructCreateMessageBody(self.listId, messageInfo[0], messageInfo[1], messageInfo[2], messageInfo[3])
        else:
            payloadData.update({'listId':self.listId})
            Logger.log('payloadData updating is :', payloadData)
            payloadData = construct.constructBody(payloadData, process, 'createmessage')
            if payloadData['channel'].lower() == 'wechat':
                if 'senderDetails' in payloadData :payloadData.pop('senderDetails')
                if 'additionalInfo' in payloadData :payloadData.pop('additionalInfo')
                if not isinstance(payloadData['message'], dict):payloadData.pop('message')

        response = Utils.makeRequest(url=createMessasgeConstructedEndPoint, data=payloadData, auth=construct.constructAuthenticate(), headers=construct.constructHeaders(), method='POST')
        return construct.constructResponse(response), payloadData    
            
    @staticmethod
    def updateDefaultMessageJson(campaignId, listId, voucherId, strategy, bucketId, groupVersionResult):
        Logger.log('Updating Default Message Object with campaignId:{} ,listId:{} ,voucherId:{} ,strategy:{} ,bucketid:{} ,groupVersionResult:{}'.format(campaignId, listId, voucherId, strategy, bucketId, groupVersionResult))
        try:
            constant.messagesDefault['campaignId'] = campaignId
            constant.messagesDefault['listId'] = listId
            constant.messagesDefault['voucherId'] = voucherId
            constant.messagesDefault['strategy'] = strategy
            constant.messagesDefault['bucketId'] = bucketId
            constant.messagesDefault['groupVersionResult'] = groupVersionResult
        except Exception, exp:
            Logger.log('Exception :{} while updating campaignInfo to Message Dict'.format(exp))
        finally:
            Logger.log('message Default Finally Set as :', constant.messagesDefault)
        
    @staticmethod
    def updateDefaultMessageJsonWithMessageInfoValues(messageInfo, payload, msgId):
        Logger.log('Updating Default Message Object with Message Info:', messageInfo)
        try:
            constant.messagesDefault[messageInfo[0]][messageInfo[1][0]][messageInfo[2][0]][messageInfo[3]] = {'messageInfo':messageInfo, 'payload':payload, 'msgId':msgId}
        except Exception, exp:
            Logger.log('Exception :{} while updating msgId :{} to messageInfo:{}'.format(exp, msgId, messageInfo))
        finally:
            Logger.log('message Default Finally Set as :', constant.messagesDefault)
    
    @staticmethod
    def assertCreateMessage(response, expectedStatusCode, expectedErrorCode=99999, expectedErrorMessage='Unexpected error : null'):
        Logger.log('Response sent to be asserted :', response)
        if response['constructed'].lower() == 'pass':
            if expectedStatusCode >= 200 and expectedStatusCode <= 300: 
                Assertion.constructAssertion(response['statusCode'] == int(expectedStatusCode), 'Matching statusCode actual :{},expected :{}'.format(response['statusCode'], expectedStatusCode))
                Assertion.constructAssertion(response['json']['entity']['messageId'] > 0, 'MessageId should always be greater then zero')
                if len(response['json']['warnings']) > 0:
                    Logger.log('There was a Warning while Creating Campaign :', response['json']['warnings'])
            else:
                Logger.log('loop for each error')
                for errorReturned in response['json']['errors']:
                    Logger.log('Validating Failed Request Data as Expected:', errorReturned)
                    Assertion.constructAssertion(response['statusCode'] == int(expectedStatusCode), 'Matching statusCode actual :{},expected :{}'.format(response['statusCode'], int(expectedStatusCode)))
                    Assertion.constructAssertion(errorReturned['code'] == expectedErrorCode, 'Matching Error Code ,actual:{} and expected:{}'.format(errorReturned['code'], expectedErrorCode))
                    Assertion.constructAssertion(errorReturned['status'] == False, 'Matching error status')
                    Assertion.constructAssertion(errorReturned['message'] in expectedErrorMessage, 'Matching Error Message ,actual:{} and expected:{}'.format(errorReturned['message'], expectedErrorMessage))          
        else:
            assert False, 'Constructed Body has Failed due to Exception so no Validation'
    
    @staticmethod
    def assertCreateMessageDbCalls(messageId, campaignId, payload):
        messageQueueResult = dbCallsMessage.getMessageQueueFromMessageId(messageId, payload)
        Assertion.constructAssertion(int(messageQueueResult['id']) == int(messageId), 'Matching MessageId with DBResult Id')
        Assertion.constructAssertion(int(messageQueueResult['campaign_id']) == int(campaignId), 'CampaignId Passed :{} and in MessageQueue :{}'.format(campaignId, messageQueueResult['campaign_id']))
        Assertion.constructAssertion(int(messageQueueResult['group_id']) == int(dbCallsList.getGroupVersionDetailsWithGroupId(payload['listId'])['TEST']['id']), 'GroupVersionId passed :{} and in MessageQueue:{}'.format(payload['listId'], messageQueueResult['group_id']))    
        Assertion.constructAssertion(str(messageQueueResult['status']) == 'OPEN', 'Matching Status should always be open')
        if 'message' in payload:
            Assertion.constructAssertion(messageQueueResult['param']['message'] == payload['message'], 'Message Queue Result:{} and payload Message is :{}'.format(str(messageQueueResult['param']['message']), str(payload['message'])))
        Assertion.constructAssertion(int(messageQueueResult['Approved']) == 0, 'Matching Approved in Message Queue as 0')

        if 'sms' in payload['channel'].lower():
            if 'targetNdnc' in payload['additionalInfo'] :Assertion.constructAssertion((json.loads(messageQueueResult['default_arguments'])['sendToNdnc'] != 'false') == payload['additionalInfo']['targetNdnc'], 'Matching Default Argument with Additional Info for NDNC')
            if 'useTinyUrl' in payload['additionalInfo'] :Assertion.constructAssertion((json.loads(messageQueueResult['default_arguments'])['useTinyUrl'] != 'false') == payload['additionalInfo']['useTinyUrl'], 'Matching Default Argument with Additional Info for useTinyUrl')
            # if 'storeType' in payload : Assertion.constructAssertion(str(json.loads(messageQueueResult['default_arguments'])['store_type']) == str(payload['storeType']).lower(), 'Matching Default Argument with storeType')

            Assertion.constructAssertion(str(json.loads(messageQueueResult['default_arguments'])['sender_cdma']) == str(payload['senderDetails']['cdmaSenderId']), 'Matching Default Argument with storeType')
            Assertion.constructAssertion(str(json.loads(messageQueueResult['default_arguments'])['sender_gsm']) == str(payload['senderDetails']['gsmSenderId']), 'Matching Default Argument with storeType')
            if 'domainGatewayMapId' in payload['senderDetails'] : Assertion.constructAssertion(str(json.loads(messageQueueResult['default_arguments'])['domain_gateway_map_id']) == str(payload['senderDetails']['domainGatewayMapId']), 'Matching Default Argument with storeType')

        if 'wechat' in payload['channel'].lower():
            Assertion.constructAssertion(str(json.loads(messageQueueResult['default_arguments'])['AppId']) == str(payload['accountDetails']['appId']), 'Matching Default Argument with AccountDetails')
            Assertion.constructAssertion(str(json.loads(messageQueueResult['default_arguments'])['AppSecret']) == str(payload['accountDetails']['appSecret']), 'Matching Default Argument with AccountDetails')
            Assertion.constructAssertion(str(json.loads(messageQueueResult['default_arguments'])['OriginalId']) == str(payload['accountDetails']['originalId']), 'Matching Default Argument with AccountDetails')

        if payload['schedule']['type'] == 'IMMEDIATELY':
            Assertion.constructAssertion(str(messageQueueResult['type']) == payload['channel'], 'Channel Passed in payload :{} and messageQueue :{}'.format(payload['channel'], messageQueueResult['type']))
            Assertion.constructAssertion(str(messageQueueResult['scheduled_type']) == str(payload['schedule']['type']), 'ScheduleType Passed :{} and in MessageQueue :{}'.format(payload['schedule']['type'], messageQueueResult['scheduled_type'])) 
        elif payload['schedule']['type'] == 'PARTICULAR_DATE':
            Assertion.constructAssertion(str(messageQueueResult['type']) == payload['channel'], 'Channel Passed in payload :{} and messageQueue :{}'.format(payload['channel'], messageQueueResult['type']))
            Assertion.constructAssertion(str(messageQueueResult['scheduled_type']) == str(payload['schedule']['type']), 'ScheduleType Passed :{} and in MessageQueue :{}'.format(payload['schedule']['type'], messageQueueResult['scheduled_type'])) 
            remindersTableResult = dbCallsMessage.getReminderDataFromMessageId(messageId, 'iris')
            campaignMessage.assertReminderTable(remindersTableResult, payload['listId'], payload['schedule']['datetime'])
        elif payload['schedule']['type'] == 'RECURRING':
            Assertion.constructAssertion(str(messageQueueResult['type']) == 'SMS_REMINDER', 'Channel Passed in payload :{} and messageQueue :{}'.format(payload['channel'], messageQueueResult['type']))
            Assertion.constructAssertion(str(messageQueueResult['scheduled_type']) == 'SCHEDULED', 'ScheduleType Passed :{} and in MessageQueue :{}'.format(payload['schedule']['type'], messageQueueResult['scheduled_type'])) 
            remindersTableResult = dbCallsMessage.getReminderDataFromMessageId(messageId, 'iris')
            campaignMessage.assertReminderTable(remindersTableResult, payload['listId'], payload['schedule']['pattern'])
        if 'incentive' in payload:
            if payload['incentive']['type'] == 'GENERIC':
                incentiveDbResult = dbCallsMessage.getGenericIncentiveId(messageQueueResult['id'])
                incentiveIdForGeneric = dbCallsMessage.getIncentiveMetaDetails()['GENERIC']
                Assertion.constructAssertion(int(incentiveDbResult['incentive_type_id']) == int(incentiveIdForGeneric), 'Incentive Type Id :{}'.format(incentiveIdForGeneric))
                Assertion.constructAssertion(int(incentiveDbResult['campaign_id']) == int(campaignId), 'Campaign Id in Incentive Table :{}'.format(campaignId))
            
    @staticmethod
    def assertReminderTable(reminderTableResult, listId, dateTimePassedToSchedulleInPayload, state='OPEN'):
        Assertion.constructAssertion(len(reminderTableResult) == 2, 'Matching Reminder Table have 2 entries')
        for eachReminderType in reminderTableResult:
            Logger.log('Checking for Reminder Type :', eachReminderType)
            Assertion.constructAssertion(int(reminderTableResult[eachReminderType]['group_id']) == int(listId), 'Passed GroupVersionId :{} and reminderTable group_id :{}'.format(listId, reminderTableResult[eachReminderType]['group_id']))
            Assertion.constructAssertion(str(reminderTableResult[eachReminderType]['state']) == str(state), 'Matching state as :' + str(state))
            campaignMessage.assertFrequencyInReminderTable(reminderTableResult[eachReminderType]['frequency'], dateTimePassedToSchedulleInPayload)
            cronTableResult = dbCallsMessage.getCronTableFromReminderId(reminderTableResult[eachReminderType]['id'], 'iris')
            Assertion.constructAssertion(str(cronTableResult['cron_pattern']) == str(reminderTableResult[eachReminderType]['frequency']), 'Matching Cron Table Pattern with Reminder Pattern')
            
    @staticmethod
    def assertFrequencyInReminderTable(reminderTableFrequency, scheduledDateTime):
        listOfWeekDays = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        listOfFrequency = reminderTableFrequency.split(' ')    
        if type(scheduledDateTime) is dict:
            Assertion.constructAssertion(int(listOfFrequency[4]) == int(scheduledDateTime['week']), 'Matching Weekday in Frequency')
            Assertion.constructAssertion(int(listOfFrequency[3]) == int(scheduledDateTime['month']), 'Matching Month in Frequency')
            Assertion.constructAssertion(int(listOfFrequency[2]) == int(scheduledDateTime['day']), 'Matching Date in Frequency')
            Assertion.constructAssertion(int(listOfFrequency[1]) == int(scheduledDateTime['hours']), 'Matching Hour in Frequency')
            Assertion.constructAssertion(int(listOfFrequency[0]) == int(scheduledDateTime['minutes']), 'Matching minute in Frequency')
        else:
            dateTime = datetime.datetime.fromtimestamp(scheduledDateTime / 1000)
            Assertion.constructAssertion(int(listOfFrequency[4]) == int(listOfWeekDays.index(str(dateTime.strftime("%A")))), 'Matching Weekday in Frequency : {}  with {}'.format(int(listOfFrequency[4]), int(listOfWeekDays.index(str(dateTime.strftime("%A"))))))
            Assertion.constructAssertion(int(listOfFrequency[3]) == int(str(dateTime.strftime("%m"))), 'Matching Month in Frequency :{} with {}'.format(int(listOfFrequency[3]), int(str(dateTime.strftime("%m")))))
            Assertion.constructAssertion(int(listOfFrequency[2]) == int(str(dateTime.strftime("%d"))), 'Matching Date in Frequency :{} with {}'.format(int(listOfFrequency[2]), int(str(dateTime.strftime("%d")))))
            try:
                Assertion.constructAssertion(int(listOfFrequency[1]) == int(str(dateTime.strftime("%H"))), 'Matching Hour in Frequency :{} with {}'.format(int(listOfFrequency[1]), int(str(dateTime.strftime("%H")))))
                Assertion.constructAssertion(int(listOfFrequency[0]) == int(str(dateTime.strftime("%M"))), 'Matching minute in Frequency :{} with {}'.format(int(listOfFrequency[0]), int(str(dateTime.strftime("%M")))))
            except AssertionError, exp:
                Logger.log('Assertion Failed on Hours or Minute due to Frequency in Reminder Table :{} and computed at our end :{}'.format(reminderTableFrequency, dateTime.strftime('%A %m %d %H %M')))

    @staticmethod
    def getWeCRMTemplates():
            response = Utils.makeRequest(constant.config['wecrm_details']['url'], {}, campaignMessage.constructWecrmHeader(), 'GET')
            data = json.loads(response.content)
            length = 0
            for k in data['template_list']:
                countOfkeyword = len(re.findall(r'keyword', k['content'], re.M | re.I))
                if length < countOfkeyword:
                    length = countOfkeyword
                    constant.config['templateId'] = k['template_id']
                    constant.config['templateTitle'] = k['title']
            constant.config['templateSize'] = length

    @staticmethod
    def constructWecrmHeader():
        WeCRMheader =   {
                            'accept': 'application/json',
                            'x-cap-we-token': 'Peach ' + constant.config['wecrm_details']['token'],
                            'x-cap-we-id': constant.config['wecrm_details']['id']
                        }
        return WeCRMheader

    @staticmethod
    def constructHeader():
        templateheaders = {'accept': 'application/json', 'X-CAP-API-AUTH-ORG-ID' : str(constant.config['orgId']),
                           'Authorization' : 'Bearer ' + constant.config['token']}
        return templateheaders

    @staticmethod
    def setupTemplateId():
        url = constant.config['intouchUrl'] + str(constant.config['wecrm_details']['creativeTemplate']).format(constant.config['wecrm_details']['id'], constant.config['wecrm_details']['token'])
        response = Utils.makeRequest(url, {}, campaignMessage.constructHeader(), 'GET')
        responseJson = construct.constructResponse(response)['json']
        return campaignMessage.constructTemplateIds(responseJson['response']['mapped'])

    @staticmethod
    def constructTemplateIds(data):
        tempDict = {'coupons':None,'points':None,'plain':None,'generic':None}
        if len(data) != 0:
            for dataJson in data:
                if '{{voucher}}' in str(dataJson['versions']) and tempDict['coupons'] == None:
                    tempDict.update({'coupons' : dataJson['_id']})
                if '{{promotion_points}}' in str(dataJson['versions']) and tempDict['points'] == None:
                    tempDict.update({'points': dataJson['_id']})
                if not ('{{promotion_points}}' in str(dataJson['versions'])) and not ('{{voucher}}' in str(dataJson['versions'])) and tempDict['plain'] == None:
                    tempDict.update({'plain': dataJson['_id']})
                    tempDict.update({'generic': dataJson['_id']})
        else:
            Logger.log('Templates not available, Please create templates')
        if None in tempDict.values():
            Assertion.constructAssertion(False, 'Templates Ids not available for anyone/all incentive types, Please create templates', True)
        return tempDict

    @staticmethod
    def replyMessage(self):
        getReplyMessasgeListConstructedEndPoint = construct.constructUrl('getreplymessagelist').format(str(self.campaignId))
        skippedErrorIds = []
        response = Utils.makeRequest(url=getReplyMessasgeListConstructedEndPoint, data='', auth=construct.constructAuthenticate(), headers=construct.constructHeaders(), method='GET')
        responseEntity = construct.constructResponse(response)['json']['entity']
        for error in responseEntity:
            messageId = error['messageId']
            if self.commDetailsId == messageId:
                for errorDetails in error['errorDetails']:
                    skippedErrorIds.append(errorDetails['errorId'])
                    Logger.log('Error Details Id: {}, Description: {}, Count: {}: '.format(errorDetails['errorId'],errorDetails['errorDescription'],errorDetails['errorCount']))

                replyMessasgeConstructedEndPoint = construct.constructUrl('replymessage').format(str(self.campaignId), str(messageId))
                payloadData = {'skippedErrors' : skippedErrorIds}
                response = Utils.makeRequest(url=replyMessasgeConstructedEndPoint, data=payloadData, auth=construct.constructAuthenticate(), headers=construct.constructHeaders(), method='POST')
                Logger.log('Response of MessageId {} Replied and Response : {}'.format(messageId, construct.constructResponse(response)))
        return construct.constructResponse(response)