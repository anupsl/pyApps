import pytest

from src.modules.campaign_shard.campaignShardHelper import CampaignShardHelper
from src.modules.campaign_shard.campaignShardObject import campaignShardObject
from src.modules.campaign_shard.campaignShardDBAssertion import CampaignShardDBAssertion
from src.utilities.logger import Logger
from src.modules.iris.dbCallsList import dbCallsList
import time

@pytest.mark.run(order=6)
class Test_CampaignShard_Thrift_AudienceGroupManagerService_Async_GroupCall():
    def setup_method(self, method):
        self.connObj = CampaignShardHelper.getConnObj(newConnection=True)
        Logger.logMethodName(method.__name__)

    @pytest.mark.parametrize('audienceType', [
        ('FILTER_BASED')
    ])
    def test_campaignShardThrift_AudienceGroup_Async_CreateAudienceGroup_Sanity(self, audienceType):
        createAudienceRequest = campaignShardObject.createAudienceRequest(audienceType=audienceType)
        audiencecGroupEntity = self.connObj.createAudienceGroup(createAudienceRequest).__dict__
        CampaignShardHelper.validateGroupStatusAsync(audiencecGroupEntity, 'PREPARE', audienceType)

    @pytest.mark.parametrize('audienceType', [
        ('FILTER_BASED')
    ])
    def test_campaignShardThrift_AudienceGroup_Async_CreateAudience_Sanity(self, audienceType):
        createAudienceRequest = campaignShardObject.createAudienceRequest(audienceType=audienceType)
        audiencecGroupEntity = self.connObj.createAudienceGroup(createAudienceRequest).__dict__
        createAudienceWithGroupId = campaignShardObject.createAudienceRequest({'groupId': audiencecGroupEntity['id']},
                                                                          audienceType=audienceType)
        time.sleep(20)
        createAudienceResponse = self.connObj.createAudience(createAudienceWithGroupId).__dict__
        userPayloadInfo = CampaignShardHelper.loyaltyUserDataConstructHelper()
        CampaignShardDBAssertion(99999, 'org', audienceType,
                                 createAudienceResponse['label'],
                                 audiencecGroupEntity['id'], 'firstName,lastName,mobile',
                                 userPayloadInfo,newFlow=True).check()

    @pytest.mark.parametrize('audienceType', [
        ('FILTER_BASED')
    ])
    def test_campaignShardThrift_AudienceGroup_Async_CreateAudience_markError_Sanity(self, audienceType):
        createAudienceRequest = campaignShardObject.createAudienceRequest(audienceType=audienceType)
        audiencecGroupEntity = self.connObj.createAudienceGroup(createAudienceRequest).__dict__
        createAudienceWithGroupId = campaignShardObject.createAudienceRequest({'groupId': audiencecGroupEntity['id']},
                                                                              audienceType=audienceType)
        self.connObj.createAudience(createAudienceWithGroupId)
        self.connObj.updateErrorStatusForAudienceGroup(audiencecGroupEntity['id'])
        CampaignShardHelper.validateErrorStatusAsync(audiencecGroupEntity['id'])

    @pytest.mark.parametrize('audienceType', [
        ('FILTER_BASED')
    ])
    def test_campaignShardThrift_AudienceGroup_Async_CreateAudience_Reload_Sanity(self, audienceType):
        createAudienceRequest = campaignShardObject.createAudienceRequest(audienceType=audienceType)
        audiencecGroupEntity = self.connObj.createAudienceGroup(createAudienceRequest).__dict__
        createAudienceWithGroupId = campaignShardObject.createAudienceRequest({'groupId': audiencecGroupEntity['id']},
                                                                              audienceType=audienceType)
        createAudienceResponse =self.connObj.createAudience(createAudienceWithGroupId).__dict__

        groupDetailsVersionInfo = dbCallsList.getGroupVersionDetailsWithGroupId(audiencecGroupEntity['id'])
        s3InfoForUsedList = CampaignShardHelper.getS3Info(createAudienceResponse['uuId'])
        thriftCampaignGroup = lambda campaignTargetType: campaignShardObject().CampaignGroup({
            'groupId': audiencecGroupEntity['id'],
            'groupLabel': createAudienceResponse['label'],
            'params': str(),
            'campaignGroupType': 'FILTER_BASED',
            'campaignTargetType': 'TEST',
            'customerCount': groupDetailsVersionInfo['TEST']['customer_count'],
            'uuId': createAudienceResponse['uuId'],
            'versionNumber': 1,
            's3Path': s3InfoForUsedList['response']['data']['s3Path'],
            's3Headers': s3InfoForUsedList['response']['data']['s3Header'],
            's3BucketTag': s3InfoForUsedList['response']['data']['s3Path'].split('/')[2]
        })

        for eachTargetType in ['TEST']:
            if not self.connObj.reloadGroup(thriftCampaignGroup(eachTargetType)):
                Logger.log('For TargetType :{} , reload was unsuccesfull'.format(eachTargetType))
        userPayloadInfo = CampaignShardHelper.loyaltyUserDataConstructHelper()
        CampaignShardDBAssertion(
            99999,
            'org',
            'FILTER_BASED',
            createAudienceResponse['label'],
            audiencecGroupEntity['id'], 'firstName,lastName,mobile',
            userPayloadInfo, newFlow=True
        ).check()





