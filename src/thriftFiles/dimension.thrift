namespace java com.capillary.dimension_builder.thrift
#@namespace scala com.capillary.scala.dimension_builder.thrift
namespace php dimension_builder

include "exceptions.thrift"
# Primary Dimension Entities

enum TDimensionType {
    STANDARD_CONSTANT,
    STANDARD,
    USER_DEFINED,
    SRC_DEFINED,
    EXTERNAL_SRC
}

enum TFactType{
    BASE,
    ETL_ONLY,
    SCD_HISTORY,
    EXPORT_ONLY
}

enum TChangeLogSourceType{
    NONE, 
    SOURCE_GENERATED, 
    ETL_GENERATED, 
    VERSIONED_PARTITIONS
}

enum TChangeLogLocationType{
    VERSION,
    COMPACTED
}



enum TScope {
    CAP,
    VERTICAL,
    ORG
}

enum TMetaClient {
    ETL,
    READ_API,
    WRITE_API,
    ETL_VALIDATOR
}

enum TStructureType {
    FLAT,
    HIERARCHICAL,
    SCD,
    BANDING
}

enum TDimColType {
    PK, VALUE, LEVEL, ATTRIBUTE, DATE_ATTRIBUTE, TIME_ATTRIBUTE, ALIAS, NONE,CHANGING_ATTRIBUTE,BANDING_ATTRIBUTE
}

enum TOperation {
    NOP, CONCEALED, SELECT, FILTER, GROUP, BANDING 
}

enum TDimColDataType {
    TEXT, NUMBER, BIGNUMBER, BOOLEAN, DATE, TIME
}

enum TDimOperationType{
    SEARCH,DISTINCT
}

enum TDimOperator{
    EQUALS, GREATER_THAN, LESS_THAN, GREATER_THAN_EQUALS, LESS_THAN_EQUALS
}

enum TTargetUploadStatus {
    UPLOADED, VALIDATED, REJECTED, SUCCESS, INVALID, MERGED, ERROR
}

enum TTimeUnit {YEAR, MONTH, DAY, HOUR, MINUTE, SECOND}

struct TDuration {
	1: required TTimeUnit unit;
	2: required i32 value;
}

struct TScopeInfo {
	1: required i32 id;
	2: required string name;
	3: required TScope scopeType;
}

struct TOrganization {
	1: required i32 orgId;
	2: required string name;
	3: required map<TScope, list<TScopeInfo>> scopes;
}

struct TDimConstraints{
  1: required string dimAttr;
  2: required TDimOperator operator;
  3: required string value;
}

struct TDimParams{
  1: optional string searchText;
  2: optional list<TDimConstraints> dimConstraints;
}

struct TDimAttrValues{
  1: required map<string,list<string>> dimAttrValues;
}

enum TComputationType {
    ETL,
    VIEW
}

struct TDefaultEtlDataStatus{
  1: required i32 statusId;
  2: required string status;
  3: required i32 dimTableId;
}

struct TDimSearchAttrValues{
  1: required string dimAttrValues;
  2: optional map<string,string> projectionsToAttrValues;
}

struct TDataLevelCondition {
        1: required string operandTableName;
	2: required string operandColName;
        3: required string operator;
        4: required string value;
}

enum TCustomColType{
	PK,MEASURE,ATTRIBUTE,DATE_ATTRIBUTE, TIME_ATTRIBUTE}

enum TDimLinkType{DIRECT, BRIDGE}

enum TTableDataDensityType{SPARSE,DENSE}

struct TBridgeTable {
	1: required string factKey;
	2: required string dimKey;
	3: required list<TDataLevelCondition> jonningCondition;
	4: required TTableDataDensityType tableType;
	5: required string tableName;
}

struct TCustomTableColumn {
   1: required i32 id;
   2: required string name;
   3: required string displayName;
   4: required TCustomColType colType;
   5: required i32 ordinalNumber;
   6: required TDimColDataType colDataType;
   7: required list<TOperation> possibleOperations;
   8: required TScope scopeType;
   9: required bool isAttrTablePresent;
   10: optional string attrTableName;
}
struct TCustomTable{
    1: required i32 id;
    2: required string name;
    3: required string displayName;
    4: required list<TCustomTableColumn> columns;
    5: required bool isDataSyncRequired;
}

struct TCustomTableForeignKey{
    1: required string tableName;
    2: required string customTableName;
    3: required string colName;
    4: required string customColName;
    5: required i32 ordinalNumber;
}


struct TLinkedCustomTable{
    1: required TCustomTable customTable;
    2: required string linkedTableName
    3: required list<TCustomTableForeignKey> fks;
    4: required list<TDataLevelCondition> jonningCondition;
}

struct TDimColumn {
    1: required string name;
    2: required TDimColType colType;
    3: required TDimColDataType colDataType;
    4: required i32 scopeId;
    5: optional i32 levelNum;
    6: optional i32 colId;
    7: optional bool hasPossibleValues;
    8: optional string displayName;
    9: optional list<TOperation> possibleOperations;
    10: optional bool isValueContinuous;
    11: optional string functionalDependencyColumn;
    12: optional string storageTableName;
    13: optional TScope valueScope;
    14: optional bool isColValueTablePresent;
    15: optional TChangeLogSourceType changeLogSourceType;
    16: optional string changeLogTableName;
    17: optional bool hasChangeLog;
    18: optional TComputationType computationType;
    19: optional bool isCustomField;
    20: optional string uniqueValueDependentColumn;
}

struct TDimension {
    1: required string name;
    2: required i32 dimId;
    3: required TDimensionType dimType;
    4: required bool isActive;
    5: required bool isLarge;
    6: required string addedOn;
    7: required string updatedOn;
    8: required TScope scope;
    9: required TStructureType structureType;
    10: required i32 dimTableId;
    11: required string dimTableName;
    12: required string dimTablePkColName;
    13: required bool isStorageFragmented;
    14: optional TDimColumn valueCol;
    15: optional map<i32, TDimColumn> levels;
    16: optional list<TDimColumn> attributes;
    17: optional list<TDimColumn> aliases;
    18: optional string factColName;
    19: optional string displayName;
    20: optional map<i32, list<TDimColumn>> levelAttributes;
    21: optional string description;
    22: optional list<TLinkedCustomTable> customTables;
    23: required TDimLinkType dimLinkType;
    24: optional TBridgeTable bridgeTable;
}



