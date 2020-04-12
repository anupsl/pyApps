from src.Constant.constant import constant
from src.initializer.generateThrift import peb
from src.utilities.logger import Logger
from thriftpy.rpc import make_client
import random


class PEBThrift(object):

    def __init__(self, port, timeout=60000):
        self.conn = make_client(peb.PEBService, '127.0.0.1', port, timeout=timeout)
        self.getServerRequestID()

    def getServerRequestID(self):    
        self.serverRequestID = 'peb_auto_'+str(random.randint(11111, 99999))

    def close(self):
        Logger.log('Closing PEBThrift connection')
        self.conn.close()

    def log(self, output):
        Logger.log(output)
        return output

    def isAlive(self):
        return self.log(self.conn.isAlive())

    # Reminder Service
    def alertBulkPointsExpiryReminder(alertBeforeDays): # queued
        Logger.log('alertBeforeDays: ',alertBeforeDays, ' serverRequestID:', self.serverRequestID)
        return self.log(self.conn.alertBulkPointsExpiryReminder(alertBeforeDays, self.serverRequestID))

    def getPointsExpiryRemindersInfo(self, orgID, startDate, endDate):
        Logger.log('orgID: ',orgID, ' startDate: ', startDate, ' endDate: ', endDate, ' serverRequestID:', self.serverRequestID)
        return self.log(self.conn.getPointsExpiryRemindersInfo(orgID, startDate, endDate, self.serverRequestID))

    def getPointsExpiryRemindersSentInfo(self, orgID, startDate, endDate):
        Logger.log('orgID: ',orgID, ' startDate: ', startDate, ' endDate: ', endDate, ' serverRequestID:', self.serverRequestID)
        return self.log(self.conn.getPointsExpiryRemindersSentInfo(orgID, startDate, endDate, self.serverRequestID))

    def sendBulkReminderMessageForAllPrograms(self): # queued
        Logger.log('serverRequestID:', self.serverRequestID)
        return self.log(self.conn.sendBulkReminderMessageForAllPrograms(self.serverRequestID))

    def sendBulkReminderMessageForProgram(self, programId, orgId):
        Logger.log('programId: ', programId, ' orgId: ', orgId, ' serverRequestID:', self.serverRequestID)
        return self.log(self.conn.sendBulkReminderMessageForProgram(programId, orgId, self.serverRequestID))


    # Expiry Service
    def getBulkPointsExpirySchedule(self, bulkExpiryReportData):
        Logger.log('programId: ', bulkExpiryReportData, ' serverRequestID:', self.serverRequestID)
        return self.log(self.conn.getBulkPointsExpirySchedule(bulkExpiryReportData, self.serverRequestID))

    def getBulkPointsExpired(self, bulkExpiryReportData):
        Logger.log('bulkExpiryReportData: ', bulkExpiryReportData, ' serverRequestID:', self.serverRequestID)
        return self.log(self.conn.getBulkPointsExpired(self.serverRequestID))        

    def getPointsExpiryScheduleForCustomer(self, orgID, customerId):
        Logger.log('orgID: ', orgID, ' customerId: ',customerId, ' serverRequestID:', self.serverRequestID)
        return self.log(self.conn.getPointsExpiryScheduleForCustomer(orgID, customerId, self.serverRequestID))  

    def getPointsExpiryDetailsOnDate(self, orgID, date):
        Logger.log('orgID: ', orgID, ' date: ', date, ' serverRequestID:', self.serverRequestID)
        return self.log(self.conn.getPointsExpiryDetailsOnDate(orgID, date, self.serverRequestID))          

    def getPointsExpiryDetailsForCustomerOnDate(self, orgID, customerId, date):
        Logger.log('orgID: ', orgID,' customerId: ',customerId, ' date: ', date, ' serverRequestID:', self.serverRequestID)
        return self.log(self.conn.getPointsExpiryDetailsForCustomerOnDate(orgID, customerId, date, self.serverRequestID))          

    def bulkExpirePointsAsOnDateForAllPrograms(self, date): # queued
        Logger.log('date: ', date, ' serverRequestID:', self.serverRequestID)
        return self.log(self.conn.bulkExpirePointsAsOnDateForAllPrograms(date, self.serverRequestID))  


    ## Health Dashboard 
    def getPointsExpiryInfo(self, orgID, startDate, endDate):
        Logger.log('orgID: ', orgID,' startDate: ',startDate, ' endDate: ', endDate, ' serverRequestID:', self.serverRequestID)
        return self.log(self.conn.getPointsExpiryInfo(orgID, startDate, endDate, self.serverRequestID))          

    def getPointsExpiredInfo(self, orgID, startDate, endDate):
        Logger.log('orgID: ', orgID,' startDate: ',startDate, ' endDate: ', endDate, ' serverRequestID:', self.serverRequestID)
        return self.log(self.conn.getPointsExpiredInfo(orgID, startDate, endDate, self.serverRequestID))          

    def getPromotionExpiryInfo(self, orgID, startDate, endDate):
        Logger.log('orgID: ', orgID,' startDate: ',startDate, ' endDate: ', endDate, ' serverRequestID:', self.serverRequestID)
        return self.log(self.conn.getPromotionExpiryInfo(orgID, startDate, endDate, self.serverRequestID))          



    def executeTierDowngrade(self): # queued
        Logger.log('serverRequestID:', self.serverRequestID)
        return self.log(self.conn.executeTierDowngrade(self.serverRequestID))

    def executeTierDowngradeAtTime(self, runningDate): # queued
        Logger.log('serverRequestID:', self.serverRequestID, ' runningDate: ', runningDate)
        return self.log(self.conn.executeTierDowngradeAtTime(self.serverRequestID, runningDate))

    def executeTierDowngradeForOrg(self, orgID, sendReminder, execute):
        Logger.log('serverRequestID:', self.serverRequestID, ' orgID: ', orgID,' sendReminder: ',sendReminder, ' execute: ', execute)
        return self.log(self.conn.executeTierDowngradeForOrg(self.serverRequestID, orgID, sendReminder, execute))          
     
    def executeTierDowngradeForOrgAtTime(self, orgID, runningTime, sendReminder, execute):
        Logger.log('serverRequestID:', self.serverRequestID, ' orgID: ', orgID,' runningTime: ',runningTime,' sendReminder: ',sendReminder, ' execute: ', execute)
        return self.log(self.conn.executeTierDowngradeForOrgAtTime(self.serverRequestID, orgID, runningTime, sendReminder, execute))          

     
    ## Merge customers

    def mergeCustomers(self, orgID, fromCustomerId, toCustomerId, mergedbyTillId):
        Logger.log('orgID: ', orgID,' fromCustomerId: ',fromCustomerId,' toCustomerId: ',toCustomerId, ' mergedbyTillId: ', mergedbyTillId, ' serverRequestID:', self.serverRequestID)
        return self.log(self.conn.mergeCustomers(orgID, fromCustomerId, toCustomerId, mergedbyTillId, self.serverRequestID))          

    def getMergeStatus(self, orgID, fromCustomerId, toCustomerId):
        Logger.log('orgID: ', orgID,' fromCustomerId: ',fromCustomerId,' toCustomerId: ',toCustomerId, ' serverRequestID:', self.serverRequestID)
        return self.log(self.conn.getMergeStatus(orgID, fromCustomerId, toCustomerId, self.serverRequestID))          

    ## Imports data
    def importCustomerSlab(self, importData):
        Logger.log('importData: ', importData,' serverRequestID:', self.serverRequestID)
        return self.log(self.conn.importCustomerSlab(importData, self.serverRequestID))          

    def importCustomerForNonDefaultProgram(self, importData):
        Logger.log('importData: ', importData,' serverRequestID:', self.serverRequestID)
        return self.log(self.conn.importCustomerForNonDefaultProgram(importData, self.serverRequestID)) 

    def importTransactionForNonDefaultProgram(self, importData):
        Logger.log('importData: ', importData,' serverRequestID:', self.serverRequestID)
        return self.log(self.conn.importTransactionForNonDefaultProgram(importData, self.serverRequestID)) 



    def extendTierExpiryDate(self, tierExtensionData):
        Logger.log('tierExtensionData: ', tierExtensionData,' serverRequestID:', self.serverRequestID)
        return self.log(self.conn.extendTierExpiryDate(tierExtensionData, self.serverRequestID)) 

    def bulkAllocatePoints(self, bulkAllocatePoints):
        Logger.log('bulkAllocatePoints: ', bulkAllocatePoints,' serverRequestID:', self.serverRequestID)
        return self.log(self.conn.bulkAllocatePoints(bulkAllocatePoints, self.serverRequestID)) 

    def getPromotionData(self, promotionRequestList, pointsAwardedStartDateInMillis, pointsAwardedEndDateInMillis):
        Logger.log('promotionRequestList: ', promotionRequestList,' pointsAwardedStartDateInMillis: ',pointsAwardedStartDateInMillis,' serverRequestID:',' pointsAwardedEndDateInMillis: ',pointsAwardedEndDateInMillis, self.serverRequestID)
        return self.log(self.conn.getPromotionData(bulkAllocatePoints, pointsAwardedStartDateInMillis, pointsAwardedEndDateInMillis, self.serverRequestID)) 

    def getCustomerPointsSummariesByProgram(self, customersData):
        Logger.log('customersData: ', customersData,' serverRequestID:', self.serverRequestID)
        return self.log(self.conn.getCustomerPointsSummariesByProgram(customersData, self.serverRequestID))

    # Delayed Accrual
    def bulkDelayedAccrualToRedeemablePoints(self, date):
        Logger.log('Date: ', date, ' serverRequestID:', self.serverRequestID)
        return self.log(self.conn.bulkDelayedAccrualToRedeemablePoints(date, self.serverRequestID))

    def bulkDelayedAccrualToRedeemablePointsByOrgId(self, orgId, date):
        Logger.log('orgId: ', orgId, ' date: ', date, ' serverRequestID:', self.serverRequestID)
        return self.log(self.conn.bulkDelayedAccrualToRedeemablePointsByOrgId(orgId, date, self.serverRequestID))

    def executeDowngradeOnReturnForOrgAtTime(self, orgId, runningTime, execute = True):
        Logger.log('orgId: {}, runningTime: {}, Execute: {}, serverRequestId: {}'.format(orgId, runningTime, execute, self.serverRequestID))
        return self.log(self.conn.executeDowngradeOnReturnForOrgAtTime(self.serverRequestID,orgId, runningTime, execute))

