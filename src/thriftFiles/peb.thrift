#!thrift -java -php -phps

/**
 * This file contains all the Points Engine Bulk (PEB) api service related classes and definitions.
*/

namespace java com.capillary.shopbook.peb.api.external

namespace php peb


/**
* This is an exception which contains the error code and message provIding information about the event manager response.
*/
exception PEBServiceException {
   1: required i32 statusCode;
   2: required string errorMessage;
}

/**
* PointsExpiry object
*/
struct PointsExpiry {
    1: required i32 customerId;
    2: required i64 loyaltyId;
    3: required double pointsToBeExpired;
    4: required i64 expiryDate;
}

/**
* CustomerExpirySchedule object
*/
struct CustomerExpirySchedule {    
    1: required list<PointsExpiry> pe;
}

/**
* PointsExpiryOnDate object
*/
struct PointsExpiryOnDate {
    1: required list<PointsExpiry> pe;
}

/**
* CustomerPointsExpiryOnDate object
*/
struct CustomerPointsExpiryOnDate {
    1: required PointsExpiry pe;
}

/**
* Pagenator Response object
*/
struct PaginatorResponse {
    1: required i32 sessionId;
    2: required i32 totalPages;
    3: required i32 sessionTimeOutPeriod;
}

/** Start: Health Dashboard related datasets **/

struct RemindersInfo {
    1: required i32 orgID;
    2: required i64 totalReminders;
    3: required i64 remindersDate;
}

struct PointsExpiryInfo {
    1: required i32 orgID;
    2: required double totalPoints;
    3: required i64 totalCustomers;
    4: required i64 expiryDateInMillis;
}

struct PromotionsExpiryInfo {
    1: required i32 orgID;
    2: required i32 promotionID;
    3: required string promotionName;
    4: required i64 expiryDateInMillis;
}

/** End: Health Dashboard related datasets **/

/**
*   CustomerPointsExpiryBulk object
*/
struct CustomerPointsExpiryBulk {
    1: required i32 customerId;    
    2: required double pointsExpiring;
    3: required i64 expiringOn;
}

/**
* CustomerPointsExpiredBulk object
*/
struct CustomerPointsExpiredBulk {
    1: required i32 customerId;    
    2: required double pointsExpired;
    3: required i64 expiredOn;
}

struct LoyaltyMergeResponse {
   1: required i32 fromCustomerId;
   2: required i32 toCustomerId;
   3: required i32 statusCode;
   4: optional string errorMessage;
}

struct MergeStatus {
   1: required i32 statusCode;
   2: optional string message;
}

/**
* To return exeception over thrift
*/
struct BoolRes {
    1: optional bool success;
    2: optional PEBServiceException ex;
}

/**
*  BulkExpiryReportData object
*/
struct BulkExpiryReportData {
	1: required i32 orgId;
	2: required i32 loggedInUserId;
	3: required i64 fromTimeInMillis;
	4: required i64 toTimeInMillis ;
	5: required bool includeExpired;
	6: required bool includeRedeemed;
}

/**
*  PromotionInfo Object
*/
struct PromotionInfo {
	1: required i32 id;
	2: required i32 programId;
	3: optional string name;// requires for new promotion
	4: optional string description;// requires for new promotion
	5: optional string sourceType;// requires for new promotion
	6: optional i32 sourceId;// requires for new promotion
	7: optional i32 eventTypeId;//Marking remaining fields as optional as they will be populated with default values
	8: optional bool isActive;
	9: optional bool isExclusive;
	10: optional string type;
	11: optional string promotionEvaluationType;
	12: optional i64 startDate;
	13: optional i64 endDate;
}

/**
*  BulkAllocatePointsData object
*/
struct BulkAllocatePointsData {
	1: required i32 orgId;
	2: required i32 programId;
	3: required i32 allocationStrategyId;
	4: required i32 expiryStrategyId;
	5: required PromotionInfo promotionInfo;
	6: required string owner;
	7: required list<i32> customerId;
	8: required i32 tillID;
	9: required i64 awardedTimeInMillis;
	10: required i32 createdBy;
	11: optional string notes;
}