struct TDimensionTable {
    1: required string name;
    2: required i32 id;
    3: required TDimensionType dimType;
    4: required bool isActive;
    5: required bool isLarge;
    6: required TScope scope;
    7: required TStructureType structureType;
    8: required list<TDimColumn> columns;
    9: required bool isStorageFragmented;
   10: required bool isElasticSearchedEnabled;
   11: optional TDimColumn pkCol;
   12: optional list<TDimColumn> autoUpdateCols;
}


struct TOrgScope {
    1: required i32 id;
    2: required i32 orgId;
    3: required i32 scopeId;
}

struct TFactDimScope {
    1: required i32 id;
    2: required string name;
    3: required TScope scope;
}

struct TDimPossibleValueTableInfo {
	1: required string attrTableName;
	2: required string dimTableName;
	3: required string columnName;
}
#---------End of Primary Dimension Entities
# Primary Fact Entities

enum TFactColumnType {
    PK,MEASURE,DIMENSION,FACT_REFERENCE,PARTITION_KEY, DUMP_DATA,BANDING_DIM, DIM_PK
}

enum TFactDataType {
    INT, BIGINT, DOUBLE, TEXT
}

enum TSelectSrcTableType {
        FACT, DIMENSION, SUMMARY
}

struct TCondition {
        1: required i32 id;
        2: required TSelectSrcTableType operandTableType;
        3: required string operandTableName;
        4: required string operandTablePkCol;
        5: required string operandCol;
        6: required string factDimName;
        7: required string factColName;
        8: required string operator;
        9: required string value;
}


struct TFactColumn {
    1: required i32 id;
    2: required string name;
    3: required TFactColumnType colType;
    4: required TFactDataType dataType;
    5: required list<string> functionalDependencyKeys;
    6: optional string metaInfo;
    7: optional i32 ordinalNum;
    8: optional list<TDimensionTable> dimensionTable;
}

struct TOverlapOn {
    1: required TFactColumnType type;
    2: required string name;
    3: optional string dimColName;
}

struct TOverlapable {
    1: required string dimensionName;
    2: required list<TOverlapOn> overlapOn;
}

struct TFact {
    1: required string name;
    2: required i32 factId;
    3: required bool isActive;
    4: required string addedOn;
    5: required string updatedOn;
    6: required TScope scope;
    7: required string primaryDateKey;
    8: required list<TFactColumn> pks;
    9: required list<TFactColumn> measures;
    10: required list<TFactColumn> dimensions; // factColumn name is logical name
    11: required list<string> partitionKeys;
    12: optional i32 primaryDateKeyColId;
    13: optional list<TCondition> standardFilters;
    14: optional TFactType factType;
    15: optional list<TOverlapable> overlapableDimensions;
    16: optional list<TLinkedCustomTable> customTables;
}

enum TKpiType {MAP,INC_REDUCE,NON_INC_REDUCE,NON_INC_RANK,SUMMARY}

struct TKpiMeta {
    1: required TFactColumn column;
    2: required i32 tableId;
    3: required TKpiType type;
    4: required string expresion;
    5: required bool isReversible;
    6: required i32 primaryKeyLevel;
    7: required string addedOn;
    8: required string updatedOn;
    9: optional string lastComputedOn;
}

enum TFactMappingType {
	ONE_TO_ONE, ONE_TO_MANY,MANY_TO_ONE,MANY_TO_MANY
}

enum TFactRelationType {
	IS,BELONGS
}

struct TFactForeignKey{
    1: required i32 columnId;
    2: required i32 tableId;
    3: required i32 ordinalPosition;
    4: required i32 refColumnId;
    5: required i32 refTableId;
    6: required TFactMappingType mappingType;
    7: required TFactRelationType relationType;
    8: required bool isActive;
    9: required string addedOn;
}

enum TContextRelationship {
    CONTEXT_LEVEL, LEAF_LEVEL, NOT_APPLICABLE
}

struct TOrgContext {
    1: required string contextKey;
    2: required list<i32> contextValues;
    3: required i32 orgDefaultContextValue;
    4: optional string deriveExpression;
}

struct TApplicableOrgContext {
    1: required TContextRelationship relation;
    2: optional TOrgContext context;
}


struct TFactEtl {
    1: required string name;
    2: required i32 factId;
    3: required bool isActive;
    4: required string addedOn;
    5: required string updatedOn;
    6: required TScope scope;
    7: required string primaryDateKey;
    8: required list<TFactColumn> pks;
    9: required list<TFactColumn> measures;
    10: required list<TFactColumn> dimensions; // fact column name is dim_* i.e physical table column name
    11: required list<string> partitionKeys;
    12: required list<TFactColumn> factReferenceKeys;
    13: required list<TKpiMeta> factKpis;
    14: required list<i32> parentSrcTables;
    15: required list<TFactForeignKey> factForeignKeys;
    16: required list<TFactColumn> dumpDataFields;
    17: required i32 incrementalPeriodInYear;
    18: required list<TFactColumn> typePartitionKeys;
    19: required i32 primaryDateKeyColId;
    20: required string strategyName;
    21: optional string strategyJsonStr;
    22: optional bool isSchemaChanged;
    23: optional TFactType factType;
    24: optional list<TApplicableOrgContext> applicableContexts;
}

struct TAttributionStrategy {
    1: required string strategyName;
    2: required i32 strategyId;
    3: required string strategyJsonStr;
    4: required i32 factTableId;
    5: required list<i32> factColumnId;
    6: optional i32 sourceTableId;
    7: optional list<i32> sourceColumnId;
}

struct TFactDimension {
    1: required TFact fact
    2: required list<TDimension> dimensions
}

struct TPartition {
    1: required i32 runId;
    2: required string runDate;
	3: required string partitionValues;
	4: required string path;
	5: required string lastModified;
}


enum TStorageEntityType {SOURCE, TEMP_TABLE, DIMENSION, FACT, SUMMARY, CUSTOM_FIELDS, SCD_LOCATION, DIM_ATTR }

#   TableNameSpace format: tableName#Orgid.dbName.endPoint
struct TStorageLocation {
	1: required TStorageEntityType tableType;
	2: required i32 fullRunId;
	3: required string fullRunDate;
	4: required string fullRunPath;
	5: required string fullRunModified;
	6: required string tableNameSpace;
	7: required string createTableSchema;
	8: required bool isPartitioned;
	9: optional string partitionKeys;
    10: optional list<TPartition> incrementalPartitions;
}

