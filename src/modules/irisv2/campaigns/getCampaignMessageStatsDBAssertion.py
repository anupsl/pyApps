from src.dbCalls.campaignInfo import campaignMessageStats
from src.modules.arya.report_data import auth
from src.utilities.assertion import Assertion
from src.utilities.logger import Logger
from src.Constant.constant import constant
import copy


class GetCampaignMessageStatsDBAssertion():



    @staticmethod
    def check(self, response):
        for eachMessagestats in response['json']['data']:
            actualResult  = eachMessagestats['messageStats']
            campaignId = eachMessagestats['campaignId']
            expectedResult = GetCampaignMessageStatsDBAssertion.constructExpectedResultForMessageStats(campaignId)
            Assertion.constructAssertion(sorted(expectedResult)== sorted(actualResult),
                                             'From DB Value Constructed :{} where campaignId is {} and passed in Response :{} where campaignId is {}'.format(
                                                 expectedResult,campaignId,
                                                 actualResult, campaignId))

    @staticmethod
    def constructExpectedResultForMessageStats(campaignId):
        expectedstats = copy.deepcopy(constant.expectedStats)
        message = campaignMessageStats().getCampaignMessageStats(campaignId)
        for eachstate in message:
                status = eachstate['state']
                if status == 'APPROVED' :
                    expectedstats['approved'] += 1
                if status == 'STOPPED' :
                    expectedstats['stopped'] += 1
                if status == 'REJECTED':
                    expectedstats['rejected'] += 1
                if status == 'CREATED':
                    expectedstats['created'] += 1

        return expectedstats




class GetCampaignPerformanceStatsDBAssertion():
    @staticmethod
    def check(self, response):
        for eachPerformanceStats in response['json']['data']:
            performanceStats = eachPerformanceStats['performanceStats']
            expectedData = auth.reportData()['json']['response']['data'][0]['factvalues']
            Assertion.constructAssertion(expectedData == performanceStats,
                                         'From reon Value Constructed :{} and passed in Response :{}'.format(
                                             expectedData,
                                             performanceStats))
