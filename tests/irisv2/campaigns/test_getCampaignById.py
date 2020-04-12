import copy
import time

import pytest

from src.Constant.constant import constant
from src.dbCalls.campaignInfo import campaign_calls
from src.modules.irisv2.campaigns.createCampaign import CreateCampaign
from src.modules.irisv2.campaigns.getCampaignById import GetCampaign
from src.modules.irisv2.campaigns.getCampaignDBAssertion import GetCampaignDBAssertion
from src.modules.irisv2.helper.irisHelper import IrisHelper
from src.utilities.assertion import Assertion
from src.utilities.logger import Logger


@pytest.mark.run(order=5)
class Test_getCampaigns():
    def setup_method(self, method):
        Logger.logMethodName(method.__name__)

    @pytest.mark.parametrize('campaignType,testControlType', [
        ('LIVE', 'ORG'),

    ])
    def test_irisV2_getCampaign_ID_ProdSanity(self, campaignType, testControlType):
        campaignInfo = CreateCampaign.create(campaignType, testControlType)
        getCampaignInfoResponse = GetCampaign.getById(campaignInfo['ID'])
        GetCampaign.assertResponse(getCampaignInfoResponse, 200)
        GetCampaignDBAssertion(campaignInfo['ID'], getCampaignInfoResponse).check()

    @pytest.mark.parametrize('campaignType,testControlType', [

        ('LIVE', 'SKIP'),
        ('LIVE', 'CUSTOM'),
    ])
    def test_irisV2_getCampaign_ID(self, campaignType, testControlType):
        campaignInfo = CreateCampaign.create(campaignType, testControlType)
        getCampaignInfoResponse = GetCampaign.getById(campaignInfo['ID'])
        GetCampaign.assertResponse(getCampaignInfoResponse, 200)
        GetCampaignDBAssertion(campaignInfo['ID'], getCampaignInfoResponse).check()

    @pytest.mark.parametrize('campaignType,testControlType', [
        ('UPCOMING', 'ORG'),
        ('UPCOMING', 'SKIP'),
        ('UPCOMING', 'CUSTOM'),
        ('LAPSED', 'ORG'),
        ('LAPSED', 'SKIP'),
        ('LAPSED', 'CUSTOM')
    ])
    def test_irisV2_getCampaign_ID(self, campaignType, testControlType):
        campaignInfo = CreateCampaign.create(campaignType, testControlType)
        getCampaignInfoResponse = GetCampaign.getById(campaignInfo['ID'])
        GetCampaign.assertResponse(getCampaignInfoResponse, 200)
        GetCampaignDBAssertion(campaignInfo['ID'], getCampaignInfoResponse).check()

    @pytest.mark.parametrize('campaignType,testControlType,testPercentage', [
        ('LIVE', 'ORG', 100),
        ('LIVE', 'ORG', 1),
        ('LIVE', 'ORG', 0),
    ])
    def test_irisV2_getCampaign_ID_differentTestPercentage(self, campaignType, testControlType, testPercentage):
        campaignInfo = CreateCampaign.create('LIVE', 'ORG', testControlPercentage=testPercentage, updateNode=True,
                                             lockNode=True)
        getCampaignInfoResponse = GetCampaign.getById(campaignInfo['ID'])
        GetCampaign.assertResponse(getCampaignInfoResponse, 200)
        GetCampaignDBAssertion(campaignInfo['ID'], getCampaignInfoResponse).check()

    def test_irisV2_getCampaign_ID_V1_Campaigns(self):
        campaignId = campaign_calls().getLatestCampaignIdOfV1()
        getCampaignInfoResponse = GetCampaign.getById(campaignId)
        GetCampaign.assertResponse(getCampaignInfoResponse, 400, 1012,
                                   'Campaign not found : No Campaign Exists For This Campaign Id')

    def test_irisV2_getCampaign_ID_unknownCampaignId(self):
        getCampaignInfoResponse = GetCampaign.getById('9999999')
        GetCampaign.assertResponse(getCampaignInfoResponse, 400, 1012,
                                   'Campaign not found : No Campaign Exists For This Campaign Id')

    @pytest.mark.parametrize(
        'campaignId,statusCode,errorCode,errorDesc', [
            ('campaignId', 400, 103, 'Invalid value for path param: campaignId'),
            ('$###', 400, 103, 'Invalid value for path param: campaignId'),
            ('-1', 400, 102, 'Invalid request : CampaignId must be greater than or equal to 1')
        ])
    def test_irisV2_getCampaign_ID_invalidCampaignId(self, campaignId, statusCode, errorCode, errorDesc):
        getCampaignInfoResponse = GetCampaign.getById(campaignId)
        GetCampaign.assertResponse(getCampaignInfoResponse, statusCode, errorCode, errorDesc)

    def test_irisV2_getCampaign_ID_wrongAuth(self):
        previousUserName = None
        try:
            payload = copy.deepcopy(constant.payload['createcampaignv2'])
            payload.update({'name': 'test_irisV2_getCampaign_ID_wrongAuth_{}'.format(int(time.time()))})
            payload["testControl"].pop("testPercentage")
            campaignInfo = CreateCampaign.create('LIVE', 'ORG', payload=payload, updateNode=True, lockNode=True)
            previousUserName = IrisHelper.updateUserName('WrongName')
            getCampaignInfoResponse = GetCampaign.getById(campaignInfo['ID'])
            GetCampaign.assertResponse(getCampaignInfoResponse, 401, 999999,
                                       'Unauthorized')
        except Exception, exp:
            Assertion.constructAssertion(False, 'Exception :{}'.format(exp))
        finally:
            if previousUserName is not None: IrisHelper.updateUserName(previousUserName)



    @pytest.mark.parametrize('campaignType,testControlType', [

        ('LIVE', 'ORG')

    ])
    def test_irisV2_getCampaign_byId_for_Objective_and_GA(self, campaignType, testControlType):
        payload = copy.deepcopy(constant.payload['createcampaignv2'])
        payload.update({
            "name": "Automation_IRISV2_{}".format(int(time.time() * 1000)),
            "objective": {
                "objectiveName": "Boost_Sales"
            },
            "gaEnabled": "true",
            "gaSource": "test gaSource",
            "gaName": "test gaName"

        })
        payload["testControl"].pop("testPercentage")
        campaignInfo = CreateCampaign.create(campaignType, testControlType, payload=payload, updateNode=True,
                                             lockNode=True)
        getCampaignInfoResponse = GetCampaign.getById(campaignInfo['ID'])
        GetCampaign.assertResponse(getCampaignInfoResponse, 200)
        GetCampaignDBAssertion(campaignInfo['ID'], getCampaignInfoResponse).check()
