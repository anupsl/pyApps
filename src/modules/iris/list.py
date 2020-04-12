import json, time, sys
from src.Constant.constant import constant
from src.modules.iris.campaigns import campaigns
from src.modules.iris.construct import construct
from src.modules.iris.dbCallsList import dbCallsList
from src.modules.iris.dbCallsCampaign import dbCallsCampaign
from src.utilities.logger import Logger
from src.utilities.assertion import Assertion
from src.utilities.utils import Utils


class campaignList():
     
    """ @createList """
    
    @staticmethod
    def createList(payloadData={}, campaignId=None, campaignType=['LIVE', 'ORG', 'List', 'TAGS', 0], process='update', key=True):    
        campaignDefault = constant.campaignDefaultValues
        if campaignId == None:    
            campaignIdValue = constant.campaignDefaultValues[campaignType[0]][campaignType[1]]['Value']
            if len(campaignIdValue['response']) == 0 and len(campaignIdValue['payload']) == 0:
                response, payload = campaigns.createCampaign({}, campaignTypeParams=[campaignType[0], campaignType[1]])   
                if response['statusCode'] == 200:
                    campaignId = response['json']['entity']['campaignId']
                else:
                    Assertion.constructAssertion(False, 'Error : While Creating Campaign , Status Code : {}'.format(response['statusCode']))
            else :
                campaignId = campaignIdValue['response']['json']['entity']['campaignId']
               
        Logger.log('CamapaignId getting used to create list :', campaignId)
        if key:
            createListConstructedEndPoint = construct.constructUrl('createlist').replace('{campaignId}', str(campaignId))
            payload = construct.constructBody(payloadData, process, 'createlist')
            response = Utils.makeRequest(url=createListConstructedEndPoint, data=payload, auth=construct.constructAuthenticate(), headers=construct.constructHeaders(), method='POST')
            if response.status_code == 200:
                Logger.log('Updating campaignDefaultValues as Status Code is 200')
                constant.campaignDefaultValues[campaignType[0]][campaignType[1]][campaignType[2]][campaignType[3]][campaignType[4]].update({'response':construct.constructResponse(response), 'payload':payload, 'campaignId':campaignId})
            return construct.constructResponse(response), payload, campaignId
        else :
            listIdValue = constant.campaignDefaultValues[campaignType[0]][campaignType[1]][campaignType[2]][campaignType[3]]
            
            if len(listIdValue['response']) == 0 or len(listIdValue['payload']) == 0:
                response, payload, campaignId = campaignList.createList(payloadData, campaignId, campaignType, process, key=True)
                listIdValue['response'].update({'response':response})
                listIdValue['payload'].update({'payload':response})
                listIdValue.update({'campaignId':campaignId})
                return response, payload, campaignId
            else :
                return listIdValue['response'], listIdValue['payload'], listIdValue['campaignId']
        
    @staticmethod
    def assertCreateList(response, expectedStatusCode, expectedErrorCode=2001, expectedErrorMessage='Unexpected error : null'):
        Logger.log('Response sent to be asserted :', response)
        if response['constructed'].lower() == 'pass':
            if expectedStatusCode >= 200 and expectedStatusCode <= 300: 
                Assertion.constructAssertion(response['statusCode'] == int(expectedStatusCode), 'Matching statusCode actual :{},expected :{}'.format(response['statusCode'], expectedStatusCode))
                Assertion.constructAssertion(response['json']['entity']['listId'] > 0, 'ListId should always be greater then zero')
                if len(response['json']['warnings']) > 0:
                    Logger.log('There was a Warning while Creating Campaign :', response['json']['warnings'])
            else:
                errorReturned = response['json']['errors'][0]
                Logger.log('Validating Failed Request Data as Expected:', errorReturned)
                Assertion.constructAssertion(response['statusCode'] == int(expectedStatusCode), 'Matching statusCode actual :{},expected :{}'.format(response['statusCode'], int(expectedStatusCode)))
                Assertion.constructAssertion(errorReturned['code'] == expectedErrorCode, 'Matching Error Code ,actual:{} and expected:{}'.format(errorReturned['code'], expectedErrorCode))
                Assertion.constructAssertion(errorReturned['status'] == False, 'Matching error status')
                Assertion.constructAssertion(errorReturned['message'] == expectedErrorMessage, 'Matching Error Message ,actual:{} and expected:{}'.format(errorReturned['message'], expectedErrorMessage))          
        else:
            assert False, 'Constructed Body has Failed due to Exception so no Validation'
    
    @staticmethod
    def assertCreateListDbCalls(listId, payload, testControlType, listType='CAMPAIGN_USERS', expectedTestUsers=0, expectedControlUsers=0):
        Logger.log('ListId Recieved to Validate is :', listId)
        Logger.log('Payload to Assert With :', payload)
        groupDetailResult = dbCallsList.getGroupDetailsWithListId(listId)
        groupVersionDetailResult = dbCallsList.getGroupVersionDetailsWithGroupId(listId)
        campaignList.assertGroupDetail(groupDetailResult, payload, listType)
        campaignList.assertGroupVersionDetail(groupVersionDetailResult, expectedTestUsers, expectedControlUsers, testConstrolType=testControlType)
        return groupVersionDetailResult, groupVersionDetailResult['TEST']['bucket_id']
        
    @staticmethod
    def assertGroupDetail(groupDetailResult, payload, listType):
        Assertion.constructAssertion(groupDetailResult['group_label'] == payload['name'] , 'Matching List Name, actual:{} and expected: {}'.format(groupDetailResult['group_label'], payload['name']))
        Assertion.constructAssertion(groupDetailResult['type'].upper() == listType, 'Type from groupDetailResult is not matching')
        
    @staticmethod
    def assertGroupVersionDetail(groupVersionDetailResult, expectedTestUsers=0, expectedControlUsers=0, testConstrolType='ORG'):
        Assertion.constructAssertion(groupVersionDetailResult['TEST']['bucket_id'] > 0, 'Bucket Id should never be less than 0')
        Assertion.constructAssertion(groupVersionDetailResult['TEST']['customer_count'] == expectedTestUsers , 'Matching Test Type User Count, actual :{} and expected :{}'.format(groupVersionDetailResult['TEST']['customer_count'], expectedTestUsers))
        if testConstrolType.lower() != 'skip':
            Assertion.constructAssertion(groupVersionDetailResult['CONTROL']['bucket_id'] > 0, 'Bucket Id should never be less than 0')
            Assertion.constructAssertion(groupVersionDetailResult['CONTROL']['customer_count'] == expectedControlUsers , 'Matching Control Type User Count, actual :{} and expected :{}'.format(groupVersionDetailResult['CONTROL']['customer_count'], expectedControlUsers))


    """ @addRecipient """
    
    @staticmethod
    def addRecipient(payloadData, campaignId, listId, userType='mobile', numberOfUsers=1, numberOfCustomTags=0, process='update', newUser=True):
        campaignList.updateRechabilityBeforeEachRun()
        addRecipientConstructedEndPoint = construct.constructUrl('addrecipient').replace('{campaignId}', str(campaignId)).replace('{listId}', str(listId))
        
        payload = {}
        if len(payloadData) == 0:
            Logger.log('Constructing Payload for userType {}, for numberOfusers {} and customCount {}'.format(userType, numberOfUsers, numberOfCustomTags))
            if newUser == True:
                payload = construct.constructAddRecipientPayload(userType, numberOfUsers, numberOfCustomTags)
            else:
                payload = construct.constructAddRecipientPayloadForOldUsers(userType, numberOfUsers, numberOfCustomTags)
        else:
            Logger.log('Constructing Payload as a Generic Way :', payloadData)
            payload = construct.constructBody(payloadData, process, 'addrecipient')
         
        response = Utils.makeRequest(url=addRecipientConstructedEndPoint, data=payload, auth=construct.constructAuthenticate(), headers=construct.constructHeaders(), method='POST')
        return construct.constructResponse(response), payload
    
    @staticmethod
    def assertAddRecipient(response, expectedStatusCode, expectedErrorCode=999999, expectedErrorMessage=''):
        Logger.log('Response sent to be asserted :', response)
        if response['constructed'].lower() == 'pass':
            if expectedStatusCode >= 200 and expectedStatusCode <= 300: 
                Assertion.constructAssertion(response['statusCode'] == int(expectedStatusCode), 'Matching Status Code, actual :{} and expected :{}'.format(response['statusCode'], int(expectedStatusCode)))
                Assertion.constructAssertion(response['json']['entity']['test'] >= 0, 'Test users should always be greater than 0')
                Assertion.constructAssertion(response['json']['entity']['control'] >= 0, 'Control users shouod always be greater than 0')
                if len(response['json']['warnings']) > 0:
                    Logger.log('There was a Warning while Creating Campaign :', response['json']['warnings'])
            else:
                errorReturned = response['json']['errors'][0]
                Logger.log('Validating Failed Request Data as Expected:', errorReturned)
                Assertion.constructAssertion(response['statusCode'] == int(expectedStatusCode), 'Matching Status Code, actual :{} and expected :{}'.format(response['statusCode'], int(expectedStatusCode)))
                Assertion.constructAssertion(errorReturned['code'] == expectedErrorCode, 'Matching Error Code ,actual:{} and expected:{}'.format(errorReturned['code'], expectedErrorCode))
                Assertion.constructAssertion(errorReturned['status'] == False, 'Error Status should always be false')
                Assertion.constructAssertion(errorReturned['message'] == expectedErrorMessage, 'Matching Error Message ,actual:{} and expected :{}'.format(errorReturned['message'], expectedErrorMessage))         
        else:
            Assertion.constructAssertion(False, 'Constructed Body has Failed due to Exception so no Validation')
    
    @staticmethod
    def assertAddRecipientDbCalls(addRecipientresponse, payload, createListResponse, campaignId, bucketId, groupVersionDetail, userType):
        userType = str(userType.split(',')[0])
        hashId = ''
        if userType.lower() == 'mobile':
            hashId = dbCallsList.getHashLookUp()['INSTORE__DEFAULT__MOBILE']
        elif userType.lower() == 'email':
            hashId = dbCallsList.getHashLookUp()['INSTORE__DEFAULT__EMAIL']
        
        testControlType = campaignList.assertTestControlUsers(addRecipientresponse, payload, campaignId, userType)
        campaignList.assertGroupVersionDetail(dbCallsList.getGroupVersionDetailsWithGroupId(createListResponse['json']['entity']['listId']), testConstrolType=testControlType, expectedTestUsers=int(addRecipientresponse['json']['entity']['test']), expectedControlUsers=int(addRecipientresponse['json']['entity']['control']))
        if addRecipientresponse['json']['entity']['test'] > 0:
            campaignList.assertCampaignGroupRecipient(addRecipientresponse, 'test', bucketId, groupVersionDetail['TEST']['id'], hashId, 'SUBSCRIBED')
            if 'customTag' in payload['schema']:
                campaignList.assertCampaignGroupRecipientCustomTag(payload, addRecipientresponse, bucketId, groupVersionDetail['TEST']['id'])
        if addRecipientresponse['json']['entity']['control'] > 0:
            campaignList.assertCampaignGroupRecipient(addRecipientresponse, 'control', bucketId, groupVersionDetail['CONTROL']['id'], hashId, 'SUBSCRIBED')
        
    @staticmethod
    def assertTestControlUsers(response, payload, campaignId, userType):
        data = ''
        listOfUserData = payload['data']
        for eachuser in listOfUserData:
            data = data + "'" + eachuser.split(',')[2] + "'," 
            
        campaignBaseResult = dbCallsCampaign.getCampaignBaseFromCampaignId(campaignId)
        
        if campaignBaseResult['test_control'].lower() == 'skip':
            Logger.log('Asserting Test Control Based on secretA with data :{} of which Test users are :{} and control users are :{} for test Control Type :{}'.format(data, len(data[:len(data) - 1].split(',')), 0, 'SKIP'))
            Assertion.constructAssertion(response['json']['entity']['test'] == len(data[:len(data) - 1].split(',')), 'Matching Test user in SKIP type is equal to size of user Data')
            Assertion.constructAssertion(response['json']['entity']['control'] == 0, 'Matching Control User in case of Skip should always be 0')
        elif campaignBaseResult['test_control'].lower() == 'custom':
            data = data[:len(data) - 1] 
            numberOfTestUsers = int(round(len(data.split(',')) * int(campaignBaseResult['test_percentage']) * 0.01))
            numberOfControlUsers = len(data.split(',')) - numberOfTestUsers
            Logger.log('Based on Calculation as Per Test percentage, number of test Users :{} and control: {}'.format(numberOfTestUsers, numberOfControlUsers))
            Assertion.constructAssertion(response['json']['entity']['test'] == numberOfTestUsers, 'Matching Test user based on Calculation for CUSTOM Type actual :{} and expected :{}'.format(response['json']['entity']['test'], numberOfTestUsers))
            Assertion.constructAssertion(response['json']['entity']['control'] == numberOfControlUsers, 'Matching Control user based on Calculation for CUSTOM Type actual :{} and expected :{}'.format(response['json']['entity']['control'], numberOfControlUsers))
        elif campaignBaseResult['test_control'].lower() == 'org':
            result = dbCallsList.getTestControlBasedOnSecreta(userType, data[:len(data) - 1], 'iris')
            Logger.log('Asserting Test Control Based on secretA with data :{} of which Test users are :{} and control users are :{} for test Control Type :{}'.format(data, result['test'], result['control'], 'ORG'))
            Assertion.constructAssertion(response['json']['entity']['test'] == len(result['test']), 'Matching Test Users as per SecretA Value, actual :{} and expected  :{}'.format(response['json']['entity']['test'], len(result['test'])))
            Assertion.constructAssertion(response['json']['entity']['control'] == len(result['control']), 'Matching Control Users as per SecretA Value, actual :{} and expected :{}'.format(response['json']['entity']['control'], len(result['control'])))
        else:
            Logger.log('Not Able to Assert as TestType is :{}'.format(campaignBaseResult['test_control']))
        
        return campaignBaseResult['test_control']
             
    @staticmethod
    def assertCampaignGroupRecipient(response, testType, bucketId, groupVersionId, hashId, ss_status):
        campaignGroupRecipient = dbCallsList.getCampaignGroupRecipient(bucketId, groupVersionId, testType, hashId)
        Logger.log('Campaign Group Recipient Detail Recieved to Assert :', campaignGroupRecipient)
        Assertion.constructAssertion(response['json']['entity'][testType] == campaignGroupRecipient[hashId]['userCount'] , 'Matching Number of Users Passed and In CGR, actual :{} and expected :{}'.format(response['json']['entity'][testType], campaignGroupRecipient[hashId]['userCount']))
        Assertion.constructAssertion(ss_status == dbCallsList.getReachabilityStatus(campaignGroupRecipient[hashId]['reachability_type_id']) , 'Matching Reachablity Id to be subscribed, actual :{} and expected is name of id:{}'.format(ss_status, campaignGroupRecipient[hashId]['reachability_type_id']))
        
    @staticmethod
    def assertCampaignGroupRecipientCustomTag(payload, addRecipientresponse, bucketId, groupVersionId): 
        campaignGroupRecipientCustomTag = dbCallsList.getCampaignGroupRecipientForCustomTags(bucketId, groupVersionId)
        Logger.log('Campaign Group Recipient Detail Recieved to Assert :', campaignGroupRecipientCustomTag)
        LengthOfCustomTags = 1
        customTagsValueToMatch = {}
        for eachSchemaValue in payload['schema'].split(','):
            if 'customTag' in eachSchemaValue:
                 customTagsValueToMatch['custom_tag_' + str(LengthOfCustomTags)] = 'tag' + str(LengthOfCustomTags)
                 LengthOfCustomTags = LengthOfCustomTags + 1
        Assertion.constructAssertion(len(campaignGroupRecipientCustomTag) == 1, 'Matching For The Same GroupVersionId all CustomTags Value should be same in case of Automation Created')
        Assertion.constructAssertion(json.loads(campaignGroupRecipientCustomTag[0][0]) == customTagsValueToMatch, 'Custom tag Value in CGR :{} and Validating with :{}'.format(campaignGroupRecipientCustomTag[0][0], customTagsValueToMatch))
        Assertion.constructAssertion(int(addRecipientresponse['json']['entity']['test']) == int(campaignGroupRecipientCustomTag[0][1]), 'Matching Number of users in CGR in payload :{} and in DB :{} '.format(len(payload['data']), int(campaignGroupRecipientCustomTag[0][1])))   
   
    @staticmethod
    def assertInvalidDataInListResponse(responseData, passedInvalidData, reason):
        invalidDate = None
        if 'recipientsResponse' in responseData['json']['entity']:
            invalidDate = responseData['json']['entity']['recipientsResponse']['invalidData']
        else:
            invalidDate = responseData['json']['entity']['invalidData']
        
        Logger.log('Invalid Data :{} and passedData to be matched :{}'.format(invalidDate, passedInvalidData))
        reason_invalidData = invalidDate['reasons']
        Logger.log('Complete Reason for Invalid Data :', reason_invalidData)
        Assertion.constructAssertion(len(reason) == len(reason_invalidData), 'Matching number Of Reasons :{} with number of reasons in response:{}'.format(len(reason), len(reason_invalidData)))
        
        for eachReason in reason:
            totalNumberOfCounts = 0
            Logger.log('Checking For Reason :', eachReason)
            for eachData in invalidDate['reasons'][eachReason]['data']:
                totalNumberOfCounts = totalNumberOfCounts + len(invalidDate['reasons'][eachReason]['data'][eachData])
                Assertion.constructAssertion(len(passedInvalidData) == len(invalidDate['reasons'][eachReason]['data'][eachData]), 'Matching Length of InvalidData:{} inside Reason :{}'.format(len(passedInvalidData), eachReason))
            
            Assertion.constructAssertion(int(invalidDate['reasons'][eachReason]['count']) == totalNumberOfCounts, 'Matching Count Key For Reason : {} and total Count :{}'.format(eachReason, totalNumberOfCounts))
         
    """ @mergeList """
    
    @staticmethod
    def mergeList(payloadData={}, campaignId=None, campaignType=['LIVE', 'ORG', 'List', 'TAGS', 0], userType='mobile', numberOfUsers=1, numberOfCustomTags=0, newUser=True, process='update'):    
        campaignList.updateRechabilityBeforeEachRun() 
        campaignDefault = constant.campaignDefaultValues
        if campaignId == None:    
            campaignIdValue = constant.campaignDefaultValues[campaignType[0]][campaignType[1]]['Value']
            if len(campaignIdValue['response']) == 0 and len(campaignIdValue['payload']) == 0:
                response, payload = campaigns.createCampaign({}, campaignTypeParams=[campaignType[0], campaignType[1]])   
                if response['statusCode'] == 200:
                    campaignId = response['json']['entity']['campaignId']
                else:
                    Assertion.constructAssertion(False, 'Error : While Creating Campaign , Status Code : {}'.format(response['statusCode']))
            else :
                campaignId = campaignIdValue['response']['json']['entity']['campaignId']
               
        Logger.log('CamapaignId getting used to create list :', campaignId)
        
        createListConstructedEndPoint = construct.constructUrl('mergelist').replace('{campaignId}', str(campaignId))
        payload = {}
        if len(payloadData) == 0:
            payload = construct.constructMergeListBody(userType, numberOfUsers, numberOfCustomTags, newUser)
        else:
            payload = construct.constructBody(payloadData, process, 'mergelist')
        
        response = Utils.makeRequest(url=createListConstructedEndPoint, data=payload, auth=construct.constructAuthenticate(), headers=construct.constructHeaders(), method='POST')
        return construct.constructResponse(response), payload, campaignId
   
    @staticmethod
    def assertMergeList(response, expectedStatusCode, expectedErrorCode=999999, expectedErrorMessage=''):
        Logger.log('Response sent to be asserted :', response)
        if response['constructed'].lower() == 'pass':
            if expectedStatusCode >= 200 and expectedStatusCode <= 300: 
                Assertion.constructAssertion(response['statusCode'] == int(expectedStatusCode), 'Matching Status Code, actual :{} and expected :{}'.format(response['statusCode'], int(expectedStatusCode)))
                Assertion.constructAssertion(response['json']['entity']['recipientsResponse']['test'] >= 0, 'Test users should always be greater than 0')
                Assertion.constructAssertion(response['json']['entity']['recipientsResponse']['control'] >= 0, 'Control users shouod always be greater than 0')
                Assertion.constructAssertion('invalidData' in response['json']['entity']['recipientsResponse'], 'Checking invalidData Json is present in Response')
                if len(response['json']['warnings']) > 0:
                    Logger.log('There was a Warning while Creating Campaign :', response['json']['warnings'])
            else:
                errorReturned = response['json']['errors'][0]
                Logger.log('Validating Failed Request Data as Expected:', errorReturned)
                Assertion.constructAssertion(response['statusCode'] == int(expectedStatusCode), 'Matching Status Code, actual :{} and expected :{}'.format(response['statusCode'], int(expectedStatusCode)))
                Assertion.constructAssertion(errorReturned['code'] == expectedErrorCode, 'Matching Error Code ,actual:{} and expected:{}'.format(errorReturned['code'], expectedErrorCode))
                Assertion.constructAssertion(errorReturned['status'] == False, 'Error Status should always be false')
                Assertion.constructAssertion(errorReturned['message'] == expectedErrorMessage, 'Matching Error Message ,actual:{} and expected :{}'.format(errorReturned['message'], expectedErrorMessage))         
        else:
            Assertion.constructAssertion(False, 'Constructed Body has Failed due to Exception so no Validation')
    
    @staticmethod
    def updateRechabilityBeforeEachRun():
        # WARNING : DONT CHANGE ANYLINE IN THIS MEHTOD , SUPER CRITICAL
        if constant.config['cluster'].lower() == 'nightly' or constant.config['cluster'].lower() == 'staging':
            Logger.log('Cluster Running is :{} , so updating Reachability Table for Each Run'.format(constant.config['cluster'].lower()))
            dbCallsList.updateReachabilityJobs()
