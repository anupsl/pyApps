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

@pytest.mark.run(order=3)
class Test_CreateList():
    
    def setup_method(self, method):
        Logger.logMethodName(str(method.__name__))
        constant.config['validataionMessage'] = []
    
    def test_pasteList_Sanity(self):
        response, payload, campaignId = campaignList.createList()
        campaignList.assertCreateList(response, 200)
        groupVersionDetailResult, bucketId = campaignList.assertCreateListDbCalls(response.get('json').get('entity').get('listId'), payload, 'ORG')
        Logger.log('GroupVersionId : {}, bucketId : {}'.format(groupVersionDetailResult, bucketId))
        
    @pytest.mark.parametrize('testControlType,customTagCount', [
        ('ORG', 0),
        ('ORG', 1),
        ('ORG', 2),
        ('ORG', 3),
        ('ORG', 4),
        ('ORG', 5),
        ('CUSTOM', 0),
        ('CUSTOM', 1),
        ('CUSTOM', 2),
        ('CUSTOM', 3),
        ('CUSTOM', 4),
        ('CUSTOM', 5),
        ('SKIP', 0),
        ('SKIP', 1),
        ('SKIP', 2),
        ('SKIP', 3),
        ('SKIP', 4),
        ('SKIP', 5)
        ])
    def test_pasteList_liveOutbondCampaign(self, testControlType, customTagCount):
        response, payload, campaignId = campaignList.createList({'customTagCount':int(customTagCount), 'name':'IRIS_LIST_' + str(int(time.time() * 100000))})
        campaignList.assertCreateList(response, 200)
        groupVersionDetailResult, bucketId = campaignList.assertCreateListDbCalls(response.get('json').get('entity').get('listId'), payload, testControlType)
        Logger.log('GroupVersionId : {}, bucketId : {}'.format(groupVersionDetailResult, bucketId))
    
    @pytest.mark.parametrize('testControltype,customTagCount', [
        ('ORG', 0),
        ('ORG', 1),
        ('ORG', 2),
        ('ORG', 3),
        ('ORG', 4),
        ('ORG', 5),
        ('CUSTOM', 0),
        ('CUSTOM', 1),
        ('CUSTOM', 2),
        ('CUSTOM', 3),
        ('CUSTOM', 4),
        ('CUSTOM', 5),
        ('SKIP', 0),
        ('SKIP', 1),
        ('SKIP', 2),
        ('SKIP', 3),
        ('SKIP', 4),
        ('SKIP', 5)
        ])   
    def test_pasteList_upcomingOutboundCampaign(self, testControltype, customTagCount):
        response, payload, campaignId = campaignList.createList({'customTagCount':int(customTagCount), 'name':'IRIS_LIST_' + str(int(time.time() * 100000))}, campaignType=['UPCOMING', testControltype, 'List', 'TAGS', customTagCount])
        campaignList.assertCreateList(response, 200)
        groupVersionDetailResult, bucketId = campaignList.assertCreateListDbCalls(response.get('json').get('entity').get('listId'), payload, testControlType=testControltype)
        Logger.log('GroupVersionId : {}, bucketId : {}'.format(groupVersionDetailResult, bucketId))
    
    @pytest.mark.parametrize('testControltype,customTagCount', [
        ('ORG', 0),
        ('ORG', 1),
        ('ORG', 2),
        ('ORG', 3),
        ('ORG', 4),
        ('ORG', 5),
        ('CUSTOM', 0),
        ('CUSTOM', 1),
        ('CUSTOM', 2),
        ('CUSTOM', 3),
        ('CUSTOM', 4),
        ('CUSTOM', 5),
        ('SKIP', 0),
        ('SKIP', 1),
        ('SKIP', 2),
        ('SKIP', 3),
        ('SKIP', 4),
        ('SKIP', 5)
        ])   
    def test_pasteList_lapsedOutboundCampaign(self, testControltype, customTagCount):
        response, payload, campaignId = campaignList.createList({'customTagCount':int(customTagCount), 'name':'IRIS_LIST_' + str(int(time.time() * 100000))}, campaignType=['LAPSED', testControltype, 'List', 'TAGS', customTagCount])
        campaignList.assertCreateList(response, 200)
        groupVersionDetailResult, bucketId = campaignList.assertCreateListDbCalls(response.get('json').get('entity').get('listId'), payload, testControlType=testControltype)
        Logger.log('GroupVersionId : {}, bucketId : {}'.format(groupVersionDetailResult, bucketId))
     
    @pytest.mark.parametrize('testControltype,customTagCount', [
        ('ORG', 6),
        ('CUSTOM', 6),
        ('SKIP', 6)
        ])    
    def test_pasteList_OutboundCampaign_MoreCustomTagCount(self, testControltype, customTagCount):
        response, payload, campaignId = campaignList.createList({'customTagCount':int(customTagCount), 'name':'IRIS_LIST_' + str(int(time.time() * 100000))}, campaignType=['LAPSED', testControltype, 'List', 'TAGS', customTagCount])
        campaignList.assertCreateList(response, 400, 100, 'Invalid request : Maximum 5 Custom Tags can be given')
        
    @pytest.mark.parametrize('description,campaignId,errorCode,errorMessage', [
        ('createPasteListWithInvalidCampaignId', 0, 100, 'Invalid request : must be greater than or equal to 1'),
        ('createPasteListWithNegativeCampaignId', -1, 100, 'Invalid request : must be greater than or equal to 1')
        ])
    def test_pasteList_wrongCampaignId(self, description, campaignId, errorCode, errorMessage):
        response, payload, campaignId = campaignList.createList({}, campaignId=int(campaignId))
        campaignList.assertCreateList(response, 400, errorCode, errorMessage)
    
    @pytest.mark.parametrize('description,listName,errorCode,errorMessage', [
        ('AllSpecialCharacter', 'IR IS_~!@#$%^&*()_+|}{:"?><,./;\][=', 100, 'Invalid request : Invalid list name. Use only alphanumeric , underscore, space. '),
        ('MoreThan50Character', 'IRIS_ssssssssssssssssssssssssssssssssssss' + str(int(time.time() * 100000)), 100, 'Invalid request : Invalid list name. Name exceeds 50 characters. '),
        ('ListNameAsEmpty', '', 100, 'Invalid request : List Name cannot be empty ')
        ])
    def test_pasteList_wrongListNames(self, description, listName, errorCode, errorMessage):
        response, payload, campaignId = campaignList.createList({'name':listName})
        campaignList.assertCreateList(response, 400 , errorCode, errorMessage)
     
    def test_pasteList_wrongOrgId(self):
        response, payload = campaigns.createCampaign(campaignTypeParams=['LIVE', 'ORG'])
        campaigns.assertCreateCampaign(response, 200)
        campaignId = response.get('json').get('entity').get('campaignId')
        previousOrgId = construct.updateOrgId(0)
        try:
            responseCreateList, payload, campaignId = campaignList.createList({}, campaignId=campaignId)  
            campaignList.assertCreateList(responseCreateList, 400, 2003, 'Invalid campaign  id : ' + str(campaignId)[:3] + ',' + str(campaignId)[3:])
        except AssertionError, exp:
            Logger.log('Assertioin Failed as :', exp)
        finally:
            construct.updateOrgId(int(previousOrgId))

    def test_pasteList_sameName_SequentialRequest(self):
        response, payload, campaignId = campaignList.createList({'name':'IRIS_SEQUENTIAL_REQUEST' + str(int(time.time() * 100000))})
        campaignList.assertCreateList(response, 200)
        groupVersionDetailResult, bucketId = campaignList.assertCreateListDbCalls(response.get('json').get('entity').get('listId'), payload, 'ORG')
        Logger.log('First List Created with CampaignId : {} having GroupVersionId : {}, bucketId : {}'.format(campaignId, groupVersionDetailResult, bucketId))
        response, payload, campaignId = campaignList.createList({'name':payload.get('name')}, campaignId=campaignId)
        campaignList.assertCreateList(response, 400, 2006, 'List Name Exception : List Name already exists')
    
    
    # Will Do these cases with Benchmark pytest
    '''
    def test_pasteList_sameName_parellelRequest(self):
        que = Queue.Queue()
        threads_list = list()
        result = []
        
        goalId = str(dbCallsCampaign.getValidGoalId().get('id'))
        objectiveId = dbCallsCampaign.getValidObjectiveId()
        response, payload = campaigns.createCampaign({'name':'IRIS_' + str(int(time.time() * 100000)), 'goalId':goalId, 'objectiveId':objectiveId})
        campaigns.assertCreateCampaign(response, 200)
        campaigns.assertCreateCampaignDBCall(response.get('json').get('entity').get('campaignId'), payload)
        uploadPayloadWith = {'name':'IRIS_' + str(int(time.time() * 100000))}
        campaignId = response.get('json').get('entity').get('campaignId')
        
        uploadPayloadWith = {'name':'IRIS_' + str(int(time.time() * 100000))}
        
        for i in range(1, 4):
            threads_list.append(Thread(target=lambda q, arg1: q.put({'createList': campaignList.createList(arg1)}), args=(que, uploadPayloadWith)))
        [x.start() for x in threads_list]
        [x.join() for x in threads_list]
        
        while not que.empty():
            thread_result = que.get().get('createList')
            result.append((thread_result[0], thread_result[1]))
        
        Logger.log('CreateList Result for all threads', result)
        
        statusCodeList = [result[0][0].get('statusCode'), result[1][0].get('statusCode'), result[2][0].get('statusCode')]
        Logger.log('Status Code from all 3 requests', statusCodeList)
        
        Assertion.constructAssertion(statusCodeList.count(200) == 1 , 'Checking Count of Created List ,expectng : 1')
        Assertion.constructAssertion(statusCodeList.count(400) == 2 , 'Checking Count of List not created ,expectng : 2')
        
        for eachResult in result:
            if eachResult[0].get('statusCode') == 200:
                campaignList.assertCreateList(eachResult[0], 200)
                groupVersionDetailResult, bucketId = campaignList.assertCreateListDbCalls(eachResult[0].get('json').get('entity').get('listId'), eachResult[1], 'ORG')
                Logger.log('GroupVersionId : {}, bucketId : {}'.format(groupVersionDetailResult, bucketId))
            else:
                campaignList.assertCreateList(eachResult[0], 400, 2002, 'Duplicate list name')
        
    def test_pasteList_differentName_parellelRequest(self):
        que = Queue.Queue()
        threads_list = list()
        result = []
        
        goalId = str(dbCallsCampaign.getValidGoalId().get('id'))
        objectiveId = dbCallsCampaign.getValidObjectiveId()
        response, payload = campaigns.createCampaign({'name':'IRIS_' + str(int(time.time() * 100000)), 'goalId':goalId, 'objectiveId':objectiveId, })
        campaigns.assertCreateCampaign(response, 200)
        campaigns.assertCreateCampaignDBCall(response.get('json').get('entity').get('campaignId'), payload)
        uploadPayloadWith = {'name':'IRIS_' + str(int(time.time() * 100000))}
        campaignId = response.get('json').get('entity').get('campaignId')
        constant.campaignId.update({'ORG':campaignId})
        
        for i in range(1, 4):
            threads_list.append(Thread(target=lambda q, arg1: q.put({'createList': campaignList.createList(arg1)}), args=(que, {'name':str(i) + '_' + str(int(time.time() * 100000))})))
        [x.start() for x in threads_list]
        [x.join() for x in threads_list]
        
        while not que.empty():
            result = que.get().get('createList')
            Logger.log('Checking for Campaign Created:', result)
            campaignList.assertCreateList(result[0], 200)
            groupVersionDetailResult, bucketId = campaignList.assertCreateListDbCalls(result[0].get('json').get('entity').get('listId'), result[1], 'ORG')
            Logger.log('GroupVersionId : {}, bucketId : {}'.format(groupVersionDetailResult, bucketId))
    '''        
