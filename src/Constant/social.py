class social():
    
    """ @Chatbot """
    GatewayResponseType = {0: 'success', 1: 'sent', 2: 'blocked', 3: 'failed', 4: 'invalidContent',
                           5: 'policyViolation'}

    ButtonType = {'web_url':0, 'postback':2, 'phone_number':3, 'element_share':4, 'payment':5,
                  'account_link':6, 'account_unlink':7}

    ButtonField = {'url':0, 'webview_height_ratio':1, 'messenger_extensions':2, 'fallback_url':3, 'payload, payment_summary':4}

    MessageType = {'textMessage':0, 'buttonMessage':1, 'genericMessage':2, 'quickReplyMessage':3, 'receiptMessage':4, 'listMessage':5}

    QuickReplyContentType = {'text':0, 'location':1}

    ListMessageTopElementStyle = {'large':0, 'compact':1}

    SocialChannel = {'none':0, 'facebook':1, 'google':2, 'twitter':3}

    GatewayResponseType = {'success':0, 'sent':1, 'blocked':2, 'failed':3, 'invalidContent':4, 'policyViolation':5}

    TargetType = {'GROUPED':1, 'TIMELINE':2, 'EXPIRY_REMINDER':3, 'SOCIAL':4}
    
    CommunicationType = {'SMS':1, 'EMAIL':2, 'CALL_TASK':3, 'WECHAT':4, 'PUSH':5, 'ANDROID':6, 'IOS':7, 'FACEBOOK':8}

    
    """ @Marketing """
    
    ExistingGroupId = {'nightly':342695, 'staging':20388, 'india':252819, 'more':11111}
    ExistingListName = {'nightly':'Apps 1509589393132', 'staging':'eid', 'apac':'Apps 1508921411318'}
    genericAdsetNameToValidateFromAllAdSets = {'facebook':'Apps 1511301758738', 'google':'Internal Test1'}  # This is specific to Advert Account used 
    