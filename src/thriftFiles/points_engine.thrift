#!thrift -java -php -phps

/**
 * This file contains all the points engine api service related classes and definitions.
*/

namespace java com.capillary.shopbook.pointsengine.api.external

namespace php points_engine

/**
* This is an exception which contains the error code and message provIding information about the event manager response.
*/
exception PointsEngineServiceException {
    1: required i32 statusCode;
    2: required string errorMessage;
}


struct DelayedAccrualLog {
    1: required double pointsToBeAccrued;
    2: required i64 accrualDate;
}

struct DelayedAccrualSummary {
    1: required double delayedPoints;           // points to be allocated (awarded - returned)
    2: required double delayedReturnedPoints;   // delayed points awarded but returned
    3: required double totalAvailablePoints;             // (normal available points + points to be allocated)
    4: required double totalReturnedPoints;     // (normal returned + delayed returned)
    5: required list<DelayedAccrualLog> delayedAccrualLogs;     // (10 delayed accrual logs order by delayed)
}

struct DelayedAccrualSchedule {
	1: required i32 programId;
	2: required i32 customerId;
	3: required list<DelayedAccrualLog> delayedAccrualLogs;
}

/**
    Customer points summary object
*/

struct CustomerPointsSummary {

    1: required i32 customerId;
    2: required i64 loyaltyId;
    3: required double currentPoints;
    4: required double cumulativePoints;
    5: required double pointsRedeemed;
    6: required double pointsExpired;
    7: required double pointsReturned;
    8: required string slabName;
    9: required i32 slabSerialNumber;
   10: required string slabDescription;
   11: required string nextSlabName;
   12: required i32 nextSlabSerialNumber;
   13: required string nextSlabDescription;
   14: required double cumulativePurchases;
   15: required i32 lastUpdatedById;
   16: required string lastUpdatedBy;
   17: required i64 lastUpdatedOn;
   18: required i64 lastAwardedOn;
   19: required i64 slabExpiryDate;
   20: optional string pointCategoryName;
   21: optional i32 pointCategoryId;
   22: optional i32 programId;
   23: optional DelayedAccrualSummary delayedAccrualSummary;
}

/**
   PointAwardedBillPromotions object
*/

struct PointAwardedBillPromotions
{
    1: required i64 pointAwardedId;
    2: required double points;
    3: required double pointsExpired;
    4: required double pointsRedeemed;
    5: required double pointsReturned;
    6: required i64 awardedDate;
    7: required string awardedBy;
    8: required i64 awardedById;
    9: required i64 billId;
    10: required i32 customerId;
    11: required i64 loyaltyId;
    12: required i64 expiryDate;
    13: required i32 promotionId;
    14: optional string promotionName;
    15: optional string pointCategoryName;
    16: optional i32 pointCategoryId;
    17: optional string promotionSourceType;
    18: optional i32 promotionSourceId;
    19: optional i32 programId;
    20: optional bool isDelayedAllocation;
}

/**
   PointAwardedCustomerPromotions object
*/

struct PointAwardedCustomerPromotions
{
    1: required i64 pointAwardedId;
    2: required double points;
    3: required double pointsExpired;
    4: required double pointsRedeemed;
    5: required double pointsReturned;
    6: required i64 awardedDate;
    7: required string awardedBy;
    8: required i64 awardedById;
    9: required i32 customerId;
    10: required i64 loyaltyId;
    11: required i64 expiryDate;
    12: required i32 promotionId;
    13: optional string promotionName;
    14: optional string pointCategoryName;
    15: optional i32 pointCategoryId;
    16: optional string promotionSourceType;
    17: optional i32 promotionSourceId;
    18: optional i32 programId;
    19: optional bool isDelayedAllocation;
}

/**
   PointAwardedLineItemPromotions object
*/

struct PointAwardedLineItemPromotions
{
    1: required i64 pointAwardedId;
    2: required double points;
    3: required double pointsExpired;
    4: required double pointsRedeemed;
    5: required double pointsReturned;
    6: required i64 awardedDate;
    7: required string awardedBy;
    8: required i64 awardedById;
    9: required i64 billId;
    10:required i32 customerId;
    11: required i64 loyaltyId;
    12: required i64 lineItemId;
    13: required i64 expiryDate;
    14: required i32 promotionId;
    15: optional string promotionName;
    16: optional string pointCategoryName;
    17: optional i32 pointCategoryId;
    18: optional string promotionSourceType;
    19: optional i32 promotionSourceId;
    20: optional i32 programId;
    21: optional bool isDelayedAllocation;
}


/**
   PointAwardedLineItem object
*/

