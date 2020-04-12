import copy, sys, traceback, time, datetime
from src.Constant.constant import constant
from src.utilities.logger import Logger
from src.modules.iris.dbCallsMessage import dbCallsMessage
from calendar import day_abbr
from src.utilities.randValues import randValues


class construct():
    
    @staticmethod
    def constructUrl(endpointName, queryParam=[], module='iris'):
        endpoint = None
        clusterUrl = None
        if module.lower() == 'arya' :
            endpoint = constant.aryaEndpoints[endpointName.lower()]
            clusterUrl = constant.config['intouchUrl']
        elif module.lower() == 'intouch' :
            endpoint = constant.intouchEndpoints[endpointName.lower()]
            clusterUrl = constant.config['intouchUrl']
        elif module.lower() == 'irisv2':
            endpoint = constant.endpointsIrisV2[endpointName.lower()]
            clusterUrl = constant.config['url']
        else:
            endpoint = constant.endpoints[endpointName.lower()]
            clusterUrl = constant.config['url']
        
        if len(queryParam) > 0:
            endpoint = endpoint + '?'
            for eachParam in queryParam:
                endpoint = endpoint + eachParam[0] + '=' + str(eachParam[1]) + '&'
                
        return str(clusterUrl) + str(endpoint)
    
    @staticmethod
    def constructAuthenticate():
        return (constant.config['intouchUsername'], constant.config['intouchPassword'])

    @staticmethod
    def constructHeaders():
        header = {'accept':'application/json',
                'content-type':'application/json',
                'X-CAP-ORG':str(constant.config['orgId'])}
        if 'aryaCookiesDict' in constant.config : header.update({'X-CAP-CT':str(constant.config['aryaCookiesDict']['CT'])})
        return header
            
    @staticmethod
    def constructBody(payloadData, process, endpointName):
        endpointGenericPayload = copy.deepcopy(constant.payload[endpointName.lower()])
        Logger.log('Generic Body Saved for this Request :', endpointGenericPayload)
        Logger.log('Payload used to update :', payloadData)
        Logger.log('Process called to Construct is :', process)
        if process.lower() == 'update' :
            endpointGenericPayload.update(payloadData)
        elif process.lower() == 'pop':
            endpointGenericPayload.pop(payloadData)
        Logger.log('Constructed Body after update is :', endpointGenericPayload)
        return endpointGenericPayload
    
    @staticmethod
    def constructResponse(response):
        responseBody = None
        try: 
            responseBody = {'constructed':'pass', 'statusCode':response.status_code, 'X-CAP-REQUEST-ID':response.headers['X-CAP-REQUEST-ID'], 'encoding':response.encoding, 'text':response.text, 'json':response.json(), 'cookies':response.cookies}
        except Exception, exp :
            Logger.log('Exception Occured While Constructing Response :' + str(exp))
            responseBody = {'constructed':'fail', 'statusCode':response.status_code, 'text':response.text}
        finally:
            Logger.log('Response body Constructed :', responseBody)
            return responseBody
        
        
    @staticmethod
    def constructAddRecipientPayload(userType, numberOfUsers, customTags):
        payload = {}
        schema = 'firstName,lastName,' + str(userType)
        tagsForUsers = ''
        listOfUsers = []
        for tags in range(1, customTags + 1):
            schema = schema + ',' + str('customTag' + str(tags))
            tagsForUsers = tagsForUsers + ',' + 'tag' + str(tags) 
        for eachUser in range(numberOfUsers):
            listOfUserType = userType.split(',')
            firstName = 'Test' + str(eachUser)
            lastName = 'Automation' + str(eachUser)
            mobile = None
            email = None
            for eachUserType in listOfUserType:
                if eachUserType.lower() == 'mobile':
                    mobile = randValues.getRandomMobileNumber()
                elif eachUserType.lower() == 'email':
                    email = randValues.randomEmailId()
            userDataToAppend = firstName + ',' + lastName 
            for eachUserType in userType.split(','):
                if eachUserType == 'mobile' : userDataToAppend = userDataToAppend + ',' + mobile
                if eachUserType == 'email' : userDataToAppend = userDataToAppend + ',' + email
            userDataToAppend = userDataToAppend + tagsForUsers
            listOfUsers.append(userDataToAppend)
                
        payload['dataSource'] = 'CSV'
        payload['schema'] = schema
        payload['data'] = listOfUsers
        
        return payload
    
    @staticmethod
    def constructAddRecipientPayloadForOldUsers(userType, numberOfUsers, customTags):
        Logger.log('Constructing Payload with Existing Users')
        payload = {}
        schema = 'firstName,lastName,' + str(userType)
        tagsForUsers = ''
        listOfUsers = []
        userType = userType.split(',')
        usersInfo = dbCallsMessage.getUsersInformation(numberOfUsers)
        for tags in range(1, customTags + 1):
            schema = schema + ',' + str('customTag' + str(tags))
            tagsForUsers = tagsForUsers + ',' + 'tag' + str(tags)
        for eachUser in usersInfo:
            userData = {'userid' : eachUser[0], 'firstname' :eachUser[1], 'lastname':eachUser[2], 'mobile':eachUser[3], 'email':eachUser[4], 'externalid' :eachUser[5]}
            dataConstructed = str(userData['firstname']) + ',' + str(userData['lastname'])
            for type in userType:
                dataConstructed = dataConstructed + ',' + str(userData[type.lower()])
            
            dataConstructed = dataConstructed + tagsForUsers
            listOfUsers.append(dataConstructed)
            dataConstructed = ''
            
        payload['dataSource'] = 'CSV'
        payload['schema'] = schema
        payload['data'] = listOfUsers
        Logger.log('Payload Constructed is :', payload)
        return payload
            
    @staticmethod
    def constructMergeListBody(userType, numberOfUsers, customTags, newUser):
        payload = {}
        if newUser :
            addRecipientsRequest = construct.constructAddRecipientPayload(userType, numberOfUsers, customTags)
        else:
            addRecipientsRequest = construct.constructAddRecipientPayloadForOldUsers(userType, numberOfUsers, customTags)
        payload['recipients'] = addRecipientsRequest
        payload['name'] = 'IRIS_MERGE_LIST_' + str(int(time.time() * 100000))
        payload['customTagCount'] = customTags
        payload['groupTags'] = []
        return payload
    
    @staticmethod
    def constructCreateMessageBody(listId, channel, scheduleType, incentives, systemDefault):
        payload = {}
        payload['channel'] = channel
        payload['schedule'] = construct.constructScheduleForCreateMessage(scheduleType)
        payload['listId'] = listId
        # payload['storeType'] = 'REGISTERED_STORE'
        if incentives[0].lower() != 'plain': payload['incentive'] = construct.constructIncentivesForCreateMessage(incentives)
        if channel.lower() == 'sms' : 
            payload['message'] = constant.irisMessage[channel.lower()][incentives[0].lower()]
            payload['senderDetails'] = construct.constructSendersDetailForCreateMessage(systemDefault)
            payload['additionalInfo'] = {'targetNdnc': False, 'useTinyUrl': False}
        if channel.lower() == 'wechat' : 
            payload['message'] = construct.constructWechatMessageBody(incentives[0].lower())
            payload['accountDetails'] = construct.constructAccountDetails()
        if channel.lower() == 'email' :
            pass
        if channel.lower() == 'mobilepush' :
            pass
        return  payload

    @staticmethod
    def constructWechatMessageBody(incentives):
        messageBody = {}
        messageBody['template_id'] = constant.config['templateId']
        messageBody['touser'] = '{{wechat_open_id}}'
        messageBody['OriginalId'] = constant.config['wechat']['OriginalId']
        messageBody['Title'] = constant.config['templateTitle']
        messageBody['BrandId'] = 'brandX'
        messageBody['url'] = 'https://www.capillarytech.com/'
        messageBody['isUrlInternal'] = True
        messageBody['TopColor'] = '#000000'
        messageBody['data'] = construct.constructWechatmessageData(incentives)
        return messageBody
    
    @staticmethod
    def constructWechatmessageData(incentives):
        data = constant.irisMessage['wechat'][incentives]
        length = constant.config['templateSize']
        messageData = {"first": {"value": data[0] + data[1], "color": "#00000"}}
        indexOfData = 2;
        if len(data) > length:
            distributeCount = len(data) / length
        else:
            distributeCount = 1
        for i in range(length):
            if (indexOfData + distributeCount) < len(data):
                value = ''
                for l in range(distributeCount):
                    value = value + data[indexOfData + l]
                messageData.update({"keyword" + str(i + 1): {"value": value, "color": "#00000"}})
                indexOfData += distributeCount
            elif (i == (length - 1) and indexOfData != len(data)):
                messageData.update({"keyword" + str(i + 1): {"value": str(data[indexOfData:]), "color": "#00000"}})
            else:
                messageData.update({"keyword" + str(i + 1): {"value": "{test_tag}", "color": "#00000"}})

            messageData.update({"remark": {"value":  data[3], "color": "#00000"}})
        constant.config['templateData'] = messageData
        return messageData
        
    @staticmethod
    def constructAccountDetails():
        if constant.config['cluster'] in ['nightly']:
            accountDetails = {}
            accountDetails['appId'] = constant.config['wechat']['appId']
            accountDetails['appSecret'] = constant.config['wechat']['appSecret']
            accountDetails['originalId'] = constant.config['wechat']['OriginalId']
            return accountDetails
    
    @staticmethod
    def constructSendersDetailForCreateMessage(systemDefault):    
        sendersDetailDict = {}
        sendersDetailDict['useSystemDefaults'] = systemDefault
        sendersDetailDict['gsmSenderId'] = constant.config['message_senders']['gsmSenderId']
        sendersDetailDict['cdmaSenderId'] = constant.config['message_senders']['cdmaSenderId']
        if systemDefault == False:
            sendersDetailDict['domainGatewayMapId'] = constant.config['message_senders']['domainGatewayMapId']
        return sendersDetailDict
  
    @staticmethod
    def constructIncentivesForCreateMessage(incentives):
        incentivesDict = {}
        if incentives[0].lower() == 'coupons':
            incentivesDict['type'] = 'COUPONS'
            incentivesDict['voucherSeriesId'] = incentives[1]
        elif incentives[0].lower() == 'points':
            strategy = construct.constructStrategyIds()
            incentivesDict['type'] = 'POINTS'
            incentivesDict['programId'] = str(strategy['programeId'])
            incentivesDict['allocationStrategyId'] = str(strategy['allocationStrategyId'])
            incentivesDict['expirationStrategyId'] = str(strategy['expirationStrategyId'])
        elif incentives[0].lower() == 'generic':
            incentivesDict['type'] = 'GENERIC'
            if len(incentives) == 2:
                incentivesDict['genericIncentiveId'] = incentives[1]
            else:
                incentivesDict['genericIncentiveId'] = 1
        return incentivesDict  
          
    @staticmethod
    def constructStrategyIds():
        programeId = dbCallsMessage.getProgrameId()
        allocationStrategyId = dbCallsMessage.getAllocationIdForPrograme(programeId)
        expirationStrategyId = dbCallsMessage.getExpiryIdForPrograme(programeId)
        return {'programeId':programeId, 'allocationStrategyId':allocationStrategyId, 'expirationStrategyId':expirationStrategyId}
        
    @staticmethod
    def constructScheduleForCreateMessage(scheduleType):
        scheduleDict = {}
        if scheduleType[0].lower() == 'immediate':
            scheduleDict['type'] = 'IMMEDIATELY'
        elif scheduleType[0].lower() == 'particulardate':
            scheduleDict['type'] = 'PARTICULAR_DATE'
            if len(scheduleType) == 1: scheduleDict['datetime'] = int(time.time() * 1000) + 100 * 1000
            if len(scheduleType) == 2: scheduleDict['datetime'] = int(scheduleType[1])
        elif scheduleType[0].lower() == 'recurring':
            scheduleDict['type'] = 'RECURRING'
            if len(scheduleType) == 1:
                timeToExecuteRecurringCampaign = int(time.time() * 1000 + 100 * 1000)
                dateTime = datetime.datetime.fromtimestamp(timeToExecuteRecurringCampaign / 1000)
                listOfWeekDays = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
                scheduleDict['pattern'] = construct.constructRecurringPattern(dateTime.strftime("%H"), dateTime.strftime("%M"), dateTime.strftime("%d"), listOfWeekDays.index(str(dateTime.strftime("%A"))), dateTime.strftime("%m"))
            else:
                scheduleDict['pattern'] = construct.constructRecurringPattern(scheduleType[1], scheduleType[2], scheduleType[3], scheduleType[4], scheduleType[5])
        else:
            Logger.log('Schedule type :{} is not defined with us'.format(scheduleType[0]))
        return scheduleDict
         
    @staticmethod
    def constructRecurringPattern(hours, minutes, day, week, month):
        recurringPattern = {}
        recurringPattern['day'] = day
        recurringPattern['week'] = week
        recurringPattern['month'] = month
        recurringPattern['hours'] = hours
        recurringPattern['minutes'] = minutes
        return recurringPattern
          
    @staticmethod
    def constructGetCampaignAllToGetCampaignIdResponse(getCampaignResponse):
        listOfAllCampaignInSpecificFormat = []
        allCampaigns = getCampaignResponse['json']['data']
        for eachCampaignjson in allCampaigns:
            responseBody = {'constructed':'pass', 'statusCode':200, 'encoding':'UTF-8', 'text':str(eachCampaignjson), 'json':{'entity':eachCampaignjson}}
            campaignId = eachCampaignjson['id']
            listOfAllCampaignInSpecificFormat.append((campaignId, responseBody))
        Logger.log('Response Constructed as required in specific format :', listOfAllCampaignInSpecificFormat)
        return listOfAllCampaignInSpecificFormat

    @staticmethod
    def resetCampaignDefaultObject():
        Logger.log('Reset The Campaign Default Object')
        constant.campaignDefaultValues = copy.deepcopy(constant.config['campaignDefaultObjectCopy'])
        
    @staticmethod
    def updateOrgId(orgId):
        workingOrgId = constant.config['orgId']
        constant.config.update({'orgId':orgId})
        return workingOrgId
    
    @staticmethod
    def updateOrgName(orgName):
        workingOrgName = constant.config['orgName']
        constant.config.update({'orgName':orgName})
        return workingOrgName
    
    @staticmethod
    def updateAuthenticate(authUser='admin'):
        if constant.config['authentication'][authUser.lower()] != None:
            constant.config['intouchUsername'] = constant.config['authentication'][authUser.lower()]['username']
            constant.config['intouchPassword'] = constant.config['authentication'][authUser.lower()]['password']
            return True
        else:
            raise Exception('Auth User :{} not Found in Constants'.format(authUser))
