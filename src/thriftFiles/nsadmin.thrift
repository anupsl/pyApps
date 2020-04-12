#!thrift -java -php

/*
   NSAdmin interface
   Author: Abhinav Sarkar
   Last modified: 01-Dec-2011
*/

namespace java in.capillary.ifaces.nsadmin
namespace php nsadmin

enum MobilePushCtaLink {
  DEEP_LINK, EXTERNAL_URL
}

struct MobilePushCta {
  1: string actionLink
  2: MobilePushCtaLink type
}

struct MobilePushCarouselItem {
  1: MobilePushCta action
  3: string imageUrl
}

struct MobilePushNotification {
  1: string title
  2: string text
  3: optional string imageUrl
  4: optional MobilePushCta primaryCta
  5: i64 timestamp
  6: optional list<MobilePushCarouselItem> carousel
}

struct Message {
  1:i64		messageId
  2:i64		clientId
  
  # for Email this is the title, for SMS the message itself.
  3:string	message
  
  # enum('SMS', 'EMAIL','WECHAT')
  4:string messageClass
  
  # For incoming messages, this is phone number or email of gateway reciveing this.
  # For outgoing messages, this is phone number or email of target user.           
  # For Emails, this is a comma separated list of "Name" <email@address>            
  5:string receiver
    
  6:i64 receiverId;
  # For incoming messages, this is phone number or email of external user.          
  # For outgoing messages, this is phone number or email of gateway sending this.   
  # For outgoing messages, if not set, gateway will put appropriate value.          
  # For Emails, this is a comma separated list of "Name" <email@address>,  ....           
  7:optional string sender
  
  8:i64 sendingOrgId
  
  # optional values for SMS
  9:optional string gsmSenderId;
  10:optional string cdmaSenderId;
  
  # enum('DEFAULT', 'HIGH')
  11:string priority;
  12:bool truncate;

  # optional values for email (for the main sender, we use sender(12), for receivers receiver(11)
  13:optional string ccList;
  14:optional string bccList;
    
  # main body of the email
  16:optional string body;

  # scheduled time for sending
  17:optional i64 scheduledTimestamp;
  
# optional id of the inbox entry in msging
  18:optional i64 inboxId;
  
  19:optional i32 relevanceInterval;
  
  20:optional i32 deliveryCheckInterval;

  21:optional list<string> tags;
  # We are over riding the gateway to be used 
  # If not set nsadmin will use its own gateway
  # selection algorithm
  22:optional string gateway;

  #set this field if the message has to be transferred immediately.. The 
  #nsadmin will pick the messages from the messages table which have is_immediate
  #set as true.
  23:optional bool immediate;
  
  #Set this field if a file has to be attached with the outgoing email
  24:optional list<i64> attachmentId;
  
  25:optional i64 campaignId;
  26:optional bool ndnc;
  27:optional i64 sentTimestamp;
  28:optional i64 receivedTimestamp;
  29:optional i64 deliveredTimestamp;
  30:optional string status;
  31:optional i64 clientContextId;
  32:optional i64 originTimestamp;
  33:optional string requestId;
  34:optional list<string> fileHandle;
  35:optional string sendError;
  36:optional string messageSubClass;
  37:optional map<string,string> additionalHeaders;
  
  # Alternate body of the email
  38:optional string altBody;

  39:optional MobilePushNotification mobilePushNotification;
  40:optional i64 userId;
}

struct MessageInternal   {
  1:i64 messageId;
  2:string messageClass;
  3:string receiver;
  4:i64 sendingOrgId;
  5:string priority;
  6:optional i64 inboxId;
  7:optional list<string> tags;
  8:optional string gateway;
  9:optional i64 campaignId;
  10:optional bool ndnc;
  11:optional string status;
  12:optional i64 receivedTimestamp;
  14:optional string notes;
  15:optional string ccList;
  16:optional string error;
  17:optional string sendError;
  18:optional i64 clientId;
  19:optional string bccList;
  20:optional string requestId;
  21:optional string messageSubClass;
  22:optional map<string,string> additionalHeaders;
}

exception NSAdminException {
  1:string what
  2:string where
}

enum SummarySelectCriteria {
  SENDING_ORG_ID, MESSAGE_PRIORITY, GATEWAY, DATE, MESSAGE_CLASS, MESSAGE_STATUS, FAILURE_REASON, GTW_NOT_FOUND_REASON, CAMPAIGN_ID
}

