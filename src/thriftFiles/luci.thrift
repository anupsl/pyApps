#!thrift -java -php -phps

/**
 * This file contains all Luci api service related classes and definitions.
*/

namespace java com.capillary.shopbook.luci.external

namespace php luci


exception LuciThriftException {
	1: required i32 errorCode,
	2: required string errorMsg
}

/**
* To return exception over thrift
*/
struct BoolRes {
    1: optional bool success;
    2: optional LuciThriftException ex;
}

struct CouponRedemptionDetails {
	1: required i64 redemptionId,
	2: required i64 redemptionDate,
	3: optional i64 redeemedByUserId ,//In case of NCA - might not be present 
	4: optional i64 redeemedAtStore ,
	5: optional i64 transactionId ,
	6: optional string transactionNumber ,
	7: optional double billAmount
}

struct ExternalUserIdentifier {//To be used for NCA and partner integration
        1: required string type,//email,mobile etc
        2: required string value
}

struct UserProfile{
        1: required list<ExternalUserIdentifier> userIdentifiers
}

struct CouponRedemptionCount {
       1: required i64 userId;
       2: required i64 redemptionCount;
}

//kept enum to reduce complexity of deciding which kind of issual should be done.
enum IssualMode {
        NONE = 0, //number of coupons to be issued pram will be considered
        USER_IDENTIFIER = 1 // provided user profiles will be considered
}

struct IssuePartnerCouponRequest {
        1: required string requestId,
        2: required i32 orgId,  // org from which coupon is getting issued
        3: required i32 couponSeriesId,
        4: required i32 clusterAdminUserId,  //admin user id used for service communications mostly for authentication
        5: required i32 partnerOrgId, //org from which communication is happening
        6: required i32 partnerIssuedById,  //original admin user id who had performed the action
        7: required IssualMode issualMode, //defines if to consider userProfiles or numCoupons to issue coupons
        8: required i64 eventTimeInMillis,
        9: optional list<UserProfile> userProfiles,//user profiles
        10: optional i32 numCouponsToBeIssued,
        11: optional bool requireExactMatch, //probably will remove this - if true, will return only if identifiers exactly match, for  now keeping this as default true
        12: optional string notes,
        13: optional bool couponSeriesRequired,
        14: optional bool couponSeriesStatisticsRequired //If true, coupon series statistics will be returned. default is true
}

enum ProductType {
        BRAND,
        CATEGORY,
	SKU
}

struct ProductInfo {
	1: required ProductType productType,
	2: required list<i32> productIds
}

enum UploadCouponStatus {
	STARTED,
	VALIDATED,
	COMMITED,
	FINISHED,
	ERRORED
}

enum OwnedBy{
	NONE,
	LOYALTY,
	OUTBOUND,
        GOODWILL,
	DVS,
	TIMELINE,
	REFERRAL
}

enum RedemptionOrgEntityType{
	ZONE,
	CONCEPT,
	STORE,
	TILL
}

enum RevokeStatus{
    STARTED,
    ERRORRED,
    FINISHED
}

struct CouponUploadInfo {
	1: required i32 jobId,
	2: required UploadCouponStatus uploadStatus,
	3: required i64 createdOn,
	4: required i64 updatedOn,
	5: optional string errorFileUrl,
	6: optional string successFileUrl,
	7: optional string uploadedFileUrl,
	8: optional i32 totalUploadedCount,
	9: optional i32 actualRowCount,
	10: optional i32 errorCount
	11: optional string uploadedFileName
}

