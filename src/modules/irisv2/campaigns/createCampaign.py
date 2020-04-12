import copy
import time

from src.Constant.constant import constant
from src.modules.irisv2.helper.irisHelper import IrisHelper
from src.utilities.assertion import Assertion
from src.utilities.logger import Logger
from src.utilities.utils import Utils


class CreateCampaign():
    @staticmethod
    def create(campaignType, testControlType, payload=None, startDate=None, endDate=None, description=None,
               testControlPercentage=None, name=None, updateNode=False, lockNode=False):
        if not CreateCampaign.checkCampaignAvialable(campaignType, testControlType) or updateNode:
            endpoint = IrisHelper.constructUrl('createcampaign')
            payload = CreateCampaign.constructPayload(campaignType, startDate, endDate, description, testControlType,
                                                      testControlPercentage, name) if payload is None else payload
            response = IrisHelper.constructResponse(
                Utils.makeRequest(url=endpoint, data=payload, auth=IrisHelper.constructAuthenticate(),
                                  headers=IrisHelper.constructHeaders(), method='POST')
            )
            if response['statusCode'] == 200:
                CreateCampaign.validateCreateCampaign(response)
                if not lockNode: CreateCampaign.updateNodeCampaign(campaignType, testControlType,
                                                                   response['json']['entity']['campaignId'],
                                                                   payload['name'], payload)
                if campaignType == 'LAPSED': time.sleep(25)  # Wait to make Campaign Lapsed
                return {
                    'ID': response['json']['entity']['campaignId'],
                    'NAME': payload['name'],
                    'PAYLOAD': payload
                }
            else:
                return {
                    'RESPONSE': response,
                    'PAYLOAD': payload
                }
        else:
            return constant.config['node'][campaignType][testControlType]['CAMPAIGN']

    @staticmethod
    def edit(campaignInfo,editInfo):
        payload = copy.deepcopy(campaignInfo['PAYLOAD'])
        payload.update(editInfo)
        endpoint = IrisHelper.constructUrl('editcampaign').replace('{campaignId}',str(campaignInfo['ID']))
        response = IrisHelper.constructResponse(
            Utils.makeRequest(url=endpoint, data=payload, auth=IrisHelper.constructAuthenticate(),
                              headers=IrisHelper.constructHeaders(), method='PUT')
        )
        return {
            'PAYLOAD':payload,
            'RESPONSE' : response
        }

    @staticmethod
    def checkCampaignAvialable(campaignType, testControlType):
        if constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'] is None or \
                        constant.config['node'][campaignType][testControlType]['CAMPAIGN']['NAME'] is None:
            return False
        else:
            return True

    @staticmethod
    def constructPayload(campaignType, startDate=None, endDate=None, description=None, testControlType=None,
                         testControlPercentage=None, name=None):
        payload = dict()
        payload['startDate'] = CreateCampaign.getStartDate(campaignType) if startDate is None else startDate
        payload['endDate'] = CreateCampaign.getEndDate(campaignType) if endDate is None else endDate
        payload['description'] = 'Iris V2 Automation Created' if description is None else description
        payload['name'] = 'IrisV2_Auto_{}_{}'.format(payload['startDate'], payload['endDate']) if name is None else name

        payload['testControl'] = {
            'type': 'ORG' if testControlType is None else testControlType,
            'testPercentage': 90 if testControlPercentage is None else testControlPercentage
        }
        if payload['testControl']['type'] in ['ORG','SKIP']: payload['testControl'].pop('testPercentage')
        return payload

    @staticmethod
    def getStartDate(campaignType):
        if campaignType == 'UPCOMING':
            return int(time.time() * 1000) + 24 * 60 * 60
        else:
            return int(time.time() * 1000)

    @staticmethod
    def getEndDate(campaignType):
        if campaignType == 'UPCOMING':
            return int(time.time() * 1000) + 2 * 24 * 60 * 60 * 1000
        elif campaignType == 'LAPSED':
            return int(time.time() * 1000) + 20500
        else:
            return int(time.time() * 1000) + 24 * 60 * 60 * 1000

    @staticmethod
    def updateNodeCampaign(campaignType, testControlType, campaignId, name, payload):
        CreateCampaign.refreshNode()
        constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'] = campaignId
        constant.config['node'][campaignType][testControlType]['CAMPAIGN']['NAME'] = name
        constant.config['node'][campaignType][testControlType]['CAMPAIGN']['PAYLOAD'] = payload

    @staticmethod
    def refreshNode():
        constant.config.update({'node': copy.deepcopy(constant.node)})

    @staticmethod
    def validateCreateCampaign(response):
        Assertion.constructAssertion('campaignId' in response['json']['entity'], 'CampaignId key in body')
        if len(response['json']['warnings']) > 0: Assertion.constructAssertion(False, 'WARNING : {}'.format(
            response['json']['warnings']), verify=True)

    @staticmethod
    def assertResponse(response, expectedStatusCode, expectedErrorCode=999999, expectedErrorMessage=[]):
        if response['constructed'].lower() == 'pass':
            if expectedStatusCode >= 200 and expectedStatusCode <= 300:
                Assertion.constructAssertion(response['statusCode'] == int(expectedStatusCode),
                                             'Matching statusCode actual :{},expected :{}'.format(
                                                 response['statusCode'], expectedStatusCode))
                if len(response['json']['warnings']) > 0:
                    Logger.log('There was a Warning while Creating Campaign :', response['json']['warning'])
            else:
                Assertion.constructAssertion(response['statusCode'] == int(expectedStatusCode),
                                             'Matching statusCode actual :{},expected :{}'.format(
                                                 response['statusCode'], expectedStatusCode))
                for errorReturned in response['json']['errors']:
                    Logger.log('Status Code :{} and error :{}', response['statusCode'], errorReturned)
                    Assertion.constructAssertion(errorReturned['code'] == expectedErrorCode,
                                                 'Matching Error Code ,actual:{} and expected:{}'.format(
                                                     errorReturned['code'], expectedErrorCode))
                    Assertion.constructAssertion(errorReturned['status'] == False, 'Checking for Error Status as False')
                    Assertion.constructAssertion(errorReturned['message'] in expectedErrorMessage,
                                                 'Matching Error Message ,actual:{} in expected:{}'.format(
                                                     errorReturned['message'], expectedErrorMessage))
        else:
            Assertion.constructAssertion(False, 'Constructed Body has Failed due to Exception so no Validation')
