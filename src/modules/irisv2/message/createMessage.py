import random
import time
import requests
from src.Constant.constant import constant
from src.dbCalls.messageInfo import emailTrack
from src.dbCalls.messageInfo import message_calls
from src.modules.irisv2.campaigns.createCampaign import CreateCampaign
from src.modules.irisv2.helper.irisHelper import IrisHelper
from src.modules.irisv2.list.createAudience import CreateAudience
from src.modules.irisv2.message.productCategory import ProductCategory
from src.modules.luci.luciHelper import LuciHelper
from src.modules.luci.luciObject import LuciObject
from src.utilities.assertion import Assertion
from src.utilities.logger import Logger
from src.utilities.randValues import randValues
from src.utilities.utils import Utils


class CreateMessage():
    def __init__(self):
        pass

    @staticmethod
    def create(campaignType, testControlType, listType, channel, messageInfo={}, listInfo=None,
               campaignId=None,
               newUser=True, messageType='OUTBOUND', payload=None, targetAudience=None, scheduleType=None,
               messageStrategy=None, messageContent=None, updateNode=False, lockNode=False,
               storeType='REGISTERED_STORE', numberOfCustomTag=0, derivedListInfo=None, maxUser=[], remindParams=None,
               couponSeriesId=None):
        if not CreateMessage.checkMessageAvialable(campaignType, testControlType, listType, channel,
                                                   messageInfo['scheduleType']['type'],
                                                   messageInfo['offerType']) or updateNode:
            campaignInfo = CreateCampaign.create(campaignType, testControlType)
            listInfo = CreateMessage.getListInfo(campaignType, testControlType, listType, channel,
                                                 newUser, derivedListInfo) if listInfo is None else listInfo
            if listType == 'REMIND':
                if 'parentMessageId' not in remindParams and remindParams[
                    'parentMessageId'] is None and 'reminderStrategy' not in remindParams and remindParams[
                    'reminderStrategy'] is None: raise Exception('RequiredParamsMissingToConstructReminder')
                targetAudience = {
                    'isDef': True,
                    'includeDefinition': {
                        'defType': 'parentMsgReminder',
                        'parentMessageId': remindParams['parentMessageId'],
                        'reminderStrategy': remindParams['reminderStrategy']
                    },
                    'orgUsers': [] if 'orgUsers' not in remindParams else remindParams['orgUsers']
                }
            if listType == 'ORG_USERS':
                targetAudience = {'include': [constant.config['FilterListID']],
                                  'orgUsers': [listInfo['ID']], 'exclude': []}
            campaignId = str(campaignInfo['ID']) if campaignId is None else campaignId
            endPoint = IrisHelper.constructUrl('createmessage').replace('{campaignId}', str(campaignId))
            payload = CreateMessage.constructPayload(campaignType, testControlType, messageInfo, listInfo, channel,
                                                     messageType, numberOfCustomTag=numberOfCustomTag,
                                                     targetAudience=targetAudience,
                                                     scheduleType=scheduleType,
                                                     messageStrategy=messageStrategy,
                                                     messageContent=messageContent,
                                                     storeType=storeType,
                                                     maxUser=maxUser,
                                                     remindParams=remindParams,
                                                     couponSeriesId=couponSeriesId) if payload is None else payload
            Logger.log('Final Payload Used to Create Message :{}'.format(payload))
            if campaignType == 'UPCOMING' and messageInfo['scheduleType']['type'] == 'IMMEDIATE':
                for _ in range(30):
                    Logger.log(
                        'Upcoming Campaign , is not Yet Live current time :{} and startDate of Campaign is :{}'.format(
                            int(time.time() * 1000), campaignInfo['PAYLOAD']['startDate']))
                    if campaignInfo['PAYLOAD']['startDate'] > int(time.time() * 1000):
                        time.sleep(5)
                    else:
                        break
            timeout = 30 if remindParams is None else 180
            response = IrisHelper.constructResponse(
                Utils.makeRequest(url=endPoint, data=payload, auth=IrisHelper.constructAuthenticate(),
                                  headers=IrisHelper.constructHeaders(), timeout=timeout, method='POST')
            )

            if response['statusCode'] == 200:
                CreateMessage.validateCreateMessageResponse(response)
                if not lockNode: CreateMessage.updateMessageNode(campaignType, testControlType, listType, channel,
                                                                 messageInfo['scheduleType']['type'],
                                                                 messageInfo['offerType'],
                                                                 response, payload)
                if campaignType == 'LAPSED': time.sleep(2 * 60)
                return {
                    'PAYLOAD': payload,
                    'RESPONSE': response
                }
            else:
                return {
                    'RESPONSE': response,
                    'PAYLOAD': payload
                }
        else:
            return constant.config['node'][campaignType][testControlType]['LIST'][listType][channel]['MESSAGE']
            [messageInfo['scheduleType']['type']][messageInfo['offerType']]

    @staticmethod
    def edit(campaignId, messageId, payload, editInfo=None):
        endpoint = IrisHelper.constructUrl('editmessage').replace('{campaignId}', str(campaignId)).replace('{msgId}',
                                                                                                           messageId)
        if editInfo is not None:
            payload.update(editInfo)
        response = IrisHelper.constructResponse(
            Utils.makeRequest(url=endpoint, data=payload, auth=IrisHelper.constructAuthenticate(),
                              headers=IrisHelper.constructHeaders(), method='PUT')
        )
        return {
            'RESPONSE': response,
            'PAYLOAD': payload
        }

    @staticmethod
    def reject(campaignId, messageId):
        endpoint = IrisHelper.constructUrl('rejectmessage').replace('{campaignId}', str(campaignId)).replace('{msgId}',
                                                                                                             messageId)
        response = IrisHelper.constructResponse(
            Utils.makeRequest(url=endpoint, data='', auth=IrisHelper.constructAuthenticate(),
                              headers=IrisHelper.constructHeaders(), method='POST')
        )
        return response

    @staticmethod
    def stop(campaignId, messageId):
        endpoint = IrisHelper.constructUrl('stopmessage').replace('{campaignId}', str(campaignId)).replace('{msgId}',
                                                                                                           messageId)
        response = IrisHelper.constructResponse(
            Utils.makeRequest(url=endpoint, data='', auth=IrisHelper.constructAuthenticate(),
                              headers=IrisHelper.constructHeaders(), method='POST')
        )
        return response

    @staticmethod
    def start(campaignId, messageId):
        endpoint = IrisHelper.constructUrl('startmessage').replace('{campaignId}', str(campaignId)).replace('{msgId}',
                                                                                                            messageId)
        response = IrisHelper.constructResponse(
            Utils.makeRequest(url=endpoint, data='', auth=IrisHelper.constructAuthenticate(),
                              headers=IrisHelper.constructHeaders(), method='POST')
        )
        return response

    @staticmethod
    def getListInfo(campaignType, testControlType, listType, schemaIdentifier, newUser, derivedListInfo):
        if schemaIdentifier.upper() == 'MOBILE_PUSH':
            return CreateAudience.uploadList(campaignType, testControlType, schemaIdentifier=['USER_ID'],
                                             schemaData=['USER_ID'], newUser=newUser, updateNode=True, lockNode=True,
                                             campaignCheck=False, mobilePush=True)
        if listType == 'UPLOAD':
            return CreateAudience.uploadList(campaignType, testControlType, schemaIdentifier=[schemaIdentifier],
                                             schemaData=[schemaIdentifier, 'FIRST_NAME'], newUser=newUser,
                                             campaignCheck=False)
        elif listType == 'LOYALTY':
            return CreateAudience.FilterList(campaignType, testControlType, schemaIdentifier=[schemaIdentifier],
                                             campaignCheck=False)
        elif listType == 'DERIVED':
            return CreateAudience.derivedList(campaignType, testControlType, schemaIdentifier=[schemaIdentifier],
                                              newUser=newUser, campaignCheck=False, derivedListInfo=derivedListInfo)
        elif listType == 'ORG_USERS':
            return CreateAudience.stickyList(campaignType, testControlType, schemaIdentifier=[schemaIdentifier],
                                             campaignCheck=False, stickyInfo=derivedListInfo)
        else:
            raise Exception('ListTypeNotSupportedException:{}'.format(listType))

    @staticmethod
    def checkMessageAvialable(campaignType, testControlType, listType, channel, scheduleType, offerType,
                              rejectListType=['REMIND']):
        if listType in rejectListType: return False
        if offerType in ['registeredStore', 'lasttransactedstore']: return False
        listAvialable = True
        for each in ['PAYLOAD', 'RESPONSE']:
            if constant.config['node'][campaignType][testControlType]['LIST'][listType][channel]['MESSAGE'][
                scheduleType][offerType][each] is None:
                listAvialable = False
        return listAvialable

    @staticmethod
    def validateCreateMessageResponse(response):
        Assertion.constructAssertion('id' in response['json']['entity'], 'ID Found in Response Entity', )
        Assertion.constructAssertion(response['json']['entity']['id'] is not None, 'Valid Value of Entity')

    @staticmethod
    def updateMessageNode(campaignType, testControlType, listType, channel, scheduleType, offerType,
                          response, payload):
        constant.config['node'][campaignType][testControlType]['LIST'][listType][channel]['MESSAGE'][
            scheduleType][offerType]['RESPONSE'] = response
        constant.config['node'][campaignType][testControlType]['LIST'][listType][channel]['MESSAGE'][
            scheduleType][offerType]['PAYLOAD'] = payload

    @staticmethod
    def constructPayload(campaignType, testControlType, messageInfo, listInfo, channel, type='OUTBOUND',
                         numberOfCustomTag=0,
                         targetAudience=None, scheduleType=None,
                         messageStrategy=None, messageContent=None, storeType='REGISTERED_STORE', maxUser=[],
                         remindParams=None, couponSeriesId=None):
        payload = dict()
        payload['type'] = type
        payload['name'] = 'AutomationMessage_{}'.format(int(time.time() * 1000))

        payload['targetAudience'] = {
            'include': [listInfo['ID']],
            'exclude': []
        } if targetAudience is None else targetAudience

        payload['schedule'] = CreateMessage.constructSchedule(
            messageInfo['scheduleType']) if scheduleType is None else scheduleType

        payload['messageStrategy'] = CreateMessage.constructMessageStrategy(
            messageInfo['messageStrategy']) if messageStrategy is None else messageStrategy

        payload['messageContent'] = CreateMessage.constructMessageContent(campaignType, testControlType,
                                                                          messageInfo['messageStrategy'],
                                                                          messageInfo['offerType'],
                                                                          channel,
                                                                          storeType=storeType,
                                                                          numberOfCustomTag=numberOfCustomTag,
                                                                          couponSeriesId=couponSeriesId) if messageContent is None else messageContent

        payload['deliverySetting'] = CreateMessage.constructDeliverySetting(messageInfo['channels'],
                                                                            messageInfo['useTinyUrl'],
                                                                            messageInfo['encryptUrl'],
                                                                            messageInfo['skipRateLimit'],
                                                                            maxUsers=maxUser)
        if remindParams is not None: payload['reminder'] = True
        return payload

    @staticmethod
    def constructSchedule(scheduleType):
        if scheduleType['type'] == 'IMMEDIATE':
            return {
                'scheduleType': 'IMMEDIATE'
            }
        elif scheduleType['type'] == 'PARTICULARDATE':
            return {
                'scheduleType': 'PARTICULAR_DATE',
                'scheduledDate': Utils.getTime(minutes=4, seconds=30, milliSeconds=True)
            }
        elif scheduleType['type'] == 'RECURRING':
            defaultScheduleTimer = Utils.getTime(hours=5, minutes=35, dateTimeFormat=True)
            return {
                'scheduleType': 'RECURRING',
                'hour': scheduleType['hour'] if 'hour' in scheduleType else int(defaultScheduleTimer[11:13]),
                'minute': scheduleType['minute'] if 'minute' in scheduleType else int(defaultScheduleTimer[14:16]),
                'startDate': scheduleType['startDate'] if 'startDate' in scheduleType else Utils.getTime(seconds=90,
                                                                                                         milliSeconds=True),
                'endDate': scheduleType['endDate'] if 'endDate' in scheduleType else Utils.getTime(hours=20,
                                                                                                   milliSeconds=True),
                'repeatType': scheduleType['repeatType'] if 'repeatType' in scheduleType else 'DAILY',
                'repeatOn': scheduleType['repeatOn'] if 'repeatOn' in scheduleType else [1]
            }
        else:
            raise Exception('NotSupportedScheduleTypeException:{}'.format(scheduleType['type']))

    @staticmethod
    def constructMessageStrategy(strategy):
        if strategy['type'] == 'DEFAULT':
            return {
                'type': 'DEFAULT'
            }
        if strategy['type'] == 'PERSONALISATION':
            return {
                'type': 'PERSONALISATION',
                'criteria': {
                    'criteriaTypes': ["PRODUCT_CATEGORY"] if 'criteriaTypes' not in strategy else  strategy[
                        'criteriaTypes'],
                    'productCategories': CreateMessage.constructProductCategory(strategy)
                }
            }
        else:
            raise Exception('OnlyDefaultStrategySupportedException')

    @staticmethod
    def constructProductCategory(strategy):
        productCategoryMap = CreateMessage.getProductCategory()
        if 'defaultCategory' in strategy:
            randomCategory = random.choice(list(productCategoryMap.keys()))
            return [{
                'productCode': [{
                    'level': productCategoryMap[randomCategory]['num'],
                    'codes': [random.choice(productCategoryMap[randomCategory]['value'])]
                }],
                'contentIdentifier': 'message_content_id_1'
            }]
        elif 'productCategory' in strategy:
            return strategy['productCategory']
        elif 'numberOfCategory' in strategy:
            if strategy['useDifferentLevel']:
                productCategory = list()
                randomCategory = list(productCategoryMap.keys())
                for each in range(strategy['numberOfCategory']):
                    randomCategoryValue = random.choice(range(len(randomCategory)))
                    productCategory.append({
                        'productCode': [{
                            'level': productCategoryMap[randomCategory[randomCategoryValue]]['num'],
                            'codes': [random.choice(productCategoryMap[randomCategory[randomCategoryValue]]['value'])]
                        }],
                        'contentIdentifier': strategy['messageContentId'][each]
                    })
                return productCategory
            else:
                productCategory = list()
                randomCategory = random.choice(list(productCategoryMap.keys()))
                for each in range(strategy['numberOfCategory']):
                    productCategory.append({
                        'productCode': [{
                            'level': productCategoryMap[randomCategory]['num'],
                            'codes': [random.choice(productCategoryMap[randomCategory]['value'])]
                        }],
                        'contentIdentifier': random.choice(strategy['messageContentId'])
                    })
        else:
            return [{
                'productCode': [{
                    'level': strategy['levelnum'],
                    'codes': strategy['codes']
                }],
                'messageContent': strategy['messageContentId']
            }]

    @staticmethod
    def getProductCategory(apiCategory='productCategory'):
        productCategoryMap = dict()
        for eachLevel in ProductCategory.getLevelsForDimension(apiCategory)['json']['entity']['levels']:
            if eachLevel['levelName'] != 'item_code':
                levelValue = \
                ProductCategory.getLevelValuesForDimension(apiCategory, eachLevel['levelName'])['json']['entity'][
                    'levelValues']
                levelValue.remove('NOT-CAPTURED')
                levelnum = eachLevel['levelNum']
                productCategoryMap.update({eachLevel['levelName']: {'value': levelValue, 'num': levelnum}})
        Logger.log(
            'Product Category Map Contructed for OrgId :{} , {}'.format(constant.config['orgId'], productCategoryMap))
        return productCategoryMap

    @staticmethod
    def constructMessageContent(campaignType, testControlType, strategy, offerType, channel,
                                storeType='REGISTERED_STORE', numberOfCustomTag=0, couponSeriesId=None):
        channel = 'SMS' if channel == 'MOBILE' else channel
        if strategy['type'] == 'DEFAULT':
            return CreateMessage.constructContentBase(campaignType, testControlType, strategy, offerType, channel,
                                                      storeType, numberOfCustomTag, couponSeriesId)
        if strategy['type'] == 'PERSONALISATION':
            if 'numberOfCategory' not in strategy:
                return CreateMessage.constructContentBase(campaignType, testControlType, strategy, offerType, channel,
                                                          storeType, numberOfCustomTag, couponSeriesId)
            else:
                actualContent = dict()
                for each in range(strategy['numberOfCategory']):
                    contentName = 'message_content_id_{}'.format(each)
                    offerType = strategy['offers'][each]
                    content = CreateMessage.constructContentBase(campaignType, testControlType, strategy, offerType,
                                                                 strategy["channels"][each],
                                                                 storeType, numberOfCustomTag, couponSeriesId,
                                                                 contentname=contentName)
                    actualContent.update({contentName: content[contentName]})
                return actualContent
        else:
            raise Exception('StrategySupportedException')

    @staticmethod
    def constructContentBase(campaignType, testControlType, strategy, offerType, channel,
                             storeType='REGISTERED_STORE', numberOfCustomTag=0, couponSeriesId=None,
                             contentname='message_content_id_1'):
        if channel.upper() == 'SMS':
            content = {
                contentname: {
                    'storeType': storeType,
                    'channel': channel,
                    'messageBody': CreateMessage.getMessageBody(offerType, channel, numberOfCustomTag)
                }
            }
        if channel.upper() == 'EMAIL':
            content = {
                contentname: {
                    'storeType': storeType,
                    'channel': 'EMAIL',
                    'emailBody': 'Automation Create Body {{unsubscribe}}',
                    'emailSubject': CreateMessage.getMessageBody(offerType, channel, numberOfCustomTag)
                }
            }
        if channel.upper() in ['EXTERNAL_ID', 'USER_ID']:
            content = {
                contentname: {
                    'storeType': storeType,
                    'channel': 'SMS',
                    'messageBody': CreateMessage.getMessageBody(offerType, 'SMS')
                }
            }
        if channel.upper() == 'MOBILE_PUSH':
            content = {
                contentname: {
                    'storeType': storeType,
                    'channel': 'MOBILEPUSH',
                    'messageSubject': 'Automation Created Subject',
                    'accountId': message_calls().getAccountIdFromMeta(constant.config['mobilepush']['account']),
                    'androidContent': CreateMessage.getAndroidContent(strategy['android']['contentType'],
                                                                      offerType=offerType,
                                                                      secondaryCTA=strategy['android'][
                                                                          'secondary_cta'],
                                                                      primaryCTA=strategy['android']['primary_cta'],
                                                                      custom=strategy['android']['custom'],
                                                                      numberOfCustomTag=numberOfCustomTag) if 'android' in strategy else None,
                    'iosContent': CreateMessage.getIOSContent(strategy['ios']['contentType'], offerType=offerType,
                                                              secondaryCTA=strategy['ios']['secondary_cta'],
                                                              primaryCTA=strategy['ios']['primary_cta'],
                                                              custom=strategy['ios']['custom'],
                                                              numberOfCustomTag=numberOfCustomTag) if 'ios' in strategy else None
                }
            }
        if offerType == 'COUPON':
            content[contentname].update(
                {
                    'offers': [{
                        'type': 'COUPON',
                        'couponSeriesId': CreateMessage.getCouponSeriesId(
                            constant.config['node'][campaignType][testControlType]['CAMPAIGN'][
                                'ID']) if couponSeriesId is None else couponSeriesId
                    }]
                }
            )
        if offerType == 'MULTICOUPONS':
            couponSeriesId = CreateMessage.getCouponSeriesId(
                            constant.config['node'][campaignType][testControlType]['CAMPAIGN'][
                                'ID']) if couponSeriesId is None else couponSeriesId
            couponSeriesId1 = CreateMessage.getSecondCouponSeriesId(
                            constant.config['node'][campaignType][testControlType]['CAMPAIGN'][
                                'ID'])
            content['message_content_id_1'].update(
                {
                    'offers': [{
                        'type': 'COUPON',
                        'couponSeriesId': couponSeriesId
                    }, {
                        'type': 'COUPON',
                        'couponSeriesId': couponSeriesId1
                    }]
                }
            )
            if channel.upper() == 'SMS':
                content['message_content_id_1'].update(
                    {
                        'messageBody': content['message_content_id_1']['messageBody'].replace("(CSId)", "(" + str(couponSeriesId) + ")").replace("(CSId1)", "(" + str(couponSeriesId1) + ")")
                    }
                )
            if channel.upper() == 'EMAIL':
                content['message_content_id_1'].update(
                    {
                        'emailSubject': content['message_content_id_1']['emailSubject'].replace("(CSId)", "(" + str(couponSeriesId) + ")").replace("(CSId1)", "(" + str(couponSeriesId1) + ")")
                    }
                )
            if channel.upper() == 'MOBILE_PUSH':
                content['message_content_id_1']['androidContent'].update(
                    {
                        'message': content['message_content_id_1']['androidContent']['message'].replace("(CSId)", "(" + str(couponSeriesId) + ")").replace("(CSId1)", "(" + str(couponSeriesId1) + ")")
                    }
                )
                content['message_content_id_1']['iosContent'].update(
                    {
                        'message': content['message_content_id_1']['iosContent']['message'].replace("(CSId)", "(" + str(couponSeriesId) + ")").replace("(CSId1)", "(" + str(couponSeriesId1) + ")")
                    }
                )
        if offerType == 'POINTS':
            pointsIds = CreateMessage.getStrategyIds()
            content[contentname].update(
                {
                    'offers': [{
                        'type': 'POINTS',
                        'programId': pointsIds['programeId'],
                        'allocationStrategyId': pointsIds['allocationStrategyId'],
                        'expirationStrategyId': pointsIds['expirationStrategyId']
                    }]
                }
            )
        return content

    @staticmethod
    def getSecondCouponSeriesId(campaignId):
        constant.config['campaignId'] = campaignId
        constant.config['adminId'] = int(constant.config['userId'])
        constant.config['requestId'] = 'RequestID_IRISV2_{}'.format(int(time.time()))
        return LuciHelper.getConnObj(newConnection=True).saveCouponConfiguration(
            LuciObject.saveCouponConfigRequest(LuciObject.couponConfiguration({
                        "description": "multiple offers testing",
                        "info": "multiple offers testing",
                        "discount_code": "ABC123"

            }))).__dict__['id']


    @staticmethod
    def getAndroidContent(type, offerType='plain', secondaryCTA=None, primaryCTA=None, custom=False,
                          numberOfCustomTag=0):
        androidContent = dict()
        androidContent.update({
            'type': type,
            'deviceType': 'ANDROID',
            'title': 'Automation Mobile Push Message Android',
            'message': CreateMessage.getMessageBody(offerType, 'SMS', numberOfCutomTags=numberOfCustomTag),
            'expandableDetails': {
                'style': 'BIG_TEXT' if type is 'TEXT' else 'BIG_PICTURE',
                'message': 'Automation Constructed',
                'ctas': CreateMessage.getSecondaryCTAS('android', secondaryCTA['value']) if secondaryCTA[
                    'enable'] else None
            },
            'cta': CreateMessage.getPrimaryCTAS(primaryCTA['value']) if primaryCTA['enable'] else None,
            'custom': CreateMessage.getCustomsMobilePush(custom)
        })
        if type.lower() == 'image': androidContent['expandableDetails'].update({
            'image': 'https://www.capillarytech.com'
        })
        return androidContent

    @staticmethod
    def getIOSContent(type, offerType='plain', secondaryCTA=None, primaryCTA=None, custom=False, numberOfCustomTag=0):
        iosContent = dict()
        iosContent.update({
            'type': type,
            'deviceType': 'IOS',
            'title': 'Automation Mobile Push Message',
            'message': CreateMessage.getMessageBody(offerType, 'SMS', numberOfCutomTags=numberOfCustomTag),
            'expandableDetails': {
                'style': 'BIG_TEXT' if type is 'TEXT' else 'BIG_PICTURE',
                'message': 'Automation Constructed',
                'categoryId': constant.config['iosSecondaryLink']['categoryId'],
                'ctas': CreateMessage.getSecondaryCTAS('ios', secondaryCTA['value']) if secondaryCTA['enable'] else None
            },
            'cta': CreateMessage.getPrimaryCTAS(primaryCTA['value']) if primaryCTA['enable'] else None,
            'custom': CreateMessage.getCustomsMobilePush(custom)
        })
        if type.lower() == 'image': iosContent['expandableDetails'].update({
            'image': 'https://www.capillarytech.com'
        })
        return iosContent

    @staticmethod
    def getSecondaryCTAS(device, ctas=None):
        listOfDicts = list()
        if device.lower() == 'android':
            ctas = [['Send', 'DEEP_LINK', 'Auto Link'],
                    ['Reply', 'EXTERNAL_URL', 'https://www.capillarytech.com']] if ctas is None else ctas
            for eachListOfValue in ctas:
                if 'Auto Link' in eachListOfValue: eachListOfValue[
                    eachListOfValue.index('Auto Link')] = CreateMessage.getDeepLinkValue()
            for eachInfo in ctas:
                listOfDicts.append({
                    'actionText': eachInfo[0],
                    'type': eachInfo[1],
                    'actionLink': eachInfo[2]
                })
        elif device.lower() == 'ios':
            ctas = [['Send', 'DEEP_LINK', 'Auto Link', '18dfbbcc']] if ctas is None else ctas
            for eachListOfValue in ctas:
                if 'Auto Link' in eachListOfValue: eachListOfValue[
                    eachListOfValue.index('Auto Link')] = CreateMessage.getDeepLinkValue()
            for eachInfo in ctas:
                ctaValue = {
                    'actionText': eachInfo[0],
                    'type': eachInfo[1],
                    'actionLink': eachInfo[2],
                    'templateCtaId': eachInfo[3]
                }
                if ctaValue['templateCtaId'] in [None, '']: ctaValue.pop('templateCtaId')
                listOfDicts.append(ctaValue)

        else:
            raise Exception('Device :{} not supported'.format(device))
        return listOfDicts

    @staticmethod
    def getDeepLinkValue():
        deepLinkValue = message_calls().getDeepLinkvalue(
            message_calls().getAccountIdFromMeta(constant.config['mobilepush']['account']),
            message_calls().getKeyOfDeepLink())
        randomKeyFromDeepLink = random.choice(list(deepLinkValue.keys()))
        linkFormed = deepLinkValue[randomKeyFromDeepLink]['link'] + '?'
        keysFrommLinked = deepLinkValue[randomKeyFromDeepLink]['keys']
        for eachKey in keysFrommLinked:
            linkFormed = linkFormed + '{}={}&'.format(eachKey, randValues.randomString(5))
        return linkFormed

    @staticmethod
    def getPrimaryCTAS(cta=None):
        primaryCTA = dict()
        cta = ['DEEP_LINK', 'Auto Link'] if cta is None else cta
        if 'Auto Link' in cta: cta[cta.index('Auto Link')] = CreateMessage.getDeepLinkValue()
        primaryCTA.update({
            'type': cta[0],
            'actionLink': cta[1]
        })
        return primaryCTA

    @staticmethod
    def getCustomsMobilePush(customEnable):
        if customEnable:
            return {
                'Automation': 'Test'
            }
        else:
            return {}

    @staticmethod
    def getMessageBody(offerType, channel, numberOfCutomTags=0):
        body = constant.irisMessage[channel.lower()][offerType.lower()]
        if numberOfCutomTags != 0:
            for idx in range(1, numberOfCutomTags + 1):
                body = body + ' {{custom_tag_' + str(idx) + '}}'
        return body

    @staticmethod
    def constructDeliverySetting(channels, tinyurl=False, encryptUrl=False, rateLimit=True, maxUsers=[]):
        deliverySetting = {
            'channelSetting': {},
            'additionalSetting': {
                'useTinyUrl': tinyurl,
                'encryptUrl': encryptUrl,
                'skipRateLimit': rateLimit
            }
        }
        if len(maxUsers) > 0: deliverySetting['additionalSetting'].update({'maxUsers': maxUsers[0]})
        for eachChannel in channels:
            if eachChannel.upper() == 'SMS':
                domainProp = IrisHelper.getDomainGatewayMapId(eachChannel)
                deliverySetting['channelSetting'].update(
                    {
                        'SMS': {
                            'channel': 'SMS',
                            'gsmSenderId': domainProp['gsm_sender_id'],
                            'cdmaSenderId': domainProp['cdma_sender_id'],
                            'domainGatewayMapId': domainProp['mapId'],
                            'targetNdnc': False
                        }
                    }
                )
            elif eachChannel.upper() == 'EMAIL':
                domainProp = IrisHelper.getDomainGatewayMapId(eachChannel)
                deliverySetting['channelSetting'].update(
                    {
                        'EMAIL': {
                            'channel': 'EMAIL',
                            'domainGatewayMapId': domainProp['mapId'],
                            'senderLabel': 'test',
                            'senderEmail': domainProp['sender_id'],
                            'senderReplyTo': domainProp['reply_to_id']
                        }
                    }
                )
            elif eachChannel.upper() == 'MOBILE_PUSH':
                deliverySetting['channelSetting'].update(
                    {
                        'MOBILEPUSH': {
                            'channel': 'MOBILEPUSH'
                        }
                    }
                )
            else:
                raise Exception('Channel:{}NotSupportedException'.format(eachChannel))
        return deliverySetting

    @staticmethod
    def assertResponse(response, expectedStatusCode, expectedErrorCode=999999, expectedErrorMessage=[]):
        if response['constructed'].lower() == 'pass':
            if expectedStatusCode >= 200 and expectedStatusCode <= 300:
                Assertion.constructAssertion(response['statusCode'] == int(expectedStatusCode),
                                             'Matching statusCode actual :{},expected :{}'.format(
                                                 response['statusCode'], expectedStatusCode))
                if len(response['json']['warnings']) > 0:
                    Logger.log('There was a Warning while Creating Campaign :', response['json']['warning'])
            else:
                Assertion.constructAssertion(response['statusCode'] == int(expectedStatusCode),
                                             'Matching statusCode actual :{},expected :{}'.format(
                                                 response['statusCode'], expectedStatusCode))
                for errorReturned in response['json']['errors']:
                    Logger.log('Status Code :{} and error :{}'.format(response['statusCode'], errorReturned))
                    Assertion.constructAssertion(errorReturned['code'] in expectedErrorCode,
                                                 'Matching Error Code ,actual:{} and expected:{}'.format(
                                                     errorReturned['code'], expectedErrorCode))
                    Assertion.constructAssertion(errorReturned['status'] == False, 'Checking for Error Status as False')
                    Logger.log(errorReturned['message'] in expectedErrorMessage)
                    Assertion.constructAssertion(errorReturned['message'] in expectedErrorMessage,
                                                 'Matching Error Message ,actual:{} in expected:{}'.format(
                                                     errorReturned['message'], expectedErrorMessage))
        else:
            Assertion.constructAssertion(False, 'Constructed Body has Failed due to Exception so no Validation')

    @staticmethod
    def getCouponSeriesId(campaignId):
        constant.config['campaignId'] = campaignId
        constant.config['adminId'] = int(constant.config['userId'])
        constant.config['requestId'] = 'RequestID_IRISV2_{}'.format(int(time.time()))
        return LuciHelper.getConnObj(newConnection=True).saveCouponConfiguration(
            LuciObject.saveCouponConfigRequest(LuciObject.couponConfiguration({}))).__dict__['id']

    @staticmethod
    def getStrategyIds():
        programeId = message_calls().getProgrameId()
        allocationStrategyId = message_calls().getAllocationIdForPrograme(programeId)
        expirationStrategyId = message_calls().getExpiryIdForPrograme(programeId)
        return {'programeId': int(programeId), 'allocationStrategyId': int(allocationStrategyId),
                'expirationStrategyId': int(expirationStrategyId)}

    @staticmethod
    def redirectURL(self, messageId, campaignId):
        messageBody = emailTrack().getMessageBody(messageId)
        emailLink = emailTrack().getEmailLinkRedirection(campaignId)
        linkId = str(emailLink[0][1]).encode('base64')
        Assertion.constructAssertion(emailLink[0][0] == 'http://www.python.org', 'The URL is same')
        Assertion.constructAssertion(linkId.rstrip() in messageBody, 'the link id is {}'.format(linkId))
        response = messageBody.split('href=')[1].split('>')[0][1:-1]
        gaLink = requests.get(
            url=response)
        finalLink = gaLink.request.url
        Assertion.constructAssertion('test+gaSource' in finalLink, "The utm_source name is correct")
        Assertion.constructAssertion('test+gaName' in finalLink, "The utm_campaign name is correct")
        return finalLink
