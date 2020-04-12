import pytest
import time

from src.Constant.constant import constant
from src.dbCalls.messageInfo import message_calls
from src.modules.irisv2.campaigns.createCampaign import CreateCampaign
from src.modules.irisv2.helper.irisHelper import IrisHelper
from src.modules.irisv2.list.createAudience import CreateAudience
from src.modules.irisv2.message.authorizeMessage import AuthorizeMessage
from src.modules.irisv2.message.authorizeMessageDbAssertion import AuthorizeMessageDBAssertion
from src.modules.irisv2.message.createMessage import CreateMessage
from src.modules.irisv2.message.createMessageDbAssertion import CreateMessageDBAssertion
from src.utilities.logger import Logger
from src.utilities.utils import Utils


class Test_Message_Pair_Edit():
    def setup_method(self, method):
        Logger.logMethodName(method.__name__)

    def setup_class(self):
        Logger.logSuiteName(str(self).split('.')[-1])
        self.listInfo = CreateAudience.uploadList('LAPSED', 'ORG')
        self.listInfoFilter = CreateAudience.FilterList('LAPSED', 'ORG')
        constant.config['FilterListID'] = CreateAudience.FilterList('LAPSED', 'ORG', campaignCheck=False)['ID']
        CreateAudience.getPocUsers()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo,toOfferType', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}, 'COUPON'),
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}, 'MULTICOUPONS')
    ])
    def test_thread1_irisv2_messageEdit_Pair_immediate_org_offer_Plain_Coupon(self, campaignType, testControlType, listType,
                                                                      channel, messageInfo, toOfferType):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True, lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION')
        editInfo = {
            'messageContent': CreateMessage.constructMessageContent(campaignType, testControlType, {'type': 'DEFAULT'},
                                                                    toOfferType, channel)
        }
        editInfo = CreateMessage.edit(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                      messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],
                                      editInfo)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 editInfo['RESPONSE']['json']['entity']['id'], editInfo['PAYLOAD'], version=1).check()
        CreateMessage.assertResponse(editInfo['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(editInfo['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION', version=1)
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                  messageCreateResponse=editInfo)
        AuthorizeMessage.assertResponse(approveRespone, 200)
        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        AuthorizeMessageDBAssertion(campaignId, editInfo['RESPONSE'], editInfo['PAYLOAD'],
                                    testControlType, version=1).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'CUSTOM', 'UPLOAD', 'EMAIL',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def test_thread1_irisv2_messageEdit_Pair_particularDate_custom_list_upload_filter(self, campaignType, testControlType,
                                                                              listType,
                                                                              channel, messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True, lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION')
        editInfo = {
            'targetAudience': {
                'include': [constant.config['FilterListID']],
                'exclude': []
            },
            'messageContent': CreateMessage.constructMessageContent(campaignType, testControlType, {'type': 'DEFAULT'},
                                                                    'POINTS', channel)
        }
        editInfo = CreateMessage.edit(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                      messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],
                                      editInfo)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 editInfo['RESPONSE']['json']['entity']['id'], editInfo['PAYLOAD'], version=1).check()
        CreateMessage.assertResponse(editInfo['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(editInfo['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION', version=1)
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                  messageCreateResponse=editInfo)
        AuthorizeMessage.assertResponse(approveRespone, 200)
        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        AuthorizeMessageDBAssertion(campaignId, editInfo['RESPONSE'], editInfo['PAYLOAD'],
                                    testControlType, version=1).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('UPCOMING', 'SKIP', 'LOYALTY', 'EMAIL',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'SKIP', 'LOYALTY', 'EMAIL',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'MULTICOUPONS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def test_thread2_irisv2_messageEdit_Pair_email_recurring_skip_offerEdit_coupon_plain_stickyListAdded(self, campaignType,
                                                                                                 testControlType,
                                                                                                 listType,
                                                                                                 channel, messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True, lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION')
        editInfo = {
            'messageContent': CreateMessage.constructMessageContent(campaignType, testControlType, {'type': 'DEFAULT'},
                                                                    'PLAIN', channel),
            'targetAudience': {
                'include': [constant.config['FilterListID']],
                'exclude': [],
                'orgUsers': [messageDetails['PAYLOAD']['targetAudience']['include'][0]]
            }
        }
        editInfo = CreateMessage.edit(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                      messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],
                                      editInfo)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 editInfo['RESPONSE']['json']['entity']['id'], editInfo['PAYLOAD'], version=2).check()
        CreateMessage.assertResponse(editInfo['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(editInfo['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION', version=1)
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                  messageCreateResponse=editInfo)
        AuthorizeMessage.assertResponse(approveRespone, 200)
        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        AuthorizeMessageDBAssertion(campaignId, editInfo['RESPONSE'], editInfo['PAYLOAD'],
                                    testControlType, version=2).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def test_thread2_irisv2_messageEdit_Pair_immediate_org_sms_points_listEdit_upload_derived(self, campaignType,
                                                                                      testControlType,
                                                                                      listType,
                                                                                      channel, messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True, lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION')
        derivedListInfo = CreateAudience.derivedList(campaignType, testControlType, schemaIdentifier=[channel],
                                                     newUser=True, campaignCheck=False,
                                                     derivedListInfo={
                                                         'includedGroups': ['UPLOAD', 'LOYALTY', 'DERIVED'],
                                                         'excludedGroup': ['UPLOADOLD'],
                                                         'derived': ['UPLOADOLD', 'UPLOAD', 'LOYALTY'],
                                                         'noOfUserUpload': 5})
        editInfo = {
            'targetAudience': {
                'include': [derivedListInfo['ID']],
                'exclude': []
            },
            'messageContent': CreateMessage.constructMessageContent(campaignType, testControlType, {'type': 'DEFAULT'},
                                                                    'POINTS', channel)
        }
        editInfo = CreateMessage.edit(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                      messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],
                                      editInfo)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 editInfo['RESPONSE']['json']['entity']['id'], editInfo['PAYLOAD'], version=1).check()
        CreateMessage.assertResponse(editInfo['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(editInfo['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION', version=1)
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                  messageCreateResponse=editInfo)
        AuthorizeMessage.assertResponse(approveRespone, 200)
        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        AuthorizeMessageDBAssertion(campaignId, editInfo['RESPONSE'], editInfo['PAYLOAD'],
                                    testControlType, version=1,skippedReason='No Loyalty Entry Found For User').check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'CUSTOM', 'LOYALTY', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def test_thread3_irisv2_messageEdit_Pair_particularDateEdit_Immediate_pointsEdit_Plain_ListEditLoyalty_Upload(self,
                                                                                                          campaignType,
                                                                                                          testControlType,
                                                                                                          listType,
                                                                                                          channel,
                                                                                                          messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True, lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION')
        uploadListInfo = CreateAudience.uploadList(campaignType, testControlType, schemaIdentifier=[channel],
                                                   schemaData=[channel, 'FIRST_NAME'], newUser=True,
                                                   campaignCheck=False)
        editInfo = {
            'messageContent': CreateMessage.constructMessageContent(campaignType, testControlType, {'type': 'DEFAULT'},
                                                                    'PLAIN', channel),
            'schedule': {'scheduleType': 'IMMEDIATE'},
            'targetAudience': {
                'include': [uploadListInfo['ID']],
                'exclude': []
            }

        }
        editInfo = CreateMessage.edit(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                      messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],
                                      editInfo)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 editInfo['RESPONSE']['json']['entity']['id'], editInfo['PAYLOAD'], version=1).check()
        CreateMessage.assertResponse(editInfo['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(editInfo['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION', version=1)
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                  messageCreateResponse=editInfo)
        AuthorizeMessage.assertResponse(approveRespone, 200)
        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        AuthorizeMessageDBAssertion(campaignId, editInfo['RESPONSE'], editInfo['PAYLOAD'],
                                    testControlType, version=1).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'LOYALTY', 'EMAIL',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def test_thread4_irisv2_messageEdit_Pair_immediateToParticularDate_ListEditFilterToAnotherFilterList_OfferEditPlainToPoints(
            self,
            campaignType,
            testControlType,
            listType,
            channel,
            messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True, lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION')
        editInfo = {
            'messageContent': CreateMessage.constructMessageContent(campaignType, testControlType, {'type': 'DEFAULT'},
                                                                    'POINTS', channel),
            'schedule': {'scheduleType': 'PARTICULAR_DATE',
                         'scheduledDate': Utils.getTime(minutes=3, seconds=30, milliSeconds=True)},
            'targetAudience': {
                'include': [constant.config['FilterListID']],
                'exclude': []
            }
        }
        editInfo = CreateMessage.edit(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                      messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],
                                      editInfo)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 editInfo['RESPONSE']['json']['entity']['id'], editInfo['PAYLOAD'], version=1).check()
        CreateMessage.assertResponse(editInfo['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(editInfo['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION', version=1)
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                  messageCreateResponse=editInfo)
        AuthorizeMessage.assertResponse(approveRespone, 200)
        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        AuthorizeMessageDBAssertion(campaignId, editInfo['RESPONSE'], editInfo['PAYLOAD'],
                                    testControlType, version=1).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('UPCOMING', 'SKIP', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT',
                                                                                            "android": {
                                                                                                "contentType": "TEXT",
                                                                                                "secondary_cta": {
                                                                                                    "enable": False,
                                                                                                    "value": None},
                                                                                                "primary_cta": {
                                                                                                    "enable": False,
                                                                                                    "value": None},
                                                                                                "custom": False},
                                                                                            "ios": {
                                                                                                "contentType": "TEXT",
                                                                                                "secondary_cta": {
                                                                                                    "enable": False,
                                                                                                    "value": None},
                                                                                                "primary_cta": {
                                                                                                    "enable": False,
                                                                                                    "value": None},
                                                                                                "custom": False}},
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'SKIP', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'MULTICOUPONS', 'messageStrategy': {'type': 'DEFAULT',
                                                                                                 "android": {
                                                                                                     "contentType": "TEXT",
                                                                                                     "secondary_cta": {
                                                                                                         "enable": False,
                                                                                                         "value": None},
                                                                                                     "primary_cta": {
                                                                                                         "enable": False,
                                                                                                         "value": None},
                                                                                                     "custom": False},
                                                                                                 "ios": {
                                                                                                     "contentType": "TEXT",
                                                                                                     "secondary_cta": {
                                                                                                         "enable": False,
                                                                                                         "value": None},
                                                                                                     "primary_cta": {
                                                                                                         "enable": False,
                                                                                                         "value": None},
                                                                                                     "custom": False}},
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def test_irisv2_messageEdit_Pair_MobilePush_targetAudieceEdit_AddedStickyList(self,
                                                                                  campaignType,
                                                                                  testControlType,
                                                                                  listType,
                                                                                  channel,
                                                                                  messageInfo):
        try:
            actualOrgId = IrisHelper.updateOrgId(constant.config['mobilepush']['orgId'])
            actualOrgName = IrisHelper.updateOrgName(constant.config['mobilepush']['orgName'])
            campaignInfo = CreateCampaign.create(campaignType, testControlType)

            messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                                  campaignId=campaignInfo['ID'],updateNode=True, lockNode=True)
            CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
            message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'],
                                                           'VARIANT_CREATION')
            editInfo = {
                'targetAudience': {
                    'include': messageDetails['PAYLOAD']['targetAudience']['include'],
                    'exclude': [constant.config['FilterListID']]
                    #'orgUsers': [constant.config['FilterListID']]
                }
            }
            editInfo = CreateMessage.edit(campaignInfo['ID'],
                                          messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],
                                          editInfo)
            CreateMessageDBAssertion(campaignInfo['ID'],
                                     editInfo['RESPONSE']['json']['entity']['id'], editInfo['PAYLOAD'],
                                     version=1).check()
            CreateMessage.assertResponse(editInfo['RESPONSE'], 200)
            message_calls().waitForJobDetailsStatusToClose(editInfo['RESPONSE']['json']['entity']['id'],
                                                           'VARIANT_CREATION', version=1)
            approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                      messageCreateResponse=editInfo)
            AuthorizeMessage.assertResponse(approveRespone, 200)
            campaignId = campaignInfo['ID']
            AuthorizeMessageDBAssertion(campaignId, editInfo['RESPONSE'], editInfo['PAYLOAD'],
                                        testControlType, version=1).check()
        finally:
            IrisHelper.updateOrgId(actualOrgId)
            IrisHelper.updateOrgName(actualOrgName)

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'CUSTOM', 'LOYALTY', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def test_thread5_irisv2_messageEdit_Pair_sms_immediate_custom_plain_listEditFilterToDerived(self,
                                                                                        campaignType,
                                                                                        testControlType,
                                                                                        listType,
                                                                                        channel,
                                                                                        messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True, lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION')
        derivedListInfo = CreateAudience.derivedList(campaignType, testControlType, schemaIdentifier=[channel],
                                                     newUser=True, campaignCheck=False,
                                                     derivedListInfo={
                                                         'includedGroups': ['UPLOAD', 'LOYALTY', 'DERIVED'],
                                                         'excludedGroup': ['UPLOADOLD'],
                                                         'derived': ['UPLOADOLD', 'UPLOAD', 'LOYALTY'],
                                                         'noOfUserUpload': 5})
        editInfo = {
            'messageContent': CreateMessage.constructMessageContent(campaignType, testControlType, {'type': 'DEFAULT'},
                                                                    'POINTS', channel),
            'targetAudience': {
                'include': [derivedListInfo['ID']],
                'exclude': []
            }
        }
        editInfo = CreateMessage.edit(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                      messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],
                                      editInfo)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 editInfo['RESPONSE']['json']['entity']['id'], editInfo['PAYLOAD'], version=1).check()
        CreateMessage.assertResponse(editInfo['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(editInfo['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION', version=1)
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                  messageCreateResponse=editInfo)
        AuthorizeMessage.assertResponse(approveRespone, 200)
        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        AuthorizeMessageDBAssertion(campaignId, editInfo['RESPONSE'], editInfo['PAYLOAD'],
                                    testControlType, version=1,skippedReason=['No Loyalty Entry Found For User'],cguhVerify=True).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('UPCOMING', 'SKIP', 'ORG_USERS', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def test_thread6_irisv2_messageEdit_Pair_Immediate_Skip_Upcoming_StickyListEditedToUpload(self,
                                                                                      campaignType,
                                                                                      testControlType,
                                                                                      listType,
                                                                                      channel,
                                                                                      messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True, lockNode=True,
                                              derivedListInfo={'excludeUsers': [], 'includeUsers': ':1'})
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION')
        uploadListInfo = CreateAudience.uploadList(campaignType, testControlType, schemaIdentifier=[channel],
                                                   schemaData=[channel, 'FIRST_NAME'], newUser=True,
                                                   campaignCheck=False)
        editInfo = {
            'messageContent': CreateMessage.constructMessageContent(campaignType, testControlType, {'type': 'DEFAULT'},
                                                                    'PLAIN', channel),
            'targetAudience': {
                'include': [uploadListInfo['ID']],
                'exclude': []
            }
        }
        editInfo = CreateMessage.edit(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                      messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],
                                      editInfo)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 editInfo['RESPONSE']['json']['entity']['id'], editInfo['PAYLOAD'], version=2).check()
        CreateMessage.assertResponse(editInfo['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(editInfo['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION', version=1)
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                  messageCreateResponse=editInfo)
        AuthorizeMessage.assertResponse(approveRespone, 200)
        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        AuthorizeMessageDBAssertion(campaignId, editInfo['RESPONSE'], editInfo['PAYLOAD'],
                                    testControlType, version=2).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'CUSTOM', 'ORG_USERS', 'EMAIL',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def test_thread6_irisv2_messageEdit_Pair_Immediate_Skip_Upcoming_StickyList_targetAudienceEditToUpload_ScheduleUpdateFromRecurringToParticularDate(
            self,
            campaignType,
            testControlType,
            listType,
            channel,
            messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True, lockNode=True, derivedListInfo={'excludeUsers': [], 'includeUsers': ':1'})
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION')
        uploadListInfo = CreateAudience.uploadList(campaignType, testControlType, schemaIdentifier=[channel],
                                                   schemaData=[channel, 'FIRST_NAME'], newUser=True,
                                                   campaignCheck=False)
        editInfo = {
            'targetAudience': {
                'include': [uploadListInfo['ID']],
                'exclude': []
            },
            'schedule': {'scheduleType': 'PARTICULAR_DATE',
                         'scheduledDate': Utils.getTime(minutes=3, seconds=30, milliSeconds=True)}
        }
        editInfo = CreateMessage.edit(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                      messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],
                                      editInfo)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 editInfo['RESPONSE']['json']['entity']['id'], editInfo['PAYLOAD'], version=2).check()
        CreateMessage.assertResponse(editInfo['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(editInfo['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION', version=1)
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                  messageCreateResponse=editInfo)
        AuthorizeMessage.assertResponse(approveRespone, 200)
        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        AuthorizeMessageDBAssertion(campaignId, editInfo['RESPONSE'], editInfo['PAYLOAD'],
                                    testControlType, version=2,skippedReason=['No Loyalty Entry Found For User']).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT',
                                                                                                "android": {
                                                                                                    "contentType": "TEXT",
                                                                                                    "secondary_cta": {
                                                                                                        "enable": False,
                                                                                                        "value": None},
                                                                                                    "primary_cta": {
                                                                                                        "enable": False,
                                                                                                        "value": None},
                                                                                                    "custom": False},
                                                                                                "ios": {
                                                                                                    "contentType": "TEXT",
                                                                                                    "secondary_cta": {
                                                                                                        "enable": False,
                                                                                                        "value": None},
                                                                                                    "primary_cta": {
                                                                                                        "enable": False,
                                                                                                        "value": None},
                                                                                                    "custom": False}},
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def test_irisv2_messageEdit_Pair_particularDateToRecurring_Upload_MobilePush_AddedStickyList_AsSameListOfMessage(
            self,
            campaignType,
            testControlType,
            listType,
            channel,
            messageInfo):
        try:
            actualOrgId = IrisHelper.updateOrgId(constant.config['mobilepush']['orgId'])
            actualOrgName = IrisHelper.updateOrgName(constant.config['mobilepush']['orgName'])
            campaignInfo = CreateCampaign.create(campaignType, testControlType)

            messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                                  campaignId=campaignInfo['ID'],updateNode=True, lockNode=True)
            CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
            message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'],
                                                           'VARIANT_CREATION')
            stickyList = CreateAudience.stickyList(campaignType, testControlType, campaignCheck=False,
                                             stickyInfo={'excludeUsers': [], 'includeUsers': ':1'})
            editInfo = {
                'targetAudience': {
                    'include': messageDetails['PAYLOAD']['targetAudience']['include'],
                    'exclude': [],
                    'orgUsers':[stickyList['ID']]
                },
                'schedule': {
                    'scheduleType': 'IMMEDIATE'
                }
            }
            editInfo = CreateMessage.edit(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                          messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],
                                          editInfo)
            CreateMessageDBAssertion(campaignInfo['ID'],
                                     editInfo['RESPONSE']['json']['entity']['id'], editInfo['PAYLOAD'],
                                     version=2).check()
            CreateMessage.assertResponse(editInfo['RESPONSE'], 200)
            message_calls().waitForJobDetailsStatusToClose(editInfo['RESPONSE']['json']['entity']['id'],
                                                           'VARIANT_CREATION', version=2)
            approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                      messageCreateResponse=editInfo)
            AuthorizeMessage.assertResponse(approveRespone, 200)
            campaignId = campaignInfo['ID']
            AuthorizeMessageDBAssertion(campaignId, editInfo['RESPONSE'], editInfo['PAYLOAD'],
                                        testControlType, version=2).check()
        finally:
            IrisHelper.updateOrgId(actualOrgId)
            IrisHelper.updateOrgName(actualOrgName)

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'SKIP', 'ORG_USERS', 'EMAIL',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def test_thread6_irisv2_messageEdit_Pair_skip_email_particularDate_stickyListEditedToDerivedList(
            self,
            campaignType,
            testControlType,
            listType,
            channel,
            messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True, lockNode=True,derivedListInfo={'excludeUsers': [], 'includeUsers': ':1'})
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION')
        derivedListInfo = CreateAudience.derivedList(campaignType, testControlType, schemaIdentifier=[channel],
                                                     newUser=True, campaignCheck=False,
                                                     derivedListInfo={
                                                         'includedGroups': ['UPLOAD', 'LOYALTY', 'DERIVED'],
                                                         'excludedGroup': ['UPLOADOLD'],
                                                         'derived': ['UPLOADOLD', 'UPLOAD', 'LOYALTY'],
                                                         'noOfUserUpload': 5})
        editInfo = {
            'targetAudience': {
                'include': [derivedListInfo['ID']],
                'exclude': []
            },
            'schedule': {
                'scheduleType': 'PARTICULAR_DATE',
                'scheduledDate': int(time.time() * 1000) + 4 * 60 * 1000
            }
        }
        editInfo = CreateMessage.edit(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                      messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],
                                      editInfo)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 editInfo['RESPONSE']['json']['entity']['id'], editInfo['PAYLOAD'], version=2).check()
        CreateMessage.assertResponse(editInfo['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(editInfo['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION', version=1)
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                  messageCreateResponse=editInfo)
        AuthorizeMessage.assertResponse(approveRespone, 200)
        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        AuthorizeMessageDBAssertion(campaignId, editInfo['RESPONSE'], editInfo['PAYLOAD'],
                                    testControlType, version=2,skippedReason=['No Loyalty Entry Found For User']).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def test_thread6_irisv2_messageEdit_Pair_org_mobile_recurring_plain_drivedListEditedToUploadList(
            self,
            campaignType,
            testControlType,
            listType,
            channel,
            messageInfo):
        campaignInfo = CreateCampaign.create(campaignType, testControlType, updateNode=True, lockNode=True)
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              campaignId=campaignInfo['ID'], updateNode=True, lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION')
        uploadListInfo = CreateAudience.uploadList(campaignType, testControlType, schemaIdentifier=[channel],
                                                   schemaData=[channel, 'FIRST_NAME'], newUser=True,
                                                   campaignCheck=False)
        editInfo = {
            'targetAudience': {
                'include': [uploadListInfo['ID']],
                'exclude': []
            },
            'schedule': {'scheduleType': 'IMMEDIATE'}
        }
        editInfo = CreateMessage.edit(campaignInfo['ID'],
                                      messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],
                                      editInfo)
        CreateMessageDBAssertion(campaignInfo['ID'],
                                 editInfo['RESPONSE']['json']['entity']['id'], editInfo['PAYLOAD'], version=1).check()
        CreateMessage.assertResponse(editInfo['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(editInfo['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION', version=1)
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,campaignId=campaignInfo['ID'],
                                                  messageCreateResponse=editInfo)
        AuthorizeMessage.assertResponse(approveRespone, 200)
        campaignId = campaignInfo['ID']
        AuthorizeMessageDBAssertion(campaignId, editInfo['RESPONSE'], editInfo['PAYLOAD'],
                                    testControlType, version=1).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('UPCOMING', 'SKIP', 'UPLOAD', 'EMAIL',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'SKIP', 'UPLOAD', 'EMAIL',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'MULTICOUPONS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def test_thread3_irisv2_messageEdit_Pair_skip_email_particularDate_coupon_derivedListToFilter(
            self,
            campaignType,
            testControlType,
            listType,
            channel,
            messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True, lockNode=True,
                                              derivedListInfo={'includedGroups': ['UPLOAD', 'LOYALTY', 'DERIVED'],
                                                               'excludedGroup': ['UPLOADOLD'],
                                                               'derived': ['UPLOADOLD', 'UPLOAD', 'LOYALTY'],
                                                               'noOfUserUpload': 5})
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION')
        editInfo = {
            'targetAudience': {
                'include': [constant.config['FilterListID']],
                'exclude': []
            },
            'messageContent': CreateMessage.constructMessageContent(campaignType, testControlType, {'type': 'DEFAULT'},
                                                                    'POINTS', channel)
        }
        editInfo = CreateMessage.edit(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                      messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],
                                      editInfo)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 editInfo['RESPONSE']['json']['entity']['id'], editInfo['PAYLOAD'], version=1).check()
        CreateMessage.assertResponse(editInfo['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(editInfo['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION', version=1)
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                  messageCreateResponse=editInfo)
        AuthorizeMessage.assertResponse(approveRespone, 200)
        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        AuthorizeMessageDBAssertion(campaignId, editInfo['RESPONSE'], editInfo['PAYLOAD'],
                                    testControlType, version=1).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo,toOfferType', [
        ('UPCOMING', 'CUSTOM', 'UPLOAD', 'EMAIL',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}, 'COUPON'),
        ('UPCOMING', 'CUSTOM', 'UPLOAD', 'EMAIL',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}, 'MULTICOUPONS')
    ])
    def test_thread4_irisv2_messageEdit_Pair_custom_email_immediate_PointEditToCoupon_derivedListEditToFilter_AddedStickyList_ImmediateToRecurring(
            self,
            campaignType,
            testControlType,
            listType,
            channel,
            messageInfo,
            toOfferType):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True, lockNode=True,
                                              derivedListInfo={'includedGroups': ['UPLOAD', 'LOYALTY', 'DERIVED'],
                                                               'excludedGroup': ['UPLOADOLD'],
                                                               'derived': ['UPLOADOLD', 'UPLOAD', 'LOYALTY'],
                                                               'noOfUserUpload': 5})
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION')
        defaultScheduleTimer = Utils.getTime(hours=5, minutes=33, dateTimeFormat=True)
        editInfo = {
            'schedule': {
                'scheduleType': 'RECURRING',
                'hour': int(defaultScheduleTimer[11:13]),
                'minute': int(defaultScheduleTimer[14:16]),
                'startDate': Utils.getTime(seconds=90,
                                           milliSeconds=True),
                'endDate': Utils.getTime(hours=20,
                                         milliSeconds=True),
                'repeatType': 'DAILY',
                'repeatOn': [1]
            },
            'targetAudience': {
                'include': [constant.config['FilterListID']],
                'exclude': [],
                'orgUsers': messageDetails['PAYLOAD']['targetAudience']['include']
            },
            'messageContent': CreateMessage.constructMessageContent(campaignType, testControlType, {'type': 'DEFAULT'},
                                                                    toOfferType, channel)
        }
        editInfo = CreateMessage.edit(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                      messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],
                                      editInfo)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 editInfo['RESPONSE']['json']['entity']['id'], editInfo['PAYLOAD'], version=2).check()
        CreateMessage.assertResponse(editInfo['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(editInfo['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION', version=1)
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                  messageCreateResponse=editInfo)
        AuthorizeMessage.assertResponse(approveRespone, 200)
        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        AuthorizeMessageDBAssertion(campaignId, editInfo['RESPONSE'], editInfo['PAYLOAD'],
                                    testControlType, version=2).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo,toOfferType', [
        ('UPCOMING', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}, 'COUPON'),
        ('UPCOMING', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}, 'MULTICOUPONS')
    ])
    def test_thread5_irisv2_messageEdit_Pair_org_mobile_immediate_plainEditToCoupon_DerivedListEditToAnotherDerivedList(
            self,
            campaignType,
            testControlType,
            listType,
            channel,
            messageInfo,
            toOfferType):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True, lockNode=True,
                                              derivedListInfo={'includedGroups': ['UPLOAD', 'LOYALTY', 'DERIVED'],
                                                               'excludedGroup': ['UPLOADOLD'],
                                                               'derived': ['UPLOADOLD', 'UPLOAD', 'LOYALTY'],
                                                               'noOfUserUpload': 5})
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION')
        newDerivedListInfo = CreateAudience.derivedList(campaignType, testControlType, schemaIdentifier=[channel],
                                                        newUser=False, campaignCheck=False,
                                                        derivedListInfo={
                                                            'includedGroups': ['UPLOAD', 'LOYALTY', 'DERIVED'],
                                                            'excludedGroup': ['UPLOADOLD'],
                                                            'derived': ['UPLOADOLD', 'UPLOAD', 'LOYALTY'],
                                                            'noOfUserUpload': 5}, updateNode=True, lockNode=True)

        editInfo = {
            'targetAudience': {
                'include': [newDerivedListInfo['ID']],
                'exclude': []
            },
            'messageContent': CreateMessage.constructMessageContent(campaignType, testControlType, {'type': 'DEFAULT'},
                                                                    toOfferType, channel)
        }
        editInfo = CreateMessage.edit(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                      messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],
                                      editInfo)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 editInfo['RESPONSE']['json']['entity']['id'], editInfo['PAYLOAD'], version=1).check()
        CreateMessage.assertResponse(editInfo['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(editInfo['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION', version=1)
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                  messageCreateResponse=editInfo)
        AuthorizeMessage.assertResponse(approveRespone, 200)
        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        AuthorizeMessageDBAssertion(campaignId, editInfo['RESPONSE'], editInfo['PAYLOAD'],
                                    testControlType, version=1).check()
