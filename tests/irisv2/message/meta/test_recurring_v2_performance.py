import pytest

from src.modules.irisv2.campaigns.createCampaign import CreateCampaign
from src.modules.irisv2.message.authorizeMessage import AuthorizeMessage
from src.modules.irisv2.message.createMessage import CreateMessage
from src.modules.irisv2.list.createAudience import CreateAudience
from src.modules.campaign_shard.campaignShardHelper import CampaignShardHelper

@pytest.mark.run(order=2)
class Test_Veneno_V2_RECURRING_performance():

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'LOYALTY', 'MOBILE',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': True, 'encryptUrl': False, 'skipRateLimit': False})
    ]*2)
    def test_irisv2_recurring_campaign_performance(self,
                                                                               campaignType,
                                                                               testControlType,
                                                                               listType,
                                                                               channel,
                                                                               messageInfo):
        #campaignId = CreateCampaign.create(campaignType, testControlType, updateNode=True, lockNode=True)['ID']
        #couponSeriesId = CreateMessage.getCouponSeriesId(campaignId)
        #approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,lockNode=True)
        #AuthorizeMessage.assertResponse(approveRespone, 200)
        campaignId = CreateCampaign.create(campaignType, testControlType)['ID']
        #listInfo = CreateAudience.FilterList(campaignType, testControlType, lockNode=True)
        detailsOfFilterListCreated = CampaignShardHelper.createFilterListWithCreateGroupRecipient()
        listInfo = detailsOfFilterListCreated['groupDetails']
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                  campaignId=campaignId, listInfo=listInfo, lockNode=True)
        AuthorizeMessage.assertResponse(approveRespone, 200)