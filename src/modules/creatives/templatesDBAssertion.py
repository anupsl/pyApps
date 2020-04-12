from src.modules.campaignUIPages.campaignsUIDBCalls import DBCallsCampaigns
from src.utilities.logger import Logger
from src.utilities.assertion import Assertion
import json

class TemplateDBAssertion():
    
    def __init__(self, templateName, channel, message):
        self.templateName = templateName
        self.channel = channel
        self.message = message
    
    def check(self):
        self.getTemplateInfo()
        self.assertTemplate()
        return self.templateInMongo['id']
    
    def getTemplateInfo(self):
        if self.channel == 'Mobile Push': self.channel = 'MOBILEPUSH'
        self.templateInMongo = DBCallsCampaigns.getTemplateDetails(self.channel, self.templateName)
       
    def assertTemplate(self):
        Assertion.constructAssertion(len(self.templateInMongo) == 1, 'Asserting Length on Template in mongo , as template should always be unique')
        Assertion.constructAssertion(self.templateInMongo[0]['versions']['base']['sms-editor'] == self.message, 'Actual Message :{} and Message in Mongo :{}'.format(self.message, self.templateInMongo[0]['versions']['base']['sms-editor']))
        Assertion.constructAssertion(self.templateInMongo[0]['versions']['history']['sms-editor'] == self.message, 'Actual Message :{} and Message in Mongo :{}'.format(self.message, self.templateInMongo[0]['versions']['history']['sms-editor']))
