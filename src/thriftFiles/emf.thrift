#!thrift -java -php -phps

/**
* This file contains all the event management related classes and definitions.
*/

namespace java com.capillary.shopbook.emf.api.external

namespace php emf

/**
* This is an exception which contains the error code and message providing information about the event manager response.
*/
exception EMFException {
1: required i32 statusCode;
2: required string errorMessage;
3: required i32 replayErrorCode;
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
7: optional string caseValue;
}

/**
* The result object which contains multiple effects of an evaluated event.
*/
struct EventEvaluationResult {
1: required list <Instruction> instructions;
}

struct TenderAttributeValues {
1: required i32 orgTenderAttributeId;
2: required string dataType;
3: required string name;
4: required string value;
5: optional i32 tenderAttributeId;
6: optional i32 orgTenderValueId;
}

struct TenderDetails {
1: required i32 orgTenderId;
2: required i32 tenderId;
3: required string tenderName;
4: required string orgTenderName;
5: required double amount;
6: optional string notes;
7: optional list <TenderAttributeValues> tenderAttributes;
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
9: optional bool nonLoyalty;//customer is a non-loyalty customer to be ignored by emf
}

/**
* The test control status of a user
*
* TEST     : The user is in test group

* CONTROL  : The user is in control group

* UNKNOWN  : The user's group is not known either because the org is not
* configured or because the org does not have a test control segment
*/
enum EMFTestControlStatus {
TEST
CONTROL
UNKNOWN
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

struct UserGroupInfo {
1: required string groupName;
2: required bool isPrimary;
3: required i64 joinedOnDateInMillis;
}

struct GroupInfo {
1: required i64 id;
2: required string groupName;
3: required i32 groupLifetimePurchase;
4: required i32 groupPrevLifetimePurchase;
5: required i32 groupNumVisits;
6: required i32 groupNumTransactionsToday;
7: required i32 groupNumTransactions;
8: required i32 groupNumItems;
9: required i32 ownerGroupPurchase;
10: required i32 ownerLifeTimePurchase;
11: required i32 ownerGroupNumVisits;
12: required i32 ownerNumVisits;
13: required i32 ownerGroupNumTransactionsToday;
14: required i32 ownerNumTransactionsToday;
15: required i32 ownerGroupNumTransactions;
16: required i32 ownerNumTransactions;
17: required i32 ownerGroupNumItems;
18: required i32 ownerNumItems;
}

struct UserDetails {
1: required i64 id;//The user id in the intouch users table
2: required list<UserProfile> profiles;
3: optional Loyalty loyalty;
4: optional EMFTestControlStatus testControlStatus;
5: optional UserGroupInfo userGroupInfo;
6: optional map<string,string> extendedFieldsData;
7: optional list<string> labels;
}

struct PointsBalance {
1: required string points;
2: required i64 pointsExpiryDateinMillis;
}

struct LoyaltyProgramEnrollment {
1: required i64 enrollmentDateTimeInMillis;
2: required i32 tierNumberAtEnrollment;
3: required i64 tierExpiryDateInMillis;
4: required list<PointsBalance> pointsBalances;
}

struct LineItem {
1: required i64 id;
2: required map<string,string> extendedFieldsData;
}

/**
* Event contianing information about the new bill.
*/
struct NewBillEvent {

1: required i32 orgID;
2: required i32 customerID;
3: required i32 billID;
4: required i32 storeUnitID;
5: required i64 eventTimeInMillis;
6: required bool ignorePoints;
7: required i32 billAmount;
8: required i32 lifetimePurchase;
9: required i32 prevLifetimePurchase;
10: required i32 numberOfVisits;
11: optional string uniqueId;
12: optional string serverReqId;
13: optional string referrerCode;
14: optional list <TenderDetails> tenderDetails;
15: optional i64 retroTimeInMillis;//the time at which retro was triggered
16: optional bool nonLoyalty;//customer is a non-loyalty customer to be ignored by emf
17: required UserDetails userDetails;//all the details of the user
18: optional string source;
19: optional string accountId;
20: optional i32 loyaltyContextId;
21: optional UserDetails groupOwnerUserDetails;
22: optional GroupInfo groupInfo;
23: optional map<string,string> extendedFieldsData;
24: optional list<LineItem> lineItems;
25: optional list<string> uniqueRedemptionId;
}

struct CustomerRegistrationEvent {

