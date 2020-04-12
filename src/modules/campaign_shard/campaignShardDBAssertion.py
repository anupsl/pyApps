import json

from src.Constant.constant import constant
from src.modules.iris.dbCallsCampaign import dbCallsCampaign
from src.modules.iris.dbCallsList import dbCallsList
from src.utilities.assertion import Assertion
from src.utilities.logger import Logger


class CampaignShardDBAssertion():
    def __init__(self, campaignId, testControlType, listType, listName, listId, userDataSchema, usersDataPassed,
                 numberOfCustomTags=0, numberOfGroupTags=0, derived=False, newFlow=False):
        Logger.log(
            "Campaign Shard DB Assertion Initialized for details : campaignId :{} , testControlType :{} , listtype :{} ,listname :{} , listId :{} , userDataSchema :{} , userDataPassed :{} , numberOfCustomTags :{} , numberofGroupTags :{}".format(
                campaignId, testControlType, listType, listName, listId, userDataSchema, usersDataPassed,
                numberOfCustomTags, numberOfGroupTags))
        self.campaignId = campaignId
        self.listType = listType
        self.testControlType = testControlType
        self.listName = listName
        self.listId = listId
        self.userDataSchema = userDataSchema
        self.usersDataPassed = usersDataPassed
        self.derivedList = derived
        self.newFlow = newFlow
        self.numberOfUsers = len(usersDataPassed)
        self.numberOfCustomTags = numberOfCustomTags
        self.numberOfGroupTags = numberOfGroupTags
        self.formDefaultValueAsPerListType()
        self.getDBInformationRelatedToCampaignShard()
        self.getTestPercentageOfCampaign()
        self.calculateTestAndControlUser()
        self.getUniqueHashLookups()

    def check(self):
        self.assertGroupDetails()
        self.assertGroupVersionBasedOnTestControlType()
        if self.numberOfUsers > 0: self.assertCampaignGroupRecipient()
        if self.numberOfCustomTags > 0: self.assertCampaignGroupRecipientForCustomTags()

    def getDBInformationRelatedToCampaignShard(self):
        self.hashLookupDetails = dbCallsList.getHashLookUp()
        self.groupDetailResult = dbCallsList.getGroupDetailsWithListId(self.listId)
        self.groupVersionDetailResult = dbCallsList.getGroupVersionDetailsWithGroupId(self.listId)

    def formDefaultValueAsPerListType(self):
        if self.listType.lower() == 'upload':
            self.listType = {'type': 'upload', 'groupDetailType': 'CAMPAIGN_USERS'}
        elif self.listType.lower() == 'filter_based':
            self.listType = {'type': 'filter_based', 'groupDetailType': 'FILTER_BASED'}
        elif self.listType.lower() == 'loyalty':
            if self.derivedList:
                Logger.log(
                    'Due to Condition DerivedList :{} and testControlType :{} setting groupDetailsType as CAMPAIGN_USERS'.format(
                        self.derivedList, self.testControlType))
                self.listType = {'type': 'loyalty', 'groupDetailType': 'CAMPAIGN_USERS'}
            else:
                Logger.log(
                    'Due to Condition DerivedList :{} and testControlType :{} setting groupDetailsType as LOYALTY'.format(
                        self.derivedList, self.testControlType))
                self.listType = {'type': 'loyalty', 'groupDetailType': 'LOYALTY'}
        elif self.listType.lower() == 'nonloyalty':
            if self.derivedList:
                self.listType = {'type': 'nonloyalty', 'groupDetailType': 'CAMPAIGN_USERS'}
            else:
                self.listType = {'type': 'nonloyalty', 'groupDetailType': 'NONLOYALTY'}

    def getTestPercentageOfCampaign(self):
        # self.testPercentage should come from ORG Config ,and this class should be independent of campaignID
        try:
            campaignBaseResult = dbCallsCampaign.getCampaignBaseFromCampaignId(self.campaignId)
            if campaignBaseResult['test_percentage'] is not None:
                self.testPercentage = int(campaignBaseResult['test_percentage'])
            else:
                self.testPercentage = 90
        except:
            self.testPercentage = 90

    def calculateTestAndControlUser(self):
        self.numberOfTestUsers = 0
        for eachSecretAValue in self.getSecretAValueOfUsersInList():
            if int(eachSecretAValue[0]) <= self.testPercentage:
                self.numberOfTestUsers = self.numberOfTestUsers + 1
        self.numberOfControlUsers = self.numberOfUsers - self.numberOfTestUsers

    def getSecretAValueOfUsersInList(self):
        allUsersValueToPassAsString = ""
        getSecretValueBasedOn = self.userDataSchema.split(',')[2]
        if len(self.usersDataPassed) == 0: return ()
        for eachUser in self.usersDataPassed:
            allUsersValueToPassAsString = allUsersValueToPassAsString + "'" + eachUser.split(',')[2] + "',"
        Logger.log(allUsersValueToPassAsString)
        return dbCallsList.getSecretA(getSecretValueBasedOn,
                                      allUsersValueToPassAsString[:len(allUsersValueToPassAsString) - 1])

    def getUniqueHashLookups(self):
        listOfUniqueValues = []
        for eachUniqueHashLookup in self.hashLookupDetails:
            if eachUniqueHashLookup.split('__')[2] not in listOfUniqueValues:
                listOfUniqueValues.append(self.hashLookupDetails[eachUniqueHashLookup])
        self.hashLookupDetails = listOfUniqueValues

    def assertGroupDetails(self):
        Assertion.constructAssertion(self.groupDetailResult['group_label'] == self.listName,
                                     'Matching List Name, actual:{} and expected: {}'.format(
                                         self.groupDetailResult['group_label'], self.listName))
        Assertion.constructAssertion(self.groupDetailResult['type'].upper() == self.listType['groupDetailType'],
                                     'Matching Type in Group Detail expected :{} and actually :{}'.format(
                                         self.listType['groupDetailType'], self.groupDetailResult['type'].upper()),verify=True)
        Assertion.constructAssertion(self.groupDetailResult['custom_tag_count'] == self.numberOfCustomTags,
                                     'Matching number Of Custom Tags in group Details :{} and actually passed :{}'.format(
                                         self.groupDetailResult['custom_tag_count'], self.numberOfCustomTags))
        # Assertion.constructAssertion(len(json.loads(self.groupDetailResult['group_tags'])) == self.numberOfGroupTags, 'Matching number Of Group Tags in group Details :{} and actually passed :{}'.format(self.groupDetailResult['custom_tag_count'] , self.numberOfCustomTags))

    def assertGroupVersionBasedOnTestControlType(self):
        Assertion.constructAssertion(int(self.groupVersionDetailResult['TEST']['bucket_id']) > 0,
                                     'BucketId should Always be greater then 0')
        Assertion.constructAssertion(self.groupVersionDetailResult['TEST']['customer_count'] in range(
            self.numberOfTestUsers + self.numberOfControlUsers - 2,
            self.numberOfTestUsers + self.numberOfControlUsers + 2),
                                     'Test Users Count in GroupVersion :{} and as per Test Control Calculation :{}'.format(
                                         self.groupVersionDetailResult['TEST']['customer_count'],
                                         self.numberOfTestUsers + self.numberOfControlUsers))
        paramsInfo = json.loads(self.groupVersionDetailResult['TEST']['params'])
        Assertion.constructAssertion(paramsInfo['test_count'] == self.numberOfTestUsers,
                                     'Test Count in params :{} and as per secretA Values :{}'.format(
                                         paramsInfo['test_count'], self.numberOfTestUsers))
        Assertion.constructAssertion(paramsInfo['control_count'] == self.numberOfControlUsers,
                                     'Control Count in params :{} and as per secretA Values :{}'.format(
                                         paramsInfo['control_count'], self.numberOfControlUsers))
        if self.testControlType.lower() != 'skip':
            if not self.newFlow: Assertion.constructAssertion(
                self.groupVersionDetailResult['CONTROL']['customer_count'] == 0,
                'Control Users Count in GroupVersion :{} and as per Test Control Calculation :{}'.format(
                    self.groupVersionDetailResult['CONTROL']['customer_count'], 0))

    def assertCampaignGroupRecipient(self):
        for eachUniqueHashId in self.hashLookupDetails:
            numberOfTestDataInCGR = dbCallsList.getCampaignGroupRecipient(
                self.groupVersionDetailResult['TEST']['bucket_id'], self.groupVersionDetailResult['TEST']['id'],
                eachUniqueHashId)
            Assertion.constructAssertion(
                numberOfTestDataInCGR[eachUniqueHashId]['userCount'] == self.groupVersionDetailResult['TEST'][
                    'customer_count'], 'Number Of Test Users in CGR :{} and expected :{}'.format(
                    numberOfTestDataInCGR[eachUniqueHashId]['userCount'],
                    self.groupVersionDetailResult['TEST']['customer_count']))
            reachabilityStatusForTestuser = self.getReachabilityStatus(
                numberOfTestDataInCGR[eachUniqueHashId]['reachability_type_id'])
            if constant.config['cluster'] == 'staging':
                Assertion.constructAssertion(reachabilityStatusForTestuser in ['SUBSCRIBED', None],
                                             'Reachability Status of Test Users :{}'.format(
                                                 reachabilityStatusForTestuser))
                if reachabilityStatusForTestuser is None: Assertion.addValidationMessage(
                    'Reachability Id is {} for hashId :{}'.format(reachabilityStatusForTestuser, eachUniqueHashId))
            else:
                Assertion.constructAssertion(reachabilityStatusForTestuser == 'SUBSCRIBED',
                                             'Reachability Status of Test Users :{}'.format(
                                                 reachabilityStatusForTestuser))

            testControlCount = dbCallsList.getCampaignGroupRecipientTestControlCount(
                self.groupVersionDetailResult['TEST']['bucket_id'], self.groupVersionDetailResult['TEST']['id'],
                eachUniqueHashId)
            Assertion.constructAssertion(testControlCount[1] == self.numberOfTestUsers,
                                         'Test Users in CGR :{} and as per secretA :{}'.format(testControlCount[1],
                                                                                               self.numberOfTestUsers))
            if 0 in testControlCount:  Assertion.constructAssertion(testControlCount[0] == self.numberOfControlUsers,
                                                                    'Control Users in CGR :{} and as per secretA :{}'.format(
                                                                        testControlCount[0], self.numberOfControlUsers))

    def getReachabilityStatus(self, reachabilityId):
        return dbCallsList.getReachabilityStatus(reachabilityId)

    def assertCampaignGroupRecipientForCustomTags(self):
        campaignGroupRecipientCustomTag = dbCallsList.getCampaignGroupRecipientForCustomTags(
            self.groupVersionDetailResult['TEST']['bucket_id'], self.groupVersionDetailResult['TEST']['id'])
        LengthOfCustomTags = 1
        customTagsValueToMatch = {}
        for eachSchemaValue in self.userDataSchema.split(','):
            if 'customTag' in eachSchemaValue:
                customTagsValueToMatch['custom_tag_' + str(LengthOfCustomTags)] = 'tag' + str(LengthOfCustomTags)
                LengthOfCustomTags = LengthOfCustomTags + 1
        Assertion.constructAssertion(len(campaignGroupRecipientCustomTag) == 1,
                                     'Matching For The Same GroupVersionId all CustomTags Value should be same in case of Automation Created')
        Assertion.constructAssertion(json.loads(campaignGroupRecipientCustomTag[0][0]) == customTagsValueToMatch,
                                     'Custom tag Value in CGR :{} and Validating with :{}'.format(
                                         campaignGroupRecipientCustomTag[0][0], customTagsValueToMatch))
        Assertion.constructAssertion(
            self.numberOfTestUsers + self.numberOfControlUsers == int(campaignGroupRecipientCustomTag[0][1]),
            'Matching Number of users in CGR in payload :{} and in DB :{} '.format(
                self.numberOfTestUsers + self.numberOfControlUsers, int(campaignGroupRecipientCustomTag[0][1])))

    def validateGroupStatus(self):
        if self.newFlow:
            Assertion.constructAssertion(self.groupVersionDetailResult['TEST']['status'] == 'ACTIVE',
                                         'Status of Group  is :{}'.format(
                                             self.groupVersionDetailResult['TEST']['status']))