struct CouponConfiguration {
1: required i32 id,
2: required i32 org_id,
3: required string description,
4: required string series_type;
5: required string client_handling_type,
6: required string discount_code,
7: optional i64 valid_till_date,
8: required i32 valid_days_from_create,
9: required i32 expiry_strategy_value,//'Number of vouchers in this series that can be used in future',

10: required bool transferrable,
11: required bool any_user,
12: required bool same_user_multiple_redeem,//'Can the same user redeem a voucher multiple times',
13: required bool allow_referral_existing_users,// 'Allow referral for existing users',
14: required bool multiple_use,
15: required bool is_validation_required,//'Is validation code checking required',
16: required bool valid_with_discounted_item,
17: required i64 created_by,
18: required i32 num_issued,
19: required i32 num_redeemed,
20: required i64 created,
21: required i64 last_used,
22: required string series_code,
23: required string sms_template,// 'sms template to be used when resending vouchers',
24: required bool disable_sms,//'If selected, sms for the series should be disabled',
25: required string info,//'Detailed Description',
26: required bool allow_multiple_vouchers_per_user,
27: required bool do_not_resend_existing_voucher,//'If true, does not send the voucher back to the customer again',
28: required string mutual_exclusive_series_ids,//'json array of voucher series ids. A voucher for a user can be present in only one of them',
29: required string store_ids_json,//'ids of the stores where the series is applicable'
30: required bool dvs_enabled,
31: required i64 dvs_expiry_date,
32: required i32 priority,
33: required string terms_and_condition,
34: required bool signal_redemption_event,//'If true, signals a voucher redemption event',
35: required bool sync_to_client,//'Selectively exclude the vouchers that are sent to the client'
36: required string short_sms_template, //'Used for clubbing of sms'
37: required i32 max_vouchers_per_user,//'Maximum number of vouchers per user in the series. -1 implies unlimited',
38: required i32 min_days_between_vouchers,//'minimum number of days between two vouchers',
39: required i32 max_referrals_per_referee,//'maximum number of times any referee can be referred by any referrer',
40: required bool show_pin_code,//'Ability to control the display of pin code at series level',
41: required string discount_on,//'Whether the discount is on BILL OR ITEM',
42: required string discount_type,//'Whether the discount is a percentage or absolute value',
43: required double discount_value,//'value corresponding to discount_type',
44: required string dvs_items,//'To contain descriptions of dvs items to be printed on paper vouchers'
45: required string redemption_range,//'To Define Redemption Range for the voucher series in {''dom:xyz'' , ''dow:xyz'' , ''hours:xyz''} format',
46: required double min_bill_amount,
47: required double max_bill_amount,
48: required string redeem_at_store,
49: optional i32 campaign_id,
50: required string tag,
51: required i32 max_redemptions_in_series_per_user,
52: required i32 min_days_between_redemption,
53: optional i64 redemption_valid_from,
54: required string redeem_store_type,
55: required string expiry_strategy_type, // Supported types are DAYS, MONTHS, MONTHS_END, SERIES_EXPIRY
56: required bool old_flow,
57: required i32 max_create,
58: required i32 max_redeem,
59: required bool pre_redeem_event_required,
60: required i32 source_org_id,
61: required bool issue_to_loyalty,
62: required bool offline_redeem_type,
63: optional list<ProductInfo> productInfo,
64: optional i32 num_uploaded_nonIssued,
65: optional i32 num_uploaded_total,
66: optional i32 redemption_valid_after_days
67: optional OwnedBy owned_by;
68: optional i32 owner_id;
69: optional double discount_upto; // Threshold value of discount. Will be considered only if discount type is PERC
70: optional RedemptionOrgEntityType redemption_org_entity_type; //Supported type of org entity for coupon redemption
71: optional i64 ownerValidity;
72: optional list<CouponUploadInfo> couponUploadInfo;
73: optional bool alphaNumeric;
74: optional i32 shortCodeLength;
75: optional i32 randomCodeLength;
76: optional i64 fixedExpiryDate;
77: optional i32 numTotal;
78: optional i64 latestIssualTime;
79: optional i64 latestRedemptionTime;
80: optional string genericCode;
81: optional bool resendMessageEnabled;
82: optional bool isExternalIssual;
83: optional string purpose;
84: optional string metadata;
}

