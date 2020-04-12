#- * - coding: utf - 8 -*-
import copy
import time

import pytest

from src.Constant.constant import constant
from src.dbCalls.campaignShard import list_Calls
from src.dbCalls.messageInfo import message_calls
from src.modules.irisv2.campaigns.createCampaign import CreateCampaign
from src.modules.irisv2.helper.irisHelper import IrisHelper
from src.utilities.utils import Utils
from src.modules.irisv2.list.createAudience import CreateAudience
from src.modules.irisv2.message.createMessage import CreateMessage
from  src.utilities.assertion import Assertion
from src.utilities.logger import Logger
from datetime import datetime
from src.modules.irisv2.message.createMessageDbAssertion import CreateMessageDBAssertion
from src.modules.irisv2.message.authorizeMessage import AuthorizeMessage
from src.modules.irisv2.message.authorizeMessageDbAssertion import AuthorizeMessageDBAssertion

class Test_createMessage_Negative_ValildationMessage():
    def setup_method(self, method):
        Logger.logMethodName(method.__name__)

    def setup_class(self):
        Logger.logSuiteName(str(self).split('.')[-1])
        self.listInfo = CreateAudience.uploadList('LIVE', 'ORG')
        self.listInfoFilter = CreateAudience.FilterList('LIVE', 'ORG')
        self.messagePayload = constant.payload['createMessagev2']
        self.messagePayload.update({'deliverySetting':CreateMessage.constructDeliverySetting(['SMS','EMAIL'])})
        self.messageInfo = {'scheduleType': {'type': 'IMMEDIATE'},
                            'offerType': 'PLAIN',
                            'messageStrategy': {'type': 'DEFAULT'},
                            'channels': ['SMS', 'EMAIL'],
                            'useTinyUrl': False,
                            'encryptUrl': False,
                            'skipRateLimit': True
                            }
        self.list1= CreateAudience.uploadList('LIVE', 'ORG',updateNode=True,
                                              lockNode=True)
        self.list2 = CreateAudience.uploadList('LIVE', 'ORG',updateNode=True,
                                              lockNode=True)
        self.list3 = CreateAudience.uploadList('LIVE', 'ORG',updateNode=True,
                                              lockNode=True)
        self.list4 = CreateAudience.uploadList('LIVE', 'ORG',updateNode=True,
                                              lockNode=True)
        self.list5 = CreateAudience.uploadList('LIVE', 'ORG',updateNode=True,
                                              lockNode=True)
        self.list6 = CreateAudience.uploadList('LIVE', 'ORG',updateNode=True,
                                              lockNode=True)

    def test_createMessage_negative_validationMessage_targetAudience_emptyJson(self):
        payload = copy.deepcopy(self.messagePayload)
        payload.update({'targetAudience': {}})
        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE', messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[102],
                                     expectedErrorMessage=['Invalid request : Target audience is required.'])

    def test_createMessage_negative_validationMessage_targetAudience_emptyIncludeAndExclude(self):
        payload = copy.deepcopy(self.messagePayload)
        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE', messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[102],
                                     expectedErrorMessage=['Invalid request : Include audience cannot be empty','Invalid request : Target audience is required.'])

    @pytest.mark.parametrize('listId,errorCode,errorMessage',[
        (99999999,[3045],'Audience exception: group not found'),
        (0, [3045], 'Audience exception: group not found'),
        (-9999999,[3045],'Audience exception: group not found'),
        (None,[3007],['Invalid request : Include audience cannot be empty','Audience group id does not exists : null']),
        ('99999',[3045],'Audience exception: group not found'),
        ('listId',[3007],'Audience group id does not exists : listId'),
        ('list$$$',[3007],'Audience group id does not exists : list$$$')
    ])
    def test_createMessage_negative_validationMessage_targetAudience_WrongListId(self,listId,errorCode,errorMessage):
        payload = copy.deepcopy(self.messagePayload)
        payload['targetAudience'].update({'include': [listId]})
        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE', messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        if listId is None: listId = 'null'
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=errorCode,
                                     expectedErrorMessage=errorMessage)

    def test_createMessage_negative_validationMessage_targetAudience_withoutTargetAudience(self):
        payload = copy.deepcopy(self.messagePayload)
        payload.pop('targetAudience')
        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE', messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[102],
                             expectedErrorMessage=['Invalid request : Audience group rule is required. ','Invalid request : Audience group rule is required.'])

    def test_createMessage_negative_validationMessage_targetAudience_WrongKeyNameOfTargetAudience(self):
        payload = copy.deepcopy(self.messagePayload)
        payload.pop('targetAudience')
        payload.update({'targetAudienceV2': {
            'include': [67538],
            'exclude': []
        }})
        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE', messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[107],
                                     expectedErrorMessage=['Unrecognized field : targetAudienceV2'])

    def test_createMessage_negative_validationMessage_targetAudience_IncludeValueAsString_NotArray(self):
        payload = copy.deepcopy(self.messagePayload)
        payload['targetAudience'].update({'include': self.listInfo['ID']})
        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE', messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[104],
                                     expectedErrorMessage=['Invalid request : invalid data type of field include'])


    def test_createMessage_negative_validationMessage_targetAudience_ExcludeValueAsString_NotArray(self):
        payload = copy.deepcopy(self.messagePayload)
        payload['targetAudience'].update({'exclude': self.listInfo['ID'], 'include': [self.listInfo['ID']]})
        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE', messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[104],
                                     expectedErrorMessage=['Invalid request : invalid data type of field exclude'])

    def test_createMessage_negative_validationMessage_targetAudience_SameListUsedMultipleTimes(self):
        payload = copy.deepcopy(self.messagePayload)
        payload['targetAudience'].update({
            'include': [self.listInfo['ID']] * 2
        })
        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE', messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[102],
                                     expectedErrorMessage=['Invalid request : Duplicate audience included'])

    def test_createMessage_negative_validationMessage_targetAudience_BoundaryValueOfList_Max_Include(self):
        payload = copy.deepcopy(self.messagePayload)
        payload['targetAudience'].update({
            'include': [ self.listInfo['ID'],self.list1['ID'],
            self.list2['ID'], self.list3['ID'],self.list4['ID'],self.list5['ID']]

        })
        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE', messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[102],
                                     expectedErrorMessage=['Invalid request : Max five audience allowed to include.'])

    def test_createMessage_negative_validationMessage_targetAudience_duplicateList(self):
        payload = copy.deepcopy(self.messagePayload)
        payload['targetAudience'].update({
            'include': [self.listInfo['ID']] * 2
        })
        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE', messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[102],
                                     expectedErrorMessage=['Invalid request : Duplicate audience included'])

    def test_createMessage_negative_validationMessage_targetAudience_BoundaryValueOfList_Max_Exclude(self):
        payload = copy.deepcopy(self.messagePayload)
        payload['targetAudience'].update({
            'exclude': [self.list6['ID'],self.list1['ID'],
            self.list2['ID'], self.list3['ID'],self.list4['ID'],self.list5['ID']],

            'include': [self.listInfo['ID']]
        })
        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE', messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[102],
                                     expectedErrorMessage=['Invalid request : Max five audience allowed to exclude.'])

    def test_createMessage_negative_validationMessage_targetAudience_WrongKeyName_InTargetAudienceJson(self):
        payload = copy.deepcopy(self.messagePayload)
        payload['targetAudience'].pop('include')
        payload['targetAudience'].update({
            'includev2': [self.listInfo['ID']]
        })

        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE', messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[107],
                                     expectedErrorMessage=['Unrecognized field : includev2'])

    def test_createMessage_negative_validationMessage_targetAudience_WrongKeyName_InTargetAudienceJson_multipleFields(
            self):
        payload = copy.deepcopy(self.messagePayload)
        payload['targetAudience'].pop('include')
        payload['targetAudience'].update({
            'includev2': [self.listInfo['ID']],
            'includev3': [self.listInfo['ID']]
        })

        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE', messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[107],
                                     expectedErrorMessage=['Unrecognized field : includev2',
                                                           'Unrecognized field : includev3'])

    def test_createMessage_negative_validationMessage_targetAudience_caseSensitive_Key_TargetAudience(self):
        payload = copy.deepcopy(self.messagePayload)
        payload.pop('targetAudience')
        payload.update({
            'targetaudience': {
                'include': [self.listInfo['ID']],
                'exclude': []
            }
        })

        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE', messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[107],
                                     expectedErrorMessage=['Unrecognized field : targetaudience'])

    def test_createMessage_negative_validationMessage_targetAudience_Stringify_listId(self):
        payload = copy.deepcopy(self.messagePayload)
        payload.pop('targetAudience')
        payload.update({
            'targetAudience': {
                'include': [str(self.listInfo['ID'])],
                'exclude': []
            }
        })

        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE', messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)

    def test_createMessage_negative_validationMessage_targetAudience_caseSensitive_Key_include_exclude_InsideTargetAudience(
            self):
        payload = copy.deepcopy(self.messagePayload)
        payload.pop('targetAudience')
        payload.update({
            'targetAudience': {
                'INCLUDE': [str(self.listInfo['ID'])],
                'EXCLUDE': []
            }
        })

        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE', messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[107],
                                     expectedErrorMessage=['Unrecognized field : INCLUDE',
                                                           'Unrecognized field : EXCLUDE'])

    def test_createMessage_negative_validationMessage_targetAudience_targetAudienceValueAs_DifferentDataType_insteadOfJson(
            self):
        payload = copy.deepcopy(self.messagePayload)
        payload.update({
            'targetAudience': self.listInfo['ID']
        })

        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE', messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[104],
                                     expectedErrorMessage=['Invalid request : invalid data type of field targetAudience'])

    def test_createMessage_negative_validationMessage_targetAudience_sameListIdInIncludeAndExclude(self):
        payload = copy.deepcopy(self.messagePayload)
        payload['targetAudience'].update({
            'include': [self.listInfo['ID']],
            'exclude': [self.listInfo['ID']]
        })

        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE', messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[102],
                                     expectedErrorMessage=['Invalid request : Same audience not allowed to include and exclude'])

    def test_createMessage_negative_validationMessage_targetAudience_setOfSameListIdInIncludeAndExclude(self):
        setOfListIds = list_Calls().getAllGroupIds(5, 0, 'created_date', None)
        payload = copy.deepcopy(self.messagePayload)
        payload['targetAudience'].update({
            'include': list(setOfListIds),
            'exclude': list(setOfListIds)
        })

        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE', messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[102],
                                     expectedErrorMessage=['Invalid request : Same audience not allowed to include and exclude'])

    def test_createMessage_negative_validationMessage_targetAudience_Include_Exclude_FieldAsNull(self):
        payload = copy.deepcopy(self.messagePayload)
        payload['targetAudience'].update({
            'include': None,
            'exclude': None
        })

        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE', messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[102],
                                     expectedErrorMessage=['Invalid request : Target audience is required.'])

    def test_createMessage_negative_validationMessage_targetAudience_TargetAudience_ValueAsNull(self):
        payload = copy.deepcopy(self.messagePayload)
        payload.update({'targetAudience': None})

        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE', messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[102],
                                     expectedErrorMessage=['Invalid request : Audience group rule is required. ','Invalid request : Audience group rule is required.'])

    def test_createMessage_negative_validationMessage_targetAudience_listWithNoUsers(self):
        listId = list_Calls().getListWithNoUsers()
        payload = copy.deepcopy(self.messagePayload)
        payload['name'] = 'listWithNoUser_{}'.format(int(time.time() * 1000))
        payload['targetAudience'].update({'include': [listId]})
        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE', messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)

    def test_createMessage_negative_validationMessage_targetAudience_WithOnlyExcludeList(self):
        payload = copy.deepcopy(self.messagePayload)
        payload['name'] = 'WithONlyExcludeList_{}'.format(int(time.time() * 1000))
        payload['targetAudience'].pop('include')
        payload['targetAudience']['exclude'] = [self.listInfo['ID']]
        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE', messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[3037,102],
                                     expectedErrorMessage=['Invalid request : Target audience is required.'])

    def test_createMessage_negative_validationMessage_type_caseSensitive_Value(self):
        payload = copy.deepcopy(self.messagePayload)
        payload['type'] = 'outbound'
        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE', messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[104],
                                     expectedErrorMessage=['Invalid request : type , Unknown value outbound, allowed values are [OUTBOUND]'])

    def test_createMessage_negative_validationMessage_type_ValueAsNull(self):
        payload = copy.deepcopy(self.messagePayload)
        payload['type'] = None
        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE', messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[104],
                                     expectedErrorMessage=['Invalid request : type , Unknown value null, allowed values are [OUTBOUND]'])

    @pytest.mark.parametrize('typeKey', [
        (''),
        ('WrongValue'),
        ('$$$$$')
    ])
    def test_createMessage_negative_validationMessage_type_WrongValue(self, typeKey):
        payload = copy.deepcopy(self.messagePayload)
        payload['type'] = typeKey
        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE', messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[104],
                                     expectedErrorMessage=[
                                         'Invalid request : type , Unknown value {}, allowed values are [OUTBOUND]'.format(typeKey)])

    def test_createMessage_negative_validationMessage_type_NoTypeKeyInBody(self):
        payload = copy.deepcopy(self.messagePayload)
        payload['targetAudience'].update({'include': [self.listInfo['ID']]})
        payload.pop('type')
        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE', messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[102],
                                     expectedErrorMessage=['Invalid request : Message type is required'])

    @pytest.mark.skipif(True,reason='not supported')
    @pytest.mark.parametrize('typeKey,errorCode', [

        ({'type': 'OUTBOUND'},104),
        (1221312,104)
    ])
    def test_createMessage_negative_validationMessage_type_ValueWithWrongDataType(self, typeKey,errorCode):
        payload = copy.deepcopy(self.messagePayload)
        payload['type'] = typeKey
        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE', messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[errorCode],
                                     expectedErrorMessage=[
                                         'Invalid request : type , Unknown value {}, allowed values are [OUTBOUND]'.format(typeKey)])

    @pytest.mark.skipif(True, reason='not supported')
    @pytest.mark.parametrize('typeKey,response,errorCode,errorMessage', [
        (['OUTBOUND'], 400, [104, 102], ['Invalid request : type , Unknown value {}, allowed values are [OUTBOUND]']),


    ])
    def test_createMessage_negative_validationMessage_type_ValueWithWrongDataType1(self, typeKey, response, errorCode,
                                                                                   errorMessage):
        payload = copy.deepcopy(self.messagePayload)
        payload['type'] = typeKey
        payload['targetAudience'].update({'include': [self.listInfo['ID']]})
        payload['name'] = 'MsgBodyUnsupportedTags_{}'.format(int(time.time() * 1000))
        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE', messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)

        Assertion.constructAssertion(messageDetails['RESPONSE']['statusCode'] == response,
                                     'Actual code :{} and Expected:{}'.format(messageDetails['RESPONSE']['statusCode'],
                                                                              response))

        for errors in messageDetails['RESPONSE']['json']['errors']:
            Assertion.constructAssertion(errors['code'] in errorCode,
                                         'Actual Error Code :{} and Expected :{}'.format(
                                             errors['code'], errorCode))

            Assertion.constructAssertion(errors['message'] in errorMessage,
                                         'Actual Error message :{} and Expected :{}'.format(
                                             errors['message'], errorMessage[0].format(typeKey[0])))


    def test_createMessage_negative_validationMessage_name_SameMessageName(self):
        messageName, campaignId = message_calls().getExistingMessageNameAndCampaignId()
        payload = copy.deepcopy(self.messagePayload)
        payload['targetAudience'].update({'include': [self.listInfo['ID']]})
        payload['name'] = messageName
        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE', campaignId=campaignId,
                                              messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[3033,3036],
                                     expectedErrorMessage=[
                                         'Message Name Exception : Message Name already exists',
                                         'Campaign expired',
                                         'Include audience cannot be empty',
                                     ])

    def test_createMessage_negative_validationMessage_name_BoundaryValueOfName(self):
        payload = copy.deepcopy(self.messagePayload)
        payload['targetAudience']['include'] = [self.listInfo['ID']]
        payload['name'] = 'A' * 161
        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
                                              messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[102],
                                     expectedErrorMessage=[
                                         'Invalid request : Invalid message name. Name exceeds 160 characters. '])

    def test_createMessage_negative_validationMessage_name_WithSpecialCharacter(self):
        payload = copy.deepcopy(self.messagePayload)
        payload['targetAudience']['include'] = [self.listInfo['ID']]
        payload['name'] = 'A$$$$'
        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
                                              messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200, expectedErrorCode=[104],
                                     expectedErrorMessage=[
                                         'name cant have special character'])

    @pytest.mark.parametrize('name', [
        (['AutomationName']),
        ({'name': 'AutomationName'})
    ])
    def test_createMessage_negative_validationMessage_name_WorngDataTypeOfName(self, name):
        payload = copy.deepcopy(self.messagePayload)
        payload['name'] = name
        payload['targetAudience']['include'] = [self.listInfo['ID']]
        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
                                              messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[104],
                                     expectedErrorMessage=[
                                         'Invalid request : invalid data type of field name'])

    def test_createMessage_negative_validationMessage_name_WorngDataTypeOfName(self):
        payload = copy.deepcopy(self.messagePayload)
        payload['name'] = 123133,
        payload['targetAudience']['include'] = [self.listInfo['ID']]
        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
                                              messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[104],
                                     expectedErrorMessage=[
                                         'Invalid request : invalid data type of field name'])

    def test_createMessage_negative_validationMessage_name_ValueAsNull(self):
        payload = copy.deepcopy(self.messagePayload)
        payload['targetAudience'].update({'include': [self.listInfo['ID']]})
        payload['name'] = None
        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
                                              messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[102],
                                     expectedErrorMessage=['Invalid request : Message name is required'])

    def test_createMessage_negative_validationMessage_name_WithoutKey(self):
        payload = copy.deepcopy(self.messagePayload)
        payload['targetAudience'].update({'include': [self.listInfo['ID']]})
        payload.pop('name')
        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
                                              messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[102],
                                     expectedErrorMessage=['Invalid request : Message name is required'])

    def test_createMessage_negative_validationMessage_messageStrategy_WrongValueOfType(self):
        payload = copy.deepcopy(self.messagePayload)
        payload['messageStrategy'].update({'type': 'WrongValue'})
        payload['targetAudience']['include'] = [self.listInfo['ID']]
        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
                                              messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[104],
                                     expectedErrorMessage=[
                                         'Invalid request : type , Unknown value {}, allowed values are [DEFAULT, PERSONALISATION, CHANNEL_PRIORITY]'.format('WrongValue')])

    def test_createMessage_negative_validationMessage_messageStrategy_caseSensitive_KeyType(self):
        payload = copy.deepcopy(self.messagePayload)
        payload['messageStrategy'].pop('type')
        payload['messageStrategy'].update({'TYPE': 'DEFAULT'})
        payload['targetAudience']['include'] = [self.listInfo['ID']]
        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
                                              messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[107],
                                     expectedErrorMessage=['Unrecognized field : TYPE'])

    def test_createMessage_negative_validationMessage_messageStrategy_wrongKeyPassed(self):
        payload = copy.deepcopy(self.messagePayload)
        payload['messageStrategy'].update({'XXX': 'DEFAULT'})
        payload['targetAudience']['include'] = [self.listInfo['ID']]
        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
                                              messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[107],
                                     expectedErrorMessage=['Unrecognized field : XXX'])

    def test_createMessage_negative_validationMessage_messageStrategy_typeAsNull(self):
        payload = copy.deepcopy(self.messagePayload)
        payload['messageStrategy'].update({'type': None})
        payload['targetAudience']['include'] = [self.listInfo['ID']]
        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
                                              messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[104],
                                     expectedErrorMessage=['Invalid request : type , Unknown value null, allowed values are [DEFAULT, PERSONALISATION, CHANNEL_PRIORITY]'])

    def test_createMessage_negative_validationMessage_messageStrategy_DifferentDataType_Type(self):
        payload = copy.deepcopy(self.messagePayload)
        payload['messageStrategy'].update({'type': ['DEFAULT']})
        payload['targetAudience']['include'] = [self.listInfo['ID']]
        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
                                              messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[104],
                                     expectedErrorMessage=['Invalid request : type , Unknown value [, allowed values are [DEFAULT, PERSONALISATION, CHANNEL_PRIORITY]'])

    def test_createMessage_negative_validationMessage_messageStrategy_DifferentDataType_messageStrategy(self):
        payload = copy.deepcopy(self.messagePayload)
        payload['messageStrategy'] = 'DEFAULT'
        payload['targetAudience']['include'] = [self.listInfo['ID']]
        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
                                              messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[104],
                                     expectedErrorMessage=['Invalid request : invalid data type of field messageStrategy'])

    def test_createMessage_negative_validationMessage_messageStrategy_AsNull(self):
        payload = copy.deepcopy(self.messagePayload)
        payload['messageStrategy'] = None
        payload['targetAudience']['include'] = [self.listInfo['ID']]
        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
                                              messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[102],
                                     expectedErrorMessage=[
                                         'Invalid request : Audience Group Split Strategy is required. '])

    def test_createMessage_negative_validationMessage_messageStrategy_WithoutStrategy(self):
        payload = copy.deepcopy(self.messagePayload)
        payload.pop('messageStrategy')
        payload['targetAudience']['include'] = [self.listInfo['ID']]
        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
                                              messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[102],
                                     expectedErrorMessage=[
                                         'Invalid request : Audience Group Split Strategy is required. '])

    def test_createMessage_negative_validationMessage_messageStrategy_extraKeysInStrategy(self):
        payload = copy.deepcopy(self.messagePayload)
        payload['targetAudience'].update({'include': [self.listInfo['ID']]})
        payload['messageStrategy'].update({'XXX': None})
        payload['targetAudience']['include'] = [self.listInfo['ID']]
        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
                                              messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[107],
                                     expectedErrorMessage=[
                                         'Unrecognized field : XXX'])

    def test_createMessage_negative_validationMessage_messageContent_multipleContent(self):

        payload = copy.deepcopy(self.messagePayload)
        payload['name'] = 'MaxNumber1OfContent_{}'.format(int(time.time() * 1000))
        payload['targetAudience'].update({'include': [self.listInfo['ID']]})
        payload['messageContent'].update({
            'message_content_id_2': {
                "channel": "SMS",
                "messageBody": "Hi {{first_name}} come and visit Shoppers Stop for attractive discounts {{optout}}"
            }, 'message_content_id_3': {
                "channel": "SMS",
                "messageBody": "Hi {{first_name}} come and visit Shoppers Stop for attractive discounts {{optout}}"
            }, 'message_content_id_4': {
                "channel": "SMS",
                "messageBody": "Hi {{first_name}} come and visit Shoppers Stop for attractive discounts {{optout}}"
            }, 'message_content_id_5': {
                "channel": "SMS",
                "messageBody": "Hi {{first_name}} come and visit Shoppers Stop for attractive discounts {{optout}}"
            }
        })
        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
                                              messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)

    def test_createMessage_negative_validationMessage_messageContent_multipleContent_maxNumberOfContent(self):
        payload = copy.deepcopy(self.messagePayload)
        payload['targetAudience'].update({'include': [self.listInfo['ID']]})
        payload['name'] = 'MaxNumberOfContent_{}'.format(int(time.time()*1000))
        payload['messageContent'].update({
            'message_content_id_2': {
                "channel": "SMS",
                "messageBody": "Hi {{first_name}} come and visit Shoppers Stop for attractive discounts {{optout}}"
            }, 'message_content_id_3': {
                "channel": "SMS",
                "messageBody": "Hi {{first_name}} come and visit Shoppers Stop for attractive discounts {{optout}}"
            }, 'message_content_id_4': {
                "channel": "SMS",
                "messageBody": "Hi {{first_name}} come and visit Shoppers Stop for attractive discounts {{optout}}"
            }, 'message_content_id_5': {
                "channel": "SMS",
                "messageBody": "Hi {{first_name}} come and visit Shoppers Stop for attractive discounts {{optout}}"
            }, 'message_content_id_6': {
                "channel": "SMS",
                "messageBody": "Hi {{first_name}} come and visit Shoppers Stop for attractive discounts {{optout}}"
            }
        })
        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
                                              messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)

    def test_createMessage_negative_validationMessage_messageContent_singleContent_ValueAsNull(self):
        payload = copy.deepcopy(self.messagePayload)
        payload['targetAudience'].update({'include': [self.listInfo['ID']]})
        payload['messageContent']['message_content_id_1'] = None
        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
                                              messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[102],
                                     expectedErrorMessage=['Invalid request : Message content is required','Invalid request : MessageContent cannot be empty.'])

    def test_createMessage_negative_validationMessage_messageContent_singleContent_ChannelUnknown(self):
        payload = copy.deepcopy(self.messagePayload)
        payload['targetAudience'].update({'include': [self.listInfo['ID']]})
        payload['messageContent']['message_content_id_1'] = None
        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
                                              messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[102],
                                     expectedErrorMessage=['Invalid request : Message content is required','Invalid request : MessageContent cannot be empty.'])

    def test_createMessage_negative_validationMessage_messageContent_singleContent_ChannelAsNull(self):
        payload = copy.deepcopy(self.messagePayload)
        payload['targetAudience'].update({'include': [self.listInfo['ID']]})
        payload['messageContent']['message_content_id_1']['channel'] = None
        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
                                              messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[104],
                                     expectedErrorMessage=['Invalid request : channel , Unknown value null, allowed values are [SMS, EMAIL, MOBILEPUSH, CALL_TASK, WECHAT, FACEBOOK]'])

    def test_createMessage_negative_validationMessage_messageContent_singleContent_ChannelWithDifferentDataType(self):
        payload = copy.deepcopy(self.messagePayload)
        payload['targetAudience'].update({'include': [self.listInfo['ID']]})
        payload['messageContent']['message_content_id_1']['channel'] = ['SMS', 'EMAIL']
        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
                                              messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[104],
                                     expectedErrorMessage=['Invalid request : channel , Unknown value [, allowed values are [SMS, EMAIL, MOBILEPUSH, CALL_TASK, WECHAT, FACEBOOK]'])

    def test_createMessage_negative_validationMessage_messageContent_singleContent_NoKeyAsChannel(self):
        payload = copy.deepcopy(self.messagePayload)
        payload['targetAudience'].update({'include': [self.listInfo['ID']]})
        payload['messageContent']['message_content_id_1'].pop('channel')
        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
                                              messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[102],
                                     expectedErrorMessage=['Invalid request : Channel in message content is required.'])



    def test_createMessage_negative_validationMessage_messageContent_singleContent_MessageBody_Null(self):
        payload = copy.deepcopy(self.messagePayload)
        payload['targetAudience'].update({'include': [self.listInfo['ID']]})
        payload['messageContent']['message_content_id_1'].update({'messageBody': None})
        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
                                              messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[102],
                                     expectedErrorMessage=[
                                         'Invalid request : Message body is required in message content.'])

    def test_createMessage_negative_validationMessage_messageContent_singleContent_MessageBody_UnknownTags(self):
        payload = copy.deepcopy(self.messagePayload)
        payload['targetAudience'].update({'include': [self.listInfo['ID']]})
        payload['name'] = 'MessageBodyUnknownTags_{}'.format(int(time.time() * 1000))
        payload['messageContent']['message_content_id_1'].update({'messageBody': "Hi {{Unknown Tag}} {{optout}}"})
        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
                                              messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[3067,102],
                                     expectedErrorMessage=[
                                         'Unsupported Tag {{Unknown Tag}}'])

    def test_createMessage_negative_validationMessage_messageContent_singleContent_MessageBody_OptoutTagNotPresent(
            self):
        payload = copy.deepcopy(self.messagePayload)
        payload['targetAudience'].update({'include': [self.listInfo['ID']]})
        payload['name'] = 'MsgBodyUnsupportedTags_{}'.format(int(time.time() * 1000))
        payload['messageContent']['message_content_id_1'].update({'messageBody': "Hi {{Unknown Tag}}"})
        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
                                              messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[3066],
                                     expectedErrorMessage=[
                                         'Invalid message content : Optout tag must be present in message.'])


    @pytest.mark.parametrize('tag,errorCode,errorMessage', [

        ('{{voucher}}',[3067],['Coupon offer should be attached to use voucher tag']),
        ('{{valid_days_from_create}}',[3067],['Voucher tag must be present in template if coupon validity tags are used']),
        ('{{valid_till_date.FORMAT_2}}',[3067],['Voucher tag must be present in template if coupon validity tags are used'])
    ])
    def test_createMessage_negative_validationMessage_messageContent_singleContent_MessageBody_IncentiveTags_coupon_WithoutOffer(
            self, tag,errorCode,errorMessage):
        payload = copy.deepcopy(self.messagePayload)
        payload['targetAudience'].update({'include': [self.listInfo['ID']]})
        payload['name'] = 'MsgBodyUnsupportedTags_{}'.format(int(time.time() * 1000))
        payload['messageContent']['message_content_id_1'].update({'messageBody': "Hi " + tag + " {{optout}}"})
        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
                                              messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=errorCode,
                                     expectedErrorMessage=errorMessage)

    @pytest.mark.parametrize('tag,response,errorCode,errorMessage', [
        ('{{promotion_points_expiring_on.FORMAT_1}}',400,[3067],['Promotion points tag must be present in template if points related tags are used']),
        ('{{promotion_points_floor}}',400,[3067],['Promotion points tag must be present in template if points related tags are used']),
        ('{{promotion_points}}',400,[3067],['Points offer should be attached to use points tags']),
        ('{{dynamic_expiry_date_after_1_days.FORMAT_2}}',200,[102],['Invalid request : Promotion points tag must be present in template if points related tags are used']),
        ('{{slab_name}}',200,[102],['Invalid request : Promotion points tag must be present in template if points related tags are used']),
        ('{{loyalty_points_value_floor}}',200,[102],['Invalid request : Promotion points tag must be present in template if points related tags are used']),
        ('{{loyalty_points_value}}',200,[102],['Invalid request : Promotion points tag must be present in template if points related tags are used']),
        ('{{loyalty_points_floor}}',200,[102],['Invalid request : Promotion points tag must be present in template if points related tags are used']),
        ('{{loyalty_points}}',200,[102],['Invalid request : Promotion points tag must be present in template if points related tags are used'])
    ])
    def test_createMessage_negative_validationMessage_messageContent_singleContent_MessageBody_IncentiveTags_point_WithoutOffer(
            self, tag,response,errorCode,errorMessage):
        payload = copy.deepcopy(self.messagePayload)
        payload['targetAudience'].update({'include': [self.listInfo['ID']]})
        payload['name'] = 'MessageBodyWithoutOffer_{}'.format(int(time.time() * 1000))
        payload['messageContent']['message_content_id_1'].update({'messageBody': "Hi " + tag + " {{optout}}"})
        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
                                              messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], response, expectedErrorCode=errorCode,
                                     expectedErrorMessage=errorMessage)

    @pytest.mark.skipif(True, reason='Size of the sms body is too big ')
    def test_createMessage_negative_validationMessage_messageContent_singleContent_MessageBody_MaxBodySize_SMS(self):
        maxNumberOfCharAllowed = 9999999
        payload = copy.deepcopy(self.messagePayload)
        payload['targetAudience'].update({'include': [self.listInfo['ID']]})
        payload['messageContent']['message_content_id_1'].update(
            {'messageBody': "Hi " * maxNumberOfCharAllowed + " {{optout}}"})
        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
                                              messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)

    @pytest.mark.skipif(True, reason='Size of the sms body is too big ')
    def test_createMessage_negative_validationMessage_messageContent_singleContent_MessageBody_MaxBodySize_EMAIL(self):
        messageBody = open(constant.csvFilePath + 'emailTemplate.html').read()
        payload = copy.deepcopy(self.messagePayload)
        payload['targetAudience'].update({'include': [self.listInfo['ID']]})
        payload['messageContent']['message_content_id_1'].pop('messageBody')
        payload['messageContent']['message_content_id_1'].update(
            {
                'emailSubject':'Auto Subject',
                'emailBody': messageBody,
                'channel':'EMAIL'
            })

        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'EMAIL',
                                              messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)

    @pytest.mark.parametrize('messageBody,errorCode,errorDesc', [
        (['Hi , Auto1', 'Hi Auto2'], [104], ['Invalid request : invalid data type of field messageBody']),
        ({'MESSAGEBODY': 'Hi Auto2'}, [104], ['Invalid request : invalid data type of field messageBody']),
        ('', [102], ['Invalid request : Message body is required in message content.']),
        (None, [102], ['Invalid request : Message body is required in message content.'])
    ])
    def test_createMessage_negative_validationMessage_messageContent_singleContent_MessageBody_DifferentDataTypes(self,
                                                                                                                  messageBody,
                                                                                                                  errorCode,
                                                                                                                  errorDesc):
        payload = copy.deepcopy(self.messagePayload)
        payload['targetAudience'].update({'include': [self.listInfo['ID']]})
        payload['messageContent']['message_content_id_1'].update({'messageBody': messageBody})
        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
                                              messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=errorCode,
                                     expectedErrorMessage=errorDesc)



    def test_createMessage_negative_validationMessage_messageContent_singleContent_MessageBody_KeyNotAvialable(self):
        payload = copy.deepcopy(self.messagePayload)
        payload['targetAudience'].update({'include': [self.listInfo['ID']]})
        payload['messageContent']['message_content_id_1'].pop('messageBody')
        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
                                              messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[102],
                                     expectedErrorMessage=[
                                         'Invalid request : Message body is required in message content.'])

    def test_createMessage_negative_validationMessage_messageContent_singleContent_MessageBody_SMS_WithoutOptout(self):
        payload = copy.deepcopy(self.messagePayload)
        payload['targetAudience'].update({'include': [self.listInfo['ID']]})
        payload['name'] = 'MsgBodyUnsupportedTags_{}'.format(int(time.time() * 1000))
        payload['messageContent']['message_content_id_1'].update({'messageBody': 'Auto Message without_opt tag'})
        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
                                              messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[3066],
                                     expectedErrorMessage=[
                                         'Invalid message content : Optout tag must be present in message.'])

    def test_createMessage_negative_validationMessage_messageContent_singleContent_MessageBody_EMAIL_WithoutUnsubscribe(
            self):
        payload = copy.deepcopy(self.messagePayload)

        payload['targetAudience'].update({'include': [self.listInfo['ID']]})
        payload['messageContent']['message_content_id_1'].pop('messageBody')
        payload['name'] = 'MsgBodyUnsupportedTags_{}'.format(int(time.time() * 1000))
        payload['messageContent']['message_content_id_1'].update(
            {
                'emailBody': 'Hi , Auto Email without Subscription Tag',
                'emailSubject': 'Auto Subject',
                'channel': 'EMAIL'
            })
        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'EMAIL',
                                              messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[3066],
                                     expectedErrorMessage=[
                                         'Invalid message content : Unsubscribe tag must be present in email.'])

    def test_createMessage_negative_validationMessage_messageContent_singleContent_MessageBody_EMAIL_WithoutSubject(
            self):
        payload = copy.deepcopy(self.messagePayload)
        payload['targetAudience'].update({'include': [self.listInfo['ID']]})
        payload['messageContent']['message_content_id_1'].pop('messageBody')
        payload['messageContent']['message_content_id_1'].update(
            {
                'emailBody': 'Hi , Auto Email with {{unsubscribe}} Tag',
                'channel': 'EMAIL'
            })
        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'EMAIL',
                                              messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[102],
                                     expectedErrorMessage=[
                                         'Invalid request : Email subject required in message content'])

    def test_createMessage_negative_validationMessage_messageContent_singleContent_MessageBody_EMAIL_WithoutBody(
            self):
        payload = copy.deepcopy(self.messagePayload)
        payload['targetAudience'].update({'include': [self.listInfo['ID']]})
        payload['messageContent']['message_content_id_1'].pop('messageBody')
        payload['messageContent']['message_content_id_1'].update(
            {
                'emailSubject': 'Auto Subject',
                'channel': 'EMAIL'
            })
        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'EMAIL',
                                              messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[102],
                                     expectedErrorMessage=[
                                         'Invalid request : Email body required in message content'])

    def test_createMessage_negative_validationMessage_messageContent_singleContent_MessageBody_EMAIL_WithExtraFieldMessageBody(
            self):
        payload = copy.deepcopy(self.messagePayload)
        payload['targetAudience'].update({'include': [self.listInfo['ID']]})
        payload['messageContent']['message_content_id_1'].update(
            {
                'emailSubject': 'Auto Subject',
                'channel': 'EMAIL'
            })
        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'EMAIL',
                                              messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[107],
                                     expectedErrorMessage=[
                                         'Unrecognized field : messageBody'])

    def test_createMessage_negative_validationMessage_messageContent_singleContent_MessageBody_UnsupportedTag(self):
        payload = copy.deepcopy(self.messagePayload)
        payload['targetAudience'].update({'include': [self.listInfo['ID']]})
        payload['name'] = 'MsgBodyUnsupportedTags_{}'.format(int(time.time() * 1000))
        payload['messageContent']['message_content_id_1'].update(
            {'messageBody': 'Hi Tag in wrong way {{first_name}} {{Unknown_Tag}} {{optout}}', 'channel': 'SMS'})
        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
                                              messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[3067],
                                     expectedErrorMessage=[
                                         'Unsupported Tag {{Unknown_Tag}}'])

    def test_createMessage_negative_validationMessage_messageContent_AsNull(self):
        payload = copy.deepcopy(self.messagePayload)
        payload['targetAudience'].update({'include': [self.listInfo['ID']]})
        payload['messageContent'] = None

        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
                                              messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 404, expectedErrorCode=[109],
                                     expectedErrorMessage=[
                                         'INVALID REQUEST PATH : HTTP 404 Not Found'])

    def test_createMessage_negative_validationMessage_messageContent_WithDifferentDataType(self):
        payload = copy.deepcopy(self.messagePayload)
        payload['targetAudience'].update({'include': [self.listInfo['ID']]})
        actualContent = payload['messageContent']
        payload['messageContent'] = [actualContent]

        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
                                              messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[104],
                                     expectedErrorMessage=[
                                         'Invalid request : invalid data type of field messageContent'])

    def test_createMessage_negative_validationMessage_messageContent_AsEmptyJson(self):
        payload = copy.deepcopy(self.messagePayload)
        payload['targetAudience'].update({'include': [self.listInfo['ID']]})
        payload['messageContent'] = {}

        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
                                              messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[102],
                                     expectedErrorMessage=['Invalid request : Message content is required','Invalid request : Atleast one Message content is required.'])

    def test_createMessage_negative_validationMessage_messageContent_WithAllFieldsAsEmpty(self):
        payload = copy.deepcopy(self.messagePayload)
        payload['targetAudience'].update({'include': [self.listInfo['ID']]})
        payload['messageContent']['message_content_id_1'].update({'channel': '', 'messageBody': ''})

        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
                                              messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[104],
                                     expectedErrorMessage =[
                                         "Invalid request : channel , Unknown value , allowed values are [SMS, EMAIL, MOBILEPUSH, CALL_TASK, WECHAT]"])

    def test_createMessage_negative_validationMessage_messageContent_WithChannelFieldsAsEmpty(self):
        payload = copy.deepcopy(self.messagePayload)
        payload['targetAudience'].update({'include': [self.listInfo['ID']]})
        payload['messageContent']['message_content_id_1'].update({'channel': '', 'messageBody': 'Hi {{optout}}'})

        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
                                              messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[104],
                                     expectedErrorMessage=[
                                         'Invalid request : channel , Unknown value , allowed values are [SMS, EMAIL, MOBILEPUSH, CALL_TASK, WECHAT, FACEBOOK]'])

    def test_createMessage_negative_validationMessage_schedule_ScheduleType_WithUnknownValue(self):
        payload = copy.deepcopy(self.messagePayload)
        payload['targetAudience'].update({'include': [self.listInfo['ID']]})
        payload['schedule']['scheduleType'] = 'NON_IMMEDIATE'
        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
                                              messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[104],
                                     expectedErrorMessage=[
                                         'Invalid request : invalid data type of field schedule'])

    def test_createMessage_negative_validationMessage_schedule_ScheduleType_WithDifferentDataTypes(self):
        payload = copy.deepcopy(self.messagePayload)
        payload['targetAudience'].update({'include': [self.listInfo['ID']]})
        payload['schedule']['scheduleType'] = ['IMMEDIATE', 'PARTICULAR_DATE', 'RECURRING']
        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
                                              messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[104],
                                     expectedErrorMessage=[
                                         'Invalid request : invalid data type of field schedule'])

    def test_createMessage_negative_validationMessage_schedule_ScheduleType_AsNull(self):
        payload = copy.deepcopy(self.messagePayload)
        payload['targetAudience'].update({'include': [self.listInfo['ID']]})
        payload['schedule']['scheduleType'] = 'immediate'
        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
                                              messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[104],
                                     expectedErrorMessage=[
                                         'Invalid request : invalid data type of field schedule'])

    def test_createMessage_negative_validationMessage_schedule_ScheduleType_KeyNotAvialable(self):
        payload = copy.deepcopy(self.messagePayload)
        payload['targetAudience'].update({'include': [self.listInfo['ID']]})
        payload['schedule'].pop('scheduleType')
        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
                                              messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[102,104],
                                     expectedErrorMessage=[
                                         'Invalid request : invalid data type of field schedule'])

    def test_createMessage_negative_validationMessage_schedule_ScheduleType_someExtraUnknownKey(self):
        payload = copy.deepcopy(self.messagePayload)
        payload['schedule'].update({'key': 'value'})
        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
                                              messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[107],
                                     expectedErrorMessage=[
                                         'Unrecognized field : key'])

    def test_createMessage_negative_validationMessage_schedule_Asnull(self):
        payload = copy.deepcopy(self.messagePayload)
        payload['targetAudience'].update({'include': [self.listInfo['ID']]})
        payload['schedule'] = None
        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
                                              messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[102],
                                     expectedErrorMessage= ['Invalid request : Schedule is required.','Invalid request : Schedule is required. '])

    def test_createMessage_negative_validationMessage_schedule_WithDifferentDataType(self):
        payload = copy.deepcopy(self.messagePayload)
        payload['targetAudience'].update({'include': [self.listInfo['ID']]})
        payload['schedule'] = [{'scheduleType': 'IMMEDIATE'}]
        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
                                              messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[104],
                                     expectedErrorMessage=[
                                         'Invalid request : invalid data type of field schedule'])

    def test_createMessage_negative_validationMessage_schedule_KeyNotAvialable(self):
        payload = copy.deepcopy(self.messagePayload)
        payload['targetAudience'].update({'include': [self.listInfo['ID']]})
        payload.pop('schedule')
        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
                                              messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[102],
                                     expectedErrorMessage=['Invalid request : Schedule is required.','Invalid request : Schedule is required. '])

    def test_createMessage_negative_validationMessage_deliverySetting_AsNull(self):
        payload = copy.deepcopy(self.messagePayload)
        payload['targetAudience'].update({'include': [self.listInfo['ID']]})
        payload['deliverySetting'] = None
        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
                                              messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[102],
                                     expectedErrorMessage=
                                         ['Invalid request : Delivery setting cannot be null','Invalid request : Delivery setting is required.'])

    def test_createMessage_negative_validationMessage_deliverySetting_WithDifferentDataType(self):
        payload = copy.deepcopy(self.messagePayload)
        payload['targetAudience'].update({'include': [self.listInfo['ID']]})
        payload['deliverySetting'] = [payload['deliverySetting']]
        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
                                              messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[104],
                                     expectedErrorMessage=[
                                         'Invalid request : invalid data type of field deliverySetting'])

    def test_createMessage_negative_validationMessage_deliverySetting_WithExtraUnknownKey(self):
        payload = copy.deepcopy(self.messagePayload)
        payload['targetAudience'].update({'include': [self.listInfo['ID']]})
        payload['deliverySetting'].update({'key': 'value'})
        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
                                              messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[107],
                                     expectedErrorMessage=[
                                         'Unrecognized field : key'])

    def test_createMessage_negative_validationMessage_deliverySetting_KeyNotAvialable(self):
        payload = copy.deepcopy(self.messagePayload)
        payload['targetAudience'].update({'include': [self.listInfo['ID']]})
        payload.pop('deliverySetting')
        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
                                              messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[102],
                                     expectedErrorMessage=[
                                         'Invalid request : Delivery setting cannot be null','Invalid request : Delivery setting is required.'
                                     ])

    def test_createMessage_negative_validationMessage_deliverySetting_channelSetting_AsNull(self):
        payload = copy.deepcopy(self.messagePayload)
        payload['targetAudience'].update({'include': [self.listInfo['ID']]})
        payload['deliverySetting']['channelSetting'] = None
        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
                                              messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[102],
                                     expectedErrorMessage=[
                                         'Invalid request : Channel settings is required.'])

    def test_createMessage_negative_validationMessage_deliverySetting_channelSetting_DifferentDataType(self):
        payload = copy.deepcopy(self.messagePayload)
        payload['targetAudience'].update({'include': [self.listInfo['ID']]})
        payload['deliverySetting']['channelSetting'] = [payload['deliverySetting']['channelSetting']]
        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
                                              messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[104],
                                     expectedErrorMessage=[
                                         'Invalid request : invalid data type of field channelSetting'])

    def test_createMessage_negative_validationMessage_deliverySetting_channelSetting_UnknownChannel(self):
        payload = copy.deepcopy(self.messagePayload)
        payload['targetAudience'].update({'include': [self.listInfo['ID']]})
        payload['deliverySetting']['channelSetting'].update({'UNKNOWN_CHANNEL': {'channel': 'unknown_channel'}})
        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
                                              messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[104],
                                     expectedErrorMessage=[
                                         'Invalid request : invalid value for field channelSetting'])

    def test_createMessage_negative_validationMessage_deliverySetting_channelSetting_SMS_DifferentChannelConfig(self):
        payload = copy.deepcopy(self.messagePayload)
        payload['name'] = 'SMSDifferentChannel_{}'.format(int(time.time()*1000))
        payload['targetAudience'].update({'include': [self.listInfo['ID']]})
        payload['deliverySetting']['channelSetting'].pop('SMS')
        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
                                              messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[3040],
                                     expectedErrorMessage=[
                                         'Message delivery settings is missing for a message content'])

    def test_createMessage_negative_validationMessage_deliverySetting_channelSetting_SMS_WithNoSMSDeliveryInfo(self):
        payload = copy.deepcopy(self.messagePayload)
        payload['targetAudience'].update({'include': [self.listInfo['ID']]})
        payload['deliverySetting']['channelSetting']['SMS'] = None
        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
                                              messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[102],
                                     expectedErrorMessage=[
                                         'Invalid request : Channel delivery setting cannot be null for SMS'])

    def test_createMessage_negative_validationMessage_deliverySetting_channelSetting_SMS_WithDifferentDataType(self):
        payload = copy.deepcopy(self.messagePayload)
        payload['targetAudience'].update({'include': [self.listInfo['ID']]})
        payload['deliverySetting']['channelSetting']['SMS'] = [payload['deliverySetting']['channelSetting']['SMS']]
        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
                                              messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[104],
                                     expectedErrorMessage=['Invalid request : invalid data type of field SMS'])

    def test_createMessage_negative_validationMessage_deliverySetting_channelSetting_SMS_WrongValueOfChannel(self):
        payload = copy.deepcopy(self.messagePayload)
        payload['targetAudience'].update({'include': [self.listInfo['ID']]})
        payload['deliverySetting']['channelSetting']['SMS']['channel'] = ''
        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
                                              messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[104],
                                     expectedErrorMessage=[
                                         'Invalid request : channel , Unknown value , allowed values are [SMS, EMAIL, MOBILEPUSH, CALL_TASK, WECHAT, FACEBOOK]'])

    def test_createMessage_negative_validationMessage_deliverySetting_channelSetting_EMAIL_WrongValueOfChannel_MessageAsSMS(
            self):
        payload = copy.deepcopy(self.messagePayload)
        payload['targetAudience'].update({'include': [self.listInfo['ID']]})
        payload['deliverySetting']['channelSetting']['EMAIL']['channel'] = 'SMS'
        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'EMAIL',
                                              messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[107],
                                     expectedErrorMessage=[
                                         'Unrecognized field : senderLabel'])

    def test_createMessage_negative_validationMessage_deliverySetting_channelSetting_EMAIL_WrongValueOfChannel(self):
        payload = copy.deepcopy(self.messagePayload)
        payload['targetAudience'].update({'include': [self.listInfo['ID']]})
        payload['messageContent']['message_content_id_1'].pop('messageBody')
        payload['messageContent']['message_content_id_1'].update(
            {
                'emailBody': 'Hi , Auto Email without Subscription Tag',
                'emailSubject': 'Auto Subject',
                'channel': 'EMAIL'
            })
        payload['deliverySetting']['channelSetting']['EMAIL']['channel'] = ''
        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'EMAIL',
                                              messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[107],
                                     expectedErrorMessage=[
                                         'Unrecognized field : senderLabel'])

    def test_createMessage_negative_validationMessage_deliverySetting_channelSetting_SMS_ChannelAsNull(self):
        payload = copy.deepcopy(self.messagePayload)
        payload['targetAudience'].update({'include': [self.listInfo['ID']]})
        payload['deliverySetting']['channelSetting']['SMS']['channel'] = None
        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
                                              messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[104],
                                     expectedErrorMessage=[
                                         'Invalid request : channel , Unknown value null, allowed values are [SMS, EMAIL, MOBILEPUSH, CALL_TASK, WECHAT, FACEBOOK]'])

    def test_createMessage_negative_validationMessage_deliverySetting_channelSetting_SMS_ChannelKeyNotPresent(self):
        payload = copy.deepcopy(self.messagePayload)
        payload['targetAudience'].update({'include': [self.listInfo['ID']]})
        payload['deliverySetting']['channelSetting']['SMS'].pop('channel')
        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
                                              messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[102],
                                     expectedErrorMessage=[
                                         'Invalid request : Invalid channel setting : Channel type is missing'])

    def test_createMessage_negative_validationMessage_deliverySetting_additionalSetting_asNull(self):
        payload = copy.deepcopy(self.messagePayload)
        payload['name'] = 'AdditionalSettingNull_{}'.format(int(time.time() * 1000))
        payload['targetAudience'].update({'include': [self.listInfo['ID']]})
        payload['deliverySetting']['additionalSetting'] = None
        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
                                              messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200, expectedErrorCode=[102],
                                     expectedErrorMessage=[
                                         'Invalid request : AdditionSetting is Mandatory Field'])

    def test_createMessage_negative_validationMessage_deliverySetting_additionalSetting_asEmpty(self):
        payload = copy.deepcopy(self.messagePayload)
        payload['targetAudience'].update({'include': [self.listInfo['ID']]})
        payload['deliverySetting']['additionalSetting'] = ''
        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
                                              messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[104],
                                     expectedErrorMessage=[
                                         'Invalid request : invalid data type of field additionalSetting'])

    def test_createMessage_negative_validationMessage_deliverySetting_additionalSetting_withWrongDataType(self):
        payload = copy.deepcopy(self.messagePayload)
        payload['targetAudience'].update({'include': [self.listInfo['ID']]})
        payload['deliverySetting']['additionalSetting'] = [payload['deliverySetting']['additionalSetting']]
        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
                                              messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[104],
                                     expectedErrorMessage=[
                                         'Invalid request : invalid data type of field additionalSetting'])

    def test_createMessage_negative_validationMessage_WithEmptyBody(self):
        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE',

                                              messageInfo=self.messageInfo,
                                              payload={},
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[102],
                                     expectedErrorMessage=['Invalid request : Audience group rule is required. ',
                                         'Invalid request : Audience group rule is required.','Invalid request : Message content is required','Invalid request : Schedule is required.','Invalid request : Delivery setting is required.','Invalid request : Schedule is required. ','Invalid request : Delivery setting cannot be null'])

    def test_createMessage_negative_validationMessage_WithExtraUnknownKeysInBody(self):
        payload = copy.deepcopy(self.messagePayload)
        payload['key'] = 'value'
        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
                                              messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[107],
                                     expectedErrorMessage=[
                                         'Unrecognized field : key'])

    @pytest.mark.parametrize('keysToPop,errorCode,errorMessage', [
        (['targetAudience', 'type', 'name'], [102], ['Invalid request : Audience group rule is required.','Invalid request : Message name is required','Invalid request : Audience group rule is required. ','Invalid request : Message content is required. ','Invalid request : Message content is required','Invalid request : Target audience is required.']),
        (['targetAudience', 'messageContent', 'messageStrategy'], [102],
         ['Invalid request : Message content is required','Invalid request : Message content is required. ','Invalid request : Audience Group Split Strategy is required. ','Invalid request : Audience group rule is required. ','Invalid request : Audience group rule is required.']),
        (['deliverySetting', 'schedule'], [102], ['Invalid request : Schedule is required. ','Invalid request : Schedule is required.','Invalid request : Audience group rule is required.','Invalid request : Include audience cannot be empty','Invalid request : Delivery setting is required.','Invalid request : Audience Group Split Strategy is required. ','Invalid request : Delivery setting cannot be null','Invalid request : Target audience is required.'])
    ])
    def test_createMessage_negative_validationMessage_integration_MultipleFieldNotPresent(self, keysToPop, errorCode,errorMessage):
        payload = copy.deepcopy(self.messagePayload)
        for each in keysToPop:
            payload.pop(each)
        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
                                              messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=errorCode,
                                     expectedErrorMessage=errorMessage
                                     )

    def test_createMessage_negative_validationMessage_wrongValueOfcampaignId(self):
        payload = copy.deepcopy(self.messagePayload)
        payload['targetAudience'].update({'include': [self.listInfo['ID']]})
        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
                                              messageInfo=self.messageInfo,
                                              campaignId=0,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[102],
                                     expectedErrorMessage=[
                                         'Invalid request : Campaign Id must be greater than or equal to 1'])

    def test_createMessage_negative_validationMessage_wrongOrgId(self):
        previousOrgId = IrisHelper.updateOrgId(-1)
        try:
            payload = copy.deepcopy(self.messagePayload)
            messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
                                                  messageInfo=self.messageInfo,
                                                  payload=payload,
                                                  updateNode=True,
                                                  lockNode=True)
            CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[102],
                                         expectedErrorMessage=[
                                             'Invalid request : Message body have unknown tag'])
        except Exception, exp:
            Logger.log('Exception Occured :{}'.format(exp))
        finally:
            IrisHelper.updateOrgId(previousOrgId)

    def test_createMessage_negative_validationMessage_integration_AllValueAsNull(self):
        payload = copy.deepcopy(self.messagePayload)
        for each in payload:
            payload[each] = None
        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
                                              messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[104],
                                     expectedErrorMessage=[
                                         'Invalid request : type , Unknown value null, allowed values are [OUTBOUND]'])

    def test_createMessage_negative_validationMessage_lapsedCampaign(self):
        payload = copy.deepcopy(self.messagePayload)
        payload['targetAudience'].update({'include': [self.listInfo['ID']]})
        campaignId = CreateCampaign.create('LAPSED', 'ORG')['ID']
        time.sleep(20)
        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
                                              messageInfo=self.messageInfo,
                                              campaignId=campaignId,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[3036],
                                     expectedErrorMessage=[
                                         'Campaign expired'])

    def test_createMessage_negative_validationMessage_DomainGatewayMapIdNotExist(self):
        payload = copy.deepcopy(self.messagePayload)
        payload['targetAudience'].update({'include': [self.listInfo['ID']]})
        payload['deliverySetting']['channelSetting']['SMS']['domainGatewayMapId'] = 99
        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
                                              messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[3005],
                                     expectedErrorMessage=[
                                         'Domain Gateway Map with id does not exist : 99'])

    def test_createMessage_negative_validationMessage_WrongAuth(self):
        previousAuth = IrisHelper.updateUserName('First')
        try:
            payload = copy.deepcopy(self.messagePayload)
            payload['targetAudience'].update({'include': [self.listInfo['ID']]})
            messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
                                                  messageInfo=self.messageInfo,
                                                  payload=payload,
                                                  updateNode=True,
                                                  lockNode=True)
            CreateMessage.assertResponse(messageDetails['RESPONSE'], 401, expectedErrorCode=[999999],
                                         expectedErrorMessage=[
                                             'Unauthorized'])
        except Exception, exp:
            Assertion.constructAssertion(False, 'Exception Occured :{}'.format(exp))
        finally:
            IrisHelper.updateUserName(previousAuth)

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo,storeType', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True},
         'LAST')
    ])
    def test_createMessage_negative_validationMessage_WithUnknownStoreType(self, campaignType, testControlType, listType,
                                                                   channel, messageInfo, storeType):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True, lockNode=True, storeType=storeType)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[104],
                                     expectedErrorMessage=[
                                         'Invalid request : storeType , Unknown value LAST, allowed values are [REGISTERED_STORE, LAST_TRANSACTED_AT]'])

    #Validation Cases For ParticularDate

    def test_createMessage_negative_validationMessage_particularDate_schedule_NoScheduleDate(self):
        payload = copy.deepcopy(self.messagePayload)
        payload['targetAudience'].update({'include': [self.listInfo['ID']]})
        payload['schedule'].update({
            'scheduleType': 'PARTICULAR_DATE'
        })
        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
                                              messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[102],
                                     expectedErrorMessage=['Invalid request : Scheduled Date is required.','Invalid request : Scheduled date is required.'])

    def test_createMessage_negative_validationMessage_particularDate_schedule_InvalidSchedulleDate(self):
        payload = copy.deepcopy(self.messagePayload)
        payload['targetAudience'].update({'include': [self.listInfo['ID']]})
        payload['schedule'].update({
            'scheduleType': 'PARTICULAR_DATE',
            'scheduledDate': datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        })
        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
                                              messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[104],
                                     expectedErrorMessage=['Invalid request : invalid value for field scheduledDate'])

    def test_createMessage_negative_validationMessage_particularDate_schedule_WrongFormatSchedulleDate(self):
        payload = copy.deepcopy(self.messagePayload)
        payload['targetAudience'].update({'include': [self.listInfo['ID']]})
        payload['schedule'].update({
            'scheduleType': 'PARTICULAR_DATE',
            'scheduledDate': {'date':datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')}
        })
        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
                                              messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[104],
                                     expectedErrorMessage=['Invalid request : invalid data type of field scheduledDate'])

    def test_createMessage_negative_validationMessage_particularDate_schedule_SchedulleDateLessThanNow(self):
        payload = copy.deepcopy(self.messagePayload)
        payload['targetAudience'].update({'include': [self.listInfo['ID']]})
        payload['schedule'].update({
            'scheduleType': 'PARTICULAR_DATE',
            'scheduledDate': time.time()-100
        })
        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
                                              messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[102],
                                     expectedErrorMessage=[
                                         'Invalid request : Scheduled date cannot be in the past'])

    def test_createMessage_negative_validationMessage_particularDate_schedule_SchedulleDateAsNow(self):
        payload = copy.deepcopy(self.messagePayload)
        payload['targetAudience'].update({'include': [self.listInfo['ID']]})
        payload['schedule'].update({
            'scheduleType': 'PARTICULAR_DATE',
            'scheduledDate': int(time.time()*1000)
        })
        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
                                              messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[102],
                                     expectedErrorMessage=[
                                         'Invalid request : Scheduled date cannot be in the past'])


    def test_createMessage_negative_validationMessage_points_programId_invalid(self):
        payload = copy.deepcopy(self.messagePayload)
    # payload['targetAudience'].update({'include': [self.listInfo['ID']]})
        payload['messageContent']['message_content_id_1'].update({'offers' : [{
                    "programId": "abc",
                    "type":"POINTS",
                    "allocationStrategyId": 59361,
                    "expirationStrategyId": 59362
        } ]
        })
        messageDetails = CreateMessage.create('LIVE','ORG','UPLOAD','MOBILE',
                                              messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True,)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[104],
                                 expectedErrorMessage=[
                                     "Invalid request : invalid value for field programId"])


    def test_createMessage_negative_validationMessage_points_withoutProgramId(self):
        payload = copy.deepcopy(self.messagePayload)
        payload['targetAudience'].update({'include': [self.listInfo['ID']]})
        payload['messageContent']['message_content_id_1'].update({'offers' : [{

                    "type":"POINTS",
                    "allocationStrategyId": 59361,
                    "expirationStrategyId": 59362
        } ]
        })
        messageDetails = CreateMessage.create('LIVE','ORG','UPLOAD','MOBILE',
                                              messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True,)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[102],
                                 expectedErrorMessage=[
                                     "Invalid request : Program id in points offers is required"])

    def test_createMessage_negative_validationMessage_points_invalidType(self):
        payload = copy.deepcopy(self.messagePayload)
        payload['targetAudience'].update({'include': [self.listInfo['ID']]})
        payload['messageContent']['message_content_id_1'].update({'offers': [{
            "programId": 1350,
            "type": "TEST",
            "allocationStrategyId": 59361,
            "expirationStrategyId": 59362
        }]
        })
        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
                                              messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True, )
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[107],
                                     expectedErrorMessage=[
                                         "Unrecognized field : programId"])

    def test_createMessage_negative_validationMessage_points_noType(self):
        payload = copy.deepcopy(self.messagePayload)
        payload['targetAudience'].update({'include': [self.listInfo['ID']]})
        payload['messageContent']['message_content_id_1'].update({'offers': [{
            "programId": 1350,

            "allocationStrategyId": 59361,
            "expirationStrategyId": 59362
        }]
        })
        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
                                              messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True, )
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[107],
                                     expectedErrorMessage=[
                                         "Invalid request : invalid value for field programId","Unrecognized field : programId"])

    def test_createMessage_negative_validationMessage_points_invalidAllocation(self):
        payload = copy.deepcopy(self.messagePayload)
        payload['targetAudience'].update({'include': [self.listInfo['ID']]})
        payload['messageContent']['message_content_id_1'].update({'offers': [{
            "programId": 1350,
            "type": "POINTS",
            "allocationStrategyId": 678,
            "expirationStrategyId": 59362
        }]
        })
        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
                                              messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True, )
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[3009],
                                     expectedErrorMessage=[
                                         "Provided points incentive details are invalid : Invalid allocation strategy id","Provided points incentive details are invalid : Invalid program id"])


    def test_createMessage_negative_validationMessage_points_withoutAllocation(self):
        payload = copy.deepcopy(self.messagePayload)
        payload['targetAudience'].update({'include': [self.listInfo['ID']]})
        payload['messageContent']['message_content_id_1'].update({'offers': [{
            "programId": 1350,
            "type": "POINTS",
            "expirationStrategyId": 59362
        }]
        })
        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
                                              messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True, )
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[102],
                                     expectedErrorMessage=[
                                         "Invalid request : Allocation strategy id in points offers is required"])


    def test_createMessage_negative_validationMessage_points_invalidExpiration(self):
        payload = copy.deepcopy(self.messagePayload)
        payload['targetAudience'].update({'include': [self.listInfo['ID']]})
        payload['messageContent']['message_content_id_1'].update({'offers': [{
            "programId": 1350,
            "type": "POINTS",
            "allocationStrategyId": 59361,
            "expirationStrategyId": 5936
        }]
        })
        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
                                              messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True, )
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[3009],
                                     expectedErrorMessage=[
                                         "Provided points incentive details are invalid : Invalid expiry strategy id","Provided points incentive details are invalid : Invalid program id"])

    def test_createMessage_negative_validationMessage_points_withoutExpiration(self):
            payload = copy.deepcopy(self.messagePayload)
            payload['targetAudience'].update({'include': [self.listInfo['ID']]})
            payload['messageContent']['message_content_id_1'].update({'offers': [{
                "programId": 1350,
                "type": "POINTS",
                "allocationStrategyId": 59361

            }]
            })
            messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
                                                  messageInfo=self.messageInfo,
                                                  payload=payload,
                                                  updateNode=True,
                                                  lockNode=True, )
            CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[102],
                                         expectedErrorMessage=[
                                             "Invalid request : Expiry strategy id in points offers is required"])

    def test_createMessage_negative_validationMessage_recurringSchedule_invalidHourValue(self):
        payload = copy.deepcopy(self.messagePayload)
        payload['schedule']['scheduleType'] = 'RECURRING'
        payload['schedule']['hour'] = "abc"
        messageDetails = CreateMessage.create('LIVE', 'ORG', 'LOYALTY', 'MOBILE',
                                              messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[104],
                                     expectedErrorMessage=[
                                         'Invalid request : invalid value for field hour'])

    def test_createMessage_negative_validationMessage_recurringSchedule_nullHourValue(self):
        payload = copy.deepcopy(self.messagePayload)
        payload['schedule']['scheduleType'] = 'RECURRING'
        payload['targetAudience'].update({'include': [self.listInfo['ID']]})
        payload['schedule']['hour'] = "NUll"
        messageDetails = CreateMessage.create('LIVE', 'ORG', 'LOYALTY', 'MOBILE',
                                              messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[104],
                                     expectedErrorMessage=[
                                         'Invalid request : invalid value for field hour'])

    def test_createMessage_negative_validationMessage_recurringSchedule_withoutHourValue(self):
        payload = copy.deepcopy(self.messagePayload)
        payload['targetAudience'].update({'include': [self.listInfo['ID']]})
        payload['schedule']['scheduleType'] = 'RECURRING'
        payload['schedule']['repeatType'] = "WEEKLY"
        payload['schedule']['startDate'] = (time.time() * 1000) + 20000
        payload['schedule']['endDate'] = (time.time() * 1000) + 20000 + 1000
        payload['schedule']['repeatOn'] = [1]
        payload['schedule']['minute'] = 15
        messageDetails = CreateMessage.create('LIVE', 'ORG', 'LOYALTY', 'MOBILE',
                                              messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[104,102],
                                     expectedErrorMessage=[
                                         'Invalid request : Invalid schedule : Invalid hour','Invalid request : Hour in reccuring schedule is required'])

    def test_createMessage_negative_validationMessage_recurringSchedule_invalidMinute(self):
        payload = copy.deepcopy(self.messagePayload)
        payload['targetAudience'].update({'include': [self.listInfo['ID']]})
        payload['schedule']['scheduleType'] = 'RECURRING'
        payload['schedule']['repeatType'] = "DAILY"
        payload['schedule']['startDate'] = (time.time() * 1000) + 20000
        payload['schedule']['endDate'] = (time.time() * 1000) + 20000 + 1000
        payload['schedule']['repeatOn'] = [1]
        payload['schedule']['hour'] = 13
        payload['schedule']['minute'] = 'abc'

        messageDetails = CreateMessage.create('LIVE', 'ORG', 'LOYALTY', 'MOBILE',
                                              messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[104],
                                     expectedErrorMessage=[
                                         'Invalid request : invalid value for field minute'])

    def test_createMessage_negative_validationMessage_recurringSchedule_nullMinute(self):
        payload = copy.deepcopy(self.messagePayload)
        payload['targetAudience'].update({'include': [self.listInfo['ID']]})
        payload['schedule']['scheduleType'] = 'RECURRING'
        payload['schedule']['repeatType'] = "MONTHLY"
        payload['schedule']['startDate'] = (time.time() * 1000) + 20000
        payload['schedule']['endDate'] = (time.time() * 1000) + 20000 +100
        payload['schedule']['repeatOn'] = [1]
        payload['schedule']['hour'] = 13
        payload['schedule']['minute'] = 'null'

        messageDetails = CreateMessage.create('LIVE', 'ORG', 'LOYALTY', 'MOBILE',
                                              messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[102],
                                     expectedErrorMessage=[
                                         'Invalid request : Minute in reccuring schedule is required'])

    def test_createMessage_negative_validationMessage_recurringSchedule_notMinute(self):
        payload = copy.deepcopy(self.messagePayload)
        payload['targetAudience'].update({'include': [self.listInfo['ID']]})
        payload['schedule']['scheduleType'] = 'RECURRING'
        payload['schedule']['repeatType'] = "WEEKLY"
        payload['schedule']['startDate'] = (time.time() * 1000) + 20000
        payload['schedule']['endDate'] = (time.time() * 1000) + 20000 +1000
        payload['schedule']['repeatOn'] = [1]
        payload['schedule']['hour'] = 13


        messageDetails = CreateMessage.create('LIVE', 'ORG', 'LOYALTY', 'MOBILE',
                                              messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[102],
                                     expectedErrorMessage=[
                                         'Invalid request : Invalid schedule : Invalid minute',
                                     'Invalid request : Minute in reccuring schedule is required'])

    def test_createMessage_negative_validationMessage_recurringSchedule_emptyRepeatOnList(self):
        payload = copy.deepcopy(self.messagePayload)
        payload['targetAudience'].update({'include': [self.listInfo['ID']]})
        payload['schedule']['scheduleType'] = 'RECURRING'
        payload['schedule']['repeatType'] = "WEEKLY"
        payload['schedule']['startDate'] = (time.time() * 1000) + 20000
        payload['schedule']['endDate'] = (time.time() * 1000) + 20000 +1000
        payload['schedule']['repeatOn'] = []
        payload['schedule']['hour'] = 13
        payload['schedule']['minute'] = 23

        messageDetails = CreateMessage.create('LIVE', 'ORG', 'LOYALTY', 'MOBILE',
                                              messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[102],
                                     expectedErrorMessage=[
                                         'Invalid request : Repeat on in reccuring schedule is required'])

    def test_createMessage_negative_validationMessage_recurringSchedule_InvalidDataType_repeatOn(self):
        payload = copy.deepcopy(self.messagePayload)
        payload['targetAudience'].update({'include': [self.listInfo['ID']]})
        payload['schedule']['scheduleType'] = 'RECURRING'
        payload['schedule']['repeatType'] = "WEEKLY"
        payload['schedule']['startDate'] = (time.time() * 1000) + 20000
        payload['schedule']['endDate'] = (time.time() * 1000) + 20000 + 1000
        payload['schedule']['repeatOn'] = 1
        payload['schedule']['hour'] = 13
        payload['schedule']['minute'] = 23

        messageDetails = CreateMessage.create('LIVE', 'ORG', 'LOYALTY', 'MOBILE',
                                              messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[104],
                                     expectedErrorMessage=[
                                         'Invalid request : invalid data type of field repeatOn'])

    def test_createMessage_negative_validationMessage_recurringSchedule_withoutRepeatOn(self):
        payload = copy.deepcopy(self.messagePayload)
        payload['targetAudience'].update({'include': [self.listInfo['ID']]})
        payload['schedule']['scheduleType'] = 'RECURRING'
        payload['schedule']['repeatType'] = "WEEKLY"
        payload['schedule']['startDate'] = (time.time() * 1000) + 20000
        payload['schedule']['endDate'] = (time.time() * 1000) + 20000 + 1000
        payload['schedule']['hour'] = 13
        payload['schedule']['minute'] = 23

        messageDetails = CreateMessage.create('LIVE', 'ORG', 'LOYALTY', 'MOBILE',
                                              messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[102],
                                     expectedErrorMessage=[
                                         'Invalid request : Repeat on in reccuring schedule is required'])

    def test_createMessage_negative_validationMessage_recurringSchedule_withoutFilterList(self):
        payload = copy.deepcopy(self.messagePayload)
        payload['targetAudience'].update({'include': [self.listInfo['ID']]})
        payload['schedule']['scheduleType'] = 'RECURRING'
        payload['schedule']['repeatType'] = "DAILY"
        payload['schedule']['startDate'] = (time.time() * 1000) + 20000
        payload['schedule']['endDate'] = (time.time() * 1000) + 20000+1000
        payload['schedule']['hour'] = 13
        payload['schedule']['minute'] = 1

        messageDetails = CreateMessage.create('LIVE', 'ORG', 'LOYALTY', 'MOBILE',
                                              messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[3050],
                                     expectedErrorMessage=[
                                         'Target Audience is not filter based : {}.'.format(self.listInfo['ID'])])

    def test_createMessage_negative_validationMessage_recurringSchedule_invalidRepeatType(self):
            payload = copy.deepcopy(self.messagePayload)
            payload['targetAudience'].update({'include': [self.listInfo['ID']]})
            payload['schedule']['scheduleType'] = 'RECURRING'
            payload['schedule']['repeatType'] = "ab"
            payload['schedule']['startDate'] = (time.time() * 1000) + 20000
            payload['schedule']['endDate'] = (time.time() * 1000) + 20000+1000
            payload['schedule']['repeatOn'] = [1]
            payload['schedule']['hour'] = 13
            payload['schedule']['minute'] = 1

            messageDetails = CreateMessage.create('LIVE', 'ORG', 'LOYALTY', 'MOBILE',
                                                  messageInfo=self.messageInfo,
                                                  payload=payload,
                                                  updateNode=True,
                                                  lockNode=True)
            CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[102],
                                         expectedErrorMessage=[
                                             'Invalid request : Missing field repeat type','Invalid request : Repeat type in reccuring schedule is required'])

    def test_createMessage_negative_validationMessage_recurringSchedule_withoutRepeatType(self):
        payload = copy.deepcopy(self.messagePayload)
        payload['targetAudience'].update({'include': [self.listInfo['ID']]})
        payload['schedule']['scheduleType'] = 'RECURRING'
        payload['schedule']['startDate'] = (time.time() * 1000) + 20000
        payload['schedule']['endDate'] = (time.time() * 1000) + 20000 + 1000
        payload['schedule']['repeatOn'] = [1]
        payload['schedule']['hour'] = 13
        payload['schedule']['minute'] = 1

        messageDetails = CreateMessage.create('LIVE', 'ORG', 'LOYALTY', 'MOBILE',
                                              messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        payload['targetAudience'].update({'include': [self.listInfo['ID']]})
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[102],
                                     expectedErrorMessage=[
                                         'Invalid request : invalid value for field repeatOn','Invalid request : Repeat type in reccuring schedule is required'])

    def test_createMessage_negative_validationMessage_recurringSchedule_startOldDate(self):

        payload = copy.deepcopy(self.messagePayload)
        payload['targetAudience'].update({'include': [self.listInfo['ID']]})
        payload['schedule']['scheduleType'] = 'RECURRING'
        payload['schedule']['repeatType'] = "WEEKLY"
        payload['schedule']['startDate'] = 1559198511000
        payload['schedule']['endDate'] = (time.time() * 1000) + 20000 +1000
        payload['schedule']['repeatOn'] = [1,3]
        payload['schedule']['hour'] = 13
        payload['schedule']['minute'] = 1

        messageDetails = CreateMessage.create('LIVE', 'ORG', 'LOYALTY', 'MOBILE',
                                              messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[102],
                                     expectedErrorMessage=[
                                         'Invalid request : Invalid schedule : Start date is less than current date'])

    def test_createMessage_negative_validationMessage_recurringSchedule_endDatelessThanStart(self):

        payload = copy.deepcopy(self.messagePayload)
        payload['targetAudience'].update({'include': [self.listInfo['ID']]})
        payload['schedule']['scheduleType'] = 'RECURRING'
        payload['schedule']['repeatType'] = "DAILY"
        payload['schedule']['startDate'] = (time.time() * 1000) + 20000 +1000
        payload['schedule']['endDate'] = (time.time() * 1000)
        payload['schedule']['repeatOn'] = [1]
        payload['schedule']['hour'] = 13
        payload['schedule']['minute'] = 1

        messageDetails = CreateMessage.create('LIVE', 'ORG', 'LOYALTY', 'MOBILE',
                                              messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[102],
                                     expectedErrorMessage=[
                                         'Invalid request : Invalid schedule : End date is less than or equal to start date'])


    def test_createMessage_negative_validationMessage_recurringSchedule_startDateIsNull(self):
        payload = copy.deepcopy(self.messagePayload)
        payload['targetAudience'].update({'include': [self.listInfo['ID']]})
        payload['schedule']['scheduleType'] = 'RECURRING'
        payload['schedule']['repeatType'] = "DAILY"
        payload['schedule']['startDate'] = "NULL"
        payload['schedule']['endDate'] = Utils.getTime(days = 2,milliSeconds=True)
        payload['schedule']['repeatOn'] = [1]
        payload['schedule']['hour'] = 13
        payload['schedule']['minute'] = 1

        messageDetails = CreateMessage.create('LIVE', 'ORG', 'LOYALTY', 'MOBILE',
                                              messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[104],
                                     expectedErrorMessage=[
                                         'Invalid request : invalid value for field startDate'])

    def test_createMessage_negative_validationMessage_recurringSchedule_endDateIsNull(self):
        payload = copy.deepcopy(self.messagePayload)
        payload['targetAudience'].update({'include': [self.listInfo['ID']]})
        payload['schedule']['scheduleType'] = 'RECURRING'
        payload['schedule']['repeatType'] = "DAILY"
        payload['schedule']['startDate'] = (time.time() * 1000) + 20000
        payload['schedule']['endDate'] = "NULL"
        payload['schedule']['repeatOn'] = [1]
        payload['schedule']['hour'] = 13
        payload['schedule']['minute'] = 1

        messageDetails = CreateMessage.create('LIVE', 'ORG', 'LOYALTY', 'MOBILE',
                                              messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[104],
                                     expectedErrorMessage=[
                                         'Invalid request : invalid value for field endDate'])

    def test_createMessage_negative_validationMessage_recurringSchedule_invalidCronValue(self):

            payload = copy.deepcopy(self.messagePayload)
            payload['targetAudience'].update({'include': [self.listInfo['ID']]})
            payload['schedule']['scheduleType'] = 'RECURRING'
            payload['schedule']['repeatType'] = "WEEKLY"
            payload['schedule']['startDate'] = (time.time() * 1000) + 20000
            payload['schedule']['endDate'] = (time.time() * 1000) + 20000 +1000
            payload['schedule']['repeatOn'] = [1]
            payload['schedule']['hour'] = 56
            payload['schedule']['minute'] = 1

            messageDetails = CreateMessage.create('LIVE', 'ORG', 'LOYALTY', 'MOBILE',
                                                  messageInfo=self.messageInfo,
                                                  payload=payload,
                                                  updateNode=True,
                                                  lockNode=True)
            payload['targetAudience'].update({'include': [self.listInfo['ID']]})
            CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[102],
                                         expectedErrorMessage=[
                                             'Invalid request : Invalid schedule : Invalid hour'])

    @pytest.mark.parametrize(
        'campaignType,testControlType,listType,channel,scheduleType,statusCode,errorCode,errorDescription', [
            ('LIVE', 'ORG', 'LOYALTY', 'MOBILE',
             {'type': 'RECURRING', 'hour': '15', 'minute': '30', 'repeatType': 'DAIL', 'repeatOn': [1]}, 400, 102,
             ['Invalid request : Repeat type in reccuring schedule is required']),
            ('LIVE', 'ORG', 'LOYALTY', 'MOBILE',
             {'type': 'RECURRING', 'hour': '15', 'minute': '30', 'repeatType': 'MONTHL', 'repeatOn': [1]}, 400, 102,
             ['Invalid request : Repeat type in reccuring schedule is required']),
            ('LIVE', 'ORG', 'LOYALTY', 'MOBILE',
             {'type': 'RECURRING', 'hour': '15', 'minute': '30', 'repeatType': 'WEEKLYY', 'repeatOn': [1]}, 400, 102,
             ['Invalid request : Repeat type in reccuring schedule is required']),
            ('LIVE', 'ORG', 'LOYALTY', 'MOBILE',
             {'type': 'RECURRING', 'hour': '1115', 'minute': '30', 'repeatType': 'WEEKLY', 'repeatOn': [1]}, 400, 102,
             ['Invalid request : Invalid schedule : Invalid hour']),
            ('LIVE', 'ORG', 'LOYALTY', 'MOBILE',
             {'type': 'RECURRING', 'hour': '-15', 'minute': '30', 'repeatType': 'WEEKLY', 'repeatOn': [1]}, 400, 102,
             ['Invalid request : Invalid schedule : Invalid hour']),
            ('LIVE', 'ORG', 'LOYALTY', 'MOBILE',
             {'type': 'RECURRING', 'hour': '15', 'minute': '30000', 'repeatType': 'WEEKLY', 'repeatOn': [1]}, 400, 102,
             ['Invalid request : Invalid schedule : Invalid minute']),
            ('LIVE', 'ORG', 'LOYALTY', 'MOBILE',
             {'type': 'RECURRING', 'hour': '15', 'minute': '-30', 'repeatType': 'WEEKLY', 'repeatOn': [1]}, 400, 102,
             ['Invalid request : Invalid schedule : Invalid minute']),
            ('LIVE', 'ORG', 'LOYALTY', 'MOBILE',
             {'type': 'RECURRING', 'hour': '15', 'minute': '30', 'repeatType': 'WEEKLY', 'repeatOn': [-1]}, 400, 102,
             ['Invalid request : Invalid repeat on : Invalid day of week']),
            ('LIVE', 'ORG', 'LOYALTY', 'MOBILE',
             {'type': 'RECURRING', 'hour': '15', 'minute': '30', 'repeatType': 'WEEKLY',
              'repeatOn': [0, 1, 2, 3, 4, 5, 6, 7]}, 400, 102,
             ['Invalid request : Invalid repeat on : Invalid day of week']),
            ('LIVE', 'ORG', 'LOYALTY', 'MOBILE',
             {'type': 'RECURRING', 'hour': '15', 'minute': '30', 'repeatType': 'MONTHLY', 'repeatOn': [-2]}, 400, 102,
             ['Invalid request : Invalid repeat on : Invalid day of month']),
            ('LIVE', 'ORG', 'LOYALTY', 'MOBILE',
             {'type': 'RECURRING', 'hour': '15', 'minute': '30', 'repeatType': 'MONTHLY', 'repeatOn':
                 [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28,
                  29,
                  30, 31, 32]}, 400, 102,
             ['Invalid request : Invalid repeat on : Invalid day of month']),
            ('LIVE', 'ORG', 'LOYALTY', 'MOBILE',
             {'type': 'RECURRING', 'hour': '15', 'minute': '30', 'repeatType': 'WEEKLY', 'repeatOn': [1],
              'startDate': Utils.getTime(days=-1, milliSeconds=True), }, 400, 102,
             ['Invalid request : Invalid schedule : Start date is less than current date']),
            ('LIVE', 'ORG', 'LOYALTY', 'MOBILE',
             {'type': 'RECURRING', 'hour': '15', 'minute': '30', 'repeatType': 'WEEKLY', 'repeatOn': [1],
              'endDate': Utils.getTime(days=-1, milliSeconds=True), }, 400, 102,
             ['Invalid request : Invalid schedule : End date is less than current date']),
            ('LIVE', 'ORG', 'LOYALTY', 'MOBILE',
             {'type': 'RECURRING', 'hour': '15', 'minute': '30', 'repeatType': 'WEEKLY', 'repeatOn': [1],
              'startDate': Utils.getTime(minutes=10, milliSeconds=True),
              'endDate': Utils.getTime(minutes=10, milliSeconds=True), }, 400, 102,
             ['Invalid request : Invalid schedule : End date is less than or equal to start date']),
        ])
    def test_createMessage_negative_validationMessage_recurringSchedule_invalidRepeatOn(self, campaignType, testControlType,
                                                                                  listType,
                                                                                  channel, scheduleType, statusCode,
                                                                                  errorCode, errorDescription):
        messageInfo = {
            'scheduleType': scheduleType,
            'offerType': 'PLAIN',
            'messageStrategy': {'type': 'DEFAULT'},
            'channels': ['SMS', 'EMAIL'],
            'useTinyUrl': False,
            'encryptUrl': False,
            'skipRateLimit': True
        }
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True, lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[errorCode],
                                     expectedErrorMessage=errorDescription)

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('UPCOMING', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def test_irisv2_message_create_upload_mobile_immediate_message_upcoming_campaign(self, campaignType, testControlType, listType,
                                                                        channel, messageInfo):
        CreateCampaign.create(campaignType, testControlType, startDate=(int(time.time() * 1000) + 20000 *60) ,endDate=int(
            time.time() * 1000) + 20000 * 60 * 1000)
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[999999],
                                     expectedErrorMessage=[
                                         'UPCOMING_CAMPAIGN_EXCEPTION'])

    @pytest.mark.parametrize( 'campaignType,testControlType,listType,channel,scheduleType,statusCode', [
        ('LIVE', 'ORG', 'LOYALTY', 'MOBILE',
         {'type': 'RECURRING', 'hour': '15', 'minute': '30', 'repeatType': 'WEEKLY', 'repeatOn': [1],
          'startDate': Utils.getTime(minutes=-100, milliSeconds=True),
          'endDate': Utils.getTime(minutes=20, milliSeconds=True), }, 200)
    ])

    def test_createMessage_negative_validationMessage_recurring_startDateIsPastDateToday(self, campaignType, testControlType,
                                                                                  listType,
                                                                                  channel, scheduleType, statusCode):
        messageInfo = {
            'scheduleType': scheduleType,
            'offerType': 'PLAIN',
            'messageStrategy': {'type': 'DEFAULT'},
            'channels': ['SMS', 'EMAIL'],
            'useTinyUrl': False,
            'encryptUrl': False,
            'skipRateLimit': True
        }
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True, lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[3038],
                                     expectedErrorMessage=['Invalid Schedule : Start date of recurring message is in past.','Invalid Schedule : Message cannot start before campaign.'])

    def test_createMessage_validationMessage_recurringSchedule_daily_without_repeatOn(self):

        payload = copy.deepcopy(self.messagePayload)
        payload['targetAudience'].update({'include': [self.listInfoFilter['ID']]})
        payload['schedule']['scheduleType'] = 'RECURRING'
        payload['schedule']['repeatType'] = 'DAILY'
        payload['schedule']['startDate'] = (time.time() * 1000) + 20000
        payload['schedule']['endDate'] = (time.time() * 1000) + 20000 + 1000
        payload['schedule']['hour'] = 13
        payload['schedule']['minute'] = 1

        messageDetails = CreateMessage.create('LIVE', 'ORG', 'LOYALTY', 'MOBILE',
                                              messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)

    def test_createMessage_negative_validationMessage_recurringSchedule_weekly_without_repeatOn(self):

        payload = copy.deepcopy(self.messagePayload)
        payload['targetAudience'].update({'include': [self.listInfo['ID']]})
        payload['schedule']['scheduleType'] = 'RECURRING'
        payload['schedule']['repeatType'] = 'WEEKLY'
        payload['schedule']['startDate'] = (time.time() * 1000) + 20000
        payload['schedule']['endDate'] = (time.time() * 1000) + 20000 + 1000
        payload['schedule']['hour'] = 13
        payload['schedule']['minute'] = 1

        messageDetails = CreateMessage.create('LIVE', 'ORG', 'LOYALTY', 'MOBILE',
                                              messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        payload['targetAudience'].update({'include': [self.listInfo['ID']]})
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode=[102],
                                     expectedErrorMessage=[
                                         'Invalid request : Repeat on in reccuring schedule is required'])

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo,statusCode,errorCode,errorDescription', [
        ('LAPSED', 'ORG', 'LOYALTY', 'MOBILE',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}, 400, [3036,3038],['Campaign expired','Invalid Schedule : Message cannot end after campaign.'])
    ])
    def test_createMessage_negative_validationMessage_recurring_creatingMessage_in_lapsed_campaign(self, campaignType, testControlType,
                                                                         listType,
                                                                         channel, messageInfo,statusCode,errorCode,errorDescription):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 400, expectedErrorCode = errorCode,
                                     expectedErrorMessage = errorDescription)

    @pytest.mark.parametrize('messageInfo', [
        (
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),])

    def test_createMessage_arabic_Characters(self,messageInfo):
        payload = copy.deepcopy(self.messagePayload)
        payload['targetAudience'].update({'include': [self.listInfo['ID']]})
        payload['messageContent'][
            'message_content_id_1']['messageBody'] = 'عروض نهاية الاسبوع  {{optout}}'
        messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
                                              messageInfo=self.messageInfo,
                                              payload=payload,
                                              updateNode=True,
                                              lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        approveRespone = AuthorizeMessage.approve('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
                                                   messageCreateResponse=messageDetails,messageInfo=messageInfo)
        AuthorizeMessage.assertResponse(approveRespone, 200)
        campaignId = constant.config['node']['LIVE']['ORG']['CAMPAIGN']['ID']

        AuthorizeMessageDBAssertion(campaignId, messageDetails['RESPONSE'], payload, 'ORG').check()