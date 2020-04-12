import json,copy

from src.dbCalls.campaignShard import meta_details
from src.dbCalls.messageInfo import message_calls
from src.dbCalls.messageInfo import message_info
from src.modules.veneno.venenoDBAssertion import VenenoDBAssertion
from src.utilities.assertion import Assertion
from src.utilities.logger import Logger


class AuthorizeMessageDBAssertion():
    def __init__(self, campaignId, response, payload, testControlType, skippedReason=[],version=0,cguhVerify=False,personalizedMessage=False):
        Logger.log(
            'Approve Check for CampaignId :{} , with response From Create as :{} and payload used to Create Message as :{}'.format(
                campaignId, response, payload))
        self.campaignId = campaignId
        self.response = response
        self.payload = payload
        self.messageId = response['json']['entity']['id']
        self.testControlType = testControlType
        self.skippedReason = skippedReason
        self.cguhVerify = cguhVerify
        self.personalizedMessage = personalizedMessage
        self.messageDbInfo = message_info(self.messageId,version=version,personalize=self.personalizedMessage).messageDbDetail

    def check(self):
        self.validateVariantToCommunicationDetailsFlow()
        self.validateApproveStatus()

    def validateApproveStatus(self):
        messageApproveStatus = message_calls().getApproveStatus(self.messageId)
        Assertion.constructAssertion(messageApproveStatus == 'APPROVED',
                                     'Approved Status is :{} for MessageId :{}'.format(messageApproveStatus,
                                                                                       self.messageId))

    def validateEntryInCron(self, cronId, messageVariantId):
        Assertion.constructAssertion(cronId != 0, 'CronId is :{}'.format(cronId))
        cronDetails = message_calls().getCronDetails(cronId)
        Assertion.constructAssertion(cronDetails['component'] == 'CAMPAIGN',
                                     'Component Name In DB :{} and Expected : CAMPAIGN'.format(
                                         cronDetails['component']))

        cronParams = json.loads(cronDetails['params'])
        Assertion.constructAssertion(cronParams['messageVariantId'] == messageVariantId,
                                     'Params Of Cron Details have messageVariantId in DB :{} and expected  from Mongo :{}'.format(
                                         cronParams['messageVariantId'], messageVariantId))

    def validateVariantToCommunicationDetailsFlow(self):
        variant_creation_key = 'VARIANT_CREATION' if not self.personalizedMessage  else 'PERSONALIZED_VARIANT_CREATION'
        for eachVariant in self.messageDbInfo['messageJobDetails_collection'][variant_creation_key]:
            for varient in eachVariant['variant_detail']:
                if varient['skipTestControl'] :
                    self.testControlType = 'skip'
                messageQueueId = varient['messageVariantId']
                communicationDetailId, channel = message_calls().getCommunicationDetails(self.messageId, messageQueueId)
                listMetaInfo = meta_details(groupId=varient['audienceId'], groupVersionDetails=True).metaDetail
                numberOfUsers = listMetaInfo['groupVersionDetails']['TEST']['customer_count']
                groupVersionIdForTargetAudience = listMetaInfo['groupVersionDetails']['TEST']['id']
                self.validateEntryInCron(varient['cronTaskId'], varient['_id'])
                if channel in ['SMS','CALL_TASK']:
                    messageBody = varient['messageContent']['messageBody']
                elif channel == 'EMAIL':
                    messageBody = varient['messageContent']['emailSubject']
                elif channel == 'PUSH':
                    messageBody = varient['messageContent']['messageSubject']
                else:
                    raise Exception('OtherChannelNotSupportedException')
                venenoObject = VenenoDBAssertion(
                    self.campaignId,
                    channel,
                    communicationDetailId,
                    numberOfUsers,
                    groupVersionIdForTargetAudience,
                    messageBody,
                    self.testControlType.lower(),
                    self.skippedReason,
                    self.cguhVerify
                )
                if venenoObject.initFailureForStickyList:
                    venenoObject.check()

                if channel == 'PUSH': self.validatePushBody(venenoObject.communicationDetailResult['body'])

    def validatePushBody(self, cdBody):
        expectedBody = self.constructMessageBodyForPush()
        actualBody = json.loads(cdBody)
        Assertion.constructAssertion(expectedBody == actualBody,
                                     'ExpectedBody :{} and actualBody :{}'.format(expectedBody, actualBody))

    def constructMessageBodyForPush(self):
        messageBody = dict()
        messageBody.update({'templateData': {}})
        for eachContent in ['iosContent', 'androidContent']:
            if eachContent in self.payload['messageContent']['message_content_id_1']:
                if self.payload['messageContent']['message_content_id_1'][eachContent] is not None:
                    if eachContent == 'androidContent':
                        messageBody['templateData'].update({
                            'ANDROID': {
                                'title': self.payload['messageContent']['message_content_id_1'][eachContent]['title'],
                                'message': self.payload['messageContent']['message_content_id_1'][eachContent][
                                    'message'],
                                'expandableDetails': self.constructExpandablesDetail(
                                    self.payload['messageContent']['message_content_id_1'][eachContent][
                                        'expandableDetails']),
                                'custom': self.constructCustom(
                                    self.payload['messageContent']['message_content_id_1'][eachContent][
                                        'custom']),
                                "cuid": "{{cuid}}",
                                "luid": "{{luid}}",
                                "communicationId": "{{communicationId}}"
                            }
                        })
                        if 'cta' in self.payload['messageContent']['message_content_id_1'][eachContent] and self.payload['messageContent']['message_content_id_1'][eachContent]['cta'] is not None:
                            messageBody['templateData']['ANDROID'].update({
                                'cta':self.payload['messageContent']['message_content_id_1'][eachContent]['cta']
                            })
                        if 'custom' in self.payload['messageContent']['message_content_id_1'][eachContent] and self.payload['messageContent']['message_content_id_1'][eachContent]['custom'] is []:
                            messageBody['templateData']['ANDROID'].pop('custom')
                    elif eachContent == 'iosContent':
                        messageBody['templateData'].update({
                            'IOS': {
                                'title': self.payload['messageContent']['message_content_id_1'][eachContent]['title'],
                                'message': self.payload['messageContent']['message_content_id_1'][eachContent][
                                    'message'],
                                'expandableDetails': self.constructExpandablesDetail(
                                    self.payload['messageContent']['message_content_id_1'][eachContent][
                                        'expandableDetails']),
                                'custom': self.constructCustom(
                                    self.payload['messageContent']['message_content_id_1'][eachContent][
                                        'custom']),
                                "cuid": "{{cuid}}",
                                "luid": "{{luid}}",
                                "communicationId": "{{communicationId}}"
                            }
                        })
                        if 'cta' in self.payload['messageContent']['message_content_id_1'][eachContent] and self.payload['messageContent']['message_content_id_1'][eachContent]['cta'] is not None:
                            messageBody['templateData']['IOS'].update({
                                'cta':self.payload['messageContent']['message_content_id_1'][eachContent]['cta']
                            })
                        if 'custom' in self.payload['messageContent']['message_content_id_1'][eachContent] and self.payload['messageContent']['message_content_id_1'][eachContent]['custom'] is []:
                            messageBody['templateData']['IOS'].pop('custom')
                    else:
                        raise Exception('OtherContentNotSupportedException')
            else:
                Logger.log('Content Type :{} Not Present in this message'.format(eachContent))
        return messageBody

    def constructExpandablesDetail(self, detail):
        try:
            for key in detail.copy():
                if detail[key] is None:
                    detail.pop(key)
        except Exception,exp:
            Logger.log('Exception Caught while Constructing Expandable Details :{}'.format(exp))
        finally:
            return detail

    def constructCustom(self, custom):
        result = list()
        if custom is not None:
            for each in custom:
                result.append({
                    'key': each,
                    'value': custom[each]
                })
        return result
