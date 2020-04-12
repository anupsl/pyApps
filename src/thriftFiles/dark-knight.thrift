#!thrift -java -php

namespace java in.capillary.ifaces.darknight
namespace php darknight 

enum JobStatus {PROCESSING, COMPLETED, FAILED, INQUEUE, SUBMITTED, NEW_JOB}
enum JobPriority { BULK = 1, TRANS = 2, CAMPAIGN =3 }
enum WChannel{ EMAIL = 1 }

struct JobInfo {
	1: required i64 jobID;
	2: required JobStatus jobStatus;
	3: required i64 expectedCount;
	4: required i64 processedCount;
	5: optional i64 queuedTime;
	6: optional i32 batchCount;
	7: optional i64 createdTime;
	9: optional WChannel channel;
	10: optional JobPriority priority;
	11: optional string clientId;
	12: optional string routingKey;
	13: required string errorDetail;
	14: required i32 errorCode;
        15: required i32 orgID;
        16: optional i64 clientContextId;
        17: optional string clientTypeId;
}

struct NewJobRequest {
	1: required i64 totalCount;
	2: required string createdTime;
	3: optional WChannel channel;
	4: optional JobPriority priority;
	5: optional string clientId;
	6: optional string routingKey;
        7: required i32 orgID;
        8: optional i64 clientContextId;
        9: optional string clientTypeId;
}

enum EmailGatewayStatusEnum { HARD_BOUNCED, SOFT_BOUNCED, DELIVERED, UNKNOWN, FAILED }

enum EmailStatusEnum { VALID, INVALID, UNKNOWN, NOT_PROCESSED }

enum VerifierTypeEnum { ROBIN, BRITE, GATEWAY, NONE }

struct EmailGatewayStatus {
	1:string emailID;
	2:EmailGatewayStatusEnum emailGatewayStatusEnum;
	3:i64 last_checked_date;
	4:string reason;
}



struct EmailStatus {
	1:EmailStatusEnum emailStatusEnum;
	2:VerifierTypeEnum verifierTypeEnum;
	3:i32 hardBounceCount;
	4:i32 softBounceCount;
	5:i32 successCount;
	6:i32 failedCount;
	7:i64 lastSuccessOn;
	8:i64 lastFailedOn;
	9:i64 lastStatusChanged;
	10:string emailID;
}


exception DarknightException {
  1:string what
  2:string where
  3:i32 exceptionCode
}


service DarknightService {

	JobInfo createNewJob(1:NewJobRequest jobReq, 2:string requestID) throws (1:DarknightException dex)
	
	#returns the status of the info
	JobInfo getJobStatus(1:i64 jobID, 2:string requestID) throws (1:DarknightException dex)

	#to update status on the basis of email gateway response 
	bool updateEmailStatus(1:list<EmailGatewayStatus> emailStatusList, 2:string requestID) throws (1:DarknightException dex)

	list<EmailStatus> getEmailStatus(1:list<string> emailIDs, 2:string requestID) throws (1:DarknightException dex)

	map<string,bool> getMobileStatus(1:list<string> mobileNumbers,2:i64 orgId ,3:string requestID) throws (1:DarknightException dex)
	
	list<EmailStatus> getEmailStatusWithReporting(1:i32 orgId, 2:map<string,list<i64>> userEmailMap, 3:string requestID) throws (1:DarknightException dex)
	bool isAlive()
}
