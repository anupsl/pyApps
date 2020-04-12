from src.utilities.logger import Logger
from src.Constant.constant import constant
from src.utilities.assertion import Assertion
from src.dbCalls.campaignInfo import campaign_info
from datetime import datetime
import json, time

class CampaignCheckDBAssertion():
    
    def __init__(self, campaignId, payload):
        self.campaignId = campaignId
        self.payload = payload
        self.campaignInfo = campaign_info(campaignId).campaignInfo
        
    def check(self):
        self.campaignCheck()
        
    def campaignCheck(self):
        dbStartDate = str(self.campaignInfo['startDate']).split('.')[0]
        dbEndDate = str(self.campaignInfo['endDate']).split('.')[0]
        payloadStartDate = str(datetime.fromtimestamp(self.payload['startDate'] / 1000).strftime('%Y-%m-%d %H:%M:%S'))
        payloadEndDate = str(datetime.fromtimestamp(self.payload['endDate'] / 1000).strftime('%Y-%m-%d %H:%M:%S'))
        
        Assertion.constructAssertion(self.campaignInfo['name'] == self.payload['name'], 'Name in DB :{} and passed :{}'.format(self.campaignInfo['name'] , self.payload['name']))
        if 'description' in self.payload : Assertion.constructAssertion(self.campaignInfo['description'] == self.payload['description'], 'description in DB :{} and passed :{}'.format(self.campaignInfo['description'] , self.payload['description']))
        if self.campaignInfo['testControl']['testControlType'] == 'CUSTOM' :Assertion.constructAssertion(self.campaignInfo['testControl']['testPercentage'] == self.payload['testControl']['testPercentage'], 'Test Percentage in DB :{} and passed :{}'.format(self.campaignInfo['testControl']['testPercentage'] , self.payload['testControl']['testPercentage']))
        Assertion.constructAssertion(self.campaignInfo['testControl']['testControlType'] == self.payload['testControl']['type'], 'Test Type in DB :{} and passed :{}'.format(self.campaignInfo['testControl']['testControlType'] , self.payload['testControl']['type']))
        
        Assertion.constructAssertion(dbStartDate == payloadStartDate, 'DB Start Date :{} and payload Start Date :{}'.format(dbStartDate , payloadStartDate), verify=True)
        Assertion.constructAssertion(dbEndDate == payloadEndDate, 'DB End Date :{} and payload End Date :{}'.format(dbEndDate , payloadEndDate), verify=True)

        if 'objective' in self.campaignInfo:
            Assertion.constructAssertion(
                self.campaignInfo['objective']['objectiveName'] == self.payload['objective']['objectiveName'],
                'objectiveName in DB :{} and passed :{}'.format(self.campaignInfo['objective']['objectiveName'],
                                                                  self.payload['objective']['objectiveName']))

            if self.campaignInfo['objective'] in ['Store_Visit','Product_Sales']:
                         Assertion.constructAssertion(
                            self.campaignInfo['objective']['value'] == self.payload['objective']['value'],
                            'Test Type in DB :{} and passed :{}'.format(self.campaignInfo['objective']['value'],
                                                                        self.payload['objective']['value']))


