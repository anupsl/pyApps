import pytest, time, pytest_ordering
from src.Constant.constant import constant
from src.modules.iris.campaigns import campaigns
from src.modules.iris.dbCallsCampaign import dbCallsCampaign
from src.utilities.logger import Logger
from src.modules.iris.construct import construct

@pytest.mark.run(order=6)
class Test_GetCampaignId():
    
    def setup_method(self, method):
        Logger.logMethodName(method.__name__)
    
    @pytest.mark.parametrize('campaignType', [
         (['LIVE', 'ORG'])
         ])
    def test_getCampaign_Sanity(self, campaignType):
        response, payload = campaigns.createCampaign(campaignTypeParams=campaignType)
        campaigns.assertCreateCampaign(response, 200)
        getCampaignResponse = campaigns.getCampaignById(campaignId=response.get('json').get('entity').get('campaignId'))
        campaigns.assertGetCampaign(getCampaignResponse, 200)
        campaigns.assertGetCampaignDBCall(getCampaignResponse, response.get('json').get('entity').get('campaignId'))
    
    @pytest.mark.parametrize('campaignType', [
         (['LIVE', 'CUSTOM']),
         (['LIVE', 'SKIP']),
         (['UPCOMING', 'ORG']),
         (['UPCOMING', 'CUSTOM']),
         (['UPCOMING', 'SKIP']),
         (['LAPSED', 'ORG']),
         (['LAPSED', 'CUSTOM']),
         (['LAPSED', 'SKIP']),
         ])
    def test_getCampaignOfDifferentCampaignTypes(self, campaignType):
        response, payload = campaigns.createCampaign(campaignTypeParams=campaignType)
        campaigns.assertCreateCampaign(response, 200)
        getCampaignResponse = campaigns.getCampaignById(campaignId=response.get('json').get('entity').get('campaignId'))
        campaigns.assertGetCampaign(getCampaignResponse, 200)
        campaigns.assertGetCampaignDBCall(getCampaignResponse, response.get('json').get('entity').get('campaignId'))
    
    @pytest.mark.parametrize('description,payloadToUpload,campaignType', [
        ('Campaign name Update ', {'name':'updateCampaign_testGetCampaign_Live' + str(int(time.time()))}, ['LIVE', 'ORG']),
        ('Campaign Start Date Update', {'startDate':int(time.time() * 1000 + 24 * 60)}, ['LIVE', 'ORG']),
        ('Campaign End Date Update', {'endDate':int(time.time() * 1000 + 24 * 60 * 60 * 1000 * 2)}, ['LIVE', 'ORG']),
        ('Campaign GoalId Update', {'goalId': constant.irisGenericValues['goalId']}, ['LIVE', 'ORG']),
        ('Campaign ObjectiveId Update', {'objectiveId':constant.irisGenericValues['objectiveId']}, ['LIVE', 'ORG']),
        ('Campaign name Update ', {'name':'updateCampaign_testGetCampaign_upcoming' + str(int(time.time()))}, ['UPCOMING', 'ORG']),
        ('Campaign GoalId Update', {'goalId':constant.irisGenericValues['goalId']}, ['UPCOMING', 'ORG']),
        ('Campaign name Update ', {'name':'updateCampaign_testGetCampaign_lapsed' + str(int(time.time()))}, ['LAPSED', 'ORG']),
        ('Campaign GoalId Update', {'goalId':constant.irisGenericValues['goalId']}, ['LAPSED', 'ORG']),
        ])    
    def test_getCampaign_updateCampaign(self, description, payloadToUpload, campaignType):
        updateResponse, createResponse, updatePayload, createPayload = campaigns.updateCampaign(payloadToUpload, campaignType=campaignType)
        Logger.log('updateResponse :{} , createResponse :{} , updatePayload :{} ,createPayload :{}'.format(updateResponse, createResponse, updatePayload, createPayload))
        campaigns.assertUpdateCampaign(updateResponse, createResponse, 200)
        if updateResponse.get('statusCode') == 200:
            createPayload.update(updatePayload)
            getCampaignResponse = campaigns.getCampaignById(campaignId=updateResponse.get('json').get('entity').get('campaignId'))
            campaigns.assertGetCampaign(getCampaignResponse, 200)
            campaigns.assertGetCampaignDBCall(getCampaignResponse, updateResponse.get('json').get('entity').get('campaignId'))
        else:
            Logger.log('Status Code for updateCampaign is not 200 so no call to Get Campaign for this case')
    
    @pytest.mark.parametrize('description,campaignId,statusCode,errorCode,errorMessage', [
        ('Campaign Id not in Org', 9999999, 404, 1007, 'Campaign Id Exception : No Campaign Exists For This Campaign Id'),
        ('Alphanumeric Campaign Id', 'alpha43', 400, 101, 'Invalid value for path param: campaign_id'),
        ('Negative Campaign id', -1, 400, 100, 'Invalid request : must be greater than or equal to 1'),
        ('Special Character in Campaign ID', 'spChar$*^', 400, 101, 'Invalid value for path param: campaign_id'),
        ('Float Value for Campaign Id', 23456.0, 400, 101, 'Invalid value for path param: campaign_id')
        ])
    def test_getCampaign_NegativeCases(self, description, campaignId, statusCode, errorCode, errorMessage):
        getCampaignResponse = campaigns.getCampaignById(campaignId=campaignId)
        campaigns.assertGetCampaign(getCampaignResponse, statusCode, errorCode, errorMessage)
        
    def test_getCampaign_PassingWorngOrg(self):
        response, payload = campaigns.createCampaign({'name':'IRIS_' + str(int(time.time())), 'goalId':str(dbCallsCampaign.getValidGoalId()), 'objectiveId': dbCallsCampaign.getValidObjectiveId()})
        campaigns.assertCreateCampaign(response, 200)
        previousOrgId = construct.updateOrgId(0)
        try:
            getCampaignResponse = campaigns.getCampaignById(campaignId=response.get('json').get('entity').get('campaignId'))
            campaigns.assertGetCampaign(getCampaignResponse, 400, 1007, 'Campaign Id Exception : No Campaign Exists For This Campaign Id')
        except AssertionError, exp:
            Logger.log('Assertion Failed as :', exp)
        finally:
            construct.updateOrgId(int(previousOrgId))
                
    
    