enum MessageClass { SMS, EMAIL, WECHAT, ANDROID, IOS, VOICECALL, LINE }

struct SummaryCriteria {
  1:optional i64 sendingOrgId;
  2:optional string messagePriority;
  3:optional string gateway;
  4:optional i64 fromDate;
  5:optional i64 toDate;	
  6:optional string messageClass;
  7:optional string messageStatus;
  8:optional i64 campaignId;
  9:optional i32 clientId;
  10:list<SummarySelectCriteria> selectFields;
}

struct OrgCreditDetails {
  1:i64 orgId;
  2:optional i32 valueCredits;
  3:optional i32 bulkCredits;
  4:optional i32 userCredits;
  5:optional i64 addedBy;
  6:optional i64 bulkCreditsThreshold;
  7:optional i64 valueCreditsThreshold;
  8:optional MessageClass messageClass;
  9:optional i64 lastUpdatedBy;
  10:optional i64 lastUpdatedAtTimestamp;
  11:optional string comments;
}

struct OrgGateway {
  1:i64 id;
  2:i64 orgId;
  3:string gateway;
  4:double weight;
  5:i64 campaignId;
  6:i64 effectiveStartTimestamp
  7:i64 effectiveEndTimestamp
  8:i64 addedBy;
  9:i64 addedOnTimeStamp;
  10:bool isdefault;
  11:bool valid;
  12:string messagePriority;
  13:bool isWhitelistingGateway;
  14:optional string serviceIp;
  15:optional string subscriptionParameters;
  16:optional string messageClass;
}

struct Gateway {
  1:i64 id;
  2:string hostName;
  3:string shortName;
  4:string fullName; 
  5:string username;
  6:string password;
  7:string connectionProperties;
  8:string serviceUrl;
  9:string statusCheckUrl; 
  10:string messageClass;
  11:string messagePriority;
  12:i32 channelCount;
  13:string status;
  14:string statusCheckType;
  15:string properties;
}

#Active inactive gateway based spam management

struct GatewayOrgConfigs {
  1:i64 id;
  2:i64 orgId;
  3:string hostName;
  4:string shortName;
  5:string fullName;
  6:string username;
  7:string password;
  8:string connectionProperties;
  9:optional string serviceIp;
  10:string serviceUrl;
  11:string statusCheckUrl;
  12:string messageClass;
  13:string messagePriority;
  14:i32 channelCount;
  15:string status;
  16:string statusCheckType;
  17:string properties;
  18:i64 startTimestamp
  19:i64 endTimestamp
}

struct ContactInfo {
  1: i64 id;
  2: optional i64 domainPropId = -1;
  3: i64 orgId;
  4: string messageClass;
  5: string type;
  6: string label;
  7: string value;
  8: string description;
  9: optional bool isValid = false;
  10: optional bool isDefault = false;
}

struct DomainProperties {
  1: i64 id;
  2: i64 orgId;
  3: string domainName;
  4: string description;
  5: list<ContactInfo> contactInfo;
}

struct DomainPropertiesGatewayMap{
  1: i64 id;
  2: i64 orgId;
  3: GatewayOrgConfigs gatewayOrgConfigs;
  4: DomainProperties domainProperties;
  5: i64 domainPropertiesId;
  6: optional string label;
  7: optional string subDomain;
  8: required i64 addedBy;
  9: required i64 addedOn;
  10: optional bool useSystemDefaults = true;
  11: optional bool isValidated = false;
  12: optional bool useForInactive = false;
  13: required i32 priority;
  14: optional string properties;
  15: optional i64 updatedBy = -1;
  16:optional i64 lastValidatedOn;
  17: optional string validationInfo;
  18: optional bool isActive;
}

enum SendingRule {
  ALL, NOBULK, NOPERSONALIZED, NONE, UNSUBSCRIBE, NULL
}

enum EmailState {
  OPENED, CLICKED, HARD_BOUNCED, SOFT_BOUNCED
} 

enum DeliveryStatus { DELIVERED, NOT_DELIVERED, HARD_BOUNCED, SOFT_BOUNCED, OPENED, CLICKED, MARKED_SPAM, IN_GTW, GTW_PROCESSED, FAILED}

enum MessageSubClass { TEXT_WECHAT, RICH_MEDIA_WECHAT, TEMPLATE_WECHAT }

struct MessageDeliveryReceipt {
 1:string msgRefId;
 2:i64 msgId;
 3:string receiver;
 4:DeliveryStatus status;
 5:string response;
 6: optional i64 deliveredTime;
 7: optional string failureReason;
 8: optional MessageClass messageClass;
}

