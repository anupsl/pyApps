import pytest,time

from src.Constant.constant import constant
from src.Constant.orgDetails import OrgDetails
from src.modules.irisv2.message.createMessage import CreateMessage
from src.modules.irisv2.message.createMessageDbAssertion import CreateMessageDBAssertion
from src.utilities.logger import Logger
from src.utilities.utils import Utils
from src.modules.irisv2.list.createAudience import CreateAudience
from src.modules.irisv2.helper.irisHelper import IrisHelper
from src.modules.irisv2.message.authorizeMessage import AuthorizeMessage
from src.modules.irisv2.campaigns.createCampaign import CreateCampaign
from src.utilities.assertion import Assertion
from src.dbCalls.messageInfo import message_calls

class Test_MessageEdit_Upcoming_Create():
    def setup_method(self, method):
        Logger.logMethodName(method.__name__)

    def setup_class(self):
        Logger.logSuiteName(str(self).split('.')[-1])
        self.listInfo = CreateAudience.uploadList('LIVE', 'ORG')
        self.listInfoFilter = CreateAudience.FilterList('LIVE', 'ORG')
        constant.config['FilterListID'] = CreateAudience.FilterList('LIVE', 'ORG', campaignCheck=False)['ID']
        CreateAudience.getPocUsers()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('UPCOMING', 'ORG', 'LOYALTY', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def irisv2_message_edit_PARTICULARDATE_upcoming_create_plain_mobile_schedulle_body_Sanity(self, campaignType, testControlType, listType,
                                                                        channel, messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True, lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION')
        dateTime = Utils.getTime(hours=5, minutes=32, dateTimeFormat=True)
        messageDetails['PAYLOAD'].update({
            'schedule': {
                'startDate': Utils.getTime(minutes=1,seconds=30, milliSeconds=True),
                'endDate': Utils.getTime(minutes=40, milliSeconds=True),
                'repeatOn': [1],
                'repeatType': 'DAILY',
                'scheduleType': 'RECURRING',
                'hour': int(dateTime[11:13]),
                'minute': int(dateTime[14:16])
            }
        })
        editInfo = CreateMessage.edit(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                      messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'])
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 editInfo['RESPONSE']['json']['entity']['id'], editInfo['PAYLOAD'],version=1).check()

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('UPCOMING', 'CUSTOM', 'LOYALTY', 'MOBILE',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'COUPON', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True}),
        ('UPCOMING', 'SKIP', 'LOYALTY', 'MOBILE',
         {'scheduleType': {'type': 'RECURRING'}, 'offerType': 'POINTS', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def irisv2_message_edit_RECURRING_upcoming_create_plain_mobile_schedulle_body_Sanity(self, campaignType,
                                                                                              testControlType, listType,
                                                                                              channel, messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True, lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION')
        messageDetails['PAYLOAD'].update({
            'schedule': {
                'scheduleType': 'PARTICULAR_DATE',
                'scheduledDate': int(time.time() * 1000) + 2 * 60 * 1000
            }
        })
        editInfo = CreateMessage.edit(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                      messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'])
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 editInfo['RESPONSE']['json']['entity']['id'], editInfo['PAYLOAD'], version=1).check()