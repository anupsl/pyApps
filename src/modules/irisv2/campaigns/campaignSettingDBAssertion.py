from src.dbCalls.campaignInfo import campaignSettingDBCalls
from src.utilities.assertion import Assertion


class CampaignSettingDBAssertion():

    def __init__(self, payload):
        self.payload = payload

        self.getDbData = campaignSettingDBCalls().getCampaignSettings()
        self.getDbData.pop('_id')
        self.getDbData.pop('_class')
        self.getDbData.pop('autoUpdateTime')

    def check(self):
        Assertion.constructAssertion(self.getDbData == self.payload,
                                     'From DB Value Constructed :{} and passed in Payload :{}'.format(self.getDbData,
                                                                                                      self.payload))

