import pytest, time, Queue, pytest_ordering
from time import sleep
from threading import Thread
from src.Constant.constant import constant
from src.modules.iris.list import campaignList
from src.utilities.logger import Logger
from src.utilities.assertion import Assertion
from src.modules.iris.campaigns import campaigns
from src.modules.iris.authorize import authorize
from src.modules.iris.message import campaignMessage
from src.modules.iris.dbCallsCampaign import dbCallsCampaign
from src.modules.iris.dbCallsMessage import dbCallsMessage
from src.modules.iris.dbCallsList import dbCallsList
from src.modules.iris.dbCallsCoupons import dbCallsCoupons
from src.modules.iris.construct import construct
from src.modules.iris.coupons import coupons
from src.modules.nsadmin.nsadminHelper import NSAdminHelper
from src.modules.luci.luciObject import LuciObject
from src.modules.luci.luciThrift import LuciThrift

@pytest.mark.run(order=9)
class Test_SMS_Authorize():
    
    def setup_class(self):
        Logger.logSuiteName(str(self).split('.')[-1])
        nsPort = constant.config['nsMasterPort']
        self.nsHelper = NSAdminHelper(constant.config['orgId'], 'SMS')
        luciPort = constant.config['luciPort'].next()
        self.luciObj = LuciThrift(luciPort)
        self.constructObj = LuciObject()
        constant.config['requestId'] = 'requestId_IRIS_LUCI'
        createListresponse, createListPayload, campaignId = campaignList.createList({'customTagCount':0, 'name':'IRIS_LIST_' + str(int(time.time() * 100000))}, campaignType=['LIVE', 'ORG', 'List', 'TAGS', 0])
        campaignList.assertCreateList(createListresponse, 200)
        groupVersionDetailResult, bucketId = campaignList.assertCreateListDbCalls(createListresponse['json']['entity']['listId'], createListPayload, 'ORG')
        Logger.log('GroupVersionId : {}, bucketId : {}'.format(groupVersionDetailResult, bucketId))
        addRecipientResponse, addRecipientPayload = campaignList.addRecipient({}, campaignId, createListresponse['json']['entity']['listId'], 'mobile', 10, 0, newUser=False)
        campaignList.assertAddRecipient(addRecipientResponse, 200)
        campaignList.assertAddRecipientDbCalls(addRecipientResponse, addRecipientPayload, createListresponse, campaignId, bucketId, {'TEST':groupVersionDetailResult['TEST'], 'CONTROL':groupVersionDetailResult['CONTROL']}, 'mobile')
        self.bucketId = bucketId
        self.groupVersionResult = dbCallsList.getGroupVersionDetailsWithGroupId(createListresponse['json']['entity']['listId'])
        responseCoupon, payloadCoupon, campaignId = coupons.createCoupons(campaignId=campaignId)
        self.strategy = construct.constructStrategyIds()
        self.programeId = self.strategy['programeId']
        self.allocationStrategyId = self.strategy['allocationStrategyId']
        self.expiryStrategyId = self.strategy['expirationStrategyId']
        if 'errors' not in responseCoupon['json']:
            self.voucherId = responseCoupon['json']['entity']['voucherSeriesId']
        else:
            self.voucherId = dbCallsCoupons.getVoucherSeriesIdUsingCampaignId(campaignId)
        self.campaignId = campaignId
        self.listId = createListresponse['json']['entity']['listId']
        Logger.log('Using CampaignId : {} , listId : {} for Execution of Create Message'.format(self.campaignId, self.listId))
        
    def setup_method(self, method):
        Logger.logMethodName(method.__name__)

    @pytest.mark.parametrize('description,messageInfo', [
        ('MessageType-Immediate-Plain', ['SMS', ['IMMEDIATE'], ['PLAIN'], True]),
        ('MessageType-Immediate-Plain', ['SMS', ['IMMEDIATE'], ['PLAIN'], False])
        ])
    def test_authorize_sms_Plain_immediate_Sanity(self, description, messageInfo):
        authorizeResult = authorize.authorizeCampaign(self, messageInfo, constant.messagesDefault['updated'])
        authorize.assertAuthorize(authorizeResult['authorizeResponse'], 200)
        authorize.dbAssertAuthorize(authorizeResult)
        
    @pytest.mark.parametrize('description,messageInfo', [
        ('MessageType-ParticularDate-Plain', ['SMS', ['PARTICULARDATE'], ['PLAIN'], True]),
        ('MessageType-ParticularDate-Plain', ['SMS', ['PARTICULARDATE'], ['PLAIN'], False]),
        ])
    def test_authorize_sms_Plain_particularDate(self, description, messageInfo):
        authorizeResult = authorize.authorizeCampaign(self, messageInfo, False)
        authorize.assertAuthorize(authorizeResult['authorizeResponse'], 200)
        authorize.dbAssertAuthorize(authorizeResult)
        
    @pytest.mark.parametrize('description,messageInfo', [
        ('MessageType-Immediate-Plain', ['SMS', ['IMMEDIATE'], ['Generic'], True]),
        ('MessageType-Immediate-Plain_systemDefault_False', ['SMS', ['IMMEDIATE'], ['Generic'], False]),
        ])        
    def test_authorize_sms_Generic_immediate_Sanity(self, description, messageInfo):
        authorizeResult = authorize.authorizeCampaign(self, messageInfo, constant.messagesDefault['updated'])
        authorize.assertAuthorize(authorizeResult['authorizeResponse'], 200)
        authorize.dbAssertAuthorize(authorizeResult)
        
    @pytest.mark.parametrize('description,messageInfo', [
        ('MessageType-ParticularDate-Plain', ['SMS', ['PARTICULARDATE'], ['Generic'], True]),
        ('MessageType-ParticularDate-Plain_systemDefault_False', ['SMS', ['PARTICULARDATE'], ['Generic'], False]),
        ])        
    def test_authorize_sms_Generic_particularDate(self, description, messageInfo):
        authorizeResult = authorize.authorizeCampaign(self, messageInfo, False)
        authorize.assertAuthorize(authorizeResult['authorizeResponse'], 200)
        authorize.dbAssertAuthorize(authorizeResult)
        
    @pytest.mark.parametrize('description,messageInfo', [
        ('MessageType-Immediate-Plain', ['SMS', ['IMMEDIATE'], ['COUPONS'], True]),
        ('MessageType-Immediate-Plain_systemDefault_False', ['SMS', ['IMMEDIATE'], ['COUPONS'], False]),
        ])        
    def test_authorize_sms_Coupon_immediate_Sanity(self, description, messageInfo):
        authorizeResult = authorize.authorizeCampaign(self, messageInfo, constant.messagesDefault['updated'])
        authorize.assertAuthorize(authorizeResult['authorizeResponse'], 200)
        authorize.dbAssertAuthorize(authorizeResult)
        
    @pytest.mark.parametrize('description,messageInfo', [
        ('MessageType-ParticularDate-Plain', ['SMS', ['PARTICULARDATE'], ['COUPONS'], True]),
        ('MessageType-ParticularDate-Plain_systemDefault_False', ['SMS', ['PARTICULARDATE'], ['COUPONS'], False]),
        ])        
    def test_authorize_sms_Coupon_particularDate(self, description, messageInfo):
        authorizeResult = authorize.authorizeCampaign(self, messageInfo, False)
        authorize.assertAuthorize(authorizeResult['authorizeResponse'], 200)
        authorize.dbAssertAuthorize(authorizeResult)
        
    @pytest.mark.parametrize('description,messageInfo', [
        ('MessageType-Immediate-Plain', ['SMS', ['IMMEDIATE'], ['POINTS'], True]),
        ('MessageType-Immediate-Plain_systemDefault_False', ['SMS', ['IMMEDIATE'], ['POINTS'], False]),
        ])        
    def test_authorize_sms_Points_immediate_Sanity(self, description, messageInfo):
        authorizeResult = authorize.authorizeCampaign(self, messageInfo, constant.messagesDefault['updated'])
        authorize.assertAuthorize(authorizeResult['authorizeResponse'], 200)
        authorize.dbAssertAuthorize(authorizeResult)
        
    @pytest.mark.parametrize('description,messageInfo', [
        ('MessageType-ParticularDate-Plain', ['SMS', ['PARTICULARDATE'], ['POINTS'], True ]),
        ('MessageType-ParticularDate-Plain_systemDefault_False', ['SMS', ['PARTICULARDATE'], ['POINTS'], False ]),
        ])        
    def test_authorize_sms_Points_praticularDate(self, description, messageInfo):
        authorizeResult = authorize.authorizeCampaign(self, messageInfo, False)
        authorize.assertAuthorize(authorizeResult['authorizeResponse'], 200)
        authorize.dbAssertAuthorize(authorizeResult)
    
    @pytest.mark.parametrize('description,messageInfo', [
        ('MessageType-Recurring-Plain', ['SMS', ['RECURRING'], ['PLAIN'], False]),
        ('MessageType-Recurring-Point', ['SMS', ['RECURRING'], ['POINTS'], False]),
        ('MessageType-Recurring-Plain', ['SMS', ['RECURRING'], ['COUPONS'], False])
        ])
    def test_authorize_sms_recurring(self, description, messageInfo):
        Logger.log('Actual ListId:{} and CampaignId:{} and used for Recurring listId:{} and campaignId:{}'.format(self.listId, self.campaignId, constant.config['message_recurring']['SMS']['listId'], constant.config['message_recurring']['SMS']['campaignId']))
        actualListIdGettingUsedInAllCases = self.listId
        actualCampaignIdGettingUsedInAllCases = self.campaignId
        actualVoucherIdGettingUsedInAllCases = self.voucherId
        try:
            self.listId = constant.config['message_recurring']['SMS']['listId']
            self.campaignId = constant.config['message_recurring']['SMS']['campaignId']
            self.voucherId = constant.config['message_recurring']['SMS']['voucherId']
            authorizeResult = authorize.authorizeCampaign(self, messageInfo, False)
            authorize.assertAuthorize(authorizeResult['authorizeResponse'], 200)
        except AssertionError, reason:
            Assertion.constructAssertion(False, reason)
        except Exception, exp:
            Assertion.constructAssertion(False, 'Not Due to Assertion but Recurring Failed due to Reason :{}'.format(exp))
        finally:
            Logger.log('Finally Setting Back the Actual ListId :{} and campaignId :{}'.format(actualListIdGettingUsedInAllCases, actualCampaignIdGettingUsedInAllCases))
            self.listId = actualListIdGettingUsedInAllCases
            self.campaignId = actualCampaignIdGettingUsedInAllCases
            self.voucherId = actualVoucherIdGettingUsedInAllCases

    @pytest.mark.parametrize('description,messageInfo, statusCode, errorCode, errorMessage', [
        ('MessageType-Immediate-Plain', ['SMS', ['IMMEDIATE'], ['PLAIN'], False], 400, 3022, ['Message is already approved']),
        ('MessageType-Particular-Plain', ['SMS', ['PARTICULARDATE'], ['PLAIN'], False], 400, 3022, ['Message is already approved']),
        ])
    def test_authorize_sms_multiple_times(self, description, messageInfo, statusCode, errorCode, errorMessage):
        authorizeResult = authorize.authorizeCampaign(self, messageInfo, constant.messagesDefault['updated'])
        authorizeResult = authorize.makeAuthorizeRequest(authorizeResult['campaignId'], authorizeResult['messageId'])
        authorize.assertAuthorize(authorizeResult, statusCode, errorCode, errorMessage)

    @pytest.mark.parametrize('description,messageInfo, statusCode, errorCode, errorMessage', [
        ('MessageType-Recurring-Plain', ['SMS', ['RECURRING'], ['PLAIN'], False], 400, 3022, ['Message is already approved'])
    ])
    def test_authorize_sms_recurring_multiple_times(self, description, messageInfo, statusCode, errorCode, errorMessage):
        actualListIdGettingUsedInAllCases = self.listId
        actualCampaignIdGettingUsedInAllCases = self.campaignId
        try:
            self.listId = constant.config['message_recurring']['SMS']['listId']
            self.campaignId = constant.config['message_recurring']['SMS']['campaignId']
            authorizeResult = authorize.authorizeCampaign(self, messageInfo, False)
            authorizeResult = authorize.makeAuthorizeRequest(authorizeResult['campaignId'], authorizeResult['messageId'])
            authorize.assertAuthorize(authorizeResult, statusCode, errorCode, errorMessage)
        except AssertionError, reason:
            Assertion.constructAssertion(False, reason)
        except Exception, exp:
            Assertion.constructAssertion(False, 'Not Due to Assertion but Recurring Failed due to Reason :{}'.format(exp))
        finally:
            Logger.log('Finally Setting Back the Actual ListId :{} and campaignId :{}'.format(
                actualListIdGettingUsedInAllCases, actualCampaignIdGettingUsedInAllCases))
            self.listId = actualListIdGettingUsedInAllCases
            self.campaignId = actualCampaignIdGettingUsedInAllCases

    @pytest.mark.parametrize('description,messageInfo,campaignIdPassed, statusCode, errorCode, errorMessage', [
        ('MessageType-Immediate-Plain-InvalidCampaignId', ['SMS', ['IMMEDIATE'], ['PLAIN'], False], '0' , 400, 1007, ['Campaign Id Exception : Invalid Campaign Id Passed 0']),
        ('MessageType-Immediate-Plain-NegativeCampaignId', ['SMS', ['IMMEDIATE'], ['PLAIN'], False], '-1234' , 400, 1007, ['Campaign Id Exception : Invalid Campaign Id Passed -1234']),
        ('MessageType-Immediate-Plain-InvalidCampaignId', ['SMS', ['IMMEDIATE'], ['PLAIN'], False], '999999999' , 400, 1007, ['Campaign Id Exception : Invalid Campaign Id Passed 999999999'])
        ])
    def test_authorize_sms_invalid_campaignId(self, description, messageInfo, campaignIdPassed, statusCode, errorCode, errorMessage):
        response = campaignMessage.createMessage(self, messageInfo=messageInfo)[0]
        messageId = response['json']['entity']['messageId']
        authorizeResult = authorize.makeAuthorizeRequest(campaignIdPassed, messageId)
        authorize.assertAuthorize(authorizeResult, statusCode, errorCode, errorMessage)

    @pytest.mark.parametrize('description,messageInfo,messageIdPassed, statusCode, errorCode, errorMessage', [
        ('MessageType-Immediate-Plain-InvalidMessageId', ['SMS', ['IMMEDIATE'], ['PLAIN'], False], '0' , 400, 3023, ['Message with message id 0 does not exists']),
        ('MessageType-Immediate-Plain-NegativeMessageId', ['SMS', ['IMMEDIATE'], ['PLAIN'], False], '-1234' , 400, 3023, ['Message with message id -1,234 does not exists']),
        ('MessageType-Immediate-Plain-InvalidMessageId', ['SMS', ['IMMEDIATE'], ['PLAIN'], False], '999999999' , 400, 3023, ['Message with message id 999,999,999 does not exists'])
        ])
    def test_authorize_sms_invalid_messageId(self, description, messageInfo, messageIdPassed, statusCode, errorCode, errorMessage):
        campaignMessage.createMessage(self, messageInfo=messageInfo)[0]
        authorizeResult = authorize.makeAuthorizeRequest(self.campaignId, messageIdPassed)
        authorize.assertAuthorize(authorizeResult, statusCode, errorCode, errorMessage)

    @pytest.mark.parametrize('description,messageInfo,orgIdPassed, statusCode, errorCode, errorMessage', [
        ('MessageType-Immediate-Plain-InvalidOrgId', ['SMS', ['IMMEDIATE'], ['PLAIN'], False], '0', 400, 1007, ['Campaign Id Exception : Invalid Campaign Id Passed {}']),
        ('MessageType-Immediate-Plain-NegativeOrgId', ['SMS', ['IMMEDIATE'], ['PLAIN'], False], '-1234', 403, 100, ["Invalid request : You don't have sufficient access for the requested organization."]),
        ('MessageType-Immediate-Plain-InvalidOrgId', ['SMS', ['IMMEDIATE'], ['PLAIN'], False], '999999999', 403, 100, ["Invalid request : You don't have sufficient access for the requested organization."])
    ])
    def test_authorize_sms_invalid_orgId(self, description, messageInfo, orgIdPassed, statusCode, errorCode, errorMessage):
        actualOrgIdGettingUsedThroughOut = constant.config['orgId']
        try:
            response = campaignMessage.createMessage(self, messageInfo=messageInfo)[0]
            messageId = response['json']['entity']['messageId']
            constant.config['orgId'] = orgIdPassed
            authorizeResult = authorize.makeAuthorizeRequest(self.campaignId, messageId)
            authorize.assertAuthorize(authorizeResult, statusCode, errorCode, errorMessage[0].format(self.campaignId))
        except AssertionError, reason:
            Assertion.constructAssertion(False, reason)
        except Exception, exp:
            Assertion.constructAssertion(False, 'Not Due to Assertion but Recurring Failed due to Reason :{}'.format(exp))
        finally:
            constant.config['orgId'] = actualOrgIdGettingUsedThroughOut

    @pytest.mark.parametrize('description,messageInfo, payload, statusCode, errorCode, errorMessage', [
        ('MessageType-Immediate-Plain-Expiry-Campaign', ['SMS', ['IMMEDIATE'], ['PLAIN'], False], {'endDate' : int(time.time() * 1000 + 24 * 60)}, 400, 1006, ['Campaign Date Exception : Campaign is already expired'])
    ])
    def test_authorize_sms_expired_campaign(self, description, messageInfo, payload, statusCode, errorCode, errorMessage):
        response = campaignMessage.createMessage(self, messageInfo=messageInfo)[0]
        messageId = response['json']['entity']['messageId']
        campaigns.updateCampaign(payload, campaignId=self.campaignId)
        authorizeResult = authorize.makeAuthorizeRequest(self.campaignId, messageId)
        authorize.assertAuthorize(authorizeResult, statusCode, errorCode, errorMessage[0].format(self.campaignId))

    @pytest.mark.skip(reason='Gateway simulation sync not happens immediate')
    @pytest.mark.parametrize('description, messageInfo, statusCode, errorCode, errorMessage', [
        ('MessageType-Immediate-Plain-Disabled-Domain-SystemDefault-True', ['SMS' , True], 400, 3006, ['Provided Sender ids are not valid']),
        ('MessageType-Immediate-Plain-Disabled-Domain-SystemDefault-False', ['SMS' , False], 400, 3014, ['Gateway with id {} is invalid', 'Domain Gateway Map with id does not exist : {}'])
        ])
    def test_authorize_sms_NSAdmin(self, description, messageInfo , statusCode, errorCode, errorMessage):

        self.nsHelper.disableDomainPropertiesGatewayMap()
        self.nsHelper.addDefaultGateway('BULK')
        gatewayId = self.nsHelper.getDomainGatewayMapId('valuefirstmock')

        payload = {'senderDetails': {'gsmSenderId': 919845012345, 'useSystemDefaults': messageInfo[1], 'cdmaSenderId': 919845012345, 'domainGatewayMapId' : gatewayId}, 'channel': 'SMS'}
        response = campaignMessage.createMessage(self, payloadData=payload)[0]
        messageId = response['json']['entity']['messageId']

        authorizeResult = authorize.makeAuthorizeRequest(self.campaignId, messageId)
        tmpErrorMessage = []
        for error in errorMessage:
            tmpErrorMessage.append(error.format(gatewayId))
        authorize.assertAuthorize(authorizeResult, statusCode, errorCode, tmpErrorMessage)

    @pytest.mark.parametrize('description,messageInfo', [
        ('MessageType-ParticularDate-Plain', ['SMS', ['PARTICULARDATE'], ['COUPONS'], True]),
    ])
    def test_authorize_sms_using_revokedvoucherseries(self, description, messageInfo):
        invalidateCouponReq = LuciObject.invalidateCouponRequest({'orgId' : constant.config['orgId'], 'couponSeriesId' : int(self.voucherId)})
        Logger.log('Is Revoked Coupons : ' , self.luciObj.invalidateCoupons(invalidateCouponReq))
        authorizeResult = authorize.authorizeCampaign(self, messageInfo, False)
        authorize.assertAuthorize(authorizeResult['authorizeResponse'], 200)
        authorize.dbAssertAuthorize(authorizeResult)

    @pytest.mark.parametrize('description,messageInfo, errorMessage', [
        ('MessageType-Recurring-Plain-Without-Authorize-HDCheck', ['SMS', ['RECURRING'], ['PLAIN'], False], ['Alert - Campaign not Authorized','Error - Campaign not Authorized'])
    ])
    def test_authorize_sms_health_dashboard_without_Authorize(self, description, messageInfo, errorMessage):
        actualListIdGettingUsedInAllCases = self.listId
        actualCampaignIdGettingUsedInAllCases = self.campaignId
        try:
            self.listId = constant.config['message_recurring']['SMS']['listId']
            self.campaignId = constant.config['message_recurring']['SMS']['campaignId']
            authorizeResult = campaignMessage.createMessage(self, messageInfo=messageInfo)[0]
            messageId = authorizeResult['json']['entity']['messageId']
            time.sleep(20)
            authorize.dbAssertAuthorize_HealthDashboardNotification(self.campaignId, messageId,ExpectedMsg=errorMessage, channel='campaign_authorized')
        except AssertionError, reason:
            Assertion.constructAssertion(False, reason)
        except Exception, exp:
            Assertion.constructAssertion(False, 'Not Due to Assertion but Recurring Failed due to Reason :{}'.format(exp))
        finally:
            Logger.log('Finally Setting Back the Actual ListId :{} and campaignId :{}'.format(actualListIdGettingUsedInAllCases, actualCampaignIdGettingUsedInAllCases))
            self.listId = actualListIdGettingUsedInAllCases
            self.campaignId = actualCampaignIdGettingUsedInAllCases

    @pytest.mark.skip(reason='Gateway simulation sync not happens immediate')
    @pytest.mark.parametrize('description, messageInfo, errorMessage', [
        ('MessageType-Recurring-Plain-Without-Authorize-HDCheck', ['SMS' , ['RECURRING'], ['PLAIN'], True], ['Alert - Campaign not Authorized', 'Error - Campaign not Authorized'])
        ])
    def test_authorize_sms_Domain_not_available(self, description, messageInfo , errorMessage):

        self.nsHelper.disableDomainPropertiesGatewayMap()
        self.nsHelper.addDefaultGateway('BULK')
        gatewayId = self.nsHelper.getDomainGatewayMapId('valuefirstmock')


        actualListIdGettingUsedInAllCases = self.listId
        actualCampaignIdGettingUsedInAllCases = self.campaignId
        try:
            self.listId = constant.config['message_recurring']['SMS']['listId']
            self.campaignId = constant.config['message_recurring']['SMS']['campaignId']

            payloadData = construct.constructCreateMessageBody(self.listId, messageInfo[0], messageInfo[1], messageInfo[2], messageInfo[3])
            payloadData.update({'senderDetails': {'gsmSenderId': int(senderIds['gsm_sender_id']), 'useSystemDefaults': True, 'cdmaSenderId': int(senderIds['cdma_sender_id']), 'domainGatewayMapId' : gatewayId}, 'channel': 'SMS'})
            response = campaignMessage.createMessage(self, payloadData=payloadData)[0]
            messageId = response['json']['entity']['messageId']
            authorizeResult = authorize.makeAuthorizeRequest(self.campaignId, messageId)

            authorize.dbAssertAuthorize_HealthDashboardNotification(self.campaignId, messageId, ExpectedMsg=errorMessage, channel='campaign_authorized')
        except AssertionError, reason:
            Assertion.constructAssertion(False, reason)
        except Exception, exp:
            Assertion.constructAssertion(False, 'Not Due to Assertion but Recurring Failed due to Reason :{}'.format(exp))
        finally:
            Logger.log('Finally Setting Back the Actual ListId :{} and campaignId :{}'.format(actualListIdGettingUsedInAllCases, actualCampaignIdGettingUsedInAllCases))
            self.listId = actualListIdGettingUsedInAllCases
            self.campaignId = actualCampaignIdGettingUsedInAllCases

    @pytest.mark.parametrize('description, messageInfo, errorMessage', [
        ('MessageType-Recurring-Plain-max_limit_exceed', ['SMS' , ['RECURRING'], ['PLAIN'], True], ['Alert - List limit crossed', 'Error - List limit crossed'])
        ])
    def test_authorize_sms_max_user_limit(self, description, messageInfo , errorMessage):
        actualListIdGettingUsedInAllCases = self.listId
        actualCampaignIdGettingUsedInAllCases = self.campaignId
        try:
            self.listId = constant.config['message_recurring']['SMS']['listId']
            self.campaignId = constant.config['message_recurring']['SMS']['campaignId']
            payloadData = construct.constructCreateMessageBody(self.listId, messageInfo[0], messageInfo[1], messageInfo[2], messageInfo[3])
            payloadData['schedule'].update({'maxUsers': 1})
            response = campaignMessage.createMessage(self, payloadData=payloadData)[0]
            messageId = response['json']['entity']['messageId']
            authorize.makeAuthorizeRequest(self.campaignId, messageId)
            time.sleep(80)
            authorize.dbAssertAuthorize_HealthDashboardNotification(self.campaignId, messageId, ExpectedMsg=errorMessage, channel='users_recurring_campaign')
        except AssertionError, reason:
            Assertion.constructAssertion(False, reason)
        except Exception, exp:
            Assertion.constructAssertion(False, 'Not Due to Assertion but Recurring Failed due to Reason :{}'.format(exp))
        finally:
            Logger.log('Finally Setting Back the Actual ListId :{} and campaignId :{}'.format(actualListIdGettingUsedInAllCases, actualCampaignIdGettingUsedInAllCases))
            self.listId = actualListIdGettingUsedInAllCases
            self.campaignId = actualCampaignIdGettingUsedInAllCases