struct CouponDetails {
	1: required i64 id,//Coupon issued id
	2: required i32 orgId,
	3: required i32 couponSeriesId,
	4: required string couponCode,
	5: required i64 createdDate,
	6: optional i64 issuedDate,
	7: optional i64 activeFromDate,
	8: optional i32 redemptionsLeft,
	9: optional i64 expiryDate,
	10: optional i64 issuedToUserId,//In case of NCA - user id will not be present
	11: optional list<CouponRedemptionDetails> redeemedCoupons,
	12: optional list<ExternalUserIdentifier> userIdentifiers,//Populated in case of NCA
	13: optional i64 issuedById,
	14: optional LuciThriftException ex,
        15: optional CouponConfiguration couponSeries, //Populated when param to return coupon series is passed
        16: optional i64 transactionId,
        17: optional list<CouponRedemptionCount> redemptionCountDetails, //populated only in case if isRedeemable call is successful
        18: optional string couponSeriesDescription
}

struct RedeemCoupon {
	1: required i32 orgId,
	2: required string couponCode,
	3: required i64 storeUnitId,
	4: required i64 eventTimeInMillis,
	5: optional i64 userId,
	6: optional i64 billId,
	7: optional double billAmount,
	8: optional string billNumber,
	9: optional string validationCode
}

struct IssuedCouponDetails {
	1: optional i64 couponId,
	2: optional string couponCode,
	3: optional i64 issuedTo
	4: optional LuciThriftException ex
}

enum ImportType {
	USER_ID = 0,
	MOBILE = 1,
	NONE = 2
}

struct IssueCouponRequest {
	1: required string requestId,
	2: required i32 orgId,
	3: required i32 couponSeriesId,
        4: required i32 storeUnitId,
        5: required i64 userId,
	6: required i64 eventTimeInMillis,
	7: optional i64 billId,
	8: optional i64 criteriaId,
	9: optional bool couponSeriesRequired,
	10: optional bool couponSeriesStatisticsRequired //If true, coupon series statistics will be returned. default is true
}

struct ResendCouponRequest {
	1: required string requestId,
	2: required i32 orgId,
	3: required i32 storeUnitId,
	4: required i64 eventTimeInMillis,
	5: optional i64 userId,
	6: optional string couponCode,
	7: optional i64 couponId,
	8: optional bool couponSeriesRequired,
	9: optional bool couponSeriesStatisticsRequired //If true, coupon series statistics will be returned. default is true
}

struct IssueMultipleCouponsRequest {
	1: required string requestId,
	2: required i32 orgId,
	3: required i32 couponSeriesId,
        4: required i32 storeUnitId,
	5: required list<i64> userIds,
	6: required i64 eventTimeInMillis,
	7: optional i64 groupId,
	8: optional bool couponSeriesRequired,
	9: optional bool couponSeriesStatisticsRequired //If true, coupon series statistics will be returned. default is true
}

struct CouponDetailsRequest {
	1: required string requestId,
	2: required i32 orgId,
	3: optional bool onlyActive,
	/*One of the below filters must be applied. If none are applied, then the method throws an exception*/
	4: optional list<string> couponCodeFilter, //Filters for these coupon codes, if null all coupons are returned.
	5: optional list<i64> couponIdFilter, //filters for these coupon ids, if null, all coupons are returned.
	6: optional list<i64> issuedToIdFilter, //Filters for these user id's. If null, coupons for all users are returned.
	7: optional i32 couponSeriesId,
	8: optional bool couponSeriesRequired,
 	9: optional bool includeProductInfo,
	10: optional bool couponSeriesStatisticsRequired //If true, coupon series statistics will be returned. default is true
}

enum RevokeType {
    COUPON_SERIES,
    ONLY_UNISSUED,
    CUSTOMER_ID,
    COUPON_CODE,
    COUPON_ID,
    CUSTOMER_AND_COUPON
}

struct InvalidateCouponRequest {
	1: required string requestId,
	2: required i32 orgId,
	3: required i32 couponSeriesId,
	4: optional list<IssuedCouponDetails> couponsToBeInvalidated
	5: optional RevokeType revokeType
	6: optional bool reuse
	7: optional bool commit
	8: optional string S3FilePath
	9: optional map<string, i32> revokeHeaders
    10: optional string uploadedFileName
}

