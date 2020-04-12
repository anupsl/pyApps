from src.dbCalls.campaignInfo import campaignObjectiveDBCalls
from src.utilities.assertion import Assertion


class CampaignObjectiveDBAssertion():

    def __init__(self, response):
        self.response = response['json']['data']
        self.response.sort()
        self.getDbData = campaignObjectiveDBCalls().getCampaignObjective()
        self.getDbData.sort()

    def check(self):
        Assertion.constructAssertion(self.getDbData == self.response,
                                     'From DB Value Constructed :{} and passed in Payload :{}'.format(self.getDbData,
                                                                                                      self.response))