struct PointAwardedLineItem
{
    1: required i64 pointAwardedId;
    2: required double points;
    3: required double pointsExclusive;
    4: required double pointsExpired;
    5: required double pointsExpiredExclusive
    6: required double pointsRedeemed;
    7: required double pointsRedeemedExclusive
    8: required double pointsReturned;
    9: required double pointsReturnedExclusive;
    10: required i64 awardedDate;
    11: required string awardedBy;
    12: required i64 awardedById;
    13: required i64 billId;
    14:required i32 customerId;
    15: required i64 loyaltyId;
    16:required i64 lineItemId;
    17: required i64 expiryDate;
    18: required list<PointAwardedLineItemPromotions> palp;
    19: optional string pointCategoryName;
    20: optional i32 pointCategoryId;
    21: optional i32 programId;
    22: optional bool isDelayedAllocation;
}


/**
    Point Awarded object
*/

struct PointAwarded {

    1: required i64 pointAwardedId;
    2: required double points;
    3: required double pointsExpired;
    4: required double pointsRedeemed;
    5: required double pointsReturned;
    6: required double pointsExclusive;
    7: required double pointsExpiredExclusive;
    8: required double pointsRedeemedExclusive;
    9: required double pointsReturnedExclusive;
    10: required i64 awardedDate;
    11: required string awardedBy;
    12: required i64 awardedById;
    13: required i64 pointsSourceTypeId;
    14: required i64 pointsSourceId;
    15: required i32 customerId;
    16: required i64 loyaltyId;
    17: required i64 expiryDate;
    18: required list<PointAwardedBillPromotions> pabp;
    19: required list<PointAwardedCustomerPromotions> pacp;
    20: required list<PointAwardedLineItem> pal;
    21: optional string pointCategoryName;
    22: optional i32 pointCategoryId;
    23: optional i32 programId;
    24: optional bool isDelayedAllocation;
    25: optional bool isGroupPoints;

  }

/**
   CustomerPurchaseHistory object
*/

struct CustomerPurchaseHistory {

    1: required i32 customerId;
    2: required i64 loyaltyId;
    3: required list<PointAwarded> pa;
    4: optional i32 programId;
}

/**
   PointsDeductions object
*/

struct PointsDeductions {

    1: required i32 customerId;
    2: required i64 loyaltyId;
    3: required string pointAwardedRefType;
    4: required i64 pointAwardedRefId;
    5: required string deductionType;
    6: required double pointsDeducted
    7: required double pointsDeductedCurrencyValue;
    8: required string pointsDeductedOn;
    9: required string pointsDeductedBy;
    10: required i64 pointsDeductedById;
}

/**
    SlabUpgradeHistory object
*/
struct SlabUpgradeHistory {

    1: required i32 customerId;
    2: required i64 loyaltyId;
    3: required i32 fromSlabSerialNo;
    4: required i32 toSlabSerialNo;
    5: required string fromSlabName;
    6: required string toSlabName;
    7: required i64 upgradedDate;
    8: required string tillName;
    9: required i32 tillId;
    10: required string notes;
    11: required i64 pointsSourceId;
    12: required i32 pointsSourceTypeId;
}

/**
    CustomerSlabUpgradeHistory object
*/
struct CustomerSlabUpgradeHistory {

    1: required list<SlabUpgradeHistory> slabUpgradeHistoryList;
    2: optional i32 programId;
}


/**
   CustomerPointsDeductions object
*/

struct CustomerPointsDeductions {

    1: required list<PointsDeductions> pd;
    2: required i32 customerId;
    3: required i64 loyaltyId;
    4: optional i64 programId;
}


/**
   PointsExpiry object
*/

struct PointsExpiry {

    1: required i32 customerId;
    2: required i64 loyaltyId;
    3: required double pointsToBeExpired;
    4: required i64 expiryDate;
}


/**
   CustomerExpirySchedule object
*/

struct CustomerExpirySchedule {

    1: required list<PointsExpiry> pe;
    2: required i32 programId;
}


/**
   BillPointsDetails object
*/

struct BillPointsDetails {

    1: required i32 customerId;
    2: required i64 loyaltyId;
    3: required PointAwarded pa;
    4: required double reissuedPoints;
    5: optional i32 programId;
}

/**
   CustomerPointsDetails object
*/

struct CustomerPointsDetails {

    1: required i32 customerId;
    2: required i64 loyaltyId;
    3: required PointAwarded pa;
    4: optional i32 programId;
}

/**
   PointsExpiryOnDate object
*/

struct PointsExpiryOnDate
{
    1: required list<PointsExpiry> pe;
    2: optional i32 programId;
}

/**
   CustomerPointsExpiryOnDate object
*/
struct CustomerPointsExpiryOnDate
{
    1: required PointsExpiry pe;
    2: optional i32 programId;
}

/**
   CustomerPointsExpiryBulk object
*/
struct CustomerPointsExpiryBulk
{
    1: required i32 customerId;
    2: required double pointsExpiring;
	3: required i64 expiringOn;
}

/**
   CustomerPointsExpiredBulk object
*/
struct CustomerPointsExpiredBulk
{
    1: required i32 customerId;
    2: required double pointsExpired;
    3: required i64 expiredOn;
}

/**
   BillPointsConsumed object
*/

