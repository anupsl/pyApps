import pytest, time, pytest_ordering
from src.Constant.constant import constant
from src.modules.iris.campaigns import campaigns
from src.modules.iris.dbCallsCampaign import dbCallsCampaign
from src.utilities.logger import Logger
from src.utilities.assertion import Assertion
from src.modules.iris.construct import construct

@pytest.mark.run(order=7)
class Test_GetCampaignAll():
    
    def setup_method(self, method):
        Logger.logMethodName(method.__name__)
    
    @pytest.mark.parametrize('description,numberOfCamaigns,startDate,endDate,startFrom', [
        ('Upcoming Campaign ', 5, constant.getCampaignAll['upcomingStartDate'], constant.getCampaignAll['upcomingEndDate'], 0),
        ])
    def test_getCampaignAll_Sanity(self, description, numberOfCamaigns, startDate, endDate, startFrom):
        getCampaignResponseCheck = campaigns.getCampaignById(queryParam=[('startDate', startDate), ('endDate', endDate), ('startFrom', startFrom), ('numberOfRecords', numberOfCamaigns)])
        campaignsRequiredToCreate = numberOfCamaigns - len(getCampaignResponseCheck.get('json').get('data'))
            
        numberOfCampaignsGotCreated = 0
        if campaignsRequiredToCreate > 0:
            for number in range(campaignsRequiredToCreate):
                response, payload = campaigns.createCampaign({'name':'IRIS_' + str(int(time.time())), 'goalId':str(constant.irisGenericValues['goalId']), 'objectiveId': constant.irisGenericValues['objectiveId'], 'startDate':startDate, 'endDate':endDate})
                campaigns.assertCreateCampaign(response, 200)
                if response.get('statusCode') == 200:
                    numberOfCampaignsGotCreated = numberOfCampaignsGotCreated + 1
        
        Logger.log('Number of Campaigns required :{} and CampaignsAlready Present in Range :{} and created Camapign in this job :{}'.format(numberOfCamaigns, len(getCampaignResponseCheck.get('json').get('data')), numberOfCampaignsGotCreated))
        
        getCampaignResponse = campaigns.getCampaignById(queryParam=[('startDate', startDate), ('endDate', endDate), ('startFrom', startFrom), ('numberOfRecords', numberOfCamaigns)])
        campaigns.assertGetCampaignAll(getCampaignResponse, numberOfCamaigns, 200)
        listOfCampaignsWithCampaignIdAndResponse = construct.constructGetCampaignAllToGetCampaignIdResponse(getCampaignResponse)
        for eachlistOfCampaignsWithCampaignIdAndResponse in listOfCampaignsWithCampaignIdAndResponse:
            campaigns.assertGetCampaignDBCall(eachlistOfCampaignsWithCampaignIdAndResponse[1], eachlistOfCampaignsWithCampaignIdAndResponse[0])
    
    @pytest.mark.parametrize('description,numberOfCamaigns,startDate,endDate,startFrom', [
        ('Upcoming Campaign ', 5, constant.getCampaignAll.get('upcomingStartDate'), constant.getCampaignAll.get('upcomingEndDate'), 0),
        ])
    def test_getCampaignAll_updateUpcomingCampaign_outOfGivenRange(self, description, numberOfCamaigns, startDate, endDate, startFrom):
        getCampaignResponseCheck = campaigns.getCampaignById(queryParam=[('startDate', startDate), ('endDate', endDate), ('startFrom', startFrom), ('numberOfRecords', numberOfCamaigns)])
        campaignsRequiredToCreate = numberOfCamaigns - len(getCampaignResponseCheck.get('json').get('data'))
    
        numberOfCampaignsGotCreated = 0
        if campaignsRequiredToCreate > 0:
            for number in range(campaignsRequiredToCreate):
                response, payload = campaigns.createCampaign({'name':'IRIS_' + str(int(time.time())), 'goalId':str(constant.irisGenericValues['goalId']), 'objectiveId': constant.irisGenericValues['objectiveId'], 'startDate':startDate, 'endDate':endDate})
                campaigns.assertCreateCampaign(response, 200)
                if response.get('statusCode') == 200:
                    numberOfCampaignsGotCreated = numberOfCampaignsGotCreated + 1
        
        Logger.log('Number of Campaigns required :{} and CampaignsAlready Present in Range :{} and created Camapign in this job :{}'.format(numberOfCamaigns, len(getCampaignResponseCheck.get('json').get('data')), numberOfCampaignsGotCreated))
        
        getCampaignResponse = campaigns.getCampaignById(queryParam=[('startDate', startDate), ('endDate', endDate), ('startFrom', startFrom), ('numberOfRecords', numberOfCamaigns)])
        campaigns.assertGetCampaignAll(getCampaignResponse, numberOfCamaigns, 200)
        listOfCampaignsWithCampaignIdAndResponse = construct.constructGetCampaignAllToGetCampaignIdResponse(getCampaignResponse)
        campaignIdToUpdate = listOfCampaignsWithCampaignIdAndResponse[0][0]
        Logger.log('Updating Campaign with id :', campaignIdToUpdate)
        campaigns.updateCampaign({'startDate':int(time.time() * 1000 + 24 * 60 * 60 * 1000 * 469), 'endDate':int(time.time() * 1000 + 24 * 60 * 60 * 1000 * 470)}, campaignId=campaignIdToUpdate)
        getCampaignResponseAfterUpdatingSingleCampaignInThatRange = campaigns.getCampaignById(queryParam=[('startDate', startDate), ('endDate', endDate), ('startFrom', startFrom), ('numberOfRecords', numberOfCamaigns)])
        for each in getCampaignResponseAfterUpdatingSingleCampaignInThatRange.get('json').get('data'):
            if int(each.get('id')) == int(campaignIdToUpdate):
                Assertion.constructAssertion(False, 'Updated Campaign Found in Get All Call')

    @pytest.mark.parametrize('description,startDate,endDate,startFrom,numberOfBreaksToCheck', [
        ('Taking All Campaign between range and using limits to check with Loop', constant.getCampaignAll.get('upcomingStartDate'), constant.getCampaignAll.get('upcomingEndDate') , 0, 1)
        ])    
    def test_getCampaignAll_loopOnLimit(self, description, startDate, endDate, startFrom, numberOfBreaksToCheck):
        getCampaignResponseToGetLengthOfCampaigns = campaigns.getCampaignById(queryParam=[('startDate', startDate), ('endDate', endDate), ('startFrom', startFrom), ('numberOfRecords', '')])
        numberOfRecords = len(getCampaignResponseToGetLengthOfCampaigns.get('json').get('data'))
        List = []
        for numberOfLoops in range(numberOfRecords / numberOfBreaksToCheck):
            getCampaignResponse = campaigns.getCampaignById(queryParam=[('startDate', startDate), ('endDate', endDate), ('startFrom', startFrom), ('numberOfRecords', startFrom + numberOfBreaksToCheck)])
            campaigns.assertGetCampaignWithPassedLimit(getCampaignResponseToGetLengthOfCampaigns.get('json').get('data'), getCampaignResponse.get('json').get('data'), startFrom, startFrom + numberOfBreaksToCheck)
            startFrom += numberOfBreaksToCheck

    @pytest.mark.parametrize('description,startDate,endDate,statusCode,errorCode,errorMessage', [
        ('StartDate Greater Than EndDate', int(time.time() * 1000 + 24 * 60 * 60 * 1000), int(time.time() * 1000), 400, 100, 'Invalid request : Start date should be greater than end date'),
        ('StartAndEndDateSame', int(time.time() * 1000), int(time.time() * 1000), 400, 100, 'Invalid request : Start date should be greater than end date'),
        ('Incorrect Format of Date', constant.config['currentTimestamp'], constant.config['currentTimestamp'], 400, 101, 'Invalid value for path param: startDate'),
        ('Character Value of Date', 'date1', 'date2', 400, 101, 'Invalid value for path param: startDate'),
        ('Special Character passed in Date', 'date##', 'date$$', 400, 101, 'Invalid value for path param: startDate'),
        ])    
    def test_getCampaignAll_DateRangeAndFormat_NegativeScenarios(self, description, startDate, endDate, statusCode, errorCode, errorMessage):
        getCampaignResponse = campaigns.getCampaignById(queryParam=[('startDate', startDate), ('endDate', endDate)])
        campaigns.assertGetCampaignAll(getCampaignResponse, 0, statusCode, errorCode, errorMessage)
        
    @pytest.mark.parametrize('description,startDate,endDate,statusCode', [
        ('NoEndDate', constant.getCampaignAll['upcomingStartDate'], '', 200),
        ('NoStartDate', '', constant.getCampaignAll['upcomingEndDate'], 200),
        ('No param Given', '', '', 200)
        ]) 
    def test_getCampaignAll_DateRangeAndFormat_positiveScenrios(self, description, startDate, endDate, statusCode):
        getCampaignResponse = campaigns.getCampaignById(queryParam=[('startDate', startDate), ('endDate', endDate)])
        Assertion.constructAssertion(getCampaignResponse['statusCode'] == int(statusCode), 'Matching statusCode actual :{},expected :{}'.format(getCampaignResponse['statusCode'], statusCode))
        Assertion.constructAssertion(len(getCampaignResponse['json']['data']) >= 0, 'CampaignCreated betweenRange is :{} and campaignRecieved in getCall :{}'.format(0, len(getCampaignResponse['json']['data'])))
        for eachRecord in getCampaignResponse['json']['data']:
            if startDate != '':
                Assertion.constructAssertion(eachRecord['startDate'] >= startDate, 'Matching endDate of Response is within given range')
            if endDate != '':
                Assertion.constructAssertion(eachRecord['endDate'] <= endDate, 'Matching endDate of Response is within given range')
