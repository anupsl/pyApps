import copy
import pytest

from src.Constant.constant import constant
from src.modules.campaign_shard.campaignShardDBAssertion import CampaignShardDBAssertion
from src.modules.campaign_shard.campaignShardHelper import CampaignShardHelper
from src.modules.campaign_shard.campaignShardObject import campaignShardObject
from src.utilities.logger import Logger


@pytest.mark.skipif(True, reason='Bucket Update Cases')
@pytest.mark.run(order=5)
class Test_CampaignShard_Thrift_CampaignShardService_bucketUpdate():
    def setup_class(self):
        Logger.logSuiteName(str(self).split('.')[-1])
        testControlTypeSupported = ['org', 'skip', 'custom']
        listSupported = ['filter']
        self.campaignShardObject = campaignShardObject()
        self.intialUsedObject = copy.deepcopy(constant.thiriftCampaignShardTestReferenceObject)
        CampaignShardHelper.setupCampaignsInThriftReference(typesOfCampaign=testControlTypeSupported)
        CampaignShardHelper.setupListInThriftReference(listSupported, typesOfCampaign=testControlTypeSupported)
        self.bucketDetails = CampaignShardHelper.updateBucketIdRowCount()

    def teardown_class(self):
        constant.thiriftCampaignShardTestReferenceObject = copy.deepcopy(self.intialUsedObject)

    def setup_method(self, method):
        self.connObj = CampaignShardHelper.getConnObj(newConnection=True)
        Logger.logMethodName(method.__name__)

    @pytest.mark.parametrize('campaignType,audienceType', [
        ('org', 'FILTER_BASED'),
        ('skip', 'FILTER_BASED'),
        ('custom', 'FILTER_BASED'),
    ])
    def test_campaignShardThrift_reloadFilterBasedList_newBucket(self, campaignType, audienceType):
        existingList = \
        constant.thiriftCampaignShardTestReferenceObject[campaignType]['campaign']['lists'][audienceType][0]
        userPayloadInfo = CampaignShardHelper.loyaltyUserDataConstructHelper()
        s3InfoForUsedList = CampaignShardHelper.getS3Info(existingList['uuid'])

        thriftCampaignGroup = lambda campaignTargetType: self.campaignShardObject.CampaignGroup({
            'campaignId': constant.thiriftCampaignShardTestReferenceObject[campaignType]['campaign']['id'],
            'groupId': existingList['groupDetails']['id'],
            'groupLabel': existingList['groupLabel'],
            'params': str(),
            'campaignGroupType': 'LOYALTY',
            'campaignTargetType': 'TEST',
            'customerCount': existingList['groupVersionDetails'][campaignTargetType]['customer_count'],
            'uuId': existingList['uuid'],
            'versionNumber': 1,
            's3Path': s3InfoForUsedList['response']['data']['s3Path'],
            's3Headers': s3InfoForUsedList['response']['data']['s3Header'],
            's3BucketTag': s3InfoForUsedList['response']['data']['s3Path'].split('/')[2]
        })

        for eachTargetType in ['TEST']:
            if not self.connObj.reloadGroup(thriftCampaignGroup(eachTargetType)):
                Logger.log('For TargetType :{} , reload was unsuccesfull'.format(eachTargetType))

        CampaignShardHelper.validateBucketIdWhenBucketUpdated(existingList['groupDetails']['id'],
                                                              self.bucketDetails['newBucket'])
        CampaignShardDBAssertion(
            constant.thiriftCampaignShardTestReferenceObject[campaignType]['campaign']['id'],
            campaignType,
            'loyalty',
            existingList['groupLabel'],
            existingList['groupDetails']['id'],
            'firstName,lastName,mobile',
            userPayloadInfo
        ).check()

    @pytest.mark.parametrize('campaignType,audienceType', [
        ('org', 'FILTER_BASED'),
        ('skip', 'FILTER_BASED'),
        ('custom', 'FILTER_BASED'),
    ])
    def test_campaignShardThrift_reloadFilterBasedList_newBucket_partiallyDistributedBucket(self, campaignType,
                                                                                            audienceType):
        self.bucketDetails = CampaignShardHelper.updateBucketIdRowCount(rows_count=14999990)
        existingList = constant.thiriftCampaignShardTestReferenceObject[campaignType]['campaign']['lists'][audienceType][1]
        userPayloadInfo = CampaignShardHelper.loyaltyUserDataConstructHelper()
        s3InfoForUsedList = CampaignShardHelper.getS3Info(existingList['uuid'])

        thriftCampaignGroup = lambda campaignTargetType: self.campaignShardObject.CampaignGroup({
            'campaignId': constant.thiriftCampaignShardTestReferenceObject[campaignType]['campaign']['id'],
            'groupId': existingList['groupDetails']['id'],
            'groupLabel': existingList['groupLabel'],
            'params': str(),
            'campaignGroupType': 'LOYALTY',
            'campaignTargetType': 'TEST',
            'customerCount': existingList['groupVersionDetails'][campaignTargetType]['customer_count'],
            'uuId': existingList['uuid'],
            'versionNumber': 1,
            's3Path': s3InfoForUsedList['response']['data']['s3Path'],
            's3Headers': s3InfoForUsedList['response']['data']['s3Header'],
            's3BucketTag': s3InfoForUsedList['response']['data']['s3Path'].split('/')[2]
        })

        for eachTargetType in ['TEST']:
            if not self.connObj.reloadGroup(thriftCampaignGroup(eachTargetType)):
                Logger.log('For TargetType :{} , reload was unsuccesfull'.format(eachTargetType))

        CampaignShardHelper.validateBucketIdWhenBucketUpdated(existingList['groupDetails']['id'],
                                                              self.bucketDetails['oldBucket'])

        CampaignShardDBAssertion(
            constant.thiriftCampaignShardTestReferenceObject[campaignType]['campaign']['id'],
            campaignType,
            'loyalty',
            existingList['groupLabel'],
            existingList['groupDetails']['id'],
            'firstName,lastName,mobile',
            userPayloadInfo
        ).check()
