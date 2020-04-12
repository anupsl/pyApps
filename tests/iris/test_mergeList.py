import pytest, time, Queue, pytest_ordering
from time import sleep
from threading import Thread
from src.Constant.constant import constant
from src.modules.iris.list import campaignList
from src.utilities.logger import Logger
from src.utilities.assertion import Assertion
from src.modules.iris.campaigns import campaigns
from src.modules.iris.dbCallsCampaign import dbCallsCampaign
from src.modules.iris.dbCallsList import dbCallsList
from src.modules.iris.construct import construct

@pytest.mark.run(order=4)
class Test_MergeList():
    
    def setup_method(self, method):
        Logger.logMethodName(method.__name__)
    
    @pytest.mark.parametrize('campaignAndListType,userType,numberOfUsers,customTagCount', [
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'mobile', 5, 0),
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'email', 5, 0)
        ])
    def test_mergeList_Sanity(self, campaignAndListType, userType, numberOfUsers, customTagCount):
        mergeListresponse, mergeListPayload, campaignId = campaignList.mergeList({}, campaignType=campaignAndListType, userType=userType, numberOfUsers=numberOfUsers, numberOfCustomTags=customTagCount)
        campaignList.assertMergeList(mergeListresponse, 200)
        groupVersionDetailResult, bucketId = campaignList.assertCreateListDbCalls(mergeListresponse.get('json').get('entity').get('listId'), mergeListPayload, campaignAndListType[1], expectedTestUsers=mergeListresponse.get('json').get('entity').get('recipientsResponse').get('test'), expectedControlUsers=mergeListresponse.get('json').get('entity').get('recipientsResponse').get('control'))
        Logger.log('GroupVersionId : {}, bucketId : {}'.format(groupVersionDetailResult, bucketId))
        addRecipientResponse = {'json':{'entity':mergeListresponse.get('json').get('entity').get('recipientsResponse')}}
        campaignList.assertAddRecipientDbCalls(addRecipientResponse, mergeListPayload.get('recipients'), mergeListresponse, campaignId, bucketId, {'TEST':groupVersionDetailResult.get('TEST'), 'CONTROL':groupVersionDetailResult.get('CONTROL')}, userType)

    @pytest.mark.parametrize('campaignAndListType,userType,numberOfUsers,customTagCount', [
        (['LIVE', 'ORG', 'List', 'TAGS', 1], 'mobile', 1, 1),
        (['LIVE', 'ORG', 'List', 'TAGS', 2], 'mobile', 2, 2),
        (['LIVE', 'ORG', 'List', 'TAGS', 3], 'mobile', 3, 3),
        (['LIVE', 'ORG', 'List', 'TAGS', 4], 'mobile', 4, 4),
        (['LIVE', 'ORG', 'List', 'TAGS', 5], 'mobile', 5, 5),
        (['LIVE', 'CUSTOM', 'List', 'TAGS', 0], 'mobile', 1, 0),
        (['LIVE', 'CUSTOM', 'List', 'TAGS', 1], 'mobile', 1, 1),
        (['LIVE', 'CUSTOM', 'List', 'TAGS', 2], 'mobile', 2, 2),
        (['LIVE', 'CUSTOM', 'List', 'TAGS', 3], 'mobile', 3, 3),
        (['LIVE', 'CUSTOM', 'List', 'TAGS', 4], 'mobile', 4, 4),
        (['LIVE', 'CUSTOM', 'List', 'TAGS', 5], 'mobile', 5, 5),
        (['LIVE', 'SKIP', 'List', 'TAGS', 0], 'mobile', 1, 0),
        (['LIVE', 'SKIP', 'List', 'TAGS', 1], 'mobile', 1, 1),
        (['LIVE', 'SKIP', 'List', 'TAGS', 2], 'mobile', 2, 2),
        (['LIVE', 'SKIP', 'List', 'TAGS', 3], 'mobile', 3, 3),
        (['LIVE', 'SKIP', 'List', 'TAGS', 4], 'mobile', 4, 4),
        (['LIVE', 'SKIP', 'List', 'TAGS', 5], 'mobile', 5, 5),
        ])
    def test_mergeList_LiveCampaign_mobile(self, campaignAndListType, userType, numberOfUsers, customTagCount):
        mergeListresponse, mergeListPayload, campaignId = campaignList.mergeList({}, campaignType=campaignAndListType, userType=userType, numberOfUsers=numberOfUsers, numberOfCustomTags=customTagCount)
        campaignList.assertMergeList(mergeListresponse, 200)
        groupVersionDetailResult, bucketId = campaignList.assertCreateListDbCalls(mergeListresponse.get('json').get('entity').get('listId'), mergeListPayload, campaignAndListType[1], expectedTestUsers=mergeListresponse.get('json').get('entity').get('recipientsResponse').get('test'), expectedControlUsers=mergeListresponse.get('json').get('entity').get('recipientsResponse').get('control'))
        Logger.log('GroupVersionId : {}, bucketId : {}'.format(groupVersionDetailResult, bucketId))
        addRecipientResponse = {'json':{'entity':mergeListresponse.get('json').get('entity').get('recipientsResponse')}}
        campaignList.assertAddRecipientDbCalls(addRecipientResponse, mergeListPayload.get('recipients'), mergeListresponse, campaignId, bucketId, {'TEST':groupVersionDetailResult.get('TEST'), 'CONTROL':groupVersionDetailResult.get('CONTROL')}, userType)
    
    @pytest.mark.parametrize('campaignAndListType,userType,numberOfUsers,customTagCount', [
        (['LIVE', 'ORG', 'List', 'TAGS', 1], 'email', 1, 1),
        (['LIVE', 'ORG', 'List', 'TAGS', 2], 'email', 2, 2),
        (['LIVE', 'ORG', 'List', 'TAGS', 3], 'email', 3, 3),
        (['LIVE', 'ORG', 'List', 'TAGS', 4], 'email', 4, 4),
        (['LIVE', 'ORG', 'List', 'TAGS', 5], 'email', 5, 5),
        (['LIVE', 'CUSTOM', 'List', 'TAGS', 0], 'email', 1, 0),
        (['LIVE', 'CUSTOM', 'List', 'TAGS', 1], 'email', 1, 1),
        (['LIVE', 'CUSTOM', 'List', 'TAGS', 2], 'email', 2, 2),
        (['LIVE', 'CUSTOM', 'List', 'TAGS', 3], 'email', 3, 3),
        (['LIVE', 'CUSTOM', 'List', 'TAGS', 4], 'email', 4, 4),
        (['LIVE', 'CUSTOM', 'List', 'TAGS', 5], 'email', 5, 5),
        (['LIVE', 'SKIP', 'List', 'TAGS', 0], 'email', 1, 0),
        (['LIVE', 'SKIP', 'List', 'TAGS', 1], 'email', 1, 1),
        (['LIVE', 'SKIP', 'List', 'TAGS', 2], 'email', 2, 2),
        (['LIVE', 'SKIP', 'List', 'TAGS', 3], 'email', 3, 3),
        (['LIVE', 'SKIP', 'List', 'TAGS', 4], 'email', 4, 4),
        (['LIVE', 'SKIP', 'List', 'TAGS', 5], 'email', 5, 5),
        ])
    def test_mergeList_LiveCampaign_email(self, campaignAndListType, userType, numberOfUsers, customTagCount):
        mergeListresponse, mergeListPayload, campaignId = campaignList.mergeList({}, campaignType=campaignAndListType, userType=userType, numberOfUsers=numberOfUsers, numberOfCustomTags=customTagCount)
        campaignList.assertMergeList(mergeListresponse, 200)
        groupVersionDetailResult, bucketId = campaignList.assertCreateListDbCalls(mergeListresponse.get('json').get('entity').get('listId'), mergeListPayload, campaignAndListType[1], expectedTestUsers=mergeListresponse.get('json').get('entity').get('recipientsResponse').get('test'), expectedControlUsers=mergeListresponse.get('json').get('entity').get('recipientsResponse').get('control'))
        Logger.log('GroupVersionId : {}, bucketId : {}'.format(groupVersionDetailResult, bucketId))
        addRecipientResponse = {'json':{'entity':mergeListresponse.get('json').get('entity').get('recipientsResponse')}}
        campaignList.assertAddRecipientDbCalls(addRecipientResponse, mergeListPayload.get('recipients'), mergeListresponse, campaignId, bucketId, {'TEST':groupVersionDetailResult.get('TEST'), 'CONTROL':groupVersionDetailResult.get('CONTROL')}, userType)

    @pytest.mark.parametrize('campaignAndListType,userType,numberOfUsers,customTagCount', [
        (['UPCOMING', 'ORG', 'List', 'TAGS', 1], 'mobile', 1, 1),
        (['UPCOMING', 'ORG', 'List', 'TAGS', 2], 'mobile', 2, 2),
        (['UPCOMING', 'ORG', 'List', 'TAGS', 3], 'mobile', 3, 3),
        (['UPCOMING', 'ORG', 'List', 'TAGS', 4], 'mobile', 4, 4),
        (['UPCOMING', 'ORG', 'List', 'TAGS', 5], 'mobile', 5, 5),
        (['UPCOMING', 'CUSTOM', 'List', 'TAGS', 0], 'mobile', 1, 0),
        (['UPCOMING', 'CUSTOM', 'List', 'TAGS', 1], 'mobile', 1, 1),
        (['UPCOMING', 'CUSTOM', 'List', 'TAGS', 2], 'mobile', 2, 2),
        (['UPCOMING', 'CUSTOM', 'List', 'TAGS', 3], 'mobile', 3, 3),
        (['UPCOMING', 'CUSTOM', 'List', 'TAGS', 4], 'mobile', 4, 4),
        (['UPCOMING', 'CUSTOM', 'List', 'TAGS', 5], 'mobile', 5, 5),
        (['UPCOMING', 'SKIP', 'List', 'TAGS', 0], 'mobile', 1, 0),
        (['UPCOMING', 'SKIP', 'List', 'TAGS', 1], 'mobile', 1, 1),
        (['UPCOMING', 'SKIP', 'List', 'TAGS', 2], 'mobile', 2, 2),
        (['UPCOMING', 'SKIP', 'List', 'TAGS', 3], 'mobile', 3, 3),
        (['UPCOMING', 'SKIP', 'List', 'TAGS', 4], 'mobile', 4, 4),
        (['UPCOMING', 'SKIP', 'List', 'TAGS', 5], 'mobile', 5, 5),
        ])    
    def test_mergeList_UpcomingCampaign_mobile(self, campaignAndListType, userType, numberOfUsers, customTagCount):
        mergeListresponse, mergeListPayload, campaignId = campaignList.mergeList({}, campaignType=campaignAndListType, userType=userType, numberOfUsers=numberOfUsers, numberOfCustomTags=customTagCount)
        campaignList.assertMergeList(mergeListresponse, 200)
        groupVersionDetailResult, bucketId = campaignList.assertCreateListDbCalls(mergeListresponse.get('json').get('entity').get('listId'), mergeListPayload, campaignAndListType[1], expectedTestUsers=mergeListresponse.get('json').get('entity').get('recipientsResponse').get('test'), expectedControlUsers=mergeListresponse.get('json').get('entity').get('recipientsResponse').get('control'))
        Logger.log('GroupVersionId : {}, bucketId : {}'.format(groupVersionDetailResult, bucketId))
        addRecipientResponse = {'json':{'entity':mergeListresponse.get('json').get('entity').get('recipientsResponse')}}
        campaignList.assertAddRecipientDbCalls(addRecipientResponse, mergeListPayload.get('recipients'), mergeListresponse, campaignId, bucketId, {'TEST':groupVersionDetailResult.get('TEST'), 'CONTROL':groupVersionDetailResult.get('CONTROL')}, userType)

    @pytest.mark.parametrize('campaignAndListType,userType,numberOfUsers,customTagCount', [
        (['UPCOMING', 'ORG', 'List', 'TAGS', 1], 'email', 1, 1),
        (['UPCOMING', 'ORG', 'List', 'TAGS', 2], 'email', 2, 2),
        (['UPCOMING', 'ORG', 'List', 'TAGS', 3], 'email', 3, 3),
        (['UPCOMING', 'ORG', 'List', 'TAGS', 4], 'email', 4, 4),
        (['UPCOMING', 'ORG', 'List', 'TAGS', 5], 'email', 5, 5),
        (['UPCOMING', 'CUSTOM', 'List', 'TAGS', 0], 'email', 1, 0),
        (['UPCOMING', 'CUSTOM', 'List', 'TAGS', 1], 'email', 1, 1),
        (['UPCOMING', 'CUSTOM', 'List', 'TAGS', 2], 'email', 2, 2),
        (['UPCOMING', 'CUSTOM', 'List', 'TAGS', 3], 'email', 3, 3),
        (['UPCOMING', 'CUSTOM', 'List', 'TAGS', 4], 'email', 4, 4),
        (['UPCOMING', 'CUSTOM', 'List', 'TAGS', 5], 'email', 5, 5),
        (['UPCOMING', 'SKIP', 'List', 'TAGS', 0], 'email', 1, 0),
        (['UPCOMING', 'SKIP', 'List', 'TAGS', 1], 'email', 1, 1),
        (['UPCOMING', 'SKIP', 'List', 'TAGS', 2], 'email', 2, 2),
        (['UPCOMING', 'SKIP', 'List', 'TAGS', 3], 'email', 3, 3),
        (['UPCOMING', 'SKIP', 'List', 'TAGS', 4], 'email', 4, 4),
        (['UPCOMING', 'SKIP', 'List', 'TAGS', 5], 'email', 5, 5),
        ])    
    def test_mergeList_UpcomingCampaign_email(self, campaignAndListType, userType, numberOfUsers, customTagCount):
        mergeListresponse, mergeListPayload, campaignId = campaignList.mergeList({}, campaignType=campaignAndListType, userType=userType, numberOfUsers=numberOfUsers, numberOfCustomTags=customTagCount)
        campaignList.assertMergeList(mergeListresponse, 200)
        groupVersionDetailResult, bucketId = campaignList.assertCreateListDbCalls(mergeListresponse.get('json').get('entity').get('listId'), mergeListPayload, campaignAndListType[1], expectedTestUsers=mergeListresponse.get('json').get('entity').get('recipientsResponse').get('test'), expectedControlUsers=mergeListresponse.get('json').get('entity').get('recipientsResponse').get('control'))
        Logger.log('GroupVersionId : {}, bucketId : {}'.format(groupVersionDetailResult, bucketId))
        addRecipientResponse = {'json':{'entity':mergeListresponse.get('json').get('entity').get('recipientsResponse')}}
        campaignList.assertAddRecipientDbCalls(addRecipientResponse, mergeListPayload.get('recipients'), mergeListresponse, campaignId, bucketId, {'TEST':groupVersionDetailResult.get('TEST'), 'CONTROL':groupVersionDetailResult.get('CONTROL')}, userType)

    @pytest.mark.parametrize('campaignAndListType,userType,numberOfUsers,customTagCount', [
        (['LAPSED', 'ORG', 'List', 'TAGS', 1], 'mobile', 1, 1),
        (['LAPSED', 'ORG', 'List', 'TAGS', 2], 'mobile', 2, 2),
        (['LAPSED', 'ORG', 'List', 'TAGS', 3], 'mobile', 3, 3),
        (['LAPSED', 'ORG', 'List', 'TAGS', 4], 'mobile', 4, 4),
        (['LAPSED', 'ORG', 'List', 'TAGS', 5], 'mobile', 5, 5),
        (['LAPSED', 'CUSTOM', 'List', 'TAGS', 0], 'mobile', 1, 0),
        (['LAPSED', 'CUSTOM', 'List', 'TAGS', 1], 'mobile', 1, 1),
        (['LAPSED', 'CUSTOM', 'List', 'TAGS', 2], 'mobile', 2, 2),
        (['LAPSED', 'CUSTOM', 'List', 'TAGS', 3], 'mobile', 3, 3),
        (['LAPSED', 'CUSTOM', 'List', 'TAGS', 4], 'mobile', 4, 4),
        (['LAPSED', 'CUSTOM', 'List', 'TAGS', 5], 'mobile', 5, 5),
        (['LAPSED', 'SKIP', 'List', 'TAGS', 0], 'mobile', 1, 0),
        (['LAPSED', 'SKIP', 'List', 'TAGS', 1], 'mobile', 1, 1),
        (['LAPSED', 'SKIP', 'List', 'TAGS', 2], 'mobile', 2, 2),
        (['LAPSED', 'SKIP', 'List', 'TAGS', 3], 'mobile', 3, 3),
        (['LAPSED', 'SKIP', 'List', 'TAGS', 4], 'mobile', 4, 4),
        (['LAPSED', 'SKIP', 'List', 'TAGS', 5], 'mobile', 5, 5),
        ])    
    def test_mergeList_LapsedCampaign_mobile(self, campaignAndListType, userType, numberOfUsers, customTagCount):
        mergeListresponse, mergeListPayload, campaignId = campaignList.mergeList({}, campaignType=campaignAndListType, userType=userType, numberOfUsers=numberOfUsers, numberOfCustomTags=customTagCount)
        campaignList.assertMergeList(mergeListresponse, 200)
        groupVersionDetailResult, bucketId = campaignList.assertCreateListDbCalls(mergeListresponse.get('json').get('entity').get('listId'), mergeListPayload, campaignAndListType[1], expectedTestUsers=mergeListresponse.get('json').get('entity').get('recipientsResponse').get('test'), expectedControlUsers=mergeListresponse.get('json').get('entity').get('recipientsResponse').get('control'))
        Logger.log('GroupVersionId : {}, bucketId : {}'.format(groupVersionDetailResult, bucketId))
        addRecipientResponse = {'json':{'entity':mergeListresponse.get('json').get('entity').get('recipientsResponse')}}
        campaignList.assertAddRecipientDbCalls(addRecipientResponse, mergeListPayload.get('recipients'), mergeListresponse, campaignId, bucketId, {'TEST':groupVersionDetailResult.get('TEST'), 'CONTROL':groupVersionDetailResult.get('CONTROL')}, userType)

    @pytest.mark.parametrize('campaignAndListType,userType,numberOfUsers,customTagCount', [
        (['LAPSED', 'ORG', 'List', 'TAGS', 1], 'email', 1, 1),
        (['LAPSED', 'ORG', 'List', 'TAGS', 2], 'email', 2, 2),
        (['LAPSED', 'ORG', 'List', 'TAGS', 3], 'email', 3, 3),
        (['LAPSED', 'ORG', 'List', 'TAGS', 4], 'email', 4, 4),
        (['LAPSED', 'ORG', 'List', 'TAGS', 5], 'email', 5, 5),
        (['LAPSED', 'CUSTOM', 'List', 'TAGS', 0], 'email', 1, 0),
        (['LAPSED', 'CUSTOM', 'List', 'TAGS', 1], 'email', 1, 1),
        (['LAPSED', 'CUSTOM', 'List', 'TAGS', 2], 'email', 2, 2),
        (['LAPSED', 'CUSTOM', 'List', 'TAGS', 3], 'email', 3, 3),
        (['LAPSED', 'CUSTOM', 'List', 'TAGS', 4], 'email', 4, 4),
        (['LAPSED', 'CUSTOM', 'List', 'TAGS', 5], 'email', 5, 5),
        (['LAPSED', 'SKIP', 'List', 'TAGS', 0], 'email', 1, 0),
        (['LAPSED', 'SKIP', 'List', 'TAGS', 1], 'email', 1, 1),
        (['LAPSED', 'SKIP', 'List', 'TAGS', 2], 'email', 2, 2),
        (['LAPSED', 'SKIP', 'List', 'TAGS', 3], 'email', 3, 3),
        (['LAPSED', 'SKIP', 'List', 'TAGS', 4], 'email', 4, 4),
        (['LAPSED', 'SKIP', 'List', 'TAGS', 5], 'email', 5, 5),
        ])    
    def test_mergeList_LapsedCampaign_email(self, campaignAndListType, userType, numberOfUsers, customTagCount):
        mergeListresponse, mergeListPayload, campaignId = campaignList.mergeList({}, campaignType=campaignAndListType, userType=userType, numberOfUsers=numberOfUsers, numberOfCustomTags=customTagCount)
        campaignList.assertMergeList(mergeListresponse, 200)
        groupVersionDetailResult, bucketId = campaignList.assertCreateListDbCalls(mergeListresponse.get('json').get('entity').get('listId'), mergeListPayload, campaignAndListType[1], expectedTestUsers=mergeListresponse.get('json').get('entity').get('recipientsResponse').get('test'), expectedControlUsers=mergeListresponse.get('json').get('entity').get('recipientsResponse').get('control'))
        Logger.log('GroupVersionId : {}, bucketId : {}'.format(groupVersionDetailResult, bucketId))
        addRecipientResponse = {'json':{'entity':mergeListresponse.get('json').get('entity').get('recipientsResponse')}}
        campaignList.assertAddRecipientDbCalls(addRecipientResponse, mergeListPayload.get('recipients'), mergeListresponse, campaignId, bucketId, {'TEST':groupVersionDetailResult.get('TEST'), 'CONTROL':groupVersionDetailResult.get('CONTROL')}, userType)

    @pytest.mark.parametrize('campaignAndListType,userType,numberOfUsers,customTagCount,statusCode,errorCode,errorMessage', [
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'mobile', 50, 0, 200, 000, ''),
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'mobile', 51, 0, 400, 2007, 'List Size Exception : Recipients list size should not exceed 50'),  # bug getting 404
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'mobile', 0, 0, 400, 2010, "User identifier not present"),
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'email', 50, 0, 200, 000, ''),
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'email', 51, 0, 400, 2007, 'List Size Exception : Recipients list size should not exceed 50'),  # bug getting 404
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'email', 0, 0, 400, 2010, "User identifier not present")
        ])
    def test_mergeList_BoundaryValue_NumberOfUsers(self, campaignAndListType, userType, numberOfUsers, customTagCount, statusCode, errorCode, errorMessage):
        mergeListresponse, mergeListPayload, campaignId = campaignList.mergeList({}, campaignType=campaignAndListType, userType=userType, numberOfUsers=numberOfUsers, numberOfCustomTags=customTagCount)
        campaignList.assertMergeList(mergeListresponse, statusCode, errorCode, errorMessage)

    @pytest.mark.parametrize('campaignAndListType,userType,numberOfUsers,customTagCount', [
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'mobile', 5, 0),
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'email', 5, 0),
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'mobile', 5, 5),
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'email', 5, 5),
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'email', 26, 0) 
        ])
    def test_mergeList_AppendingInSameList(self, campaignAndListType, userType, numberOfUsers, customTagCount):
        mergeListresponse, mergeListPayload, campaignId = campaignList.mergeList({}, campaignType=campaignAndListType, userType=userType, numberOfUsers=numberOfUsers, numberOfCustomTags=customTagCount)
        campaignList.assertMergeList(mergeListresponse, 200)
        addRecipientResponse, addRecipientPayload = campaignList.addRecipient({}, campaignId, mergeListresponse.get('json').get('entity').get('listId'), str(userType), int(numberOfUsers), int(customTagCount))
        campaignList.assertAddRecipient(addRecipientResponse, 200)
        Assertion.constructAssertion(addRecipientResponse.get('json').get('entity').get('test') + addRecipientResponse.get('json').get('entity').get('control') == numberOfUsers * 2, 'Matching Data has got Appended')
        
    @pytest.mark.parametrize('campaignAndListType,schema,data,reasonResponse', [
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'firstName,lastName,mobile', ['Test1,Automation1,xyz@gmail.com'], ['Invalid mobile number']),
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'firstName,lastName,email', ['Test1,Automation1,8497846843'], ['Invalid Email Id'])
        ])
    def test_mergeList_WrongSchemaAndData(self, campaignAndListType, schema, data, reasonResponse):
        mergeListresponse, mergeListPayload, campaignId = campaignList.mergeList({'recipients':{'schema':schema, 'data':data}, 'name':'IRIS_MERGE_LIST_' + str(int(time.time()))}, campaignType=campaignAndListType)
        campaignList.assertMergeList(mergeListresponse, 200)
        addRecipientResponse = addRecipientResponse = {'json':{'entity':mergeListresponse.get('json').get('entity').get('recipientsResponse')}}
        campaignList.assertInvalidDataInListResponse(addRecipientResponse, data, reasonResponse)
        
    @pytest.mark.parametrize('payloadToUpdate,statusCode,errorCode,errorMessage', [
        ({'name':'IRIS_NEGATIVECASE_A_LIST_' + str(int(time.time())), 'customTagCount':0, 'recipients':{'dataSource':'CSV', 'schema':'firstName,lastName,mobile', 'data' : ['Test1,Automation1,8497846843,tag1,tag2,tag3,tag4,tag5']}}, 200, 000, ''),
        ({'name':'IRIS_NEGATIVECASE_B_LIST_' + str(int(time.time())), 'customTagCount':5, 'recipients':{'dataSource':'CSV', 'schema':'firstName,lastName,mobile,customTag1,customTag2,customTag3,customTag4,customTag5', 'data' : ['Test1,Automation1,8497846843']}}, 200, 000, ''),
        ({'name':'IRIS_NEGATIVECASE__C_LIST_' + str(int(time.time())), 'customTagCount':1, 'recipients':{'dataSource':'CSV', 'schema':'firstName,lastName,mobile,customTag1', 'data' : ['Test1,Automation1,8497846843,tag1,tag2']}}, 200, 000, ''),
        ({'name':'IRIS_NEGATIVECASE_D_LIST_' + str(int(time.time())), 'customTagCount':0, 'recipients':{'dataSource':'CSV', 'schema':'firstName,lastName,email', 'data' : ['Test1,Automation1,xyz@gmail.com,tag1,tag2,tag3,tag4,tag5']}}, 200, 000, ''),
        ({'name':'IRIS_NEGATIVECASE_E_LIST_' + str(int(time.time())), 'customTagCount':5, 'recipients':{'dataSource':'CSV', 'schema':'firstName,lastName,email,customTag1,customTag2,customTag3,customTag4,customTag5', 'data' : ['Test1,Automation1,xyz@gmail.com']}}, 200, 000, ''),
        ({'name':'IRIS_NEGATIVECASE__F_LIST_' + str(int(time.time())), 'customTagCount':1, 'recipients':{'dataSource':'CSV', 'schema':'firstName,lastName,email,customTag1', 'data' : ['Test1,Automation1,xyz@gmail.com,tag1,tag2']}}, 200, 000, '') 
        ])
    def test_mergeList_WrongValuesInCustomTagAndDataPassed(self, payloadToUpdate, statusCode, errorCode, errorMessage):
        mergeListresponse, mergeListPayload, campaignId = campaignList.mergeList(payloadData=payloadToUpdate)
        campaignList.assertMergeList(mergeListresponse, statusCode, errorCode, errorMessage)
        campaignList.assertInvalidDataInListResponse(mergeListresponse, payloadToUpdate['recipients']['data'], ['Data does not match with schema'])
        
    @pytest.mark.parametrize('campaignAndListType', [
        (['LIVE', 'ORG', 'List', 'TAGS', 0]) 
        ])
    def test_mergeList_WrongDataSourceInSchema(self, campaignAndListType):
        mergeListresponse, mergeListPayload, campaignId = campaignList.mergeList({'recipients':{'dataSource':'wrong', 'schema':'firstName,lastName,mobile', 'data' : ['Test1,Automation1,8497846843']}}, campaignType=campaignAndListType)
        campaignList.assertMergeList(mergeListresponse, 400, 100, '')
        
    @pytest.mark.parametrize('campaignAndListType,keyToPop,statusCode,errorCode,errorMessage', [
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'name', 400, 100, 'Invalid request : List name is required. '),
        ])   
    def test_mergeList_popKeysFromAddRecipientPayload(self, campaignAndListType, keyToPop, statusCode, errorCode, errorMessage):
        mergeListresponse, mergeListPayload, campaignId = campaignList.mergeList(keyToPop, campaignType=campaignAndListType, process='pop')
        campaignList.assertMergeList(mergeListresponse, statusCode, errorCode, errorMessage)
    
    @pytest.mark.parametrize('campaignAndListType,schema,data', [
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'firstName,lastName,mobile', ['Test1,Automation1,8497846843', 'Test1,Automation1,8497846843']),
        (['LIVE', 'ORG', 'List', 'TAGS', 0], 'firstName,lastName,email', ['Test1,Automation1,xyz@gmail.com', 'Test1,Automation1,xyz@gmail.com'])  
        ])   
    def test_mergeList_DuplicateData(self, campaignAndListType, schema, data): 
        mergeListresponse, mergeListPayload, campaignId = campaignList.mergeList({'recipients':{
                        'dataSource' : 'CSV',
                        'schema' : schema,
                        'data' : data
                    }, 'name':'IRIS_MERGE_DUPLICATE_' + str(int(time.time()))}, campaignType=campaignAndListType)
        campaignList.assertMergeList(mergeListresponse, 200)
        Assertion.constructAssertion(mergeListresponse.get('json').get('entity').get('recipientsResponse').get('test') == 1, 'Matching test count to be 1 as 2 data were passed of same details')
       
    def test_mergeList_WrongCampaignId(self):
        mergeListresponse, mergeListPayload, campaignId = campaignList.mergeList({'name':'IRIS_WRONG_CAMPAIGNID_' + str(int(time.time()))}, campaignId=-1)
        campaignList.assertMergeList(mergeListresponse, 400, 100, 'Invalid request : must be greater than or equal to 1')
        
