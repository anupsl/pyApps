import time
from src.Constant.constant import constant
from src.initializer.generateThrift import nsadmin



class NSAdminObject(object):

    MessageClass = {'SMS' : 0, 'EMAIL' : 1, 'WECHAT' : 2, 'ANDROID' : 3, 
                'IOS' : 4, 'VOICECALL' : 5, 'LINE' : 6}

    @staticmethod
    def message(msgDict):
        tmpDict = {'inboxId': 1, 'messageId': 1, 'sender': 'NSADMINTEST', 'clientId': 111,
                    'receiverId':111, 'campaignId': 845015, 'sendingOrgId' :  1604}
        additionalheaders = {'domain_prop_id': '2637'}
        tmpDict['additionalHeaders'] = additionalheaders
        tmpDict.update(msgDict)
        if not 'scheduledTimestamp' in msgDict:
            tmpDict['scheduledTimestamp']=int(time.time())*1000
        return nsadmin.Message(**tmpDict)

    @staticmethod
    def contactInfo(requestDict):
        tmpDict = {'orgId' : constant.config['orgId'], 'messageClass' : 'SMS', 'type' : '',
                   'label' : '', 'value' : '' , 'description' : ''}
        tmpDict.update(requestDict)
        return nsadmin.ContactInfo(**tmpDict)

    @staticmethod
    def domainProperties(requestDict):
        tmpDict = { 'orgId' : constant.config['orgId'], 'domainName' : '',
                    'description' : 'NsAdmin Test Domain'}
        tmpDict.update(requestDict)
        return nsadmin.DomainProperties(**tmpDict)

    @staticmethod
    def gatewayOrgConfigs(requestDict):
        tmpDict = {
            "channelCount": 1,
            "status": "ACTIVE",
            "statusCheckType": "PUSH",
            "startTimestamp": int(time.time() - 7200)*1000,
            "endTimestamp" : int(time.time() + 18000)*1000
        }
        tmpDict.update(requestDict)
        return nsadmin.GatewayOrgConfigs(**tmpDict)

    @staticmethod
    def domainPropertiesGatewayMap(requestDict):
        tmpDict = {
            "addedBy" : 1,
            "addedOn" : 1,
            "useSystemDefaults" : 0,
            "isValidated" : 1,
            "priority" : 1,
            "isActive" : 1
        }
        tmpDict.update(requestDict)
        return nsadmin.DomainPropertiesGatewayMap(**tmpDict) 


    @staticmethod
    def OrgCreditDetails(requestDict):
        tmpDict = {
            "orgId": constant.config['orgId'],
            "addedBy": 4,
            "lastUpdatedBy": 4,
            "lastUpdatedAtTimestamp" : int(time.time())*1000
        }
        tmpDict.update(requestDict)
        return nsadmin.OrgCreditDetails(**tmpDict)      