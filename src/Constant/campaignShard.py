import time

class campaignShardConstant():
    
    filterV2Json = {
        "filterName": "filterV2" + str(time.time() * 1000),
        "targetBlock": [{
            "betweenError": False,
            "loyalty": {
                "attribute": "type",
                "dimension": "loyalty_type",
                "dslString": {
                    "value": "0",
                    "operator": "GREATER_THAN",
                    "dslQuery": "user.projections.customer_summary.filter(loyalty_type.typein({{#each values}}'{{this}}'{{#unless @last}},{{/unless}}{{/each}})).count(dim_event_user_id)"
                },
                "values": ["loyalty"],
                "edit": False,
                "hideEdit": True
            },
            "blocks": [{
                "label": "Unique Identifier",
                "description": "Filter customers based on their unique identifier (mobile number and email).",
                "isSelected": True,
                "editMode": True,
                "data": {},
                "filters": [{
                    "_id": "5a793caaf485003d241b97d9",
                    "name": "Unique Identifier",
                    "description": "Filter customers based on their unique identifier (mobile number and email).",
                    "category": "User Profile",
                    "scope": {
                        "isPublic": True,
                        "tag": "GLOBAL",
                        "orgId": 0
                    },
                    "supportLink": "http://support.capillarytech.com/support/solutions/articles/4000118995-unique-identifier",
                    "entities": {
                        "description": "{{#if invertedFilter}}Exclude{{else}}Include{{/if}} customers whose {{entities.kpis.[0].values.[0]}} {{beautify entities.kpis.[1].kpi}} {{entities.kpis.[1].values.[0]}}",
                        "isDSL": True,
                        "dslString": [{
                            "string": "user.projections.customer_summary.filter(event_user.{{entities.kpis.[0].values.[0]}}like({{parseLike entities.kpis.[1].kpi entities.kpis.[1].values.[0]}})).count(dim_event_user_id)",
                            "operator": "GREATER_THAN",
                            "value": "0"
                        }],
                        "labelArray": [],
                        "where": [],
                        "dimensions": [],
                        "kpis": [{
                            "fromValueError": False,
                            "values": ["email"],
                            "operator": "LIKE",
                            "hideOperatorList": True,
                            "kpi": "event_user",
                            "placeholder": "mobile no",
                            "possibleValues": [{
                                "key": "mobile",
                                "value": "Mobile"
                            }, {
                                "key": "email",
                                "value": "Email"
                            }],
                            "label": "customers whose",
                            "possibleOperations": [{
                                "value": "greater than equal",
                                "key": "GREATER_THAN_EQUALS"
                            }, {
                                "value": "less than equal",
                                "key": "LESS_THAN_EQUALS"
                            }, {
                                "value": "equals",
                                "key": "EQUALS"
                            }, {
                                "value": "in range of",
                                "key": "BETWEEN"
                            }, {
                                "value": "not in",
                                "key": "NOT_IN"
                            }, {
                                "value": "in",
                                "key": "IN"
                            }, {
                                "value": "is",
                                "key": "IS"
                            }, {
                                "value": "is not",
                                "key": "IS_NOT"
                            }],
                            "userInput": True
                        }, {
                            "fromValueError": False,
                            "values": ["iris"],
                            "operator": "EQUALS",
                            "hideOperatorList": True,
                            "dataType": "string",
                            "kpi": "contains",
                            "defaultLabel": "",
                            "placeholder": "select",
                            "possibleValues": [],
                            "label": [{
                                "value": "Contains",
                                "key": "Contains::kpis::1::kpi::contains"
                            }, {
                                "value": "Start with",
                                "key": "Start with::kpis::1::kpi::start_with"
                            }, {
                                "value": "End with",
                                "key": "End with::kpis::1::kpi::end_with"
                            }],
                            "selectedLabel": "Contains::kpis::1::kpi::contains",
                            "possibleOperations": [{
                                "value": "not in",
                                "key": "NOT_IN"
                            }, {
                                "value": "in",
                                "key": "IN"
                            }, {
                                "value": "is",
                                "key": "IS"
                            }, {
                                "value": "is not",
                                "key": "IS_NOT"
                            }],
                            "userInput": True
                        }],
                        "appliedDescription": "Include customers whose email contains iris"
                    },
                    "isFavourite": True
                }]
            }],
            "data": {},
            "editMode": False,
            "isApplied": True,
            "customers": {
                "type": "all",
                "data": {
                    "test_control_status___EXPERIMENT": 0,
                    "test_control_status___NOT-CAPTURED": 0,
                    "test_control_status___INVALID": 0,
                    "test_control_status___All": 0,
                    "totalCount": 368,
                    "test_control_status___CONTROL": 27,
                    "test_control_status___TEST": 341
                }
            },
            "isError": False,
            "key": 1
        }],
        "campaignId": "73433",
        "type": "LOYALTY",
        "testGroupPercentage": "90",
        "list_level_enabled": "0",
        "source": "",
        "callBackUrl": "/campaign/v3/base/CampaignOverview#recipient/73433"
    }
    
    thiriftCampaignShardTestReferenceObject = {
            'org':{
                'campaign':{
                    'name':None,
                    'id':None,
                    'lists':{
                        'UPLOADED':[],
                        'FILTER_BASED':[],
                        'DUPLICATE':[],
                        'MERGE':[],
                        'SPLIT':[],
                        'DEDUP':[]
                        }
                    }
                },
            'skip':{
                'campaign':{
                    'name':None,
                    'id':None,
                    'lists':{
                        'UPLOADED':[],
                        'FILTER_BASED':[],
                        'DUPLICATE':[],
                        'MERGE':[],
                        'SPLIT':[],
                        'DEDUP':[]
                        }
                    }
                },
            'custom':{
                'campaign':{
                    'name':None,
                    'id':None,
                    'lists':{
                        'UPLOADED':[],
                        'FILTER_BASED':[],
                        'DUPLICATE':[],
                        'MERGE':[],
                        'SPLIT':[],
                        'DEDUP':[]
                        }
                    }
                }
            }
    