/**
*  CustomerPointsData object
*/
struct CustomerPointsData {
	1: required i32 customerId;
	2: required double pointsAwarded;
	3: required i64 expiryDate;
	4: optional i32 statusCode;//If customer specific status is to be maintained
}

/**
*  BulkAllocatePointsResponse object
*/
struct BulkAllocatePointsResponse {
	1: required i32 statusCode;// 0 is failure, 1 is successful
	2: required list<CustomerPointsData> customerPointsDataList;
	3: optional string notes;
	4: optional PEBServiceException ex;
}

/**
* ReportFileData object
*/
struct ReportFileData {
	1: required string fileHandle;
	2: required i32 version;
}
		
struct ImportData{
	1: required i32 orgId;
	2: required i32 programId;
	3: required i32 userId;
	4: required i32 profileId;
	5: required i32 importId;
	6: required string tempImportTable;
	7: required i64 importTimeInMillis;
	8: optional string emailCsvToNotifyFailures;
}

/*
* @var filterType can have values - [STRATEGY, SLAB_EXPIRY_DATE, MIN_SLAB_EXPIRY_DATE]
* @var startDate - start slab expiry date
* @var endDate - end slab expiry expiry date
*/
struct TierExtensionData{
	1: required i32 orgId;
	2: required i32 programId;
	3: required string filterType;
	4: required i64 startDate;
	5: required i64 endDate;
	6: required i64 targetExpiryDate;
	7: required i64 minSlabExpiryDate;
	8: required bool retainPoints;
	9: required string tiersCsv;
}

struct PromotionData{
	1: required i32 id;
	2: required i32 orgId;
	3: required i32 programId;
	4: required string name;
	5: required string type; // "BILL" or "CUSTOMER"
	6: required i64 promoStartDateInMillis;
	7: required i64 promoEndDateInMillis;
	8: required i64 pointsAwardedStartDateInMillis;
	9: required i64 pointsAwardedEndDateInMillis;
	10: required double totalAllocatedPointsInDateRange;
}

struct GetPromotionRequest{
	1: required i32 orgId;
	2: required list<i32> promotionIds;
}

struct CustomersData{
	1: required i32 orgId;
	2: required i32 programId;
	3: required list<i32> customerIds;
}
struct ProgramSlabDetails{
	1: required i32 slabId
	2: required string slabName;
	3: required i32 slabSerialNumber;
	4: required string slabDescription;
}

struct CustomerPointsSummary {

    1: required i32 customerId;
    2: required i32 orgId;
    3: required i32 programId;
    4: required double currentPoints;
    5: required double cumulativePoints;
    6: required double pointsRedeemed;
    7: required double pointsExpired;
    8: required double pointsReturned;
    9: required ProgramSlabDetails currentProgramSlab;
   10: optional ProgramSlabDetails nextProgramSlab
   11: required double lifetimePurchases;
   12: required i32 lastUpdatedById;
   13: required i64 slabExpiryDate;
   14: required i32 visits;
   15: required i64 enrollmentDate;
   16: required i64 lastSlabchangeDate;
   17: optional i32 pointCategoryId;
}

enum PEBTestControlStatus {
	TEST
	CONTROL
	UNKNOWN
}

struct Loyalty {
	1: required i64 id;
	2: required i32 lifetimePurchase;
	3: required i32 initialLifetimePurchase;
	4: required i64 joinDate;
	5: required i32 registrationTillId;
	6: optional string type = "LOYALTY";
	7: optional i32 lastUpdatedByTill;
	8: optional i32 numberOfVisits;
	9: optional bool nonLoyalty;
}

struct CommChannelAttribute {
	1: required string name;
	2: required string value;
}

struct CommChannel {
	1: required string type;
	2: required string value;
	3: required bool verified;
	4: required bool primary;
	5: optional string commChannelMeta;//Meta details in the form of JSON
	6: optional list<CommChannelAttribute> attributes;
	7: optional bool subscribed;
}

