import pytest, pytest_ordering, time
from src.Constant.constant import constant
from src.utilities.logger import Logger
from src.utilities.assertion import Assertion
from src.modules.irisv2.list.checkAvailabilityName import CheckAvailabiltyName
from src.modules.irisv2.list.createAudience import CreateAudience

@pytest.mark.run(order=8)
class Test_checkAvailability():
    
    def setup_method(self, method):
        Logger.logMethodName(method.__name__)
    
    @pytest.mark.parametrize('campaignType,testControlType,listType,schemaIdentifier', [
        ('LIVE', 'ORG', 'UPLOAD', ['MOBILE']),
        ])
    def test_irisV2_checkAvailability_differentTypesOfList_Mobile_Sanity(self, campaignType, testControlType, listType, schemaIdentifier):
        list = CreateAudience.uploadList(campaignType, testControlType, schemaIdentifier=schemaIdentifier)
        response = CheckAvailabiltyName.checkExists(list['NAME'])
        CheckAvailabiltyName.assertCheckExists(response, 200)
        
    @pytest.mark.parametrize('campaignType,testControlType,listType,schemaIdentifier', [
        ('UPCOMING', 'ORG', 'UPLOAD', ['MOBILE']),
        ('LAPSED', 'ORG', 'UPLOAD', ['MOBILE']),
        ])
    def test_irisV2_checkAvailability_differentTypesOfList_Mobile(self, campaignType, testControlType, listType, schemaIdentifier):
        list = CreateAudience.uploadList(campaignType, testControlType, schemaIdentifier=schemaIdentifier)
        response = CheckAvailabiltyName.checkExists(list['NAME'])
        CheckAvailabiltyName.assertCheckExists(response, 200)
        
    @pytest.mark.parametrize('description,campaignType,testControlType,listType,schemaIdentifier,listName', [
        ('Label With Space', 'LIVE', 'ORG', 'UPLOAD', ['MOBILE'], 'List Automation'),
        ])
    def test_irisV2_checkAvailability_LabelWithSpace(self, description, campaignType, testControlType, listType, schemaIdentifier, listName):
        list = CreateAudience.uploadList(campaignType, testControlType, label=listName + str(int(time.time())), schemaIdentifier=schemaIdentifier, updateNode=True, campaignCheck=False)
        response = CheckAvailabiltyName.checkExists(list['NAME'])
        CheckAvailabiltyName.assertCheckExists(response, 200)
        
    @pytest.mark.parametrize('description,campaignType,testControlType,listType,schemaIdentifier,listName', [
        ('Only Prefix Of List', 'LIVE', 'ORG', 'UPLOAD', ['MOBILE'], 'List Automation'),
        ])
    def test_irisV2_checkAvailability_OnlyPrefixOfList(self, description, campaignType, testControlType, listType, schemaIdentifier, listName):
        list = CreateAudience.uploadList(campaignType, testControlType, label=listName + str(int(time.time())), schemaIdentifier=schemaIdentifier, updateNode=True, campaignCheck=False)
        response = CheckAvailabiltyName.checkExists(list['NAME'][:len(list['NAME']) - 1])
        CheckAvailabiltyName.assertCheckExists(response, 200, isExists=False)
       
    @pytest.mark.parametrize('description,campaignType,testControlType,listType,schemaIdentifier,listName', [
        ('Only Suffix Of List', 'LIVE', 'ORG', 'UPLOAD', ['MOBILE'], 'List Automation'),
        ])
    def test_irisV2_checkAvailability_OnlySuffixOfList(self, description, campaignType, testControlType, listType, schemaIdentifier, listName):
        list = CreateAudience.uploadList(campaignType, testControlType, label=listName + str(int(time.time())), schemaIdentifier=schemaIdentifier, updateNode=True, campaignCheck=False)
        response = CheckAvailabiltyName.checkExists(list['NAME'][1:])
        CheckAvailabiltyName.assertCheckExists(response, 200, isExists=False) 
        
    def test_irisV2_checkAvailability_EmptyStringAsListName(self):
        response = CheckAvailabiltyName.checkExists('')
        CheckAvailabiltyName.assertCheckExists(response, 400, expectedErrorCode=[103], expectedErrorMessage=['Invalid value for path param: groupId'])
           
    @pytest.mark.parametrize('description,listName', [
        ('List With Special Character', 'ListName$$$####'),
        ('List Doesnt Exist', 'ListNameDoesntExist')
        ])
    def test_irisV2_checkAvailability_Negative_VariationOfWrongName(self, description, listName):
        response = CheckAvailabiltyName.checkExists(listName)
        CheckAvailabiltyName.assertCheckExists(response, 200, isExists=False)
        
