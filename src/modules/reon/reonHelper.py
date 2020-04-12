from src.Constant.constant import constant
from src.modules.reon.reonThrift import ReonThrift
from src.utilities.utils import Utils
from src.utilities.logger import Logger

class ReonHelper():
    @staticmethod
    def checkReonConnection(ignoreConnectionError=False):
        Utils.checkServerConnection('REON_METADATA_API_THRIFT_SERVICE', ReonThrift, 'reonport',
                                    ignoreConnectionError)

    @staticmethod
    def getConnObj(newConnection=False):
        port = constant.config['reonport'].next()
        connPort = str(port) + '_obj'
        if connPort in constant.config:
            if newConnection:
                constant.config[connPort].close()
                constant.config[connPort] = ReonThrift(port)
            return constant.config[connPort]
        else:
            return ReonThrift(port)

    @staticmethod
    def getLevelsForDimension(dimName):
        try:
            connection = ReonHelper.getConnObj()
            defaultLevelForDimension = connection.getDimensionByOrgIdDimName(dimName).levels
            dimAttrValue = connection.getDimAttrValueAvailability()
            return ReonHelper.constructLevelForDimension(defaultLevelForDimension, dimAttrValue, dimName)
        except Exception,exp:
            raise Exception(exp)

    @staticmethod
    def constructLevelForDimension(defaultLevelForDimension, dimAttrValue, dimName):
        result = list()
        for eachLevelForDimension in defaultLevelForDimension:
            attrName = defaultLevelForDimension[eachLevelForDimension].name
            for eachAttr in dimAttrValue:
                cardinaliaty = 'HIGH'
                if dimName == eachAttr.dimName and attrName == eachAttr.attrName:
                    if not eachAttr.isHighCardinality:
                        cardinaliaty = 'LOW'
                    result.append({
                        'levelNum':eachLevelForDimension,
                        'levelName':attrName,
                        'levelValuesCount':eachAttr.valueCount,
                        'cardinality':cardinaliaty
                    })
        return result

    @staticmethod
    def getLevelValuesForDimension(dimName,attrName):
        try:
            connection = ReonHelper.getConnObj()
            listOfDimAttrValues = connection.getDimensionAttrValues(dimName,attrName)
            return listOfDimAttrValues
        except Exception,exp:
            raise Exception(exp)

    @staticmethod
    def getLevelValuesUsingSearchText(dimName,levelName,searchText):
        #try:
        result = list()
        connection = ReonHelper.getConnObj()
        dimSearchAttrValues = connection.getDimAttrValuesByConstraints(dimName,levelName,searchText)
        for each in dimSearchAttrValues:
            result.append(each.dimAttrValues)
        return {
            'levelName' : levelName,
            'searchText':searchText,
            'levelValues':result
        }
        #except Exception,exp:
        #    raise Exception(exp)
