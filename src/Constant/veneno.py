
class Veneno():
    listOfReplyMessage = ['COUPON_ALREADY_ISSUED', 'MAX_COUPON_ISSUAL_PER_USER_EXCEEDED', 'DAYS_BETWEEN_ISSUAL_LESS_THAN_MIN_DAYS_CONFIGURED','MAX_COUPON_ISSUAL_PER_SERIES_EXCEEDED',
                          'REDEMPTION_VALID_START_DATE_AFTER_SERIES_EXPIRY','INVALID_ISSUAL_STORE_ID','COUPONS_EXHAUSTED', 'COUPON_PRESENT_IN_MUTUAL_EXCLUSIVE_SERIES', 'COUPON_EXPIRED']
    testConfig = [
        [['COUPON_ALREADY_ISSUED', 'user already has a coupon'], {'do_not_resend_existing_voucher': True}],
        [['MAX_COUPON_ISSUAL_PER_USER_EXCEEDED', 'max coupon per user exceeded'],{'allow_multiple_vouchers_per_user': True, 'max_vouchers_per_user': 1,'do_not_resend_existing_voucher': True}],
        [['DAYS_BETWEEN_ISSUAL_LESS_THAN_MIN_DAYS_CONFIGURED', 'days between consecutive issuals for a user less than min days between issuals'], {'allow_multiple_vouchers_per_user': True, 'max_vouchers_per_user': 2,'do_not_resend_existing_voucher': True, 'min_days_between_vouchers' : 3}],
        [['MAX_COUPON_ISSUAL_PER_SERIES_EXCEEDED', 'max create for series exceeded'], {'allow_multiple_vouchers_per_user': True, 'max_vouchers_per_user': 2,'do_not_resend_existing_voucher': True, 'max_create' : 8}],
        [['REDEMPTION_VALID_START_DATE_AFTER_SERIES_EXPIRY', 'coupon redemption valid start date is after series expiry date'], {'allow_multiple_vouchers_per_user': True, 'max_vouchers_per_user': 2,'do_not_resend_existing_voucher': True, 'redemption_valid_after_days' : 10, 'redemption_valid_from' : None}],
        [['INVALID_ISSUAL_STORE_ID', 'invalid store'], {'allow_multiple_vouchers_per_user': True, 'max_vouchers_per_user': 2,'do_not_resend_existing_voucher': True, 'store_ids_json' : '[87728]'}],
        [['COUPONS_EXHAUSTED', 'coupons exhausted'], {'allow_multiple_vouchers_per_user': True,'do_not_resend_existing_voucher': True, 'client_handling_type' : 'DISC_CODE_PIN'}],
        [['COUPON_PRESENT_IN_MUTUAL_EXCLUSIVE_SERIES', 'coupon present in mutually exclusive series id '], {'allow_multiple_vouchers_per_user': True, 'max_vouchers_per_user': 2,'do_not_resend_existing_voucher': True}],
        [['COUPON_EXPIRED', 'coupon series expired'], {'allow_multiple_vouchers_per_user': True, 'max_vouchers_per_user': 2,'do_not_resend_existing_voucher': True, 'expiry_strategy_value' : 1, 'expiry_strategy_type' : 'SERIES_EXPIRY', 'valid_till_date' : None}]
    ]

    wechatMobilepush = {
        'nightly' : {
            'line':{
                'orgName':'Keep Calm',
                'orgId':1619,
                'accountId':'8782',
                'sourceAccountId':'4e61838d9b9c303c6e95b3aabfd1d625',
                'user':[
                    {
                        'firstName':'',
                        'lastName':'',
                        'mobile':'',
                        'email':'',
                        'userId' : 24130657
                    },
                    {
                        'firstName':'',
                        'lastName':'',
                        'mobile':'',
                        'email':'',
                        'userId' : 340289542
                    }
                ]
            },
            'wechat':{
                'orgName':'Houdini',
                'orgId':780,
                'account':'CapillaryDev3',
                'user':[{
                    'firstName':'Jerry',
                    'lastName':'Wu',
                    'mobile':'13700000002',
                    'email':'jerry.wu@capillarytech.com',
                    'userId' : 315690334
                    },
                    {
                    'firstName':'casey',
                    'lastName':'Wu',
                    'mobile':'13888886666',
                    'email':'casey.test@cap.com',
                    'userId' : 315779208
                    }
                ],
                'wecrm_details': {
                    'token': 'eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJqdWxpYS56aG91QGNhcGlsbGFyeXRlY2guY29tIiwiaWwiOnRydWUsImV4cCI6NDcwOTg3NTY2MiwiaWF0IjoxNTU0MjAyMDYyNzAzLCJqdGkiOiIxMDg3NzEifQ.Xc7bbuCI9XpsySqeiPR41eGSiZXC8UEpQK_N2oluHAVGf2EkKMrTG7wbPKN20KeAt7H59p_3fuwXNA9jsGuqzQ',
                    'id': 'wxc7bf989decc7e35b',
                    'url': ' https://test-aws-we-api.capillarytech-cn.com/template',
                    'creativeTemplate': '//arya/api/v1/creatives/templates/wechat?wecrmId={}&wecrmToken={}'
                },
                'appId': 'wxc7bf989decc7e35b',
                'appSecret': 'eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJqdWxpYS56aG91QGNhcGlsbGFyeXRlY2guY29tIiwiaWwiOnRydWUsImV4cCI6NDcwOTg3NTY2MiwiaWF0IjoxNTU0MjAyMDYyNzAzLCJqdGkiOiIxMDg3NzEifQ.Xc7bbuCI9XpsySqeiPR41eGSiZXC8UEpQK_N2oluHAVGf2EkKMrTG7wbPKN20KeAt7H59p_3fuwXNA9jsGuqzQ',
                'OriginalId': 'gh_b5e131178808',
            },
            'mobilepush':{
                'orgName':'mobile push',
                'orgId':50074,
                'account':'urdoorstep',
                'androidE2E_User': '917022012384',
                'channels': ['android', 'ios']
            }                           
        },
        'staging' : {
            'line':{
                'orgName':'reon_data',
                'orgId':50128,
                'accountId':'1820',
                'sourceAccountId':'4e61838d9b9c303c6e95b3aabfd1d625',
                'user':[
                    {
                        'firstName':'',
                        'lastName':'',
                        'mobile':'',
                        'email':'',
                        'userId' : 340293445
                    },
                    {
                        'firstName':'',
                        'lastName':'',
                        'mobile':'',
                        'email':'',
                        'userId' : 340289542
                    }
                ]
            },
            'wechat':{
                'orgName':'Orianna',
                'orgId':522,
                'account':'CapillaryDev3',
                'user':[],
                'wecrm_details': {
                    'token': '',
                    'id': '',
                    'url': '',
                    'creativeTemplate': '//arya/api/v1/creatives/templates/wechat?wecrmId={}&wecrmToken={}'
                },
                'appId': '',
                'appSecret': '',
                'OriginalId': '',
                },
            'mobilepush':{
                'orgName':'Cool Map',
                'orgId': 568,
                'account':'urdoorstep',
                'androidE2E_User': '917022012384',
                'channels': ['android', 'ios']
            }
        },
        'more': {
            'line':{
                'orgName':'Cool Map',
                'orgId':150124,
                'accountId':'525',
                'sourceAccountId':'4e61838d9b9c303c6e95b3aabfd1d625',
                'user':[
                    {
                        'firstName':'',
                        'lastName':'',
                        'mobile':'',
                        'email':'',
                        'userId' : 63783511
                    },
                    {
                        'firstName':'',
                        'lastName':'',
                        'mobile':'',
                        'email':'',
                        'userId' : 63782321
                    }
                ]
            },
            'mobilepush':{
                'orgName':'Cool Map',
                'orgId': None,
                'account':'urdoorstep',
                'androidE2E_User': '917022012384',
                'channels': ['android', 'ios']
            }        
        },
        'india': {
            'mobilepush':{
                'orgName':'Cool Map',
                'orgId': 1170,
                'account':'urdoorstep',
                'androidE2E_User': '917022012384',
                'channels': ['android', 'ios']
            }        
        },
        'eu': {
            'line':{
                'orgName':'REON_DATA',
                'orgId':100323,
                'accountId':'326',
                'sourceAccountId':'4e61838d9b9c303c6e95b3aabfd1d625',
                'user':[
                    {
                        'firstName':'',
                        'lastName':'',
                        'mobile':'',
                        'email':'',
                        'userId' : 65387464
                    },
                    {
                        'firstName':'',
                        'lastName':'',
                        'mobile':'',
                        'email':'',
                        'userId' : 65387474
                    }
                ]
            },
            'mobilepush':{
                'orgName':'PH_Demo',
                'orgId': 1170,
                'account':'urdoorstep',
                'androidE2E_User': '917022012384',
                'channels': ['android', 'ios']
            }        
        },
        'china' : {
            'wechat':{
                'orgName':'Purples',
                'orgId':200018,
                'account':'Purples',
                'user':[{
                    'firstName':'Manish',
                    'lastName':'Mishra',
                    'mobile':'8618621994057',
                    'email':'manish.mishra@capillarytech.com',
                    'userId' : 29040
                    }
                ],
                'wecrm_details': {
                    'token': 'eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJ6aG91cGluZyIsImlsIjp0cnVlLCJleHAiOjQ2NzEzMjc2MDYsImlhdCI6MTUxNTY1NDAwNjU3MSwianRpIjozfQ.PrpK2hRr2Mt9j-ctEMZeApwePPnq_mpLzs6kxTM6hZMA6pOtU--hlDnn26oQomVWnK3Zr-eXYT-ieo0Nv-7-Ig',
                    'id': 'wxaab7f09307c6c5fc',
                    'url': 'http://w.capillarytech-cn.com/template',
                    'creativeTemplate': '//arya/api/v1/creatives/templates/wechat?wecrmId={}&wecrmToken={}'
                },
                'appId': 'wxaab7f09307c6c5fc',
                'appSecret': 'eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJ6aG91cGluZyIsImlsIjp0cnVlLCJleHAiOjQ2NzEzMjc2MDYsImlhdCI6MTUxNTY1NDAwNjU3MSwianRpIjozfQ.PrpK2hRr2Mt9j-ctEMZeApwePPnq_mpLzs6kxTM6hZMA6pOtU--hlDnn26oQomVWnK3Zr-eXYT-ieo0Nv-7-Ig',
                'OriginalId': 'gh_82e2ace58c5a',
                },
            'mobilepush':{
                'orgName':'',
                'orgId': None,
                'account':'urdoorstep'
            }                
        },
        'local' : {

        }
    }
