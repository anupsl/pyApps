import pytest
from src.modules.irisv2.list.createAudience import CreateAudience
from src.modules.irisv2.list.createAudienceDBAssertion import CreateAudienceDBAssertion
from src.utilities.logger import Logger
from src.utilities.awsHelper import AWSHelper
from src.Constant.constant import constant


@pytest.mark.run(order=10)
class Test_CreateAudience_FilterBased():

    def setup_class(self):
        Logger.log('Getting Uploaded User list by filters')
        self.filterUserList = (filter(None, AWSHelper.readFileFromS3(bucketName=constant.orgDetails[constant.config['cluster']][constant.config['orgId']]['s3BucketName'],
                                                   keyName=constant.orgDetails[constant.config['cluster']][constant.config['orgId']]['s3KeyName'])))

    def setup_method(self, method):
        Logger.logMethodName(method.__name__)

    @pytest.mark.parametrize('campaignType,testControlType,listType', [
        ('LIVE', 'ORG', 'FILTER_BASED')
    ])
    def test_irisV2_createAudience_Filter_Sanity(self, campaignType, testControlType, listType):
        list = CreateAudience.FilterList(campaignType, testControlType, campaignCheck=False)
        CreateAudience.waitForGVDToBeUpdated(list['ID'])
        CreateAudienceDBAssertion(list['ID'], list, listType, len(self.filterUserList), reachabilityCheck=True).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType', [
        ('UPCOMING', 'ORG', 'FILTER_BASED'),
        ('LAPSED', 'ORG', 'FILTER_BASED'),
        ('LIVE', 'CUSTOM', 'FILTER_BASED'),
        ('UPCOMING', 'CUSTOM', 'FILTER_BASED'),
        ('LAPSED', 'CUSTOM', 'FILTER_BASED'),
        ('LIVE', 'SKIP', 'FILTER_BASED'),
        ('UPCOMING', 'SKIP', 'FILTER_BASED'),
        ('LAPSED', 'SKIP', 'FILTER_BASED')
    ])
    def test_irisV2_createAudience_Filter(self, campaignType, testControlType, listType):
        list = CreateAudience.FilterList(campaignType, testControlType, campaignCheck=False)
        CreateAudience.waitForGVDToBeUpdated(list['ID'])
        CreateAudienceDBAssertion(list['ID'], list, listType, len(self.filterUserList), reachabilityCheck=True).check()