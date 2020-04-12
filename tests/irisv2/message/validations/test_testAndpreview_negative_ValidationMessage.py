import copy

import pytest

from src.Constant.constant import constant
from src.modules.irisv2.helper.irisHelper import IrisHelper
from src.modules.irisv2.message.testAndPreviewDBAssertion import PreviewDBAssertion
from src.modules.irisv2.message.testPreview import TestPreview
from src.utilities.assertion import Assertion
from src.utilities.logger import Logger


class Test_testAndpreview_Negative_ValidationMessage():
    def setup_method(self, method):
        Logger.logMethodName(method.__name__)

    def setup_class(self):
        Logger.logSuiteName(str(self).split('.')[-1])
        self.testAndControlPayload = {
            'SMS': constant.payload['testandpreview_sms'],
            'EMAIL': constant.payload['testandpreview_email']
        }

    def test_testAndPreview_negative_validationCases_NoIdentifiers(self):
        payload = copy.deepcopy(self.testAndControlPayload['SMS'])
        payload['testContentOn']['testAudiences'] = []
        testPreviewResponse, testPreviewPayload = TestPreview.create('LIVE', 'ORG', 'MOBILE', 0, payload=payload)
        TestPreview.assertResponse(testPreviewResponse, 400, 102, 'Invalid request : Test audience is required')

    @pytest.mark.parametrize('channel', [
        ('SMS'),
        ('EMAIL')
    ])
    def test_testAndPreview_negative_validationCases_MaxLimitOnIdentifiers(self, channel):
        payload = copy.deepcopy(self.testAndControlPayload[channel])
        payload['testContentOn'] = TestPreview.createAudience(channel, 11)
        testPreviewResponse, testPreviewPayload = TestPreview.create('LIVE', 'ORG', 'MOBILE', 0, payload=payload)
        TestPreview.assertResponse(testPreviewResponse, 400, 102, 'Invalid request : Max 10 test users are allowed')

    @pytest.mark.parametrize('channel,value,errorMessage', [
        ('SMS', '9148585260,AutomationUser','Invalid request : [Invalid mobile number]'),
        ('SMS', 'AutomationUser,9148585260','Invalid request : [Invalid mobile number]'),
        ('SMS', 'Auto,User,9148585260','Invalid request : [Invalid mobile number]'),
        ('SMS', '','Invalid request : Test audience identifier is required')
    ])
    def test_testAndPreview_negative_validationCases_VariationInIndetiferValue_SMS(self, channel, value,errorMessage):
        payload = copy.deepcopy(self.testAndControlPayload[channel])
        payload['testContentOn']['testAudiences'] = [{
            "identifier": value,
            "identifierType": "MOBILE"
        }]
        testPreviewResponse, testPreviewPayload = TestPreview.create('LIVE', 'ORG', 'MOBILE', 0, payload=payload)
        TestPreview.assertResponse(testPreviewResponse, 400, 102, errorMessage)

    @pytest.mark.parametrize('channel,value,errorMessage', [
        ('EMAIL', 'auto.user@gmail.com,AutomationUser','Invalid request : Invalid Email Identifier: {}'),
        ('EMAIL', 'AutomationUser,auto.user@gmail.com','Invalid request : Invalid Email Identifier: {}'),
        ('EMAIL', 'Auto,User,auto.user@gmail.com','Invalid request : Invalid Email Identifier: {}'),
        ('EMAIL', '','Invalid request : Test audience identifier is required')
    ])
    def test_testAndPreview_negative_validationCases_VariationInIndetiferValue_EMAIL(self, channel, value,errorMessage):

        payload = copy.deepcopy(self.testAndControlPayload[channel])
        payload['testContentOn']['testAudiences'] = [{
            "identifier": value,
            "identifierType":"EMAIL"
        }]
        testPreviewResponse, testPreviewPayload = TestPreview.create('LIVE', 'ORG', 'MOBILE', 0, payload=payload)
        TestPreview.assertResponse(testPreviewResponse, 400, 102,errorMessage.format(value)
                                   )

    def test_testAndPreview_negative_validationCases_NoTestAudienceKey(self):
        payload = copy.deepcopy(self.testAndControlPayload['SMS'])
        payload['testContentOn'] = {}
        testPreviewResponse, testPreviewPayload = TestPreview.create('LIVE', 'ORG', 'MOBILE', 0, payload=payload)
        TestPreview.assertResponse(testPreviewResponse, 400, 102, 'Invalid request : Test audience is required')

    def test_testAndPreview_negative_validationCases_NoTestContentOn(self):
        payload = copy.deepcopy(self.testAndControlPayload['SMS'])
        payload.pop('testContentOn')
        testPreviewResponse, testPreviewPayload = TestPreview.create('LIVE', 'ORG', 'MOBILE', 0, payload=payload)
        TestPreview.assertResponse(testPreviewResponse, 400, 102, 'Invalid request : Test audience is required')

    def test_testAndPreview_negative_validationCases_WrongDataTypeofIdentifier(self):
        payload = copy.deepcopy(self.testAndControlPayload['SMS'])
        payload['testContentOn']['testAudiences'] = [{
            'identifier': ['9148585260']
        }]
        testPreviewResponse, testPreviewPayload = TestPreview.create('LIVE', 'ORG', 'MOBILE', 0, payload=payload)
        TestPreview.assertResponse(testPreviewResponse, 400, 104,
                                   'Invalid request : invalid data type of field identifier')

    def test_testAndPreview_negative_validationCases_WrongDataTypeOfTestAudience(self):
        payload = copy.deepcopy(self.testAndControlPayload['SMS'])
        payload['testContentOn']['testAudiences'] = {
            'identifier': '9148585260'
        }
        testPreviewResponse, testPreviewPayload = TestPreview.create('LIVE', 'ORG', 'MOBILE', 0, payload=payload)
        TestPreview.assertResponse(testPreviewResponse, 400, 104,
                                   'Invalid request : invalid data type of field testAudiences')

    def test_testAndPreview_negative_validationCases_WrongDataTypeOfTestContent(self):
        payload = copy.deepcopy(self.testAndControlPayload['SMS'])
        payload['testContentOn'] = [{
            'testAudiences': {
                'identifier': '9148585260'
            }
        }]
        testPreviewResponse, testPreviewPayload = TestPreview.create('LIVE', 'ORG', 'MOBILE', 0, payload=payload)
        TestPreview.assertResponse(testPreviewResponse, 400, 104,
                                   'Invalid request : invalid data type of field testContentOn ')

    def test_testAndPreview_negative_validationCases_identifiers_multipleIdentifier_WithSingleIdentifierDefinedWrong(
            self):
        payload = copy.deepcopy(self.testAndControlPayload['SMS'])
        testContentOn = TestPreview.createAudience('SMS', 1)
        testContentOn['testAudiences'].append({
            'identifier': 'Auto,9148585260',
            'identifierType': "MOBILE"
        })
        payload['testContentOn'] = testContentOn
        testPreviewResponse, testPreviewPayload = TestPreview.create('LIVE', 'ORG', 'MOBILE', 0, payload=payload)
        TestPreview.assertResponse(testPreviewResponse, 400, 102, 'Invalid request : [Invalid mobile number]')

    def test_testAndPreview_negative_validationCases_identifiers_SameNumber_AsMultipleIdentifier_WithAndWithoutMobileCode(
            self):
        payload = copy.deepcopy(self.testAndControlPayload['SMS'])
        payload['testContentOn']['testAudiences'] = [
            {
                'identifier': '8497846843',
                'identifierType': "MOBILE"
            },
            {
                'identifier': '918497846843',
                'identifierType': "MOBILE"
            }
        ]
        payload['messageContent']['mesage_content_1'].pop('offers')
        testPreviewResponse, testPreviewPayload = TestPreview.create('LIVE', 'ORG', 'MOBILE', 0, payload=payload)
        TestPreview.assertResponse(testPreviewResponse, 200)
        PreviewDBAssertion(testPreviewResponse['json']['entity']['id'], 1).check()

    @pytest.mark.skipif(constant.config['cluster'] not in ['nightly'],
                        reason='Coupon series Confid is in hardcoded state, need to get fixed')
    def test_testAndPreview_negative_validationCases_coupons(
            self):
        payload = copy.deepcopy(self.testAndControlPayload['SMS'])
        testPreviewResponse, testPreviewPayload = TestPreview.create('LIVE', 'ORG', 'MOBILE', 0, payload=payload)
        TestPreview.assertResponse(testPreviewResponse, 400, 3039, 'Coupon series is claimed : 20,349')

    def test_testAndPreview_negative_validationCases_messageContentEmpty(self):
        payload = copy.deepcopy(self.testAndControlPayload['SMS'])
        payload['messageContent'] = {}
        testPreviewResponse, testPreviewPayload = TestPreview.create('LIVE', 'ORG', 'MOBILE', 0, payload=payload)
        TestPreview.assertResponse(testPreviewResponse, 400, 102, ['Invalid request : One Message content is required.','Invalid request : Message content is required'])

    def test_testAndPreview_negative_validationCases_multipleMessageContent(self):
        payload = copy.deepcopy(self.testAndControlPayload['SMS'])
        payload['messageContent'].update({
            'message_content_2': payload['messageContent']['mesage_content_1']
        })
        testPreviewResponse, testPreviewPayload = TestPreview.create('LIVE', 'ORG', 'MOBILE', 0, payload=payload)
        TestPreview.assertResponse(testPreviewResponse, 400, 102, 'Invalid request : One Message content is required.')

    def test_testAndPreview_negative_validationCases_content_sms_noMessageBody(self):
        payload = copy.deepcopy(self.testAndControlPayload['SMS'])
        payload['messageContent']['mesage_content_1'].pop('messageBody')
        testPreviewResponse, testPreviewPayload = TestPreview.create('LIVE', 'ORG', 'MOBILE', 0, payload=payload)
        TestPreview.assertResponse(testPreviewResponse, 400, 102,
                                   'Invalid request : Message body is required in message content.')

    def test_testAndPreview_negative_validationCases_content_email_noEmailSubject(self):
        payload = copy.deepcopy(self.testAndControlPayload['EMAIL'])
        payload['messageContent']['mesage_content_1'].pop('emailSubject')
        testPreviewResponse, testPreviewPayload = TestPreview.create('LIVE', 'ORG', 'MOBILE', 0, payload=payload)
        TestPreview.assertResponse(testPreviewResponse, 400, 102,
                                   'Invalid request : Email subject required in message content')

    def test_testAndPreview_negative_validationCases_content_email_noEmailBody(self):
        payload = copy.deepcopy(self.testAndControlPayload['EMAIL'])
        payload['messageContent']['mesage_content_1'].pop('emailBody')
        testPreviewResponse, testPreviewPayload = TestPreview.create('LIVE', 'ORG', 'MOBILE', 0, payload=payload)
        TestPreview.assertResponse(testPreviewResponse, 400, 102,
                                   'Invalid request : Email body required in message content')

    def test_testAndPreview_negative_validationCases_noChannelSpecified(self):
        payload = copy.deepcopy(self.testAndControlPayload['SMS'])
        payload['messageContent']['mesage_content_1'].pop('channel')
        testPreviewResponse, testPreviewPayload = TestPreview.create('LIVE', 'ORG', 'MOBILE', 0, payload=payload)
        TestPreview.assertResponse(testPreviewResponse, 400, 102,
                                   'Invalid request : Channel in message content is required.')

    def test_testAndPreview_negative_validationCases_UnknownTagInMessage(self):
        payload = copy.deepcopy(self.testAndControlPayload['SMS'])
        payload['messageContent']['mesage_content_1'][
            'messageBody'] = 'Automation Negative Case{{Unknwon_Tag}} {{optout}}'
        payload['messageContent']['mesage_content_1'].pop("offers")
        testPreviewResponse, testPreviewPayload = TestPreview.create('LIVE', 'ORG', 'MOBILE', 0, payload=payload,couponEnabled=False)
        TestPreview.assertResponse(testPreviewResponse, 400, 3067, 'Invalid request : Unsupported Tag {{Unknwon_Tag}}')

    def test_testAndPreview_negative_validationCases_MultipleUnknownTagInMessage(self):
        payload = copy.deepcopy(self.testAndControlPayload['SMS'])
        payload['messageContent']['mesage_content_1'][
            'messageBody'] = 'Automation Negative Case {{Unknwon_Tag}} {{Unknown_Tag_2}} {{optout}}'
        payload['messageContent']['mesage_content_1'].pop("offers")
        testPreviewResponse, testPreviewPayload = TestPreview.create('LIVE', 'ORG', 'MOBILE', 0, payload=payload,couponEnabled=False)

        TestPreview.assertResponse(testPreviewResponse, 400, 3067, ['Unsupported Tag {{Unknwon_Tag}}',
                                                                   'Unsupported Tag {{Unknown_Tag_2}}'])

    def test_testAndPreview_negative_validationCases_sms_withoutOptoutTag(self):
        payload = copy.deepcopy(self.testAndControlPayload['SMS'])
        payload['messageContent']['mesage_content_1'][
            'messageBody'] = 'Automation Negative Case Without Optout tag'
        payload['messageContent']['mesage_content_1'].pop("offers")
        testPreviewResponse, testPreviewPayload = TestPreview.create('LIVE', 'ORG', 'MOBILE', 0, payload=payload)
        TestPreview.assertResponse(testPreviewResponse, 400, 3066,
                                   'Invalid message content : Optout tag must be present in message.')

    def test_testAndPreview_negative_validationCases_email_withoutUnsubscribeTag(self):
        payload = copy.deepcopy(self.testAndControlPayload['EMAIL'])
        payload['messageContent']['mesage_content_1'][
            'emailBody'] = 'Automation Negative Case Without Unsubscribe tag'
        payload['messageContent']['mesage_content_1'].pop("offers")
        testPreviewResponse, testPreviewPayload = TestPreview.create('LIVE', 'ORG', 'MOBILE', 0, payload=payload)
        TestPreview.assertResponse(testPreviewResponse, 400, 3066,
                                   'Invalid message content : Unsubscribe tag must be present in email.')

    def test_testAndPreview_negative_validationCases_couponTag_withoutOffers(self):
        payload = copy.deepcopy(self.testAndControlPayload['SMS'])
        payload['messageContent']['mesage_content_1'][
            'messageBody'] = 'Automation Negative Case Coupon tag without Incentive info {{voucher}} {{optout}}'
        payload['messageContent']['mesage_content_1'].pop('offers')
        testPreviewResponse, testPreviewPayload = TestPreview.create('LIVE', 'ORG', 'MOBILE', 0, payload=payload)
        TestPreview.assertResponse(testPreviewResponse, 400, 3067,
                                   'Coupon offer should be attached to use voucher tag')

    def test_testAndPreview_negative_validationCases_wrongChannel(self):
        payload = copy.deepcopy(self.testAndControlPayload['SMS'])
        payload['messageContent']['mesage_content_1']['channel'] = 'Auto'
        testPreviewResponse, testPreviewPayload = TestPreview.create('LIVE', 'ORG', 'MOBILE', 0, payload=payload)
        TestPreview.assertResponse(testPreviewResponse, 400, 104,
                                   'Invalid request : channel , Unknown value Auto, allowed values are [SMS, EMAIL, MOBILEPUSH, CALL_TASK, WECHAT]')

    def test_testAndPreview_negative_validationCases_wrongCouponSeriesId(self):
        payload = copy.deepcopy(self.testAndControlPayload['SMS'])
        payload['messageContent']['mesage_content_1']['offers'][0]['couponSeriesId'] = 'Auto'
        testPreviewResponse, testPreviewPayload = TestPreview.create('LIVE', 'ORG', 'MOBILE', 0, payload=payload)
        TestPreview.assertResponse(testPreviewResponse, 400, 104,
                                   'Invalid request : invalid value for field couponSeriesId')

    def test_testAndPreview_negative_validationCases_noCouponType(self):
        payload = copy.deepcopy(self.testAndControlPayload['SMS'])
        payload['messageContent']['mesage_content_1']['offers'][0].pop('type')
        testPreviewResponse, testPreviewPayload = TestPreview.create('LIVE', 'ORG', 'MOBILE', 0, payload=payload)
        TestPreview.assertResponse(testPreviewResponse, 400, 107, 'Unrecognized field : couponSeriesId')

    def test_testAndPreview_negative_validationCases_multipleTestAndPreviewWithSameIdentifier(self):
        payload = copy.deepcopy(self.testAndControlPayload['SMS'])
        payload['messageContent']['mesage_content_1'].pop('offers')
        testPreviewResponse, testPreviewPayload = TestPreview.create('LIVE', 'ORG', 'MOBILE', 0, payload=payload)
        TestPreview.assertResponse(testPreviewResponse, 200)
        testPreviewResponse, testPreviewPayload = TestPreview.create('LIVE', 'ORG', 'MOBILE', 0, payload=payload)
        TestPreview.assertResponse(testPreviewResponse, 200)

    def test_testAndPreview_negative_validationCases_messageContent1_AsEmpty(self):
        payload = copy.deepcopy(self.testAndControlPayload['SMS'])
        payload['messageContent']['mesage_content_1'] = {}
        testPreviewResponse, testPreviewPayload = TestPreview.create('LIVE', 'ORG', 'MOBILE', 0, payload=payload)
        TestPreview.assertResponse(testPreviewResponse, 400, 102,['Invalid request : Message body is required in message content.',
                    'Invalid request : Channel in message content is required.'])

    def test_testAndPreview_negative_validationCases_wrongAuth(self):
        previousAuth = IrisHelper.updateUserName('First')
        try:
            payload = copy.deepcopy(self.testAndControlPayload['SMS'])
            testPreviewResponse, testPreviewPayload = TestPreview.create('LIVE', 'ORG', 'MOBILE', 0, payload=payload)
            TestPreview.assertResponse(testPreviewResponse, 401, 999999, 'Unauthorized')
        except Exception, exp:
            Assertion.constructAssertion(False, 'Exception Occured :{}'.format(exp))
        finally:
            IrisHelper.updateUserName(previousAuth)

    def test_testAndPreview_negative_validationCases_emptyAuth(self):
        previousAuth = IrisHelper.updateUserName('')
        previousPass = IrisHelper.updatepassword('')
        try:
            payload = copy.deepcopy(self.testAndControlPayload['SMS'])
            testPreviewResponse, testPreviewPayload = TestPreview.create('LIVE', 'ORG', 'MOBILE', 0, payload=payload)
            TestPreview.assertResponse(testPreviewResponse, 401, 999999, 'Unauthorized')
        except Exception, exp:
            Assertion.constructAssertion(False, 'Exception Occured :{}'.format(exp))
        finally:
            IrisHelper.updateUserName(previousAuth)
            IrisHelper.updatepassword(previousPass)

    def test_testAndPreview_negative_validationCases_wrongCampaignId(self):
        payload = copy.deepcopy(self.testAndControlPayload['SMS'])
        testPreviewResponse, testPreviewPayload = TestPreview.create('LIVE', 'ORG', 'MOBILE', 0, payload=payload,
                                                                     campaignId=0)
        TestPreview.assertResponse(testPreviewResponse, 400, 102,
                                   'Invalid request : campaignId must be greater than or equal to 1')