struct UserProfile {
	1: required map<string,string> customFields; //Custom Fields
	2: required string source;
	3: required list<CommChannel> commChannels;
	4: optional string firstName;
	5: optional string lastName;
	6: optional string accountId;
}

struct GroupInfo {
	1: required string groupName;
	2: required bool isPrimary;
	3: required i64 joinedOnDateInMillis;
}

struct UserDetails {
	1: required i64 id;//The user id in the intouch users table
	2: required list<UserProfile> profiles;
	3: optional Loyalty loyalty;
	4: optional PEBTestControlStatus testControlStatus;
	5: optional GroupInfo groupInfo;
	6: optional map<string,string> extendedFieldsData;
	7: optional list<string> labels;
}

struct PointsRedemptionEventData {

    1: required i32 orgID;
    2: required i32 customerID;
    3: required i32 numPointsToBeRedeemed;
    4: required i32 redeemedAtStoreUnitId;
    5: required string redeemedOnBillNumber;
    //Send -1 if not present
    6: required i32 redeemedOnBillId;
    7: required i64 eventTimeInMillis;
    8: optional string validationCode;
    9: optional string notes;
    10: optional i32 referenceId;
    11: optional string uniqueId;
    12: optional string serverReqId;
    13: required UserDetails userDetails;//all the details of the user
    14: required string source;
    15: optional string accountId;
    16: optional bool nonLoyalty;
    17: optional i32 loyaltyContextId;
    18: optional UserDetails groupOwnerUserDetails;
}

struct CustomerFilter {
   1: required i32 orgId;
   2: required list<i32> customerIds;
   3: required i32 programId;
}

struct GapFilter {

    1: optional i64 fixedDateInMillis;
    2: optional i32 numDays;
}

struct AdvancedCustomerGetFilter {

    1: required CustomerFilter customerFilter;
    2: required GapFilter gapToUpgradeFilter;
    3: required GapFilter gapToRenewFilter;
}

enum KpiType {

    CURRENT_POINTS,
    CUMULATIVE_POINTS,
    CUMULATIVE_PURCHASES,
    TRACKER_VALUE_BASED,
    WINDOW_NUM_VISITS,
    WINDOW_POINTS,
    WINDOW_PURCHASES
}

enum GapType {

    GAP_TO_UPGRADE,
    GAP_TO_RENEW
}

struct KpiDetails {

    1: required KpiType kpiType
    2: required double gap;
}

struct GapDetails {

    1: required GapType gapType;
    2: required i64 validTillDate;
    3: required list<KpiDetails> kpiDetails;
}

struct AdvancedCustomerSummary {

    1: required i32 orgId;
    2: required i32 programId;
    3: required i32 customerId;
    4: required list<GapDetails> gapDetails;
}

struct SimpleProperty {
    1: required string key;
    2: optional string value;
}

struct ComplexProperty {
    1: required string key;
    2: required list <SimpleProperty> values;
}

struct Instruction {
    1: required string mnemonic;
    2: required i32 ruleSetId;
    3: required i32 ruleId;
    4: required i64 createdOnInMillis;
    5: required list <SimpleProperty> simpleProperties;
    6: required list <ComplexProperty> complexProperties;
}

struct EventEvaluationResult {
    1: required list <Instruction> instructions;
    2: required BoolRes result;
}

