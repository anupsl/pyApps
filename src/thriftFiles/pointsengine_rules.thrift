#!thrift -java -php -phps

/**
 * This file contains all the service and data object definitions which will be used to generate thrift classes.
*/

namespace java com.capillary.shopbook.pointsengine.endpoint.api.external
namespace php pointsengine_rules

exception PointsEngineRuleServiceException {
    1: required string errorMessage;
}

struct StrategyInfo {
    1: required i32 id;
    2: required i32 programId;
    3: required string name;
    4: required string description;
    5: required i32 strategyTypeId;
    6: required string propertyValues;
    7: required string owner;
 }
/* If any changes in PromotionInfo, please keep campaigns team in loop */
struct PromotionInfo {
    1: required i32 id;
    2: required i32 programId;
    3: required string name;
    4: required string description;
    5: required string eventName;
    6: required bool isActive;
    7: required bool isExclusive;
    8: required string type;
    9: required string promotionEvaluationType;
    10: required i64 startDate;
    11: required i64 endDate;
    12: required string startRuleIdentifier;
    13: optional i32 sourceId;
    14: optional string promotionSourceType;
    15: optional i32 eventsPerMemberLimit;
    16: optional i32 pointsPerMemberLimit;
    17: optional i32 pointsPerPromotionLimit;
}

struct SlabInfo {

    1: required i32 id;
    2: required i32 programId;
    3: required i32 serialNumber;
    4: required string name;
    5: required string description;
}

struct BoolRes {
    1: optional bool success;
    2: optional PointsEngineRuleServiceException ex;
}

struct ProgramInfo {

    1: required i32 id;
    2: required string name;
    3: required string description;
    4: required bool isActive;
    5: required i64 lastActivated;
    6: required i32 slabUpgradePointCategoryId;
    7: required i32 slabUpgradeStategyId;
    8: required string slabUpgradeMode;
    9: required string slabUpgradeRuleIdentifier;
    10: required i32 redeemablePointCategoryId;
    11: required double pointsCurrencyRatio;
    12: required i32 roundDecimals;
    13: optional string reminderBeforeDaysCsv;
    14: optional i32 reminderMinExpirypoints;
    15: optional string reminderSmsTemplate;
    16: optional string reminderMailSubject;
    17: optional string reminderMailBody;
    18: required bool isDefault;

}

struct TenderCombinationAttribute {
    1: required i32 id;
    2: required i32 orgId;
    3: required i32 tenderCombinationId;
    4: required i32 tenderAttributeId;
    5: required i32 tenderAttributeValueId;
}

struct TenderCombination {
    1: required i32 id;
    2: required i32 orgId;
    3: required i32 programId;
    4: required i32 tenderId;
    5: required string label;
    6: required i32 priority;
    7: required i32 modifiedBy;
    8: optional i64 modifiedOn;
    9: optional string description = "";
    10: optional bool isValid = false;
    11: optional list <TenderCombinationAttribute> attributeInfo;
}

struct TrackerConditionExpression{
    1: required string aggrFunc;
    2: required bool uniqueValue;
    3: required string operator;
    4: required i32 threasholdValue1;
    5: optional i32 threasholdValue2 = 0;
    6: optional i32 minimumThreasholdValue = 0;
}

enum TrackingPeriodType {
DAYS
MONTHS
}

struct TrackerCondition{
    1: required i32 id;
    2: required i32 orgId;
    3: required i32 programId;
    4: required i32 strategyId;
    5: required string name;
    6: required i32 rank;
    7: required i32 period;
    8: required i64 maxTimesSuccessSignals;
    9: required TrackerConditionExpression expression;
    10: required i32 modifiedBy;
    11: required i64 modifiedOn;
    12: required i32 rulesetId;
    13: required i32 pointsCategoryId;
    14: optional bool isActive = false;
    15: optional TrackingPeriodType trackingPeriodType;
}

struct PointsCategory{
    1: required i32 id;
    2: required i32 orgId;
    3: required i32 programId;
    4: required string name;
    5: required string description;
    6: required i32 modifiedBy;
    7: required i64 modifiedOn;
}

struct ProgramFilter{
	1: required i32 orgId;
	2: required i32 tillId;
}

