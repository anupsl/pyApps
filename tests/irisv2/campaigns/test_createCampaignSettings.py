import pytest

from src.utilities.logger import Logger
from src.modules.irisv2.campaigns.campaignSetting import CampaignSetting
from src.dbCalls.campaignInfo import campaign_calls
from src.modules.irisv2.campaigns.campaignSettingDBAssertion import CampaignSettingDBAssertion

@pytest.mark.run(order=3)
class Test_campaignSettings():

    def setup_method(self, method):
        Logger.logMethodName(method.__name__)

    @pytest.mark.skipif(True, reason='Post Request For Campaign Setting not supported ')
    @pytest.mark.parametrize('settingInfo',[
        ({'enableLinkTracking':True,'summary':{'count':1,'channels':['SMS']},'credit':{'count':1,'channels':['SMS']},'failure':{'count':1,'channels':['SMS']},'lowDelivery':{'count':1,'channels':['SMS']}})
    ])
    def test_irisV2_campaignSettings_Sanity_create(self,settingInfo):

        create= CampaignSetting.settings(self,settingInfo)
        CampaignSetting.assertResponse(create['RESPONSE'], 200)
        CampaignSettingDBAssertion(create['PAYLOAD']).check()

    @pytest.mark.parametrize('settingInfo', [
            ({'enableLinkTracking': True, 'summary': {'count': 1, 'channels': ['SMS']},
              'credit': {'count': 1, 'channels': ['SMS']}, 'failure': {'count': 1, 'channels': ['SMS']},
              'lowDelivery': {'count': 1, 'channels': ['SMS']}})
        ])
    def test_irisV2_campaignSettings_alreadyExist(self, settingInfo):
            create = CampaignSetting.settings(self, settingInfo)
            CampaignSetting.assertResponse(create['RESPONSE'], 400,expectedErrorCode=6002,
                                       expectedErrorMessage=['Campaign Settings Exception : Org level campaign settings already exist.'])


    @pytest.mark.skipif(True, reason='Post Request For Campaign Setting not supported ')
    @pytest.mark.parametrize('settingInfo,popField', [
        ({'enableLinkTracking':True,'summary': {'count': 1, 'channels': ['SMS']}, 'credit': {'count': 1, 'channels': ['SMS']},
          'failure': {'count': 1, 'channels': ['SMS']}, 'lowDelivery': {'count': 1, 'channels': ['SMS']}},"messageSettings")
    ])


    def test_irisV2_campaignSettings_create_withoutMessageSetting(self, settingInfo,popField):
        create = CampaignSetting.settings(self, settingInfo,popField)
        CampaignSetting.assertResponse(create['RESPONSE'], 200)
        campaign_calls.getUserId()
        CampaignSettingDBAssertion(create['PAYLOAD']).check()

    @pytest.mark.skipif(True, reason='Post Request For Campaign Setting not supported ')
    @pytest.mark.parametrize('settingInfo,popField', [
        ({'enableLinkTracking': True, 'summary': {'count': 1, 'channels': ['SMS']},
          'credit': {'count': 1, 'channels': ['SMS']},
          'failure': {'count': 1, 'channels': ['SMS']}, 'lowDelivery': {'count': 1, 'channels': ['SMS']}},
         "reportsSettings")
    ])

    def test_irisV2_campaignSettings_create_withoutreportsSettings(self, settingInfo, popField):
        create = CampaignSetting.settings(self, settingInfo, popField)
        CampaignSetting.assertResponse(create['RESPONSE'], 200)
        campaign_calls.getUserId()
        CampaignSettingDBAssertion(create['PAYLOAD']).check()

    @pytest.mark.skipif(True, reason='Post Request For Campaign Setting not supported ')
    @pytest.mark.parametrize('settingInfo,popField', [
        ({'enableLinkTracking': True, 'summary': {'count': 1, 'channels': ['SMS']},
          'credit': {'count': 1, 'channels': ['SMS']},
          'failure': {'count': 1, 'channels': ['SMS']}, 'lowDelivery': {'count': 1, 'channels': ['SMS']}},
         "alertsSettings")
    ])
    def test_irisV2_campaignSettings_create_withoutalertSettings(self, settingInfo, popField):
        create = CampaignSetting.settings(self, settingInfo, popField)
        CampaignSetting.assertResponse(create['RESPONSE'], 200)

        CampaignSettingDBAssertion(create['PAYLOAD']).check()

    @pytest.mark.skipif(True, reason='Post Request For Campaign Setting not supported ')
    @pytest.mark.parametrize('settingInfo', [
        ({'enableLinkTracking': True, 'summary': {'count': 1, 'channels': ['EMAIL', 'SMS']},
          'credit': {'count': 1, 'channels': ['EMAIL', 'SMS']},
          'failure': {'count': 1, 'channels': ['EMAIL', 'SMS']}, 'lowDelivery': {'count': 1, 'channels': ['EMAIL', 'SMS']}})
    ])
    def est_irisV2_campaignSettings_create_withBothChannel(self, settingInfo):
        create = CampaignSetting.settings(self, settingInfo)
        CampaignSetting.assertResponse(create['RESPONSE'], 200)
        campaign_calls.getUserId()
        CampaignSettingDBAssertion(create['PAYLOAD']).check()

    @pytest.mark.skipif(True, reason='Post Request For Campaign Setting not supported ')

    @pytest.mark.parametrize('settingInfo', [
        ({'enableLinkTracking': True, 'summary': {'count': 1, 'channels': ['EMAIL']},
          'credit': {'count': 1, 'channels': ['EMAIL']},
          'failure': {'count': 1, 'channels': ['EMAIL']},
          'lowDelivery': {'count': 1, 'channels': ['EMAIL']}})
    ])
    def est_irisV2_campaignSettings_create_withEmailChannel(self, settingInfo):
        create = CampaignSetting.settings(self, settingInfo)
        CampaignSetting.assertResponse(create['RESPONSE'], 200)
        campaign_calls.getUserId()
        CampaignSettingDBAssertion(create['PAYLOAD']).check()