   1: required i32 orgID;
   2: required i32 customerID;
   3: required i32 storeUnitID;
   4: required i64 eventTimeInMillis;
   5: optional string uniqueId;
   6: optional string serverReqId;
   7: optional string referrerCode;
   8: optional bool nonLoyalty;//customer is a non-loyalty customer to be ignored by emf
   9: required UserDetails userDetails;//all the details of the user
   10: optional string source;
   11: optional string accountId;
   12: optional i32 loyaltyContextId;
   13: optional UserDetails groupOwnerUserDetails;
   14: optional map<i32,LoyaltyProgramEnrollment> LoyaltyProgramEnrollments;
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
   14: optional string source;
   15: optional string accountId;
   16: optional bool nonLoyalty;
   17: optional i32 loyaltyContextId;
   18: optional UserDetails groupOwnerUserDetails;
}

/**
* Event containing information about the voucher redemption data
*/
struct VoucherRedemptionEventData {

   1: required i32 orgID;
   2: required i32 customerID;
   3: required i32 redeemedVoucherId;
   4: required i32 redeemedVoucherSeriesId;
   5: required i32 redeemedAtStoreUnitId;
   6: required i64 eventTimeInMillis;
   7: optional string uniqueId;
   8: optional string serverReqId;
   9: optional i64 voucherValue;
   10: optional bool nonLoyalty;//customer is a non-loyalty customer to be ignored by emf
   11: required UserDetails userDetails;//all the details of the user
   12: optional string source;
   13: optional string accountId;
   14: optional i32 loyaltyContextId;
   15: optional string redeemedCouponCode;
   16: optional string billId;
   17: optional UserDetails groupOwnerUserDetails;
}

struct VoucherPreRedemptionEventData {