struct TSchemaStorage {
	1: required string nameSpace;
	2: required string createSchema;
	3: required string properties;
	4: required string addedDate;
	5: optional string modifiedDate;
}

struct TFactDataLocation {
	1: required i32 orgId;
	2: required string tableName;
	3: required string createTableSchema;
	4: required i32 fullRunId;
	5: required string fullRunDate;
	6: required string fullPartionPath;
	7: required string fullPartionModified;
	8: required bool isPartitioned;
	9: optional string partitionKeys;
    	10: optional list<TPartition> incrementalPartitions;
}

struct TSourceDataLocation {
	1: required i32 runId;
	2: required string runDate;
	3: required i32 orgId;
	4: required string endPoint;
	5: required string dbName;
	6: required string tableName;
	7: required string createTableSchema;
	8: required string path;
	9: optional string lastModified;
}

struct TDimensionDataLocation {
	1: required i32 runId;
	2: required string runDate;
	3: required i32 orgId;
	4: required string tableName;
	5: required string createTableSchema;
	6: required string path;
	7: optional string lastModified;
}


struct TChangeLogDataLocation {
    1: required i32 versionId;
    2: required i32 orgId;
    3: required string tableName;
    4: required string createTableSchema;
    5: required string path;
    6: optional string lastModified;
    7: TChangeLogLocationType type
}


struct TDimensionValueTables {
    1: required TDimensionType dimensionType;
    2: required string dbName;
    3: required list<string> tables;
}

#---------End of Primary Fact Entities
# Dimension Mapping Entities
struct TValueMapping {
    1: required string colValue
    2: required string colResult
    3: optional string colOperand
}
struct TColumnMapping {
    1: required string src_column_name
    2: required string dest_column_name
    3: required TDimColType dimColType
    4: required TDimColDataType dataType
    5: optional string nullValue
    6: optional string notNullValue
    7: optional list<TValueMapping> valueMappings
    8: optional bool captureDefaultValue
}

struct TTableMapping {
    1: required string sourceTableName;
    2: required string destTableName;
    3: required string dimensionName;
    4: required TDimensionType dimensionType;
    5: required TStructureType structureType;
    6: required bool isLarge;
    7: required list<string> pkColumns;
    8: required list<TColumnMapping> mappings;
    9: required i32 dimTableId;
    10: required bool isFullRunRequired;
}

enum TTransformationType{
    HIERARCHICAL, NORMAL
}

struct TTransformation {
    1: required i32 id
    2: required string outputTableName
    3: required string jsonStr
    4: required i32 providerId
    5: required i32 orgId
    6: required TTransformationType transformType
    7: required bool isSqlProvided
    8: required bool isFullRunRequired
    9: optional string sql
    10: optional i32 providerTableId
    11: optional bool isVerified
    12: optional bool isExactMatch
}

#---------End of Dimension Mapping Entities

#----Source Meta Structs

enum TMappingTableType {
    SOURCE,TARGET,LOGICAL
}

enum TMappingType {
    ONE_TO_ONE,UNION_MAPPING,DENORM_MAPPING,POLYMORPHIC_MAPPING
}

enum TDialect {MYSQL, SPARK, MONGO}

struct TEndPoint {
    1: required i32 id;
    2: required string dbName;
    3: required string endPointName;
    4: required TDialect dialect;
}

struct TSourceColumn{
    1: required i32 id;
    2: required i32 tableId;
    3: required string name;
    4: required string dataType;
    5: optional string columnTypeMeta;
}

struct TSourceForeignKey{
    1: required i32 id;
    2: required TSourceColumn col;
    3: required TSourceColumn refCol;
}

struct TShardTableSelection {
    1: required string selectColumn;
    2: required string fromDb;
    3: required string fromTable;
    4: required string endPointName;
    5: required bool isTableSharded;
}

struct TSourceTable {
    1: required i32 id;
    2: required string name;
    3: required TEndPoint endPoint;
    4: required list<TSourceColumn> columns;
    5: required map<i32, TSourceColumn> primaryKeys;
    6: required list<TSourceForeignKey> foreignKeys;
    7: required bool isShardedTable;
    8: optional TSourceColumn timestampCol;
    9: optional TShardTableSelection shardTableSelection;
    10: optional TSourceColumn partitionKeyCol;
    11: optional string filterExpression;
    12: optional bool isHiveTableEnabled;

}

struct TIntermediateTableDataLocation {
	1: required i32 runId;
	2: required string runDate;
	3: required i32 orgId;
	4: required string dbName;
	5: required string tableName;
	6: required string createTableSchema;
	7: required string path;
	8: optional string lastModified;
}

#----End of Source Meta Structs


# Fact Mapping Entities
struct TFactColumnMapping{
    1: required string sourceColumnName;
    2: required string targetColumnName;
}

struct TSourceFactMapping{
    1: required i32 factTableId;
    2: required i32 sourceTableId;
    3: required TMappingTableType sourceTableType;
    4: required i32 targetTableId;
    5: required TMappingTableType targetTableType;
    6: required TMappingType mappingType;
    7: required list<TFactColumnMapping> columnMappings;
    8: optional string factDiffColName;
    9: optional string factDiffColValue;
    10: optional bool isDynamicPartition;
    11: optional string sourceFilterExpression;
}

struct TSourceDimLinkingColumnMapping{
    1: required i32 sourceColumnId
    2: required i32 dimensionId
    3: required string sourceColumnName
    4: required bool isLinkingRequired
    5: required string dimensionTableName
    6: required string dimensionEtlTable
    7: required string dimPkColumnName
    8: required string dimValueColumnName
    9: required string factColumnName
    10: required string sourceColDataType
    11: optional list<TValueMapping> valueMappings
}

struct TSourceDimLinkingMapping{
    1: required i32 factTableId
    2: required i32 sourceTableId
    3: required string sourceTableName
    4: required list<TSourceDimLinkingColumnMapping> columnMappings
    5: required string linkedTableName
}
#---------End of Fact Mapping Entities

struct TDimensionTableWithColumn {
    1: required TDimensionTable dimTable;
    2: required list<TDimColumn> columns;
}

struct TDimensionTableInfo {
    1: required TDimensionTable dimensionTable;
    2: optional string pkCol;
    3: optional TDimColumn valueCol;
    4: optional map<i32, TDimColumn> levels;
    5: optional list<TDimColumn> attributes;
    6: optional list<TDimColumn> aliases;
    7: optional map<i32, list<TDimColumn>> levelAttributes;
}