enum CouponStatus{
    REDEEMED  ,
    EXPIRED ,
    ACTIVE ,
    UNREDEEMED    // how is it different from active
}

enum CouponSeriesType{
     CAMPAIGN ,
     DVS ,
     ALLIANCE ,
     GOODWILL
}

enum CouponConfigOrderBy{
     CREATED_DATE,
     LAST_MODIFIED_DATE
}

enum OrderBy{
     CREATED_DATE ,
     ISSUED_TILL ,
     EXPIRY_DATE
}

enum Sort{
    ASC  ,
    DESC
}

struct RedemptionFilters {
        1: optional i64 redemptionDateStart,
        2: optional i64 redemptionDateEnd,
        3: optional list<i64> transactionId,
        4: optional list<string> transactionNumber

}

struct IssualFilters {
        1: optional i64 issualDateStart,
        2: optional i64 issualDateEnd,
        3: optional list<i64> transactionId,
        4: optional list<i64> redeemableAtStoreId // this is STORE not TILL
}

// customer ids or coupon series ids, redemptionFilters is mandatory
struct  CouponSearchRequest{
        1: required string requestId,
        2: required i32 orgId,
        3: optional list<i32> couponSeriesIds,
        4: optional list<i64> customerIds,
        5: optional RedemptionFilters redemptionFilters,
        6: optional IssualFilters issualFilters,
        7: optional list<CouponStatus> couponStatus, // to get all active/issued/redeemed/unissued coupons, isRedeemed can be supported by this
        8: optional CouponSeriesType couponSeriesType, // GOODWILL/CAMPAIGN/DVS
        9: optional bool includeRedemptions, // default is false
        10: optional i32 offset,
        11: optional i32 limit,
        12: optional OrderBy orderBy,
        13: optional Sort sort,
        14: optional bool couponSeriesRequired,
        15: optional bool includeProductInfo,
        16: optional bool couponSeriesStatisticsRequired //If true, coupon series statistics will be returned. default is true
}

struct RedeemCouponsRequest {
	1: required string requestId,
	2: required i32 orgId,
	3: required list<RedeemCoupon> redeemCoupons,
	4: required bool commit,
	5: optional bool couponSeriesRequired,
 	6: optional bool includeProductInfo,
	7: optional bool couponSeriesStatisticsRequired //If true, coupon series statistics will be returned. default is true
}

struct SaveCouponConfigRequest {
	1: required string requestId,
	2: required i32 orgId,
	3: required CouponConfiguration couponConfig,
	4: required i32 modifiedBy,
	5: optional bool includeProductInfo //If true, no product info will be returned. if false product info will be returned, default is false
}

struct GetCouponConfigRequest {
	1: required string requestId,
	2: required i32 orgId,
	3: optional i32 couponSeriesId, //If null, return all non-expired coupon series of the org
	4: optional bool includeProductInfo, //If true, no product info will be returned. if false product info will be returned, default is true
	5: optional i32 storeUnitId //if null, org timezone will be used for filtering expired series
	6: optional OwnedBy ownedBy,
	7: optional i32 ownerId,
	8: optional CouponConfigOrderBy orderBy,
	9: optional Sort sort,
	10: optional i32 limit,
	11: optional i32 offset,
	12: optional bool includeExpired
	13:	optional bool uploadInfoRequired // Will get all coupon upload jobs history
	14: optional string seriesDescription
	15: optional string seriesCode
	16: optional bool includeUnclaimed
}


struct GetAllCouponConfigsRequest {
        1: required string requestId,
        2: required i32 orgId,
        3: optional list<i32> couponSeriesIds, //If null, return all coupon series of the org
        4: optional bool includeProductInfo, //If true, product info will be returned. if false product info will not be returned, default is true
        5: optional bool uploadInfoRequired, // Will get all coupon upload jobs history
        6: optional bool couponSeriesStatisticsRequired //If true, coupon series statistics will be returned. default is true
        7: optional bool includeExpired //default true
        8: optional CouponConfigOrderBy orderBy
        9: optional Sort sort
        10: optional i32 limit
        11: optional i32 offset
}



