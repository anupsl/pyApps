import copy
import pytest
import time

from src.Constant.constant import constant
from src.modules.campaign_shard.campaignShardHelper import CampaignShardHelper
from src.modules.campaign_shard.campaignShardObject import campaignShardObject
from src.utilities.logger import Logger


@pytest.mark.run(order=3)
class Test_CampaignShard_Thrift_AudienceGroupManagerService():
    
    def setup_class(self):
        testControlTypeSupported = ['org', 'skip', 'custom']
        listSupported = ['filter', 'upload', 'duplicate', 'split', 'merge', 'dedup']
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
        ('org', 'UPLOADED'),
        ('org', 'SPLIT'),
        ('org', 'MERGE'),
        ('org', 'DUPLICATE'),
        ('org', 'DEDUP'),
        ('skip', 'UPLOADED'),
        ('skip', 'SPLIT'),
        ('skip', 'MERGE'),
        ('skip', 'DUPLICATE'),
        ('custom', 'UPLOADED'),
        ('custom', 'SPLIT'),
        ('custom', 'MERGE'),
        ('custom', 'DUPLICATE'),
        ('custom', 'DEDUP'),
        ])
    def test_campaignShardThrfit_getAudienceGroupWithDataSourceInfo(self, campaignType, audienceType):
        groupId = constant.thiriftCampaignShardTestReferenceObject[campaignType]['campaign']['lists'][audienceType][0]['groupDetails']['id']        
        Logger.log('Making getAudienceGroupWithDataSourceInfo Thrift Call for campaignType :{} , audienceType :{} with  groupId :{}'.format(campaignType, audienceType, groupId))
        AudienceGroup = self.connObj.getAudienceGroupWithDataSourceInfo(self.campaignShardObject.AudienceGroupDataSourceInfoRequest(groupId))
        CampaignShardHelper.validateGetAudienceGroupWithDataSourceInfo(campaignType, audienceType, AudienceGroup)
    
    @pytest.mark.parametrize('campaignType,audienceType', [
        ('org', 'UPLOADED'),
        ('org', 'SPLIT'),
        ('org', 'MERGE'),
        ('org', 'DUPLICATE'),
        ('org', 'DEDUP'),
        ('skip', 'UPLOADED'),
        ('skip', 'SPLIT'),
        ('skip', 'MERGE'),
        ('skip', 'DUPLICATE'),
        ('custom', 'UPLOADED'),
        ('custom', 'SPLIT'),
        ('custom', 'MERGE'),
        ('custom', 'DUPLICATE')
        ])
    def test_campaignShardThrfit_AudienceGroupUserInfoRequest_nonFilterBased(self, campaignType, audienceType):
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