struct TDimValue {
    1: required i32 id;
    2: required string value;
}

struct TProviderDimensionMapping {
    1: required i32 dimId;
    2: required i32 dimensionColumnId;
    3: required string providerColName;
    4: required i32 providerTableId;
    5: required i32 scopeId;
    6: optional string nullValue;
    7: optional string notNullValue;
    8: optional list<TValueMapping> valueMappings;
    9: optional bool captureDefaultValue;
}

struct TConfigKeyValue {
    1: required i32 id;
    2: required string key;
    3: required string value;
    4: required bool isActive;
    5: required string lastUpdatedOn;
}



struct TResponse {
    1: required i32 code;
    2: required string status;
    3: required string msg;
}


enum TCatTableType {
	BASE_FACT, SUMMARY, VIEW
}

struct TScdDetails{
    1: TChangeLogSourceType sourceType,
    2: optional string tableName
}

struct TDimAttrChangeLogTable{
    1: TDimensionTable dimTable
    2: TDimColumn dimColumn
    3: TScdDetails changeLogDetails
}
struct TRelationalDimTable {
	1: required i32 id;
	2: required string name
	3: required string pkColName;
	4: required list<TDimColumn> attributes;
    	5: required bool isStorageFragmented;
	6: required TDimLinkType dimLinkType;
	7: optional TBridgeTable bridgeTable;
}

enum TGroupByColType {
	FACT_PK, DIM_PK, DIM_ATTR
}

struct TGroupBy {
	1: required i32 id;
	2: required TSelectSrcTableType tableType;
	3: required string tableName;
	4: required string column;
	5: required TGroupByColType grpColType; // only for ETL
	6: required string logicalDimName;  // event_user : logical name
	7: optional string factColumnName; // dim_*
	8: optional string dimTablePkCol;
	9: optional string columnDataType;
}

struct TCatCol {
	1: required i32 id;
	2: required string name; // logical_dim name in case of dimension
	3: required string factColName; // dim_*
	4: required TFactDataType dataType;
    	5: required list<string> functionalDependencyKeys;
    	6: required TFactColumnType colType;
	7: optional TSelectSrcTableType selectSrcTableType; // applicable only for summary col select definition
    	8: optional string tableName; //applicable only for summary col select definition
    	9: optional string selectCol; // applicable only for summary col select definition
    	10: optional string udaf;  // applicable only for summary col select definition
    	11: optional list<TCondition> filters;  // applicable only for summary col select definition
    	12: optional TRelationalDimTable dimensionTable;
}

struct TCatalog {
	1: required i32 id;
	2: required TCatTableType type;
	3: required string name;
	4: required i32 tableId;
	5: required string tableName;
	6: required list<TCatCol> pks;
	7: required list<string> partitionKeys;
	8: required list<TCatCol> measures;
	9: required list<TCatCol> dimensions;
	10: required list<TCatCol> subDimensions;
	11: optional string primaryDateKey;
	12: optional list<TGroupBy> groupBy;
	13: optional list<TCondition> whereClauses;
	14: optional list<TCondition> factStandardFilters;
	15: optional bool isStandardFilterApplicable;
	16: optional bool isSchemaChanged;
	17: optional string viewCreateSchema;
}


struct TFactStorageInfo{
	1: required string tableName;
	2: required string createTableSchema;
	3: required string path;
	4: required string partitionKeys;
	5: required list<string> partitionValues;
	6: required TCatTableType tableType;
}


struct TDimAttrValueAvailability{
	1: required string dimName;
	2: required string attrName;
	3: required i32 valueCount;
	4: required bool isHighCardinality;
}


enum TTranposeColumnType{
	 GROUPING, MAP, TRANSPOSE
}

struct TTransposeCondition{
	1: required TSourceColumn lhs;
	2: required string rhs;
	3: required string op;
        4: optional string colDataType;
}

struct TTransposeColumn{
	1: required TSourceColumn transposeColumn;
	2: required TSourceColumn sourceColumn;
	3: required TTranposeColumnType type;
	4: required bool is_new_column;
	5: optional list<TTransposeCondition> conditions; # value to match if its value column
}
struct TTransposeTable{
	1: required TSourceTable transposeTable;
	2: required TSourceTable sourceTable;
	3: optional list<TTransposeColumn> columns;
	4: optional list<TTransposeCondition> whereClauses;
}

struct TDataLocationPath{
	1: required i32 orgId;
	2: required TSelectSrcTableType tableType;
	3: required string tableName;
	4: required list<string> paths;
}

struct TMongoStructInfo {
	1: required string name;
	2: required string dataType;
	3: optional string info;
}

struct TMongoStruct {
	1: required i32 id;
	2: required string name;
	3: required list<TMongoStructInfo> structInfo;
}

struct TMongoCollection {
	1: required i32 id;
	2: required string name;
	3: required string timestampColName;
	4: required TEndPoint endPoint;
	5: required TMongoStruct primaryMongoStruct;
	6: required list<TMongoStruct> dependentMongoStructs;
}

struct TMongoColMapping {
	1: required TSourceColumn derivedSrcCol;
        2: required string mongoExpr;
}

struct TMongoSrcDerivedTableMapping {
	1: required TSourceTable derivedSrcTable;
	2: required i32 mongoCollectionId;
	3: required string lateralViewInfo;
	4: required list<TMongoColMapping> mappings;
}

#Banding
enum TBandValType {VALUE, DATE}

enum TOperator {NOP,GT,LT,LE,GE,EQ}
struct TBandConditon {
	1: required TOperator operator;
	2: required double operand;
}

struct TBandRange{
	1: required string name;
	2: required list<TBandConditon> conditions;
}

struct TBand{
	1: required i32 id;
	2: required string name;
	3: required string dimTableName;
	4: required string attrName;
	5: required TBandValType type;
	6: required list<TBandRange> bandRanges;
}

struct TDimAttrEntity{
	1: required string dimension;
	2: required string attrName;
}


struct TRangeFilter {
	1: required  TDimAttrEntity operand;
	2: required string startValue;
	3: required string endValue;
}

struct TTargetDataLocation {
    	1: required i32 id;
    	2: required TTargetUploadStatus status;
    	3: required string location;
    	4: required string addedOn;
	5: required string uploadedBy;
	6: optional TRangeFilter range;
	7: optional TDimAttrEntity periodUnit;
	8: optional string errorFileLocation;
}

struct TKpiName {
	1: required string kpiId;
	2: required string name;
	3: required bool isAdditive;
	4: optional string dbName;
	5: optional string tableName;
	6: optional string dataLocation;
}

