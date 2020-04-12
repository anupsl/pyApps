import pytest, time
from src.Constant.constant import constant
from src.modules.iris.campaigns import campaigns
from src.modules.iris.construct import construct
from src.modules.iris.dbCallsCampaign import dbCallsCampaign
from src.utilities.logger import Logger

@pytest.mark.run(order=11)
class Test_UpdateCampaign():
    
    def setup_class(self):
        Logger.logSuiteName(str(self).split('.')[-1])
        construct.resetCampaignDefaultObject()
    
    def teardown_class(self):
        construct.resetCampaignDefaultObject()
        
    def setup_method(self, method):
        Logger.logMethodName(method.__name__)
    
    @pytest.mark.parametrize('description,campaignType,payloadToUpload,statusCode,errorCode,errorMessage', [
        ('Sanity Case to Update Name', ['LIVE', 'ORG'], {'name':'IRIS_UPDATE' + str(int(time.time()))}, 200, 000, ''),
        ])
    def test_updateCampaign_Sanity(self, description, campaignType, payloadToUpload, statusCode, errorCode, errorMessage):
        updateResponse, createResponse, updatePayload, createPayload = campaigns.updateCampaign(payloadToUpload, campaignType=campaignType)
        Logger.log('updateResponse :{} , createResponse :{} , updatePayload :{} ,createPayload :{}'.format(updateResponse, createResponse, updatePayload, createPayload))
        campaigns.assertUpdateCampaign(updateResponse, createResponse, statusCode, errorCode, errorMessage)
        if statusCode == 200:
            createPayload.update(updatePayload)
            Logger.log('Payload Constructed from updatepayload and create payload : ', createPayload)
            campaigns.assertUpdateCampaignDBCall(createPayload, updateResponse.get('json').get('entity').get('campaignId'))
        else:
            Logger.log('No DB Validation as statusCode :', statusCode)
            
    @pytest.mark.parametrize('description,campaignType,payloadToUpload,statusCode,errorCode,errorMessage', [
        ('Update StartDate', ['LIVE', 'ORG'], {'startDate':int(time.time() * 1000 + 24 * 60)}, 200, 000, ''),
        ('Update endDate', ['LIVE', 'ORG'], {'endDate':int(time.time() * 1000 + 24 * 60 * 60 * 1000 * 2)}, 200, 000, ''),
        ('Update goalId', ['LIVE', 'ORG'], {'goalId':constant.irisGenericValues['goalId']}, 200, 000, ''),
        ('Update objectiveId', ['LIVE', 'ORG'], {'objectiveId':constant.irisGenericValues['objectiveId']}, 200, 000, ''),
        ('Update StartDate and endDate', ['LIVE', 'ORG'], {'startDate':int(time.time() * 1000 + 24 * 60 * 60 * 1000 * 2), 'endDate':int(time.time() * 1000 + 24 * 60 * 60 * 1000) * 3}, 200, 000, ''),
        ('Update goaldId and ObjectiveId', ['LIVE', 'ORG'], {'goalId':constant.irisGenericValues['goalId'], 'objectiveId':constant.irisGenericValues['objectiveId']}, 200, 000, ''),
        ('Update name,startDate,endDate,goalId and ObjectiveId', ['LIVE', 'ORG'], {'name':'IRIS_TEST_UPDATE_LIVE' + str(int(time.time())), 'startDate':int(time.time() * 1000 + 24 * 60 * 60 * 1000 * 2), 'endDate':int(time.time() * 1000 + 24 * 60 * 60 * 1000 * 3), 'goalId':constant.irisGenericValues['goalId'], 'objectiveId':constant.irisGenericValues['objectiveId']}, 200, 000, ''),
        ('Update StartDate for Campaign With TestType Custom', ['LIVE', 'CUSTOM'], {'startDate':int(time.time() * 1000 + 24 * 60)}, 200, 000, ''),
        ('Update endDate for Campaign With TestType Custom', ['LIVE', 'CUSTOM'], {'endDate':int(time.time() * 1000 + 24 * 60 * 60 * 1000 * 2)}, 200, 000, ''),
        ('Update StartDate for Campaign With TestType Skip', ['LIVE', 'SKIP'], {'startDate':int(time.time() * 1000 + 24 * 60)}, 200, 000, ''),
        ('Update endDate for Campaign With TestType Skip', ['LIVE', 'SKIP'], {'endDate':int(time.time() * 1000 + 24 * 60 * 60 * 1000 * 2)}, 200, 000, ''),
        ])
    def test_updateCampaign_Live(self, description, campaignType, payloadToUpload, statusCode, errorCode, errorMessage):
        updateResponse, createResponse, updatePayload, createPayload = campaigns.updateCampaign(payloadToUpload, campaignType=campaignType)
        Logger.log('updateResponse :{} , createResponse :{} , updatePayload :{} ,createPayload :{}'.format(updateResponse, createResponse, updatePayload, createPayload))
        campaigns.assertUpdateCampaign(updateResponse, createResponse, statusCode, errorCode, errorMessage)
        if statusCode == 200:
            createPayload.update(updatePayload)
            Logger.log('Payload Constructed from updatepayload and create payload : ', createPayload)
            campaigns.assertUpdateCampaignDBCall(createPayload, updateResponse.get('json').get('entity').get('campaignId'))
        else:
            Logger.log('No DB Validation as statusCode :', statusCode)        
    
    @pytest.mark.parametrize('description,campaignType,payloadToUpload,statusCode,errorCode,errorMessage', [
        ('Update StartDate', ['UPCOMING', 'ORG'], {'startDate':int(time.time() * 1000 + 24 * 60)}, 200, 000, ''),
        ('Update endDate', ['UPCOMING', 'ORG'], {'endDate':int(time.time() * 1000 + 24 * 60 * 60 * 1000 * 5)}, 200, 000, ''),
        ('Update goalId', ['UPCOMING', 'ORG'], {'goalId':constant.irisGenericValues['goalId']}, 200, 000, ''),
        ('Update objectiveId', ['UPCOMING', 'ORG'], {'objectiveId':constant.irisGenericValues['objectiveId']}, 200, 000, ''),
        ('Update StartDate and endDate', ['UPCOMING', 'ORG'], {'startDate':int(time.time() * 1000 + 24 * 60 * 60 * 1000 * 5), 'endDate':int(time.time() * 1000 + 24 * 60 * 60 * 1000 * 6)}, 200, 000, ''),
        ('Update goaldId and ObjectiveId', ['UPCOMING', 'ORG'], {'goalId':constant.irisGenericValues['goalId'], 'objectiveId':constant.irisGenericValues['objectiveId']}, 200, 000, ''),
        ('Update name,startDate,endDate,goalId and ObjectiveId', ['UPCOMING', 'ORG'], {'name':'IRIS_TEST_UPDATE_UPCOMING' + str(int(time.time())), 'startDate':int(time.time() * 1000 + 24 * 60 * 60 * 1000 * 2), 'endDate':int(time.time() * 1000 + 24 * 60 * 60 * 1000 * 3), 'goalId':constant.irisGenericValues['goalId'], 'objectiveId':constant.irisGenericValues['objectiveId']}, 200, 000, ''),
        ('Update StartDate for Campaign With TestType Custom', ['UPCOMING', 'CUSTOM'], {'startDate':int(time.time() * 1000 + 24 * 60)}, 200, 000, ''),
        ('Update endDate for Campaign With TestType Custom', ['UPCOMING', 'CUSTOM'], {'endDate':int(time.time() * 1000 + 24 * 60 * 60 * 1000 * 4)}, 200, 000, ''),
        ('Update StartDate for Campaign With TestType Skip', ['UPCOMING', 'SKIP'], {'startDate':int(time.time() * 1000 + 24 * 60)}, 200, 000, ''),
        ('Update endDate for Campaign With TestType Skip', ['UPCOMING', 'SKIP'], {'endDate':int(time.time() * 1000 + 24 * 60 * 60 * 1000 * 4)}, 200, 000, ''),
        ])
    def test_updateCampaign_Upcoming(self, description, campaignType, payloadToUpload, statusCode, errorCode, errorMessage):
        updateResponse, createResponse, updatePayload, createPayload = campaigns.updateCampaign(payloadToUpload, campaignType=campaignType)
        Logger.log('updateResponse :{} , createResponse :{} , updatePayload :{} ,createPayload :{}'.format(updateResponse, createResponse, updatePayload, createPayload))
        campaigns.assertUpdateCampaign(updateResponse, createResponse, statusCode, errorCode, errorMessage)
        if statusCode == 200:
            createPayload.update(updatePayload)
            Logger.log('Payload Constructed from updatepayload and create payload : ', createPayload)
            campaigns.assertUpdateCampaignDBCall(createPayload, updateResponse.get('json').get('entity').get('campaignId'))
        else:
            Logger.log('No DB Validation as statusCode :', statusCode)        
    
    @pytest.mark.parametrize('description,campaignType,payloadToUpload,statusCode,errorCode,errorMessage', [
        ('Update StartDate', ['LAPSED', 'ORG'], {'startDate':int(time.time() * 1000 + 24 * 60), 'endDate':int(time.time() * 1000 + 24 * 60 * 60 * 1000 * 3)}, 200, 000, ''),
        ('Update endDate', ['LAPSED', 'ORG'], {'endDate':int(time.time() * 1000 + 24 * 60 * 60 * 1000 * 5)}, 200, 000, ''),
        ('Update goalId', ['LAPSED', 'ORG'], {'goalId':constant.irisGenericValues['goalId']}, 200, 000, ''),
        ('Update objectiveId', ['LAPSED', 'ORG'], {'objectiveId':constant.irisGenericValues['objectiveId']}, 200, 000, ''),
        ('Update StartDate and endDate', ['LAPSED', 'ORG'], {'startDate':int(time.time() * 1000 + 24 * 60 * 60 * 1000 * 5), 'endDate':int(time.time() * 1000 + 24 * 60 * 60 * 1000) * 6}, 200, 000, ''),
        ('Update goaldId and ObjectiveId', ['LAPSED', 'ORG'], {'goalId':constant.irisGenericValues['goalId'], 'objectiveId':constant.irisGenericValues['objectiveId']}, 200, 000, ''),
        ('Update name,startDate,endDate,goalId and ObjectiveId', ['LAPSED', 'ORG'], {'name':'IRIS_TEST_UPDATE_LAPSED' + str(int(time.time())), 'startDate':int(time.time() * 1000 + 24 * 60 * 60 * 1000 * 2), 'endDate':int(time.time() * 1000 + 24 * 60 * 60 * 1000 * 3), 'goalId':constant.irisGenericValues['goalId'], 'objectiveId':constant.irisGenericValues['objectiveId']}, 200, 000, ''),
        ('Update StartDate for Campaign With TestType Custom', ['LAPSED', 'CUSTOM'], {'startDate':int(time.time() * 1000 + 24 * 60), 'endDate':int(time.time() * 1000 + 24 * 60 * 60 * 1000 * 3)}, 200, 000, ''),
        ('Update endDate for Campaign With TestType Custom', ['LAPSED', 'CUSTOM'], {'endDate':int(time.time() * 1000 + 24 * 60 * 60 * 1000 * 4)}, 200, 000, ''),
        ('Update StartDate for Campaign With TestType Skip', ['LAPSED', 'SKIP'], {'startDate':int(time.time() * 1000 + 24 * 60), 'endDate':int(time.time() * 1000 + 24 * 60 * 60 * 1000 * 3)}, 200, 000, ''),
        ('Update endDate for Campaign With TestType Skip', ['LAPSED', 'SKIP'], {'endDate':int(time.time() * 1000 + 24 * 60 * 60 * 1000 * 4)}, 200, 000, ''),
        ])
    def test_updateCampaign_Lapsed(self, description, campaignType, payloadToUpload, statusCode, errorCode, errorMessage):
        updateResponse, createResponse, updatePayload, createPayload = campaigns.updateCampaign(payloadToUpload, campaignType=campaignType)
        Logger.log('updateResponse :{} , createResponse :{} , updatePayload :{} ,createPayload :{}'.format(updateResponse, createResponse, updatePayload, createPayload))
        campaigns.assertUpdateCampaign(updateResponse, createResponse, statusCode, errorCode, errorMessage)
        if statusCode == 200:
            createPayload.update(updatePayload)
            Logger.log('Payload Constructed from updatepayload and create payload : ', createPayload)
            campaigns.assertUpdateCampaignDBCall(createPayload, updateResponse.get('json').get('entity').get('campaignId'))
        else:
            Logger.log('No DB Validation as statusCode :', statusCode)        
    
    @pytest.mark.parametrize('description,campaignId', [
        ('CampaignId as 0', 0),
        ('CampaignId as -1', -1)
        ])        
    def test_updateCampaign_WrongCampaignId(self, description, campaignId):
        updateResponse, createResponse, updatePayload, createPayload = campaigns.updateCampaign({'name':'Wrong_CampaignId' + str(int(time.time()))}, campaignId=campaignId)
        Logger.log('updateResponse :{} , createResponse :{} , updatePayload :{} ,createPayload :{}'.format(updateResponse, createResponse, updatePayload, createPayload))
        campaigns.assertUpdateCampaign(updateResponse, createResponse, 400, 100, 'Invalid request : must be greater than or equal to 1')
        
    def test_updateCampaign_WithExistingCampaignName(self):
        existingCampaignId, existingCampaignPayload = dbCallsCampaign.getLapsedCamapign(constant.config['orgId'], 'ORG')
        existingCampaignName = existingCampaignPayload.get('name') 
        updateResponse, createResponse, updatePayload, createPayload = campaigns.updateCampaign({'name':existingCampaignName}, campaignType=['LIVE', 'ORG'])
        Logger.log('updateResponse :{} , createResponse :{} , updatePayload :{} ,createPayload :{}'.format(updateResponse, createResponse, updatePayload, createPayload))
        campaigns.assertUpdateCampaign(updateResponse, createResponse, 400, 1003, 'Campaign Name Exception : Campaign Name already exists')
    
    @pytest.mark.parametrize('description,campaignName,statusCode,errorCode,errorMessage', [
        ('Special Characters', 'UpdateCampaign_SpecialChar_$$##**%%', 400, 100, 'Invalid request : Invalid campaign name. Use only alphanumeric , underscore, space. '),
        ('LengthOfCampName >50 char', 'IRIS_CampaignName_BoundaryValue_MoreThan50Character', 400, 100, 'Invalid request : Invalid campaign name. Name exceeds 50 characters. '),
        ('Empty Campaign Name', '', 400, 100, 'Invalid request : Invalid Campaign name. Campaign name cant be empty')
        ])                 
    def test_updateCampaign_WithDifferntCampaignName_NegativeCases(self, description, campaignName, statusCode, errorCode, errorMessage):
        updateResponse, createResponse, updatePayload, createPayload = campaigns.updateCampaign({'name':campaignName}, campaignType=['LIVE', 'ORG'])
        Logger.log('updateResponse :{} , createResponse :{} , updatePayload :{} ,createPayload :{}'.format(updateResponse, createResponse, updatePayload, createPayload))
        campaigns.assertUpdateCampaign(updateResponse, createResponse, statusCode, errorCode, errorMessage)
             
    def test_updateCampaign_invalidGoalId(self):
        updateResponse, createResponse, updatePayload, createPayload = campaigns.updateCampaign({'name':'InvalidGoalId' + str(int(time.time())), 'goalId':9999}, campaignType=['LIVE', 'ORG'])
        Logger.log('updateResponse :{} , createResponse :{} , updatePayload :{} ,createPayload :{}'.format(updateResponse, createResponse, updatePayload, createPayload))
        campaigns.assertUpdateCampaign(updateResponse, createResponse, 400, 1004, 'Campaign Goal Exception : Invalid Campaign Goal Id')
        
    def test_updateCampaign_invalidObjectiveId(self):
        updateResponse, createResponse, updatePayload, createPayload = campaigns.updateCampaign({'name':'InvalidObjectiveId' + str(int(time.time())), 'objectiveId':9999}, campaignType=['LIVE', 'ORG'])
        Logger.log('updateResponse :{} , createResponse :{} , updatePayload :{} ,createPayload :{}'.format(updateResponse, createResponse, updatePayload, createPayload))
        campaigns.assertUpdateCampaign(updateResponse, createResponse, 400, 1005, 'Campaign Objective Exception : Invalid Campaign Objective Id')
    
    @pytest.mark.parametrize('description,startDate,endDate,statusCode,errorCode,errorMessage', [
        ('Invalid Start Date', constant.config['currentTimestamp'], int(time.time() * 1000 + 24 * 60 * 60 * 1000), 400, 100, ''),
        ('Invalid End Date', int(time.time() * 1000 + 24 * 60 * 60 * 1000), constant.config['currentTimestamp'], 400, 100, ''),
        ('Updating End Date to equal of startDate', '', int(time.time() * 1000 + 24 * 60 * 60 * 1000), 400, 1006, 'Campaign Date Exception : Campaign End Date Cannot Be Before Start Date'),
        ('Updating Start Date to be equal to endDate', int(time.time() * 1000 + 24 * 60 * 60 * 1000 * 2), '', 400, 1006, 'Campaign Date Exception : Campaign End Date Cannot Be Before Start Date'),
        ('Updating Start Date to be greater than endData', int(time.time() * 1000 + 24 * 60 * 60 * 1000 * 5), '', 400, 1006, 'Campaign Date Exception : Campaign End Date Cannot Be Before Start Date'),
        ('Updating End Date less than Start Date', '', int(time.time() * 1000), 400, 1006, 'Campaign Date Exception : Campaign End Date Cannot Be Before Start Date')
        ])     
    def test_updateCampaign_VariationInStartEndDate(self, description, startDate, endDate, statusCode, errorCode, errorMessage):
        payloadToUpdate = {'name':'StartDate_EndDate_Variation' + str(int(time.time())), 'startDate':startDate, 'endDate':endDate}
        if startDate == '':
            payloadToUpdate.pop('startDate')
        elif endDate == '':
            payloadToUpdate.pop('endDate')
        updateResponse, createResponse, updatePayload, createPayload = campaigns.updateCampaign(payloadToUpdate, campaignType=['UPCOMING', 'ORG'])
        Logger.log('updateResponse :{} , createResponse :{} , updatePayload :{} ,createPayload :{}'.format(updateResponse, createResponse, updatePayload, createPayload))
        campaigns.assertUpdateCampaign(updateResponse, createResponse, statusCode, errorCode, errorMessage)
        
            
    def test_strictOrgUpdate(self):
        strictOrg = constant.config['strict_org_id']
        previousOrgId = construct.updateOrgId(strictOrg)
        try:
            updateResponse, createResponse, updatePayload, createPayload = campaigns.updateCampaign({'name':'strict_ORG_ShouldNotBeUpdated' + str(int(time.time()))}, campaignId=int(constant.config['strict_campaign_id']))
            Logger.log('updateResponse :{} , createResponse :{} , updatePayload :{} ,createPayload :{}'.format(updateResponse, createResponse, updatePayload, createPayload))
            campaigns.assertUpdateCampaign(updateResponse, createResponse, 400, 1010, 'CAMPAIGN_UPDATE_EXCEPTION : Campaign Cannot be updated as it has already approved messages')
        except AssertionError, exp:
            Logger.log('Assertion Failed as :', exp)
        finally:
            construct.updateOrgId(int(previousOrgId))
            
    ''' 
    #This case will be Activate when Create Coupon Automation is done      
    def test_CouponsDateUpdate(self):
        updateResponse, createResponse, updatePayload, createPayload = campaigns.updateCampaign({'name':'CouponAlsoShouldUpdate' + str(int(time.time())), 'endDate':int(time.time() * 1000 + 10 * 24 * 60 * 60 * 1000)}, campaignId=300654)
        Logger.log('updateResponse :{} , createResponse :{} , updatePayload :{} ,createPayload :{}'.format(updateResponse, createResponse, updatePayload, createPayload))
    '''        
            
