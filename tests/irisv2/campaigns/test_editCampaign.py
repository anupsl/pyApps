import time

import pytest

from src.Constant.constant import constant
from src.modules.irisv2.campaigns.campaignCheckDBAssertion import CampaignCheckDBAssertion
from src.modules.irisv2.campaigns.createCampaign import CreateCampaign
from src.modules.irisv2.helper.irisHelper import IrisHelper
from src.modules.irisv2.message.createMessage import CreateMessage
from src.utilities.assertion import Assertion
from src.utilities.logger import Logger
from src.utilities.randValues import randValues
from src.utilities.utils import Utils



@pytest.mark.run(order=1)
class Test_EditCampaigns():
    def setup_method(self, method):
        Logger.logMethodName(method.__name__)

    @pytest.mark.parametrize('description,campaignType,testControlType,editInfo', [
        ('Edit start date', 'LIVE', 'ORG', {'startDate': Utils.getTime(hours=23, milliSeconds=True)}),
        ('Edit end date', 'LIVE', 'ORG', {'endDate': Utils.getTime(days=2, milliSeconds=True)}),
        ('Edit description', 'LIVE', 'ORG', {'description': randValues.randomString(10)}),
        ('Edit type', 'LIVE', 'ORG', {'testControl': {'type': 'CUSTOM','testPercentage': 10}}),
        ('Edit type', 'LIVE', 'ORG', {'testControl': {'type': 'SKIP'}}),

        ('Edit start date', 'LIVE', 'SKIP', {'startDate': Utils.getTime(hours=23, milliSeconds=True)}),
        ('Edit end date', 'LIVE', 'SKIP', {'endDate': Utils.getTime(days=2, milliSeconds=True)}),
        ('Edit description', 'LIVE', 'SKIP', {'description': randValues.randomString(10)}),
        ('Edit testPercentage', 'LIVE', 'SKIP', {'testControl': {'type': 'ORG'}}),
        ('Edit type', 'LIVE', 'SKIP', {'testControl': {'type': 'CUSTOM', 'testPercentage': 50}}),
        ('Edit type', 'LIVE', 'SKIP', {'testControl': {'type': 'ORG'}}),

        ('Edit start date', 'LIVE', 'CUSTOM', {'startDate': Utils.getTime(hours=23, milliSeconds=True)}),
        ('Edit end date', 'LIVE', 'CUSTOM', {'endDate': Utils.getTime(days=2, milliSeconds=True)}),
        ('Edit description', 'LIVE', 'CUSTOM', {'description': randValues.randomString(10)}),
        ('Edit testPercentage', 'LIVE', 'CUSTOM', {'testControl': {'type': 'SKIP'}}),
        ('Edit type', 'LIVE', 'CUSTOM', {'testControl': {'type': 'SKIP'}}),
        ('Edit type', 'LIVE', 'CUSTOM', {'testControl': {'type': 'ORG'}}),

    ])
    def test_irisV2_editCampaign_Sanity(self, description, campaignType, testControlType, editInfo):
        campaignInfo = CreateCampaign.create(campaignType, testControlType, updateNode=True)
        editInfo = CreateCampaign.edit(campaignInfo, editInfo)
        CreateCampaign.assertResponse(editInfo['RESPONSE'], 200)
        CampaignCheckDBAssertion(campaignInfo['ID'], editInfo['PAYLOAD']).check()

    @pytest.mark.parametrize('description,campaignType,testControlType,editInfo', [
        ('Edit name', 'LIVE', 'ORG',
         {'name': 'IrisV2_Auto_{}_{}'.format(randValues.randomString(5), randValues.randomString(10))}),
        ('Edit name', 'LIVE', 'SKIP',
         {'name': 'IrisV2_Auto_{}_{}'.format(randValues.randomString(5), randValues.randomString(10))}),
        ('Edit name', 'LIVE', 'CUSTOM',
         {'name': 'IrisV2_Auto_{}_{}'.format(randValues.randomString(5), randValues.randomString(10))})
        ])

    def test_irisV2_editCampaign_name(self, description, campaignType, testControlType, editInfo):
        campaignInfo = CreateCampaign.create(campaignType, testControlType, updateNode=True)
        editInfo = CreateCampaign.edit(campaignInfo, editInfo)
        CreateCampaign.assertResponse(editInfo['RESPONSE'], 400,expectedErrorCode=1003,
                                     expectedErrorMessage="Campaign Name Exception : Changing campaign name is not allowed.")

    @pytest.mark.parametrize('description,campaignType,testControlType,channel,messageInfo,editInfo', [

        ('Edit end date', 'LIVE', 'ORG', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True},
         {'endDate': Utils.getTime(days=2, milliSeconds=True)}),
        ('Edit description', 'LIVE', 'ORG', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True},
         {'description': randValues.randomString(10)}),
        ('Edit end date', 'UPCOMING', 'ORG', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True},
         {'endDate': Utils.getTime(days=2, milliSeconds=True)}),
        ('Edit description', 'UPCOMING', 'ORG', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True},
         {'description': randValues.randomString(10)}),
        ('Edit end date', 'UPCOMING', 'ORG', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True},
         {'endDate': Utils.getTime(days=2, milliSeconds=True)}),
        ('Edit description', 'UPCOMING', 'ORG', 'MOBILE',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True},
         {'description': randValues.randomString(10)})

    ])
    def test_irisV2_editCampaign_AftereCreatingMessage(self, description, campaignType, testControlType, channel,
                                                       messageInfo, editInfo):

        campaignInfo = CreateCampaign.create(campaignType, testControlType, updateNode=True)
        messageDetails = CreateMessage.create(campaignType, testControlType, 'LOYALTY', channel, messageInfo,
                                              campaignId=campaignInfo['ID'],
                                              updateNode=True)
        campaignInfo = constant.config['node'][campaignType][testControlType]['CAMPAIGN']
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        editInfo = CreateCampaign.edit(campaignInfo, editInfo)
        CreateCampaign.assertResponse(editInfo['RESPONSE'], 200)
        CampaignCheckDBAssertion(campaignInfo['ID'], editInfo['PAYLOAD']).check()

    @pytest.mark.parametrize('description,campaignType,testControlType,channel,messageInfo,editInfo', [
        ('Edit name', 'UPCOMING', 'ORG', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True},
         {'name': 'IrisV2_Auto_{}_{}'.format(randValues.randomString(5), randValues.randomString(10))}),
        ('Edit name', 'UPCOMING', 'ORG', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True},
         {'name': 'IrisV2_Auto_{}_{}'.format(randValues.randomString(5), randValues.randomString(10))}),
        ('Edit name', 'LIVE', 'ORG', 'MOBILE',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True},
         {'name': 'IrisV2_Auto_{}_{}'.format(randValues.randomString(5), randValues.randomString(10))})
    ])


    def test_irisV2_editCampaign_Name_AftereCreatingMessage(self, description, campaignType, testControlType, channel,
                                                       messageInfo, editInfo):

        campaignInfo = CreateCampaign.create(campaignType, testControlType, updateNode=True)
        messageDetails = CreateMessage.create(campaignType, testControlType, 'LOYALTY', channel, messageInfo,
                                              campaignId=campaignInfo['ID'],
                                              updateNode=True)
        campaignInfo = constant.config['node'][campaignType][testControlType]['CAMPAIGN']
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        editInfo = CreateCampaign.edit(campaignInfo, editInfo)
        CreateCampaign.assertResponse(editInfo['RESPONSE'], 400,expectedErrorCode=1003,
                                      expectedErrorMessage="Campaign Name Exception : Changing campaign name is not allowed.")


    @pytest.mark.parametrize(
        'editInfo,campaignType,testControlType,channel,messageInfo,statusCode,errorCode,errorDescription', [
            ({'testControl': {'type': 'CUSTOM', 'testPercentage': 50}}, 'LIVE', 'ORG', 'MOBILE',
             {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
              'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}, 400, 1013,
             'Campaign edit Exception : Test control ratio cannot be edited'),
            ({'testControl': {'type': 'ORG', 'testPercentage': 50}}, 'LIVE', 'ORG', 'MOBILE',
             {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
              'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}, 400, 102,
             'Invalid request : test percentage must be null'),
            ({'testControl': {'type': 'CUSTOM', 'testPercentage': 10}}, 'LIVE', 'CUSTOM', 'MOBILE',
             {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
              'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}, 400, 1013,
             'Campaign edit Exception : Test control ratio cannot be edited'),
        ])
    def test_irisv2_editCampaign_After_Creating_Message(self, editInfo, campaignType, testControlType,
                                                        channel, messageInfo, statusCode, errorCode, errorDescription):
        messageDetails = CreateMessage.create(campaignType, testControlType, 'LOYALTY', channel, messageInfo,
                                              updateNode=True)
        campaignInfo = constant.config['node'][campaignType][testControlType]['CAMPAIGN']
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        editInfo = CreateCampaign.edit(campaignInfo, editInfo)
        Assertion.constructAssertion(editInfo['RESPONSE']['statusCode'] == statusCode,
                                     'Actual Status Code :{} and Expected : {}'.format(
                                         editInfo['RESPONSE']['statusCode'], statusCode))
        Assertion.constructAssertion(editInfo['RESPONSE']['json']['errors'][0]['code'] == errorCode,
                                     'Actual Error Code :{} and Expected : {}'.format(
                                         editInfo['RESPONSE']['json']['errors'][0]['code'], errorCode))
        Assertion.constructAssertion(errorDescription in editInfo['RESPONSE']['json']['errors'][0]['message'],
                                     'Expected Error message :{} and Actual : {}'.format(errorDescription,
                                                                                         editInfo['RESPONSE']['json'][
                                                                                             'errors'][0]['message']))

    @pytest.mark.parametrize('description,campaignType,testControlType,editInfo', [

        ('Edit end date', 'UPCOMING', 'ORG', {'endDate': Utils.getTime(days=1, milliSeconds=True)}),
        ('Edit description', 'UPCOMING', 'ORG', {'description': randValues.randomString(10)}),
        ('Edit testPercentage', 'UPCOMING', 'ORG', {'testControl': {'type': 'ORG'}}),
        ('Edit type', 'UPCOMING', 'ORG', {'testControl': {'type': 'CUSTOM', 'testPercentage': 50}}),


        ('Edit end date', 'UPCOMING', 'SKIP', {'endDate': Utils.getTime(days=1, milliSeconds=True)}),
        ('Edit description', 'UPCOMING', 'SKIP', {'description': randValues.randomString(10)}),
        ('Edit testPercentage', 'UPCOMING', 'SKIP', {'testControl': {'type': 'CUSTOM', 'testPercentage': 50}}),
        ('Edit type', 'UPCOMING', 'SKIP', {'testControl': {'type': 'CUSTOM', 'testPercentage': 50}}),
        ('Edit end date', 'UPCOMING', 'CUSTOM', {'endDate': Utils.getTime(days=1, milliSeconds=True)}),
        ('Edit description', 'UPCOMING', 'CUSTOM', {'description': randValues.randomString(10)}),
        ('Edit testPercentage', 'UPCOMING', 'CUSTOM', {'testControl': {'type': 'CUSTOM', 'testPercentage': 50}}),
        ('Edit type', 'UPCOMING', 'CUSTOM', {'testControl': {'type': 'CUSTOM', 'testPercentage': 50}}),

        ('Edit start and end date', 'LAPSED', 'ORG', {'startDate': Utils.getTime(minutes=30, milliSeconds=True),
                                                      'endDate': Utils.getTime(minutes=40, milliSeconds=True)}),
        ('Edit start and end date', 'LAPSED', 'SKIP', {'startDate': Utils.getTime(minutes=30, milliSeconds=True),
                                                       'endDate': Utils.getTime(minutes=50, milliSeconds=True)}),
        ('Edit start and end date', 'LAPSED', 'CUSTOM', {'startDate': Utils.getTime(minutes=30, milliSeconds=True),
                                                         'endDate': Utils.getTime(minutes=50, milliSeconds=True)}),
    ])
    def test_irisV2_editCampaign__OtheTypes(self, description, campaignType, testControlType, editInfo):
        campaignInfo = CreateCampaign.create(campaignType, testControlType, updateNode=True)
        CampaignCheckDBAssertion(campaignInfo['ID'], campaignInfo['PAYLOAD']).check()
        editInfo = CreateCampaign.edit(campaignInfo, editInfo)
        CreateCampaign.assertResponse(editInfo['RESPONSE'], 200)
        CampaignCheckDBAssertion(campaignInfo['ID'], editInfo['PAYLOAD']).check()

    @pytest.mark.parametrize('description,campaignType,testControlType,editInfo', [
        ('Edit start date', 'UPCOMING', 'ORG', {'startDate': Utils.getTime(minutes=5, milliSeconds=True)}),
        ('Edit start date', 'UPCOMING', 'SKIP', {'startDate': Utils.getTime(minutes=5, milliSeconds=True)}),
        ('Edit start date', 'UPCOMING', 'CUSTOM', {'startDate': Utils.getTime(minutes=5, milliSeconds=True)})
    ])
    def test_irisV2_editCampaign_startDate(self, description, campaignType, testControlType, editInfo):
        campaignInfo = CreateCampaign.create(campaignType, testControlType, updateNode=True)
        CampaignCheckDBAssertion(campaignInfo['ID'], campaignInfo['PAYLOAD']).check()
        editInfo = CreateCampaign.edit(campaignInfo, editInfo)
        CreateCampaign.assertResponse(editInfo['RESPONSE'], 200)
        CampaignCheckDBAssertion(campaignInfo['ID'], editInfo['PAYLOAD']).check()



    @pytest.mark.parametrize('description,campaignType,testControlType,editInfo',[
        ('Edit name', 'UPCOMING', 'ORG',
         {'name': 'IrisV2_Auto_{}_{}'.format(randValues.randomString(5), randValues.randomString(10))}),
        ('Edit name', 'UPCOMING', 'SKIP',
         {'name': 'IrisV2_Auto_{}_{}'.format(randValues.randomString(5), randValues.randomString(10))}),
        ('Edit name', 'UPCOMING', 'CUSTOM',
         {'name': 'IrisV2_Auto_{}_{}'.format(randValues.randomString(5), randValues.randomString(10))})
    ])

    def test_irisV2_editCampaign_Name_OtheTypes(self, description, campaignType, testControlType, editInfo):
        campaignInfo = CreateCampaign.create(campaignType, testControlType, updateNode=True)
        CampaignCheckDBAssertion(campaignInfo['ID'], campaignInfo['PAYLOAD']).check()
        editInfo = CreateCampaign.edit(campaignInfo, editInfo)
        CreateCampaign.assertResponse(editInfo['RESPONSE'], 400,expectedErrorCode=1003,expectedErrorMessage="Campaign Name Exception : Changing campaign name is not allowed.")


    @pytest.mark.parametrize('description,campaignType,testControlType,editInfo,statusCode,errorCode,errorDescription',
                             [
                                 (
                                 'Edit description', 'LAPSED', 'ORG', {'description': randValues.randomString(10)}, 400,
                                 1006, 'Campaign Date Exception : Campaign is already expired on'),
                                 ('Edit type', 'LAPSED', 'ORG',
                                  {'testControl': {'type': 'CUSTOM', 'testPercentage': 50}}, 400, 1006,
                                  'Campaign Date Exception : Campaign is already expired on'),
                                 ('Edit description', 'LAPSED', 'SKIP', {'description': randValues.randomString(10)},
                                  400, 1006,
                                  'Campaign Date Exception : Campaign is already expired on'),
                                 ('Edit testPercentage', 'LAPSED', 'SKIP',
                                  {'testControl': {'type': 'CUSTOM', 'testPercentage': 50}}, 400, 1006,
                                  'Campaign Date Exception : Campaign is already expired on'),
                                 ('Edit type', 'LAPSED', 'SKIP',
                                  {'testControl': {'type': 'CUSTOM', 'testPercentage': 50}}, 400, 1006,
                                  'Campaign Date Exception : Campaign is already expired on'),
                                 ('Edit description', 'LAPSED', 'CUSTOM', {'description': randValues.randomString(10)},
                                  400, 1006,
                                  'Campaign Date Exception : Campaign is already expired on'),
                                 ('Edit testPercentage', 'LAPSED', 'CUSTOM',
                                  {'testControl': {'type': 'CUSTOM', 'testPercentage': 50}}, 400, 1006,
                                  'Campaign Date Exception : Campaign is already expired on'),
                                 ('Edit type', 'LAPSED', 'CUSTOM',
                                  {'testControl': {'type': 'CUSTOM', 'testPercentage': 50}}, 400, 1006,
                                  'Campaign Date Exception : Campaign is already expired on')

                             ])
    def test_irisV2_editCampaign_LapsedOtheTypes(self, description, campaignType, testControlType, editInfo, statusCode,
                                                 errorCode, errorDescription):
        campaignInfo = CreateCampaign.create(campaignType, testControlType, updateNode=True)
        CampaignCheckDBAssertion(campaignInfo['ID'], campaignInfo['PAYLOAD']).check()
        editInfo = CreateCampaign.edit(campaignInfo, editInfo)
        Assertion.constructAssertion(editInfo['RESPONSE']['statusCode'] == statusCode,
                                     'Actual Status Code :{} and Expected : {}'.format(
                                         editInfo['RESPONSE']['statusCode'], statusCode))
        Assertion.constructAssertion(editInfo['RESPONSE']['json']['errors'][0]['code'] == errorCode,
                                     'Actual Error Code :{} and Expected : {}'.format(
                                         editInfo['RESPONSE']['json']['errors'][0]['code'], errorCode))
        Assertion.constructAssertion(errorDescription in editInfo['RESPONSE']['json']['errors'][0]['message'],
                                     'Expected Error message :{} and Actual : {}'.format(errorDescription,
                                                                                         editInfo['RESPONSE']['json'][
                                                                                             'errors'][0]['message']))

    @pytest.mark.parametrize('description,campaignType,testControlType,editInfo,statusCode,errorCode,errorDescription',
                             [
                                 ('Edit start and end date with same date', 'LIVE', 'ORG',
                                  {'startDate': int(time.time() * 1000) + 20000,
                                   'endDate': int(time.time() * 1000) + 20000}, 400, 1006,
                                  'Campaign Date Exception : Campaign end date is less or equal than start date'),
                                 ('Edit start date where start date is greater than end date', 'LIVE', 'ORG',
                                  {'startDate': Utils.getTime(days=2, milliSeconds=True)}, 400, 1006,
                                  'Campaign Date Exception : Campaign end date is less or equal than start date'),
                             ])
    def test_irisV2_editCampaign_NegativeCase_EditStartDate(self, description, campaignType, testControlType, editInfo,
                                                            statusCode, errorCode, errorDescription):
        campaignInfo = CreateCampaign.create(campaignType, testControlType, updateNode=True)
        CampaignCheckDBAssertion(campaignInfo['ID'], campaignInfo['PAYLOAD']).check()
        editInfo = CreateCampaign.edit(campaignInfo, editInfo)
        Assertion.constructAssertion(editInfo['RESPONSE']['statusCode'] == statusCode,
                                     'Actual Status Code :{} and Expected : {}'.format(
                                         editInfo['RESPONSE']['statusCode'], statusCode))
        Assertion.constructAssertion(editInfo['RESPONSE']['json']['errors'][0]['code'] == errorCode,
                                     'Actual Error Code :{} and Expected : {}'.format(
                                         editInfo['RESPONSE']['json']['errors'][0]['code'], errorCode))
        Assertion.constructAssertion(errorDescription == editInfo['RESPONSE']['json']['errors'][0]['message'],
                                     'Expected Error message :{} and Actual : {}'.format(errorDescription,
                                                                                         editInfo['RESPONSE']['json'][
                                                                                             'errors'][0]['message']))

    @pytest.mark.parametrize('description,campaignType,testControlType,editInfo,statusCode,errorCode,errorDescription',
                             [
                                 ('Edit start date where start date is less than current date and time', 'LIVE', 'ORG',
                                  {'startDate': Utils.getTime(days=-2, milliSeconds=True)}, 400, 1006,
                                  'Campaign Date Exception : Campaign start date is less than current date'),
                             ])
    def test_irisV2_editCampaign_NegativeCase_EditStartDate(self, description, campaignType, testControlType, editInfo,
                                                            statusCode, errorCode, errorDescription):
        campaignInfo = CreateCampaign.create(campaignType, testControlType, updateNode=True)
        CampaignCheckDBAssertion(campaignInfo['ID'], campaignInfo['PAYLOAD']).check()
        editInfo = CreateCampaign.edit(campaignInfo, editInfo)
        Assertion.constructAssertion(editInfo['RESPONSE']['statusCode'] == statusCode,
                                     'Actual Status Code :{} and Expected : {}'.format(
                                         editInfo['RESPONSE']['statusCode'], statusCode))
        Assertion.constructAssertion(editInfo['RESPONSE']['json']['errors'][0]['code'] == errorCode,
                                     'Actual Error Code :{} and Expected : {}'.format(
                                         editInfo['RESPONSE']['json']['errors'][0]['code'], errorCode))
        Assertion.constructAssertion(errorDescription in editInfo['RESPONSE']['json']['errors'][0]['message'],
                                     'Expected Error message :{} and Actual : {}'.format(errorDescription,
                                                                                         editInfo['RESPONSE']['json'][
                                                                                             'errors'][0]['message']))

    @pytest.mark.parametrize('description,campaignType,testControlType,editInfo,statusCode,errorCode,errorDescription',
                             [
                                 ('Edit end date where end date is less than current date and time', 'LIVE', 'ORG',
                                  {'endDate': Utils.getTime(days=-2, milliSeconds=True)}, 400, 1006,
                                  'Campaign Date Exception : Campaign is already expired on'),
                             ])
    def test_irisV2_editCampaign_NegativeCase_EditEndDate(self, description, campaignType, testControlType, editInfo,
                                                          statusCode,
                                                          errorCode, errorDescription):
        campaignInfo = CreateCampaign.create(campaignType, testControlType, updateNode=True)
        CampaignCheckDBAssertion(campaignInfo['ID'], campaignInfo['PAYLOAD']).check()
        editInfo = CreateCampaign.edit(campaignInfo, editInfo)
        Assertion.constructAssertion(statusCode == editInfo['RESPONSE']['statusCode'],
                                     'Error status actual {} and expected {}'.format(statusCode, editInfo['RESPONSE'][
                                         'statusCode']))
        Assertion.constructAssertion(errorCode == editInfo['RESPONSE']['json']['errors'][0]['code'],
                                     'Error status actual {} and expected {}'.format(errorCode,
                                                                                     editInfo['RESPONSE']['json'][
                                                                                         'errors'][0]['code']))
        Assertion.constructAssertion(errorDescription in
                                     editInfo['RESPONSE']['json']['errors'][0]['message'],
                                     'Error message expected {} and actual {}'.format
                                     (errorDescription, editInfo['RESPONSE']['json']['errors'][0]['message']))



    @pytest.mark.parametrize('description,campaignType,testControlType,editInfo,statusCode,errorCode,errorDescription',
                             [
                                 ('Invalid orgId', 'LIVE', 'ORG',
                                  {'endDate': Utils.getTime(days=2, milliSeconds=True)}, 500, 101,
                                  'Generic error: HTTP 401 Unauthorized')
                             ])
    def test_irisV2_editCampaign_InvalidOrgId(self, description, campaignType, testControlType, editInfo, statusCode,
                                              errorCode, errorDescription):
        campaignInfo = CreateCampaign.create(campaignType, testControlType, updateNode=True)
        actualOrgId = constant.config['orgId']
        try:
            constant.config['orgId'] = 999999
            editInfo = CreateCampaign.edit(campaignInfo, editInfo)
            Assertion.constructAssertion(editInfo['RESPONSE']['statusCode'] == statusCode,
                                         'Actual Status Code :{} and Expected : {}'.format(
                                             editInfo['RESPONSE']['statusCode'], statusCode))
            Assertion.constructAssertion(editInfo['RESPONSE']['json']['errors'][0]['code'] == errorCode,
                                         'Actual Error Code :{} and Expected : {}'.format(
                                             editInfo['RESPONSE']['json']['errors'][0]['code'], errorCode))
            Assertion.constructAssertion(errorDescription == editInfo['RESPONSE']['json']['errors'][0]['message'],
                                         'Expected Error message :{} and Actual : {}'.format(errorDescription,
                                                                                             editInfo['RESPONSE'][
                                                                                                 'json'][
                                                                                                 'errors'][0][
                                                                                                 'message']))
        finally:
            constant.config['orgId'] = actualOrgId

    @pytest.mark.parametrize('description,campaignType,testControlType,editInfo,statusCode,errorCode,errorDescription',
                             [
                                 ('Invalid orgId', 'LIVE', 'ORG',
                                  {'endDate': Utils.getTime(days=2, milliSeconds=True)}, 401, 999999,
                                  'Invalid org id')
                             ])
    def test_irisV2_editCampaign_NegativeOrgId(self, description, campaignType, testControlType, editInfo, statusCode,
                                               errorCode, errorDescription):
        campaignInfo = CreateCampaign.create(campaignType, testControlType, updateNode=True)
        actualOrgId = constant.config['orgId']
        try:
            constant.config['orgId'] = -99999
            editInfo = CreateCampaign.edit(campaignInfo, editInfo)
            Assertion.constructAssertion(editInfo['RESPONSE']['statusCode'] == statusCode,
                                         'Actual Status Code :{} and Expected : {}'.format(
                                             editInfo['RESPONSE']['statusCode'], statusCode))
            Assertion.constructAssertion(editInfo['RESPONSE']['json']['errors'][0]['code'] == errorCode,
                                         'Actual Error Code :{} and Expected : {}'.format(
                                             editInfo['RESPONSE']['json']['errors'][0]['code'], errorCode))
            Assertion.constructAssertion(errorDescription == editInfo['RESPONSE']['json']['errors'][0]['message'],
                                         'Expected Error message :{} and Actual : {}'.format(errorDescription,
                                                                                             editInfo['RESPONSE'][
                                                                                                 'json'][
                                                                                                 'errors'][0][
                                                                                                 'message']))
        finally:
            constant.config['orgId'] = actualOrgId

    @pytest.mark.parametrize('description,campaignType,testControlType,editInfo,statusCode,errorCode,errorDescription',
                             [
                                 ('Wrong auth', 'LIVE', 'ORG',
                                  {'endDate': Utils.getTime(days=2, milliSeconds=True)}, 401, 999999,
                                  'Unauthorized')
                             ])
    def test_irisV2_editCampaign_WrongAuth(self, description, campaignType, testControlType, editInfo, statusCode,
                                           errorCode, errorDescription):
        campaignInfo = CreateCampaign.create(campaignType, testControlType, updateNode=True)
        previousUserName = None
        try:
            previousUserName = IrisHelper.updateUserName('WrongName')
            editInfo = CreateCampaign.edit(campaignInfo, editInfo)
            Assertion.constructAssertion(editInfo['RESPONSE']['statusCode'] == statusCode,
                                         'Actual Status Code :{} and Expected : {}'.format(
                                             editInfo['RESPONSE']['statusCode'], statusCode))
        finally:
            if previousUserName is not None: IrisHelper.updateUserName(previousUserName)

    @pytest.mark.parametrize(
        'description,campaignType,testControlType,channel,messageInfo,editInfo,statusCode,errorCode,errorDescription', [
            ('Edit start date', 'LIVE', 'ORG', 'MOBILE',
             {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
              'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True},
             {'startDate': Utils.getTime(hours=23, milliSeconds=True)}, 400, 1006,
             'Campaign Date Exception : Campaign start date cannot be modified '),
            ('Edit start date', 'UPCOMING', 'ORG', 'MOBILE',
             {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN',
              'messageStrategy': {'type': 'DEFAULT'},
              'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True},
             {'startDate': Utils.getTime(hours=23, milliSeconds=True)}, 400, 1006,
             'Campaign Date Exception : Campaign start date cannot be modified '),
            ('Edit start date', 'LIVE', 'ORG', 'MOBILE',
             {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
              'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True},
             {'startDate': Utils.getTime(hours=23, milliSeconds=True)}, 400, 1006,
             'Campaign Date Exception : Campaign start date cannot be modified ')

        ])
    def test_irisV2_editCampaignStartDate_AftereCreatingMessage(self, description, campaignType, testControlType,
                                                                channel,
                                                                messageInfo, editInfo, statusCode, errorCode,
                                                                errorDescription):
        campaignInfo = CreateCampaign.create(campaignType, testControlType, updateNode=True)
        messageDetails = CreateMessage.create(campaignType, testControlType, 'LOYALTY', channel, messageInfo,
                                              campaignId=campaignInfo['ID'],
                                              updateNode=True)
        campaignInfo = constant.config['node'][campaignType][testControlType]['CAMPAIGN']
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        editInfo = CreateCampaign.edit(campaignInfo, editInfo)
        Assertion.constructAssertion(editInfo['RESPONSE']['statusCode'] == statusCode,
                                     'Actual Status Code :{} and Expected : {}'.format(
                                         editInfo['RESPONSE']['statusCode'], statusCode))
        Assertion.constructAssertion(editInfo['RESPONSE']['json']['errors'][0]['code'] == errorCode,
                                     'Actual Error Code :{} and Expected : {}'.format(
                                         editInfo['RESPONSE']['json']['errors'][0]['code'], errorCode))
        Assertion.constructAssertion(editInfo['RESPONSE']['json']['errors'][0]['message'] in errorDescription,
                                     'Actual Error Code :{} and Expected : {}'.format(
                                         editInfo['RESPONSE']['json']['errors'][0]['message'], errorDescription))

    @pytest.mark.parametrize(
        'campaignTypeFirst,testControlTypeFirst,campaignTypeSecond,testControlTypeSecond,statusCode,errorCode',
        [

            ('LIVE', 'ORG', 'LAPSED', 'ORG', 400, [1003,1006]),

            ('LAPSED', 'ORG', 'LAPSED', 'ORG', 400, [1003,1006])
        ])
    def test_irisV2_editCampaign_NegativeCase_Lapsed(self, campaignTypeFirst, testControlTypeFirst,
                                                               campaignTypeSecond, testControlTypeSecond, statusCode,
                                                               errorCode):
        campaignInfo1 = CreateCampaign.create(campaignTypeFirst, testControlTypeFirst, updateNode=True, lockNode=True)
        campaignInfo = CreateCampaign.create(campaignTypeSecond, testControlTypeSecond, updateNode=True, lockNode=True)
        editInfo = CreateCampaign.edit(campaignInfo, {'name': campaignInfo1['NAME']})
        Assertion.constructAssertion(editInfo['RESPONSE']['statusCode'] == statusCode,
                                     'Actual Status Code :{} and Expected : {}'.format(
                                         editInfo['RESPONSE']['statusCode'], statusCode))
        Assertion.constructAssertion(editInfo['RESPONSE']['json']['errors'][0]['code'] in errorCode,
                                     'Actual Error Code :{} and Expected : {}'.format(
                                         editInfo['RESPONSE']['json']['errors'][0]['code'], errorCode))
        Assertion.constructAssertion('Campaign Date Exception : Campaign is already expired on' in editInfo['RESPONSE']['json']['errors'][0]['message'] or "Campaign Name Exception : Campaign Name already exists" in editInfo['RESPONSE']['json']['errors'][0]['message'] or "Campaign Name Exception : Changing campaign name is not allowed." in editInfo['RESPONSE']['json']['errors'][0]['message'],
                                     'Actual Error Code :{} and Expected : {}'.format(
                                         editInfo['RESPONSE']['json']['errors'][0]['message'],editInfo['RESPONSE']['json']['errors'][0]['message']))



