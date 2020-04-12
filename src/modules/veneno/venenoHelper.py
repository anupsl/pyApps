from src.modules.veneno.venenoThrift import VenenoThrift
from src.modules.iris.campaigns import campaigns
from src.modules.iris.message import campaignMessage
from src.modules.campaign_shard.campaignShardHelper import CampaignShardHelper
from src.modules.veneno.venenoDBAssertion import VenenoDBAssertion
from src.modules.iris.dbCallsCampaign import dbCallsCampaign
from src.modules.iris.dbCallsMessage import dbCallsMessage
from src.modules.iris.dbCallsAuthorize import dbCallsAuthorize
from src.modules.iris.dbCallsCoupons import dbCallsCoupons
from src.modules.iris.dbCallsList import dbCallsList
from src.modules.nsadmin.nsadminHelper import NSAdminHelper
from src.modules.iris.construct import construct
from src.modules.iris.coupons import coupons
from src.modules.iris.authorize import authorize
from src.modules.iris.list import campaignList
from src.modules.luci.luciObject import LuciObject
from src.modules.luci.luciThrift import LuciThrift
from src.utilities.logger import Logger
from src.Constant.constant import constant
from src.utilities.utils import Utils
from itertools import cycle
import traceback, time, json

class VenenoHelper():
    
    @staticmethod
    def checkVenenoServerConnection(ignoreConnectionError=False):
        Utils.checkServerConnection('VENENO_LISTENER_THRIFT_SERVICE', VenenoThrift, 'venenoPort', ignoreConnectionError)


    @staticmethod
    def getConnObj(newConnection=False):
        port = constant.config['venenoPort'].next()
        connPort = str(port) + '_obj'
        if connPort in constant.config:
            if newConnection:
                constant.config[connPort].close()
                constant.config[connPort] = VenenoThrift(port)
            return constant.config[connPort]
        else:
            return VenenoThrift(port)

    @staticmethod
    def preRequisitesForVeneno(testControlType='org'):
        if 'storeType' in constant.payload['createmessage'] :constant.payload['createmessage'].pop('storeType')
         
        campaignResponse, campaignPayload = campaigns.createCampaign({'name':'IRIS_' + str(int(time.time() * 100000)), 'goalId':constant.irisGenericValues['goalId'], 'objectiveId':constant.irisGenericValues['objectiveId'], 'testControl':{'type' : testControlType.upper(), 'test' : 90}})
        listResponse, listPayload, campaignId = campaignList.createList({'customTagCount':1, 'name':'IRIS_LIST_' + str(int(time.time() * 100000))}, campaignId=campaignResponse['json']['entity']['campaignId'])
        addRecipientResponse, addRecipientPayload = campaignList.addRecipient({}, campaignId, listResponse['json']['entity']['listId'], 'mobile,email', 10, 1, newUser=False)
        responseCoupon, payloadCoupon, campaignId = coupons.createCoupons(campaignId=campaignId)
        strategyDict = construct.constructStrategyIds()
        groupVersionDict = dbCallsList.getGroupVersionDetailsWithGroupId(listResponse['json']['entity']['listId'])

        return {'campaignId':campaignId,
                'listId':listResponse['json']['entity']['listId'],
                'voucherId':responseCoupon['json']['entity']['voucherSeriesId'],
                'strategy':strategyDict,
                'programeId':strategyDict['programeId'],
                'allocationStrategyId':strategyDict['allocationStrategyId'],
                'expiryStrategyId':strategyDict['expirationStrategyId'],
                'bucketId':groupVersionDict['TEST']['bucket_id'],
                'groupVersionResult':groupVersionDict,
                'groupName':listPayload['name']
                }
        
    @staticmethod
    def preRequisitesForVenenoRateLimit(channel,testControl='org'):
        if channel.lower() in ['mobile', 'email']:
            campaignResponse, campaignPayload = campaigns.createCampaign({'name':'Veneno_RateLimit_' + str(int(time.time() * 100000)), 'goalId':constant.irisGenericValues['goalId'], 'objectiveId':constant.irisGenericValues['objectiveId'], 'testControl':{'type' : testControl.upper(), 'test' : 90}})
            return {
                    'campaign':{
                        'name':campaignPayload['name'],
                        'id':campaignResponse['json']['entity']['campaignId']
                        },
                    'list':{
                        'upload':CampaignShardHelper.setupUploadList('org', campaignPayload['name'], campaignResponse['json']['entity']['campaignId'], 'RL' , newUser=True, setupObjectForCampaignShard=False, channel=channel)
                        }
                }
        elif channel.lower() in ['android', 'ios']:
            venenoObjectForPush = VenenoHelper.preRequisitesForVenenoMobilePush(channel.lower())
            return {
                    'campaign':{
                        'name':venenoObjectForPush['campaignName'],
                        'id':venenoObjectForPush['campaignId']
                        },
                    'list':{
                        'upload':{
                            'addRecipientPayload':venenoObjectForPush['addRecipientPayload'],
                            'groupLabel':venenoObjectForPush['groupName'],
                            'groupDetails':venenoObjectForPush['groupDetails'],
                            'groupVersionDetails':venenoObjectForPush['groupVersionResult'],
                            'campaignGroupRecipients':venenoObjectForPush['campaignGroupRecipient']
                            }
                        }
                }
        elif channel.lower() in ['wechat']:
            venenoObjectForWechat = VenenoHelper.preRequisitesForVenenoWechat()
            return {
                    'campaign':{
                        'name':venenoObjectForWechat['campaignName'],
                        'id':venenoObjectForWechat['campaignId']
                        },
                    'list':{
                        'upload':{
                            'addRecipientPayload':venenoObjectForWechat['addRecipientPayload'],
                            'groupLabel':venenoObjectForWechat['groupName'],
                            'groupDetails':venenoObjectForWechat['groupDetails'],
                            'groupVersionDetails':venenoObjectForWechat['groupVersionResult'],
                            'campaignGroupRecipients':venenoObjectForWechat['campaignGroupRecipient']
                            }
                        }
                }
        else:
            raise Exception("Channel :{} not Supported in preRequisites".format(channel))
            
    @staticmethod
    def preRequisitesForVenenoWechat(userData=[],testControlType='org'):
        if len(userData) == 0 :
            for eachUser in constant.config['wechat']['user']:
                userData.append(eachUser['firstName'] + ',' + eachUser['lastName'] + ',' + eachUser['email'])
        
        if 'storeType' in constant.payload['createmessage'] :constant.payload['createmessage'].pop('storeType')
         
        campaignResponse, campaignPayload = campaigns.createCampaign({'name':'IRIS_' + str(int(time.time() * 100000)), 'goalId':constant.irisGenericValues['goalId'], 'objectiveId':constant.irisGenericValues['objectiveId'], 'testControl':{'type' : testControlType.upper(), 'test' : 90}})
        listResponse, listPayload, campaignId = campaignList.createList({'customTagCount':0, 'name':'IRIS_LIST_' + str(int(time.time() * 100000))}, campaignId=campaignResponse['json']['entity']['campaignId'])
        addRecipientResponse, addRecipientPayload = campaignList.addRecipient({'data':userData, 'schema' : 'firstName,lastName,email'}, campaignId, listResponse['json']['entity']['listId'], newUser=False)
        responseCoupon, payloadCoupon, campaignId = coupons.createCoupons(campaignId=campaignId)
        
        groupVersionDetails = dbCallsList.getGroupVersionDetailsWithGroupId(listResponse['json']['entity']['listId'])
        camapignGroupRecipientsData = {'TEST':dbCallsList.getAllUsersFromCampaignGroupRecipient(groupVersionDetails['TEST']['bucket_id'], groupVersionDetails['TEST']['id'])}
        if 'CONTROL' in groupVersionDetails: camapignGroupRecipientsData.update({'CONTROL':dbCallsList.getAllUsersFromCampaignGroupRecipient(groupVersionDetails['CONTROL']['bucket_id'], groupVersionDetails['CONTROL']['id'])})
          
        
        return {
                'campaignName':campaignPayload['name'],
                'campaignId':campaignId,
                'listId':listResponse['json']['entity']['listId'],
                'voucherId':responseCoupon['json']['entity']['voucherSeriesId'],
                'strategy':None,
                'programeId':None,
                'allocationStrategyId':None,
                'expiryStrategyId':None,
                'groupDetails':dbCallsList.getGroupDetailsWithListId(listResponse['json']['entity']['listId']),
                'campaignGroupRecipient':camapignGroupRecipientsData,
                'bucketId':groupVersionDetails['TEST']['bucket_id'],
                'groupVersionResult':groupVersionDetails,
                'groupName':listPayload['name'],
                'addRecipientPayload':addRecipientPayload
                }
    
    @staticmethod
    def preRequisitesForVenenoMobilePush(commChannelType,testControlType='org'):
        singleUserProfile = dbCallsAuthorize.getUserForMobilePush(commChannelType)[0]
        secondUserProfile = dbCallsAuthorize.getUserForMobilePush(commChannelType)[1]
        userData = ['Test,Automation,' + str(singleUserProfile['userId']), 'Test,Automation,' + str(secondUserProfile['userId'])]
        
        if 'storeType' in constant.payload['createmessage'] :constant.payload['createmessage'].pop('storeType')
         
        campaignResponse, campaignPayload = campaigns.createCampaign({'name':'IRIS_' + str(int(time.time() * 100000)), 'goalId':constant.irisGenericValues['goalId'], 'objectiveId':constant.irisGenericValues['objectiveId'], 'testControl':{'type' : testControlType.upper(), 'test' : 90}})
        listResponse, listPayload, campaignId = campaignList.createList({'customTagCount':0, 'name':'IRIS_LIST_' + str(int(time.time() * 100000))}, campaignId=campaignResponse['json']['entity']['campaignId'])
        addRecipientResponse, addRecipientPayload = campaignList.addRecipient({'data':userData, 'schema' : 'firstName,lastName,userId'}, campaignId, listResponse['json']['entity']['listId'], newUser=False)
        responseCoupon, payloadCoupon, campaignId = coupons.createCoupons(campaignId=campaignId)
        
        groupVersionDetails = dbCallsList.getGroupVersionDetailsWithGroupId(listResponse['json']['entity']['listId'])
        camapignGroupRecipientsData = {'TEST':dbCallsList.getAllUsersFromCampaignGroupRecipient(groupVersionDetails['TEST']['bucket_id'], groupVersionDetails['TEST']['id'])}
        if 'CONTROL' in groupVersionDetails: camapignGroupRecipientsData.update({'CONTROL':dbCallsList.getAllUsersFromCampaignGroupRecipient(groupVersionDetails['CONTROL']['bucket_id'], groupVersionDetails['CONTROL']['id'])})
            
        return {
                'campaignName':campaignPayload['name'],
                'campaignId':campaignId,
                'listId':listResponse['json']['entity']['listId'],
                'voucherId':responseCoupon['json']['entity']['voucherSeriesId'],
                'strategy':None,
                'programeId':None,
                'allocationStrategyId':None,
                'expiryStrategyId':None,
                'groupDetails':dbCallsList.getGroupDetailsWithListId(listResponse['json']['entity']['listId']),
                'campaignGroupRecipient':camapignGroupRecipientsData,
                'bucketId':groupVersionDetails['TEST']['bucket_id'],
                'groupVersionResult':groupVersionDetails,
                'groupName':listPayload['name'],
                'addRecipientPayload':addRecipientPayload
                }
        
    @staticmethod
    def preRequisitesForVenenoLine(testControlType='org'):
        userData = []
        for eachUser in constant.config['line']['user']:
            userData.append('Test,Automation,{}'.format(eachUser['userId']))
        campaignResponse, campaignPayload = campaigns.createCampaign({'name':'IRIS_' + str(int(time.time() * 100000)), 'goalId':constant.irisGenericValues['goalId'], 'objectiveId':constant.irisGenericValues['objectiveId'], 'testControl':{'type' : testControlType.upper(), 'test' : 90}})
        listResponse, listPayload, campaignId = campaignList.createList({'customTagCount':0, 'name':'IRIS_LIST_' + str(int(time.time() * 100000))}, campaignId=campaignResponse['json']['entity']['campaignId'])
        addRecipientResponse, addRecipientPayload = campaignList.addRecipient({'data':userData, 'schema' : 'firstName,lastName,userId'}, campaignId, listResponse['json']['entity']['listId'], newUser=False)
        responseCoupon, payloadCoupon, campaignId = coupons.createCoupons(campaignId=campaignId)
        
        return {
                'campaignName':campaignPayload['name'],
                'campaignId':campaignId,
                'listId':listResponse['json']['entity']['listId'],
                'voucherId':responseCoupon['json']['entity']['voucherSeriesId'],
                'strategy':None,
                'programeId':None,
                'allocationStrategyId':None,
                'expiryStrategyId':None,
                'bucketId':dbCallsList.getGroupVersionDetailsWithGroupId(listResponse['json']['entity']['listId'])['TEST']['bucket_id'],
                'groupVersionResult':dbCallsList.getGroupVersionDetailsWithGroupId(listResponse['json']['entity']['listId']),
                'groupName':listPayload['name']
                }
        
    @staticmethod
    def getDefaultArguments(channel='SMS', fieldsToUpdate={}):
        tmpDict = {
            'custom_tag_1' : '{{NA}}',
            'custom_tag_2' : '{{NA}}',
            'custom_tag_3' : '{{NA}}',
            'custom_tag_4' : '{{NA}}',
            'custom_tag_5' : '{{NA}}',
            'custom_tag_6' : '{{NA}}',
            'custom_tag_7' : '{{NA}}',
            'custom_tag_8' : '{{NA}}',
            'custom_tag_9' : '{{NA}}'
        }
        if channel.upper() == 'SMS':
            tmpDict.update({
                "reachability_rules":"UNABLE_TO_VERIFY,VALID,SOFTBOUNCED",
                "sendToNdnc":"false",
                "useTinyUrl":"false",
                "created_by":14783,
                "domain_gateway_map_id":22741,
                "is_list_processed_for_reachability":True,
                "msg_count":"1"
            })
            tmpDict.update(fieldsToUpdate)
        elif channel.upper() == 'EMAIL':
            tmpDict.update({
                "msg_queue_id":"74121",
                "plain_text":"new project  \r\n\r\n\t\tfirst_name [ {{first_name}} ], last_name [ {{last_name}} ],\r\nunsubscribe [ {{unsubscribe}} ]",
                "is_list_processed_for_reachability":False
            })
            tmpDict.update(fieldsToUpdate)
        elif channel.upper() == 'WECHAT':
            tmpDict.update({
                "entity_id":-1,
                "TemplateIds":None,
                "AppId" : constant.config['wechat']['appId'],
                "AppSecret": constant.config['wechat']['appSecret'],
                "ServiceAccoundId" : constant.config['wechat']['OriginalId'],
                "template_id":constant.config['templateId'],
                "summary":"\u60a8\u597d\uff0c\u60a8\u5df2\u8d2d\u4e70\u6210\u529f\u3002\n\n{{productType.DATA}}\uff1a{{name.DATA}}\n\u8d2d\u4e70\u6570\u91cf\uff1a{{number.DATA}}\n\u6709\u6548\u671f\uff1a{{expDate.DATA}}\n{{remark.DATA}}",
                "title":constant.config['templateTitle'],
                "name":constant.config['templateTitle'],
                "image":None,
                "OriginalId" : constant.config['wechat']['OriginalId'],
                "msg_type":"WECHAT_TEMPLATE",
                "is_drag_drop":0,
                "drag_drop_id":None,
                "csrf_token":"RAwns4+sFEMaLP9Qp5qBinkrchEaDW",
                "email_address":"default email address",
                "email_email":"default email email",
                "email_extra":"default email extra",
                "email_land_line":"default email land line",
                "email_mobile":"default email mobile",
                "email_store_name":"default email store name",
                "first_name":"ROBO",
                "fullname":"xxxxxx",
                "last_name":"",
                "sms_address":"default sms address",
                "sms_email":"default sms email",
                "sms_extra":"default sms extra",
                "sms_land_line":"default sms landline",
                "sms_mobile":"default sms mobile",
                "sms_store_name":"default sms store name",
                "store_address":"mgroad, ropenaagarasjdnf",
                "store_email":"default store email",
                "store_external_id":"default store external id1",
                "store_external_id_1":"default store external id2",
                "store_external_id_2":"default store external id3",
                "store_land_line":"default store landline",
                "store_name":"default store name",
                "store_number":"default store number",
                "valid_days_from_create":"default valid days from create",
                "is_list_processed_for_reachability":True
                })
            tmpDict.update(fieldsToUpdate)
        elif channel.upper() == 'CALL_TASK':
            tmpDict = {
                "entity_id":-1,
                "is_drag_drop":0,
                "drag_drop_id":None,
                "custom_tag_1":"{{NA}}",
                "custom_tag_2":"{{NA}}",
                "custom_tag_3":"{{NA}}",
                "custom_tag_4":"{{NA}}",
                "custom_tag_5":"{{NA}}",
                "custom_tag_6":"{{NA}}",
                "custom_tag_7":"{{NA}}",
                "custom_tag_8":"{{NA}}",
                "custom_tag_9":"{{NA}}",
                "is_list_processed_for_reachability":True
                }
            tmpDict.update(fieldsToUpdate)
            return str(tmpDict)
        elif channel.upper() == 'PUSH':
            tmpDict = {
                "entity_id":-1,
                "is_list_processed_for_reachability":True,
                "authToken":"701af5b4-2092-4b42-ad26-330e199a9dc9",
                "licenseCode":"~15ba1da98",
                "variationId":"~dajfno",
                "campaignId":"~dajfno",
                "supported_channels":"android,ios",
                "accountId":"118",
                "template_id":"9418",
                "is_drag_drop":0,
                "drag_drop_id":None,
                "custom_tag_1":"{{NA}}",
                "custom_tag_2":"{{NA}}",
                "custom_tag_3":"{{NA}}",
                "custom_tag_4":"{{NA}}",
                "custom_tag_5":"{{NA}}",
                "custom_tag_6":"{{NA}}",
                "custom_tag_7":"{{NA}}",
                "custom_tag_8":"{{NA}}",
                "custom_tag_9":"{{NA}}",
                "subject":"automation test777"
            }
            tmpDict.update(fieldsToUpdate)
            return str(tmpDict)
        elif channel.upper() == 'LINE':
            tmpDict.update({
                "entity_id":-1,
                "is_list_processed_for_reachability":True,
                "accountId":constant.config['line']['accountId'],
                "sourceAccountId":constant.config['line']['sourceAccountId']
            })
            tmpDict.update(fieldsToUpdate)
            return str(tmpDict)
        elif channel.upper() == 'FACEBOOK':
            tmpDict.update({
                "entity_id":-1,
                "accountId":constant.config['facebook']['accountId']
            })
            tmpDict.update(fieldsToUpdate)
            return str(tmpDict)
        else:
            raise Exception('Unsupported channel Type :{}'.format(channel))
        return json.dumps(tmpDict)

    @staticmethod
    def getMessageProperties(channel='SMS', fieldsToUpdate={}):
        if channel.upper() == 'SMS':
            tmpDict = {
                "admin_user_id": "-1",
                "created_by": "Admin",
                "default_status": "close",
                "expiring_in": "-1",
                "expiry_reminder": "0",
                "is_ndnc_enabled": "false",
                "num_of_attributes": "-1",
                "num_of_recommendations": "-1",
                "recommendation_plan_id": "-1",
                "sender_cdma": "9090909099",
                "sender_email": "",
                "sender_gsm": "9090909091",
                "sender_label": "",
                "sender_reply_to": "",
                "store_type": "registered_store",
                "task_id": "-1",
                "unsubscribe_label": "unsubscribe",
                "voucher_series": "-1"
            }
            tmpDict.update(fieldsToUpdate)
            return str(tmpDict)
        elif channel.upper() == 'EMAIL':
            tmpDict = {
                "admin_user_id": "-1",
                "created_by": "15000449",
                "default_status": "close",
                "expiring_in": "-1",
                "expiry_reminder": "0",
                "num_of_attributes": "-1",
                "num_of_recommendations": "-1",
                "recommendation_plan_id": "-1",
                "sender_cdma": "",
                "sender_email": "automation@capillarytech.com",
                "sender_gsm": "",
                "sender_label": "automation",
                "sender_reply_to": "",
                "store_type": "registered_store",
                "task_id": "-1",
                "unsubscribe_label": "unsubscribe",
                "voucher_series": "-1"
            }
            tmpDict.update(fieldsToUpdate)
            return str(tmpDict)
        elif channel.upper() == 'WECHAT':
            tmpDict = {
                "store_type":"registered_store",
                "created_by":"15000449",
                "voucher_series":"-1",
                "task_id":"-1",
                "default_status":"close",
                "admin_user_id":"-1",
                "unsubscribe_label":"unsubscribe",
                "sender_gsm":"",
                "sender_cdma":"",
                "sender_label":"",
                "sender_reply_to":"",
                "sender_email":"",
                "expiry_reminder":"0",
                "expiring_in":"-1",
                "recommendation_plan_id":"-1",
                "num_of_recommendations":"-1",
                "num_of_attributes":"-1"
            }
            tmpDict.update(fieldsToUpdate)
            return json.dumps(tmpDict)
        elif channel.upper() == 'CALL_TASK':
            tmpDict = {
                "store_type":"registered_store",
                "admin_user_id":"15000449",
                "default_status":"23",
                "created_by":"15000449",
                "voucher_series":"-1",
                "task_id":"893",
                "unsubscribe_label":"unsubscribe",
                "sender_gsm":"",
                "sender_cdma":"",
                "sender_label":"",
                "sender_reply_to":"",
                "sender_email":"",
                "expiry_reminder":"0",
                "expiring_in":"-1",
                "recommendation_plan_id":"-1",
                "num_of_recommendations":"-1",
                "num_of_attributes":"-1"
            }
            tmpDict.update(fieldsToUpdate)
            return str(tmpDict)
        elif channel.upper() == 'PUSH':
            tmpDict = {
                "store_type":"registered_store",
                "created_by":"15000449",
                "voucher_series":"-1",
                "task_id":"-1",
                "default_status":"close",
                "admin_user_id":"-1",
                "unsubscribe_label":"unsubscribe",
                "sender_gsm":"", "sender_cdma":"",
                "sender_label":"", "sender_reply_to":"",
                "sender_email":"", "expiry_reminder":"0",
                "expiring_in":"-1", "recommendation_plan_id":"-1",
                "num_of_recommendations":"-1", "num_of_attributes":"-1"
            }
            tmpDict.update(fieldsToUpdate)
            return str(tmpDict)
        elif channel.upper() == 'LINE':
            tmpDict = {
                "store_type":"registered_store",
                "created_by":"15000449",
                "voucher_series":"-1",
                "task_id":"-1",
                "default_status":"close",
                "admin_user_id":"-1",
                "unsubscribe_label":"unsubscribe",
                "sender_gsm":"", "sender_cdma":"",
                "sender_label":"", "sender_reply_to":"",
                "sender_email":"", "expiry_reminder":"0",
                "expiring_in":"-1", "recommendation_plan_id":"-1",
                "num_of_recommendations":"-1", "num_of_attributes":"-1"
            }
            tmpDict.update(fieldsToUpdate)
            return str(tmpDict)
        elif channel.upper() == 'FACEBOOK':
            tmpDict = {
                "store_type":"registered_store",
                "created_by":"15000449",
                "voucher_series":"-1",
                "task_id":"-1",
                "default_status":"close",
                "admin_user_id":"-1",
                "unsubscribe_label":"unsubscribe",
                "sender_gsm":"", "sender_cdma":"",
                "sender_label":"", "sender_reply_to":"",
                "sender_email":"", "expiry_reminder":"0",
                "expiring_in":"-1", "recommendation_plan_id":"-1",
                "num_of_recommendations":"-1", "num_of_attributes":"-1"
            }
            tmpDict.update(fieldsToUpdate)
            return str(tmpDict)
        else:
            raise Exception('Unsupported channel Type :{}'.format(channel))

    @staticmethod
    def couponConfigChange(self, condition):
        Logger.log('Setting Voucher Resent Config to :{} for voucherId :{}'.format(condition, self.voucherId))
        constant.config['campaignId'] = self.campaignId
        port = constant.config['luciPort'].next()
        connObj = LuciThrift(port)
        constructObj = LuciObject()

        configRequest = LuciObject.getCouponConfigRequest({'couponSeriesId': self.voucherId})
        couponConfigList = connObj.getCouponConfiguration(configRequest)
        couponConfig = couponConfigList[0].__dict__
        couponConfig.update(condition)

        couponConfigObject = LuciObject.couponConfiguration(couponConfig)
        saveCouponConfigObject = LuciObject.saveCouponConfigRequest(couponConfigObject)
        connObj.saveCouponConfiguration(saveCouponConfigObject)

    @staticmethod
    def createCouponLuci(self, condition):
        port = constant.config['luciPort'].next()
        connObj = LuciThrift(port)

        couponConfigObject = LuciObject.couponConfiguration(condition)
        saveCouponConfigObject = LuciObject.saveCouponConfigRequest(couponConfigObject)
        response = connObj.saveCouponConfiguration(saveCouponConfigObject)
        couponConfigObj = response.__dict__
        return couponConfigObj['id']

    @staticmethod
    def preRequisitesForVenenoReply(testControlType='org'):
        if 'storeType' in constant.payload['createmessage']: constant.payload['createmessage'].pop('storeType')

        campaignResponse, campaignPayload = campaigns.createCampaign({'name': 'IRIS_' + str(int(time.time() * 100000)), 'goalId': constant.irisGenericValues['goalId'], 'objectiveId': constant.irisGenericValues['objectiveId'], 'testControl': {'type': testControlType.upper(), 'test': 90}});
        listResponse, listPayload, campaignId = campaignList.createList({'customTagCount': 1, 'name': 'IRIS_LIST_' + str(int(time.time() * 100000))}, campaignId=campaignResponse['json']['entity']['campaignId'])
        addRecipientResponse, addRecipientPayload = campaignList.addRecipient({}, campaignId, listResponse['json']['entity']['listId'], 'mobile,email', 10, 1, newUser=False)
        strategyDict = construct.constructStrategyIds()
        groupVersionDict = dbCallsList.getGroupVersionDetailsWithGroupId(listResponse['json']['entity']['listId'])

        return {'campaignId': campaignId,
                'listId': listResponse['json']['entity']['listId'],
                'strategy': strategyDict,
                'programeId': strategyDict['programeId'],
                'allocationStrategyId': strategyDict['allocationStrategyId'],
                'expiryStrategyId': strategyDict['expirationStrategyId'],
                'bucketId': groupVersionDict['TEST']['bucket_id'],
                'groupVersionResult': groupVersionDict,
                'groupName': listPayload['name']
                }

    @staticmethod
    def constructReplyCampaignDetails(self, replyType, skippedErrors, couponConfigChange):
        try:
            if replyType in ['COUPON_ALREADY_ISSUED', 'MAX_COUPON_ISSUAL_PER_USER_EXCEEDED', 'DAYS_BETWEEN_ISSUAL_LESS_THAN_MIN_DAYS_CONFIGURED','MAX_COUPON_ISSUAL_PER_SERIES_EXCEEDED']:
                VenenoHelper.messageAuthorizeWithoutAssertions(self)
                time.sleep(10)
            communicationDetailsId, communicationDetailBucketId ,communicationDetailExpectedCount= VenenoHelper.messageAuthorize(self, skippedError=skippedErrors, isSkippedMessage=True, couponConfig=couponConfigChange)
            self.Details[replyType].update({'communicationDetailsId': communicationDetailsId, 'communicationDetailBucketId': communicationDetailBucketId, 'communicationDetailExpectedCount':communicationDetailExpectedCount})
        except Exception, exp:
            Logger.log('Failed error Message : ', exp)


    @staticmethod
    def messageAuthorizeWithoutAssertions(self):
        messagePayloadToUpdate = {
            'incentive': {
                'type': 'COUPONS',
                'voucherSeriesId': self.voucherId
            },
            'senderDetails': {
                'domainGatewayMapId': constant.config['message_senders']['domainGatewayMapId'],
                'gsmSenderId': constant.config['message_senders']['gsmSenderId'],
                'useSystemDefaults': False,
                'cdmaSenderId': constant.config['message_senders']['cdmaSenderId']
            },
            'message': 'This Message is Going to Skip Due to Coupon issuable : {{voucher}} {{optout}}'
        }

        messageResponse, messagePayload = campaignMessage.createMessage(self, payloadData=messagePayloadToUpdate)
        authorize.makeAuthorizeRequest(self.campaignId, messageResponse['json']['entity']['messageId'])

    @staticmethod
    def messageAuthorize(self, skippedError=[], isSkippedMessage=False, couponConfig=None):
        if couponConfig is not None:
            VenenoHelper.couponConfigChange(self, couponConfig)
        messagePayloadToUpdate = {
            'incentive': {
                'type': 'COUPONS',
                'voucherSeriesId': self.voucherId
            },
            'senderDetails': {
                'domainGatewayMapId': constant.config['message_senders']['domainGatewayMapId'],
                'gsmSenderId': constant.config['message_senders']['gsmSenderId'],
                'useSystemDefaults': False,
                'cdmaSenderId': constant.config['message_senders']['cdmaSenderId']
            },
            'message': 'This Message is Going to Skip Due to Coupon issuable : {{voucher}} {{optout}}'
        }

        messageResponse, messagePayload = campaignMessage.createMessage(self, payloadData=messagePayloadToUpdate)
        authorizeResponse = authorize.makeAuthorizeRequest(self.campaignId, messageResponse['json']['entity']['messageId'])
        authorizeResult = VenenoHelper.getAuthorizeResultBody(self.campaignId, self.listId, self.groupVersionResult, self.bucketId, self.voucherId, self.strategy, messagePayload, str(messageResponse['json']['entity']['messageId']), authorizeResponse)
        if not isSkippedMessage:
            communicationDetailId ,communicationDetailBucketId ,communicationDetailExpectedCount=authorize.assertMessageQueueAndGetCommunicationDetailsForReferenceMessageQueueId(self.campaignId,self.groupVersionResult['TEST']['id'],authorizeResult['messageId'])
            VenenoDBAssertion(self.campaignId, 'SMS', communicationDetailId, self.groupVersionResult['TEST']['customer_count'], self.groupVersionResult['TEST']['id'], authorizeResult['payload']['message'], testControlType=self.testControlType).check()
            authorize.assertUserPresenceInNsAdminTable(communicationDetailId , communicationDetailBucketId, int(communicationDetailExpectedCount))
        else:
            communicationDetailId ,communicationDetailBucketId, communicationDetailExpectedCount=authorize.assertMessageQueueAndGetCommunicationDetailsForReferenceMessageQueueId(self.campaignId,self.groupVersionResult['TEST']['id'],authorizeResult['messageId'])
            VenenoDBAssertion(self.campaignId, 'SMS', communicationDetailId, self.groupVersionResult['TEST']['customer_count'], self.groupVersionResult['TEST']['id'], authorizeResult['payload']['message'],skippedReasons=[skippedError[1]], testControlType=self.testControlType).check()
            authorize.assertUserPresenceInSkippedTable(communicationDetailId, communicationDetailBucketId, constant.config['skipped_errors'][skippedError[0]], skippedError[1])
        return communicationDetailId ,communicationDetailBucketId, communicationDetailExpectedCount

    @staticmethod
    def getAuthorizeResultBody(campaignId, listId, groupVersionResult, bucketId, voucherId, strategy, messagePayload, messageId, authorizeResponse, messageInfo=['SMS', ['IMMEDIATE'], ['PLAIN'], True]):
        return {
            'campaignId':campaignId,
            'listId':listId,
            'groupVersionResult':groupVersionResult ,
            'bucketId':bucketId,
            'voucherId':voucherId,
            'strategy':strategy,
            'messageInfo':messageInfo,
            'payload':messagePayload,
            'messageId':messageId,
            'authorizeResponse':authorizeResponse
        }

    @staticmethod
    def configRateLimit(enable, channel):
        Logger.log('Request to enable :{} RateLimit'.format(enable))
        try:
            dbCallsAuthorize.configRateLimit(enable, channel)
        except Exception, exp:
            raise Exception('Exception Occured while Disbaling RateLimt :{}'.format(exp))
            dbCallsAuthorize.configRateLimit(False, channel)
        
    @staticmethod
    def setupStrategy(daily=None, weekly=None, monthly=None , channel='SMS'):
        Logger.log('Setting up Strategy with Daily :{} , weekly :{} and monthly :{}'.format(daily, weekly, monthly))
        if daily is not None:
            dbCallsAuthorize.setupStrategy(daily=daily, channel=channel)
        if weekly is not None:
            dbCallsAuthorize.setupStrategy(weekly=weekly, channel=channel)
        if monthly is not None:
            dbCallsAuthorize.setupStrategy(monthly=monthly, channel=channel)
        
    @staticmethod
    def authorizeForRateLimit(self, listType):
        messageResponse, messagePayload = campaignMessage.createMessage(self, messageInfo=['SMS', ['IMMEDIATE'], ['PLAIN'], True])
        authorizeResponse = authorize.makeAuthorizeRequest(str(self.testObjectForRateLimit['campaign']['id']), str(messageResponse['json']['entity']['messageId']))
        return {
            'campaignId':self.testObjectForRateLimit['campaign']['id'],
            'listId':self.testObjectForRateLimit['list'][listType]['groupDetails']['id'],
            'groupVersionResult':self.testObjectForRateLimit['list'][listType]['groupVersionDetails'] ,
            'bucketId':self.testObjectForRateLimit['list'][listType]['groupVersionDetails']['TEST']['bucket_id'],
            'voucherId':None,
            'strategy':None,
            'messageInfo':['SMS', ['IMMEDIATE'], ['PLAIN'], True],
            'payload':messagePayload,
            'messageId':str(messageResponse['json']['entity']['messageId']),
            'authorizeResponse':authorizeResponse
            }
        
    @staticmethod
    def updateWindowValueToByPassStrategy(userIds, strategy, channel='SMS'):
        strategyId = dbCallsAuthorize.getStrategyId(strategy, channel)
        dbCallsAuthorize.updateWindowValueToByPassStrategy(tuple(userIds), strategyId)
        
    @staticmethod
    def updateEmailStatus(listObject):
        nsObj = NSAdminHelper.getConnObj()
        for eachList in listObject:
            allusersInList = [eachUser.split(',')[2] for eachUser in listObject[eachList]['addRecipientPayload']['data']]
            if not nsObj.whitelistEmailIds(allusersInList):
                raise Exception("Not Able To Whitelist New Created users ")
 
    @staticmethod
    def getCommunicationBucketId(communicationId):
        return dbCallsAuthorize.getCommunicationDetailsWithId(communicationId)['bucket_id']        

    @staticmethod
    def getCommunicationGroupId(communicationId):
        return dbCallsAuthorize.getCommunicationDetailsWithId(communicationId)['recipient_list_id']

    @staticmethod
    def updateStartegyForRateLimit():
        dbCallsAuthorize.updateStartegyForRateLimit()
        