struct BillPointsConsumed
{
    1: required i32 customerId;
    2: required i64 loyaltyId;
    3: required PointAwarded pa;
    4: optional i32 programId;
}

/**
	Pagenator Response object
*/
struct PaginatorResponse
{
	1: required i32 sessionId;
	2: required i32 totalPages;
	3: required i32 sessionTimeOutPeriod;
}

/** Health Dashboard related datasets **/

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

struct SlabInfo {
	1: required string name;
	2: required string desc;
	3: required i32 serialNumber;
	4: required i32 upgradeOnLifeTimePurchase;
	5: required double allocationPerc;
	6: required i32 redemptionMinCurrentPoints;
	7: required i32 redemptionBlock; //Multiples of X for redemption.
	8: required string expiryUnit;
	9: required i32 expiryValue;
	10: required bool rollingExpiry;
}

struct Program {
	1: required i32 id;
	2: required string name;
	3: optional string description;
}

struct BasicProgram {
	1: required i32 id;
	2: required list<SlabInfo> slabs;
	3: required double pointsCurrencyRatio;
	4: optional string contactInfo;
	5: optional string transMessage;
	6: optional string transEmailSub;
	7: optional string transEmailBody;
	8: optional i32 transTemplateID;
	9: optional string welcomeMessage;
	10: optional string welcomeEmailSub;
	11: optional string welcomeEmailBody;
	12: optional i32 welcomeTemplateID;
	13: required bool isDefault;
}

struct SegmentValue {
	1: required string id;
	2: required string value;
}

struct Segment {
	1: required string id;
	2: required i32 orgId;
	3: required string name;
	4: required string status;
	5: required list<SegmentValue> segmentValues;
}

struct BoolRes {
    1: optional bool success;
    2: optional PointsEngineServiceException ex;
}

struct PointsRedemptionData {
   1: required i32 redemptionId;
   2: required i32 numPointsToBeRedeemed;
   3: required i32 redeemedAtStoreId;
   4: required i64 eventTimeInMillis;
   5: optional string redeemedOnBillNumber;
   6: optional i32 redeemedOnBillId;
   7: optional string validationCode;
   8: optional string notes;
}

struct PointsRedemptionCustomerData {
   1: required i32 customerID;
   2: required list<PointsRedemptionData> customerRedemptions;
   3: required i32 referenceId;
}

struct PointsRedemptionOrgData {
   1: required i32 orgId;
   2: required i32 programId;
   3: required list<PointsRedemptionCustomerData> customerPointsRedemptions;
   4: optional string serverReqId;
}

struct PointsRedemptionResponse {
   1: required i32 customerID;
   2: required i32 statusCode;
   3: optional string errorMessage;
   4: optional i32 failedRedemptionId;
}

struct GoodwillPointsData{
   1: required i32 orgID;
   2: required i32 customerID;
   3: required double pointsValue;
   4: required i32 tillID;
   5: required i64 awardedTimeInMillis;
   6: required i32 createdBy;
   7: required i32 goodwillReferenceID;
   8: optional string notes;
   9: optional i32 programId;
}

struct PromotionPointsData{
   1: required i32 orgId;
   2: required i32 customerId;
   3: required double pointsValue;
   4: required i32 tillId;
   5: required i64 awardedTimeInMillis;
   6: required i32 createdBy;
   7: required i32 promotionId;
   8: required i32 expiryStrategyId;
   9: optional i32 allocationStrategyId;
   10: optional i32 referenceId;
   11: optional string notes;
   12: optional i32 programId;
}

struct RecalculateKpiJobDetails{
   1: required i32 orgId
   2: required i32 programId;
   3: required i32 jobId;
   4: required string jobType;
   5: required string status;
   6: required i32 version;
   7: required i32 processedUptoId;
   8: required i32 endingId;
   9: required i64 jobStartTimeInMillis;
}

struct KpiDetails{
   1: required string type;
   2: required double value;
   3: required double gap;
}

struct GapDetails{
   1: required i32 targetSlabNumber;
   2: required i64 fromDateInMillis;
   3: required i64 toDateInMillis;
   4: required string gapType;
   5: required list<KpiDetails> kpiDetails;
}

struct CustomerKpiGap{
   1: required i32 orgId;
   2: required i32 programId;
   3: required i32 customerId;
   4: required i32 gapToUpgradeVersion;
   5: required i32 gapToRenewVersion;
   6: required list<GapDetails> gapDetails;
   7: required i64 lastUpdateTimeInMillis;
}

struct LoyaltyMergeResponse {
   1: required i32 fromCustomerId;
   2: required i32 toCustomerId;
   3: required i32 statusCode;
   4: optional string errorMessage;
   5: optional CustomerPointsSummary fromCustomer;
   6: optional CustomerPointsSummary toCustomer;
}

struct MergeStatus {
   1: required i32 statusCode;
   2: optional string message;
}

enum RedemptionType{
   REDEMPTION, REVERSAL
}

struct PointsRedemptionSummary {