struct TKpiTarget {
	1: required i32 id;
	2: required string targetName;
	3: required list<TKpiName> kpis;
	4: required i32 orgId;
	5: required list<TTargetDataLocation> dataLocations;
	6: required bool isActive;
	7: required string modifiedOn;
	8: required bool isTargetDataAvailable;
	9: required list<TDimAttrEntity> groupDimension;
}

struct THierarchyChangeRequest {
	1: required string requestId;
	2: required string dimTableName;
	3: required i32 dimTableId;
	4: required list<string> levels;
	5: required string status;
	6: optional string errorMessage;
}

struct TDimensionLevel {
        1: required string name;
        2: required bool isMutable;
}

struct TDimensionHierarchy {
        1: required string dimName;
        2: required string displayName;
        3: required list<TDimensionLevel> levels;
}

service TDimensionService {

    bool isAlive();
#dimension etl:
    list<TTableMapping> getAllMappingsForOrg(1: i32 orgId, 2: optional TMetaClient clientType) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
    list<TTransformation> getAllTransformations(1: i32 orgId, 2: optional TMetaClient clientType) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
    list<TSourceDimLinkingMapping> getAllDimLinkingInfo(1: i32 orgId, 2: optional TMetaClient clientType);
    list<TDimensionTable> getDimensionTablesByOrgId(1: i32 orgId, 2: optional TMetaClient clientType) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
    list<TDimensionTable> getElasticSearchableDimensionTablesByOrgId(1: i32 orgId, 2: optional TMetaClient clientType) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
    TSourceTable getSourceTableById(1: i32 orgId, 2: i32 id ,3: optional TMetaClient clientType) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
    list<TSourceTable> getSourceTablesByIds(1: i32 orgId, 2: list<i32> ids, 3: optional TMetaClient clientType) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
    TSourceColumn getSourceTableColumnById(1: i32 orgId, 2: i32 id, 3: optional TMetaClient clientType) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
    TSourceForeignKey getSourceForeignKeyById(1: i32 id, 2: optional TMetaClient clientType) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
    bool isMorningFileSyncEnabled(1: i32 orgId, 2: optional TMetaClient clientType) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);

#mongo sqoop
    list<TMongoCollection> getMongoCollections(1: i32 orgId, 2: optional TMetaClient clientType);
    list<TMongoSrcDerivedTableMapping> getMongoSrcDerivedTableMapping(1: i32 orgId, 2: optional TMetaClient clientType);

#api:
    TFact getFact(1: i32 orgId, 2: string factName, 3: optional TMetaClient clientType, 4: optional bool includeAllCols) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
    TFact getFactIncludingAllCols(1: string requestId, 2: i32 orgId, 3: string factName, 4: optional TMetaClient clientType) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
    TFact getPartialColumnDependentFact(1: i32 orgId, 2: string factName,3: string columnName, 4: optional TMetaClient clientType, 5: optional bool includeAllCols) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
    TFactDimension getFactWithDimension(1: i32 orgId, 2: string factName, 3: optional TMetaClient clientType, 4: optional bool includeAllCols, 5: optional bool includeCustomFields) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
    TFactDimension getFactWithDimensionIncludingAllCols(1:string requestId, 2: i32 orgId, 3: string factName, 4: optional TMetaClient clientType) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
    TFactDimension getPartialColumnDependentFactWithDimension(1: i32 orgId, 2: string factName, 3: string columnName, 4: optional TMetaClient clientType, 5: optional bool includeAllCols, 6: optional bool includeCustomFields) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
    list<TFact> getAllFacts(1: i32 orgId,2: optional TMetaClient clientType, 3: optional bool includeAllCols)  throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
    list<TDimension> getDimensionsByOrgId(1: i32 orgId, 2: optional TMetaClient clientType, 3: optional bool includeCustomFields) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
    string getLastSyncTimeForFact(1: i32 orgId, 2: string factName, 3: optional TMetaClient clientType) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
    string getLastSyncTimeForExecutionEnd(1: i32 orgId, 2: optional TMetaClient clientType) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
    TResponse updateSyncTimeForExecutionEnd(1: i32 orgId, 2: string masterTime, 3: optional TMetaClient clientType) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
    list<TDimAttrValueAvailability> getDimAttrValueAvailability(1: i32 orgId, 2: optional TMetaClient clientType) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
    map<string,list<string>> getDimensionValues(1: i32 orgId, 2: string dimension, 3: optional TMetaClient clientType) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
    list<string> getDimensionAttrValues(1: i32 orgId, 2: string dimension, 3: string attrName, 4: optional TMetaClient clientType) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
    list<string> getChangeLogAttrValues(1:i32 orgId, 2:i32 dimTableId, 3:i32 dimColId, 4:optional TMetaClient clientType) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
    TDimension getDimensionByOrgIdDimName(1: i32 orgId, 2: string name, 3: optional TMetaClient clientType, 4: optional bool includeCustomFields) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
	list<TDimColumn> getAllBandableAttr(1: i32 orgId, 2: string dimTableName, 3: optional TMetaClient clientType) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);

	TResponse createBanding(1: i32 orgId, 2: string dimTableName, 3: string attrName, 4: TBandValType type, 5: string bandName, 6: string displayName, 7: string description, 8: list<string> bandValueNames, 9: list<double> bandValues, 10: optional TMetaClient clientType) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
	TResponse editBanding(1: i32 orgId, 2: string dimTableName, 3: string attrName, 4: TBandValType type, 5: string bandName, 6: string displayName, 7: string description, 8: list<string> bandValueNames, 9: list<double> bandValues, 10: optional TMetaClient clientType) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
	TResponse deleteBanding(1: i32 orgId, 2: string dimTableName, 3: string bandName, 4: optional TMetaClient clientType) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);

	TBand getBanding(1: i32 orgId, 2: string dimName, 3: string bandName, 4: optional TMetaClient clientType) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
	list<TBand> getBandingByDimension(1: i32 orgId, 2: string dimName, 3: optional TMetaClient clientType) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
    list<TApplicableOrgContext> getApplicableContexts(1: i32 orgId, 2: string tableName, 3: optional TMetaClient clientType) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
	TResponse createTarget(1: i32 orgId, 2: string targetName, 3: list<TKpiName> kpis, 4: list<TDimAttrEntity> groupDimensions, 5: optional TMetaClient clientType) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
	TTargetDataLocation addTargetDataLocation(1: i32 orgId, 2: i32 targetId, 3: string location, 4: string uploadedBy, 5: optional TMetaClient clientType) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
	TTargetDataLocation updateTargetDataLocation(1: i32 orgId, 2: i32 targetId, 3: TTargetDataLocation taregetDataLocation, 4: optional TMetaClient clientType) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
	TResponse updateTargetMergeDataLocation(1: i32 orgId, 2: i32 targetId, 3: string kpiId, 4: string dataLocation, 5: optional TMetaClient clientType) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
	TResponse updateTargetUploadStatus(1: i32 orgId, 2: i32 targetId, 3: i32 dataLocationId, 4: TTargetUploadStatus status, 5: optional TMetaClient clientType) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
	list<TKpiTarget> getAllTargetKPIs(1: i32 orgId, 2: optional TMetaClient clientType) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
	TKpiTarget getTargetKPIById(1: i32 orgId, 2: i32 id, 3: optional TMetaClient clientType) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
	TResponse disableTargetKPI(1: i32 orgId, 2: i32 id, 3: optional TMetaClient clientType) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
	TResponse enableTargetKPI(1: i32 orgId, 2: i32 id, 3: optional TMetaClient clientType) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);


