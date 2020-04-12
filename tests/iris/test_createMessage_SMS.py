import pytest, time, Queue, pytest_ordering
from time import sleep
from threading import Thread
from src.Constant.constant import constant
from src.modules.iris.list import campaignList
from src.utilities.logger import Logger
from src.utilities.assertion import Assertion
from src.modules.iris.campaigns import campaigns
from src.modules.iris.message import campaignMessage
from src.modules.iris.dbCallsCampaign import dbCallsCampaign
from src.modules.iris.dbCallsMessage import dbCallsMessage
from src.modules.iris.dbCallsList import dbCallsList
from src.modules.iris.construct import construct
from src.modules.iris.coupons import coupons

@pytest.mark.run(order=8)
class Test_SMS_CreateMessage():
    
    def setup_class(self):
        Logger.logSuiteName(str(self).split('.')[-1])
        createListresponse, createListPayload, campaignId = campaignList.createList({'customTagCount':0, 'name':'IRIS_LIST_' + str(int(time.time() * 100000))}, campaignType=['LIVE', 'ORG', 'List', 'TAGS', 0])
        campaignList.assertCreateList(createListresponse, 200)
        groupVersionDetailResult, bucketId = campaignList.assertCreateListDbCalls(createListresponse['json']['entity']['listId'], createListPayload, 'ORG')
        Logger.log('GroupVersionId : {}, bucketId : {}'.format(groupVersionDetailResult, bucketId))
        addRecipientResponse, addRecipientPayload = campaignList.addRecipient({}, campaignId, createListresponse['json']['entity']['listId'], 'mobile', 10, 0)
        campaignList.assertAddRecipient(addRecipientResponse, 200)
        campaignList.assertAddRecipientDbCalls(addRecipientResponse, addRecipientPayload, createListresponse, campaignId, bucketId, {'TEST':groupVersionDetailResult.get('TEST'), 'CONTROL':groupVersionDetailResult.get('CONTROL')}, 'mobile')
        self.groupVersionResult = dbCallsList.getGroupVersionDetailsWithGroupId(createListresponse['json']['entity']['listId'])
        self.bucketId = bucketId
        responseCoupon, payloadCoupon, campaignId = coupons.createCoupons(campaignId=campaignId)
        self.strategy = construct.constructStrategyIds()
        self.programeId = self.strategy['programeId']
        self.allocationStrategyId = self.strategy['allocationStrategyId']
        self.expiryStrategyId = self.strategy['expirationStrategyId']
        self.voucherId = responseCoupon['json']['entity']['voucherSeriesId']
        self.campaignId = campaignId
        self.listId = createListresponse['json']['entity']['listId']
        campaignMessage.updateDefaultMessageJson(self.campaignId, self.listId, self.voucherId, self.strategy, self.bucketId, self.groupVersionResult)
        constant.messagesDefault['updated'] = True
        Logger.log('Using CampaignId : {} , listId : {} for Execution of Create Message'.format(self.campaignId, self.listId))
        
    def setup_method(self, method):
        Logger.logMethodName(method.__name__)
        
    def teardown_class(self):
        Logger.log('Default Object Set is :', constant.messagesDefault)
        
    @pytest.mark.parametrize('description,messageInfo', [
        ('MessageType-Immediate-Plain', ['SMS', ['IMMEDIATE'], ['PLAIN'], True]),
        ('MessageType-ParticularDate-Plain', ['SMS', ['PARTICULARDATE', int(time.time() * 1000 + 4 * 60 * 60 * 1000)], ['PLAIN'], True]),
        ])
    def test_createMessage_sms_Plain_Sanity(self, description, messageInfo):
        response, payload = campaignMessage.createMessage(self, messageInfo=messageInfo)
        campaignMessage.assertCreateMessage(response, 200)
        campaignMessage.assertCreateMessageDbCalls(response['json']['entity']['messageId'], self.campaignId, payload)
        campaignMessage.updateDefaultMessageJsonWithMessageInfoValues(messageInfo, payload, response['json']['entity']['messageId'])
        
    @pytest.mark.parametrize('description,messageInfo', [
        ('MessageType-Immediate-Plain', ['SMS', ['IMMEDIATE'], ['PLAIN'], False]),
        ('MessageType-ParticularDate-Plain', ['SMS', ['PARTICULARDATE', int(time.time() * 1000 + 4 * 60 * 60 * 1000)], ['PLAIN'], False]),
        ])
    def test_createMessage_sms_Plain_systemDefault_False(self, description, messageInfo):
        response, payload = campaignMessage.createMessage(self, messageInfo=messageInfo)
        campaignMessage.assertCreateMessage(response, 200)
        campaignMessage.assertCreateMessageDbCalls(response['json']['entity']['messageId'], self.campaignId, payload)
        campaignMessage.updateDefaultMessageJsonWithMessageInfoValues(messageInfo, payload, response['json']['entity']['messageId'])
        
    @pytest.mark.parametrize('description,messageInfo', [
        ('MessageType-Immediate-Plain', ['SMS', ['IMMEDIATE'], ['Generic'], True]),
        ('MessageType-ParticularDate-Plain', ['SMS', ['PARTICULARDATE', int(time.time() * 1000 + 4 * 60 * 60 * 1000)], ['Generic'], True]),
        ('MessageType-Immediate-Plain_systemDefault_False', ['SMS', ['IMMEDIATE'], ['Generic'], False]),
        ('MessageType-ParticularDate-Plain_systemDefault_False', ['SMS', ['PARTICULARDATE', int(time.time() * 1000 + 4 * 60 * 60 * 1000)], ['Generic'], False]),
        ])        
    def test_createMessage_sms_Generic(self, description, messageInfo):
        response, payload = campaignMessage.createMessage(self, messageInfo=messageInfo)
        campaignMessage.assertCreateMessage(response, 200)
        campaignMessage.assertCreateMessageDbCalls(response['json']['entity']['messageId'], self.campaignId, payload)
        campaignMessage.updateDefaultMessageJsonWithMessageInfoValues(messageInfo, payload, response['json']['entity']['messageId'])
        
    @pytest.mark.parametrize('description,messageInfo', [
        ('MessageType-Immediate-Plain', ['SMS', ['IMMEDIATE'], ['COUPONS'], True]),
        ('MessageType-ParticularDate-Plain', ['SMS', ['PARTICULARDATE', int(time.time() * 1000 + 4 * 60 * 60 * 1000)], ['COUPONS'], True]),
        ('MessageType-Immediate-Plain_systemDefault_False', ['SMS', ['IMMEDIATE'], ['COUPONS'], False]),
        ('MessageType-ParticularDate-Plain_systemDefault_False', ['SMS', ['PARTICULARDATE', int(time.time() * 1000 + 4 * 60 * 60 * 1000)], ['COUPONS'], False]),
        ])        
    def test_createMessage_sms_Coupon(self, description, messageInfo):
        response, payload = campaignMessage.createMessage(self, messageInfo=messageInfo)
        campaignMessage.assertCreateMessage(response, 200)
        campaignMessage.assertCreateMessageDbCalls(response['json']['entity']['messageId'], self.campaignId, payload)
        campaignMessage.updateDefaultMessageJsonWithMessageInfoValues(messageInfo, payload, response['json']['entity']['messageId'])
        
    @pytest.mark.parametrize('description,messageInfo', [
        ('MessageType-Immediate-Plain', ['SMS', ['IMMEDIATE'], ['POINTS'], True]),
        ('MessageType-ParticularDate-Plain', ['SMS', ['PARTICULARDATE', int(time.time() * 1000 + 4 * 60 * 60 * 1000)], ['POINTS'], True ]),
        ('MessageType-Immediate-Plain_systemDefault_False', ['SMS', ['IMMEDIATE'], ['POINTS'], False]),
        ('MessageType-ParticularDate-Plain_systemDefault_False', ['SMS', ['PARTICULARDATE', int(time.time() * 1000 + 4 * 60 * 60 * 1000)], ['POINTS'], False ]),
        ])        
    def test_createMessage_sms_Points(self, description, messageInfo):
        response, payload = campaignMessage.createMessage(self, messageInfo=messageInfo)
        campaignMessage.assertCreateMessage(response, 200)
        campaignMessage.assertCreateMessageDbCalls(response['json']['entity']['messageId'], self.campaignId, payload)
        campaignMessage.updateDefaultMessageJsonWithMessageInfoValues(messageInfo, payload, response['json']['entity']['messageId'])
        
    @pytest.mark.parametrize('description,messageInfo', [
        ('MessageType-Recurring-Plain', ['SMS', ['RECURRING', '14', '03', '02', '01', '10'], ['PLAIN'], False]),
        ('MessageType-Recurring-Point', ['SMS', ['RECURRING', '14', '03', '02', '01', '10'], ['POINTS'], False]),
        ('MessageType-Recurring-Plain', ['SMS', ['RECURRING', '14', '03', '02', '01', '10'], ['COUPONS'], False])
        ])
    def test_createMessage_sms_Recurring(self, description, messageInfo):
        Logger.log('Actual ListId:{} and CampaignId:{} and used for Recurring listId:{} and campaignId:{}'.format(self.listId, self.campaignId, constant.config['message_recurring']['SMS']['listId'], constant.config['message_recurring']['SMS']['campaignId']))
        actualListIdGettingUsedInAllCases = self.listId 
        actualCampaignIdGettingUsedInAllCases = self.campaignId
        actualVoucherIdGettingUsedInAllCases = self.voucherId
        try:
            self.listId = constant.config['message_recurring']['SMS']['listId']
            self.campaignId = constant.config['message_recurring']['SMS']['campaignId']
            self.voucherId = constant.config['message_recurring']['SMS']['voucherId']
            response, payload = campaignMessage.createMessage(self, messageInfo=messageInfo)
            campaignMessage.assertCreateMessage(response, 200)
            campaignMessage.assertCreateMessageDbCalls(response['json']['entity']['messageId'], self.campaignId, payload)
            campaignMessage.updateDefaultMessageJsonWithMessageInfoValues(messageInfo, payload, response['json']['entity']['messageId'])
        except AssertionError, reason:
            Assertion.constructAssertion(False, reason)
        except Exception, exp:
            Logger.log('Not Due to Assertion but Recurring Failed due to Reason :{}'.format(exp))
        finally:
            Logger.log('Finally Setting Back the Actual ListId :{} and campaignId :{}'.format(actualListIdGettingUsedInAllCases, actualCampaignIdGettingUsedInAllCases))
            self.listId = actualListIdGettingUsedInAllCases
            self.campaignId = actualCampaignIdGettingUsedInAllCases
            self.voucherId = actualVoucherIdGettingUsedInAllCases

    @pytest.mark.parametrize('description,payload,campaignIdPassed,statusCode,errorCode,errorMessage', [
        ('MessageType-Immediate-Plain-WithInvalidCampaignId', {'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}}, '0', 400, 100, ['Invalid request : must be greater than or equal to 1']),
        ('MessageType-Immediate-Plain-WithNegativeCampaignId', {'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}}, '-1234', 400, 100, ['Invalid request : must be greater than or equal to 1']),
        ('MessageType-Immediate-Plain-WithInvalidCampaignId', {'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}}, '999999999', 400, 1007, ['Campaign Id Exception : Invalid Campaign Id Passed 999999999'])
        ])
    def test_createMessage_sms_Immediate_Plain_WrongCampaignId(self, description, payload, campaignIdPassed, statusCode, errorCode, errorMessage):
        actualCampaignIdGettingUsedThroughOut = self.campaignId
        try:
            self.campaignId = campaignIdPassed
            response, payload = campaignMessage.createMessage(self, payloadData=payload)
            campaignMessage.assertCreateMessage(response, statusCode, errorCode, errorMessage)
        except AssertionError, reason:
            Assertion.constructAssertion(False, reason)
        except Exception, exp:
            Logger.log('Not Due to Assertion but Recurring Failed due to Reason :{}'.format(exp))
        finally:
            self.campaignId = actualCampaignIdGettingUsedThroughOut

    @pytest.mark.parametrize('description,payload,statusCode,errorCode,errorMessage', [
        ('MessageType-Immediate-Plain-MessageWithoutOptoutTag', {'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'message':'Hi {{first_name}} {{last_name}} {{store_id}},Sending SMS via IRIS Automation'}, 400, 100, ['Invalid request : optout tag must be present in template']),
        ('MessageType-Immediate-Plain-MessageWithVoucherTag', {'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'message':'Hi {{first_name}} {{last_name}} {{store_id}} {{voucher}} {{optout}} } ,Sending SMS via IRIS Automation'}, 400, 100, ['Invalid request : Coupons incentive should be attached to use voucher tags']),
        ('MessageType-Immediate-Plain-MessageWithPointsTag', {'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'message':'Hi {{first_name}} {{last_name}} {{store_id}} {{promotion_points}} {{optout}} } ,Sending SMS via IRIS Automation'}, 400, 100, ['Invalid request : Points incentive should be attached to use points tags'])
        ])
    def test_createMessage_sms_Immediate_Plain_MessageWithInvalidTags(self, description, payload, statusCode, errorCode, errorMessage):
        response, payload = campaignMessage.createMessage(self, payloadData=payload)
        campaignMessage.assertCreateMessage(response, statusCode, errorCode, errorMessage)

    @pytest.mark.parametrize('description,payload', [
        ('MessageType-Immediate-Plain-MessageWithStoreTypeAsLastTransactedAt', {'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'storeType':'LAST_TRANSACTED_AT', 'message':'Hi {{first_name}} {{last_name}} {{store_id}} ,Sending SMS via IRIS Automation with store id : {{store_id}} {{optout}}'})
        ])  
    def test_createMessage_sms_Immediate_Plain_MessageWithStoreTypeAsLastTransactedAt(self, description, payload):
        response, payload = campaignMessage.createMessage(self, payloadData=payload)
        campaignMessage.assertCreateMessage(response, 200)
        campaignMessage.assertCreateMessageDbCalls(response['json']['entity']['messageId'], self.campaignId, payload)

    @pytest.mark.parametrize('description,payload,statusCode,errorCode,errorMessage', [
        ('MessageType-Immediate-Plain-WithInvalidGsmSenderId', {'senderDetails':{'gsmSenderId':1122, 'useSystemDefaults':True, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}}, 400, 3006, ['Provided Sender ids are not valid']),
        ('MessageType-Immediate-Plain-WithNegativeGsmSenderId', {'senderDetails':{'gsmSenderId':-1122, 'useSystemDefaults':True, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}}, 400, 3006, ['Provided Sender ids are not valid']),
        ('MessageType-Immediate-Plain-WithInvalidCdmaSenderId', {'senderDetails':{'cdmaSenderId':1122, 'useSystemDefaults':True, 'gsmSenderId':constant.config['message_senders']['gsmSenderId']}}, 400, 3006, ['Provided Sender ids are not valid']),
        ('MessageType-Immediate-Plain-WithNegativeCdmaSenderId', {'senderDetails':{'cdmaSenderId':-1122, 'useSystemDefaults':True, 'gsmSenderId':constant.config['message_senders']['gsmSenderId']}}, 400, 3006, ['Provided Sender ids are not valid']),
        ('MessageType-Immediate-Plain-WithInvalidDomainGatewayMapId', {'senderDetails':{'domainGatewayMapId':1212, 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}}, 400, 3005, ['Domain Gateway Map with id does not exist : 1212']),
        ('MessageType-Immediate-Plain-WithNegativeDomainGatewayMapId', {'senderDetails':{'domainGatewayMapId':-1212, 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}}, 400, 3005, ['Domain Gateway Map with id does not exist : -1212']),
        ('MessageType-Immediate-Plain-WithoutPassingDomainGatewayMapId', {'senderDetails':{'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}}, 400, 3012, ['Sender Details Exception : Please provide Domain Gateway Map Id if use system defaults is false']),
        ('MessageType-Immediate-Plain-WithoutPassingGsmAndCdmaSenderId', {'senderDetails':{'useSystemDefaults':True}}, 400, 100, ['Invalid request : CDMA sender id is required', 'Invalid request : GSM sender id is required'])
        ])
    def test_createMessage_sms_Immediate_Plain_WrongSenderIds(self, description, payload, statusCode, errorCode, errorMessage):
        response, payload = campaignMessage.createMessage(self, payloadData=payload)
        campaignMessage.assertCreateMessage(response, statusCode, errorCode, errorMessage)

    @pytest.mark.parametrize('description,payload,listIdPassed,statusCode,errorCode,errorMessage', [
        ('MessageType-Immediate-Plain-WithInvalidListId', {'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}}, 1111111, 400, 3007, ['List id does not exists : 1,111,111']),
        ('MessageType-Immediate-Plain-WithNegativeListId', {'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}}, -1111111, 400, 100, ['Invalid request : Invalid list Id'])
        ])
    def test_createMessage_sms_Immediate_Plain_WithInvalidListId(self, description, payload, listIdPassed, statusCode, errorCode, errorMessage):
        actualListIdGettingUsedThroughOut = self.listId
        try:
            self.listId = listIdPassed
            response, payload = campaignMessage.createMessage(self, payloadData=payload)
            campaignMessage.assertCreateMessage(response, statusCode, errorCode, errorMessage)
        except AssertionError, reason:
            Assertion.constructAssertion(False, reason)
        except Exception, exp:
            Logger.log('Not Due to Assertion but Recurring Failed due to Reason :{}'.format(exp))
        finally:
            self.listId = actualListIdGettingUsedThroughOut

    @pytest.mark.parametrize('description,payload', [
        ('MessageType-Immediate-Plain-MessageWithTargetNdncAsTrue', {'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'message':'Hi {{first_name}} {{store_id}} https://nightly.capillary.in/campaign/v3/base/CampaignOverview#campaign/302821 {{last_name}} ,Sending SMS via IRIS Automation{{optout}}' , 'additionalInfo':{'targetNdnc':True, 'useTinyUrl':False}}),
        ('MessageType-Immediate-Plain-MessageWithTargetNdncAsFalse', {'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'message':'Hi {{first_name}} {{store_id}} https://nightly.capillary.in/campaign/v3/base/CampaignOverview#campaign/302821 {{last_name}} ,Sending SMS via IRIS Automation{{optout}}', 'additionalInfo':{'targetNdnc':False, 'useTinyUrl':True}})
        ])  
    def test_createMessage_sms_Immediate_Plain_MessageWithAdditionalInfo(self, description, payload):
        response, payload = campaignMessage.createMessage(self, payloadData=payload)
        campaignMessage.assertCreateMessage(response, 200)
        campaignMessage.assertCreateMessageDbCalls(response['json']['entity']['messageId'], self.campaignId, payload)

    @pytest.mark.parametrize('description,payload,statusCode,errorCode,errorMessage', [
        ('MessageType-Immediate-Plain-MessageWithIncorrectChannel', {'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'channel':'SM'}, 400, 103, ["Invalid type: Could not resolve type id 'SM' into a subtype of [simple type, class com.capillary.campaigns.api.data.message.MessageBody]: known type ids = [MessageBody, SMS, WECHAT]"]),
        ('MessageType-Immediate-Plain-MessageWithIncorrectSchedule', {'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'schedule':{'type':'IMMEDIATEL'}}, 400, 103, ["Invalid type: Could not resolve type id 'IMMEDIATEL' into a subtype of [simple type, class com.capillary.campaigns.api.data.message.Schedule]: known type ids = [IMMEDIATELY, PARTICULAR_DATE, RECURRING, Schedule]"]),
        ('MessageType-Immediate-Plain-MessageWithIncorrectSenderDetails', {'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':'Fals', 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}}, 400, 103, ['Invalid type: Can not construct instance of java.lang.Boolean from String value \'SMS\': only "true" or "false" recognized']),
        ('MessageType-Immediate-Plain-MessageWithIncorrectListId', {'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'senderDetails':{'listId':'null'}}, 400, 103, ['Invalid type: Unrecognized field "listId" (class com.capillary.campaigns.api.data.message.impl.sender.SmsSenderDetails), not marked as ignorable']),
        ('MessageType-Immediate-Plain-MessageWithIncorrectStoreType', {'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'storeType':'REGISTERED_STOR'}, 400, 100, ['Invalid request : Valid store type must be provided if store tags are used']),
        ('MessageType-Immediate-Plain-MessageWithIncorrectAdditionalInfo', {'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'additionalInfo':{'targetNdnc':'Fal'}}, 400, 103, ['Invalid type: Can not construct instance of boolean from String value \'SMS\': only "true" or "false" recognized'])
        ])
    def test_createMessage_sms_Immediate_Plain_WrongSchema(self, description, payload, statusCode, errorCode, errorMessage):
        response, payload = campaignMessage.createMessage(self, payloadData=payload)
        campaignMessage.assertCreateMessage(response, statusCode, errorCode, errorMessage)

    @pytest.mark.parametrize('description,payload,campaignIdPassed,statusCode,errorCode,errorMessage', [
        ('MessageType-Immediate-Generic-WithInvalidCampaignId', {'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'GENERIC', 'genericIncentiveId':1}}, '0', 400, 100, ['Invalid request : must be greater than or equal to 1']),
        ('MessageType-Immediate-Generic-WithNegativeCampaignId', {'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'GENERIC', 'genericIncentiveId':1}}, '-1234', 400, 100, ['Invalid request : must be greater than or equal to 1']),
        ('MessageType-Immediate-Generic-WithInvalidCampaignId', {'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'GENERIC', 'genericIncentiveId':1}}, '1111234', 400, 1007, ['Campaign Id Exception : Invalid Campaign Id Passed 1111234'])
        ])
    def test_createMessage_sms_Immediate_Generic_WrongCampaignId(self, description, payload, campaignIdPassed, statusCode, errorCode, errorMessage):
        actualCampaignIdGettingUsedThroughOut = self.campaignId
        try:
            self.campaignId = campaignIdPassed
            response, payload = campaignMessage.createMessage(self, payloadData=payload)
            campaignMessage.assertCreateMessage(response, statusCode, errorCode, errorMessage)
        except Exception, exp:
            Logger.log('Exception Occured as :', exp)
            raise Exception('Failed with Assertion')
        finally:
            self.campaignId = actualCampaignIdGettingUsedThroughOut

    @pytest.mark.parametrize('description,payload,statusCode,errorCode,errorMessage', [
        ('MessageType-Immediate-Generic-MessageWithoutOptoutTag', {'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'GENERIC', 'genericIncentiveId':1}, 'message':'Hi {{first_name}} {{last_name}} {{store_id}},Sending SMS via IRIS Automation'}, 400, 100, ['Invalid request : optout tag must be present in template']),
        ('MessageType-Immediate-Generic-MessageWithVoucherTag', {'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'GENERIC', 'genericIncentiveId':1}, 'message':'Hi {{first_name}} {{last_name}} {{store_id}} {{voucher}} {{optout}} } ,Sending SMS via IRIS Automation'}, 400, 100, ['Invalid request : Coupons incentive should be attached to use voucher tags']),
        ('MessageType-Immediate-Generic-MessageWithPointsTag', {'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'GENERIC', 'genericIncentiveId':1}, 'message':'Hi {{first_name}} {{last_name}} {{store_id}} {{promotion_points}} {{optout}} } ,Sending SMS via IRIS Automation'}, 400, 100, ['Invalid request : Points incentive should be attached to use points tags'])
        ])
    def test_createMessage_sms_Immediate_Generic_MessageWithInvalidTags(self, description, payload, statusCode, errorCode, errorMessage):
        response, payload = campaignMessage.createMessage(self, payloadData=payload)
        campaignMessage.assertCreateMessage(response, statusCode, errorCode, errorMessage)

    @pytest.mark.parametrize('description,payload', [
        ('MessageType-Immediate-Generic-MessageWithStoreTypeAsLastTransactedAt', {'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'GENERIC', 'genericIncentiveId':1}, 'storeType':'LAST_TRANSACTED_AT'})
        ])  
    def test_createMessage_sms_Immediate_Generic_MessageWithStoreTypeAsLastTransactedAt(self, description, payload):
        response, payload = campaignMessage.createMessage(self, payloadData=payload)
        campaignMessage.assertCreateMessage(response, 200)
        campaignMessage.assertCreateMessageDbCalls(response['json']['entity']['messageId'], self.campaignId, payload)

    @pytest.mark.parametrize('description,payload,statusCode,errorCode,errorMessage', [
        ('MessageType-Immediate-Generic-WithInvalidGsmSenderId', {'senderDetails':{'gsmSenderId':1122, 'useSystemDefaults':True, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'GENERIC', 'genericIncentiveId':1}}, 400, 3006, ['Provided Sender ids are not valid']),
        ('MessageType-Immediate-Generic-WithNegativeGsmSenderId', {'senderDetails':{'gsmSenderId':-1122, 'useSystemDefaults':True, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'GENERIC', 'genericIncentiveId':1}}, 400, 3006, ['Provided Sender ids are not valid']),
        ('MessageType-Immediate-Generic-WithInvalidCdmaSenderId', {'senderDetails':{'cdmaSenderId':1122, 'useSystemDefaults':True, 'gsmSenderId':constant.config['message_senders']['gsmSenderId']}, 'incentive':{'type':'GENERIC', 'genericIncentiveId':1}}, 400, 3006, ['Provided Sender ids are not valid']),
        ('MessageType-Immediate-Generic-WithNegativeCdmaSenderId', {'senderDetails':{'cdmaSenderId':-1122, 'useSystemDefaults':True, 'gsmSenderId':constant.config['message_senders']['gsmSenderId']}, 'incentive':{'type':'GENERIC', 'genericIncentiveId':1}}, 400, 3006, ['Provided Sender ids are not valid']),
        ('MessageType-Immediate-Generic-WithInvalidDomainGatewayMapId', {'senderDetails':{'domainGatewayMapId':1212, 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'GENERIC', 'genericIncentiveId':1}}, 400, 3005, ['Domain Gateway Map with id does not exist : 1212']),
        ('MessageType-Immediate-Generic-WithNegativeDomainGatewayMapId', {'senderDetails':{'domainGatewayMapId':-1212, 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'GENERIC', 'genericIncentiveId':1}}, 400, 3005, ['Domain Gateway Map with id does not exist : -1212']),
        ('MessageType-Immediate-Generic-WithoutPassingDomainGatewayMapId', {'senderDetails':{'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'GENERIC', 'genericIncentiveId':1}}, 400, 3012, ['Sender Details Exception : Please provide Domain Gateway Map Id if use system defaults is false']),
        ('MessageType-Immediate-Generic-WithoutPassingGsmAndCdmaSenderId', {'senderDetails':{'useSystemDefaults':True}}, 400, 100, ['Invalid request : CDMA sender id is required', 'Invalid request : GSM sender id is required'])
        ])
    def test_createMessage_sms_Immediate_Generic_WrongSenderIds(self, description, payload, statusCode, errorCode, errorMessage):
        response, payload = campaignMessage.createMessage(self, payloadData=payload)
        campaignMessage.assertCreateMessage(response, statusCode, errorCode, errorMessage)

    @pytest.mark.parametrize('description,payload,listIdPassed,statusCode,errorCode,errorMessage', [
        ('MessageType-Immediate-Generic-WithInvalidListId', {'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'GENERIC', 'genericIncentiveId':1}}, 1111111, 400, 3007, ['List id does not exists : 1,111,111']),
        ('MessageType-Immediate-Generic-WithNegativeListId', {'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'GENERIC', 'genericIncentiveId':1}}, -1111111, 400, 100, ['Invalid request : Invalid list Id'])
        ])
    def test_createMessage_sms_Immediate_Generic_WithInvalidListId(self, description, payload, listIdPassed, statusCode, errorCode, errorMessage):
        actualListIdGettingUsedThroughOut = self.listId
        try:
            self.listId = listIdPassed
            response, payload = campaignMessage.createMessage(self, payloadData=payload)
            campaignMessage.assertCreateMessage(response, statusCode, errorCode, errorMessage)
        except AssertionError, reason:
            Assertion.constructAssertion(False, reason)
        except Exception, exp:
            Logger.log('Not Due to Assertion but Recurring Failed due to Reason :{}'.format(exp))
        finally:
            self.listId = actualListIdGettingUsedThroughOut

    @pytest.mark.parametrize('description,payload', [
        ('MessageType-Immediate-Generic-MessageWithTargetNdncAsTrue', {'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'GENERIC', 'genericIncentiveId':1}, 'message':'Hi {{first_name}} https://nightly.capillary.in/campaign/v3/base/CampaignOverview#campaign/302821 {{last_name}}{{store_id}} ,Sending SMS via IRIS Automation{{optout}}', 'additionalInfo':{'targetNdnc':True, 'useTinyUrl':False}}),
        ('MessageType-Immediate-Generic-MessageWithTargetNdncAsTrue', {'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'GENERIC', 'genericIncentiveId':1}, 'message':'Hi {{first_name}} https://nightly.capillary.in/campaign/v3/base/CampaignOverview#campaign/302821 {{last_name}}{{store_id}} ,Sending SMS via IRIS Automation{{optout}}', 'additionalInfo':{'targetNdnc':False, 'useTinyUrl':True}})
        ])  
    def test_createMessage_sms_Immediate_Generic_MessageWithAdditionalInfo(self, description, payload):
        response, payload = campaignMessage.createMessage(self, payloadData=payload)
        campaignMessage.assertCreateMessage(response, 200)
        campaignMessage.assertCreateMessageDbCalls(response['json']['entity']['messageId'], self.campaignId, payload)

    @pytest.mark.parametrize('description,payload,statusCode,errorCode,errorMessage', [
        ('MessageType-Immediate-Generic-MessageWithIncorrectChannel', {'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'GENERIC', 'genericIncentiveId':1}, 'channel':'SM'}, 400, 103, ['Invalid type: Could not resolve type id \'SM\' into a subtype of [simple type, class com.capillary.campaigns.api.data.message.MessageBody]: known type ids = [MessageBody, SMS, WECHAT]']),
        ('MessageType-Immediate-Generic-MessageWithIncorrectSchedule', {'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'GENERIC', 'genericIncentiveId':1}, 'schedule':{'type':'IMMEDIATEL'}}, 400, 103, ['Invalid type: Could not resolve type id \'IMMEDIATEL\' into a subtype of [simple type, class com.capillary.campaigns.api.data.message.Schedule]: known type ids = [IMMEDIATELY, PARTICULAR_DATE, RECURRING, Schedule]']),
        ('MessageType-Immediate-Generic-MessageWithIncorrectSenderDetails', {'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':'Fals', 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'GENERIC', 'genericIncentiveId':1}}, 400, 103, ['Invalid type: Can not construct instance of java.lang.Boolean from String value \'SMS\': only "true" or "false" recognized']),
        ('MessageType-Immediate-Generic-MessageWithIncorrectStoreType', {'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'GENERIC', 'genericIncentiveId':1}, 'storeType':'REGISTERED_STOR'}, 400, 100, ['Invalid request : Valid store type must be provided if store tags are used']),
        ('MessageType-Immediate-Generic-MessageWithIncorrectAdditionalInfo', {'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'GENERIC', 'genericIncentiveId':1}, 'additionalInfo':{'targetNdnc':'Fal'}}, 400, 103, ['Invalid type: Can not construct instance of boolean from String value \'SMS\': only "true" or "false" recognized'])
        ])
    def test_createMessage_sms_Immediate_Generic_WrongSchema(self, description, payload, statusCode, errorCode, errorMessage):
        response, payload = campaignMessage.createMessage(self, payloadData=payload)
        campaignMessage.assertCreateMessage(response, statusCode, errorCode, errorMessage)

    def test_createMessage_sms_Immediate_Generic_invalidListId(self):
        payload = {'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'GENERIC', 'genericIncentiveId':1}, 'schedule':{'type':'IMMEDIATELY'}, 'listId':99999}
        actuallistIdGettingUsedThroughOut = self.listId
        try:
            self.listId = payload['listId']
            response, payload = campaignMessage.createMessage(self, payloadData=payload)
            campaignMessage.assertCreateMessage(response, 400, 3007, 'List id does not exists : 99,999')
        except AssertionError, reason:
            Assertion.constructAssertion(False, reason)
        except Exception, exp:
            Logger.log('Not Due to Assertion but Case Failed due to Reason :{}'.format(exp))
        finally:
            self.listId = actuallistIdGettingUsedThroughOut

    
    @pytest.mark.parametrize('description,payload,campaignIdPassed,statusCode,errorCode,errorMessage', [
        ('MessageType-Immediate-Coupon-WithInvalidCampaignId', {'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'COUPONS', 'voucherSeriesId':0}}, '0', 400, 100, ['Invalid request : must be greater than or equal to 1']),
        ('MessageType-Immediate-Coupon-WithNegativeCampaignId', {'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'COUPONS', 'voucherSeriesId':0}}, '-1234', 400, 100, ['Invalid request : must be greater than or equal to 1']),
        ('MessageType-Immediate-Coupon-WithInvalidCampaignId', {'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'COUPONS', 'voucherSeriesId':0}}, '1111234', 400, 1007, ['Campaign Id Exception : Invalid Campaign Id Passed 1111234'])
        ])
    def test_createMessage_sms_Immediate_Coupon_WrongCampaignId(self, description, payload, campaignIdPassed, statusCode, errorCode, errorMessage):
        payload.update({'incentive':{'type':'COUPONS', 'voucherSeriesId':self.voucherId}})
        actualCampaignIdGettingUsedThroughOut = self.campaignId
        try:
            self.campaignId = campaignIdPassed
            response, payload = campaignMessage.createMessage(self, payloadData=payload)
            campaignMessage.assertCreateMessage(response, statusCode, errorCode, errorMessage)
        except AssertionError, reason:
            Assertion.constructAssertion(False, reason)
        except Exception, exp:
            Logger.log('Not Due to Assertion but Case Failed due to Reason :{}'.format(exp))
        finally:
            self.campaignId = actualCampaignIdGettingUsedThroughOut

    @pytest.mark.parametrize('description,payload,statusCode,errorCode,errorMessage', [
        ('MessageType-Immediate-Coupon-MessageWithoutOptoutTag', {'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'COUPONS', 'voucherSeriesId':0}, 'message':'Hi {{first_name}} {{last_name}} {{store_id}} ,Sending SMS via IRIS Automation'}, 400, 100, ['Invalid request : optout tag must be present in template']),
        ('MessageType-Immediate-Coupon-MessageWithPointsTag', {'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'COUPONS', 'voucherSeriesId':0}, 'message':'Hi {{first_name}} {{last_name}} {{store_id}} {{promotion_points}} {{optout}} } ,Sending SMS via IRIS Automation'}, 400, 100, 'Invalid request : Points incentive should be attached to use points tags')
        ])
    def test_createMessage_sms_Immediate_Coupon_MessageWithInvalidTags(self, description, payload, statusCode, errorCode, errorMessage):
        payload.update({'incentive':{'type':'COUPONS', 'voucherSeriesId':self.voucherId}})
        response, payload = campaignMessage.createMessage(self, payloadData=payload)
        campaignMessage.assertCreateMessage(response, statusCode, errorCode, errorMessage)

    @pytest.mark.parametrize('description,payload', [
        ('MessageType-Immediate-Coupon-MessageWithStoreTypeAsLastTransactedAt', {'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'COUPONS', 'voucherSeriesId':0}, 'storeType':'LAST_TRANSACTED_AT'})
        ])  
    def test_createMessage_sms_Immediate_Coupon_MessageWithStoreTypeAsLastTransactedAt(self, description, payload):
        payload.update({'incentive':{'type':'COUPONS', 'voucherSeriesId':self.voucherId}})
        response, payload = campaignMessage.createMessage(self, payloadData=payload)
        campaignMessage.assertCreateMessage(response, 200)
        campaignMessage.assertCreateMessageDbCalls(response['json']['entity']['messageId'], self.campaignId, payload)

    @pytest.mark.parametrize('description,payload,statusCode,errorCode,errorMessage', [
        ('MessageType-Immediate-Coupon-WithInvalidGsmSenderId', {'senderDetails':{'gsmSenderId':1122, 'useSystemDefaults':True, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'COUPONS', 'voucherSeriesId':0}}, 400, 3006, ['Provided Sender ids are not valid']),
        ('MessageType-Immediate-Coupon-WithNegativeGsmSenderId', {'senderDetails':{'gsmSenderId':-1122, 'useSystemDefaults':True, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'COUPONS', 'voucherSeriesId':0}}, 400, 3006, ['Provided Sender ids are not valid']),
        ('MessageType-Immediate-Coupon-WithInvalidCdmaSenderId', {'senderDetails':{'cdmaSenderId':1122, 'useSystemDefaults':True, 'gsmSenderId':constant.config['message_senders']['gsmSenderId']}, 'incentive':{'type':'COUPONS', 'voucherSeriesId':0}}, 400, 3006, ['Provided Sender ids are not valid']),
        ('MessageType-Immediate-Coupon-WithNegativeCdmaSenderId', {'senderDetails':{'cdmaSenderId':-1122, 'useSystemDefaults':True, 'gsmSenderId':constant.config['message_senders']['gsmSenderId']}, 'incentive':{'type':'COUPONS', 'voucherSeriesId':0}}, 400, 3006, ['Provided Sender ids are not valid']),
        ('MessageType-Immediate-Coupon-WithInvalidDomainGatewayMapId', {'senderDetails':{'domainGatewayMapId':1212, 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'COUPONS', 'voucherSeriesId':0}}, 400, 3005, ['Domain Gateway Map with id does not exist : 1212']),
        ('MessageType-Immediate-Coupon-WithNegativeDomainGatewayMapId', {'senderDetails':{'domainGatewayMapId':-1212, 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'COUPONS', 'voucherSeriesId':0}}, 400, 3005, ['Domain Gateway Map with id does not exist : -1212']),
        ('MessageType-Immediate-Coupon-WithoutPassingDomainGatewayMapId', {'senderDetails':{'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'COUPONS', 'voucherSeriesId':0}}, 400, 3012, ['Sender Details Exception : Please provide Domain Gateway Map Id if use system defaults is false']),
        ('MessageType-Immediate-Coupon-WithoutPassingGsmAndCdmaSenderId', {'senderDetails':{'useSystemDefaults':True}}, 400, 100, ['Invalid request : CDMA sender id is required', 'Invalid request : GSM sender id is required'])
        ])
    def test_createMessage_sms_Immediate_Coupon_WrongSenderIds(self, description, payload, statusCode, errorCode, errorMessage):
        payload.update({'incentive':{'type':'COUPONS', 'voucherSeriesId':self.voucherId}})
        response, payload = campaignMessage.createMessage(self, payloadData=payload)
        campaignMessage.assertCreateMessage(response, statusCode, errorCode, errorMessage)

    @pytest.mark.parametrize('description,payload,listIdPassed,statusCode,errorCode,errorMessage', [
        ('MessageType-Immediate-Coupon-WithInvalidListId', {'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'COUPONS', 'voucherSeriesId':0}}, 1111111, 400, 3007, ['List id does not exists : 1,111,111']),
        ('MessageType-Immediate-Coupon-WithNegativeListId', {'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'COUPONS', 'voucherSeriesId':0}}, -1111111, 400, 100, ['Invalid request : Invalid list Id'])
        ])
    def test_createMessage_sms_Immediate_Coupon_WithInvalidListId(self, description, payload, listIdPassed, statusCode, errorCode, errorMessage):
        payload.update({'incentive':{'type':'COUPONS', 'voucherSeriesId':self.voucherId}})
        actualListIdGettingUsedThroughOut = self.listId
        try:
            self.listId = listIdPassed
            response, payload = campaignMessage.createMessage(self, payloadData=payload)
            campaignMessage.assertCreateMessage(response, statusCode, errorCode, errorMessage)
        except AssertionError, reason:
            Assertion.constructAssertion(False, reason)
        except Exception, exp:
            Logger.log('Not Due to Assertion but Recurring Failed due to Reason :{}'.format(exp))
        finally:
            self.listId = actualListIdGettingUsedThroughOut

    @pytest.mark.parametrize('description,payload', [
        ('MessageType-Immediate-Coupon-MessageWithTargetNdncAsTrue', {'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'COUPONS', 'voucherSeriesId':0}, 'message':'Hi {{first_name}} {{store_id}}https://nightly.capillary.in/campaign/v3/base/CampaignOverview#campaign/302821 {{last_name}} ,Sending SMS via IRIS Automation{{optout}}', 'additionalInfo':{'targetNdnc':True, 'useTinyUrl':False}}),
        ('MessageType-Immediate-Coupon-MessageWithTargetNdncAsTrue', {'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'COUPONS', 'voucherSeriesId':0}, 'message':'Hi {{first_name}} {{store_id}}https://nightly.capillary.in/campaign/v3/base/CampaignOverview#campaign/302821 {{last_name}} ,Sending SMS via IRIS Automation{{optout}}', 'additionalInfo':{'targetNdnc':False, 'useTinyUrl':True}})
        ])  
    def test_createMessage_sms_Immediate_Coupon_MessageWithAdditionalInfo(self, description, payload):
        payload.update({'incentive':{'type':'COUPONS', 'voucherSeriesId':self.voucherId}})
        response, payload = campaignMessage.createMessage(self, payloadData=payload)
        campaignMessage.assertCreateMessage(response, 200)
        campaignMessage.assertCreateMessageDbCalls(response['json']['entity']['messageId'], self.campaignId, payload)

    @pytest.mark.parametrize('description,payload,statusCode,errorCode,errorMessage', [
        ('MessageType-Immediate-Coupon-MessageWithIncorrectChannel', {'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'COUPONS', 'voucherSeriesId':0}, 'channel':'SM'}, 400, 103, ['Invalid type: Could not resolve type id \'SM\' into a subtype of [simple type, class com.capillary.campaigns.api.data.message.MessageBody]: known type ids = [MessageBody, SMS, WECHAT]']),
        ('MessageType-Immediate-Coupon-MessageWithIncorrectSchedule', {'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'COUPONS', 'voucherSeriesId':0}, 'schedule':{'type':'IMMEDIATEL'}}, 400, 103, ['Invalid type: Could not resolve type id \'IMMEDIATEL\' into a subtype of [simple type, class com.capillary.campaigns.api.data.message.Schedule]: known type ids = [IMMEDIATELY, PARTICULAR_DATE, RECURRING, Schedule]']),
        ('MessageType-Immediate-Coupon-MessageWithIncorrectSenderDetails', {'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':'Fals', 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'COUPONS', 'voucherSeriesId':0}}, 400, 103, ['Invalid type: Can not construct instance of java.lang.Boolean from String value \'SMS\': only "true" or "false" recognized']),
        ('MessageType-Immediate-Coupon-MessageWithIncorrectListId', {'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'COUPONS', 'voucherSeriesId':0}, 'senderDetails':{'listId':'null'}}, 400, 103, ['Invalid type: Unrecognized field "listId" (class com.capillary.campaigns.api.data.message.impl.sender.SmsSenderDetails), not marked as ignorable']),
        ('MessageType-Immediate-Coupon-MessageWithIncorrectStoreType', {'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'COUPONS', 'voucherSeriesId':0}, 'storeType':'REGISTERED_STOR'}, 400, 100, ['Invalid request : Valid store type must be provided if store tags are used']),
        ('MessageType-Immediate-Coupon-MessageWithIncorrectAdditionalInfo', {'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'COUPONS', 'voucherSeriesId':0}, 'additionalInfo':{'targetNdnc':'Fal'}}, 400, 103, ['Invalid type: Can not construct instance of boolean from String value \'SMS\': only "true" or "false" recognized'])
        ])
    def test_createMessage_sms_Immediate_Coupon_WrongSchema(self, description, payload, statusCode, errorCode, errorMessage):
        payload.update({'incentive':{'type':'COUPONS', 'voucherSeriesId':self.voucherId}})
        response, payload = campaignMessage.createMessage(self, payloadData=payload)
        campaignMessage.assertCreateMessage(response, statusCode, errorCode, errorMessage)

    @pytest.mark.parametrize('description,payload,campaignIdPassed,statusCode,errorCode,errorMessage', [
        ('MessageType-Immediate-Points-WithInvalidCampaignId', {'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'POINTS', 'programId':0, 'allocationStrategyId':0, 'expirationStrategyId':0}}, '0', 400, 100, ['Invalid request : must be greater than or equal to 1']),
        ('MessageType-Immediate-Points-WithNegativeCampaignId', {'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'POINTS', 'programId':0, 'allocationStrategyId':0, 'expirationStrategyId':0}}, '-1234', 400, 100, ['Invalid request : must be greater than or equal to 1']),
        ('MessageType-Immediate-Points-WithInvalidCampaignId', {'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'POINTS', 'programId':0, 'allocationStrategyId':0, 'expirationStrategyId':0}}, '1111234', 400, 1007, ['Campaign Id Exception : Invalid Campaign Id Passed 1111234'])
        ])
    def test_createMessage_sms_Immediate_Points_WrongCampaignId(self, description, payload, campaignIdPassed, statusCode, errorCode, errorMessage):
        payload.update({'incentive':{'type':'POINTS', 'programId':self.programeId, 'allocationStrategyId':self.allocationStrategyId, 'expirationStrategyId':self.expiryStrategyId}})
        actualCampaignIdGettingUsedThroughOut = self.campaignId
        try:
            self.campaignId = campaignIdPassed
            response, payload = campaignMessage.createMessage(self, payloadData=payload)
            campaignMessage.assertCreateMessage(response, statusCode, errorCode, errorMessage)
        except AssertionError, reason:
            Assertion.constructAssertion(False, reason)
        except Exception, exp:
            Logger.log('Not Due to Assertion but Recurring Failed due to Reason :{}'.format(exp))
        finally:
            self.campaignId = actualCampaignIdGettingUsedThroughOut

    @pytest.mark.parametrize('description,payload,statusCode,errorCode,errorMessage', [
        ('MessageType-Immediate-Points-MessageWithoutOptoutTag', {'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'POINTS', 'programId':0, 'allocationStrategyId':0, 'expirationStrategyId':0}, 'message':'Hi {{first_name}} {{store_id}} {{last_name}} ,Sending SMS via IRIS Automation'}, 400, 100, ['Invalid request : optout tag must be present in template']),
        ('MessageType-Immediate-Plain-MessageWithVoucherTag', {'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'message':'Hi {{first_name}} {{last_name}} {{store_id}} {{voucher}} {{optout}} } ,Sending SMS via IRIS Automation'}, 400, 100, ['Invalid request : Coupons incentive should be attached to use voucher tags']),
        ])
    def test_createMessage_sms_Immediate_Points_MessageWithInvalidTags(self, description, payload, statusCode, errorCode, errorMessage):
        payload.update({'incentive':{'type':'POINTS', 'programId':self.programeId, 'allocationStrategyId':self.allocationStrategyId, 'expirationStrategyId':self.expiryStrategyId}})
        response, payload = campaignMessage.createMessage(self, payloadData=payload)
        campaignMessage.assertCreateMessage(response, statusCode, errorCode, errorMessage)

    @pytest.mark.parametrize('description,payload', [
        ('MessageType-Immediate-Points-MessageWithStoreTypeAsLastTransactedAt', {'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'POINTS', 'programId':0, 'allocationStrategyId':0, 'expirationStrategyId':0}, 'storeType':'LAST_TRANSACTED_AT'})
        ])  
    def test_createMessage_sms_Immediate_Points_MessageWithStoreTypeAsLastTransactedAt(self, description, payload):
        payload.update({'incentive':{'type':'POINTS', 'programId':self.programeId, 'allocationStrategyId':self.allocationStrategyId, 'expirationStrategyId':self.expiryStrategyId}})
        response, payload = campaignMessage.createMessage(self, payloadData=payload)
        campaignMessage.assertCreateMessage(response, 200)
        campaignMessage.assertCreateMessageDbCalls(response['json']['entity']['messageId'], self.campaignId, payload)

    @pytest.mark.parametrize('description,payload,statusCode,errorCode,errorMessage', [
        ('MessageType-Immediate-Points-WithInvalidGsmSenderId', {'senderDetails':{'gsmSenderId':1122, 'useSystemDefaults':True, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'POINTS', 'programId':0, 'allocationStrategyId':0, 'expirationStrategyId':0}}, 400, 3006, ['Provided Sender ids are not valid']),
        ('MessageType-Immediate-Points-WithNegativeGsmSenderId', {'senderDetails':{'gsmSenderId':-1122, 'useSystemDefaults':True, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'POINTS', 'programId':0, 'allocationStrategyId':0, 'expirationStrategyId':0}}, 400, 3006, ['Provided Sender ids are not valid']),
        ('MessageType-Immediate-Points-WithInvalidCdmaSenderId', {'senderDetails':{'cdmaSenderId':1122, 'useSystemDefaults':True, 'gsmSenderId':constant.config['message_senders']['gsmSenderId']}, 'incentive':{'type':'POINTS', 'programId':0, 'allocationStrategyId':0, 'expirationStrategyId':0}}, 400, 3006, ['Provided Sender ids are not valid']),
        ('MessageType-Immediate-Points-WithNegativeCdmaSenderId', {'senderDetails':{'cdmaSenderId':-1122, 'useSystemDefaults':True, 'gsmSenderId':constant.config['message_senders']['gsmSenderId']}, 'incentive':{'type':'POINTS', 'programId':0, 'allocationStrategyId':0, 'expirationStrategyId':0}}, 400, 3006, ['Provided Sender ids are not valid']),
        ('MessageType-Immediate-Points-WithInvalidDomainGatewayMapId', {'senderDetails':{'domainGatewayMapId':1212, 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'POINTS', 'programId':0, 'allocationStrategyId':0, 'expirationStrategyId':0}}, 400, 3005, ['Domain Gateway Map with id does not exist : 1212']),
        ('MessageType-Immediate-Points-WithNegativeDomainGatewayMapId', {'senderDetails':{'domainGatewayMapId':-1212, 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'POINTS', 'programId':0, 'allocationStrategyId':0, 'expirationStrategyId':0}}, 400, 3005, ['Domain Gateway Map with id does not exist : -1212']),
        ('MessageType-Immediate-Points-WithoutPassingDomainGatewayMapId', {'senderDetails':{'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'POINTS', 'programId':0, 'allocationStrategyId':0, 'expirationStrategyId':0}}, 400, 3012, ['Sender Details Exception : Please provide Domain Gateway Map Id if use system defaults is false']),
        ('MessageType-Immediate-Points-WithoutPassingGsmAndCdmaSenderId', {'senderDetails':{'useSystemDefaults':True}}, 400, 100, ['Invalid request : CDMA sender id is required', 'Invalid request : GSM sender id is required'])
        ])
    def test_createMessage_sms_Immediate_Points_WrongSenderIds(self, description, payload, statusCode, errorCode, errorMessage):
        payload.update({'incentive':{'type':'POINTS', 'programId':self.programeId, 'allocationStrategyId':self.allocationStrategyId, 'expirationStrategyId':self.expiryStrategyId}})
        response, payload = campaignMessage.createMessage(self, payloadData=payload)
        campaignMessage.assertCreateMessage(response, statusCode, errorCode, errorMessage)

    @pytest.mark.parametrize('description,payload,listIdPassed,statusCode,errorCode,errorMessage', [
        ('MessageType-Immediate-Points-WithInvalidListId', {'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'POINTS', 'programId':0, 'allocationStrategyId':0, 'expirationStrategyId':0}}, 1111111, 400, 3007, ['List id does not exists : 1,111,111']),
        ('MessageType-Immediate-Points-WithNegativeListId', {'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'POINTS', 'programId':0, 'allocationStrategyId':0, 'expirationStrategyId':0}}, -1111111, 400, 100, ['Invalid request : Invalid list Id'])
        ])
    def test_createMessage_sms_Immediate_Points_WithInvalidListId(self, description, payload, listIdPassed, statusCode, errorCode, errorMessage):
        payload.update({'incentive':{'type':'POINTS', 'programId':self.programeId, 'allocationStrategyId':self.allocationStrategyId, 'expirationStrategyId':self.expiryStrategyId}})
        actualListIdGettingUsedThroughOut = self.listId
        try:
            self.listId = listIdPassed
            response, payload = campaignMessage.createMessage(self, payloadData=payload)
            campaignMessage.assertCreateMessage(response, statusCode, errorCode, errorMessage)
        except AssertionError, reason:
            Assertion.constructAssertion(False, reason)
        except Exception, exp:
            Logger.log('Not Due to Assertion but Recurring Failed due to Reason :{}'.format(exp))
        finally:
            self.listId = actualListIdGettingUsedThroughOut

    @pytest.mark.parametrize('description,payload', [
        ('MessageType-Immediate-Points-MessageWithTargetNdncAsTrue', {'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'POINTS', 'programId':0, 'allocationStrategyId':0, 'expirationStrategyId':0}, 'message':'Hi Buddy , only passing store tag :{{store_id}} {{optout}}', 'additionalInfo':{'targetNdnc':True, 'useTinyUrl':False}}),
        ('MessageType-Immediate-Points-MessageWithTargetNdncAsTrue', {'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'POINTS', 'programId':0, 'allocationStrategyId':0, 'expirationStrategyId':0}, 'message':'Hi {{first_name}} https://nightly.capillary.in/campaign/v3/base/CampaignOverview#campaign/302821 {{last_name}} {{store_id}} ,Sending SMS via IRIS Automation{{optout}}', 'additionalInfo':{'targetNdnc':False, 'useTinyUrl':True}})
        ])  
    def test_createMessage_sms_Immediate_Points_MessageWithAdditionalInfo(self, description, payload):
        payload.update({'incentive':{'type':'POINTS', 'programId':self.programeId, 'allocationStrategyId':self.allocationStrategyId, 'expirationStrategyId':self.expiryStrategyId}})
        response, payload = campaignMessage.createMessage(self, payloadData=payload)
        campaignMessage.assertCreateMessage(response, 200)
        campaignMessage.assertCreateMessageDbCalls(response['json']['entity']['messageId'], self.campaignId, payload)

    @pytest.mark.parametrize('description,payload,statusCode,errorCode,errorMessage', [
        ('MessageType-Immediate-Points-MessageWithIncorrectChannel', {'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'POINTS', 'programId':0, 'allocationStrategyId':0, 'expirationStrategyId':0}, 'channel':'SM'}, 400, 103, ['Invalid type: Could not resolve type id \'SM\' into a subtype of [simple type, class com.capillary.campaigns.api.data.message.MessageBody]: known type ids = [MessageBody, SMS, WECHAT]']),
        ('MessageType-Immediate-Points-MessageWithIncorrectSchedule', {'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'POINTS', 'programId':0, 'allocationStrategyId':0, 'expirationStrategyId':0}, 'schedule':{'type':'IMMEDIATEL'}}, 400, 103, ['Invalid type: Could not resolve type id \'IMMEDIATEL\' into a subtype of [simple type, class com.capillary.campaigns.api.data.message.Schedule]: known type ids = [IMMEDIATELY, PARTICULAR_DATE, RECURRING, Schedule]']),
        ('MessageType-Immediate-Points-MessageWithIncorrectSenderDetails', {'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':'Fals', 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'POINTS', 'programId':0, 'allocationStrategyId':0, 'expirationStrategyId':0}}, 400, 103, ['Invalid type: Can not construct instance of java.lang.Boolean from String value \'SMS\': only "true" or "false" recognized']),
        ('MessageType-Immediate-Points-MessageWithIncorrectListId', {'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'POINTS', 'programId':0, 'allocationStrategyId':0, 'expirationStrategyId':0}, 'senderDetails':{'listId':'null'}}, 400, 103, ['Invalid type: Unrecognized field "listId" (class com.capillary.campaigns.api.data.message.impl.sender.SmsSenderDetails), not marked as ignorable']),
        ('MessageType-Immediate-Points-MessageWithIncorrectStoreType', {'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'POINTS', 'programId':0, 'allocationStrategyId':0, 'expirationStrategyId':0}, 'storeType':'REGISTERED_STOR'}, 400, 100, ['Invalid request : Valid store type must be provided if store tags are used']),
        ('MessageType-Immediate-Points-MessageWithIncorrectAdditionalInfo', {'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'POINTS', 'programId':0, 'allocationStrategyId':0, 'expirationStrategyId':0}, 'additionalInfo':{'targetNdnc':'Fal'}}, 400, 103, ['Invalid type: Can not construct instance of boolean from String value \'SMS\': only "true" or "false" recognized'])
        ])
    def test_createMessage_sms_Immediate_Points_WrongSchema(self, description, payload, statusCode, errorCode, errorMessage):
        payload.update({'incentive':{'type':'POINTS', 'programId':self.programeId, 'allocationStrategyId':self.allocationStrategyId, 'expirationStrategyId':self.expiryStrategyId}})
        response, payload = campaignMessage.createMessage(self, payloadData=payload)
        campaignMessage.assertCreateMessage(response, statusCode, errorCode, errorMessage)

    @pytest.mark.parametrize('description,payload,campaignIdPassed,statusCode,errorCode,errorMessage', [
        ('MessageType-ParticularDate-Plain-WithInvalidCampaignId', {'schedule':{'type':'PARTICULAR_DATE', 'datetime':int(time.time() * 1000 + 10 * 60 * 60 * 1000)}, 'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}}, '0', 400, 100, ['Invalid request : must be greater than or equal to 1']),
        ('MessageType-ParticularDate-Plain-WithNegativeCampaignId', {'schedule':{'type':'PARTICULAR_DATE', 'datetime':int(time.time() * 1000 + 10 * 60 * 60 * 1000)}, 'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}}, '-1234', 400, 100, ['Invalid request : must be greater than or equal to 1']),
        ('MessageType-ParticularDate-Plain-WithInvalidCampaignId', {'schedule':{'type':'PARTICULAR_DATE', 'datetime':int(time.time() * 1000 + 10 * 60 * 60 * 1000)}, 'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}}, '1111234', 400, 1007, ['Campaign Id Exception : Invalid Campaign Id Passed 1111234'])
        ])
    def test_createMessage_sms_ParticularDate_Plain_WrongCampaignId(self, description, payload, campaignIdPassed, statusCode, errorCode, errorMessage):
        actualCampaignIdGettingUsedThroughOut = self.campaignId
        try:
            self.campaignId = campaignIdPassed
            response, payload = campaignMessage.createMessage(self, payloadData=payload)
            campaignMessage.assertCreateMessage(response, statusCode, errorCode, errorMessage)
        except AssertionError, reason:
            Assertion.constructAssertion(False, reason)
        except Exception, exp:
            Logger.log('Not Due to Assertion but Recurring Failed due to Reason :{}'.format(exp))
        finally:
            self.campaignId = actualCampaignIdGettingUsedThroughOut

    @pytest.mark.parametrize('description,messageInfo,voucherSeriesIdPassed, statusCode, errorCode, errorMessage', [
        ('MessageType-Immediate-Plain-InvalidVoucherId', ['SMS', ['IMMEDIATE'], ['COUPONS'], False], '0', 400, 100, ['Invalid request : Invalid voucher series id is used while using voucher tags']),
        ('MessageType-Immediate-Plain-NegativeVoucherId', ['SMS', ['IMMEDIATE'], ['COUPONS'], False], '-1234', 400, 100, ['Invalid request : Invalid voucher series id is used while using voucher tags']),
        ('MessageType-Immediate-Plain-InvalidVoucherId', ['SMS', ['IMMEDIATE'], ['COUPONS'], False], '999999999', 400, 3002, ['Voucher series id not found : 999999999'])
    ])
    def test_createMessage_sms_Immediate_Coupons_MessageWithInvalidVoucherId(self, description, messageInfo, voucherSeriesIdPassed, statusCode, errorCode, errorMessage):
        actualVoucherIdGettingUsedThroughOut = self.voucherId
        try:
            self.voucherId = voucherSeriesIdPassed
            response = campaignMessage.createMessage(self, messageInfo=messageInfo)[0]
            campaignMessage.assertCreateMessage(response, statusCode, errorCode, errorMessage)
        except AssertionError, reason:
            Assertion.constructAssertion(False, reason)
        except Exception, exp:
            Assertion.constructAssertion(False, 'Not Due to Assertion but Recurring Failed due to Reason :{}'.format(exp))
        finally:
            self.voucherId = actualVoucherIdGettingUsedThroughOut

    @pytest.mark.parametrize('description,payload,statusCode,errorCode,errorMessage', [
        ('MessageType-ParticularDate-Plain-MessageWithoutOptoutTag', {'schedule':{'type':'PARTICULAR_DATE', 'datetime':int(time.time() * 1000 + 10 * 60 * 60 * 1000)}, 'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'message':'Hi {{first_name}} {{store_id}} {{last_name}} ,Sending SMS via IRIS Automation'}, 400, 100, ['Invalid request : optout tag must be present in template']),
        ('MessageType-ParticularDate-Plain-MessageWithVoucherTag', {'schedule':{'type':'PARTICULAR_DATE', 'datetime':int(time.time() * 1000 + 10 * 60 * 60 * 1000)}, 'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'message':'Hi {{first_name}} {{last_name}} {{store_id}} {{voucher}} {{optout}} } ,Sending SMS via IRIS Automation'}, 400, 100, ['Invalid request : Coupons incentive should be attached to use voucher tags']),
        ('MessageType-ParticularDate-Plain-MessageWithPointsTag', {'schedule':{'type':'PARTICULAR_DATE', 'datetime':int(time.time() * 1000 + 10 * 60 * 60 * 1000)}, 'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'message':'Hi {{first_name}} {{last_name}} {{store_id}} {{promotion_points}} {{optout}} } ,Sending SMS via IRIS Automation'}, 400, 100, 'Invalid request : Points incentive should be attached to use points tags')
        ])
    def test_createMessage_sms_ParticularDate_Plain_MessageWithInvalidTags(self, description, payload, statusCode, errorCode, errorMessage):
        response, payload = campaignMessage.createMessage(self, payloadData=payload)
        campaignMessage.assertCreateMessage(response, statusCode, errorCode, errorMessage)

    @pytest.mark.parametrize('description,payload', [
        ('MessageType-ParticularDate-Plain-MessageWithStoreTypeAsLastTransactedAt', {'schedule':{'type':'PARTICULAR_DATE', 'datetime':int(time.time() * 1000 + 10 * 60 * 60 * 1000)}, 'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'storeType':'LAST_TRANSACTED_AT'})
        ])  
    def test_createMessage_sms_ParticularDate_Plain_MessageWithStoreTypeAsLastTransactedAt(self, description, payload):
        response, payload = campaignMessage.createMessage(self, payloadData=payload)
        campaignMessage.assertCreateMessage(response, 200)
        campaignMessage.assertCreateMessageDbCalls(response['json']['entity']['messageId'], self.campaignId, payload)

    @pytest.mark.parametrize('description,payload,statusCode,errorCode,errorMessage', [
        ('MessageType-ParticularDate-Plain-WithInvalidGsmSenderId', {'schedule':{'type':'PARTICULAR_DATE', 'datetime':int(time.time() * 1000 + 10 * 60 * 60 * 1000)}, 'senderDetails':{'gsmSenderId':1122, 'useSystemDefaults':True, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}}, 400, 3006, ['Provided Sender ids are not valid']),
        ('MessageType-ParticularDate-Plain-WithNegativeGsmSenderId', {'schedule':{'type':'PARTICULAR_DATE', 'datetime':int(time.time() * 1000 + 10 * 60 * 60 * 1000)}, 'senderDetails':{'gsmSenderId':-1122, 'useSystemDefaults':True, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}}, 400, 3006, ['Provided Sender ids are not valid']),
        ('MessageType-ParticularDate-Plain-WithInvalidCdmaSenderId', {'schedule':{'type':'PARTICULAR_DATE', 'datetime':int(time.time() * 1000 + 10 * 60 * 60 * 1000)}, 'senderDetails':{'cdmaSenderId':1122, 'useSystemDefaults':True, 'gsmSenderId':constant.config['message_senders']['gsmSenderId']}}, 400, 3006, ['Provided Sender ids are not valid']),
        ('MessageType-ParticularDate-Plain-WithNegativeCdmaSenderId', {'schedule':{'type':'PARTICULAR_DATE', 'datetime':int(time.time() * 1000 + 10 * 60 * 60 * 1000)}, 'senderDetails':{'cdmaSenderId':-1122, 'useSystemDefaults':True, 'gsmSenderId':constant.config['message_senders']['gsmSenderId']}}, 400, 3006, ['Provided Sender ids are not valid']),
        ('MessageType-ParticularDate-Plain-WithInvalidDomainGatewayMapId', {'schedule':{'type':'PARTICULAR_DATE', 'datetime':int(time.time() * 1000 + 10 * 60 * 60 * 1000)}, 'senderDetails':{'domainGatewayMapId':1212, 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}}, 400, 3005, ['Domain Gateway Map with id does not exist : 1212']),
        ('MessageType-ParticularDate-Plain-WithNegativeDomainGatewayMapId', {'schedule':{'type':'PARTICULAR_DATE', 'datetime':int(time.time() * 1000 + 10 * 60 * 60 * 1000)}, 'senderDetails':{'domainGatewayMapId':-1212, 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}}, 400, 3005, ['Domain Gateway Map with id does not exist : -1212']),
        ('MessageType-ParticularDate-Plain-WithoutPassingDomainGatewayMapId', {'schedule':{'type':'PARTICULAR_DATE', 'datetime':int(time.time() * 1000 + 10 * 60 * 60 * 1000)}, 'senderDetails':{'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}}, 400, 3012, ['Sender Details Exception : Please provide Domain Gateway Map Id if use system defaults is false']),
        ('MessageType-ParticularDate-Plain-WithoutPassingGsmAndCdmaSenderId', {'schedule':{'type':'PARTICULAR_DATE', 'datetime':int(time.time() * 1000 + 10 * 60 * 60 * 1000)}, 'senderDetails':{'useSystemDefaults':True}}, 400, 100, ['Invalid request : CDMA sender id is required', 'Invalid request : GSM sender id is required'])
        ])
    def test_createMessage_sms_ParticularDate_Plain_WrongSenderIds(self, description, payload, statusCode, errorCode, errorMessage):
        response, payload = campaignMessage.createMessage(self, payloadData=payload)
        campaignMessage.assertCreateMessage(response, statusCode, errorCode, errorMessage)

    @pytest.mark.parametrize('description,payload,listIdPassed,statusCode,errorCode,errorMessage', [
        ('MessageType-ParticularDate-Plain-WithInvalidListId', {'schedule':{'type':'PARTICULAR_DATE', 'datetime':int(time.time() * 1000 + 10 * 60 * 60 * 1000)}, 'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}}, 1111111, 400, 3007, ['List id does not exists : 1,111,111']),
        ('MessageType-ParticularDate-Plain-WithNegativeListId', {'schedule':{'type':'PARTICULAR_DATE', 'datetime':int(time.time() * 1000 + 10 * 60 * 60 * 1000)}, 'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}}, -1111111, 400, 100, ['Invalid request : Invalid list Id'])
        ])
    def test_createMessage_sms_ParticularDate_Plain_WithInvalidListId(self, description, payload, listIdPassed, statusCode, errorCode, errorMessage):
        actualListIdGettingUsedThroughOut = self.listId
        try:
            self.listId = listIdPassed
            response, payload = campaignMessage.createMessage(self, payloadData=payload)
            campaignMessage.assertCreateMessage(response, statusCode, errorCode, errorMessage)
        except AssertionError, reason:
            Assertion.constructAssertion(False, reason)
        except Exception, exp:
            Logger.log('Not Due to Assertion but Recurring Failed due to Reason :{}'.format(exp))
        finally:
            self.listId = actualListIdGettingUsedThroughOut

    @pytest.mark.parametrize('description,payload', [
        ('MessageType-ParticularDate-Plain-MessageWithTargetNdncAsTrue', {'schedule':{'type':'PARTICULAR_DATE', 'datetime':int(time.time() * 1000 + 10 * 60 * 60 * 1000)}, 'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'message':'Hi Buddy , only passing {{store_id}} {{optout}}', 'additionalInfo':{'targetNdnc':True, 'useTinyUrl':False}}),
        ('MessageType-ParticularDate-Plain-MessageWithTargetNdncAsTrue', {'schedule':{'type':'PARTICULAR_DATE', 'datetime':int(time.time() * 1000 + 10 * 60 * 60 * 1000)}, 'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'message':'Hi {{first_name}} {{store_id}} https://nightly.capillary.in/campaign/v3/base/CampaignOverview#campaign/302821 {{last_name}} ,Sending SMS via IRIS Automation{{optout}}', 'additionalInfo':{'targetNdnc':False, 'useTinyUrl':True}})
        ])  
    def test_createMessage_sms_ParticularDate_Plain_MessageWithAdditionalInfo(self, description, payload):
        response, payload = campaignMessage.createMessage(self, payloadData=payload)
        campaignMessage.assertCreateMessage(response, 200)
        campaignMessage.assertCreateMessageDbCalls(response['json']['entity']['messageId'], self.campaignId, payload)

    @pytest.mark.parametrize('description,payload,statusCode,errorCode,errorMessage', [
        ('MessageType-ParticularDate-Plain-MessageWithIncorrectChannel', {'schedule':{'type':'PARTICULAR_DATE', 'datetime':int(time.time() * 1000 + 10 * 60 * 60 * 1000)}, 'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'channel':'SM'}, 400, 103, ['Invalid type: Could not resolve type id \'SM\' into a subtype of [simple type, class com.capillary.campaigns.api.data.message.MessageBody]: known type ids = [MessageBody, SMS, WECHAT]']),
        ('MessageType-ParticularDate-Plain-MessageWithIncorrectSchedule', {'schedule':{'type':'PARTICULAR_DATE', 'datetime':int(time.time() * 1000 + 10 * 60 * 60 * 1000)}, 'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'schedule':{'type':'IMMEDIATEL'}}, 400, 103, ['Invalid type: Could not resolve type id \'IMMEDIATEL\' into a subtype of [simple type, class com.capillary.campaigns.api.data.message.Schedule]: known type ids = [IMMEDIATELY, PARTICULAR_DATE, RECURRING, Schedule]']),
        ('MessageType-ParticularDate-Plain-MessageWithIncorrectSenderDetails', {'schedule':{'type':'PARTICULAR_DATE', 'datetime':int(time.time() * 1000 + 10 * 60 * 60 * 1000)}, 'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':'Fals', 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}}, 400, 103, ['Invalid type: Can not construct instance of java.lang.Boolean from String value \'SMS\': only "true" or "false" recognized']),
        ('MessageType-ParticularDate-Plain-MessageWithIncorrectListId', {'schedule':{'type':'PARTICULAR_DATE', 'datetime':int(time.time() * 1000 + 10 * 60 * 60 * 1000)}, 'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'schedule':{'type':'PARTICULAR_DATE', 'datetime':int(time.time() * 1000 + 10 * 60 * 60 * 1000)}, 'senderDetails':{'listId':'null'}}, 400, 103, ['Invalid type: Unrecognized field "listId" (class com.capillary.campaigns.api.data.message.impl.sender.SmsSenderDetails), not marked as ignorable']),
        ('MessageType-ParticularDate-Plain-MessageWithIncorrectStoreType', {'schedule':{'type':'PARTICULAR_DATE', 'datetime':int(time.time() * 1000 + 10 * 60 * 60 * 1000)}, 'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'storeType':'REGISTERED_STOR'}, 400, 100, ['Invalid request : Valid store type must be provided if store tags are used']),
        ('MessageType-ParticularDate-Plain-MessageWithIncorrectAdditionalInfo', {'schedule':{'type':'PARTICULAR_DATE', 'datetime':int(time.time() * 1000 + 10 * 60 * 60 * 1000)}, 'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'additionalInfo':{'targetNdnc':'Fal'}}, 400, 103, ['Invalid type: Can not construct instance of boolean from String value \'SMS\': only "true" or "false" recognized'])
        ])
    def test_createMessage_sms_ParticularDate_Plain_WrongSchema(self, description, payload, statusCode, errorCode, errorMessage):
        response, payload = campaignMessage.createMessage(self, payloadData=payload)
        campaignMessage.assertCreateMessage(response, statusCode, errorCode, errorMessage)

    @pytest.mark.parametrize('description,payload,campaignIdPassed,statusCode,errorCode,errorMessage', [
        ('MessageType-ParticularDate-Generic-WithInvalidCampaignId', {'schedule':{'type':'PARTICULAR_DATE', 'datetime':int(time.time() * 1000 + 10 * 60 * 60 * 1000)}, 'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'GENERIC', 'genericIncentiveId':1}}, '0', 400, 100, ['Invalid request : must be greater than or equal to 1']),
        ('MessageType-ParticularDate-Generic-WithNegativeCampaignId', {'schedule':{'type':'PARTICULAR_DATE', 'datetime':int(time.time() * 1000 + 10 * 60 * 60 * 1000)}, 'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'GENERIC', 'genericIncentiveId':1}}, '-1234', 400, 100, ['Invalid request : must be greater than or equal to 1']),
        ('MessageType-ParticularDate-Generic-WithInvalidCampaignId', {'schedule':{'type':'PARTICULAR_DATE', 'datetime':int(time.time() * 1000 + 10 * 60 * 60 * 1000)}, 'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'GENERIC', 'genericIncentiveId':1}}, '1111234', 400, 1007, ['Campaign Id Exception : Invalid Campaign Id Passed 1111234'])
        ])
    def test_createMessage_sms_ParticularDate_Generic_WrongCampaignId(self, description, payload, campaignIdPassed, statusCode, errorCode, errorMessage):
        actualCampaignIdGettingUsedThroughOut = self.campaignId
        try:
            self.campaignId = campaignIdPassed
            response, payload = campaignMessage.createMessage(self, payloadData=payload)
            campaignMessage.assertCreateMessage(response, statusCode, errorCode, errorMessage)
        except Exception, exp:
            Logger.log('Exception Occured as :', exp)
            raise Exception('Failed with Assertion')
        finally:
            self.campaignId = actualCampaignIdGettingUsedThroughOut

    @pytest.mark.parametrize('description,payload,statusCode,errorCode,errorMessage', [
        ('MessageType-ParticularDate-Generic-MessageWithoutOptoutTag', {'schedule':{'type':'PARTICULAR_DATE', 'datetime':int(time.time() * 1000 + 10 * 60 * 60 * 1000)}, 'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'GENERIC', 'genericIncentiveId':1}, 'message':'Hi {{first_name}} {{last_name}} {{store_id}},Sending SMS via IRIS Automation'}, 400, 100, ['Invalid request : optout tag must be present in template']),
        ('MessageType-ParticularDate-Generic-MessageWithVoucherTag', {'schedule':{'type':'PARTICULAR_DATE', 'datetime':int(time.time() * 1000 + 10 * 60 * 60 * 1000)}, 'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'GENERIC', 'genericIncentiveId':1}, 'message':'Hi {{first_name}} {{last_name}} {{store_id}} {{voucher}} {{optout}} } ,Sending SMS via IRIS Automation'}, 400, 100, ['Invalid request : Coupons incentive should be attached to use voucher tags']),
        ('MessageType-ParticularDate-Generic-MessageWithPointsTag', {'schedule':{'type':'PARTICULAR_DATE', 'datetime':int(time.time() * 1000 + 10 * 60 * 60 * 1000)}, 'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'GENERIC', 'genericIncentiveId':1}, 'message':'Hi {{first_name}} {{last_name}} {{store_id}} {{promotion_points}} {{optout}} } ,Sending SMS via IRIS Automation'}, 400, 100, 'Invalid request : Points incentive should be attached to use points tags')
        ])
    def test_createMessage_sms_ParticularDate_Generic_MessageWithInvalidTags(self, description, payload, statusCode, errorCode, errorMessage):
        response, payload = campaignMessage.createMessage(self, payloadData=payload)
        campaignMessage.assertCreateMessage(response, statusCode, errorCode, errorMessage)

    @pytest.mark.parametrize('description,payload', [
        ('MessageType-ParticularDate-Generic-MessageWithStoreTypeAsLastTransactedAt', {'schedule':{'type':'PARTICULAR_DATE', 'datetime':int(time.time() * 1000 + 10 * 60 * 60 * 1000)}, 'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'GENERIC', 'genericIncentiveId':1}, 'storeType':'LAST_TRANSACTED_AT'})
        ])  
    def test_createMessage_sms_ParticularDate_Generic_MessageWithStoreTypeAsLastTransactedAt(self, description, payload):
        response, payload = campaignMessage.createMessage(self, payloadData=payload)
        campaignMessage.assertCreateMessage(response, 200)
        campaignMessage.assertCreateMessageDbCalls(response['json']['entity']['messageId'], self.campaignId, payload)

    @pytest.mark.parametrize('description,payload,statusCode,errorCode,errorMessage', [
        ('MessageType-ParticularDate-Generic-WithInvalidGsmSenderId', {'schedule':{'type':'PARTICULAR_DATE', 'datetime':int(time.time() * 1000 + 10 * 60 * 60 * 1000)}, 'senderDetails':{'gsmSenderId':1122, 'useSystemDefaults':True, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'GENERIC', 'genericIncentiveId':1}}, 400, 3006, ['Provided Sender ids are not valid']),
        ('MessageType-ParticularDate-Generic-WithNegativeGsmSenderId', {'schedule':{'type':'PARTICULAR_DATE', 'datetime':int(time.time() * 1000 + 10 * 60 * 60 * 1000)}, 'senderDetails':{'gsmSenderId':-1122, 'useSystemDefaults':True, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'GENERIC', 'genericIncentiveId':1}}, 400, 3006, ['Provided Sender ids are not valid']),
        ('MessageType-ParticularDate-Generic-WithInvalidCdmaSenderId', {'schedule':{'type':'PARTICULAR_DATE', 'datetime':int(time.time() * 1000 + 10 * 60 * 60 * 1000)}, 'senderDetails':{'cdmaSenderId':1122, 'useSystemDefaults':True, 'gsmSenderId':constant.config['message_senders']['gsmSenderId']}, 'incentive':{'type':'GENERIC', 'genericIncentiveId':1}}, 400, 3006, ['Provided Sender ids are not valid']),
        ('MessageType-ParticularDate-Generic-WithNegativeCdmaSenderId', {'schedule':{'type':'PARTICULAR_DATE', 'datetime':int(time.time() * 1000 + 10 * 60 * 60 * 1000)}, 'senderDetails':{'cdmaSenderId':-1122, 'useSystemDefaults':True, 'gsmSenderId':constant.config['message_senders']['gsmSenderId']}, 'incentive':{'type':'GENERIC', 'genericIncentiveId':1}}, 400, 3006, ['Provided Sender ids are not valid']),
        ('MessageType-ParticularDate-Generic-WithInvalidDomainGatewayMapId', {'schedule':{'type':'PARTICULAR_DATE', 'datetime':int(time.time() * 1000 + 10 * 60 * 60 * 1000)}, 'senderDetails':{'domainGatewayMapId':1212, 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'GENERIC', 'genericIncentiveId':1}}, 400, 3005, ['Domain Gateway Map with id does not exist : 1212']),
        ('MessageType-ParticularDate-Generic-WithNegativeDomainGatewayMapId', {'schedule':{'type':'PARTICULAR_DATE', 'datetime':int(time.time() * 1000 + 10 * 60 * 60 * 1000)}, 'senderDetails':{'domainGatewayMapId':-1212, 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'GENERIC', 'genericIncentiveId':1}}, 400, 3005, ['Domain Gateway Map with id does not exist : -1212']),
        ('MessageType-ParticularDate-Generic-WithoutPassingDomainGatewayMapId', {'schedule':{'type':'PARTICULAR_DATE', 'datetime':int(time.time() * 1000 + 10 * 60 * 60 * 1000)}, 'senderDetails':{'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'GENERIC', 'genericIncentiveId':1}}, 400, 3012, ['Sender Details Exception : Please provide Domain Gateway Map Id if use system defaults is false']),
        ('MessageType-ParticularDate-Generic-WithoutPassingGsmAndCdmaSenderId', {'schedule':{'type':'PARTICULAR_DATE', 'datetime':int(time.time() * 1000 + 10 * 60 * 60 * 1000)}, 'senderDetails':{'useSystemDefaults':True}}, 400, 100, ['Invalid request : GSM sender id is required', 'Invalid request : CDMA sender id is required'])
        ])
    def test_createMessage_sms_ParticularDate_Generic_WrongSenderIds(self, description, payload, statusCode, errorCode, errorMessage):
        response, payload = campaignMessage.createMessage(self, payloadData=payload)
        campaignMessage.assertCreateMessage(response, statusCode, errorCode, errorMessage)

    @pytest.mark.parametrize('description,payload', [
        ('MessageType-ParticularDate-Generic-MessageWithTargetNdncAsTrue', {'schedule':{'type':'PARTICULAR_DATE', 'datetime':int(time.time() * 1000 + 10 * 60 * 60 * 1000)}, 'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'GENERIC', 'genericIncentiveId':1}, 'message':'Hi buddy , only passing {{store_id}} {{optout}}', 'additionalInfo':{'targetNdnc':True, 'useTinyUrl':False}}),
        ('MessageType-ParticularDate-Generic-MessageWithTargetNdncAsTrue', {'schedule':{'type':'PARTICULAR_DATE', 'datetime':int(time.time() * 1000 + 10 * 60 * 60 * 1000)}, 'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'GENERIC', 'genericIncentiveId':1}, 'message':'Hi {{first_name}} {{store_id}} https://nightly.capillary.in/campaign/v3/base/CampaignOverview#campaign/302821 {{last_name}} ,Sending SMS via IRIS Automation{{optout}}', 'additionalInfo':{'targetNdnc':False, 'useTinyUrl':True}})
        ])  
    def test_createMessage_sms_ParticularDate_Generic_MessageWithAdditionalInfo(self, description, payload):
        response, payload = campaignMessage.createMessage(self, payloadData=payload)
        campaignMessage.assertCreateMessage(response, 200)
        campaignMessage.assertCreateMessageDbCalls(response['json']['entity']['messageId'], self.campaignId, payload)

    @pytest.mark.parametrize('description,payload,statusCode,errorCode,errorMessage', [
        ('MessageType-ParticularDate-Generic-MessageWithIncorrectChannel', {'schedule':{'type':'PARTICULAR_DATE', 'datetime':int(time.time() * 1000 + 10 * 60 * 60 * 1000)}, 'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'GENERIC', 'genericIncentiveId':1}, 'channel':'SM'}, 400, 103, ['Invalid type: Could not resolve type id \'SM\' into a subtype of [simple type, class com.capillary.campaigns.api.data.message.MessageBody]: known type ids = [MessageBody, SMS, WECHAT]']),
        ('MessageType-ParticularDate-Generic-MessageWithIncorrectSchedule', {'schedule':{'type':'PARTICULAR_DATE', 'datetime':int(time.time() * 1000 + 10 * 60 * 60 * 1000)}, 'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'GENERIC', 'genericIncentiveId':1}, 'schedule':{'type':'IMMEDIATEL'}}, 400, 103, ['Invalid type: Could not resolve type id \'IMMEDIATEL\' into a subtype of [simple type, class com.capillary.campaigns.api.data.message.Schedule]: known type ids = [IMMEDIATELY, PARTICULAR_DATE, RECURRING, Schedule]']),
        ('MessageType-ParticularDate-Plain-MessageWithIncorrectSenderDetails', {'schedule':{'type':'PARTICULAR_DATE', 'datetime':int(time.time() * 1000 + 10 * 60 * 60 * 1000)}, 'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':'Fals', 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}}, 400, 103, ['Invalid type: Can not construct instance of java.lang.Boolean from String value \'SMS\': only "true" or "false" recognized']),
        ('MessageType-ParticularDate-Generic-MessageWithIncorrectStoreType', {'schedule':{'type':'PARTICULAR_DATE', 'datetime':int(time.time() * 1000 + 10 * 60 * 60 * 1000)}, 'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'GENERIC', 'genericIncentiveId':1}, 'storeType':'REGISTERED_STOR'}, 400, 100, ['Invalid request : Valid store type must be provided if store tags are used']),
        ('MessageType-ParticularDate-Generic-MessageWithIncorrectAdditionalInfo', {'schedule':{'type':'PARTICULAR_DATE', 'datetime':int(time.time() * 1000 + 10 * 60 * 60 * 1000)}, 'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'GENERIC', 'genericIncentiveId':1}, 'additionalInfo':{'targetNdnc':'Fal'}}, 400, 103, ['Invalid type: Can not construct instance of boolean from String value \'SMS\': only "true" or "false" recognized'])
        ])
    def test_createMessage_sms_ParticularDate_Generic_WrongSchema(self, description, payload, statusCode, errorCode, errorMessage):
        response, payload = campaignMessage.createMessage(self, payloadData=payload)
        campaignMessage.assertCreateMessage(response, statusCode, errorCode, errorMessage)

    @pytest.mark.parametrize('description,payload,campaignIdPassed,statusCode,errorCode,errorMessage', [
        ('MessageType-ParticularDate-Coupon-WithInvalidCampaignId', {'schedule':{'type':'PARTICULAR_DATE', 'datetime':int(time.time() * 1000 + 10 * 60 * 60 * 1000)}, 'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'COUPONS', 'voucherSeriesId':0}}, '0', 400, 100, ['Invalid request : must be greater than or equal to 1']),
        ('MessageType-ParticularDate-Coupon-WithNegativeCampaignId', {'schedule':{'type':'PARTICULAR_DATE', 'datetime':int(time.time() * 1000 + 10 * 60 * 60 * 1000)}, 'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'COUPONS', 'voucherSeriesId':0}}, '-1234', 400, 100, ['Invalid request : must be greater than or equal to 1']),
        ('MessageType-ParticularDate-Coupon-WithInvalidCampaignId', {'schedule':{'type':'PARTICULAR_DATE', 'datetime':int(time.time() * 1000 + 10 * 60 * 60 * 1000)}, 'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'COUPONS', 'voucherSeriesId':0}}, '1111234', 400, 1007, ['Campaign Id Exception : Invalid Campaign Id Passed 1111234'])
        ])
    def test_createMessage_sms_ParticularDate_Coupon_WrongCampaignId(self, description, payload, campaignIdPassed, statusCode, errorCode, errorMessage):
        payload.update({'incentive':{'type':'COUPONS', 'voucherSeriesId':self.voucherId}})
        actualCampaignIdGettingUsedThroughOut = self.campaignId
        try:
            self.campaignId = campaignIdPassed
            response, payload = campaignMessage.createMessage(self, payloadData=payload)
            campaignMessage.assertCreateMessage(response, statusCode, errorCode, errorMessage)
        except Exception, exp:
            Logger.log('Exception Occured as :', exp)
            raise Exception('Failed with Assertion')
        finally:
            self.campaignId = actualCampaignIdGettingUsedThroughOut

    @pytest.mark.parametrize('description,payload,statusCode,errorCode,errorMessage', [
        ('MessageType-ParticularDate-Coupon-MessageWithoutOptoutTag', {'schedule':{'type':'PARTICULAR_DATE', 'datetime':int(time.time() * 1000 + 10 * 60 * 60 * 1000)}, 'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'COUPONS', 'voucherSeriesId':0}, 'message':'Hi {{first_name}} {{last_name}} {{store_id}},Sending SMS via IRIS Automation'}, 400, 100, ['Invalid request : optout tag must be present in template']),
        ('MessageType-ParticularDate-Coupon-MessageWithPointsTag', {'schedule':{'type':'PARTICULAR_DATE', 'datetime':int(time.time() * 1000 + 10 * 60 * 60 * 1000)}, 'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'COUPONS', 'voucherSeriesId':0}, 'message':'Hi {{first_name}} {{last_name}} {{store_id}} {{promotion_points}} {{optout}} } ,Sending SMS via IRIS Automation'}, 400, 100, 'Invalid request : Points incentive should be attached to use points tags')
        ])
    def test_createMessage_sms_ParticularDate_Coupon_MessageWithInvalidTags(self, description, payload, statusCode, errorCode, errorMessage):
        payload.update({'incentive':{'type':'COUPONS', 'voucherSeriesId':self.voucherId}})
        response, payload = campaignMessage.createMessage(self, payloadData=payload)
        campaignMessage.assertCreateMessage(response, statusCode, errorCode, errorMessage)

    @pytest.mark.parametrize('description,payload', [
        ('MessageType-ParticularDate-Coupon-MessageWithStoreTypeAsLastTransactedAt', {'schedule':{'type':'PARTICULAR_DATE', 'datetime':int(time.time() * 1000 + 10 * 60 * 60 * 1000)}, 'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'COUPONS', 'voucherSeriesId':0}, 'storeType':'LAST_TRANSACTED_AT'})
        ])  
    def test_createMessage_sms_ParticularDate_Coupon_MessageWithStoreTypeAsLastTransactedAt(self, description, payload):
        payload.update({'incentive':{'type':'COUPONS', 'voucherSeriesId':self.voucherId}})
        response, payload = campaignMessage.createMessage(self, payloadData=payload)
        campaignMessage.assertCreateMessage(response, 200)
        campaignMessage.assertCreateMessageDbCalls(response['json']['entity']['messageId'], self.campaignId, payload)

    @pytest.mark.parametrize('description,payload,statusCode,errorCode,errorMessage', [
        ('MessageType-ParticularDate-Coupon-WithInvalidGsmSenderId', {'schedule':{'type':'PARTICULAR_DATE', 'datetime':int(time.time() * 1000 + 10 * 60 * 60 * 1000)}, 'senderDetails':{'gsmSenderId':1122, 'useSystemDefaults':True, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'COUPONS', 'voucherSeriesId':0}}, 400, 3006, ['Provided Sender ids are not valid']),
        ('MessageType-ParticularDate-Coupon-WithNegativeGsmSenderId', {'schedule':{'type':'PARTICULAR_DATE', 'datetime':int(time.time() * 1000 + 10 * 60 * 60 * 1000)}, 'senderDetails':{'gsmSenderId':-1122, 'useSystemDefaults':True, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'COUPONS', 'voucherSeriesId':0}}, 400, 3006, ['Provided Sender ids are not valid']),
        ('MessageType-ParticularDate-Coupon-WithInvalidCdmaSenderId', {'schedule':{'type':'PARTICULAR_DATE', 'datetime':int(time.time() * 1000 + 10 * 60 * 60 * 1000)}, 'senderDetails':{'cdmaSenderId':1122, 'useSystemDefaults':True, 'gsmSenderId':constant.config['message_senders']['gsmSenderId']}, 'incentive':{'type':'COUPONS', 'voucherSeriesId':0}}, 400, 3006, ['Provided Sender ids are not valid']),
        ('MessageType-ParticularDate-Coupon-WithNegativeCdmaSenderId', {'schedule':{'type':'PARTICULAR_DATE', 'datetime':int(time.time() * 1000 + 10 * 60 * 60 * 1000)}, 'senderDetails':{'cdmaSenderId':-1122, 'useSystemDefaults':True, 'gsmSenderId':constant.config['message_senders']['gsmSenderId']}, 'incentive':{'type':'COUPONS', 'voucherSeriesId':0}}, 400, 3006, ['Provided Sender ids are not valid']),
        ('MessageType-ParticularDate-Coupon-WithInvalidDomainGatewayMapId', {'schedule':{'type':'PARTICULAR_DATE', 'datetime':int(time.time() * 1000 + 10 * 60 * 60 * 1000)}, 'senderDetails':{'domainGatewayMapId':1212, 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'COUPONS', 'voucherSeriesId':0}}, 400, 3005, ['Domain Gateway Map with id does not exist : 1212']),
        ('MessageType-ParticularDate-Coupon-WithNegativeDomainGatewayMapId', {'schedule':{'type':'PARTICULAR_DATE', 'datetime':int(time.time() * 1000 + 10 * 60 * 60 * 1000)}, 'senderDetails':{'domainGatewayMapId':-1212, 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'COUPONS', 'voucherSeriesId':0}}, 400, 3005, ['Domain Gateway Map with id does not exist : -1212']),
        ('MessageType-ParticularDate-Coupon-WithoutPassingDomainGatewayMapId', {'schedule':{'type':'PARTICULAR_DATE', 'datetime':int(time.time() * 1000 + 10 * 60 * 60 * 1000)}, 'senderDetails':{'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'COUPONS', 'voucherSeriesId':0}}, 400, 3012, ['Sender Details Exception : Please provide Domain Gateway Map Id if use system defaults is false']),
        ('MessageType-ParticularDate-Coupon-WithoutPassingGsmAndCdmaSenderId', {'schedule':{'type':'PARTICULAR_DATE', 'datetime':int(time.time() * 1000 + 10 * 60 * 60 * 1000)}, 'senderDetails':{'useSystemDefaults':True}}, 400, 100, ['Invalid request : GSM sender id is required', 'Invalid request : CDMA sender id is required'])
        ])
    def test_createMessage_sms_ParticularDate_Coupon_WrongSenderIds(self, description, payload, statusCode, errorCode, errorMessage):
        payload.update({'incentive':{'type':'COUPONS', 'voucherSeriesId':self.voucherId}})
        response, payload = campaignMessage.createMessage(self, payloadData=payload)
        campaignMessage.assertCreateMessage(response, statusCode, errorCode, errorMessage)

    @pytest.mark.parametrize('description,payload,listIdPassed,statusCode,errorCode,errorMessage', [
        ('MessageType-ParticularDate-Coupon-WithInvalidListId', {'schedule':{'type':'PARTICULAR_DATE', 'datetime':int(time.time() * 1000 + 10 * 60 * 60 * 1000)}, 'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'COUPONS', 'voucherSeriesId':0}}, 1111111, 400, 3007, ['List id does not exists : 1,111,111']),
        ('MessageType-ParticularDate-Coupon-WithNegativeListId', {'schedule':{'type':'PARTICULAR_DATE', 'datetime':int(time.time() * 1000 + 10 * 60 * 60 * 1000)}, 'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'COUPONS', 'voucherSeriesId':0}}, -1111111, 400, 100, ['Invalid request : Invalid list Id'])
        ])
    def test_createMessage_sms_ParticularDate_Coupon_WithInvalidListId(self, description, payload, listIdPassed, statusCode, errorCode, errorMessage):
        payload.update({'incentive':{'type':'COUPONS', 'voucherSeriesId':self.voucherId}})
        actualListIdGettingUsedThroughOut = self.listId
        try:
            self.listId = listIdPassed
            response, payload = campaignMessage.createMessage(self, payloadData=payload)
            campaignMessage.assertCreateMessage(response, statusCode, errorCode, errorMessage)
        except AssertionError, reason:
            Assertion.constructAssertion(False, reason)
        except Exception, exp:
            Logger.log('Not Due to Assertion but Recurring Failed due to Reason :{}'.format(exp))
        finally:
            self.listId = actualListIdGettingUsedThroughOut

    @pytest.mark.parametrize('description,payload', [
        ('MessageType-ParticularDate-Coupon-MessageWithTargetNdncAsTrue', {'schedule':{'type':'PARTICULAR_DATE', 'datetime':int(time.time() * 1000 + 10 * 60 * 60 * 1000)}, 'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'COUPONS', 'voucherSeriesId':0}, 'message':'Hi Buddy , only passing {{store_id}} {{optout}}', 'additionalInfo':{'targetNdnc':True, 'useTinyUrl':False}}),
        ('MessageType-ParticularDate-Coupon-MessageWithTargetNdncAsTrue', {'schedule':{'type':'PARTICULAR_DATE', 'datetime':int(time.time() * 1000 + 10 * 60 * 60 * 1000)}, 'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'COUPONS', 'voucherSeriesId':0}, 'message':'Hi {{first_name}} {{store_id}} https://nightly.capillary.in/campaign/v3/base/CampaignOverview#campaign/302821 {{last_name}} ,Sending SMS via IRIS Automation{{optout}}', 'additionalInfo':{'targetNdnc':False, 'useTinyUrl':True}})
        ])  
    def test_createMessage_sms_ParticularDate_Coupon_MessageWithAdditionalInfo(self, description, payload):
        payload.update({'incentive':{'type':'COUPONS', 'voucherSeriesId':self.voucherId}})
        response, payload = campaignMessage.createMessage(self, payloadData=payload)
        campaignMessage.assertCreateMessage(response, 200)
        campaignMessage.assertCreateMessageDbCalls(response['json']['entity']['messageId'], self.campaignId, payload)

    @pytest.mark.parametrize('description,payload,statusCode,errorCode,errorMessage', [
        ('MessageType-ParticularDate-Coupon-MessageWithIncorrectChannel', {'schedule':{'type':'PARTICULAR_DATE', 'datetime':int(time.time() * 1000 + 10 * 60 * 60 * 1000)}, 'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'COUPONS', 'voucherSeriesId':0}, 'channel':'SM'}, 400, 103, ['Invalid type: Could not resolve type id \'SM\' into a subtype of [simple type, class com.capillary.campaigns.api.data.message.MessageBody]: known type ids = [MessageBody, SMS, WECHAT]']),
        ('MessageType-ParticularDate-Coupon-MessageWithIncorrectSchedule', {'schedule':{'type':'PARTICULAR_DATE', 'datetime':int(time.time() * 1000 + 10 * 60 * 60 * 1000)}, 'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'COUPONS', 'voucherSeriesId':0}, 'schedule':{'type':'IMMEDIATEL'}}, 400, 103, ['Invalid type: Could not resolve type id \'IMMEDIATEL\' into a subtype of [simple type, class com.capillary.campaigns.api.data.message.Schedule]: known type ids = [IMMEDIATELY, PARTICULAR_DATE, RECURRING, Schedule]']),
        ('MessageType-ParticularDate-Coupon-MessageWithIncorrectSenderDetails', {'schedule':{'type':'PARTICULAR_DATE', 'datetime':int(time.time() * 1000 + 10 * 60 * 60 * 1000)}, 'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':'Fals', 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'COUPONS', 'voucherSeriesId':0}}, 400, 103, ['Invalid type: Can not construct instance of java.lang.Boolean from String value \'SMS\': only "true" or "false" recognized']),
        ('MessageType-ParticularDate-Coupon-MessageWithIncorrectListId', {'schedule':{'type':'PARTICULAR_DATE', 'datetime':int(time.time() * 1000 + 10 * 60 * 60 * 1000)}, 'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'COUPONS', 'voucherSeriesId':0}, 'schedule':{'type':'PARTICULAR_DATE', 'datetime':int(time.time() * 1000 + 10 * 60 * 60 * 1000)}, 'senderDetails':{'listId':'null'}}, 400, 103, ['Invalid type: Unrecognized field "listId" (class com.capillary.campaigns.api.data.message.impl.sender.SmsSenderDetails), not marked as ignorable']),
        ('MessageType-ParticularDate-Coupon-MessageWithIncorrectStoreType', {'schedule':{'type':'PARTICULAR_DATE', 'datetime':int(time.time() * 1000 + 10 * 60 * 60 * 1000)}, 'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'COUPONS', 'voucherSeriesId':0}, 'storeType':'REGISTERED_STOR'}, 400, 100, ['Invalid request : Valid store type must be provided if store tags are used']),
        ('MessageType-ParticularDate-Coupon-MessageWithIncorrectAdditionalInfo', {'schedule':{'type':'PARTICULAR_DATE', 'datetime':int(time.time() * 1000 + 10 * 60 * 60 * 1000)}, 'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'COUPONS', 'voucherSeriesId':0}, 'additionalInfo':{'targetNdnc':'Fal'}}, 400, 103, ['Invalid type: Can not construct instance of boolean from String value \'SMS\': only "true" or "false" recognized'])
        ])
    def test_createMessage_sms_ParticularDate_Coupon_WrongSchema(self, description, payload, statusCode, errorCode, errorMessage):
        payload.update({'incentive':{'type':'COUPONS', 'voucherSeriesId':self.voucherId}})
        response, payload = campaignMessage.createMessage(self, payloadData=payload)
        campaignMessage.assertCreateMessage(response, statusCode, errorCode, errorMessage)

    @pytest.mark.parametrize('description,payload,campaignIdPassed,statusCode,errorCode,errorMessage', [
        ('MessageType-ParticularDate-Points-WithInvalidCampaignId', {'schedule':{'type':'PARTICULAR_DATE', 'datetime':int(time.time() * 1000 + 10 * 60 * 60 * 1000)}, 'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'POINTS', 'programId':0, 'allocationStrategyId':0, 'expirationStrategyId':0}}, '0', 400, 100, ['Invalid request : must be greater than or equal to 1']),
        ('MessageType-ParticularDate-Points-WithNegativeCampaignId', {'schedule':{'type':'PARTICULAR_DATE', 'datetime':int(time.time() * 1000 + 10 * 60 * 60 * 1000)}, 'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'POINTS', 'programId':0, 'allocationStrategyId':0, 'expirationStrategyId':0}}, '-1234', 400, 100, ['Invalid request : must be greater than or equal to 1']),
        ('MessageType-ParticularDate-Points-WithInvalidCampaignId', {'schedule':{'type':'PARTICULAR_DATE', 'datetime':int(time.time() * 1000 + 10 * 60 * 60 * 1000)}, 'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'POINTS', 'programId':0, 'allocationStrategyId':0, 'expirationStrategyId':0}}, '1111234', 400, 1007, ['Campaign Id Exception : Invalid Campaign Id Passed 1111234'])
        ])
    def test_createMessage_sms_ParticularDate_Points_WrongCampaignId(self, description, payload, campaignIdPassed, statusCode, errorCode, errorMessage):
        payload.update({'incentive':{'type':'POINTS', 'programId':self.programeId, 'allocationStrategyId':self.allocationStrategyId, 'expirationStrategyId':self.expiryStrategyId}})
        actualCampaignIdGettingUsedThroughOut = self.campaignId
        try:
            self.campaignId = campaignIdPassed
            response, payload = campaignMessage.createMessage(self, payloadData=payload)
            campaignMessage.assertCreateMessage(response, statusCode, errorCode, errorMessage)
        except AssertionError, reason:
            Assertion.constructAssertion(False, reason)
        except Exception, exp:
            Logger.log('Not Due to Assertion but Recurring Failed due to Reason :{}'.format(exp))
        finally:
            self.campaignId = actualCampaignIdGettingUsedThroughOut

    @pytest.mark.parametrize('description,payload,statusCode,errorCode,errorMessage', [
        ('MessageType-ParticularDate-Points-MessageWithoutOptoutTag', {'schedule':{'type':'PARTICULAR_DATE', 'datetime':int(time.time() * 1000 + 10 * 60 * 60 * 1000)}, 'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'POINTS', 'programId':0, 'allocationStrategyId':0, 'expirationStrategyId':0}, 'message':'Hi {{first_name}} {{last_name}} {{store_id}} ,Sending SMS via IRIS Automation'}, 400, 100, ['Invalid request : optout tag must be present in template']),
        ('MessageType-ParticularDate-Plain-MessageWithVoucherTag', {'schedule':{'type':'PARTICULAR_DATE', 'datetime':int(time.time() * 1000 + 10 * 60 * 60 * 1000)}, 'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'message':'Hi {{first_name}} {{last_name}} {{store_id}} {{voucher}} {{optout}} } ,Sending SMS via IRIS Automation'}, 400, 100, ['Invalid request : Coupons incentive should be attached to use voucher tags']),
        ])
    def test_createMessage_sms_ParticularDate_Points_MessageWithInvalidTags(self, description, payload, statusCode, errorCode, errorMessage):
        payload.update({'incentive':{'type':'POINTS', 'programId':self.programeId, 'allocationStrategyId':self.allocationStrategyId, 'expirationStrategyId':self.expiryStrategyId}})
        response, payload = campaignMessage.createMessage(self, payloadData=payload)
        campaignMessage.assertCreateMessage(response, statusCode, errorCode, errorMessage)

    @pytest.mark.parametrize('description,payload', [
        ('MessageType-ParticularDate-Points-MessageWithStoreTypeAsLastTransactedAt', {'schedule':{'type':'PARTICULAR_DATE', 'datetime':int(time.time() * 1000 + 10 * 60 * 60 * 1000)}, 'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'POINTS', 'programId':0, 'allocationStrategyId':0, 'expirationStrategyId':0}, 'storeType':'LAST_TRANSACTED_AT'})
        ])  
    def test_createMessage_sms_ParticularDate_Points_MessageWithStoreTypeAsLastTransactedAt(self, description, payload):
        payload.update({'incentive':{'type':'POINTS', 'programId':self.programeId, 'allocationStrategyId':self.allocationStrategyId, 'expirationStrategyId':self.expiryStrategyId}})
        response, payload = campaignMessage.createMessage(self, payloadData=payload)
        campaignMessage.assertCreateMessage(response, 200)
        campaignMessage.assertCreateMessageDbCalls(response['json']['entity']['messageId'], self.campaignId, payload)

    @pytest.mark.parametrize('description,payload,statusCode,errorCode,errorMessage', [
        ('MessageType-ParticularDate-Points-WithInvalidGsmSenderId', {'schedule':{'type':'PARTICULAR_DATE', 'datetime':int(time.time() * 1000 + 10 * 60 * 60 * 1000)}, 'senderDetails':{'gsmSenderId':1122, 'useSystemDefaults':True, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'POINTS', 'programId':0, 'allocationStrategyId':0, 'expirationStrategyId':0}}, 400, 3006, ['Provided Sender ids are not valid']),
        ('MessageType-ParticularDate-Points-WithNegativeGsmSenderId', {'schedule':{'type':'PARTICULAR_DATE', 'datetime':int(time.time() * 1000 + 10 * 60 * 60 * 1000)}, 'senderDetails':{'gsmSenderId':-1122, 'useSystemDefaults':True, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'POINTS', 'programId':0, 'allocationStrategyId':0, 'expirationStrategyId':0}}, 400, 3006, ['Provided Sender ids are not valid']),
        ('MessageType-ParticularDate-Points-WithInvalidCdmaSenderId', {'schedule':{'type':'PARTICULAR_DATE', 'datetime':int(time.time() * 1000 + 10 * 60 * 60 * 1000)}, 'senderDetails':{'cdmaSenderId':1122, 'useSystemDefaults':True, 'gsmSenderId':constant.config['message_senders']['gsmSenderId']}, 'incentive':{'type':'POINTS', 'programId':0, 'allocationStrategyId':0, 'expirationStrategyId':0}}, 400, 3006, ['Provided Sender ids are not valid']),
        ('MessageType-ParticularDate-Points-WithNegativeCdmaSenderId', {'schedule':{'type':'PARTICULAR_DATE', 'datetime':int(time.time() * 1000 + 10 * 60 * 60 * 1000)}, 'senderDetails':{'cdmaSenderId':-1122, 'useSystemDefaults':True, 'gsmSenderId':constant.config['message_senders']['gsmSenderId']}, 'incentive':{'type':'POINTS', 'programId':0, 'allocationStrategyId':0, 'expirationStrategyId':0}}, 400, 3006, ['Provided Sender ids are not valid']),
        ('MessageType-ParticularDate-Points-WithInvalidDomainGatewayMapId', {'schedule':{'type':'PARTICULAR_DATE', 'datetime':int(time.time() * 1000 + 10 * 60 * 60 * 1000)}, 'senderDetails':{'domainGatewayMapId':1212, 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'POINTS', 'programId':0, 'allocationStrategyId':0, 'expirationStrategyId':0}}, 400, 3005, ['Domain Gateway Map with id does not exist : 1212']),
        ('MessageType-ParticularDate-Points-WithNegativeDomainGatewayMapId', {'schedule':{'type':'PARTICULAR_DATE', 'datetime':int(time.time() * 1000 + 10 * 60 * 60 * 1000)}, 'senderDetails':{'domainGatewayMapId':-1212, 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'POINTS', 'programId':0, 'allocationStrategyId':0, 'expirationStrategyId':0}}, 400, 3005, ['Domain Gateway Map with id does not exist : -1212']),
        ('MessageType-ParticularDate-Points-WithoutPassingDomainGatewayMapId', {'schedule':{'type':'PARTICULAR_DATE', 'datetime':int(time.time() * 1000 + 10 * 60 * 60 * 1000)}, 'senderDetails':{'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'POINTS', 'programId':0, 'allocationStrategyId':0, 'expirationStrategyId':0}}, 400, 3012, ['Sender Details Exception : Please provide Domain Gateway Map Id if use system defaults is false']),
        ('MessageType-ParticularDate-Points-WithoutPassingGsmAndCdmaSenderId', {'schedule':{'type':'PARTICULAR_DATE', 'datetime':int(time.time() * 1000 + 10 * 60 * 60 * 1000)}, 'senderDetails':{'useSystemDefaults':True}}, 400, 100, ['Invalid request : CDMA sender id is required', 'Invalid request : GSM sender id is required'])
        ])
    def test_createMessage_sms_ParticularDate_Points_WrongSenderIds(self, description, payload, statusCode, errorCode, errorMessage):
        payload.update({'incentive':{'type':'POINTS', 'programId':self.programeId, 'allocationStrategyId':self.allocationStrategyId, 'expirationStrategyId':self.expiryStrategyId}})
        response, payload = campaignMessage.createMessage(self, payloadData=payload)
        campaignMessage.assertCreateMessage(response, statusCode, errorCode, errorMessage)

    @pytest.mark.parametrize('description,payload,listIdPassed,statusCode,errorCode,errorMessage', [
        ('MessageType-ParticularDate-Points-WithInvalidListId', {'schedule':{'type':'PARTICULAR_DATE', 'datetime':int(time.time() * 1000 + 10 * 60 * 60 * 1000)}, 'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'POINTS', 'programId':0, 'allocationStrategyId':0, 'expirationStrategyId':0}}, 1111111, 400, 3007, ['List id does not exists : 1,111,111']),
        ('MessageType-ParticularDate-Points-WithNegativeListId', {'schedule':{'type':'PARTICULAR_DATE', 'datetime':int(time.time() * 1000 + 10 * 60 * 60 * 1000)}, 'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'POINTS', 'programId':0, 'allocationStrategyId':0, 'expirationStrategyId':0}}, -1111111, 400, 100, ['Invalid request : Invalid list Id'])
        ])
    def test_createMessage_sms_ParticularDate_Points_WithInvalidListId(self, description, payload, listIdPassed, statusCode, errorCode, errorMessage):
        payload.update({'incentive':{'type':'POINTS', 'programId':self.programeId, 'allocationStrategyId':self.allocationStrategyId, 'expirationStrategyId':self.expiryStrategyId}})
        actualListIdGettingUsedThroughOut = self.listId
        try:
            self.listId = listIdPassed
            response, payload = campaignMessage.createMessage(self, payloadData=payload)
            campaignMessage.assertCreateMessage(response, statusCode, errorCode, errorMessage)
        except AssertionError, reason:
            Assertion.constructAssertion(False, reason)
        except Exception, exp:
            Logger.log('Not Due to Assertion but Recurring Failed due to Reason :{}'.format(exp))
        finally:
            self.listId = actualListIdGettingUsedThroughOut

    @pytest.mark.parametrize('description,payload', [
        ('MessageType-ParticularDate-Points-MessageWithTargetNdncAsTrue', {'schedule':{'type':'PARTICULAR_DATE', 'datetime':int(time.time() * 1000 + 10 * 60 * 60 * 1000)}, 'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'POINTS', 'programId':0, 'allocationStrategyId':0, 'expirationStrategyId':0}, 'additionalInfo':{'targetNdnc':True, 'useTinyUrl':False}}),
        ('MessageType-ParticularDate-Points-MessageWithTargetNdncAsTrue', {'schedule':{'type':'PARTICULAR_DATE', 'datetime':int(time.time() * 1000 + 10 * 60 * 60 * 1000)}, 'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'POINTS', 'programId':0, 'allocationStrategyId':0, 'expirationStrategyId':0}, 'message':'Hi {{first_name}} {{store_id}} https://nightly.capillary.in/campaign/v3/base/CampaignOverview#campaign/302821 {{last_name}} ,Sending SMS via IRIS Automation{{optout}}', 'additionalInfo':{'targetNdnc':False, 'useTinyUrl':True}})
        ])  
    def test_createMessage_sms_ParticularDate_Points_MessageWithAdditionalInfo(self, description, payload):
        payload.update({'incentive':{'type':'POINTS', 'programId':self.programeId, 'allocationStrategyId':self.allocationStrategyId, 'expirationStrategyId':self.expiryStrategyId}})
        response, payload = campaignMessage.createMessage(self, payloadData=payload)
        campaignMessage.assertCreateMessage(response, 200)
        campaignMessage.assertCreateMessageDbCalls(response['json']['entity']['messageId'], self.campaignId, payload)

    @pytest.mark.parametrize('description,payload,statusCode,errorCode,errorMessage', [
        ('MessageType-ParticularDate-Points-MessageWithIncorrectChannel', {'schedule':{'type':'PARTICULAR_DATE', 'datetime':int(time.time() * 1000 + 10 * 60 * 60 * 1000)}, 'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'POINTS', 'programId':0, 'allocationStrategyId':0, 'expirationStrategyId':0}, 'channel':'SM'}, 400, 103, ['Invalid type: Could not resolve type id \'SM\' into a subtype of [simple type, class com.capillary.campaigns.api.data.message.MessageBody]: known type ids = [MessageBody, SMS, WECHAT]']),
        ('MessageType-ParticularDate-Points-MessageWithIncorrectSchedule', {'schedule':{'type':'PARTICULAR_DATE', 'datetime':int(time.time() * 1000 + 10 * 60 * 60 * 1000)}, 'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'POINTS', 'programId':0, 'allocationStrategyId':0, 'expirationStrategyId':0}, 'schedule':{'type':'IMMEDIATEL'}}, 400, 103, ['Invalid type: Could not resolve type id \'IMMEDIATEL\' into a subtype of [simple type, class com.capillary.campaigns.api.data.message.Schedule]: known type ids = [IMMEDIATELY, PARTICULAR_DATE, RECURRING, Schedule]']),
        ('MessageType-ParticularDate-Points-MessageWithIncorrectSenderDetails', {'schedule':{'type':'PARTICULAR_DATE', 'datetime':int(time.time() * 1000 + 10 * 60 * 60 * 1000)}, 'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':'Fals', 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'POINTS', 'programId':0, 'allocationStrategyId':0, 'expirationStrategyId':0}}, 400, 103, ['Invalid type: Can not construct instance of java.lang.Boolean from String value \'SMS\': only "true" or "false" recognized']),
        ('MessageType-ParticularDate-Points-MessageWithIncorrectListId', {'schedule':{'type':'PARTICULAR_DATE', 'datetime':int(time.time() * 1000 + 10 * 60 * 60 * 1000)}, 'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'POINTS', 'programId':0, 'allocationStrategyId':0, 'expirationStrategyId':0}, 'schedule':{'type':'PARTICULAR_DATE', 'datetime':int(time.time() * 1000 + 10 * 60 * 60 * 1000)}, 'senderDetails':{'listId':'null'}}, 400, 103, ['Invalid type: Unrecognized field "listId" (class com.capillary.campaigns.api.data.message.impl.sender.SmsSenderDetails), not marked as ignorable']),
        ('MessageType-ParticularDate-Points-MessageWithIncorrectStoreType', {'schedule':{'type':'PARTICULAR_DATE', 'datetime':int(time.time() * 1000 + 10 * 60 * 60 * 1000)}, 'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'POINTS', 'programId':0, 'allocationStrategyId':0, 'expirationStrategyId':0}, 'storeType':'REGISTERED_STOR'}, 400, 100, ['Invalid request : Valid store type must be provided if store tags are used']),
        ('MessageType-ParticularDate-Points-MessageWithIncorrectAdditionalInfo', {'schedule':{'type':'PARTICULAR_DATE', 'datetime':int(time.time() * 1000 + 10 * 60 * 60 * 1000)}, 'senderDetails':{'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'], 'gsmSenderId':constant.config['message_senders']['gsmSenderId'], 'useSystemDefaults':False, 'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']}, 'incentive':{'type':'POINTS', 'programId':0, 'allocationStrategyId':0, 'expirationStrategyId':0}, 'additionalInfo':{'targetNdnc':'Fal'}}, 400, 103, ['Invalid type: Can not construct instance of boolean from String value \'SMS\': only "true" or "false" recognized'])
        ])
    def test_createMessage_sms_ParticularDate_Points_WrongSchema(self, description, payload, statusCode, errorCode, errorMessage):
        payload.update({'incentive':{'type':'POINTS', 'programId':self.programeId, 'allocationStrategyId':self.allocationStrategyId, 'expirationStrategyId':self.expiryStrategyId}})
        response, payload = campaignMessage.createMessage(self, payloadData=payload)
        campaignMessage.assertCreateMessage(response, statusCode, errorCode, errorMessage)
