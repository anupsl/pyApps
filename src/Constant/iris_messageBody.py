class iris_messageBody():
    # Used in IRISV2
    irisMessage = {
        'sms': {
            'plain': 'Hi buddy , This is Iris Automation Generated SMS with  Tags {{first_name}} {{last_name}} {{fullname}}  {{optout}}', #{{dynamic_expiry_date_after_1_days.FORMAT_2}}
            'generic': 'Hi buddy , This is Iris Automation for Generic Type with tags : {{first_name}} {{last_name}} {{fullname}}   {{optout}}',#{{dynamic_expiry_date_after_1_days.FORMAT_2}}
            'points': 'Hi buddy , This is Iris Automation for points Type with Tags : {{first_name}} {{last_name}} {{fullname}}  {{loyalty_points}}  {{loyalty_points_floor}}  {{loyalty_points_value}}   {{loyalty_points_value_floor}}   {{slab_name}}   {{promotion_points}} {{promotion_points_floor}} {{promotion_points_expiring_on.FORMAT_1}} {{optout}}', #{{dynamic_expiry_date_after_1_days.FORMAT_2}}
            'coupon': 'Hi buddy , This is Iris Automation for Coupon Type with Tags : {{first_name}} {{last_name}} {{fullname}}  {{dynamic_expiry_date_after_1_days.FORMAT_2}} {{voucher}} {{valid_days_from_create}} {{valid_till_date.FORMAT_2}} {{optout}}',
            'coupons': 'Hi buddy , This is Iris Automation for Coupon Type with Tags : {{first_name}} {{last_name}} {{fullname}}  {{dynamic_expiry_date_after_1_days.FORMAT_2}} {{voucher}} {{valid_days_from_create}} {{valid_till_date.FORMAT_2}} {{optout}}',
            'multicoupons': 'Hi buddy , This is Iris Automation for Coupon Type with Tags : {{first_name}} {{last_name}} {{fullname}}  {{dynamic_expiry_date_after_1_days.FORMAT_2}} {{voucher(CSId)}} {{valid_days_from_create(CSId)}} {{valid_till_date.FORMAT_2(CSId)}} {{offer_name(CSId)}} {{voucher(CSId1)}} {{valid_days_from_create(CSId1)}} {{valid_till_date.FORMAT_2(CSId1)}} {{offer_name(CSId1)}}{{optout}}',
            'registeredstore' : 'Hi buddy, This is Iris Automation for registered store Tags : {{registered_store_name}} {{registered_base_store_name}} {{registered_store_number}} {{registered_base_store_number}} {{registered_store_land_line}} {{registered_store_email}} {{registered_store_external_id}} {{registered_store_external_id_1}} {{registered_store_external_id_2}} {{registered_sms_store_name}} {{registered_sms_email}} {{registered_sms_mobile}} {{registered_sms_land_line}} {{registered_sms_address}} {{registered_sms_extra}} {{registered_email_store_name}} {{registered_email_email}} {{registered_email_mobile}} {{registered_email_land_line}} {{registered_email_address}} {{registered_email_extra}} {{optout}}',
            'lasttransactedstore': 'Hi buddy, This is Iris Automation for last transacted store Tags : {{last_transacted_store_id}} {{last_transacted_store_name}} {{last_transacted_base_store_name}} {{last_transacted_store_number}}{{last_transacted_base_store_number}} {last_transacted_store_land_line}} {{last_transacted_store_email}} {{last_transacted_store_external_id}} {{last_transacted_store_external_id_1}} {{last_transacted_store_external_id_2}} {{last_transacted_sms_store_name}} {{last_transacted_sms_email}} {{last_transacted_sms_mobile}} {{last_transacted_sms_land_line}} {{last_transacted_sms_address}}{{last_transacted_sms_extra}} {{last_transacted_email_store_name}} {{last_transacted_email_email}} {{last_transacted_email_mobile}} {{last_transacted_email_land_line}} {{last_transacted_email_address}}{{last_transacted_email_extra}} {{optout}}'
        },
        'email': {
            'plain': 'Hi buddy , This is Iris Automation Generated EMAIL with tags {{unsubscribe}}',
            'generic': 'Hi buddy , This is Iris Automation Generated EMAIL with tags {{unsubscribe}} ',
            'points': 'Hi buddy , This is Iris Automation Generated EMAIL with tags {{unsubscribe}}',
            'coupon': 'Hi buddy , This is Iris Automation Generated EMAIL with tags {{unsubscribe}}',
            'coupons': 'Hi buddy , This is Iris Automation Generated EMAIL with tags {{unsubscribe}}',
            'multicoupons': 'Hi buddy , This is Iris Automation Generated EMAIL with tags {{voucher(CSId)}} {{valid_days_from_create(CSId)}} {{valid_till_date.FORMAT_2(CSId)}} {{offer_name(CSId)}} {{voucher(CSId1)}} {{valid_days_from_create(CSId1)}} {{valid_till_date.FORMAT_2(CSId1)}} {{offer_name(CSId1)}} {{unsubscribe}}'
        },
        'wechat': {
            'plain': ['{{first_name}}', '{{last_name}}', '{{fullname}}', '{{loyalty_points}}',
                      '{{loyalty_points_floor}}', '{{loyalty_points_value}}', '{{loyalty_points_value_floor}}',
                      '{{slab_name}}', '{{dynamic_expiry_date_after_1_days.FORMAT_2}}', '{{custom_tag_1}}'],
            'generic': ['{{first_name}}', '{{last_name}}', '{{fullname}}', '{{loyalty_points}}',
                        '{{loyalty_points_floor}}', '{{loyalty_points_value}}', '{{loyalty_points_value_floor}}',
                        '{{slab_name}}', '{{dynamic_expiry_date_after_1_days.FORMAT_2}}', '{{custom_tag_1}}'],
            'points': ['{{first_name}}', '{{last_name}}', '{{fullname}}', '{{loyalty_points}}',
                       '{{loyalty_points_floor}}', '{{loyalty_points_value}}', '{{loyalty_points_value_floor}}',
                       '{{slab_name}}', '{{dynamic_expiry_date_after_1_days.FORMAT_2}}', '{{custom_tag_1}}',
                       '{{promotion_points}}', '{{promotion_points_floor}}',
                       '{{promotion_points_expiring_on.FORMAT_1}}'],
            'coupon': ['{{first_name}}', '{{last_name}}', '{{fullname}}', '{{loyalty_points}}',
                        '{{loyalty_points_floor}}', '{{loyalty_points_value}}', '{{loyalty_points_value_floor}}',
                        '{{slab_name}}', '{{dynamic_expiry_date_after_1_days.FORMAT_2}}', '{{custom_tag_1}}',
                        '{{voucher}}', '{{valid_days_from_create}}', '{{valid_till_date.FORMAT_2}}'],
            'coupons': ['{{first_name}}', '{{last_name}}', '{{fullname}}', '{{loyalty_points}}',
                        '{{loyalty_points_floor}}', '{{loyalty_points_value}}', '{{loyalty_points_value_floor}}',
                        '{{slab_name}}', '{{dynamic_expiry_date_after_1_days.FORMAT_2}}', '{{custom_tag_1}}',
                        '{{voucher}}', '{{valid_days_from_create}}', '{{valid_till_date.FORMAT_2}}'],
        },
        'mobilepush': {
            'plain': '',
            'generic': '',
            'points': '',
            'coupon': '',
            'coupons': ''
        }
    }

    campaignId = {'ORG': -1, 'CUSTOM': -1, 'SKIP': -1}

    irisGenericValues = {}

    getCampaignAll = {
        'upcomingStartDate': 1549327356000,
        'upcomingEndDate': 1549500156000
    }

    messagesDefault = {
        'updated': False,
        'campaignId': -1,
        'listId': -1,
        'voucherId': -1,
        'strategy': {},
        'groupVersionResult': {},
        'bucketId': -1,
        'SMS': {
            'IMMEDIATE': {
                'PLAIN': {True: {}, False: {}},
                'Generic': {True: {}, False: {}},
                'COUPONS': {True: {}, False: {}},
                'POINTS': {True: {}, False: {}},
            },
            'PARTICULARDATE': {
                'PLAIN': {True: {}, False: {}},
                'Generic': {True: {}, False: {}},
                'COUPONS': {True: {}, False: {}},
                'POINTS': {True: {}, False: {}},
            },
            'RECURRING': {
                'PLAIN': {True: {}, False: {}},
                'Generic': {True: {}, False: {}},
                'COUPONS': {True: {}, False: {}},
                'POINTS': {True: {}, False: {}},
            }
        },
        'WECHAT': {
            'IMMEDIATE': {
                'PLAIN': {True: {}, False: {}},
                'Generic': {True: {}, False: {}},
                'COUPONS': {True: {}, False: {}},
                'POINTS': {True: {}, False: {}},
            },
            'PARTICULARDATE': {
                'PLAIN': {True: {}, False: {}},
                'Generic': {True: {}, False: {}},
                'COUPONS': {True: {}, False: {}},
                'POINTS': {True: {}, False: {}},
            },
            'RECURRING': {
                'PLAIN': {True: {}, False: {}},
                'Generic': {True: {}, False: {}},
                'COUPONS': {True: {}, False: {}},
                'POINTS': {True: {}, False: {}},
            }
        }
    }

    campaignDefaultValues = {
        'LIVE': {
            'ORG': {
                'Value': {
                    'response': {},
                    'payload': {}
                },
                'Coupon': {
                    'response': {},
                    'payload': {}
                },
                'List': {
                    'TAGS': {
                        0: {'response': {}, 'payload': {}, 'campaignId': -1},
                        1: {'response': {}, 'payload': {}, 'campaignId': -1},
                        2: {'response': {}, 'payload': {}, 'campaignId': -1},
                        3: {'response': {}, 'payload': {}, 'campaignId': -1},
                        4: {'response': {}, 'payload': {}, 'campaignId': -1},
                        5: {'response': {}, 'payload': {}, 'campaignId': -1}
                    }
                }
            },
            'CUSTOM': {
                'Value': {
                    'response': {},
                    'payload': {}
                },
                'Coupon': {
                    'response': {},
                    'payload': {}
                },
                'List': {
                    'TAGS': {
                        0: {'response': {}, 'payload': {}, 'campaignId': -1},
                        1: {'response': {}, 'payload': {}, 'campaignId': -1},
                        2: {'response': {}, 'payload': {}, 'campaignId': -1},
                        3: {'response': {}, 'payload': {}, 'campaignId': -1},
                        4: {'response': {}, 'payload': {}, 'campaignId': -1},
                        5: {'response': {}, 'payload': {}, 'campaignId': -1}
                    }
                }
            },
            'SKIP': {
                'Value': {
                    'response': {},
                    'payload': {}
                },
                'Coupon': {
                    'response': {},
                    'payload': {}
                },
                'List': {
                    'TAGS': {
                        0: {'response': {}, 'payload': {}, 'campaignId': -1},
                        1: {'response': {}, 'payload': {}, 'campaignId': -1},
                        2: {'response': {}, 'payload': {}, 'campaignId': -1},
                        3: {'response': {}, 'payload': {}, 'campaignId': -1},
                        4: {'response': {}, 'payload': {}, 'campaignId': -1},
                        5: {'response': {}, 'payload': {}, 'campaignId': -1}
                    }
                }
            }
        },
        'LAPSED': {
            'ORG': {
                'Value': {
                    'response': {},
                    'payload': {}
                },
                'Coupon': {
                    'response': {},
                    'payload': {}
                },
                'List': {
                    'TAGS': {
                        0: {'response': {}, 'payload': {}, 'campaignId': -1},
                        1: {'response': {}, 'payload': {}, 'campaignId': -1},
                        2: {'response': {}, 'payload': {}, 'campaignId': -1},
                        3: {'response': {}, 'payload': {}, 'campaignId': -1},
                        4: {'response': {}, 'payload': {}, 'campaignId': -1},
                        5: {'response': {}, 'payload': {}, 'campaignId': -1}
                    }
                }
            },
            'CUSTOM': {
                'Value': {
                    'response': {},
                    'payload': {}
                },
                'Coupon': {
                    'response': {},
                    'payload': {}
                },
                'List': {
                    'TAGS': {
                        0: {'response': {}, 'payload': {}, 'campaignId': -1},
                        1: {'response': {}, 'payload': {}, 'campaignId': -1},
                        2: {'response': {}, 'payload': {}, 'campaignId': -1},
                        3: {'response': {}, 'payload': {}, 'campaignId': -1},
                        4: {'response': {}, 'payload': {}, 'campaignId': -1},
                        5: {'response': {}, 'payload': {}, 'campaignId': -1}
                    }
                }
            },
            'SKIP': {
                'Value': {
                    'response': {},
                    'payload': {}
                },
                'Coupon': {
                    'response': {},
                    'payload': {}
                },
                'List': {
                    'TAGS': {
                        0: {'response': {}, 'payload': {}, 'campaignId': -1},
                        1: {'response': {}, 'payload': {}, 'campaignId': -1},
                        2: {'response': {}, 'payload': {}, 'campaignId': -1},
                        3: {'response': {}, 'payload': {}, 'campaignId': -1},
                        4: {'response': {}, 'payload': {}, 'campaignId': -1},
                        5: {'response': {}, 'payload': {}, 'campaignId': -1}
                    }
                }
            }
        },
        'UPCOMING': {
            'ORG': {
                'Value': {
                    'response': {},
                    'payload': {}
                },
                'Coupon': {
                    'response': {},
                    'payload': {}
                },
                'List': {
                    'TAGS': {
                        0: {'response': {}, 'payload': {}, 'campaignId': -1},
                        1: {'response': {}, 'payload': {}, 'campaignId': -1},
                        2: {'response': {}, 'payload': {}, 'campaignId': -1},
                        3: {'response': {}, 'payload': {}, 'campaignId': -1},
                        4: {'response': {}, 'payload': {}, 'campaignId': -1},
                        5: {'response': {}, 'payload': {}, 'campaignId': -1}
                    }
                }
            },
            'CUSTOM': {
                'Value': {
                    'response': {},
                    'payload': {}
                },
                'Coupon': {
                    'response': {},
                    'payload': {}
                },
                'List': {
                    'TAGS': {
                        0: {'response': {}, 'payload': {}, 'campaignId': -1},
                        1: {'response': {}, 'payload': {}, 'campaignId': -1},
                        2: {'response': {}, 'payload': {}, 'campaignId': -1},
                        3: {'response': {}, 'payload': {}, 'campaignId': -1},
                        4: {'response': {}, 'payload': {}, 'campaignId': -1},
                        5: {'response': {}, 'payload': {}, 'campaignId': -1}
                    }
                }
            },
            'SKIP': {
                'Value': {
                    'response': {},
                    'payload': {}
                },
                'Coupon': {
                    'response': {},
                    'payload': {}
                },
                'List': {
                    'TAGS': {
                        0: {'response': {}, 'payload': {}, 'campaignId': -1},
                        1: {'response': {}, 'payload': {}, 'campaignId': -1},
                        2: {'response': {}, 'payload': {}, 'campaignId': -1},
                        3: {'response': {}, 'payload': {}, 'campaignId': -1},
                        4: {'response': {}, 'payload': {}, 'campaignId': -1},
                        5: {'response': {}, 'payload': {}, 'campaignId': -1}
                    }
                }
            }
        }
    }
