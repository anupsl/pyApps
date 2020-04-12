import pytest

from src.utilities.logger import Logger
from src.modules.irisv2.campaigns.campaignSetting import CampaignSetting
from src.dbCalls.campaignInfo import campaign_calls
from src.modules.irisv2.campaigns.campaignSettingDBAssertion import CampaignSettingDBAssertion

@pytest.mark.run(order=7)
class Test_updateCampaignSettings():

    def setup_method(self, method):
        Logger.logMethodName(method.__name__)

    @pytest.mark.parametrize('updateInfo',[
        ({'enableLinkTracking':False,})
    ])
    def test_irisV2_updateCampaignSettings_messageSettings(self,updateInfo):

        update= CampaignSetting.updateSettings(self,updateInfo)
        CampaignSetting.assertResponse(update['RESPONSE'], 200)
        CampaignSettingDBAssertion(update['PAYLOAD']).check()

    @pytest.mark.parametrize('updateInfo', [
        ({'enableLinkTracking':True,'summary':{'count':1,'channels':['SMS']},'credit':{'count':1,'channels':['SMS']},'failure':{'count':1,'channels':['SMS']},'lowDelivery':{'count':1,'channels':['SMS']}})
    ])
    def test_irisV2_updateCampaignSettings_allSettings_Sanity(self, updateInfo):
        update = CampaignSetting.updateSettings(self, updateInfo)
        CampaignSetting.assertResponse(update['RESPONSE'], 200)
        CampaignSettingDBAssertion(update['PAYLOAD']).check()



    @pytest.mark.parametrize('updateInfo',[
        ({'failure':{'count':1,'channels':['SMS']},'lowDelivery':{'count':1,'channels':['SMS']}})
    ])

    def test_irisV2_updateCampaignSettings_alertsSettings(self, updateInfo):
        update = CampaignSetting.updateSettings(self, updateInfo)
        CampaignSetting.assertResponse(update['RESPONSE'], 200)
        CampaignSettingDBAssertion(update['PAYLOAD']).check()

    @pytest.mark.parametrize('updateInfo', [
        ({'summary':{'count':1,'channels':['SMS']},'credit':{'count':1,'channels':['SMS']}})
    ])
    def test_irisV2_updateCampaignSettings_reportsSettings(self, updateInfo):
        update = CampaignSetting.updateSettings(self, updateInfo)
        CampaignSetting.assertResponse(update['RESPONSE'], 200)
        CampaignSettingDBAssertion(update['PAYLOAD']).check()

    @pytest.mark.parametrize('updateInfo', [
        ({'enableLinkTracking': True, 'summary': {'count': 1, 'channels': ['EMAIL']},
          'credit': {'count': 1, 'channels': ['EMAIL']},
          'failure': {'count': 1, 'channels': ['EMAIL']},
          'lowDelivery': {'count': 1, 'channels': ['EMAIL']}})
    ])
    def test_irisV2_updateCampaignSettings_multipleChannel(self, updateInfo):
        update = CampaignSetting.updateSettings(self, updateInfo)
        CampaignSetting.assertResponse(update['RESPONSE'], 200)
        CampaignSettingDBAssertion(update['PAYLOAD']).check()

    @pytest.mark.parametrize('updateInfo', [
        ({'enableLinkTracking': "", })
    ])
    def test_irisV2_updateCampaignSettings_emptyLink(self, updateInfo):
        update = CampaignSetting.updateSettings(self, updateInfo)
        CampaignSetting.assertResponse(update['RESPONSE'], 400, expectedErrorCode= 102, expectedErrorMessage=['Invalid request : enableLinkTracking is required.'])

    @pytest.mark.parametrize('updateInfo', [
        ({'summary': {'count': 1, 'channels': ['']},
          'credit': {'count': 1, 'channels': ['']}}
          )
    ])
    def test_irisV2_updateCampaignSettings_emptyChannel(self, updateInfo):
        update = CampaignSetting.updateSettings(self, updateInfo)
        CampaignSetting.assertResponse(update['RESPONSE'], 400, expectedErrorCode=104,
                                       expectedErrorMessage=['Invalid request : null , Unknown value , allowed values are [SMS, EMAIL, MOBILEPUSH, CALL_TASK, WECHAT]'])


