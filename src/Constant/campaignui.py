import time

class campaignuiConstant():
    
    campaignuiUserInfo = {}
    timelineDetails = {
        'nightly':{
            'timelineEndTime': "23:00",
            'templateName':'timeline_sms_automationUsed',
            'templateNameCoupon':'timeline_sms_coupon_automationUsed',
            'templateNamePoints':'timeline_point_SMS_automationUsed',
            'segment': 'test_list_ORG_1539078396'
            },
        'staging':{
            'timelineEndTime': "21:00",
            'templateName':'timeline_sms_automationUsed',
            'templateNameCoupon':'timeline_sms_coupon_automationUsed',
            'templateNamePoints':'timeline_point_SMS_automationUsed',
            'segment': 'TestAndControl'
            },
        'india':{
            'timelineEndTime': "23:00",
            'templateName':'timeline_sms_automationUsed',
            'templateNameCoupon':'timeline_sms_coupon_automationUsed',
            'templateNamePoints':'timeline_point_SMS_automationUsed',
            'segment': 'testAndControlv5'
            },
        'more':{
            'timelineEndTime': "23:00",
            'templateName':'timeline_sms_automationUsed',
            'templateNameCoupon':'timeline_sms_coupon_automationUsed',
            'templateNamePoints':'timeline_point_SMS_automationUsed',
            'segment': 'testAndControlv5'
            },
        'eu':{
            'timelineEndTime': "23:00",
            'templateName':'timeline_sms_automationUsed',
            'templateNameCoupon':'timeline_sms_coupon_automationUsed',
            'templateNamePoints':'timeline_point_SMS_automationUsed',
            'segment': 'TestAndControlV2'
            },
        'china':{
            'timelineEndTime': "21:00",
            'templateName':'timeline_sms_automationUsed',
            'templateNameCoupon':'timeline_sms_coupon_automationUsed',
            'templateNamePoints':'timeline_point_SMS_automationUsed',
            'segment': 'TestAndControl'
            }           
        }
    
    campaignuiDetails = {
            'campaign':{
                    'name': None,
                    'id':-1
                },
            'incentives':{
                    'coupon':{
                        'name': None
                        },
                    'point':{
                        'strategy': None,
                        'id':-1
                        }
                },
            'list':{
                    'loyalty': {
                            'name': 'LoyaltyList' + str(int(time.time())),
                            'id':-1
                        },
                    'nonloyalty': {
                            'name': 'NonLoyaltyList' + str(int(time.time())),
                            'id':-1
                        },
                    'upload': {
                            'name': 'UploadList' + str(int(time.time())),
                            'id':-1
                        },
                    'paste': {
                            'name': 'PasteList' + str(int(time.time())),
                            'id':-1
                        },
                },
            'templateName':{
                'sms':{
                    'nodeal':  'smsnoDealTemplate',
                    'coupon': 'smscouponAutomationTemplate',
                    'point' : 'smspointAutomationTemplate',
                    'generic': 'smsnoDealTemplate'
                    },
                'email':{
                    'nodeal':  'emailnoDealTemplate',
                    'coupon': 'emailcouponAutomationTemplate',
                    'point' : 'emailpointAutomationTemplate',
                    'generic': 'emailnoDealTemplate'
                    },
                'mobilepush':{
                    'android': 'nodealPushCommonTemplateAutomation',
                    'ios':'nodealPushCommonTemplateAutomation'
                    }            
                }
                         
        }