   1: required i32 orgID;
   2: required i32 customerID;
   3: required i32 redeemedVoucherId;
   4: required i32 redeemedVoucherSeriesId;
   5: required i32 redeemedAtStoreUnitId;
   6: required string couponCode;
   7: required i64 eventTimeInMillis;
   8: optional string uniqueId;
   9: optional string serverReqId;
   10: optional i64 voucherValue;
   11: optional bool nonLoyalty;//customer is a non-loyalty customer to be ignored by emf
   12: required UserDetails userDetails;//all the details of the user
   13: optional string source;
   14: optional string accountId;
   15: optional i32 loyaltyContextId;
   16: optional UserDetails groupOwnerUserDetails;
}

struct CancelBillEventData {
   1: required i32 orgID;
   2: required i32 customerID;
   3: required i32 cancelBillID;
   4: required i32 storeUnitID;
   5: required i64 eventTimeInMillis;
   6: optional string uniqueId;
   7: optional string serverReqId;
   8: optional bool nonLoyalty;//customer is a non-loyalty customer to be ignored by emf
   9: required UserDetails userDetails;//all the details of the user
   10: optional string source;
   11: optional string accountId;
   12: optional i32 loyaltyContextId;
   13: optional UserDetails groupOwnerUserDetails;
}

struct ReturnLineItem
{
        1: required i64 id;
        2: required double qty;
}

struct ReturnBillLineitemsEventData
{
   1: required i32 orgID;
   2: required i32 customerID;
   3: required i32 returnBillID;
   4: required list <ReturnLineItem> returnLineItems;
   5: required i32 storeUnitID;
   6: required i64 eventTimeInMillis;
   7: optional string uniqueId;
   8: optional string serverReqId;
   9: optional list <TenderDetails> tenderDetails;
   10: optional bool nonLoyalty;//customer is a non-loyalty customer to be ignored by emf
   11: required UserDetails userDetails;//all the details of the user
   12: optional string source;
   13: optional string accountId;
   14: optional i32 loyaltyContextId;
   15: optional UserDetails groupOwnerUserDetails;
   16: optional i32 lifetimePurchase;
   17: optional i32 prevLifetimePurchase;
   18: optional i32 numberOfVisits;
   19: optional GroupInfo groupInfo;
   20: optional i32 parentBillId;
   21: optional map<string,string> extendedFieldsData;
   22: optional list<LineItem> lineItems;
}

struct ReturnBillAmountEventData
{
   1: required i32 orgID;
   2: required i32 customerID;
   3: required i32 returnBillID;
   4: required double returnAmount;
   5: required i32 storeUnitID;
   6: required i64 eventTimeInMillis;
   7: optional string uniqueId;
   8: optional string serverReqId;
   9: optional list <TenderDetails> tenderDetails;
   10: optional bool nonLoyalty;//customer is a non-loyalty customer to be ignored by emf
   11: required UserDetails userDetails;//all the details of the user
   12: optional string source;
   13: optional string accountId;
   14: optional i32 loyaltyContextId;
   15: optional UserDetails groupOwnerUserDetails;
   16: optional i32 lifetimePurchase;
   17: optional i32 prevLifetimePurchase;
   18: optional i32 numberOfVisits;
   19: optional GroupInfo groupInfo;
   20: optional i32 parentBillId;
   21: optional map<string,string> extendedFieldsData;
   22: optional list<LineItem> lineItems;
}

struct TrackerConditionSuccessEventData
{
   1: required i32 orgID;
   2: required i32 customerID;
   3: required i32 trackerID;
   4: required i32 trackerConditionID;
   5: required i32 storeUnitID;
   6: required double currentAggregate;
   7: required double trackedValue;
   8: required i64 timeInMillis;
   /*
   * DO NOT CHANGE ORDER UNLESS YOU ARE MODIFYING ALL END POINTS
   *	CUSTOMER = 1
   *	BILL = 2
   *	BILL_LINEITEM = 3
   */
   9: required i32 referenceType;
   10: required i64 referenceID;
   11: required i32 numberOfVisits;
   12: optional string uniqueId;
   13: optional string serverReqId;
   14: optional list <TenderDetails> tenderDetails;
   15: optional i64 retroTimeInMillis;//the time at which retro was triggered
   16: optional bool nonLoyalty;//customer is a non-loyalty customer to be ignored by emf
}

struct TransactionFinishedEventData {
   1: required i32 orgID;
   2: required i32 customerID;
   3: required i32 billID;
   4: required i32 storeUnitID;
   5: required i64 eventTimeInMillis;
   6: required i32 billAmount;
   7: required i32 lifetimePurchase;
   8: required i32 prevLifetimePurchase;
   9: required i32 numberOfVisits;
   10: optional string uniqueId;
   11: optional string serverReqId;
   12: optional list <TenderDetails> tenderDetails;
   13: optional i64 retroTimeInMillis;//the time at which retro was triggered
   14: optional bool nonLoyalty;//customer is a non-loyalty customer to be ignored by emf
}

struct CustomFieldsData {
   1: required i32 assocID;
   2: required string customFieldName;
   3: optional string customFieldType;
   4: optional string previousCustomFieldValue;
   5: optional string customFieldValue;
}

struct CustomerUpdateEventData {
   1: required i32 orgID;
   2: required i32 customerID;
   3: required i32 storeUnitID;
   4: required i64 eventTimeInMillis;
   5: optional string previousFirstName;
   6: optional string firstName;
   7: optional string previousLastName;
   8: optional string lastName;
   9: optional string previousMobileNumber;
   10: optional string mobileNumber;
   11: optional string previousEmail;
   12: optional string email;
   13: optional string previousExternalId;
   14: optional string externalId;
   15: optional string uniqueId;
   16: optional string serverReqId;
   17: optional list <CustomFieldsData> customFieldsData;
   18: optional bool nonLoyalty;
   19: required UserDetails oldUserDetails;//all the details of the user
   20: required UserDetails newUserDetails;//all the details of the user
   21: optional string source;
   22: optional string accountId;
   23: optional bool oldNonLoyalty;
   24: optional i32 loyaltyContextId;
   25: optional UserDetails groupOwnerUserDetails;
   26: optional map<i32,LoyaltyProgramEnrollment> LoyaltyProgramEnrollments;
}

struct TransactionUpdateEventData {
   1: required i32 orgID;
   2: required i32 customerID;
   3: required i32 billID;
   4: required i32 storeUnitID;
   5: required i64 eventTimeInMillis;
   6: optional string uniqueId;
   7: optional string serverReqId;
   8: optional list <CustomFieldsData> customFieldsData;
   9: optional bool nonLoyalty;//customer is a non-loyalty customer to be ignored by emf
   10: required UserDetails userDetails;//all the details of the user
   11: optional string source;
   12: optional string accountId;
   13: optional i32 loyaltyContextId;
   14: optional UserDetails groupOwnerUserDetails;
   15: optional map<string,string> extendedFieldsData;
   16: optional list<LineItem> lineItems;
}

struct SocialConnectEventData {
  1: required i32 orgId;
  2: required i32 storeUnitId;
  3: required i32 userId;
  4: required i64 eventTimeInMillis;
  5: required string uniqueId;
  6: required string moduleName;
  7: required string channelName;
  8: required string type;
  9: required i64 publishedOn;
 10: required string activityChannelId;
 11: required string actorChannelId;
 12: optional string targetChannelId;
 13: optional i64 updatedOn;
 14: optional string title;
 15: optional string url;
 16: optional string visibility;
 17: optional string flowCode;
 18: optional string stepCode;
 19: optional string serverReqId;
 20: optional bool nonLoyalty;//customer is a non-loyalty customer to be ignored by emf
 21: required UserDetails userDetails;//all the details of the user
 22: optional string source;
 23: optional string accountId;
 24: optional i32 loyaltyContextId;
 25: optional UserDetails groupOwnerUserDetails;
}

struct SocialConnectUpdateEventData {
   1: required i32 orgID;
   2: required i32 customerID;
   3: required i64 eventTimeInMillis;
   4: required string eventType;
   5: required string flowCode;
   6: required string stepCode;
   7: required double value;
   8: optional string uniqueId;
   9: optional string serverReqId;
   10: optional bool nonLoyalty;//customer is a non-loyalty customer to be ignored by emf
   11: optional i32 loyaltyContextId;
}


struct DelayedAccrualEventData {
   1: required i32 orgID;
   2: required i32 customerID;
   3: required i32 storeUnitId;
   4: required i64 eventTimeInMillis;
   5: required string uniqueId;
   6: required string serverReqId;
   7: required bool nonLoyalty;
   8: required UserDetails userDetails;
   9: required string source;
   10: required double pointsValue;
   11: required double returnPoints;
   12: required double redeemedPoints;
   13: required double expiredPoints;
   14: optional string accountId;
   15: optional i32 loyaltyContextId;
   16: optional UserDetails groupOwnerUserDetails;
}


struct Product {
    1: required string code;
    2: optional double rate;
    6: optional string category;
    7: optional list<string> categoryParents;
    8: optional string brand;
    9: optional list<string> brandParents;
}


struct ScanEventData{
   1: required i32 orgID;
   2: required i32 customerID;
   3: required i32 storeUnitId;
   4: required i64 eventTimeInMillis;
   5: required string uniqueId;
   6: required string serverReqId;
   7: required bool nonLoyalty;
   8: required UserDetails userDetails;
   9: required string source;
   10: optional string promotion;
   11: optional Product currentProduct;
   12: optional string accountId;
   13: optional i32 loyaltyContextId;
   14: optional UserDetails groupOwnerUserDetails;
}


