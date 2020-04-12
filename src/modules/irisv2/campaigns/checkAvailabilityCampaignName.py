import json, time

from src.Constant.constant import constant
from src.modules.irisv2.helper.irisHelper import IrisHelper
from src.utilities.assertion import Assertion
from src.utilities.logger import Logger
from src.utilities.utils import Utils

class CheckCampaignAvailabilty():

	@staticmethod
	def checkExists(campaignName):
		checkExistsEndpoint = IrisHelper.constructUrl('checkcampaignexists').replace('{name}', campaignName)
		response = Utils.makeRequest(url=checkExistsEndpoint, data='',auth=IrisHelper.constructAuthenticate(), headers=IrisHelper.constructHeaders(), method='GET')
		return IrisHelper.constructResponse(response)

	@staticmethod
	def assertCheckExists(response, expectedStatusCode, isExists=True, expectedErrorCode=[], expectedErrorMessage=[]):
		if response['constructed'].lower() == 'pass':
			if expectedStatusCode >= 200 and expectedStatusCode <= 300: 
			    Assertion.constructAssertion(response['statusCode'] == int(expectedStatusCode), 'Matching statusCode actual :{},expected :{}'.format(response['statusCode'], expectedStatusCode))
			    Assertion.constructAssertion(response['json']['entity'] == isExists, 'isExists value in actual :{} and expected :{}'.format(response['json']['entity'], isExists))
			    if len(response['json']['warnings']) > 0:
			        Logger.log('There was a Warning while Creating Campaign :', response['json']['warning'])
			else:
			    for errorReturned in response['json']['errors']:
			        Logger.log('Status Code :{} and error :{}', response['statusCode'], errorReturned)
			        Assertion.constructAssertion(response['statusCode'] == int(expectedStatusCode), 'Matching statusCode actual :{},expected :{}'.format(response['statusCode'], expectedStatusCode))
			        Assertion.constructAssertion(errorReturned['code'] in expectedErrorCode, 'Matching Error Code ,actual:{} and expected:{}'.format(errorReturned['code'], expectedErrorCode))
			        Assertion.constructAssertion(errorReturned['status'] == False, 'Checking for Error Status as False')
			        Assertion.constructAssertion(errorReturned['message'] in expectedErrorMessage, 'Matching Error Message ,actual:{} and expected'.format(errorReturned['message'], expectedErrorMessage))          
		else:
		    Assertion.constructAssertion(False, 'Constructed Body has Failed due to Exception so no Validation')