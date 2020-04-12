from src.dbCalls.campaignInfo import campaign_calls
from src.modules.irisv2.campaigns.getCampaignDBAssertion import GetCampaignDBAssertion
from src.modules.irisv2.helper.irisHelper import IrisHelper
from src.dbCalls.messageInfo import monitorStatus_calls
from src.utilities.logger import Logger
from src.Constant.constant import constant
from src.utilities.utils import Utils
from src.modules.inTouchAPI.inTouchAPI import InTouchAPI
from src.utilities.randValues import randValues
from src.modules.inTouchAPI.customer import Customer
from src.modules.inTouchAPI.request import Request
from src.modules.iris.dbCallsMessage import dbCallsMessage
from src.utilities.fileHelper import FileHelper
from src.modules.irisv2.list.createAudience import CreateAudience
from src.dbCalls.messageInfo import message_info
import time

class GetMonitoringDetails():

    @staticmethod
    def getByCampaignId(campaignId,queryParam):
        endpoint = IrisHelper.constructUrl('monitoringbycampaignid', queryParam=queryParam).format(campaignId)
        response = Utils.makeRequest(url=endpoint, data='', auth=IrisHelper.constructAuthenticate(),
                                     headers=IrisHelper.constructHeaders(), method='GET')
        return GetMonitoringDetails.constructMonitorStatusResponse(IrisHelper.constructResponse(response)['json'], byCampaignId=True)

    @staticmethod
    def getByMessageId(campaignId,messageId,queryParam):
        endpoint = IrisHelper.constructUrl('monitoringbymessageid', queryParam=queryParam).format(campaignId,messageId)
        response = Utils.makeRequest(url=endpoint, data='', auth=IrisHelper.constructAuthenticate(),
                                     headers=IrisHelper.constructHeaders(), method='GET')
        return GetMonitoringDetails.constructMonitorStatusResponse(IrisHelper.constructResponse(response)['json'])

    @staticmethod
    def getByOrgId(queryParam,entity=False):
        endpoint = IrisHelper.constructUrl('monitoringbyorgid', queryParam=queryParam)
        response = Utils.makeRequest(url=endpoint, data='', auth=IrisHelper.constructAuthenticate(),
                                     headers=IrisHelper.constructHeaders(), method='GET')
        return GetMonitoringDetails.constructMonitorStatusResponse(IrisHelper.constructResponse(response)['json'],byCampaignId=entity)

    @staticmethod
    def constructMonitorStatusResponse(response, byCampaignId = False):
        monitorStatus = []
        if byCampaignId and 'data' in response:
            for data in response['data']:
                monitorStatus.append(GetMonitoringDetails.constructMonitorStatusResponse({'entity' : data})[0])
        else:
            monitorStatus.append({'orgId' : response['entity']['orgId'],
                            'campaignId' : response['entity']['campaignId'],
                            'messageId' : response['entity']['messageId'],
                            'monitoringDetails' : response['entity']['monitoringDetails']})
        return monitorStatus

    @staticmethod
    def contructExpectedMonitorDetails(messageObjectId, isDeliveryBreakEnabled = False, isScheduledMsg = False,queryParam=None):
        sentDetails = None
        campaignIdFromCD = None
        cdDetails = monitorStatus_calls().getMsgId(messageObjectId)
        if 'id' in cdDetails:
            reportNsadmin = monitorStatus_calls().getSummaryReportNsadmin(cdDetails['id'])
            campaignIdFromCD = cdDetails['campaignId']
            sentDetails = {
                'totalCustomerCount': cdDetails['overall_recipient_count'] if 'overall_recipient_count' in cdDetails else 0,
                'targetCustomerCount': cdDetails['expected_delivery_count'] if 'expected_delivery_count' in cdDetails else 0,
                'sentCount': 0,
                'skippedCount': 0,
                'inProgressCount': 0,
                'failedCount': 0,
                'deliveredCount': 0,
                'channelDeliveryBreakup': {},
                'executionDateHour': 0
            }
            for x in reportNsadmin:
                if 'Sent' == x['status']:
                    sentDetails.update({'sentCount': x['count']})
                elif 'About to send' == x['status']:
                    sentDetails.update({'inProgressCount': x['count']})
                elif 'Not Delivered' == x['status']:
                    sentDetails.update({'failedCount': x['count']})
                elif 'Delivered' == x['status']:
                    sentDetails.update({'deliveredCount': x['count']})
            if isDeliveryBreakEnabled:
                sentDetails.update({'channelDeliveryBreakup' : GetMonitoringDetails.constructCDBreakup(cdDetails['communication_type'], cdDetails['id'])})
                if len(sentDetails['channelDeliveryBreakup'][cdDetails['communication_type']]['skippedStatistics']) !=0:
                    skippedCount = 0
                    for each in sentDetails['channelDeliveryBreakup'][cdDetails['communication_type']]['skippedStatistics']:
                        skippedCount = skippedCount + each['count']
                    sentDetails.update({'skippedCount':skippedCount})
        failedDetails,campaignId = monitorStatus_calls().getExecutionJobStatus(messageObjectId,queryParam=queryParam)
        scheduleList = []
        if isScheduledMsg:
            scheduleList.append({'totalCustomerCount': len(constant.config['totalUserCount'])})

        if campaignIdFromCD is None and campaignId is None:
            campaignId = message_info(messageObjectId, messageJobDetailsCollection=False,
                         messageVariantsCollection=False).messageDbDetail['message_collection']['campaignId']

        return  {   'orgId' : constant.config['orgId'], 'campaignId' : campaignIdFromCD if campaignIdFromCD is not None else campaignId,
                    'messageId' : messageObjectId, 'monitoringDetails' : {'SENT': [] if sentDetails is None else [sentDetails], 'FAILED' : failedDetails, 'SCHEDULED' : scheduleList}}

    @staticmethod
    def constructCDBreakup(channelType, msgId):
        return {channelType : { 'sentStatistics' : monitorStatus_calls().getSummaryReportNsadmin(msgId),
                                'skippedStatistics' : monitorStatus_calls().getSummaryReportVeneno(msgId)}}


    @staticmethod
    def sortAndFormatDict(actualResponse, popFields = ['executionDateHour']):
        if type(actualResponse) == dict:
            for popKey in popFields:
                if popKey in actualResponse:
                    actualResponse.pop(popKey)
            for each in actualResponse:
                if type(actualResponse[each]) == list:
                    x = actualResponse[each]
                    GetMonitoringDetails.sortAndFormatDict(x)
                    for eachList in x:
                        if type(eachList) == dict:
                            GetMonitoringDetails.sortAndFormatDict(eachList)
                elif type(actualResponse[each]) == dict:
                    GetMonitoringDetails.sortAndFormatDict(actualResponse[each])
        elif type(actualResponse) == list:
            actualResponse.sort()
            for each in actualResponse:
                if type(each) == dict:
                    GetMonitoringDetails.sortAndFormatDict(each)
                elif type(each) == list:
                    GetMonitoringDetails.sortAndFormatDict(each)
        return actualResponse

    @staticmethod
    def removeUnWantedJsonInResponse(response):
        for each in response:
            failedData = each['monitoringDetails']['FAILED']
            try:
                while(True):
                    del failedData[failedData.index({})]
            except Exception,exp:
                Logger.log('Removed All Empty json created in Failed , Current Value :{}'.format(failedData))
        return response


    @staticmethod
    def formatingMonitorDetails(actualResponse, isDeliveryBreakEnabled = False, isScheduledMsg = False,forceUpdate=False,queryParam=None):
        formatedAR = list()
        formatedER = list()
        expectedResponse = list()
        for expRes in actualResponse:
            expectedResponse.append(GetMonitoringDetails.contructExpectedMonitorDetails(expRes['messageId'], isDeliveryBreakEnabled=isDeliveryBreakEnabled, isScheduledMsg=isScheduledMsg,queryParam=queryParam))
        for actual, expected in zip(actualResponse,expectedResponse):
            if len(actual['monitoringDetails']['SCHEDULED'])==0 or forceUpdate:
                formatedAR.append(GetMonitoringDetails.sortAndFormatDict(actual))
                formatedER.append(GetMonitoringDetails.sortAndFormatDict(expected))
        GetMonitoringDetails.removeUnWantedJsonInResponse(formatedAR)
        GetMonitoringDetails.removeUnWantedJsonInResponse(formatedER)
        return formatedAR,formatedER

    @staticmethod
    def createSkippedPartialList():
        user1 = randValues.getRandomMobileNumber()
        user2 = str(int(user1) + 1)
        user3 = str(int(user1) + 2)
        user4 = GetMonitoringDetails.getNDNCUser()
        user5= GetMonitoringDetails.getInvalidMobile()
        listInfo=GetMonitoringDetails.createListForSkippedUser([user1,user2,user3,user4,user5])
        GetMonitoringDetails.markInactiveUser(user1,user2)
        return listInfo

    @staticmethod
    def createListForSkippedUser(users):
        filePath = GetMonitoringDetails.createFileForSkippedUsers(users)
        listInfo = CreateAudience.uploadList('LIVE', 'ORG',filePath=filePath,
                                         campaignCheck=False, updateNode=True, lockNode=True)
        return listInfo

    @staticmethod
    def createFileForSkippedUsers(users):
        filePath = constant.autoTempFilePath + 'AutoList_{}_{}'.format(randValues.randomString(8),
                                                                       int(time.time() * 1000))
        file = FileHelper(filePath)
        for eachUser in users:
            file.appendToFile('{},{}'.format(eachUser,'Skip_{}'.format(eachUser)))
        Logger.log('FilePath Create for Skipped User :{}'.format(filePath))
        return filePath

    @staticmethod
    def markInactiveUser(customer1Mobile,customer2Mobile):
        try:
            cusObj1 = InTouchAPI(Customer.Add(mobile=customer1Mobile))
            cusObj2 = InTouchAPI(Customer.Add(mobile=customer2Mobile))
            reqObj = InTouchAPI(Request.Add(mobileS=cusObj1.params['mobile'], emailS=cusObj1.params['email'],
                                            mobileT=cusObj2.params['mobile'], emailT=cusObj2.params['email']))
        except Exception,exp:
            Logger.log('NotAbleToCreateInactiveUser, Exception :{}'.format(exp))

    @staticmethod
    def getNDNCUser():
        return dbCallsMessage.getNDNCUserMobileNumber()[0]

    @staticmethod
    def markUnsubscribedUser(cusObj):
        unsubscribeObj = InTouchAPI(
            Customer.unsubscribe(body={'root': {'subscription': {'mobile': cusObj.params['mobile']}}}))


    @staticmethod
    def getInvalidMobile():
        return dbCallsMessage.getInvalidUserMobileNumber()[0]
