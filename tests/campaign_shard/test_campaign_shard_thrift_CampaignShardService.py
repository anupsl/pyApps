import copy
import pytest

from src.Constant.constant import constant
from src.modules.campaign_shard.campaignShardDBAssertion import CampaignShardDBAssertion
from src.modules.campaign_shard.campaignShardHelper import CampaignShardHelper
from src.modules.campaign_shard.campaignShardObject import campaignShardObject
from src.utilities.logger import Logger


@pytest.mark.run(order=2)
class Test_CampaignShard_Thrift_CampaignShardService():
    
    def setup_class(self):
        Logger.logSuiteName(str(self).split('.')[-1])
        testControlTypeSupported = ['org']
        listSupported = ['filter', 'upload']
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
        ('custom', 'FILTER_BASED'),
        ])
    def test_campaignShardThrift_reloadFilterBasedList(self, campaignType, audienceType):
        existingList = constant.thiriftCampaignShardTestReferenceObject[campaignType]['campaign']['lists'][audienceType][1] 
        userPayloadInfo = CampaignShardHelper.loyaltyUserDataConstructHelper()
        s3InfoForUsedList = CampaignShardHelper.getS3Info(existingList['uuid'])
        
        thriftCampaignGroup = lambda  campaignTargetType:self.campaignShardObject.CampaignGroup({
            'campaignId':constant.thiriftCampaignShardTestReferenceObject[campaignType]['campaign']['id'],
            'groupId':existingList['groupDetails']['id'],
            'groupLabel':existingList['groupLabel'],
            'params':str(),
            'campaignGroupType':'LOYALTY',
            'campaignTargetType':'TEST',
            'customerCount':existingList['groupVersionDetails'][campaignTargetType]['customer_count'],
            'uuId':existingList['uuid'],
            'versionNumber':1,
            's3Path':s3InfoForUsedList['response']['data']['s3Path'],
            's3Headers':s3InfoForUsedList['response']['data']['s3Header'],
            's3BucketTag':s3InfoForUsedList['response']['data']['s3Path'].split('/')[2]
            })
        
        for eachTargetType in ['TEST']:
            if  not self.connObj.reloadGroup(thriftCampaignGroup(eachTargetType)):
                Logger.log('For TargetType :{} , reload was unsuccesfull'.format(eachTargetType))
        
        CampaignShardDBAssertion(
            constant.thiriftCampaignShardTestReferenceObject[campaignType]['campaign']['id'],
            campaignType,
            'loyalty',
            existingList['groupLabel'],
            existingList['groupDetails']['id'],
            'firstName,lastName,mobile',
            userPayloadInfo
            ).check()
            
    @pytest.mark.parametrize('campaignType,audienceType,listType', [
        ('org', 'FILTER_BASED', 'DUPLICATE'),
        ('skip', 'FILTER_BASED', 'DUPLICATE'),
        ('custom', 'FILTER_BASED', 'DUPLICATE'),
        ])
    def test_campaignShardThrfit_duplicateList_filterBased(self, campaignType, audienceType, listType):
        existingList = constant.thiriftCampaignShardTestReferenceObject[campaignType]['campaign']['lists'][audienceType][0] 
        groupIdsOfListCreated = self.connObj.createList(
            constant.thiriftCampaignShardTestReferenceObject[campaignType]['campaign']['id'],
            self.campaignShardObject.ListType[listType],
            self.campaignShardObject.ListInfo(listType, {'oldGroupId':existingList['groupDetails']['id'], 'newGroupName':'duplicate_' + existingList['groupLabel']}))
        userPayloadInfo = CampaignShardHelper.loyaltyUserDataConstructHelper()
        CampaignShardDBAssertion(
            constant.thiriftCampaignShardTestReferenceObject[campaignType]['campaign']['id'],
            campaignType,
            'loyalty',
            'duplicate_' + existingList['groupLabel'],
            groupIdsOfListCreated[0],
            'firstName,lastName,mobile',
            userPayloadInfo,
            derived=True).check()
        
    @pytest.mark.parametrize('campaignType,audienceType,listType', [
        ('org', 'UPLOADED', 'DUPLICATE'),
        ('skip', 'UPLOADED', 'DUPLICATE'),
        ('custom', 'UPLOADED', 'DUPLICATE')
        ])
    def test_campaignShardThrfit_duplicateList_uploadBased(self, campaignType, audienceType, listType):
        existingList = constant.thiriftCampaignShardTestReferenceObject[campaignType]['campaign']['lists'][audienceType][0] 
        groupIdsOfListCreated = self.connObj.createList(
            constant.thiriftCampaignShardTestReferenceObject[campaignType]['campaign']['id'],
            self.campaignShardObject.ListType[listType],
            self.campaignShardObject.ListInfo(listType.lower(), {'oldGroupId':existingList['groupDetails']['id'], 'newGroupName':'duplicate_' + existingList['groupLabel']}))
        CampaignShardDBAssertion(
            constant.thiriftCampaignShardTestReferenceObject[campaignType]['campaign']['id'],
            campaignType,
            'upload',
            'duplicate_' + existingList['groupLabel'],
            groupIdsOfListCreated[0],
            existingList['addRecipientPayload']['schema'],
            existingList['addRecipientPayload']['data'],
            derived=True).check()    
    
    @pytest.mark.parametrize('campaignType,audienceType,listType', [
        ('org', 'UPLOADED', 'SPLIT'),
        ('skip', 'UPLOADED', 'SPLIT'),
        ('custom', 'UPLOADED', 'SPLIT')
        ])
    def test_campaignShardThrfit_splitList_uploadBased(self, campaignType, audienceType, listType):
        existingList = constant.thiriftCampaignShardTestReferenceObject[campaignType]['campaign']['lists'][audienceType][0] 
        splitA = self.campaignShardObject.SplitGroup('splitA_{}'.format(existingList['groupLabel']), 50)
        splitB = self.campaignShardObject.SplitGroup('splitB_{}'.format(existingList['groupLabel']), 50)
        listOfSplit = [splitA, splitB]
        userPayloadInfo = existingList['addRecipientPayload']['data']
        groupIdsOfListCreated = self.connObj.createList(
            constant.thiriftCampaignShardTestReferenceObject[campaignType]['campaign']['id'],
            self.campaignShardObject.ListType[listType],
            self.campaignShardObject.ListInfo(listType.lower(), {'oldGroupId':existingList['groupDetails']['id'], 'splitGroupsList':listOfSplit}))
        groupIndex = 0 
        for eachCreatedListData in CampaignShardHelper.splitListUsers(campaignType, userPayloadInfo):
            CampaignShardDBAssertion(
                constant.thiriftCampaignShardTestReferenceObject[campaignType]['campaign']['id'],
                campaignType,
                'upload',
                listOfSplit[groupIndex].newGroupName,
                groupIdsOfListCreated[groupIndex],
                'firstName,lastName,mobile',
                eachCreatedListData,
                derived=True).check()
            groupIndex = groupIndex + 1
    
    @pytest.mark.parametrize('campaignType,audienceType,listType', [
        ('org', 'FILTER_BASED', 'SPLIT'),
        ('skip', 'FILTER_BASED', 'SPLIT'),
        ('custom', 'FILTER_BASED', 'SPLIT')
        ])
    def test_campaignShardThrfit_splitList_filterBased(self, campaignType, audienceType, listType):
        existingList = constant.thiriftCampaignShardTestReferenceObject[campaignType]['campaign']['lists'][audienceType][0] 
        splitA = self.campaignShardObject.SplitGroup('splitA_{}'.format(existingList['groupLabel']), 50)
        splitB = self.campaignShardObject.SplitGroup('splitB_{}'.format(existingList['groupLabel']), 50)
        listOfSplit = [splitA, splitB]
        userPayloadInfo = CampaignShardHelper.loyaltyUserDataConstructHelper()
        groupIdsOfListCreated = self.connObj.createList(
            constant.thiriftCampaignShardTestReferenceObject[campaignType]['campaign']['id'],
            self.campaignShardObject.ListType[listType],
            self.campaignShardObject.ListInfo(listType.lower(), {'oldGroupId':existingList['groupDetails']['id'], 'splitGroupsList':listOfSplit}))
        groupIndex = 0
        for eachCreatedListData in CampaignShardHelper.splitListUsers(campaignType, userPayloadInfo):
            CampaignShardDBAssertion(
                constant.thiriftCampaignShardTestReferenceObject[campaignType]['campaign']['id'],
                campaignType,
                'loyalty',
                listOfSplit[groupIndex].newGroupName,
                groupIdsOfListCreated[groupIndex],
                'firstName,lastName,mobile',
                eachCreatedListData,
                derived=True).check()
            groupIndex = groupIndex + 1
    
    @pytest.mark.parametrize('campaignType,audienceTypeFirst,audienceTypeSecond,listType', [
        ('org', 'UPLOADED', 'UPLOADED', 'MERGE'),
        ('skip', 'UPLOADED', 'UPLOADED', 'MERGE'),
        ('custom', 'UPLOADED', 'UPLOADED', 'MERGE'),
        ])            
    def test_campaignShardThrift_mergeList_upload_uploadBased(self, campaignType, audienceTypeFirst, audienceTypeSecond, listType):
        existingListFirst = constant.thiriftCampaignShardTestReferenceObject[campaignType]['campaign']['lists'][audienceTypeFirst][0] 
        existingListSecond = constant.thiriftCampaignShardTestReferenceObject[campaignType]['campaign']['lists'][audienceTypeSecond][1] 
        groupIdsOfListCreated = self.connObj.createList(
            constant.thiriftCampaignShardTestReferenceObject[campaignType]['campaign']['id'],
            self.campaignShardObject.ListType[listType],
            self.campaignShardObject.ListInfo(listType.lower(), {'newGroupName':'Merge_' + existingListFirst['groupLabel'] + '_And_' + existingListSecond['groupLabel'], 'oldGroupIdList':[existingListFirst['groupDetails']['id'], existingListSecond['groupDetails']['id']]}))
        CampaignShardDBAssertion(
            constant.thiriftCampaignShardTestReferenceObject[campaignType]['campaign']['id'],
            campaignType,
            'upload',
            'Merge_' + existingListFirst['groupLabel'] + '_And_' + existingListSecond['groupLabel'],
            groupIdsOfListCreated[0],
            existingListFirst['addRecipientPayload']['schema'],
            existingListFirst['addRecipientPayload']['data'],
            derived=True).check() 
    
    @pytest.mark.parametrize('campaignType,audienceTypeFirst,audienceTypeSecond,listType', [
        ('org', 'UPLOADED', 'FILTER_BASED', 'MERGE'),
        ('skip', 'UPLOADED', 'FILTER_BASED', 'MERGE'),
        ('custom', 'UPLOADED', 'FILTER_BASED', 'MERGE')
        ])            
    def test_campaignShardThrift_mergeList_upload_filterBased(self, campaignType, audienceTypeFirst, audienceTypeSecond, listType):
        existingListFirst = constant.thiriftCampaignShardTestReferenceObject[campaignType]['campaign']['lists'][audienceTypeFirst][0] 
        existingListSecond = constant.thiriftCampaignShardTestReferenceObject[campaignType]['campaign']['lists'][audienceTypeSecond][0] 
        userPayloadInfo = CampaignShardHelper.loyaltyUserDataConstructHelper()
        groupIdsOfListCreated = self.connObj.createList(
            constant.thiriftCampaignShardTestReferenceObject[campaignType]['campaign']['id'],
            self.campaignShardObject.ListType[listType],
            self.campaignShardObject.ListInfo(listType.lower(), {'newGroupName':'Merge_' + existingListFirst['groupLabel'] + '_And_' + existingListSecond['groupLabel'], 'oldGroupIdList':[existingListFirst['groupDetails']['id'], existingListSecond['groupDetails']['id']]}))
        CampaignShardDBAssertion(
            constant.thiriftCampaignShardTestReferenceObject[campaignType]['campaign']['id'],
            campaignType,
            'upload',
            'Merge_' + existingListFirst['groupLabel'] + '_And_' + existingListSecond['groupLabel'],
            groupIdsOfListCreated[0],
            existingListFirst['addRecipientPayload']['schema'],
            list(set(existingListFirst['addRecipientPayload']['data'] + userPayloadInfo)),
            derived=True).check() 
    
    @pytest.mark.parametrize('campaignType,audienceTypeFirst,audienceTypeSecond,audienceTypeThird,listType', [
        ('org', 'UPLOADED', 'FILTER_BASED', 'FILTER_BASED', 'DEDUP'),
        #('skip', 'UPLOADED', 'FILTER_BASED', 'FILTER_BASED', 'DEDUP'),
        #('custom', 'UPLOADED', 'FILTER_BASED', 'FILTER_BASED' , 'DEDUP')
        ])        
    def test_campaignShardThrift_dedupList_multipleList_newList(self, campaignType, audienceTypeFirst, audienceTypeSecond, audienceTypeThird, listType):
        existingListFirst = constant.thiriftCampaignShardTestReferenceObject[campaignType]['campaign']['lists'][audienceTypeFirst][0] 
        existingListSecond = constant.thiriftCampaignShardTestReferenceObject[campaignType]['campaign']['lists'][audienceTypeSecond][0] 
        existingListThird = constant.thiriftCampaignShardTestReferenceObject[campaignType]['campaign']['lists'][audienceTypeThird][1] 
        userPayloadInfo = CampaignShardHelper.loyaltyUserDataConstructHelper()
        listOfGroupIdNamePair = [
            self.campaignShardObject.GroupIdNamePair(existingListFirst['groupDetails']['id'], existingListFirst['groupLabel']),
            self.campaignShardObject.GroupIdNamePair(existingListSecond['groupDetails']['id'], 'dedup_A_' + existingListSecond['groupLabel']),
            self.campaignShardObject.GroupIdNamePair(existingListThird['groupDetails']['id'], 'dedup_B_' + existingListThird['groupLabel'])
        ]
        
        groupIdsOfListCreated = self.connObj.createList(
            constant.thiriftCampaignShardTestReferenceObject[campaignType]['campaign']['id'],
            self.campaignShardObject.ListType[listType],
            self.campaignShardObject.ListInfo(listType.lower(), {'createNewGroups':True, 'groupIdNameList':listOfGroupIdNamePair}))
        
        CampaignShardDBAssertion(
            constant.thiriftCampaignShardTestReferenceObject[campaignType]['campaign']['id'],
            campaignType,
            'upload',
            'dedup_A_' + existingListSecond['groupLabel'],
            groupIdsOfListCreated[0],
            existingListFirst['addRecipientPayload']['schema'],
            list(set(userPayloadInfo) - set(existingListFirst['addRecipientPayload']['data'])),
            derived=True).check()
        CampaignShardDBAssertion(
            constant.thiriftCampaignShardTestReferenceObject[campaignType]['campaign']['id'],
            campaignType,
            'upload',
            'dedup_B_' + existingListThird['groupLabel'],
            groupIdsOfListCreated[1],
            existingListFirst['addRecipientPayload']['schema'],
            list(set(userPayloadInfo) - set(userPayloadInfo) - set(existingListFirst['addRecipientPayload']['data'])),
            derived=True).check()
    
    @pytest.mark.parametrize('campaignType,audienceTypeFirst,audienceTypeSecond,audienceTypeThird,listType', [
        ('org', 'UPLOADED', 'FILTER_BASED', 'FILTER_BASED', 'DEDUP'),
        ('skip', 'UPLOADED', 'FILTER_BASED', 'FILTER_BASED', 'DEDUP'),
        ('custom', 'UPLOADED', 'FILTER_BASED', 'FILTER_BASED' , 'DEDUP')
        ])        
    def test_campaignShardThrift_dedupList_multipleList_newVersion(self, campaignType, audienceTypeFirst, audienceTypeSecond, audienceTypeThird, listType):
        existingListFirst = constant.thiriftCampaignShardTestReferenceObject[campaignType]['campaign']['lists'][audienceTypeFirst][0] 
        existingListSecond = constant.thiriftCampaignShardTestReferenceObject[campaignType]['campaign']['lists'][audienceTypeSecond][0] 
        existingListThird = constant.thiriftCampaignShardTestReferenceObject[campaignType]['campaign']['lists'][audienceTypeThird][1] 
        userPayloadInfo = CampaignShardHelper.loyaltyUserDataConstructHelper()
        listOfGroupIdNamePair = [
            self.campaignShardObject.GroupIdNamePair(existingListFirst['groupDetails']['id'], existingListFirst['groupLabel']),
            self.campaignShardObject.GroupIdNamePair(existingListSecond['groupDetails']['id'], existingListSecond['groupLabel']),
            self.campaignShardObject.GroupIdNamePair(existingListThird['groupDetails']['id'], existingListThird['groupLabel'])
        ]
        
        groupIdsOfListCreated = self.connObj.createList(
            constant.thiriftCampaignShardTestReferenceObject[campaignType]['campaign']['id'],
            self.campaignShardObject.ListType[listType],
            self.campaignShardObject.ListInfo(listType.lower(), {'createNewGroups':False, 'groupIdNameList':listOfGroupIdNamePair}))
        
        CampaignShardDBAssertion(
            constant.thiriftCampaignShardTestReferenceObject[campaignType]['campaign']['id'],
            campaignType,
            'upload',
            existingListSecond['groupLabel'],
            groupIdsOfListCreated[0],
            existingListFirst['addRecipientPayload']['schema'],
            list(set(userPayloadInfo) - set(existingListFirst['addRecipientPayload']['data'])),
            derived=True).check()
        CampaignShardDBAssertion(
            constant.thiriftCampaignShardTestReferenceObject[campaignType]['campaign']['id'],
            campaignType,
            'upload',
            existingListThird['groupLabel'],
            groupIdsOfListCreated[1],
            existingListFirst['addRecipientPayload']['schema'],
            list(set(userPayloadInfo) - set(userPayloadInfo) - set(existingListFirst['addRecipientPayload']['data'])),
            derived=True).check()
    