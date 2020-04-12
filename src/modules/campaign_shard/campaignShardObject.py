import time

from src.Constant.constant import constant
from src.initializer.generateThrift import campaignShard
from src.utilities.utils import Utils


class campaignShardObject(object):
    def __init__(self):
        self.CampaignGroupType = {'STICKY_GROUP': 1, 'LOYALTY': 2, 'CUSTOMER': 3, 'CAMPAIGN_USERS': 4, 'TEST_GROUP': 5,
                                  'NON_LOYALTY': 6, 'ALL': 7, 'UPLOAD': 8, 'FILTER_BASED': 9, 'DERIVED': 10}
        self.CampaignTargetType = {'ALL': 1, 'TEST': 2, 'CONTROL': 3, 'EXPERIMENT': 4}
        self.TestControlType = {'ORG': 1, 'CUSTOM': 2, 'SKIP': 3}
        self.UploadType = {'MOBILE': 1, 'EMAIL': 2, 'EXTERNALID': 3, 'USERID': 4}
        self.ListType = {'UPLOAD': 1, 'PASTE': 2, 'MERGE': 3, 'DEDUP': 4, 'SPLIT': 5, 'DUPLICATE': 6, 'FILTER': 7}
        self.AudienceGroupType = {'UPLOADED': 1, 'FILTER_BASED': 2, 'DERIVED': 3}
        self.DataSource = {'S3': 0}
        self.AudienceGroupStatus = {'PREPARE': 0, 'PROCESSING': 1, 'ACTIVE': 2, 'ERROR': 3}

    @staticmethod
    def TestControl(type, testPercentage):
        tmpDict = {
            'type': type,
            'testPercentage': testPercentage
        }
        csObj = campaignShardObject()
        tmpDict['type'] = csObj.TestControlType[tmpDict['type'].upper()]
        return campaignShard.TestControl(**tmpDict)

    @staticmethod
    def GroupIdNamePair(id, name):
        tmpDict = {
            'id': id,
            'name': name
        }
        return campaignShard.GroupIdNamePair(**tmpDict)

    @staticmethod
    def MergeListInfo(newGroupName, oldGroupIdList):
        tmpDict = {
            'newGroupName': newGroupName,
            'oldGroupIdList': oldGroupIdList
        }
        return campaignShard.MergeListInfo(**tmpDict)

    @staticmethod
    def DedupListInfo(createNewGroups, groupIdNameList):
        tmpDict = {
            'createNewGroups': createNewGroups,
            'groupIdNameList': groupIdNameList
        }
        return campaignShard.DedupListInfo(**tmpDict)

    @staticmethod
    def SplitListInfo(oldGroupId, splitGroupsList):
        tmpDict = {
            'oldGroupId': oldGroupId,
            'splitGroupsList': splitGroupsList
        }
        return campaignShard.SplitListInfo(**tmpDict)

    @staticmethod
    def DuplicateListInfo(oldGroupId, newGroupName):
        tmpDict = {
            'oldGroupId': oldGroupId,
            'newGroupName': newGroupName
        }
        return campaignShard.DuplicateListInfo(**tmpDict)

    @staticmethod
    def SplitGroup(newGroupName, percentage):
        tmpDict = {
            'newGroupName': newGroupName,
            'percentage': percentage
        }
        return campaignShard.SplitGroup(**tmpDict)

    @staticmethod
    def ListInfo(listType, listDetails):
        tmpDict = {
            'createdBy': int(time.time()),
        }
        if listType.lower() == 'merge':
            tmpDict['mergeListInfo'] = campaignShardObject.MergeListInfo(listDetails['newGroupName'],
                                                                         listDetails['oldGroupIdList'])
        if listType.lower() == 'dedup':
            tmpDict['dedupListInfo'] = campaignShardObject.DedupListInfo(listDetails['createNewGroups'],
                                                                         listDetails['groupIdNameList'])
        if listType.lower() == 'split':
            tmpDict['splitListInfo'] = campaignShardObject.SplitListInfo(listDetails['oldGroupId'],
                                                                         listDetails['splitGroupsList'])
        if listType.lower() == 'duplicate':
            tmpDict['duplicateListInfo'] = campaignShardObject.DuplicateListInfo(listDetails['oldGroupId'],
                                                                                 listDetails['newGroupName'])
        return campaignShard.ListInfo(**tmpDict)

    @staticmethod
    def CampaignGroup(messageDetails={}):
        tmpDict = {
            'id': int(time.time()),
            'orgId': constant.config['orgId'],
            'campaignId': None,
            'groupId': None,
            'groupLabel': str(),
            'params': str(),
            'campaignGroupType': 'CAMPAIGN_USERS',
            'campaignTargetType': 'TEST',
            'customerCount': 0,
            'isFavourite': True,
            'createdBy': None,
            'lastUpdatedBy': None,
            'createdDate': str(int(time.time())),
            'autoUpdateTime': str(int(time.time())),
        }
        tmpDict.update(messageDetails)
        csObj = campaignShardObject()
        tmpDict['campaignGroupType'] = csObj.CampaignGroupType[tmpDict['campaignGroupType']]
        tmpDict['campaignTargetType'] = csObj.CampaignTargetType[tmpDict['campaignTargetType']]
        return campaignShard.CampaignGroup(**tmpDict)

    @staticmethod
    def BucketDetails(messageDetails={}):
        tmpDict = {
            'groupID': None,
            'groupName': None,
            'dbHostName': None,
            'dbUsername': None,
            'dbPassword': None,
            'databaseName': None,
            'groupBucketName': None
        }
        tmpDict.update(messageDetails)
        return campaignShard.BucketDetails(**tmpDict)

    @staticmethod
    def HashLookup(messageDetails={}):
        tmpDict = {
            'id': 'ID_' + str(int(time.time())),
            'orgId': constant.config['orgId'],
            'lookupString': None
        }
        tmpDict.update(messageDetails)
        return campaignShard.HashLookup(**tmpDict)

    @staticmethod
    def AudienceGroupDataSourceInfoRequest(groupId, dataSource='S3', versionNumber=''):
        tmpDict = {
            'orgId': constant.config['orgId'],
            'groupId': int(groupId),
            'dataSource': dataSource
        }
        csObj = campaignShardObject()
        tmpDict['dataSource'] = csObj.DataSource[tmpDict['dataSource']]
        if versionNumber != '':
            tmpDict['versionNumber'] = versionNumber
        return campaignShard.AudienceGroupDataSourceInfoRequest(**tmpDict)

    @staticmethod
    def AudienceGroupUserInfoRequest(userId, groupId):
        tmpDict = {
            'orgId': constant.config['orgId'],
            'userId': userId,
            'groupId': groupId
        }
        return campaignShard.AudienceGroupUserInfoRequest(**tmpDict)

    @staticmethod
    def AudienceSearchRequest(searchText, audienceGroupTypes, testControl):
        tmpDict = {
            'searchText': searchText,
            'audienceGroupTypes': audienceGroupTypes,
            'testControl': testControl
        }
        return campaignShard.AudienceSearchRequest(**tmpDict)

    @staticmethod
    def createAudienceGroupRequest(requestParam={}, audienceType='FILTER_BASED'):
        csobj = campaignShardObject()
        tmpDict = {
            'orgId': constant.config['orgId'],
            'label': 'createGroupRecipient_{}'.format(int(time.time() * 1000)),
            'description': 'createGroupRecipient_Description_{}'.format(int(time.time() * 1000)),
            'type': csobj.CampaignGroupType[audienceType],
            'createdBy': int(constant.config['userId']),
            'requestId': Utils.generateGUID()
        }
        tmpDict.update(requestParam)
        return campaignShard.CreateAudienceRequest(**tmpDict)

    @staticmethod
    def createAudienceRequest(requestParam={}, audienceType='FILTER_BASED'):
        csobj = campaignShardObject()
        tmpDict = {
            'orgId': constant.config['orgId'],
            'label': 'createGroupRecipient_{}'.format(int(time.time() * 1000)),
            'description': 'createGroupRecipient_Description_{}'.format(int(time.time() * 1000)),
            'type': csobj.CampaignGroupType[audienceType],
            'createdBy': int(constant.config['userId']),
            'requestId': Utils.generateGUID()
        }
        if audienceType == 'FILTER_BASED':
            filterRequestDict = {'s3BucketTag': 'reon', 's3Headers': 'test_control_status,USER_ID'}
            filterRequestDict.update(constant.orgDetails[constant.config['cluster']][constant.config['orgId']]['s3'])
            filterRequestObj = {'filterRequest': campaignShard.FilterAudienceRequest(**filterRequestDict)}
            tmpDict.update(filterRequestObj)
        elif audienceType == 'UPLOAD':  # Still in Development & testcases not implemented
            tmpDict.update({'type': 0, 'identifiers': [], 's3BucketTag': 'reon', 'dataSource': 0})
        elif audienceType == 'DERIVED':  # Still in Development & testcases not implemented
            tmpDict.update({'includeGroups': 12, 'excludeGroups': 21})
        tmpDict.update(requestParam)
        return campaignShard.CreateAudienceRequest(**tmpDict)
