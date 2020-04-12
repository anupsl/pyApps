import json
import time

from src.Constant.constant import constant
from src.dbCalls.socialInfo import social_info
from src.dbCalls.socialInfo import social_user_calls
from src.modules.iris.campaigns import campaigns
from src.modules.iris.dbCallsList import dbCallsList
from src.modules.iris.list import campaignList
from src.modules.luci.luciObject import LuciObject
from src.modules.luci.luciThrift import LuciThrift
from src.modules.social.socialObject import SocialObject
from src.modules.social.socialThrift import SocialThrift
from src.modules.veneno.venenoHelper import VenenoHelper
from src.modules.veneno.venenoObject import VenenoObject
from src.utilities.assertion import Assertion
from src.utilities.logger import Logger
from src.utilities.utils import Utils
from src.modules.iris.campaigns import campaigns

class SocialHelper():
    @staticmethod
    def checkSocialConn(ignoreConnectionError=False):
        Utils.checkServerConnection('FACEBOOK_GATEWAY_THRIFT_SERVICE', SocialThrift, 'facebookPort',
                                    ignoreConnectionError)

    @staticmethod
    def getConnObj(newConnection=False):
        port = constant.config['facebookPort']
        connPort = str(port) + '_obj'
        if connPort in constant.config:
            if newConnection:
                constant.config[connPort].close()
                constant.config[connPort] = SocialThrift(port)
            return constant.config[connPort]
        else:
            return SocialThrift(port)

    @staticmethod
    def createUserListObject(numberOfUsers, identifier='mobile'):
        userDetail = social_user_calls().getUsersInformation(numberOfUsers, identifier)
        listOfUserDetails = list()
        for eachUser in userDetail:
            if identifier == 'mobile': listOfUserDetails.append(SocialObject.UserDetails(mobile=eachUser))
            if identifier == 'email': listOfUserDetails.append(SocialObject.UserDetails(email=eachUser))
        return listOfUserDetails

    @staticmethod
    def createCampaignsForSocialThrift(testControlType=['ORG', 'CUSTOM', 'SKIP']):
        buildResult = dict()
        for each in testControlType:
            buildResult[each] = campaigns.createCampaign({'name': 'Social_Thrift_' + str(int(time.time() * 100000)),
                                                          'goalId': constant.irisGenericValues['goalId'],
                                                          'objectiveId': constant.irisGenericValues['objectiveId'],
                                                          'testControl': {'type': each, 'test': 90}})[0]['json'][
                'entity']['campaignId']

        return buildResult

    @staticmethod
    def createListForSocial(campaignInfo, campaignType, numberOfUsers=5, newUser=False):
        mergeListresponse, mergeListPayload, campaignId = campaignList.mergeList({},
                                                                                 campaignId=campaignInfo[campaignType],
                                                                                 campaignType=['LIVE', campaignType,
                                                                                               'List', 'TAGS', 0],
                                                                                 userType='mobile',
                                                                                 numberOfUsers=numberOfUsers,
                                                                                 numberOfCustomTags=0, newUser=newUser)
        return dbCallsList.getGroupVersionDetailsWithGroupId(mergeListresponse['json']['entity']['listId'])['TEST'][
                   'id'], mergeListPayload['name']

    @staticmethod
    def assertCreateCustomList(groupVersionid, messageId, CreateCustomAudienceListResponse, name, description,
                               type='FACEBOOK'):
        socialAudienceListInfo = \
            social_info(groupVersionid=groupVersionid, messageId=messageId, socialAudienceList=True).socialInfo[
                'audienceList']
        Assertion.constructAssertion(socialAudienceListInfo['type'] == type.upper(),
                                     'Audience List Type , Actual :{} and Expected :{}'.format(
                                         socialAudienceListInfo['type'], type.upper()))
        Assertion.constructAssertion(
            int(socialAudienceListInfo['account_id']) == constant.config['facebook']['accountId'],
            'AccountId , Actual :{} and Expected :{}'.format(socialAudienceListInfo['account_id'],
                                                             constant.config['facebook']['accountId']))
        Assertion.constructAssertion(
            socialAudienceListInfo['remote_list_id'] == CreateCustomAudienceListResponse.listid,
            'Remote List Id , Actual :{} and Expected :{}'.format(socialAudienceListInfo['remote_list_id'],
                                                                  CreateCustomAudienceListResponse.listid))
        Assertion.constructAssertion(socialAudienceListInfo['name'] == name,
                                     'Name of List , Actual :{} and Expected :{}'.format(socialAudienceListInfo['name'],
                                                                                         name))
        Assertion.constructAssertion(socialAudienceListInfo['description'] == description,
                                     'Description of List , Actual :{} and Expected :{}'.format(
                                         socialAudienceListInfo['description'], description))
        Assertion.constructAssertion(socialAudienceListInfo['approximate_count'] >= 0,
                                     'approximate_count of List,Expected to Be greater than or equal to 0')

    @staticmethod
    def assertNewCreatedListInGetCall(listName, GetCustomAudienceListsResponse):
        flag = False
        for each in GetCustomAudienceListsResponse.customAudienceLists:
            if each.name == listName:
                flag = True
                break
        Assertion.constructAssertion(flag,
                                     'New Created List with Name :{} found in GetCustomAudienceListsResponse'.format(
                                         listName))

    @staticmethod
    def assertRemoteListIds(prelistId, postListId):
        Assertion.constructAssertion(prelistId == postListId,
                                     'Remote ListId ,Actual :{} and expected :{}'.format(prelistId, postListId))

    @staticmethod
    def assertGetCustomAudienceList(GetCustomAudienceListsResponse):
        for each in range(len(GetCustomAudienceListsResponse.customAudienceLists)):
            eachCustomAudienceListObject = GetCustomAudienceListsResponse.customAudienceLists[each]
            remoteListId, name = social_user_calls().getCustomAudienceListsWithRecipientListId(
                eachCustomAudienceListObject.recepientlistId, eachCustomAudienceListObject.name)
            Assertion.constructAssertion(remoteListId == eachCustomAudienceListObject.remoteListId,
                                         'remote List Id for GroupVersionId :{} , Actual :{} and Expected :{}'.format(
                                             eachCustomAudienceListObject.recepientlistId, remoteListId,
                                             eachCustomAudienceListObject.remoteListId))
            Assertion.constructAssertion(name == eachCustomAudienceListObject.name,
                                         'remote List Name for GroupVersionId :{} , Actual :{} and Expected :{}'.format(
                                             eachCustomAudienceListObject.recepientlistId, name,
                                             eachCustomAudienceListObject.name))

    @staticmethod
    def assertDeleteSocialAudienceList(GetCustomAudienceListsResponse, firstListFromGetAudienceList):
        if len(GetCustomAudienceListsResponse.customAudienceLists) > 0:
            Assertion.constructAssertion(
                GetCustomAudienceListsResponse.customAudienceLists[0].remoteListId != firstListFromGetAudienceList,
                'RemoteListId :{} Found even after Delete Call'.format(
                    GetCustomAudienceListsResponse.customAudienceLists[0].remoteListId))

    @staticmethod
    def assertCreateCampaignForSocial(campaignId, SocialCampaignObject):
        Assertion.constructAssertion(SocialCampaignObject.campaignId == campaignId,
                                     'Intouch CampaignId, Actual :{} and Expected :{}'.format(
                                         SocialCampaignObject.campaignId, campaignId))
        Assertion.constructAssertion(SocialCampaignObject.socialCampaignStatus == 0, 'socialCampaignStatus is 0')
        Assertion.constructAssertion(SocialCampaignObject.orgId == constant.config['orgId'],
                                     'OrgId , Actual :{} and Expected :{}'.format(SocialCampaignObject.orgId,
                                                                                  constant.config['orgId']))
        Assertion.constructAssertion(int(SocialCampaignObject.accountId) == constant.config['facebook']['accountId'],
                                     'AccountId , Actual :{} and Expected :{}'.format(SocialCampaignObject.accountId,
                                                                                      constant.config['facebook'][
                                                                                          'accountId']))

    @staticmethod
    def createRemoteCampaignsForSocialThrift(campaignId):
        connObj = SocialHelper.getConnObj(newConnection=True)
        return connObj.createCampaign(
            constant.config['orgId'],
            SocialObject().SocialChannel['facebook'],
            SocialObject.SocialCampaign(
                'SocialCampaign_{}'.format(int(time.time() * 1000)),
                constant.config['orgId'],
                campaignId
            ),
            'requestId_automationthriftCall_{}'.format(int(time.time() * 1000))
        ).remoteCampaignId

    @staticmethod
    def createRemoteListForSocialThrift(campaigns):
        groupVersionid, groupName = SocialHelper.createListForSocial(campaigns, 'ORG')
        messageId = SocialHelper.createMessageForThriftHelp(campaigns['ORG'], groupVersionid, 5, groupName)
        connObj = SocialHelper.getConnObj(newConnection=True)
        return connObj.createCustomList(
            SocialHelper.createUserListObject(5),
            SocialObject.CustomAudienceListDetails('remoteList_testAdset_{}'.format(int(time.time())),
                                                   'Test Create Adset', messageId),
            SocialObject.SocialAccountDetails('facebook'),
            constant.config['orgId'],
            str(groupVersionid),
            'requestId_automationthriftCall_{}'.format(int(time.time() * 1000))
        ).listid, groupVersionid

    @staticmethod
    def assertCreateAdsetSocial(SocialAdsetInfoObject, expectedRemoteCampainId, expectedSocialStatus, expectedAdsetName,
                                expectedRemoteOfferId=None, expectedRemoteListId=None):
        Assertion.constructAssertion(SocialAdsetInfoObject.socialAdsetStatus == expectedSocialStatus,
                                     'Social Status of created Adset ,Actual :{} and Expected :{}'.format(
                                         SocialAdsetInfoObject.socialAdsetStatus, expectedSocialStatus))
        if expectedRemoteOfferId is not None: Assertion.constructAssertion(
            SocialAdsetInfoObject.remoteOfferId == expectedRemoteOfferId,
            'RemoteOfferId , Actual :{} and expected :{}'.format(SocialAdsetInfoObject.remoteOfferId,
                                                                 expectedRemoteOfferId))
        if expectedRemoteListId is not None: Assertion.constructAssertion(
            SocialAdsetInfoObject.customAudienceId == expectedRemoteListId,
            'remote listID , Actual :{} and Expected :{}'.format(SocialAdsetInfoObject.customAudienceId,
                                                                 expectedRemoteListId))
        Assertion.constructAssertion(SocialAdsetInfoObject.adsetName == expectedAdsetName,
                                     'AdsetName , Actual :{} and Expected :{}'.format(SocialAdsetInfoObject.adsetName,
                                                                                      expectedAdsetName))
        Assertion.constructAssertion(SocialAdsetInfoObject.remoteAdsetId is not None,
                                     'RemoteAdsetId :{}'.format(SocialAdsetInfoObject.remoteAdsetId))
        Assertion.constructAssertion(SocialAdsetInfoObject.remoteCampaignId == expectedRemoteCampainId,
                                     'CampaignId , Actual :{} and expected :{}'.format(
                                         SocialAdsetInfoObject.remoteCampaignId, expectedRemoteCampainId))

    @staticmethod
    def assertGetAdsetInsight(AdInsightObject, adsetId):
        Assertion.constructAssertion(AdInsightObject.orgId == constant.config['orgId'],
                                     'Adsetinsight Mapped to Correct org :{}'.format(constant.config['orgId']))
        Assertion.constructAssertion(Adsetinsight.adsetId == adsetId,
                                     'Adset Mapping to Insight , Actual :{} and Expected :{}'.format(
                                         Adsetinsight.adsetId, adsetId))
        Logger.log(Adsetinsight.insights)

    @staticmethod
    def assertGetAdset(SocialAdSets, SocialAdsetInfo, expectedStatus):
        flag = False
        for SocialAdSet in SocialAdSets:
            if SocialAdSet.id == SocialAdsetInfo.remoteAdsetId:
                Assertion.constructAssertion(SocialAdSet.status == expectedStatus,
                                             'Actual :{} ,Expected :{} Status Code'.format(SocialAdSet.status,
                                                                                           expectedStatus))
                flag = True
                break
        Assertion.constructAssertion(flag, 'SocialAdsetInfo remoteId found in getSocialAdset')

    @staticmethod
    def assertOfferCreation(SocialOffer):
        Assertion.constructAssertion(SocialOffer.remoteOfferId is not None,
                                     'remote Offer Id :{} , generated Sucessfully'.format(SocialOffer.remoteOfferId))
        Assertion.constructAssertion(SocialOffer.pageId == constant.config['facebook']['pageId'],
                                     'PageId , Actual :{} and Expected :{}'.format(SocialOffer.pageId,
                                                                                   constant.config['facebook'][
                                                                                       'pageId']))

    @staticmethod
    def updateRemoteCampaignIdInCampaignsBase(campaignId, remoteId):
        try:
            additionalProperties = {
                'additionalProperties':
                    {
                        'socialCampaignId': remoteId
                    }
            }
            campaigns.updateCampaign(additionalProperties, campaignId=campaignId)
        except Exception, exp:
            Logger.log('Exception with Update Campaign V1 API :{} , trying to update with update Query'.format(exp))
            social_user_calls().updateCampaignsBaseAdditionalInfo(campaignId, remoteId)

    @staticmethod
    def couponConfigChange(condition, campaignId, voucherId):
        Logger.log('Setting Voucher Resent Config to :{} for voucherId :{}'.format(condition, voucherId))
        constant.config['requestId'] = 'couponConfigChange_{}'.format(int(time.time()))
        constant.config['campaignId'] = campaignId
        port = constant.config['luciPort'].next()
        connObj = LuciThrift(port)
        constructObj = LuciObject()

        configRequest = LuciObject.getCouponConfigRequest({'couponSeriesId': voucherId})
        couponConfigList = connObj.getCouponConfiguration(configRequest)
        couponConfig = couponConfigList[0].__dict__
        couponConfig.update(condition)

        couponConfigObject = LuciObject.couponConfiguration(couponConfig)
        saveCouponConfigObject = LuciObject.saveCouponConfigRequest(couponConfigObject)
        connObj.saveCouponConfiguration(saveCouponConfigObject)

    @staticmethod
    def updateConfigKeyValue(valid, ckvId=None):
        try:
            if ckvId is None:
                ckvId = social_user_calls().getValidKeyIdForFacebookAccount()
            social_user_calls().updateConfigKeyValue(ckvId, valid)
        except Exception, exp:
            Logger.log('Exception while Updating Key Value for Account id :{}'.format(exp))
        return ckvId

    @staticmethod
    def assertCommunicationDetailInErrorState(groupVersionId, communicationId):
        for _ in range(10):
            time.sleep(30)
            try:
                social_info(groupVersionid=groupVersionId, messageId=communicationId).veneno_monitoringStatus()
                break
            except Exception, exp:
                Logger.log('Monitoring Status Still Not Updated')
        time.sleep(30)
        cdState = social_info(groupVersionid=groupVersionId, messageId=communicationId).veneno_communicationDetails()[
            'state']
        Assertion.constructAssertion(cdState == 'ERROR', 'Check CD State is Error as remote Campaign Id is not set')

    @staticmethod
    def assertAggregationDetailAndAudienceListCreated(groupVersionId, communicationId):
        socialInfo = social_info(groupVersionid=groupVersionId, messageId=communicationId, aggregationDetail=True,
                                 socialAudienceList=True).socialInfo
        Assertion.constructAssertion(socialInfo['audienceList']['message_id'] == communicationId,
                                     'Social Audience List is Published')
        Assertion.constructAssertion('LIST_DELETE' in socialInfo['aggregationDetails'],
                                     'LIST_DELETE in aggregation Details', verify=True)
        Assertion.constructAssertion('LIST_PUBLISHED' in socialInfo['aggregationDetails'],
                                     'LIST_PUBLISHED in aggregation Details', verify=True)
        Assertion.constructAssertion('POST_PROCESS' in socialInfo['aggregationDetails'],
                                     'POST_PROCESS in aggregation Details', verify=True)

    @staticmethod
    def createMessageForThriftHelp(campaignId, groupVersionid, numberOfUsers, groupName):
        connObj = VenenoHelper.getConnObj(newConnection=True)
        cdDetailsBody = {
            'campaignId': campaignId,
            'targetType': 'SOCIAL',
            'communicationType': 'FACEBOOK',
            'subject': '',
            'recipientListId': groupVersionid,
            'overallRecipientCount': numberOfUsers,
            'expectedDeliveryCount': numberOfUsers,
            'groupName': groupName
        }
        extraParams = {
            'voucher_series': -1,
            'default_argument': {
                "entity_id": -1,
                "is_loyalty_checkbox_enabled": "0",
                "voucher_series_id": "-1",
                "daily_budget": 1000000
            }
        }
        communicationDetailObject = VenenoObject.communicationDetail(cdDetailsBody, extraParams=extraParams)
        communicationId = connObj.addMessageForRecipients(communicationDetailObject)
        return communicationId

    @staticmethod
    def validateGetSoicalCampaignDetails(socialCampaignDetails, campaignId):
        Assertion.constructAssertion(socialCampaignDetails.socialCampaign.campaignId == campaignId,
                                     'Campaign Id In Response :{} and actual :{}'.format(
                                         socialCampaignDetails.socialCampaign.campaignId, campaignId))
        Assertion.constructAssertion(socialCampaignDetails.socialCampaign.orgId == constant.config['orgId'],
                                     'Org Id In Response :{} and actual :{}'.format(
                                         socialCampaignDetails.socialCampaign.orgId, constant.config['orgId']))
        remoteCampaignId = json.loads(social_user_calls().getCampaignDetails(campaignId))['social_campaign_id']
        Assertion.constructAssertion(socialCampaignDetails.socialCampaign.remoteCampaignId == str(remoteCampaignId),
                                     'Remote CampaignId In response :{} and actual :{}'.format(
                                         socialCampaignDetails.socialCampaign.remoteCampaignId, str(remoteCampaignId)))

    @staticmethod
    def validateSocialAdsetInfo(SocialAdsetInfo, remoteAdsetId, remoteListId):
        Assertion.constructAssertion(SocialAdsetInfo.remoteAdsetId == str(remoteAdsetId),
                                     'Remote Adset Id in response :{} and Expected :{}'.format(
                                         SocialAdsetInfo.remoteAdsetId, remoteAdsetId))
        Assertion.constructAssertion(SocialAdsetInfo.customAudienceId == str(remoteListId),
                                     'Remote List Id in response :{} and Expected :{}'.format(
                                         SocialAdsetInfo.customAudienceId, remoteListId))

    @staticmethod
    def validateAggregationDetailInExceptionCase(message_id):
        for _ in range(6):
            try:
                job_type = social_user_calls().getJobDetail(message_id)
                Assertion.constructAssertion(job_type == 'ERROR', 'Social Adset expected to be in Error State')
                break
            except Exception, exp:
                time.sleep(10)
