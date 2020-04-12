#!thrift -java -php -phps

namespace java com.capillary.campaign.shard.external.thrift.api.server

namespace php campaign_shard

exception CampaignGroupDiscoveryException{
    1:string what
    2:string where
}

exception CampaignGroupUpdateException{
    1:string what
    2:string where
}

exception CampaignDiscoveryException{
    1:string what
    2:string where
}

exception CampaignGroupMergeException{
    1:string what
    2:string where
}

exception CampaignDataException{
    1: required i32 statusCode;
    2: required string errorMessage;
}

exception AudienceGroupException{
    1:i32 errorCode
    2:string errorMessage;
}

enum CampaignGroupType {
    STICKY_GROUP = 1,
    LOYALTY = 2,
    CUSTOMER = 3,
    CAMPAIGN_USERS = 4,
    TEST_GROUP = 5,
    NON_LOYALTY = 6,
    ALL = 7,
    UPLOAD = 8,
    FILTER_BASED = 9,
    DERIVED = 10,
    ORG_USERS = 11
}

enum CampaignTargetType{
    ALL = 1,
    TEST = 2,
    CONTROL = 3,
    EXPERIMENT = 4
}

enum TestControlType{
    ORG = 1,
    CUSTOM = 2,
    SKIP = 3
}

enum UploadType {
    MOBILE = 1,
    EMAIL = 2,
    EXTERNALID = 3,
    USERID = 4
}

enum ListType {
    UPLOAD = 1,
    PASTE = 2,
    MERGE = 3,
    DEDUP  = 4,
    SPLIT = 5,
    DUPLICATE = 6,
    FILTER = 7
}

enum DataSource {
    S3
}

enum ProcessStatus{
  OPEN,
  PROCESSING,
  CLOSED,
  ERROR
}

struct CampaignGroup {
    1: i32 id;
    2: i32 orgId;
    3: i32 campaignId;
    4: i32 groupId;
    5: string groupLabel;
    6: string params;
    7: CampaignGroupType campaignGroupType;
    8: CampaignTargetType campaignTargetType;
    9: i32 customerCount;
    10: bool isFavourite;
    11: i32 createdBy;
    12: i32 lastUpdatedBy;
    13: string createdDate;
    14: string autoUpdateTime;
    15: optional i32 versionNumber;
    16: optional map<string,string> groupTags;
    17: optional i32 bucketId;
    18: optional bool isReloading;
    19: optional bool isVisible=true;
    20: optional string uuId;
    21: optional string s3Path;
    22: optional bool isCampaignListLevel;
    23: optional i32 testGroupPercentage;
    24: optional string s3Headers;
    25: optional string s3BucketTag;
    26: optional i32 customTagCount;
}

struct BucketDetails{
   1: required i32 groupID;
   2: required string groupName;
   3: required string dbHostName;
   4: required string dbUsername;
   5: required string dbPassword;
   6: required string databaseName;
   7: required string groupBucketName;
}

struct BoolRes{
   1: optional bool success;
   2: optional CampaignDataException ex;
}

struct AudienceGroupBoolRes{
   1: optional bool success;
   2: optional AudienceGroupException ex;
}

struct SplitGroup{
   1: string newGroupName;
   2: i32 percentage
}

struct HashLookup{
   1: i32 id;
   2: i32 orgId;
   3: string lookupString;
}

struct GroupIdNamePair {
    1: i32 id;
    2: string name;
}

struct TestControl{
    1: TestControlType type;
    2: i32 testPercentage;
}

enum GroupUpdateType{
   ADD = 1,
   REMOVE = 2
}


struct UploadPasteListInfo {
   1: required string groupName;
   2: required string tempTableName;
   3: required UploadType uploadType;
   4: required i32 customTagCount;
}

struct MergeListInfo{
   1: required string newGroupName;
   2: required list<i32> oldGroupIdList;
}

struct DedupListInfo{
   1:  required bool createNewGroups;
   2:  required list<GroupIdNamePair> groupIdNameList;
}

struct SplitListInfo{
   1: required i32 oldGroupId;
   2: required list<SplitGroup> splitGroupsList;
}

struct DuplicateListInfo{
   1: required i32 oldGroupId;
   2: required string newGroupName;
}

struct FilterListInfo{
   1: required string uuid;
   2: string s3Header;
   3: string s3Path;
   4: string s3BucketTag;
}

