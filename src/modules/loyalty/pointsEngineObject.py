import time
from src.Constant.constant import constant
from src.initializer.generateThrift import pointsEngine
from src.utilities.utils import Utils
from src.utilities.randValues import randValues

class PointsEngineObject(object):

    @staticmethod
    def PurchaseHistoryFilterParams(updateDict = {}):
        tmpDict = {
            'billIds' : []
        }
        tmpDict.update(updateDict)
        return pointsEngine.PurchaseHistoryFilterParams(**tmpDict)

    @staticmethod
    def BillPointsParams(updateDict = {}):
        tmpDict = {
            'orgId' : constant.config['orgId'],
            'billId' : 0
        }
        tmpDict.update(updateDict)
        return pointsEngine.BillPointsParams(**tmpDict)

    @staticmethod
    def CustomerFilter(updateDict = {}):
        tmpDict = {
            'orgId' : constant.config['orgId'],
            'customerId' : 0
        }
        tmpDict.update(updateDict)
        return pointsEngine.CustomerFilter(**tmpDict)