#!thrift -java -php

/*
TemporalEngine Interfaces
Author: ketaki
*/

namespace java in.capillary.ifaces.temporalengine
namespace php temporalengine

typedef i32 UserId

/** An org id */
typedef i32 OrgId

/** A lifecycle id */
typedef i32 OrgConfigId

/** A timestamp in milliseconds */
typedef i64 Timestamp

struct Event
{
  1:string name
  2:i32 userId
  3:i32 orgId
  4:map<string, string> properties
}

exception TemporalEngineException {
  1:string what
  2:string where
}

struct SessionId {
  1:required OrgId orgId
  2:optional OrgConfigId orgConfigId
  3:required string apacheThreadId
  4:required UserId userId
  5:required string moduleName
}

/** Rule definition related structs - begin */

enum ContextType {
    MILESTONE
    PHASE
    STATE
    USER_INIT
}

enum LifecycleActionType {
  SendEmail
  SendSMS
  SendOffer
  gap
  JumpPhase
  JumpTimeline
  JumpToEndOfPhase
  NoOperation
  UserInit
}

struct SimplePropertyInfo {
    1: required string key;
    2: required string value;
}

struct ActionInfo {
    1: optional i32 id;
    2: required LifecycleActionType actionName;
    3: optional list <SimplePropertyInfo> mandatoryPropertiesValues;
    4: optional string description;
}

struct CaseActionListInfo {
    1: optional i32 id;
    2: required i32 orgID;
    3: required i32 caseId;
    4: required string value;
    5: required list<ActionInfo> actionsInfos;
}

struct RuleInfo {
    1: optional i32 id;
    2: required i32 orgID;
    3: required string exp;
    4: required string expJSON;
    5: required bool isActive;
    6: required i32 priority;
    7: required Timestamp startDate;
    8: required Timestamp endDate;
    9: required Timestamp createdOn;
    10: required list <CaseActionListInfo> caseActionListInfos;    
    11: required i32 createdBy;
    12: required i32 modifiedBy;
    13: required Timestamp modifiedOn;
    14: optional string name = "";
    15: optional string description = "";
}

struct RulesetInfo {
    1: optional i32 id;
    2: required i32 orgID; 
    3: required string name;
    4: required i32 contextID;
    5: required string contextType;
    6: required list <RuleInfo> rules;
    7: required Timestamp startDate;
    8: required Timestamp endDate;
    9: required Timestamp createdOn
    10: required i32 createdBy;
    11: required i32 modifiedBy;
    12: required Timestamp modifiedOn;
    13: required bool isActive;
    14: optional string description = "";
}

struct DataType {
    1: required string typeName;
    //A comma separated list of allowed values in the enum
    2: optional list <string> allowedValues;
    3: optional bool isMultiSelect;
}

struct SimplePropertyMeta {
  1: required string name;
  2: required DataType dataType;
  3: required bool isMandatory;
  4: optional string defaultValue;
}

struct ActionMeta {
  1: required i32 id;
  2: required LifecycleActionType actionName;
  3: optional list <SimplePropertyMeta> simpleProperties;
}

exception TimelineRuleConfigException {
    1: required string message;
    2: required string details;
}

/** Rule definition related structs - end */ 

/** Lifecycle definition related structs - begin */

enum LifecycleStatus {
  ACTIVE
  INACTIVE
  PAUSED
}

enum LifecycleProperty {
  /* Minimum time duration between 2 successive user communication */
  MINIMUM_GAP_SECONDS
  /* Segment which determines whether users should get reinitiated in the lifecycle if its updated */
  CLUSTER
  /* Segments which determines whether users should get reinitiated in the lifecycle if its updated */
  CLUSTERS
  /* Multiplicative factor with which to multiply the timeline gaps to compress the time duration */
  TIME_COMPRESSION_FACTOR
  /* Determines if the user should be reinitiated in the lifecycle even when he has reached the end of the lifecycle. */
  /* The user will be reinitiated when he makes a new bill given that the EVENT_BILL_GENERATED event is configured*/
  USER_INIT_ON_FIRST_BILL
  /*Is Test and Control enabled*/
  TEST_CONTROL
  /*group id version info*/
  GROUP_VERSION
}

/**
 * The reference for the starting point of the user's timeline 
 *
 * FIRST_BILL:  user's timeline should start from his first bill date
 * LAST_BILL: user's timeline should start from his last bill date
 * REGISTERED: user's timeline should start from his registration date
 * NOW: user's timeline should start from the date of start of the lifecycle campaign
 */
