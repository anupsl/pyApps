/*
	Veneno Interface
*/
#include "../capillarybase_thriftservice.thrift"
namespace java com.capillary.veneno
namespace php veneno

enum CommunicationType {
  SMS = 1,
  EMAIL = 2,
  CALL_TASK = 3,
  WECHAT = 4,
  PUSH = 5,
  ANDROID = 6,
  IOS = 7,
  FACEBOOK = 8,
  GOOGLE = 9,
  TWITTER = 10,
  LINE = 11
}

enum TargetType {
  GROUPED = 1,
  TIMELINE = 2,
  EXPIRY_REMINDER = 3,
  SOCIAL = 4
}

struct CommunicationDetail {
  1:  optional i32		 id
  2:  required i32		 orgId			//org id of the msg
  3:  required string 		 guid			//unique id
  4:  required string 		 subject		//subject line
  5:  required string 		 body			//body of the msg
  6:  required i32  		 priority		
  7:  required string 		 defaultArguments
  8:  required string		 messageProperties	
  9:  required CommunicationType communicationType 	//SMS or EMAIL type	
  10: required TargetType 	 targetType		//type of recipients; supporting only grouped for now
  11: required string		 receivedTime
  12: required i32		 campaignId
  13: required i32		 recipientListId
  14: required i32 		 expectedDeliveryCount 
  15: optional i32		 queuedBy		 
  16: optional string		 lastUpdatedOn
  17: optional i32		 lastUpdatedBy
  18: required string		 groupName
  19: required i32		 overallRecipientCount
  20: optional i32		 message_queue_id
}

struct EmailBody {
  1: required string 	body;
  2: required i32 	orgId;
  3: optional i32 	messageId; 
  4: required i32 	recipientId;
  5: optional string 	resolvedTags;
  6: optional string 	createdTime;
  7: optional string 	retrievedTime;
  8: required bool 	isPresent;
  9: required string 	subject;
}

struct BucketDetails{
  1: required i32 	messageID;
  2: required i32 	bucketID;
  3: required string 	dbHostName;
  4: required string 	dbUsername;
  5: required string 	dbPassword;
  6: required string 	databaseName;
}

struct CampaignReplayStats {
  1: required i32	id;
  2: required i32       messageID;
  3: required i64	receivedTime;
  4: required i64 	pickedTime;
  5: required i32       skippedCount;
  6: required list<i32>    skippedErrors;
}

struct ErrorDetails {
  1: required i32 errorId;
  2: required string errorDescription;
  3: required i32 errorCount;
}

struct SkippedMessageWithErrorDetails {
  1: required i64 messageId;
  2: required list<ErrorDetails> errorDetailsList;
}

struct MessageIdValidationForReplay { 
  1: required bool isReplayable;
  2: required string reason;
}

exception VenenoException {
  1: string message
}

service VenenoService /*extends capillarybase_thriftservice.CapillaryBaseThriftService*/ {

  i32 addMessageForRecipients(1:CommunicationDetail messageDetails, 2: string serverRequestID ) throws (1:VenenoException ex)
 
  i32 replayMessageForRecipients(1:i32 messageId, 2:CampaignReplayStats campaignReplayStats 3: string serverRequestID ) throws (1:VenenoException ex)

  i32 getSkippedCount(1:i32 messageId, 2:list<i32> skippedErrors, 3:string serverRequestID ) throws (1:VenenoException ex)  

  i32 isErrorsValidForReplay(1:list<i32> skippedErrors, 2:string serverRequestID) throws (1:VenenoException ex)	
 
   MessageIdValidationForReplay isMessageIdReplayable(1:i64 orgId, 2:i64 campaignId, 3:i64 messageId, 4:string serverRequestID ) throws (1:VenenoException ex)

  list<SkippedMessageWithErrorDetails> getReplayableMessageIdsWithErrorDetails(1:i64 campaignId, 2:i64 orgId, 3: string serverRequestID) throws (1:VenenoException ex) 

  EmailBody getMessageBody(1:i32 userId, 2:i32 outboxId , 3: string serverRequestID ) throws (1:VenenoException ex)
  
  string replaceTemplate(1:i32 userId, 2:i32 orgId, 3:string template, 4:string arguments , 5: string serverRequestID ) throws (1:VenenoException ex)
  
  string getStatus( 1: string serverRequestID ) throws (1:VenenoException ex)

  bool pauseMessage(1:CommunicationDetail messageDetail , 2:string serverRequestID ) throws (1:VenenoException ex)

  BucketDetails getBucketDetailsByMessageID(1: i32 messageID , 2: string serverRequestID ) throws (1:VenenoException ex)

  bool updateInboxDeliveryStatus(1: i32 messageID, 2: string deliveryStatus, 3: string serverRequestID) throws (1:VenenoException ex)
 
  bool updateUserUnsubscriptionStatus(1: i32 orgId, 2: i32 messageId, 3: i32 recipientId, 4: string requestId) throws (1: VenenoException ex)

  bool isAlive();

}

service VenenoCommonService /*extends capillarybase_thriftservice.CapillaryBaseThriftService*/ {

 bool pauseMessage(1:i32 msgId , 2: string serverRequestID ) throws (1:VenenoException ex)
 
 bool isAlive();
}