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

@pytest.mark.run(order=10)
@pytest.mark.skipif(constant.config['cluster'] not in ['nightly'], reason = 'Wechat Configured only in nightly')
class Test_Wechat_CreateMessage():
    
    def setup_method(self, method):
        Logger.logMethodName(method.__name__)
    
    def setup_class(self):
        campaignMessage.getWeCRMTemplates()
        self.nonWechatOrgId = construct.updateOrgId(constant.config['wechat_org_id'])
        self.templateIdDict = campaignMessage.setupTemplateId()
        createListresponse, createListPayload, campaignId = campaignList.createList({'customTagCount':0, 'name':'IRIS_LIST_' + str(int(time.time() * 100000))}, campaignId=Test_Wechat_CreateMessage.createCampaign())
        campaignList.assertCreateList(createListresponse, 200)
        groupVersionDetailResult, bucketId = campaignList.assertCreateListDbCalls(createListresponse['json']['entity']['listId'], createListPayload, 'ORG')
        Logger.log('GroupVersionId : {}, bucketId : {}'.format(groupVersionDetailResult, bucketId))
        addRecipientResponse, addRecipientPayload = campaignList.addRecipient(Test_Wechat_CreateMessage.addRecipientPayload(), campaignId, createListresponse['json']['entity']['listId'])
        campaignList.assertAddRecipient(addRecipientResponse, 200)
        responseCoupon, payloadCoupon, campaignId = coupons.createCoupons(campaignId=campaignId)
        self.groupVersionResult = dbCallsList.getGroupVersionDetailsWithGroupId(createListresponse['json']['entity']['listId'])
        self.bucketId = bucketId
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
        
    def teardown_class(self):
        construct.updateOrgId(self.nonWechatOrgId)
        Logger.log('Default Object Set is :', constant.messagesDefault)

    @staticmethod
    def createCampaign():
        response, payload = campaigns.createCampaign({'name': 'IRIS_' + str(int(time.time())), 'goalId': constant.irisGenericValues['goalId'],'objectiveId': constant.irisGenericValues['objectiveId']})
        campaigns.assertCreateCampaign(response, 200)
        campaigns.assertCreateCampaignDBCall(response['json']['entity']['campaignId'], payload)
        return response['json']['entity']['campaignId']

    @staticmethod
    def addRecipientPayload():
        payload = { 'schema' : 'firstName,lastName,userId',
                    'dataSource': 'CSV',
                    'data' : ['Test1,Automation1,' + str(constant.config['wechat']['user'][0]['userId'])]}
        return payload
        
    @pytest.mark.parametrize('description,messageInfo', [
        ('MessageType-Immediate-Plain', ['WECHAT', ['IMMEDIATE'], ['PLAIN'], True]),
        ('MessageType-ParticularDate-Plain',['WECHAT', ['PARTICULARDATE', int(time.time() * 1000 + 5 * 60 * 60 * 1000)], ['PLAIN'], True])
        ])
    def test_wechat_createMessage_Plain_Sanity(self, description, messageInfo):
        response, payload = campaignMessage.createMessage(self, messageInfo=messageInfo)
        campaignMessage.assertCreateMessage(response, 200)
        campaignMessage.assertCreateMessageDbCalls(response['json']['entity']['messageId'], self.campaignId, payload)
        campaignMessage.updateDefaultMessageJsonWithMessageInfoValues(messageInfo, payload, response['json']['entity']['messageId'])
        
    @pytest.mark.parametrize('description,messageInfo', [
        ('MessageType-Immediate-Plain', ['WECHAT', ['IMMEDIATE'], ['PLAIN'], False]),
        ('MessageType-ParticularDate-Plain', ['WECHAT', ['PARTICULARDATE', int(time.time() * 1000 + 5 * 60 * 60 * 1000)], ['PLAIN'], False]),
        ])
    def test_wechat_createMessage_Plain_systemDefault_False(self, description, messageInfo):
        response, payload = campaignMessage.createMessage(self, messageInfo=messageInfo)
        campaignMessage.assertCreateMessage(response, 200)
        campaignMessage.assertCreateMessageDbCalls(response['json']['entity']['messageId'], self.campaignId, payload)
        campaignMessage.updateDefaultMessageJsonWithMessageInfoValues(messageInfo, payload, response['json']['entity']['messageId'])
        
    @pytest.mark.parametrize('description,messageInfo', [
        ('MessageType-Immediate-Plain', ['WECHAT', ['IMMEDIATE'], ['Generic'], True]),
        ('MessageType-ParticularDate-Plain', ['WECHAT', ['PARTICULARDATE', int(time.time() * 1000 + 5 * 60 * 60 * 1000)], ['Generic'], True]),
        ('MessageType-Immediate-Plain_systemDefault_False', ['WECHAT', ['IMMEDIATE'], ['Generic'], False]),
        ('MessageType-ParticularDate-Plain_systemDefault_False', ['WECHAT', ['PARTICULARDATE', int(time.time() * 1000 + 5 * 60 * 60 * 1000)], ['Generic'], False]),
        ])        
    def test_wechat_createMessage_Generic(self, description, messageInfo):
        response, payload = campaignMessage.createMessage(self, messageInfo=messageInfo)
        campaignMessage.assertCreateMessage(response, 200)
        campaignMessage.assertCreateMessageDbCalls(response['json']['entity']['messageId'], self.campaignId, payload)
        campaignMessage.updateDefaultMessageJsonWithMessageInfoValues(messageInfo, payload, response['json']['entity']['messageId'])
        
    @pytest.mark.parametrize('description,messageInfo', [
        ('MessageType-Immediate-Plain', ['WECHAT', ['IMMEDIATE'], ['COUPONS'], True]),
        ('MessageType-ParticularDate-Plain', ['WECHAT', ['PARTICULARDATE', int(time.time() * 1000 + 5 * 60 * 60 * 1000)], ['COUPONS'], True]),
        ('MessageType-Immediate-Plain_systemDefault_False', ['WECHAT', ['IMMEDIATE'], ['COUPONS'], False]),
        ('MessageType-ParticularDate-Plain_systemDefault_False', ['WECHAT', ['PARTICULARDATE', int(time.time() * 1000 + 5 * 60 * 60 * 1000)], ['COUPONS'], False]),
        ])        
    def test_wechat_createMessage_Coupon(self, description, messageInfo):
        response, payload = campaignMessage.createMessage(self, messageInfo=messageInfo)
        campaignMessage.assertCreateMessage(response, 200)
        campaignMessage.assertCreateMessageDbCalls(response['json']['entity']['messageId'], self.campaignId, payload)
        campaignMessage.updateDefaultMessageJsonWithMessageInfoValues(messageInfo, payload, response['json']['entity']['messageId'])
        
    @pytest.mark.parametrize('description,messageInfo', [
        ('MessageType-Immediate-Plain', ['WECHAT', ['IMMEDIATE'], ['POINTS'], True]),
        ('MessageType-ParticularDate-Plain', ['WECHAT', ['PARTICULARDATE', int(time.time() * 1000 + 5 * 60 * 60 * 1000)], ['POINTS'], True ]),
        ('MessageType-Immediate-Plain_systemDefault_False', ['WECHAT', ['IMMEDIATE'], ['POINTS'], False]),
        ('MessageType-ParticularDate-Plain_systemDefault_False', ['WECHAT', ['PARTICULARDATE', int(time.time() * 1000 + 5 * 60 * 60 * 1000)], ['POINTS'], False ]),
        ])        
    def test_wechat_createMessage_Points(self, description, messageInfo):
        response, payload = campaignMessage.createMessage(self, messageInfo=messageInfo)
        campaignMessage.assertCreateMessage(response, 200)
        campaignMessage.assertCreateMessageDbCalls(response['json']['entity']['messageId'], self.campaignId, payload)
        campaignMessage.updateDefaultMessageJsonWithMessageInfoValues(messageInfo, payload, response['json']['entity']['messageId'])

    @pytest.mark.parametrize('description,payload, incentives', [
        ('MessageType-Immediate-Plain',{'channel' : 'WECHAT','accountDetails': construct.constructAccountDetails()}, 'PLAIN'),
        ('MessageType-Immediate-Generic',{'channel' : 'WECHAT','accountDetails': construct.constructAccountDetails()}, 'GENERIC'),
        ('MessageType-Immediate-Coupons',{'channel' : 'WECHAT','accountDetails': construct.constructAccountDetails()}, 'COUPONS'),
        ('MessageType-Immediate-Points',{'channel' : 'WECHAT','accountDetails': construct.constructAccountDetails()}, 'POINTS'),
    ])
    def test_wechat_createMessage_using_templateIds(self, description, payload, incentives):
        payload.update({'templateId' : self.templateIdDict[incentives.lower()]})
        if incentives.lower() == 'coupons':
            payload.update({'incentive' : construct.constructIncentivesForCreateMessage([incentives,self.voucherId])})
        if incentives.lower() != 'plain' and incentives.lower() != 'coupons':
            payload.update({'incentive' : construct.constructIncentivesForCreateMessage([incentives])})
        response, payload = campaignMessage.createMessage(self, payload)
        campaignMessage.assertCreateMessage(response, 200)
        campaignMessage.assertCreateMessageDbCalls(response['json']['entity']['messageId'], self.campaignId,payload)

    @pytest.mark.parametrize('description,messageInfo', [
        ('MessageType-Recurring-Plain', ['WECHAT', ['RECURRING', '14', '03', '02', '01', '10'], ['PLAIN'], False]),
        ('MessageType-Recurring-Point', ['WECHAT', ['RECURRING', '14', '03', '02', '01', '10'], ['POINTS'], False]),
        ('MessageType-Recurring-Coupons', ['WECHAT', ['RECURRING', '14', '03', '02', '01', '10'], ['COUPONS'], False]),
        ('MessageType-Recurring-Generic', ['WECHAT', ['RECURRING', '14', '03', '02', '01', '10'], ['GENERIC'], False])
    ])
    def test_wechat_createMessage_Recurring(self, description, messageInfo):
        Logger.log('Actual ListId:{} and CampaignId:{} and used for Recurring listId:{} and campaignId:{}'.format(self.listId,self.campaignId,constant.config['message_recurring']['WECHAT']['listId'],constant.config['message_recurring']['WECHAT']['campaignId']))
        actualListIdGettingUsedInAllCases = self.listId
        actualCampaignIdGettingUsedInAllCases = self.campaignId
        actualVoucherIdGettingUsedInAllCases = self.voucherId
        try:
            self.listId = constant.config['message_recurring']['WECHAT']['listId']
            self.campaignId = constant.config['message_recurring']['WECHAT']['campaignId']
            self.voucherId = constant.config['message_recurring']['WECHAT']['voucherId']
            response, payload = campaignMessage.createMessage(self, messageInfo=messageInfo)
            campaignMessage.assertCreateMessage(response, 200)
            campaignMessage.assertCreateMessageDbCalls(response['json']['entity']['messageId'], self.campaignId,payload)
            campaignMessage.updateDefaultMessageJsonWithMessageInfoValues(messageInfo, payload,response['json']['entity']['messageId'])
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
        ('MessageType-Immediate-Plain-WithInvalidCampaignId', {'channel' : 'WECHAT','accountDetails': construct.constructAccountDetails()}, '0', 400, 100,['Invalid request : must be greater than or equal to 1']),
        ('MessageType-Immediate-Plain-WithNegativeCampaignId', {'channel' : 'WECHAT','accountDetails': construct.constructAccountDetails()}, '-1234', 400, 100,['Invalid request : must be greater than or equal to 1']),
        ('MessageType-Immediate-Plain-WithInvalidCampaignId', {'channel' : 'WECHAT','accountDetails': construct.constructAccountDetails()}, '999999999', 400,1007, ['Campaign Id Exception : Invalid Campaign Id Passed 999999999'])
        ])
    def test_wechat_createMessage_Immediate_Plain_WrongCampaignId(self, description, payload, campaignIdPassed, statusCode,errorCode, errorMessage):
        actualCampaignIdGettingUsedThroughOut = self.campaignId
        try:
            self.campaignId = campaignIdPassed
            payload.update({'templateId' : self.templateIdDict['plain']})
            response, payload = campaignMessage.createMessage(self, payloadData=payload)
            campaignMessage.assertCreateMessage(response, statusCode, errorCode, errorMessage)
        except AssertionError, reason:
            Assertion.constructAssertion(False, reason)
        except Exception, exp:
            Logger.log('Not Due to Assertion but Recurring Failed due to Reason :{}'.format(exp))
        finally:
            self.campaignId = actualCampaignIdGettingUsedThroughOut

    @pytest.mark.parametrize('description,payload,listIdPassed,statusCode,errorCode,errorMessage', [
        ('MessageType-Immediate-Plain-WithInvalidListId', {'channel' : 'WECHAT','accountDetails': construct.constructAccountDetails()}, 1111111, 400, 3007,['List id does not exists : 1,111,111']),
        ('MessageType-Immediate-Plain-WithNegativeListId', {'channel' : 'WECHAT','accountDetails': construct.constructAccountDetails()}, -1111111, 400, 100,['Invalid request : Invalid list Id'])
        ])
    def test_wechat_createMessage_Immediate_Plain_WithInvalidListId(self, description, payload, listIdPassed, statusCode,errorCode, errorMessage):
        actualListIdGettingUsedThroughOut = self.listId
        try:
            self.listId = listIdPassed
            payload.update({'templateId': self.templateIdDict['plain']})
            response, payload = campaignMessage.createMessage(self, payloadData=payload)
            campaignMessage.assertCreateMessage(response, statusCode, errorCode, errorMessage)
        except AssertionError, reason:
            Assertion.constructAssertion(False, reason)
        except Exception, exp:
            Logger.log('Not Due to Assertion but Recurring Failed due to Reason :{}'.format(exp))
        finally:
            self.listId = actualListIdGettingUsedThroughOut

    @pytest.mark.parametrize('description, payload, accountDetailsPassed, statusCode, errorCode, errorMessage', [
        ('MessageType-Immediate-Plain-WithInvalidAppId',{'channel': 'WECHAT', 'accountDetails': construct.constructAccountDetails()}, {'appId' : 'AppId-qaz123'}, 400, 3018, ['Invalid account details : Invalid App Id']),
        ('MessageType-Immediate-Plain-WithInvalidAppSecret',{'channel': 'WECHAT', 'accountDetails': construct.constructAccountDetails()}, {'appSecret' : 'AppSecret-qaz123'}, 400, 3018, ['Invalid account details : Invalid App secret token']),
        ('MessageType-Immediate-Plain-WithInvalidOriginalId',{'channel': 'WECHAT', 'accountDetails': construct.constructAccountDetails()}, {'originalId' : '999999999'}, 400, 3018,['Invalid account details : Invalid Original Id'])
    ])
    def test_wechat_createMessage_Immediate_Plain_InvalidAccountDetails(self, description, payload, accountDetailsPassed,statusCode, errorCode, errorMessage):
        try:
            payload.update({accountDetailsPassed})
            payload.update({'templateId': self.templateIdDict['plain']})
            response, payload = campaignMessage.createMessage(self, payloadData=payload)
            campaignMessage.assertCreateMessage(response, statusCode, errorCode, errorMessage)
        except AssertionError, reason:
            Assertion.constructAssertion(False, reason)
        except Exception, exp:
            Logger.log('Not Due to Assertion but Recurring Failed due to Reason :{}'.format(exp))


    @pytest.mark.parametrize('description, payload, incentives, statusCode, errorCode, errorMessage', [
        ('MessageType-Immediate-Coupons-WithoutType',{'channel' : 'WECHAT','accountDetails': construct.constructAccountDetails()}, 'COUPONS', 400, 3019, ['Creatives template error : Coupons incentive should be attached to use voucher tags']),
        ('MessageType-Immediate-Points-WithoutType',{'channel' : 'WECHAT','accountDetails': construct.constructAccountDetails()}, 'POINTS', 400, 3019, ['Creatives template error : Points incentive should be attached to use points tags']),
    ])
    def test_wechat_createMessage_Invalid_IncentivesType(self, description, payload, incentives, statusCode, errorCode, errorMessage):
        try:
            payload.update({'templateId': self.templateIdDict[incentives.lower()]})
            response, payload = campaignMessage.createMessage(self, payloadData=payload)
            campaignMessage.assertCreateMessage(response, statusCode, errorCode, errorMessage)
        except AssertionError, reason:
            Assertion.constructAssertion(False, reason)
        except Exception, exp:
            Logger.log('Not Due to Assertion but Recurring Failed due to Reason :{}'.format(exp))

    @pytest.mark.parametrize('description, invalidpayload, statusCode, errorCode, errorMessage', [
         ('MessageType-Immediate-Invalid_Title',{'Title' : 'InvalidTitle'}, 400, 3020, ['WeCRM template error : Invalid title in message details']),
         ('MessageType-Immediate-Invalid_originalId',{'OriginalId' : 'InvalidId'}, 400, 3020, ['WeCRM template error : Invalid original id in message details']),
         ('MessageType-Immediate-Invalid_templateId',{'template_id' : 'InvalidId'}, 400, 3020, ['WeCRM template error : Invalid WeCRM template id in message details']),
         ('MessageType-Immediate-Invalid_data',{'data' : {"first" : "Test"}}, 400, 3020, ['WeCRM template error : Message details should contain all tags required by WeCRM template','WeCRM template error : Invalid structure of message details data']),
    ])
    def test_wechat_createMessage_Wrong_Message(self, description, invalidpayload, statusCode, errorCode,errorMessage):
        try:
            payload = {'message': construct.constructWechatMessageBody('plain')}
            payload['message'].update(invalidpayload)
            payload.update({'channel' : 'WECHAT','accountDetails' : construct.constructAccountDetails()})
            response, payload = campaignMessage.createMessage(self, payloadData=payload)
            campaignMessage.assertCreateMessage(response, statusCode, errorCode, errorMessage)
        except AssertionError, reason:
            Assertion.constructAssertion(False, reason)
        except Exception, exp:
            Logger.log('Not Due to Assertion but Recurring Failed due to Reason :{}'.format(exp))

    @pytest.mark.parametrize('description, invalidpayload, statusCode, errorCode, errorMessage', [
        ('MessageType-Immediate-Without_Title', {'message': 'Title'}, 400, 100,['Invalid request : Title as per the WeCRM structure must be provided in message details']),
        ('MessageType-Immediate-Without_originalId', {'message': 'OriginalId'}, 400, 100,['Invalid request : Original id must be provided in message details']),
        ('MessageType-Immediate-Without_templateId', {'message': 'template_id'}, 400, 100,['Invalid request : WeCRM template id must be provided']),
        ('MessageType-Immediate-Without_messageData', {'message': 'Data'}, 400, 100,['Invalid request : WeCRM template data must be provided']),
    ])
    def test_wechat_createMessage_Invalid_Payload(self, description, invalidpayload, statusCode, errorCode, errorMessage):
        try:
            payload = {'message': construct.constructWechatMessageBody('plain')}
            payload.update({'channel': 'WECHAT', 'accountDetails': construct.constructAccountDetails()})
            if 'data' == invalidpayload.keys()[0]:
                payload.pop(invalidpayload[invalidpayload.keys()[0]])
            else:
                payload[invalidpayload.keys()[0]].pop(invalidpayload[invalidpayload.keys()[0]])

            response, payload = campaignMessage.createMessage(self, payloadData=payload)
            campaignMessage.assertCreateMessage(response, statusCode, errorCode, errorMessage)
        except AssertionError, reason:
            Assertion.constructAssertion(False, reason)
        except Exception, exp:
            Logger.log('Not Due to Assertion but Recurring Failed due to Reason :{}'.format(exp))