enum InitStartTime {
  FIRST_BILL
  LAST_BILL
  REGISTERED
  NOW
}

/** 
 * Types of external events that can be configured to be handled by lifecycle 
 * 
 * EVENT_BILL_GENERATED: A new bill generated for the user
 */
enum EventConfigType {
  EVENT_BILL_GENERATED
  VOUCHER_REDEMPTION
  EMAIL_OPEN
  EMAIL_CLICK
}

enum EventCategoryType {
  USER
}

/**
 * Scope in which the configured event should be applied
 *
 * TIMELINE: apply event only if user in this timeline
 * PHASE: apply event only if user in this phase
 * MILESTONE: apply event only if user in this milestone
 */
enum EventScope {
  TIMELINE
  PHASE
  MILESTONE
}

/** 
 * States of the events
 *
 */
enum EventGroup {
  ACTIVE
  PASSIVE
}

/**
 * Types of filter supported for defining offer applicability
 *
 * CITY: offer is valid only if user registered city in these cities
 * ZONE: offer is valid only if user registered  zone in these zones
 * STORE: offer is valid only if user registered store in these stores
 */
enum CommunicationFilterType {
  CITY
  ZONE
  STORE
}

/**
 * Offer sending strategy
 *
 * SEND_FIRST: Send the first communication which matches the filter criteria
 * SEND_ALL: Send all the communications which match the filter criteria
 */
enum CommunicationSendingPreference {
  SEND_FIRST
  SEND_ALL
}

enum SkipLevelType {
  CITY
  ZONE
  STORE
  TIMELINE
  MILESTONE
  TEST_CONTROL
  NOT_INTERESTED
}

enum ExecutionStatus {
  EXECUTING
  EXECUTED
  PARTIALLY_EXECUTED
  TO_BE_EXECUTED
  SCHEDULED
  CANCELLED
  SKIPPED
  EXPIRED
  ERROR
}

enum MilestoneExecutionSource {
  TIMELINE
  EVENT
}

enum MessageType {
  EMAIL
  SMS
}

enum TimeUnit {
  SECONDS
  MINUTES
  HOURS
  DAYS
  WEEKS
  WEEKENDS
  MONTHS
  YEARS
  LATENCY
  SIX_MONTH_LATENCY
}

struct TimeDuration {
  1:required i32 length
  2:required TimeUnit timeUnit
}

struct Milestone {
  1:optional i32 id
  2:required OrgId orgId
  3:required OrgConfigId orgConfigId
  4:required string name
  5:required string userDefinedName
  6:optional string description
  7:required i32 idx
  8:optional RulesetInfo rulesetInfo
}

struct Phase {
  1:optional i32 id
  2:required OrgId orgId
  3:required OrgConfigId orgConfigId
  4:required string name
  5:required string userDefinedName
  6:optional string description
  7:required i32 idx
  8:optional RulesetInfo phaseChangerRuleset
  9:optional RulesetInfo stateAnalyzerRuleset
  10:optional list<Milestone> milestones
}

struct Timeline {
  1:optional i32 id
  2:required OrgId orgId
  3:required OrgConfigId orgConfigId
  4:required string name
  5:required string userDefinedName
  6:optional string description
  7:optional string stateName
  8:required TimeDuration timelineLength
  9:optional InitStartTime initStartTime = InitStartTime.LAST_BILL
  10:optional list<Phase> phases
  11:optional bool isLegacy
}

struct Lifecycle {
  1:optional OrgConfigId id
  2:required i32 campaignId
  3:required string name
  4:required string userDefinedName
  5:required OrgId orgId
  6:required i32 startMinuteOfDay
  7:required i32 endMinuteOfDay
  8:required LifecycleStatus status
  9:optional string stateTimelineMapping
  10:optional RulesetInfo userInitiationRuleset
  11:optional map<LifecycleProperty,string> properties
  12:optional list<Timeline> timelines
}

struct LifecycleConfiguration {
  1:required map<SkipLevelType, list<i32>> msgSendingSkipIdsMap
}

struct EventCategory {
  1: optional i32 id = 1
  2: required EventCategoryType type
}

struct EventConfig {
  1:optional i32 id
  2:required OrgId orgID
  3:required OrgConfigId orgConfigId
  4:required EventConfigType name
  5:optional string description
  6:required EventGroup eventStatus
  7:required EventScope eventScope
  8:required EventCategory eventCategory
}

struct EventMilestoneConfig {
  1:optional i32 id
  2:required EventConfig eventConfig
  3:required i32 eventScopeId
  4:required Milestone milestone
}

