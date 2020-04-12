import os
from src.Constant.payload import payload
from src.Constant.iris_messageBody import iris_messageBody

class irisConstant(payload, iris_messageBody):
    rootPath = os.getcwd()
    userFileMobile = rootPath + '/src/csvFiles/user_mobile.csv'
    userFileEmail = rootPath + '/src/csvFiles/user_mobile.csv'
    userFileUserId = rootPath + '/src/csvFiles/user_userID.csv'    

    irisDetails = {
        'nightly' : {
            'wechat_org_id':780,
            'strict_org_id':1346,
            'strict_campaign_id': 300645,
            'message_recurring': {
                'SMS':{
                    'listId':21949  ,
                    'campaignId':303459,
                    'voucherId' :126644
                },
                'WECHAT':{
                    'listId':33896,
                    'campaignId':306724,
                    'voucherId' :128682
                }
            },
            'authentication' :{
                'concept': {'username':'c1@capillarytech.com', 'password':'KP4qutX?7`'},
                'store':{'username':'s1@capillarytech.com', 'password':'j#E=ges?fRNp9'},
                'zone':{'username':'z1@capillarytech.com', 'password':'j#E=ges?fRNp9'},
                'admin':{'username':'ashish', 'password':123}
            }        
        },
        'staging' : {
            'wechat_org_id':0,
            'strict_org_id':522,
            'strict_campaign_id':252135,
            'message_recurring': {
                'SMS' : {
                    'listId': 5804,
                    'campaignId': 252348,
                    'voucherId': 14510
                },
                'WECHAT': {
                    'listId': 0,
                    'campaignId': 0,
                    'voucherId': 0
                }
            },
            'authentication' :{
                'concept': {'username':'c1@capillarytech.com', 'password':'j#E=ges?fRNp9'},
                'store':{'username':'s1@capillarytech.com', 'password':'j#E=ges?fRNp9'},
                'zone':{'username':'z1@capillarytech.com', 'password':'j#E=ges?fRNp9'},
                'admin':{'username':'first_user@capillarytech.com', 'password': '123'}
            }
        },
        'india' : {
            'wechat_org_id':0,
            'strict_org_id':1346,
            'strict_campaign_id': 300645,
            'message_recurring': {
                'SMS' : {
                    'listId': 62386,
                    'campaignId': 66713,
                    'voucherId': 25445
                },
                'WECHAT' : {
                    'listId': 0,
                    'campaignId': 0,
                    'voucherId': 0
                }
            },
            'authentication' :{
                'concept': {'username':'c1@capillarytech.com', 'password':123},
                'store':{'username':'s1@capillarytech.com', 'password':123},
                'zone':{'username':'z1@capillarytech.com', 'password':123},
                'till':{'username':'t1@capillarytech.com', 'password':123}
            }
        },
        'more' : {
                'wechat_org_id':0,
                'strict_org_id':1346,
                'strict_campaign_id': 300645,
                'message_recurring': {
                    'SMS' : {
                        'listId': 88991,
                        'campaignId': 41786,
                        'voucherId': 9355
                    },
                    'WECHAT' : {
                        'listId': 0,
                        'campaignId': 0,
                        'voucherId': 0
                    }
                },
                'authentication' :{
                    'concept': {'username':'c1@capillarytech.com', 'password':123},
                    'store':{'username':'s1@capillarytech.com', 'password':123},
                    'zone':{'username':'z1@capillarytech.com', 'password':123},
                    'till':{'username':'t1@capillarytech.com', 'password':123}
                }
        },
        'eu' : {
            'wechat_org_id':0,
            'strict_org_id':1346,
            'strict_campaign_id': 300645,
            'message_recurring': {
                'SMS' : {
                    'listId': 33381,
                    'campaignId': 16911,
                    'voucherId': 7620
                },
                'WECHAT' : {
                    'listId': 0,
                    'campaignId': 0,
                    'voucherId': 0
                }
            },
            'authentication' :{
                'concept': {'username':'c1@capillarytech.com', 'password':123},
                'store':{'username':'s1@capillarytech.com', 'password':123},
                'zone':{'username':'z1@capillarytech.com', 'password':123},
                'till':{'username':'t1@capillarytech.com', 'password':123}
            }
        },
        'china' : {
            'wechat_org_id':0,
            'strict_org_id':1346,
            'strict_campaign_id': 300645,
            'message_recurring': {
                'SMS' : {
                    'listId': 4578,
                    'campaignId': 4039,
                    'voucherId': 1999
                },
                'WECHAT' : {
                    'listId': 0,
                    'campaignId': 0,
                    'voucherId': 0
                }
            },
            'authentication' :{
                'concept': {'username':'c1@capillarytech.com', 'password':123},
                'store':{'username':'s1@capillarytech.com', 'password':123},
                'zone':{'username':'z1@capillarytech.com', 'password':123},
                'till':{'username':'t1@capillarytech.com', 'password':123}
            }
        },
        'local' : {
            'wechat_org_id':0,
            'strict_org_id':1346,
            'strict_campaign_id': 300645,
            'message_recurring': {
                'SMS':{
                    'listId':0,
                    'campaignId':0,
                    'voucherId' :0
                },
                'WECHAT':{
                    'listId':0,
                    'campaignId':0,
                    'voucherId' :0
                }
            },
            'authentication' :{
                'concept': {'username':'c1@capillarytech.com', 'password':123},
                'store':{'username':'s1@capillarytech.com', 'password':123},
                'zone':{'username':'z1@capillarytech.com', 'password':123},
                'admin':{'username':'ashish', 'password':123}
            }        
        }
    }