from src.dbCalls.messageInfo import message_info
from src.utilities.assertion import Assertion
from src.utilities.logger import Logger

class VariantDBAssertion():
    def __init__(self, campaignId, messageId, response, offer=False, draft=False, approved=False, numberOfVariant=1,
                 messageCollection=True,
                 messageJobDetailsCollection=True, messageVariantsCollection=True):
        self.campaignId = campaignId
        self.messageId = messageId
        self.response = response
        self.offer = offer
        self.draft = draft
        self.approved = approved
        self.numberOfVariant = numberOfVariant
        self.messageCollection = messageCollection
        self.messageJobDetailsCollection = messageJobDetailsCollection
        self.messageVariantsCollection = messageVariantsCollection

        self.messageDbDetail = message_info(self.messageId, messageCollection, messageJobDetailsCollection,
                                            messageVariantsCollection).messageDbDetail

    def check(self):
        if len(self.response) == 0: Assertion.constructAssertion(False, 'messageVariantList is Empty in response')
        for eachVariant in self.response:
            variantId_validation = eachVariant['id']
            for eachVariantInDB in self.messageDbDetail['messageJobDetails_collection']['VARIANT_CREATION']:
                for variantDetail in eachVariantInDB['variant_detail']:
                    if variantDetail['_id'] == variantId_validation:
                        self.validateVariation(eachVariant, variantDetail)
                        break

    def validateVariation(self, responseVariantInfo, dbVarinatInfo):
        self.validateSchedule(responseVariantInfo, dbVarinatInfo)
        self.validateMessageContent(responseVariantInfo, dbVarinatInfo)
        self.validateBasicInfo(responseVariantInfo, dbVarinatInfo)
        self.validateChannelSetting(responseVariantInfo, dbVarinatInfo)

    def validateBasicInfo(self, responseVariantInfo, dbVarinatInfo):
        for eachKey in ['messageId', 'orgId', 'orgUnitId', 'campaignId']:
            Assertion.constructAssertion(
                responseVariantInfo[eachKey] == dbVarinatInfo[eachKey],
                'BasicInfo for Key :{} in Response :{} and in DB :{}'.format(
                    eachKey, responseVariantInfo[eachKey], dbVarinatInfo[eachKey]
                )
            )

        for eachKey in ['audienceId', 'createdBy', 'cronTaskId', 'lastUpdatedBy', 'messageVariantId']:
            Assertion.constructAssertion(
                responseVariantInfo[eachKey] == dbVarinatInfo[eachKey],
                'BasicInfo from Variant Detail :{} in Response :{} and in DB :{}'.format(
                    eachKey, responseVariantInfo[eachKey], dbVarinatInfo[eachKey]
                )
            )

    def validateMessageContent(self, responseVariantInfo, dbVarinatInfo):
        if responseVariantInfo['messageContent']['channel'] == 'SMS':
            keysToValidate = ['channel', 'messageBody', 'storeType']
        elif responseVariantInfo['messageContent']['channel'] == 'MOBILEPUSH':
            keysToValidate = ['channel', 'storeType', 'accountId', 'androidContent', 'iosContent']
        else:
            keysToValidate = ['channel', 'emailSubject', 'emailBody', 'storeType']
        for eachMessageContentKey in keysToValidate:
            if type(responseVariantInfo['messageContent'][eachMessageContentKey]) is dict:
                for eachKey in responseVariantInfo['messageContent'][eachMessageContentKey]:
                    if eachKey in dbVarinatInfo['messageContent'][eachMessageContentKey]:
                        Assertion.constructAssertion(
                            responseVariantInfo['messageContent'][eachMessageContentKey][eachKey] ==
                            dbVarinatInfo['messageContent'][eachMessageContentKey][eachKey],
                            'Key :{} in {} -> Value in Db and in response :{}'.format(eachKey,eachMessageContentKey,responseVariantInfo['messageContent'][eachMessageContentKey][eachKey],dbVarinatInfo['messageContent'][eachMessageContentKey][eachKey])
                        )
                    else:
                        Logger.log('Not Asserting for Key : {}'.format(eachKey))
            else:
                Assertion.constructAssertion(
                    responseVariantInfo['messageContent'][eachMessageContentKey] ==
                    dbVarinatInfo['messageContent'][eachMessageContentKey],
                    'MessageContent for key :{} in Response :{} and in DB :{}'.format(
                        eachMessageContentKey,
                        responseVariantInfo['messageContent'][eachMessageContentKey],
                        dbVarinatInfo['messageContent'][eachMessageContentKey]
                    )
                )
        if self.offer:
            for eachOffer in dbVarinatInfo['messageContent']['offers']:
                eachOffer.pop('_class')
            Assertion.constructAssertion(
                responseVariantInfo['messageContent']['offers'] ==
                dbVarinatInfo['messageContent']['offers'],
                'Offers from messageContent in Response :{} and in DB :{}'.format(
                    responseVariantInfo['messageContent']['offers'],
                    dbVarinatInfo['messageContent']['offers']
                ),verify=True
            )

    def validateChannelSetting(self, responseVariantInfo, dbVarinatInfo):
        if responseVariantInfo['channelSetting']['channel'] == 'SMS':
            keyToBeValidated = ['channel', 'gsmSenderId', 'domainGatewayMapId', 'targetNdnc', 'cdmaSenderId']
        elif responseVariantInfo['channelSetting']['channel'] == 'MOBILEPUSH':
            keyToBeValidated = ['channel']
        else:
            keyToBeValidated = ['channel', 'domainGatewayMapId', 'senderLabel', 'senderEmail', 'senderReplyTo']

        for eachChannelSettingKey in keyToBeValidated:
            Assertion.constructAssertion(
                responseVariantInfo['channelSetting'][eachChannelSettingKey] ==
                dbVarinatInfo['channelSetting'][eachChannelSettingKey],
                'ChannelSetting from key :{} in Response :{} and in DB :{}'.format(
                    eachChannelSettingKey,
                    responseVariantInfo['channelSetting'][eachChannelSettingKey],
                    dbVarinatInfo['channelSetting'][eachChannelSettingKey]
                )
            )

        for eachAdditionalSetting in ['useTinyUrl', 'encryptUrl', 'skipRateLimit']:
            Assertion.constructAssertion(
                responseVariantInfo['additionalSetting'][eachAdditionalSetting] ==
                dbVarinatInfo['additionalSetting'][eachAdditionalSetting],
                'AdditionalInfo from key :{} in Response :{} and in DB :{}'.format(
                    eachAdditionalSetting,
                    responseVariantInfo['additionalSetting'][eachAdditionalSetting],
                    dbVarinatInfo['additionalSetting'][eachAdditionalSetting]
                )
            )

    def validateSchedule(self, responseVariantInfo, dbVarinatInfo):
        Assertion.constructAssertion(
            responseVariantInfo['schedule']['scheduleType'] ==
            dbVarinatInfo['schedule']['type'],
            'Schedule in Response :{} and in DB :{}'.format(
                responseVariantInfo['schedule']['scheduleType'],
                dbVarinatInfo['schedule']['type']
            )
        )