 struct CampaignRefereeRedeemEventData {
   1: required i32 orgID;
   2: required i32 referrerID;
   3: required i32 refereeID;
   4: required i32 redeemedStoreUnitID;
   5: required string newVoucherCode;
   6: required i32 numReferralRedemptions;
   7: required string redeemedVoucherCode;
   8: required i64 redeemedTimeInMillis;
   9: required i32 totalTimesRedeemed;
   10: optional string uniqueId;
   11: optional string serverReqId;
   12: optional bool nonLoyalty;//customer is a non-loyalty customer to be ignored by emf
   13: required UserDetails userDetails;//all the details of the user
   14: optional string source;
   15: optional string accountId;
   16: optional i32 loyaltyContextId;
   17: optional UserDetails groupOwnerUserDetails;
}

struct CampaignReferralReferrerEventData {
   1: required i32 orgID;
   2: required i32 referrerID;
   3: required i32 storeID;
   4: required string issuedVoucherCode;
   5: required i32 numOfReferrals;
   6: required i32 numOfReferralsToday;
   7: required i64 eventTimeInMillis;
   8: optional string uniqueId;
   9: optional string serverReqId;
   10: optional bool nonLoyalty;//customer is a non-loyalty customer to be ignored by emf
   11: required UserDetails userDetails;//all the details of the user
   12: optional string source;
   13: optional string accountId;
   14: optional i32 loyaltyContextId;
   15: optional UserDetails groupOwnerUserDetails;
}

struct CampaignReferralEventData {

   1: required i32 orgID;
   2: required i32 referrerID;
   3: required i32 refereeID;
   4: required i32 storeUnitID;
   5: required string voucherCode;
   6: required i64 eventTimeInMillis;
   7: optional string uniqueId;
   8: optional string serverReqId;
   9: optional bool nonLoyalty;//customer is a non-loyalty customer to be ignored by emf
   10: required UserDetails userDetails;//all the details of the user
   11: optional string source;
   12: optional string accountId;
   13: optional i32 loyaltyContextId;
   14: optional UserDetails groupOwnerUserDetails;
}

struct IncomingSmsEventData {

   1: required i32 orgID;
   2: required i32 userID;
   3: required string smsCode;
   4: required i32 storeUnitID;
   5: required i64 eventTimeInMillis;
   6: optional string uniqueId;
   7: optional string serverReqId;
   8: optional bool nonLoyalty;//customer is a non-loyalty customer to be ignored by emf
   9: required UserDetails userDetails;//all the details of the user
   10: optional string source;
   11: optional string accountId;
   12: optional i32 loyaltyContextId;
   13: optional UserDetails groupOwnerUserDetails;
}

struct RuleSummary {

   1: required i32 ruleId;
   2: required i32 noOfTransactions;
   3: required i32 successVoucherCount;
   4: required i32 failureVoucherCount;
}

struct VoucherSummary {

   1: required i32 voucherSeriesId
   2: required i32 count;
   3: required i32 noOfTransactions;
}

struct SimulationResult {