    1: required i32 Id;
    2: required i32 programId;
    3: required i32 orgId;
    4: required i32 customerId;
    5: required double pointsRedeemed;
    6: required i64 billId;
    7: required string billNumber;
    8: required string validationCode;
    9: required string notes;
    10: required i64 redemptionTime;
    11: required i64 pointsRedemptionTime;
    12: required i32 tillId;
    13: required string tillName;
    14: required RedemptionType redemptionType;
    15: optional list<PointsDeductions> pd;
    16: optional string redemptionId;
}

struct RenewCustomerSlabData{
	1: required i32 orgId;
	2: required i32 customerId;
	3: required i32 toSlabId;
	4: required i32 tillId;
	5: required string notes;
	6: required i64 renewedOn;
	7: optional i32 programId;
}

struct TierDowngradeRetentionCriteria{
    1: required i32 programId;
    2: required i32 orgId;
    3: required i32 customerId;
    4: required i32 visits;
    5: required double purchase;
}

struct TierUpgradeCriteria{
    1: required i32 programId;
    2: required i32 orgId;
    3: required i32 customerId;
    4: required string purchaseType;
    5: required string description;
    6: required double purchaseValue;
}

struct TrackerDataRequest{
    1: required i32 orgId;
    2: required i32 customerId;
    3: required bool onlyActive;
    4: optional i32 trackerStrategyId;
    5: optional i32 trackerConditionId;
    6: optional i32 tillId;
    7: optional list<i32> programIds;
}

struct TrackerData{
    1: required i32 orgId;
    2: required i32 programId;
    3: required i32 trackerStrategyId;
    4: required string trackerStrategyName;
    5: required i32 trackerConditionId;
    6: required string trackerConditionName;
    7: required i32 customerId;
    8: required string trackerType;
    9: required double trackedValue;
    10: required i64 trackedOn;
}

struct DeductionFilterParams{
    1: optional string deductionType; /* REDEEMED, EXPIRED, CANCELLED, MIGRATION, RETURN */
    2: optional i64 minPoints = 0; /* Defaults to 0 */
    3: optional i64 fromDate; /* start of date range in milliseconds since epoch */
    4: optional i64 toDate; /* end of date range in milliseconfs since epoch */
    5: optional bool isSortingOrderAsc; /* ASC/DESC on deductedOn , defaults to DESC */
}

struct PurchaseHistoryFilterParams{
    1: required list<i64> billIds;
    2: optional i64 fromDate; /* start of date range in milliseconds since epoch */
    3: optional i64 toDate; /* end of date range in milliseconfs since epoch */
    4: optional bool isSortingOrderAsc; /* ASC/DESC on deductedOn, defaults to ASC */
}

struct PointsExpiryScheduleFilterParams{
    1: optional bool isPromotion; /* PROMOTION/NON_PROMOTION , defaults to BOTH */
    2: optional i64 fromDate; /* start of date range in milliseconds since epoch */
    3: optional i64 toDate; /* end of date range in milliseconfs since epoch */
    4: optional bool isSortingOrderAsc; /* ASC/DESC on deductedOn, defaults to DESC */
}

struct PointsRedemptionFilterParams{
    1: optional list<i64> billIds;
    2: optional bool includePointsDeductions = false; /* include points deductions for the bill Ids*/
}

struct PointsRedemptionUpdate {
   1: required i32 orgId;
   2: required i32 pointsRedemptionSummaryId;
   3: required i32 billId;
   4: required string billNumber;
   5: optional i32 programId;
}

struct BillPointsParams {
   1: required i64 billId;
   2: required i32 orgId;
   3: optional i32 customerId;
   4: optional i32 tillId;
   5: optional list<i32> programIds;
}

struct UserGroupInfo {
   1: required string groupName;
   2: required bool isPrimary;
   3: required i64 joinedOnDateInMillis;
}

struct CustomerFilter {
   1: required i32 orgId;
   2: required i32 customerId;
   3: optional i32 tillId;
   4: optional list<i32> programIds;
   5: optional UserGroupInfo userGroupInfo;
}

struct ProgramFilter{
	1: required i32 orgId;
	2: optional i32 tillId;
	3: required list<i32> programIds;
	4: optional bool isDefault;  //default value will be false
	5: optional bool isActive;   //default value will be true
}

struct CampaignProgramConfig{
	1: required i32 orgId;
	2: required i32 programId;
	3: required i32 allocationStrategyId;
	4: required i32 expiryStrategyId;
}

/**
	Transfer Type enum
*/
enum TransferType{
	ADDITION,
	DEDUCTION
}

/**
	Points Transfer Summary object
*/
struct PointsTransferSummary{
	1: required i32 Id;
    	2: required Program program;
    	3: required i32 orgId;
    	4: required double pointsCredited;
	5: required double pointsDeducted;
	6: required i32 fromCustomerId;
        7: required i32 toCustomerId;
	8: required i32 fromCustomerGroup;
	9: required i32 toCustomerGroup;
	10: required TransferType transferType;
	11: required i32 tillId;
	12: required string transferNotes;
	13: required string transferredOn;
	14: required i64 paId;
	15: required string createdOn;
}