struct ListInfo {
   1: required i32 createdBy;
   2: optional UploadPasteListInfo uploadPasteListInfo ;
   3: optional MergeListInfo mergeListInfo;
   4: optional DedupListInfo dedupListInfo;
   5: optional SplitListInfo splitListInfo;
   6: optional DuplicateListInfo duplicateListInfo;
   7: optional FilterListInfo filterListInfo;
}

#--Reachability stuff Starts Here--#

exception ReachabilityServiceException {
    1: required i32 statusCode;
    2: required string errorMessage;
}

enum ReachabilityChannel{
   MOBILE = 1,
   EMAIL = 2,
   WECHAT = 3,
   ALL = 4,
   ANDROID = 5,
   IOS = 6,
   LINE = 7
}

enum AudienceGroupStatus{
   PREPARE, PROCESSING, ACTIVE, ERROR
}
struct ReachabilityRequest{
   1: required i32 orgID;
   2: required i32 campaignID;
   3: required i32 groupID;
   4: required ReachabilityChannel channel;
   5: optional bool reTryLastFailedJob;
}

struct ReachabilityBreakup {
 1: required string sendingRules ;
 2: required i32 count ;
 3: required bool status ;
}

struct GroupResponse {
 1: required i32 totalCustomerCount ;
 2: required bool isFavourite ;
 3: required i32 testCount ;
 4: required i32 controlCount ;
 5: required i32 mobileCount ;
 6: required i32 emailCount ;
 7: required string groupType;
 8: required string groupLabel;
 9: required list<ReachabilityBreakup> emailBreakup ;
 10: required list<ReachabilityBreakup> mobileBreakup ;
 11: required map<string,string> wechatServiceIdToOpenIdsCountMap;
 12: required ProcessStatus reachabilityJobStatus;
 13: optional bool isReloading;
 14: optional bool isVisible;
 15: optional string uuId;
}


struct ReachabilityResponse {
   1: required i32 campaignID;
   2: required map<string, GroupResponse> groupResponseBreakupMap;
   3: required map<string, string> categoryToLabelMap;
}

struct ReloadableGroup{
   1: required i32 orgId;
   2: optional i32 campaignId;
   3: optional i32 groupId;
   4: optional i32 messageId;
}

enum AudienceTargetType{
    TEST = 1,
    CONTROL = 2
}

enum AudienceGroupType {
    UPLOADED = 1,
    FILTER_BASED = 2,
    DERIVED = 3
}

struct ReachabilitySummaryReport{
   1: string label;
   2: string category;
   3: i32 count;
}

struct AudienceGroupReachabilityResponse{
  1: map<ReachabilityChannel,list<ReachabilitySummaryReport>> channelToSummaryMap;
  2: map<ReachabilityChannel,map<string,i32>> channelToAccountCount;
}

struct AudienceGroupVersion {
  1: i32 groupVersionId;
  2: i32 versionNumber;
  3: TestControl testControl;
  4: i32 customerCount;
  5: i32 audienceGroupId;
  6: optional AudienceGroupReachabilityResponse audienceGroupReachability;
  7: optional AudienceGroupStatus status;
  8: optional string errorDescription;
}

enum EventName{
  GROUP_RELOAD
}

struct AudienceS3Info{
   1: string s3Header;
   2: string s3Path;
   3: i32 customerCount;
   4: optional string bucketName;
}

struct AudienceGroupDataSourceInfo{
    1: optional AudienceS3Info audienceS3Info;
}

struct AudienceGroupUserInfoRequest{
    1: i32 userId;
    2: i32 orgId;
    3: i32 groupId;
    4: optional i32 versionNumber;
}

struct AudienceGroupDataSourceInfoRequest{
    1: i32 orgId;
    2: i32 groupId;
    3: DataSource dataSource;
    4: optional i32 versionNumber;
}

struct AudienceGroup {
    1: i32 groupId;
    2: i32 orgId;
    3: string uuId;
    4: string groupLabel;
    5: AudienceGroupType audienceGroupType;
    6: i32 totalCustomerCount;
    7: i32 createdBy;
    8: map<AudienceTargetType, AudienceGroupVersion> audienceTargetToGroupVersion;
    9: optional bool isFavourite;
    10: optional bool isReloading;
    11: optional bool isVisible;
    12: optional AudienceS3Info audienceS3Info;
    13: optional AudienceGroupDataSourceInfo audienceGroupDataSourceInfo;
    14: optional AudienceGroupStatus status;
    15: optional string errorDescription;
}

