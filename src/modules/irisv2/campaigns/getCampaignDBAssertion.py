from datetime import datetime

from src.dbCalls.campaignInfo import campaign_info
from src.utilities.assertion import Assertion


class GetCampaignDBAssertion():
    def __init__(self, campaignId, response):
        self.campaignId = campaignId
        self.response = response
        self.campaignInfo = campaign_info(campaignId).campaignInfo

    def check(self):
        self.campaignCheck()

    def campaignCheck(self):
        Assertion.constructAssertion(self.campaignId == self.response['json']['entity']['campaignId'],
                                     'CampaignId in DB :{} and passed :{}'.format(self.campaignId,
                                                                                  self.response['json']['entity'][
                                                                                      'campaignId']))
        Assertion.constructAssertion(self.campaignInfo['name'] == self.response['json']['entity']['name'],
                                     'Name in DB :{} and passed :{}'.format(self.campaignInfo['name'],
                                                                            self.response['json']['entity']['name']))
        if 'description' in self.response: Assertion.constructAssertion(
            self.campaignInfo['description'] == self.response['json']['entity']['description'],
            'description in DB :{} and passed :{}'.format(self.campaignInfo['description'],
                                                          self.response['json']['entity']['description']))

        if self.response['json']['entity']['testControl']['type'] == 'CUSTOM':
            if 'testPercentage' in self.response['json']['entity']['testControl']: Assertion.constructAssertion(
                self.campaignInfo['testControl']['testPercentage'] == self.response['json']['entity']['testControl'][
                    'testPercentage'],
                'Test Percentage in DB :{} and passed :{}'.format(self.campaignInfo['testControl']['testPercentage'],
                                                                  self.response['json']['entity']['testControl'][
                                                                      'testPercentage']))
        Assertion.constructAssertion(
            self.campaignInfo['testControl']['testControlType'] == self.response['json']['entity']['testControl'][
                'type'],
            'Test Type in DB :{} and passed :{}'.format(self.campaignInfo['testControl']['testControlType'],
                                                        self.response['json']['entity']['testControl']['type']))


        Assertion.constructAssertion(self.campaignInfo['endDate'].split('.')[0] == datetime.fromtimestamp(
            self.response['json']['entity']['endDate'] / 1000).strftime('%Y-%m-%d %H:%M:%S'),
                                     'End Date In DB :{} and in response :{}'.format(
                                         self.campaignInfo['endDate'].split('.')[0], datetime.fromtimestamp(
                                             self.response['json']['entity']['endDate'] / 1000).strftime(
                                             '%Y-%m-%d %H:%M:%S')), verify=True)
        Assertion.constructAssertion(self.campaignInfo['startDate'].split('.')[0] == datetime.fromtimestamp(
            self.response['json']['entity']['startDate'] / 1000).strftime('%Y-%m-%d %H:%M:%S'),
                                     'End Date In DB :{} and in response :{}'.format(
                                         self.campaignInfo['startDate'].split('.')[0], datetime.fromtimestamp(
                                             self.response['json']['entity']['startDate'] / 1000).strftime(
                                             '%Y-%m-%d %H:%M:%S')), verify=True)
        if 'gaEnabled'==True in self.campaignInfo:
            Assertion.constructAssertion(
                self.campaignInfo['gaSource'] == self.response['json']['entity']['gaSource'],
                'gaSource in DB :{} and passed :{}'.format(self.campaignInfo['gaSource'], self.response['json']['entity']['gaSource']
                                                                ))
            Assertion.constructAssertion(
                self.campaignInfo['gaName'] == self.response['json']['entity']['gaName'],
                'gaName in DB :{} and passed :{}'.format(self.campaignInfo['gaName'],
                                                            self.response['json']['entity']['gaName']))




        if 'objective' in self.response:
            Assertion.constructAssertion(
                self.campaignInfo['objective']['objectiveName'] == self.response['objective']['objectiveName'],
                'objectiveName in DB :{} and passed :{}'.format(self.campaignInfo['objective']['objectiveName'],
                                                                self.response['objective']['objectiveName']))
