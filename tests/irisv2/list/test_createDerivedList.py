import pytest
import copy
import time
from src.modules.irisv2.list.createAudience import CreateAudience
from src.modules.irisv2.list.createAudienceDBAssertion import CreateAudienceDBAssertion
from src.dbCalls.campaignShard import list_Calls
from src.utilities.logger import Logger
from src.Constant.constant import constant


@pytest.mark.run(order=9)
class Test_CreateAudience_Derived():

    def setup_class(self):
        self.listInfo = list_Calls().getAllGroupIds(2, 0, 'created_date', None)
        self.listId_1 = self.listInfo[0]
        self.listId_2 = self.listInfo[1]

    def setup_method(self, method):
        Logger.logMethodName(method.__name__)

    @pytest.mark.parametrize('description,campaignType,testControlType,listType, derivedListInfo,popfield', [
        ('Simple include', 'LIVE', 'ORG', 'DERIVED', {'includedGroups': ['UPLOAD', 'UPLOAD'], 'noOfUserUpload': 5},['excludedGroups']),

    ])
    def test_irisV2_createAudience_Derived_Include_SMS(self,description, campaignType, testControlType, listType, derivedListInfo,popfield):
        list = CreateAudience.derivedList(campaignType, testControlType, campaignCheck=False,derivedListInfo=derivedListInfo,popFields=popfield)
        CreateAudience.waitForGVDToBeUpdated(list['ID'])
        CreateAudienceDBAssertion(list['ID'], list, listType, list['expectedUserCount'] , reachabilityCheck=True).check()

    @pytest.mark.parametrize('description,campaignType,testControlType,listType, derivedListInfo,popfield', [

        ('Simple include', 'UPCOMING', 'ORG', 'DERIVED', {'includedGroups': ['UPLOAD', 'UPLOAD'], 'noOfUserUpload': 5},
         ['excludedGroups']),
        ('Simple include', 'LAPSED', 'ORG', 'DERIVED', {'includedGroups': ['UPLOAD', 'UPLOAD'], 'noOfUserUpload': 5},
         ['excludedGroups']),
        ('Simple include', 'LIVE', 'CUSTOM', 'DERIVED', {'includedGroups': ['UPLOAD', 'UPLOAD'], 'noOfUserUpload': 5},
         ['excludedGroups']),
        ('Simple include', 'UPCOMING', 'CUSTOM', 'DERIVED',
         {'includedGroups': ['UPLOAD', 'UPLOAD'], 'noOfUserUpload': 5}, ['excludedGroups']),
        ('Simple include', 'LAPSED', 'CUSTOM', 'DERIVED', {'includedGroups': ['UPLOAD', 'UPLOAD'], 'noOfUserUpload': 5},
         ['excludedGroups']),
        ('Simple include', 'LIVE', 'SKIP', 'DERIVED', {'includedGroups': ['UPLOAD', 'UPLOAD'], 'noOfUserUpload': 5},
         ['excludedGroups']),
        ('Simple include', 'UPCOMING', 'SKIP', 'DERIVED', {'includedGroups': ['UPLOAD', 'UPLOAD'], 'noOfUserUpload': 5},
         ['excludedGroups']),
        ('Simple include', 'LAPSED', 'SKIP', 'DERIVED', {'includedGroups': ['UPLOAD', 'UPLOAD'], 'noOfUserUpload': 5},
         ['excludedGroups']),
    ])
    def test_irisV2_createAudience_Derived_Include_SMS(self, description, campaignType, testControlType,
                                                              listType, derivedListInfo, popfield):
        list = CreateAudience.derivedList(campaignType, testControlType, campaignCheck=False,
                                          derivedListInfo=derivedListInfo, popFields=popfield)
        CreateAudience.waitForGVDToBeUpdated(list['ID'])
        CreateAudienceDBAssertion(list['ID'], list, listType, list['expectedUserCount'], reachabilityCheck=True).check()

    @pytest.mark.parametrize('description,campaignType,testControlType,listType, derivedListInfo,schemaIdentifier,popfield', [
        ('Simple include', 'LIVE', 'ORG', 'DERIVED', {'includedGroups': ['UPLOAD', 'UPLOAD','LOYALTY','DERIVED'], 'noOfUserUpload': 5,'derived':['UPLOAD', 'LOYALTY'] },'EMAIL',['excludedGroups']),

    ])
    def test_irisV2_createAudience_Derived_Include_DifferentChannels_Sanity(self, description, campaignType, testControlType,listType, derivedListInfo,schemaIdentifier, popfield):
        list = CreateAudience.derivedList(campaignType, testControlType,schemaIdentifier=[schemaIdentifier], newUser=False,campaignCheck=False,derivedListInfo=derivedListInfo, popFields=popfield)
        CreateAudience.waitForGVDToBeUpdated(list['ID'])
        CreateAudienceDBAssertion(list['ID'], list, listType, list['expectedUserCount'], reachabilityCheck=True).check()

    @pytest.mark.parametrize(
        'description,campaignType,testControlType,listType, derivedListInfo,schemaIdentifier,popfield', [

            ('Simple include', 'LIVE', 'ORG', 'DERIVED',
             {'includedGroups': ['UPLOADOLD', 'UPLOADOLD', 'DERIVED'], 'noOfUserUpload': 5,
              'derived': ['UPLOADOLD', 'UPLOADOLD']}, 'USER_ID', ['excludedGroups']),
            ('Simple include', 'LIVE', 'ORG', 'DERIVED',
             {'includedGroups': ['UPLOADOLD', 'UPLOADOLD', 'DERIVED'], 'noOfUserUpload': 5,
              'derived': ['UPLOADOLD', 'UPLOADOLD']}, 'EXTERNAL_ID', ['excludedGroups'])
        ])
    def test_irisV2_createAudience_Derived_Include_DifferentChannels(self, description, campaignType,
                                                                            testControlType, listType, derivedListInfo,
                                                                            schemaIdentifier, popfield):
        list = CreateAudience.derivedList(campaignType, testControlType, schemaIdentifier=[schemaIdentifier],
                                          newUser=False, campaignCheck=False, derivedListInfo=derivedListInfo,
                                          popFields=popfield)
        CreateAudience.waitForGVDToBeUpdated(list['ID'])
        CreateAudienceDBAssertion(list['ID'], list, listType, list['expectedUserCount'], reachabilityCheck=True).check()

    @pytest.mark.parametrize('description,campaignType,testControlType,listType, derivedListInfo,popfield', [
        ('Simple include and exclude', 'LIVE', 'ORG', 'DERIVED',{'includedGroups': ['UPLOAD', 'LOYALTY'], 'excludedGroup': ['LOYALTY'], 'noOfUserUpload': 5}, []),

    ])
    def test_irisV2_createAudience_Derived_Include_Exclude_SMS(self, description, campaignType, testControlType, listType,derivedListInfo, popfield):
        list = CreateAudience.derivedList(campaignType, testControlType, campaignCheck=False,derivedListInfo=derivedListInfo, popFields=popfield)
        CreateAudience.waitForGVDToBeUpdated(list['ID'])
        CreateAudienceDBAssertion(list['ID'], list, listType, list['expectedUserCount'] , reachabilityCheck=True).check()

    @pytest.mark.parametrize('description,campaignType,testControlType,listType, derivedListInfo,popfield', [

        ('Simple include and exclude', 'UPCOMING', 'ORG', 'DERIVED',
         {'includedGroups': ['UPLOAD', 'LOYALTY'], 'excludedGroup': ['LOYALTY'], 'noOfUserUpload': 5}, []),
        ('Simple include and exclude', 'LAPSED', 'ORG', 'DERIVED',
         {'includedGroups': ['UPLOAD', 'LOYALTY'], 'excludedGroup': ['LOYALTY'], 'noOfUserUpload': 5}, []),
        ('Simple include and exclude', 'LIVE', 'CUSTOM', 'DERIVED',
         {'includedGroups': ['UPLOAD', 'LOYALTY'], 'excludedGroup': ['LOYALTY'], 'noOfUserUpload': 5}, []),
        ('Simple include and exclude', 'UPCOMING', 'CUSTOM', 'DERIVED',
         {'includedGroups': ['UPLOAD', 'LOYALTY'], 'excludedGroup': ['LOYALTY'], 'noOfUserUpload': 5}, []),
        ('Simple include and exclude', 'LAPSED', 'CUSTOM', 'DERIVED',
         {'includedGroups': ['UPLOAD', 'LOYALTY'], 'excludedGroup': ['LOYALTY'], 'noOfUserUpload': 5}, []),
        ('Simple include and exclude', 'LIVE', 'SKIP', 'DERIVED',
         {'includedGroups': ['UPLOAD', 'LOYALTY'], 'excludedGroup': ['LOYALTY'], 'noOfUserUpload': 5}, []),
        ('Simple include and exclude', 'UPCOMING', 'SKIP', 'DERIVED',
         {'includedGroups': ['UPLOAD', 'LOYALTY'], 'excludedGroup': ['LOYALTY'], 'noOfUserUpload': 5}, []),
        ('Simple include and exclude', 'LAPSED', 'SKIP', 'DERIVED',
         {'includedGroups': ['UPLOAD', 'LOYALTY'], 'excludedGroup': ['LOYALTY'], 'noOfUserUpload': 5}, [])
    ])
    def test_irisV2_createAudience_Derived_Include_Exclude_SMS(self, description, campaignType, testControlType,
                                                                      listType, derivedListInfo, popfield):
        list = CreateAudience.derivedList(campaignType, testControlType, campaignCheck=False,
                                          derivedListInfo=derivedListInfo, popFields=popfield)
        CreateAudience.waitForGVDToBeUpdated(list['ID'])
        CreateAudienceDBAssertion(list['ID'], list, listType, list['expectedUserCount'], reachabilityCheck=True).check()

    @pytest.mark.parametrize('description,campaignType,testControlType,listType, derivedListInfo,schemaIdentifier,popfield', [
        ('Simple include', 'LIVE', 'ORG', 'DERIVED',{'includedGroups': ['UPLOAD', 'UPLOAD', 'LOYALTY', 'DERIVED'], 'excludedGroup': ['UPLOADOLD'], 'noOfUserUpload': 5,'derived': ['UPLOAD', 'LOYALTY']}, 'EMAIL', []),

        ])
    def test_irisV2_createAudience_Derived_Include_Exclude_DifferentChannels_Sanity(self, description, campaignType,testControlType, listType, derivedListInfo,schemaIdentifier, popfield):
        list = CreateAudience.derivedList(campaignType, testControlType, schemaIdentifier=[schemaIdentifier],newUser=False, campaignCheck=False, derivedListInfo=derivedListInfo,popFields=popfield)
        CreateAudience.waitForGVDToBeUpdated(list['ID'])
        CreateAudienceDBAssertion(list['ID'], list, listType, list['expectedUserCount'], reachabilityCheck=False).check()

    @pytest.mark.parametrize(
        'description,campaignType,testControlType,listType, derivedListInfo,schemaIdentifier,popfield', [

            ('Simple include', 'LIVE', 'ORG', 'DERIVED',
             {'includedGroups': ['UPLOADOLD', 'UPLOADOLD', 'DERIVED'], 'excludedGroup': ['UPLOADOLD'],
              'noOfUserUpload': 5, 'derived': ['UPLOADOLD', 'UPLOADOLD']}, 'USER_ID', []),
            ('Simple include', 'LIVE', 'ORG', 'DERIVED',
             {'includedGroups': ['UPLOADOLD', 'UPLOADOLD', 'DERIVED'], 'excludedGroup': ['UPLOADOLD'],
              'noOfUserUpload': 5, 'derived': ['UPLOADOLD', 'UPLOADOLD']}, 'EXTERNAL_ID', [])
        ])
    def test_irisV2_createAudience_Derived_Include_Exclude_DifferentChannels(self, description, campaignType,
                                                                                    testControlType, listType,
                                                                                    derivedListInfo, schemaIdentifier,
                                                                                    popfield):
        list = CreateAudience.derivedList(campaignType, testControlType, schemaIdentifier=[schemaIdentifier],
                                          newUser=False, campaignCheck=False, derivedListInfo=derivedListInfo,
                                          popFields=popfield)
        CreateAudience.waitForGVDToBeUpdated(list['ID'])
        CreateAudienceDBAssertion(list['ID'], list, listType, list['expectedUserCount'],
                                  reachabilityCheck=False).check()

    @pytest.mark.parametrize('description,campaignType,testControlType,listType,derivedListInfo,popfield', [
        ('Include multiple files of all list types', 'LIVE', 'ORG', 'DERIVED',{'includedGroups': ['UPLOAD', 'UPLOADOLD', 'LOYALTY', 'DERIVED'], 'noOfUserUpload': 5, 'derived':['UPLOAD', 'LOYALTY'] },['excludedGroups']),
        ('Include two uploaded list', 'LIVE', 'ORG', 'DERIVED', {'includedGroups': ['UPLOAD','UPLOAD'], 'noOfUserUpload': 5},['excludedGroups']),
        ('Include one uploaded and one filter list', 'LIVE', 'ORG', 'DERIVED',{'includedGroups': ['UPLOAD', 'LOYALTY'], 'noOfUserUpload': 5}, ['excludedGroups']),
        ('Include one uploaded and one Derived list', 'LIVE', 'ORG', 'DERIVED',{'includedGroups': ['UPLOAD', 'DERIVED'], 'noOfUserUpload': 5,'derived':['UPLOAD', 'LOYALTY']}, ['excludedGroups']),
        ('Include one uploaded and one Derived and one filter list', 'LIVE', 'ORG', 'DERIVED',{'includedGroups': ['UPLOAD','LOYALTY', 'DERIVED'], 'noOfUserUpload': 5, 'derived':['UPLOAD', 'LOYALTY']}, ['excludedGroups']),
        ('Include two filter list', 'LIVE', 'ORG', 'DERIVED',{'includedGroups': ['LOYALTY', 'LOYALTY'], 'noOfUserUpload': 5}, ['excludedGroups']),
        ('Include one filter and one upload list', 'LIVE', 'ORG', 'DERIVED',{'includedGroups': ['LOYALTY', 'UPLOAD'], 'noOfUserUpload': 5}, ['excludedGroups']),
        ('Include one filter and one derived list', 'LIVE', 'ORG', 'DERIVED',{'includedGroups': ['LOYALTY', 'DERIVED'], 'noOfUserUpload': 5,'derived':['UPLOAD', 'LOYALTY']}, ['excludedGroups']),
        ('Include one filter and one derived and upload list', 'LIVE', 'ORG', 'DERIVED',{'includedGroups': ['LOYALTY','UPLOAD', 'DERIVED'], 'noOfUserUpload': 5,'derived':['UPLOAD', 'LOYALTY']}, ['excludedGroups']),
        ('Include two derived list', 'LIVE', 'ORG', 'DERIVED',{'includedGroups': ['DERIVED', 'DERIVED'], 'noOfUserUpload': 5,'derived':['UPLOAD', 'LOYALTY'] }, ['excludedGroups']),
        ('Include one derived list and one upload list', 'LIVE', 'ORG', 'DERIVED',{'includedGroups': ['DERIVED', 'LOYALTY'], 'noOfUserUpload': 5, 'derived': ['UPLOAD', 'LOYALTY']},['excludedGroups']),
        ('Include one derived list and one filter list', 'LIVE', 'ORG', 'DERIVED',{'includedGroups': ['DERIVED', 'LOYALTY'], 'noOfUserUpload': 5, 'derived': ['UPLOAD', 'LOYALTY']},['excludedGroups']),
        ('Include one derived list and one filter and one upload list list', 'LIVE', 'ORG', 'DERIVED',{'includedGroups': ['DERIVED','UPLOAD', 'LOYALTY'], 'noOfUserUpload': 5, 'derived': ['UPLOAD', 'LOYALTY']},['excludedGroups']),
        ('Include two list having same users', 'LIVE', 'ORG', 'DERIVED',{'includedGroups': ['UPLOADOLD','UPLOADOLD'], 'noOfUserUpload': 5},['excludedGroups'])
    ])
    def test_irisV2_createAudience_Derived_IncludeAllCases(self, description, campaignType, testControlType, listType,derivedListInfo,popfield):
        list = CreateAudience.derivedList(campaignType, testControlType, campaignCheck=False,derivedListInfo=derivedListInfo,popFields=popfield)
        CreateAudience.waitForGVDToBeUpdated(list['ID'])
        CreateAudienceDBAssertion(list['ID'], list, listType, list['expectedUserCount'] , reachabilityCheck=True).check()

    @pytest.mark.parametrize('description,campaignType,testControlType,listType,derivedListInfo,popfield', [
        ('Include bulk files', 'LIVE', 'ORG', 'DERIVED', {'includedGroups': ['UPLOAD', 'UPLOADOLD', 'LOYALTY', 'DERIVED', 'UPLOAD'], 'noOfUserUpload': 10000, 'derived': ['UPLOAD', 'LOYALTY']}, ['excludedGroups'])
    ])
    def test_irisV2_bulk_createAudience_Derived_IncludeAllCases(self, description, campaignType, testControlType, listType,
                                                           derivedListInfo, popfield):
        list = CreateAudience.derivedList(campaignType, testControlType, campaignCheck=False,
                                          derivedListInfo=derivedListInfo, popFields=popfield)
        CreateAudience.waitForGVDToBeUpdated(list['ID'])
        CreateAudienceDBAssertion(list['ID'], list, listType, list['expectedUserCount'], reachabilityCheck=True).check()

    def test_irisV2_createAudience_Derived_ExistingListName(self):
        label = 'Automation_ExistingList_check_{}'.format(int(time.time() * 1000))
        CreateAudience.derivedList('LIVE', 'ORG',label=label,derivedListInfo={'includedGroups': ['UPLOAD', 'LOYALTY'], 'excludedGroup': ['LOYALTY'], 'noOfUserUpload': 5})
        listDetail = CreateAudience.derivedList('LIVE', 'ORG',label=label,derivedListInfo={'includedGroups': ['UPLOAD', 'LOYALTY'], 'excludedGroup': ['LOYALTY'], 'noOfUserUpload': 5})
        CreateAudience.assertResponse(listDetail['RESPONSE'], 400, 5003,['invalid request : Audience label already exits'])

    def test_irisV2_createAudience_Derived_WithSpecialCharecters(self):
        label = '~!@#$%^&*)(_{}'.format(int(time.time() * 1000))
        list = CreateAudience.derivedList('LIVE', 'ORG',label=label,derivedListInfo={'includedGroups': ['UPLOAD','UPLOAD', 'LOYALTY'], 'excludedGroup': ['LOYALTY'], 'noOfUserUpload': 5})
        CreateAudience.waitForGVDToBeUpdated(list['ID'])
        CreateAudienceDBAssertion(list['ID'], list,'DERIVED', list['expectedUserCount'] , reachabilityCheck=True).check()

    def test_irisV2_createAudience_Derived_WithLabelLengthGretaerThan50Charecters_NegativeCases(self):
        label = 'Automation_ExistingList_checkkkkkkkkkkkkkk_{}'.format(int(time.time() * 1000))
        listDetail = CreateAudience.derivedList('LIVE', 'ORG',label=label*3,derivedListInfo={'includedGroups': ['UPLOAD', 'LOYALTY'], 'excludedGroup': ['LOYALTY'], 'noOfUserUpload': 5})
        CreateAudience.assertResponse(listDetail['RESPONSE'], 400, 102,['Invalid request : Invalid audience name. Name exceeds 160 characters. '])

    @pytest.mark.parametrize('description,derivedListInfo,popfield,statusCode,errorCode,errorDescription' ,[
        ('Include just one list',{'includedGroups': ['UPLOAD'], 'noOfUserUpload': 5},['excludedGroups'],400,5006,['invalid request : combine include and exclude groups size should be minimum 2']),
        ('Empty includeGroups filed', {'includedGroups': [], 'noOfUserUpload': 5}, ['excludedGroups'], 400, 102,['Invalid request : include groups cannot be empty'])
    ])
    def test_irisV2_createAudience_Derived_IncludeList_IncludeGroups_NegativeCases(self, description,derivedListInfo,popfield,statusCode,errorCode,errorDescription):
        list = CreateAudience.derivedList('LIVE','ORG',updateNode=True,lockNode=True,campaignCheck=False,derivedListInfo=derivedListInfo,popFields=popfield)
        CreateAudience.assertResponse(list['RESPONSE'],statusCode,errorCode,errorDescription)

    def test_irisV2_createAudience_Derived_IncludeList_InvalidIncludedGroups_NegativeCases(self):
        payload = copy.deepcopy(constant.payload['derivedlist'])
        payload.pop('excludedGroups')
        payload['includedGroups'] = [self.listId_1, -9999]
        list = CreateAudience.derivedList('LIVE', 'ORG', updateNode=True, lockNode=True, campaignCheck=False,payload=payload)
        CreateAudience.assertResponse(list['RESPONSE'], 400, 5004, ['invalid audience group : audience groups not exists: [-9999]'])

    def test_irisV2_createAudience_Derived_IncludeList_InvalidIncludedGroups_NegativeCases(self):
        payload = copy.deepcopy(constant.payload['derivedlist'])
        payload.pop('excludedGroups')
        payload['includedGroups'] = [self.listId_1, 999999]
        list = CreateAudience.derivedList('LIVE', 'ORG', updateNode=True, lockNode=True, campaignCheck=False,payload=payload)
        CreateAudience.assertResponse(list['RESPONSE'], 400, 5004, ['invalid audience group : audience groups not exists: [999999]'])

    def test_irisV2_createAudience_Derived_IncludeList_SameListIdIncludedGroups_NegativeCases(self):
        payload = copy.deepcopy(constant.payload['derivedlist'])
        payload.pop('excludedGroups')
        payload['includedGroups'] = [self.listId_1, self.listId_1]
        list = CreateAudience.derivedList('LIVE', 'ORG', updateNode=True, lockNode=True, campaignCheck=False,payload=payload)
        CreateAudience.assertResponse(list['RESPONSE'], 400, 5006, ['invalid request : include groups contains duplicate','invalid request : combine include and exclude groups size should be minimum 2'])

    @pytest.mark.parametrize('description,payloadChange,statusCode,errorCode,errorDescription', [
        ('Incorrect audience group field value', {"audienceGroupType" : "DDDD"}, 400, 102,['Invalid request : Invalid Audience group type ']),
        ('Audience group field empty', {"audienceGroupType": ""}, 400, 102,['Invalid request : Invalid Audience group type ']),
        ('Label field value empty', {"label": ""}, 400, 102,['Invalid request : Group Label cannot be empty'])

    ])
    def test_irisV2_createAudience_Derived_IncludeList_InvalidFields_NegativeCases(self, description,payloadChange, statusCode,errorCode, errorDescription):
        payload = copy.deepcopy(constant.payload['derivedlist'])
        payload.pop('excludedGroups')
        payload['includedGroups'] = [self.listId_1, self.listId_2]
        for eachKey in payload:
            if eachKey in payloadChange: payload[eachKey] = payloadChange[eachKey]

        list = CreateAudience.derivedList('LIVE', 'ORG', updateNode=True, lockNode=True, campaignCheck=False,payload=payload)
        CreateAudience.assertResponse(list['RESPONSE'], statusCode, errorCode, errorDescription)

    @pytest.mark.parametrize('description,payloadChange,statusCode,errorCode,errorDescription', [
        ('Incorrect audience group field', {"audienceGroupType": "audienceGroupTypeee"}, 400, 107,['Unrecognized field : audienceGroupTypeee']),
        ('Incorrect includedGroups group field', {"includedGroups": "includedGroupss"}, 400, 107,['Unrecognized field : includedGroupss']),
        ('Incorrect label field', {"label": "labe"}, 400, 107,['Unrecognized field : labe']),
        ('Incorrect description field', {"description": "desc"}, 400, 107,['Unrecognized field : desc']),
        ('Incorrect excludedGroups field', {"excludedGroups": "excludedGroupssss"}, 400, 107, ['Unrecognized field : excludedGroupssss'])
        ])
    def test_irisV2_createAudience_Derived_IncludeList_InvalidFieldIncludedGroups_NegativeCases(self, description, payloadChange, statusCode,errorCode, errorDescription):
        payload = copy.deepcopy(constant.payload['derivedlist'])
        payload['includedGroups'] = [self.listId_1, self.listId_2]
        for eachKey in payload:
            if eachKey in payloadChange:
                value = payload[eachKey]
                payload.pop(eachKey)
                payload[payloadChange[eachKey]] = value
        list = CreateAudience.derivedList('LIVE', 'ORG', updateNode=True, lockNode=True, campaignCheck=False,payload=payload)
        CreateAudience.assertResponse(list['RESPONSE'], statusCode, errorCode, errorDescription)


    @pytest.mark.parametrize('description,payloadChange,statusCode,errorCode,errorDescription', [
        ('Without audience group field', "includedGroups", 400, 102,['Invalid request : include groups cannot be null','Invalid request : include groups cannot be empty']),
        ('Without includedGroups group field', "audienceGroupType", 400, 102,['Invalid request : Invalid Audience group type ']),
        ('Without label field', "label", 400, 102, ['Invalid request : Group Label cannot be null','Invalid request : Group Label cannot be empty'])
    ])
    def test_irisV2_createAudience_Derived_IncludeList_WithoutFieldInPayload_NegativeCases(self, description, payloadChange, statusCode,errorCode, errorDescription):
        payload = copy.deepcopy(constant.payload['derivedlist'])
        payload.pop('excludedGroups')
        payload['includedGroups'] = [self.listId_1, self.listId_2]
        payload.pop(payloadChange)
        list = CreateAudience.derivedList('LIVE', 'ORG', updateNode=True, lockNode=True, campaignCheck=False,payload=payload)
        CreateAudience.assertResponse(list['RESPONSE'], statusCode, errorCode, errorDescription)

    @pytest.mark.parametrize('description,campaignType,testControlType,listType, derivedListInfo,popfield', [
        ('Include and exclude multiple file', 'LIVE', 'ORG', 'DERIVED',{'includedGroups': ['UPLOADOLD','UPLOAD','UPLOAD', 'UPLOAD','LOYALTY','DERIVED'], 'excludedGroup': ['LOYALTY','UPLOADOLD','UPLOAD','DERIVED'], 'noOfUserUpload': 5, 'derived':['UPLOAD', 'LOYALTY']}, []),
        ('Include and exclude two different file with different users', 'LIVE', 'ORG', 'DERIVED',{'includedGroups': ['UPLOAD'],'excludedGroup': ['UPLOAD'], 'noOfUserUpload': 5}, []),
        ('Exclude group is empty', 'LIVE', 'ORG', 'DERIVED',{'includedGroups': ['UPLOAD','UPLOAD'], 'excludedGroup': [], 'noOfUserUpload': 5}, [])
    ])
    def test_irisV2_createAudience_Derived_Include_Exclude_Allcases(self, description, campaignType, testControlType,listType,derivedListInfo, popfield):
        list = CreateAudience.derivedList(campaignType, testControlType, campaignCheck=False,derivedListInfo=derivedListInfo, popFields=popfield)
        CreateAudience.waitForGVDToBeUpdated(list['ID'])
        CreateAudienceDBAssertion(list['ID'], list, listType, list['expectedUserCount'] , reachabilityCheck=True).check()

    def test_irisV2_createAudience_Derived_IncludeExcludeList_WithNegativeListIdInExcludeGroup_NegativeCases(self):
        payload = copy.deepcopy(constant.payload['derivedlist'])
        payload['includedGroups'] = [self.listId_1, self.listId_2]
        payload['excludedGroups'] = [-9999]
        list = CreateAudience.derivedList('LIVE', 'ORG', updateNode=True, lockNode=True, campaignCheck=False,payload=payload)
        CreateAudience.assertResponse(list['RESPONSE'], 400, 5004, ['invalid audience group : audience groups not exists: [-9999]'])

    def test_irisV2_createAudience_Derived_IncludeExcludeList_WithInvalidIdInExcludeGroup_NegativeCases(self):
        payload = copy.deepcopy(constant.payload['derivedlist'])
        payload['includedGroups'] = [self.listId_1, self.listId_2]
        payload['excludedGroups'] = [99999]
        list = CreateAudience.derivedList('LIVE', 'ORG', updateNode=True, lockNode=True, campaignCheck=False,payload=payload)
        CreateAudience.assertResponse(list['RESPONSE'], 400, 5004, ['invalid audience group : audience groups not exists: [99999]'])

    def test_irisV2_createAudience_Derived_IncludeExcludeList_WithSameIdInExcludeIncludeGroup_NegativeCases(self):
        payload = copy.deepcopy(constant.payload['derivedlist'])
        payload['includedGroups'] = [self.listId_1, self.listId_2]
        payload['excludedGroups'] = [self.listId_1]
        list = CreateAudience.derivedList('LIVE', 'ORG', updateNode=True, lockNode=True, campaignCheck=False,payload=payload)
        CreateAudience.assertResponse(list['RESPONSE'], 400, 5006, ['invalid request : groups added in both include and exclude : [{}]'.format(self.listId_1)])

    @pytest.mark.parametrize('description,derivedListInfo,popfield,statusCode,errorCode,errorDescription', [
        ('Include more than 10 lists', {'includedGroups': ['UPLOAD','UPLOAD','UPLOAD','UPLOAD','UPLOAD','UPLOAD','UPLOAD','UPLOAD','UPLOAD','UPLOAD','UPLOAD'], 'noOfUserUpload': 5}, ['excludedGroups'], 400, 5006,['invalid request : more than 10 groups are not allowed in include audience list']),
        ('Exclude more than 10 lists', {'includedGroups': ['UPLOAD'],'excludedGroup': ['UPLOAD','UPLOAD','UPLOAD','UPLOAD','UPLOAD','UPLOAD','UPLOAD','UPLOAD','UPLOAD','UPLOAD','UPLOAD'], 'noOfUserUpload': 5}, [], 400, 5006,['invalid request : more than 10 groups are not allowed in exclude audience list']),
        ('Include more than 10 lists', {'includedGroups': ['UPLOAD', 'UPLOAD', 'UPLOAD', 'UPLOAD', 'UPLOAD', 'UPLOAD', 'UPLOAD', 'UPLOAD', 'UPLOAD','UPLOAD', 'UPLOAD'],'excludedGroup': ['UPLOAD','UPLOAD','UPLOAD','UPLOAD','UPLOAD','UPLOAD','UPLOAD','UPLOAD','UPLOAD','UPLOAD','UPLOAD'], 'noOfUserUpload': 5}, [], 400, 5006,['invalid request : more than 10 groups are not allowed in exclude audience list', 'invalid request : more than 10 groups are not allowed in include audience list'])
    ])
    def test_irisV2_createAudience_Derived_IncludeList_ExcludeList_MoreThan10Lists_NegativeCases(self, description, derivedListInfo,popfield, statusCode, errorCode,errorDescription):
        list = CreateAudience.derivedList('LIVE', 'ORG', updateNode=True, lockNode=True, campaignCheck=False,derivedListInfo=derivedListInfo, popFields=popfield)
        CreateAudience.assertResponse(list['RESPONSE'], statusCode, errorCode, errorDescription)