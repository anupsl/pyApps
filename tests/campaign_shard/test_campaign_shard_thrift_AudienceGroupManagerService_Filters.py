import pytest, time, json, pytest_ordering, copy
from src.Constant.constant import constant
from src.utilities.logger import Logger
from src.modules.iris.construct import construct
from src.modules.campaign_shard.campaignShardObject import campaignShardObject
from src.modules.campaign_shard.campaignShardHelper import CampaignShardHelper

@pytest.mark.run(order=4)
class Test_CampaignShard_Thrift_AudienceGroupManagerService_Filters():
    
    def setup_class(self):
        testControlTypeSupported = ['org', 'skip', 'custom']
        listSupported = ['filter', 'upload']
        Logger.logSuiteName(str(self).split('.')[-1])
        self.campaignShardObject = campaignShardObject()
        self.intialUsedObject = copy.deepcopy(constant.thiriftCampaignShardTestReferenceObject)
        CampaignShardHelper.setupCampaignsInThriftReference(typesOfCampaign=testControlTypeSupported)
        CampaignShardHelper.setupListInThriftReference(listSupported, typesOfCampaign=testControlTypeSupported)
    
    def teardown_class(self):
        constant.thiriftCampaignShardTestReferenceObject = copy.deepcopy(self.intialUsedObject)
     
    def setup_method(self, method):
        self.connObj = CampaignShardHelper.getConnObj(newConnection=True)
        Logger.logMethodName(method.__name__)
        
    @pytest.mark.parametrize('campaignType,audienceType', [
        ('org', 'FILTER_BASED'),
        ('skip', 'FILTER_BASED'),
        ('custom', 'FILTER_BASED')
        ])
    def test_campaignShardThrfit_getAudienceGroupWithDataSourceInfo_filter(self, campaignType, audienceType):
        groupId = constant.thiriftCampaignShardTestReferenceObject[campaignType]['campaign']['lists'][audienceType][0]['groupDetails']['id']        
        Logger.log('Making getAudienceGroupWithDataSourceInfo Thrift Call for campaignType :{} , audienceType :{} with  groupId :{}'.format(campaignType, audienceType, groupId))
        AudienceGroup = self.connObj.getAudienceGroupWithDataSourceInfo(self.campaignShardObject.AudienceGroupDataSourceInfoRequest(groupId))
        CampaignShardHelper.validateGetAudienceGroupWithDataSourceInfo(campaignType, audienceType, AudienceGroup)
    
    @pytest.mark.parametrize('campaignType,audienceType', [
        ('org', 'FILTER_BASED'),
        ('skip', 'FILTER_BASED'),
        ('custom', 'FILTER_BASED')
        ])   
    def test_campaignShardThrfit_AudienceGroupUserInfoRequest_filterBased(self, campaignType, audienceType):
        testList = constant.thiriftCampaignShardTestReferenceObject[campaignType]['campaign']['lists'][audienceType][0]
        groupId = testList['groupDetails']['id']       
        Logger.log('Checking for All Test Users in groupId : {}'.format(groupId))
        listOfTestResponse = []
        listOfControlResponse = []
        for eachuser in  testList['campaignGroupRecipients']['TEST']:
            AudienceGroupBoolRes = self.connObj.isUserInGroup(self.campaignShardObject.AudienceGroupUserInfoRequest(eachuser, groupId))
            listOfTestResponse.append((eachuser, AudienceGroupBoolRes.success))
        if 'CONTROL' in testList['campaignGroupRecipients']:
            Logger.log('Checking for All Control Users in groupId : {}'.format(groupId))
            for eachuser in  testList['campaignGroupRecipients']['CONTROL']:
                AudienceGroupBoolRes = self.connObj.isUserInGroup(self.campaignShardObject.AudienceGroupUserInfoRequest(eachuser, groupId))
                listOfControlResponse.append((eachuser, AudienceGroupBoolRes.success)) 
        CampaignShardHelper.validateAudienceGroupBoolRes({'TEST':listOfTestResponse, 'CONTROL':listOfControlResponse})
    
    @pytest.mark.parametrize('audienceType', [
        (['FILTER_BASED']),
        (['UPLOADED'])
        ])   
    def test_campaignShardThrift_searchAudienceGroup_filterBased(self, audienceType):
        listOfAudienceType = []
        for eachAudienceType in audienceType:
            listOfAudienceType.append(self.campaignShardObject.AudienceGroupType[eachAudienceType])
        listOfAudienceGroup = self.connObj.searchAudienceGroup(listOfAudienceType)
        CampaignShardHelper.validateSearchAudienceGroup(audienceType, listOfAudienceGroup, campaignType=['org'])
    
    @pytest.mark.parametrize('campaignType,audienceType', [
        ('org', 'FILTER_BASED'),
        ('org', 'UPLOADED')
        ])
    def test_campaignShardThrift_searchAudienceGroupByLabel_filterBased(self, campaignType, audienceType):
        listOfAudienceType = [self.campaignShardObject.AudienceGroupType[audienceType]]
        listOfAudienceGroup = self.connObj.searchAudienceGroup(listOfAudienceType)
    
        groupLabel = constant.thiriftCampaignShardTestReferenceObject[campaignType]['campaign']['lists'][audienceType][0]['groupLabel']        
        listOfAudienceGroup = self.connObj.searchAudienceGroupByLabel(groupLabel, listOfAudienceType)
        CampaignShardHelper.validateGetAudienceGroupWithDataSourceInfo(campaignType, audienceType, listOfAudienceGroup[0], checkS3=False)
    
    
    @pytest.mark.parametrize('campaignType,audienceType,testPercentage', [
        ('org', 'FILTER_BASED', 90),
        ('org', 'UPLOADED', 90)
        ])   
    def test_campaignShardThrift_newSearchAudienceGroup(self, campaignType, audienceType, testPercentage):
        audienceSearchRequest = self.campaignShardObject.AudienceSearchRequest(
            searchText="",
            audienceGroupTypes=[self.campaignShardObject.AudienceGroupType[audienceType]],
            testControl=self.campaignShardObject.TestControl(campaignType, testPercentage)
            )
        listOfAudienceGroup = self.connObj.newSearchAudienceGroup(audienceSearchRequest)
        CampaignShardHelper.validateSearchAudienceGroup([audienceType], listOfAudienceGroup, campaignType=[campaignType])

    @pytest.mark.parametrize('campaignType,audienceType,testPercentage', [
        ('org', 'FILTER_BASED', 90),
        ('org', 'UPLOADED', 90)
        ])
    def test_campaignShardThrift_newSearchAudienceGroupByLabel(self, campaignType, audienceType, testPercentage):
        audienceSearchRequest = self.campaignShardObject.AudienceSearchRequest(
            searchText=constant.thiriftCampaignShardTestReferenceObject[campaignType]['campaign']['lists'][audienceType][0]['groupLabel'],
            audienceGroupTypes=[self.campaignShardObject.AudienceGroupType[audienceType]],
            testControl=self.campaignShardObject.TestControl(campaignType, testPercentage)
            )
        listOfAudienceGroup = self.connObj.newSearchAudienceGroupByLabel(audienceSearchRequest)
        CampaignShardHelper.validateGetAudienceGroupWithDataSourceInfo(campaignType, audienceType, listOfAudienceGroup[0], checkS3=False)
    
    @pytest.mark.parametrize('campaignType,audienceType,testPercentage', [
        ('org', ['FILTER_BASED', 'UPLOADED'], 90)
        ])
    def test_campaignShardThrift_newSearchAudienceGroupByLabel_multipleLists(self, campaignType, audienceType, testPercentage):
        audienceSearchRequest = self.campaignShardObject.AudienceSearchRequest(
            searchText=constant.thiriftCampaignShardTestReferenceObject[campaignType]['campaign']['lists'][audienceType[0]][0]['groupLabel'],
            audienceGroupTypes=[self.campaignShardObject.AudienceGroupType[audienceType[0]], self.campaignShardObject.AudienceGroupType[audienceType[1]]],
            testControl=self.campaignShardObject.TestControl(campaignType, testPercentage)
            )
        listOfAudienceGroup = self.connObj.newSearchAudienceGroupByLabel(audienceSearchRequest)
        CampaignShardHelper.validateGetAudienceGroupWithDataSourceInfo(campaignType, audienceType[0], listOfAudienceGroup[0], checkS3=False)
    
    @pytest.mark.parametrize('campaignType,audienceType', [
        ('org', 'FILTER_BASED'),
        ('skip', 'FILTER_BASED'),
        ('custom', 'FILTER_BASED')
        ])
    def test_campaignShardThrfit_getAudienceGroupWithDataSourceInfo_filter_zeroUsers(self, campaignType, audienceType):
        campaignId = constant.thiriftCampaignShardTestReferenceObject[campaignType.lower()]['campaign']['id']
        groupId = CampaignShardHelper.getGroupIdForFilterBasedListWithZeroRecords(campaignType,campaignId)['groupDetails']['id']
        
        Logger.log('Making getAudienceGroupWithDataSourceInfo Thrift Call for campaignType :{} , audienceType :{} with  groupId :{}'.format(campaignType, audienceType, groupId))
        AudienceGroup = self.connObj.getAudienceGroupWithDataSourceInfo(self.campaignShardObject.AudienceGroupDataSourceInfoRequest(groupId))
        CampaignShardHelper.validateGetAudienceGroupWithDataSourceInfo(campaignType, audienceType, AudienceGroup)
    