struct UploadCouponRecord {
	1: required i32 serialNo,
	2: optional i64 userId,
	3: optional string couponCode
}

struct UploadCouponsRequest {
	1: required string requestId,
	2: required i32 orgId,
	3: required i32 couponSeriesId,
        4: required ImportType importType,
        5: required i32 uploadedBy,
	6: optional map<string, string> couponCodeVsUserMap,	//user is -1 for disc_code_pin, user_id or mobile for dic_code
	7: optional list<UploadCouponRecord> couponRecordList
	8: optional string s3Location,
        9: optional bool couponSeriesRequired
}

struct DownloadCouponsRequest {
	1: required string requestId,
	2: required i32 orgId,
	3: required i32 couponSeriesId,
	4: optional string s3Location
}

struct VoucherExpiryReminderRequest {
	1: required string requestId,
	2: optional i32 orgId/*pass -1 for all orgs*/
}

struct MergeStatus {
   1: required i32 statusCode;
   2: optional string message;
}

struct MergeResponse {
   1: required i64 fromUserId;
   2: required i64 toUserId;
   3: required MergeStatus status;
}

struct ReloadCouponConfigRequest{
   1: required string requestId,
   2: required i32 orgId,
   3: optional list<i32> couponSeriesIds, //if no coupon series id is  provided, we will reload all coupon series. reloading all coupon series will be a heavy operation.
   4: optional bool invalidateUnissuedCoupons //invalidates unissued coupons, this will not invalidate uploaded DISC_CODE_PIN coupons.
}

struct CouponSearchResponse {
        1: required list<CouponDetails> coupons,
        2: required i32 totalCount
}

struct CouponCreateRequest {
        1: required string requestId,
        2: required i32 orgId,
        3: required i32 couponSeriesId,
        4: required i32 count
}

struct CouponCreateResponse {
       1: required i32 statusCode;
       2: optional string message;
}

struct ClaimCouponConfigRequest{
       1: required string requestId,
       2: required i32 orgId,
       3: required i32 couponSeriesId,
       4: required OwnedBy ownedBy;
       5: optional i32 ownerId,
       6: required i32 modifiedById,
       7: required i64 ownerValidity
}

struct NotifyCouponsUploadRequest {
	1: required string requestId,
	2: required i32 orgId,
	3: required i32 couponSeriesId,
	4: optional i32 totalIssuedCount
}

struct OrgDefaults{
     1: required i32 orgId,
     2: optional string smsTemplate,
     3: optional bool alphaNumeric,
     4: optional i32 shortCodeLength,
     5: optional i32 randomCodeLength,
     6: optional bool syncToInstore,
     7: optional i64 updatedBy,
     8: optional i64 updatedOn,
     9: optional string purposeList
 }

struct SaveOrgDefaultsRequest{
    1: required string requestId,
    2: required i32 orgId,
    3: required OrgDefaults orgDefaults
}

struct GetOrgDefaultsRequest{
    1: required string requestId,
    2: required i32 orgId
}

struct CouponRevokeHistory{
    1: required i32 id
    2: required i32 orgId
    3: required i32 couponSeriesId
    4: required RevokeStatus status
    5: required RevokeType revokeType
    6: required string inputTableName
    7: required string tempTableName
    8: required i32 inputCount
    9: required i32 invalidCount
    10: required i32 unrevokedCount
    11: required i32 revokedCount
    12: required string uploadedFileName
    13: required string uploadedFileHandle
    14: required string errorFileHandle
    15: required string successFileHandle
    16: required i64 createdOn
}

struct GetRevokeHistoryRequest{
    1: required string requestId
    2: required i32 orgId
    3: required i32 couponSeriesId
}

