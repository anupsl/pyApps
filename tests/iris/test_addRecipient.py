import pytest, time, Queue, pytest_ordering
from time import sleep
from threading import Thread
from src.Constant.constant import constant
from src.modules.iris.list import campaignList
from src.utilities.assertion import Assertion
from src.utilities.logger import Logger
from src.modules.iris.campaigns import campaigns
from src.modules.iris.dbCallsCampaign import dbCallsCampaign
from src.modules.iris.dbCallsList import dbCallsList
from src.modules.iris.construct import construct

@pytest.mark.run(order=5)
class Test_AddRecipient():
    
    def setup_method(self, method):
        Logger.logMethodName(method.__name__)
    
    @pytest.mark.parametrize('campaignAndListType,userType,numberOfUsers,customTagCount', [
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'mobile', 50, 0),
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'email', 50, 0)
        ])
    def test_addRecipient_Sanity(self, campaignAndListType, userType, numberOfUsers, customTagCount):
        createListresponse, createListPayload, campaignId = campaignList.createList({'customTagCount':int(customTagCount), 'name':'IRIS_LIST_' + str(int(time.time() * 100000))}, campaignType=campaignAndListType)
        campaignList.assertCreateList(createListresponse, 200)
        groupVersionDetailResult, bucketId = campaignList.assertCreateListDbCalls(createListresponse.get('json').get('entity').get('listId'), createListPayload, campaignAndListType[1])
        Logger.log('GroupVersionId : {}, bucketId : {}'.format(groupVersionDetailResult, bucketId))
        addRecipientResponse, addRecipientPayload = campaignList.addRecipient({}, campaignId, createListresponse.get('json').get('entity').get('listId'), str(userType), int(numberOfUsers), int(customTagCount))
        campaignList.assertAddRecipient(addRecipientResponse, 200)
        campaignList.assertAddRecipientDbCalls(addRecipientResponse, addRecipientPayload, createListresponse, campaignId, bucketId, {'TEST':groupVersionDetailResult.get('TEST'), 'CONTROL':groupVersionDetailResult.get('CONTROL')}, userType)
    
    @pytest.mark.parametrize('campaignAndListType,userType,numberOfUsers,customTagCount', [
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'mobile,email', 10, 0)
        ])
    def test_addRecipient_Combination_Sanity(self, campaignAndListType, userType, numberOfUsers, customTagCount):
        createListresponse, createListPayload, campaignId = campaignList.createList({'customTagCount':int(customTagCount), 'name':'IRIS_LIST_' + str(int(time.time() * 100000))}, campaignType=campaignAndListType)
        campaignList.assertCreateList(createListresponse, 200)
        groupVersionDetailResult, bucketId = campaignList.assertCreateListDbCalls(createListresponse.get('json').get('entity').get('listId'), createListPayload, campaignAndListType[1])
        Logger.log('GroupVersionId : {}, bucketId : {}'.format(groupVersionDetailResult, bucketId))
        addRecipientResponse, addRecipientPayload = campaignList.addRecipient({}, campaignId, createListresponse.get('json').get('entity').get('listId'), str(userType), int(numberOfUsers), int(customTagCount), newUser=False)
        campaignList.assertAddRecipient(addRecipientResponse, 200)
        campaignList.assertAddRecipientDbCalls(addRecipientResponse, addRecipientPayload, createListresponse, campaignId, bucketId, {'TEST':groupVersionDetailResult.get('TEST'), 'CONTROL':groupVersionDetailResult.get('CONTROL')}, userType)
    
    @pytest.mark.parametrize('campaignAndListType,userType,numberOfUsers,customTagCount', [
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'userId', 5, 0),
        (['LIVE', 'ORG', 'List', 'TAGS', 1], 'userId', 5, 1),
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'externalId', 5, 0),
        (['LIVE', 'ORG', 'List', 'TAGS', 1], 'externalId,userId', 5, 1)
        ])
    def test_addRecipient_UsingExistingUsers_Sanity(self, campaignAndListType, userType, numberOfUsers, customTagCount):
        createListresponse, createListPayload, campaignId = campaignList.createList({'customTagCount':int(customTagCount), 'name':'IRIS_LIST_' + str(int(time.time() * 100000))}, campaignType=campaignAndListType)
        campaignList.assertCreateList(createListresponse, 200)
        groupVersionDetailResult, bucketId = campaignList.assertCreateListDbCalls(createListresponse.get('json').get('entity').get('listId'), createListPayload, campaignAndListType[1])
        Logger.log('GroupVersionId : {}, bucketId : {}'.format(groupVersionDetailResult, bucketId))
        addRecipientResponse, addRecipientPayload = campaignList.addRecipient({}, campaignId, createListresponse.get('json').get('entity').get('listId'), str(userType), int(numberOfUsers), int(customTagCount), newUser=False)
        campaignList.assertAddRecipient(addRecipientResponse, 200)
    
    @pytest.mark.parametrize('campaignAndListType,userType,numberOfUsers,customTagCount', [
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'mobile,userId', 5, 0),
        (['LIVE', 'ORG', 'List', 'TAGS', 1], 'mobile,externalId', 5, 1),
        (['LIVE', 'ORG', 'List', 'TAGS', 2], 'email,userId', 5, 2),
        (['LIVE', 'ORG', 'List', 'TAGS', 3], 'email,externalId', 5, 3),
        (['LIVE', 'ORG', 'List', 'TAGS', 4], 'mobile,email', 5, 4),
        (['LIVE', 'ORG', 'List', 'TAGS', 5], 'mobile,email,userId', 5, 5),
        (['LIVE', 'ORG', 'List', 'TAGS', 5], 'mobile,email,externalId', 5, 5),
        (['LIVE', 'ORG', 'List', 'TAGS', 5], 'mobile,email,userId,externalId', 5, 5)
        ])
    def test_addRecipient_combination_CustomTags(self, campaignAndListType, userType, numberOfUsers, customTagCount):
        createListresponse, createListPayload, campaignId = campaignList.createList({'customTagCount':int(customTagCount), 'name':'IRIS_LIST_' + str(int(time.time() * 100000))}, campaignType=campaignAndListType)
        campaignList.assertCreateList(createListresponse, 200)
        groupVersionDetailResult, bucketId = campaignList.assertCreateListDbCalls(createListresponse.get('json').get('entity').get('listId'), createListPayload, campaignAndListType[1])
        Logger.log('GroupVersionId : {}, bucketId : {}'.format(groupVersionDetailResult, bucketId))
        addRecipientResponse, addRecipientPayload = campaignList.addRecipient({}, campaignId, createListresponse.get('json').get('entity').get('listId'), str(userType), int(numberOfUsers), int(customTagCount), newUser=False)
        campaignList.assertAddRecipient(addRecipientResponse, 200)
        campaignList.assertAddRecipientDbCalls(addRecipientResponse, addRecipientPayload, createListresponse, campaignId, bucketId, {'TEST':groupVersionDetailResult.get('TEST'), 'CONTROL':groupVersionDetailResult.get('CONTROL')}, userType)
        
    @pytest.mark.parametrize('campaignAndListType,userType,numberOfUsers,customTagCount', [
        (['LIVE', 'ORG', 'List', 'TAGS', 5], 'mobile', 5, 5),
        (['LIVE', 'CUSTOM', 'List', 'TAGS', 0], 'mobile', 1, 0),
        (['LIVE', 'CUSTOM', 'List', 'TAGS', 5], 'mobile', 5, 5),
        (['LIVE', 'SKIP', 'List', 'TAGS', 0], 'mobile', 1, 0),
        (['LIVE', 'SKIP', 'List', 'TAGS', 5], 'mobile', 5, 5),
        ])
    def test_addRecipient_LiveCampaign_mobile(self, campaignAndListType, userType, numberOfUsers, customTagCount):
        createListresponse, createListPayload, campaignId = campaignList.createList({'customTagCount':int(customTagCount), 'name':'IRIS_LIST_' + str(int(time.time() * 100000))}, campaignType=campaignAndListType)
        campaignList.assertCreateList(createListresponse, 200)
        groupVersionDetailResult, bucketId = campaignList.assertCreateListDbCalls(createListresponse.get('json').get('entity').get('listId'), createListPayload, campaignAndListType[1])
        Logger.log('GroupVersionId : {}, bucketId : {}'.format(groupVersionDetailResult, bucketId))
        addRecipientResponse, addRecipientPayload = campaignList.addRecipient({}, campaignId, createListresponse.get('json').get('entity').get('listId'), str(userType), int(numberOfUsers), int(customTagCount))
        campaignList.assertAddRecipient(addRecipientResponse, 200)
        campaignList.assertAddRecipientDbCalls(addRecipientResponse, addRecipientPayload, createListresponse, campaignId, bucketId, {'TEST':groupVersionDetailResult.get('TEST'), 'CONTROL':groupVersionDetailResult.get('CONTROL')}, userType)
    
    @pytest.mark.parametrize('campaignAndListType,userType,numberOfUsers,customTagCount', [
        (['LIVE', 'ORG', 'List', 'TAGS', 5], 'email', 5, 5),
        (['LIVE', 'CUSTOM', 'List', 'TAGS', 0], 'email', 1, 0),
        (['LIVE', 'CUSTOM', 'List', 'TAGS', 5], 'email', 5, 5),
        (['LIVE', 'SKIP', 'List', 'TAGS', 0], 'email', 1, 0),
        (['LIVE', 'SKIP', 'List', 'TAGS', 5], 'email', 5, 5),
        ])
    def test_addRecipient_LiveCampaign_email(self, campaignAndListType, userType, numberOfUsers, customTagCount):
        createListresponse, createListPayload, campaignId = campaignList.createList({'customTagCount':int(customTagCount), 'name':'IRIS_LIST_' + str(int(time.time() * 100000))}, campaignType=campaignAndListType)
        campaignList.assertCreateList(createListresponse, 200)
        groupVersionDetailResult, bucketId = campaignList.assertCreateListDbCalls(createListresponse.get('json').get('entity').get('listId'), createListPayload, campaignAndListType[1])
        Logger.log('GroupVersionId : {}, bucketId : {}'.format(groupVersionDetailResult, bucketId))
        addRecipientResponse, addRecipientPayload = campaignList.addRecipient({}, campaignId, createListresponse.get('json').get('entity').get('listId'), str(userType), int(numberOfUsers), int(customTagCount))
        campaignList.assertAddRecipient(addRecipientResponse, 200)
        campaignList.assertAddRecipientDbCalls(addRecipientResponse, addRecipientPayload, createListresponse, campaignId, bucketId, {'TEST':groupVersionDetailResult.get('TEST'), 'CONTROL':groupVersionDetailResult.get('CONTROL')}, userType)
     
    @pytest.mark.parametrize('campaignAndListType,userType,numberOfUsers,customTagCount', [
        (['UPCOMING', 'ORG', 'List', 'TAGS', 5], 'mobile', 5, 5),
        (['UPCOMING', 'CUSTOM', 'List', 'TAGS', 0], 'mobile', 1, 0),
        (['UPCOMING', 'CUSTOM', 'List', 'TAGS', 5], 'mobile', 5, 5),
        (['UPCOMING', 'SKIP', 'List', 'TAGS', 0], 'mobile', 1, 0),
        (['UPCOMING', 'SKIP', 'List', 'TAGS', 5], 'mobile', 5, 5),
        ])    
    def test_addRecipient_UpcomingCampaign_mobile(self, campaignAndListType, userType, numberOfUsers, customTagCount):
        createListresponse, createListPayload, campaignId = campaignList.createList({'customTagCount':int(customTagCount), 'name':'IRIS_LIST_' + str(int(time.time() * 100000))}, campaignType=campaignAndListType)
        campaignList.assertCreateList(createListresponse, 200)
        groupVersionDetailResult, bucketId = campaignList.assertCreateListDbCalls(createListresponse.get('json').get('entity').get('listId'), createListPayload, campaignAndListType[1])
        Logger.log('GroupVersionId : {}, bucketId : {}'.format(groupVersionDetailResult, bucketId))
        addRecipientResponse, addRecipientPayload = campaignList.addRecipient({}, campaignId, createListresponse.get('json').get('entity').get('listId'), str(userType), int(numberOfUsers), int(customTagCount))
        campaignList.assertAddRecipient(addRecipientResponse, 200)
        campaignList.assertAddRecipientDbCalls(addRecipientResponse, addRecipientPayload, createListresponse, campaignId, bucketId, {'TEST':groupVersionDetailResult.get('TEST'), 'CONTROL':groupVersionDetailResult.get('CONTROL')}, userType)
    
    @pytest.mark.parametrize('campaignAndListType,userType,numberOfUsers,customTagCount', [
        (['UPCOMING', 'ORG', 'List', 'TAGS', 5], 'email', 5, 5),
        (['UPCOMING', 'CUSTOM', 'List', 'TAGS', 0], 'email', 1, 0),
        (['UPCOMING', 'CUSTOM', 'List', 'TAGS', 5], 'email', 5, 5),
        (['UPCOMING', 'SKIP', 'List', 'TAGS', 0], 'email', 1, 0),
        (['UPCOMING', 'SKIP', 'List', 'TAGS', 5], 'email', 5, 5),
        ])    
    def test_addRecipient_UpcomingCampaign_email(self, campaignAndListType, userType, numberOfUsers, customTagCount):
        createListresponse, createListPayload, campaignId = campaignList.createList({'customTagCount':int(customTagCount), 'name':'IRIS_LIST_' + str(int(time.time() * 100000))}, campaignType=campaignAndListType)
        campaignList.assertCreateList(createListresponse, 200)
        groupVersionDetailResult, bucketId = campaignList.assertCreateListDbCalls(createListresponse.get('json').get('entity').get('listId'), createListPayload, campaignAndListType[1])
        Logger.log('GroupVersionId : {}, bucketId : {}'.format(groupVersionDetailResult, bucketId))
        addRecipientResponse, addRecipientPayload = campaignList.addRecipient({}, campaignId, createListresponse.get('json').get('entity').get('listId'), str(userType), int(numberOfUsers), int(customTagCount))
        campaignList.assertAddRecipient(addRecipientResponse, 200)
        campaignList.assertAddRecipientDbCalls(addRecipientResponse, addRecipientPayload, createListresponse, campaignId, bucketId, {'TEST':groupVersionDetailResult.get('TEST'), 'CONTROL':groupVersionDetailResult.get('CONTROL')}, userType)
        
    @pytest.mark.parametrize('campaignAndListType,userType,numberOfUsers,customTagCount', [
        (['LAPSED', 'ORG', 'List', 'TAGS', 5], 'mobile', 5, 5),
        (['LAPSED', 'CUSTOM', 'List', 'TAGS', 0], 'mobile', 1, 0),
        (['LAPSED', 'CUSTOM', 'List', 'TAGS', 5], 'mobile', 5, 5),
        (['LAPSED', 'SKIP', 'List', 'TAGS', 0], 'mobile', 1, 0),
        (['LAPSED', 'SKIP', 'List', 'TAGS', 5], 'mobile', 5, 5),
        ])    
    def test_addRecipient_LapsedCampaign_mobile(self, campaignAndListType, userType, numberOfUsers, customTagCount):
        createListresponse, createListPayload, campaignId = campaignList.createList({'customTagCount':int(customTagCount), 'name':'IRIS_LIST_' + str(int(time.time() * 100000))}, campaignType=campaignAndListType)
        campaignList.assertCreateList(createListresponse, 200)
        groupVersionDetailResult, bucketId = campaignList.assertCreateListDbCalls(createListresponse.get('json').get('entity').get('listId'), createListPayload, campaignAndListType[1])
        Logger.log('GroupVersionId : {}, bucketId : {}'.format(groupVersionDetailResult, bucketId))
        addRecipientResponse, addRecipientPayload = campaignList.addRecipient({}, campaignId, createListresponse.get('json').get('entity').get('listId'), str(userType), int(numberOfUsers), int(customTagCount))
        campaignList.assertAddRecipient(addRecipientResponse, 200)
        campaignList.assertAddRecipientDbCalls(addRecipientResponse, addRecipientPayload, createListresponse, campaignId, bucketId, {'TEST':groupVersionDetailResult.get('TEST'), 'CONTROL':groupVersionDetailResult.get('CONTROL')}, userType)
        
    @pytest.mark.parametrize('campaignAndListType,userType,numberOfUsers,customTagCount', [
        (['LAPSED', 'ORG', 'List', 'TAGS', 5], 'email', 5, 5),
        (['LAPSED', 'CUSTOM', 'List', 'TAGS', 0], 'email', 1, 0),
        (['LAPSED', 'CUSTOM', 'List', 'TAGS', 5], 'email', 5, 5),
        (['LAPSED', 'SKIP', 'List', 'TAGS', 0], 'email', 1, 0),
        (['LAPSED', 'SKIP', 'List', 'TAGS', 5], 'email', 5, 5),
        ])    
    def test_addRecipient_LapsedCampaign_email(self, campaignAndListType, userType, numberOfUsers, customTagCount):
        createListresponse, createListPayload, campaignId = campaignList.createList({'customTagCount':int(customTagCount), 'name':'IRIS_LIST_' + str(int(time.time() * 100000))}, campaignType=campaignAndListType)
        campaignList.assertCreateList(createListresponse, 200)
        groupVersionDetailResult, bucketId = campaignList.assertCreateListDbCalls(createListresponse.get('json').get('entity').get('listId'), createListPayload, campaignAndListType[1])
        Logger.log('GroupVersionId : {}, bucketId : {}'.format(groupVersionDetailResult, bucketId))
        addRecipientResponse, addRecipientPayload = campaignList.addRecipient({}, campaignId, createListresponse.get('json').get('entity').get('listId'), str(userType), int(numberOfUsers), int(customTagCount))
        campaignList.assertAddRecipient(addRecipientResponse, 200)
        campaignList.assertAddRecipientDbCalls(addRecipientResponse, addRecipientPayload, createListresponse, campaignId, bucketId, {'TEST':groupVersionDetailResult.get('TEST'), 'CONTROL':groupVersionDetailResult.get('CONTROL')}, userType)
        
    @pytest.mark.parametrize('campaignAndListType,userType,numberOfUsers,customTagCount,statusCode,errorCode,errorMessage', [
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'mobile', 1000, 0, 200, 000, ''),
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'mobile', 1001, 0, 400, 2007, "List Size Exception : Recipients list size should not exceed 1000"),
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'mobile', 0, 0, 400, 100, "Invalid request : Data can't be empty."),
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'email', 1000, 0, 200, 000, ''),
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'email', 1001, 0, 400, 2007, "List Size Exception : Recipients list size should not exceed 1000"),
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'email', 0, 0, 400, 100, "Invalid request : Data can't be empty."),
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'userId', 1000, 0, 200, 000, ''),
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'userId', 1001, 0, 400, 2007, "List Size Exception : Recipients list size should not exceed 1000"),
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'userId', 0, 0, 400, 100, "Invalid request : Data can't be empty."),
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'externalId', 1000, 0, 200, 000, ''),
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'externalId', 1001, 0, 400, 2007, "List Size Exception : Recipients list size should not exceed 1000"),
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'externalId', 0, 0, 400, 100, "Invalid request : Data can't be empty."),
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'userId,externalId', 1000, 0, 200, 000, ''),
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'userId,externalId', 1001, 0, 400, 2007, "List Size Exception : Recipients list size should not exceed 1000"),
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'userId,externalId', 0, 0, 400, 100, "Invalid request : Data can't be empty."),
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'mobile,userId', 1000, 0, 200, 000, ''),
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'mobile,userId', 1001, 0, 400, 2007, "List Size Exception : Recipients list size should not exceed 1000"),
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'mobile,userId', 0, 0, 400, 100, "Invalid request : Data can't be empty."),
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'mobile,externalId', 1000, 0, 200, 000, ''),
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'mobile,externalId', 1001, 0, 400, 2007, "List Size Exception : Recipients list size should not exceed 1000"),
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'mobile,externalId', 0, 0, 400, 100, "Invalid request : Data can't be empty."),
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'email,userId', 1000, 0, 200, 000, ''),
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'email,userId', 1001, 0, 400, 2007, "List Size Exception : Recipients list size should not exceed 1000"),
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'email,userId', 0, 0, 400, 100, "Invalid request : Data can't be empty."),
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'email,externalId', 1000, 0, 200, 000, ''),
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'email,externalId', 1001, 0, 400, 2007, "List Size Exception : Recipients list size should not exceed 1000"),
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'email,externalId', 0, 0, 400, 100, "Invalid request : Data can't be empty."),
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'mobile,email', 1000, 0, 200, 000, ''),
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'mobile,email', 1001, 0, 400, 2007, "List Size Exception : Recipients list size should not exceed 1000"),
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'mobile,email', 0, 0, 400, 100, "Invalid request : Data can't be empty."),
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'mobile,email,userId', 1000, 0, 200, 000, ''),
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'mobile,email,userId', 1001, 0, 400, 2007, "List Size Exception : Recipients list size should not exceed 1000"),
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'mobile,email,userId', 0, 0, 400, 100, "Invalid request : Data can't be empty."),
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'mobile,email,externalId', 1000, 0, 200, 000, ''),
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'mobile,email,externalId', 1001, 0, 400, 2007, "List Size Exception : Recipients list size should not exceed 1000"),
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'mobile,email,externalId', 0, 0, 400, 100, "Invalid request : Data can't be empty."),
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'mobile,email,userId,externalId', 1000, 0, 200, 000, ''),
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'mobile,email,userId,externalId', 1001, 0, 400, 2007, "List Size Exception : Recipients list size should not exceed 1000"),
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'mobile,email,userId,externalId', 0, 0, 400, 100, "Invalid request : Data can't be empty."),
        ])
    def test_addRecipient_BoundaryValue_NumberOfUsers(self, campaignAndListType, userType, numberOfUsers, customTagCount, statusCode, errorCode, errorMessage):
        createListresponse, createListPayload, campaignId = campaignList.createList({'customTagCount':int(customTagCount), 'name':'IRIS_LIST_' + str(int(time.time() * 100000))}, campaignType=campaignAndListType)
        campaignList.assertCreateList(createListresponse, 200)
        groupVersionDetailResult, bucketId = campaignList.assertCreateListDbCalls(createListresponse.get('json').get('entity').get('listId'), createListPayload, 'ORG')
        Logger.log('GroupVersionId : {}, bucketId : {}'.format(groupVersionDetailResult, bucketId))
        addRecipientResponse, addRecipientPayload = campaignList.addRecipient({}, campaignId, createListresponse.get('json').get('entity').get('listId'), str(userType), int(numberOfUsers), int(customTagCount), newUser=False)
        campaignList.assertAddRecipient(addRecipientResponse, statusCode, errorCode, errorMessage)
        
    @pytest.mark.parametrize('campaignAndListType,userType,numberOfUsers,customTagCount', [
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'mobile', 5, 0),
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'email', 5, 0),
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'mobile', 5, 5),
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'email', 5, 5),
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'mobile', 501, 0),
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'email', 501, 0) 
        ])
    def test_addRecipient_AppendingInSameList_NewUsers(self, campaignAndListType, userType, numberOfUsers, customTagCount):
        createListresponse, createListPayload, campaignId = campaignList.createList({'customTagCount':int(customTagCount), 'name':'IRIS_LIST_' + str(int(time.time() * 100000))}, campaignType=campaignAndListType)
        campaignList.assertCreateList(createListresponse, 200)
        groupVersionDetailResult, bucketId = campaignList.assertCreateListDbCalls(createListresponse.get('json').get('entity').get('listId'), createListPayload, 'ORG')
        Logger.log('GroupVersionId : {}, bucketId : {}'.format(groupVersionDetailResult, bucketId))
        addRecipientResponse, addRecipientPayload = campaignList.addRecipient({}, campaignId, createListresponse.get('json').get('entity').get('listId'), str(userType), int(numberOfUsers), int(customTagCount))
        campaignList.assertAddRecipient(addRecipientResponse, 200)
        Logger.log('Appending in the same list with listId :', createListresponse.get('json').get('entity').get('listId'))
        campaignList.assertAddRecipientDbCalls(addRecipientResponse, addRecipientPayload, createListresponse, campaignId, bucketId, {'TEST':groupVersionDetailResult.get('TEST'), 'CONTROL':groupVersionDetailResult.get('CONTROL')}, userType)
        addRecipientResponseSecondCall, addRecipientPayloadSecondCall = campaignList.addRecipient({}, campaignId, createListresponse.get('json').get('entity').get('listId'), str(userType), int(numberOfUsers), int(customTagCount))
        campaignList.assertAddRecipient(addRecipientResponseSecondCall, 200)
        for data in addRecipientPayload['data']:
            addRecipientPayloadSecondCall['data'].append(data)
        campaignList.assertAddRecipientDbCalls(addRecipientResponseSecondCall, addRecipientPayloadSecondCall, createListresponse, campaignId, bucketId, {'TEST':groupVersionDetailResult.get('TEST'), 'CONTROL':groupVersionDetailResult.get('CONTROL')}, userType)
      
    @pytest.mark.parametrize('campaignAndListType,userType,numberOfUsers,customTagCount,reason', [
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'mobile,email', 5, 0, ['Duplicate user id']),
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'mobile,email,userId', 5, 0, ['Duplicate user id']),
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'mobile,email,externalId', 5, 0, ['Duplicate user id']),
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'mobile,email,userId,externalId', 5, 0, ['Duplicate user id']),
        (['LIVE', 'ORG', 'List', 'TAGS', 5], 'mobile,email', 5, 5, ['Duplicate user id']),
        (['LIVE', 'ORG', 'List', 'TAGS', 5], 'mobile,email,userId', 5, 5, ['Duplicate user id']),
        (['LIVE', 'ORG', 'List', 'TAGS', 5], 'mobile,email,externalId', 5, 5, ['Duplicate user id']),
        (['LIVE', 'ORG', 'List', 'TAGS', 5], 'mobile,email,userId,externalId', 5, 5, ['Duplicate user id']),
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'mobile,email', 500, 0, ['Duplicate user id']),
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'mobile,email,userId', 500, 0, ['Duplicate user id']),
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'mobile,email,externalId', 500, 0, ['Duplicate user id']),
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'mobile,email,userId,externalId', 500, 0, ['Duplicate user id'])
        ])
    def test_addRecipient_AppendingInSameList_ExistingUser_DuplicateUserInSecondCall_V1(self, campaignAndListType, userType, numberOfUsers, customTagCount, reason):
        createListresponse, createListPayload, campaignId = campaignList.createList({'customTagCount':int(customTagCount), 'name':'IRIS_LIST_' + str(int(time.time() * 100000))}, campaignType=campaignAndListType)
        campaignList.assertCreateList(createListresponse, 200)
        groupVersionDetailResult, bucketId = campaignList.assertCreateListDbCalls(createListresponse.get('json').get('entity').get('listId'), createListPayload, 'ORG')
        Logger.log('GroupVersionId : {}, bucketId : {}'.format(groupVersionDetailResult, bucketId))
        addRecipientResponse, addRecipientPayload = campaignList.addRecipient({}, campaignId, createListresponse.get('json').get('entity').get('listId'), str(userType), int(numberOfUsers), int(customTagCount), newUser=False)
        campaignList.assertAddRecipient(addRecipientResponse, 200)
        Logger.log('Appending in the same list with listId :', createListresponse.get('json').get('entity').get('listId'))
        campaignList.assertAddRecipientDbCalls(addRecipientResponse, addRecipientPayload, createListresponse, campaignId, bucketId, {'TEST':groupVersionDetailResult.get('TEST'), 'CONTROL':groupVersionDetailResult.get('CONTROL')}, userType)
        addRecipientResponseAppendCall, addRecipientPayloadAppendCall = campaignList.addRecipient({}, campaignId, createListresponse.get('json').get('entity').get('listId'), str(userType), int(numberOfUsers * 2), int(customTagCount), newUser=False)
        campaignList.assertAddRecipient(addRecipientResponseAppendCall, 200)
        campaignList.assertInvalidDataInListResponse(addRecipientResponseAppendCall, addRecipientPayload['data'], reason)
        totalNumberOfUsersAddedInList = int(addRecipientResponseAppendCall['json']['entity']['test']) + int(addRecipientResponseAppendCall['json']['entity']['control'])
        Assertion.constructAssertion(totalNumberOfUsersAddedInList == int(numberOfUsers * 2), 'Matching Total Size in Response is :{}'.format({numberOfUsers * 2}))
        
    @pytest.mark.parametrize('campaignAndListType,userType,numberOfUsers,customTagCount,reason', [
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'userId', 5, 0, ['Duplicate user id']),
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'externalId', 5, 0, ['Duplicate user id']),
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'userId,externalId', 5, 0, ['Duplicate user id']),
        (['LIVE', 'ORG', 'List', 'TAGS', 5], 'userId', 5, 5, ['Duplicate user id']),
        (['LIVE', 'ORG', 'List', 'TAGS', 5], 'externalId', 5, 5, ['Duplicate user id']),
        (['LIVE', 'ORG', 'List', 'TAGS', 5], 'userId,externalId', 5, 5, ['Duplicate user id']),
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'userId', 500, 0, ['Duplicate user id']),
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'externalId', 500, 0, ['Duplicate user id']),
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'userId,externalId', 500, 0, ['Duplicate user id']),
        ])    
    def test_addRecipient_AppendingInSameList_ExistingUser_DuplicateUserInSecondCall_V2(self, campaignAndListType, userType, numberOfUsers, customTagCount, reason):
        createListresponse, createListPayload, campaignId = campaignList.createList({'customTagCount':int(customTagCount), 'name':'IRIS_LIST_' + str(int(time.time() * 100000))}, campaignType=campaignAndListType)
        campaignList.assertCreateList(createListresponse, 200)
        groupVersionDetailResult, bucketId = campaignList.assertCreateListDbCalls(createListresponse.get('json').get('entity').get('listId'), createListPayload, 'ORG')
        Logger.log('GroupVersionId : {}, bucketId : {}'.format(groupVersionDetailResult, bucketId))
        addRecipientResponse, addRecipientPayload = campaignList.addRecipient({}, campaignId, createListresponse.get('json').get('entity').get('listId'), str(userType), int(numberOfUsers), int(customTagCount), newUser=False)
        campaignList.assertAddRecipient(addRecipientResponse, 200)
        Logger.log('Appending in the same list with listId :', createListresponse.get('json').get('entity').get('listId'))
        addRecipientResponse, addRecipientPayloadSecondCall = campaignList.addRecipient({}, campaignId, createListresponse.get('json').get('entity').get('listId'), str(userType), int(numberOfUsers * 2), int(customTagCount), newUser=False)
        campaignList.assertAddRecipient(addRecipientResponse, 200)
        campaignList.assertInvalidDataInListResponse(addRecipientResponse, addRecipientPayload['data'], reason)
        totalNumberOfUsersAddedInList = int(addRecipientResponse['json']['entity']['test']) + int(addRecipientResponse['json']['entity']['control'])
        Assertion.constructAssertion(totalNumberOfUsersAddedInList == int(numberOfUsers * 2), 'Matching Total Size in Response is :'.format({numberOfUsers * 2}))
        
    @pytest.mark.parametrize('campaignAndListType,schema,data,reasonResponse', [
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'firstName,lastName,mobile', ['Test1,Automation1,xyz@gmail.com'], ['Invalid mobile number']),
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'firstName,lastName,email', ['Test1,Automation1,8497846843'], ['Invalid Email Id']),
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'firstName,lastName,userId', ['Test1,Automation1,xyz@gmail.com'], ['Invalid User Id']),
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'firstName,lastName,externalId', ['Test2,Automation2,8497846843'], ['Invalid External Id']),
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'firstName,lastName,userId,externalId', ['Test3,Automation3,8497846843,8497846843'], ['Invalid External Id', 'Invalid User Id']),
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'firstName,lastName,mobile,email', ['Test3,Automation3,iris1,iris2'], ['Invalid mobile number', 'Invalid Email Id']),
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'firstName,lastName,mobile,email,userId', ['Test3,Automation3,xyz@gmail.com,8497846843,irsi1'], ['Invalid mobile number', 'Invalid Email Id', 'Invalid User Id']),
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'firstName,lastName,mobile,email,externalId', ['Test3,Automation3,xyz@gmail.com,8497846843,irsi1'], ['Invalid mobile number', 'Invalid Email Id', 'Invalid External Id']),
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'firstName,lastName,mobile,email,userId,externalId', ['Test3,Automation3,xyz@gmail.com,8497846843,8497846843,123'], ['Invalid mobile number', 'Invalid Email Id', 'Invalid User Id', 'Invalid External Id']),
        (['LIVE', 'ORG', 'List', 'TAGS', 1], 'firstName,lastName,mobile,customTag1', ['Test3,Automation3,xyz@gmail.com,tag1'], ['Invalid mobile number']),
        (['LIVE', 'ORG', 'List', 'TAGS', 1], 'firstName,lastName,mobile,email,userId,externalId,customTag1', ['Test3,Automation3,xyz@gmail.com,8497846843,8497846843,123,tag1'], ['Invalid mobile number', 'Invalid Email Id', 'Invalid User Id', 'Invalid External Id'])
        ])
    def test_addRecipient_WrongSchemaAndData(self, campaignAndListType, schema, data, reasonResponse):
        createListresponse, createListPayload, campaignId = campaignList.createList({'name':'IRIS_LIST_' + str(int(time.time() * 100000)), 'customTagCount':campaignAndListType[4]}, campaignType=campaignAndListType)
        campaignList.assertCreateList(createListresponse, 200)
        groupVersionDetailResult, bucketId = campaignList.assertCreateListDbCalls(createListresponse.get('json').get('entity').get('listId'), createListPayload, 'ORG')
        Logger.log('GroupVersionId : {}, bucketId : {}'.format(groupVersionDetailResult, bucketId))
        addRecipientResponse, addRecipientPayload = campaignList.addRecipient({'schema':schema, 'data':data}, campaignId, createListresponse.get('json').get('entity').get('listId'))
        campaignList.assertAddRecipient(addRecipientResponse, 200)
        campaignList.assertInvalidDataInListResponse(addRecipientResponse, data, reasonResponse)
    
    @pytest.mark.parametrize('campaignAndListType,userType,numberOfUsers,customTagCountAddRecipient', [
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'mobile', 2, 5),
        (['LIVE', 'ORG', 'List', 'TAGS', 5], 'mobile', 2, 0),
        (['LIVE', 'ORG', 'List', 'TAGS', 1], 'mobile', 2, 2),
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'email', 2, 5),
        (['LIVE', 'ORG', 'List', 'TAGS', 5], 'email', 2, 0),
        (['LIVE', 'ORG', 'List', 'TAGS', 1], 'email', 2, 2),
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'userId', 2, 5),
        (['LIVE', 'ORG', 'List', 'TAGS', 5], 'userId', 2, 0),
        (['LIVE', 'ORG', 'List', 'TAGS', 1], 'userId', 2, 2),
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'externalId', 2, 5),
        (['LIVE', 'ORG', 'List', 'TAGS', 5], 'externalId', 2, 0),
        (['LIVE', 'ORG', 'List', 'TAGS', 1], 'externalId', 2, 2),
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'userId,externalId', 2, 5),
        (['LIVE', 'ORG', 'List', 'TAGS', 5], 'userId,externalId', 2, 0),
        (['LIVE', 'ORG', 'List', 'TAGS', 1], 'userId,externalId', 2, 2),
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'mobile,email', 2, 5),
        (['LIVE', 'ORG', 'List', 'TAGS', 5], 'mobile,email', 2, 0),
        (['LIVE', 'ORG', 'List', 'TAGS', 1], 'mobile,email', 2, 2),
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'mobile,email,userId', 2, 5),
        (['LIVE', 'ORG', 'List', 'TAGS', 5], 'mobile,email,userId', 2, 0),
        (['LIVE', 'ORG', 'List', 'TAGS', 1], 'mobile,email,userId', 2, 2),
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'mobile,email,externalId', 2, 5),
        (['LIVE', 'ORG', 'List', 'TAGS', 5], 'mobile,email,externalId', 2, 0),
        (['LIVE', 'ORG', 'List', 'TAGS', 1], 'mobile,email,externalId', 2, 2),
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'mobile,email,userId,externalId', 2, 5),
        (['LIVE', 'ORG', 'List', 'TAGS', 5], 'mobile,email,userId,externalId', 2, 0),
        (['LIVE', 'ORG', 'List', 'TAGS', 1], 'mobile,email,userId,externalId', 2, 2)
        ])
    def test_addRecipient_WrongValuesInCustomTagAndDataPassed(self, campaignAndListType, userType, numberOfUsers, customTagCountAddRecipient):
        createListresponse, createListPayload, campaignId = campaignList.createList({'customTagCount':int(campaignAndListType[4]), 'name':'IRIS_LIST_' + str(int(time.time() * 100000))}, campaignType=campaignAndListType)
        campaignList.assertCreateList(createListresponse, 200)
        groupVersionDetailResult, bucketId = campaignList.assertCreateListDbCalls(createListresponse.get('json').get('entity').get('listId'), createListPayload, 'ORG')
        Logger.log('GroupVersionId : {}, bucketId : {}'.format(groupVersionDetailResult, bucketId))
        addRecipientResponse, addRecipientPayload = campaignList.addRecipient({}, campaignId, createListresponse.get('json').get('entity').get('listId'), str(userType), int(numberOfUsers), int(customTagCountAddRecipient), newUser=False)
        campaignList.assertAddRecipient(addRecipientResponse, 400, 2012, 'Invalid Schema : Invalid Custom Tags Count')
    
    @pytest.mark.parametrize('campaignAndListType,schema,data', [
        (['LIVE', 'ORG', 'List', 'TAGS', 1], 'firstName,lastName,mobile,customTag0', ['Test1,Automation1,8497846843,tag1', 'Test1,Automation1,8497846843,tag1']),
        ])
    def test_addRecipient_invalidFieldNames(self, campaignAndListType, schema, data):
        createListresponse, createListPayload, campaignId = campaignList.createList({'name':'IRIS_LIST_' + str(int(time.time() * 100000)), 'customTagCount':campaignAndListType[4]}, campaignType=campaignAndListType)
        campaignList.assertCreateList(createListresponse, 200)
        groupVersionDetailResult, bucketId = campaignList.assertCreateListDbCalls(createListresponse.get('json').get('entity').get('listId'), createListPayload, 'ORG')
        Logger.log('GroupVersionId : {}, bucketId : {}'.format(groupVersionDetailResult, bucketId))
        addRecipientResponse, addRecipientPayload = campaignList.addRecipient({'schema':schema, 'data':data}, campaignId, createListresponse.get('json').get('entity').get('listId'))
        campaignList.assertAddRecipient(addRecipientResponse, 400, 2012, 'Invalid Schema : Schema Contains Invalid Field Names')
        
    @pytest.mark.parametrize('campaignAndListType,schema,data', [
        (['LIVE', 'ORG', 'List', 'TAGS', 1], 'firstName,lastName,mobile,customTag1', ['Test1,Automation1,8497846843,tag1,tag2', 'Test1,Automation1,8497846843,tag1,tag2']),
        ])
    def test_addRecipient_dataDoesntMatchWithSchema(self, campaignAndListType, schema, data):
        createListresponse, createListPayload, campaignId = campaignList.createList({'name':'IRIS_LIST_' + str(int(time.time() * 100000)), 'customTagCount':campaignAndListType[4]}, campaignType=campaignAndListType)
        campaignList.assertCreateList(createListresponse, 200)
        groupVersionDetailResult, bucketId = campaignList.assertCreateListDbCalls(createListresponse.get('json').get('entity').get('listId'), createListPayload, 'ORG')
        Logger.log('GroupVersionId : {}, bucketId : {}'.format(groupVersionDetailResult, bucketId))
        addRecipientResponse, addRecipientPayload = campaignList.addRecipient({'schema':schema, 'data':data}, campaignId, createListresponse.get('json').get('entity').get('listId'))
        campaignList.assertAddRecipient(addRecipientResponse, 200)
        campaignList.assertInvalidDataInListResponse(addRecipientResponse, data, ['Data does not match with schema'])
    
    
    @pytest.mark.parametrize('campaignAndListType', [
        (['LIVE', 'ORG', 'List', 'TAGS', 0])
        ])
    def test_addRecipient_WrongDataSourceInSchema(self, campaignAndListType):
        createListresponse, createListPayload, campaignId = campaignList.createList({'name':'IRIS_LIST_' + str(int(time.time() * 100000))}, campaignType=campaignAndListType)
        campaignList.assertCreateList(createListresponse, 200)
        groupVersionDetailResult, bucketId = campaignList.assertCreateListDbCalls(createListresponse.get('json').get('entity').get('listId'), createListPayload, 'ORG')
        Logger.log('GroupVersionId : {}, bucketId : {}'.format(groupVersionDetailResult, bucketId))
        addRecipientResponse, addRecipientPayload = campaignList.addRecipient({'dataSource':'wrong'}, campaignId, createListresponse.get('json').get('entity').get('listId'))
        campaignList.assertAddRecipient(addRecipientResponse, 400, 100, 'Invalid request : Invalid dataSource. ')

    @pytest.mark.parametrize('campaignAndListType,keyToPop,statusCode,errorCode,errorMessage', [
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'dataSource', 400, 100, 'Invalid request : Invalid dataSource. '),
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'schema', 400, 100, 'Invalid request : Invalid schema'),
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'data', 400, 100, 'Invalid request : Invalid data')  
        ])   
    def test_addRecipient_popKeysFromAddRecipientPayload(self, campaignAndListType, keyToPop, statusCode, errorCode, errorMessage):
        createListresponse, createListPayload, campaignId = campaignList.createList({'name':'IRIS_LIST_' + str(int(time.time() * 100000))}, campaignType=campaignAndListType)
        campaignList.assertCreateList(createListresponse, 200)
        groupVersionDetailResult, bucketId = campaignList.assertCreateListDbCalls(createListresponse.get('json').get('entity').get('listId'), createListPayload, 'ORG')
        Logger.log('GroupVersionId : {}, bucketId : {}'.format(groupVersionDetailResult, bucketId))
        addRecipientResponse, addRecipientPayload = campaignList.addRecipient(keyToPop, campaignId, createListresponse.get('json').get('entity').get('listId'), process='pop')
        campaignList.assertAddRecipient(addRecipientResponse, statusCode, errorCode, errorMessage)
  
    @pytest.mark.parametrize('campaignAndListType,schema,data,invalidReason', [
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'firstName,lastName,mobile', ['Test1,Automation1,8497846843', 'Test1,Automation1,8497846843'], ['Duplicate mobile number']),
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'firstName,lastName,email', ['Test1,Automation1,xyz@gmail.com', 'Test1,Automation1,xyz@gmail.com'], ['Duplicate Email']),
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'firstName,lastName,userId', ['Test1,Automation1,' + str(constant.irisGenericValues['existingUserId']), 'Test1,Automation1,' + str(constant.irisGenericValues['existingUserId'])], ['Duplicate User Id']),  # Failed 
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'firstName,lastName,externalId', ['Test1,Automation1,' + str(constant.irisGenericValues['existingUserExternalId']), 'Test1,Automation1,' + str(constant.irisGenericValues['existingUserExternalId'])], ['Duplicate External Id']),  # Failed 
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'firstName,lastName,externalId,userId', ['Test1,Automation1,' + str(constant.irisGenericValues['existingUserExternalId']) + ',' + str(constant.irisGenericValues['existingUserId']), 'Test1,Automation1,' + str(constant.irisGenericValues['existingUserExternalId']) + ',' + str(constant.irisGenericValues['existingUserId'])], ['Duplicate External Id', 'Duplicate User Id'])  # Failed 
        ])
    def test_addRecipient_DuplicateData(self, campaignAndListType, schema, data, invalidReason): 
        createListresponse, createListPayload, campaignId = campaignList.createList({'name':'IRIS_LIST_' + str(int(time.time() * 100000))}, campaignType=campaignAndListType)
        campaignList.assertCreateList(createListresponse, 200)
        groupVersionDetailResult, bucketId = campaignList.assertCreateListDbCalls(createListresponse.get('json').get('entity').get('listId'), createListPayload, 'ORG')
        Logger.log('GroupVersionId : {}, bucketId : {}'.format(groupVersionDetailResult, bucketId))
        addRecipientResponse, addRecipientPayload = campaignList.addRecipient({'schema':schema, 'data':data}, campaignId, createListresponse.get('json').get('entity').get('listId'))
        campaignList.assertAddRecipient(addRecipientResponse, 200)
        Assertion.constructAssertion(addRecipientResponse.get('json').get('entity').get('test') == 1, 'Matching test count to be 1 as 2 data were passed of same details')
        campaignList.assertInvalidDataInListResponse(addRecipientResponse, list(set(data)), invalidReason)
    
    @pytest.mark.parametrize('campaignAndListType,schema,data,invalidReason', [
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'firstName,lastName,mobile,email', ['Test1,Automation1,8497846843,xyz@gmail.com', 'Test1,Automation1,8497846843,xyz@gmail.com'], ['Duplicate Email', 'Duplicate mobile number']),  # Failed 
        ])
    def test_addRecipient_DuplicateData_MixOfMultipleUser(self, campaignAndListType, schema, data, invalidReason): 
        createListresponse, createListPayload, campaignId = campaignList.createList({'name':'IRIS_LIST_' + str(int(time.time() * 100000))}, campaignType=campaignAndListType)
        campaignList.assertCreateList(createListresponse, 200)
        groupVersionDetailResult, bucketId = campaignList.assertCreateListDbCalls(createListresponse.get('json').get('entity').get('listId'), createListPayload, 'ORG')
        Logger.log('GroupVersionId : {}, bucketId : {}'.format(groupVersionDetailResult, bucketId))
        addRecipientResponse, addRecipientPayload = campaignList.addRecipient({'schema':schema, 'data':data}, campaignId, createListresponse.get('json').get('entity').get('listId'))
        campaignList.assertAddRecipient(addRecipientResponse, 200)
        Assertion.constructAssertion(addRecipientResponse.get('json').get('entity').get('test') == 2, 'Matching test count to be 2 as 2 data were passed of same details and are mix of 2 different users')
        campaignList.assertInvalidDataInListResponse(addRecipientResponse, list(set(data)), invalidReason)
    
    
    @pytest.mark.parametrize('campaignAndListType,userType,numberOfUsers,customTagCount', [
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'mobile', 5, 0),
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'email', 5, 0)
        ])
    def test_addRecipient_AppendingWithDuplicateData(self, campaignAndListType, userType, numberOfUsers, customTagCount):
        createListresponse, createListPayload, campaignId = campaignList.createList({'customTagCount':int(customTagCount), 'name':'IRIS_LIST_' + str(int(time.time() * 100000))}, campaignType=campaignAndListType)
        campaignList.assertCreateList(createListresponse, 200)
        groupVersionDetailResult, bucketId = campaignList.assertCreateListDbCalls(createListresponse.get('json').get('entity').get('listId'), createListPayload, 'ORG')
        Logger.log('GroupVersionId : {}, bucketId : {}'.format(groupVersionDetailResult, bucketId))
        addRecipientResponse, addRecipientPayload = campaignList.addRecipient({}, campaignId, createListresponse.get('json').get('entity').get('listId'), str(userType), int(numberOfUsers), int(customTagCount))
        campaignList.assertAddRecipient(addRecipientResponse, 200)
        Logger.log('Appending in the same list with listId :', createListresponse.get('json').get('entity').get('listId'))
        campaignList.assertAddRecipientDbCalls(addRecipientResponse, addRecipientPayload, createListresponse, campaignId, bucketId, {'TEST':groupVersionDetailResult.get('TEST'), 'CONTROL':groupVersionDetailResult.get('CONTROL')}, userType)
        addRecipientResponseSecondCall, addRecipientPayloadSecondCall = campaignList.addRecipient(addRecipientPayload, campaignId, createListresponse.get('json').get('entity').get('listId'))
        campaignList.assertAddRecipient(addRecipientResponseSecondCall, 200)
        campaignList.assertAddRecipientDbCalls(addRecipientResponseSecondCall, addRecipientPayloadSecondCall, createListresponse, campaignId, bucketId, {'TEST':groupVersionDetailResult.get('TEST'), 'CONTROL':groupVersionDetailResult.get('CONTROL')}, userType)
        campaignList.assertInvalidDataInListResponse(addRecipientResponseSecondCall, addRecipientPayload['data'], ['Duplicate user id'])    
        
    def test_addRecipient_WrongCampaignId(self):
        createListresponse, createListPayload, campaignId = campaignList.createList({'name':'IRIS_LIST_' + str(int(time.time() * 100000))}, campaignType=['LIVE', 'ORG', 'List', 'TAGS', 0])
        campaignList.assertCreateList(createListresponse, 200)
        groupVersionDetailResult, bucketId = campaignList.assertCreateListDbCalls(createListresponse.get('json').get('entity').get('listId'), createListPayload, 'ORG')
        Logger.log('GroupVersionId : {}, bucketId : {}'.format(groupVersionDetailResult, bucketId))
        addRecipientResponse, addRecipientPayload = campaignList.addRecipient({}, 0, createListresponse.get('json').get('entity').get('listId'))
        campaignList.assertAddRecipient(addRecipientResponse, 400, 100, 'Invalid request : must be greater than or equal to 1')
    
    def test_addRecipient_WrongListId(self):
        createListresponse, createListPayload, campaignId = campaignList.createList({'name':'IRIS_LIST_' + str(int(time.time() * 100000))}, campaignType=['LIVE', 'ORG', 'List', 'TAGS', 0])
        campaignList.assertCreateList(createListresponse, 200)
        groupVersionDetailResult, bucketId = campaignList.assertCreateListDbCalls(createListresponse.get('json').get('entity').get('listId'), createListPayload, 'ORG')
        Logger.log('GroupVersionId : {}, bucketId : {}'.format(groupVersionDetailResult, bucketId))
        addRecipientResponse, addRecipientPayload = campaignList.addRecipient({}, campaignId, 0)
        campaignList.assertAddRecipient(addRecipientResponse, 400, 100, 'Invalid request : must be greater than or equal to 1')
