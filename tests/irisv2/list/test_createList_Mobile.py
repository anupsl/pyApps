import copy
import time

import pytest

from src.Constant.constant import constant
from src.modules.irisv2.helper.irisHelper import IrisHelper
from src.modules.irisv2.list.createAudience import CreateAudience
from src.modules.irisv2.list.createAudienceDBAssertion import CreateAudienceDBAssertion
from src.utilities.assertion import Assertion
from src.utilities.logger import Logger


@pytest.mark.run(order=11)
class Test_CreateAudience():
    def setup_method(self, method):
        Logger.logMethodName(method.__name__)

    @pytest.mark.parametrize('campaignType,testControlType,listType,schemaIdentifier', [
        ('LIVE', 'ORG', 'UPLOAD', ['MOBILE']),

    ])
    def test_irisV2_createAudience_upload_Mobile_BulkUserTest(self, campaignType, testControlType, listType,
                                                        schemaIdentifier):
        try:
            actualOrg = constant.config['orgId']
            constant.config['orgId']= 50146
            list = CreateAudience.uploadList(campaignType, testControlType, schemaIdentifier=schemaIdentifier,numberOfUsers=2000000,
                                         campaignCheck=False, updateNode=True, lockNode=True)
        finally:
            constant.config['orgId'] = actualOrg


    @pytest.mark.parametrize('campaignType,testControlType,listType,schemaIdentifier', [
        ('LIVE', 'ORG', 'UPLOAD', ['MOBILE']),

    ])
    def test_irisV2_createAudience_upload_Mobile_Sanity(self, campaignType, testControlType, listType, schemaIdentifier):
        list = CreateAudience.uploadList(campaignType, testControlType, schemaIdentifier=schemaIdentifier,
                                         campaignCheck=False,updateNode=True,lockNode=True)
        CreateAudience.waitForGVDToBeUpdated(list['ID'])
        CreateAudienceDBAssertion(list['ID'], list, listType, 10).check()

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
    def test_irisV2_createAudience_upload_Mobile(self, campaignType, testControlType, listType,
                                                        schemaIdentifier):
        list = CreateAudience.uploadList(campaignType, testControlType, schemaIdentifier=schemaIdentifier,
                                         campaignCheck=False, updateNode=True, lockNode=True)
        CreateAudience.waitForGVDToBeUpdated(list['ID'])
        CreateAudienceDBAssertion(list['ID'], list, listType, 10).check()


    @pytest.mark.parametrize('campaignType,testControlType,listType,schemaIdentifier', [
        ('LIVE', 'ORG', 'UPLOAD', ['MOBILE'])
    ])
    def test_irisV2_createAudience_upload_Mobile_ExistingUser(self, campaignType, testControlType, listType,
                                                              schemaIdentifier):
        list = CreateAudience.uploadList(campaignType, testControlType, schemaIdentifier=schemaIdentifier,
                                         newUser=False, updateNode=True, lockNode=True, campaignCheck=False)
        CreateAudience.waitForGVDToBeUpdated(list['ID'])
        CreateAudienceDBAssertion(list['ID'], list, listType, 10).check()

    @pytest.mark.parametrize(
        'campaignType,testControlType,listType,schemaIdentifier,schemaData,numberOfUser,numberOfCustomTags', [
            ('LIVE', 'ORG', 'UPLOAD', ['MOBILE'], ['MOBILE', 'FIRST_NAME', 'custom_tag_1'], 2, 1),
            ('LIVE', 'ORG', 'UPLOAD', ['MOBILE'], ['MOBILE', 'FIRST_NAME', 'custom_tag_1', 'custom_tag_2'], 2, 2),
            ('LIVE', 'ORG', 'UPLOAD', ['MOBILE'], ['MOBILE', 'FIRST_NAME', 'custom_tag_1', 'custom_tag_2', 'custom_tag_3'], 2, 3),
            ('LIVE', 'ORG', 'UPLOAD', ['MOBILE'], ['MOBILE', 'FIRST_NAME', 'custom_tag_1', 'custom_tag_2', 'custom_tag_3', 'custom_tag_4'], 2, 4),
            ('LIVE', 'ORG', 'UPLOAD', ['MOBILE'], ['MOBILE', 'FIRST_NAME', 'custom_tag_1', 'custom_tag_2', 'custom_tag_3', 'custom_tag_4', 'custom_tag_5'], 2, 5)
        ])
    def test_irisV2_createAudience_upload_CustomTags(self, campaignType, testControlType, listType, schemaIdentifier,
                                              schemaData, numberOfUser, numberOfCustomTags):
        list = CreateAudience.uploadList(campaignType, testControlType, schemaIdentifier=schemaIdentifier,
                                         schemaData=schemaData, numberOfUsers=numberOfUser,
                                         numberOfCustomTags=numberOfCustomTags, updateNode=True, lockNode=True,
                                         campaignCheck=False)
        CreateAudience.waitForGVDToBeUpdated(list['ID'])
        CreateAudienceDBAssertion(list['ID'], list, listType, numberOfUser,
                                  numberOfCustomTag=numberOfCustomTags).check()

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
    def test_irisV2_createAudience_upload_Variation_Identifiers(self, campaignType, testControlType, listType,
                                                         schemaIdentifier, schemaData, numberOfUser,
                                                         numberOfCustomTags):
        list = CreateAudience.uploadList(campaignType, testControlType, schemaIdentifier=schemaIdentifier,
                                         schemaData=schemaData, numberOfUsers=numberOfUser,
                                         numberOfCustomTags=numberOfCustomTags, updateNode=True, lockNode=True,
                                         campaignCheck=False)
        CreateAudience.waitForGVDToBeUpdated(list['ID'])
        CreateAudienceDBAssertion(list['ID'], list, listType, numberOfUser,
                                  numberOfCustomTag=numberOfCustomTags).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,numberOfUser,numberOfFiles,schemaIdentifier', [
        ('LIVE', 'ORG', 'UPLOAD', 10, 2, ['MOBILE']),
        ('LIVE', 'ORG', 'UPLOAD', 100, 3, ['MOBILE']),
        ('LIVE', 'ORG', 'UPLOAD', 1, 4, ['MOBILE']),
        ('LIVE', 'ORG', 'UPLOAD', 50, 5, ['MOBILE'])
    ])
    def test_irisV2_createAudience_upload_ListCreatedWithMultipleFiles(self, campaignType, testControlType, listType,
                                                                numberOfUser, numberOfFiles, schemaIdentifier):
        list = CreateAudience.uploadList(campaignType, testControlType, schemaIdentifier=schemaIdentifier,
                                         numberOfUsers=numberOfUser, numberOfFiles=numberOfFiles, updateNode=True,
                                         lockNode=True, campaignCheck=False)
        CreateAudience.waitForGVDToBeUpdated(list['ID'])
        CreateAudienceDBAssertion(list['ID'], list, listType, numberOfUser * numberOfFiles).check()

    @pytest.mark.parametrize('fileFormat', [
        (''),
        ('.xls'),
        ('.csv'),
        ('.pdf')
    ])
    def test_irisV2_createAudience_upload_differentFileFormat(self, fileFormat):
        filePath = constant.csvFilePath + 'listIrisV2_DifferentFormat{}'.format(fileFormat)
        audiencegroupbody = copy.deepcopy(constant.payload['audiencegroupbody'])
        audiencegroupbody['label'] = "AutomationListWithDifferentFileFormat_{}".format(int(time.time() * 1000))[:49]
        payload = CreateAudience.createFinalPayload(audiencegroupbody, numberOfUsers=10, newUser=True, numberOfFiles=0,
                                                    popFields=[])
        payload.append(('file', (filePath.split('/')[-1], open(filePath, 'rb'), 'text/csv')))
        listDetail = CreateAudience.uploadList('LIVE', 'ORG', payload=payload, updateNode=True, lockNode=True,
                                               campaignCheck=False)
        CreateAudience.waitForGVDToBeUpdated(listDetail['ID'])
        CreateAudience.assertResponse(listDetail['RESPONSE'], 200)
        CreateAudienceDBAssertion(listDetail['ID'], listDetail, 'UPLOAD', 1).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,schemaIdentifier,schemaData', [
        ('LIVE', 'ORG', 'UPLOAD', ['EMAIL'], ['EMAIL', 'FIRST_NAME'])
    ])
    def test_irisV2_createAudience_upload_Email_Sanity(self, campaignType, testControlType, listType, schemaIdentifier,
                                                schemaData):
        list = CreateAudience.uploadList(campaignType, testControlType, schemaIdentifier=schemaIdentifier,
                                         schemaData=schemaData, campaignCheck=False)
        CreateAudience.waitForGVDToBeUpdated(list['ID'])
        CreateAudienceDBAssertion(list['ID'], list, listType, 10).check()

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
    def test_irisV2_createAudience_upload_Email(self, campaignType, testControlType, listType, schemaIdentifier, schemaData):
        list = CreateAudience.uploadList(campaignType, testControlType, schemaIdentifier=schemaIdentifier,
                                         schemaData=schemaData, campaignCheck=False)
        CreateAudience.waitForGVDToBeUpdated(list['ID'])
        CreateAudienceDBAssertion(list['ID'], list, listType, 10).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,schemaIdentifier,schemaData', [
        ('LIVE', 'ORG', 'UPLOAD', ['EMAIL'], ['EMAIL', 'FIRST_NAME'])
    ])
    def test_irisV2_createAudience_upload_Email_ExistingUser(self, campaignType, testControlType, listType,
                                                             schemaIdentifier, schemaData):
        list = CreateAudience.uploadList(campaignType, testControlType, schemaIdentifier=schemaIdentifier,
                                         schemaData=schemaData, newUser=False, updateNode=True, lockNode=True,
                                         campaignCheck=False)
        CreateAudience.waitForGVDToBeUpdated(list['ID'])
        CreateAudienceDBAssertion(list['ID'], list, listType, 10).check()


    @pytest.mark.parametrize(
        'campaignType,testControlType,listType,schemaIdentifier,schemaData,numberOfUser,numberOfCustomTags', [
            ('LIVE', 'ORG', 'UPLOAD', ['EMAIL'], ['EMAIL', 'FIRST_NAME', 'custom_tag_1'], 2, 1),
            ('LIVE', 'ORG', 'UPLOAD', ['EMAIL'], ['EMAIL', 'FIRST_NAME', 'custom_tag_1', 'custom_tag_2'], 2, 2),
            ('LIVE', 'ORG', 'UPLOAD', ['EMAIL'], ['EMAIL', 'FIRST_NAME', 'custom_tag_1', 'custom_tag_2', 'custom_tag_3'], 2, 3),
            ('LIVE', 'ORG', 'UPLOAD', ['EMAIL'], ['EMAIL', 'FIRST_NAME', 'custom_tag_1', 'custom_tag_2', 'custom_tag_3', 'custom_tag_4'], 2, 4),
            ('LIVE', 'ORG', 'UPLOAD', ['EMAIL'], ['EMAIL', 'FIRST_NAME', 'custom_tag_1', 'custom_tag_2', 'custom_tag_3', 'custom_tag_4', 'custom_tag_5'], 2, 5)
        ])
    def test_irisV2_createAudience_upload_Email_CustomTags(self, campaignType, testControlType, listType, schemaIdentifier,
                                                    schemaData, numberOfUser, numberOfCustomTags):
        list = CreateAudience.uploadList(campaignType, testControlType, schemaIdentifier=schemaIdentifier,
                                         schemaData=schemaData, numberOfUsers=numberOfUser,
                                         numberOfCustomTags=numberOfCustomTags, updateNode=True, lockNode=True,
                                         campaignCheck=False)
        CreateAudience.waitForGVDToBeUpdated(list['ID'])
        CreateAudienceDBAssertion(list['ID'], list, listType, numberOfUser,
                                  numberOfCustomTag=numberOfCustomTags).check()

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
    def test_irisV2_createAudience_upload_Email_Variation_Identifiers(self, campaignType, testControlType, listType,
                                                               schemaIdentifier, schemaData, numberOfUser,
                                                               numberOfCustomTags):
        list = CreateAudience.uploadList(campaignType, testControlType, schemaIdentifier=schemaIdentifier,
                                         schemaData=schemaData, numberOfUsers=numberOfUser,
                                         numberOfCustomTags=numberOfCustomTags, updateNode=True, lockNode=True,
                                         campaignCheck=False)
        CreateAudience.waitForGVDToBeUpdated(list['ID'])
        CreateAudienceDBAssertion(list['ID'], list, listType, numberOfUser,
                                  numberOfCustomTag=numberOfCustomTags).check()

    @pytest.mark.parametrize(
        'campaignType,testControlType,listType,numberOfUser,numberOfFiles,schemaIdentifier,schemaData', [
            ('LIVE', 'ORG', 'UPLOAD', 10, 2, ['EMAIL'], ['EMAIL', 'FIRST_NAME']),
            ('LIVE', 'ORG', 'UPLOAD', 100, 3, ['EMAIL'], ['EMAIL', 'FIRST_NAME']),
            ('LIVE', 'ORG', 'UPLOAD', 1, 4, ['EMAIL'], ['EMAIL', 'FIRST_NAME']),
            ('LIVE', 'ORG', 'UPLOAD', 50, 5, ['EMAIL'], ['EMAIL', 'FIRST_NAME'])
        ])
    def test_irisV2_createAudience_upload_Email_ListCreatedWithMultipleFiles(self, campaignType, testControlType, listType,
                                                                      numberOfUser, numberOfFiles, schemaIdentifier,
                                                                      schemaData):
        list = CreateAudience.uploadList(campaignType, testControlType, schemaIdentifier=schemaIdentifier,
                                         schemaData=schemaData, numberOfUsers=numberOfUser, numberOfFiles=numberOfFiles,
                                         updateNode=True, lockNode=True, campaignCheck=False)
        CreateAudience.waitForGVDToBeUpdated(list['ID'])
        CreateAudienceDBAssertion(list['ID'], list, listType, numberOfUser * numberOfFiles).check()

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
    def test_irisV2_createAudience_upload_UserId(self, campaignType, testControlType, listType, schemaIdentifier, schemaData):
        list = CreateAudience.uploadList(campaignType, testControlType, schemaIdentifier=schemaIdentifier,
                                         schemaData=schemaData, newUser=False, campaignCheck=False)
        CreateAudience.waitForGVDToBeUpdated(list['ID'])
        CreateAudienceDBAssertion(list['ID'], list, listType, 10).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,schemaIdentifier,schemaData', [
        ('LIVE', 'ORG', 'UPLOAD', ['USER_ID'], ['USER_ID', 'FIRST_NAME'])
    ])
    def test_irisV2_createAudience_upload_UserId(self, campaignType, testControlType, listType, schemaIdentifier,
                                                 schemaData):
        list = CreateAudience.uploadList(campaignType, testControlType, schemaIdentifier=schemaIdentifier,
                                         schemaData=schemaData, newUser=False, updateNode=True, campaignCheck=False)
        CreateAudience.waitForGVDToBeUpdated(list['ID'])
        CreateAudienceDBAssertion(list['ID'], list, listType, 10).check()

    @pytest.mark.parametrize(
        'campaignType,testControlType,listType,schemaIdentifier,schemaData,numberOfUser,numberOfCustomTags', [
            ('LIVE', 'ORG', 'UPLOAD', ['USER_ID'], ['USER_ID', 'FIRST_NAME', 'custom_tag_1'], 2, 1),
            ('LIVE', 'ORG', 'UPLOAD', ['USER_ID'], ['USER_ID', 'FIRST_NAME', 'custom_tag_1', 'custom_tag_2'], 2, 2),
            ('LIVE', 'ORG', 'UPLOAD', ['USER_ID'], ['USER_ID', 'FIRST_NAME', 'custom_tag_1', 'custom_tag_2', 'custom_tag_3'], 2, 3),
            ('LIVE', 'ORG', 'UPLOAD', ['USER_ID'], ['USER_ID', 'FIRST_NAME', 'custom_tag_1', 'custom_tag_2', 'custom_tag_3', 'custom_tag_4'], 2, 4),
            ('LIVE', 'ORG', 'UPLOAD', ['USER_ID'], ['USER_ID', 'FIRST_NAME', 'custom_tag_1', 'custom_tag_2', 'custom_tag_3', 'custom_tag_4', 'custom_tag_5'], 2, 5)
        ])
    def test_irisV2_createAudience_upload_UserId_CustomTags(self, campaignType, testControlType, listType, schemaIdentifier,
                                                     schemaData, numberOfUser, numberOfCustomTags):
        list = CreateAudience.uploadList(campaignType, testControlType, schemaIdentifier=schemaIdentifier,
                                         schemaData=schemaData, newUser=False, numberOfUsers=numberOfUser,
                                         numberOfCustomTags=numberOfCustomTags, updateNode=True, lockNode=True,
                                         campaignCheck=False)
        CreateAudience.waitForGVDToBeUpdated(list['ID'])
        CreateAudienceDBAssertion(list['ID'], list, listType, numberOfUser,
                                  numberOfCustomTag=numberOfCustomTags).check()

    @pytest.mark.parametrize(
        'campaignType,testControlType,listType,schemaIdentifier,schemaData,numberOfUser,numberOfCustomTags', [
            ('LIVE', 'ORG', 'UPLOAD', ['USER_ID'], ['USER_ID', 'custom_tag_1', 'FIRST_NAME'], 2, 1),
            ('LIVE', 'ORG', 'UPLOAD', ['USER_ID'], ['custom_tag_1', 'FIRST_NAME', 'USER_ID'], 2, 1),
            ('LIVE', 'ORG', 'UPLOAD', ['USER_ID'],
             ['USER_ID', 'FIRST_NAME', 'custom_tag_1', 'custom_tag_2', 'custom_tag_3', 'custom_tag_4', 'custom_tag_5'],
             2, 5),
            ('LIVE', 'ORG', 'UPLOAD', ['USER_ID'],
             ['USER_ID', 'custom_tag_1', 'FIRST_NAME', 'custom_tag_2', 'custom_tag_3', 'custom_tag_4', 'custom_tag_5'],
             2, 5),
            ('LIVE', 'ORG', 'UPLOAD', ['USER_ID'],
             ['FIRST_NAME', 'custom_tag_1', 'custom_tag_2', 'custom_tag_3', 'USER_ID', 'custom_tag_4', 'custom_tag_5'],
             2, 5),
            ('LIVE', 'ORG', 'UPLOAD', ['USER_ID'],
             ['USER_ID', 'FIRST_NAME', 'custom_tag_1', 'custom_tag_2', 'custom_tag_3', 'custom_tag_4', 'custom_tag_5'],
             2, 5),
            ('LIVE', 'ORG', 'UPLOAD', ['USER_ID'],
             ['USER_ID', 'custom_tag_1', 'custom_tag_2', 'custom_tag_3', 'custom_tag_4', 'custom_tag_5', 'FIRST_NAME'],
             2, 5),
        ])
    def test_irisV2_createAudience_upload_UserId_Variation_Identifiers(self, campaignType, testControlType, listType,
                                                                schemaIdentifier, schemaData, numberOfUser,
                                                                numberOfCustomTags):
        list = CreateAudience.uploadList(campaignType, testControlType, schemaIdentifier=schemaIdentifier,
                                         schemaData=schemaData, newUser=False, numberOfUsers=numberOfUser,
                                         numberOfCustomTags=numberOfCustomTags, updateNode=True, lockNode=True,
                                         campaignCheck=False)
        CreateAudience.waitForGVDToBeUpdated(list['ID'])
        CreateAudienceDBAssertion(list['ID'], list, listType, numberOfUser,
                                  numberOfCustomTag=numberOfCustomTags).check()

    @pytest.mark.parametrize(
        'campaignType,testControlType,listType,numberOfUser,numberOfFiles,schemaIdentifier,schemaData', [
            ('LIVE', 'ORG', 'UPLOAD', 5, 2, ['USER_ID'], ['USER_ID', 'FIRST_NAME']),
            ('LIVE', 'ORG', 'UPLOAD', 4, 3, ['USER_ID'], ['USER_ID', 'FIRST_NAME']),
            ('LIVE', 'ORG', 'UPLOAD', 1, 4, ['USER_ID'], ['USER_ID', 'FIRST_NAME']),
            ('LIVE', 'ORG', 'UPLOAD', 2, 5, ['USER_ID'], ['USER_ID', 'FIRST_NAME'])
        ])
    def test_irisV2_createAudience_upload_UserId_ListCreatedWithMultipleFiles(self, campaignType, testControlType, listType,
                                                                       numberOfUser, numberOfFiles, schemaIdentifier,
                                                                       schemaData):
        list = CreateAudience.uploadList(campaignType, testControlType, schemaIdentifier=schemaIdentifier,
                                         schemaData=schemaData, newUser=False, numberOfUsers=numberOfUser,
                                         numberOfFiles=numberOfFiles, updateNode=True, lockNode=True,
                                         campaignCheck=False)
        CreateAudience.waitForGVDToBeUpdated(list['ID'])
        CreateAudienceDBAssertion(list['ID'], list, listType, numberOfUser * numberOfFiles).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,schemaIdentifier,schemaData', [
        ('LIVE', 'ORG', 'UPLOAD', ['EXTERNAL_ID'], ['EXTERNAL_ID', 'FIRST_NAME']),
    ])
    def test_irisV2_createAudience_upload_ExternalId(self, campaignType, testControlType, listType, schemaIdentifier,
                                                     schemaData):
        list = CreateAudience.uploadList(campaignType, testControlType, schemaIdentifier=schemaIdentifier,
                                         newUser=False, schemaData=schemaData, campaignCheck=False)
        CreateAudience.waitForGVDToBeUpdated(list['ID'])
        CreateAudienceDBAssertion(list['ID'], list, listType, 10).check()

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
    def test_irisV2_createAudience_upload_ExternalId(self, campaignType, testControlType, listType, schemaIdentifier,
                                              schemaData):
        list = CreateAudience.uploadList(campaignType, testControlType, schemaIdentifier=schemaIdentifier,
                                         newUser=False, schemaData=schemaData, campaignCheck=False)
        CreateAudience.waitForGVDToBeUpdated(list['ID'])
        CreateAudienceDBAssertion(list['ID'], list, listType, 10).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,schemaIdentifier,schemaData', [
        ('LIVE', 'ORG', 'UPLOAD', ['EXTERNAL_ID'], ['EXTERNAL_ID', 'FIRST_NAME'])
    ])
    def test_irisV2_createAudience_upload_ExternalId_ExistingUser(self, campaignType, testControlType, listType,
                                                                  schemaIdentifier, schemaData):
        list = CreateAudience.uploadList(campaignType, testControlType, schemaIdentifier=schemaIdentifier,
                                         schemaData=schemaData, newUser=False, updateNode=True, lockNode=True,
                                         campaignCheck=False)
        CreateAudience.waitForGVDToBeUpdated(list['ID'])
        CreateAudienceDBAssertion(list['ID'], list, listType, 10).check()

    @pytest.mark.parametrize(
        'campaignType,testControlType,listType,schemaIdentifier,schemaData,numberOfUser,numberOfCustomTags', [
            ('LIVE', 'ORG', 'UPLOAD', ['EXTERNAL_ID'], ['EXTERNAL_ID', 'FIRST_NAME', 'custom_tag_1'], 2, 1),
            ('LIVE', 'ORG', 'UPLOAD', ['EXTERNAL_ID'], ['EXTERNAL_ID', 'FIRST_NAME', 'custom_tag_1', 'custom_tag_2'], 2, 2),
            ('LIVE', 'ORG', 'UPLOAD', ['EXTERNAL_ID'], ['EXTERNAL_ID', 'FIRST_NAME', 'custom_tag_1', 'custom_tag_2', 'custom_tag_3'], 2, 3),
            ('LIVE', 'ORG', 'UPLOAD', ['EXTERNAL_ID'], ['EXTERNAL_ID', 'FIRST_NAME', 'custom_tag_1', 'custom_tag_2', 'custom_tag_3', 'custom_tag_4'], 2, 4),
            ('LIVE', 'ORG', 'UPLOAD', ['EXTERNAL_ID'], ['EXTERNAL_ID', 'FIRST_NAME', 'custom_tag_1', 'custom_tag_2', 'custom_tag_3', 'custom_tag_4', 'custom_tag_5'], 2, 5)
        ])
    def test_irisV2_createAudience_upload_ExternalId_CustomTags(self, campaignType, testControlType, listType,
                                                         schemaIdentifier, schemaData, numberOfUser,
                                                         numberOfCustomTags):
        list = CreateAudience.uploadList(campaignType, testControlType, schemaIdentifier=schemaIdentifier,
                                         schemaData=schemaData, newUser=False, numberOfUsers=numberOfUser,
                                         numberOfCustomTags=numberOfCustomTags, updateNode=True, lockNode=True,
                                         campaignCheck=False)
        CreateAudience.waitForGVDToBeUpdated(list['ID'])
        CreateAudienceDBAssertion(list['ID'], list, listType, numberOfUser,
                                  numberOfCustomTag=numberOfCustomTags).check()

    @pytest.mark.parametrize(
        'campaignType,testControlType,listType,schemaIdentifier,schemaData,numberOfUser,numberOfCustomTags', [
            ('LIVE', 'ORG', 'UPLOAD', ['EXTERNAL_ID'], ['EXTERNAL_ID', 'custom_tag_1', 'FIRST_NAME'], 2, 1),
            ('LIVE', 'ORG', 'UPLOAD', ['EXTERNAL_ID'], ['custom_tag_1', 'FIRST_NAME', 'EXTERNAL_ID'], 2, 1),
            ('LIVE', 'ORG', 'UPLOAD', ['EXTERNAL_ID'],
             ['EXTERNAL_ID', 'FIRST_NAME', 'custom_tag_1', 'custom_tag_2', 'custom_tag_3', 'custom_tag_4',
              'custom_tag_5'], 2, 5),
            ('LIVE', 'ORG', 'UPLOAD', ['EXTERNAL_ID'],
             ['EXTERNAL_ID', 'custom_tag_1', 'FIRST_NAME', 'custom_tag_2', 'custom_tag_3', 'custom_tag_4',
              'custom_tag_5'], 2, 5),
            ('LIVE', 'ORG', 'UPLOAD', ['EXTERNAL_ID'],
             ['FIRST_NAME', 'custom_tag_1', 'custom_tag_2', 'custom_tag_3', 'EXTERNAL_ID', 'custom_tag_4',
              'custom_tag_5'], 2, 5),
            ('LIVE', 'ORG', 'UPLOAD', ['EXTERNAL_ID'],
             ['EXTERNAL_ID', 'FIRST_NAME', 'custom_tag_1', 'custom_tag_2', 'custom_tag_3', 'custom_tag_4',
              'custom_tag_5'], 2, 5),
            ('LIVE', 'ORG', 'UPLOAD', ['EXTERNAL_ID'],
             ['EXTERNAL_ID', 'custom_tag_1', 'custom_tag_2', 'custom_tag_3', 'custom_tag_4', 'custom_tag_5',
              'FIRST_NAME'], 2, 5),
        ])
    def test_irisV2_createAudience_upload_ExternalId_Variation_Identifiers(self, campaignType, testControlType, listType,
                                                                    schemaIdentifier, schemaData, numberOfUser,
                                                                    numberOfCustomTags):
        list = CreateAudience.uploadList(campaignType, testControlType, schemaIdentifier=schemaIdentifier,
                                         schemaData=schemaData, newUser=False, numberOfUsers=numberOfUser,
                                         numberOfCustomTags=numberOfCustomTags, updateNode=True, lockNode=True,
                                         campaignCheck=False)
        CreateAudience.waitForGVDToBeUpdated(list['ID'])
        CreateAudienceDBAssertion(list['ID'], list, listType, numberOfUser,
                                  numberOfCustomTag=numberOfCustomTags).check()

    @pytest.mark.parametrize(
        'campaignType,testControlType,listType,numberOfUser,numberOfFiles,schemaIdentifier,schemaData', [
            ('LIVE', 'ORG', 'UPLOAD', 1, 2, ['EXTERNAL_ID'], ['EXTERNAL_ID', 'FIRST_NAME']),
            ('LIVE', 'ORG', 'UPLOAD', 2, 3, ['EXTERNAL_ID'], ['EXTERNAL_ID', 'FIRST_NAME']),
            ('LIVE', 'ORG', 'UPLOAD', 1, 4, ['EXTERNAL_ID'], ['EXTERNAL_ID', 'FIRST_NAME']),
            ('LIVE', 'ORG', 'UPLOAD', 2, 5, ['EXTERNAL_ID'], ['EXTERNAL_ID', 'FIRST_NAME'])
        ])
    def test_irisV2_createAudience_upload_ExternalId_ListCreatedWithMultipleFiles(self, campaignType, testControlType,
                                                                           listType, numberOfUser, numberOfFiles,
                                                                           schemaIdentifier, schemaData):
        list = CreateAudience.uploadList(campaignType, testControlType, schemaIdentifier=schemaIdentifier,
                                         schemaData=schemaData, newUser=False, numberOfUsers=numberOfUser,
                                         numberOfFiles=numberOfFiles, updateNode=True, lockNode=True,
                                         campaignCheck=False)
        CreateAudience.waitForGVDToBeUpdated(list['ID'])
        CreateAudienceDBAssertion(list['ID'], list, listType, numberOfUser * numberOfFiles).check()

    @pytest.mark.parametrize('popFields,statusCode,errorCode,errorDescription', [
        (['type'], 400, 5003, ['invalid request : Invalid Audience group type ']),
        (['label'], 400, 5003,
         ['invalid request : Group Label cannot be null', 'invalid request : Group Label cannot be empty']),
        (['tags'], 200, '', ''),
        (['type', 'label'], 400, 5003,
         ['invalid request : Group Label cannot be null', 'invalid request : Invalid Audience group type ',
          'invalid request : Group Label cannot be empty']),
        (['type', 'label', 'tags'], 400, 5003,
         ['invalid request : Group Label cannot be null', 'invalid request : Invalid Audience group type ',
          'invalid request : Group Label cannot be empty'])
    ])
    def test_irisV2_createAudience_upload_pop_mandatory_Keys(self, popFields, statusCode, errorCode, errorDescription):
        listDetail = CreateAudience.uploadList('LIVE', 'ORG', updateNode=True, lockNode=True, campaignCheck=False,
                                               popFields=popFields)
        CreateAudience.assertResponse(listDetail['RESPONSE'], statusCode, errorCode, errorDescription)

    @pytest.mark.parametrize('popFields,statusCode,errorCode,errorDescription', [
        (['type'], 400, 5003, ['invalid request : Invalid identifier type']),
        (['identifier'], 400, 5003, ['invalid request : Invalid identifiers']),
        (['type', 'identifier'], 400, 5003,
         ['invalid request : Invalid identifiers', 'invalid request : Invalid identifier type'])
    ])
    def test_irisV2_createAudience_upload_pop_dataFields(self, popFields, statusCode, errorCode, errorDescription):
        audiencegroupbody = copy.deepcopy(constant.payload['audiencegroupbody'])
        for eachField in popFields:
            audiencegroupbody['data']['schema'].pop(eachField)
        payload = CreateAudience.createFinalPayload(audiencegroupbody, numberOfUsers=10, newUser=True, numberOfFiles=1,
                                                    popFields=[])
        listDetail = CreateAudience.uploadList('LIVE', 'ORG', payload=payload, updateNode=True, lockNode=True,
                                               campaignCheck=False)
        CreateAudience.assertResponse(listDetail['RESPONSE'], 400, errorCode, errorDescription)

    def test_irisV2_createAudience_upload_NoDataField(self):
        audiencegroupbody = copy.deepcopy(constant.payload['audiencegroupbody'])
        audiencegroupbody.pop('data')
        payload = CreateAudience.createFinalPayload(audiencegroupbody, numberOfUsers=10, newUser=True, numberOfFiles=0,
                                                    popFields=[])
        listDetail = CreateAudience.uploadList('LIVE', 'ORG', payload=payload, updateNode=True, lockNode=True,
                                               campaignCheck=False)
        CreateAudience.assertResponse(listDetail['RESPONSE'], 400, 5003, ['invalid request : Invalid Data',
                                                                          'invalid request : creating audience without uploading file'])

    def test_irisV2_createAudience_upload_payload_withoutFileAttached(self):
        audiencegroupbody = copy.deepcopy(constant.payload['audiencegroupbody'])
        payload = CreateAudience.createFinalPayload(audiencegroupbody, numberOfUsers=10, newUser=True, numberOfFiles=0,
                                                    popFields=[])
        listDetail = CreateAudience.uploadList('LIVE', 'ORG', payload=payload, updateNode=True, lockNode=True,
                                               campaignCheck=False)
        CreateAudience.assertResponse(listDetail['RESPONSE'], 400, 5003,
                                      ['invalid request : creating audience without uploading file'])

    @pytest.mark.parametrize('keyValue,statusCode,errorCode,errorDescription', [
        ({'type': None}, 400, 5003, ['invalid request : Invalid Audience group type ']),
        ({'type': ''}, 400, 104, ['Invalid request : invalid value for field type']),
        ({'type': 'UPLOA'}, 400, 104, ['Invalid request : invalid value for field type']),
        ({'type': 'UPLOA$$$'}, 400, 104, ['Invalid request : invalid value for field type']),
        ({'type': -1}, 400, 104, ['Invalid request : invalid value for field type']),
        ({'label': None}, 400, 5003,
         ['invalid request : Group Label cannot be null', 'invalid request : Group Label cannot be empty']),
        ({'label': ''}, 400, 5003, ['invalid request : Group Label cannot be empty']),
        ({'type': None, 'label': None}, 400, 5003,
         ['invalid request : Group Label cannot be null', 'invalid request : Invalid Audience group type ',
          'invalid request : Group Label cannot be empty']),
        ({'type': 'UPLOA', 'label': 99999}, 400, 104, ['Invalid request : invalid value for field type']),
        ({'tags': -1}, 400, 104, ['Invalid request : invalid data type of field tags'])

    ])
    def test_irisV2_createAudience_upload_payload_withWrongValues_nonSchemaIdentifier(self, keyValue, statusCode, errorCode,
                                                                               errorDescription):
        audiencegroupbody = copy.deepcopy(constant.payload['audiencegroupbody'])
        for each in keyValue:
            audiencegroupbody[each] = keyValue[each]
        payload = CreateAudience.createFinalPayload(audiencegroupbody, numberOfUsers=10, newUser=True, numberOfFiles=1,
                                                    popFields=[])
        listDetail = CreateAudience.uploadList('LIVE', 'ORG', payload=payload, updateNode=True, lockNode=True,
                                               campaignCheck=False)
        CreateAudience.assertResponse(listDetail['RESPONSE'], statusCode, errorCode, errorDescription)

    @pytest.mark.parametrize('keyValue,statusCode,errorCode,errorDescription', [
        ({'source': 'UPLOADD'}, 400, 104, ['Invalid request : invalid value for field source']),
        ({'source': ''}, 400, 104, ['Invalid request : invalid value for field source']),
        ({'source': None}, 400, 5003, ['invalid request : Invalid Source']),
        ({'source': '#$@$'}, 400, 104, ['Invalid request : invalid value for field source']),
        ({'schema': {'type': '_KEY_IDENTIFIER', 'identifier': ['MOBILE'], 'data': ["MOBILE", "FIRST_NAME"]}}, 400, 104,
         ['Invalid request : invalid value for field type']),
        ({'schema': {'type': None, 'identifier': ['MOBILE'], 'data': ["MOBILE", "FIRST_NAME"]}}, 400, 5003,
         ['invalid request : Invalid identifier type']),
        ({'schema': {'type': -1, 'identifier': ['MOBILE'], 'data': ["MOBILE", "FIRST_NAME"]}}, 400, 104,
         ['Invalid request : invalid value for field type']),
        ({'schema': {'type': 'SINGLE_KEY_IDENTIFIER', 'identifier': ['MOBILE', 'EMA'],
                     'data': ["MOBILE", "FIRST_NAME"]}}, 400, 5003,
         ['invalid request : Invalid identifier in schema ']),
        ({'schema': {'type': 'SINGLE_KEY_IDENTIFIER', 'identifier': ['MOBILE', 'FIRST_NAME'], 'data': ["MOBILE"]}}, 400,
         5003, ['invalid request : Invalid identifier in schema ']),
        ({'schema': {'type': 'SINGLE_KEY_IDENTIFIER', 'identifier': ['MOBI'], 'data': ["MOBILE", "FIRST_NAME"]}}, 400,
         5003, ['invalid request : Invalid identifier in schema ']),
        ({'schema': {'type': 'SINGLE_KEY_IDENTIFIER', 'identifier': ['MOBILE'], 'data': ["EMAIL", "FIRST_NAME"]}}, 400,
         5003, ['invalid request : Identifier is missing in schema data: MOBILE']),
        ({'schema': {'type': 'SINGLE_KEY_IDENTIFIER', 'identifier': ['MOBILE'], 'data': ["MOBI", "FIRST_NAME"]}}, 400,
         5003, ['invalid request : Identifier is missing in schema data: MOBILE',
                'invalid request : unsupported custom tag or identifier: MOBI']),
       (
                {'schema': {'type': 'SINGLE_KEY_IDENTIFIER', 'identifier': ['MOBILE'], 'data': ["MOBILE", "FNAME"]}},
                400, 5003,
                ['invalid request : unsupported custom tag or identifier: FNAME']),
        ({'schema': {'type': '_KEY_IDENTIFIER', 'identifier': ['EMAIL'], 'data': ["EMAIL", "FIRST_NAME"]}}, 400, 104,
         ['Invalid request : invalid value for field type']),
        ({'schema': {'type': None, 'identifier': ['EMAIL'], 'data': ["EMAIL", "FIRST_NAME"]}}, 400, 5003,
         ['invalid request : Invalid identifier type']),
        ({'schema': {'type': -1, 'identifier': ['EMAIL'], 'data': ["EMAIL", "FIRST_NAME"]}}, 400, 104,
         ['Invalid request : invalid value for field type']),
        ({'schema': {'type': 'SINGLE_KEY_IDENTIFIER', 'identifier': ['EMAIL', 'MOB'], 'data': ["EMAIL", "FIRST_NAME"]}},
         400, 5003, ['invalid request : single key identifier type group expect only one identifier',
                     'invalid request : Invalid identifier in schema ']),
        ({'schema': {'type': 'SINGLE_KEY_IDENTIFIER', 'identifier': ['EMAIL', 'FIRST_NAME'], 'data': ["EMAIL"]}}, 400,
         5003, ['invalid request : single key identifier type group expect only one identifier',
                'invalid request : Invalid identifier in schema ']),
        ({'schema': {'type': 'SINGLE_KEY_IDENTIFIER', 'identifier': ['EMAI'], 'data': ["EMAIL", "FIRST_NAME"]}}, 400,
         5003, ['invalid request : Invalid identifier in schema ']),
        ({'schema': {'type': 'SINGLE_KEY_IDENTIFIER', 'identifier': ['EMAIL'], 'data': ["MOBILE", "FIRST_NAME"]}}, 400,
         5003, ['invalid request : Identifier is missing in schema data: EMAIL']),
        ({'schema': {'type': 'SINGLE_KEY_IDENTIFIER', 'identifier': ['EMAIL'], 'data': ["EMAI", "FIRST_NAME"]}}, 400,
         5003, ['invalid request : Identifier is missing in schema data: EMAIL',
                'invalid request : unsupported custom tag or identifier: EMAI']),
        ({'schema': {'type': 'SINGLE_KEY_IDENTIFIER', 'identifier': ['EMAIL'], 'data': ["EMAIL", "FNAME"]}}, 400, 5003,
         ['invalid request : unsupported custom tag or identifier: FNAME']),
        ({'schema': {'type': '_KEY_IDENTIFIER', 'identifier': ['USER_ID'], 'data': ["USER_ID", "FIRST_NAME"]}}, 400,
         104, ['Invalid request : invalid value for field type']),
        ({'schema': {'type': None, 'identifier': ['USER_ID'], 'data': ["USER_ID", "FIRST_NAME"]}}, 400, 5003,
         ['invalid request : Invalid identifier type']),
        ({'schema': {'type': -1, 'identifier': ['USER_ID'], 'data': ["USER_ID", "FIRST_NAME"]}}, 400, 104,
         ['Invalid request : invalid value for field type']),
        ({'schema': {'type': 'SINGLE_KEY_IDENTIFIER', 'identifier': ['USER_ID', 'MOB'],
                     'data': ["USER_ID", "FIRST_NAME"]}}, 400, 5003,
         ['invalid request : single key identifier type group expect only one identifier',
          'invalid request : Invalid identifier in schema ']),
        ({'schema': {'type': 'SINGLE_KEY_IDENTIFIER', 'identifier': ['USER_ID', 'FIRST_NAME'], 'data': ["USER_ID"]}},
         400, 5003, ['invalid request : single key identifier type group expect only one identifier',
                     'invalid request : Invalid identifier in schema ']),
       (
                {'schema': {'type': 'SINGLE_KEY_IDENTIFIER', 'identifier': ['USER_I'],
                            'data': ["USER_ID", "FIRST_NAME"]}}, 400,
                5003, ['invalid request : Invalid identifier in schema ']),
       (
                {'schema': {'type': 'SINGLE_KEY_IDENTIFIER', 'identifier': ['USER_ID'],
                            'data': ["MOBILE", "FIRST_NAME"]}}, 400,
                5003, ['invalid request : Identifier is missing in schema data: USER_ID']),
       (
                {'schema': {'type': 'SINGLE_KEY_IDENTIFIER', 'identifier': ['USER_ID'],
                            'data': ["USER_I", "FIRST_NAME"]}}, 400,
                5003, ['invalid request : Identifier is missing in schema data: USER_ID',
                       'invalid request : unsupported custom tag or identifier: USER_I']),
        ({'schema': {'type': 'SINGLE_KEY_IDENTIFIER', 'identifier': ['USER_ID'], 'data': ["USER_ID", "FNAME"]}}, 400,
         5003, ['invalid request : unsupported custom tag or identifier: FNAME']),
        ({'schema': {'type': 'SINGLE_KEY_IDENTIFIER', 'identifier': ['EXTERNAL_ID', 'FIRST_NAME'],
                     'data': ["EXTERNAL_ID"]}}, 400, 5003,
         ['invalid request : single key identifier type group expect only one identifier',
          'invalid request : Invalid identifier in schema ']),
        ({'schema': {'type': 'SINGLE_KEY_IDENTIFIER', 'identifier': ['EXTERNAL_I'],
                     'data': ["EXTERNAL_ID", "FIRST_NAME"]}}, 400, 5003,
         ['invalid request : Invalid identifier in schema ']),
        ({'schema': {'type': 'SINGLE_KEY_IDENTIFIER', 'identifier': ['EXTERNAL_ID'], 'data': ["MOBILE", "FIRST_NAME"]}},
         400, 5003, ['invalid request : Identifier is missing in schema data: EXTERNAL_ID']),
        ({'schema': {'type': 'SINGLE_KEY_IDENTIFIER', 'identifier': ['EXTERNAL_ID'],
                     'data': ["EXTERNAL_I", "FIRST_NAME"]}}, 400, 5003,
         ['invalid request : Identifier is missing in schema data: EXTERNAL_ID',
          'invalid request : unsupported custom tag or identifier: EXTERNAL_I']),
        ({'schema': {'type': 'SINGLE_KEY_IDENTIFIER', 'identifier': ['EXTERNAL_ID'], 'data': ["EXTERNAL_ID", "FNAME"]}},
         400, 5003, ['invalid request : unsupported custom tag or identifier: FNAME'])
    ])
    def test_irisV2_createAudience_upload_payload_withWrongValues_schemaIdentifier(self, keyValue, statusCode, errorCode,
                                                                            errorDescription):
        audiencegroupbody = copy.deepcopy(constant.payload['audiencegroupbody'])
        audiencegroupbody['label'] = "AutomationList_{}".format(int(time.time() * 1000))
        for each in keyValue:
            audiencegroupbody['data'][each] = keyValue[each]
        payload = CreateAudience.createFinalPayload(audiencegroupbody, numberOfUsers=10, newUser=True, numberOfFiles=1,
                                                    popFields=[], lockDataAppend=True)
        listDetail = CreateAudience.uploadList('LIVE', 'ORG', payload=payload, updateNode=True, lockNode=True,
                                               campaignCheck=False)
        CreateAudience.assertResponse(listDetail['RESPONSE'], statusCode, errorCode, errorDescription)

    @pytest.mark.parametrize('numberOfCharacters,statusCode,errorCode,errorDescription', [
        (1, 400, 5003, ['invalid request : Minimum length supported for audience label: 5',  'invalid request : Audience label already exits']),
        (161, 400, 5003, ['invalid request : Invalid audience name. Name exceeds 160 characters. '])
    ])
    def test_irisV2_createAudience_upload_boundaryValueForFields(self, numberOfCharacters, statusCode, errorCode,
                                                          errorDescription):
        listDetail = CreateAudience.uploadList('LIVE', 'ORG',
                                               label=('l' * 200 + str(int(time.time() * 1000)))[:numberOfCharacters],
                                               updateNode=True, lockNode=True, campaignCheck=False)
        CreateAudience.assertResponse(listDetail['RESPONSE'], statusCode, errorCode, errorDescription)

    def test_irisV2_createAudience_upload_ExistingListName(self):
        label = 'Automation_ExistingList_check_{}'.format(int(time.time() * 1000))
        CreateAudience.uploadList('LIVE', 'ORG', label=label, newUser=False, updateNode=True, lockNode=True,
                                  campaignCheck=False)
        listDetail = CreateAudience.uploadList('LIVE', 'ORG', label=label, newUser=False, updateNode=True,
                                               lockNode=True, campaignCheck=False)
        CreateAudience.assertResponse(listDetail['RESPONSE'], 400, 5003,
                                      ['invalid request : Audience label already exits'])

    def test_irisV2_createAudience_upload_MaxNumberOfFilesSupported(self):
        listDetail = CreateAudience.uploadList('LIVE', 'ORG', numberOfUsers=2, numberOfFiles=6, updateNode=True,
                                               lockNode=True, campaignCheck=False)
        CreateAudience.assertResponse(listDetail['RESPONSE'], 400, 5003,
                                      ['invalid request : maximum number of files supported in upload audience is :5'])

    @pytest.mark.parametrize(
        'campaignType,testControlType,listType,schemaIdentifier,schemaData,numberOfUser,numberOfCustomTags', [
            ('LIVE', 'ORG', 'UPLOAD', ['MOBILE'],
             ['MOBILE', 'FIRST_NAME', 'custom_tag_1', 'custom_tag_2', 'custom_tag_3', 'custom_tag_4', 'custom_tag_5',
              'custom_tag_6'], 2, 6),
        ])
    def test_irisV2_createAudience_upload_Negative_CustomTags(self, campaignType, testControlType, listType, schemaIdentifier,
                                                       schemaData, numberOfUser, numberOfCustomTags):
        listDetail = CreateAudience.uploadList(campaignType, testControlType, schemaIdentifier=schemaIdentifier,
                                               schemaData=schemaData, numberOfUsers=numberOfUser,
                                               numberOfCustomTags=numberOfCustomTags, updateNode=True, lockNode=True,
                                               campaignCheck=False)
        CreateAudience.assertResponse(listDetail['RESPONSE'], 400, 5003,
                                      ['invalid request : unsupported custom tag or identifier: custom_tag_6'])

    @pytest.mark.parametrize(
        'campaignType,testControlType,listType,schemaIdentifier,schemaData,numberOfUser,numberOfCustomTags', [
            ('LIVE', 'ORG', 'UPLOAD', ['EMAIL'],
             ['EMAIL', 'FIRST_NAME', 'custom_tag_1', 'custom_tag_2', 'custom_tag_3', 'custom_tag_4', 'custom_tag_5',
              'custom_tag_6'], 2, 6),
        ])
    def test_irisV2_createAudience_upload_Email_Negative_CustomTags(self, campaignType, testControlType, listType,
                                                             schemaIdentifier, schemaData, numberOfUser,
                                                             numberOfCustomTags):
        listDetail = CreateAudience.uploadList(campaignType, testControlType, schemaIdentifier=schemaIdentifier,
                                               schemaData=schemaData, numberOfUsers=numberOfUser,
                                               numberOfCustomTags=numberOfCustomTags, updateNode=True, lockNode=True,
                                               campaignCheck=False)
        CreateAudience.assertResponse(listDetail['RESPONSE'], 400, 5003,
                                      ['invalid request : unsupported custom tag or identifier: custom_tag_6'])

    def test_irisV2_createAudience_upload_wrong_orgid(self):
        previousOrgId = None
        try:
            previousOrgId = IrisHelper.updateOrgId(-1)
            listDetail = CreateAudience.uploadList('LIVE', 'ORG', campaignCheck=False)
            CreateAudience.assertResponse(listDetail['RESPONSE'], 401, 999999, ['Invalid org id'])
        except Exception, exp:
            Assertion.constructAssertion(False, 'Exception :{}'.format(exp))
        finally:
            if previousOrgId is not None: IrisHelper.updateOrgId(int(previousOrgId))

    def test_irisV2_createAudience_upload_wrongAuth(self):
        previousUserName = None
        try:
            previousUserName = IrisHelper.updateUserName('WrongName')
            listDetail = CreateAudience.uploadList('LIVE', 'ORG', campaignCheck=False)
            CreateAudience.assertResponse(listDetail['RESPONSE'], 401, 999999, ['Unauthorized'])
        except Exception, exp:
            Assertion.constructAssertion(False, 'Exception :{}'.format(exp))
        finally:
            if previousUserName is not None: IrisHelper.updateUserName(previousUserName)

    @pytest.mark.parametrize(
        'campaignType,testControlType,listType,schemaIdentifier,schemaData,numberOfUser,numberOfCustomTags', [
            ('LIVE', 'ORG', 'UPLOAD', ['MOBILE'], ['MOBILE', 'CUSTOM_TAG_1', 'FIRST_NAME'], 2, 1),
        ])
    def test_irisV2_createAudience_upload_CustomTag_InUpperCase_Validation(self, campaignType, testControlType, listType,
                                                         schemaIdentifier, schemaData, numberOfUser,
                                                         numberOfCustomTags):
        list = CreateAudience.uploadList(campaignType, testControlType, schemaIdentifier=schemaIdentifier,
                                         schemaData=schemaData, numberOfUsers=numberOfUser,
                                         numberOfCustomTags=numberOfCustomTags, updateNode=True, lockNode=True,
                                         campaignCheck=False)
        CreateAudience.assertResponse(list['RESPONSE'], 400, 5003, ['invalid request : unsupported custom tag or identifier: CUSTOM_TAG_1'])

    @pytest.mark.parametrize('campaignType,testControlType,listType,schemaIdentifier', [
        ('LIVE', 'ORG', 'UPLOAD', ['MOBILE'])
    ])
    def test_irisV2_createAudience_upload_EmptyFile(self, campaignType, testControlType, listType,
                                                              schemaIdentifier):
        list = CreateAudience.uploadList(campaignType, testControlType, schemaIdentifier=schemaIdentifier,
                                         newUser=False, updateNode=True, lockNode=True, campaignCheck=False, numberOfUsers=0)
        CreateAudience.assertResponse(list['RESPONSE'], 400, 5003,
                                      ['invalid request : Uploaded audience file is empty'])