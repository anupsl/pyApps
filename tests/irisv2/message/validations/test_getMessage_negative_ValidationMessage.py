import pytest

from src.modules.irisv2.helper.irisHelper import IrisHelper
from src.modules.irisv2.message.createMessage import CreateMessage
from src.modules.irisv2.message.getMessage import GetMessage
from src.utilities.assertion import Assertion
from src.utilities.logger import Logger
from src.modules.irisv2.campaigns.createCampaign import CreateCampaign

class Test_GetMessage_Negative_ValidationMessage():
    def setup_method(self, method):
        Logger.logMethodName(method.__name__)

    def setup_class(self):
        messageInfo = {
            'scheduleType': {'type': 'IMMEDIATE'},
            'offerType': 'POINTS',
            'messageStrategy': {'type': 'DEFAULT'},
            'channels': ['SMS', 'EMAIL'],
            'useTinyUrl': False,
            'encryptUrl': False,
            'skipRateLimit': True
        }
        self.campaignId = GetMessage.getCampaignIDHavingNoMessage('LIVE', 'ORG')
        self.messageDetails = CreateMessage.create('LIVE', 'ORG', 'UPLOAD', 'MOBILE', messageInfo,campaignId=self.campaignId)

    @pytest.mark.parametrize('wrongMessageId', [
        ('xxxxx'),
        ('$'),
        ('99999')

    ])
    def test_getMessage_negative_validationMessage_wrongValueOfMessageId(self, wrongMessageId):
        response = GetMessage.getMessageById(self.campaignId, wrongMessageId)
        GetMessage.assertResponse(response, 400,3023,'Message with message id {} does not exists'.format(wrongMessageId))

    @pytest.mark.parametrize('wrongMessageId', [
        ('')
    ])
    def test_getMessage_negative_validationMessage_withoutTheMessageId(self, wrongMessageId):
        response = GetMessage.getMessageById(self.campaignId, wrongMessageId)
        GetMessage.assertResponse(response, 200)

    @pytest.mark.parametrize('wrongMessageId', [
        ('xxxxx'),
        ('$'),
        ('99999')
    ])
    def test_getMessage_negative_validationMessage_usingVarinatId(self, wrongMessageId):
        response = GetMessage.getMessageVariantById(self.campaignId, wrongMessageId)
        GetMessage.assertResponse(response, 400, 3040,
                                  'Message with message id {} does not exists'.format(wrongMessageId))

    @pytest.mark.parametrize('wrongMessageId', [
        ('')
    ])
    def test_getMessage_negative_validationMessage_usingVarinatId(self, wrongMessageId):
        response = GetMessage.getMessageVariantById(self.campaignId, wrongMessageId)
        GetMessage.assertResponse(response, 400, 3023, 'Message with message id variant does not exists')

    def test_getMessage_negative_validationMessage_unknownQueryParam(self):
        response = GetMessage.getMessageById(self.campaignId, self.messageDetails['RESPONSE']['json']['entity']['id'],
                                             queryParam=[('include', 'true')])
        GetMessage.assertResponse(response, 200)

    def test_getMessage_negative_validationMessage_wrongValueOfIncludeVariant(self):
        response = GetMessage.getMessageById(self.campaignId, self.messageDetails['RESPONSE']['json']['entity']['id'],
                                             queryParam=[('includeAudience', '$$$$$$')])
        GetMessage.assertResponse(response, 200)

    def test_getMessage_negative_validationMessage_wrongCampaignId(self):
        response = GetMessage.getMessageById(99999, self.messageDetails['RESPONSE']['json']['entity']['id'],
                                             queryParam=[('includeAudience', '$$$$$$')])
        GetMessage.assertResponse(response, 400, 1007, 'Campaign Id Exception : Invalid Campaign Id Passed 99999')

    def test_getMessage_negative_validationMessage_withCampaignId_differentCampaign(self):
        campaignInfo = CreateCampaign.create('LIVE','CUSTOM')
        diffId = campaignInfo['ID']
        response = GetMessage.getMessageById(diffId, self.messageDetails['RESPONSE']['json']['entity']['id'],
                                             queryParam=[('includeAudience', '$$$$$$')])
        GetMessage.assertResponse(response, 400, 3023, 'Message with message id {} does not exists'.format(self.messageDetails['RESPONSE']['json']['entity']['id']))

    def test_getMessage_negative_validationMessage_wrongOrgId(self):
        previousOrgId = IrisHelper.updateOrgId(0)
        try:
            response = GetMessage.getMessageById(self.campaignId,
                                                 self.messageDetails['RESPONSE']['json']['entity']['id'],
                                                 queryParam=[('include', 'true')])
            GetMessage.assertResponse(response, 400, 1007,
                                      'Campaign Id Exception : Invalid Campaign Id Passed {}'.format(self.campaignId))
        except Exception, exp:
            Assertion.constructAssertion(False, 'Exception Occured :{}'.format(exp))
        finally:
            IrisHelper.updateOrgId(previousOrgId)

    def test_getMessage_negative_validationMessagewrongAuth(self):
        previousUser = IrisHelper.updateUserName('XXXXXX')
        try:
            response = GetMessage.getMessageById(self.campaignId,
                                                 self.messageDetails['RESPONSE']['json']['entity']['id'],
                                                 queryParam=[('include', 'true')])
            GetMessage.assertResponse(response, 401,999999, 'Unauthorized')
        except Exception, exp:
            Assertion.constructAssertion(False, 'Exception Occured :{}'.format(exp))
        finally:
            IrisHelper.updateUserName(previousUser)

    def test_getMessage_negative_validationMessage_getVariant_withMessageId(self):
        response = GetMessage.getMessageVariantById(self.campaignId, self.messageDetails['RESPONSE']['json']['entity']['id'])
        GetMessage.assertResponse(response, 400, 3040,
                                  'Message variant with id {} does not exists'.format(
                                      self.messageDetails['RESPONSE']['json']['entity']['id']))
