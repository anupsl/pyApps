import pytest
import time

from src.Constant.constant import constant
from src.dbCalls.messageInfo import message_calls
from src.modules.irisv2.list.createAudience import CreateAudience
from src.modules.irisv2.message.authorizeMessage import AuthorizeMessage
from src.modules.irisv2.message.authorizeMessageDbAssertion import AuthorizeMessageDBAssertion
from src.modules.irisv2.message.createMessage import CreateMessage
from src.modules.irisv2.message.createMessageDbAssertion import CreateMessageDBAssertion
from src.utilities.logger import Logger


class Test_MessageStatus_Pair_Integration():
    def setup_method(self, method):
        Logger.logMethodName(method.__name__)

    def setup_class(self):
        Logger.logSuiteName(str(self).split('.')[-1])
        self.listInfo = CreateAudience.uploadList('LIVE', 'ORG')
        self.listInfoFilter = CreateAudience.FilterList('LIVE', 'ORG')

    @pytest.mark.parametrize('campaignType,testControlType,listType,channel,messageInfo', [
        ('LIVE', 'ORG', 'UPLOAD', 'MOBILE',
         {'scheduleType': {'type': 'PARTICULARDATE'}, 'offerType': 'PLAIN', 'messageStrategy': {'type': 'DEFAULT'},
          'channels': ['SMS', 'EMAIL'], 'useTinyUrl': False, 'encryptUrl': False, 'skipRateLimit': True})
    ])
    def test_irisv2_message_edit_reject_edit_stop_execute_Sanity(self, campaignType, testControlType, listType,
                                                            channel, messageInfo):
        messageDetails = CreateMessage.create(campaignType, testControlType, listType, channel, messageInfo,
                                              updateNode=True, lockNode=True)
        CreateMessage.assertResponse(messageDetails['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(messageDetails['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION')
        messageDetails['PAYLOAD'].update({
            'schedule': {
                'scheduleType': 'PARTICULAR_DATE',
                'scheduledDate': int(time.time() * 1000) + 6 * 60 * 1000
            }
        })
        # editing message
        editInfo = CreateMessage.edit(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                      messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'])
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 editInfo['RESPONSE']['json']['entity']['id'], editInfo['PAYLOAD'], version=1).check()

        # rejecting message
        rejectResponse = CreateMessage.reject(
            constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
            messageDetails['RESPONSE']['json']['entity']['id'])
        CreateMessage.assertResponse(rejectResponse, 200)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],
                                 approved='REJECTED').check()
        # editing message
        messageDetails['PAYLOAD'].update({
            'schedule': {
                'scheduleType': 'PARTICULAR_DATE',
                'scheduledDate': int(time.time() * 1000) + 4 * 60 * 1000
            }
        })
        editInfo = CreateMessage.edit(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                      messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'])
        CreateMessage.assertResponse(editInfo['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(editInfo['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION', version=2)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 editInfo['RESPONSE']['json']['entity']['id'], editInfo['PAYLOAD'], version=2).check()
        # approving message
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                  messageCreateResponse=editInfo)
        AuthorizeMessage.assertResponse(approveRespone, 200)
        time.sleep(15)
        # stopping the message
        stopResponse = CreateMessage.stop(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                          approveRespone['json']['entity']['messageId'])
        CreateMessage.assertResponse(stopResponse, 200)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'],
                                 reject={'status': 'CLOSED'}, approved='STOPPED').check()
        # editing message
        messageDetails['PAYLOAD'].update({
            'schedule': {
                'scheduleType': 'PARTICULAR_DATE',
                'scheduledDate': int(time.time() * 1000) + 5 * 60 * 1000
            }
        })
        editInfo = CreateMessage.edit(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                      messageDetails['RESPONSE']['json']['entity']['id'], messageDetails['PAYLOAD'])
        CreateMessage.assertResponse(editInfo['RESPONSE'], 200)
        message_calls().waitForJobDetailsStatusToClose(editInfo['RESPONSE']['json']['entity']['id'],
                                                       'VARIANT_CREATION', version=3)
        CreateMessageDBAssertion(constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID'],
                                 editInfo['RESPONSE']['json']['entity']['id'], editInfo['PAYLOAD'], version=3).check()
        # approving message
        approveRespone = AuthorizeMessage.approve(campaignType, testControlType, listType, channel, messageInfo,
                                                  messageCreateResponse=editInfo)
        AuthorizeMessage.assertResponse(approveRespone, 200)
        campaignId = constant.config['node'][campaignType][testControlType]['CAMPAIGN']['ID']
        AuthorizeMessageDBAssertion(campaignId, editInfo['RESPONSE'], editInfo['PAYLOAD'],
                                    testControlType, version=3).check()
