import time

from src.dbCalls.campaignShard import list_Calls
from src.dbCalls.messageInfo import message_calls
from src.modules.irisv2.list.createAudienceDBAssertion import CreateAudienceDBAssertion
from src.modules.irisv2.message.authorizeMessageDbAssertion import AuthorizeMessageDBAssertion


class PreviewDBAssertion():
    def __init__(self, messageId, numberOfUsers):
        self.messageId = messageId
        self.listType = 'TEST_GROUP'
        self.numberOfusers = numberOfUsers
        self.getBasicInfoFromMessageId()

    def check(self):
        self.validateAudienceInfo()
        self.validateMessageInfo()

    def waitForListToBeUpdated(self):
        for _ in range(12):
            if list_Calls().getCustomerCountInGVD(self.listId) > 0:
                break
            time.sleep(5)

    def getBasicInfoFromMessageId(self):
        self.listId, self.campaignId = message_calls().getTargetAudienceForTestAndPreview(self.messageId)
        self.waitForListToBeUpdated()
        self.listInfo = {
            'VID': list_Calls().getGroupVersionId(self.listId)
        }

    def validateAudienceInfo(self):
        CreateAudienceDBAssertion(self.listId, self.listInfo, self.listType, self.numberOfusers).check()

    def validateMessageInfo(self):
        response = {
            'json': {
                'entity': {
                    'id': self.messageId
                }
            }
        }
        AuthorizeMessageDBAssertion(self.campaignId, response, {}, 'skip').check()
