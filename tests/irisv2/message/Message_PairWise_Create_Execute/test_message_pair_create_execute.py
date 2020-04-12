import pytest

from src.Constant.constant import constant
from src.modules.irisv2.helper.irisHelper import IrisHelper
from src.modules.irisv2.list.createAudience import CreateAudience
from src.modules.irisv2.message.authorizeMessage import AuthorizeMessage
from src.modules.irisv2.message.authorizeMessageDbAssertion import AuthorizeMessageDBAssertion
from src.modules.irisv2.message.createMessage import CreateMessage
from src.utilities.logger import Logger
from src.modules.irisv2.campaigns.createCampaign import CreateCampaign

class Test_Message_Pair_Create_Execute_Combinations():
    def setup_method(self, method):
        Logger.logMethodName(method.__name__)

    def setup_class(self):
        Logger.logSuiteName(str(self).split('.')[-1])
        CreateAudience.getPocUsers()
        constant.config['FilterListID'] = CreateAudience.FilterList('LAPSED', 'ORG', campaignCheck=False)['ID']

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
    ])
    def test_irisv2_message_execute_upload_sms_immediate_plain_live_smoke(self, campaignType, testControlType,
                                                                           listType,
                                                                           channel, messageInfo):
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo)
        AuthorizeMessage.assertResponse(approveRespone, 200)

        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        response = constant.config['node'][campaignType][testControlType]['LIST'][listType][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['RESPONSE']
        payload = constant.config['node'][campaignType][testControlType]['LIST'][listType][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['PAYLOAD']

        AuthorizeMessageDBAssertion(campaignId, response, payload, testControlType).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'LOYALTY', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def test_irisv2_message_execute_upload_sms_immediate_points_plain_live(self, campaignType, testControlType,
                                                                           listType,
                                                                           channel, messageInfo):
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo)
        AuthorizeMessage.assertResponse(approveRespone, 200)

        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        response = constant.config['node'][campaignType][testControlType]['LIST'][listType][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['RESPONSE']
        payload = constant.config['node'][campaignType][testControlType]['LIST'][listType][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['PAYLOAD']

        AuthorizeMessageDBAssertion(campaignId, response, payload, testControlType).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'CUSTOM', 'UPLOAD', 'EMAIL',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': True, 'skipRateLimit': True}),
    ])
    def test_irisv2_message_execute_upload_email_particulardate_points_live(self, campaignType,
                                                                            testControlType,
                                                                            listType, channel, messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True)
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                  messageCreateResponse=messageDetails)
        AuthorizeMessage.assertResponse(approveRespone, 200)

        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        response = constant.config['node'][campaignType][testControlType]['LIST'][listType][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['RESPONSE']
        payload = constant.config['node'][campaignType][testControlType]['LIST'][listType][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['PAYLOAD']
        AuthorizeMessageDBAssertion(campaignId, response, payload, testControlType,skippedReason=['No Loyalty Entry Found For User']).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'SKIP', 'UPLOAD', 'MOBILE_PUSH',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT',
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
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': True, 'encryptUrl': False, 'skipRateLimit': False})
    ])
    def test_irisv2_message_execute_upload_push_immediate_coupon_live_pushThread(self, campaignType, testControlType,
                                                                                listType,
                                                                                channel, messageInfo):
        try:
            actualOrgId = IrisHelper.updateOrgId(constant.config['mobilepush']['orgId'])
            actualOrgName = IrisHelper.updateOrgName(constant.config['mobilepush']['orgName'])
            campaignInfo = CreateCampaign.create(campaignType, testControlType, updateNode=True, lockNode=True)
            couponSeriesId = CreateMessage.getCouponSeriesId(campaignInfo['ID'])
            approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,campaignId=campaignInfo['ID'],couponSeriesId=couponSeriesId)
            AuthorizeMessage.assertResponse(approveRespone, 200)

            campaignId = campaignInfo['ID']
            response = constant.config['node'][campaignType][testControlType]['LIST'][listType][channel]['MESSAGE'][
                messageInfo['scheduleType']['type']][messageInfo['offerType']]['RESPONSE']
            payload = constant.config['node'][campaignType][testControlType]['LIST'][listType][channel]['MESSAGE'][
                messageInfo['scheduleType']['type']][messageInfo['offerType']]['PAYLOAD']

            AuthorizeMessageDBAssertion(campaignId, response, payload, testControlType).check()
        finally:
            IrisHelper.updateOrgId(actualOrgId)
            IrisHelper.updateOrgName(actualOrgName)

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('UPCOMING', 'SKIP', 'UPLOAD', 'MOBILE_PUSH',
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
          'channels': ['MOBILE_PUSH'], 'useTinyUrl': True, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def test_irisv2_message_execute_upload_push_recurring_immediate_points_live_ProdSanity_pushThread(self, campaignType, testControlType,
                                                                                listType,
                                                                                channel, messageInfo):
        try:
            actualOrgId = IrisHelper.updateOrgId(constant.config['mobilepush']['orgId'])
            actualOrgName = IrisHelper.updateOrgName(constant.config['mobilepush']['orgName'])
            campaignInfo = CreateCampaign.create(campaignType, testControlType, updateNode=True, lockNode=True)

            approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                      campaignId=campaignInfo['ID'])
            AuthorizeMessage.assertResponse(approveRespone, 200)

            campaignId = campaignInfo['ID']
            response = constant.config['node'][campaignType][testControlType]['LIST'][listType][channel]['MESSAGE'][
                messageInfo['scheduleType']['type']][messageInfo['offerType']]['RESPONSE']
            payload = constant.config['node'][campaignType][testControlType]['LIST'][listType][channel]['MESSAGE'][
                messageInfo['scheduleType']['type']][messageInfo['offerType']]['PAYLOAD']

            AuthorizeMessageDBAssertion(campaignId, response, payload, testControlType).check()
        finally:
            IrisHelper.updateOrgId(actualOrgId)
            IrisHelper.updateOrgName(actualOrgName)

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'CUSTOM', 'LOYALTY', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': True, 'encryptUrl': True, 'skipRateLimit': False}),
        ('UPCOMING', 'ORG', 'LOYALTY', 'EMAIL',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': True, 'skipRateLimit': False}),
        ('LIVE', 'CUSTOM', 'LOYALTY', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': False}),
    ])
    def test_irisv2_message_execute_loyalty_mobile_email_recurring_immediate_particulardate_allOffer_live_current(self,
                                                                                                          campaignType,
                                                                                                          testControlType,
                                                                                                          listType,
                                                                                                          channel,
                                                                                                          messageInfo):
        campaignId = CreateCampaign.create(campaignType,testControlType,updateNode=True,lockNode=True)['ID']
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,campaignId=campaignId)
        AuthorizeMessage.assertResponse(approveRespone, 200)

        campaignId = campaignId
        response = constant.config['node'][campaignType][testControlType]['LIST'][listType][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['RESPONSE']
        payload = constant.config['node'][campaignType][testControlType]['LIST'][listType][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['PAYLOAD']

        AuthorizeMessageDBAssertion(campaignId, response, payload, testControlType).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'SKIP', 'LOYALTY', 'MOBILE',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': True, 'encryptUrl': False, 'skipRateLimit': False})
    ])
    def test_irisv2_message_execute_loyalty_mobile_coupon_recurring_ProdSanity(self,
                                                                            campaignType,
                                                                            testControlType,
                                                                            listType,
                                                                            channel,
                                                                            messageInfo):
        campaignId = CreateCampaign.create(campaignType, testControlType, updateNode=True, lockNode=True)['ID']
        couponSeriesId = CreateMessage.getCouponSeriesId(campaignId)
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                  campaignId=campaignId,couponSeriesId=couponSeriesId)
        AuthorizeMessage.assertResponse(approveRespone, 200)

        campaignId = campaignId
        response = constant.config['node'][campaignType][testControlType]['LIST'][listType][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['RESPONSE']
        payload = constant.config['node'][campaignType][testControlType]['LIST'][listType][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['PAYLOAD']

        AuthorizeMessageDBAssertion(campaignId, response, payload, testControlType).check()


    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo,skippedReason', [
        ('LIVE', 'CUSTOM', 'ORG_USERS', 'EMAIL',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': True, 'skipRateLimit': True},['No Loyalty Entry Found For User']),
        ('LIVE', 'ORG', 'ORG_USERS', 'EMAIL',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True},['No Loyalty Entry Found For User'])
    ])
    def test_irisv2_message_execute_stickylistThread_mobile_email_plain_points_live(self, campaignType,
                                                                               testControlType, listType,
                                                                               channel, messageInfo,skippedReason):
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                  derivedListInfo={'excludeUsers': [], 'includeUsers': ':1'})
        AuthorizeMessage.assertResponse(approveRespone, 200)

        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        response = constant.config['node'][campaignType][testControlType]['LIST'][listType][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['RESPONSE']
        payload = constant.config['node'][campaignType][testControlType]['LIST'][listType][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['PAYLOAD']

        AuthorizeMessageDBAssertion(campaignId, response, payload, testControlType,skippedReason=skippedReason).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo,skippedReason', [
        ('UPCOMING', 'SKIP', 'ORG_USERS', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': True, 'encryptUrl': True, 'skipRateLimit': True}, ['User has an NDNC mobile.']),
       ('UPCOMING', 'SKIP', 'ORG_USERS', 'MOBILE',
        {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'MULTICOUPONS', 'messageStrategy': {'type': 'DEFAULT'},
         'channels': ['SMS', 'EMAIL'], 'useTinyUrl': True, 'encryptUrl': True, 'skipRateLimit': True},  ['User has an NDNC mobile.'])
    ])
    def test_irisv2_message_execute_stickylistThread_mobile_email_coupon_live_ProdSanity(self, campaignType,
                                                                               testControlType, listType,
                                                                               channel, messageInfo, skippedReason):
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                  derivedListInfo={'excludeUsers': [], 'includeUsers': ':1'})
        AuthorizeMessage.assertResponse(approveRespone, 200)

        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        response = constant.config['node'][campaignType][testControlType]['LIST'][listType][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['RESPONSE']
        payload = constant.config['node'][campaignType][testControlType]['LIST'][listType][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['PAYLOAD']

        AuthorizeMessageDBAssertion(campaignId, response, payload, testControlType, skippedReason=skippedReason).check()

    @pytest.mark.parametrize('campaignType,testControlType,channel,messageInfo', [
        ('LIVE', 'ORG', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': True, 'encryptUrl': True, 'skipRateLimit': False}),
        ('UPCOMING', 'SKIP', 'EMAIL',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': True, 'encryptUrl': False, 'skipRateLimit': False}),
        ('UPCOMING', 'SKIP', 'EMAIL',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'MULTICOUPONS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': True, 'encryptUrl': False, 'skipRateLimit': False}),
        ('UPCOMING', 'ORG', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': True, 'encryptUrl': False, 'skipRateLimit': False}),
        ('UPCOMING', 'CUSTOM', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': True, 'encryptUrl': True, 'skipRateLimit': False}),
        ('LIVE', 'SKIP', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'SKIP', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('LIVE', 'SKIP', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'MULTICOUPONS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def test_irisv2_message_execute_derivedThread_mobile_email_coupon_plain_live(
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
        AuthorizeMessageDBAssertion(campaignId, messageDetails['RESPONSE'], messageDetails['PAYLOAD'],
                                    testControlType).check()
                        
    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'IMMEDIATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
    ])
    def est_irisv2_message_execute_upload_sms_immediate_points_plain_live_callTask(self, campaignType, testControlType,
                                                                                 listType,
                                                                                 channel, messageInfo):
        #TODO Task Still pending . 
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo)
        AuthorizeMessage.assertResponse(approveRespone, 200)

        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        response = constant.config['node'][campaignType][testControlType]['LIST'][listType][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['RESPONSE']
        payload = constant.config['node'][campaignType][testControlType]['LIST'][listType][channel]['MESSAGE'][
            messageInfo['scheduleType']['type']][messageInfo['offerType']]['PAYLOAD']

        AuthorizeMessageDBAssertion(campaignId, response, payload, testControlType).check()

