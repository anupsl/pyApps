import pytest, time, Queue, pytest_ordering
from threading import Thread
from src.Constant.constant import constant
from src.utilities.logger import Logger
from src.utilities.assertion import Assertion
from src.modules.iris.campaigns import campaigns
from src.modules.iris.dbCallsCampaign import dbCallsCampaign
from src.modules.iris.construct import construct

@pytest.mark.run(order=1)
class Test_CreateCampaign():
    
    def setup_method(self, method):
        Logger.logMethodName(method.__name__)
    
    def test_outboundCampaign_Sanity(self):
        response, payload = campaigns.createCampaign({'name':'IRIS_' + str(int(time.time() * 100000)), 'goalId':constant.irisGenericValues['goalId'], 'objectiveId':constant.irisGenericValues['objectiveId']})
        campaigns.assertCreateCampaign(response, 200)
        campaigns.assertCreateCampaignDBCall(response['json']['entity']['campaignId'], payload)

    @pytest.mark.parametrize('testControl', [
        ({'type' : 'ORG', 'test' : 90}),
        ({'type' : 'CUSTOM', 'test' : 90}),
        ({'type' : 'SKIP', 'test' : 90})
        ])
    def test_outboundCampaign_differentTestControl(self, testControl):
        response, payload = campaigns.createCampaign({'name':'IRIS_' + str(int(time.time() * 100000)), 'goalId':constant.irisGenericValues['goalId'], 'objectiveId':constant.irisGenericValues['objectiveId'], 'testControl':testControl})
        campaigns.assertCreateCampaign(response, 200)
        campaigns.assertCreateCampaignDBCall(response['json']['entity']['campaignId'], payload)
    
    def test_outboundCampaign_googleAnalytics(self):
        response, payload = campaigns.createCampaign({'name':'IRIS_' + str(int(time.time() * 100000)), 'goalId':constant.irisGenericValues['goalId'], 'objectiveId':constant.irisGenericValues['objectiveId'], 'gaName':'Test', 'gaSource':'Automation'})
        campaigns.assertCreateCampaign(response, 200)
        campaigns.assertCreateCampaignDBCall(response['json']['entity']['campaignId'], payload)
    
    def test_outboundCampaign_upcoming(self):
        response, payload = campaigns.createCampaign({'name':'IRIS_' + str(int(time.time() * 100000)), 'goalId':constant.irisGenericValues['goalId'], 'objectiveId':constant.irisGenericValues['objectiveId'], 'startDate':int(time.time() * 1000 + 24 * 60 * 60 * 1000), 'endDate':int(time.time() * 1000 + 24 * 60 * 60 * 2000)})
        campaigns.assertCreateCampaign(response, 200)
        campaigns.assertCreateCampaignDBCall(response['json']['entity']['campaignId'], payload)
    
    def test_outboundCampaign_differentName_parellelRequest(self):
        que = Queue.Queue()
        threads_list = list()
        
        for i in range(1, 11):
            threads_list.append(Thread(target=lambda q, arg1: q.put({'createCampaign': campaigns.createCampaign(arg1)}), args=(que, {'name':str(i) + '_' + str(int(time.time() * 100000)), 'goalId':constant.irisGenericValues['goalId'], 'objectiveId':constant.irisGenericValues['objectiveId']})))
        [x.start() for x in threads_list]
        [x.join() for x in threads_list]
        
        while not que.empty():
            result = que.get().get('createCampaign')
            Logger.log('Checking for Campaign Created:', result)
            campaigns.assertCreateCampaign(result[0], 200)
            campaigns.assertCreateCampaignDBCall(result[0]['json']['entity']['campaignId'], result[1])
            
    def test_outboundCampaign_sameName_SequentialRequest(self):
        response, payload = campaigns.createCampaign({'name':'IRIS_' + str(int(time.time() * 100000)), 'goalId':constant.irisGenericValues['goalId'], 'objectiveId':constant.irisGenericValues['objectiveId']})
        campaigns.assertCreateCampaign(response, 200)
        campaigns.assertCreateCampaignDBCall(response['json']['entity']['campaignId'], payload)
        response, payload = campaigns.createCampaign({'goalId':constant.irisGenericValues['goalId'], 'objectiveId':constant.irisGenericValues['objectiveId'], 'name':payload['name']})
        campaigns.assertCreateCampaign(response, 400, 1003, 'Campaign Name Exception : Campaign Name already exists')
    
    def test_outboundCampaign_sameDate(self):
        response, payload = campaigns.createCampaign({'name':'IRIS_sameDate_' + str(int(time.time() * 100000)), 'goalId':constant.irisGenericValues['goalId'], 'objectiveId':constant.irisGenericValues['objectiveId'], 'startDate':int(time.time() * 1000), 'endDate':int(time.time() * 1000)})
        campaigns.assertCreateCampaign(response, 400, 1006, 'Campaign Date Exception : Campaign End Date Cannot Be before Start Date')
       
    def test_outboundCampaign_lapsed(self):
        response = campaigns.createCampaign({'name':'IRIS_' + str(int(time.time() * 100000)), 'goalId':constant.irisGenericValues['goalId'], 'objectiveId':constant.irisGenericValues['objectiveId'], 'endDate':int(time.time() * 1000 - 24 * 60 * 60 * 1000)})[0]
        campaigns.assertCreateCampaign(response, 400, 1006, 'Campaign Date Exception : Campaign End Date Cannot Be Before Start Date')
    
    def test_outboundCampaign_lapsed_timezoneDifference(self):
        response = campaigns.createCampaign({'name':'IRIS_' + str(int(time.time() * 100000)), 'goalId':constant.irisGenericValues['goalId'], 'objectiveId':constant.irisGenericValues['objectiveId'], 'startDate':int(time.time() * 1000 - 24 * 60 * 60 * 1000)})[0]
        campaigns.assertCreateCampaign(response, 400, 1006, 'Campaign Date Exception : Campaign Start Date Cannot Be before Current Date')
    
    def test_outboundCampaign_wrongGoalId(self):
        goalId = str(dbCallsCampaign.getInvalidGoalId()['id'])
        response = campaigns.createCampaign({'name':'IRIS_' + str(int(time.time() * 100000)), 'goalId':goalId, 'objectiveId':constant.irisGenericValues['objectiveId']})[0]
        campaigns.assertCreateCampaign(response, 400, 1004, 'Campaign Goal Exception : Invalid Campaign Goal Id')
    
    def test_outboundCampaign_wrongObjectiveId(self):
        objectiveId = str(dbCallsCampaign.getInvalidObjectiveId()['id'])
        response = campaigns.createCampaign({'name':'IRIS_' + str(int(time.time() * 100000)), 'goalId':constant.irisGenericValues['goalId'], 'objectiveId':objectiveId})[0]
        campaigns.assertCreateCampaign(response, 400, 1005, 'Campaign Objective Exception : Invalid Campaign Objective Id')
    
    def test_outboundCampaign_wrongCampaignType(self):
        response = campaigns.createCampaign({'goalId':constant.irisGenericValues['goalId'], 'objectiveId':constant.irisGenericValues['objectiveId'], 'campaignType':'WRONGTYPE'})[0]
        campaigns.assertCreateCampaign(response, 400, 102, 'Invalid request : CampaignType is required. ')
    
    @pytest.mark.parametrize('popKeysFromBody,errorCode,errorMessage', [
        ('name', 102, 'Invalid request : Campaign name is required. '),
        ('startDate', 102, 'Invalid request : Campaign start date is required. '),
        ('endDate', 102, 'Invalid request : Campaign end date is required. '),
        ('campaignType', 102, 'Invalid request : CampaignType is required. '),
        ('testControl', 102, 'Invalid request : TestControl is required. ')
        ])
    def test_outboundCampaign_popField(self, popKeysFromBody, errorCode, errorMessage):
        response = campaigns.createCampaign(popKeysFromBody, process='pop')[0]
        campaigns.assertCreateCampaign(response, 400, errorCode, errorMessage)
    
    @pytest.mark.parametrize('caseName,campaignName', [
        ('IncludingAlphanumericUnderscoreSpace', 'IR IS_' + str(int(time.time() * 100000))),
        ])
    def test_outboundCampaign_differentCampaignName_positiveScenario(self, caseName, campaignName):
        response, payload = campaigns.createCampaign({'name':campaignName, 'goalId':constant.irisGenericValues['goalId'], 'objectiveId':constant.irisGenericValues['objectiveId']})
        campaigns.assertCreateCampaign(response, 200)
        campaigns.assertCreateCampaignDBCall(response['json']['entity']['campaignId'], payload)
    
    @pytest.mark.parametrize('caseName,campaignName,errorCode,errorMessage', [
        ('AllSpecialCharacter', 'IR IS_~!@#$%^&*()_+|}{:"?><,./;\][=', 1003, 'Campaign Name Exception : Invalid campaign name. Use only alphanumeric, underscore, space.'),
        ('MoreThan50Character', 'IRIS_ssssssssssssssssssssssssssssssssssss' + str(int(time.time() * 100000)), 102, 'Invalid request : Invalid campaign name. Name exceeds 50 characters. '),
        ])
    def test_outboundCampaign_differentCampaignName_negativeScenario(self, caseName, campaignName, errorCode, errorMessage):
        response = campaigns.createCampaign({'name':campaignName, 'goalId':constant.irisGenericValues['goalId'], 'objectiveId':constant.irisGenericValues['objectiveId']})[0]
        campaigns.assertCreateCampaign(response, 400, errorCode, errorMessage)
