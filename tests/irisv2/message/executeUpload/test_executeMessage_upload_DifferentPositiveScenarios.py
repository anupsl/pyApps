import pytest

from src.Constant.constant import constant
from src.dbCalls.messageInfo import message_calls
from src.modules.irisv2.list.createAudience import CreateAudience
from src.modules.irisv2.message.authorizeMessage import AuthorizeMessage
from src.modules.irisv2.message.authorizeMessageDbAssertion import AuthorizeMessageDBAssertion
from src.modules.irisv2.message.createMessage import CreateMessage
from src.utilities.logger import Logger


@pytest.mark.run(order=30)
class Test_ApproveMessage_DifferentPositiveScenarios():
    def setup_method(self, method):
        Logger.logMethodName(method.__name__)

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo,customTags', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True},
         ['custom_tag_1']),
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True},
         ['custom_tag_1', 'custom_tag_2', 'custom_tag_3']),
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True},
         ['custom_tag_1', 'custom_tag_2', 'custom_tag_3', 'custom_tag_4', 'custom_tag_5'])
    ])
    def test_approveMessage_SMS_positiveScenarios_WithDifferntCustomTags_NewUsers(self, campaignType,
                                                                                  testControlType, listType,
                                                                                  channel, messageInfo,
                                                                                  customTags):
        listInfo = CreateAudience.uploadList(campaignType, testControlType, schemaIdentifier=[channel],
                                             schemaData=[channel, 'FIRST_NAME'] + customTags, newUser=True,
                                             campaignCheck=False, updateNode=True, lockNode=True)

        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel,
                                              messageInfo=messageInfo, listInfo=listInfo, updateNode=True,
                                              lockNode=True, numberOfCustomTag=len(customTags))
        if not message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'],
                                                              'VARIANT_CREATION'):
            raise Exception('VariantNotCreatedException')

        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        approveRespone = AuthorizeMessage.approveWithCampaignAndMessageId(campaignId,
                                                                          messageDetails['RESPONSE']['json'][
                                                                              'entity']['id'])
        AuthorizeMessage.assertResponse(approveRespone, 200)
        AuthorizeMessageDBAssertion(campaignId, messageDetails['RESPONSE'], messageDetails['PAYLOAD'],
                                    testControlType).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo,customTags', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True},
         ['custom_tag_1']),
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True},
         ['custom_tag_1', 'custom_tag_2', 'custom_tag_3']),
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True},
         ['custom_tag_1', 'custom_tag_2', 'custom_tag_3', 'custom_tag_4', 'custom_tag_5'])
    ])
    def test_approveMessage_SMS_positiveScenarios_WithDifferntCustomTags_ExistingUsers(self, campaignType,
                                                                                       testControlType, listType,
                                                                                       channel, messageInfo,
                                                                                       customTags):
        listInfo = CreateAudience.uploadList(campaignType, testControlType, schemaIdentifier=[channel],
                                             schemaData=[channel, 'FIRST_NAME'] + customTags, newUser=False,
                                             campaignCheck=False, updateNode=True, lockNode=True)

        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel,
                                              messageInfo=messageInfo, listInfo=listInfo, updateNode=True,
                                              lockNode=True, numberOfCustomTag=len(customTags))
        if not message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'],
                                                              'VARIANT_CREATION'):
            raise Exception('VariantNotCreatedException')

        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        approveRespone = AuthorizeMessage.approveWithCampaignAndMessageId(campaignId,
                                                                          messageDetails['RESPONSE']['json'][
                                                                              'entity']['id'])
        AuthorizeMessage.assertResponse(approveRespone, 200)
        AuthorizeMessageDBAssertion(campaignId, messageDetails['RESPONSE'], messageDetails['PAYLOAD'],
                                    testControlType).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo,customTags', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True},
         ['custom_tag_1']),
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True},
         ['custom_tag_1', 'custom_tag_2', 'custom_tag_3']),
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True},
         ['custom_tag_1', 'custom_tag_2', 'custom_tag_3', 'custom_tag_4', 'custom_tag_5'])
    ])
    def test_approveMessage_SMS_positiveScenarios_WithDifferntCustomTags_coupons_ExistingUsers(self, campaignType,
                                                                                       testControlType, listType,
                                                                                       channel, messageInfo,
                                                                                       customTags):
        listInfo = CreateAudience.uploadList(campaignType, testControlType, schemaIdentifier=[channel],
                                             schemaData=[channel, 'FIRST_NAME'] + customTags, newUser=False,
                                             campaignCheck=False, updateNode=True, lockNode=True)

        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel,
                                              messageInfo=messageInfo, listInfo=listInfo, updateNode=True,
                                              lockNode=True, numberOfCustomTag=len(customTags))
        if not message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'],
                                                              'VARIANT_CREATION'):
            raise Exception('VariantNotCreatedException')

        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        approveRespone = AuthorizeMessage.approveWithCampaignAndMessageId(campaignId,
                                                                          messageDetails['RESPONSE']['json'][
                                                                              'entity']['id'])
        AuthorizeMessage.assertResponse(approveRespone, 200)
        AuthorizeMessageDBAssertion(campaignId, messageDetails['RESPONSE'], messageDetails['PAYLOAD'],
                                    testControlType).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo,customTags', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True},
         ['custom_tag_1']),
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True},
         ['custom_tag_1', 'custom_tag_2', 'custom_tag_3']),
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True},
         ['custom_tag_1', 'custom_tag_2', 'custom_tag_3', 'custom_tag_4', 'custom_tag_5'])
    ])
    def test_approveMessage_SMS_positiveScenarios_WithDifferntCustomTags_points_ExistingUsers(self, campaignType,
                                                                                               testControlType,
                                                                                               listType,
                                                                                               channel, messageInfo,
                                                                                               customTags):
        listInfo = CreateAudience.uploadList(campaignType, testControlType, schemaIdentifier=[channel],
                                             schemaData=[channel, 'FIRST_NAME'] + customTags, newUser=False,
                                             campaignCheck=False, updateNode=True, lockNode=True)

        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel,
                                              messageInfo=messageInfo, listInfo=listInfo, updateNode=True,
                                              lockNode=True, numberOfCustomTag=len(customTags))
        if not message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'],
                                                              'VARIANT_CREATION'):
            raise Exception('VariantNotCreatedException')

        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        approveRespone = AuthorizeMessage.approveWithCampaignAndMessageId(campaignId,
                                                                          messageDetails['RESPONSE']['json'][
                                                                              'entity']['id'])
        AuthorizeMessage.assertResponse(approveRespone, 200)
        AuthorizeMessageDBAssertion(campaignId, messageDetails['RESPONSE'], messageDetails['PAYLOAD'],
                                    testControlType).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo,customTags', [
        ('LIVE', 'ORG', 'UPLOAD', 'EMAIL',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True},
         ['custom_tag_1']),
        ('LIVE', 'ORG', 'UPLOAD', 'EMAIL',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True},
         ['custom_tag_1', 'custom_tag_2', 'custom_tag_3']),
        ('LIVE', 'ORG', 'UPLOAD', 'EMAIL',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True},
         ['custom_tag_1', 'custom_tag_2', 'custom_tag_3', 'custom_tag_4', 'custom_tag_5'])
    ])
    def test_approveMessage_EMAIl_positiveScenarios_WithDifferntCustomTags(self, campaignType, testControlType,
                                                                           listType,
                                                                           channel, messageInfo, customTags):
        listInfo = CreateAudience.uploadList(campaignType, testControlType, schemaIdentifier=[channel],
                                             schemaData=[channel, 'FIRST_NAME'] + customTags, newUser=False,
                                             campaignCheck=False, updateNode=True, lockNode=True)

        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel,
                                              messageInfo=messageInfo, listInfo=listInfo, updateNode=True,
                                              lockNode=True, numberOfCustomTag=len(customTags))
        if not message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'],
                                                              'VARIANT_CREATION'):
            raise Exception('VariantNotCreatedException')

        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        approveRespone = AuthorizeMessage.approveWithCampaignAndMessageId(campaignId,
                                                                          messageDetails['RESPONSE']['json'][
                                                                              'entity']['id'])
        AuthorizeMessage.assertResponse(approveRespone, 200)
        AuthorizeMessageDBAssertion(campaignId, messageDetails['RESPONSE'], messageDetails['PAYLOAD'],
                                    testControlType).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo,customTags', [
        ('LIVE', 'ORG', 'UPLOAD', 'USER_ID',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True},
         ['custom_tag_1']),
        ('LIVE', 'ORG', 'UPLOAD', 'USER_ID',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True},
         ['custom_tag_1', 'custom_tag_2', 'custom_tag_3']),
        ('LIVE', 'ORG', 'UPLOAD', 'USER_ID',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True},
         ['custom_tag_1', 'custom_tag_2', 'custom_tag_3', 'custom_tag_4', 'custom_tag_5'])
    ])
    def test_approveMessage_USER_ID_positiveScenarios_WithDifferntCustomTags(self, campaignType, testControlType,
                                                                             listType,
                                                                             channel, messageInfo, customTags):
        listInfo = CreateAudience.uploadList(campaignType, testControlType, schemaIdentifier=[channel],
                                             schemaData=[channel, 'FIRST_NAME'] + customTags, newUser=False,
                                             campaignCheck=False, updateNode=True, lockNode=True)

        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel,
                                              messageInfo=messageInfo, listInfo=listInfo, updateNode=True,
                                              lockNode=True, numberOfCustomTag=len(customTags))
        if not message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'],
                                                              'VARIANT_CREATION'):
            raise Exception('VariantNotCreatedException')

        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        approveRespone = AuthorizeMessage.approveWithCampaignAndMessageId(campaignId,
                                                                          messageDetails['RESPONSE']['json'][
                                                                              'entity']['id'])
        AuthorizeMessage.assertResponse(approveRespone, 200)
        AuthorizeMessageDBAssertion(campaignId, messageDetails['RESPONSE'], messageDetails['PAYLOAD'],
                                    testControlType).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo,customTags', [
        ('LIVE', 'ORG', 'UPLOAD', 'EXTERNAL_ID',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True},
         ['custom_tag_1']),
        ('LIVE', 'ORG', 'UPLOAD', 'EXTERNAL_ID',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True},
         ['custom_tag_1', 'custom_tag_2', 'custom_tag_3']),
        ('LIVE', 'ORG', 'UPLOAD', 'EXTERNAL_ID',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True},
         ['custom_tag_1', 'custom_tag_2', 'custom_tag_3', 'custom_tag_4', 'custom_tag_5'])
    ])
    def test_approveMessage_USER_ID_positiveScenarios_WithDifferntCustomTags(self, campaignType, testControlType,
                                                                             listType,
                                                                             channel, messageInfo, customTags):
        listInfo = CreateAudience.uploadList(campaignType, testControlType, schemaIdentifier=[channel],
                                             schemaData=[channel, 'FIRST_NAME'] + customTags, newUser=False,
                                             campaignCheck=False, updateNode=True, lockNode=True)

        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel,
                                              messageInfo=messageInfo, listInfo=listInfo, updateNode=True,
                                              lockNode=True, numberOfCustomTag=len(customTags))
        if not message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'],
                                                              'VARIANT_CREATION'):
            raise Exception('VariantNotCreatedException')

        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        approveRespone = AuthorizeMessage.approveWithCampaignAndMessageId(campaignId,
                                                                          messageDetails['RESPONSE']['json'][
                                                                              'entity']['id'])
        AuthorizeMessage.assertResponse(approveRespone, 200)
        AuthorizeMessageDBAssertion(campaignId, messageDetails['RESPONSE'], messageDetails['PAYLOAD'],
                                    testControlType).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo,storeType', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True},
         'REGISTERED_STORE'),
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True},
         'LAST_TRANSACTED_AT')
    ])
    def test_approveMessage_positiveScenarios_WithDifferntStoreType(self, campaignType, testControlType, listType,
                                                                    channel, messageInfo, storeType):
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                  updateNode=True, lockNode=True, storeType=storeType)
        AuthorizeMessage.assertResponse(approveRespone, 200)

        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        response = constant.config['node'][campaignType][testControlType]['LIST'][listType][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['RESPONSE']
        payload = constant.config['node'][campaignType][testControlType]['LIST'][listType][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['PAYLOAD']

        AuthorizeMessageDBAssertion(campaignId, response, payload, testControlType).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo,customTags', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True},
         ['custom_tag_1'])
    ])
    def test_approveMessage_SMS_positiveScenarios_WithDifferntCustomTags_NewUsers_particularDate(self, campaignType,
                                                                                  testControlType, listType,
                                                                                  channel, messageInfo,
                                                                                  customTags):
        listInfo = CreateAudience.uploadList(campaignType, testControlType, schemaIdentifier=[channel],
                                             schemaData=[channel, 'FIRST_NAME'] + customTags, newUser=True,
                                             campaignCheck=False, updateNode=True, lockNode=True)

        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel,
                                              messageInfo=messageInfo, listInfo=listInfo, updateNode=True,
                                              lockNode=True, numberOfCustomTag=len(customTags))
        if not message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'],
                                                              'VARIANT_CREATION'):
            raise Exception('VariantNotCreatedException')

        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        approveRespone = AuthorizeMessage.approveWithCampaignAndMessageId(campaignId,
                                                                          messageDetails['RESPONSE']['json'][
                                                                              'entity']['id'])
        AuthorizeMessage.assertResponse(approveRespone, 200)
        AuthorizeMessageDBAssertion(campaignId, messageDetails['RESPONSE'], messageDetails['PAYLOAD'],
                                    testControlType).check()