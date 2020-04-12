import time
from src.Constant.constant import constant
from src.initializer.generateThrift import peb
from src.utilities.utils import Utils



class PEBObject(object):

    @staticmethod
    def BulkExpiryReportData(bulkExpiryReportData):
        tmpDict = {
            'orgId' : constant.config['orgId'],
            'loggedInUserId' : 0,
            'fromTimeInMillis' : Utils.getTime(days=-1, milliSeconds=True),
            'toTimeInMillis' : Utils.getTime(milliSeconds=True),
            'includeExpired' : True,
            'includeRedeemed' : True
        }
        tmpDict.update(bulkExpiryReportData)
        return peb.BulkExpiryReportData(**tmpDict)

    @staticmethod
    def BulkAllocatePointsData(bulkAllocatePointsData={}, promotionInfo='', customerIdList=[]):
        tmpDict = {
            'orgId' : constant.config['orgId'],
            'programId' : constant.config['programId'],
            'allocationStrategyId' : constant.config['allocationStrategyId'],
            'expiryStrategyId' : constant.config['expiryStrategyId'],
            'promotionInfo' : promotionInfo,
            'owner' : 'CAMPAIGN',
            'customerId' : customerIdList,
            'tillID' : constant.config['tillId'],
            'awardedTimeInMillis' : Utils.getTime(milliSeconds=True),
            'createdBy' : -1
        }
        tmpDict.update(bulkAllocatePointsData)
        return peb.BulkAllocatePointsData(**tmpDict)

    @staticmethod
    def CustomersData(customerIds):
        tmpDict = {
            'orgId' : constant.config['orgId'],
            'programId' : constant.config['programId'],
            'customerIds' : customerIds
        }
        return peb.CustomersData(**tmpDict)
