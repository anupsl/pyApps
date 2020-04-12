import pytest, time, sys, unicodedata
from src.Constant.constant import constant
from src.utilities.logger import Logger
from src.utilities.assertion import Assertion
from src.modules.iris.construct import construct
from src.modules.iris.message import campaignMessage
from src.modules.veneno.venenoObject import VenenoObject
from src.modules.veneno.venenoHelper import VenenoHelper
from src.modules.veneno.venenoDBAssertion import VenenoDBAssertion
from src.utilities.randValues import randValues

@pytest.mark.run(order=4)
class Test_VenenoThrift_CUSTOM():
    
    def setup_class(self):
        Logger.logSuiteName(str(self).split('.')[-1])
        self.details = VenenoHelper.preRequisitesForVeneno(testControlType='custom')
        
    def setup_method(self, method):
        self.connObj = VenenoHelper.getConnObj(newConnection=True)
        Logger.logMethodName(method.__name__)

    def test_venenoThrift_inboxUser_Email_Sanity(self):
        cdDetailsBody = {
             'campaignId':self.details['campaignId'],
             'communicationType':'EMAIL',
             'subject':'Automation Generated Body {{unsubscribe}}',
             'recipientListId':self.details['groupVersionResult']['TEST']['id'],
             'overallRecipientCount':self.details['groupVersionResult']['TEST']['customer_count'],
             'expectedDeliveryCount':self.details['groupVersionResult']['TEST']['customer_count'],
             'groupName':self.details['groupName']
            }
        communicationDetailObject = VenenoObject.communicationDetail(cdDetailsBody)
        communicationId = self.connObj.addMessageForRecipients(communicationDetailObject)
        VenenoDBAssertion(cdDetailsBody['campaignId'], cdDetailsBody['communicationType'], communicationId, cdDetailsBody['overallRecipientCount'], cdDetailsBody['recipientListId'], cdDetailsBody['subject'], testControlType='custom').check()

    def test_venenoThrift_inboxUser_Email_GenericTags(self):
        cdDetailsBody = {'campaignId':self.details['campaignId'],
             'communicationType':'EMAIL',
             'subject':'Automation Generated Body {{first_name}} {{last_name}} {{fullname}} {{unsubscribe}}',
             'recipientListId':self.details['groupVersionResult']['TEST']['id'],
             'overallRecipientCount':self.details['groupVersionResult']['TEST']['customer_count'],
             'expectedDeliveryCount':self.details['groupVersionResult']['TEST']['customer_count'],
             'groupName':self.details['groupName']
            }
        communicationDetailObject = VenenoObject.communicationDetail(cdDetailsBody)
        communicationId = self.connObj.addMessageForRecipients(communicationDetailObject)
        VenenoDBAssertion(cdDetailsBody['campaignId'], cdDetailsBody['communicationType'], communicationId, cdDetailsBody['overallRecipientCount'], cdDetailsBody['recipientListId'], cdDetailsBody['subject'], testControlType='custom').check()
    
    def test_venenoThrift_skippeduser_Email_pointsMessageConfiguredError(self):
        cdDetailsBody = {'campaignId':self.details['campaignId'],
             'communicationType':'EMAIL',
             'subject':'Automation Generated Body {{first_name}} {{last_name}} {{fullname}} {{promotion_points}} {{unsubscribe}}',
             'recipientListId':self.details['groupVersionResult']['TEST']['id'],
             'overallRecipientCount':self.details['groupVersionResult']['TEST']['customer_count'],
             'expectedDeliveryCount':self.details['groupVersionResult']['TEST']['customer_count'],
             'groupName':self.details['groupName']
            }
        extraDefaultPrams = {
            "default_argument":{
                "drag_drop_id": None,
                "entity_id":-1,
                "expiry_strategy_id": "7496",
                "is_drag_drop": 0,
                "is_list_processed_for_reachability": True,
                "msg_count": "1",
                "program_id": "1215",
                "promotion_id": 8616,
                "reachability_rules": "UNABLE_TO_VERIFY,VALID,SOFTBOUNCED",
                "sendToNdnc": "false",
                "till_id": "50012200",
                "useTinyUrl": "false"
                }
            }
        communicationDetailObject = VenenoObject.communicationDetail(cdDetailsBody, extraParams=extraDefaultPrams)
        communicationId = self.connObj.addMessageForRecipients(communicationDetailObject)
        VenenoDBAssertion(cdDetailsBody['campaignId'], cdDetailsBody['communicationType'], communicationId, cdDetailsBody['overallRecipientCount'], cdDetailsBody['recipientListId'], cdDetailsBody['subject'], testControlType='custom', skippedReasons=['Message is not configured properly and is missing points related properties']).check()
          
    @pytest.mark.skipif(constant.config['cluster'] not in ['nightly', 'china'], reason='Wechat Configured only in nightly')
    def est_venenoThrift_inboxUser_WeChat_Sanity(self):
        actualOrgId = construct.updateOrgId(constant.config['wechat']['orgId'])
        actualOrgName = construct.updateOrgName(constant.config['wechat']['orgName'])
        try:
            details = VenenoHelper.preRequisitesForVenenoWechat(testControlType='custom')
            campaignMessage.getWeCRMTemplates()
            subject = {
                "template_id" : unicodedata.normalize('NFKD', constant.config['templateId']).encode('ascii', 'ignore'),
                "touser" : "{{wechat_open_id}}",
                "OriginalId" : constant.config['wechat']['OriginalId'],
                "Title" : "",
                "BrandId" : "f",
                "url" : "http://we.capillarytech-cn.com/web?appid=wxc7bf989decc7e35b&redirect_uri=http://somelink.com/someword?nowAParam=firstParam&second=second.Param&response_type=code&scope=snsapi_base&state=STATE",
                "TopColor" : "#000000",
                "data" : {"productType": {"value": "HakeemProduct", "color": "#00000"}, "name": {"value": "Hakeem {{first_name}} Lukka", "color": "#00000"}, "number": {"value": "898767 skdjnjn", "color": "#00000"}, "expDate": {"value": "look down", "color": "#00000"}, "remark": { "value": "Look up", "color": "#00000"}}
            }
            cdDetailsBody = {
                 'campaignId':details['campaignId'],
                 'communicationType':'WECHAT',
                 'subject': str(subject),
                 'body': 'Thrift Created Automation Wechat Body',
                 'recipientListId':details['groupVersionResult']['TEST']['id'],
                 'overallRecipientCount':details['groupVersionResult']['TEST']['customer_count'],
                 'expectedDeliveryCount':details['groupVersionResult']['TEST']['customer_count'],
                 'groupName':details['groupName']
                }
            communicationDetailObject = VenenoObject.communicationDetail(cdDetailsBody)
            communicationId = self.connObj.addMessageForRecipients(communicationDetailObject)
            VenenoDBAssertion(cdDetailsBody['campaignId'], cdDetailsBody['communicationType'], communicationId, cdDetailsBody['overallRecipientCount'], cdDetailsBody['recipientListId'], cdDetailsBody['subject'], testControlType='custom', skippedReasons=['Captured OpenId for user seems to be unsubscribed']).check()
        except Exception, exp:
            raise Exception('Wechat Case Failed due to :{}'.format(exp))
        finally:
            construct.updateOrgId(actualOrgId)
            construct.updateOrgName(actualOrgName)
    
    def test_venenoThrift_inboxUser_CallTask_Sanity(self):
        cdDetailsBody = {
             'campaignId':self.details['campaignId'],
             'communicationType':'CALL_TASK',
             'subject':'Automation Generated Body {{first_name}} {{last_name}} {{fullname}} {{optout}}',
             'recipientListId':self.details['groupVersionResult']['TEST']['id'],
             'overallRecipientCount':self.details['groupVersionResult']['TEST']['customer_count'],
             'expectedDeliveryCount':self.details['groupVersionResult']['TEST']['customer_count'],
             'groupName':self.details['groupName']
            }
        communicationDetailObject = VenenoObject.communicationDetail(cdDetailsBody)
        communicationId = self.connObj.addMessageForRecipients(communicationDetailObject)
        VenenoDBAssertion(cdDetailsBody['campaignId'], cdDetailsBody['communicationType'], communicationId, cdDetailsBody['overallRecipientCount'], cdDetailsBody['recipientListId'], cdDetailsBody['subject'], testControlType='custom').check()

    def test_venenoThrift_skippedUser_CallTask(self):
        cdDetailsBody = {
             'campaignId':self.details['campaignId'],
             'communicationType':'CALL_TASK',
             'subject':'Automation Generated Body {{first_name}} {{last_name}} {{fullname}} {{custom_tag_2}} {{optout}}',
             'recipientListId':self.details['groupVersionResult']['TEST']['id'],
             'overallRecipientCount':self.details['groupVersionResult']['TEST']['customer_count'],
             'expectedDeliveryCount':self.details['groupVersionResult']['TEST']['customer_count'],
             'groupName':self.details['groupName']
            }
        communicationDetailObject = VenenoObject.communicationDetail(cdDetailsBody)
        communicationId = self.connObj.addMessageForRecipients(communicationDetailObject)
        VenenoDBAssertion(cdDetailsBody['campaignId'], cdDetailsBody['communicationType'], communicationId, cdDetailsBody['overallRecipientCount'], cdDetailsBody['recipientListId'], cdDetailsBody['subject'], testControlType='custom', skippedReasons=['Custom Tag Not Present']).check()

    @pytest.mark.skipif(constant.config['cluster'] not in ['nightly'], reason='Mobilepush Configured only in nightly')
    def est_venenoThrift_inboxUser_MobilePush_Android_Sanity(self):
        actualOrgId = construct.updateOrgId(constant.config['mobilepush']['orgId'])
        actualOrgName = construct.updateOrgName(constant.config['mobilepush']['orgName'])
        try:
            details = VenenoHelper.preRequisitesForVenenoMobilePush('android',testControlType='custom')
    
            cdDetailsBody = {
                 'campaignId':details['campaignId'],
                 'communicationType':'PUSH',
                 'subject':'Automation Generated Body',
                 'body':'{"templateData":{"ANDROID":{"luid":"{{luid}}","cuid":"{{cuid}}","communicationId":"{{communicationId}}","title":"asas","message":"asasas","expandableDetails":{"style":"BIG_TEXT","message":"asasas"},"custom":[]}}}',
                 'recipientListId':details['groupVersionResult']['TEST']['id'],
                 'overallRecipientCount':details['groupVersionResult']['TEST']['customer_count'],
                 'expectedDeliveryCount':details['groupVersionResult']['TEST']['customer_count'],
                 'groupName':details['groupName']
                }
            communicationDetailObject = VenenoObject.communicationDetail(cdDetailsBody)
            communicationId = self.connObj.addMessageForRecipients(communicationDetailObject)
            VenenoDBAssertion(cdDetailsBody['campaignId'], cdDetailsBody['communicationType'], communicationId, cdDetailsBody['overallRecipientCount'], cdDetailsBody['recipientListId'], cdDetailsBody['subject'], testControlType='custom').check()
        except Exception, exp:
            raise Exception('MobilePush Failure ,due to :{}'.format(exp))
        finally:
            construct.updateOrgId(actualOrgId)
            construct.updateOrgName(actualOrgName)
    
    @pytest.mark.skipif(constant.config['cluster'] not in ['nightly'], reason='Wechat Configured only in nightly')   
    def est_venenoThrift_inboxUser_MobilePush_IOS(self):
        actualOrgId = construct.updateOrgId(constant.config['mobilepush']['orgId'])
        actualOrgName = construct.updateOrgName(constant.config['mobilepush']['orgName'])
        try:
            details = VenenoHelper.preRequisitesForVenenoMobilePush('ios',testControlType='custom')
    
            cdDetailsBody = {
                 'campaignId':details['campaignId'],
                 'communicationType':'PUSH',
                 'subject':'Automation Generated Body ',
                 'body':'{"templateData":{"ANDROID":{"luid":"{{luid}}","cuid":"{{cuid}}","communicationId":"{{communicationId}}","title":"hi {{first_name}}","message":"{{first_name}}","expandableDetails":{"style":"BIG_TEXT","message":"{{first_name}}"},"custom":[]},"IOS":{"luid":"{{luid}}","cuid":"{{cuid}}","communicationId":"{{communicationId}}","title":"hi {{first_name}}","message":"{{first_name}}","expandableDetails":{"style":"BIG_TEXT","message":"hi {{first_name}}","ctas":[]},"custom":[]}}}',
                 'recipientListId':details['groupVersionResult']['TEST']['id'],
                 'overallRecipientCount':details['groupVersionResult']['TEST']['customer_count'],
                 'expectedDeliveryCount':details['groupVersionResult']['TEST']['customer_count'],
                 'groupName':details['groupName']
                }
            communicationDetailObject = VenenoObject.communicationDetail(cdDetailsBody)
            communicationId = self.connObj.addMessageForRecipients(communicationDetailObject)
            VenenoDBAssertion(cdDetailsBody['campaignId'], cdDetailsBody['communicationType'], communicationId, cdDetailsBody['overallRecipientCount'], cdDetailsBody['recipientListId'], cdDetailsBody['subject'], testControlType='custom').check()
        except Exception, exp:
            raise Exception('MobilePush Failure ,due to :{}'.format(exp))
        finally:
            construct.updateOrgId(actualOrgId)
            construct.updateOrgName(actualOrgName)
            
    def test_venenoThrift_inboxUser_Line_Sanity(self):
        actualOrgId = construct.updateOrgId(constant.config['line']['orgId'])
        actualOrgName = construct.updateOrgName(constant.config['line']['orgName'])
        try:
            details = VenenoHelper.preRequisitesForVenenoLine(testControlType='custom')
            cdDetailsBody = {
                 'campaignId':details['campaignId'],
                 'communicationType':'LINE',
                 'subject':'{"to":"{{line_id}}","messages":[{"type":"text","text":"Automated Call {{user_id_b64}}"}]}',
                 'body':'',
                 'recipientListId':details['groupVersionResult']['TEST']['id'],
                 'overallRecipientCount':details['groupVersionResult']['TEST']['customer_count'],
                 'expectedDeliveryCount':details['groupVersionResult']['TEST']['customer_count'],
                 'groupName':details['groupName']
                }
            communicationDetailObject = VenenoObject.communicationDetail(cdDetailsBody)
            communicationId = self.connObj.addMessageForRecipients(communicationDetailObject)
            VenenoDBAssertion(cdDetailsBody['campaignId'], cdDetailsBody['communicationType'], communicationId, cdDetailsBody['overallRecipientCount'], cdDetailsBody['recipientListId'], cdDetailsBody['subject'], testControlType='custom').check()
        except Exception, exp:
            raise Exception('Line Failure ,due to :{}'.format(exp))
        finally:
            construct.updateOrgId(actualOrgId)
            construct.updateOrgName(actualOrgName)
