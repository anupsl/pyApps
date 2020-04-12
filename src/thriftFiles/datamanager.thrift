#!thrift -java -php -phps

/**
 * This file contains all the service and data object definitions which will be used to generate thrift classes.
*/

namespace java com.capillary.shopbook.events.api.data.thrift
namespace php dataservice

include "./src/thriftFiles/nrules.thrift"

struct FactInfo {
    1: required i64 factID;
    2: required string factName;
    3: required nrules.DataType factDataType;
    4: required bool isComplex;
    5: optional list <nrules.DataType> parameterTypes;
}

struct PackageInfo {
    1: required i64 packageID;
    2: required string packageName;
    3: optional string description;
    4: optional map <string, FactInfo> namesToFactMap;
}



service DataManagerService {

    /**
    * The list of all the available packages.
    * @param orgID The organization id.
    */
    list <PackageInfo> getAvailablePackagesInfo (1: i32 orgID);

    /**
    * @param orgID The organization id.
    * @return The list of all packages with the details of all facts under the package.
    */
    list <PackageInfo> getAvailablePackagesDetails (1: i32 orgID);

    void addDataToPackage (1:i32 orgID, 2:i64 packageID, 3:string idColumnName, 4:map <string, list <string>> data);
    i64 createDataPack (1:i32 orgID, 2:string packageName, 3:string idColumnName, 4:map <string, list <string>> data);

	/**
	* @param orgID
	* @return Rule grammar JSON string
	*/
	string getRuleExpressionLibrary (1:i32 orgID, 2:string eventType);

	/**
	* @param orgID
    * @param type
	* @return List of values for the dependent enum
	*/
    list <string> resolveDependentEnum(1:i32 orgID, 2:string type);
}
