from src.Constant.constant import constant
import json

from src.Constant.constant import constant
from src.dbCalls.campaignShard import meta_details
from src.utilities.assertion import Assertion


class CreateAudienceDBAssertion():
    def __init__(self, groupId, listInfo, listType, numberOfUser, numberOfCustomTag=None, groupDetails=True,
                 groupVersionDetails=True, campaignHashLookUp=False, createAudienceJob=False, reachabilityCheck=False,
                 bucketDetails=False, isGVUpdated=False):
        self.metaInfoFromDB = meta_details(groupId=groupId, groupDetails=groupDetails,
                                           groupVersionDetails=groupVersionDetails,
                                           campaignHashLookUp=campaignHashLookUp, createAudienceJob=createAudienceJob,
                                           reachabilityCheck=reachabilityCheck, bucketDetails=bucketDetails).metaDetail
        self.listType = listType
        self.listInfo = listInfo
        self.numberOfUser = numberOfUser
        self.numberOfCustomTag = numberOfCustomTag
        self.isGVUpdated = isGVUpdated

    def check(self):
        self.validateGroupDetails()
        self.validateGroupVersionDetails()
        if self.numberOfUser > 0: self.validateParams()
        if self.numberOfCustomTag is not None: self.validateCountOfCustomtag()

    def validateGroupDetails(self):
        Assertion.constructAssertion(self.metaInfoFromDB['groupDetails']['org_id'] == constant.config['orgId'],
                                     'OrgId :{} matched in groupDetails'.format(constant.config['orgId']))
        Assertion.constructAssertion(self.metaInfoFromDB['groupDetails']['is_reloading'] == 0,
                                     'Is Reloading is 0 when list is created')
        Assertion.constructAssertion(self.metaInfoFromDB['groupDetails']['is_visible'] == 1,
                                     'Is Visible is 1 when list is created')
        Assertion.constructAssertion(self.metaInfoFromDB['groupDetails']['type'] == self.listType,
                                     'List Type :{} with groupId'.format(self.listType, self.metaInfoFromDB['groupId']))
        if self.listType == 'FILTER_BASED':
            Assertion.constructAssertion(self.metaInfoFromDB['groupDetails']['uuid'] == self.listInfo['UUID'],
                                         'UUID For FilterBased List in DB :{} and in payload :{}'.format(
                                             self.metaInfoFromDB['groupDetails']['uuid'],self.listInfo['UUID']))

    def validateGroupVersionDetails(self):
        Assertion.constructAssertion(self.metaInfoFromDB['groupVersionDetails']['TEST']['id'] == self.listInfo['VID'],
                                     'Group Version ID from response :{} and in DB :{}'.format(self.listInfo['VID'],
                                                                                               self.metaInfoFromDB[
                                                                                                   'groupVersionDetails'][
                                                                                                   'TEST']['id']))
        Assertion.constructAssertion(
            self.metaInfoFromDB['groupVersionDetails']['TEST']['customer_count'] == self.numberOfUser,
            'Customer Count from DB :{} and passed :{}'.format(
                self.metaInfoFromDB['groupVersionDetails']['TEST']['customer_count'], self.numberOfUser),verify=True)
        Assertion.constructAssertion(self.metaInfoFromDB['groupVersionDetails']['TEST']['bucket_id'] > 0,
                                     'Bucket Id is greate than 0 ')
        Assertion.constructAssertion(self.metaInfoFromDB['groupVersionDetails']['TEST']['is_active'] == 1,
                                     'Is Active is 1 for fresh created List')
        if not self.isGVUpdated:
            Assertion.constructAssertion(self.metaInfoFromDB['groupVersionDetails']['TEST']['version_number'] == 0,
                                         'Version number is 0 for fresh created List')
        else:
            Assertion.constructAssertion(self.metaInfoFromDB['groupVersionDetails']['TEST']['version_number'] != 0,
                                         'Version number is {} for refresh existing List'.format(
                                             self.metaInfoFromDB['groupVersionDetails']['TEST']['version_number']))

    def validateParams(self):
        params_dict = json.loads(self.metaInfoFromDB['groupVersionDetails']['TEST']['params'])
        Assertion.constructAssertion(params_dict['test_count'] + params_dict['control_count'] == self.numberOfUser,
                                     'Test Count :{} and Control Count :{} and totalNumberOfuser :{}'.format(
                                         params_dict['test_count'], params_dict['control_count'], self.numberOfUser))

    def validateCountOfCustomtag(self):
        Assertion.constructAssertion(self.metaInfoFromDB['groupDetails']['custom_tag_count'] == self.numberOfCustomTag,
                                     'Actual Number Of Custom tags :{} and Expected :{}'.format(
                                         self.metaInfoFromDB['groupDetails']['custom_tag_count'],
                                         self.numberOfCustomTag))
