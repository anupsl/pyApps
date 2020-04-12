import pytest, time

from src.utilities.dbhelper import dbHelper
from src.Constant.constant import constant
from src.modules.iris.campaigns import campaigns
from src.modules.iris.authorize import authorize
from src.modules.campaign_shard.campaignShardHelper import CampaignShardHelper
from src.utilities.assertion import Assertion
from src.utilities.logger import Logger

@pytest.mark.run(order=2)
class Test_Veneno_RECURRING_performance():

    def setup_class(self):
        if 'storeType' in constant.payload['createmessage']: constant.payload['createmessage'].pop('storeType')
        campaignResponse, campaignPayload = campaigns.createCampaign(
            {'name': 'IRIS_' + str(int(time.time() * 100000)), 'goalId': constant.irisGenericValues['goalId'],
             'objectiveId': constant.irisGenericValues['objectiveId'], 'testControl': {'type': 'ORG', 'test': 90}})
        self.campaignId = campaignResponse['json']['entity']['campaignId']
        self.groupVersionResult = None
        self.bucketId = None
        self.voucherId=None
        self.strategy = None
        self.node = list()


    @pytest.mark.parametrize('description,messageInfo', [
        ('MessageType-Immediate-Plain', ['SMS', ['RECURRING'], ['PLAIN'], True])
    ]*1)
    def test_veneno_recurring(self, description, messageInfo):
        detailsOfFilterListCreated = CampaignShardHelper.createFilterList(self.campaignId,
                                                                          'test_list_{}'.format(int(time.time())))
        self.listId= detailsOfFilterListCreated['groupDetails']['id']
        authorizeResult = authorize.authorizeCampaign(self, messageInfo, False)
        authorize.assertAuthorize(authorizeResult['authorizeResponse'], 200)

        self.node.append([self.listId,detailsOfFilterListCreated,authorizeResult])

    @pytest.mark.parametrize('nodes', [
        ('nodes')] * 1)
    def test_veneno_dbAssertionForAllNodes(self,nodes):
        detailsToVerify = self.node.pop(0)
        self.validateDBAssertion(detailsToVerify)


    def validateDBAssertion(self,details):
        self.validatePrecheck(details[2]['messageId'])
        self.validateNewVersionForList(details[0])

    def validatePrecheck(self,messageId):
        query = "select status,error from precheck_processing_log where message_id = {}".format(messageId)
        for each in range(80):
            result = dbHelper.queryDB(query, 'msging')
            if len(result) !=0 and result[0][0] != 'USER_REFRESH':

                break
            else:
                time.sleep(25)
        Logger.log('result isssssssssss',result)
        Assertion.constructAssertion(result[0][0]=='CLOSED','Status in Precheck Processing Logs for MessageId :{} is {}'.format(messageId,result[0][0]))
        Assertion.constructAssertion(result[0][1] == '','No error in Precheck Processing Logs for MessageId :{} is {}'.format(messageId,result[0][1]))

    def validateNewVersionForList(self,groupId):
        query = "select * from group_version_details where group_id = {} and org_id = {} and version_number=1 and is_active=1".format(groupId,constant.config['orgId'])
        result = dbHelper.queryDB(query, 'campaign_meta_details')
        Logger.log('GroupVersionDetail Result with Version 1 is :{}'.format(result))
        Assertion.constructAssertion(len(result) is not 0, 'Validating Group Version with New Version is Created')

