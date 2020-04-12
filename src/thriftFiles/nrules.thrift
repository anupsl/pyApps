#!thrift -java -php -phps

/**
 * This file contains all the service and data object definitions which will be used to generate thrift classes.
*/

namespace java com.capillary.shopbook.nrules.thrift
namespace php ruleservice

struct DataType {
    1: required string typeName;
    //A comma separated list of allowed values in the enum
    2: optional map <string, string> allowedValues;
    3: optional bool isMultiSelect;
}

struct FilterType {
    1: required i32 id;
    2: required string typeName;
    3: required string description;
}

struct SimpleProperty {
	1: required string name;
	2: required DataType dataType;
	3: required bool isMandatory;
	4: optional string defaultValue;
}

struct ComplexProperty {
	1: required string name;
	2: required list <SimpleProperty> simpleProperties;
}

struct FilterTemplateInfo {
    1: required FilterType type;
    2: required list <SimpleProperty> simpleProperties;
    3: optional list <ComplexProperty> complexPropertiesInfo;
}

struct FilterInfo {
    	1: required i32 id;
	2: required i32 orgID;
    	3: required i32 ruleID;
	4: required string name;
	5: required string className;
	6: required bool isInclude;
    	7: required map <string, list<string>> propertyToValues;
}

struct OrgConfigFilterInfo {
    	1: required i32 id;
	2: required i32 orgID;
	3: optional i32 contextId;
	4: optional string contextType;
	5: required string name;
	6: required string className;
	7: required bool isInclude;
    	8: required map <string, list<string>> propertyToValues;
}

struct ActionTemplateInfo {
    1: required string actionName;
    2: required string actionClass;
    3: required list <SimpleProperty> simpleProperties;
    4: optional string description;
    5: optional list <ComplexProperty> complexProperties;
}

struct ActionInfo {
    1: required i32 id;
    2: required string actionName;
    3: required string actionClass;
    4: required map <string, string> mandatoryPropertiesValues;
    5: required map <string, map <string, string>> mandatoryComplexPropertiesValues;
    6: optional string description;
}

struct RuleInfo {
    1: required i32 id;
    2: required string exp;
    3: required string expJSON;
    4: required string jsonType;
    5: required bool isActive;
    6: required i32 priority;
    7: required i64 startDate;
    8: required i64 endDate;
    9: required i64 createdOn;
    10: required map <string,list<ActionInfo>> caseToActions;    
    11: required string ruleScope;
    12: required i32 createdBy;
    13: required i32 modifiedBy;
    14: optional i64 modifiedOn;
    15: optional string name = "";
    16: optional string description = "";
    17: optional DataType expDataType;    
    18: optional list <FilterInfo> filterInfo;
    19: optional i32 ruleSetId;
}

struct RulesetInfo {
    1: required i32 id;    
    2: required string orgName;
    4: required i32 contextID;
    3: required i32 orgID;
    5: required string contextType;
    6: required list <RuleInfo> rules;
    7: required string ruleScope;
    8: required i64 startDate;
    9: required i64 endDate;
    10: required i64 createdOn
    11: required i32 createdBy;
    12: required i32 modifiedBy;
    13: optional i64 modifiedOn;
    14: optional string name = "";
    15: optional string packageName = "";
    16: optional string description = "";
    17: optional bool isPrivate = false;    
    18: optional list <FilterInfo> filterInfo;
    19: optional string eventType;
}

exception RuleConfigException {
    1: required string message;
    2: required string details;
}

struct BoolRes {
    1: optional bool success;
    2: optional RuleConfigException ex;
}

struct GetOrgConfigFilterReqest{
	1:required i32 orgId;
	2:required list<i32> contextIds;
}


