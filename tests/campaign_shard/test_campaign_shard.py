import pytest, time , pytest_ordering
from src.Constant.constant import constant
from src.utilities.logger import Logger
from src.utilities.assertion import Assertion
from src.modules.iris.campaigns import campaigns
from src.modules.iris.list import campaignList
from src.modules.iris.dbCallsCampaign import dbCallsCampaign
from src.modules.iris.construct import construct
from src.modules.campaign_shard.campaignShardDBAssertion import CampaignShardDBAssertion
from src.modules.campaign_shard.campaignShardHelper import CampaignShardHelper

@pytest.mark.run(order=1)
class Test_CampaignShard():
    
    def setup_class(self):
        campaignResponse_ORG, campaignPayload_ORG = campaigns.createCampaign({'name':'IRIS_' + str(int(time.time() * 100000)), 'goalId':constant.irisGenericValues['goalId'], 'objectiveId':constant.irisGenericValues['objectiveId'], 'testControl':{'type' : 'ORG', 'test' : 90}})
        campaignResponse_SKIP, campaignPayload_SKIP = campaigns.createCampaign({'name':'IRIS_' + str(int(time.time() * 100000)), 'goalId':constant.irisGenericValues['goalId'], 'objectiveId':constant.irisGenericValues['objectiveId'], 'testControl':{'type' : 'SKIP', 'test' : 90}})
        campaignResponse_CUSTOM, campaignPayload_CUSTOM = campaigns.createCampaign({'name':'IRIS_' + str(int(time.time() * 100000)), 'goalId':constant.irisGenericValues['goalId'], 'objectiveId':constant.irisGenericValues['objectiveId'], 'testControl':{'type' : 'CUSTOM', 'test' : 90}})
        
        self.campaignId = {
            'ORG':campaignResponse_ORG['json']['entity']['campaignId'],
            'SKIP':campaignResponse_SKIP['json']['entity']['campaignId'],
            'CUSTOM':campaignResponse_CUSTOM['json']['entity']['campaignId']
        }
        
    def setup_method(self, method):
        Logger.logMethodName(str(method.__name__))
    
    @pytest.mark.parametrize('campaignType', [
        ('ORG')
        ])
    def test_campaignShard_loyalty_sanity(self, campaignType):
        detailsOfFilterListCreated = CampaignShardHelper.createFilterList(self.campaignId[campaignType], 'test_list_{}_{}'.format(campaignType, int(time.time())))
        userPayloadInfo = CampaignShardHelper.loyaltyUserDataConstructHelper()
        CampaignShardDBAssertion(self.campaignId[campaignType], campaignType, detailsOfFilterListCreated['listType'], detailsOfFilterListCreated['groupLabel'], detailsOfFilterListCreated['groupDetails']['id'], 'firstName,lastName,mobile', userPayloadInfo).check()
    
    @pytest.mark.parametrize('campaignType', [
        ('SKIP'),
        ('CUSTOM')
        ])
    def test_campaignShard_loyalty_generic(self, campaignType):
        detailsOfFilterListCreated = CampaignShardHelper.createFilterList(self.campaignId[campaignType], 'test_list_{}_{}'.format(campaignType, int(time.time())))
        userPayloadInfo = CampaignShardHelper.loyaltyUserDataConstructHelper()
        CampaignShardDBAssertion(self.campaignId[campaignType], campaignType, detailsOfFilterListCreated['listType'], detailsOfFilterListCreated['groupLabel'], detailsOfFilterListCreated['groupDetails']['id'], 'firstName,lastName,mobile', userPayloadInfo).check()
    
    @pytest.mark.parametrize('campaignType', [
        ('ORG')
        ])
    def est_campaignShard_nonLoyalty(self, campaignType):
        detailsOfFilterListCreated = CampaignShardHelper.createFilterList(self.campaignId[campaignType], 'test_list_{}_{}'.format(campaignType, int(time.time())), loyaltyType='non_loyalty')
        userPayloadInfo = CampaignShardHelper.loyaltyUserDataConstructHelper(loyaltyType='non_loyalty')
        CampaignShardDBAssertion(self.campaignId[campaignType], campaignType, detailsOfFilterListCreated['listType'], detailsOfFilterListCreated['groupLabel'], detailsOfFilterListCreated['groupDetails']['id'], 'firstName,lastName,mobile', userPayloadInfo).check()
        
    @pytest.mark.parametrize('campaignType', [
        ('SKIP'),
        ('CUSTOM')
        ])
    def est_campaignShard_nonLoyalty_generic(self, campaignType):
        detailsOfFilterListCreated = CampaignShardHelper.createFilterList(self.campaignId[campaignType], 'test_list_{}_{}'.format(campaignType, int(time.time())), loyaltyType='non_loyalty')
        userPayloadInfo = CampaignShardHelper.loyaltyUserDataConstructHelper(loyaltyType='non_loyalty')
        CampaignShardDBAssertion(self.campaignId[campaignType], campaignType, detailsOfFilterListCreated['listType'], detailsOfFilterListCreated['groupLabel'], detailsOfFilterListCreated['groupDetails']['id'], 'firstName,lastName,mobile', userPayloadInfo).check()
        
    @pytest.mark.parametrize('campaignType,userType,numberOfUsers,customTagCount', [
        ('ORG', 'mobile', 10, 0),
        ('SKIP', 'mobile', 10, 0),
        ('CUSTOM', 'mobile', 10, 0)
        ])
    def test_campaignShard_upload_paste_mobile_sanity(self, campaignType, userType, numberOfUsers, customTagCount):
        mergeListresponse, mergeListPayload, campaignId = campaignList.mergeList({}, campaignId=self.campaignId[campaignType], campaignType=['LIVE', campaignType, 'List', 'TAGS', 0], userType=userType, numberOfUsers=numberOfUsers, numberOfCustomTags=customTagCount, newUser=False)
        campaignList.assertMergeList(mergeListresponse, 200)
        CampaignShardDBAssertion(self.campaignId[campaignType], campaignType, 'upload', mergeListPayload['name'], mergeListresponse['json']['entity']['listId'], mergeListPayload['recipients']['schema'], mergeListPayload['recipients']['data'], numberOfCustomTags=customTagCount, numberOfGroupTags=0).check()
        
    @pytest.mark.parametrize('campaignType,userType,numberOfUsers,customTagCount', [
        ('ORG', 'email', 10, 0),
        ('SKIP', 'email', 10, 0),
        ('CUSTOM', 'email', 10, 0)
        ])    
    def test_campaignShard_upload_paste_email_sanity(self, campaignType, userType, numberOfUsers, customTagCount):
        mergeListresponse, mergeListPayload, campaignId = campaignList.mergeList({}, campaignId=self.campaignId[campaignType], campaignType=['LIVE', campaignType, 'List', 'TAGS', 0], userType=userType, numberOfUsers=numberOfUsers, numberOfCustomTags=customTagCount, newUser=False)
        campaignList.assertMergeList(mergeListresponse, 200)
        CampaignShardDBAssertion(self.campaignId[campaignType], campaignType, 'upload', mergeListPayload['name'], mergeListresponse['json']['entity']['listId'], mergeListPayload['recipients']['schema'], mergeListPayload['recipients']['data'], numberOfCustomTags=customTagCount, numberOfGroupTags=0).check()
        
    @pytest.mark.parametrize('campaignType,userType,numberOfUsers,customTagCount', [
        ('ORG', 'userId', 10, 0),
        ('SKIP', 'userId', 10, 0),
        ('CUSTOM', 'userId', 10, 0)
        ]) 
    def test_campaignShard_upload_paste_userId(self, campaignType, userType, numberOfUsers, customTagCount):
        mergeListresponse, mergeListPayload, campaignId = campaignList.mergeList({}, campaignId=self.campaignId[campaignType], campaignType=['LIVE', campaignType, 'List', 'TAGS', 0], userType=userType, numberOfUsers=numberOfUsers, numberOfCustomTags=customTagCount, newUser=False)
        campaignList.assertMergeList(mergeListresponse, 200)
        CampaignShardDBAssertion(self.campaignId[campaignType], campaignType, 'upload', mergeListPayload['name'], mergeListresponse['json']['entity']['listId'], mergeListPayload['recipients']['schema'], mergeListPayload['recipients']['data'], numberOfCustomTags=customTagCount, numberOfGroupTags=0).check()
        
    @pytest.mark.parametrize('campaignType,userType,numberOfUsers,customTagCount', [
        ('ORG', 'externalId', 10, 0),
        ('SKIP', 'externalId', 10, 0),
        ('CUSTOM', 'externalId', 10, 0)
        ])
    def test_campaignShard_upload_paste_externalId(self, campaignType, userType, numberOfUsers, customTagCount):
        mergeListresponse, mergeListPayload, campaignId = campaignList.mergeList({}, campaignId=self.campaignId[campaignType], campaignType=['LIVE', campaignType, 'List', 'TAGS', 0], userType=userType, numberOfUsers=numberOfUsers, numberOfCustomTags=customTagCount, newUser=False)
        campaignList.assertMergeList(mergeListresponse, 200)
        CampaignShardDBAssertion(self.campaignId[campaignType], campaignType, 'upload', mergeListPayload['name'], mergeListresponse['json']['entity']['listId'], mergeListPayload['recipients']['schema'], mergeListPayload['recipients']['data'], numberOfCustomTags=customTagCount, numberOfGroupTags=0).check()
        
    @pytest.mark.parametrize('campaignType,userType,numberOfUsers,customTagCount', [
        ('ORG', 'mobile,email', 10, 0),
        ('SKIP', 'mobile,email', 10, 0),
        ('CUSTOM', 'mobile,email', 10, 0)
        ])
    def test_campaignShard_upload_paste_mobile_email(self, campaignType, userType, numberOfUsers, customTagCount):
        mergeListresponse, mergeListPayload, campaignId = campaignList.mergeList({}, campaignId=self.campaignId[campaignType], campaignType=['LIVE', campaignType, 'List', 'TAGS', 0], userType=userType, numberOfUsers=numberOfUsers, numberOfCustomTags=customTagCount, newUser=False)
        campaignList.assertMergeList(mergeListresponse, 200)
        CampaignShardDBAssertion(self.campaignId[campaignType], campaignType, 'upload', mergeListPayload['name'], mergeListresponse['json']['entity']['listId'], mergeListPayload['recipients']['schema'], mergeListPayload['recipients']['data'], numberOfCustomTags=customTagCount, numberOfGroupTags=0).check()
        
    @pytest.mark.parametrize('campaignType,userType,numberOfUsers,customTagCount', [
        ('ORG', 'userId,externalId', 10, 0),
        ('SKIP', 'userId,externalId', 10, 0),
        ('CUSTOM', 'userId,externalId', 10, 0)
        ])
    def test_campaignShard_upload_paste_userId_externalId(self, campaignType, userType, numberOfUsers, customTagCount):
        mergeListresponse, mergeListPayload, campaignId = campaignList.mergeList({}, campaignId=self.campaignId[campaignType], campaignType=['LIVE', campaignType, 'List', 'TAGS', 0], userType=userType, numberOfUsers=numberOfUsers, numberOfCustomTags=customTagCount, newUser=False)
        campaignList.assertMergeList(mergeListresponse, 200)
        CampaignShardDBAssertion(self.campaignId[campaignType], campaignType, 'upload', mergeListPayload['name'], mergeListresponse['json']['entity']['listId'], mergeListPayload['recipients']['schema'], mergeListPayload['recipients']['data'], numberOfCustomTags=customTagCount, numberOfGroupTags=0).check()
        
    @pytest.mark.parametrize('campaignType,userType,numberOfUsers,customTagCount', [
        ('ORG', 'mobile,email,userId,externalId', 10, 0),
        ('SKIP', 'mobile,email,userId,externalId', 10, 0),
        ('CUSTOM', 'mobile,email,userId,externalId', 10, 0)
        ])
    def test_campaignShard_upload_paste_mobile_email_userId_externalId(self, campaignType, userType, numberOfUsers, customTagCount):
        mergeListresponse, mergeListPayload, campaignId = campaignList.mergeList({}, campaignId=self.campaignId[campaignType], campaignType=['LIVE', campaignType, 'List', 'TAGS', 0], userType=userType, numberOfUsers=numberOfUsers, numberOfCustomTags=customTagCount, newUser=False)
        campaignList.assertMergeList(mergeListresponse, 200)
        CampaignShardDBAssertion(self.campaignId[campaignType], campaignType, 'upload', mergeListPayload['name'], mergeListresponse['json']['entity']['listId'], mergeListPayload['recipients']['schema'], mergeListPayload['recipients']['data'], numberOfCustomTags=customTagCount, numberOfGroupTags=0).check()
        
    @pytest.mark.parametrize('campaignType,userType,numberOfUsers,customTagCount', [
        ('ORG', 'mobile', 10, 5),
        ('SKIP', 'mobile', 10, 5),
        ('CUSTOM', 'mobile', 10, 5)
        ])
    def test_campaignShard_upload_paste_mobile_customTag(self, campaignType, userType, numberOfUsers, customTagCount):
        mergeListresponse, mergeListPayload, campaignId = campaignList.mergeList({}, campaignId=self.campaignId[campaignType], campaignType=['LIVE', campaignType, 'List', 'TAGS', 0], userType=userType, numberOfUsers=numberOfUsers, numberOfCustomTags=customTagCount, newUser=False)
        campaignList.assertMergeList(mergeListresponse, 200)
        CampaignShardDBAssertion(self.campaignId[campaignType], campaignType, 'upload', mergeListPayload['name'], mergeListresponse['json']['entity']['listId'], mergeListPayload['recipients']['schema'], mergeListPayload['recipients']['data'], numberOfCustomTags=customTagCount, numberOfGroupTags=0).check()
        
    @pytest.mark.parametrize('campaignType,userType,numberOfUsers,customTagCount', [
        ('ORG', 'email', 10, 5),
        ('SKIP', 'email', 10, 5),
        ('CUSTOM', 'email', 10, 5)
        ])
    def test_campaignShard_upload_paste_email_customTag(self, campaignType, userType, numberOfUsers, customTagCount):
        mergeListresponse, mergeListPayload, campaignId = campaignList.mergeList({}, campaignId=self.campaignId[campaignType], campaignType=['LIVE', campaignType, 'List', 'TAGS', 0], userType=userType, numberOfUsers=numberOfUsers, numberOfCustomTags=customTagCount, newUser=False)
        campaignList.assertMergeList(mergeListresponse, 200)
        CampaignShardDBAssertion(self.campaignId[campaignType], campaignType, 'upload', mergeListPayload['name'], mergeListresponse['json']['entity']['listId'], mergeListPayload['recipients']['schema'], mergeListPayload['recipients']['data'], numberOfCustomTags=customTagCount, numberOfGroupTags=0).check()
        
    @pytest.mark.parametrize('campaignType,userType,numberOfUsers,groupTags', [
        ('ORG', 'mobile', 10, ['group1', 'group2', 'group3']),
        ('SKIP', 'mobile', 10, ['group1', 'group2', 'group3']),
        ('CUSTOM', 'mobile', 10, ['group1', 'group2', 'group3'])
        ])
    def test_campaignShard_upload_paste_mobile_groupTags(self, campaignType, userType, numberOfUsers, groupTags):
        createListresponse, createListPayload, campaignId = campaignList.createList({'groupTags':groupTags, 'name':'CAMPAIGNSHARD_LIST_' + str(int(time.time() * 100000))}, campaignId=self.campaignId[campaignType])
        if createListresponse['statusCode'] != 200 : Assertion.constructAssertion(False, 'Not Able To Create List')
        addRecipientResponse, addRecipientPayload = campaignList.addRecipient({}, campaignId, createListresponse['json']['entity']['listId'], str(userType), int(numberOfUsers), 0, newUser=False)
        if addRecipientResponse['statusCode'] != 200 : Assertion.constructAssertion(False, 'Not Able To Add Recipient')
        CampaignShardDBAssertion(self.campaignId[campaignType], campaignType, 'upload', createListPayload['name'], createListresponse['json']['entity']['listId'], addRecipientPayload['schema'], addRecipientPayload['data'], numberOfCustomTags=0, numberOfGroupTags=len(groupTags)).check()
