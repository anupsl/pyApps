import copy, inspect
import json, collections
import time, itertools

from src.modules.campaign_shard.campaignShardObject import campaignShardObject
from src.modules.campaign_shard.campaignShardHelper import CampaignShardHelper
from src.Constant.constant import constant
from src.dbCalls.campaignShard import list_Calls
from src.dbCalls.messageInfo import pocMetaInfo
from src.modules.irisv2.campaigns.createCampaign import CreateCampaign
from src.modules.irisv2.helper.irisHelper import IrisHelper
from src.utilities.assertion import Assertion
from src.utilities.awsHelper import AWSHelper
from src.utilities.fileHelper import FileHelper
from src.utilities.logger import Logger
from src.utilities.randValues import randValues
from src.utilities.utils import Utils

class CreateAudience():
    @staticmethod
    def uploadList(campaignType, testControlType, payload=None, label=None, schemaType=None,
                   schemaIdentifier=["MOBILE"], schemaData=None, numberOfUsers=10, numberOfFiles=1,
                   numberOfCustomTags=0, newUser=True, updateNode=False, lockNode=False, campaignCheck=True,
                   popFields=[], offset=0,mobilePush=False, filePath = None):
        if campaignCheck: CreateCampaign.create(campaignType, testControlType, updateNode=updateNode)
        if not CreateAudience.checkListAvailable(campaignType, testControlType, 'UPLOAD',
                                                 schemaIdentifier[0].upper()) or updateNode:
            endpoint = IrisHelper.constructUrl('createlist')
            payload = CreateAudience.constructUploadPayload(
                'UPLOAD',
                label=label,
                description=None,
                numberOfCustomTags=numberOfCustomTags,
                schemaType=schemaType,
                schemaIdentifier=schemaIdentifier,
                schemaData=schemaData,
                source=None,
                numberOfUsers=numberOfUsers,
                newUser=newUser,
                numberOfFiles=numberOfFiles,
                popFields=popFields,
                offset=offset,
                mobilePush=mobilePush,
                filePath=filePath
            ) if payload is None else payload
            Logger.log('Final Payload Getting used :{}'.format(payload))

            response = IrisHelper.constructResponse(
                Utils.makeRequest(url=endpoint, data='', auth=IrisHelper.constructAuthenticate(),
                                  headers=IrisHelper.constructHeaders(contentType=False), files=payload, method='POST')
            )

            if response['statusCode'] == 200:
                CreateAudience.validateUploadList(response, payload)
                if not lockNode: CreateAudience.updateNodeList(campaignType, testControlType, 'UPLOAD',
                                                               schemaIdentifier[0], response,
                                                               response['json']['entity']['id'],
                                                               response['json']['entity']['versionId'],
                                                               response['json']['entity']['uploadStatus'][0]['fileUrl'],
                                                               response['json']['entity']['label'])
                return {
                    'ID': response['json']['entity']['id'],
                    'NAME': response['json']['entity']['label'],
                    'VID': response['json']['entity']['versionId'],
                    'S3': response['json']['entity']['uploadStatus'][0]['fileUrl'],
                    'RESPONSE': response
                }
            else:
                return {
                    'RESPONSE': response,
                    'PAYLOAD': payload
                }
        else:
            return constant.config['node'][campaignType][testControlType]['LIST']['UPLOAD'][schemaIdentifier[0]]

    @staticmethod
    def FilterList(campaignType, testControlType, schemaIdentifier=["MOBILE"], updateNode=False, lockNode=False, campaignCheck=True):
        if campaignCheck: CreateCampaign.create(campaignType, testControlType, updateNode=updateNode)
        if not CreateAudience.checkListAvailable(campaignType, testControlType, 'LOYALTY',
                                                 schemaIdentifier[0].upper()) or updateNode:

            groupLabel = 'createGroupRecipient_{}'.format(int(time.time() * 1000))

            audienceGroupRequestObj = campaignShardObject.createAudienceRequest({'label': groupLabel})
            connObj = CampaignShardHelper.getConnObj(newConnection=True)
            audienceGroupResponse = connObj.createAudienceGroup(audienceGroupRequestObj).__dict__
            audienceGroupRequestObj = campaignShardObject.createAudienceRequest({'groupId' : audienceGroupResponse['id'],
                                                                                        'label' : audienceGroupResponse['label']})
            response = connObj.createAudience(audienceGroupRequestObj).__dict__
            uploadStatus = response['uploadStatus'][0].__dict__
            s3FileUrlWithBucket = uploadStatus['fileUrl'].split('//')[1]
            if not lockNode:
                CreateAudience.updateNodeList(campaignType, testControlType, 'LOYALTY', schemaIdentifier[0], response,
                                              response['id'], response['versionId'], s3FileUrlWithBucket[s3FileUrlWithBucket.index('/'):],
                                              response['label'])

            return {
                'ID': response['id'],
                'NAME': response['label'],
                'VID': response['versionId'],
                'S3': s3FileUrlWithBucket[s3FileUrlWithBucket.index('/'):],
                'RESPONSE': response,
                'UUID': constant.orgDetails[constant.config['cluster']][constant.config['orgId']]['s3']['uuid']
            }
        else:
            return constant.config['node'][campaignType][testControlType]['LIST']['LOYALTY'][schemaIdentifier[0]]

    @staticmethod
    def derivedList(campaignType, testControlType, payload=None, label=None, schemaIdentifier=["MOBILE"],
                   numberOfCustomTags=0, newUser=True, updateNode=False, lockNode=False, campaignCheck=True,
                   popFields=[], derivedListInfo = {}):
        if campaignCheck: CreateCampaign.create(campaignType, testControlType, updateNode=updateNode)
        if not CreateAudience.checkListAvailable(campaignType, testControlType, 'DERIVED',
                                                 schemaIdentifier[0].upper()) or updateNode:
            inclsUsers, exclsUsers = list(), list()
            endpoint = IrisHelper.constructUrl('createderivedlist')
            if payload is None:
                includedGroupsIds, excludedGroupsIds = list(), list()
                if 'includedGroups' in derivedListInfo:
                    includedGroupsIds, inclsUsers = CreateAudience.createDerivedList(campaignType, testControlType,
                                                                         derivedListInfo['includedGroups'],
                                                                         schemaIdentifier[0], newUser, derivedListInfo,
                                                                         derivedListInfo['includedUserIds'] if 'includedUserIds' in derivedListInfo else None)
                if 'excludedGroup' in derivedListInfo:
                    if not 'sameIds' in derivedListInfo:
                        excludedGroupsIds, exclsUsers = CreateAudience.createDerivedList(campaignType, testControlType,
                                                                             derivedListInfo['excludedGroup'],
                                                                             schemaIdentifier[0], newUser,
                                                                             derivedListInfo,
                                                                             derivedListInfo['excludedUserIds'] if 'excludedUserIds' in derivedListInfo else None)
                    else:
                        if len(derivedListInfo['includedGroups']) >= len(derivedListInfo['excludedGroup']):
                            for excId in derivedListInfo['excludedGroup']:
                                if excId in derivedListInfo['includedGroups']:
                                    excludedGroupsIds.append(
                                        includedGroupsIds[derivedListInfo['includedGroups'].index(excId)])
                payload = CreateAudience.constructDrivedPayload(
                    'DERIVED',
                    label=label,
                    description=None,
                    numberOfCustomTags=numberOfCustomTags,
                    includedGroups=includedGroupsIds,
                    excludedGroups=excludedGroupsIds,
                    popFields=popFields
                )
            Logger.log('Final Payload Getting used :{}'.format(payload))
            response = IrisHelper.constructResponse(
                Utils.makeRequest(url=endpoint, data=payload, auth=IrisHelper.constructAuthenticate(),
                                  headers=IrisHelper.constructHeaders(), method='POST')
            )
            if response['statusCode'] == 200:
                CreateAudience.validateDerivedList(response, payload)
                if not lockNode: CreateAudience.updateNodeList(campaignType, testControlType, 'DERIVED',
                                                               schemaIdentifier[0], response,
                                                               response['json']['entity']['id'],
                                                               response['json']['entity']['versionId'],
                                                               None,
                                                               response['json']['entity']['label'])
                return {
                    'ID': response['json']['entity']['id'],
                    'NAME': response['json']['entity']['label'],
                    'VID': response['json']['entity']['versionId'],
                    'S3': None,
                    'RESPONSE': response,
                    'expectedUserCount' : len(list(set(inclsUsers) - set(exclsUsers)))
                }
            else:
                return {
                    'RESPONSE': response,
                    'PAYLOAD': payload
                }
        else:
            return constant.config['node'][campaignType][testControlType]['LIST']['DERIVED'][schemaIdentifier[0]]

    @staticmethod
    def stickyList(campaignType, testControlType, payload=None, label=None,
                   schemaIdentifier=["MOBILE"], updateNode=False, lockNode=False, campaignCheck=True,
                   popFields=[], stickyInfo = {}):
        if campaignCheck: CreateCampaign.create(campaignType, testControlType, updateNode=updateNode)
        if not CreateAudience.checkListAvailable(campaignType, testControlType, 'ORG_USERS',
                                                 schemaIdentifier[0].upper()) or updateNode:
            Logger.log('excluser user: ', stickyInfo)
            endpoint = IrisHelper.constructUrl('sticklylist')
            payload = CreateAudience.constructStickyPayload(
                label=label,
                description=None,
                popFields=popFields,
                includedUsers=stickyInfo['includeUsers'] if 'includeUsers' in stickyInfo else ':1',
                excludedUsers=stickyInfo['excludeUsers'] if 'excludeUsers' in stickyInfo else ':1',
                groupId=stickyInfo['groupId'] if 'groupId' in stickyInfo else None,
            ) if payload is None else payload
            Logger.log('Final Payload Getting used :{}'.format(payload))
            response = IrisHelper.constructResponse(
                Utils.makeRequest(url=endpoint, data=payload, auth=IrisHelper.constructAuthenticate(),
                                  headers=IrisHelper.constructHeaders(), method='POST')
            )
            if 'label' in stickyInfo:
                payload.update({'label' : stickyInfo['label']})
            if response['statusCode'] == 200:
                CreateAudience.validateStickyList(response, payload)
                if not lockNode: CreateAudience.updateNodeList(campaignType, testControlType, 'ORG_USERS',
                                                               schemaIdentifier[0], response,
                                                               response['json']['entity']['id'],
                                                               response['json']['entity']['versionId'],
                                                               None,
                                                               response['json']['entity']['label'])
                return {
                    'ID': response['json']['entity']['id'],
                    'NAME': response['json']['entity']['label'],
                    'VID': response['json']['entity']['versionId'],
                    'S3': None,
                    'RESPONSE': response
                }
            else:
                return {
                    'RESPONSE': response,
                    'PAYLOAD': payload
                }
        else:
            return constant.config['node'][campaignType][testControlType]['LIST']['ORG_USERS'][schemaIdentifier[0]]

    @staticmethod
    def assertResponse(response, expectedStatusCode, expectedErrorCode=999999, expectedErrorMessage=[]):
        if response['constructed'].lower() == 'pass':
            if expectedStatusCode >= 200 and expectedStatusCode <= 300:
                Assertion.constructAssertion(response['statusCode'] == int(expectedStatusCode),
                                             'Matching statusCode actual :{},expected :{}'.format(
                                                 response['statusCode'], expectedStatusCode))
                if len(response['json']['warnings']) > 0:
                    Logger.log('There was a Warning while Creating Campaign :', response['json']['warning'])
            else:
                Assertion.constructAssertion(response['statusCode'] == int(expectedStatusCode),
                                             'Matching statusCode actual :{},expected :{}'.format(
                                                 response['statusCode'], expectedStatusCode))
                for errorReturned in response['json']['errors']:
                    Logger.log('Status Code :{} and error :{}', response['statusCode'], errorReturned)
                    Assertion.constructAssertion(errorReturned['code'] == expectedErrorCode,
                                                 'Matching Error Code ,actual:{} and expected:{}'.format(
                                                     errorReturned['code'], expectedErrorCode))
                    Assertion.constructAssertion(errorReturned['status'] == False, 'Checking for Error Status as False')
                    Assertion.constructAssertion(errorReturned['message'] in expectedErrorMessage,
                                                 'Matching Error Message ,actual:{} in expected:{}'.format(
                                                     errorReturned['message'], expectedErrorMessage))
        else:
            Assertion.constructAssertion(False, 'Constructed Body has Failed due to Exception so no Validation')

    @staticmethod
    def checkListAvailable(campaignType, testControlType, listType, identifier):
        listAvialable = True
        for each in ['ID', 'NAME', 'RESPONSE', 'VID', 'S3']:
            if constant.config['node'][campaignType][testControlType]['LIST'][listType][identifier][each] is None:
                listAvialable = False
        return listAvialable

    @staticmethod
    def updateNodeList(campaignType, testControlType, listType, identifier, response, listId, listVersionId, s3Path,
                       listName):
        constant.config['node'][campaignType][testControlType]['LIST'][listType][identifier]['ID'] = listId
        constant.config['node'][campaignType][testControlType]['LIST'][listType][identifier]['VID'] = listVersionId
        constant.config['node'][campaignType][testControlType]['LIST'][listType][identifier]['S3'] = s3Path
        constant.config['node'][campaignType][testControlType]['LIST'][listType][identifier]['NAME'] = listName
        constant.config['node'][campaignType][testControlType]['LIST'][listType][identifier]['RESPONSE'] = response

    @staticmethod
    def waitForGVDToBeUpdated(groupId, checkCustomerCount=True, checkParams=True):
        if checkCustomerCount:
            for _ in range(10):
                if list_Calls().getCustomerCountInGVD(groupId) > 0: break
                time.sleep(5)
        if checkParams:
            for _ in range(10):
                params = json.loads(list_Calls().getParamsFromGVD(groupId))
                if 'test_count' in params and 'control_count' in params: break
                time.sleep(5)

    @staticmethod
    def waitForReachabilityJobCompletion(groupVersionId):
        reachabilityFlag = False
        for _ in range(12):
            if list_Calls().getReachabilityStatus(groupVersionId) == 'CLOSED':
                reachabilityFlag = True
                break
            time.sleep(5)

    @staticmethod
    def constructUploadPayload(listType, label=None, description=None, numberOfCustomTags=0, schemaType=None,
                               schemaIdentifier=None, schemaData=None, source=None, numberOfUsers=10, newUser=True,
                               numberOfFiles=1, popFields=[], offset=0,mobilePush=False, filePath=None):
        audienceGroupBody = {
            "type": listType,
            "label": "AutomationList_{}".format(int(time.time() * 1000)) if label is None else label,
            "description": "Automation Created List" if description is None else description,
            "tags": CreateAudience.createCustomTags(numberOfCustomTags),
            "data": {
                "schema": {
                    "type": "SINGLE_KEY_IDENTIFIER" if schemaType is None else schemaType,
                    "identifier": ["MOBILE"] if schemaIdentifier is None else schemaIdentifier,
                    "data": ["MOBILE", "FIRST_NAME"] if schemaData is None else schemaData
                },
                "source": "FILE" if source is None else source
            }
        }
        return CreateAudience.createFinalPayload(audienceGroupBody, numberOfUsers, newUser, numberOfFiles,
                                                 popFields=popFields, offset=offset,mobilePush=mobilePush, filePath=filePath)


    @staticmethod
    def createFinalPayload(audienceGroupBody, numberOfUsers, newUser, numberOfFiles, popFields, lockDataAppend=False,
                           offset=0,mobilePush=False, filePath = None):
        payload = list()
        if len(popFields) > 0: audienceGroupBody = CreateAudience.popFieldsFromPayload(audienceGroupBody, popFields)
        payload.append(['audienceGroupBody', (None, json.dumps(audienceGroupBody), 'application/json')])
        for _ in range(numberOfFiles):
            createdfilePath = CreateAudience.createCSV(audienceGroupBody, numberOfUsers, newUser,
                                                lockDataAppend=lockDataAppend, offset=offset,mobilePush=mobilePush) if filePath is None else filePath
            Logger.log('FilePath :{}'.format(createdfilePath))

            payload.append(['file', [createdfilePath.split('/')[-1], open(createdfilePath, 'rb'), 'text/csv']])
            if 'identifier' in audienceGroupBody['data']['schema']:
                if audienceGroupBody['data']['schema']['identifier'][0] in ['USER_ID',
                                                                            'EXTERNAL_ID']: offset = offset + numberOfUsers
            time.sleep(1)
        return payload

    @staticmethod
    def constructDrivedPayload(listType, label=None, description=None, numberOfCustomTags=0,
                               popFields=[], includedGroups = [], excludedGroups = []):
        audienceGroupBody = {
                "audienceGroupType": listType,
                "label": "AutomationList_{}".format(int(time.time() * 1000)) if label is None else label,
                "description": "Automation Created List" if description is None else description,
                "tags": CreateAudience.createCustomTags(numberOfCustomTags),
                "includedGroups": includedGroups,
                "excludedGroups": excludedGroups
            }
        if len(popFields) > 0: audienceGroupBody = CreateAudience.popFieldsFromPayload(audienceGroupBody, popFields)
        return audienceGroupBody

    @staticmethod
    def constructStickyPayload(label=None, description=None, popFields=[],includedUsers = '', excludedUsers = '', groupId = None):
        audienceGroupBody = {
                "label": "AutomationList_{}".format(int(time.time() * 1000)) if label is None else label,
                "description": "Automation Created List" if description is None else description,
                "includeUsers": CreateAudience.userListSplit(userList=constant.config['pocUsers'], listType='ORG_USERS', splitIndex=includedUsers) if type(includedUsers) == str else includedUsers,
                "excludeUsers": CreateAudience.userListSplit(userList=constant.config['pocUsers'], listType='ORG_USERS', splitIndex=excludedUsers) if type(excludedUsers) == str else excludedUsers,
            }
        if groupId is not None: audienceGroupBody.update({'groupId' : groupId})
        if len(popFields) > 0: audienceGroupBody = CreateAudience.popFieldsFromPayload(audienceGroupBody, popFields)
        return audienceGroupBody

    @staticmethod
    def getPocUsers():
        endpoint = IrisHelper.constructUrl('pocUsers')
        response = IrisHelper.constructResponse(Utils.makeRequest(url=endpoint, data='', auth=IrisHelper.constructAuthenticate(),
                                                                  headers=IrisHelper.constructHeaders(contentType=False), method='GET'))
        usersList = list()
        if response['statusCode'] == 200:
            orgPocList = response['json']['entity']['orgPocs']
            if len(orgPocList) != 0:
                for pocUser in orgPocList:
                    usersList.append({'email': pocUser['email'],
                                      'mobile': pocUser['mobile'], 'name': pocUser['firstName'],
                                      })
        else:
            Logger.log('Get POC user API is down and statusCode ',response['statusCode'])
        if len(usersList) == 0:
            pocMetaData = pocMetaInfo().pocMetaData
            for id in pocMetaData['orgPocs']:
                pocUser = pocMetaData['orgPocs'][id]
                usersList.append({'email': pocUser['email'],
                                  'mobile': pocUser['mobile'], 'name': pocUser['firstName'],
                                  })
        constant.config['pocUsers'] = usersList

    @staticmethod
    def getPocNewUsers(noOfUsers =2, offset = 0, newUsers = False):
        usersList = list()
        if not newUsers:
            usersFromDB = list_Calls().getExistingUsers(noOfUsers,offset= offset)
            for eachUser in usersFromDB:
                usersList.append({'email': eachUser[4], 'mobile': eachUser[3], 'name': eachUser[1]})
        else:
            for _ in range(noOfUsers):
                usersList.append({'email': randValues.randomEmailId(),
                                  'mobile': randValues.getRandomMobileNumber(), 'name': randValues.randomString(size=5),
                                  })
        return usersList

    @staticmethod
    def createDerivedList(campaignType, testControlType, groupsType, schemaIdentifier, newUser, derivedInfo, userIds = None):
        groupListIds = []
        uploadUserIdsListCount = 0
        userslist = []
        deriveUsersList = []
        actualIdentifier = schemaIdentifier
        for eachListType in groupsType:
            groupId = None
            if eachListType[:6] == 'UPLOAD':
                if userIds is None or uploadUserIdsListCount == len(userIds):
                    if eachListType[6:] == 'OLD':
                        schemaIdentifier = 'USER_ID'
                    groupId = CreateAudience.uploadList(campaignType, testControlType, schemaIdentifier=[schemaIdentifier],
                                                     schemaData=[schemaIdentifier, 'FIRST_NAME'], newUser= True if eachListType[6:] != 'OLD' else False, numberOfUsers=derivedInfo['noOfUserUpload'],
                                                     campaignCheck=False, updateNode=True, lockNode=True)['ID']
                    groupListIds.append(groupId)
                else:
                    data = list()
                    for userId in userIds[uploadUserIdsListCount]:
                        data.append(str(userId) + ',Test_{}'.format(randValues.getRandomMobileNumber()))
                    Logger.log('CSV file ', data)
                    filePath = CreateAudience.createCSVUsingList(data)
                    groupId = CreateAudience.uploadList(campaignType, testControlType, schemaIdentifier=['USER_ID'],
                                                schemaData=['USER_ID', 'FIRST_NAME'],campaignCheck=False,
                                                updateNode=True, lockNode=True, filePath=filePath)['ID']
                    groupListIds.append(groupId)
                    uploadUserIdsListCount = uploadUserIdsListCount + 1
            elif eachListType == 'LOYALTY':
                groupListIds.append(CreateAudience.FilterList(campaignType, testControlType, schemaIdentifier=[schemaIdentifier],
                                                 campaignCheck=False, updateNode=True, lockNode=True)['ID'])
            elif eachListType == 'DERIVED':
                groupIds, deriveUsersList = CreateAudience.createDerivedList(campaignType, testControlType, derivedInfo[eachListType.lower()],
                                                schemaIdentifier=schemaIdentifier, newUser=newUser, derivedInfo=derivedInfo)
                endpoint = IrisHelper.constructUrl('createderivedlist')
                payload = CreateAudience.constructDrivedPayload('DERIVED', label=None, description=None,
                                                numberOfCustomTags=0, includedGroups=groupIds)
                Logger.log('Final Payload Getting used :{}'.format(payload))
                response = IrisHelper.constructResponse(
                    Utils.makeRequest(url=endpoint, data=payload, auth=IrisHelper.constructAuthenticate(),
                                      headers=IrisHelper.constructHeaders(), method='POST')
                )
                if response['statusCode'] == 200:
                    groupId = response['json']['entity']['id']
                    groupListIds.append(groupId)
                else:
                    Logger.log('Derived list creation Failed: ' , response)

            else:
                raise Exception('ListTypeNotSupportedException:{}'.format(eachListType))
            if eachListType in 'UPLOADOLD':
                s3FileUrl = list_Calls().getUploadedFileUrl(groupId)
                userslist.append(filter(None,AWSHelper.readFileFromS3('campaigns{}'.format(constant.config['cluster']), s3FileUrl)))
            elif eachListType == 'DERIVED':
                userslist.append(deriveUsersList)
            else:
                userslist.append((filter(None, AWSHelper.readFileFromS3(bucketName=constant.orgDetails[constant.config['cluster']][constant.config['orgId']]
                                    ['s3BucketName'], keyName=constant.orgDetails[constant.config['cluster']][constant.config['orgId']]['s3KeyName']))))
            schemaIdentifier = actualIdentifier
        return groupListIds, CreateAudience.userListSplit(list(set(list(itertools.chain.from_iterable(userslist)))))

    @staticmethod
    def validateDerivedList(response, payload):
        for eachKey in ['id', 'label', 'auditInfo', 'type', 'versionId', 'versionNumber', 'uploadStatus',
                        'customerCount', 'testCount', 'controlCount']:
            Assertion.constructAssertion(eachKey in response['json']['entity'],
                                         'Key :{}, found in Response entity'.format(eachKey))
        Assertion.constructAssertion(response['json']['entity']['label'] == payload['label'],
                                     'Label in Response :{} and in Payload :{}'.format(
                                         response['json']['entity']['label'], payload['label']))

        CreateAudience.validateAuditInfo(response['json']['entity']['auditInfo'])
        if len(response['json']['warnings']) > 0: Assertion.constructAssertion(False, 'WARNING : {}'.format(
            response['json']['warnings']), verify=True)

    @staticmethod
    def popFieldsFromPayload(audienceGroupBody, popFields):
        for each in popFields:
            audienceGroupBody.pop(each)
        return audienceGroupBody

    @staticmethod
    def createCustomTags(numberOfTags):
        result = list()
        for each in range(numberOfTags):
            result.append('Tag{}'.format(each))
        return result

    @staticmethod
    def createCSV(audienceGroupBody, numberOfUsers, newUser, lockDataAppend=False, offset=0,mobilePush=False):
        filePath = constant.autoTempFilePath + 'AutoList_{}_{}'.format(randValues.randomString(8),int(time.time() * 1000))
        file = FileHelper(filePath)
        if lockDataAppend: return filePath
        if mobilePush: newUser=False
        if newUser:
            mobile = randValues.getRandomMobileNumber()
            for each in range(numberOfUsers):
                data = ''
                for identifier in audienceGroupBody['data']['schema']['data']:
                    if data is not '': data = data + ','
                    if identifier.upper() == 'MOBILE':
                        data = data + mobile
                        mobile = str(int(mobile) + 1)
                    elif identifier.upper() == 'EMAIL':
                        data = data + randValues.randomEmailId()
                    elif identifier.upper() == 'FIRST_NAME':
                        data = data + 'Test_{}'.format(randValues.getRandomMobileNumber())
                    elif identifier.upper() == 'LAST_NAME':
                        data = data + 'Automation_{}'.format(randValues.getRandomMobileNumber())
                    elif 'CUSTOM_TAG' in identifier.upper():
                        data = data + 'User_{}'.format(int(time.time()))
                    else:
                        raise Exception('Identifier :{} Not Supported'.format(identifier))
                file.appendToFile(data)
        else:
            for each in list_Calls().getExistingUsers(numberOfUsers, offset=offset,mobilePush=mobilePush):
                data = ''
                for identifier in audienceGroupBody['data']['schema']['data']:
                    if data is not '': data = data + ','
                    if identifier.upper() == 'MOBILE':
                        data = data + each[3]
                    elif identifier.upper() == 'EMAIL':
                        data = data + each[4]
                    elif identifier.upper() == 'FIRST_NAME':
                        data = data + each[2]
                    elif identifier.upper() == 'LAST_NAME':
                        data = data + each[1]
                    elif identifier.upper() == 'USER_ID':
                        data = data + str(each[0])
                    elif identifier.upper() == 'EXTERNAL_ID':
                        data = data + str(each[5])
                    elif 'CUSTOM_TAG' in identifier.upper():
                        data = data + 'User_{}'.format(each[0])
                    else:
                        raise Exception('Identifier :{} Not Supported'.format(identifier))
                file.appendToFile(data)
        return filePath

    @staticmethod
    def validateUploadList(response, payload):
        for eachKey in ['id', 'label', 'auditInfo', 'type', 'versionId', 'versionNumber', 'uploadStatus',
                        'customerCount', 'testCount', 'controlCount']:
            Assertion.constructAssertion(eachKey in response['json']['entity'],
                                         'Key :{}, found in Response entity'.format(eachKey))
        Assertion.constructAssertion(response['json']['entity']['label'] == json.loads(payload[0][1][1])['label'],
                                     'Label in Response :{} and in Payload :{}'.format(
                                         response['json']['entity']['label'], json.loads(payload[0][1][1])['label']))

        CreateAudience.validateAuditInfo(response['json']['entity']['auditInfo'])
        CreateAudience.validateUploadStatus(response['json']['entity']['uploadStatus'], payload)
        if len(response['json']['warnings']) > 0: Assertion.constructAssertion(False, 'WARNING : {}'.format(
            response['json']['warnings']), verify=True)

    @staticmethod
    def validateAuditInfo(auditInfo):
        for eachKey in ['createdBy', 'createdOn', 'lastUpdatedOn']:
            Assertion.constructAssertion(eachKey in auditInfo, 'Key :{} Found in auditInfo'.format(eachKey))
        Assertion.constructAssertion(str(auditInfo['createdBy']['id']) == str(constant.config['userId']),
                                     'CreatedBy in Response :{} and actually :{}'.format(auditInfo['createdBy']['id'],
                                                                                         constant.config['userId']),
                                     verify=True)

    @staticmethod
    def validateUploadStatus(uploadStatus, payload, maxLinesToTest=100):
        Assertion.constructAssertion(len(payload) - 1 == len(uploadStatus),
                                     'Length of payload Excluding audienceGroupBody :{} and length of Upload Status :{}'.format(
                                         len(payload) - 1, len(uploadStatus)))
        dataInFile = list()
        for eachFile in range(1, len(payload)):
            if 'differentFileFormat' in inspect.stack()[3][3]:
                dataInFile = dataInFile + FileHelper.readFile(constant.csvFilePath + payload[eachFile][1][0]).split('\n')
            else:
                dataInFile = dataInFile + FileHelper.readFile(constant.autoTempFilePath + payload[eachFile][1][0]).split('\n')
        for eachUploadStatus in uploadStatus:
            for eachKey in ['totalUploadCount', 'fileUrl', 'errorCount', 'status']:
                Assertion.constructAssertion(eachKey in eachUploadStatus,
                                             'Key :{} , found in Upload Status'.format(eachKey))
            Assertion.constructAssertion(eachUploadStatus['totalUploadCount'] == 0,
                                         'totalUploadCount is {}'.format(eachUploadStatus['totalUploadCount']))
            Assertion.constructAssertion(eachUploadStatus['errorCount'] == 0,
                                         'errorCount is {}'.format(eachUploadStatus['errorCount']))
            Assertion.constructAssertion(eachUploadStatus['status'] == 'OPEN',
                                         'upload Status is {}'.format(eachUploadStatus['status']))

            dataFromS3 = AWSHelper.readFileFromS3('campaigns{}'.format(constant.config['cluster']),
                                                  eachUploadStatus['fileUrl'])

            for eachLine in dataFromS3:
                Assertion.constructAssertion(eachLine in dataInFile, 'Line :{} found in FileData'.format(eachLine))
                maxLinesToTest = maxLinesToTest - 1
                if maxLinesToTest == 0: break

    @staticmethod
    def validateStickyList(response, payload):
        for eachKey in ['id', 'label', 'auditInfo', 'type', 'versionId', 'versionNumber',
                        'customerCount', 'testCount', 'controlCount']:
            Assertion.constructAssertion(eachKey in response['json']['entity'],
                                         'Key :{}, found in Response entity'.format(eachKey))
        Assertion.constructAssertion(response['json']['entity']['label'] == payload['label'],
                                     'Label in Response :{} and in Payload :{}'.format(
                                         response['json']['entity']['label'], payload['label']))

        # Logger.log(response['json']['entity']['users'])
        # CreateAudience.validateStickyUsers(response['json']['entity']['users'])
        CreateAudience.validateAuditInfo(response['json']['entity']['auditInfo'])
        if len(response['json']['warnings']) > 0: Assertion.constructAssertion(False, 'WARNING : {}'.format(
            response['json']['warnings']), verify=True)

    @staticmethod
    def validateStickyUsers(usersList):
        usersKeyList = ['name', 'email', 'mobile']
        for users in usersList:
            responseUserkeys = users.keys()
            Assertion.constructAssertion(collections.Counter(usersKeyList) == collections.Counter(responseUserkeys),
                                         'Users Response Keys Missing Actual keys: {} and Expected keys: {}'.format(responseUserkeys, usersKeyList))

    @staticmethod
    def waitForListToProcess(groupId, numberOfUsers):
        timeTaken = 0
        sleep = 5  # 1 second for each 1000 batch
        for _ in range(numberOfUsers / 1000):
            time.sleep(sleep)
            timeTaken = timeTaken + sleep
            if list_Calls().getCustomerCountInGVD(groupId) > 0: break
        customerCount = list_Calls().getCustomerCountInGVD(groupId)
        Assertion.constructAssertion(customerCount > 0,
                                     'For GroupId :{} with numberOfUsers :{} and customerCount :{}, time taken :{}'.format(
                                         groupId, numberOfUsers, customerCount, timeTaken), verify=True)

    @staticmethod
    def createMobileUsers(numberOfUser=1, newUser=True, append='91'):
        listOfUser = list()
        for each in range(numberOfUser):
            if newUser:
                mobile = randValues.getRandomMobileNumber(append=append)
                listOfUser.append('{},{}'.format(mobile, 'FNAME_{}'.format(mobile)))
            else:
                for each in list_Calls().getExistingUsers(numberOfUser):
                    mobile = str(each[3])
                    if append == '': mobile = str(each[3])[2:]
                    listOfUser.append('{},{}'.format(mobile, each[2]))
        return listOfUser

    @staticmethod
    def createCSVUsingList(listOfUsers, append=''):
        filePath = constant.autoTempFilePath + 'AutoList_{}'.format(int(time.time() * 1000)) + append
        file = FileHelper(filePath)
        for each in listOfUsers:
            file.appendToFile(each)
        return filePath

    @staticmethod
    def createPayloadForSpecificCase(case, identifier='mobile'):
        if case.lower() == 'duplicateuserwithbulkemail':
            filePath = CreateAudience.createCSVUsingList(
                ['automation1@gmail.com,Automation', 'automation2@gmail.com,Automation',
                 'automation3@gmail.com,Automation', 'automation1@gmail.com,Automation',
                 'automation2@gmail.com,Automation', 'automation1@gmail.com,Automation',
                 'automation1@gmail.com,Automation', 'automation4@gmail.com,Automation'] * 1000)
        if case.lower() == 'duplicateuserwithbulk':
            filePath = CreateAudience.createCSVUsingList(
                ['8497846843,Automation', '8497846842,Automation', '8497846841,Automation', '8497846843,Automation',
                 '8497846842,Automation', '8497846843,Automation', '8497846843,Automation',
                 '8497846840,Automation'] * 1000)
        if case.lower() == 'invalid_mobile':
            filePath = CreateAudience.createCSVUsingList(
                ['8497846843,Automation', '915000000005,User1', '5000000005,User2', '91600000000,User3',
                 '600000000,User4'])
        if case.lower() == 'invalid_email':
            filePath = CreateAudience.createCSVUsingList(
                ['automationaa.user@gmail.com,Automation', 'autoemaiaal7022014000,User1',
                 'autoemaaail7022014001@,User2',
                 'autoemailb7022014002a1a@gmail,User3', 'autoemaaail7022014003@b.,User4',
                 'autoemaialaa+7022014005@123.123.123.123,User5'])
        if case.lower() == 'empty_mobile':
            filePath = CreateAudience.createCSVUsingList(['8497846843,Automation', ',User1WithoutMobile'])
        if case.lower() == 'empty_mobile_bulk':
            filePath = CreateAudience.createCSVUsingList(
                ['8497846843,Automation', ',User1WithoutMobile', '8497846843,Automation'] * 1000)
        if case.lower() == 'duplicatemobile_withoutcountrycode':
            filePath = CreateAudience.createCSVUsingList(['8497846843,Automation', '8497846843,Automation'])
        if case.lower() == 'duplicatemobile_withcountrycode':
            filePath = CreateAudience.createCSVUsingList(['918497846843,Automation', '918497846843,Automation'])
        if case.lower() == 'duplicatemobile_with_withoutcountrycode':
            filePath = CreateAudience.createCSVUsingList(['8497846843,Automation', '918497846843,Automation'])
        if case.lower() == 'duplicatemobile_multipletimessamenumber':
            filePath = CreateAudience.createCSVUsingList(
                ['8497846843,Automation', '918497846843,Automation', '8497846843,Automation',
                 '918497846843,Automation'])
        if case.lower() == 'first_name_empty':
            filePath = CreateAudience.createCSVUsingList(['8497846843,', '8497846843,Automation'])
        if case.lower() == 'first_name_exceed_100character':
            filePath = CreateAudience.createCSVUsingList(
                ['8497846843,Automation', '8497846843,{}'.format('Automation' * 26)])
        if case.lower() == 'data_does_not_match_schema':
            filePath = CreateAudience.createCSVUsingList(
                ['8497846844', '8497846843,Automation,Automation,auto.list@gmail.com'])
        if case.lower() == 'multiple_data_does_not_match_schema':
            filePath = CreateAudience.createCSVUsingList(
                ['8497846844', '8497846843,Automation,Automation,auto.list@gmail.com',
                 '8497846845,Automation,Automation,auto.list@gmail.com',
                 '8497846846,Automation,Automation,auto.list@gmail.com'])
        if case.lower() == 'multiple_error_in_same_file':
            filePath = CreateAudience.createCSVUsingList(
                ['8497846843,Automation', '915000000005,User1', ',User1WithoutMobile', '8497846843,Automation'])
        if case.lower() == 'multiple_error_in_same_file_bulk':
            filePath = CreateAudience.createCSVUsingList(
                ['915000000005,User1', ',User1WithoutMobile', '8497846843,Automation',
                 '8497846843,Automation'] * 15000 + ['8497846843,Automation'])
        if case.lower() == 'multiple_error_in_same_file_email':
            filePath = CreateAudience.createCSVUsingList(
                ['automation.user@gmail.com,User1', ',User1WithoutMobile', 'automation.user@gmail.com,User2',
                 'autoemail7022014000,User3'])
        if case.lower() == 'invalid_userid':
            validUserId = list_Calls().getExistingUsers(1, offset=0)[0][0]
            filePath = CreateAudience.createCSVUsingList(
                ['{},{}'.format(validUserId, 'ValidAutomationUser'), '-1,InvalidUserId'])
        if case.lower() == 'multiple_error_in_same_file_userid':
            validUserId = list_Calls().getExistingUsers(1, offset=0)[0][0]
            filePath = CreateAudience.createCSVUsingList(
                ['{},{}'.format(validUserId, 'ValidAutomationUser'), '-1,InvalidUserId',
                 '{},{}'.format(validUserId, 'ValidAutomationUser')])
        if case.lower() == 'invalid_externalid':
            validExternalId = list_Calls().getExistingUsers(1, offset=0)[0][5]
            filePath = CreateAudience.createCSVUsingList(
                ['{},{}'.format(validExternalId, 'ValidAutomationUser'), '-1,InvalidUserId'])
        if case.lower() == 'multiple_error_in_same_file_externalid':
            validExternalId = list_Calls().getExistingUsers(1, offset=0)[0][5]
            filePath = CreateAudience.createCSVUsingList(
                ['{},{}'.format(validExternalId, 'ValidAutomationUser'), '-1,InvalidUserId',
                 '{},{}'.format(validExternalId, 'ValidAutomationUser')])

        audiencegroupbody = copy.deepcopy(constant.payload['audiencegroupbody'])
        audiencegroupbody['label'] = "AutomationListInvalidMobileNumber_{}".format(int(time.time() * 1000))
        if identifier == 'email':
            audiencegroupbody['data']['schema']['identifier'] = ["EMAIL"]
            audiencegroupbody['data']['schema']['data'] = ["EMAIL", "FIRST_NAME"]
        if identifier == 'userid':
            audiencegroupbody['data']['schema']['identifier'] = ["USER_ID"]
            audiencegroupbody['data']['schema']['data'] = ["USER_ID", "FIRST_NAME"]
        if identifier == 'externalid':
            audiencegroupbody['data']['schema']['identifier'] = ["EXTERNAL_ID"]
            audiencegroupbody['data']['schema']['data'] = ["EXTERNAL_ID", "FIRST_NAME"]

        payload = CreateAudience.createFinalPayload(audiencegroupbody, numberOfUsers=10, newUser=True, numberOfFiles=0,
                                                    popFields=[])
        payload.append(('file', (filePath.split('/')[-1], open(filePath, 'r'), 'text/csv')))
        return payload, filePath

    @staticmethod
    def createPayloadWithMultipleFilesForSpecificCase(case):
        if case.lower() == 'invalid_mobile':
            filePath_1 = CreateAudience.createCSVUsingList(
                ['8497846843,Automation', '915000000005,User1', '5000000005,User2', '91600000000,User3',
                 '600000000,User4'], append='case1')
            filePath_2 = CreateAudience.createCSVUsingList(
                ['8497846842,Automation', '915000000005,User1', '5000000005,User2', '91600000000,User3',
                 '600000000,User4'], append='case2')
        if case.lower() == 'empty_mobile':
            filePath_1 = CreateAudience.createCSVUsingList(['8497846843,Automation', ',User1WithoutMobile'],
                                                           append='case1')
            filePath_2 = CreateAudience.createCSVUsingList(['8497846842,Automation', ',User1WithoutMobile'],
                                                           append='case2')
        if case.lower() == 'empty_mobile_bulk':
            filePath_1 = CreateAudience.createCSVUsingList(
                [',User1WithoutMobile', '8497846843,Automation'] * 1000 + ['8497846843,Automation'], append='case1')
            filePath_2 = CreateAudience.createCSVUsingList(
                [',User1WithoutMobile', '8497846842,Automation'] * 1000 + ['8497846842,Automation'], append='case2')
        if case.lower() == 'duplicatemobile_withoutcountrycode':
            filePath_1 = CreateAudience.createCSVUsingList(['8497846843,Automation', '8497846843,Automation'],
                                                           append='case1')
            filePath_2 = CreateAudience.createCSVUsingList(['8497846842,Automation', '8497846842,Automation'],
                                                           append='case2')
        if case.lower() == 'duplicatemobile_withcountrycode':
            filePath_1 = CreateAudience.createCSVUsingList(['918497846843,Automation', '918497846843,Automation'],
                                                           append='case1')
            filePath_2 = CreateAudience.createCSVUsingList(['918497846842,Automation', '8497846842,Automation'],
                                                           append='case2')
        if case.lower() == 'duplicatemobile_with_withoutcountrycode':
            filePath_1 = CreateAudience.createCSVUsingList(['8497846843,Automation', '918497846843,Automation'],
                                                           append='case1')
            filePath_2 = CreateAudience.createCSVUsingList(['8497846842,Automation', '8497846842,Automation'],
                                                           append='case2')
        if case.lower() == 'duplicatemobile_multipletimessamenumber':
            filePath_1 = CreateAudience.createCSVUsingList(
                ['8497846843,Automation', '918497846843,Automation', '8497846843,Automation',
                 '918497846843,Automation'], append='case1')
            filePath_2 = CreateAudience.createCSVUsingList(
                ['8497846842,Automation', '918497846842,Automation', '8497846842,Automation',
                 '918497846842,Automation'], append='case2')
        if case.lower() == 'first_name_empty':
            filePath_1 = CreateAudience.createCSVUsingList(['8497846843,', '8497846843,Automation'], append='case1')
            filePath_2 = CreateAudience.createCSVUsingList(['8497846842,', '8497846842,Automation'], append='case2')
        if case.lower() == 'first_name_exceed_100character':
            filePath_1 = CreateAudience.createCSVUsingList(
                ['8497846843,Automation', '8497846843,{}'.format('Automation' * 26)], append='case1')
            filePath_2 = CreateAudience.createCSVUsingList(
                ['8497846842,Automation', '8497846843,{}'.format('Automation' * 26)], append='case2')
        if case.lower() == 'data_does_not_match_schema':
            filePath_1 = CreateAudience.createCSVUsingList(
                ['8497846842', '8497846843,Automation,Automation,auto.list@gmail.com'], append='case1')
            filePath_2 = CreateAudience.createCSVUsingList(
                ['8497846844', '8497846845,Automation,Automation,auto.list@gmail.com'], append='case2')
        if case.lower() == 'multiple_data_does_not_match_schema':
            filePath_1 = CreateAudience.createCSVUsingList(
                ['8497846842', '8497846843,Automation,Automation,auto.list@gmail.com',
                 '8497846844,Automation,auto.list@gmail.com',
                 '8497846845,Automation,auto.list@gmail.com'], append='case1')
            filePath_2 = CreateAudience.createCSVUsingList(
                ['8497846849', '8497846846,Automation,Automation,auto.list@gmail.com',
                 '8497846847,Automation,Automation,auto.list@gmail.com',
                 '8497846848,Automation,Automation,auto.list@gmail.com'], append='case2')
        if case.lower() == 'multiple_error_in_same_file':
            filePath_1 = CreateAudience.createCSVUsingList(
                ['8497846843,Automation', '915000000005,User1', ',User1WithoutMobile', '8497846843,Automation'],
                append='case1')
            filePath_2 = CreateAudience.createCSVUsingList(
                ['8497846842,Automation', '915000000005,User1', ',User1WithoutMobile', '8497846842,Automation'],
                append='case2')
        if case.lower() == 'multiple_error_in_same_file_bulk':
            filePath_1 = CreateAudience.createCSVUsingList(
                ['915000000005,User1', ',User1WithoutMobile', '8497846843,Automation',
                 '8497846843,Automation'] * 15000 + ['8497846843,Automation'], append='case1')
            filePath_2 = CreateAudience.createCSVUsingList(
                ['915000000005,User1', ',User1WithoutMobile', '8497846842,Automation',
                 '8497846842,Automation'] * 15000 + ['8497846842,Automation'], append='case2')

        audiencegroupbody = copy.deepcopy(constant.payload['audiencegroupbody'])
        audiencegroupbody['label'] = "AutomationListInvalidMobileNumber_{}".format(int(time.time() * 1000))
        payload = CreateAudience.createFinalPayload(audiencegroupbody, numberOfUsers=10, newUser=True, numberOfFiles=0,
                                                    popFields=[])
        payload.append(('file', (filePath_1.split('/')[-1], open(filePath_1, 'rb'), 'text/csv')))
        payload.append(('file', (filePath_2.split('/')[-1], open(filePath_2, 'rb'), 'text/csv')))

        return payload, filePath_1, filePath_2

    @staticmethod
    def userListSplit(userList, listType = 'DERIVED', splitIndex = None):
        if listType == 'DERIVED':
            userIds = []
            for record in userList:
                if type(record) == int:
                    userIds.append(record)
                else:
                    record = (record.encode('utf-8')).split(',')
                    try:
                        if '@' in record[0]:
                            userIds.append(record[0])
                        else:
                            userIds.append(int(record[0]))
                    except:
                        if '@' in record[1]:
                            userIds.append(record[1])
                        else:
                            userIds.append(int(record[1]))
            return userIds
        elif listType == 'ORG_USERS':
            if splitIndex != None:
                strIndexing = splitIndex.split(':')
                if strIndexing[0] != '':
                    return userList[int(strIndexing[0]):]
                else:
                    return userList[: int(strIndexing[1])]
            else:
                return userList
