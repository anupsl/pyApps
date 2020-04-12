from src.Constant.constant import constant
from src.initializer.generateThrift import datamanager
from src.utilities.logger import Logger
from thriftpy.rpc import make_client
import random


class DatamanagerThrift(object):

    def __init__(self, port, timeout=60000):
        self.conn = make_client(datamanager.DataManagerService, '127.0.0.1', port, timeout=timeout)

    def getServerRequestID(self):
        pass
        
    def close(self):
        Logger.log('Closing DatamanagerThrift connection')
        self.conn.close()

    def log(self, output):
        Logger.log(output)
        return output

    def getAvailablePackagesInfo(self, orgID):       
        Logger.log('orgID: ',orgID)
        return self.log(self.conn.getAvailablePackagesInfo(orgID))

    def getAvailablePackagesDetails(self, orgID):       
        Logger.log('orgID: ',orgID)
        return self.log(self.conn.getAvailablePackagesDetails(orgID))

    def addDataToPackage(self, orgID, packageID, idColumnName, data):       
        Logger.log('orgID: ',orgID, ' packageID: ',packageID, ' idColumnName: ',idColumnName, ' data: ',data)
        return self.log(self.conn.addDataToPackage(orgID, packageID, idColumnName, data))

    def createDataPack(self, orgID, packageName, idColumnName, data):       
        Logger.log('orgID: ',orgID, ' packageName: ',packageName, ' idColumnName: ',idColumnName, ' data: ',data)
        return self.log(self.conn.createDataPack(orgID, packageName, idColumnName, data))

    def getRuleExpressionLibrary(self, orgID, eventType):       
        Logger.log('orgID: ',orgID, ' eventType: ',eventType)
        return self.log(self.conn.getRuleExpressionLibrary(orgID, eventType))

    def resolveDependentEnum(self, orgID, typ):       
        Logger.log('orgID: ',orgID, ' type: ',typ)
        return self.log(self.conn.resolveDependentEnum(orgID, typ))

