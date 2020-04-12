import pytest, copy, time
from src.modules.irisv2.list.createAudience import CreateAudience
from src.modules.irisv2.list.createAudienceDBAssertion import CreateAudienceDBAssertion
from src.dbCalls.campaignShard import list_Calls
from src.utilities.logger import Logger
from src.Constant.constant import constant


@pytest.mark.run(order=12)
class Test_CreateAudience_StickyList():

    def setup_class(self):
        CreateAudience.getPocUsers()

    def setup_method(self, method):
        Logger.logMethodName(method.__name__)
        self.listInfo = list_Calls().getAllGroupDetails(2, 0, 'created_date', None)

    @pytest.mark.parametrize('campaignType,testControlType,listType', [
        ('LIVE', 'ORG', 'ORG_USERS')
    ])
    def test_irisV2_createAudience_stickyList_Sanity(self, campaignType, testControlType, listType):
        list = CreateAudience.stickyList(campaignType, testControlType, campaignCheck=False,
                                         stickyInfo={'excludeUsers': [], 'includeUsers': ':1'})
        CreateAudience.waitForGVDToBeUpdated(list['ID'])
        CreateAudienceDBAssertion(list['ID'], list, listType, 1, reachabilityCheck=True).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType', [
        ('UPCOMING', 'ORG', 'ORG_USERS'),
        ('LAPSED', 'ORG', 'ORG_USERS'),
        ('LIVE', 'CUSTOM', 'ORG_USERS'),
        ('UPCOMING', 'CUSTOM', 'ORG_USERS'),
        ('LAPSED', 'CUSTOM', 'ORG_USERS'),
        ('LIVE', 'SKIP', 'ORG_USERS'),
        ('UPCOMING', 'SKIP', 'ORG_USERS'),
        ('LAPSED', 'SKIP', 'ORG_USERS'),
    ])
    def test_irisV2_createAudience_stickyList(self, campaignType, testControlType, listType):
        list = CreateAudience.stickyList(campaignType, testControlType, campaignCheck=False,
                                         stickyInfo={'excludeUsers': [], 'includeUsers': ':1'})
        CreateAudience.waitForGVDToBeUpdated(list['ID'])
        CreateAudienceDBAssertion(list['ID'], list, listType, 1, reachabilityCheck=True).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType', [
        ('LIVE', 'ORG', 'ORG_USERS')
    ])
    def test_irisV2_createAudience_stickyList_updateGroupId_Sanity(self, campaignType, testControlType, listType):
        customerCount = list_Calls().getCustomerCountInGVD(self.listInfo[0]['gId'])
        list = CreateAudience.stickyList(campaignType, testControlType, campaignCheck=False,
                                         stickyInfo={'excludeUsers': [], 'includeUsers': ':1',
                                                     'groupId': self.listInfo[0]['gId'],
                                                     'label': self.listInfo[0]['gLabel']})
        CreateAudience.waitForGVDToBeUpdated(list['ID'])
        CreateAudienceDBAssertion(list['ID'], list, listType, customerCount, reachabilityCheck=True, isGVUpdated=True).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType', [
        ('UPCOMING', 'ORG', 'ORG_USERS'),
        ('LAPSED', 'ORG', 'ORG_USERS'),
        ('LIVE', 'CUSTOM', 'ORG_USERS'),
        ('UPCOMING', 'CUSTOM', 'ORG_USERS'),
        ('LAPSED', 'CUSTOM', 'ORG_USERS'),
        ('LIVE', 'SKIP', 'ORG_USERS'),
        ('UPCOMING', 'SKIP', 'ORG_USERS'),
        ('LAPSED', 'SKIP', 'ORG_USERS'),
    ])
    def test_irisV2_createAudience_stickyList_updateGroupId(self, campaignType, testControlType, listType):
        customerCount = list_Calls().getCustomerCountInGVD(self.listInfo[0]['gId'])
        list = CreateAudience.stickyList(campaignType, testControlType, campaignCheck=False,
                                         stickyInfo={'excludeUsers': [], 'includeUsers': ':1',
                                                     'groupId': self.listInfo[0]['gId'],
                                                     'label': self.listInfo[0]['gLabel']})
        CreateAudience.waitForGVDToBeUpdated(list['ID'])
        CreateAudienceDBAssertion(list['ID'], list, listType, customerCount , reachabilityCheck=True,
                                  isGVUpdated=True).check()

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
    def test_irisV2_createAudience_stickyList_newUsers(self, campaignType, testControlType, listType):
        list = CreateAudience.stickyList(campaignType, testControlType,
                                         campaignCheck=False,
                                         stickyInfo={'excludeUsers': CreateAudience.getPocNewUsers(newUsers=True),
                                                     'includeUsers': CreateAudience.getPocNewUsers(newUsers=True)})
        CreateAudience.waitForGVDToBeUpdated(list['ID'])
        CreateAudienceDBAssertion(list['ID'], list, listType, 2, reachabilityCheck=True).check()

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
    def test_irisV2_createAudience_stickyList_includeNewUsersWithGroupId(self, campaignType, testControlType, listType):
        customerCount = list_Calls().getCustomerCountInGVD(self.listInfo[0]['gId'])
        list = CreateAudience.stickyList(campaignType, testControlType, campaignCheck=False,
                                         stickyInfo={'excludeUsers': [],
                                                     'includeUsers': CreateAudience.getPocNewUsers(newUsers=True),
                                                     'groupId': self.listInfo[0]['gId'],
                                                     'label': self.listInfo[0]['gLabel']})
        CreateAudience.waitForGVDToBeUpdated(list['ID'])
        CreateAudienceDBAssertion(list['ID'], list, listType, (customerCount + 2), reachabilityCheck=True,
                                  isGVUpdated=True).check()

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
    def test_irisV2_createAudience_stickyList_newUsersAndGroupId(self, campaignType, testControlType, listType):
        customerCount = list_Calls().getCustomerCountInGVD(self.listInfo[0]['gId'])
        list = CreateAudience.stickyList(campaignType, testControlType, campaignCheck=False,
                                         stickyInfo={'excludeUsers': CreateAudience.getPocNewUsers(newUsers=True),
                                                     'includeUsers': CreateAudience.getPocNewUsers(newUsers=True),
                                                     'groupId': self.listInfo[0]['gId'],
                                                     'label': self.listInfo[0]['gLabel']})
        CreateAudience.waitForGVDToBeUpdated(list['ID'])
        CreateAudienceDBAssertion(list['ID'], list, listType, (customerCount + 2), reachabilityCheck=True, isGVUpdated=True).check()

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
    def test_irisV2_createAudience_stickyList_PocUsersAndNewUsers(self, campaignType, testControlType, listType):
        stickyId = CreateAudience.stickyList(campaignType, testControlType, campaignCheck=False, updateNode=True, lockNode=True, stickyInfo={'excludeUsers': [], 'includeUsers': ':1', })
        includeUsers = constant.config['pocUsers'] + CreateAudience.getPocNewUsers(newUsers=True)
        customerCount = list_Calls().getCustomerCountInGVD(stickyId['ID']) + (len(includeUsers) -1)
        list = CreateAudience.stickyList(campaignType, testControlType, campaignCheck=False,
                                         stickyInfo={'excludeUsers': CreateAudience.getPocNewUsers(newUsers=True),
                                                     'includeUsers': includeUsers,
                                                     'groupId': stickyId['ID'],
                                                     'label': stickyId['NAME']})
        CreateAudience.waitForGVDToBeUpdated(list['ID'])
        CreateAudienceDBAssertion(list['ID'], list, listType, (customerCount), reachabilityCheck=True, isGVUpdated=True).check()

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
    def test_irisV2_createAudience_stickyList_ExcludePocUsersAndNewUsers(self, campaignType, testControlType, listType):
        stickyId = CreateAudience.stickyList(campaignType, testControlType, campaignCheck=False, updateNode=True, lockNode=True ,stickyInfo={'excludeUsers': [], 'includeUsers': ':1',})
        excludeUsers = constant.config['pocUsers'] + CreateAudience.getPocNewUsers(newUsers=True)
        customerCount = list_Calls().getCustomerCountInGVD(stickyId['ID']) - 1
        list = CreateAudience.stickyList(campaignType, testControlType, campaignCheck=False,
                                         stickyInfo={'excludeUsers': excludeUsers,
                                                     'includeUsers': CreateAudience.getPocNewUsers(newUsers=True),
                                                     'groupId': stickyId['ID'],
                                                     'label': stickyId['NAME']})
        CreateAudience.waitForGVDToBeUpdated(list['ID'])
        CreateAudienceDBAssertion(list['ID'], list, listType, (customerCount + 2), reachabilityCheck=True, isGVUpdated=True).check()

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
    def test_irisV2_createAudience_stickyList_emptyIncludeUsersUpdate(self, campaignType, testControlType, listType):
        customerCount = list_Calls().getCustomerCountInGVD(self.listInfo[0]['gId'])
        list = CreateAudience.stickyList(campaignType, testControlType, campaignCheck=False,
                                         stickyInfo={'excludeUsers': constant.config['pocUsers'],
                                                     'includeUsers': [],
                                                     'groupId': self.listInfo[0]['gId'],
                                                     'label': self.listInfo[0]['gLabel']})
        CreateAudience.waitForGVDToBeUpdated(list['ID'])
        CreateAudienceDBAssertion(list['ID'], list, listType, (customerCount), reachabilityCheck=True, isGVUpdated=True).check()

    @pytest.mark.parametrize('description,includeUsers, excludeUsers,statusCode, errorCode, errorMessage', [
        ('Duplicate usersList include',2,1, 400, 5006, ['invalid request : duplicate users in include users list']),
        ('Duplicate usersList exclude',1,2, 400, 5006, ['invalid request : duplicate users in exclude users list']),
        ('same usersList include & exclude',0,0, 400, 5006, ['invalid request : no users for inclusion and exclusion in org users group'])
    ])
    def test_irisV2_createAudience_stickyList_NegativeCase_01(self,description,includeUsers, excludeUsers,statusCode, errorCode, errorMessage):
        list = CreateAudience.stickyList('LIVE', 'ORG', campaignCheck=False,
                                         stickyInfo={'excludeUsers': CreateAudience.getPocNewUsers() * excludeUsers, 'includeUsers': constant.config['pocUsers'] * includeUsers})
        CreateAudience.assertResponse(list['RESPONSE'], statusCode, errorCode,errorMessage)

    @pytest.mark.parametrize('description,popFields,updatePayload,statusCode, errorCode, errorMessage', [
        ('without Label in payload',['label'],{}, 400, 102, ['Invalid request : Group Label cannot be null', 'Invalid request : Group Label cannot be empty']),
        ('without includeUsers in payload',['includeUsers'],{}, 400, 102, ['Invalid request : include users cannot be null']),
        ('Negative group id update',[],{'groupId' : -99999}, 400, 5006, ['invalid request : group id must be positive number']),
        ('Invalid group id update',[],{'groupId' : 99999}, 400, 5006, ['invalid request : group not found'])
    ])
    def test_irisV2_createAudience_stickyList_NegativeCase_02(self,description,popFields,updatePayload,statusCode, errorCode, errorMessage):
        stickyData = {'excludeUsers': CreateAudience.getPocNewUsers(), 'includeUsers': constant.config['pocUsers']}
        stickyData.update(updatePayload)
        list = CreateAudience.stickyList('LIVE', 'ORG', campaignCheck=False,
                                         stickyInfo=stickyData, popFields=popFields)
        CreateAudience.assertResponse(list['RESPONSE'], statusCode, errorCode,errorMessage)

    @pytest.mark.parametrize('description,updatePayload,statusCode, errorCode, errorMessage', [
        ('same usersList include & exclude', {}, 400, 5006, ['invalid request : users are present in include and exclude list'])
    ])
    def test_irisV2_createAudience_stickyList_NegativeCase_03(self,description,updatePayload,statusCode, errorCode, errorMessage):
        stickyData = {'excludeUsers': constant.config['pocUsers'], 'includeUsers': constant.config['pocUsers'], 'groupId': self.listInfo[0]['gId'], 'label': self.listInfo[0]['gLabel']}
        stickyData.update(updatePayload)
        list = CreateAudience.stickyList('LIVE', 'ORG', campaignCheck=False,
                                         stickyInfo=stickyData)
        CreateAudience.assertResponse(list['RESPONSE'], statusCode, errorCode,errorMessage)