struct CommunicationFilter {
  1:optional i32 id
  2:required string name
  3:required CommunicationFilterType filterType
  4:required list<i32> filterValues
}

struct SmsCommunication {
  1:optional i32 id
  2:required MessageType type
  3:required string smsTemplate
  4:optional CommunicationFilter communicationFilter
}

struct EmailCommunication {
  1:optional i32 id
  2:required MessageType type
  3:required string subjectTemplate
  4:required string bodyTemplate
  5:optional CommunicationFilter communicationFilter
}

/** A type of communication. It can be one of these possible types */
union Communication {
  1:optional SmsCommunication smsCommunication
  2:optional EmailCommunication emailCommunication
}

struct PrioritizedCommunication {
  1:required Communication communication
  2:required i32 priority 
}

/** Strategy for prioritizing the communications and specifying the sending preference*/
struct CommunicationStrategy {
  1:optional i32 id
  2:required string name
  3:optional CommunicationSendingPreference preference = CommunicationSendingPreference.SEND_FIRST
  4:optional list<PrioritizedCommunication> communications
}

/** Define other activities here too */

struct SmsActivity {
  1:required MessageType type
  2:required string smsTemplate
  3:optional string campaign
  4:optional string validity
  5:optional string replacedSmsTemplate
}

struct EmailActivity {
  1:required MessageType type
  2:required string subjectTemplate
  3:required string bodyTemplate
  4:optional string campaignpe
  5:optional string validity
  6:optional string replacedSubjectTemplate
  7:optional string replacedBodyTemplate
}

struct UserActivity {
  1:required LifecycleActionType actionType 
  2:required map<string,string> actionProps
}

struct UserMilestoneContext {
  1:required OrgId orgId
  2:required OrgConfigId orgConfigId
  3:required UserId userId
  4:required Milestone milestone
  7:required ExecutionStatus executionStatus
  8:required MilestoneExecutionSource executionSource
  9:optional Timestamp executionTime
}

struct UserActivityContext {
  1:required OrgId orgId
  2:required OrgConfigId orgConfigId
  3:required UserId userId
  4:required UserMilestoneContext milestoneContext
  5:required UserActivity activity
  6:required ExecutionStatus executionStatus
  7:required Timestamp executionTime
  8:optional string errorString 
}

struct UserTimelineHistory {
  1:required OrgId orgId
  2:required OrgConfigId orgConfigId
  3:required UserId userId
  4:required Timeline timeline
  5:required list<UserActivityContext> contexts
  6:required Timestamp initializationTime
}

struct UserState {
  1:required OrgId orgId
  2:required OrgConfigId orgConfigId
  3:required UserId userId
  /** the mapping from timeline name to user's current state for that timeline */
  4:required map<Timeline,UserMilestoneContext> timelineContextMapping
}

struct UserLifecycleState {
  1:required OrgId orgId
  2:required OrgConfigId orgConfigId
  3:required UserId userId
  /** the mapping from timeline name to user's history for that timeline */
  4:required map<Timeline,UserTimelineHistory> timelineContextsMapping
}

struct TimelineState {
  1:required Timeline timeline
  /** the list of user's current state in the timeline */
  2:required list<UserMilestoneContext> contexts
}

struct Statistics {
  1:required ExecutionStatus status
  2:required Timestamp timestamp
  3:required i32 userCount
}

struct MessageStatistics {
  1:optional map<MessageType, i32> messagesSent
  2:optional map<MessageType, i32> messagesDelivered
  3:optional map<MessageType, i32> messagesFailed 
}

struct MilestoneStatistics {
  1:required Milestone milestone
  2:optional MessageStatistics messageStats
  3:optional Statistics executionStats
}

struct PhaseStatistics {
  1:required Phase phase
  2:optional MessageStatistics messageStats
  3:optional list<MilestoneStatistics> milestoneStats
}

struct TimelineStatistics {
  1:required Timeline timeline
  2:optional MessageStatistics messageStats
  3:optional list<PhaseStatistics> phaseStatistics
}

struct FutureSchedule {
  /** the day for which the schedule is with respect to the currentTimestamp */
  1: required i32 peekAheadDay
  /** the total user actions scheduled on the day */
  2: required i32 userActionCount
  /** execution status wise schedule for all actions for the day */
  3: required map<ExecutionStatus, i32> statusCount
  /** the timestamp of the schedule report */
  4: required Timestamp currentTimestamp
  /** user action wise action count configured for the day */
  5: optional map<LifecycleActionType, i32> actionCountMap
}