#Validator
    list<TDimension> getDimensionByDimTableName(1: string dimTableName, 2: optional TMetaClient clientType, 3: optional bool includeCustomFields);
    TFact getFactTableByName(1: i32 orgId, 2: string name, 3:optional TMetaClient clientType, 4: optional bool includeAllCols);
#phaseExecutor

    list<TOrganization> getAllOrganizations(1: optional TMetaClient clientType);

#fact_etl_apis:
    list<TCatalog> getAllCatalogs(1: i32 orgId, 2: optional TMetaClient clientType, 3: optional bool includeAllCols, 4: optional bool includeCustomFields) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
    list<TCatalog> getAllSummaryCatalogs(1: i32 orgId, 2: optional TMetaClient clientType, 3: optional bool includeAllCols, 4: optional bool includeCustomFields) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
    list<TCatalog> getAllViewCatalogs(1: i32 orgId, 2: optional TMetaClient clientType) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
    list<TEndPoint> getAllEndPoints(1: optional TMetaClient clientType) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
    list<TSourceTable> getAllSourceTables(1: i32 orgId, 2: optional TMetaClient clientType) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
    list<TSourceTable> getAllSqoopSourceTables(1: optional TMetaClient clientType) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
    list<TSourceFactMapping> getAllFactMappings(1: i32 orgId, 2: optional TMetaClient clientType) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
    TFactEtl getFactForEtl(1: i32 orgId, 2: string factName, 3: optional TMetaClient clientType) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
    list<TFactEtl> getAllFactsForEtl(1: i32 orgId, 2: optional TMetaClient clientType) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
    list<TFactForeignKey> getForeignKey(1: i32 orgId, 2: string factName, 3: string refTableName, 4: optional TMetaClient clientType) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
    list<TAttributionStrategy> getAttributionStrategiesForFact(1: i32 orgId, 2: string factName, 3: optional TMetaClient clientType) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
    void createValueTablesForDimension(1: i32 orgId, 2: i32 dimTableId, 3: optional TMetaClient clientType) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);

    list<TSourceForeignKey> getAllForeignKeys(1: i32 orgId, 2: optional TMetaClient clientType);
    void updateLastComputedForKPIs(1: list<i32> columnIds, 2: string computedOn, 3: optional TMetaClient clientType);
    void addFactDataLocation(1: i32 runId, 	2: bool isFullRun, 	3: string runDate, 	4: i32 orgId,
     	5: string tableName, 	6: string createTableSchema, 	7: string path, 8: string
     	partitionKeys, 9: list<string> partitionValues, 10: TCatTableType tableType, 11: optional TMetaClient clientType);
    TResponse addFactDataLocations(1: i32 runId, 2: bool isFullRun, 3: string runDate, 	4: i32 orgId, 5: list<TFactStorageInfo> storageInfo, 6: optional TMetaClient clientType);
    TFactDataLocation getFactDataLocation(1: i32 orgId, 2: string tableName, 3: TCatTableType tableType, 4: optional TMetaClient clientType);
    void addIntermediateTableDataLocation(1: list<TIntermediateTableDataLocation> intermediateTableDataLocation, 2: optional TMetaClient clientType);
    TIntermediateTableDataLocation getIntermediateTableDataLocation(1: i32 orgId, 2: string dbName, 3: string tableName, 4: optional TMetaClient clientType);
    void addDimensionDataLocation(1: list<TDimensionDataLocation> dimDataLocations, 2: optional TMetaClient clientType);
    void addCustomTableDataLocation(1: list<TDimensionDataLocation> dimDataLocations, 2: optional TMetaClient clientType);
    TResponse informCustomFieldsSyncUpdate(1: i32 orgId, 2: i32 customTableId, 3: list<string> colNames, 4: string syncTime, 5: optional TMetaClient clientType);
    TResponse uploadSegment(1: i32 orgId, 2: i32 runId, 3: string runDate, 4: string dimensionName, 5: string attrName,6: string segmentDisplayName, 7: string createStatement, 8:string path, 9: list<string> segmentValues, 10: bool hasChangeLog, 11: bool isDataRefreshRequired, 12: optional TMetaClient clientType);
    TResponse disableOrgSpecificDimAttr(1: i32 orgId, 2: string dimensionTableName, 3: string attrName, 4: optional TMetaClient clientType) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
    TDimensionDataLocation getDimensionDataLocation(1: i32 orgId, 2: string tableName, 3: optional TMetaClient clientType) throws(1:exceptions.WrongArgumentException ex);
    TDimensionDataLocation getCustomTableDataLocation(1: i32 orgId, 2: string tableName, 3: optional TMetaClient clientType) throws(1:exceptions.WrongArgumentException ex);
    TDimensionDataLocation getDimensionAttrDataLocation(1: i32 orgId, 2: string tableName, 3: string attrName, 4: optional TMetaClient clientType) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
    list<TDimPossibleValueTableInfo> getDimAttrTableDetails(1: i32 orgId, 2: optional TMetaClient clientType) throws(1:exceptions.WrongArgumentException ex);
    TResponse notifyEtlCompletionForTheOrg(1: i32 orgId, 2: optional TMetaClient clientType) throws(1:exceptions.WrongArgumentException ex);
    list<TDataLocationPath> getAllDataLocationPaths(1: i32 orgId, 2: optional TMetaClient clientType) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
    map<string, string> getViewCreateSchema(1: i32 orgId, 2: optional TMetaClient clientType) throws(1:exceptions.WrongArgumentException ex);
    list<string> getCommonFactNamesForDimension(1: i32 orgId, 2: list<string> dimensions, 3: optional TMetaClient clientType) throws(1:exceptions.WrongArgumentException ex);

    # returns the versio id
    #string addChangeLogLocation(1:  string runDate,  2: i32 orgId, 3: string tableName,  4: i32 dimTableId, 5: i32 dimColumnId, 6:string createTableSchema, 7: TChangeLogLocationType type,  8: string path, 9: list<string> partitionKeys, list<string> partitionvalues ,  optional list<i32> versionsToInvalidate,  optional TMetaClient clientType);
    list<TChangeLogDataLocation> getChangeLogLocation( 1: i32 orgId,  2: i32 dimId, 3: i32 dimColumnId, 4: optional TMetaClient clientType)

