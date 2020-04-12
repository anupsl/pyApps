import time

from src.Constant.constant import constant
from src.modules.campaign_shard.campaignShardObject import campaignShardObject
from src.modules.campaign_shard.campaignShardThrift import CampaignShardThrift
from src.modules.iris.campaigns import campaigns
from src.modules.iris.construct import construct
from src.modules.iris.dbCallsList import dbCallsList
from src.modules.iris.dbCallsMessage import dbCallsMessage
from src.modules.iris.list import campaignList
from src.utilities.assertion import Assertion
from src.utilities.awsHelper import AWSHelper
from src.utilities.logger import Logger
from src.utilities.utils import Utils


class CampaignShardHelper():
    @staticmethod
    def checkCampaignShardConnection(ignoreConnectionError=False):
        Utils.checkServerConnection('CAMPAIGN_SHARD_THRIFT_SERVICE', CampaignShardThrift, 'campaignShardPort',
                                    ignoreConnectionError)

    @staticmethod
    def getConnObj(newConnection=False):
        port = constant.config['campaignShardPort'].next()
        connPort = str(port) + '_obj'
        if connPort in constant.config:
            if newConnection:
                constant.config[connPort].close()
                constant.config[connPort] = CampaignShardThrift(port)
            return constant.config[connPort]
        else:
            return CampaignShardThrift(port)

    @staticmethod
    def constructHeader():
        return {'accept': 'application/json',
                'X-CAP-API-AUTH-ORG-ID': str(constant.config['orgId']),
                'Content-Type': 'application/json',
                'Authorization': 'Bearer {}'.format(constant.config['token'])}

    @staticmethod
    def constructPayload(campaignId, listName='', loyaltyType='loyalty'):
        payloadReference = constant.filterV2Json
        if listName == '':
            payloadReference.update({'campaignId': campaignId})
            payloadReference['targetBlock'][0]['loyalty']['values'] = [loyaltyType]
        else:
            payloadReference.update({'filterName': listName, 'campaignId': campaignId})
            payloadReference['targetBlock'][0]['loyalty']['values'] = [loyaltyType]
        return payloadReference

    @staticmethod
    def constructFilterPayloadForZeroData(campaignId, listName, loyaltyType='loyalty'):
        payloadReference = constant.filterV2Json
        payloadReference.update({'filterName': listName, 'campaignId': campaignId})
        payloadReference['targetBlock'][0]['loyalty']['values'] = [loyaltyType]
        payloadReference['targetBlock'][0]['blocks'][0]['filters'][0]['entities']['kpis'][1]['values'] = [
            "noUserWithSuchName"]
        return payloadReference

    @staticmethod
    def validateFilterResponse(response, campaignId=None):
        if response != None:  # To handling timeout exception
            responseJson = response.json()
            if response.status_code >= 200 and response.status_code <= 300 and responseJson['status'][
                'message'] == 'success' and 'failure' not in responseJson['response']['callBackUrl']:
                filterData = CampaignShardHelper.constructFilterData({
                    'groupLabel': responseJson['response']['filterName'],
                    'uuid': responseJson['response']['_id'],
                    'listType': 'loyalty'
                })
                if filterData['groupVersionDetails']['TEST']['customer_count'] == 0:
                    return CampaignShardHelper.createFilterListWithCreateGroupRecipient()
                else:
                    if 's3Path' in responseJson['response']:
                        data = {
                            "path": responseJson['response']['s3Path'],
                            "bucket": responseJson['response']['s3Path'].split("/")[2],
                            "uuid": responseJson['response']['_id']
                        }
                        CampaignShardHelper.savetestData('s3Info', data)
                    return filterData
            else:
                return CampaignShardHelper.createFilterListWithCreateGroupRecipient()
        else:
            return CampaignShardHelper.createFilterListWithCreateGroupRecipient()

    @staticmethod
    def createFilterListWithCreateGroupRecipient():
        try:
            groupLabel = 'createGroupRecipient_{}'.format(int(time.time() * 1000))
            uuid = constant.orgDetails[constant.config['cluster']][constant.config['orgId']]['s3']['uuid']

            createAudienceRequestObj = campaignShardObject.createAudienceRequest({'label': groupLabel})
            connObj = CampaignShardHelper.getConnObj(newConnection=True)
            connObj.createAudience(createAudienceRequestObj)

            return CampaignShardHelper.constructFilterData({
                'groupLabel': groupLabel,
                'uuid': uuid,
                'listType': 'filter_based'
            })
        except Exception, exp:
            raise Exception(
                'Filter From NFS Failed and even CreateGroupRecipient Failed with Exception :{}'.format(exp))

    @staticmethod
    def constructFilterData(data):
        data.update({'groupDetails': dbCallsList.getGroupDetailsWithListName(data['groupLabel'], data['uuid'])})
        data.update({'groupVersionDetails': dbCallsList.getGroupVersionDetailsWithGroupId(data['groupDetails']['id'])})
        camapignGroupRecipientsData = {
            'TEST': dbCallsList.getAllUsersFromCampaignGroupRecipient(data['groupVersionDetails']['TEST']['bucket_id'],
                                                                      data['groupVersionDetails']['TEST']['id'])}
        if 'CONTROL' in data['groupVersionDetails']: camapignGroupRecipientsData.update({
            'CONTROL': dbCallsList.getAllUsersFromCampaignGroupRecipient(
                data[
                    'groupVersionDetails'][
                    'CONTROL'][
                    'bucket_id'], data[
                    'groupVersionDetails'][
                    'CONTROL']['id'])})
        data.update({'campaignGroupRecipients': camapignGroupRecipientsData})
        Logger.log('Constructed Filter Data , Returned Finally To Test Class :{}'.format(data))
        return data

    @staticmethod
    def createFilterList(campaignId, listName, loyaltyType='loyalty'):
        response = None
        try:
            endPoint = construct.constructUrl('filterlist', module='arya').format(str(int(time.time())))
            response = Utils.makeRequest(endPoint,
                                         CampaignShardHelper.constructPayload(campaignId, listName, loyaltyType),
                                         CampaignShardHelper.constructHeader(), 'POST', timeout=300)
        except Exception, exp:
            Logger.log("Exception Occured while Creating Filter List :{}".format(exp))
        return CampaignShardHelper.validateFilterResponse(response, campaignId)

    @staticmethod
    def savetestData(module, value):
        endPoint = 'http://apitester.capillary.in/apitest_app/testData'
        data = {
            'orgId': constant.config['orgId'],
            'cluster': constant.config['cluster'],
            'module': module,
            'value': value
        }
        response = Utils.makeRequest(url=endPoint, headers='', body=data, method='POST')
        return response['message']

    @staticmethod
    def gettestData(module):
        endPoint = 'http://apitester.capillary.in/apitest_app/testData?module={}&cluster={}&orgId={}'.format(module,
                                                                                                             constant.config[
                                                                                                                 'cluster'],
                                                                                                             constant.config[
                                                                                                                 'orgId'])
        response = Utils.makeRequest(url=endPoint, headers='', body='', method='GET')
        return response['message']

    @staticmethod
    def getGroupIdForFilterBasedListWithZeroRecords(campaignType, campaignId,
                                                    listName='ZeroDataCreatedLlist' + str(time.time()),
                                                    loyaltyType='loyalty'):
        try:
            endPoint = construct.constructUrl('filterlist', module='arya').format(str(int(time.time())))
            response = Utils.makeRequest(endPoint,
                                         CampaignShardHelper.constructFilterPayloadForZeroData(campaignId, listName,
                                                                                               loyaltyType),
                                         CampaignShardHelper.constructHeader(), 'POST', timeout=120)
        except Exception, exp:
            Logger.log("Exception Occured while Creating Filter List :{}".format(exp))
        filterResponse = CampaignShardHelper.validateFilterResponse(response)
        constant.thiriftCampaignShardTestReferenceObject[campaignType.lower()]['campaign']['lists'][
            'FILTER_BASED'].insert(0,
                                   filterResponse)
        return filterResponse

    @staticmethod
    def getS3Info(uuid):
        endPoint = construct.constructUrl('s3info', module='arya').format(uuid)
        response = Utils.makeRequest(endPoint, '', CampaignShardHelper.constructHeader(), 'GET', timeout=120)
        return response.json()

    @staticmethod
    def setupCampaignsInThriftReference(typesOfCampaign=['org', 'custom', 'skip']):
        if 'org' in typesOfCampaign:
            campaignResponse_ORG, campaignPayload_ORG = campaigns.createCampaign(
                {'name': 'CampaignShard_' + str(int(time.time() * 100000)),
                 'goalId': constant.irisGenericValues['goalId'],
                 'objectiveId': constant.irisGenericValues['objectiveId'], 'testControl': {'type': 'ORG', 'test': 90}})
            constant.thiriftCampaignShardTestReferenceObject['org']['campaign']['name'] = campaignPayload_ORG['name']
            constant.thiriftCampaignShardTestReferenceObject['org']['campaign']['id'] = \
                campaignResponse_ORG['json']['entity']['campaignId']
        if 'skip' in typesOfCampaign:
            campaignResponse_SKIP, campaignPayload_SKIP = campaigns.createCampaign(
                {'name': 'CampaignShard_' + str(int(time.time() * 100000)),
                 'goalId': constant.irisGenericValues['goalId'],
                 'objectiveId': constant.irisGenericValues['objectiveId'], 'testControl': {'type': 'SKIP', 'test': 90}})
            constant.thiriftCampaignShardTestReferenceObject['skip']['campaign']['name'] = campaignPayload_SKIP['name']
            constant.thiriftCampaignShardTestReferenceObject['skip']['campaign']['id'] = \
                campaignResponse_SKIP['json']['entity']['campaignId']
        if 'custom' in typesOfCampaign:
            campaignResponse_CUSTOM, campaignPayload_CUSTOM = campaigns.createCampaign(
                {'name': 'CampaignShard_' + str(int(time.time() * 100000)),
                 'goalId': constant.irisGenericValues['goalId'],
                 'objectiveId': constant.irisGenericValues['objectiveId'],
                 'testControl': {'type': 'CUSTOM', 'test': 90}})
            constant.thiriftCampaignShardTestReferenceObject['custom']['campaign']['name'] = campaignPayload_CUSTOM[
                'name']
            constant.thiriftCampaignShardTestReferenceObject['custom']['campaign']['id'] = \
                campaignResponse_CUSTOM['json']['entity']['campaignId']

    @staticmethod
    def setupListInThriftReference(typesOfList, typesOfCampaign=['org', 'skip', 'custom'], numberOfList=['A', 'B']):
        campaignShardObjectRef = campaignShardObject()
        for eachCampaignType in typesOfCampaign:
            campaignName = constant.thiriftCampaignShardTestReferenceObject[eachCampaignType.lower()]['campaign'][
                'name']
            campaignId = constant.thiriftCampaignShardTestReferenceObject[eachCampaignType.lower()]['campaign']['id']
            for eachList in typesOfList:
                for nameOfFilterLists in numberOfList:
                    connObj = CampaignShardHelper.getConnObj(newConnection=True)
                    if 'filter' in eachList:
                        CampaignShardHelper.setupFilterList(eachCampaignType, campaignName, campaignId,
                                                            nameOfFilterLists)
                    if 'upload' in eachList:
                        CampaignShardHelper.setupUploadList(eachCampaignType, campaignName, campaignId,
                                                            nameOfFilterLists)
                    if 'split' in eachList:
                        CampaignShardHelper.setupSplitList(connObj, campaignShardObjectRef, eachCampaignType,
                                                           campaignName, campaignId)
                    if 'merge' in eachList:
                        CampaignShardHelper.setupMergeList(connObj, campaignShardObjectRef, eachCampaignType,
                                                           campaignName, campaignId)
                    if 'duplicate' in eachList:
                        CampaignShardHelper.setupDuplicateList(connObj, campaignShardObjectRef, eachCampaignType,
                                                               campaignName, campaignId)
                    if 'dedup' in eachList:
                        CampaignShardHelper.setupDedupList(connObj, campaignShardObjectRef, eachCampaignType,
                                                           campaignName, campaignId)

    @staticmethod
    def setupSplitList(connObj, campaignShardObjectRef, campaignType, campaignName, campaignId, listType='SPLIT',
                       audienceType='FILTER_BASED'):
        try:
            Logger.log('Setting up Split List for campaignType :{} in campaign :{} campaignId :{}'.format(campaignType,
                                                                                                          campaignName,
                                                                                                          campaignId))
            existingList = \
                constant.thiriftCampaignShardTestReferenceObject[campaignType]['campaign']['lists'][audienceType][0]
            splitA = campaignShardObjectRef.SplitGroup('splitA_{}'.format(existingList['groupLabel']), 50)
            splitB = campaignShardObjectRef.SplitGroup('splitB_{}'.format(existingList['groupLabel']), 50)
            listOfSplit = [splitA, splitB]

            groupIdsOfListCreated = connObj.createList(
                constant.thiriftCampaignShardTestReferenceObject[campaignType]['campaign']['id'],
                campaignShardObjectRef.ListType[listType],
                campaignShardObjectRef.ListInfo(listType.lower(), {'oldGroupId': existingList['groupDetails']['id'],
                                                                   'splitGroupsList': listOfSplit}))
            CampaignShardHelper.setupCampaignShardThriftObjectWithDBDetails(campaignType, listType,
                                                                            groupIdsOfListCreated)
        except Exception, exp:
            raise Exception('Failed while setting up SplitList with Exception :{}'.format(exp))

    @staticmethod
    def setupMergeList(connObj, campaignShardObjectRef, campaignType, campaignName, campaignId, listType='MERGE',
                       audienceType='FILTER_BASED'):
        try:
            Logger.log('Setting up Merge List for campaignType :{} in campaign :{} campaignId :{}'.format(campaignType,
                                                                                                          campaignName,
                                                                                                          campaignId))
            existingListFirst = \
                constant.thiriftCampaignShardTestReferenceObject[campaignType]['campaign']['lists']['UPLOADED'][0]
            existingListSecond = \
                constant.thiriftCampaignShardTestReferenceObject[campaignType]['campaign']['lists']['FILTER_BASED'][0]

            groupIdsOfListCreated = connObj.createList(
                constant.thiriftCampaignShardTestReferenceObject[campaignType]['campaign']['id'],
                campaignShardObjectRef.ListType[listType],
                campaignShardObjectRef.ListInfo(listType.lower(), {
                    'newGroupName': 'Merge_' + existingListFirst['groupLabel'] + '_And_' + existingListSecond[
                        'groupLabel'], 'oldGroupIdList': [existingListFirst['groupDetails']['id'],
                                                          existingListSecond['groupDetails']['id']]}))
            CampaignShardHelper.setupCampaignShardThriftObjectWithDBDetails(campaignType, listType,
                                                                            groupIdsOfListCreated)
        except Exception, exp:
            raise Exception('Failed while setting up MergeList with Exception :{}'.format(exp))

    @staticmethod
    def setupDuplicateList(connObj, campaignShardObjectRef, campaignType, campaignName, campaignId,
                           listType='DUPLICATE', audienceType='FILTER_BASED'):
        try:
            Logger.log(
                'Setting up Duplicate List for campaignType :{} in campaign :{} campaignId :{}'.format(campaignType,
                                                                                                       campaignName,
                                                                                                       campaignId))
            existingList = \
                constant.thiriftCampaignShardTestReferenceObject[campaignType]['campaign']['lists'][audienceType][0]
            groupIdsOfListCreated = connObj.createList(
                constant.thiriftCampaignShardTestReferenceObject[campaignType]['campaign']['id'],
                campaignShardObjectRef.ListType[listType],
                campaignShardObjectRef.ListInfo(listType, {'oldGroupId': existingList['groupDetails']['id'],
                                                           'newGroupName': 'duplicate_' + existingList['groupLabel']}))
            CampaignShardHelper.setupCampaignShardThriftObjectWithDBDetails(campaignType, listType,
                                                                            groupIdsOfListCreated)
        except Exception, exp:
            raise Exception('Failed while setting up DuplicateList with Exception :{}'.format(exp))

    @staticmethod
    def setupDedupList(connObj, campaignShardObjectRef, campaignType, campaignName, campaignId, listType='DEDUP',
                       audienceType='FILTER_BASED'):
        try:
            Logger.log('Setting up Dedup List for campaignType :{} in campaign :{} campaignId :{}'.format(campaignType,
                                                                                                          campaignName,
                                                                                                          campaignId))
            existingListFirst = \
                constant.thiriftCampaignShardTestReferenceObject[campaignType]['campaign']['lists']['UPLOADED'][0]
            existingListSecond = \
                constant.thiriftCampaignShardTestReferenceObject[campaignType]['campaign']['lists'][audienceType][0]
            existingListThird = \
                constant.thiriftCampaignShardTestReferenceObject[campaignType]['campaign']['lists'][audienceType][1]
            listOfGroupIdNamePair = [
                campaignShardObjectRef.GroupIdNamePair(existingListFirst['groupDetails']['id'],
                                                       existingListFirst['groupLabel']),
                campaignShardObjectRef.GroupIdNamePair(existingListSecond['groupDetails']['id'],
                                                       existingListSecond['groupLabel']),
                campaignShardObjectRef.GroupIdNamePair(existingListThird['groupDetails']['id'],
                                                       existingListThird['groupLabel'])
            ]

            groupIdsOfListCreated = connObj.createList(
                constant.thiriftCampaignShardTestReferenceObject[campaignType]['campaign']['id'],
                campaignShardObjectRef.ListType[listType],
                campaignShardObjectRef.ListInfo(listType.lower(),
                                                {'createNewGroups': False, 'groupIdNameList': listOfGroupIdNamePair}))
            CampaignShardHelper.setupCampaignShardThriftObjectWithDBDetails(campaignType, listType,
                                                                            groupIdsOfListCreated)
        except Exception, exp:
            raise Exception('Failed while setting up DedupList with Exception :{}'.format(exp))

    @staticmethod
    def setupFilterList(eachCampaignType, campaignName, campaignId, nameOfFilterLists):
        try:
            Logger.log('Setting up Filter List :{} for campaignName :{} , campaignId :{}'.format(nameOfFilterLists,
                                                                                                 campaignName,
                                                                                                 campaignId))
            constant.thiriftCampaignShardTestReferenceObject[eachCampaignType.lower()]['campaign']['lists'][
                'FILTER_BASED'].insert(0,
                                       CampaignShardHelper.createFilterList(campaignId,
                                                                            '{}_{}_{}_list_Filter_{}'.format(
                                                                                eachCampaignType, campaignName,
                                                                                campaignId, nameOfFilterLists))
                                       )
        except Exception, exp:
            raise Exception('Filter Setup Failed with  Exception :{}'.format(exp))

    @staticmethod
    def setupCampaignShardThriftObjectWithDBDetails(campaignType, listType, groupIdsOfListCreated):
        for eachGroupId in groupIdsOfListCreated:
            data = {}
            data.update({'groupId': eachGroupId})
            data.update({'groupDetails': dbCallsList.getGroupDetailsWithListId(eachGroupId)})
            data.update({'groupLabel': data['groupDetails']['group_label'], 'uuid': None})
            data.update(
                {'groupVersionDetails': dbCallsList.getGroupVersionDetailsWithGroupId(data['groupDetails']['id'])})
            camapignGroupRecipientsData = {'TEST': dbCallsList.getAllUsersFromCampaignGroupRecipient(
                data['groupVersionDetails']['TEST']['bucket_id'], data['groupVersionDetails']['TEST']['id'])}
            if 'CONTROL' in data['groupVersionDetails']: camapignGroupRecipientsData.update({
                'CONTROL': dbCallsList.getAllUsersFromCampaignGroupRecipient(
                    data[
                        'groupVersionDetails'][
                        'CONTROL'][
                        'bucket_id'],
                    data[
                        'groupVersionDetails'][
                        'CONTROL'][
                        'id'])})
            data.update({'campaignGroupRecipients': camapignGroupRecipientsData})
            constant.thiriftCampaignShardTestReferenceObject[campaignType.lower()]['campaign']['lists'][
                listType].append(data)

    @staticmethod
    def loyaltyUserDataConstructHelper(loyaltyType='loyalty'):
        Logger.log("Constructing user data for all loyalty Users in this Org")
        allUsersInOrgList = dbCallsMessage.getAllUserInformationFromOrg(loyaltyType)
        userConstructedInfo = []
        for eachUserList in allUsersInOrgList:
            userConstructedInfo.append("{},{},{}".format(eachUserList[0], eachUserList[1], eachUserList[2]))
        Logger.log('User Constructed to Pass :{}'.format(userConstructedInfo))
        return userConstructedInfo

    @staticmethod
    def setupUploadList(eachCampaignType, campaignName, campaignId, nameOfFilterLists, newUser=False,
                        setupObjectForCampaignShard=True, channel='mobile'):
        try:
            Logger.log('Setting up Upload List :{} for campaignName :{} , campaignId :{}'.format(nameOfFilterLists,
                                                                                                 campaignName,
                                                                                                 campaignId))
            mergeListresponse, mergeListPayload, campaignId = campaignList.mergeList({}, campaignId=campaignId,
                                                                                     campaignType=['LIVE',
                                                                                                   eachCampaignType,
                                                                                                   'List', 'TAGS', 0],
                                                                                     userType=channel, numberOfUsers=10,
                                                                                     numberOfCustomTags=0,
                                                                                     newUser=newUser)
            groupDetails = dbCallsList.getGroupDetailsWithListId(mergeListresponse['json']['entity']['listId'])
            groupVersionDetails = dbCallsList.getGroupVersionDetailsWithGroupId(
                mergeListresponse['json']['entity']['listId'])
            camapignGroupRecipientsData = {
                'TEST': dbCallsList.getAllUsersFromCampaignGroupRecipient(groupVersionDetails['TEST']['bucket_id'],
                                                                          groupVersionDetails['TEST']['id'])}
            if 'CONTROL' in groupVersionDetails: camapignGroupRecipientsData.update({
                'CONTROL': dbCallsList.getAllUsersFromCampaignGroupRecipient(
                    groupVersionDetails[
                        'CONTROL']['bucket_id'],
                    groupVersionDetails[
                        'CONTROL']['id'])})
            if setupObjectForCampaignShard:
                constant.thiriftCampaignShardTestReferenceObject[eachCampaignType.lower()]['campaign']['lists'][
                    'UPLOADED'].append(
                    {
                        'addRecipientPayload': mergeListPayload['recipients'],
                        'groupLabel': mergeListPayload['name'],
                        'groupDetails': groupDetails,
                        'groupVersionDetails': groupVersionDetails,
                        'campaignGroupRecipients': camapignGroupRecipientsData
                    }
                )
            else:
                return {
                    'addRecipientPayload': mergeListPayload['recipients'],
                    'groupLabel': mergeListPayload['name'],
                    'groupDetails': groupDetails,
                    'groupVersionDetails': groupVersionDetails,
                    'campaignGroupRecipients': camapignGroupRecipientsData
                }
        except Exception, exp:
            raise Exception('Upload Setup Failed with  Exception :{}'.format(exp))

    @staticmethod
    def validateGetAudienceGroupWithDataSourceInfo(campaignType, audienceType, AudienceGroup, checkS3=True):
        Assertion.constructAssertion(int(AudienceGroup.orgId) == int(constant.config['orgId']),
                                     'Thrift Recieved OrgId :{} and actual :{}'.format(AudienceGroup.orgId,
                                                                                       constant.config['orgId']))

        groupLabels = list()
        groupIds = list()

        for each in constant.thiriftCampaignShardTestReferenceObject[campaignType]['campaign']['lists'][audienceType]:
            groupLabels.append(each['groupLabel'])
            groupIds.append(int(each['groupDetails']['id']))

        Assertion.constructAssertion(AudienceGroup.groupLabel in groupLabels,
                                     'Thrift Recieved groupLabel :{} and actual :{}'.format(AudienceGroup.groupLabel,
                                                                                            groupLabels))

        Assertion.constructAssertion(int(AudienceGroup.groupId) in groupIds, 'Thrift Recieved groupId :{} and actual :{}'.format(AudienceGroup.groupId,
                                                                                            groupIds))
        if audienceType == 'FILTER_BASED': Assertion.constructAssertion(AudienceGroup.uuId ==
                                                                        constant.thiriftCampaignShardTestReferenceObject[
                                                                            campaignType]['campaign']['lists'][
                                                                            audienceType][0]['uuid'],
                                                                        'Thrift Recieved uuid :{} and actual :{}'.format(
                                                                            AudienceGroup.uuId,
                                                                            constant.thiriftCampaignShardTestReferenceObject[
                                                                                campaignType]['campaign']['lists'][
                                                                                audienceType][0]['uuid']),verify=True)

        numberOfTestUsers = \
            constant.thiriftCampaignShardTestReferenceObject[campaignType]['campaign']['lists'][audienceType][0][
                'groupVersionDetails']['TEST']['customer_count']
        numberOfControlUsers = 0
        if 'CONTROL' in \
                constant.thiriftCampaignShardTestReferenceObject[campaignType]['campaign']['lists'][audienceType][0][
                    'groupVersionDetails']:
            numberOfControlUsers = \
                constant.thiriftCampaignShardTestReferenceObject[campaignType]['campaign']['lists'][audienceType][0][
                    'groupVersionDetails']['CONTROL']['customer_count']
        totalNumberOfUsers = int(numberOfTestUsers) + int(numberOfControlUsers)
        Logger.log(
            'totalNumberOfUsers :{} of which test :{} and control :{}'.format(totalNumberOfUsers, numberOfTestUsers,
                                                                              numberOfControlUsers))
        Assertion.constructAssertion(int(AudienceGroup.totalCustomerCount) == totalNumberOfUsers,
                                     'Thirft Recieved customerCount :{} and actual:{}'.format(
                                         AudienceGroup.totalCustomerCount, totalNumberOfUsers))
        Assertion.constructAssertion(AudienceGroup.isVisible == True, 'isVisible is True for the list')

        CampaignShardHelper.validateAudienceTargetToGroupVersion(campaignType, audienceType,
                                                                 AudienceGroup.audienceTargetToGroupVersion)
        if checkS3: CampaignShardHelper.validateAudienceGroupDataSourceInfo(campaignType, audienceType,
                                                                            AudienceGroup.audienceGroupDataSourceInfo,
                                                                            AudienceGroup.totalCustomerCount)

    @staticmethod
    def validateAudienceTargetToGroupVersion(campaignType, audienceType, audienceTargetToGroupVersion):
        for eachAudienceTargetToGroupVersion in audienceTargetToGroupVersion:
            AudienceGroupVersion = audienceTargetToGroupVersion[eachAudienceTargetToGroupVersion]
            groupVersionIdOfList = AudienceGroupVersion.groupVersionId
            if int(groupVersionIdOfList) == int(
                    constant.thiriftCampaignShardTestReferenceObject[campaignType]['campaign']['lists'][audienceType][
                        0]['groupVersionDetails']['TEST']['id']):
                Logger.log('Validating Customer Count for Test version id with groupVersionId :{}'.format(
                    groupVersionIdOfList))
                customerCountOfVersion = int(
                    constant.thiriftCampaignShardTestReferenceObject[campaignType]['campaign']['lists'][audienceType][
                        0]['groupVersionDetails']['TEST']['customer_count'])
                Assertion.constructAssertion(int(AudienceGroupVersion.customerCount) == customerCountOfVersion,
                                             'Cusomter Count with Thirft Call :{} and actual in DB :{}'.format(
                                                 AudienceGroupVersion.customerCount, customerCountOfVersion))
            elif int(groupVersionIdOfList) == int(
                    constant.thiriftCampaignShardTestReferenceObject[campaignType]['campaign']['lists'][audienceType][
                        0]['groupVersionDetails']['CONTROL']['id']):
                Logger.log('Validating Customer Count for Control version id with groupVersionId :{}'.format(
                    groupVersionIdOfList))
                customerCountOfVersion = int(
                    constant.thiriftCampaignShardTestReferenceObject[campaignType]['campaign']['lists'][audienceType][
                        0]['groupVersionDetails']['CONTROL']['customer_count'])
                Assertion.constructAssertion(int(AudienceGroupVersion.customerCount) == customerCountOfVersion,
                                             'Cusomter Count with Thirft Call :{} and actual in DB :{}'.format(
                                                 AudienceGroupVersion.customerCount, customerCountOfVersion))

    @staticmethod
    def getGroupInfoOfInvisibleList():
        return dbCallsList.getGroupDetailsOfInvisibleList()

    @staticmethod
    def splitListUsers(campaignType, userPayloadInfo):
        listOfMobiles = ''
        for each in userPayloadInfo:
            listOfMobiles = listOfMobiles + '{},'.format(each.split(',')[2])
        Logger.log('For camapaignType :{} , listofMobileNumbers : {}'.format(campaignType,
                                                                             listOfMobiles[:len(listOfMobiles) - 1]))
        listOfTestUsersId, listOfControlUserId = dbCallsMessage.getUserIdsForAlistOfMobileNumbers(
            listOfMobiles[:len(listOfMobiles) - 1])
        Logger.log(
            'List Of Test userIds : {}, List of Control userIds :{}'.format(listOfTestUsersId, listOfControlUserId))
        firstList = listOfTestUsersId[
                    int(len(listOfTestUsersId) * .00): int(len(listOfTestUsersId) * .50)] + listOfControlUserId[int(
            len(listOfControlUserId) * .00): int(len(listOfControlUserId) * .50)]
        secondList = listOfTestUsersId[
                     int(len(listOfTestUsersId) * .50): int(len(listOfTestUsersId) * 1.0)] + listOfControlUserId[int(
            len(listOfControlUserId) * .50): int(len(listOfControlUserId) * 1.0)]
        return map(lambda firstList: 'iris,automation,{}'.format(firstList['mobile']), firstList), map(
            lambda secondList: 'iris,automation,{}'.format(secondList['mobile']), secondList)

    @staticmethod
    def validateAudienceGroupDataSourceInfo(campaignType, audienceType, audienceGroupDataSourceInfo,
                                            totalNumberOfUsers):
        Logger.log('S3 Path :{} , Header :{} , bucketName :{} with totalNumberOfUsers :{}'.format(
            audienceGroupDataSourceInfo.audienceS3Info.s3Path, audienceGroupDataSourceInfo.audienceS3Info.s3Header,
            audienceGroupDataSourceInfo.audienceS3Info.bucketName,
            audienceGroupDataSourceInfo.audienceS3Info.customerCount))
        resultFromAWS = AWSHelper.readFileFromS3(audienceGroupDataSourceInfo.audienceS3Info.bucketName,
                                                 audienceGroupDataSourceInfo.audienceS3Info.s3Path)
        Logger.log('Result From AWS :{} with count :{}'.format(resultFromAWS, len(resultFromAWS)))

        usersInCGR = \
            constant.thiriftCampaignShardTestReferenceObject[campaignType]['campaign']['lists'][audienceType][0][
                'campaignGroupRecipients']
        for eachVersion in usersInCGR:
            Logger.log('Matching users in version :{}'.format(eachVersion))
            usersVersionSpecific = usersInCGR[eachVersion]
            numberOfUsersInEachVersion = 0
            for eachUser in usersVersionSpecific:
                Assertion.constructAssertion(str(eachUser) in resultFromAWS,
                                             'UserId :{} from version :{}  found in aws list'.format(eachUser,
                                                                                                     eachVersion))
                numberOfUsersInEachVersion = numberOfUsersInEachVersion + 1
            Logger.log('Total Number of users for version:{} are :{}'.format(eachVersion, numberOfUsersInEachVersion))

    @staticmethod
    def validateAudienceGroupBoolRes(listOfUsersAndStatus):
        for eachUserType in listOfUsersAndStatus:
            Logger.log('Validating for all :{} users'.format(eachUserType))
            for eachUserInfo in listOfUsersAndStatus[eachUserType]:
                Assertion.constructAssertion(eachUserInfo[1],
                                             'Status for UserId :{} is {}'.format(eachUserInfo[0], eachUserInfo[1]))

    @staticmethod
    def validateSearchAudienceGroup(listOfAudienceTypes, listOfAudienceGroup, campaignType=['org', 'skip', 'custom']):
        expectedDictOfGroupIdsPresent = {}
        for listType in listOfAudienceTypes:
            for eachCampaignType in campaignType:
                length = len(
                    constant.thiriftCampaignShardTestReferenceObject[eachCampaignType]['campaign']['lists'][listType])
                expectedDictOfGroupIdsPresent[
                    constant.thiriftCampaignShardTestReferenceObject[eachCampaignType]['campaign']['lists'][listType][
                        length - 1]['groupDetails']['id']] = {'campaignType': eachCampaignType, 'listType': listType}

        if len(expectedDictOfGroupIdsPresent) > 5:
            expectedDictOfGroupIdsPresent = expectedDictOfGroupIdsPresent[len(expectedDictOfGroupIdsPresent) - 5:]
        Logger.log('Expected GroupIds to Be Validated :{}'.format(expectedDictOfGroupIdsPresent))

        actualDictOfGroupIdsPresent = {}
        for eachAudienceGroup in listOfAudienceGroup:
            actualDictOfGroupIdsPresent[eachAudienceGroup.groupId] = eachAudienceGroup
        Logger.log('Actual AudienceGroup Data to be Validated :{}'.format(actualDictOfGroupIdsPresent))

        for eachGroupId in expectedDictOfGroupIdsPresent:
            Assertion.constructAssertion(eachGroupId in actualDictOfGroupIdsPresent,
                                         'Expected GroupId :{} found in list :{}'.format(eachGroupId,
                                                                                         actualDictOfGroupIdsPresent))
            Logger.log(
                'For Campaign Type :{} , audienceType :{} , audienceGroup :{} calling validateGetAudienceGroupWithDataSourceInfo'.format(
                    expectedDictOfGroupIdsPresent[eachGroupId]['campaignType'],
                    expectedDictOfGroupIdsPresent[eachGroupId]['listType'], actualDictOfGroupIdsPresent[eachGroupId]))
            CampaignShardHelper.validateGetAudienceGroupWithDataSourceInfo(
                expectedDictOfGroupIdsPresent[eachGroupId]['campaignType'],
                expectedDictOfGroupIdsPresent[eachGroupId]['listType'], actualDictOfGroupIdsPresent[eachGroupId],
                checkS3=False)

    @staticmethod
    def updateBucketIdRowCount(rows_count=15037664):
        if constant.config['cluster'] == 'nightly':
            return dbCallsList.updateRowCountOfBucket(rows_count=rows_count)
        else:
            raise Exception('Warning : Warning : Warning : updateBucketIdRowCount getting called for Other clusters ')

    @staticmethod
    def validateBucketIdWhenBucketUpdated(groupId, expectedBucketDetails):
        Logger.log(
            'Checking for Bucket Id with groupId :{} and expectedBucketDetails:'.format(groupId, expectedBucketDetails))
        groupVersionDetailslatest = dbCallsList.getGroupVersionDetailsWithGroupId(groupId)
        latestBucketId = groupVersionDetailslatest['TEST']['bucket_id']
        Assertion.constructAssertion(int(latestBucketId) == expectedBucketDetails,
                                     'Expected Bucket Id :{} but actually in DB :{}'.format(expectedBucketDetails,
                                                                                            latestBucketId))

    @staticmethod
    def validateGroupStatusAsync(audiencecGroupEntity, status, audienceType):
        CampaignShardHelper.validateGroupStatusAsync_response(audiencecGroupEntity, status, audienceType)
        CampaignShardHelper.validateGroupStatusAsync_database(audiencecGroupEntity, status, audienceType)

    @staticmethod
    def validateGroupStatusAsync_response(audiencecGroupEntity, status, audienceType):
        Assertion.constructAssertion(
            audiencecGroupEntity['status'] == campaignShardObject().AudienceGroupStatus[status],
            'Status In Response :{} and Expected :{}'.format(audiencecGroupEntity['status'], status))
        for eachExpectedResult in [('customerCount', 0), ('controlCount', 0),
                                   ('reachabilityStatus', None), ('versionNumber', 0), ('testCount', 0)]:
            Assertion.constructAssertion(audiencecGroupEntity[eachExpectedResult[0]] == eachExpectedResult[1],
                                         'Actual Value of :{} is :{} and expected is :{}'.format(eachExpectedResult[0],
                                                                                                 audiencecGroupEntity[
                                                                                                     eachExpectedResult[
                                                                                                         0]],
                                                                                                 eachExpectedResult[1]))

        Assertion.constructAssertion(audiencecGroupEntity['versionId'] is not None,
                                     'Group Version id is :{} and Expected in NULL'.format(
                                         audiencecGroupEntity['versionId']
                                     ))
        Assertion.constructAssertion(
            audiencecGroupEntity['type'] == campaignShardObject().CampaignGroupType[audienceType],
            'Type in Actual is :{} and passed:{}'.format(audiencecGroupEntity['type'], audienceType))
        Assertion.constructAssertion(audiencecGroupEntity['orgId'] == constant.config['orgId'],
                                     'OrgId is :{}'.format(constant.config['orgId']))
        if audienceType == 'FILTER_BASED':
            Assertion.constructAssertion(audiencecGroupEntity['uuId'] is not None, 'UUID is not None')

    @staticmethod
    def validateGroupStatusAsync_database(audiencecGroupEntity, status, audienceType):
        CampaignShardHelper.validateGroupStatusAsync_database_groupDetails(audiencecGroupEntity)
        CampaignShardHelper.validateGroupStatusAsync_database_groupVersionDetails(audiencecGroupEntity, status,
                                                                                  audienceType)

    @staticmethod
    def validateGroupStatusAsync_database_groupDetails(audiencecGroupEntity):
        groupDetailsInfo = dbCallsList.getGroupDetailsWithListId(audiencecGroupEntity['id'])

        for eachGroupMetaEntry in ['uuId', 'orgId']: #'description'
            Assertion.constructAssertion(
                audiencecGroupEntity[eachGroupMetaEntry] == groupDetailsInfo[eachGroupMetaEntry],
                'For :{} , Actual :{} and expected :{}'.format(eachGroupMetaEntry,
                                                               audiencecGroupEntity[eachGroupMetaEntry],
                                                               groupDetailsInfo[eachGroupMetaEntry]))
        Assertion.constructAssertion(audiencecGroupEntity['type'] == campaignShardObject().CampaignGroupType[groupDetailsInfo['type']],
                                     'Type in Response :{} and in DB :{}'.format(audiencecGroupEntity['type'],
                                                                             groupDetailsInfo['type']))
        Assertion.constructAssertion(groupDetailsInfo['is_visible'] == 1 ,
                                     'Is_visible in DB :{} and expected is 1'.format(groupDetailsInfo['type']))
        Assertion.constructAssertion(audiencecGroupEntity['label'] == groupDetailsInfo['label'],
                                     'label in Response and in DB :{}'.format(audiencecGroupEntity['label'],
                                                                              groupDetailsInfo['label']))

    @staticmethod
    def validateGroupStatusAsync_database_groupVersionDetails(audiencecGroupEntity, status, audienceType):
        groupDetailsVersionInfo = dbCallsList.getGroupVersionDetailsWithGroupId(audiencecGroupEntity['id'])
        Assertion.constructAssertion(groupDetailsVersionInfo['TEST']['status'] == status,
                                     'In Status :{} and Expected :{} in GVD'.format(groupDetailsVersionInfo['TEST']['status'],
                                                                                    status))
        if 'CONTROL' in groupDetailsVersionInfo:
            Assertion.constructAssertion(True,'For createorUpdateGroup Call CONTROL entry should be present in new Flow As Well')

    @staticmethod
    def validateErrorStatusAsync(groupId):
        groupDetailsVersionInfo = dbCallsList.getGroupVersionDetailsWithGroupId(groupId,expectedStatus='ERROR')
        Assertion.constructAssertion(groupDetailsVersionInfo['TEST']['status'] == 'ERROR',
                                     'Mark Error Status :{} and Expected :{} in GVD'.format(
                                         groupDetailsVersionInfo['TEST']['status'],
                                         'ERROR'))