import pytest, time, datetime, copy, json, sys
from src.Constant.constant import constant
from src.utilities.randValues import randValues
from src.modules.iris.list import campaignList
from src.utilities.logger import Logger
from src.utilities.assertion import Assertion
from src.modules.iris.campaigns import campaigns
from src.modules.iris.message import campaignMessage
from src.modules.iris.dbCallsCampaign import dbCallsCampaign
from src.modules.iris.dbCallsMessage import dbCallsMessage
from src.modules.iris.dbCallsCoupons import dbCallsCoupons
from src.modules.iris.dbCallsList import dbCallsList
from src.modules.iris.construct import construct
from src.modules.iris.coupons import coupons
from src.modules.iris.authorize import authorize
from src.modules.iris.message import campaignMessage
from src.modules.luci.luciHelper import LuciHelper
from src.modules.luci.luciObject import LuciObject
from src.modules.luci.luciThrift import LuciThrift
from src.modules.inTouchAPI.customer import Customer
from src.modules.inTouchAPI.transaction import Transaction
from src.modules.inTouchAPI.request import Request
from src.modules.inTouchAPI.coupon import Coupon
from src.modules.inTouchAPI.inTouchAPI import InTouchAPI
from src.modules.veneno.venenoDBAssertion import VenenoDBAssertion

