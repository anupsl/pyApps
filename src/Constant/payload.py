import time


class payload():
    payload = {
        'createcampaign':
            {
                'description': 'Automation Created Campaign',
                'name': 'IRIS_' + str(int(time.time() * 100000)),
                'campaignType': 'OUTBOUND',
                'startDate': int(time.time() * 1000),
                'endDate': int(time.time() * 1000 + 25 * 60 * 60 * 1000),
                'goalId': '1',
                'objectiveId': '1',
                'classifier': 'Newsletter',
                'gaName': '',
                'gaSource': '',
                'tags': 'Diwali,AllWomen',
                'entityId': '-2',
                'testControl': {'type': 'ORG', 'test': 90}
            },
        'createlist':
            {
                'name': 'IRIS_LIST_' + str(int(time.time() * 100000)),
                'customTagCount': 0,
                'groupTags': []
            },
        'mergelist':
            {
                'name': 'IRIS_LIST_' + str(int(time.time() * 100000)),
                'customTagCount': 0,
                'groupTags': [],
                'recipients':
                    {
                        'dataSource': 'CSV',
                        'schema': 'firstName,lastName,mobile',
                        'data': ['Test1,Automation1,918497846843']
                    }
            },
        'addrecipient':
            {
                'dataSource': 'CSV',
                'schema': 'firstName,lastName,mobile',
                'data': ['Test1,Automation1,8497846843']
            },
        'createcoupon':
            {
                'campaignId': 0,
                'couponLimit':
                    {
                        'limit': 0,
                        'type': 'UNLIMITED'
                    },
                'couponSeriesTag': 'IRIS_COUPON' + str(int(time.time() * 100000)),
                'discountOn': 'BILL',
                'discountType': 'ABS',
                'discountValue': 10,
                'issuableTillIds': None,
                'redeemableTillIds': None
            },
        'createmessage':
            {
                'channel': 'SMS',
                'schedule':
                    {
                        'type': 'IMMEDIATELY',
                    },

                'message': 'Hi {{first_name}} {{last_name}} {{store_id}},Sending SMS via IRIS Automation  {{optout}}',
                'senderDetails':
                    {
                        'useSystemDefaults': False
                    },
                'listId': 99999999999,
                'storeType': 'REGISTERED_STORE',
                'additionalInfo':
                    {
                        'targetNdnc': False,
                        'useTinyUrl': False
                    }
            },
        'audiencegroupbody':
            {
                "type": 'UPLOAD',
                "label": "AutomationList_{}".format(int(time.time() * 1000)),
                "description": "Automation Created List",
                "tags": [],
                "data": {
                    "schema": {
                        "type": "SINGLE_KEY_IDENTIFIER",
                        "identifier": ["MOBILE"],
                        "data": ["MOBILE", "FIRST_NAME"]
                    },
                    "source": "FILE"
                }
            },
        'createcampaignv2':
            {
                "startDate": int(time.time() * 1000) + 24 * 60 * 60 * 1000,
                "endDate": int(time.time() * 1000) + 2 * 24 * 60 * 60 * 1000,
                "description": "Auto Set Payload in Automation constant",
                "testControl": {
                    "type": "ORG",
                    "testPercentage": 90
                },

                "name": "Automation_IRISV2_{}".format(int(time.time() * 1000))
            },
        'createMessagev2':
            {
                "targetAudience": {
                    "include": [],
                    "exclude": []
                },
                "type": "OUTBOUND",
                "name": "Automation_IRISV2_{}".format(int(time.time() * 1000)),
                "messageStrategy": {
                    "type": "DEFAULT"
                },
                "messageContent": {
                    "message_content_id_1": {
                        "channel": "SMS",
                        "messageBody": "Hi {{first_name}} come and visit Shoppers Stop for attractive discounts {{optout}}"
                    }
                },
                "schedule": {
                    "scheduleType": "IMMEDIATE"
                },
                "deliverySetting": {
                    "channelSetting": {
                        "SMS": {
                            "gsmSenderId": "7022012380",
                            "domainGatewayMapId": 84608,
                            "targetNdnc": False,
                            "channel": "SMS",
                            "cdmaSenderId": "7022012380"
                        },
                        "EMAIL": {
                            "senderLabel": "test",
                            "domainGatewayMapId": 84606,
                            "senderEmail": "test@irisv2test.com",
                            "channel": "EMAIL",
                            "senderReplyTo": "test@irisv2test.com"
                        }
                    },
                    "additionalSetting": {
                        "useTinyUrl": False,
                        "encryptUrl": False,
                        "skipRateLimit": True
                    }
                }
            },
        'testandpreview_sms':
            {
                "testContentOn": {
                    "testAudiences": [
                        {
                            "identifier": "9148585260",
                            "identifierType": "MOBILE",
                        }
                    ]
                },
                "messageContent": {
                    "mesage_content_1": {
                        "offers": [
                            {
                                "couponSeriesId": 20349,
                                "type": "COUPON"
                            }
                        ],
                        "channel": "SMS",
                        "messageBody": "Hi buddy , This is Iris Automation Generated SMS with tags {{optout}}"
                    }
                }
            },
        'testandpreview_email':
            {
                "testContentOn": {
                    "testAudiences": [
                        {
                            "identifier": "testAutomation_h89179@gmail.com",
                            "identifierType": "EMAIL",
                        }
                    ]
                },
                "messageContent": {
                    "mesage_content_1": {
                        "offers": [
                            {
                                "couponSeriesId": 20349,
                                "type": "COUPON"
                            }
                        ],
                        "emailSubject": "TestAndPreviewAutomation",
                        "channel": "EMAIL",
                        "emailBody": "Hi buddy , This is Iris Automation Generated EMAIL with tags {{unsubscribe}}"
                    }
                }
            },
        'derivedlist':{
            "includedGroups": [],
            "excludedGroups" : [],
            "audienceGroupType": "DERIVED",
            "label": "Automation_Test_Derived_{}".format(time.time()),
            "description":"Auto_Test_Description_{}".format(time.time()),
            "tags": []
        },
        'campaignsetting':{
            "messageSettings" : {
                "enableLinkTracking" :  False
            },
            "reportsSettings" : {
                "summaryReportReceivers" : [],
                "creditReportReceivers" : []
            },
            "alertsSettings" : {
                "failureReceivers" : [],
                "lowDeliveryReceivers" : []
        }
}


    }
