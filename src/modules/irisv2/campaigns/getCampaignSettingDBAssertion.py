from src.dbCalls.campaignInfo import campaignSettingDBCalls
from src.utilities.assertion import Assertion
from src.utilities.logger import Logger


class GetCampaignSettingDBAssertion():

    def __init__(self, responseActual):
        if 'ndncGatewayPresent' in responseActual: responseActual.pop('ndncGatewayPresent')
        if 'ndncCampaign' in responseActual :responseActual.pop('ndncCampaign')
        self.response = responseActual
        self.getDbData = campaignSettingDBCalls().getCampaignSettings()
        self.getDbData.pop('_id')
        self.getDbData.pop('_class')
        self.getDbData.pop('autoUpdateTime')


    def check(self):

        Assertion.constructAssertion(self.getDbData == self.response,
                                     'From DB Value Constructed :{} and passed in Response :{}'.format(self.getDbData,
                                                                                                      self.response))

