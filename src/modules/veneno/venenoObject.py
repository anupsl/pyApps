from src.Constant.constant import constant
from src.initializer.generateThrift import veneno
from src.utilities.utils import Utils
from src.modules.veneno.venenoHelper import VenenoHelper
import uuid, time

class VenenoObject(object):
    def __init__(self):
        self.CommunicationType = {
            'SMS': 1,
            'EMAIL' : 2,
            'CALL_TASK' : 3,
            'WECHAT' : 4,
            'PUSH' : 5,
            'ANDROID' : 6,
            'IOS' : 7,
            'FACEBOOK' : 8,
            'GOOGLE' : 9,
            'TWITTER' :10,
            'LINE' : 11	
        }    
        self.TargetType = {
            'GROUPED' : 1,
            'TIMELINE' : 2,
            'EXPIRY_REMINDER' : 3,
            'SOCIAL' : 4
        }
        
    @staticmethod
    def communicationDetail(messageDetails={}, extraParams={}):
        tmpDict = {
            'orgId' : constant.config['orgId'],
            'guid' : Utils.generateGUID(),
            'subject' : 'Veneno Thrift Automation',
            'body' : 'Thirft Created Automation Test Body {{optout}}',
            'priority' : 2,
            'defaultArguments' : '',
            'messageProperties' : '',
            'communicationType' : 'EMAIL',
            'targetType' : 'GROUPED',
            'message_queue_id':0,
            'receivedTime' : str(Utils.getTime(milliSeconds=True)),
            'lastUpdatedBy':int(constant.config['userId'])
        }
        messageExtraUpdate = {}
        defaultExtraParam = {}
        
        if extraParams != {}:
            if 'voucher_series' in extraParams: messageExtraUpdate.update({'voucher_series':extraParams['voucher_series']})
            if 'default_argument' in extraParams :defaultExtraParam.update(extraParams['default_argument'])
            
        tmpDict.update(messageDetails)
        venObj = VenenoObject()
        tmpDict['defaultArguments'] = VenenoHelper.getDefaultArguments(channel=tmpDict['communicationType'], fieldsToUpdate=defaultExtraParam)
        tmpDict['messageProperties'] = VenenoHelper.getMessageProperties(channel=tmpDict['communicationType'], fieldsToUpdate=messageExtraUpdate)
        tmpDict['communicationType'] = venObj.CommunicationType[tmpDict['communicationType']]
        tmpDict['targetType'] = venObj.TargetType[tmpDict['targetType']]
        return veneno.CommunicationDetail(**tmpDict)

    @staticmethod
    def emailBody(emailBodyDict={}):
        tmpDict = {
        'body' : 'test body',
        'orgId' : constant.config['orgId'],
        'createdTime' : str(Utils.getTime()),
        'retrievedTime' : str(Utils.getTime()),
        'subject' : 'test subject'
        }
        tmpDict.update(emailBodyDict)
        return veneno.EmailBody(**tmpDict)