service PointsEngineRuleService {

	/*
	 * Get the information of Program based on tillId
	 */
	 ProgramInfo getProgramByTill(1:ProgramFilter programFilter, 2:string serverReqID) throws (1: PointsEngineRuleServiceException ex);

      /*
       * creates / update non redeemable points category
       */
      PointsCategory createOrUpdatePointsCategory(1:PointsCategory pointsCategory, 2:string serverReqId) throws (1: PointsEngineRuleServiceException ex);

      /*
       * retrives points category for given id
       */
      PointsCategory getPointsCategory(1:i32 orgId, 2:i32 programId, 3: i32 categoryId, 4:string serverReqId ) throws (1: PointsEngineRuleServiceException ex);

      /*
       * Save all given Tracker Condition
       */
      TrackerCondition createOrUpdateTrackerCondition(1:TrackerCondition trackerCondition, 2:string serverReqId) throws ( 1: PointsEngineRuleServiceException ex);

      /*
       * get all tracker condition
       */
      list<TrackerCondition> getTrackerConditionForTrackerStrategy(1:i32 orgId, 2:i32 programId, 3:i32 strategyId, 4:string serverReqId) throws (1: PointsEngineRuleServiceException ex);

      /*
       * get all slabs info based on program id
       */
      list <SlabInfo> getAllSlabs(1:i32 programId, 2:i32 orgId, 3:string serverReqId) throws ( 1: PointsEngineRuleServiceException ex);

      /*
       * get all strategies info based on program id
       */
      list <StrategyInfo> getAllConfiguredStrategies(1:i32 programId, 2:i32 orgId, 3:string serverReqId)  throws (1: PointsEngineRuleServiceException ex);

      /*
       * get all strategies info based on program id and strategyTypeId
       */
      list <StrategyInfo> getAllStrategiesByStrategyTypeId(1:i32 programId, 2:i32 orgId, 3:i32 strategyTypeId, 4:string serverReqId)  throws (1: PointsEngineRuleServiceException ex);


      /*
       * get Strategy info based on strategy id
       */
      StrategyInfo getStrategy(1:i32 strategyId, 2:i32 programId, 3:i32 orgId, 4:string serverReqId)  throws (1: PointsEngineRuleServiceException ex);

      /*
       * create/update strategy
       * return Strategy info created/updated
       */
      StrategyInfo createOrUpdateStrategy(1:StrategyInfo strategyInfo, 2:i32 programId, 3:i32 orgId, 4:i32 lastModifiedBy, 5:i64 lastModifiedOn, 6:string serverReqId)  throws (1: PointsEngineRuleServiceException ex);

      /*
       * creation of slab along with updation strategies
       * return SlabInfo info created
       */
      SlabInfo createSlabAndUpdateStrategies(1:i32 programId, 2:i32 orgId, 3:SlabInfo slabInfo, 4:list<StrategyInfo> strategyInfos, 5:i32 lastModifiedBy, 6:i64 lastModifiedOn, 7:string serverReqId)  throws (1: PointsEngineRuleServiceException ex);

      /*
       * get all promotions info based on program id
       */
	list <PromotionInfo> getPromotionsByProgramId(1:i32 programId, 2:i32 orgId, 3:string serverReqId)  throws (1: PointsEngineRuleServiceException ex);

	/*
       * get all promotions info based on ruleset name
       */
	list <PromotionInfo> getPromotionsByRulesetName(1:i32 programId, 2:i32 orgId, 3:string rulesetName, 4:string serverReqId)  throws (1: PointsEngineRuleServiceException ex);

	/*
       * get all promotions info based on event type id
       */
	list <PromotionInfo> getPromotionsByProgramAndEventType(1:i32 programId, 2:i32 orgId, 3:string eventName, 4:string serverReqId)  throws (1: PointsEngineRuleServiceException ex);

      /*
       * get Promotion info based on strategy id
       */
      PromotionInfo getPromotion(1:i32 promotionId, 2:i32 programId, 3:i32 orgId, 4:string serverReqId)  throws (1: PointsEngineRuleServiceException ex);

      /*
       * create/update promotion
       * return Promotion info created/updated
       */
      PromotionInfo createOrUpdatePromotion(1:PromotionInfo promotionInfo, 2:i32 programId, 3:i32 orgId, 4:i32 lastModifiedBy, 5:i64 lastModifiedOn, 6:string serverReqId)  throws (1: PointsEngineRuleServiceException ex);


      /*
       * get All events
       * return map of < eventId, eventName >
       */
      map <i32, string> getAllEvents( 1:string serverReqId)  throws (1: PointsEngineRuleServiceException ex);

      /*
       * get All Strategy Types
       * return map of < strategyTypeId, strategyTypeName >
       */
      map <i32, string> getStrategyTypes( 1:string serverReqId) throws (1: PointsEngineRuleServiceException ex);

      /*
       * get programId based on orgId
       */
	i32 getProgramId(1:i32 orgId, 2:string serverReqId)  throws (1: PointsEngineRuleServiceException ex);

     /**
      *  update ProgramInfo
      */
     ProgramInfo updateProgram( 1:ProgramInfo program, 2:i32 orgId, 3:i32 lastModifiedBy, 4:i64 lastModifiedOn, 5:string serverReqId)  throws (1: PointsEngineRuleServiceException ex);

	/**
	 * Create if slab not exist, otherwise update
	 */
	SlabInfo createOrUpdateSlab(1:SlabInfo slabInfo, 2:i32 orgId, 3:i32 lastModifiedBy, 4:i64 lastModifiedOn, 5:string serverReqId) throws ( 1: PointsEngineRuleServiceException ex);

	/**
	 * Get the active programInfo
	 */
	ProgramInfo getProgram(1:i32 programId, 2:i32 orgId, 3:string serverReqId ) throws ( 1: PointsEngineRuleServiceException ex);

	/**
	 * Get the all programInfo including inactive programs
	 */
	list<ProgramInfo> getAllPrograms(1:i32 orgId, 2:string serverReqId ) throws ( 1: PointsEngineRuleServiceException ex);

	/**
	 * Rollout new UI for an org
	 */
	bool rolloutNewUI(1:i32 orgId, 2:string serverReqId)  throws (1: PointsEngineRuleServiceException ex);

        //Tender combinations
        TenderCombination getTenderCombination(1:i32 orgID, 2:i32 tenderCombinationId, 3:string serverReqId) throws (1: PointsEngineRuleServiceException ex);

	list<TenderCombination> getAllTenderCombinations(1:i32 orgID, 2:i32 programId,3:string serverReqId) throws (1: PointsEngineRuleServiceException ex);

        TenderCombination createTenderCombination(1:i32 orgID, 2:TenderCombination tenderCombination, 3:string serverReqId) throws (1: PointsEngineRuleServiceException ex);

        TenderCombination editTenderCombination(1:i32 orgID, 2:TenderCombination tenderCombination, 3:string serverReqId) throws (1: PointsEngineRuleServiceException ex);

}