#   TableNameSpace format: tableName#Orgid.dbName.endPoint
	list<TStorageLocation> getDataStorageLocation(1: TStorageEntityType tableType, 2: string tableNameSpace, 3: TMetaClient clientType) throws(1:exceptions.WrongArgumentException ex);
	TResponse setDataStorageLocation(1: list<TStorageLocation> storageLocations,2: TMetaClient clientType) throws(1:exceptions.WrongArgumentException ex);
    list<TSchemaStorage> getSchemaStorage(1: string nameSpace, 2: TMetaClient clientType) throws(1:exceptions.WrongArgumentException ex);
	TResponse setSchemaStorage(1: list<TSchemaStorage> schemaStorages,2: TMetaClient clientType) throws(1:exceptions.WrongArgumentException ex);
    TDuration getFactIncrementalComputationPeriod(1: i32 orgId, 2:string factName, 3: TMetaClient clientType) throws(1:exceptions.WrongArgumentException ex);

    list<TScopeInfo> getAllVerticalScopes();
    list<TScopeInfo> getVerticalScopesForOrg(1: i32 orgId, 2: TMetaClient clientType) throws(1:exceptions.WrongArgumentException ex);

#untracked:
    void addSourceDataLocation(1: list<TSourceDataLocation> sourceDataLocation, 2: optional TMetaClient clientType) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
    TSourceDataLocation getSourceDataLocation(1: i32 orgId, 2: string endPoint, 3: string dbName, 4: string tableName, 5: optional TMetaClient clientType) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
    map<i32, i32> getDimSrcIdTargetIdMap(1: i32 dimId, 2: i32 scopeId, 3: list<i32> values) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
    list<TFactDimScope> getAllScopes() throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
    void addDimValues(1: i32 dimId, 2: i32 scopeId, 3: list<string> values) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
    map<string, i32> getDimSrcValueTargetIdMap(1: i32 dimId, 2: i32 scopeId, 3: list<string> values) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
    map<string, i32> getDimSrcValuesTargetMap(1: i32 dimId, 2: i32 scopeId) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
    map<i32, i32> getDimSrcIdsTargetMap(1: i32 dimId, 2: i32 scopeId) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
    map<string, i32> getNewDimIds(1: i32 dimId, 2: i32 scopeId, 3: list<string> dimValues) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
    map<i32, i32> getNewDimIdsForSrcIds(1: i32 dimId, 2: i32 scopeId, 3: map<string, i32> dimValues) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
    list<string> getInvalidDimValues(1: i32 dimId, 2: i32 scopeId) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
    list<string> getInvalidDimValuesForSrcId(1: i32 dimId, 2: i32 scopeId) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
    void acceptDimValueForSrcValues(1: i32 dimId, 2: i32 scopeId, 3: map<string, string> targetValueMap) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
    void acceptDimValueForSrcIds(1: i32 dimId, 2: i32 scopeId, 3: map<string, string> targetValueMap) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
    void addSrcValueTargetDimMap(1: i32 dimId, 2: i32 scopeId, 3: map<string, i32> srcTargetMap) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
    void addSrcIdTargetDimMap(1: i32 dimId, 2: i32 scopeId, 3: map<string, i32> srcTargetMap) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
    void rejectSrcDimValues(1: i32 dimId, 2: i32 scopeId, 3: list<string> srcDimValues) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
    void rejectSrcDimIdValues(1: i32 dimId, 2: i32 scopeId, 3: list<string> srcDimValues) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
    void disableDimension(1: string name) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
    list<TDimensionValueTables> getDimensionValueTables(1: i32 orgId) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
    i32 getProviderTableId(1: i32 providerId, 2: string providerTableName) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
    void addDimension(1: string dimName, 2: string dimTableName) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
    void addFactTable(1: string name, 2: string definition, 3: TScope scope, 4: i32 scopeId, 5: string primaryDateDimension, 6: list<i32> parentSourceTables);
    void addFactTableColumns(1: string factTableName, 2: list<TFactColumn> columnList, 3: i32 scopeId) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
    void addDimensionTable(1: string name, 2: TDimensionType dimType, 3: TStructureType structureType, 4: TScope scope, 5: i32 scopeId, 6: bool isLarge) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
    void updateDimensionTable(1: i32 dimId, 2: string name, 3: TScope scope, 4: bool isLarge, 5: bool isActive);
    TResponse updateDimensionHierarchy(1: i32 orgId, 2: string orgName, 3: string dimTableName, 4: list<string> levels, 5: optional TMetaClient clientType) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
    list<TDimensionHierarchy> getDefaultLevelsForDimensionHierarchy(1: i32 orgId, 2: TMetaClient clientType) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
    TResponse addHierarchyUpdateRequestForDimension(1: i32 orgId, 2: string dimTableName, 3: list<string> levels, 4: TMetaClient clientType) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
    list<THierarchyChangeRequest> getDimensionHierarchyUpdateStatus(1: i32 orgId, 2: TMetaClient clientType) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
    TResponse disableHierarchyUpdateRequest(1: i32 orgId, 2: string requestId, 3: TMetaClient clientType) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
    TResponse executeDimHierarchyUpdateRequest(1: i32 orgId, 2: TMetaClient clientType) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
    TResponse executeAllDimHierarchyUpdateRequest(1: TMetaClient clientType) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
    void disableDimensionTable(1: i32 dimId);
    list<TDimColType> getDimColType();
    list<TDimColDataType> getDimColDataType();
    void addScope(1: TScope scope, 2: string name);
    list<TScope> getDimensionScopeTypes();
    list<TDimensionType> getDimensionTypes();
    list<TStructureType> getDimensionStructureTypes();
    list<string> getDimColumnPossibleValues(1: i32 orgId, 2: i32 dimId, 3:TStructureType structureType, 4: i32 columnId);
    void putConfigKeyValue(1: i32 orgId, 2: string key, 3: string value, 4: optional TMetaClient clientType) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
    list<TSourceForeignKey> getAllFksBetweenTable(1: i32 primaryTable, 2: i32 secondaryTable, 3: optional TMetaClient clientType) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
    list<TDimension> getAllApplicableDimensions(1: i32 scopeId, 2: optional TMetaClient clientType) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
    TResponse syncCustomTablesMetadata(1: i32 orgId, 2: bool isFullRun,3: string masterTime , 4: optional TMetaClient clientType) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
    TResponse syncAllCustomTableMetadata(1: bool isFullRun, 2: optional TMetaClient clientType) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
    TResponse syncOrgConfigKeys(1: i32 orgId, 2: optional TMetaClient clientType) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
    TResponse syncAllOrgsConfigKeys(1: optional TMetaClient clientType) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
    list<TCustomTable> getCustomTables(1: i32 orgId, 2: optional TMetaClient clientType) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
    TCustomTable getCustomTableByName(1: i32 orgId, 2: string name, 3: optional TMetaClient clientType) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
    list<TCustomTable> getAllDefinedCustomTables(1: i32 orgId, 2: optional TMetaClient clientType) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
    list<TTransposeTable> getCustomTransposeTables(1: i32 orgId, 2: bool isFullRun, 3: optional TMetaClient clientType) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
    list<TTransposeTable> getCustomTransposeTableByName(1: i32 orgId, 2: bool isFullRun, 3: string customTableName, 4: optional TMetaClient clientType) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
    list<TTransposeTable> getTransposeTables(1: i32 orgId, 2: optional TMetaClient clientType) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
    list<TTransposeTable> getTransposeTablesWithColumns(1: i32 orgId, 2: optional TMetaClient clientType) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
    bool isFullSolrIndexRequired(1: i32 orgId, 2: optional TMetaClient clientType) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
    #list<TTransposeColumn> getTransposeColumns(1: i32 orgId; 2: i32 transposeTableId, 3: optional TMetaClient clientType);