struct AudienceGroupChangeSet{
   1: i32 orgId;
   2: i32 groupId;
   3: i32 fromVersionNumber;
   4: i32 toVersionNumber;
   5: AudienceS3Info addedAudienceS3Info;
   6: AudienceS3Info removedAudienceS3Info;
}

struct AudienceSearchRequest{
   1: string searchText = "" ;
   2: optional list<AudienceGroupType> audienceGroupTypes;
   3: optional TestControl testControl;
}

enum AudienceGroupSort {
    CREATED_ON = 1
}

struct GetAudienceGroupRequest{
  1: i32 orgId;
  2: AudienceGroupSort audienceGroupSort;
  3: i32 offset;
  4: i32 limit;
  6: optional string search;
  7: optional CampaignGroupType type;
  8: string requestId;
}


enum AudienceGroupJobStatus {
    OPEN = 1,
    VALIDATING = 2,
    PROCESSING = 3,
    CLOSED = 4,
    ERROR = 5
}

struct AuditInfo {
  1: i32 createdBy;
  2: i64 createdOn;
  3: optional i32 updatedBy;
  4: optional i64 updatedOn;
}

struct AudienceUploadStatus {
  1: string fileUrl;
  2: string uploadedFileName;
  3: optional i32 totalUploadCount;
  4: optional AudienceGroupJobStatus status;
  5: optional string errorFileUrl;
  6: optional i32 errorCount;
}

enum ReachabiltyCategory {
    VALID, INVALID, UNSUBSCRIBED, SOFTBOUNCED, HARDBOUNCED, CONTACT_UNAVAILABLE, UNABLE_TO_VERIFY
}

struct Reachabilty{
  1: ReachabiltyCategory category;
  2: i32 count;
}

struct ChannelReachabilty {
  1: string source;
  2: string accountId;
  3: i32 count;
  4: list<Reachabilty> reachability;
}

struct AudienceReachabilityStats {
  1: ReachabilityChannel channel;
  2: list<ChannelReachabilty> accounts;
}

struct User{
  1: string name;
  2: string email;
  3: string mobile;
}

struct AudienceGroupEntity {
  1: i32 id;
  2: i32 orgId;
  3: string label;
  4: string description;
  5: CampaignGroupType type;
  6: AudienceGroupStatus status;
  7: AuditInfo auditInfo;
  8: i32 versionId;
  9: i32 versionNumber;
  10: optional string uuId;
  11: optional string s3Path;
  12: optional list<AudienceUploadStatus> uploadStatus;
  13: optional i32 customerCount;
  14: optional i32 testCount;
  15: optional i32 controlCount;
  16: optional ProcessStatus reachabilityStatus;
  17: optional list<AudienceReachabilityStats> reachabilityStats;
  18: optional list<User> users;
}

enum SchemaIdentifierType{
  SINGLE_KEY_IDENTIFIER = 1,
  MULTI_KEY_IDENTIFIER = 2
}

enum AudienceSchemaKey{
  MOBILE = 1,
  EMAIL = 2,
  EXTERNAL_ID = 3,
  USER_ID = 4
}

struct UploadAudienceRequest{
  1: SchemaIdentifierType type;
  2: list<AudienceSchemaKey> identifiers;
  3: string s3BucketTag;
  4: optional list<AudienceUploadStatus> uploadedFiles;
  5: optional list<string> data;
  6: DataSource dataSource;
}

struct DerivedAudienceRequest{
  1: list<i64> includeGroups;
  2: optional list<i64> excludeGroups;
}

struct FilterAudienceRequest{
  1: string uuid;
  2: string s3BucketTag;
  3: string s3Headers;
  4: string s3Path;
}

struct CreateAudienceRequest{
  1: i32 orgId;
  2: string label;
  3: string description;
  4: CampaignGroupType type;
  5: i32 createdBy;
  6: optional string tag;
  7: optional list<string> groupTags;
  8: optional UploadAudienceRequest uploadRequest;
  9: optional DerivedAudienceRequest derivedRequest;
  10: optional FilterAudienceRequest filterRequest;
  11: optional i32 groupId;
  12: string requestId;
}

struct OrgUsersGroupRequest{
  1: i64 orgId;
  2: string label;
  3: string description;
  4: i64 createdBy;
  5: list<User> includeUsers;
  6: list<User> excludeUsers;
  7: optional i64 groupId;
  8: string serverRequestId;
}