struct EmailStatusInfo {
 1:string emailId
 2:i64 campaignId
 3:i64 inboxId
 4:EmailState status
}

struct SendingRuleDetails {
 1:string receiver
 2:i64 orgId
 3:SendingRule rule
 4:MessageClass messageClass
}

enum EnumBoolean { YES, NO, DEFLT }

struct OrgStatusDetails {
  1:i64 orgId
  2:bool active
  3:optional i64 rateLimitThreshold
  4:i64 updatedBy
  5:i64 updatedAtTimestamp
  6:optional EnumBoolean customSenderAdded = EnumBoolean.DEFLT
}

struct GatewayConfig {
  1:string hostanme
  2:string configs
}

enum AppConfigType { FIXED, DYNAMIC }

struct ApplicationConfig {
  1: string name
  2: optional string label
  3: string value
  4: AppConfigType type
}

struct EmailGatewayConfig { 
  1: i32 id
  2: string shortName
  3: string username
  4: string password
  5: i64 addedOn
}

struct QueueConfig {
  1: i32 id
  2: string exchangeName
  3: string queueName
  4: string queueType
  5: string properties
  6: bool isActive
  7: i64 createdOn
}

struct CampaignRequest{
  1: i32 orgId
  2: i32 campaignId
}

struct DLRRequest {
  1: string response
  2: string handler
  3: optional string messageClass
}

struct MessageDeliveryStatus{
  1: string receiver;
  2: string messageClass;
  3: i64 deliveredTime;
  4: DeliveryStatus deliveryStatus; 
}

exception CreditManagementException {
	1: string what
	2: string where
}

exception RequestParamaterException {
	1: string parameter
	2: string reason
}

exception NotImplementedException {
	1: string reason
}

enum PriorityType { HIGH, BULK }

enum TransactionType { ADDED, REMOVED }

struct SMSChannelDetails {
  1: i32 countryCode
  2: optional string countryName
}

struct ChannelSpecificParams {
	1: optional SMSChannelDetails smsChannelDetails
}

struct CommonChannelParams {
	1: MessageClass messageClass
	2: optional PriorityType priorityType
	3: ChannelSpecificParams channelSpecificParams
}

struct CreditDetailsResponse {
	1: bool status
	2: double credits
}

struct CreditRatesParams {
	1: optional i64 orgId
	2: CommonChannelParams commonChannelParams
	3: double creditRate
	4: optional double previousCreditRate
	5: optional double nextDateCreditRate
	6: optional i64 effectiveDate
	7: optional i64 expiryDate
	8: optional string comments
	9: optional i64 createdBy
	10: optional i64 createdDate
}

struct CreditChunkParams {
	1: optional i32 chunkId
	2: optional string orderNumber
	3: optional double creditCount
	4: optional i64 expiryDate
	5: optional string comments
}

# only for ADDED and REMOVED transactions
struct OrgTransactionDetails {
	1: i64 orgId
	2: i64 transactionDate
	3: double creditCount
	4: TransactionType transactionType
	5: i64 chunkId
	6: optional string orderNumber
	7: optional i64 expiryDate
	8: optional string comments
	9: i64 createdBy
}

struct OrgTransactionRequest {
	1: i64 orgId
	2: optional i64 startDate
	3: optional i64 endDate
}

struct OrgCreditBalanceResponse {
	1: i64 orgId
	2: double orgCreditBalance
	3: double orgThresholdCredits
}

struct CreditEstimationRequest {
    1: CommonChannelParams commonChannelParams
    2: i64 messageCount
}

