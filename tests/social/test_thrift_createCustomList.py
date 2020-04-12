import pytest, time, json, pytest_ordering, copy
from src.Constant.constant import constant
from src.utilities.logger import Logger
from src.modules.iris.construct import construct
from src.modules.social.socialObject import SocialObject
from src.modules.social.socialHelper import SocialHelper

@pytest.mark.run(order=1)
class Test_Social_Thrift_CustomList():
    
    def setup_class(self):
        self.campaigns = SocialHelper.createCampaignsForSocialThrift()

    def setup_method(self, method):
        self.connObj = SocialHelper.getConnObj(newConnection=True)
        Logger.logMethodName(method.__name__)
    
    @pytest.mark.parametrize('numberOfUsers,identifier,listName,description,channel,testControlType', [
        (5, 'mobile', 'Auto_List_{}_{}_{}', 'createCustomList thrift Call Test','facebook','ORG'),
        ])
    def test_socialThrift_createCustomList_Sanity(self,numberOfUsers,identifier,listName,description,channel,testControlType):
        groupVersionid,groupName = SocialHelper.createListForSocial(self.campaigns,testControlType)
        messageId = SocialHelper.createMessageForThriftHelp(self.campaigns[testControlType],groupVersionid,numberOfUsers,groupName)
        listName = listName.format(identifier,testControlType,int(time.time()*1000))
        CreateCustomAudienceListResponse = self.connObj.createCustomList(
            SocialHelper.createUserListObject(numberOfUsers,identifier),
            SocialObject.CustomAudienceListDetails(listName,description,messageId),
            SocialObject.SocialAccountDetails(channel),
            constant.config['orgId'],
            str(groupVersionid),
            'requestId_automationthriftCall_{}'.format(int(time.time()*1000))
        )
        Logger.log('Create Audience List , Response Message :{}'.format(CreateCustomAudienceListResponse.message))
        SocialHelper.assertCreateCustomList(groupVersionid,messageId,CreateCustomAudienceListResponse,listName,description)

    
    @pytest.mark.parametrize('numberOfUsers,identifier,listName,description,channel,testControlType', [
        (5, 'mobile', 'Auto_List_{}_{}_{}', 'createCustomList thrift Call Test','facebook','CUSTOM'),
        (5, 'mobile', 'Auto_List_{}_{}_{}', 'createCustomList thrift Call Test','facebook','SKIP'),
        (5, 'email', 'Auto_List_{}_{}_{}', 'createCustomList thrift Call Test','facebook','ORG'),
        (5, 'email', 'Auto_List_{}_{}_{}', 'createCustomList thrift Call Test','facebook','CUSTOM'),
        (5, 'email', 'Auto_List_{}_{}_{}', 'createCustomList thrift Call Test','facebook','SKIP'),
        ])
    def test_socialThrift_createCustomList_WithDifferentTestControlType(self,numberOfUsers,identifier,listName,description,channel,testControlType):
        groupVersionid,groupName = SocialHelper.createListForSocial(self.campaigns,testControlType)
        messageId = SocialHelper.createMessageForThriftHelp(self.campaigns[testControlType],groupVersionid,numberOfUsers,groupName)
        listName = listName.format(identifier,testControlType,int(time.time()*1000))
        CreateCustomAudienceListResponse = self.connObj.createCustomList(
            SocialHelper.createUserListObject(numberOfUsers,identifier),
            SocialObject.CustomAudienceListDetails(listName,description,messageId),
            SocialObject.SocialAccountDetails(channel),
            constant.config['orgId'],
            str(groupVersionid),
            'requestId_automationthriftCall_{}'.format(int(time.time()*1000))
        )
        Logger.log('Create Audience List , Response Message :{}'.format(CreateCustomAudienceListResponse.message))
        SocialHelper.assertCreateCustomList(groupVersionid,messageId,CreateCustomAudienceListResponse,listName,description)

    @pytest.mark.parametrize('numberOfUsers,identifier,listName,description,channel,testControlType', [
        (5, 'mobile', 'Auto_List_{}_{}_{}', 'createCustomList thrift Call Test','facebook','ORG'),
        ])
    def test_socialThrift_createCustomList_withSameIdMultipleTimes(self,numberOfUsers,identifier,listName,description,channel,testControlType):
        groupVersionid,groupName = SocialHelper.createListForSocial(self.campaigns,testControlType)
        messageId = SocialHelper.createMessageForThriftHelp(self.campaigns[testControlType],groupVersionid,numberOfUsers,groupName)
        listName = listName.format(identifier,testControlType,int(time.time()*1000))
        preCreatedListId = None
        for _ in range(2):
            CreateCustomAudienceListResponse = self.connObj.createCustomList(
                SocialHelper.createUserListObject(numberOfUsers,identifier),
                SocialObject.CustomAudienceListDetails(listName,description,messageId),
                SocialObject.SocialAccountDetails(channel),
                constant.config['orgId'],
                str(groupVersionid),
                'requestId_automationthriftCall_{}'.format(int(time.time()*1000))
            )
            SocialHelper.assertCreateCustomList(groupVersionid,messageId,CreateCustomAudienceListResponse,listName,description)
            if preCreatedListId is None :
                preCreatedListId = CreateCustomAudienceListResponse.listid
            else:
                SocialHelper.assertRemoteListIds(preCreatedListId,CreateCustomAudienceListResponse.listid)

    def test_socialThrift_getCustomAudienceLists_Sanity(self):
        GetCustomAudienceListsResponse = self.connObj.getCustomAudienceLists(
            constant.config['orgId'],
            SocialObject().SocialChannel['facebook'],
            True,
            'requestId_automationthriftCall_{}'.format(int(time.time()*1000))
        )
        Logger.log('Message From Get Custom Audience List : {}'.format(GetCustomAudienceListsResponse.message))
        SocialHelper.assertGetCustomAudienceList(GetCustomAudienceListsResponse)

    def test_socialThrift_deleteSocialAudienceList(self):
        GetCustomAudienceListsResponse = self.connObj.getCustomAudienceLists(
            constant.config['orgId'],
            SocialObject().SocialChannel['facebook'],
            True,
            'requestId_automationthriftCall_{}'.format(int(time.time()*1000))
        )

        for eachList in GetCustomAudienceListsResponse.customAudienceLists:
            firstListFromGetAudienceList = eachList.remoteListId
            self.connObj.deleteSocialAudienceList(
                SocialObject().SocialChannel['facebook'],
                constant.config['orgId'],
                firstListFromGetAudienceList,
                'requestId_automationthriftCall_{}'.format(int(time.time()*1000))
                )

            GetCustomAudienceListsResponseForEach = self.connObj.getCustomAudienceLists(
                constant.config['orgId'],
                SocialObject().SocialChannel['facebook'],
                True,
                'requestId_automationthriftCall_{}'.format(int(time.time()*1000))
            )
            SocialHelper.assertDeleteSocialAudienceList(GetCustomAudienceListsResponseForEach,firstListFromGetAudienceList)

    @pytest.mark.parametrize('numberOfUsers,identifier,listName,description,channel,testControlType', [
        (5, 'mobile', 'Auto_List_{}_{}_{}', 'createCustomList thrift Call Test','facebook','ORG'),
        ])
    def test_socialThrift_integrateOfCreateAndGetList(self,numberOfUsers,identifier,listName,description,channel,testControlType):
        groupVersionid,groupName = SocialHelper.createListForSocial(self.campaigns,testControlType)
        messageId = SocialHelper.createMessageForThriftHelp(self.campaigns[testControlType],groupVersionid,numberOfUsers,groupName)
        listName = listName.format(identifier,testControlType,int(time.time()*1000))
        CreateCustomAudienceListResponse = self.connObj.createCustomList(
            SocialHelper.createUserListObject(numberOfUsers,identifier),
            SocialObject.CustomAudienceListDetails(listName,description,messageId),
            SocialObject.SocialAccountDetails(channel),
            constant.config['orgId'],
            str(groupVersionid),
            'requestId_automationthriftCall_{}'.format(int(time.time()*1000))
        )
        Logger.log('Create Audience List , Response Message :{}'.format(CreateCustomAudienceListResponse.message))
        
        GetCustomAudienceListsResponse = self.connObj.getCustomAudienceLists(
            constant.config['orgId'],
            SocialObject().SocialChannel['facebook'],
            True,
            'requestId_automationthriftCall_{}'.format(int(time.time()*1000))
        )
        Logger.log('Message From Get Custom Audience List : {}'.format(GetCustomAudienceListsResponse.message))
        SocialHelper.assertNewCreatedListInGetCall(listName,GetCustomAudienceListsResponse)

