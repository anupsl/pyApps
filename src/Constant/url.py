class url():
    
    clusterUrl = {
        'local' : {
            'url' : 'http://localhost:9340',
            'intouchUrl' : 'http://localhost:9340'
        },
        'nightly' : {
            'url' : 'http://iris.nightly.capillary.in',
             'intouchUrl' : 'https://nightly.capillary.in'
        },
        'staging' : {
            'url' : 'http://iris.staging.capillary.in',
            'intouchUrl' : 'https://intouch-staging.capillary.in'
        },
        'more' : {
            'url' : 'http://apac2.intouch.capillarytech.com',
            'intouchUrl' : 'https://apac2.intouch.capillarytech.com'
        },
        'india' : {
            'url' : 'http://intouch.capillary.co.in',
            'intouchUrl' : 'https://intouch.capillary.co.in'
        },
        'eu' : {
            'url' : 'http://eu.intouch.capillarytech.com',
            'intouchUrl' : 'https://eu.intouch.capillarytech.com'
        },
        'china' : {
            'url' : 'http://intouch.capillarytech.cn.com',
            'intouchUrl' : 'https://intouch.capillarytech.cn.com'
        }
    }

    endpoints = {
        'createcampaign'    : '/iris/v1/campaign',
        'getcampaign'   : '/iris/v1/campaign/{campaignId}',
        'updatecampaign'   : '/iris/v1/campaign/{campaignId}',
        'createlist'    : '/iris/v1/campaign/{campaignId}/lists',
        'mergelist'    : '/iris/v1/campaign/{campaignId}/lists',
        'addrecipient'  : '/iris/v1/campaign/{campaignId}/lists/{listId}/recipients',
        'createcoupon'  : '/iris/v1/coupon',
        'createmessage' : '/iris/v1/campaign/{campaignId}/message/',
        'authorize' : '/iris/v1/campaign/{campaignId}/message/{messageId}/approve',
        'getreplymessagelist' : '/iris/v1/campaign/{}/message/replay',  # campaignId
        'replymessage' : '/iris/v1/campaign/{}/message/replay/{}'  # campaignId and messageId
    }

    endpointsIrisV2 = {
        'checkexists' : '/iris/v2/audience/checkExists/{name}',
        'checkcampaignexists' :'/iris/v2/campaigns/checkExists?name={name}',
        'getbyid' : '/iris/v2/audience/{group_id}',
        'createcampaign' : '/iris/v2/campaigns',
        'createlist': '/iris/v2/audience',
        'createderivedlist': '/iris/v2/audience/derived',
        'sticklylist': '/iris/v2/audience/orgusers',
        'getcampaignbyid': '/iris/v2/campaigns/{campaignId}',
        'createmessage':'/iris/v2/campaigns/{campaignId}/messages',
        'getmessage':'/iris/v2/campaigns/{campaignId}/messages/{messageId}',
        'getmessagevariant':'/iris/v2/campaigns/{campaignId}/messages/variant/{variantId}',
        'approvemessage': '/iris/v2/campaigns/{campaignId}/messages/{msgId}/approve',
        'testpreview': '/iris/v2/campaigns/{campaignId}/messages/test',
        'loyaltyprogram':'/iris/v2/org/campaign/meta/loyaltyProgram',
        'pocusers' : '/iris/v2/org/campaign/meta/pocs',
        'precheck': '/iris/v2/campaigns/{campaignId}/messages/{messageId}/precheck',
        'monitoringbymessageid' : '/iris/v2/campaigns/{}/messages/{}',#campaignId_&_MessageId
        'monitoringbycampaignid' : '/iris/v2/campaigns/{}/messages',#campaignId
        'monitoringbyorgid' : '/iris/v2/campaigns/monitoring',
        'campaignsettings' :'/iris/v2/org/campaign/settings',
        'editcampaign' : '/iris/v2/campaigns/{campaignId}',
        'campaignobjectives':'/iris/v2/org/campaign/meta/objectives',#campaignId
        'rejectmessage': '/iris/v2/campaigns/{campaignId}/messages/{msgId}/reject',
        'startmessage': '/iris/v2/campaigns/{campaignId}/messages/{msgId}/start',
        'stopmessage': '/iris/v2/campaigns/{campaignId}/messages/{msgId}/stop',
        'editmessage': '/iris/v2/campaigns/{campaignId}/messages/{msgId}',
        'productcategory': '/iris/v2/org/campaign/meta/{category}/levels',
        'productlevel': '/iris/v2/org/campaign/meta/{urlSubstringForDimension}/{levelName}/values',
        'productsearch':'/iris/v2/org/campaign/meta/{urlSubstringForDimension}/{levelName}/values/{searchText}',
        'remindercount':'/iris/v2/org/campaign/meta/reminderFilters?campaignId={campaignId}&messageId={messageId}&reminderStrategy={reminderType}',
        'orgv2status' :'/iris/v2/org/campaign/meta/orgCampaignV2Status',
        'orgonboadringstatus' :'/iris/migration/onboardcheck/{orgId}'
    }

    aryaEndpoints = {
        'authlogin' : '/arya/api/v1/auth/login',
        's3info' : '/arya/api/v1/nfs/filters/{}/stats',
        'filterlist' : '/arya/api/v1/nfs/filters/create?context=campaign&time={}',
        'data' :'/arya/api/v1/bi/data/reports/charts/identifier/CAMPAIGN_PERFORMANCE?type=NORMAL',
        'remindernfs': '/arya/api/v1/nfs/filters/reminder'
    }
    
    intouchEndpoints = {
        'customerAdd' : '/v1.1/customer/add?format=json&user_id=true',
        'customerGet' : '/v1.1/customer/get?format=json',
        'requestAdd' : '/v1.1/request/add?format=json&client_auto_approve=true',
        'customerSubscriptions' : '/v1.1/customer/subscriptions?format=json',
        'couponRedeem' : '/v1.1/coupon/redeem?format=json',
        'transactionAdd' : '/v1.1/transaction/add?format=json&user_id=true'       
    }

    auth = {
        'local' : {
            'intouchUsername' : 'ashish', 'intouchPassword' : '123', 'userId' : '0'
        },
        'nightly' : {
            'intouchUsername' : 'ashish', 'intouchPassword' : '123', 'userId' : '15000449'
        },
        'staging' : {
            'intouchUsername' : 'first_user@capillarytech.com', 'intouchPassword' : 'First@123', 'userId' : '4'
        },
        'more' : {
            'intouchUsername' : 'automation@dealhunt.in', 'intouchPassword' : 'j#E=ges?fRNp12', 'userId' : '200041419'
        },
        'india' : {
            'intouchUsername' : 'automation@dealhunt.in', 'intouchPassword' : 'j#E=ges?fRNp12', 'userId' : '12808453'
        },
        'eu' : {
            'intouchUsername' : 'automation@dealhunt.in', 'intouchPassword' : 'j#E=ges?fRNp12', 'userId' : '75001527'
        },
        'china' : {
            'intouchUsername' : 'automation@dealhunt.in', 'intouchPassword' : 'j#E=ges?fRNp13', 'userId' : '300002029'
        }
    }
