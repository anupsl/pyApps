import pytest

from src.Constant.constant import constant
from src.modules.irisv2.helper.irisHelper import IrisHelper
from src.modules.irisv2.list.createAudience import CreateAudience
from src.modules.irisv2.message.authorizeMessage import AuthorizeMessage
from src.modules.irisv2.message.authorizeMessageDbAssertion import AuthorizeMessageDBAssertion
from src.utilities.logger import Logger
from src.modules.irisv2.message.createMessage import CreateMessage


class Test_Message_Pair_Create_Execute_Personalize_Combinations():
    def setup_method(self, method):
        Logger.logMethodName(method.__name__)

    def setup_class(self):
        Logger.logSuiteName(str(self).split('.')[-1])
        self.actualOrgId = IrisHelper.updateOrgId(constant.config['reon']['orgId'])
        self.actualOrgName = IrisHelper.updateOrgName(constant.config['reon']['orgName'])
        CreateAudience.getPocUsers()
        # TODO: s3 Path in orgDetails of 50136 has to be added  , todo is added there as well
        # constant.config['FilterListID'] = CreateAudience.FilterList('LAPSED', 'ORG', campaignCheck=False)['ID']

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN',
          'messageStrategy': {'type': 'PERSONALISATION', 'defaultCategory': True,'channels':['SMS','SMS']},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
    ])
    def test_irisv2_message_personalize_execute_upload_sms_immediate_points_plain_live(self, campaignType,
                                                                                       testControlType,
                                                                                       listType,
                                                                                       channel, messageInfo):
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo)
        AuthorizeMessage.assertResponse(approveRespone, 200)

        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        response = constant.config['node'][campaignType][testControlType]['LIST'][listType][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['RESPONSE']
        payload = constant.config['node'][campaignType][testControlType]['LIST'][listType][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['PAYLOAD']

        AuthorizeMessageDBAssertion(campaignId, response, payload, testControlType, personalizedMessage=True).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN',
          'messageStrategy': {'type': 'PERSONALISATION', 'numberOfCategory': 2, 'useDifferentLevel': True,
                              'messageContentId': ['message_content_id_0', 'message_content_id_1'], 'offers':['PLAIN','PLAIN'],'channels':['SMS','SMS']},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
    ])
    def test_irisv2_message_personalize_execute_upload_sms_sms_immediate_plain_plain_live_multiCategory(self, campaignType,
                                                                                                     testControlType,
                                                                                                     listType,
                                                                                                     channel,
                                                                                                     messageInfo):
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo)
        AuthorizeMessage.assertResponse(approveRespone, 200)

        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        response = constant.config['node'][campaignType][testControlType]['LIST'][listType][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['RESPONSE']
        payload = constant.config['node'][campaignType][testControlType]['LIST'][listType][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['PAYLOAD']

        AuthorizeMessageDBAssertion(campaignId, response, payload, testControlType, personalizedMessage=True).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'SKIP', 'LOYALTY', 'EMAIL',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN',
          'messageStrategy': {'type': 'PERSONALISATION', 'numberOfCategory': 3, 'useDifferentLevel': True,
                              'messageContentId': ['message_content_id_0', 'message_content_id_1','message_content_id_2'],
                              'offers': ['COUPON', 'POINTS', 'PLAIN'],'channels':['SMS','EMAIL','SMS']},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
    ])
    def test_irisv2_message_personalize_execute_loyalty_smsssssssssssssssss_email_sms_immediate_coupon_points_plain_live_multiCategory(self,
                                                                                                            campaignType,
                                                                                                            testControlType,
                                                                                                            listType,
                                                                                                            channel,
                                                                                                            messageInfo):
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo)
        AuthorizeMessage.assertResponse(approveRespone, 200)

        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        response = constant.config['node'][campaignType][testControlType]['LIST'][listType][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['RESPONSE']
        payload = constant.config['node'][campaignType][testControlType]['LIST'][listType][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['PAYLOAD']

        AuthorizeMessageDBAssertion(campaignId, response, payload, testControlType, personalizedMessage=True).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'SKIP', 'ORG_USERS', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN',
          'messageStrategy': {'type': 'PERSONALISATION', 'numberOfCategory': 2, 'useDifferentLevel': True,
                              'messageContentId': ['message_content_id_0', 'message_content_id_1'],
                              'offers': ['PLAIN', 'PLAIN']},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
    ])
    def test_irisv2_message_personalize_execute_stickylist_Msms_Msms_particulardate_plain_plain_live_multiCategory(
            self,
            campaignType,
            testControlType,
            listType,
            channel,
            messageInfo):
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                  derivedListInfo={'excludeUsers': [], 'includeUsers': ':1'})
        AuthorizeMessage.assertResponse(approveRespone, 200)

        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        response = constant.config['node'][campaignType][testControlType]['LIST'][listType][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['RESPONSE']
        payload = constant.config['node'][campaignType][testControlType]['LIST'][listType][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['PAYLOAD']

        AuthorizeMessageDBAssertion(campaignId, response, payload, testControlType, personalizedMessage=True).check()

    @pytest.mark.parametrize('campaignType,testControlType,channel,messageInfo', [
        ('UPCOMING', 'CUSTOM', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN',
          'messageStrategy': {'type': 'PERSONALISATION', 'numberOfCategory': 2, 'useDifferentLevel': True,
                              'messageContentId': ['message_content_id_0', 'message_content_id_1'],
                              'offers': ['PLAIN', 'PLAIN'],'channels':['SMS','EMAIL']},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
    ])
    def test_irisv2_message_personalize_execute_derived_smssssssssssssss_email_immediate_plain_plain_live_multiCategory(
            self,
            campaignType,
            testControlType,
            channel,
            messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, 'DERIVED', channel, messageInfo,
                                              derivedListInfo={'includedGroups': ['UPLOAD', 'LOYALTY', 'DERIVED'],
                                                               'excludedGroup': ['UPLOADOLD'],
                                                               'derived': ['UPLOADOLD', 'UPLOAD', 'LOYALTY'],
                                                               'noOfUserUpload': 5})
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, 'DERIVED', channel,
                                                  messageInfo=messageInfo, messageCreateResponse=messageDetails)
        AuthorizeMessage.assertResponse(approveRespone, 200)

        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        response = constant.config['node'][campaignType][testControlType]['LIST'][listType][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['RESPONSE']
        payload = constant.config['node'][campaignType][testControlType]['LIST'][listType][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['PAYLOAD']

        AuthorizeMessageDBAssertion(campaignId, response, payload, testControlType, personalizedMessage=True).check()
