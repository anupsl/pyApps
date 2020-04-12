import pytest
from src.Constant.constant import constant
from src.modules.irisv2.list.createAudience import CreateAudience
from src.modules.irisv2.list.getAudienceById import GetAudienceById
from src.modules.irisv2.list.getListDBAssertion import GetListDBAssertion
from src.utilities.logger import Logger

@pytest.mark.run(order=15)
class Test_GetAudienceById_FilterBased():
    def setup_method(self, method):
        Logger.logMethodName(method.__name__)

    @pytest.mark.parametrize('campaignType,testControlType', [
        ('LIVE', 'ORG'),

    ])
    def test_irisV2_getAudienceById_Filter_Sanity(self, campaignType, testControlType):
        list = CreateAudience.FilterList(campaignType, testControlType, campaignCheck=False)
        CreateAudience.waitForGVDToBeUpdated(list['ID'], checkParams=False)
        response = GetAudienceById.getById(list['ID'])
        GetAudienceById.assertResponse(response, 200)
        GetListDBAssertion(list['ID'], response,bucketUsed=constant.orgDetails[constant.config['cluster']][constant.config['orgId']]['s3BucketName'],createAudienceJob=False).check()

    @pytest.mark.parametrize('campaignType,testControlType', [

        ('UPCOMING', 'ORG'),
        ('LAPSED', 'ORG'),
        ('LIVE', 'CUSTOM'),
        ('UPCOMING', 'CUSTOM'),
        ('LAPSED', 'CUSTOM'),
        ('LIVE', 'SKIP'),
        ('UPCOMING', 'SKIP'),
        ('LAPSED', 'SKIP')
    ])
    def test_irisV2_getAudienceById_Filter(self, campaignType, testControlType):
        list = CreateAudience.FilterList(campaignType, testControlType, campaignCheck=False)
        CreateAudience.waitForGVDToBeUpdated(list['ID'], checkParams=False)
        response = GetAudienceById.getById(list['ID'])
        GetAudienceById.assertResponse(response, 200)
        GetListDBAssertion(list['ID'], response,
                           bucketUsed=constant.orgDetails[constant.config['cluster']][constant.config['orgId']][
                               's3BucketName'], createAudienceJob=False).check()