struct UpdateAudienceGroupRequest{
   1: i64 orgId;
   2: i64 groupId;
   3: optional bool isVisible;
   4: string serverRequestId;
}

service CampaignShardService {

    CampaignGroup create( 1: CampaignGroup campaignGroup, 2: string serverRequestID ) throws (1:CampaignGroupUpdateException ex);

    CampaignGroup update( 1: i32 groupID, 2: bool isReload, 3: CampaignGroup campaignGroup, 4: string serverRequestID ) throws (1:CampaignGroupUpdateException ex);

    CampaignGroup loadAndUpdate( 1: i32 groupID, 2: string serverRequestID ) throws (1:CampaignGroupDiscoveryException gde, 2:CampaignGroupMergeException gme, 3:CampaignGroupUpdateException gue);

    bool deleteGroup( 1: i32 groupID, 2:  string serverRequestID ) throws (1:CampaignGroupUpdateException ex);

    CampaignGroup getGroupDetailsByID( 1: i32 groupID, 2: string serverRequestID ) throws (1:CampaignGroupDiscoveryException ex, 2:CampaignGroupMergeException e);

    CampaignGroup getGroupDetailsByName( 1: string groupLabel, 2: i32 campaignID, 3: string serverRequestID ) throws (1:CampaignGroupDiscoveryException ex, 2:CampaignGroupMergeException e);

    CampaignGroup findByCampaignIdGroupIdType(1:i32 campaignId, 2:i32 groupId, 3:i32 orgID, 4:CampaignTargetType campaignTargetType, 5:string serverRequestId);

    list<CampaignGroup> getAllGroupsByCampaignID( 1: i32 campaignID, 2: i32 orgID ,
        3: bool isFavouriteReq, 4: string search_filter, 5: list<CampaignTargetType> groupTargetType, 6: bool include_inactive, 7: string serverRequestID) throws (1:CampaignDiscoveryException ex, 2:CampaignGroupMergeException e);

    list<CampaignGroup> getAllGroupsByOrgID( 1: i32 orgID, 2: list<CampaignTargetType> groupTargetType, 3: string serverRequestID );

    list<CampaignGroup> getAllGroupsByType( 1: CampaignGroupType campaignGroupType, 2: string serverRequestID ) throws (1:CampaignGroupMergeException e);

    bool isGroupNameAvailable( 1: string label, 2: CampaignTargetType targetType, 3: i32 campaignID, 4: string serverRequestID ) throws (1:CampaignDiscoveryException ex);

    map<string,bool> areGroupNamesAvailable( 1: list<string> groupNames, 2: i32 campaignID, 3: string serverRequestID ) throws (1:CampaignDiscoveryException ex);

    list<CampaignGroup> getAllByIDs( 1: list<i32> groupIDS, 2: string serverRequestID ) throws (1:CampaignGroupDiscoveryException ex, 2:CampaignGroupMergeException e);

    BucketDetails getBucketDetailsByGroupID( 1: i32 groupID, 2: string serverRequestID ) throws (1:CampaignGroupDiscoveryException ex);

    i32 getPeerGroupID(1: i32 groupId, 2: string serverRequestID);

    bool isAlive() throws (1:CampaignGroupDiscoveryException ex);

    BoolRes insertGroupRecipients(1:CampaignGroup thriftCampaignGroup, 2:string campaignFilterTempTable, 3:string requestId) throws  (1:CampaignDataException ex);

    i32 getUpdatedGroupVersionId(1: i32 groupVersionId, 2: CampaignTargetType campaignTargetType, 3: string requestId) throws (1:CampaignGroupDiscoveryException ex);

    void  updateGroupMetaInfo(1: i32 groupVersionId, 2: i32 orgId, 3: string requestId) throws (1:CampaignGroupDiscoveryException ex);

    list<CampaignGroup> getAllByGroupId(1:i32 campaignId, 2:i32 groupId, 3:i32 orgId, 4:string requestId);

    bool updateUserIds(1: i32 orgId,  2: UploadType uploadType, 3: map<string,string> info, 4: string requestId) throws (1: CampaignDataException ex);

    bool uploadOrPasteRecipients( 1: i32 orgID, 2: i32 groupVersionId, 3: map<string,string> info, 4: UploadType uploadType, 5: string requestId) throws (1: CampaignDataException ex);

    bool updateUsersInGroup( 1: i32 orgID, 2: i32 oldGroupVesrionId, 3: i32 newGroupVersionId, 4: i32 userId, 5: GroupUpdateType groupUpdateType, 6: string customTags 7: string requestId) throws (1: CampaignDataException ex);

    bool exportUsers(1: i32 exportMappingId, 2:list<i32> versionIds, 3:i32 orgId, 4:string requestId) throws (1:CampaignDataException ex);

    void exportToS3(1: i32 groupVersionId, 2:string s3Bucket, 3:string s3Path, 4:string requestId) throws (1:CampaignDataException ex);

    bool updateHashLookup(1: HashLookup lookup, 2: string requestId) throws (1:CampaignDataException ex);

    list<CampaignGroup> createNewGroupVersions(1:i32 groupId, 2:i32 campaignId, 3:i32 orgId, 4:string requestId) throws (1:CampaignGroupUpdateException ex);

    BoolRes createGroupRecipients(1:CampaignGroup thriftCampaignGroup, 2:string requestId) throws  (1:CampaignDataException ex);

    BoolRes createGroupRecipientsForCustomTags(1:CampaignGroup thriftCampaignGroup, 2:string requestId) throws  (1:CampaignDataException ex);

    BoolRes reloadGroup(1:CampaignGroup thriftCampaignGroup, 2:string requestId) throws  (1:CampaignDataException ex);

    //--Reachability Service--//
	ReachabilityResponse getReachabilityProgressByID(1:ReachabilityRequest request, 2:string serverRequestID) throws (1:ReachabilityServiceException ex);

	ReachabilityResponse getReachabilityProgressByCampaignID (1:ReachabilityRequest request, 2:string serverRequestID) throws (1:ReachabilityServiceException ex);

	i32 updateReachabilityStatus(1:ReachabilityRequest request, 2:string serverRequestID) throws (1:ReachabilityServiceException ex);

	list<CampaignGroup> getAllByUuid(1:i32 orgId, 2:i32 campaignId, 3:string uuid, 4:string serverRequestId) throws (1:CampaignGroupDiscoveryException ex);

        bool copyCustomTags(1: i32 orgId, 2: i32 newGroupVersionId, 3: i32 oldGroupVersionId, 4: string requestId) throws (1: CampaignDataException ex);

	list<CampaignGroup> createGroup(1: CampaignGroup campaignGroup, 24: TestControl testControl, 3: string requestId) throws (1: CampaignGroupUpdateException ex);

	list<i32> createList( 1: i32 orgID, 2: i32 campaignID, 3: ListType listType , 4: ListInfo listInfo ,5: string requestId) throws (1: CampaignDataException ex);

	BoolRes markDuplicateUsers(1: i32 orgId, 2:i32 campaignId, 3:i32 groupId,  4:string tempTable, 5:string requestId) throws(1: CampaignDataException ex);

	void triggerMDWGroupReloadForOrg(1:i32 orgId, 2:string requestId) throws (1: CampaignDataException ex);

        void triggerReonGroupReloadForOrg(1:i32 orgId, 2:string requestId) throws (1: CampaignDataException ex);

	bool updateControlGroupUserHistory(1: i32 orgId, 2: i32 campaignId, 3: i32 groupId, 4: i32 messageId, 5: string requestId) throws (1: CampaignDataException ex);

	void updateReloadableGroup(1:ReloadableGroup group, 2:string requestId) throws (1: CampaignDataException ex);

	BoolRes isGroupReloadDone(1:i32 groupId, 2:i32 orgId, 3:string requestId);

	map<string,string> getCustomTagsForSampleUser(1:i32 groupVersionId, 2:i32 orgId, 3:string requestId) throws (1: CampaignDataException ex);
}