#fact platformization
    TResponse createSourceTable(1: string details, 2: TMetaClient clientType) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
    TResponse createDimensionTable(1: string details, 2: TMetaClient clientType) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
    TResponse createFactTable(1: string details, 2: TMetaClient clientType) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);

# metadata population client
    TResponse saveProviderDimensionMapping(1: i32 orgId, 2: i32 dimTableId, 3: list<TProviderDimensionMapping> mappings, 4: optional TMetaClient clientType);
    TResponse saveTransformation(1: TTransformation transformation, 2: optional TMetaClient clientType);
    TDimensionTable getDimensionTableByDimId(1: i32 orgId, 2: i32 dimId, 3: optional TMetaClient clientType) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
    TDimensionTableInfo getDimensionTableByOrgIdDimTableName(1: i32 orgId, 2: string dimTableName, 3: optional TMetaClient clientType) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
    TDimensionTableWithColumn getDimensionTableColumns(1: i32 orgId, 2: string dimTableName, 3: optional TMetaClient clientType) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
    list<TOrgScope> getOrganizationScopesByOrgId(1: i32 orgId, 2: optional TMetaClient clientType) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
    TResponse addOrg(1: i32 orgId, 2: string orgName, 3: list<string> scopes, 4: optional TMetaClient clientType) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
    list<TDimensionTable> getAllDimensionTables(1: optional TMetaClient clientType) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
    map<TScope,list<string>> getScopeWiseValues(1: optional TMetaClient clientType);
    TResponse addDimensionTableCols(1: string dimTableName, 2: list<TDimColumn> columns, 3: optional TMetaClient clientType);
    TResponse saveDimensionTableCols(1: string dimTableName, 2: list<TDimColumn> columns, 3: optional TMetaClient clientType);
    list<TDimensionTable> getOrgSpecificDimensionTables(1: i32 orgId, 2: optional TMetaClient clientType) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
    TTransformation getTransformation(1: i32 orgId, 2: i32 dimTableId, 3: optional TMetaClient clientType) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
    list<string> getProviderTables(1: optional TMetaClient clientType);
    list<string> getProviderTablesByDimTableId(1: i32 dimTableId, 2: optional TMetaClient clientType) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
    list<TDimension> getDimensionByOrgIdDimNames(1: i32 orgId, 2: list<string> dimName, 3: optional TMetaClient clientType) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
    TTransformation getSuitableTransformation(1: i32 orgId, 2: i32 dimId, 3: optional TMetaClient clientType) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
    map<i32,string> getAllOrgs(1: optional TMetaClient clientType);
    list<TProviderDimensionMapping> getProviderDimMapping(1:i32 orgId, 2:i32 dimId, 3: optional TMetaClient clientType) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
#s3sync apis for hierarchy update requests
    TResponse putHierarchyUpdateRequestsToS3(1: TMetaClient clientType) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
    TResponse syncHierarchyUpdateRequestsToMeta(1: TMetaClient clientType) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
    TResponse putHierarchyUpdateResponseToS3(1: TMetaClient clientType) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
    TResponse syncHierarchyUpdateResponseToMeta(1: TMetaClient clientType) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
#config management
    list<TConfigKeyValue> getAllConfigsForOrg(1: i32 orgId, 2: optional TMetaClient clientType) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);

    list<TDimAttrChangeLogTable> getAllDimAttrChangeLogTables(1: i32 orgId, 2: optional TMetaClient clientType) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
    list<TDefaultEtlDataStatus> getDefaultEtlDataStatusForDimension(1: i32 orgId, 2: i32 dimTableId, 3: optional TMetaClient clientType) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
    list<TDimSearchAttrValues> getDimAttrValuesByConstraints(1: i32 orgId, 2: string dimName, 3: string dimAttr, 4: TDimOperationType operation, 5: TDimParams searchParams, 6: optional list<string> projections, 7: optional TMetaClient clientType) throws(1: exceptions.WrongArgumentException ex1, 2: exceptions.InvalidMetadataException ex2, 3: exceptions.MetaApiRunTimeException ex3);
}