/**
* The rule configuration service which allows creating/editing/viewing rulesets API.
*/
service RuleConfigService {

     /**
     * @param organizationID The org id
     * @param serverReqId server request id
     * @return True, iff the organization was successfiully enabled.
     */
      BoolRes reconfigureOrganization (1: i32 orgID, 2: i32 userID, 3: string endpointName, 4: i32 contextId, 5: string serverReqId) throws (1 :RuleConfigException ex);
      
     /**
      * @return This method returns the list of available filter types in the system. The list of filter types does not
      * depend upon the organization and is fixed.
      */
      list <FilterType> getAvailableFilterTypes (1: string endpointName, 2: string serverReqId);

      FilterTemplateInfo getFilterTemplate (1:i32 orgID, 2:FilterType filterType, 3: string endpointName, 4:string serverReqId);

      DataType validateExpression (1:i32 orgID, 2:string ruleExpression, 3:string ruleExpJSON, 4: string endpointName, 5:string serverReqId);

      list <ActionTemplateInfo> getConfigurableActions (1:i32 orgID, 2: string endpointName, 3:string serverReqId);

      list <RulesetInfo> getConfiguredRulesetsByContextId (1:i32 orgID, 2:bool isPrivate, 3: string endpointName, 4:i32 contextId, 5:string serverReqId);

      list <RulesetInfo> getConfiguredRulesets (1:i32 orgID, 2:bool isPrivate, 3: string endpointName,4: i32 contextId, 5:string serverReqId);

      list <RulesetInfo> getConfiguredRulesetsByEventType(1:i32 orgID, 2:string eventType, 3: string endpointName,4:i32 contextId, 5:string serverReqId);

      RulesetInfo searchRulesetById (1:i32 orgID, 2:i32 rulesetID, 3: string endpointName, 4:string serverReqId) throws (1:RuleConfigException ex);
      list <RulesetInfo> searchRulesetsByNamePattern (1:i32 orgID, 2:string rulesetNamePattern, 3: string endpointName, 4:string serverReqId) throws (1:RuleConfigException ex);

      list <RulesetInfo> searchRulesetsByFacts (1:i32 orgID, 2:string factNameRegex, 3: string endpointName, 4:string serverReqId) throws (1:RuleConfigException ex);

      list <RulesetInfo> searchRulesetsByPackages (1:i32 orgID, 2:string packageNameRegex, 3: string endpointName, 4: string serverReqId) throws (1:RuleConfigException ex);

      RulesetInfo createNewRuleset (1:i32 orgID, 2:string name, 3:RulesetInfo rulesetInfo, 4:string eventName, 
	5: string endpointName, 6:string serverReqId) throws (1:RuleConfigException ex);

      RulesetInfo editRuleset (1:i32 orgID, 2:string name, 3:RulesetInfo rulesetInfo, 4: string endpointName, 5:string serverReqId) throws (1:RuleConfigException ex);

      RulesetInfo addRule (1:i32 orgID, 2:i32 rulesetID, 3:RuleInfo ruleInfo, 4: string endpointName, 5:string serverReqId) throws (1:RuleConfigException ex);

      RulesetInfo changeExpression (1:i32 orgID, 2:string rulesetName, 3:i32 ruleIndex, 4:string ruleExpression, 5:string ruleExpJSON, 
	6: string endpointName, 7: i32 lastModifiedBy, 8:string serverReqId) throws (1:RuleConfigException ex);

      RulesetInfo updateRulesetStatus (1:i32 orgID, 2:i32 rulesetID, 3:bool status, 4: string endpointName, 5: i32 lastModifiedBy, 6:string serverReqId) throws 	(1:RuleConfigException ex);
	  
      bool updateRuleStatus (1:i32 orgID, 2:i32 ruleID, 3:bool status, 4:i32 priority, 5: string endpointName, 6: i32 lastModifiedBy, 7: string serverReqId) throws (1:RuleConfigException ex);      
	  
      list<RulesetInfo> getRulesetExpiryInfo(1:i32 orgID, 2:i64 startDate, 3:i64 endDate, 4: string endpointName, 5:string serverReqId) 
      throws (1:RuleConfigException ex);
	  
      RuleInfo searchRuleById (1:i32 ruleID, 2:i32 orgID, 3: string endpointName, 4:string serverReqId) throws (1:RuleConfigException ex);
	  
      RuleInfo editRule (1:i32 orgID, 2:RuleInfo ruleInfo, 3: string endpointName, 4:string serverReqId) throws (1:RuleConfigException ex);

      bool updateRulesetDates(1:i32 orgID, 2:i32 rulesetID, 3:i64 startDate, 4:i64 endDate, 5: string endpointName, 6: i32 lastModifiedBy, 7:string serverReqId) throws (1:RuleConfigException ex);
	  
      BoolRes updateRulesPriority(1:i32 orgID, 2:map <i32, i32> ruleToPriorityMap, 3: string endpointName, 4:i32 lastModifiedBy, 5:string serverReqID);
      
      BoolRes editOrgConfigFilters(1: i32 orgId, 2: i32 contextId,3: list<OrgConfigFilterInfo> filters, 4: string serverReqId)throws (1:RuleConfigException ex);

      list<OrgConfigFilterInfo> getOrgConfigFilters(1:GetOrgConfigFilterReqest orgConfigFilterRequest, 2: string serverReqID);

      bool retryOrgConfigLoad();	  

      /**
      * Get all fields supported by given generic event
      */
      map<string, string> getAllFieldsOfGenericEvent(1: i64 orgId, 2: string endPointName, 3: string eventName, 4: string requestId);
}