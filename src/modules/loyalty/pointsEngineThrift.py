from src.Constant.constant import constant
from src.initializer.generateThrift import pointsEngine
from src.utilities.logger import Logger
from thriftpy.rpc import make_client
import random


class PointsEngineThrift(object):

    def __init__(self, port, timeout=60000):
        self.conn = make_client(pointsEngine.PointsEngineService, '127.0.0.1', port, timeout=timeout)
        self.getServerRequestID()

    def getServerRequestID(self):
        self.serverRequestID = 'pe_auto_'+str(random.randint(11111, 99999))

    def close(self):
        Logger.log('Closing PointsEngineThrift connection')
        self.conn.close()

    def log(self, output):
        Logger.log(output)
        return output

    def isActive(self):
        return self.log(self.conn.isActive())

    def getCustomerPointsSummary(self, orgID, customerId):       
        Logger.log('orgID: ',orgID, ' customerId:', customerId, ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.getCustomerPointsSummary(orgID, customerId, self.serverRequestID))

    def getCustomerPointsSummariesByFilter(self, customerFilter):       
        Logger.log('customerFilter:', customerFilter, ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.getCustomerPointsSummariesByFilter(customerFilter, self.serverRequestID))

    def getCustomerPointsSummaries(self, orgID, customerId):       
        Logger.log('orgID: ',orgID, ' customerId:', customerId, ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.getCustomerPointsSummaries(orgID, customerId, self.serverRequestID))

    def getPurchaseHistoryForCustomer(self, orgID, customerId):       
        Logger.log('orgID: ',orgID, ' customerId:', customerId, ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.getPurchaseHistoryForCustomer(orgID, customerId, self.serverRequestID))

    def getAllPurchaseHistoryForCustomer(self, customerFilter):       
        Logger.log('customerFilter:', customerFilter, ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.getAllPurchaseHistoryForCustomer(customerFilter, self.serverRequestID))

    def getPurchaseHistoryForCustomerFiltered(self, orgID, customerId, purchaseHistoryFilterParams):       
        Logger.log('orgID: ',orgID, ' customerId:', customerId,' purchaseHistoryFilterParams: ',purchaseHistoryFilterParams, ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.getPurchaseHistoryForCustomerFiltered(orgID, customerId, purchaseHistoryFilterParams, self.serverRequestID))

    def getAllPurchaseHistoryForCustomerFiltered(self, customerFilter, purchaseHistoryFilterParams):       
        Logger.log('customerFilter:', customerFilter,' purchaseHistoryFilterParams: ',purchaseHistoryFilterParams, ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.getAllPurchaseHistoryForCustomerFiltered(customerFilter, purchaseHistoryFilterParams, self.serverRequestID))

    def getAllPointsTransferSummaries(self, customerFilter):
        Logger.log('customerFilter:', customerFilter, ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.getAllPointsTransferSummaries(customerFilter, self.serverRequestID))

    def getPointsExpiryScheduleForCustomer(self, orgID, customerId):       
        Logger.log('orgID: ',orgID, ' customerId:', customerId, ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.getPointsExpiryScheduleForCustomer(orgID, customerId, self.serverRequestID))

    def getAllPointsExpiryScheduleForCustomer(self, customerFilter):       
        Logger.log('customerFilter:', customerFilter, ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.getAllPointsExpiryScheduleForCustomer(customerFilter, self.serverRequestID))


    def getPointsExpiryScheduleForCustomerFiltered(self, orgID, customerId, pointsExpiryScheduleFilterParams):       
        Logger.log('orgID: ',orgID, ' customerId:', customerId,' pointsExpiryScheduleFilterParams: ',pointsExpiryScheduleFilterParams, ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.getPointsExpiryScheduleForCustomerFiltered(orgID, customerId, self.serverRequestID))

    def getAllPointsExpiryScheduleForCustomerFiltered(self, customerFilter, pointsExpiryScheduleFilterParams):       
        Logger.log('customerFilter:', customerFilter,' pointsExpiryScheduleFilterParams: ',pointsExpiryScheduleFilterParams, ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.getAllPointsExpiryScheduleForCustomerFiltered(customerFilter, self.serverRequestID))


    def getBillPointsDetails(self, orgID, customerId, billId):       
        Logger.log('orgID: ',orgID, ' customerId:', customerId,' billId: ',billId, ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.getBillPointsDetails(orgID, customerId, billId, self.serverRequestID))

    def getAllBillPointsDetails(self, billPointsParams):       
        Logger.log('billPointsParams:', billPointsParams, ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.getAllBillPointsDetails(billPointsParams, self.serverRequestID))


    def getDeductionsForCustomer(self, orgID, customerId):       
        Logger.log('orgID: ',orgID, ' customerId:', customerId, ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.getDeductionsForCustomer(orgID, customerId, self.serverRequestID))

    def getAllDeductionsForCustomer(self, customerFilter):       
        Logger.log('customerFilter:', customerFilter, ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.getAllDeductionsForCustomer(customerFilter, self.serverRequestID))


    def getDeductionsForCustomerFiltered(self, orgID, customerId):       
        Logger.log('orgID: ',orgID, ' customerId:', customerId, ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.getDeductionsForCustomerFiltered(orgID, customerId, self.serverRequestID))

    def getAllDeductionsForCustomerFiltered(self, customerFilter):       
        Logger.log('customerFilter:', customerFilter, ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.getAllDeductionsForCustomerFiltered(customerFilter, self.serverRequestID))


    def getPointsExpiryDetailsForCustomerOnDate(self, orgID, customerId):       
        Logger.log('orgID: ',orgID, ' customerId:', customerId, ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.getPointsExpiryDetailsForCustomerOnDate(orgID, customerId, self.serverRequestID))

    def getAllPointsExpiryDetailsForCustomerOnDate(self, customerFilter):       
        Logger.log('customerFilter:', customerFilter, ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.getAllPointsExpiryDetailsForCustomerOnDate(customerFilter, self.serverRequestID))

    
    def getSlabUpgradeHistory(self, orgID, customerId):       
        Logger.log('orgID: ',orgID, ' customerId:', customerId, ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.getSlabUpgradeHistory(orgID, customerId, self.serverRequestID))

    def getAllSlabUpgradeHistory(self, customerFilter):       
        Logger.log('customerFilter:', customerFilter, ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.getAllSlabUpgradeHistory(customerFilter, self.serverRequestID))

    def getCustomerLevelPointsDetails(self, orgID, customerId):       
        Logger.log('orgID: ',orgID, ' customerId:', customerId, ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.getCustomerLevelPointsDetails(orgID, customerId, self.serverRequestID))

    def getAllCustomerLevelPointsDetails(self, customerFilter):       
        Logger.log('customerFilter:', customerFilter, ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.getAllCustomerLevelPointsDetails(customerFilter, self.serverRequestID))

    def sendBulkReminderMessageForAllPrograms(self):
        return self.log(self.conn.sendBulkReminderMessageForAllPrograms())

    def sendBulkReminderMessageForProgram(self, programId):       
        Logger.log('programId:', programId)
        return self.log(self.conn.sendBulkReminderMessageForProgram(programId))

    def bulkExpirePointsAsOnDateForAllPrograms(self, date):       
        Logger.log('date:', date)
        return self.log(self.conn.bulkExpirePointsAsOnDateForAllPrograms(date))
    
    def bulkExpirePointsAsOnDate(self, programId, date):       
        Logger.log('programId: ',programId,' date:', date)
        return self.log(self.conn.bulkExpirePointsAsOnDate(programId, date))

    def validateProgramConfiguration(self, progID, orgID):       
        Logger.log('progID: ',progID,' orgID: ',orgID, ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.validateProgramConfiguration(progID, orgID, self.serverRequestID))
    
    def alertBulkPointsExpiryReminder(self, alertBeforeDays):       
        Logger.log('alertBeforeDays: ',alertBeforeDays)
        return self.log(self.conn.alertBulkPointsExpiryReminder(alertBeforeDays))

    def bulkPointsExpiryScheduleInit(self, orgID, fromDate, toDate):       
        Logger.log('orgID: ',orgID, ' fromDate:', fromDate,' toDate: ',toDate, ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.bulkPointsExpiryScheduleInit(orgID, fromDate, toDate, self.serverRequestID))

    def bulkPointsExpiredInit(self, orgID, fromExpiryDate, toExpiryDate, includeExpired, includeRedeemed):       
        Logger.log('orgID: ',orgID, ' fromExpiryDate:', fromExpiryDate,' toExpiryDate: ',toExpiryDate,' includeExpired: ',includeExpired,' includeRedeemed: ',includeRedeemed, ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.bulkPointsExpiredInit(orgID, fromExpiryDate, toExpiryDate, includeExpired, includeRedeemed,  self.serverRequestID))
    
    def getBulkPointsExpired(self, orgID, pageId, sessionId):       
        Logger.log('orgID: ',orgID, ' pageId:',pageId, ' sessionId: ',sessionId, ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.getBulkPointsExpired(orgID, pageId, sessionId, self.serverRequestID))
    

    ## Health Dashboard related methods 
    def getPointsExpiryRemindersInfo(self, orgID, startDate, endDate):       
        Logger.log('orgID: ',orgID, ' startDate:', startDate,' endDate: ',endDate, ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.getPointsExpiryRemindersInfo(orgID, startDate, endDate, self.serverRequestID))

    def getPointsExpiryRemindersSentInfo(self, orgID, startDate, endDate):       
        Logger.log('orgID: ',orgID, ' startDate:', startDate,' endDate: ',endDate, ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.getPointsExpiryRemindersSentInfo(orgID, startDate, endDate, self.serverRequestID))

    def getPointsExpiryInfo(self, orgID, startDate, endDate):       
        Logger.log('orgID: ',orgID, ' startDate:', startDate,' endDate: ',endDate, ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.getPointsExpiryInfo(orgID, startDate, endDate, self.serverRequestID))
    
    def getPointsExpiredInfo(self, orgID, startDate, endDate):       
        Logger.log('orgID: ',orgID, ' startDate:', startDate,' endDate: ',endDate, ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.getPointsExpiredInfo(orgID, startDate, endDate, self.serverRequestID))

    def getPromotionExpiryInfo(self, orgID, startDate, endDate):       
        Logger.log('orgID: ',orgID, ' startDate:', startDate,' endDate: ',endDate, ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.getPromotionExpiryInfo(orgID, startDate, endDate, self.serverRequestID))

    def isProgramPresentForOrg(self, orgID):       
        Logger.log('orgID: ', ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.isProgramPresentForOrg(orgID, self.serverRequestID))
    
    def createBasicProgram(self, orgID, basicProgram, createdBy):       
        Logger.log('orgID: ',orgID, ' basicProgram:', basicProgram,' createdBy: ',createdBy, ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.createBasicProgram(orgID, basicProgram, createdBy, self.serverRequestID))

    def getBasicProgramDetails(self, orgID):       
        Logger.log('orgID: ', ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.getBasicProgramDetails(orgID, self.serverRequestID))

    def getAllBasicProgramDetails(self, programFilter):       
        Logger.log('programFilter: ', ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.getAllBasicProgramDetails(programFilter, self.serverRequestID))

    def getPointsCurrencyRatio(self, orgID):       
        Logger.log('orgID: ', orgID, ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.getPointsCurrencyRatio(orgID, self.serverRequestID))
    
    def getSegments(self, orgID):       
        Logger.log('orgID: ', orgID,' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.getSegments(orgID, self.serverRequestID))
       
    def getSegmentWithValues(self, orgID, segmentName):       
        Logger.log('orgID: ', orgID,' segmentName: ',segmentName, ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.getSegmentWithValues(orgID, self.serverRequestID))
       
    def bulkRedeemPoints(self, pointsRedemptionOrgData):       
        Logger.log('pointsRedemptionOrgData: ',pointsRedemptionOrgData, ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.bulkRedeemPoints(orgID, self.serverRequestID))
    
    def allocateGoodwillPoints(self, goodwillPointsData):       
        Logger.log('goodwillPointsData: ',goodwillPointsData, ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.allocateGoodwillPoints(orgID, self.serverRequestID))
    
    def mergeCustomers(self, orgID, fromCustomerId, toCustomerId, mergedbyTillId):       
        Logger.log('orgID: ',orgID, ' fromCustomerId:', fromCustomerId,' toCustomerId: ',toCustomerId,' mergedbyTillId: ',mergedbyTillId, ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.mergeCustomers(orgID, fromCustomerId, toCustomerId, mergedbyTillId, self.serverRequestID))

    def getMergeStatus(self, orgID, fromCustomerId, toCustomerId):       
        Logger.log('orgID: ',orgID, ' fromCustomerId:', fromCustomerId,' toCustomerId: ',toCustomerId, ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.getMergeStatus(orgID, fromCustomerId, toCustomerId, self.serverRequestID))

    def getPointsRedemptionSummaryForCustomer(self, orgID, customerId, includePointsDeductions):       
        Logger.log('orgID: ',orgID, ' customerId:', customerId,' includePointsDeductions: ',includePointsDeductions, ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.getPointsRedemptionSummaryForCustomer(orgID, customerId, includePointsDeductions, self.serverRequestID))

    def getAllPointsRedemptionSummaryForCustomer(self, customerFilter, includePointsDeductions):       
        Logger.log('customerFilter: ',customerFilter, ' includePointsDeductions:', includePointsDeductions, ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.getAllPointsRedemptionSummaryForCustomer(orgID, customerFilter, includePointsDeductions, self.serverRequestID))

    def getPointsRedemptionSummaryForCustomerFiltered(self, orgID, customerId, pointsRedemptionFilterParams):       
        Logger.log('orgID: ',orgID, ' customerId:', customerId,' pointsRedemptionFilterParams: ',pointsRedemptionFilterParams, ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.getPointsRedemptionSummaryForCustomerFiltered(orgID, startDate, endDate, self.serverRequestID))

    def getAllPointsRedemptionSummaryForCustomerFiltered(self, customerFilter, pointsRedemptionFilterParams):       
        Logger.log('customerFilter: ',customerFilter, ' pointsRedemptionFilterParams:', pointsRedemptionFilterParams, ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.getAllPointsRedemptionSummaryForCustomerFiltered(orgID, customerFilter, includePointsDeductions, self.serverRequestID))

    def clearCustomerDataCache(self, orgId):       
        Logger.log('orgId: ',orgId, ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.clearCustomerDataCache(orgID, self.serverRequestID))
 
    def renewCustomerSlab(self, renewCustomerSlabData, renewedBy):       
        Logger.log('renewCustomerSlabData: ',renewCustomerSlabData, ' renewedBy:', renewedBy, ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.renewCustomerSlab(renewCustomerSlabData, renewedBy, self.serverRequestID))

    def getTierDowngradeStatus(self, orgId):       
        Logger.log('orgId: ',orgId, ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.getTierDowngradeStatus(orgID, self.serverRequestID))

    def getTierDowngradeStatusByFilter(self, programFilter):       
        Logger.log('programFilter: ',programFilter, ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.getTierDowngradeStatusByFilter(orgID, self.serverRequestID))

    def getTierDowngradeRetentionCriteria(self, orgId, customerId):       
        Logger.log('orgId: ',orgId, ' customerId:', customerId, ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.getTierDowngradeRetentionCriteria(orgId, customerId, self.serverRequestID))

    def getAllTierDowngradeRetentionCriteria(self, customerFilter):       
        Logger.log('customerFilter: ',customerFilter, ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.getAllTierDowngradeRetentionCriteria(orgID, self.serverRequestID))

    def getTierUpgradeCriteria(self, orgId, customerId):       
        Logger.log('orgId: ',orgId, ' customerId:', customerId, ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.getTierUpgradeCriteria(orgId, customerId, self.serverRequestID))
 
    def getAllTierUpgradeCriteria(self, customerFilter):       
        Logger.log('customerFilter: ',customerFilter, ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.getAllTierUpgradeCriteria(orgID, self.serverRequestID))

    def getTrackedData(self, request):       
        Logger.log('request: ',request, ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.getTrackedData(orgID, self.serverRequestID))

    def updateRedemptionBillDetails(self, prs):       
        Logger.log('prs: ',prs, ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.updateRedemptionBillDetails(orgID, self.serverRequestID))  

    def getProgramIdsForTills(self, orgId, tills):       
        Logger.log('orgId: ',orgId, ' tills:', tills, ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.getProgramIdsForTills(orgId, tills, self.serverRequestID))
    
    def validate(self, config):       
        Logger.log('config: ',config, ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.validate(orgID, self.serverRequestID))
 
