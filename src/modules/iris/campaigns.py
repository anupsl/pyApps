import json, time
from src.Constant.constant import constant
from src.utilities.logger import Logger
from src.utilities.assertion import Assertion
from src.modules.iris.construct import construct
from src.modules.iris.dbCallsCampaign import dbCallsCampaign
from src.utilities.utils import Utils


class campaigns():

    @staticmethod
    def createCampaign(payloadData={}, process='update', campaignTypeParams=[]):
        if len(campaignTypeParams) != 0:
            campaign = constant.campaignDefaultValues
            response, Payload = {}, {}
            for eachType in campaignTypeParams:
                campaign = campaign[eachType]
            
            if len(campaign['Value']['response']) == 0 or len(campaign['Value']['payload']) == 0:
                if campaignTypeParams[0] == 'LIVE':
                    response, Payload = campaigns.createCampaign({'name':'IRIS_' + str(int(time.time() * 1000000)), 'testControl':{'type' : campaignTypeParams[1], 'test' : 90}, 'goalId':str(constant.irisGenericValues['goalId']), 'objectiveId':str(constant.irisGenericValues['objectiveId'])})
                elif campaignTypeParams[0] == 'UPCOMING':
                    response, Payload = campaigns.createCampaign({'name':'IRIS_' + str(int(time.time() * 1000000)), 'testControl':{'type' : campaignTypeParams[1], 'test' : 90}, 'goalId':str(constant.irisGenericValues['goalId']), 'objectiveId':str(constant.irisGenericValues['objectiveId']), 'startDate':int(time.time() * 1000 + 24 * 60 * 60 * 1000), 'endDate':int(time.time() * 1000 + 24 * 60 * 60 * 2000)})
                elif campaignTypeParams[0] == 'LAPSED':
                    response, Payload = campaigns.createCampaign({'name':'IRIS_' + str(int(time.time() * 1000000)), 'testControl':{'type' : campaignTypeParams[1], 'test' : 90}, 'goalId':str(constant.irisGenericValues['goalId']), 'objectiveId':str(constant.irisGenericValues['objectiveId']), 'startDate':int(time.time() * 1000), 'endDate':int(time.time() * 1000 + 5 * 1000)})
                    time.sleep(6)  # Campaign Created will lapsed in 6 seconds
                Logger.log('Default Value Found -1 and CampaignCreated of type :{} with response :{}'.format(campaignTypeParams, response))
                constant.campaignDefaultValues[campaignTypeParams[0]][campaignTypeParams[1]]['Value'].update({'response':response, 'payload':Payload})
                return response, Payload
            else:
                Logger.log('Returning Campaign Id Directly From Saved Json as :', campaign['Value'])
                return campaign['Value']['response'], campaign['Value']['payload']
        else:
            createCampaignConstructedEndPoint = construct.constructUrl('createcampaign')
            payload = construct.constructBody(payloadData, process, 'createcampaign')
            response = Utils.makeRequest(url=createCampaignConstructedEndPoint, data=payload, auth=construct.constructAuthenticate(), headers=construct.constructHeaders(), method='POST')
            return construct.constructResponse(response), payload
        
    @staticmethod
    def assertCreateCampaign(response, expectedStatusCode, expectedErrorCode=999999, expectedErrorMessage=''):
        Logger.log('Response sent to be asserted :', response)
        if response['constructed'].lower() == 'pass':
            if expectedStatusCode >= 200 and expectedStatusCode <= 300: 
                Assertion.constructAssertion(response['statusCode'] == int(expectedStatusCode), 'Matching statusCode actual :{},expected :{}'.format(response['statusCode'], expectedStatusCode))
                Assertion.constructAssertion(response['json']['entity']['campaignId'] > 0, 'CampaignId should always be greater then zero')
                if len(response['json']['warnings']) > 0:
                    Logger.log('There was a Warning while Creating Campaign :', response['json']['warning'])
            else:
                errorReturned = response['json']['errors'][0]
                Logger.log('Status Code :{} and error :{}', response['statusCode'], errorReturned)
                Assertion.constructAssertion(response['statusCode'] == int(expectedStatusCode), 'Matching statusCode actual :{},expected :{}'.format(response['statusCode'], expectedStatusCode))
                Assertion.constructAssertion(errorReturned['code'] == expectedErrorCode, 'Matching Error Code ,actual:{} and expected:{}'.format(errorReturned['code'], expectedErrorCode))
                Assertion.constructAssertion(errorReturned['status'] == False, 'Checking for Error Status as False')
                Assertion.constructAssertion(errorReturned['message'] == expectedErrorMessage, 'Matching Error Message ,actual:{} and expected'.format(errorReturned['message'], expectedErrorMessage))          
        else:
            Assertion.constructAssertion(False, 'Constructed Body has Failed due to Exception so no Validation')
    
    @staticmethod
    def assertCreateCampaignDBCall(campaignId, payload):
        Logger.log('Asserting on DB for Campaign Id as :', campaignId, ' with payload :', payload)
        campaigns.assertCampaignBase(dbCallsCampaign.getCampaignBaseFromCampaignId(campaignId), payload)
        campaigns.assertTagResult(dbCallsCampaign.getCampaignTagsFromCampaignId(campaignId), payload)
        campaigns.assertObjectiveResult(dbCallsCampaign.getObjectiveMappingIdFromCampaignId(campaignId), payload)
           
    @staticmethod
    def assertCampaignBase(campaignBaseResult, payload):
        if 'name' in payload :Assertion.constructAssertion(campaignBaseResult['name'] == payload['name'], 'Matching CampaignName ,actual :{} and expected :{}'.format(campaignBaseResult['name'], payload['name']))
        if 'campaignType' in payload :Assertion.constructAssertion(campaignBaseResult['type'].lower() == payload['campaignType'].lower(), 'Matching CampaignType, actual :{} and expected :{}'.format(campaignBaseResult['type'].lower(), payload['campaignType'].lower()))
        if 'description' in payload :Assertion.constructAssertion(campaignBaseResult['description'] == payload['description'], 'Matching Campaign Description, actual :{} and expected :{}'.format(campaignBaseResult['description'], payload['description']))
        if 'goalId' in payload :Assertion.constructAssertion(str(campaignBaseResult['campaign_roi_type_id']) == str(payload['goalId']), 'Matching goalid, actual :{} and expected :{}'.format(str(campaignBaseResult['campaign_roi_type_id']), payload['goalId']))
        if 'testControl' in payload :Assertion.constructAssertion(campaignBaseResult['test_control'] == payload['testControl']['type'], 'Matching Test Control Type, actual :{} and expected :{}'.format(campaignBaseResult['test_control'], payload['testControl']['type']))
        if 'gaName' in payload :Assertion.constructAssertion(campaignBaseResult['ga_name'] == payload['gaName'], 'Matching Google Analytics Name, actual :{} and expected :{}'.format(campaignBaseResult['ga_name'], payload['gaName']))
        if 'gaSource' in payload :Assertion.constructAssertion(campaignBaseResult['ga_source_name'] == payload['gaSource'], 'Matching Google Analytics Source Name, actual :{} and expected :{}'.format(campaignBaseResult['ga_source_name'], payload['gaSource']))
        if campaignBaseResult['test_control'].lower() == 'custom':
            if 'testControl' in payload :Assertion.constructAssertion(campaignBaseResult['test_percentage'] == payload['testControl']['test'], 'Matching Test Control Percentage, actual :{} and expected :{}'.format(campaignBaseResult['test_percentage'], payload['testControl']['test']))
        
    @staticmethod
    def assertTagResult(tagsResult, payload):
        Assertion.constructAssertion(tagsResult['tags'] == payload['tags'], 'Matching Tags, actual :{} and expected:{}'.format(tagsResult['tags'], payload['tags']))
    
    @staticmethod
    def assertObjectiveResult(objectiveResult, payload):
        if 'objectiveId' in payload : Assertion.constructAssertion(str(objectiveResult['objective_type_id']) == str(payload['objectiveId']), 'Matching ObjectiveId, actual: {} and expected: {}'.format(str(objectiveResult['objective_type_id']), payload['objectiveId']))
        
    @staticmethod
    def getCampaignById(campaignId=None, queryParam=[]):
        getCampaignConstructedEndPoint = None
        if len(queryParam) > 0:
            getCampaignConstructedEndPoint = construct.constructUrl('getCampaign', queryParam=queryParam).replace('{campaignId}', '')
        else:
            Assertion.constructAssertion(campaignId != None , 'CampaignId and Query param both are None')
            getCampaignConstructedEndPoint = construct.constructUrl('getCampaign').replace('{campaignId}', str(campaignId))
        response = Utils.makeRequest(url=getCampaignConstructedEndPoint, data='', auth=construct.constructAuthenticate(), headers=construct.constructHeaders(), method='GET')
        return construct.constructResponse(response)
    
    @staticmethod
    def assertGetCampaign(response, expectedStatusCode, expectedErrorCode=999999, expectedErrorMessage=''):
        Logger.log('Response sent to be asserted for GetCampaign:', response)
        if response['constructed'].lower() == 'pass':
            if expectedStatusCode >= 200 and expectedStatusCode <= 300: 
                Assertion.constructAssertion(response['statusCode'] == int(expectedStatusCode), 'Matching statusCode actual :{},expected :{}'.format(response['statusCode'], expectedStatusCode))
                Assertion.constructAssertion(len(response['json']['entity']) > 0, 'Length Of Entity should always be greater then zero')
                if len(response['json']['warnings']) > 0:
                    Logger.log('There was a Warning while Creating Campaign :', response['json'].get('warning'))
            else:
                errorReturned = response['json'].get('errors')[0]
                Logger.log('Status Code :{} and error :{}', response['statusCode'], errorReturned)
                Assertion.constructAssertion(response['statusCode'] == int(expectedStatusCode), 'Matching statusCode actual :{},expected :{}'.format(response['statusCode'], expectedStatusCode))
                Assertion.constructAssertion(errorReturned['code'] == expectedErrorCode, 'Matching Error Code ,actual:{} and expected:{}'.format(errorReturned['code'], expectedErrorCode))
                Assertion.constructAssertion(errorReturned['status'] == False, 'Checking for Error Status as False')
                Assertion.constructAssertion(errorReturned['message'] == expectedErrorMessage, 'Matching Error Message ,actual:{} and expected:{}'.format(errorReturned['message'], expectedErrorMessage))          
        else:
            Assertion.constructAssertion(False, 'Constructed Body has Failed due to Exception so no Validation')
    
    @staticmethod
    def assertGetCampaignAll(response, numberOfCampaignsGotCreated, expectedStatusCode, expectedErrorCode=999999, expectedErrorMessage=''):
        Logger.log('Response sent to be asserted for GetCampaign:', response)
        if response['constructed'].lower() == 'pass':
            if expectedStatusCode >= 200 and expectedStatusCode <= 300: 
                Assertion.constructAssertion(response['statusCode'] == int(expectedStatusCode), 'Matching statusCode actual :{},expected :{}'.format(response['statusCode'], expectedStatusCode))
                Assertion.constructAssertion(len(response['json']['data']) >= numberOfCampaignsGotCreated, 'CampaignCreated betweenRange is :{} and campaignRecieved in getCall :{}'.format(numberOfCampaignsGotCreated, len(response['json']['data'])))
                for eachRecord in response['json']['data']:
                    Assertion.constructAssertion(eachRecord['startDate'] >= constant.getCampaignAll.get('upcomingStartDate'), 'Matching startDate of Response is within given range')
                    Assertion.constructAssertion(eachRecord['endDate'] <= constant.getCampaignAll.get('upcomingEndDate'), 'Matching endDate of Response is within given range')
                if len(response['json']['warnings']) > 0:
                    Logger.log('There was a Warning while Creating Campaign :', response['json'].get('warning'))
            else:
                errorReturned = response['json'].get('errors')[0]
                Logger.log('Status Code :{} and error :{}', response['statusCode'], errorReturned)
                Assertion.constructAssertion(response['statusCode'] == int(expectedStatusCode), 'Matching statusCode actual :{},expected :{}'.format(response['statusCode'], expectedStatusCode))
                Assertion.constructAssertion(errorReturned['code'] == expectedErrorCode, 'Matching Error Code ,actual:{} and expected:{}'.format(errorReturned['code'], expectedErrorCode))
                Assertion.constructAssertion(errorReturned['status'] == False, 'Checking for Error Status as False')
                Assertion.constructAssertion(errorReturned['message'] == expectedErrorMessage, 'Matching Error Message ,actual:{} and expected:{}'.format(errorReturned['message'], expectedErrorMessage))          
        else:
            Assertion.constructAssertion(False, 'Constructed Body has Failed due to Exception so no Validation')
    
    @staticmethod
    def assertGetCampaignWithPassedLimit(alldataInRange, dataWithLimit, startFrom, endTo):
        eachDataWithIndex = (each for each in dataWithLimit)
        while startFrom < endTo:
            Assertion.constructAssertion(alldataInRange[startFrom] == eachDataWithIndex.next(), 'Matching each Json with Limit')
            startFrom += 1
    
    @staticmethod
    def assertGetCampaignDBCall(response, campaignId):
        Assertion.constructAssertion(response['json']['entity']['id'] == campaignId, 'Matching Id of Response : {} and passed campaignId : {} are same'.format(response['json']['entity']['id'], campaignId))
        campaignBaseResult = dbCallsCampaign.getCampaignBaseFromCampaignId(campaignId)
        campaigns.assertCampaignBase(campaignBaseResult, response['json']['entity'])
        campaigns.assertTestControlRatiobasedOnTestType(campaignBaseResult['test_control'], campaignBaseResult.get('test_percentage'))
        if 'tags' in response['json']['entity']:
            campaigns.assertTagResult(dbCallsCampaign.getCampaignTagsFromCampaignId(campaignId), response['json']['entity'])
        campaigns.assertObjectiveResult(dbCallsCampaign.getObjectiveMappingIdFromCampaignId(campaignId), response['json']['entity'])
    
    @staticmethod
    def assertTestControlRatiobasedOnTestType(testControlType, test_percentage):
        if testControlType.lower() == 'skip':
            pass
        elif testControlType.lower() == 'org':
            pass
    
    @staticmethod
    def updateCampaign(afterUpdatepayload, campaignType=['LIVE', 'ORG'], campaignId=None, process='update'):
        beforeUpdateResponse, beforeUpdatePayload = {}, {}
        if campaignId == None:
            beforeUpdateResponse, beforeUpdatePayload = campaigns.createCampaign({'name':'IRIS_UPDATE_CAMPAIGN' + str(int(time.time()))}, campaignTypeParams=campaignType)
            campaignId = beforeUpdateResponse['json']['entity']['campaignId']
            Logger.log('CampaignId Recieved : {} for campaignType : {}'.format(campaignId, campaignType))
        
        updateCampaignConstructedEndPoint = construct.constructUrl('updateCampaign').replace('{campaignId}', str(campaignId))
        afterUpdateresponse = Utils.makeRequest(url=updateCampaignConstructedEndPoint, data=afterUpdatepayload, auth=construct.constructAuthenticate(), headers=construct.constructHeaders(), method='PUT')
        if afterUpdateresponse.status_code == 200:
            beforeUpdatePayload.update(afterUpdatepayload)
            constant.campaignDefaultValues[campaignType[0]][campaignType[1]]['Value'].update({'payload':beforeUpdatePayload})
                 
        return construct.constructResponse(afterUpdateresponse), beforeUpdateResponse, afterUpdatepayload, beforeUpdatePayload
    
    @staticmethod
    def assertUpdateCampaign(afterUpdateResponse, beforeUpdateResponse, expectedStatusCode, expectedErrorCode=999999, expectedErrorMessage=''):
        Logger.log('Before Update Response was :{} and after Update Response is :{}'.format(beforeUpdateResponse, afterUpdateResponse))
        if afterUpdateResponse['constructed'].lower() == 'pass':
            if expectedStatusCode >= 200 and expectedStatusCode <= 300: 
                Assertion.constructAssertion(afterUpdateResponse['statusCode'] == int(expectedStatusCode), 'Matching statusCode actual :{},expected :{}'.format(afterUpdateResponse['statusCode'], expectedStatusCode))
                Assertion.constructAssertion(afterUpdateResponse['json']['entity']['campaignId'] > 0, 'CampaignId should always be greater then zero')
                Assertion.constructAssertion(afterUpdateResponse['json']['entity']['campaignId'] == beforeUpdateResponse['json']['entity']['campaignId'], 'CampaignId in afterUpdate call and createCampaign Call are :{},{} '.format(afterUpdateResponse['json']['entity']['campaignId'], beforeUpdateResponse['json']['entity']['campaignId']))
                if len(afterUpdateResponse['json']['warnings']) > 0:
                    Logger.log('There was a Warning while Creating Campaign :', afterUpdateResponse['json']['warnings'])
            else:
                errorReturned = afterUpdateResponse['json'].get('errors')[0]
                Logger.log('Status Code :{} and error :{}', afterUpdateResponse['statusCode'], errorReturned)
                Assertion.constructAssertion(afterUpdateResponse['statusCode'] == int(expectedStatusCode), 'Matching statusCode actual :{},expected :{}'.format(afterUpdateResponse['statusCode'], expectedStatusCode))
                Assertion.constructAssertion(errorReturned['code'] == expectedErrorCode, 'Matching Error Code ,actual:{} and expected:{}'.format(errorReturned['code'], expectedErrorCode))
                Assertion.constructAssertion(errorReturned['status'] == False, 'Checking for Error Status as False')
                Assertion.constructAssertion(errorReturned['message'].strip() == expectedErrorMessage.strip(), 'Matching Error Message ,actual:{} and expected:{}'.format(errorReturned['message'], expectedErrorMessage))          
        else:
            Assertion.constructAssertion(False, 'Constructed Body has Failed due to Exception so no Validation')
    
    @staticmethod
    def assertUpdateCampaignDBCall(payload, campaignId):
        Logger.log('DB Assertion for UpdateCampaign with payload :{}'.format(payload))
        campaignBaseResult = dbCallsCampaign.getCampaignBaseFromCampaignId(campaignId)
        Logger.log('campaignBaseResult :{}'.format(campaignBaseResult))
        campaigns.assertCampaignBase(campaignBaseResult, payload)
        if 'tags' in payload:
            campaigns.assertTagResult(dbCallsCampaign.getCampaignTagsFromCampaignId(campaignId), payload)
        campaigns.assertObjectiveResult(dbCallsCampaign.getObjectiveMappingIdFromCampaignId(campaignId), payload)
    
