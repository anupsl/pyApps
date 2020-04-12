import copy
import time

import pytest

from src.Constant.constant import OrgMapping
from src.Constant.constant import constant
from src.dbCalls.campaignShard import list_Calls
from src.modules.irisv2.helper.irisHelper import IrisHelper
from src.modules.irisv2.list.createAudience import CreateAudience
from src.modules.irisv2.list.createAudienceDBAssertion import CreateAudienceDBAssertion
from src.modules.irisv2.list.getAudienceById import GetAudienceById
from src.modules.irisv2.list.getListDBAssertion import GetListDBAssertion
from src.utilities.assertion import Assertion
from src.utilities.logger import Logger
from src.utilities.utils import Utils


@pytest.mark.run(order=14)
class Test_GetAudienceById():

    def setup_class(self):
        CreateAudience.getPocUsers()

    def setup_method(self, method):
        Logger.logMethodName(method.__name__)

    @pytest.mark.parametrize('campaignType,testControlType,listType,schemaIdentifier', [
        ('LIVE', 'ORG', 'UPLOAD', ['MOBILE'])
    ])
    def test_irisV2_getAudienceById_Mobile_Sanity(self, campaignType, testControlType, listType, schemaIdentifier):
        list = CreateAudience.uploadList(campaignType, testControlType, schemaIdentifier=schemaIdentifier,
                                         campaignCheck=False, updateNode=True, lockNode=True)
        CreateAudience.waitForGVDToBeUpdated(list['ID'], checkParams=False)
        response = GetAudienceById.getById(list['ID'])
        GetAudienceById.assertResponse(response, 200)
        GetListDBAssertion(list['ID'], response).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,schemaIdentifier', [
        ('UPCOMING', 'ORG', 'UPLOAD', ['MOBILE']),
        ('LAPSED', 'ORG', 'UPLOAD', ['MOBILE']),
        ('LIVE', 'CUSTOM', 'UPLOAD', ['MOBILE']),
        ('UPCOMING', 'CUSTOM', 'UPLOAD', ['MOBILE']),
        ('LAPSED', 'CUSTOM', 'UPLOAD', ['MOBILE']),
        ('LIVE', 'SKIP', 'UPLOAD', ['MOBILE']),
        ('UPCOMING', 'SKIP', 'UPLOAD', ['MOBILE']),
        ('LAPSED', 'SKIP', 'UPLOAD', ['MOBILE'])
    ])
    def test_irisV2_getAudienceById_Mobile_NewUser(self, campaignType, testControlType, listType, schemaIdentifier):
        list = CreateAudience.uploadList(campaignType, testControlType, schemaIdentifier=schemaIdentifier,
                                         campaignCheck=False, updateNode=True, lockNode=True)
        CreateAudience.waitForGVDToBeUpdated(list['ID'], checkParams=False)
        response = GetAudienceById.getById(list['ID'])
        GetAudienceById.assertResponse(response, 200)
        GetListDBAssertion(list['ID'], response).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,schemaIdentifier', [
        ('LIVE', 'ORG', 'UPLOAD', ['MOBILE']),
    ])
    def test_irisV2_getAudienceById_Mobile_ExistingUser(self, campaignType, testControlType, listType,
                                                               schemaIdentifier):
        list = CreateAudience.uploadList(campaignType, testControlType, schemaIdentifier=schemaIdentifier,
                                         newUser=False, updateNode=True, lockNode=True, campaignCheck=False)
        CreateAudience.waitForGVDToBeUpdated(list['ID'], checkCustomerCount=False)
        response = GetAudienceById.getById(list['ID'])
        GetAudienceById.assertResponse(response, 200)
        GetListDBAssertion(list['ID'], response, campaignHashLookUp=False, reachabilityCheck=False,
                           createAudienceJob=False).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,schemaIdentifier', [
        ('UPCOMING', 'ORG', 'UPLOAD', ['MOBILE']),
        ('LAPSED', 'ORG', 'UPLOAD', ['MOBILE']),
        ('LIVE', 'CUSTOM', 'UPLOAD', ['MOBILE']),
        ('UPCOMING', 'CUSTOM', 'UPLOAD', ['MOBILE']),
        ('LAPSED', 'CUSTOM', 'UPLOAD', ['MOBILE']),
        ('LIVE', 'SKIP', 'UPLOAD', ['MOBILE']),
        ('UPCOMING', 'SKIP', 'UPLOAD', ['MOBILE']),
        ('LAPSED', 'SKIP', 'UPLOAD', ['MOBILE'])
    ])
    def test_irisV2_getAudienceById_Mobile_ExistingUser(self, campaignType, testControlType, listType,
                                                        schemaIdentifier):
        list = CreateAudience.uploadList(campaignType, testControlType, schemaIdentifier=schemaIdentifier,
                                         newUser=False, updateNode=True, lockNode=True, campaignCheck=False)
        CreateAudience.waitForGVDToBeUpdated(list['ID'], checkCustomerCount=False)
        response = GetAudienceById.getById(list['ID'])
        GetAudienceById.assertResponse(response, 200)
        GetListDBAssertion(list['ID'], response, campaignHashLookUp=False, reachabilityCheck=False,
                           createAudienceJob=False).check()

    @pytest.mark.parametrize(
        'campaignType,testControlType,listType,schemaIdentifier,schemaData,numberOfUser,numberOfCustomTags', [
            ('LIVE', 'ORG', 'UPLOAD', ['MOBILE'], ['MOBILE', 'FIRST_NAME', 'custom_tag_1'], 2, 1),
            ('LIVE', 'ORG', 'UPLOAD', ['MOBILE'], ['MOBILE', 'FIRST_NAME', 'custom_tag_1', 'custom_tag_2'], 2, 2),
            ('LIVE', 'ORG', 'UPLOAD', ['MOBILE'],
             ['MOBILE', 'FIRST_NAME', 'custom_tag_1', 'custom_tag_2', 'custom_tag_3'], 2, 3),
            ('LIVE', 'ORG', 'UPLOAD', ['MOBILE'],
             ['MOBILE', 'FIRST_NAME', 'custom_tag_1', 'custom_tag_2', 'custom_tag_3', 'custom_tag_4'], 2, 4),
            ('LIVE', 'ORG', 'UPLOAD', ['MOBILE'],
             ['MOBILE', 'FIRST_NAME', 'custom_tag_1', 'custom_tag_2', 'custom_tag_3', 'custom_tag_4', 'custom_tag_5'],
             2, 5)
        ])
    def test_irisV2_getAudienceById_Mobile_CustomTags(self, campaignType, testControlType, listType, schemaIdentifier,
                                               schemaData, numberOfUser, numberOfCustomTags):
        list = CreateAudience.uploadList(campaignType, testControlType, schemaIdentifier=schemaIdentifier,
                                         schemaData=schemaData, numberOfUsers=numberOfUser,
                                         numberOfCustomTags=numberOfCustomTags, updateNode=True, lockNode=True,
                                         campaignCheck=False)
        CreateAudience.waitForGVDToBeUpdated(list['ID'], checkParams=False)
        response = GetAudienceById.getById(list['ID'])
        GetAudienceById.assertResponse(response, 200)
        GetListDBAssertion(list['ID'], response).check()

    @pytest.mark.parametrize(
        'campaignType,testControlType,listType,schemaIdentifier,schemaData,numberOfUser,numberOfCustomTags', [
            ('LIVE', 'ORG', 'UPLOAD', ['MOBILE'], ['MOBILE', 'custom_tag_1', 'FIRST_NAME'], 2, 1),
            ('LIVE', 'ORG', 'UPLOAD', ['MOBILE'], ['custom_tag_1', 'FIRST_NAME', 'MOBILE'], 2, 1),
            ('LIVE', 'ORG', 'UPLOAD', ['MOBILE'],
             ['MOBILE', 'FIRST_NAME', 'custom_tag_1', 'custom_tag_2', 'custom_tag_3', 'custom_tag_4', 'custom_tag_5'],
             2, 5),
            ('LIVE', 'ORG', 'UPLOAD', ['MOBILE'],
             ['MOBILE', 'custom_tag_1', 'FIRST_NAME', 'custom_tag_2', 'custom_tag_3', 'custom_tag_4', 'custom_tag_5'],
             2, 5),
            ('LIVE', 'ORG', 'UPLOAD', ['MOBILE'],
             ['FIRST_NAME', 'custom_tag_1', 'custom_tag_2', 'custom_tag_3', 'MOBILE', 'custom_tag_4', 'custom_tag_5'],
             2, 5),
            ('LIVE', 'ORG', 'UPLOAD', ['MOBILE'],
             ['MOBILE', 'FIRST_NAME', 'custom_tag_1', 'custom_tag_2', 'custom_tag_3', 'custom_tag_4', 'custom_tag_5'],
             2, 5),
            ('LIVE', 'ORG', 'UPLOAD', ['MOBILE'],
             ['MOBILE', 'custom_tag_1', 'custom_tag_2', 'custom_tag_3', 'custom_tag_4', 'custom_tag_5', 'FIRST_NAME'],
             2, 5),
        ])
    def test_irisV2_getAudienceById_Mobile_Variation_Identifiers(self, campaignType, testControlType, listType,
                                                          schemaIdentifier, schemaData, numberOfUser,
                                                          numberOfCustomTags):
        list = CreateAudience.uploadList(campaignType, testControlType, schemaIdentifier=schemaIdentifier,
                                         schemaData=schemaData, numberOfUsers=numberOfUser,
                                         numberOfCustomTags=numberOfCustomTags, updateNode=True, lockNode=True,
                                         campaignCheck=False)
        CreateAudience.waitForGVDToBeUpdated(list['ID'], checkParams=False)
        response = GetAudienceById.getById(list['ID'])
        GetAudienceById.assertResponse(response, 200)
        GetListDBAssertion(list['ID'], response, customTag=numberOfCustomTags).check()

    @pytest.mark.parametrize(
        'campaignType,testControlType,listType,schemaIdentifier,schemaData,numberOfUser,numberOfCustomTags', [
            ('LIVE', 'ORG', 'UPLOAD', ['MOBILE'],
             ['MOBILE', 'FIRST_NAME', 'custom_tag_5', 'custom_tag_4', 'custom_tag_3', 'custom_tag_2', 'custom_tag_1'],
             2, 5)
        ])
    def test_irisV2_getAudienceById_Mobile_CustomTags_InReverseOrder(self, campaignType, testControlType, listType,
                                                             schemaIdentifier, schemaData, numberOfUser,
                                                             numberOfCustomTags):
        list = CreateAudience.uploadList(campaignType, testControlType, schemaIdentifier=schemaIdentifier,
                                         schemaData=schemaData, numberOfUsers=numberOfUser,
                                         numberOfCustomTags=numberOfCustomTags, updateNode=True, lockNode=True,
                                         campaignCheck=False)
        CreateAudience.waitForGVDToBeUpdated(list['ID'], checkParams=False)
        response = GetAudienceById.getById(list['ID'])
        GetAudienceById.assertResponse(response, 200)
        GetListDBAssertion(list['ID'], response, customTag=numberOfCustomTags).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,schemaIdentifier,numberOfUsers', [
        ('LIVE', 'ORG', 'UPLOAD', ['MOBILE'], 10000),
        ('LIVE', 'ORG', 'UPLOAD', ['MOBILE'], 50000),
        ('LIVE', 'ORG', 'UPLOAD', ['MOBILE'], 100000)
    ])
    def test_irisV2_bulk_getAudienceById_bulkUpload_NewUsers(self, campaignType, testControlType, listType, schemaIdentifier,
                                                        numberOfUsers):
        list = CreateAudience.uploadList(campaignType, testControlType, schemaIdentifier=schemaIdentifier,
                                         numberOfUsers=numberOfUsers, updateNode=True, lockNode=True,
                                         campaignCheck=False)
        CreateAudience.waitForListToProcess(list['ID'], numberOfUsers)
        response = GetAudienceById.getById(list['ID'])
        GetAudienceById.assertResponse(response, 200)
        CreateAudienceDBAssertion(list['ID'], list, listType, numberOfUsers).check()
        GetListDBAssertion(list['ID'], response, reachabilityCheck=False).check()

    @pytest.mark.parametrize('newUser,countryCode', [
        (True, '91'),
        (True, ''),
        (False, '91'),
        (False, '')
    ])
    def test_irisV2_getAudienceById_Mobile_number_variationCountryCode(self, newUser, countryCode):
        listOfUsers = CreateAudience.createMobileUsers(newUser=True, append=countryCode)
        filePath = CreateAudience.createCSVUsingList(listOfUsers)
        audiencegroupbody = copy.deepcopy(constant.payload['audiencegroupbody'])
        audiencegroupbody['label'] = "AutomationListWithDifferentCountryCode_{}".format(int(time.time() * 1000))[:49]
        payload = CreateAudience.createFinalPayload(audiencegroupbody, numberOfUsers=10, newUser=True, numberOfFiles=0,
                                                    popFields=[])
        payload.append(('file', (filePath.split('/')[-1], open(filePath, 'rb'), 'text/csv')))
        listDetail = CreateAudience.uploadList('LIVE', 'ORG', payload=payload, updateNode=True, lockNode=True,
                                               campaignCheck=False)
        CreateAudience.waitForGVDToBeUpdated(listDetail['ID'])
        response = GetAudienceById.getById(listDetail['ID'])
        GetAudienceById.assertResponse(response, 200)
        GetListDBAssertion(listDetail['ID'], response).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,schemaIdentifier,numberOfUsers', [
        ('LIVE', 'ORG', 'UPLOAD', ['MOBILE'], 10000),
        ('LIVE', 'ORG', 'UPLOAD', ['MOBILE'], 50000),
        ('LIVE', 'ORG', 'UPLOAD', ['MOBILE'], 100000)
    ])
    def test_irisV2_bulk_getAudienceById_bulkUpload_withExistingUsers(self, campaignType, testControlType, listType,
                                                                 schemaIdentifier, numberOfUsers):
        list = CreateAudience.uploadList(campaignType, testControlType, schemaIdentifier=schemaIdentifier,
                                         numberOfUsers=numberOfUsers, newUser=False, updateNode=True, lockNode=True,
                                         campaignCheck=False)
        CreateAudience.waitForListToProcess(list['ID'], numberOfUsers)
        response = GetAudienceById.getById(list['ID'])
        GetAudienceById.assertResponse(response, 200)
        GetListDBAssertion(list['ID'], response, reachabilityCheck=False).check()

    @pytest.mark.parametrize('testControlType', [
        ('ORG'),
        ('CUSTOM')
    ])
    def test_irisV2_getAudienceById_Mobile_Reloaded(self, testControlType):
        previousOrgId = None
        try:
            previousOrgId = IrisHelper.updateOrgId(
                OrgMapping.orgMapping[constant.config['cluster']]['timeline']['orgId'])
            list = list_Calls().getIdOfReloadedList(testControlType)
            response = GetAudienceById.getById(list['id'])
            GetAudienceById.assertResponse(response, 200)
            GetListDBAssertion(list['id'], response, createAudienceJob=False, campaignGroupRecipients=False,
                               reachabilityCheck=False).check()
        except Exception, exp:
            Assertion.constructAssertion(False, 'Exception :{}'.format(exp))
        finally:
            if previousOrgId is not None: IrisHelper.updateOrgId(previousOrgId)

    @pytest.mark.parametrize('testControlType', [
        ('ORG'),
        ('CUSTOM'),
        ('SKIP')
    ])
    def test_irisV2_getAudienceById_Mobile_OlderCreatedList(self, testControlType):
        previousOrgId = None
        try:
            previousOrgId = IrisHelper.updateOrgId(OrgMapping.orgMapping[constant.config['cluster']]['iris']['orgId'])
            list = list_Calls().getIdofOlderList(testControlType)
            response = GetAudienceById.getById(list['id'])
            GetAudienceById.assertResponse(response, 200)
            GetListDBAssertion(list['id'], response, createAudienceJob=False, campaignGroupRecipients=False).check()
        except Exception, exp:
            Assertion.constructAssertion(False, 'Exception :{}'.format(exp))
        finally:
            if previousOrgId is not None: IrisHelper.updateOrgId(previousOrgId)

    @pytest.mark.parametrize('listType', [
        ('CAMPAIGN_USERS'),
        ('LOYALTY')
    ])
    def test_irisV2_getAudienceById_Mobile_NotVisibleList(self, listType):
        previousOrgId = None
        try:
            previousOrgId = IrisHelper.updateOrgId(OrgMapping.orgMapping[constant.config['cluster']]['iris']['orgId'])
            list = list_Calls().getNonVisibleList(listType)
            response = GetAudienceById.getById(list['id'])
            Assertion.constructAssertion('entity' not in response['json'],
                                         'For Invisible List No Entry Found from GetCall')
        except Exception, exp:
            Assertion.constructAssertion(False, 'Exception :{}'.format(exp))
        finally:
            if previousOrgId is not None: IrisHelper.updateOrgId(previousOrgId)

    @pytest.mark.parametrize('campaignType,testControlType,listType,schemaIdentifier', [
        ('LIVE', 'ORG', 'UPLOAD', ['MOBILE']),
        ('LIVE', 'CUSTOM', 'UPLOAD', ['MOBILE']),
        ('LIVE', 'SKIP', 'UPLOAD', ['MOBILE'])
    ])
    def test_irisV2_getAudienceById_Mobile_InActiveList(self, campaignType, testControlType, listType, schemaIdentifier):
        list = CreateAudience.uploadList(campaignType, testControlType, schemaIdentifier=schemaIdentifier,
                                         updateNode=True,
                                         lockNode=True, campaignCheck=False)
        list_Calls().updateGroupVersionDetailAsInactive(list['ID'])
        response = GetAudienceById.getById(list['ID'])
        Assertion.constructAssertion('entity' not in response['json'], 'For Inactive List No Entry Found from GetCall')

    @pytest.mark.parametrize('campaignType,testControlType,listType,numberOfFiles,schemaIdentifier', [
        ('LIVE', 'ORG', 'UPLOAD', 2, ['MOBILE']),
        ('LIVE', 'ORG', 'UPLOAD', 3, ['MOBILE']),
        ('LIVE', 'ORG', 'UPLOAD', 4, ['MOBILE']),
        ('LIVE', 'ORG', 'UPLOAD', 5, ['MOBILE']),
        ('LIVE', 'CUSTOM', 'UPLOAD', 5, ['MOBILE']),
        ('LIVE', 'SKIP', 'UPLOAD', 3, ['MOBILE'])
    ])
    def test_irisV2_getAudienceById_Mobile_ListCreatedWithMultipleFiles(self, campaignType, testControlType, listType,
                                                                 numberOfFiles, schemaIdentifier):
        list = CreateAudience.uploadList(campaignType, testControlType, schemaIdentifier=schemaIdentifier,
                                         numberOfFiles=numberOfFiles, updateNode=True, lockNode=True,
                                         campaignCheck=False)
        CreateAudience.waitForGVDToBeUpdated(list['ID'], checkParams=False)
        response = GetAudienceById.getById(list['ID'])
        GetAudienceById.assertResponse(response, 200)
        GetListDBAssertion(list['ID'], response).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,schemaIdentifier,schemaData', [
        ('LIVE', 'ORG', 'UPLOAD', ['EMAIL'], ['EMAIL', 'FIRST_NAME'])
    ])
    def test_irisV2_getAudienceById_Email_Sanity(self, campaignType, testControlType, listType, schemaIdentifier,
                                                 schemaData):
        list = CreateAudience.uploadList(campaignType, testControlType, schemaIdentifier=schemaIdentifier,
                                         schemaData=schemaData, campaignCheck=False)
        CreateAudience.waitForGVDToBeUpdated(list['ID'], checkParams=False)
        CreateAudience.waitForReachabilityJobCompletion(list['VID'])
        response = GetAudienceById.getById(list['ID'])
        GetAudienceById.assertResponse(response, 200)
        GetListDBAssertion(list['ID'], response).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,schemaIdentifier,schemaData', [
        ('UPCOMING', 'ORG', 'UPLOAD', ['EMAIL'], ['EMAIL', 'FIRST_NAME']),
        ('LAPSED', 'ORG', 'UPLOAD', ['EMAIL'], ['EMAIL', 'FIRST_NAME']),
        ('LIVE', 'CUSTOM', 'UPLOAD', ['EMAIL'], ['EMAIL', 'FIRST_NAME']),
        ('UPCOMING', 'CUSTOM', 'UPLOAD', ['EMAIL'], ['EMAIL', 'FIRST_NAME']),
        ('LAPSED', 'CUSTOM', 'UPLOAD', ['EMAIL'], ['EMAIL', 'FIRST_NAME']),
        ('LIVE', 'SKIP', 'UPLOAD', ['EMAIL'], ['EMAIL', 'FIRST_NAME']),
        ('UPCOMING', 'SKIP', 'UPLOAD', ['EMAIL'], ['EMAIL', 'FIRST_NAME']),
        ('LAPSED', 'SKIP', 'UPLOAD', ['EMAIL'], ['EMAIL', 'FIRST_NAME'])
    ])
    def test_irisV2_getAudienceById_Email_NewUser(self, campaignType, testControlType, listType, schemaIdentifier,
                                                  schemaData):
        list = CreateAudience.uploadList(campaignType, testControlType, schemaIdentifier=schemaIdentifier,
                                         schemaData=schemaData, campaignCheck=False)
        CreateAudience.waitForGVDToBeUpdated(list['ID'], checkParams=False)
        CreateAudience.waitForReachabilityJobCompletion(list['VID'])
        response = GetAudienceById.getById(list['ID'])
        GetAudienceById.assertResponse(response, 200)
        GetListDBAssertion(list['ID'], response).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,schemaIdentifier,schemaData', [
        ('LIVE', 'ORG', 'UPLOAD', ['EMAIL'], ['EMAIL', 'FIRST_NAME']),
    ])
    def test_irisV2_getAudienceById_Email_ExistingUser(self, campaignType, testControlType, listType,
                                                              schemaIdentifier, schemaData):
        list = CreateAudience.uploadList(campaignType, testControlType, schemaIdentifier=schemaIdentifier,
                                         schemaData=schemaData, newUser=False, updateNode=True, lockNode=True,
                                         campaignCheck=False)
        CreateAudience.waitForGVDToBeUpdated(list['ID'], checkCustomerCount=False)
        CreateAudience.waitForReachabilityJobCompletion(list['VID'])
        response = GetAudienceById.getById(list['ID'])
        GetAudienceById.assertResponse(response, 200)
        GetListDBAssertion(list['ID'], response, campaignHashLookUp=False, createAudienceJob=False).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,schemaIdentifier,schemaData', [
        ('UPCOMING', 'ORG', 'UPLOAD', ['EMAIL'], ['EMAIL', 'FIRST_NAME']),
        ('LAPSED', 'ORG', 'UPLOAD', ['EMAIL'], ['EMAIL', 'FIRST_NAME']),
        ('LIVE', 'CUSTOM', 'UPLOAD', ['EMAIL'], ['EMAIL', 'FIRST_NAME']),
        ('UPCOMING', 'CUSTOM', 'UPLOAD', ['EMAIL'], ['EMAIL', 'FIRST_NAME']),
        ('LAPSED', 'CUSTOM', 'UPLOAD', ['EMAIL'], ['EMAIL', 'FIRST_NAME']),
        ('LIVE', 'SKIP', 'UPLOAD', ['EMAIL'], ['EMAIL', 'FIRST_NAME']),
        ('UPCOMING', 'SKIP', 'UPLOAD', ['EMAIL'], ['EMAIL', 'FIRST_NAME']),
        ('LAPSED', 'SKIP', 'UPLOAD', ['EMAIL'], ['EMAIL', 'FIRST_NAME'])
    ])
    def test_irisV2_getAudienceById_Email_ExistingUser(self, campaignType, testControlType, listType, schemaIdentifier,
                                                       schemaData):
        list = CreateAudience.uploadList(campaignType, testControlType, schemaIdentifier=schemaIdentifier,
                                         schemaData=schemaData, newUser=False, updateNode=True, lockNode=True,
                                         campaignCheck=False)
        CreateAudience.waitForGVDToBeUpdated(list['ID'], checkCustomerCount=False)
        response = GetAudienceById.getById(list['ID'])
        GetAudienceById.assertResponse(response, 200)
        GetListDBAssertion(list['ID'], response, campaignHashLookUp=False, reachabilityCheck=False,
                           createAudienceJob=False).check()

    @pytest.mark.parametrize(
        'campaignType,testControlType,listType,schemaIdentifier,schemaData,numberOfUser,numberOfCustomTags', [
            ('LIVE', 'ORG', 'UPLOAD', ['EMAIL'], ['EMAIL', 'FIRST_NAME', 'custom_tag_1'], 2, 1),
            ('LIVE', 'ORG', 'UPLOAD', ['EMAIL'], ['EMAIL', 'FIRST_NAME', 'custom_tag_1', 'custom_tag_2'], 2, 2),
            ('LIVE', 'ORG', 'UPLOAD', ['EMAIL'], ['EMAIL', 'FIRST_NAME', 'custom_tag_1', 'custom_tag_2', 'custom_tag_3'], 2, 3),
            ('LIVE', 'ORG', 'UPLOAD', ['EMAIL'],
             ['EMAIL', 'FIRST_NAME', 'custom_tag_1', 'custom_tag_2', 'custom_tag_3', 'custom_tag_4'], 2, 4),
            ('LIVE', 'ORG', 'UPLOAD', ['EMAIL'],
             ['EMAIL', 'FIRST_NAME', 'custom_tag_1', 'custom_tag_2', 'custom_tag_3', 'custom_tag_4', 'custom_tag_5'], 2, 5)
        ])
    def test_irisV2_getAudienceById_Email_CustomTags(self, campaignType, testControlType, listType, schemaIdentifier,
                                                     schemaData, numberOfUser, numberOfCustomTags):
        list = CreateAudience.uploadList(campaignType, testControlType, schemaIdentifier=schemaIdentifier,
                                         schemaData=schemaData, numberOfUsers=numberOfUser,
                                         numberOfCustomTags=numberOfCustomTags, updateNode=True, lockNode=True,
                                         campaignCheck=False)
        CreateAudience.waitForGVDToBeUpdated(list['ID'], checkParams=False)
        CreateAudience.waitForReachabilityJobCompletion(list['VID'])
        response = GetAudienceById.getById(list['ID'])
        GetAudienceById.assertResponse(response, 200)
        GetListDBAssertion(list['ID'], response).check()

    @pytest.mark.parametrize(
        'campaignType,testControlType,listType,schemaIdentifier,schemaData,numberOfUser,numberOfCustomTags', [
            ('LIVE', 'ORG', 'UPLOAD', ['EMAIL'], ['EMAIL', 'custom_tag_1', 'FIRST_NAME'], 2, 1),
            ('LIVE', 'ORG', 'UPLOAD', ['EMAIL'], ['custom_tag_1', 'FIRST_NAME', 'EMAIL'], 2, 1),
            ('LIVE', 'ORG', 'UPLOAD', ['EMAIL'],
             ['EMAIL', 'FIRST_NAME', 'custom_tag_1', 'custom_tag_2', 'custom_tag_3', 'custom_tag_4', 'custom_tag_5'], 2,
             5),
            ('LIVE', 'ORG', 'UPLOAD', ['EMAIL'],
             ['EMAIL', 'custom_tag_1', 'FIRST_NAME', 'custom_tag_2', 'custom_tag_3', 'custom_tag_4', 'custom_tag_5'], 2,
             5),
            ('LIVE', 'ORG', 'UPLOAD', ['EMAIL'],
             ['FIRST_NAME', 'custom_tag_1', 'custom_tag_2', 'custom_tag_3', 'EMAIL', 'custom_tag_4', 'custom_tag_5'], 2,
             5),
            ('LIVE', 'ORG', 'UPLOAD', ['EMAIL'],
             ['EMAIL', 'FIRST_NAME', 'custom_tag_1', 'custom_tag_2', 'custom_tag_3', 'custom_tag_4', 'custom_tag_5'], 2,
             5),
            ('LIVE', 'ORG', 'UPLOAD', ['EMAIL'],
             ['EMAIL', 'custom_tag_1', 'custom_tag_2', 'custom_tag_3', 'custom_tag_4', 'custom_tag_5', 'FIRST_NAME'], 2,
             5),
        ])
    def test_irisV2_getAudienceById_Email_Variation_Identifiers(self, campaignType, testControlType, listType,
                                                                schemaIdentifier, schemaData, numberOfUser,
                                                                numberOfCustomTags):
        list = CreateAudience.uploadList(campaignType, testControlType, schemaIdentifier=schemaIdentifier,
                                         schemaData=schemaData, numberOfUsers=numberOfUser,
                                         numberOfCustomTags=numberOfCustomTags, updateNode=True, lockNode=True,
                                         campaignCheck=False)
        CreateAudience.waitForGVDToBeUpdated(list['ID'], checkParams=False)
        CreateAudience.waitForReachabilityJobCompletion(list['VID'])
        response = GetAudienceById.getById(list['ID'])
        GetAudienceById.assertResponse(response, 200)
        GetListDBAssertion(list['ID'], response, customTag=numberOfCustomTags).check()

    @pytest.mark.parametrize(
        'campaignType,testControlType,listType,schemaIdentifier,schemaData,numberOfUser,numberOfCustomTags', [
            ('LIVE', 'ORG', 'UPLOAD', ['EMAIL'],
             ['EMAIL', 'FIRST_NAME', 'custom_tag_5', 'custom_tag_4', 'custom_tag_3', 'custom_tag_2', 'custom_tag_1'], 2,
             5)
        ])
    def test_irisV2_getAudienceById_Email_CustomTags_InReverseOrder(self, campaignType, testControlType, listType,
                                                             schemaIdentifier, schemaData, numberOfUser,
                                                             numberOfCustomTags):
        list = CreateAudience.uploadList(campaignType, testControlType, schemaIdentifier=schemaIdentifier,
                                         schemaData=schemaData, numberOfUsers=numberOfUser,
                                         numberOfCustomTags=numberOfCustomTags, updateNode=True, lockNode=True,
                                         campaignCheck=False)
        CreateAudience.waitForGVDToBeUpdated(list['ID'], checkParams=False)
        CreateAudience.waitForReachabilityJobCompletion(list['VID'])
        response = GetAudienceById.getById(list['ID'])
        GetAudienceById.assertResponse(response, 200)
        GetListDBAssertion(list['ID'], response, customTag=numberOfCustomTags).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,schemaIdentifier,schemaData,numberOfUsers', [
        ('LIVE', 'ORG', 'UPLOAD', ['EMAIL'], ['EMAIL', 'FIRST_NAME'], 10000),
        ('LIVE', 'ORG', 'UPLOAD', ['EMAIL'], ['EMAIL', 'FIRST_NAME'], 50000),
        ('LIVE', 'ORG', 'UPLOAD', ['EMAIL'], ['EMAIL', 'FIRST_NAME'], 100000)
    ])
    def test_irisV2_bulk_getAudienceById_Email_bulkUpload_NewUser(self, campaignType, testControlType, listType,
                                                             schemaIdentifier,
                                                             schemaData, numberOfUsers):
        list = CreateAudience.uploadList(campaignType, testControlType, schemaIdentifier=schemaIdentifier,
                                         schemaData=schemaData, numberOfUsers=numberOfUsers, updateNode=True,
                                         lockNode=True,
                                         campaignCheck=False)
        CreateAudience.waitForListToProcess(list['ID'], numberOfUsers)
        response = GetAudienceById.getById(list['ID'])
        GetAudienceById.assertResponse(response, 200)
        GetListDBAssertion(list['ID'], response, reachabilityCheck=False, bulkCaseSkip=False).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,schemaIdentifier,schemaData,numberOfUsers', [
        ('LIVE', 'ORG', 'UPLOAD', ['EMAIL'], ['EMAIL', 'FIRST_NAME'], 10000),
        ('LIVE', 'ORG', 'UPLOAD', ['EMAIL'], ['EMAIL', 'FIRST_NAME'], 50000),
        ('LIVE', 'ORG', 'UPLOAD', ['EMAIL'], ['EMAIL', 'FIRST_NAME'], 100000)
    ])
    def test_irisV2_bulk_getAudienceById_Email_bulkUpload_withExistingUsers(self, campaignType, testControlType, listType,
                                                                       schemaIdentifier, schemaData, numberOfUsers):
        list = CreateAudience.uploadList(campaignType, testControlType, schemaIdentifier=schemaIdentifier,
                                         schemaData=schemaData, numberOfUsers=numberOfUsers, newUser=False,
                                         updateNode=True,
                                         lockNode=True, campaignCheck=False)
        CreateAudience.waitForListToProcess(list['ID'], numberOfUsers)
        response = GetAudienceById.getById(list['ID'])
        GetAudienceById.assertResponse(response, 200)
        GetListDBAssertion(list['ID'], response, reachabilityCheck=False, bulkCaseSkip=False).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,schemaIdentifier,schemaData', [
        ('LIVE', 'ORG', 'UPLOAD', ['EMAIL'], ['EMAIL', 'FIRST_NAME']),
        ('LIVE', 'CUSTOM', 'UPLOAD', ['EMAIL'], ['EMAIL', 'FIRST_NAME']),
        ('LIVE', 'SKIP', 'UPLOAD', ['EMAIL'], ['EMAIL', 'FIRST_NAME'])
    ])
    def test_irisV2_getAudienceById_Email_InActiveList(self, campaignType, testControlType, listType, schemaIdentifier,
                                                       schemaData):
        list = CreateAudience.uploadList(campaignType, testControlType, schemaIdentifier=schemaIdentifier,
                                         schemaData=schemaData, updateNode=True, lockNode=True, campaignCheck=False)
        list_Calls().updateGroupVersionDetailAsInactive(list['ID'])
        response = GetAudienceById.getById(list['ID'])
        Assertion.constructAssertion('entity' not in response['json'], 'For Inactive List No Entry Found from GetCall')

    @pytest.mark.parametrize('campaignType,testControlType,listType,numberOfFiles,schemaIdentifier,schemaData', [
        ('LIVE', 'ORG', 'UPLOAD', 2, ['EMAIL'], ['EMAIL', 'FIRST_NAME']),
        ('LIVE', 'ORG', 'UPLOAD', 3, ['EMAIL'], ['EMAIL', 'FIRST_NAME']),
        ('LIVE', 'ORG', 'UPLOAD', 4, ['EMAIL'], ['EMAIL', 'FIRST_NAME']),
        ('LIVE', 'ORG', 'UPLOAD', 5, ['EMAIL'], ['EMAIL', 'FIRST_NAME']),
        ('LIVE', 'CUSTOM', 'UPLOAD', 5, ['EMAIL'], ['EMAIL', 'FIRST_NAME']),
        ('LIVE', 'SKIP', 'UPLOAD', 3, ['EMAIL'], ['EMAIL', 'FIRST_NAME'])
    ])
    def test_irisV2_getAudienceById_Email_ListCreatedWithMultipleFiles(self, campaignType, testControlType, listType,
                                                                       numberOfFiles, schemaIdentifier, schemaData):
        list = CreateAudience.uploadList(campaignType, testControlType, schemaIdentifier=schemaIdentifier,
                                         schemaData=schemaData, numberOfFiles=numberOfFiles, updateNode=True,
                                         lockNode=True,
                                         campaignCheck=False)
        CreateAudience.waitForGVDToBeUpdated(list['ID'], checkParams=False)
        CreateAudience.waitForReachabilityJobCompletion(list['VID'])
        response = GetAudienceById.getById(list['ID'])
        GetAudienceById.assertResponse(response, 200)
        GetListDBAssertion(list['ID'], response, reachabilityCheck=False).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,schemaIdentifier,schemaData', [
        ('LIVE', 'ORG', 'UPLOAD', ['USER_ID'], ['USER_ID', 'FIRST_NAME']),
    ])
    def test_irisV2_getAudienceById_UserId_ExistingUser(self, campaignType, testControlType, listType,
                                                               schemaIdentifier, schemaData):
        list = CreateAudience.uploadList(campaignType, testControlType, schemaIdentifier=schemaIdentifier,
                                         schemaData=schemaData, newUser=False, updateNode=True, lockNode=True,
                                         campaignCheck=False)
        CreateAudience.waitForGVDToBeUpdated(list['ID'], checkCustomerCount=False)
        response = GetAudienceById.getById(list['ID'])
        GetAudienceById.assertResponse(response, 200)
        GetListDBAssertion(list['ID'], response, campaignHashLookUp=False, reachabilityCheck=False,
                           createAudienceJob=False).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,schemaIdentifier,schemaData', [
        ('UPCOMING', 'ORG', 'UPLOAD', ['USER_ID'], ['USER_ID', 'FIRST_NAME']),
        ('LAPSED', 'ORG', 'UPLOAD', ['USER_ID'], ['USER_ID', 'FIRST_NAME']),
        ('LIVE', 'CUSTOM', 'UPLOAD', ['USER_ID'], ['USER_ID', 'FIRST_NAME']),
        ('UPCOMING', 'CUSTOM', 'UPLOAD', ['USER_ID'], ['USER_ID', 'FIRST_NAME']),
        ('LAPSED', 'CUSTOM', 'UPLOAD', ['USER_ID'], ['USER_ID', 'FIRST_NAME']),
        ('LIVE', 'SKIP', 'UPLOAD', ['USER_ID'], ['USER_ID', 'FIRST_NAME']),
        ('UPCOMING', 'SKIP', 'UPLOAD', ['USER_ID'], ['USER_ID', 'FIRST_NAME']),
        ('LAPSED', 'SKIP', 'UPLOAD', ['USER_ID'], ['USER_ID', 'FIRST_NAME'])
    ])
    def test_irisV2_getAudienceById_UserId_ExistingUser(self, campaignType, testControlType, listType, schemaIdentifier,
                                                        schemaData):
        list = CreateAudience.uploadList(campaignType, testControlType, schemaIdentifier=schemaIdentifier,
                                         schemaData=schemaData, newUser=False, updateNode=True, lockNode=True,
                                         campaignCheck=False)
        CreateAudience.waitForGVDToBeUpdated(list['ID'], checkCustomerCount=False)
        response = GetAudienceById.getById(list['ID'])
        GetAudienceById.assertResponse(response, 200)
        GetListDBAssertion(list['ID'], response, campaignHashLookUp=False, reachabilityCheck=False,
                           createAudienceJob=False).check()

    @pytest.mark.parametrize(
        'campaignType,testControlType,listType,schemaIdentifier,schemaData,numberOfUser,numberOfCustomTags', [
            ('LIVE', 'ORG', 'UPLOAD', ['USER_ID'], ['USER_ID', 'FIRST_NAME', 'custom_tag_1'], 2, 1),
            ('LIVE', 'ORG', 'UPLOAD', ['USER_ID'], ['USER_ID', 'FIRST_NAME', 'custom_tag_1', 'custom_tag_2'], 2, 2),
            ('LIVE', 'ORG', 'UPLOAD', ['USER_ID'], ['USER_ID', 'FIRST_NAME', 'custom_tag_1', 'custom_tag_2', 'custom_tag_3'], 2, 3),
            ('LIVE', 'ORG', 'UPLOAD', ['USER_ID'], ['USER_ID', 'FIRST_NAME', 'custom_tag_1', 'custom_tag_2', 'custom_tag_3', 'custom_tag_4'], 2, 4),
            ('LIVE', 'ORG', 'UPLOAD', ['USER_ID'], ['USER_ID', 'FIRST_NAME', 'custom_tag_1', 'custom_tag_2', 'custom_tag_3', 'custom_tag_4', 'custom_tag_5'], 2, 5)
        ])
    def test_irisV2_getAudienceById_UserId_CustomTags(self, campaignType, testControlType, listType, schemaIdentifier,
                                                      schemaData, numberOfUser, numberOfCustomTags):
        list = CreateAudience.uploadList(campaignType, testControlType, schemaIdentifier=schemaIdentifier,
                                         schemaData=schemaData, newUser=False, numberOfUsers=numberOfUser,
                                         numberOfCustomTags=numberOfCustomTags, updateNode=True, lockNode=True,
                                         campaignCheck=False)
        CreateAudience.waitForGVDToBeUpdated(list['ID'], checkParams=False)
        response = GetAudienceById.getById(list['ID'])
        GetAudienceById.assertResponse(response, 200)
        GetListDBAssertion(list['ID'], response).check()

    @pytest.mark.parametrize(
        'campaignType,testControlType,listType,schemaIdentifier,schemaData,numberOfUser,numberOfCustomTags', [
            ('LIVE', 'ORG', 'UPLOAD', ['USER_ID'], ['USER_ID', 'custom_tag_1', 'FIRST_NAME'], 2, 1),
            ('LIVE', 'ORG', 'UPLOAD', ['USER_ID'], ['custom_tag_1', 'FIRST_NAME', 'USER_ID'], 2, 1),
            ('LIVE', 'ORG', 'UPLOAD', ['USER_ID'],
             ['USER_ID', 'FIRST_NAME', 'custom_tag_1', 'custom_tag_2', 'custom_tag_3', 'custom_tag_4', 'custom_tag_5'],
             2,
             5),
            ('LIVE', 'ORG', 'UPLOAD', ['USER_ID'],
             ['USER_ID', 'custom_tag_1', 'FIRST_NAME', 'custom_tag_2', 'custom_tag_3', 'custom_tag_4', 'custom_tag_5'],
             2,
             5),
            ('LIVE', 'ORG', 'UPLOAD', ['USER_ID'],
             ['FIRST_NAME', 'custom_tag_1', 'custom_tag_2', 'custom_tag_3', 'USER_ID', 'custom_tag_4', 'custom_tag_5'],
             2,
             5),
            ('LIVE', 'ORG', 'UPLOAD', ['USER_ID'],
             ['USER_ID', 'FIRST_NAME', 'custom_tag_1', 'custom_tag_2', 'custom_tag_3', 'custom_tag_4', 'custom_tag_5'],
             2,
             5),
            ('LIVE', 'ORG', 'UPLOAD', ['USER_ID'],
             ['USER_ID', 'custom_tag_1', 'custom_tag_2', 'custom_tag_3', 'custom_tag_4', 'custom_tag_5', 'FIRST_NAME'],
             2,
             5),
        ])
    def test_irisV2_getAudienceById_UserId_Variation_Identifiers(self, campaignType, testControlType, listType,
                                                                 schemaIdentifier, schemaData, numberOfUser,
                                                                 numberOfCustomTags):
        list = CreateAudience.uploadList(campaignType, testControlType, schemaIdentifier=schemaIdentifier,
                                         schemaData=schemaData, newUser=False, numberOfUsers=numberOfUser,
                                         numberOfCustomTags=numberOfCustomTags, updateNode=True, lockNode=True,
                                         campaignCheck=False)
        CreateAudience.waitForGVDToBeUpdated(list['ID'], checkParams=False)
        response = GetAudienceById.getById(list['ID'])
        GetAudienceById.assertResponse(response, 200)
        GetListDBAssertion(list['ID'], response, customTag=numberOfCustomTags).check()

    @pytest.mark.parametrize(
        'campaignType,testControlType,listType,schemaIdentifier,schemaData,numberOfUser,numberOfCustomTags', [
            ('LIVE', 'ORG', 'UPLOAD', ['USER_ID'],
             ['USER_ID', 'FIRST_NAME', 'custom_tag_5', 'custom_tag_4', 'custom_tag_3', 'custom_tag_2', 'custom_tag_1'],
             2,
             5)
        ])
    def test_irisV2_getAudienceById_UserId_CustomTags_InReverseOrder(self, campaignType, testControlType, listType,
                                                             schemaIdentifier, schemaData, numberOfUser,
                                                             numberOfCustomTags):
        list = CreateAudience.uploadList(campaignType, testControlType, schemaIdentifier=schemaIdentifier,
                                         schemaData=schemaData, newUser=False, numberOfUsers=numberOfUser,
                                         numberOfCustomTags=numberOfCustomTags, updateNode=True, lockNode=True,
                                         campaignCheck=False)
        CreateAudience.waitForGVDToBeUpdated(list['ID'], checkParams=False)
        response = GetAudienceById.getById(list['ID'])
        GetAudienceById.assertResponse(response, 200)
        GetListDBAssertion(list['ID'], response, customTag=numberOfCustomTags).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,schemaIdentifier,schemaData', [
        ('LIVE', 'ORG', 'UPLOAD', ['USER_ID'], ['USER_ID', 'FIRST_NAME']),
        ('LIVE', 'CUSTOM', 'UPLOAD', ['USER_ID'], ['USER_ID', 'FIRST_NAME']),
        ('LIVE', 'SKIP', 'UPLOAD', ['USER_ID'], ['USER_ID', 'FIRST_NAME'])
    ])
    def test_irisV2_getAudienceById_UserId_InActiveList(self, campaignType, testControlType, listType, schemaIdentifier,
                                                        schemaData):
        list = CreateAudience.uploadList(campaignType, testControlType, schemaIdentifier=schemaIdentifier,
                                         schemaData=schemaData, newUser=False, updateNode=True, lockNode=True,
                                         campaignCheck=False)
        list_Calls().updateGroupVersionDetailAsInactive(list['ID'])
        response = GetAudienceById.getById(list['ID'])
        Assertion.constructAssertion('entity' not in response['json'], 'For Inactive List No Entry Found from GetCall')

    @pytest.mark.parametrize('campaignType,testControlType,listType,numberOfFiles,schemaIdentifier,schemaData', [
        ('LIVE', 'ORG', 'UPLOAD', 2, ['USER_ID'], ['USER_ID', 'FIRST_NAME']),
        ('LIVE', 'ORG', 'UPLOAD', 3, ['USER_ID'], ['USER_ID', 'FIRST_NAME']),
        ('LIVE', 'ORG', 'UPLOAD', 4, ['USER_ID'], ['USER_ID', 'FIRST_NAME']),
        ('LIVE', 'ORG', 'UPLOAD', 5, ['USER_ID'], ['USER_ID', 'FIRST_NAME']),
        ('LIVE', 'CUSTOM', 'UPLOAD', 5, ['USER_ID'], ['USER_ID', 'FIRST_NAME']),
        ('LIVE', 'SKIP', 'UPLOAD', 3, ['USER_ID'], ['USER_ID', 'FIRST_NAME'])
    ])
    def test_irisV2_getAudienceById_UserId_ListCreatedWithMultipleFiles(self, campaignType, testControlType, listType,
                                                                        numberOfFiles, schemaIdentifier, schemaData):
        list = CreateAudience.uploadList(campaignType, testControlType, schemaIdentifier=schemaIdentifier,
                                         schemaData=schemaData, numberOfUsers=1, newUser=False,
                                         numberOfFiles=numberOfFiles,
                                         updateNode=True, lockNode=True, campaignCheck=False)
        CreateAudience.waitForGVDToBeUpdated(list['ID'], checkParams=False)
        response = GetAudienceById.getById(list['ID'])
        GetAudienceById.assertResponse(response, 200)
        GetListDBAssertion(list['ID'], response).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,schemaIdentifier,schemaData', [
        ('LIVE', 'ORG', 'UPLOAD', ['EXTERNAL_ID'], ['EXTERNAL_ID', 'FIRST_NAME']),
    ])
    def test_irisV2_getAudienceById_ExternalId_ExistingUser(self, campaignType, testControlType, listType,
                                                                   schemaIdentifier, schemaData):
        list = CreateAudience.uploadList(campaignType, testControlType, schemaIdentifier=schemaIdentifier,
                                         schemaData=schemaData, newUser=False, updateNode=True, lockNode=True,
                                         campaignCheck=False)
        CreateAudience.waitForGVDToBeUpdated(list['ID'], checkCustomerCount=False)
        response = GetAudienceById.getById(list['ID'])
        GetAudienceById.assertResponse(response, 200)
        GetListDBAssertion(list['ID'], response, campaignHashLookUp=False, reachabilityCheck=False,
                           createAudienceJob=False).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,schemaIdentifier,schemaData', [
        ('UPCOMING', 'ORG', 'UPLOAD', ['EXTERNAL_ID'], ['EXTERNAL_ID', 'FIRST_NAME']),
        ('LAPSED', 'ORG', 'UPLOAD', ['EXTERNAL_ID'], ['EXTERNAL_ID', 'FIRST_NAME']),
        ('LIVE', 'CUSTOM', 'UPLOAD', ['EXTERNAL_ID'], ['EXTERNAL_ID', 'FIRST_NAME']),
        ('UPCOMING', 'CUSTOM', 'UPLOAD', ['EXTERNAL_ID'], ['EXTERNAL_ID', 'FIRST_NAME']),
        ('LAPSED', 'CUSTOM', 'UPLOAD', ['EXTERNAL_ID'], ['EXTERNAL_ID', 'FIRST_NAME']),
        ('LIVE', 'SKIP', 'UPLOAD', ['EXTERNAL_ID'], ['EXTERNAL_ID', 'FIRST_NAME']),
        ('UPCOMING', 'SKIP', 'UPLOAD', ['EXTERNAL_ID'], ['EXTERNAL_ID', 'FIRST_NAME']),
        ('LAPSED', 'SKIP', 'UPLOAD', ['EXTERNAL_ID'], ['EXTERNAL_ID', 'FIRST_NAME'])
    ])
    def test_irisV2_getAudienceById_ExternalId_ExistingUser(self, campaignType, testControlType, listType,
                                                            schemaIdentifier,
                                                            schemaData):
        list = CreateAudience.uploadList(campaignType, testControlType, schemaIdentifier=schemaIdentifier,
                                         schemaData=schemaData, newUser=False, updateNode=True, lockNode=True,
                                         campaignCheck=False)
        CreateAudience.waitForGVDToBeUpdated(list['ID'], checkCustomerCount=False)
        response = GetAudienceById.getById(list['ID'])
        GetAudienceById.assertResponse(response, 200)
        GetListDBAssertion(list['ID'], response, campaignHashLookUp=False, reachabilityCheck=False,
                           createAudienceJob=False).check()

    @pytest.mark.parametrize(
        'campaignType,testControlType,listType,schemaIdentifier,schemaData,numberOfUser,numberOfCustomTags', [
            ('LIVE', 'ORG', 'UPLOAD', ['EXTERNAL_ID'], ['EXTERNAL_ID', 'FIRST_NAME', 'custom_tag_1'], 2, 1),
            ('LIVE', 'ORG', 'UPLOAD', ['EXTERNAL_ID'], ['EXTERNAL_ID', 'FIRST_NAME', 'custom_tag_1', 'custom_tag_2'], 2,
             2),
            ('LIVE', 'ORG', 'UPLOAD', ['EXTERNAL_ID'],
             ['EXTERNAL_ID', 'FIRST_NAME', 'custom_tag_1', 'custom_tag_2', 'custom_tag_3'], 2, 3),
            ('LIVE', 'ORG', 'UPLOAD', ['EXTERNAL_ID'],
             ['EXTERNAL_ID', 'FIRST_NAME', 'custom_tag_1', 'custom_tag_2', 'custom_tag_3', 'custom_tag_4'], 2, 4),
            ('LIVE', 'ORG', 'UPLOAD', ['EXTERNAL_ID'],
             ['EXTERNAL_ID', 'FIRST_NAME', 'custom_tag_1', 'custom_tag_2', 'custom_tag_3', 'custom_tag_4',
              'custom_tag_5'],
             2, 5)
        ])
    def test_irisV2_getAudienceById_ExternalId_CustomTags(self, campaignType, testControlType, listType,
                                                          schemaIdentifier,
                                                          schemaData, numberOfUser, numberOfCustomTags):
        list = CreateAudience.uploadList(campaignType, testControlType, schemaIdentifier=schemaIdentifier,
                                         schemaData=schemaData, newUser=False, numberOfUsers=numberOfUser,
                                         numberOfCustomTags=numberOfCustomTags, updateNode=True, lockNode=True,
                                         campaignCheck=False)
        CreateAudience.waitForGVDToBeUpdated(list['ID'], checkParams=False)
        response = GetAudienceById.getById(list['ID'])
        GetAudienceById.assertResponse(response, 200)
        GetListDBAssertion(list['ID'], response).check()

    @pytest.mark.parametrize(
        'campaignType,testControlType,listType,schemaIdentifier,schemaData,numberOfUser,numberOfCustomTags', [
            ('LIVE', 'ORG', 'UPLOAD', ['EXTERNAL_ID'], ['EXTERNAL_ID', 'custom_tag_1', 'FIRST_NAME'], 2, 1),
            ('LIVE', 'ORG', 'UPLOAD', ['EXTERNAL_ID'], ['custom_tag_1', 'FIRST_NAME', 'EXTERNAL_ID'], 2, 1),
            ('LIVE', 'ORG', 'UPLOAD', ['EXTERNAL_ID'],
             ['EXTERNAL_ID', 'FIRST_NAME', 'custom_tag_1', 'custom_tag_2', 'custom_tag_3', 'custom_tag_4',
              'custom_tag_5'],
             2, 5),
            ('LIVE', 'ORG', 'UPLOAD', ['EXTERNAL_ID'],
             ['EXTERNAL_ID', 'custom_tag_1', 'FIRST_NAME', 'custom_tag_2', 'custom_tag_3', 'custom_tag_4',
              'custom_tag_5'],
             2, 5),
            ('LIVE', 'ORG', 'UPLOAD', ['EXTERNAL_ID'],
             ['FIRST_NAME', 'custom_tag_1', 'custom_tag_2', 'custom_tag_3', 'EXTERNAL_ID', 'custom_tag_4',
              'custom_tag_5'],
             2, 5),
            ('LIVE', 'ORG', 'UPLOAD', ['EXTERNAL_ID'],
             ['EXTERNAL_ID', 'FIRST_NAME', 'custom_tag_1', 'custom_tag_2', 'custom_tag_3', 'custom_tag_4',
              'custom_tag_5'],
             2, 5),
            ('LIVE', 'ORG', 'UPLOAD', ['EXTERNAL_ID'],
             ['EXTERNAL_ID', 'custom_tag_1', 'custom_tag_2', 'custom_tag_3', 'custom_tag_4', 'custom_tag_5',
              'FIRST_NAME'],
             2, 5),
        ])
    def test_irisV2_getAudienceById_ExternalId_Variation_Identifiers(self, campaignType, testControlType, listType,
                                                                     schemaIdentifier, schemaData, numberOfUser,
                                                                     numberOfCustomTags):
        list = CreateAudience.uploadList(campaignType, testControlType, schemaIdentifier=schemaIdentifier,
                                         schemaData=schemaData, newUser=False, numberOfUsers=numberOfUser,
                                         numberOfCustomTags=numberOfCustomTags, updateNode=True, lockNode=True,
                                         campaignCheck=False)
        CreateAudience.waitForGVDToBeUpdated(list['ID'], checkParams=False)
        response = GetAudienceById.getById(list['ID'])
        GetAudienceById.assertResponse(response, 200)
        GetListDBAssertion(list['ID'], response, customTag=numberOfCustomTags).check()

    @pytest.mark.parametrize(
        'campaignType,testControlType,listType,schemaIdentifier,schemaData,numberOfUser,numberOfCustomTags', [
            ('LIVE', 'ORG', 'UPLOAD', ['EXTERNAL_ID'],
             ['EXTERNAL_ID', 'FIRST_NAME', 'custom_tag_5', 'custom_tag_4', 'custom_tag_3', 'custom_tag_2',
              'custom_tag_1'],
             2, 5)
        ])
    def test_irisV2_createAudience_ExternalId_CustomTags_InReverseOrder(self, campaignType, testControlType, listType,
                                                             schemaIdentifier, schemaData, numberOfUser,
                                                             numberOfCustomTags):
        list = CreateAudience.uploadList(campaignType, testControlType, schemaIdentifier=schemaIdentifier,
                                         schemaData=schemaData, newUser=False, numberOfUsers=numberOfUser,
                                         numberOfCustomTags=numberOfCustomTags, updateNode=True, lockNode=True,
                                         campaignCheck=False)
        CreateAudience.waitForGVDToBeUpdated(list['ID'], checkParams=False)
        response = GetAudienceById.getById(list['ID'])
        GetAudienceById.assertResponse(response, 200)
        GetListDBAssertion(list['ID'], response, customTag=numberOfCustomTags).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,schemaIdentifier,schemaData', [
        ('LIVE', 'ORG', 'UPLOAD', ['EXTERNAL_ID'], ['EXTERNAL_ID', 'FIRST_NAME']),
        ('LIVE', 'CUSTOM', 'UPLOAD', ['EXTERNAL_ID'], ['EXTERNAL_ID', 'FIRST_NAME']),
        ('LIVE', 'SKIP', 'UPLOAD', ['EXTERNAL_ID'], ['EXTERNAL_ID', 'FIRST_NAME'])
    ])
    def test_irisV2_getAudienceById_ExternalId_InActiveList(self, campaignType, testControlType, listType,
                                                            schemaIdentifier,
                                                            schemaData):
        list = CreateAudience.uploadList(campaignType, testControlType, schemaIdentifier=schemaIdentifier,
                                         schemaData=schemaData, newUser=False, updateNode=True, lockNode=True,
                                         campaignCheck=False)
        list_Calls().updateGroupVersionDetailAsInactive(list['ID'])
        response = GetAudienceById.getById(list['ID'])
        Assertion.constructAssertion('entity' not in response['json'], 'For Inactive List No Entry Found from GetCall')

    @pytest.mark.parametrize('campaignType,testControlType,listType,numberOfFiles,schemaIdentifier,schemaData', [
        ('LIVE', 'ORG', 'UPLOAD', 2, ['EXTERNAL_ID'], ['EXTERNAL_ID', 'FIRST_NAME']),
        ('LIVE', 'ORG', 'UPLOAD', 3, ['EXTERNAL_ID'], ['EXTERNAL_ID', 'FIRST_NAME']),
        ('LIVE', 'ORG', 'UPLOAD', 4, ['EXTERNAL_ID'], ['EXTERNAL_ID', 'FIRST_NAME']),
        ('LIVE', 'ORG', 'UPLOAD', 5, ['EXTERNAL_ID'], ['EXTERNAL_ID', 'FIRST_NAME']),
        ('LIVE', 'CUSTOM', 'UPLOAD', 5, ['EXTERNAL_ID'], ['EXTERNAL_ID', 'FIRST_NAME']),
        ('LIVE', 'SKIP', 'UPLOAD', 3, ['EXTERNAL_ID'], ['EXTERNAL_ID', 'FIRST_NAME'])
    ])
    def test_irisV2_getAudienceById_ExternalId_ListCreatedWithMultipleFiles(self, campaignType, testControlType,
                                                                            listType,
                                                                            numberOfFiles, schemaIdentifier,
                                                                            schemaData):
        list = CreateAudience.uploadList(campaignType, testControlType, schemaIdentifier=schemaIdentifier,
                                         schemaData=schemaData, numberOfUsers=1, newUser=False,
                                         numberOfFiles=numberOfFiles,
                                         updateNode=True, lockNode=True, campaignCheck=False)
        CreateAudience.waitForGVDToBeUpdated(list['ID'], checkParams=False)
        response = GetAudienceById.getById(list['ID'])
        GetAudienceById.assertResponse(response, 200)
        GetListDBAssertion(list['ID'], response).check()

    def test_irisV2_getAudienceById_NC_UnknownList(self):
        response = GetAudienceById.getById(999999)
        GetAudienceById.assertResponse(response, 400, 5006,'invalid request : group not found')
        Assertion.constructAssertion('entity' not in response['json'], 'For Unknown List No Entry Found from GetCall')

    def test_irisV2_getAudienceById_NC_NegativeListId(self):
        response = GetAudienceById.getById(-999999)
        GetAudienceById.assertResponse(response, 400, 102, 'Invalid request : Group id should be greater than zero')
        Assertion.constructAssertion('entity' not in response['json'], 'For Unknown List No Entry Found from GetCall')

    def test_irisV2_getAudienceById_NC_ListIdAsSpecialCharacter(self):
        response = GetAudienceById.getById('99#$%')
        GetAudienceById.assertResponse(response,400, 5006,'invalid request : group not found')
        Assertion.constructAssertion('entity' not in response['json'], 'For Unknown List No Entry Found from GetCall')

    @pytest.mark.parametrize('caseName,errorReasons', [
        ('invalid_mobile', {'reason': 'INVALID_MOBILE_NUMBER', 'numberOfUser': 4}),
        ('empty_mobile', {'reason': 'EMPTY_MOBILE_NUMBER', 'numberOfUser': 1}),
        ('duplicatemobile_withCountryCode', {'reason': 'Duplicate mobile number', 'numberOfUser': 1}),
        ('duplicatemobile_withoutCountryCode', {'reason': 'Duplicate mobile number', 'numberOfUser': 1}),
        ('duplicatemobile_with_withoutCountryCode', {'reason': 'Duplicate mobile number', 'numberOfUser': 1}),
        ('duplicatemobile_multipletimessamenumber', {'reason': 'Duplicate mobile number', 'numberOfUser': 3}),
        ('first_name_empty', {'reason': 'Data does not match with schema', 'numberOfUser': 1}),
        ('first_name_exceed_100character', {'reason': ' first name exceeds 100 characters', 'numberOfUser': 1}),
        ('data_does_not_match_schema', {'reason': 'Data does not match with schema', 'numberOfUser': 1}),
        ('multiple_data_does_not_match_schema', {'reason': 'Data does not match with schema', 'numberOfUser': 1}),
        ('multiple_error_in_same_file',
         {'reason': ['INVALID_MOBILE_NUMBER', 'EMPTY_MOBILE_NUMBER', 'Duplicate mobile number'], 'numberOfUser': 3}),
        ('duplicateuserwithbulk', {'reason': 'Duplicate mobile number', 'numberOfUser': 7996})
    ])
    def test_irisV2_getAudienceById_NC_ErrorInUpload_mobile(self, caseName, errorReasons):
        payload, filePath = CreateAudience.createPayloadForSpecificCase(caseName)
        listDetail = CreateAudience.uploadList('LIVE', 'ORG', payload=payload, updateNode=True, lockNode=True,
                                               campaignCheck=False)
        CreateAudience.waitForGVDToBeUpdated(listDetail['ID'])
        response = GetAudienceById.getById(listDetail['ID'])
        GetAudienceById.assertResponse(response, 200)
        GetListDBAssertion(listDetail['ID'], response, errorReasons={filePath.split('/')[-1]: errorReasons},
                           reachabilityCheck=False).check()

    @pytest.mark.parametrize('caseName,errorReasons', [
        ('invalid_email', {'reason': 'Invalid Email Id', 'numberOfUser': 5}),

    ])
    def test_irisV2_getAudienceById_NC_ErrorInUpload_Email(self, caseName, errorReasons):
        payload, filePath = CreateAudience.createPayloadForSpecificCase(caseName, identifier='email')
        listDetail = CreateAudience.uploadList('LIVE', 'ORG', payload=payload, updateNode=True, lockNode=True,
                                               campaignCheck=False)
        CreateAudience.waitForGVDToBeUpdated(listDetail['ID'])
        response = GetAudienceById.getById(listDetail['ID'])
        GetAudienceById.assertResponse(response, 200)
        GetListDBAssertion(listDetail['ID'], response, errorReasons={filePath.split('/')[-1]: errorReasons},
                           reachabilityCheck=False).check()

    @pytest.mark.parametrize('caseName,errorReasons', [

        ('multiple_error_in_same_file_email', {'reason': ['Invalid Email Id', 'Duplicate Email'], 'numberOfUser': 3}),
        ('duplicateuserwithbulkemail', {'reason': 'Duplicate Email', 'numberOfUser': 7996})
    ])
    def test_irisV2_getAudienceById_NC_ErrorInUpload_Email(self, caseName, errorReasons):
        payload, filePath = CreateAudience.createPayloadForSpecificCase(caseName, identifier='email')
        listDetail = CreateAudience.uploadList('LIVE', 'ORG', payload=payload, updateNode=True, lockNode=True,
                                               campaignCheck=False)
        CreateAudience.waitForGVDToBeUpdated(listDetail['ID'])
        response = GetAudienceById.getById(listDetail['ID'])
        GetAudienceById.assertResponse(response, 200)
        GetListDBAssertion(listDetail['ID'], response, errorReasons={filePath.split('/')[-1]: errorReasons},
                           reachabilityCheck=False).check()

    @pytest.mark.parametrize('caseName,errorReasons', [
        ('invalid_userid', {'reason': 'User does not belong to org', 'numberOfUser': 1}),
        ('multiple_error_in_same_file_userid',
         {'reason': ['User does not belong to org', 'Duplicate User Id'], 'numberOfUser': 2})
    ])
    def test_irisV2_getAudienceById_NC_ErrorInUpload_UserId(self, caseName, errorReasons):
        payload, filePath = CreateAudience.createPayloadForSpecificCase(caseName, identifier='userid')
        listDetail = CreateAudience.uploadList('LIVE', 'ORG', payload=payload, updateNode=True, lockNode=True,
                                               campaignCheck=False)
        CreateAudience.waitForGVDToBeUpdated(listDetail['ID'])
        response = GetAudienceById.getById(listDetail['ID'])
        GetAudienceById.assertResponse(response, 200)
        GetListDBAssertion(listDetail['ID'], response, errorReasons={filePath.split('/')[-1]: errorReasons},
                           reachabilityCheck=False).check()

    @pytest.mark.parametrize('caseName,errorReasons', [
        ('invalid_externalid', {'reason': 'invalid external id', 'numberOfUser': 1}),
        ('multiple_error_in_same_file_externalid',
         {'reason': ['invalid external id', 'duplicate external id'], 'numberOfUser': 2})
    ])
    def test_irisV2_getAudienceById_NC_ErrorInUpload_ExternalId(self, caseName, errorReasons):
        payload, filePath = CreateAudience.createPayloadForSpecificCase(caseName, identifier='externalid')
        listDetail = CreateAudience.uploadList('LIVE', 'ORG', payload=payload, updateNode=True, lockNode=True,
                                               campaignCheck=False)
        CreateAudience.waitForGVDToBeUpdated(listDetail['ID'])
        response = GetAudienceById.getById(listDetail['ID'])
        GetAudienceById.assertResponse(response, 200)
        GetListDBAssertion(listDetail['ID'], response, errorReasons={filePath.split('/')[-1]: errorReasons},
                           reachabilityCheck=False).check()

    @pytest.mark.parametrize('caseName,errorReasons', [
        ('empty_mobile_bulk', {'reason': ['EMPTY_MOBILE_NUMBER', 'Duplicate mobile number'], 'numberOfUser': 2999}),
        ('multiple_error_in_same_file_bulk',
         {'reason': ['INVALID_MOBILE_NUMBER', 'EMPTY_MOBILE_NUMBER', 'Duplicate mobile number'], 'numberOfUser': 60000})
    ])
    def test_irisV2__bulk_getAudienceById_bulkCase_ErrorInUpload_withSingleFile(self, caseName, errorReasons):
        payload, filePath = CreateAudience.createPayloadForSpecificCase(caseName)
        listDetail = CreateAudience.uploadList('LIVE', 'ORG', payload=payload, updateNode=True, lockNode=True,
                                               campaignCheck=False)
        CreateAudience.waitForGVDToBeUpdated(listDetail['ID'])
        response = GetAudienceById.getById(listDetail['ID'])
        GetAudienceById.assertResponse(response, 200)
        GetListDBAssertion(listDetail['ID'], response, errorReasons={filePath.split('/')[-1]: errorReasons},
                           reachabilityCheck=False).check()

    @pytest.mark.parametrize('caseName,errorReason1,errorReason2', [
        ('invalid_mobile', {'reason': 'INVALID_MOBILE_NUMBER', 'numberOfUser': 4},
         {'reason': 'INVALID_MOBILE_NUMBER', 'numberOfUser': 4}),
        ('empty_mobile', {'reason': 'EMPTY_MOBILE_NUMBER', 'numberOfUser': 1},
         {'reason': 'EMPTY_MOBILE_NUMBER', 'numberOfUser': 1}),
        ('duplicatemobile_withCountryCode', {'reason': 'Duplicate mobile number', 'numberOfUser': 1},
         {'reason': 'Duplicate mobile number', 'numberOfUser': 1}),
        ('duplicatemobile_withoutCountryCode', {'reason': 'Duplicate mobile number', 'numberOfUser': 1},
         {'reason': 'Duplicate mobile number', 'numberOfUser': 1}),
        ('duplicatemobile_with_withoutCountryCode', {'reason': 'Duplicate mobile number', 'numberOfUser': 1},
         {'reason': 'Duplicate mobile number', 'numberOfUser': 1}),
        ('duplicatemobile_multipletimessamenumber', {'reason': 'Duplicate mobile number', 'numberOfUser': 3},
         {'reason': 'Duplicate mobile number', 'numberOfUser': 3}),
        ('first_name_empty', {'reason': 'Data does not match with schema', 'numberOfUser': 1},
         {'reason': 'Data does not match with schema', 'numberOfUser': 1}),
        ('first_name_exceed_100character', {'reason': ' first name exceeds 100 characters', 'numberOfUser': 1},
         {'reason': ' first name exceeds 100 characters', 'numberOfUser': 1}),
        ('data_does_not_match_schema', {'reason': 'Data does not match with schema', 'numberOfUser': 1},
         {'reason': 'Data does not match with schema', 'numberOfUser': 1}),
        ('multiple_data_does_not_match_schema', {'reason': 'Data does not match with schema', 'numberOfUser': 1},
         {'reason': 'Data does not match with schema', 'numberOfUser': 1}),
        ('multiple_error_in_same_file',
         {'reason': ['INVALID_MOBILE_NUMBER', 'EMPTY_MOBILE_NUMBER', 'Duplicate mobile number'], 'numberOfUser': 3},
         {'reason': ['INVALID_MOBILE_NUMBER', 'EMPTY_MOBILE_NUMBER', 'Duplicate mobile number'], 'numberOfUser': 3})
    ])
    def test_irisV2_getAudienceById_NC_ErrorInUpload_withMultipleFiles(self, caseName, errorReason1, errorReason2):
        payload, filePath_1, filePath_2 = CreateAudience.createPayloadWithMultipleFilesForSpecificCase(caseName)
        listDetail = CreateAudience.uploadList('LIVE', 'ORG', payload=payload, updateNode=True, lockNode=True,
                                               campaignCheck=False)
        CreateAudience.waitForGVDToBeUpdated(listDetail['ID'])
        response = GetAudienceById.getById(listDetail['ID'])
        GetAudienceById.assertResponse(response, 200)
        GetListDBAssertion(listDetail['ID'], response,
                           errorReasons={filePath_1.split('/')[-1]: errorReason1,
                                         filePath_2.split('/')[-1]: errorReason2},
                           reachabilityCheck=False).check()

    @pytest.mark.parametrize('caseName,errorReasons1,errorReasons2', [
        ('empty_mobile_bulk', {'reason': ['EMPTY_MOBILE_NUMBER', 'Duplicate mobile number'], 'numberOfUser': 2000},
         {'reason': ['EMPTY_MOBILE_NUMBER', 'Duplicate mobile number'], 'numberOfUser': 2000}),
        ('multiple_error_in_same_file_bulk',
         {'reason': ['INVALID_MOBILE_NUMBER', 'EMPTY_MOBILE_NUMBER', 'Duplicate mobile number'], 'numberOfUser': 60000},
         {'reason': ['INVALID_MOBILE_NUMBER', 'EMPTY_MOBILE_NUMBER', 'Duplicate mobile number'], 'numberOfUser': 60000})
    ])
    def test_irisV2_bulk_getAudienceById_bulkCase_ErrorInUpload_multipleFiles(self, caseName, errorReasons1, errorReasons2):
        payload, filePath_1, filePath_2 = CreateAudience.createPayloadWithMultipleFilesForSpecificCase(caseName)
        listDetail = CreateAudience.uploadList('LIVE', 'ORG', payload=payload, updateNode=True, lockNode=True,
                                               campaignCheck=False)
        CreateAudience.waitForGVDToBeUpdated(listDetail['ID'])
        response = GetAudienceById.getById(listDetail['ID'])
        GetAudienceById.assertResponse(response, 200)
        GetListDBAssertion(listDetail['ID'], response,
                           errorReasons={filePath_1.split('/')[-1]: errorReasons1,
                                         filePath_2.split('/')[-1]: errorReasons2},
                           reachabilityCheck=False).check()

    @pytest.mark.parametrize('orgId,statusCode,errorCode,erroDesc', [
        (0, 400, 5006, 'invalid request : group not found'),
        (-1, 401, 999999, 'Invalid org id')
    ])
    def test_irisV2_getAudienceById_NC_WrongOrgId(self, orgId, statusCode, errorCode, erroDesc):
        previousOrgId = None
        try:
            list = CreateAudience.uploadList('LIVE', 'ORG', campaignCheck=False)
            previousOrgId = IrisHelper.updateOrgId(orgId)
            response = GetAudienceById.getById(list['ID'])
            GetAudienceById.assertResponse(response, statusCode, expectedErrorCode=errorCode,
                                           expectedErrorMessage=erroDesc)
        except Exception, exp:
            Assertion.constructAssertion(False, 'Exception :{}'.format(exp))
        finally:
            if previousOrgId is not None: IrisHelper.updateOrgId(int(previousOrgId))

    def test_irisV2_getAudienceById_NC_WrongAuth(self):
        previousUserName = None
        try:
            list = CreateAudience.uploadList('LIVE', 'ORG', campaignCheck=False)
            previousUserName = IrisHelper.updateUserName('WrongName')
            response = GetAudienceById.getById(list['ID'])
            GetAudienceById.assertResponse(response, 401, expectedErrorCode=999999,
                                           expectedErrorMessage='Unauthorized')
            Assertion.constructAssertion('entity' not in response['json'],
                                         'For Unknown List No Entry Found from GetCall')
        except Exception, exp:
            Assertion.constructAssertion(False, 'Exception :{}'.format(exp))
        finally:
            if previousUserName is not None: IrisHelper.updateUserName(previousUserName)

    def test_irisV2_getAudienceById_NC_WrongHeader(self):
        endpoint = IrisHelper.constructUrl('getbyid').replace('{group_id}', str(99999))
        response = Utils.makeRequest(url=endpoint, data='', auth=IrisHelper.constructAuthenticate(),
                                     headers={'accept': 'application/json'}, method='GET')
        response = IrisHelper.constructResponse(response)
        GetAudienceById.assertResponse(response, 401, expectedErrorCode=999999,
                                       expectedErrorMessage='X-CAP-ORG header must be present')


    @pytest.mark.parametrize('campaignType,testControlType,listType', [
        ('LIVE', 'ORG', 'ORG_USERS'),
        ('UPCOMING', 'ORG', 'ORG_USERS'),
        ('LAPSED', 'ORG', 'ORG_USERS'),
        ('LIVE', 'CUSTOM', 'ORG_USERS'),
        ('UPCOMING', 'CUSTOM', 'ORG_USERS'),
        ('LAPSED', 'CUSTOM', 'ORG_USERS'),
        ('LIVE', 'SKIP', 'ORG_USERS'),
        ('UPCOMING', 'SKIP', 'ORG_USERS'),
        ('LAPSED', 'SKIP', 'ORG_USERS'),
    ])
    def test_irisV2_getAudienceById_Email_stickyList(self, campaignType, testControlType, listType):
        list = CreateAudience.stickyList(campaignType, testControlType, campaignCheck=False,
                                         stickyInfo={'excludeUsers': [], 'includeUsers': ':1'})
        CreateAudience.waitForGVDToBeUpdated(list['ID'])
        response = GetAudienceById.getById(list['ID'])
        GetAudienceById.assertResponse(response, 200)
        GetListDBAssertion(list['ID'], response,createAudienceJob=False).check()