service NSAdminService {
	bool isAlive()
	i64 sendMessage(1:Message message) throws (1:NSAdminException ex)
	map<i64, i64> sendMultipleMessages(1:list<Message> messages) throws (1:NSAdminException ex)
	string getStatus() throws (1:NSAdminException ex)
	map<string,double> chooseGateways(1:Message message) throws (1:NSAdminException ex)
	bool disableOrgGatewaysById(1:i64 orgGatewayId) throws (1:NSAdminException ex)
	bool disableOrgGatewayByOrgId(1:i64 orgId, 2:list<string> priority) throws (1:NSAdminException ex)
	bool addOrgGateways(1:list<OrgGateway> orgGateways) throws (1:NSAdminException ex)
	bool addGateway(1:Gateway gateway) throws (1:NSAdminException ex)
	bool addCredits(1: OrgCreditDetails creditDetails) throws (1:NSAdminException ex)
	bool setWhitelistingGateway(1:i64 orgId, 2:string short_name) throws (1:NSAdminException ex)

	#updates the message's delivery status in messages and msg_out table based on the reference id
	bool reportMessageDelivered(1:string msgRefId, 2:string receiver, 3:string status, 4:string response) throws (1:NSAdminException ex)
	#updates the message's delivery status in messages and msg_out table based on the NSadmin id
	bool reportMessageDeliveredById(1:i64 messageId, 2:string receiver, 3:string status, 4:string response) throws (1:NSAdminException ex)
	#updates the delivery status of a bunch of messages whose reference/nsadmin id is mentioned in the delivery receipts
	bool reportMessagesDelivered(1:list<MessageDeliveryReceipt> deliveryReceipts) throws (1:NSAdminException ex)
	#returns true if the status of the message with the id provided is "Delivered"
	bool isMessageDelivered(1:i64 messageId) throws (1:NSAdminException ex)


	bool reportMessageSent(1:i64 messageId, 2:string sentTime) throws (1:NSAdminException ex)
	map<string,i32> getSummary(1:SummaryCriteria criteria) throws (1:NSAdminException ex)
	#returns the credit details for the requested org id
	OrgCreditDetails getCreditDetails(1:i64 orgId) throws (1:NSAdminException ex)
	#returns the message details for the list of provided nsadmin ids
	list<Message> getMessagesById(1:list<i64> messageIds) throws (1:NSAdminException ex)
	list<Message> getMessageLogs(1:i64 orgId, 2:string messageClass, 3:string receiver) throws (1:NSAdminException ex)
	list<Message> getSentMessages(1:i64 orgId, 2:string messageClass, 3:i64 startSentTime, 4:i64 endSentTime, 5:string priority, 6:i64 limit) throws (1:NSAdminException ex)
	list<Message> getMessagesByReceiver(1:i64 orgId, 2:string receiver) throws (1:NSAdminException ex)
        list<Message> getMessagesByUserOrReciever(1:i64 orgId, 2:string userId 3:string receiver) throws (1:NSAdminException ex)
	void updateMessageStatus(1:i64 orgId, 2:string status, 3:i64 campaignId, 4:i64 startSentTime, 5:i64 endSentTime, 6:string priority) throws (1:NSAdminException ex)
	#returns credit transactions log for a particular org id
	list<OrgCreditDetails> getCreditsLog(1:i64 orgId) throws (1:NSAdminException ex)
	#marks the particular email in the email_status table with the provided details + updates the status for messageId provided in the messages table
	oneway void updateBouncedEmailStatus(1:string email, 2:EmailState status, 3:i64 bouncedTime, 4: i64 messageId)
	#updates the status(Eg.OPENED, CLICKED) of emails in the messages & msg_out table
        void updateEmailStatus(1:list<EmailStatusInfo> emailStatuses) throws (1:NSAdminException ex)

	#whitelists the email ids so that emails to this receiver wont be blocked since it had bounced earlier
	bool whitelistEmailIds(1:list<string> emailIds)
	#returns the reason for message failure
	string getMessageSendError(1:i64 messageId) throws (1:NSAdminException ex)


	SendingRule getSmsSendingRule(1:string mobile, 2:i64 orgId) throws (1:NSAdminException ex)
	SendingRule getEmailSendingRule(1:string email, 2:i64 orgId) throws (1:NSAdminException ex)

	bool resubscribeToEmail(1:string email, 2:i64 orgId) throws (1:NSAdminException ex)
        bool resubscribeToSms(1:string mobile_number, 2:i64 orgId) throws (1:NSAdminException ex)
	#depending on the messageClass(SMS, EMAIL, WECHAT) the receiver of the sms/email_sending_rule table will be updated with the new receiver
	#returns true on success

	list<OrgGateway> getOrgGatewaysById(1:list<i64> orgGatewayIds) throws (1:NSAdminException ex)
	list<OrgGateway> getValidOrgGateways(1:list<i64> orgId) throws (1:NSAdminException ex)
	list<OrgGateway> getAllValidOrgGateways(1:string priority) throws (1:NSAdminException ex)
	list<Gateway> getGateways(1:i64 gatewayId) throws (1:NSAdminException ex)
	Gateway getGateway(1:string shortName) throws (1:NSAdminException ex)
	list<string> getActiveGatewayShortNames() throws (1:NSAdminException ex)
        list<string> getAllActiveGatewayShortNames() throws (1:NSAdminException ex)
	list<i32> getSummaryAvailableCampaigns(1:i64 orgId)  throws (1:NSAdminException ex)

	bool updateOrgStatus(1:OrgStatusDetails orgStatusDetails) throws (1:NSAdminException ex)

  bool resetCacheForOrg(1:i64 orgId) throws (1:NSAdminException ex)

	EmailGatewayConfig getEmailGatewayConfig(1:string shortName) throws (1:NSAdminException ex)

	bool reloadGateway(1:string shortName) throws (1:NSAdminException ex)

	list<QueueConfig> getAllActiveQueueConfig() throws (1:NSAdminException ex);
	bool addQueueConfig(1:QueueConfig queueConfig) throws (1:NSAdminException ex);
        void addGatewayConnConfig(1:string hostName, 2:string configs) throws (1:NSAdminException ex);
	list<string> getAllExchangeNames() throws (1:NSAdminException ex);
	map<string, list<string>> getQueueTypeToQueuesMapping() throws (1:NSAdminException ex);

	i32 reloadLoadDistribution(1:i32 newCommengineLoad) throws (1:NSAdminException ex);
	#calls made by admin console
	bool addGatewayFactoryConfig(1:GatewayConfig gatewayConfig) throws (1:NSAdminException ex)
	list<GatewayConfig> getGatewayFactoryConfigs(1:MessageClass messageClass) throws (1:NSAdminException ex)
	list<ApplicationConfig> getApplicationConfigs() throws (1:NSAdminException ex)
	bool updateApplicationConfig(1:ApplicationConfig config) throws (1:NSAdminException ex)
	bool reloadConfig() throws (1:NSAdminException ex)
        bool reloadGateways() throws (1:NSAdminException ex)
	bool isMaster() throws (1:NSAdminException ex)
        list<string> getCommEngineHosts() throws (1:NSAdminException ex)
        string getCommEngineMasterHost() throws (1:NSAdminException ex)
	#Active inactive gateway based spam management
	#this will be used in case of emails
	list<DomainProperties> getDomainPropertiesByOrg(1:i64 orgId)  throws (1:NSAdminException ex)
	DomainProperties getDomainPropertiesByID(1:i64 domainPropertiesId)  throws (1:NSAdminException ex)
	void updateDomainProperties(1:DomainProperties domainProperties) throws (1:NSAdminException ex)
	void insertDomainProperties(1:DomainProperties domainProperties) throws (1:NSAdminException ex)
	void disableDomainProperties(1:i64 domainPropsId, 2:i64 orgId) throws (1:NSAdminException ex)
	#only way through which the gateway_org_configs can be saved
	list<DomainPropertiesGatewayMap> getDomainPropertiesGatewayMapByOrg(1:i64 orgId, 2:MessageClass messageClass) throws (1:NSAdminException ex)
        DomainPropertiesGatewayMap getDomainPropertiesGatewayMapByID(1:i64 id)  throws (1:NSAdminException ex)
	void saveDomainPropertiesGatewayMap(1:DomainPropertiesGatewayMap domainPropertiesGatewayMap) throws (1:NSAdminException ex)
	void disableDomainPropertiesGatewayMap(1:i64 domainPropertiesGatewayMapId) throws (1:NSAdminException ex)
	#this will be used in case of sms, to directly fetch details
	list<ContactInfo> getSMSContactInfo(1:i64 orgId) throws (1:NSAdminException ex)
	DomainPropertiesGatewayMap validateDomain(1:i64 domainPropGatewayMapId, 2:i64 triggeredBy) throws (1:NSAdminException ex)
	#return updated count
	i64 replayCampaignMessage(1:i64 orgId, 2:i64 startSentTime, 3:i64 endSentTime, 4:string priority, 5:i64 campaignId, 6:i64 clientContextId, 7:string messageClass, 8:string gateway, 9:list<i32> status) throws (1:NSAdminException ex)

	i64 replayMessageByID(1:list<i64> messageIds, 2:list<i32> status) throws (1:NSAdminException ex)

  list<OrgGateway> getOrgGatewaysByCampaign(1:list<CampaignRequest> campaigns,  2:string requestId) throws (1:NSAdminException ex)

  list<Message> getLastNMobilePushMessages(1:i64 orgId, 2:string licenseCode, 3:string cuid, 4:list<string> communicationIds, 5:i32
  notificationCount)
  throws (1:NSAdminException ex)

  list<Message> getMobilePushMessages(1:i64 orgId, 2:string licenseCode, 3:string cuid, 4:string userId, 5:list<string> communicationIds, 6:i32 limit,7:i32 offset) throws (1:NSAdminException ex)

  bool addDomainGatewayMapForMobilePush(1:i64 orgId, 2:string licenseCode, 3:string authToken, 4:string campaignId, 5:string variationId) throws (1:NSAdminException ex)

  map<string, list<MessageDeliveryStatus>> getMessageDeliveryHistory(1:list<string> receiver, 2:string messageClass, 3:list<DeliveryStatus> deliveryStatus,  4:string requestId) throws (1:NSAdminException ex)

  void setConfigKeyValue(1:string configKey, 2:string configKeyValue, 3:i32 orgId, 4:i32 createdBy, 5:string requestId) throws (1:NSAdminException ex)

  string getConfigKeyValue(1:string configKey, 2:i32 orgId, 3:string requestId) throws (1:NSAdminException ex)

  OrgCreditDetails getCreditDetailsByOrgAndChannel(1:i64 orgId, 2:MessageClass messageClass, 3:string requestId) throws (1:NSAdminException ex)

	CreditDetailsResponse getOrgCreditRateForConfiguration(1:i64 orgId, 2:i64 date, 3:CommonChannelParams request) throws (1:CreditManagementException ex, 2:RequestParamaterException rpEx, 3:NotImplementedException niEx)

	list<CreditRatesParams> getOrgCreditRates(1:i64 orgId, 2:i64 date) throws (1:CreditManagementException ex)

	void setOrgCreditRates(1:i64 orgId, 2:list<CreditRatesParams> creditRatesParamList, 3:i64 createdBy) throws (1:CreditManagementException ex, 2:RequestParamaterException rpEx, 3:NotImplementedException niEx)

	void addOrgCredits(1:i64 orgId, 2:CreditChunkParams creditChunkParams, 3:i64 createdBy) throws (1:CreditManagementException ex, 2:RequestParamaterException rpEx)

	void removeOrgCredits(1:i64 orgId, 2:CreditChunkParams creditChunkParams, 3:i64 createdBy) throws (1:CreditManagementException ex, 2:RequestParamaterException rpEx, 3:NotImplementedException niEx)

	void updateOrgCreditChunk(1:CreditChunkParams creditChunkParams) throws (1:CreditManagementException ex, 2:RequestParamaterException rpEx, 3:NotImplementedException niEx)

	OrgCreditBalanceResponse getOrgCreditBalance (1:i64 orgId) throws (1:CreditManagementException ex)

	list<OrgTransactionDetails> getOrgTransactionDetails (1:OrgTransactionRequest orgTransactionRequest) throws (1:CreditManagementException ex)

	void setOrgThreshold (1: i64 orgId, 2: double thresholdCredits) throws (1:CreditManagementException ex)

	void setBrandPocDetails (1: i64 orgId, 2: list<i64> pocUserIds, 3: i64 createdBy) throws (1:CreditManagementException ex, 2:RequestParamaterException rpEx)

	void runCreditUtilization () throws (1:CreditManagementException ex, 2:RequestParamaterException rpEx)

	double getOrgCreditBalanceFromCache (1: i64 orgId) throws (1:CreditManagementException ex)

	list<i64> getBrandPocDetails (1: i64 orgId) throws (1:CreditManagementException ex)

	void enableCreditManagementForOrgs (1: list<i64> orgId) throws (1:CreditManagementException ex)

	bool isOrgCreditManagementEnabled (1: i64 orgId) throws (1:CreditManagementException ex)

	#CreditDetailsResponse getCreditEstimateForConfigurationList (1:i64 orgId, 2:i64 date, 3:list<CreditEstimationRequest> requestList)
	#	throws (1:CreditManagementException ex, 2:RequestParamaterException rpEx, 3:NotImplementedException niEx)
}

service NSAdminServiceInternal  {
	bool isAlive()
        string getStatus()
        void reloadConfig() throws (1:NSAdminException ex)
	void reloadGateway(1:string shortName) throws (1:NSAdminException ex)
        void reloadGateways() throws (1:NSAdminException ex)
	void stopGateway(1:string shortName) throws (1:NSAdminException ex)
	void recordMessagePending(1:MessageInternal message) throws (1:NSAdminException ex)
	void recordMessagesPending(1:list<MessageInternal> messages) throws (1:NSAdminException ex)
}