service AudienceGroupManagerService {

  AudienceGroup getAudienceGroupById(1: i32 groupId, 2: i32 orgId, 3: bool reachabilityDetails, 4: string serverRequestId) throws (1:AudienceGroupException e);

  AudienceGroup getAudienceGroupByUuId(1: string uuId, 2: i32 orgId, 3:  bool reachabilityDetails, 4: string serverRequestId) throws (1:AudienceGroupException e);

  AudienceGroupVersion getAudienceGroupVersion(1: i32 groupVersionId, 2: i32 orgId, 3: string serverRequestId) throws (1:AudienceGroupException e);

  list<AudienceGroup> getAllAudienceGroupByGroupIds(1: list<i32> groupIds, 2: i32 orgId, 3: string serverRequestId) throws (1:AudienceGroupException e);

  list<AudienceGroup> getAllAudienceGroupByUuIds(1: list<string> uuIds, 2: i32 orgId, 3: string serverRequestId) throws (1:AudienceGroupException e);

  list<AudienceGroup> searchAudienceGroup(1: i32 orgId, 2: list<AudienceGroupType> audienceGroupTypes, 3: string serverRequestId) throws (1:AudienceGroupException e);

  list<AudienceGroup> searchAudienceGroupByLabel(1: i32 orgId, 2: string groupLabel, 3: list<AudienceGroupType> audienceGroupTypes, 4: string serverRequestId) throws (1:AudienceGroupException e);

  list<AudienceGroup> newSearchAudienceGroup(1: i32 orgId, 2: AudienceSearchRequest audienceSearchRequest , 3: string serverRequestId) throws (1:AudienceGroupException e);

  list<AudienceGroup> newSearchAudienceGroupByLabel(1: i32 orgId, 2: AudienceSearchRequest audienceSearchRequest , 3: string serverRequestId) throws (1:AudienceGroupException e);

  list<AudienceGroup> searchAudienceGroupByCampaign(1: i32 orgId, 2: list<AudienceGroupType> audienceGroupTypes, 3: string groupLabel, 4: i32 campaignId, 5: string serverRequestId) throws (1:AudienceGroupException e);

  AudienceGroupBoolRes subscribe(1:EventName eventName, 2:i32 orgId, 3:i32 groupId, 4:string entityName, 5:string entityId, 6:string params, 7:i32 updatedBy, 8:string requestId) throws (1:AudienceGroupException e);

  AudienceGroupBoolRes unsubscribe(1:EventName eventName, 2:i32 orgId, 3:i32 groupId, 4:string entityName, 5:string entityId, 6:i32 updatedBy, 7:string requestId) throws (1:AudienceGroupException e);

  AudienceGroup getAudienceGroupS3Info(1:i32 orgId, 2:i32 groupId, 3:i32 versionNumber, 4:string requestId) throws (1:AudienceGroupException e);

  AudienceGroupChangeSet getChangeSetForAudienceGroup(1:i32 orgId, 2:i32 groupId, 3:i32 fromVersionNumber, 4:string requestId) throws (1:AudienceGroupException e);

  AudienceGroupBoolRes isUserInGroup(1:AudienceGroupUserInfoRequest audienceGroupUserInfoRequest, 2:string serverRequestId) throws (1:AudienceGroupException e);

  AudienceGroup getAudienceGroupWithDataSourceInfo(1:AudienceGroupDataSourceInfoRequest audienceGroupDataSourceInfoRequest, 2:string serverRequestId) throws (1:AudienceGroupException e);

  list<AudienceGroupEntity> getAllAudienceGroup(1: GetAudienceGroupRequest getAudienceGroupRequest) throws (1:AudienceGroupException e);

  AudienceGroupEntity getAudienceGroupEntityById(1:i32 orgId , 2:i32 groupId, 3:string requestId ) throws (1:AudienceGroupException e);

  AudienceGroupBoolRes checkNameExists(1: string name, 2: i32 orgId, 3:string requestId) throws (1:AudienceGroupException e);

  AudienceGroupEntity createAudience(1: CreateAudienceRequest createAudienceRequest) throws (1:AudienceGroupException e);

  AudienceGroupEntity createOrUpdateAudienceGroup(1:CreateAudienceRequest createAudienceRequest) throws (1:AudienceGroupException e);

  list<AudienceGroupEntity> getAudienceGroupEntitiesByGroupIds(1: list<i64> groupIds, 2: i64 orgId, 3: string serverRequestId) throws (1:AudienceGroupException e);

  AudienceGroupEntity createOrUpdateOrgUsersGroup(1:OrgUsersGroupRequest orgUsersGroupRequest) throws (1:AudienceGroupException e);

  i64 updateAudienceGroup(1: UpdateAudienceGroupRequest updateAudienceGroupRequest) throws (1:AudienceGroupException e);

  bool updateErrorStatusForAudienceGroup(1: i64 groupId, 2: i64 orgId, 3: string errorDescription, 4:string requestId) throws (1:AudienceGroupException e);
}
