import copy
import time
from datetime import datetime

import pytest

from src.Constant.constant import constant
from src.modules.irisv2.campaigns.campaignCheckDBAssertion import CampaignCheckDBAssertion
from src.modules.irisv2.campaigns.createCampaign import CreateCampaign
from src.modules.irisv2.helper.irisHelper import IrisHelper
from src.utilities.assertion import Assertion
from src.utilities.logger import Logger
from src.utilities.utils import Utils


@pytest.mark.run(order=1)
class Test_createCampaigns():
    def setup_method(self, method):
        Logger.logMethodName(method.__name__)

    @pytest.mark.parametrize('campaignType,testControlType', [
        ('LIVE', 'ORG'),

    ])
    def test_irisV2_createCampaign_Sanity(self, campaignType, testControlType):
        campaignInfo = CreateCampaign.create(campaignType, testControlType)
        CampaignCheckDBAssertion(campaignInfo['ID'], campaignInfo['PAYLOAD']).check()

    @pytest.mark.parametrize('campaignType,testControlType', [

        ('LIVE', 'SKIP'),
        ('LIVE', 'CUSTOM'),
    ])
    def test_irisV2_createCampaign(self, campaignType, testControlType):
        campaignInfo = CreateCampaign.create(campaignType, testControlType)
        CampaignCheckDBAssertion(campaignInfo['ID'], campaignInfo['PAYLOAD']).check()

    @pytest.mark.parametrize('campaignType,testControlType', [
        ('UPCOMING', 'ORG'),
        ('UPCOMING', 'SKIP'),
        ('UPCOMING', 'CUSTOM'),
        ('LAPSED', 'ORG'),
        ('LAPSED', 'SKIP'),
        ('LAPSED', 'CUSTOM')
    ])
    def test_irisV2_createCampaign_OtherTypes(self, campaignType, testControlType):
        campaignInfo = CreateCampaign.create(campaignType, testControlType)
        CampaignCheckDBAssertion(campaignInfo['ID'], campaignInfo['PAYLOAD']).check()

    def test_irisV2_createCampaign_WithStartTime_now(self):
        campaignInfo = CreateCampaign.create('LIVE', 'ORG', startDate=int(time.time() * 1000), updateNode=True,
                                             lockNode=True)
        CampaignCheckDBAssertion(campaignInfo['ID'], campaignInfo['PAYLOAD']).check()

    @pytest.mark.parametrize('campaignType,testControlType,testPercentage', [
        ('LIVE', 'CUSTOM', 100),
        ('LIVE', 'CUSTOM', 1),
        ('LIVE', 'CUSTOM', 0),
    ])
    def test_irisV2_createCampaign_differentTestPercentageCustom(self, campaignType, testControlType, testPercentage):
        campaignInfo = CreateCampaign.create('LIVE', 'CUSTOM', testControlPercentage=testPercentage, updateNode=True,
                                             lockNode=True)
        CampaignCheckDBAssertion(campaignInfo['ID'], campaignInfo['PAYLOAD']).check()

    def test_irisV2_createCampaign_withSameStartAndEndDate(self):
        startAndEndtime = int(time.time() * 1000) + 20000
        campaignInfo = CreateCampaign.create('LIVE', 'ORG', startDate=startAndEndtime, endDate=startAndEndtime,
                                             updateNode=True, lockNode=True)
        CreateCampaign.assertResponse(campaignInfo['RESPONSE'], 400, 1006,
                                      'Campaign Date Exception : Campaign end date is less or equal than start date')

    def test_irisV2_createCampaign_ProdSanity_withStartDateLessThanToday(self):
        campaignInfo = CreateCampaign.create('LIVE', 'ORG', startDate=int(time.time() * 1000) - 24 * 60 * 60 * 1000,
                                             updateNode=True, lockNode=True)
        Assertion.constructAssertion(campaignInfo['RESPONSE']['statusCode'] == 400,
                                     'Status Code is :{}'.format(campaignInfo['RESPONSE']['statusCode']))
        Assertion.constructAssertion(campaignInfo['RESPONSE']['json']['errors'][0]['code'] == 1006,
                                     'ErrorCode is :{} and expected :104'.format(
                                         campaignInfo['RESPONSE']['json']['errors'][0]['code']))
        Assertion.constructAssertion('Campaign Date Exception : Campaign start date is less than current date' in
                                     campaignInfo['RESPONSE']['json']['errors'][0]['message'],
                                     'Actual Message :{}'.format(
                                         campaignInfo['RESPONSE']['json']['errors'][0]['message']))

    def test_irisV2_createCampaign_ProdSanity_withStartDateGreaterThanEndDate(self):
        startDate = int(time.time() * 1000) + 2 * 24 * 60 * 60 * 1000
        endDate = int(time.time() * 1000) + 24 * 60 * 60 * 1000
        campaignInfo = CreateCampaign.create('LIVE', 'ORG', startDate=startDate, endDate=endDate, updateNode=True,
                                             lockNode=True)
        CreateCampaign.assertResponse(campaignInfo['RESPONSE'], 400, 1006,
                                      'Campaign Date Exception : Campaign end date is less or equal than start date')

    def test_irisV2_createCampaign_ProdSanity_campaignWithSameName(self):
        campaignInfo = CreateCampaign.create('LIVE', 'ORG', updateNode=True, lockNode=True)
        campaignInfo = CreateCampaign.create('LIVE', 'ORG', name=campaignInfo['NAME'], updateNode=True, lockNode=True)
        CreateCampaign.assertResponse(campaignInfo['RESPONSE'], 400, 1003,
                                      'Campaign Name Exception : Campaign Name already exists')


    @pytest.mark.parametrize('campaignType,testControlType,keyPop,statusCode,errorCode,errorDesc', [
        ('LIVE', 'ORG', 'testControl', 400, 102, 'Invalid request : TestControlV2 is required. '),
        ('LIVE', 'ORG', 'name', 400, 102, 'Invalid request : Campaign name is required. '),
        ('LIVE', 'ORG', 'startDate', 400, 102, 'Invalid request : Campaign start date is required. '),
        ('LIVE', 'ORG', 'endDate', 400, 102, 'Invalid request : Campaign end date is required. '),
    ])
    def test_irisV2_createCampaign_KeyPop_invalidJson_missingRequiredKeys(self, campaignType, testControlType, keyPop,
                                                                          statusCode, errorCode, errorDesc):
        payload = copy.deepcopy(constant.payload['createcampaignv2'])
        payload.pop(keyPop)
        campaignInfo = CreateCampaign.create(campaignType, testControlType, payload=payload, updateNode=True,
                                             lockNode=True)
        CreateCampaign.assertResponse(campaignInfo['RESPONSE'], statusCode, errorCode, errorDesc)

    def test_irisV2_createCampaign_MissingNonMandatoryField(self):
        payload = copy.deepcopy(constant.payload['createcampaignv2'])
        payload.pop('description')
        payload["testControl"].pop("testPercentage")
        campaignInfo = CreateCampaign.create('LIVE', 'ORG', payload=payload, updateNode=True, lockNode=True)
        CampaignCheckDBAssertion(campaignInfo['ID'], campaignInfo['PAYLOAD']).check()

    @pytest.mark.parametrize('campaignType,testControlType,keyValue,statusCode,errorCode,errorDesc', [
        ('LIVE', 'ORG', {'name': ''}, 400, 102, 'Invalid request : Campaign name is required. '),
        ('LIVE', 'ORG', {'name': 'x' * 51}, 400, 102,
         'Invalid request : Invalid campaign name. Name exceeds 50 characters. '),
        ('LIVE', 'ORG', {'startDate': ''}, 400, 102, ['Invalid request : invalid value for field startDate',
                                                      'Invalid request : Campaign start date is required. ']),
        ('LIVE', 'ORG', {'startDate': datetime.fromtimestamp(int(time.time())).strftime('%Y-%m-%d %H:%M:%S')}, 400, 104,
         ['Invalid data type for : startDate', 'Invalid request : invalid value for field startDate']),
        ('LIVE', 'ORG', {'endDate': ''}, 400, 102,
         ['Invalid request : invalid value for field endDate', 'Invalid request : Campaign end date is required. ']),
        ('LIVE', 'ORG', {'endDate': datetime.fromtimestamp(int(time.time())).strftime('%Y-%m-%d %H:%M:%S')}, 400, 104,
         'Invalid request : invalid value for field endDate'),
        ('LIVE', 'ORG', {'description': 'Description' * 5000}, 400, 102,
         ['Invalid request : Invalid campaign description. Name exceeds 1000 characters. ',
          'Invalid request : Invalid campaign description.']),
        ('LIVE', 'ORG', {'testControl': {}}, 400, 102, 'Invalid request : Invalid testPercentage control type.'),
        ('LIVE', 'ORG', {'testControl': ''}, 400, 104, 'Invalid request : invalid data type of field testControl'),
        ('LIVE', 'ORG', {'testControl': {'type': 'CUSTOM'}}, 400, 102
         , ['Test control exception : Test percentage is required','Invalid request : test percentage cannot be null']),
        ('LIVE', 'ORG', {'testControl': {'testPercentage': 90}}, 400, 102,
         'Invalid request : Invalid testPercentage control type.'),
        ('LIVE', 'ORG', {'testControl': {'testPercentage': '', 'type': 'CUSTOM'}}, 400, 102
         , ['Test control exception : Test percentage is required','Invalid request : test percentage cannot be null']),
        ('LIVE', 'ORG', {'testControl': {'testPercentage': 'ABC', 'type': 'CUSTOM'}}, 400, 104,
         'Invalid request : invalid value for field testPercentage'),
        ('LIVE', 'ORG', {'testControl': {'testPercentage': 90, 'type': 'CUSTOMER'}}, 400, 102,
         'Invalid request : Invalid testPercentage control type.'),
    ])
    def test_irisV2_createCampaign_InvalidValues(self, campaignType, testControlType, keyValue, statusCode, errorCode,
                                                 errorDesc):
        payload = copy.deepcopy(constant.payload['createcampaignv2'])
        payload.update({'name': 'AutomationNegativeCase_Campaign_{}'.format(int(time.time() * 1000))})
        payload.update(keyValue)
        campaignInfo = CreateCampaign.create(campaignType, testControlType, payload=payload, updateNode=True,
                                             lockNode=True)
        CreateCampaign.assertResponse(campaignInfo['RESPONSE'], statusCode, errorCode, errorDesc)

    @pytest.mark.parametrize('campaignType,testControlType,keyValue,statusCode,errorCode,errorDesc',[('LIVE', 'ORG', {'startDate': int(time.time() * 1000) + 1000 * 1000 * 60 * 60 * 1000,
                         'endDate': int(time.time() * 1000) + 2 * 1000 * 1000 * 60 * 60 * 1000}, 400, 1006,
         'Campaign Date Exception : Campaign start date should not be greater than 20 years')])
    def test_irisV2_createCampaign_Invalid_future(self, campaignType, testControlType, keyValue, statusCode, errorCode,
                                                 errorDesc):
        payload = copy.deepcopy(constant.payload['createcampaignv2'])
        payload.update({'name': 'AutomationNegativeCase_Campaign_{}'.format(int(time.time() * 1000))})
        payload.update(keyValue)
        payload["testControl"].pop("testPercentage")
        campaignInfo = CreateCampaign.create(campaignType, testControlType, payload=payload, updateNode=True,
                                             lockNode=True)
        CreateCampaign.assertResponse(campaignInfo['RESPONSE'], statusCode, errorCode, errorDesc)



    def test_irisV2_createCampaign_PostWithEmptyJson(self):
        campaignInfo = CreateCampaign.create('LIVE', 'ORG', payload={}, updateNode=True, lockNode=True)
        CreateCampaign.assertResponse(campaignInfo['RESPONSE'], 400, 102,
                                      ['Invalid request : Campaign name is required. ',
                                       'Invalid request : TestControlV2 is required. ',
                                       'Invalid request : Campaign start date is required. ',
                                       'Invalid request : Campaign end date is required. '])

    def test_irisV2_createCampaign_AllFieldsAsEmpty(self):
        payload = {
            'startDate': '',
            'endDate': '',
            'name': '',
            'testControl': ''
        }
        campaignInfo = CreateCampaign.create('LIVE', 'ORG', payload=payload, updateNode=True, lockNode=True)
        Assertion.constructAssertion(campaignInfo['RESPONSE']['statusCode'] == 400,
                                     'Status Code is :{}'.format(campaignInfo['RESPONSE']['statusCode']))
        Assertion.constructAssertion(campaignInfo['RESPONSE']['json']['errors'][0]['code'] == 104,
                                     'ErrorCode is :{} and expected :104'.format(
                                         campaignInfo['RESPONSE']['json']['errors'][0]['code']))
        Assertion.constructAssertion(campaignInfo['RESPONSE']['json']['errors'][0]['message'] in [
            'Invalid request : invalid data type of field testControl', 'Invalid data type for : testControl',
            'Invalid data type for : name', 'Invalid data type for : endDate',
            'invalid data type of field testControl '],
                                     'Error Message is :{} and expected is :Invalid Data Type for :...>> Verification Enabled'.format(
                                         campaignInfo['RESPONSE']['json']['errors'][0]['message']), verify=True)

    def test_irisV2_createCampaign_SomeExtraParamInPayload(self):
        payload = copy.deepcopy(constant.payload['createcampaignv2'])
        payload.update({'extraParam': 'SomeValue'})
        campaignInfo = CreateCampaign.create('LIVE', 'ORG', payload=payload, updateNode=True, lockNode=True)
        CreateCampaign.assertResponse(campaignInfo['RESPONSE'], 400, 107, 'Unrecognized field : extraParam')

    def test_irisV2_createCampaign_WrongOrgId(self):
        previousOrgId = None
        try:
            payload = copy.deepcopy(constant.payload['createcampaignv2'])
            previousOrgId = IrisHelper.updateOrgId(-1)
            campaignInfo = CreateCampaign.create('LIVE', 'ORG', payload=payload, updateNode=True, lockNode=True)
            CreateCampaign.assertResponse(campaignInfo['RESPONSE'], 401, 999999, 'Invalid org id')
        except Exception, exp:
            Assertion.constructAssertion(False, 'Exception :{}'.format(exp))
        finally:
            if previousOrgId is not None: IrisHelper.updateOrgId(int(previousOrgId))

    def test_irisV2_createCampaign_WrongAuth(self):
        previousUserName = None
        try:
            payload = copy.deepcopy(constant.payload['createcampaignv2'])
            previousUserName = IrisHelper.updateUserName('WrongName')
            campaignInfo = CreateCampaign.create('LIVE', 'ORG', payload=payload, updateNode=True, lockNode=True)
            CreateCampaign.assertResponse(campaignInfo['RESPONSE'], 401, 999999, 'Unauthorized')
        except Exception, exp:
            Assertion.constructAssertion(False, 'Exception :{}'.format(exp))
        finally:
            if previousUserName is not None: IrisHelper.updateUserName(previousUserName)

    @pytest.mark.parametrize('campaignName', [
        ('Automation_!@#$%^&*()_+=[:::><?/\|_{}'.format(int(time.time())))
    ])
    def test_irisV2_createCampaign_validNamesOfCampaign(self, campaignName):
        payload = copy.deepcopy(constant.payload['createcampaignv2'])
        payload.update({'name': campaignName})
        payload["testControl"].pop("testPercentage")
        campaignInfo = CreateCampaign.create('LIVE', 'ORG', payload=payload, updateNode=True,
                                             lockNode=True)
        CampaignCheckDBAssertion(campaignInfo['ID'], campaignInfo['PAYLOAD']).check()

    def test_irisV2_createCampaign_CT_AsNull(self):
        payload = copy.deepcopy(constant.payload['createcampaignv2'])
        payload.update({'name': 'CT_AsNull_{}'.format(int(time.time()))})
        payload['testControl'].pop("testPercentage")
        header = IrisHelper.constructHeaders()
        header.update({'X-CAP-CT':None})
        response = IrisHelper.constructResponse(
            Utils.makeRequest(url=IrisHelper.constructUrl('createcampaign'), data=payload, auth=IrisHelper.constructAuthenticate(),
                              headers=header, method='POST')
        )
        CreateCampaign.assertResponse(response,200)

    def test_irisV2_createCampaign_Auth_AsNull(self):
        payload = copy.deepcopy(constant.payload['createcampaignv2'])
        payload.update({'name': 'Auth_AsEmpty_{}'.format(int(time.time()))})
        header = IrisHelper.constructHeaders()
        header.update({'X-CAP-CT':None})
        response = IrisHelper.constructResponse(
            Utils.makeRequest(url=IrisHelper.constructUrl('createcampaign'), data=payload, auth=(),
                              headers=header, method='POST')
        )
        CreateCampaign.assertResponse(response,401,999999, 'Could not authenticate user due to missing credentials.')

    @pytest.mark.parametrize('campaignType,testControlType', [
        ('LIVE', 'ORG'),

    ])
    def test_irisV2_createCampaign_objective_Product_Sales(self, campaignType, testControlType):
        payload = copy.deepcopy(constant.payload['createcampaignv2'])
        payload.update({
            "name": "Automation_IRISV2_{}".format(int(time.time() * 1000)),
                "objective": {
            "objectiveName": "Product_Sales",
            "value": {"Category Level 1" : ["T-Shirts"], "Color" : ["Blue", "Red"]}
           }
            })
        payload["testControl"].pop("testPercentage")
        campaignInfo = CreateCampaign.create(campaignType, testControlType, payload=payload, updateNode=True,
                                             lockNode=True)
        CampaignCheckDBAssertion(campaignInfo['ID'], campaignInfo['PAYLOAD']).check()




    @pytest.mark.parametrize('campaignType,testControlType,response,errorCode,errorMessage', [
        ('LIVE', 'ORG',400,[1005,104],["Campaign Objective Exception : Specified campaign objective Product_Sales should have a map as value."]),
    ])

    def test_irisV2_createCampaign_objective_Product_Sales_invalidDataType(self, campaignType, testControlType,response,errorCode,errorMessage):
        payload = copy.deepcopy(constant.payload['createcampaignv2'])
        payload.update({
            "name": "Automation_IRISV2_{}".format(int(time.time() * 1000)),
            "objective": {
                "objectiveName": "Product_Sales",
                "value": "Test"
            }
        })
        payload["testControl"].pop("testPercentage")
        campaignInfo = CreateCampaign.create(campaignType, testControlType, payload=payload, updateNode=True,
                                             lockNode=True)
        Assertion.constructAssertion(campaignInfo['RESPONSE']['statusCode']==response,
                                    "Actual code:{} and Expected Code :{}".format(campaignInfo['RESPONSE'],response))
        for errors in campaignInfo["RESPONSE"]["json"]['errors']:
            Assertion.constructAssertion(errors["code"]in errorCode,
                                         "Actual Error Code :{} and Expected Error Code :{}".format(errors["code"],errorCode))

            Assertion.constructAssertion(errors["message"] in errorMessage,
                                         "Actual Error Message :{} and Expected Error Message :{}".format(errors["message"],errorMessage))

    @pytest.mark.parametrize('campaignType,testControlType', [
        ('LIVE', 'ORG'),

    ])
    def test_irisV2_createCampaign_objective_Store_Visit(self, campaignType, testControlType):
        payload = copy.deepcopy(constant.payload['createcampaignv2'])
        payload.update({
            "name": "Automation_IRISV2_{}".format(int(time.time() * 1000)),
            "objective": {
                "objectiveName": "Store_Visit",
                "value": {"name": ["customer"], "number of visit": [10, 20]}
            }
        })
        payload["testControl"].pop("testPercentage")
        campaignInfo = CreateCampaign.create(campaignType, testControlType, payload=payload, updateNode=True,
                                             lockNode=True)
        CampaignCheckDBAssertion(campaignInfo['ID'], campaignInfo['PAYLOAD']).check()

    @pytest.mark.parametrize('campaignType,testControlType,response,errorCode,errorMessage', [
            ('LIVE', 'ORG',400,[1005,104],["Campaign Objective Exception : Specified campaign objective Store_Visit should have a map as value."]),

    ])
    def test_irisV2_createCampaign_objective_Store_Visit_InvalidDataType(self, campaignType, testControlType,response,errorCode,errorMessage):
            payload = copy.deepcopy(constant.payload['createcampaignv2'])
            payload.update({
                "name": "Automation_IRISV2_{}".format(int(time.time() * 1000)),
                "objective": {
                    "objectiveName": "Store_Visit",
                    "value": "test"
                }
            })
            payload["testControl"].pop("testPercentage")

            campaignInfo = CreateCampaign.create(campaignType, testControlType, payload=payload, updateNode=True,
                                                 lockNode=True)
            Assertion.constructAssertion(campaignInfo["RESPONSE"]["statusCode"]==response,
                                         "Actual code :{} and EXpected Code :{}".format(campaignInfo["RESPONSE"],response))
            for errors in campaignInfo["RESPONSE"]["json"]["errors"]:
                Assertion.constructAssertion(errors["code"] in errorCode,
                                             "Actual Code :{} and Expected Code :{}".format(errors["code"],errorCode))
                Assertion.constructAssertion(errors["message"]in errorMessage,
                                             "Actual Error Message :{} and Expected Error Message :{}".format(errors["message"],errorMessage))


    @pytest.mark.parametrize('campaignType,testControlType', [
        ('LIVE', 'ORG'),

    ])
    def test_irisV2_createCampaign_objective_Retention(self, campaignType, testControlType):
        payload = copy.deepcopy(constant.payload['createcampaignv2'])
        payload.update({
            "name": "Automation_IRISV2_{}".format(int(time.time() * 1000)),
            "objective": {
                "objectiveName": "Retention"

        }})
        payload["testControl"].pop("testPercentage")
        campaignInfo = CreateCampaign.create(campaignType, testControlType, payload=payload, updateNode=True,
                                             lockNode=True)

        CampaignCheckDBAssertion(campaignInfo['ID'], campaignInfo['PAYLOAD']).check()

    @pytest.mark.parametrize('campaignType,testControlType,response, errorCode, errorMessage', [
        ('LIVE', 'ORG',400, [104, 1005], ['Campaign Objective Exception : Specified campaign objective Retention does not accept a value.']),

    ])
    def test_irisV2_createCampaign_objective_Retention_withValue(self,campaignType, testControlType, response, errorCode,
                                                                                   errorMessage):
        payload = copy.deepcopy(constant.payload['createcampaignv2'])
        payload.update({
            "name": "Automation_IRISV2_{}".format(int(time.time() * 1000)),
            "objective": {
                "objectiveName": "Retention",
                "value": {"name": ["customer"], "number of visit": [10, 20]}
            }})
        payload["testControl"].pop("testPercentage")

        campaignInfo = CreateCampaign.create(campaignType, testControlType, payload=payload, updateNode=True,
                                             lockNode=True)
        Assertion.constructAssertion(campaignInfo['RESPONSE']['statusCode'] == response,
                                 'Actual code :{} and Expected:{}'.format(campaignInfo['RESPONSE'],
                                                                          response))

        for errors in campaignInfo['RESPONSE']['json']['errors']:
                Assertion.constructAssertion(errors['code'] in errorCode,
                                             'Actual Error Code :{} and Expected :{}'.format(
                                                 errors['code'], errorCode))

                Assertion.constructAssertion(errors['message'] in errorMessage,
                                             'Actual Error message :{} and Expected :{}'.format(
                                                 errors['message'], errorMessage))


    @pytest.mark.parametrize('campaignType,testControlType', [
        ('LIVE', 'ORG'),

    ])
    def test_irisV2_createCampaign_objective_Greetings(self, campaignType, testControlType):
        payload = copy.deepcopy(constant.payload['createcampaignv2'])
        payload.update({
            "name": "Automation_IRISV2_{}".format(int(time.time() * 1000)),
            "objective": {
                "objectiveName": "Greetings"

        }})
        payload["testControl"].pop("testPercentage")
        campaignInfo = CreateCampaign.create(campaignType, testControlType, payload=payload, updateNode=True,
                                             lockNode=True)

        CampaignCheckDBAssertion(campaignInfo['ID'], campaignInfo['PAYLOAD']).check()



    @pytest.mark.parametrize('campaignType,testControlType,response,errorCode,errorMessage', [
        ('LIVE', 'ORG',400, [104, 1005], ['Campaign Objective Exception : Specified campaign objective Greetings does not accept a value.']),

    ])
    def test_irisV2_createCampaign_objective_Greetings_withValue(self, campaignType, testControlType,response,errorCode,errorMessage):
        payload = copy.deepcopy(constant.payload['createcampaignv2'])
        payload.update({
            "name": "Automation_IRISV2_{}".format(int(time.time() * 1000)),
            "objective": {
                "objectiveName": "Greetings",
                "value": {"name":["Anniversary"]}
            }})
        payload["testControl"].pop("testPercentage")
        campaignInfo = CreateCampaign.create(campaignType, testControlType, payload=payload, updateNode=True,
                                             lockNode=True)
        Assertion.constructAssertion(campaignInfo['RESPONSE']['statusCode'] == response,
                                     'Actual code :{} and Expected:{}'.format(campaignInfo['RESPONSE'],
                                                                              response))

        for errors in campaignInfo['RESPONSE']['json']['errors']:
            Assertion.constructAssertion(errors['code'] in errorCode,
                                         'Actual Error Code :{} and Expected :{}'.format(
                                             errors['code'], errorCode))

            Assertion.constructAssertion(errors['message'] in errorMessage,
                                         'Actual Error message :{} and Expected :{}'.format(
                                             errors['message'], errorMessage))



    @pytest.mark.parametrize('campaignType,testControlType', [
        ('LIVE', 'ORG'),

    ])
    def test_irisV2_createCampaign_objective_Data_Capture(self, campaignType, testControlType):
        payload = copy.deepcopy(constant.payload['createcampaignv2'])
        payload.update({
            "name": "Automation_IRISV2_{}".format(int(time.time() * 1000)),
            "objective": {
                "objectiveName":"Data_Capture"
                            }
        })
        payload["testControl"].pop("testPercentage")
        campaignInfo = CreateCampaign.create(campaignType, testControlType, payload=payload, updateNode=True,
                                             lockNode=True)

        CampaignCheckDBAssertion(campaignInfo['ID'], campaignInfo['PAYLOAD']).check()

    @pytest.mark.parametrize('campaignType,testControlType,response,errorCode,errorMessage', [
        ('LIVE', 'ORG',400, [104, 1005], ['Campaign Objective Exception : Specified campaign objective Data_Capture does not accept a value.']),

    ])

    def test_irisV2_createCampaign_objective_Data_Capture_withValue(self, campaignType, testControlType,response,errorCode,errorMessage):
        payload = copy.deepcopy(constant.payload['createcampaignv2'])
        payload.update({
            "name": "Automation_IRISV2_{}".format(int(time.time() * 1000)),
            "objective": {
                "objectiveName": "Data_Capture",
                "value": "Date of birth"
            }
        })
        payload["testControl"].pop("testPercentage")
        campaignInfo = CreateCampaign.create(campaignType, testControlType, payload=payload, updateNode=True,
                                             lockNode=True)

        Assertion.constructAssertion(campaignInfo['RESPONSE']['statusCode']==response,
                                     'Actual code :{} and Expected:{}'.format(campaignInfo['RESPONSE'],
                                                                              response))
        for errors in campaignInfo['RESPONSE']['json']['errors']:
            Assertion.constructAssertion(errors['code'] in errorCode,
                                         'Actual Error Code :{} and Expected :{}'.format(
                                             errors['code'], errorCode))

            Assertion.constructAssertion(errors['message'] in errorMessage,
                                     'Actual Error message :{} and Expected :{}'.format(
                                         errors['message'], errorMessage))




    @pytest.mark.parametrize('campaignType,testControlType', [
        ('LIVE', 'ORG'),

    ])
    def test_irisV2_createCampaign_objective_Boost_Sales(self, campaignType, testControlType):
        payload = copy.deepcopy(constant.payload['createcampaignv2'])
        payload.update({
            "name": "Automation_IRISV2_{}".format(int(time.time() * 1000)),
            "objective": {
                "objectiveName": "Boost_Sales"

            }
        })
        payload["testControl"].pop("testPercentage")
        campaignInfo = CreateCampaign.create(campaignType, testControlType, payload=payload, updateNode=True,
                                             lockNode=True)

        CampaignCheckDBAssertion(campaignInfo['ID'], campaignInfo['PAYLOAD']).check()

    @pytest.mark.parametrize('campaignType,testControlType,response,errorCode,errorMessage', [
        ('LIVE', 'ORG',400,[1005,104],["Campaign Objective Exception : Specified campaign objective Boost_Sales does not accept a value."]),

    ])

    def test_irisV2_createCampaign_objective_Boost_Sales_withValue(self, campaignType, testControlType,response,errorCode,errorMessage):



        payload = copy.deepcopy(constant.payload['createcampaignv2'])
        payload.update({
            "name": "Automation_IRISV2_{}".format(int(time.time() * 1000)),
            "objective": {
                "objectiveName": "Boost_Sales",
                "value": {"Festival":"test"}
            }
        })
        payload["testControl"].pop("testPercentage")
        campaignInfo = CreateCampaign.create(campaignType, testControlType, payload=payload, updateNode=True,
                                             lockNode=True)
        Assertion.constructAssertion(campaignInfo['RESPONSE']['statusCode'] == response,
                                     'Actual code :{} and Expected:{}'.format(campaignInfo['RESPONSE'],
                                                                              response))
        for errors in campaignInfo['RESPONSE']['json']['errors']:
            Assertion.constructAssertion(errors['code'] in errorCode,
                                         'Actual Error Code :{} and Expected :{}'.format(
                                             errors['code'], errorCode))

            Assertion.constructAssertion(errors['message'] in errorMessage,
                                     'Actual Error message :{} and Expected :{}'.format(
                                         errors['message'], errorMessage))


    @pytest.mark.parametrize('campaignType,testControlType', [
        ('LIVE', 'ORG'),

    ])
    def test_irisV2_createCampaign_objective_Winback(self, campaignType, testControlType):
        payload = copy.deepcopy(constant.payload['createcampaignv2'])
        payload.update({
            "name": "Automation_IRISV2_{}".format(int(time.time() * 1000)),
            "objective": {
                "objectiveName": "Winback"

            }
        })
        payload["testControl"].pop("testPercentage")
        campaignInfo = CreateCampaign.create(campaignType, testControlType, payload=payload, updateNode=True,
                                             lockNode=True)

        CampaignCheckDBAssertion(campaignInfo['ID'], campaignInfo['PAYLOAD']).check()

    @pytest.mark.parametrize('campaignType,testControlType,response,errorCode,errorMessage', [
        ('LIVE', 'ORG',400,[104,1005],"Campaign Objective Exception : Specified campaign objective Winback does not accept a value."),

    ])
    def test_irisV2_createCampaign_objective_Winback_withValue(self, campaignType, testControlType,response,errorCode,errorMessage):
        payload = copy.deepcopy(constant.payload['createcampaignv2'])
        payload.update({
            "name": "Automation_IRISV2_{}".format(int(time.time() * 1000)),
            "objective": {
                "objectiveName": "Winback",
                "value": {"Festival": "test"}
            }
        })
        payload["testControl"].pop("testPercentage")

        campaignInfo = CreateCampaign.create(campaignType, testControlType, payload=payload, updateNode=True,
                                             lockNode=True)
        Assertion.constructAssertion(campaignInfo['RESPONSE']['statusCode'] == response,
                                     'Actual code :{} and Expected:{}'.format(campaignInfo['RESPONSE'],
                                                                              response))
        for errors in campaignInfo['RESPONSE']['json']['errors']:
            Assertion.constructAssertion(errors['code'] in errorCode,
                                         'Actual Error Code :{} and Expected :{}'.format(
                                             errors['code'], errorCode))

        Assertion.constructAssertion(errors['message'] in errorMessage,
                                     'Actual Error message :{} and Expected :{}'.format(
                                         errors['message'], errorMessage))


    @pytest.mark.parametrize('campaignType,testControlType', [
        ('LIVE', 'ORG'),

    ])
    def test_irisV2_createCampaign_objective_Acquire(self, campaignType, testControlType):
        payload = copy.deepcopy(constant.payload['createcampaignv2'])
        payload.update({
            "name": "Automation_IRISV2_{}".format(int(time.time() * 1000)),
            "objective": {
                "objectiveName": "Acquire"

            }
        })
        payload["testControl"].pop("testPercentage")
        campaignInfo = CreateCampaign.create(campaignType, testControlType, payload=payload, updateNode=True,
                                             lockNode=True)

        CampaignCheckDBAssertion(campaignInfo['ID'], campaignInfo['PAYLOAD']).check()

    @pytest.mark.parametrize('campaignType,testControlType,response,errorCode,errorMessage', [
        ('LIVE', 'ORG',400,[1005,104],"Campaign Objective Exception : Specified campaign objective Acquire does not accept a value."),

    ])
    def test_irisV2_createCampaign_objective_Acquire_withValue(self, campaignType, testControlType,response,errorCode,errorMessage):
        payload = copy.deepcopy(constant.payload['createcampaignv2'])
        payload.update({
            "name": "Automation_IRISV2_{}".format(int(time.time() * 1000)),
            "objective": {
                "objectiveName": "Acquire",
                "value": {"Festival": "test"}
            }
        })
        payload["testControl"].pop("testPercentage")
        campaignInfo = CreateCampaign.create(campaignType, testControlType, payload=payload, updateNode=True,
                                             lockNode=True)
        Assertion.constructAssertion(campaignInfo['RESPONSE']['statusCode'] == response,
                                     'Actual code :{} and Expected:{}'.format(campaignInfo['RESPONSE'],
                                                                              response))
        for errors in campaignInfo['RESPONSE']['json']['errors']:
            Assertion.constructAssertion(errors['code'] in errorCode,
                                         'Actual Error Code :{} and Expected :{}'.format(
                                             errors['code'], errorCode))

        Assertion.constructAssertion(errors['message'] in errorMessage,
                                     'Actual Error message :{} and Expected :{}'.format(
                                         errors['message'], errorMessage))


    @pytest.mark.parametrize('campaignType,testControlType', [
        ('LIVE', 'ORG'),

    ])

    def test_irisV2_createCampaign_objective_Feedback(self, campaignType, testControlType):
        payload = copy.deepcopy(constant.payload['createcampaignv2'])
        payload.update({
            "name": "Automation_IRISV2_{}".format(int(time.time() * 1000)),
            "objective": {
                "objectiveName": "Feedback"

            }
        })
        payload["testControl"].pop("testPercentage")
        campaignInfo = CreateCampaign.create(campaignType, testControlType, payload=payload, updateNode=True,
                                             lockNode=True)

        CampaignCheckDBAssertion(campaignInfo['ID'], campaignInfo['PAYLOAD']).check()

    @pytest.mark.parametrize('campaignType,testControlType,response,errorCode,errorMessage', [
        ('LIVE', 'ORG',400,[104,1005],["Campaign Objective Exception : Specified campaign objective Feedback does not accept a value."]),

    ])
    def test_irisV2_createCampaign_objective_Feedback_withValue(self, campaignType, testControlType,response,errorCode,errorMessage):
        payload = copy.deepcopy(constant.payload['createcampaignv2'])
        payload.update({
            "name": "Automation_IRISV2_{}".format(int(time.time() * 1000)),
            "objective": {
                "objectiveName": "Feedback",
                "value": {"Festival": "test"}
            }
        })
        payload["testControl"].pop("testPercentage")
        campaignInfo = CreateCampaign.create(campaignType, testControlType, payload=payload, updateNode=True,
                                             lockNode=True)
        Assertion.constructAssertion(campaignInfo["RESPONSE"]["statusCode"]==response,
                          "Actual code :{} and Expected :{}".format(campaignInfo['RESPONSE'],response))

        for errors in campaignInfo['RESPONSE']['json']['errors']:
            Assertion.constructAssertion(errors['code'] in errorCode,
                                         "Actual Error code :{} and Expected Error Code :{}".format(errors['code'],errorCode))

            Assertion.constructAssertion(errors['message'] in errorMessage,
                                         "Actual Message :{} and Expected Message {}".format(errors["message"],errorMessage))

    @pytest.mark.parametrize('campaignType,testControlType', [
        ('LIVE', 'ORG'),

    ])
    def test_irisV2_createCampaign_withGAEnabled(self, campaignType, testControlType):
        payload = copy.deepcopy(constant.payload['createcampaignv2'])
        payload.update({
            "name": "Automation_IRISV2_{}".format(int(time.time() * 1000)),
            "gaEnabled":"true",
	        "gaName":"test gaName",
	        "gaSource":"test gaSource"
        })
        payload["testControl"].pop("testPercentage")
        campaignInfo = CreateCampaign.create(campaignType, testControlType, payload=payload, updateNode=True,
                                             lockNode=True)

        CampaignCheckDBAssertion(campaignInfo['ID'], campaignInfo['PAYLOAD']).check()

    @pytest.mark.parametrize('campaignType,testControlType', [
        ('LIVE', 'ORG'),

    ])
    def test_irisV2_createCampaign_withoutGAnameandSource(self, campaignType, testControlType):
        payload = copy.deepcopy(constant.payload['createcampaignv2'])
        payload.update({
            "name": "Automation_IRISV2_{}".format(int(time.time() * 1000)),
            "gaEnabled": "true"
        })
        payload["testControl"].pop("testPercentage")
        campaignInfo = CreateCampaign.create(campaignType, testControlType, payload=payload, updateNode=True,
                                             lockNode=True)

        CreateCampaign.assertResponse(campaignInfo["RESPONSE"],400,expectedErrorCode =102,expectedErrorMessage=["Invalid request : gaName and gaSource are required in case isGaEnabled is true"])

    @pytest.mark.parametrize('campaignType,testControlType', [
        ('LIVE', 'ORG'),

    ])
    def test_irisV2_createCampaign_InvalidDataType_GAsource(self, campaignType, testControlType):
        payload = copy.deepcopy(constant.payload['createcampaignv2'])
        payload.update({
            "name": "Automation_IRISV2_{}".format(int(time.time() * 1000)),
            "gaEnabled": "true",
            "gaSource": ["test gaSource"],
            "gaName": "test gaName"

        })
        campaignInfo = CreateCampaign.create(campaignType, testControlType, payload=payload, updateNode=True,
                                             lockNode=True)

        CreateCampaign.assertResponse(campaignInfo["RESPONSE"], 400, expectedErrorCode=104, expectedErrorMessage=[
            "Invalid request : invalid data type of field gaSource"])

    @pytest.mark.parametrize('campaignType,testControlType', [
        ('LIVE', 'ORG'),

    ])
    def test_irisV2_createCampaign_InvalidDataType_GAName(self, campaignType, testControlType):
        payload = copy.deepcopy(constant.payload['createcampaignv2'])
        payload.update({
            "name": "Automation_IRISV2_{}".format(int(time.time() * 1000)),
            "gaEnabled": "true",
            "gaSource": "test gaSource",
            "gaName": ["test gaName"]

        })
        campaignInfo = CreateCampaign.create(campaignType, testControlType, payload=payload, updateNode=True,
                                             lockNode=True)

        CreateCampaign.assertResponse(campaignInfo["RESPONSE"], 400, expectedErrorCode=104, expectedErrorMessage=[
            "Invalid request : invalid data type of field gaName"])

    @pytest.mark.parametrize('campaignType,testControlType', [
        ('LIVE', 'ORG'),

    ])
    def test_irisV2_createCampaign_Without_GAsource(self, campaignType, testControlType):
        payload = copy.deepcopy(constant.payload['createcampaignv2'])
        payload.update({
            "name": "Automation_IRISV2_{}".format(int(time.time() * 1000)),
            "gaEnabled": "true",
            "gaName": "test gaName"

        })
        payload["testControl"].pop("testPercentage")
        campaignInfo = CreateCampaign.create(campaignType, testControlType, payload=payload, updateNode=True,
                                             lockNode=True)

        CreateCampaign.assertResponse(campaignInfo['RESPONSE'],400, expectedErrorCode=102,expectedErrorMessage=["Invalid request : gaName and gaSource are required in case isGaEnabled is true"])

    @pytest.mark.parametrize('campaignType,testControlType', [
        ('LIVE', 'ORG'),

    ])
    def test_irisV2_createCampaign_Without_GAname(self, campaignType, testControlType):
        payload = copy.deepcopy(constant.payload['createcampaignv2'])
        payload.update({
            "name": "Automation_IRISV2_{}".format(int(time.time() * 1000)),
            "gaEnabled": "true",
            "gaSource" : "test gaSource"
        })
        payload["testControl"].pop("testPercentage")
        campaignInfo = CreateCampaign.create(campaignType, testControlType, payload=payload, updateNode=True,
                                             lockNode=True)

        CreateCampaign.assertResponse(campaignInfo['RESPONSE'], 400, expectedErrorCode=102, expectedErrorMessage=[
            "Invalid request : gaName and gaSource are required in case isGaEnabled is true"])

    @pytest.mark.parametrize('campaignType,testControlType', [
        ('LIVE', 'ORG'),

    ])
    def test_irisV2_createCampaign_Without_GASource(self, campaignType, testControlType):
        payload = copy.deepcopy(constant.payload['createcampaignv2'])
        payload.update({
            "name": "Automation_IRISV2_{}".format(int(time.time() * 1000)),
            "gaEnabled": "true",
            "gaName" : "test gaName"
        })
        payload["testControl"].pop("testPercentage")
        campaignInfo = CreateCampaign.create(campaignType, testControlType, payload=payload, updateNode=True,
                                             lockNode=True)

        CreateCampaign.assertResponse(campaignInfo['RESPONSE'], 400, expectedErrorCode=102, expectedErrorMessage=[
            "Invalid request : gaName and gaSource are required in case isGaEnabled is true"])

    @pytest.mark.parametrize('campaignType,testControlType', [
        ('LIVE', 'ORG'),

    ])
    def test_irisV2_createCampaign_With_GADisabled(self, campaignType, testControlType):
        payload = copy.deepcopy(constant.payload['createcampaignv2'])
        payload.update({
            "name": "Automation_IRISV2_{}".format(int(time.time() * 1000)),
            "gaEnabled": "false",

        })
        payload["testControl"].pop("testPercentage")
        campaignInfo = CreateCampaign.create(campaignType, testControlType, payload=payload, updateNode=True,
                                             lockNode=True)

        CampaignCheckDBAssertion(campaignInfo['ID'], campaignInfo['PAYLOAD']).check()