service PEBService {

	//isAlive
	bool isAlive();

	// Delayed Accrual to Redeemable service

	/**
	* Convert delayed accrual points to redeemable points
	*/
	bool bulkDelayedAccrualToRedeemablePoints(1: i64 date, 2: string serverReqId);

	/**
	* Convert delayed accrual points to redeemable points for given orgId
	*/
	bool bulkDelayedAccrualToRedeemablePointsByOrgId(1: i32 orgId, 2: i64 date, 3: string serverReqId);

	// Reminder Service
	/**
	* Prepare and send the report on Points Expiry/ Reminder to be sent on next day.
	*/
	bool alertBulkPointsExpiryReminder(1: i32 alertBeforeDays, 2: string serverReqId) throws (1: PEBServiceException ex);

	/**
	* Fetch how many reminders to be sent for number of customers
	**/
	list<RemindersInfo> getPointsExpiryRemindersInfo(1:i32 orgID, 2:i64 startDate, 3:i64 endDate, 4:string serverReqID) throws (1: PEBServiceException ex);

	/**
	* Fetch how many reminders were sent for number of customers
	**/
	list<RemindersInfo> getPointsExpiryRemindersSentInfo(1:i32 orgID, 2:i64 startDate, 3:i64 endDate, 4:string serverReqID) throws
	(1: PEBServiceException ex);

	/**
	* Send Bulk Reminder Message for Points Expiring across all Programs
	*/
	i64 sendBulkReminderMessageForAllPrograms(1: string serverReqId);

	/**
	* Send Bulk Reminder Message for Points Expiring for particular Programs
	*/
	i64 sendBulkReminderMessageForProgram(1: i32 programId, 2: i32 orgId, 3: string serverReqId);

	// Expiry Service

	/**
	* Gets the bulk points expiry schedule for a particular program between startDate and endDate
	*/
	bool getBulkPointsExpirySchedule(1:BulkExpiryReportData bulkExpiryReportData, 2:string serverReqId ) throws
	(1: PEBServiceException ex);


	/**
	 * Gets the bulk points expired for all customers in a particular program on expiryDate
	 */
	bool getBulkPointsExpired(1:BulkExpiryReportData bulkExpiryReportData, 2:string serverReqId ) throws
	(1: PEBServiceException ex);

	/**
	* Returns points expiring for customer
	*/
	CustomerExpirySchedule getPointsExpiryScheduleForCustomer(1:i32 orgID,2: i32 customerId, 3: string serverReqId) throws
(1 :PEBServiceException ex);

	/**
	* Returns the points expiring for each customer on a date
	*/
	PointsExpiryOnDate getPointsExpiryDetailsOnDate(1: i32 orgID,2: i64 date, 3: string serverReqId) throws (1 :PEBServiceException ex);

	/**
	* Returns points expiring for a customer on a date
	*/
	CustomerPointsExpiryOnDate getPointsExpiryDetailsForCustomerOnDate(1:i32 orgID,2: i32 customerId,3: i64 date, 4: string serverReqId)
throws (1 :PEBServiceException ex);

	/**
	* Bulk Expire Points for all Customers accross all Programs
	*/
	bool bulkExpirePointsAsOnDateForAllPrograms(1: i64 date, 2: string serverReqId);


	/** Health Dashboard related methods Start **/

	/**
	* Fetch total points getting expired for number of customers on date
	**/
	list<PointsExpiryInfo> getPointsExpiryInfo(1:i32 orgID, 2:i64 startDate, 3:i64 endDate, 4:string serverReqID) throws
	(1: PEBServiceException ex);

	/**
	* Fetch total points expired for number of customers on date
	**/
	list<PointsExpiryInfo> getPointsExpiredInfo(1:i32 orgID, 2:i64 startDate, 3:i64 endDate, 4:string serverReqID) throws
	(1: PEBServiceException ex);

	/**
	* Fetch promotions getting expired for number of customers on date
	**/
	list<PromotionsExpiryInfo> getPromotionExpiryInfo(1:i32 orgID, 2:i64 startDate, 3:i64 endDate, 4:string serverReqID) throws
	(1: PEBServiceException ex);

	/** Health Dashboard related methods End **/


	/**
	* Executes tier downgrade for all orgs at current time
	*/
	bool executeTierDowngrade(1: string serverReqId)
	throws (1: PEBServiceException ex);

	/**
	* Executes tier downgrade for all orgs at given time
	*/
	bool executeTierDowngradeAtTime(1: string serverReqId, 2: i64 runningDate)
	throws (1: PEBServiceException ex);

	/**
	* Executes tier downgrade for org
	*/
	bool executeTierDowngradeForOrg(1: string serverReqId, 2: i32 orgId, 3:bool sendReminder, 4:bool execute)
	throws (1: PEBServiceException ex);

	/**
	* Executes tier downgrade for org at given time
	*/
	bool executeTierDowngradeForOrgAtTime(1: string serverReqId, 2: i32 orgId, 3: i64 runningTime, 4:bool sendReminder, 5:bool execute)
	throws (1: PEBServiceException ex);

	/**
        * Executes tier downgrade on return for org at given time
        */
	bool executeDowngradeOnReturnForOrgAtTime(1: string serverReqId, 2: i32 orgId, 3: i64 runningTime, 4: bool execute)
	throws (1: PEBServiceException ex);

       /**
        * Merge customers
        */
        LoyaltyMergeResponse mergeCustomers(1:i32 orgID, 2:i32 fromCustomerId, 3:i32 toCustomerId, 4:i32 mergedbyTillId, 5:string serverReqId) throws (1: PEBServiceException ex);

        MergeStatus getMergeStatus(1:i32 orgID, 2:i32 fromCustomerId, 3:i32 toCustomerId, 4:string serverReqId) throws (1: PEBServiceException ex);

	/**
	*   Imports data for an org ( used for customer slab import )
	*/
	BoolRes importCustomerSlab(1: ImportData importData, 2:string serverReqId) throws (1: PEBServiceException ex);

	BoolRes importCustomerForNonDefaultProgram(1: ImportData importData, 2:string serverReqId) throws (1: PEBServiceException ex);

	/**
	*   Imports transaction details into customer_transactions for non default program
	*/
	BoolRes importTransactionForNonDefaultProgram(1: ImportData importData, 2:string serverReqId) throws (1: PEBServiceException ex);

	/**
	*  Extends tier expiry strategy
	*/
	BoolRes extendTierExpiryDate(1: TierExtensionData tierExtensionData, 2:string serverReqId) throws (1: PEBServiceException ex);

	/**
        * allocate points as per strategy and owner
        */
        BulkAllocatePointsResponse bulkAllocatePoints(1: BulkAllocatePointsData bulkAllocatePoints, 2:string serverReqId)
        throws (1: PEBServiceException ex);

	/**
	* get points issued in a date range pointsIssualStartDateInMillis and pointsIssualEndDateInMillis for a list promotions
	* promotion type can be - BILL or CUSTOMER
	*/
	list<PromotionData> getPromotionData(1: list<GetPromotionRequest> promotionRequestList, 2: i64 pointsAwardedStartDateInMillis,
	3: i64  pointsAwardedEndDateInMillis, 4: string serverReqId) throws (1: PEBServiceException ex);

	list<CustomerPointsSummary> getCustomerPointsSummariesByProgram(1:CustomersData customersData,
	 2:string  serverReqId ) throws (1: PEBServiceException ex);

	/*
	*
	* Imports transaction details into customer_transactions and publishes customer ids from temp table
	*/
	BoolRes publishKpiEventsPostImport(1: ImportData importData, 2:string serverReqId) throws (1: PEBServiceException ex);

	/**
    	* redemption of large number of points
    	*/
    	EventEvaluationResult bulkPointsRedemption(1: PointsRedemptionEventData pointsRedemptionEventData, 2:bool isCommit) throws (1: PEBServiceException ex);


	/*
	* get gap to upgrade/renew details for a customer
	*/
        list<AdvancedCustomerSummary> getAdvancedCustomerSummary(1:AdvancedCustomerGetFilter advancedCustomerGetFilter, 2:string serverReqId) throws (1: PEBServiceException ex);

}

// Expiry service callback

service BulkReportsCallback {

	bool fileServiceCallbackHandler(1: BulkExpiryReportData bulkExpiryReportData, 2: ReportFileData fileData, 3:i64 recordsCount, 4:BoolRes boolres, 5: string  serverReqId ) throws (1: PEBServiceException ex);

}