   1: required i32 totalTransactions;
   2: required bool isError;
   3: required string resultMessage;
   4: optional list<RuleSummary> ruleSummaryList;
   5: optional list<VoucherSummary> voucherSummaryList;
}

struct SimulationInputData {

   1: required i32 orgId;
   2: required i64 startTimeInMillis;
   3: required i64 endTimeInMillis;
   4: required i32 campaignId;
   5: required string serverRequestId;
   6: optional i32 loyaltyContextId;
}

struct ReferralPostProcessingEventData {
   1: required i32 orgId;
   2: required i32 campaignId;
   3: required i32 userId;
   4: required string referrerCode;
   5: optional string serverReqId;
   6: optional bool nonLoyalty;//customer is a non-loyalty customer to be ignored by emf
   7: required UserDetails userDetails;//all the details of the user
   8: optional string source;
   9: optional string accountId;
   10: optional i32 loyaltyContextId;
   11: optional UserDetails groupOwnerUserDetails;
}

struct EmailOpenEventData {
   1: required i32 orgID;
   2: required i32 campaignId;
   3: required i32 customerID;
   4: required i64 eventTimeInMillis;
   5: optional i32 msgId;
   6: optional map<string,string> props;
   7: optional string serverReqId;
   8: required i32 storeUnitID;
   9: optional bool nonLoyalty;//customer is a non-loyalty customer to be ignored by emf
   10: required UserDetails userDetails;//all the details of the user
   11: optional string source;
   12: optional string accountId;
   13: optional i32 loyaltyContextId;
   14: optional UserDetails groupOwnerUserDetails;
}

struct EmailClickEventData {
   1: required i32 orgID;
   2: required i32 campaignId;
   3: required i32 customerID;
   4: required i64 eventTimeInMillis;
   5: optional i32 msgId;
   6: optional map<string,string> props;
   7: optional string serverReqId;
   8: required i32 storeUnitID;
   9: optional bool nonLoyalty;//customer is a non-loyalty customer to be ignored by emf
   10: required UserDetails userDetails;//all the details of the user
   11: optional string source;
   12: optional string accountId;
   13: optional i32 loyaltyContextId;
   14: optional UserDetails groupOwnerUserDetails;
}

struct GroupMemberJoinEventData {
   1: required i32 orgID;
   2: required i32 customerID;
   3: required i32 storeUnitID;
   4: required i64 eventTimeInMillis;
   5: optional string uniqueId;
   6: optional string serverReqId;
   7: optional bool nonLoyalty;//customer is a non-loyalty customer to be ignored by emf
   8: required UserDetails userDetails;//all the details of the user with user group details
   9: optional string source;
   10: optional string accountId;
   11: optional i32 loyaltyContextId;
   12: required UserDetails groupOwnerUserDetails;
}

struct GroupMemberLeaveEventData {
   1: required i32 orgID;
   2: required i32 customerID;
   3: required i32 storeUnitID;
   4: required i64 eventTimeInMillis;
   5: optional string uniqueId;
   6: optional string serverReqId;
   7: optional bool nonLoyalty;//customer is a non-loyalty customer to be ignored by emf
   8: required UserDetails userDetails;//all the details of the user
   9: optional string source;
   10: optional string accountId;
   11: optional i32 loyaltyContextId;
}

struct PointsTransferEventData {
   1: required i32 orgID;
   2: required i32 transferredAtStoreUnitID;
   3: required i64 eventTimeInMillis;
   4: required i32 numPointsToBeTransferred;
   5: required UserDetails fromCustomerDetails;//details of the transfer initiating user
   6: required UserDetails toCustomerDetails;//details of the transfer accepting user
   7: optional string uniqueId;
   8: optional string serverReqId;
   9: optional string notes;
   10: optional string source;
   11: optional string accountId;
   12: optional i32 loyaltyContextId;
   13: optional string validationCode;
   14: optional i32 referenceId;
   15: optional GroupInfo fromCustomerGroupInfo;
   16: optional GroupInfo toCustomerGroupInfo;
}

struct Target{
   1: required string name;
   2: required string targetType;//e.g. Sales, Quantity
   3: required i64 currentCycleDefinedTarget;
   4: required i64 currentCycleAchievedValue;
}

/**
* A target group contains a list of target.
* period for all these targets will be same
*/
struct TargetGroup{
   1: required i64 id;
   2: required string name;
   3: required i64 startDate;
   4: required i64 endDate;
   5: required i64 currentCycleStartDate;
   6: required i64 currentCycleEndDate;
   7: required string currentPeriodName;
   8: required list<Target> targetList;
}

/**
* contains information about the target complete event.
*/
struct TargetCompletedEventData {
   1: required i32 orgID;
   2: required i32 storeUnitID;
   3: required i64 eventTimeInMillis;
   4: required UserDetails userDetails;//all the details of the user
   5: required TargetGroup targetGroup;
   6: optional string uniqueId;
   7: optional string serverReqId;
   8: optional string referrerCode;
   9: optional string source;
   10: optional string accountId;
   11: optional i32 loyaltyContextId;
}

/**
* contains information about the points redemption reversal event.
*/
struct PointsRedemptionReversalEventData {
   1: required i32 orgID;
   2: required i32 storeUnitID;
   3: required i64 eventTimeInMillis;
   4: required UserDetails userDetails;//all the details of the user
   5: required string uniqueRedemptionId;
   6: optional double pointsToBeReversed
   7: optional string uniqueId;
   8: required string serverReqId;
   9: optional string source;
   10: optional string accountId;
   11: optional i32 loyaltyContextId;
   12: optional string notes;
}

/**
* Event containing information about the generic event.
*/
struct GenericEvent {
  1: required i32 orgID;
  2: required i32 customerID;
  3: required i32 storeUnitID;
  4: required i64 eventTimeInMillis;
  5: required string genericEventId;
  6: required string genericEventName;
  7: required string uniqueId;
  8: required string serverReqId;
  9: required UserDetails userDetails;//all the details of the user
  10: required string source;
  11: required string accountId;
  12: required map<string, string> eventData;
  13: optional Product currentProduct;
  14: optional string referrerCode;
  15: optional i32 loyaltyContextId;
  16: optional UserDetails groupOwnerUserDetails;
  17: optional GroupInfo groupInfo;

}

struct SideEffects {
  1: required list <Instruction> instructions;
}

struct Page {
  1: required i32 pageNumber;
  2: required i32 pageSize;
}

struct SideEffectsFilter {
  1: required i32 orgId;
  2: required i32 customerId;
  3: optional string eventName;
  4: optional list <string> uniqueIds;
  5: optional i64 eventTimeInMillis;
  6: optional i32 promoId;
  7: optional Page page;
}

struct EvaluationLog {
    1: required string id;
    2: required i64 customerId;
    3: required i64 date;
    4: required string eventName;
    5: required string hostname;
    6: required i64 orgId;
    7: required string requestId;
    8: required i64 transactionId;
    9: required string uniqueId;
    10: required string evaluationTree;
    11: required string effects;
}

struct EvaluationLogSearchRequest {
    1: optional i64 customerId;
    2: optional i64 dateGte;
    3: optional i64 dateLte;
    4: optional string eventName;
    5: optional string hostname;
    6: required i64 orgId;
    7: optional string requestId;
    8: optional i64 transactionId;
    9: optional string uniqueId;
    10: optional i64 limit;
    11: optional i64 skip;
}

service EMFService {

	//LIFE CYCLE
	/**
	* Checks if the event management service is in a running state
	*/
	bool isRunning(1: string serverReqId);

	//same as is running
	bool isAlive();

	//ORGANIZATION RELATED
     /**
     * @param orgID The id of the org
     * @return True, iff the event management framework is accepting events for the passed org.
     */
     bool isOrganizationEnabled (1: i32 orgID, 2: string serverReqId);

     /**
     * @param orgID The org id.
     * @return True, iff the org was successfiully disabled.
     */
     bool disableOrganization (1: i32 orgID, 2: string serverReqId) throws (1 :EMFException ex);

	 /**
     * @param orgID The id of the org for which the configuration has to be checked
     * @param serverReqId server request id
     * @return Whether the org configuration is fine or not
     */
	bool checkOrganizationConfiguration(1:i32 orgID, 2: string serverReqId) throws (1 :EMFException ex);


	 //EVENT RELATED
     /**
     * @param newBillEvent The event data for new bill.
     * @return The evaluation result for this event.
     */
     EventEvaluationResult newBillEvent (1: NewBillEvent newBillEvent, 2: bool isCommit, 3: bool isReplayed) throws (1 :EMFException ex);

    /**
     * @param newBillEvent The event data for new bill.
     * @return The evaluation result for this event.
     */
     EventEvaluationResult newBillDVSEvent (1: NewBillEvent newBillEvent, 2: bool isCommit, 3: bool isReplayed) throws (1 :EMFException ex);

     /**
     * @param registrationEvent The event data for customer registration related event.
     * @return The evaluation result for this event.
     */
     EventEvaluationResult registrationEvent (1: CustomerRegistrationEvent registrationEvent, 2: bool isCommit, 3: bool isReplayed)
	 throws (1 :EMFException ex);

	/**
     * @param pointsRedemptionEventData The event data for points redemption.
     * @return The evaluation result for this event.
     */
     EventEvaluationResult pointsRedemptionEvent (1: PointsRedemptionEventData pointsRedemptionEventData, 2: bool isCommit, 3: bool isReplayed)
	 throws (1 :EMFException ex);

     /**
     * @param voucherRedemptionEventData the data for which voucher redemption will happen
     * @return The evaluation result for this event
     */
     EventEvaluationResult voucherPreRedemptionEvent(1: VoucherPreRedemptionEventData voucherPreRedemptionEventData, 2: bool isCommit, 3: bool isReplayed) throws (1 :EMFException ex);

	/**
     * @param voucherRedemptionEventData The event data for voucher redemption.
     * @return The evaluation result for this event.
     */
     EventEvaluationResult voucherRedemptionEvent (1: VoucherRedemptionEventData voucherRedemptionEventData, 2: bool isCommit, 3: bool isReplayed)
	 throws (1 :EMFException ex);

	/**
     * @param returnLineitemsEventData The event data for return bill lineitems
     * @return The evaluation result for this event.
     */
     EventEvaluationResult returnLineitemsEvent (1: ReturnBillLineitemsEventData returnBillLineitemsEventData, 2: bool isCommit, 3: bool isReplayed)
	 throws (1 :EMFException ex);

	/**
     * @param returnBillAmountEventData The event data for return bill amount
     * @return The evaluation result for this event.
     */
     EventEvaluationResult returnBillAmountEvent (1: ReturnBillAmountEventData returnBillAmountEventData, 2: bool isCommit, 3: bool isReplayed)
	 throws (1 :EMFException ex);

	/**
     * @param cancelBillEventData The event data for cancel bill.
     * @return The evaluation result for this event.
     */
     EventEvaluationResult cancelBillEvent (1: CancelBillEventData cancelBillEventData, 2: bool isCommit, 3: bool isReplayed)
	 throws (1 :EMFException ex);

	/**
     * @param trackerSuccessEventData The event data for tracker success
     * @return The evaluation result for this event.
     */
     EventEvaluationResult trackerConditionSuccessEvent (1: TrackerConditionSuccessEventData trackerConditionSuccessEventData, 2: bool isCommit, 3: bool isReplayed)
        throws (1 :EMFException ex);

	/**
     * @param customerUpdateEventData the event data for customer update event
     * @return The evaluation result for this event.
     */
     EventEvaluationResult customerUpdateEvent (1: CustomerUpdateEventData customerUpdateEventData, 2: bool isCommit, 3: bool isReplayed)
 	throws (1 :EMFException ex);

	 /**
     * @param transactionUpdateEventData the event data for transaction update event
     * @return The evaluation result for this event.
     */
     EventEvaluationResult transactionUpdateEvent (1: TransactionUpdateEventData transactionUpdateEventData, 2: bool isCommit, 3: bool isReplayed)
 	throws (1 :EMFException ex);

    /**
     * @param socialConnectEvent The event data for social connect
     * @return The evaluation result for this event.
     */
     EventEvaluationResult socialConnectEvent (1: SocialConnectEventData socialConnectEvent, 2: bool isCommit, 3: bool isReplayed)
	 throws (1 :EMFException ex);

     /**
     * @param socialConnectUpdateEvent The event data for social connect update
     * @return The evaluation result for this event.
     */
     EventEvaluationResult socialConnectUpdateEvent (1: SocialConnectUpdateEventData socialConnectUpdateEvent, 2: bool isCommit, 3: bool isReplayed)
         throws (1 :EMFException ex);

     EventEvaluationResult delayedAccrualEvent (1: DelayedAccrualEventData delayedAccrualEvent, 2: bool isCommit, 3: bool isReplayed)
	 throws (1 :EMFException ex);

     /**
     * @param CampaignrRefereeRedeemEvenData The event data for campaign referee redemption
     * @return The evaluation result for this event.
     */
     EventEvaluationResult CampaignRefereeRedeemEvent (1: CampaignRefereeRedeemEventData campaignRefereeRedeemEventData, 2: bool isCommit, 3: bool isReplayed)
        throws (1 :EMFException ex);

    /**
     * @param CampaignReferralReferrerEventData The event data for CampaignReferralReferrerEvent
     * @return The evaluation result for this event.
     */
      EventEvaluationResult CampaignReferralReferrerEvent (1: CampaignReferralReferrerEventData campaignReferralReferrerEventData, 2: bool isCommit, 3: bool isReplayed)
        throws (1 :EMFException ex);

    /**
     * @param scanEventData the event data for scan event
     * @return The evaluation result for this event.
     */
     EventEvaluationResult scanEvent (1: ScanEventData scanEventData, 2: bool isCommit, 3: bool isReplayed)
	throws (1: EMFException ex);

    /**
     * @param CampaignReferralEventData The event data for CampaignReferralEvent
     * @return The evaluation result for this event.
     */
      EventEvaluationResult CampaignReferralEvent (1: CampaignReferralEventData campaignReferralEventData, 2: bool isCommit, 3: bool isReplayed)
	  throws (1 :EMFException ex);

    /**
     * @param IncomingSmsEventData The event data for IncomingSmsEvent
     * @return The evaluation result for this event.
     */
      EventEvaluationResult IncomingSmsEvent (1: IncomingSmsEventData IncomingSmsEventData, 2: bool isCommit, 3: bool isReplayed)
	  throws (1 :EMFException ex);

    /**
     * @param transactionFinishedEvent The event data for transaction finished.
     * @return The evaluation result for this event.
     */
     EventEvaluationResult transactionFinishedEvent (1: TransactionFinishedEventData transactionFinishedEventData, 2: bool isCommit, 3: bool isReplayed) throws (1 :EMFException ex);


    /**
     * @param startDateInMillis Start date
     * @param endDateInMillis End date
     * @return The simulation result for this event.
     */
      SimulationResult simulateRulesBasedOnDateRange (1: SimulationInputData simulationInputData)
	  throws (1 :EMFException ex);

    EventEvaluationResult referralPostProcessingEvent(1: ReferralPostProcessingEventData referralPostProcessingEventData, 2: bool isCommit, 3: bool isReplayed) throws (1 :EMFException ex);

    EventEvaluationResult emailOpenEvent(1: EmailOpenEventData emailOpenEventData, 2: bool isCommit, 3: bool isReplayed) throws (1 :EMFException ex);

    EventEvaluationResult emailClickEvent(1: EmailClickEventData emailClickEventData, 2: bool isCommit, 3: bool isReplayed) throws (1 :EMFException ex);

     /**
     * @param groupMemberJoinEventData The event data for group member join event.
     * @return The evaluation result for this event.
     */
     EventEvaluationResult groupMemberJoinEvent (1: GroupMemberJoinEventData groupMemberJoinEventData, 2: bool isCommit, 3: bool isReplayed)
	 throws (1 :EMFException ex);


     /**
     * @param poinstTranferEventData The event data for points transfer event.
     * @return The evaluation result for this event.
     */
     EventEvaluationResult pointsTransferEvent (1: PointsTransferEventData pointsTransferEventData, 2: bool isCommit, 3: bool isReplayed)
         throws (1 :EMFException ex);

     /**
     * @param genericEvent The event data for generic event.
     * @return The evaluation result for the event.
     */
     EventEvaluationResult genericEvent (1: GenericEvent genericEvent, 2: bool isCommit, 3: bool isReplayed) throws (1 :EMFException ex);

	 /**
	 * @param endPoint
	 * @param orgId
	 * @return Map of events
	 */
	list<string> getAllGenericEvents(1: i64 orgId, 2: string endPointName, 3: string requestId) throws (1 :EMFException ex);

	/**
	 * @param orgId
	 * @param endPointName
	 * @param eventName
	 * @return boolean
	 */
	 bool isGenericEvent(1: i64 orgId, 2: string endPointName, 3: string eventName, 4: string requestId) throws (1 :EMFException ex);

	 /**
     * @param groupMemberLeaveEventData The event data for group member leave event.
     * @return The evaluation result for this event.
     */
     EventEvaluationResult groupMemberLeaveEvent (1: GroupMemberLeaveEventData groupMemberLeaveEventData, 2: bool isCommit, 3: bool isReplayed)
	 throws (1 :EMFException ex);


	 list<SideEffects> getSideEffectsForCustomer(1: SideEffectsFilter sideEffectsFilter, 2: string serverReqId);

    /**
     * @param targetCompleteEvent The event data for target completed event.
     * @return The evaluation result for this event.
     */
     EventEvaluationResult targetCompletedEvent (1: TargetCompletedEventData targetCompleteEventData, 2: bool isCommit, 3: bool isReplayed) throws (1 :EMFException ex);

     /**
     * @param pointsRedemptionReversalEvent The event data for points redemption reversal event.
     * @return The evaluation result for this event.
     */
     EventEvaluationResult pointsRedemptionReversalEvent (1: PointsRedemptionReversalEventData pointsRedemptionReversalEventData, 2: bool isCommit, 3: bool isReplayed) throws (1 :EMFException ex);


    /**
     * @param requestId This request id.
     * @param request The request body
     *
     * @return List of EvaluationLog objects matching this request
     */
    list<EvaluationLog> searchEvaluationLog (1: string currentRequestId, 2: EvaluationLogSearchRequest search) throws (1 :EMFException ex);
}