@pytest.mark.run(order=1)
class Test_Veneno_ORG():
    
    def setup_class(self):
        if 'storeType' in constant.payload['createmessage'] :constant.payload['createmessage'].pop('storeType')
         
        campaignResponse, campaignPayload = campaigns.createCampaign({'name':'IRIS_' + str(int(time.time() * 100000)), 'goalId':constant.irisGenericValues['goalId'], 'objectiveId':constant.irisGenericValues['objectiveId'], 'testControl':{'type' : 'ORG', 'test' : 90}})
        listResponse, listPayload, campaignId = campaignList.createList({'customTagCount':1, 'name':'IRIS_LIST_' + str(int(time.time() * 100000))}, campaignId=campaignResponse['json']['entity']['campaignId'])
        addRecipientResponse, addRecipientPayload = campaignList.addRecipient({}, campaignId, listResponse['json']['entity']['listId'], 'mobile', 10, 1, newUser=False)
        responseCoupon, payloadCoupon, campaignId = coupons.createCoupons(campaignId=campaignId)

        self.campaignId = campaignId
        self.listId = listResponse['json']['entity']['listId']
        self.voucherId = responseCoupon['json']['entity']['voucherSeriesId']
        self.strategy = construct.constructStrategyIds()
        self.programeId = self.strategy['programeId']
        self.allocationStrategyId = self.strategy['allocationStrategyId']
        self.expiryStrategyId = self.strategy['expirationStrategyId']
        self.bucketId = dbCallsList.getGroupVersionDetailsWithGroupId(listResponse['json']['entity']['listId'])['TEST']['bucket_id']
        self.groupVersionResult = dbCallsList.getGroupVersionDetailsWithGroupId(listResponse['json']['entity']['listId'])
        Logger.log('Veneno Setup Details --> campaignId:{} ,ListId:{} ,voucherId:{} ,strategy:{}, bucketId:{}, groupVersionDetail:{}'.format(self.campaignId, self.listId, self.voucherId, self.strategy, self.bucketId, self.groupVersionResult))
        
    def setup_method(self, method):
        Logger.logMethodName(str(method.__name__))
    
    def couponConfigChange(self, condition):
        Logger.log('Setting Voucher Resent Config to :{} for voucherId :{}'.format(condition, self.voucherId))
        constant.config['campaignId'] = self.campaignId
        port = constant.config['luciPort'].next()
        connObj = LuciThrift(port)
        constructObj = LuciObject()
        
        configRequest = LuciObject.getCouponConfigRequest({'couponSeriesId': self.voucherId})
        couponConfigList = connObj.getCouponConfiguration(configRequest)
        couponConfig = couponConfigList[0].__dict__
        couponConfig.update(condition)
        
        couponConfigObject = LuciObject.couponConfiguration(couponConfig)
        saveCouponConfigObject = LuciObject.saveCouponConfigRequest(couponConfigObject)
        connObj.saveCouponConfiguration(saveCouponConfigObject)
            
    def getAuthorizeResultBody(self, campaignId, listId, groupVersionResult, bucketId, voucherId, strategy, messagePayload, messageId, authorizeResponse, messageInfo=['SMS', ['IMMEDIATE'], ['PLAIN'], True]):
        return {
            'campaignId':campaignId,
            'listId':listId,
            'groupVersionResult':groupVersionResult ,
            'bucketId':bucketId,
            'voucherId':voucherId,
            'strategy':strategy,
            'messageInfo':messageInfo,
            'payload':messagePayload,
            'messageId':messageId,
            'authorizeResponse':authorizeResponse
            }
    
    @pytest.mark.parametrize('description,messageInfo', [
        ('MessageType-Immediate-Plain', ['SMS', ['IMMEDIATE'], ['PLAIN'], True])
        ])
    def test_veneno_inboxUser_ProdSanity(self, description, messageInfo):
        authorizeResult = authorize.authorizeCampaign(self, messageInfo, False)
        authorize.assertAuthorize(authorizeResult['authorizeResponse'], 200)
        communicationDetailId , communicationDetailBucketId , communicationDetailExpectedCount = authorize.assertMessageQueueAndGetCommunicationDetailsForReferenceMessageQueueId(self.campaignId, self.groupVersionResult['TEST']['id'], authorizeResult['messageId'])
        VenenoDBAssertion(self.campaignId, messageInfo[0], communicationDetailId, self.groupVersionResult['TEST']['customer_count'], self.groupVersionResult['TEST']['id'], authorizeResult['payload']['message']).check()
        authorize.assertUserPresenceInNsAdminTable(communicationDetailId , communicationDetailBucketId, int(communicationDetailExpectedCount))
        
    @pytest.mark.parametrize('description,messageInfo', [
        ('MessageType-Immediate-Coupon', ['SMS', ['IMMEDIATE'], ['COUPONS'], True]),
        ('MessageType-Immediate-Point', ['SMS', ['IMMEDIATE'], ['POINTS'], True]),
        ])
    def test_veneno_inboxUser_incentives_generic_ProdSanity(self, description, messageInfo):
        authorizeResult = authorize.authorizeCampaign(self, messageInfo, False)
        authorize.assertAuthorize(authorizeResult['authorizeResponse'], 200)
        communicationDetailId , communicationDetailBucketId , communicationDetailExpectedCount = authorize.assertMessageQueueAndGetCommunicationDetailsForReferenceMessageQueueId(self.campaignId, self.groupVersionResult['TEST']['id'], authorizeResult['messageId'])
        VenenoDBAssertion(self.campaignId, messageInfo[0], communicationDetailId, self.groupVersionResult['TEST']['customer_count'], self.groupVersionResult['TEST']['id'], authorizeResult['payload']['message']).check()
        authorize.assertUserPresenceInNsAdminTable(communicationDetailId , communicationDetailBucketId, int(communicationDetailExpectedCount))
        
    def test_veneno_inboxUser_CustomFiledValue(self):
        obj = InTouchAPI(Customer.Add(body={'root':{'customer':{'custom_fields':{'field':{'name':'gender', 'value':'Male'}}}}}))
        mergeListresponse, mergeListPayload, campaignId = campaignList.mergeList({'name': 'IRIS_LIST_' + str(int(time.time() * 100000)), 'recipients':{'dataSource':'CSV', 'schema':'firstName,lastName,mobile', 'data':['TestX,AutomationX,{}'.format(obj.params['mobile'])]}}, campaignId=self.campaignId)
        self.listId = mergeListresponse['json']['entity']['listId']
        self.groupVersionResult = dbCallsList.getGroupVersionDetailsWithGroupId(mergeListresponse['json']['entity']['listId'])
        self.bucketId = self.groupVersionResult['TEST']['bucket_id']
           
        messagePayloadToUpdate = {
                'senderDetails':{
                    'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'],
                    'gsmSenderId':constant.config['message_senders']['gsmSenderId'],
                    'useSystemDefaults':False,
                    'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']
                },
                'message' : 'This Message is Going to Inbox Due to custom Field Value : {{custom_field.gender}} {{optout}}'
        }
        
        messageResponse, messagePayload = campaignMessage.createMessage(self, payloadData=messagePayloadToUpdate)
        authorizeResponse = authorize.makeAuthorizeRequest(self.campaignId, messageResponse['json']['entity']['messageId'])
        authorizeResult = self.getAuthorizeResultBody(self.campaignId, self.listId, self.groupVersionResult, self.bucketId, self.voucherId, self.strategy, messagePayload, str(messageResponse['json']['entity']['messageId']), authorizeResponse)
        
        communicationDetailId , communicationDetailBucketId , communicationDetailExpectedCount = authorize.assertMessageQueueAndGetCommunicationDetailsForReferenceMessageQueueId(self.campaignId, self.groupVersionResult['TEST']['id'], authorizeResult['messageId'])
        VenenoDBAssertion(self.campaignId, 'SMS', communicationDetailId, self.groupVersionResult['TEST']['customer_count'], self.groupVersionResult['TEST']['id'], authorizeResult['payload']['message']).check()
        authorize.assertUserPresenceInNsAdminTable(communicationDetailId , communicationDetailBucketId, 1)
    
    def test_veneno_inboxUser_GroupTagPresent(self):
        messagePayloadToUpdate = {
                'senderDetails':{
                    'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'],
                    'gsmSenderId':constant.config['message_senders']['gsmSenderId'],
                    'useSystemDefaults':False,
                    'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']
                },
                'message' : 'This Message is Going to Inbox Due to group Tag Present in List :{{group_tag_1}} {{optout}}'
        }
        
        mergeListresponse, mergeListPayload, campaignId = campaignList.mergeList({'groupTags':['TestAutomation_GroupTag1', 'TestAutomation_GroupTag2']}, campaignId=self.campaignId)
        self.listId = mergeListresponse['json']['entity']['listId']
        self.groupVersionResult = dbCallsList.getGroupVersionDetailsWithGroupId(mergeListresponse['json']['entity']['listId'])
        self.bucketId = self.groupVersionResult['TEST']['bucket_id']
           
        messageResponse, messagePayload = campaignMessage.createMessage(self, payloadData=messagePayloadToUpdate)
        authorizeResponse = authorize.makeAuthorizeRequest(self.campaignId, messageResponse['json']['entity']['messageId'])
        authorizeResult = self.getAuthorizeResultBody(self.campaignId, self.listId, self.groupVersionResult, self.bucketId, self.voucherId, self.strategy, messagePayload, str(messageResponse['json']['entity']['messageId']), authorizeResponse)
        
        communicationDetailId , communicationDetailBucketId , communicationDetailExpectedCount = authorize.assertMessageQueueAndGetCommunicationDetailsForReferenceMessageQueueId(self.campaignId, self.groupVersionResult['TEST']['id'], authorizeResult['messageId'])
        VenenoDBAssertion(self.campaignId, 'SMS', communicationDetailId, self.groupVersionResult['TEST']['customer_count'], self.groupVersionResult['TEST']['id'], authorizeResult['payload']['message']).check()
        authorize.assertUserPresenceInNsAdminTable(communicationDetailId , communicationDetailBucketId, 1)

    def test_veneno_skippedUser_nonLoyaltyCustomer(self):
        originalListId = self.listId
        originalBucketId = self.bucketId
        originalGroupVersionDetail = self.groupVersionResult
        try:
            messagePayloadToUpdate = {
                'senderDetails':{
                    'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'],
                    'gsmSenderId':constant.config['message_senders']['gsmSenderId'],
                    'useSystemDefaults':False,
                    'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']
                    },
                'message' : 'This Message is Going to Skip Due to Loyalty Tag used :{{loyalty_points}} {{optout}}'
            }
    
            mergeListresponse, mergeListPayload, campaignId = campaignList.mergeList({}, campaignId=self.campaignId)
            self.listId = mergeListresponse['json']['entity']['listId']
            self.groupVersionResult = dbCallsList.getGroupVersionDetailsWithGroupId(mergeListresponse['json']['entity']['listId'])
            self.bucketId = self.groupVersionResult['TEST']['bucket_id']
           
            messageResponse, messagePayload = campaignMessage.createMessage(self, payloadData=messagePayloadToUpdate)
            authorizeResponse = authorize.makeAuthorizeRequest(self.campaignId, messageResponse['json']['entity']['messageId'])
            authorizeResult = self.getAuthorizeResultBody(self.campaignId, self.listId, self.groupVersionResult, self.bucketId, self.voucherId, self.strategy, messagePayload, str(messageResponse['json']['entity']['messageId']), authorizeResponse)
            communicationDetailId , communicationDetailBucketId, communicationDetailExpectedCount = authorize.assertMessageQueueAndGetCommunicationDetailsForReferenceMessageQueueId(self.campaignId, self.groupVersionResult['TEST']['id'], authorizeResult['messageId'])
            VenenoDBAssertion(self.campaignId, 'SMS', communicationDetailId, self.groupVersionResult['TEST']['customer_count'], self.groupVersionResult['TEST']['id'], authorizeResult['payload']['message'], skippedReasons=['Users are not registered in loyalty program']).check()
            authorize.assertUserPresenceInSkippedTable(communicationDetailId, communicationDetailBucketId, constant.config['skipped_errors']['NON_LOYALTY_CUSTOMER'], 'Users are not registered in loyalty program')
        except Exception, exp:
            Assertion.constructAssertion(False, exp)
        finally:
            self.listId = originalListId
            self.groupVersionResult = originalGroupVersionDetail
            self.bucketId = originalBucketId

    @pytest.mark.parametrize('storeType,errorType,errorMessage', [
        ('REGISTERED_STORE', constant.config['skipped_errors']['NO_STORE'], 'No entry for store present'),
        ('LAST_TRANSACTED_AT', constant.config['skipped_errors']['NO_LAST_SHOPPED_STORE'], 'No entry for last shopped store present'),
        ])
    def test_veneno_skippedUser_noStore(self, storeType, errorType, errorMessage):
        originalListId = self.listId
        originalBucketId = self.bucketId
        originalGroupVersionDetail = self.groupVersionResult
        try:
            messagePayloadToUpdate = {
                'senderDetails':{
                    'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'],
                    'gsmSenderId':constant.config['message_senders']['gsmSenderId'],
                    'useSystemDefaults':False,
                    'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']
                },
                'message' : 'This Message is Going to Skip Due to Store Name Tag used :{{store_name}} {{optout}}',
                'storeType' : storeType
            }
            
            mergeListresponse, mergeListPayload, campaignId = campaignList.mergeList({}, campaignId=self.campaignId)
            self.listId = mergeListresponse['json']['entity']['listId']
            self.groupVersionResult = dbCallsList.getGroupVersionDetailsWithGroupId(mergeListresponse['json']['entity']['listId'])
            self.bucketId = self.groupVersionResult['TEST']['bucket_id']
           
            messageResponse, messagePayload = campaignMessage.createMessage(self, payloadData=messagePayloadToUpdate)
            authorizeResponse = authorize.makeAuthorizeRequest(self.campaignId, messageResponse['json']['entity']['messageId'])
            authorizeResult = self.getAuthorizeResultBody(self.campaignId, self.listId, self.groupVersionResult, self.bucketId, self.voucherId, self.strategy, messagePayload, str(messageResponse['json']['entity']['messageId']), authorizeResponse)
            communicationDetailId , communicationDetailBucketId, communicationDetailExpectedCount = authorize.assertMessageQueueAndGetCommunicationDetailsForReferenceMessageQueueId(self.campaignId, self.groupVersionResult['TEST']['id'], authorizeResult['messageId'])
            VenenoDBAssertion(self.campaignId, 'SMS', communicationDetailId, self.groupVersionResult['TEST']['customer_count'], self.groupVersionResult['TEST']['id'], authorizeResult['payload']['message'], skippedReasons=[errorMessage]).check()
            authorize.assertUserPresenceInSkippedTable(communicationDetailId, communicationDetailBucketId, errorType, errorMessage)
        except Exception, exp:
            Assertion.constructAssertion(False, exp)
        finally:
            self.listId = originalListId
            self.groupVersionResult = originalGroupVersionDetail
            self.bucketId = originalBucketId
        
    def test_veneno_skippedUser_noCustomFieldValue(self):
        messagePayloadToUpdate = {
                'senderDetails':{
                    'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'],
                    'gsmSenderId':constant.config['message_senders']['gsmSenderId'],
                    'useSystemDefaults':False,
                    'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']
                },
                'message' : 'This Message is Going to Skip Due to More Custom Tags then used in List :{{custom_tag_1}} {{custom_tag_2}} {{optout}}'
        }
        
        messageResponse, messagePayload = campaignMessage.createMessage(self, payloadData=messagePayloadToUpdate)
        authorizeResponse = authorize.makeAuthorizeRequest(self.campaignId, messageResponse['json']['entity']['messageId'])
        authorizeResult = self.getAuthorizeResultBody(self.campaignId, self.listId, self.groupVersionResult, self.bucketId, self.voucherId, self.strategy, messagePayload, str(messageResponse['json']['entity']['messageId']), authorizeResponse)
        communicationDetailId , communicationDetailBucketId, communicationDetailExpectedCount = authorize.assertMessageQueueAndGetCommunicationDetailsForReferenceMessageQueueId(self.campaignId, self.groupVersionResult['TEST']['id'], authorizeResult['messageId'])
        VenenoDBAssertion(self.campaignId, 'SMS', communicationDetailId, self.groupVersionResult['TEST']['customer_count'], self.groupVersionResult['TEST']['id'], authorizeResult['payload']['message'], skippedReasons=['Custom Tag Not Present']).check()
        authorize.assertUserPresenceInSkippedTable(communicationDetailId, communicationDetailBucketId, constant.config['skipped_errors']['CUSTOM_TAG_NOT_PRESENT'], 'Custom Tag Not Present')
        
    def test_veneno_skippedUser_NDNC_Sanity(self):
        originalListId = self.listId
        originalBucketId = self.bucketId
        originalGroupVersionDetail = self.groupVersionResult
        try:
            messagePayloadToUpdate = {
                'senderDetails':{
                    'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'],
                    'gsmSenderId':constant.config['message_senders']['gsmSenderId'],
                    'useSystemDefaults':False,
                    'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']
                },
                'message' : 'This Message is Going to Skip Due to List Have NDNC users only : {{optout}}'
            }
            ndncUserData = 'ndncFirstName,ndncLastName,{}'.format(dbCallsMessage.getNDNCUserMobileNumber()[0])
            mergeListresponse, mergeListPayload, campaignId = campaignList.mergeList({'name': 'IRIS_LIST_NDNC' + str(int(time.time() * 100000)), 'recipients':{'dataSource':'CSV', 'schema':'firstName,lastName,mobile', 'data':[ndncUserData]}}, campaignId=self.campaignId)
            self.listId = mergeListresponse['json']['entity']['listId']
            self.groupVersionResult = dbCallsList.getGroupVersionDetailsWithGroupId(mergeListresponse['json']['entity']['listId'])
            self.bucketId = self.groupVersionResult['TEST']['bucket_id']
           
            messageResponse, messagePayload = campaignMessage.createMessage(self, payloadData=messagePayloadToUpdate)
            authorizeResponse = authorize.makeAuthorizeRequest(self.campaignId, messageResponse['json']['entity']['messageId'])
            authorizeResult = self.getAuthorizeResultBody(self.campaignId, self.listId, self.groupVersionResult, self.bucketId, self.voucherId, self.strategy, messagePayload, str(messageResponse['json']['entity']['messageId']), authorizeResponse)
            communicationDetailId , communicationDetailBucketId, communicationDetailExpectedCount = authorize.assertMessageQueueAndGetCommunicationDetailsForReferenceMessageQueueId(self.campaignId, self.groupVersionResult['TEST']['id'], authorizeResult['messageId'])
            VenenoDBAssertion(self.campaignId, 'SMS', communicationDetailId, self.groupVersionResult['TEST']['customer_count'], self.groupVersionResult['TEST']['id'], authorizeResult['payload']['message'], skippedReasons=['User has an NDNC mobile.']).check()
            authorize.assertUserPresenceInSkippedTable(communicationDetailId, communicationDetailBucketId, constant.config['skipped_errors']['NDNC'], 'User has an NDNC mobile.')
        except Exception, exp:
            Assertion.constructAssertion(False, exp)
        finally:
            self.listId = originalListId
            self.groupVersionResult = originalGroupVersionDetail
            self.bucketId = originalBucketId
    
    def test_veneno_skippedUser_invalidMobile(self):
        originalListId = self.listId
        originalBucketId = self.bucketId
        originalGroupVersionDetail = self.groupVersionResult
        try:
            messagePayloadToUpdate = {
                'senderDetails':{
                    'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'],
                    'gsmSenderId':constant.config['message_senders']['gsmSenderId'],
                    'useSystemDefaults':False,
                    'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']
                },
                'message' : 'This Message is Going to Skip Due Invalid User : {{optout}}'
            }
            invalidUserData = 'ndncFirstName,ndncLastName,{}'.format(dbCallsMessage.getInvalidUserMobileNumber()[0])
            mergeListresponse, mergeListPayload, campaignId = campaignList.mergeList({'name': 'IRIS_LIST_' + str(int(time.time() * 100000)), 'recipients':{'dataSource':'CSV', 'schema':'firstName,lastName,mobile', 'data':[invalidUserData]}}, campaignId=self.campaignId)
            self.listId = mergeListresponse['json']['entity']['listId']
            self.groupVersionResult = dbCallsList.getGroupVersionDetailsWithGroupId(mergeListresponse['json']['entity']['listId'])
            self.bucketId = self.groupVersionResult['TEST']['bucket_id']
           
            messageResponse, messagePayload = campaignMessage.createMessage(self, payloadData=messagePayloadToUpdate)
            authorizeResponse = authorize.makeAuthorizeRequest(self.campaignId, messageResponse['json']['entity']['messageId'])
            authorizeResult = self.getAuthorizeResultBody(self.campaignId, self.listId, self.groupVersionResult, self.bucketId, self.voucherId, self.strategy, messagePayload, str(messageResponse['json']['entity']['messageId']), authorizeResponse)
            communicationDetailId , communicationDetailBucketId, communicationDetailExpectedCount = authorize.assertMessageQueueAndGetCommunicationDetailsForReferenceMessageQueueId(self.campaignId, self.groupVersionResult['TEST']['id'], authorizeResult['messageId'])
            VenenoDBAssertion(self.campaignId, 'SMS', communicationDetailId, self.groupVersionResult['TEST']['customer_count'], self.groupVersionResult['TEST']['id'], authorizeResult['payload']['message'], skippedReasons=['Captured mobile for user seems to be invalid']).check()
            authorize.assertUserPresenceInSkippedTable(communicationDetailId, communicationDetailBucketId, constant.config['skipped_errors']['INVALID_MOBILE'], 'Captured mobile for user seems to be invalid')
        except Exception, exp:
            Assertion.constructAssertion(False, exp)
        finally:
            self.listId = originalListId
            self.groupVersionResult = originalGroupVersionDetail
            self.bucketId = originalBucketId
    
    def test_veneno_skippedUser_noGroupTagPresent(self):
        messagePayloadToUpdate = {
                'senderDetails':{
                    'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'],
                    'gsmSenderId':constant.config['message_senders']['gsmSenderId'],
                    'useSystemDefaults':False,
                    'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']
                },
                'message' : 'This Message is Going to Skip Due to group Tag Not Present in List :{{group_tag_1}} {{optout}}'
        }
        
        messageResponse, messagePayload = campaignMessage.createMessage(self, payloadData=messagePayloadToUpdate)
        authorizeResponse = authorize.makeAuthorizeRequest(self.campaignId, messageResponse['json']['entity']['messageId'])
        authorizeResult = self.getAuthorizeResultBody(self.campaignId, self.listId, self.groupVersionResult, self.bucketId, self.voucherId, self.strategy, messagePayload, str(messageResponse['json']['entity']['messageId']), authorizeResponse)
        communicationDetailId , communicationDetailBucketId, communicationDetailExpectedCount = authorize.assertMessageQueueAndGetCommunicationDetailsForReferenceMessageQueueId(self.campaignId, self.groupVersionResult['TEST']['id'], authorizeResult['messageId'])
        VenenoDBAssertion(self.campaignId, 'SMS', communicationDetailId, self.groupVersionResult['TEST']['customer_count'], self.groupVersionResult['TEST']['id'], authorizeResult['payload']['message'], skippedReasons=['Group Tag Not Present']).check()
        authorize.assertUserPresenceInSkippedTable(communicationDetailId, communicationDetailBucketId, constant.config['skipped_errors']['GROUP_TAG_NOT_PRESENT'], 'Group Tag Not Present')
            
    def test_veneno_skippedUser_unsubscribed(self):
        originalListId = self.listId
        originalBucketId = self.bucketId
        originalGroupVersionDetail = self.groupVersionResult
        try:
            messagePayloadToUpdate = {
                'senderDetails':{
                    'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'],
                    'gsmSenderId':constant.config['message_senders']['gsmSenderId'],
                    'useSystemDefaults':False,
                    'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']
                },
                'message' : 'This Message is Going to Skip Due Unsubscribe User : {{optout}}'
            }
            
            cusObj = InTouchAPI(Customer.Add())
            mergeListresponse, mergeListPayload, campaignId = campaignList.mergeList({'name': 'IRIS_LIST_' + str(int(time.time() * 100000)), 'recipients':{'dataSource':'CSV', 'schema':'firstName,lastName,mobile', 'data':['TestX,AutomationX,{}'.format(cusObj.params['mobile'])]}}, campaignId=self.campaignId)
            self.listId = mergeListresponse['json']['entity']['listId']
            self.groupVersionResult = dbCallsList.getGroupVersionDetailsWithGroupId(mergeListresponse['json']['entity']['listId'])
            self.bucketId = self.groupVersionResult['TEST']['bucket_id']
            
            unsubscribeObj = InTouchAPI(Customer.unsubscribe(body={'root':{'subscription':{'mobile':cusObj.params['mobile']}}}))
            if unsubscribeObj.status_code == 200:
                messageResponse, messagePayload = campaignMessage.createMessage(self, payloadData=messagePayloadToUpdate)
                authorizeResponse = authorize.makeAuthorizeRequest(self.campaignId, messageResponse['json']['entity']['messageId'])
                authorizeResult = self.getAuthorizeResultBody(self.campaignId, self.listId, self.groupVersionResult, self.bucketId, self.voucherId, self.strategy, messagePayload, str(messageResponse['json']['entity']['messageId']), authorizeResponse)
                communicationDetailId , communicationDetailBucketId, communicationDetailExpectedCount = authorize.assertMessageQueueAndGetCommunicationDetailsForReferenceMessageQueueId(self.campaignId, self.groupVersionResult['TEST']['id'], authorizeResult['messageId'])
                VenenoDBAssertion(self.campaignId, 'SMS', communicationDetailId, self.groupVersionResult['TEST']['customer_count'], self.groupVersionResult['TEST']['id'], authorizeResult['payload']['message'], skippedReasons=['Captured mobile for user seems to be unsubscribed']).check()
                authorize.assertUserPresenceInSkippedTable(communicationDetailId, communicationDetailBucketId, constant.config['skipped_errors']['UNSUBSCRIBED'], 'Captured mobile for user seems to be unsubscribed')
            else :
                raise Exception('Not Able To Unsubscribe using Intouch Call')
        except Exception, exp:
            Assertion.constructAssertion(False, exp)
        finally:
            self.listId = originalListId
            self.groupVersionResult = originalGroupVersionDetail
            self.bucketId = originalBucketId  
    
    def test_veneno_skippedUser_couponReedemed(self):
        try:
            cusObj = InTouchAPI(Transaction.Add())

            mergeListresponse, mergeListPayload, campaignId = campaignList.mergeList({'name': 'IRIS_LIST_' + str(int(time.time() * 100000)), 'recipients':{'dataSource':'CSV', 'schema':'firstName,lastName,mobile', 'data':['TestX,AutomationX,{}'.format(cusObj.params['mobile'])]}}, campaignId=self.campaignId)
            self.listId = mergeListresponse['json']['entity']['listId']
            self.groupVersionResult = dbCallsList.getGroupVersionDetailsWithGroupId(mergeListresponse['json']['entity']['listId'])
            self.bucketId = self.groupVersionResult['TEST']['bucket_id']
           
            self.couponConfigChange({'allow_multiple_vouchers_per_user':False,'same_user_multiple_redeem':False,'multiple_use':False})
            time.sleep(70)
            messagePayloadToUpdate = {
                    'incentive':{
                        'type':'COUPONS',
                        'voucherSeriesId':self.voucherId
                    },
                    'senderDetails':{
                        'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'],
                        'gsmSenderId':constant.config['message_senders']['gsmSenderId'],
                        'useSystemDefaults':False,
                        'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']
                    },
                    'message' : 'This Message is Going to Skip Due to Coupon has already been redeemed : {{voucher}} {{optout}}'
            }
            
            messageResponse, messagePayload = campaignMessage.createMessage(self, payloadData=messagePayloadToUpdate)
            authorizeResponse = authorize.makeAuthorizeRequest(self.campaignId, messageResponse['json']['entity']['messageId'])
            
            custObjResponse = cusObj.response  # json.loads(cusObj.response.replace("'", "\""))
            couponCode = dbCallsCoupons.getCouponCode(self.voucherId, custObjResponse['response']['transactions']['transaction'][0]['customer']['user_id'])
            coupObj = InTouchAPI(Coupon.Redeem(body={'root':{'coupon':{'transaction':{'number':cusObj.params['transactionId'], 'amount':100}}}}, mobile=cusObj.params['mobile'], code=couponCode))
            messageResponse, messagePayload = campaignMessage.createMessage(self, payloadData=messagePayloadToUpdate)
            authorizeResponse = authorize.makeAuthorizeRequest(self.campaignId, messageResponse['json']['entity']['messageId'])
            authorizeResult = self.getAuthorizeResultBody(self.campaignId, self.listId, self.groupVersionResult, self.bucketId, self.voucherId, self.strategy, messagePayload, str(messageResponse['json']['entity']['messageId']), authorizeResponse)
            communicationDetailId , communicationDetailBucketId, communicationDetailExpectedCount = authorize.assertMessageQueueAndGetCommunicationDetailsForReferenceMessageQueueId(self.campaignId, self.groupVersionResult['TEST']['id'], authorizeResult['messageId'])
            VenenoDBAssertion(self.campaignId, 'SMS', communicationDetailId, self.groupVersionResult['TEST']['customer_count'], self.groupVersionResult['TEST']['id'], authorizeResult['payload']['message'], skippedReasons=['Coupon For user was already redeemed.']).check()
            authorize.assertUserPresenceInSkippedTable(communicationDetailId, communicationDetailBucketId, constant.config['skipped_errors']['COUPON_REDEEMED'], 'Coupon For user was already redeemed.')
        except Exception, exp:
            Assertion.constructAssertion(False, exp)
        finally:
            self.couponConfigChange({'allow_multiple_vouchers_per_user':True,'same_user_multiple_redeem':True,'multiple_use':True})
    
    def test_veneno_skippedUser_couponAlreadyIssued(self):
        try:
            self.couponConfigChange({'do_not_resend_existing_voucher':True})
            time.sleep(70)
            messagePayloadToUpdate = {
                    'incentive':{
                        'type':'COUPONS',
                        'voucherSeriesId':self.voucherId
                    },
                    'senderDetails':{
                        'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'],
                        'gsmSenderId':constant.config['message_senders']['gsmSenderId'],
                        'useSystemDefaults':False,
                        'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']
                    },
                    'message' : 'This Message is Going to Skip Due to Coupon is not reusable : {{voucher}} {{optout}}'
            }
            
            messageResponse, messagePayload = campaignMessage.createMessage(self, payloadData=messagePayloadToUpdate)
            authorizeResponse = authorize.makeAuthorizeRequest(self.campaignId, messageResponse['json']['entity']['messageId'])
            
            messageResponse, messagePayload = campaignMessage.createMessage(self, payloadData=messagePayloadToUpdate)
            authorizeResponse = authorize.makeAuthorizeRequest(self.campaignId, messageResponse['json']['entity']['messageId'])
            authorizeResult = self.getAuthorizeResultBody(self.campaignId, self.listId, self.groupVersionResult, self.bucketId, self.voucherId, self.strategy, messagePayload, str(messageResponse['json']['entity']['messageId']), authorizeResponse)
            communicationDetailId , communicationDetailBucketId, communicationDetailExpectedCount = authorize.assertMessageQueueAndGetCommunicationDetailsForReferenceMessageQueueId(self.campaignId, self.groupVersionResult['TEST']['id'], authorizeResult['messageId'])
            VenenoDBAssertion(self.campaignId, 'SMS', communicationDetailId, self.groupVersionResult['TEST']['customer_count'], self.groupVersionResult['TEST']['id'], authorizeResult['payload']['message'], skippedReasons=['max coupon per user exceeded']).check()
            authorize.assertUserPresenceInSkippedTable(communicationDetailId, communicationDetailBucketId, constant.config['skipped_errors']['MAX_COUPON_ISSUAL_PER_USER_EXCEEDED'], 'max coupon per user exceeded')
        except Exception, exp:
            Assertion.constructAssertion(False, exp)
        finally:
            self.couponConfigChange({'do_not_resend_existing_voucher':False})
    
    def test_veneno_skippedUser_noCouponForUser(self):
        try:
            mergeListresponse, mergeListPayload, campaignId = campaignList.mergeList(campaignId=self.campaignId, numberOfUsers=2)
            self.listId = mergeListresponse['json']['entity']['listId']
            self.groupVersionResult = dbCallsList.getGroupVersionDetailsWithGroupId(mergeListresponse['json']['entity']['listId'])
            self.bucketId = self.groupVersionResult['TEST']['bucket_id']
           
            self.couponConfigChange({'max_create':1,'max_redeem':1})
            time.sleep(70)
            messagePayloadToUpdate = {
                    'incentive':{
                        'type':'COUPONS',
                        'voucherSeriesId':self.voucherId
                    },
                    'senderDetails':{
                        'domainGatewayMapId':constant.config['message_senders']['domainGatewayMapId'],
                        'gsmSenderId':constant.config['message_senders']['gsmSenderId'],
                        'useSystemDefaults':False,
                        'cdmaSenderId':constant.config['message_senders']['cdmaSenderId']
                    },
                    'message' : 'This Message is Going to Skip Due to number of Issued coupon is 1 and users are 2 : {{voucher}} {{optout}}'
            }
            
            messageResponse, messagePayload = campaignMessage.createMessage(self, payloadData=messagePayloadToUpdate)
            authorizeResponse = authorize.makeAuthorizeRequest(self.campaignId, messageResponse['json']['entity']['messageId'])
            authorizeResult = self.getAuthorizeResultBody(self.campaignId, self.listId, self.groupVersionResult, self.bucketId, self.voucherId, self.strategy, messagePayload, str(messageResponse['json']['entity']['messageId']), authorizeResponse)
            communicationDetailId , communicationDetailBucketId, communicationDetailExpectedCount = authorize.assertMessageQueueAndGetCommunicationDetailsForReferenceMessageQueueId(self.campaignId, self.groupVersionResult['TEST']['id'], authorizeResult['messageId'])
            VenenoDBAssertion(self.campaignId, 'SMS', communicationDetailId, self.groupVersionResult['TEST']['customer_count'], self.groupVersionResult['TEST']['id'], authorizeResult['payload']['message'], skippedReasons=['max create for series exceeded']).check()
            authorize.assertUserPresenceInSkippedTable(communicationDetailId, communicationDetailBucketId, constant.config['skipped_errors']['MAX_COUPON_ISSUAL_PER_SERIES_EXCEEDED'], 'max create for series exceeded')
        except Exception, exp:
            Assertion.constructAssertion(False, exp)
        finally:
            self.couponConfigChange({'max_create':-1,'max_redeem':-1})

    def test_veneno_skippedUser_couponExpired(self):
        try:
            self.couponConfigChange({'fixedExpiryDate': int(time.time() * 1000 - 24 * 60 * 60 * 1000)})
            time.sleep(70)
            messagePayloadToUpdate = {
                'incentive': {
                    'type': 'COUPONS',
                    'voucherSeriesId': self.voucherId
                },
                'senderDetails': {
                    'domainGatewayMapId': constant.config['message_senders']['domainGatewayMapId'],
                    'gsmSenderId': constant.config['message_senders']['gsmSenderId'],
                    'useSystemDefaults': False,
                    'cdmaSenderId': constant.config['message_senders']['cdmaSenderId']
                },
                'message': 'This Message is Going to Skip Due to Coupon not issuable as its Expired : {{voucher}} {{optout}}'
            }

            messageResponse, messagePayload = campaignMessage.createMessage(self, payloadData=messagePayloadToUpdate)
            authorizeResponse = authorize.makeAuthorizeRequest(self.campaignId,
                                                               messageResponse['json']['entity']['messageId'])

            messageResponse, messagePayload = campaignMessage.createMessage(self, payloadData=messagePayloadToUpdate)
            authorizeResponse = authorize.makeAuthorizeRequest(self.campaignId,
                                                               messageResponse['json']['entity']['messageId'])
            authorizeResult = self.getAuthorizeResultBody(self.campaignId, self.listId, self.groupVersionResult,
                                                          self.bucketId, self.voucherId, self.strategy, messagePayload,
                                                          str(messageResponse['json']['entity']['messageId']),
                                                          authorizeResponse)
            communicationDetailId, communicationDetailBucketId, communicationDetailExpectedCount = authorize.assertMessageQueueAndGetCommunicationDetailsForReferenceMessageQueueId(
                self.campaignId, self.groupVersionResult['TEST']['id'], authorizeResult['messageId'])
            VenenoDBAssertion(self.campaignId, 'SMS', communicationDetailId,
                              self.groupVersionResult['TEST']['customer_count'], self.groupVersionResult['TEST']['id'],
                              authorizeResult['payload']['message'], skippedReasons=['coupon series expired']).check()
            authorize.assertUserPresenceInSkippedTable(communicationDetailId, communicationDetailBucketId,
                                                       constant.config['skipped_errors']['COUPON_EXPIRED'],
                                                       'coupon series expired')
        except Exception, exp:
            Assertion.constructAssertion(False, exp)
        finally:
            self.couponConfigChange({'fixedExpiryDate': int(time.time() * 1000 + 24 * 60 * 60 * 1000)})
