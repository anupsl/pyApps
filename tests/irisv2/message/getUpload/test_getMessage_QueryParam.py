import pytest

from src.Constant.constant import constant
from src.dbCalls.messageInfo import message_calls
from src.modules.irisv2.list.getListDBAssertion import GetListDBAssertion
from src.modules.irisv2.message.createMessage import CreateMessage
from src.modules.irisv2.message.createMessageDbAssertion import CreateMessageDBAssertion
from src.modules.irisv2.message.getMessage import GetMessage
from src.modules.irisv2.message.variantDbAssertion import VariantDBAssertion
from src.utilities.assertion import Assertion
from src.utilities.logger import Logger



@pytest.mark.run(order=41)
class Test_GetMessage_QueryParam():
    def setup_method(self, method):
        Logger.logMethodName(method.__name__)

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'EMAIL',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),

    ])
    def test_irisv2_getMessage_queryParam_withVariation_Sanity(self, campaignType, testControlType, listType,
                                                                      channel,
                                                                      messageInfo):
        CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo)

        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        messageId = constant.config['node'][campaignType][testControlType]['LIST'][listType][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['RESPONSE']['json']['entity']['id']

        for eachType in ['MESSAGE_TARGET_AUDIENCE', 'VARIANT_CREATION']:
            status = message_calls().waitForJobDetailsStatusToClose(messageId, eachType, maxNumberOfAttempts=20)

        if status:
            getMessageResponse = GetMessage.getMessageById(campaignId, messageId, [('includeVariant', 'true')])
            GetMessage.assertResponse(getMessageResponse, 200)
            CreateMessageDBAssertion(campaignId, messageId, getMessageResponse['json']['entity']).check()
            VariantDBAssertion(campaignId, messageId,
                               getMessageResponse['json']['entity']['messageVariantList']).check()
        else:
            Assertion.constructAssertion(False, 'Variant_Creation is Not Closed in Specified time')

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('UPCOMING', 'CUSTOM', 'UPLOAD', 'EMAIL',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'SKIP', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def test_irisv2_getMessage_queryParam_withVariation(self, campaignType, testControlType, listType,
                                                                      channel,
                                                                      messageInfo):
        CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo)

        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        messageId = constant.config['node'][campaignType][testControlType]['LIST'][listType][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['RESPONSE']['json']['entity']['id']

        for eachType in ['MESSAGE_TARGET_AUDIENCE', 'VARIANT_CREATION']:
            status = message_calls().waitForJobDetailsStatusToClose(messageId, eachType, maxNumberOfAttempts=20)

        if status:
            getMessageResponse = GetMessage.getMessageById(campaignId, messageId, [('includeVariant', 'true')])
            GetMessage.assertResponse(getMessageResponse, 200)
            CreateMessageDBAssertion(campaignId, messageId, getMessageResponse['json']['entity']).check()
            VariantDBAssertion(campaignId, messageId,
                               getMessageResponse['json']['entity']['messageVariantList']).check()
        else:
            Assertion.constructAssertion(False, 'Variant_Creation is Not Closed in Specified time')



    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'SKIP', 'UPLOAD', 'EMAIL',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def test_irisv2_getMessage_queryParam_withVariation_OfferType(self, campaignType, testControlType, listType,
                                                                         channel,
                                                                         messageInfo):
        CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo)

        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        messageId = constant.config['node'][campaignType][testControlType]['LIST'][listType][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['RESPONSE']['json']['entity']['id']

        for eachType in ['MESSAGE_TARGET_AUDIENCE', 'VARIANT_CREATION']:
            status = message_calls().waitForJobDetailsStatusToClose(messageId, eachType, maxNumberOfAttempts=20)

        if status:
            getMessageResponse = GetMessage.getMessageById(campaignId, messageId, [('includeVariant', 'true')])
            GetMessage.assertResponse(getMessageResponse, 200)
            CreateMessageDBAssertion(campaignId, messageId, getMessageResponse['json']['entity']).check()
            VariantDBAssertion(campaignId, messageId,
                               getMessageResponse['json']['entity']['messageVariantList'], offer=True).check()
        else:
            Assertion.constructAssertion(False, 'Variant_Creation is Not Closed in Specified time')

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'SKIP', 'UPLOAD', 'EMAIL',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'SKIP', 'UPLOAD', 'EMAIL',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
    ])
    def test_irisv2_getMessage_queryParam_withTargetAudience(self, campaignType, testControlType, listType,
                                                                    channel, messageInfo):
        CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo)

        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        messageId = constant.config['node'][campaignType][testControlType]['LIST'][listType][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['RESPONSE']['json']['entity']['id']

        getMessageResponse = GetMessage.getMessageById(campaignId, messageId, [('includeAudience', 'true')])
        GetMessage.assertResponse(getMessageResponse, 200)
        CreateMessageDBAssertion(campaignId, messageId, getMessageResponse['json']['entity']).check()
        GetListDBAssertion(
            constant.config['node'][campaignType][testControlType]['LIST'][listType][channel]['ID'],
            {'json':
                {
                    'entity': getMessageResponse['json']['entity']['targetAudience'][
                        'includeAudienceGroupInfo'][0]
                }
            },
            campaignHashLookUp=False, createAudienceJob=False, reachabilityCheck=False, campaignGroupRecipients=False
        ).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'CUSTOM', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'SKIP', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def test_irisv2_getMessage_queryParam_WithBothTargetAudienceAndVariation_WithoutOffer(self, campaignType,
                                                                                          testControlType,
                                                                                          listType,
                                                                                          channel,
                                                                                          messageInfo):
        CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo)

        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        messageId = constant.config['node'][campaignType][testControlType]['LIST'][listType][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['RESPONSE']['json']['entity']['id']

        for eachType in ['MESSAGE_TARGET_AUDIENCE', 'VARIANT_CREATION']:
            status = message_calls().waitForJobDetailsStatusToClose(messageId, eachType, maxNumberOfAttempts=20)

        if status:
            getMessageResponse = GetMessage.getMessageById(campaignId, messageId,
                                                           [('includeVariant', 'true'), ('includeAudience', 'true')])
            GetMessage.assertResponse(getMessageResponse, 200)
            CreateMessageDBAssertion(campaignId, messageId, getMessageResponse['json']['entity']).check()
            VariantDBAssertion(campaignId, messageId,
                               getMessageResponse['json']['entity']['messageVariantList'], offer=True).check()
            GetListDBAssertion(
                constant.config['node'][campaignType][testControlType]['LIST'][listType][channel]['ID'],
                {'json':
                    {
                        'entity': getMessageResponse['json']['entity']['targetAudience'][
                            'includeAudienceGroupInfo'][0]
                    }
                },
                campaignHashLookUp=False, createAudienceJob=False, reachabilityCheck=False,
                campaignGroupRecipients=False
            ).check()
        else:
            Assertion.constructAssertion(False, 'Variant_Creation is Not Closed in Specified time')

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'EMAIL',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
    ])
    def test_irisv2_getMessage_queryParam_WithBothTargetAudienceAndVariation_HavingOffer(self, campaignType,
                                                                                         testControlType,
                                                                                         listType,
                                                                                         channel,
                                                                                         messageInfo):
        CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo)

        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        messageId = constant.config['node'][campaignType][testControlType]['LIST'][listType][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['RESPONSE']['json']['entity']['id']

        for eachType in ['MESSAGE_TARGET_AUDIENCE', 'VARIANT_CREATION']:
            status = message_calls().waitForJobDetailsStatusToClose(messageId, eachType, maxNumberOfAttempts=20)

        if status:
            getMessageResponse = GetMessage.getMessageById(campaignId, messageId,
                                                           [('includeVariant', 'true'), ('includeAudience', 'true')])
            GetMessage.assertResponse(getMessageResponse, 200)
            CreateMessageDBAssertion(campaignId, messageId, getMessageResponse['json']['entity']).check()
            VariantDBAssertion(campaignId, messageId,
                               getMessageResponse['json']['entity']['messageVariantList'], offer=True).check()
            GetListDBAssertion(
                constant.config['node'][campaignType][testControlType]['LIST'][listType][channel]['ID'],
                {'json':
                    {
                        'entity': getMessageResponse['json']['entity']['targetAudience'][
                            'includeAudienceGroupInfo'][0]
                    }
                },
                campaignHashLookUp=False, createAudienceJob=False, reachabilityCheck=False,
                campaignGroupRecipients=False
            ).check()
        else:
            Assertion.constructAssertion(False, 'Variant_Creation is Not Closed in Specified time')

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'EMAIL',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def test_irisv2_getMessage_queryParam_With_QueryParamPassedButAsFalse(self, campaignType,
                                                                          testControlType,
                                                                          listType,
                                                                          channel,
                                                                          messageInfo):
        CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo)

        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        messageId = constant.config['node'][campaignType][testControlType]['LIST'][listType][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['RESPONSE']['json']['entity']['id']

        for eachType in ['MESSAGE_TARGET_AUDIENCE', 'VARIANT_CREATION']:
            status = message_calls().waitForJobDetailsStatusToClose(messageId, eachType, maxNumberOfAttempts=20)

        if status:
            getMessageResponse = GetMessage.getMessageById(campaignId, messageId,
                                                           [('includeVariant', 'false'), ('includeAudience', 'false')])
            GetMessage.assertResponse(getMessageResponse, 200)
            CreateMessageDBAssertion(campaignId, messageId, getMessageResponse['json']['entity']).check()
            Assertion.constructAssertion('messageVariantList' not in getMessageResponse['json']['entity'],
                                         'messageVariantList Key Check in Response',verify=True)
            Assertion.constructAssertion(
                'includeAudienceGroupInfo' not in getMessageResponse['json']['entity']['targetAudience'],
                'includeAudienceGroupInfo Key Check in Response->json->Entity->message->targetAudience',verify=True)
        else:
            Assertion.constructAssertion(False, 'Variant_Creation is Not Closed in Specified time')