// Service
service PointsEngineService {

	//LIFE CYCLE
	/**
	* Checks if the points api service is in a running state
	*/
    bool isActive();

    /**
	* Returns customer points summary, returns for default program
	*/
    CustomerPointsSummary getCustomerPointsSummary(1: i32 orgID, 2: i32 customerId, 3: string serverReqId) throws (1 :PointsEngineServiceException ex);

	/**
	* Returns customer points summary for redeemable points type
	**/
    list<CustomerPointsSummary> getCustomerPointsSummariesByFilter(1: CustomerFilter customerFilter, 2: string serverReqId) throws (1 :PointsEngineServiceException ex);

   /**
	* Returns customer points summary, for default program
	* TODO: MLP check if required for multiple loyalty program
	*/
    list<CustomerPointsSummary> getCustomerPointsSummaries(1: i32 orgID, 2: i32 customerId, 3: string serverReqId) throws (1 :PointsEngineServiceException ex);


  /**
  	* Returns whole point awarded tree for each bill for the customer
        */

    CustomerPurchaseHistory getPurchaseHistoryForCustomer(1:i32 orgID,2: i32 customerId, 3: string serverReqId) throws (1 :PointsEngineServiceException ex);

    /**
    * For a particular program or default program,
    Returns whole point awarded tree for each bill for the customer
        */
    list<CustomerPurchaseHistory> getAllPurchaseHistoryForCustomer(1:CustomerFilter customerFilter, 2: string serverReqId) throws (1 :PointsEngineServiceException ex);

 /**
        * Returns whole point awarded tree for each bill for the customer
        * billIds list, date range, sort order on bill date, limit records to 100
        */

    CustomerPurchaseHistory getPurchaseHistoryForCustomerFiltered(1:i32 orgID, 2:i32 customerId, 3:PurchaseHistoryFilterParams purchaseHistoryFilterParams, 4:string serverRequestId) throws (1 :PointsEngineServiceException ex);

     /**
        * For a particular program or default program,
        * Returns whole point awarded tree for each bill for the customer
        * billIds list, date range, sort order on bill date, limit records to 100
        */

	list<CustomerPurchaseHistory> getAllPurchaseHistoryForCustomerFiltered(1:CustomerFilter customerFilter,
			2: PurchaseHistoryFilterParams purchaseHistoryFilterParams, 3:string serverRequestId) throws (1 :PointsEngineServiceException ex);

/**
	* Returns points expiring for customer
	*/

    CustomerExpirySchedule getPointsExpiryScheduleForCustomer(1:i32 orgID,2: i32 customerId, 3: string serverReqId) throws (1 :PointsEngineServiceException ex);


    /**
      * For a particular program or default program
      * Returns points expiring for customer
      */

    list<CustomerExpirySchedule> getAllPointsExpiryScheduleForCustomer(1:CustomerFilter customerFilter, 2: string serverReqId) throws (1 :PointsEngineServiceException ex);

/**
        * Returns points expiring for customer
        * promotion/non-promo, date range, sort order on expiry date, limit to 100
        */

    CustomerExpirySchedule getPointsExpiryScheduleForCustomerFiltered(1:i32 orgID,2: i32 customerId, 3: PointsExpiryScheduleFilterParams pointsExpiryScheduleFilterParams, 4: string serverReqId) throws (1 :PointsEngineServiceException ex);

    /**
        * For a particular program or default program, returns points expiring for customer
        * promotion/non-promo, date range, sort order on expiry date, limit to 100
        */

    list<CustomerExpirySchedule> getAllPointsExpiryScheduleForCustomerFiltered(1:CustomerFilter customerFilter,
    		2:PointsExpiryScheduleFilterParams pointsExpiryScheduleFilterParams, 3: string serverReqId) throws (1 :PointsEngineServiceException ex);

	/**
	* Returns point awarded tree for a bill.
	*/

    BillPointsDetails getBillPointsDetails(1:i32 orgID,2: i32 customerId,3: i64 billId, 4: string serverReqId) throws (1 :PointsEngineServiceException ex);


  /**
  * Returns point awarded tree for a bill.
  */
//TODO:  make common request object for bills
    list<BillPointsDetails> getAllBillPointsDetails(1:BillPointsParams billPointsParams, 2: string serverReqId) throws (1 :PointsEngineServiceException ex);

	/**
	* Returns deductions for customer
	* defaults to deducted on DESC
	*/

    CustomerPointsDeductions getDeductionsForCustomer(1:i32 orgID, 2: i32 customerId, 3: string serverReqId) throws (1 :PointsEngineServiceException ex);

  /**
  * For a particular program or default program, Returns deductions for customer
  * defaults to deducted on DESC
  */

    list<CustomerPointsDeductions> getAllDeductionsForCustomer(1:CustomerFilter customerFilter, 2: string serverReqId) throws (1 :PointsEngineServiceException ex);

	/**
        * Returns deductions for customer filtered on
        * min points, deduction type, date range, sort by deducted on DESC
        */

    CustomerPointsDeductions getDeductionsForCustomerFiltered(1:i32 orgID, 2: i32 customerId, 3: DeductionFilterParams deductionFilterParams, 4: string serverReqId) throws (1 :PointsEngineServiceException ex);


  /**
    * For a particular program or default program, Returns deductions for customer filtered on
    * min points, deduction type, date range, sort by deducted on DESC
    */

    list<CustomerPointsDeductions> getAllDeductionsForCustomerFiltered(1:CustomerFilter customerFilter, 2: DeductionFilterParams deductionFilterParams, 3: string serverReqId) throws (1 :PointsEngineServiceException ex);



	/**
	* Returns the points expiring for each customer on a date
	*
	*/
//Not supported
    PointsExpiryOnDate getPointsExpiryDetailsOnDate(1: i32 orgID,2: i64 date, 3: string serverReqId) throws (1 :PointsEngineServiceException ex);

	/**
	* Returns points expiring for a customer on a date
	*/

    CustomerPointsExpiryOnDate getPointsExpiryDetailsForCustomerOnDate(1:i32 orgID,2: i32 customerId,3: i64 date, 4: string serverReqId)
throws (1 :PointsEngineServiceException ex);

  /**
  * For a particular program or default program, Returns points expiring for a customer on a date
  */

    list<CustomerPointsExpiryOnDate> getAllPointsExpiryDetailsForCustomerOnDate(1:CustomerFilter customerFilter, 2: string serverReqId)
throws (1 :PointsEngineServiceException ex);

	/**
	* Checks if the bill points have been redeemed/expired
	*/
// not implemented
    BillPointsConsumed hasBillPointsBeenConsumed(1: i32 orgID, 2: i64 billId, 3: string serverReqId) throws (1 :PointsEngineServiceException ex);

	/**
	* Returns slab upgrade history for a customer
	* default sort to desc by upgrade date
	*/

    CustomerSlabUpgradeHistory getSlabUpgradeHistory(1: i32 orgId,2: i32 customerId, 3: string serverReqId) throws (1: PointsEngineServiceException ex);

  /**
  * For a particular program or default program, Returns slab upgrade history for a customer
  * default sort to desc by upgrade date
  */

    list<CustomerSlabUpgradeHistory> getAllSlabUpgradeHistory(1: CustomerFilter customerFilter, 2: string serverReqId) throws (1: PointsEngineServiceException ex);

    /**
    * Returns the customer points details. Contains point awarded and point awarded customer promotion data.
    */
    CustomerPointsDetails getCustomerLevelPointsDetails(1: i32 orgId,2: i32 customerId, 3: string serverReqId) throws (1: PointsEngineServiceException ex);

    /**
    * For a particular program or default program, return the customer points details. Contains point awarded and point awarded customer promotion data.
    */
    list<CustomerPointsDetails> getAllCustomerLevelPointsDetails(1: CustomerFilter customerFilter, 2: string serverReqId) throws (1: PointsEngineServiceException ex);

	/**
	* Send Bulk Reminder Message for Points Expiring across all Programs
    */
	i64 sendBulkReminderMessageForAllPrograms();

	/**
	* Send Bulk Reminder Message for Points Expiring for particular Programs
    */
	i64 sendBulkReminderMessageForProgram(1: i32 programId);

    /**
    * Bulk Expire Points for all Customers accross all Programs
    */
    bool bulkExpirePointsAsOnDateForAllPrograms(1: i64 date);

    /**
    * Bulk Expire Points for all Customers for particular Program
    */
    bool bulkExpirePointsAsOnDate(1: i32 programId, 2: i64 date);

	/**
	* Validates all the program related configurations. Used in validated switch over
	*/
    bool validateProgramConfiguration(1: i32 progID, 2: i32 orgId, 3: string serverReqId) throws (1: PointsEngineServiceException ex);

	/**
	* Prepare and send the report on Points Expiry/ Reminder to be sent on next day.
	*/
	bool alertBulkPointsExpiryReminder(1: i32 alertBeforeDays) throws (1: PointsEngineServiceException ex);

	/**
	* Initialize the call for Bulk Points Expiry Schedule
	*/
	PaginatorResponse bulkPointsExpiryScheduleInit(1: i32 orgId, 2: i64 fromDate, 3: i64 toDate, 4: string serverReqId)
	throws (1: PointsEngineServiceException ex);

	/**
	* Gets the bulk points expiry schedule for a particular program between startDate and endDate
	*/
	//not implemented
	list<CustomerPointsExpiryBulk> getBulkPointsExpirySchedule(1: i32 orgId, 2: i32 pageId, 3: i32 sessionId, 4: string serverReqId)
	throws (1: PointsEngineServiceException ex);

	/**
	* Initialize the call for Bulk Points Expired
	*/
	PaginatorResponse bulkPointsExpiredInit(1: i32 orgId, 2: i64 fromExpiryDate, 3: i64 toExpiryDate, 4: bool includeExpired, 5: bool includeRedeemed,
	6: string serverReqId) throws (1: PointsEngineServiceException ex);

	/**
	 * Gets the bulk points expired for all customers in a particular program on expiryDate
	 */
	list<CustomerPointsExpiredBulk> getBulkPointsExpired(1: i32 orgId, 2: i32 pageId, 3: i32 sessionId, 4: string serverReqId)
	throws (1: PointsEngineServiceException ex);


	/** Health Dashboard related methods Start **/

	/**
	* Fetch how many reminders to be sent for number of customers
	**/
	list<RemindersInfo> getPointsExpiryRemindersInfo(1:i32 orgID, 2:i64 startDate, 3:i64 endDate, 4:string serverReqID) throws (1: PointsEngineServiceException ex);

	/**
	* Fetch how many reminders were sent for number of customers
	**/
	list<RemindersInfo> getPointsExpiryRemindersSentInfo(1:i32 orgID, 2:i64 startDate, 3:i64 endDate, 4:string serverReqID) throws
	(1: PointsEngineServiceException ex);

	/**
	* Fetch total points getting expired for number of customers on date
	**/
	list<PointsExpiryInfo> getPointsExpiryInfo(1:i32 orgID, 2:i64 startDate, 3:i64 endDate, 4:string serverReqID) throws
	(1: PointsEngineServiceException ex);

	/**
	* Fetch total points expired for number of customers on date
	**/
	list<PointsExpiryInfo> getPointsExpiredInfo(1:i32 orgID, 2:i64 startDate, 3:i64 endDate, 4:string serverReqID) throws
	(1: PointsEngineServiceException ex);

	/**
	* Fetch promotions getting expired for number of customers on date
	**/
	list<PromotionsExpiryInfo> getPromotionExpiryInfo(1:i32 orgID, 2:i64 startDate, 3:i64 endDate, 4:string serverReqID) throws
	(1: PointsEngineServiceException ex);

	/** Health Dashboard related methods End **/

	/**
	* Check whether a program is present for the provided orgID or not
	**/
	bool isProgramPresentForOrg(1:i32 orgID, 2:string serverReqID) throws (1: PointsEngineServiceException ex);

	/**
	* Create basic program for an org
	**/
	BoolRes createBasicProgram(1:i32 orgID, 2:BasicProgram basicProgram, 3:i32 createdBy, 4:string serverReqID);

	/**
	* Get the information of BasicProgram for default program
	*/
	BasicProgram getBasicProgramDetails(1:i32 orgID, 2:string serverReqID) throws (1: PointsEngineServiceException ex);

	/**
	* Get the information of BasicProgram based on program filter
	*/
	list<BasicProgram> getAllBasicProgramDetails(1:ProgramFilter programFilter, 2:string serverReqID) throws (1: PointsEngineServiceException ex);

	/**
	* Get the points to currency ratio for default program,
	* to get points to currency ratio for all programs use "getAllBasicProgramDetails" method
	*/
	double getPointsCurrencyRatio(1:i32 orgId, 2:string serverReqId) throws (1: PointsEngineServiceException ex);

	/**
	* Get the segements
	*/
	list<Segment> getSegments(1:i32 orgId, 2:string serverReqId) throws (1: PointsEngineServiceException ex);

	/**
	* Get the segements
	*/
	Segment getSegmentWithValues(1:i32 orgId, 2:string segmentName, 3:string serverReqId) throws (1: PointsEngineServiceException ex);

    /**
    * Bulk Redeem points for org
    */
  list<PointsRedemptionResponse> bulkRedeemPoints(1:PointsRedemptionOrgData pointsRedemptionOrgData, 2:string serverReqId) throws (1: PointsEngineServiceException ex);

	/**
	* allocate good will points
	**/
	BoolRes allocateGoodwillPoints(1:GoodwillPointsData goodwillPointsData, 2:string serverReqID);

	/**
	* allocate promotion points
	**/
	BoolRes allocatePromotionPoints(1:PromotionPointsData promotionPointsData, 2:string serverReqID);

	 /**
        * Merge customers
        */
        LoyaltyMergeResponse mergeCustomers(1:i32 orgID, 2:i32 fromCustomerId, 3:i32 toCustomerId, 4:i32 mergedbyTillId, 5:string serverReqId) throws (1: PointsEngineServiceException ex);

	MergeStatus getMergeStatus(1:i32 orgID, 2:i32 fromCustomerId, 3:i32 toCustomerId, 4:string serverReqId) throws (1: PointsEngineServiceException ex);

	/**
	* Sort by redemption date desc for default program
	*/
	list<PointsRedemptionSummary> getPointsRedemptionSummaryForCustomer(1:i32 orgId, 2: i32 customerId, 3: bool includePointsDeductions, 4: string serverReqId) throws (1 :PointsEngineServiceException ex);

  /**
  * For a particular program or default program, Sort by redemption date desc
  */
  map<i32, list<PointsRedemptionSummary>> getAllPointsRedemptionSummaryForCustomer(1:CustomerFilter customerFilter,
  		2: bool includePointsDeductions , 3: string serverReqId) throws (1 :PointsEngineServiceException ex);

        /**
	* Points Redemption for given customer for default program
	* filter params of billIds, include points deductions
        * Sort by redemption date desc
        */
        list<PointsRedemptionSummary> getPointsRedemptionSummaryForCustomerFiltered(1:i32 orgId, 2: i32 customerId,
        		3:PointsRedemptionFilterParams pointsRedemptionFilterParams, 4: string serverReqId) throws (1 :PointsEngineServiceException ex);

 /**
  * Points Redemption for given customer
  * filter params of billIds, include points deductions
  * Sort by redemption date desc
  */
  map<i32, list<PointsRedemptionSummary>> getAllPointsRedemptionSummaryForCustomerFiltered(1: CustomerFilter customerFilter,
  		2: PointsRedemptionFilterParams pointsRedemptionFilterParams, 3: string serverReqId) throws (1 :PointsEngineServiceException ex);


	/**
	* clear cache for customer data in org
	**/
	BoolRes clearCustomerDataCache(1:i32 orgId, 2:string serverReqId);

	/**
	*    renew customer slab in membership program
	**/
	BoolRes renewCustomerSlab(1: RenewCustomerSlabData renewCustomerSlabData, 2:i32 renewedBy, 3:string serverReqId) throws (1 :PointsEngineServiceException ex);

	/**
	*    get tier downgrade  for default program
	**/
	bool getTierDowngradeStatus(1: i32 orgId, 2:string serverReqId) throws (1 :PointsEngineServiceException ex);

	/**
	*	get tier downgrade status for all programs
	**/
	map<i32, bool> getTierDowngradeStatusByFilter(1: ProgramFilter programFilter , 3:string serverReqId) throws (1 :PointsEngineServiceException ex);

	/**
	*   get tier renewal criteria for a customer for default program
	**/
	TierDowngradeRetentionCriteria getTierDowngradeRetentionCriteria(1: i32 orgId, 2: i32 customerId, 3:string serverReqId) throws (1 :PointsEngineServiceException ex);

  /**
  *   For particular program or default program, get tier renewal criteria for a customer
  **/
	list<TierDowngradeRetentionCriteria> getAllTierDowngradeRetentionCriteria(1: CustomerFilter customerFilter, 2:string serverReqId) throws (1 :PointsEngineServiceException ex);

  /**
  *   get tier upgrade criteria for a customer
  **/
  TierUpgradeCriteria getTierUpgradeCriteria(1: i32 orgId, 2: i32 customerId, 3:string serverReqId) throws (1 :PointsEngineServiceException ex);

  /**
  *   For a particular program or default program, get tier upgrade criteria for a customer
  **/
  list<TierUpgradeCriteria> getAllTierUpgradeCriteria(1: CustomerFilter customerFilter, 2:string serverReqId) throws (1 :PointsEngineServiceException ex);

	/**
	*    get trackerd data for all customers and for all trackers,
	*    including expired trackers as we don't consider any trackers as expired anymore
	*     Default the sorting to tracked date
	**/
	list<TrackerData> getTrackedData(1: TrackerDataRequest request, 3:string serverReqId) throws (1 :PointsEngineServiceException ex);

	/**
	* Update the bill details after the redemption completes. Throws an error if prs not found or if bill details already present
	**/
	bool updateRedemptionBillDetails(1: PointsRedemptionUpdate prs, 2: string serverReqId) throws (1 :PointsEngineServiceException ex);

	map<i32,list<i32>> getProgramIdsForTills(1:i32 orgId, 2:list<i32> tills, 3: string serverRequestId) throws (1 :PointsEngineServiceException ex);

	BoolRes validate(1:CampaignProgramConfig config, 2:string serverRequestId);

	list<DelayedAccrualSchedule> getDelayedAccruals(1:CustomerFilter filter, 2:string serverReqId) throws (1 :PointsEngineServiceException ex);

	/**
	*  get kpi recalculation status for a program
	**/
	list<RecalculateKpiJobDetails> getKpiRecalculationStatus(1: ProgramFilter programFilter, 2: string serverReqId) throws (1 :PointsEngineServiceException ex);

	/**
	*  get customer kpi gap values for a customer
	**/
	list<CustomerKpiGap> getCustomerKpiGapValues(1: CustomerFilter customerFilter, 2: string serverReqId) throws (1 :PointsEngineServiceException ex);

	/**
	*  get customer points transfer summaries
	**/
	list<PointsTransferSummary> getAllPointsTransferSummaries(1: CustomerFilter customerFilter, 2: string serverReqId) throws (1 :PointsEngineServiceException ex);
}