struct FutureSchedules {
  1: required list<FutureSchedule> futureSchedules;
}

struct UserExecutionStats {
  1:required i32 usersQualified
  2:required i32 usersDroppedOff
  3:required i32 usersMovedAhead
  4:required MessageStatistics messageStats
}

struct MilestoneStats {
  1:required Milestone milestone
  2:required UserExecutionStats messageStats
  3:optional map<ExecutionStatus, i32> statusCount
}

struct TimelineStats {
  1:required Timeline timeline
  2:required UserExecutionStats messageStats
  3:required list<MilestoneStats> milestoneStatistics
  4:optional map<ExecutionStatus, i32> statusCount
}

struct LifecycleStats {
  1:required list<TimelineStats> timelineStatistics
}

struct BoolRes {
  1:optional bool success
  2:optional TemporalEngineException ex
}

service TemporalEngineService {

  bool isAlive()

  void processEvent(1:Event event) throws (1:TemporalEngineException ex)

  void startTimelines(1:i32 orgId, 2:i32 orgConfigId) throws (1:TemporalEngineException ex)

  void stopTimelines(1:i32 orgId, 2:i32 orgConfigId) throws (1:TemporalEngineException ex)

  bool areTimelinesRunning(1:i32 orgId, 2:i32 orgConfigId) throws (1:TemporalEngineException ex)

  bool initializeTimelines(1:i32 orgId, 2:i32 orgConfigId) throws (1:TemporalEngineException ex)

  string getInitializeTimelineStatus(1:i32 orgId, 2:i32 orgConfigId) throws (1:TemporalEngineException ex)

  void cancelTimelinesInitialization(1:i32 orgId, 2:i32 orgConfigId) throws (1:TemporalEngineException ex)

  bool reinitializeTimeline(1:i32 orgId, 2:i32 orgConfigId, 3:string timelineName) throws (1:TemporalEngineException ex)

  string getReinitializeTimelineStatus(1:i32 orgId, 2:i32 orgConfigId, 3:string timelineName) throws (1:TemporalEngineException ex)

  bool notifyClustersUploaded(1:i32 orgId, 2:string segmentName) throws (1:TemporalEngineException ex)

  BoolRes notifyGroupReloaded(1:i32 orgId, 2:i32 groupId, 3:string entityId, 4:string paramJson, 5:string requestId) throws (1:TemporalEngineException ex)

  string getNotifyClustersUploadedStatus(1:i32 orgId, 2:i32 orgConfigId) throws (1:TemporalEngineException ex)

  void registerOrgConfig(1:i32 orgId, 2:i32 orgConfigId) throws (1:TemporalEngineException ex)

  bool deactivateCampaign(1:i32 orgId, 2:i32 orgConfigId) throws (1:TemporalEngineException ex)

  bool activateCampaign(1:i32 orgId, 2:i32 orgConfigId) throws (1:TemporalEngineException ex)

  bool pauseCampaign(1:i32 orgId, 2:i32 orgConfigId) throws (1:TemporalEngineException ex)

  bool restartCampaign(1:i32 orgId, 2:i32 orgConfigId) throws (1:TemporalEngineException ex)
}

