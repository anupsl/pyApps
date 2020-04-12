import random

from thriftpy.rpc import make_client

from src.Constant.constant import constant
from src.initializer.generateThrift import reonDimension
from src.modules.reon.reonObject import ReonObject
from src.utilities.logger import Logger


class ReonThrift(object):
    def __init__(self, port, timeout=60000):
        self.conn = make_client(reonDimension.TDimensionService, '127.0.0.1', port, timeout=timeout)
        self.getServerRequestID()

    def close(self):
        Logger.log('Closing Reon thrift connection')
        self.conn.close()

    def getServerRequestID(self):
        self.serverRequestID = 'campaignShard_auto_' + str(random.randint(11111, 99999))

    def log(self, output):
        Logger.log(output)
        return output

    def isAlive(self):
        return self.log(self.conn.isAlive())

    def getDefaultLevelsForDimensionHierarchy(self, clientType):
        Logger.log('Params : OrgId :{} and clientType as :{}'.format(constant.config['orgId'], clientType))
        return self.log(self.conn.getDefaultLevelsForDimensionHierarchy(constant.config['orgId'], clientType))

    def getDimAttrValueAvailability(self):
        Logger.log('Params : OrgId :{}'.format(constant.config['orgId']))
        return self.log(
            self.conn.getDimAttrValueAvailability(constant.config['orgId'], ReonObject().TMetaClient['READ_API']))

    def getDimensionByOrgIdDimName(self, dimName):
        Logger.log('Params : OrgId :{} and clientType as :{}'.format(constant.config['orgId'], dimName))
        return self.log(self.conn.getDimensionByOrgIdDimName(constant.config['orgId'], dimName,
                                                             ReonObject().TMetaClient['READ_API'], True))

    def getDimensionAttrValues(self, dimName, attrName):
        Logger.log(
            'Params : OrgId :{} and clientType as :{} and attributeName :{} '.format(constant.config['orgId'], dimName,
                                                                                     attrName))
        return self.log(self.conn.getDimensionAttrValues(constant.config['orgId'], dimName, attrName,
                                                         ReonObject().TMetaClient['READ_API']))

    def getDimAttrValuesByConstraints(self, dimName, levelName, searchText):
        Logger.log(
            'Params : OrgId :{} and clientType as :{} and LevelName :{} and searchText :{}'.format(
                constant.config['orgId'], dimName,
                levelName, searchText))
        return self.log(self.conn.getDimAttrValuesByConstraints(constant.config['orgId'], dimName, levelName,
                                                                ReonObject().TDimOperationType['SEARCH'],
                                                                ReonObject().TDimParams(searchText), list(),
                                                                ReonObject().TMetaClient['READ_API']))