service LuciService {
        //isAlive
        bool isAlive();

	//Per coupon actions
	CouponDetails issueCoupon(1: IssueCouponRequest request) throws (1:LuciThriftException ex);

	CouponDetails resendCoupon(1: ResendCouponRequest request) throws (1:LuciThriftException ex);

	list<CouponDetails> issueMultipleCoupons(1: IssueMultipleCouponsRequest request) throws (1:LuciThriftException ex);

	list<CouponDetails> getCouponDetails(1: CouponDetailsRequest request) throws (1:LuciThriftException ex);

	CouponSearchResponse couponSearch(1: CouponSearchRequest couponSearchRequest)  throws (1: LuciThriftException ex) ;

	bool invalidateCoupons(1: InvalidateCouponRequest request) throws (1:LuciThriftException ex);

	list<CouponDetails> redeemCoupons(1: RedeemCouponsRequest request) throws (1:LuciThriftException ex);

	list<CouponDetails> issuePartnerCoupons(1: IssuePartnerCouponRequest request) throws (1: LuciThriftException ex);

	//Config
	CouponConfiguration saveCouponConfiguration(1: SaveCouponConfigRequest request) throws (1: LuciThriftException ex);

	list<CouponConfiguration> getCouponConfiguration(1: GetCouponConfigRequest request) throws (1: LuciThriftException ex);

	//Deprecated
	//returns map of coupon code to error message
	map<string,string> uploadCoupons(1: UploadCouponsRequest request) throws (1: LuciThriftException ex);

	list<CouponDetails> uploadCouponList(1: UploadCouponsRequest request) throws (1: LuciThriftException ex);

	void downloadCoupons(1: DownloadCouponsRequest request) throws (1: LuciThriftException ex);

	void sendVoucherExpiryReminders(1: VoucherExpiryReminderRequest request) throws (1: LuciThriftException ex);

	i32 getQueueSize(1: i32 orgId, 2: i32 couponSeriesId, 3: string requestId) throws (1: LuciThriftException ex);

        MergeResponse mergeUsers(1:i32 orgId, 2:i64 fromUserId, 3:i64 toUserId, 4:i32 mergedbyTillId, 5:string requestId) throws (1: LuciThriftException ex);

        MergeStatus getMergeStatus(1:i32 orgId, 2:i32 fromUserId, 3:i32 toUserId, 4:string requestId) throws (1: LuciThriftException ex);

	//reloads coupon configs
	bool reloadCouponConfigs(1:ReloadCouponConfigRequest reloadCouponConfigRequest) throws (1: LuciThriftException ex);

	//pump coupons to mongodb
	CouponCreateResponse createCoupons(1: CouponCreateRequest pumpCouponRequest)  throws (1: LuciThriftException ex);

	//required for testing
	bool changeCouponIssuedDate(1:i32 orgId, 2: i64 couponId, 3: i64 issuedDate, 4: string requestId) throws (1: LuciThriftException ex);

	//the data returned will not have upload,issued,redeemed count set, reuuired for API's
	list<CouponConfiguration> getAllCouponConfigurations(1: GetAllCouponConfigsRequest request) throws (1: LuciThriftException ex);

	BoolRes claimCouponConfig(1: ClaimCouponConfigRequest claimCouponConfigRequest) throws (1: LuciThriftException ex);

	void notifyCouponsUploadRequest(1: NotifyCouponsUploadRequest notifyCouponsUploadRequest) throws (1: LuciThriftException ex);

	OrgDefaults saveOrgDefaults(1: SaveOrgDefaultsRequest saveOrgDefaultsRequest) throws (1: LuciThriftException ex);

	OrgDefaults getOrgDefaults(1: GetOrgDefaultsRequest getOrgDefaultsRequest) throws (1: LuciThriftException ex);

	list<CouponRevokeHistory> getRevokeHistory(1: GetRevokeHistoryRequest getRevokeHistoryRequest) throws (1: LuciThriftException ex);

}