service LifecycleConfigurationService {

  list<Lifecycle> getOrgLifecycles(1: OrgId orgId, 2: SessionId sessionId) throws (1:TemporalEngineException ex);

  Lifecycle saveLifecycle(1: Lifecycle lifecycle, 2: SessionId sessionId) throws (1:TemporalEngineException ex);

  Timeline saveTimeline(1: Timeline timeline, 2: RuleInfo userInitRule, 3: SessionId sessionId) throws (1:TemporalEngineException ex);

  list<ActionMeta> getLifecycleActions(1:OrgId orgId, 2:OrgConfigId orgConfigId, 3: SessionId sessionId) throws (1:TemporalEngineException ex);

  ActionMeta getLifecycleActionByName(1:OrgId orgId, 2:OrgConfigId orgConfigId, 3: LifecycleActionType actionName, 4: SessionId sessionId) throws (1:TemporalEngineException ex);

  list<string> getSupportedTags(1:OrgId orgId, 2:OrgConfigId orgConfigId, 3:SessionId sessionId) throws (1:TemporalEngineException ex);

  EventMilestoneConfig saveEventConfiguration(1: EventMilestoneConfig eventMilestoneConfig, 
    2: SessionId sessionId) throws (1:TemporalEngineException ex);

  list<EventMilestoneConfig> getEventConfigurations(1:OrgId orgId, 2:OrgConfigId orgConfigId, 3: EventScope eventScope, 
    4: i32 scopeId, 5: SessionId sessionId) throws (1:TemporalEngineException ex);

  bool isLifecycleNameAvailable(1: OrgId orgId, 2: string lifecycleName, 3: SessionId sessionId) throws (1:TemporalEngineException ex);

  Lifecycle getLifecycleById(1: OrgId orgId, 2: OrgConfigId orgConfigId, 3: SessionId sessionId) throws (1:TemporalEngineException ex);

  Lifecycle getLifecycleByName(1: OrgId orgId, 2: string lifecycleName, 3: SessionId sessionId) throws (1:TemporalEngineException ex);

  Lifecycle getLifecycleByCampaignId(1: OrgId orgId, 2: i32 campaignId, 3: SessionId sessionId) throws (1:TemporalEngineException ex);

  list<Timeline> getTimelinesForLifecycle(1: OrgId orgId, 2: OrgConfigId orgConfigId, 3: SessionId sessionId) throws (1:TemporalEngineException ex);

  Timeline getTimelineById(1:OrgId orgId, 2:OrgConfigId orgConfigId, 3: i32 timelineId, 4:SessionId sessionId) throws (1:TemporalEngineException ex);

  list<Phase> getPhasesForTimeline(1: Timeline timeline, 2: SessionId sessionId) throws (1:TemporalEngineException ex);

  list<Milestone> getMilestonesForPhase(1: Phase phase, 2: SessionId sessionId) throws (1:TemporalEngineException ex);

}

service PackageManagerService {
    
    string getRuleExpressionLibrary (1:OrgId orgId, 2: MilestoneExecutionSource source, 3: SessionId sessionId) throws (1:TemporalEngineException ex);

    list <string> resolveDependentEnum(1:OrgId orgId, 2:string type, 3: SessionId sessionId) throws (1:TemporalEngineException ex);

}

service LifecycleReportingService {

    /** Returns the schedule for the next peek_ahead_period days from today.
    *
    *   @param orgId              the org id <br>
    *   @param org_config_id      the campaign id <br>
    *   @param peek_ahead_period  Determines the look ahead period in days from the current timestamp 
    *                             to fetch the schedule for the campaign
    *   @param SessionId          the session id 
    */
  map<i32, FutureSchedules> getCampaignActivitySchedule(1: OrgId orgId, 2: OrgConfigId orgConfigId, 
    3: i32 peekAheadPeriod, 4: SessionId sessionId) throws (1: TemporalEngineException ex);

    /** Returns the schedule for the next peek_ahead_period days from today.
    *
    *   @param orgId              the org id <br>
    *   @param org_config_id      the campaign id <br>
    *   @param timeline           the timeline for which schedule is required
    *   @param peek_ahead_period  Determines the look ahead period in days from from the current timestamp 
    *                             to fetch the schedule for the campaign
    *   @param SessionId          the session id 
    */
  FutureSchedules getTimelineActivitySchedule(1: OrgId orgId, 2: OrgConfigId orgConfigId, 3: Timeline timeline, 
    4: i32 peekAheadPeriod, 5: SessionId sessionId) throws (1: TemporalEngineException ex);

    /** Returns a map of campaignId to total users initialized in that campaign
    *
    *   @param orgId              the org id <br>
    *   @param SessionId          the session id
    */

  map<i32,i32> getUserInitializationSummary(1: OrgId orgId, 2: SessionId sessionId) throws (1: TemporalEngineException ex);

    /** Returns a map of campaignId to total events processed from the peekWindow days
    *
    *   @param orgId              the org id <br>
    *   @param peekWind		  how many days behind u want the summary
    *   @param SessionId          the session id
    */

  map<i32,i32> getEventsProcessedSummary(1: OrgId orgId, 2: i32 peekBehindWindow, 3: SessionId sessionId) throws (1: TemporalEngineException ex);
  
    /** Returns the timeline dashboard details for a specified day in last one month
    *
    *   @param orgId              	the org id <br>
    *   @param org_config_id      	the campaign id <br>
    *   @param look_back_date		the date for which we need the capaign execution details
    *   @param SessionId          	the session id 
    */
  LifecycleStats getCampaignExecutionDetails(1: SessionId sessionId, 2: Timestamp lookBackDate) throws (1: TemporalEngineException ex);

  map<i32,i32> getLookAheadMilestoneContexts(1: SessionId sessionId, 2: Timestamp lookAheadTillDate) throws (1: TemporalEngineException ex);

}