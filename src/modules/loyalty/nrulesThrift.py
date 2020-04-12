from src.Constant.constant import constant
from src.initializer.generateThrift import nrules
from src.utilities.logger import Logger
from thriftpy.rpc import make_client
import random


class NrulesThrift(object):

    def __init__(self, port, timeout=60000):
        self.conn = make_client(nrules.RuleConfigService, '127.0.0.1', port, timeout=timeout)
        self.getServerRequestID()

    def getServerRequestID(self):
        self.serverRequestID = 'nrules_'+str(random.randint(11111, 99999))

    def close(self):
        Logger.log('Closing NrulesThrift connection')
        self.conn.close()
        
    def log(self, output):
        Logger.log(output)
        return output

    def reconfigureOrganization(self, orgID, userID, endpointName, contextId):       
        Logger.log('orgID: ',orgID, ' userID:', userID,' endpointName: ',endpointName,' contextId: ',contextId, ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.reconfigureOrganization(orgID, userID, endpointName, contextId, self.serverRequestID))

    def getAvailableFilterTypes(self, endpointName):       
        Logger.log('endpointName: ',endpointName, ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.getAvailableFilterTypes(endpointName, self.serverRequestID))

    def getFilterTemplate(self, orgID, filterType, endpointName):       
        Logger.log('orgID: ',orgID, ' filterType:', filterType,' endpointName: ',endpointName, ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.getFilterTemplate(orgID, filterType, endpointName, self.serverRequestID))

    def validateExpression(self, orgID, ruleExpression, ruleExpJSON, endpointName):       
        Logger.log('orgID: ',orgID, ' ruleExpression:', ruleExpression,' ruleExpJSON: ',ruleExpJSON,' endpointName: ',endpointName, ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.validateExpression(orgID, ruleExpression, ruleExpJSON, endpointName, self.serverRequestID))

    def getConfigurableActions(self, orgID, endpointName):       
        Logger.log('orgID: ',orgID, ' endpointName: ',endpointName, ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.getConfigurableActions(orgID, endpointName, self.serverRequestID))

    def getConfiguredRulesetsByContextId(self, orgID, isPrivate, endpointName, contextId):       
        Logger.log('orgID: ',orgID, ' isPrivate:', isPrivate,' endpointName: ',endpointName, ' contextId: ',contextId, ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.getConfiguredRulesetsByContextId(orgID, isPrivate, endpointName, contextId, self.serverRequestID))

    def getConfiguredRulesets(self, orgID, isPrivate, endpointName):       
        Logger.log('orgID: ',orgID, ' isPrivate:', isPrivate,' endpointName: ',endpointName, ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.getConfiguredRulesets(orgID, isPrivate, endpointName, self.serverRequestID))

    def getConfiguredRulesetsByEventType(self, orgID, eventType, endpointName):       
        Logger.log('orgID: ',orgID, ' eventType:', eventType,' endpointName: ',endpointName, ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.getConfiguredRulesetsByEventType(orgID, eventType, endpointName, self.serverRequestID))

    def searchRulesetById(self, orgID, rulesetID, endpointName):       
        Logger.log('orgID: ',orgID, ' rulesetID:', rulesetID,' endpointName: ',endpointName, ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.searchRulesetById(orgID, rulesetID, endpointName, self.serverRequestID))


    def searchRulesetsByNamePattern(self, orgID, rulesetNamePattern, endpointName):       
        Logger.log('orgID: ',orgID, ' rulesetNamePattern:', rulesetNamePattern,' endpointName: ',endpointName, ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.searchRulesetsByNamePattern(orgID, rulesetNamePattern, endpointName, self.serverRequestID))

    def searchRulesetsByFacts(self, orgID, factNameRegex, endpointName):       
        Logger.log('orgID: ',orgID, ' factNameRegex:', factNameRegex,' endpointName: ',endpointName, ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.searchRulesetsByFacts(orgID, factNameRegex, endpointName, self.serverRequestID))

    def searchRulesetsByPackages(self, orgID, packageNameRegex, endpointName):       
        Logger.log('orgID: ',orgID, ' packageNameRegex:', packageNameRegex,' endpointName: ',endpointName, ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.searchRulesetsByPackages(orgID, packageNameRegex, endpointName, self.serverRequestID))

    def createNewRuleset(self, orgID, name, rulesetInfo, eventName, endpointName):       
        Logger.log('orgID: ',orgID, ' name:', name,' rulesetInfo: ',rulesetInfo, ' eventName: ',eventName, ' endpointName:', endpointName, ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.createNewRuleset(orgID, name, rulesetInfo, eventName, endpointName, self.serverRequestID))

    def editRuleset(self, orgID, name, rulesetInfo, endpointName):       
        Logger.log('orgID: ',orgID, ' name:', name,' rulesetInfo: ',rulesetInfo, ' endpointName:', endpointName, ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.editRuleset(orgID, name, rulesetInfo, endpointName, self.serverRequestID))

    def addRule(self, orgID, rulesetID, ruleInfo, endpointName):       
        Logger.log('orgID: ',orgID, ' rulesetID:', rulesetID,' ruleInfo: ',ruleInfo, ' endpointName:', endpointName, ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.addRule(orgID, rulesetID, ruleInfo, endpointName, self.serverRequestID))

    def changeExpression(self, orgID, rulesetName, ruleIndex, ruleExpression, ruleExpJSON, endpointName, lastModifiedBy):       
        Logger.log('orgID: ',orgID, ' rulesetName:', rulesetName,' ruleIndex: ',ruleIndex, ' ruleExpression:', ruleExpression, ' ruleExpJSON: ',ruleExpJSON, ' endpointName: ',endpointName, ' lastModifiedBy: ',lastModifiedBy, ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.changeExpression(orgID, rulesetName, ruleIndex, ruleExpression, ruleExpJSON, endpointName, lastModifiedBy, self.serverRequestID))

    def updateRulesetStatus(self, orgID, rulesetID, status, endpointName, lastModifiedBy):       
        Logger.log('orgID: ',orgID, ' rulesetID:', rulesetID,' status: ',status, ' endpointName:', endpointName, ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.updateRulesetStatus(orgID, rulesetID, status, endpointName, lastModifiedBy, self.serverRequestID))

    def updateRuleStatus(self, orgID, ruleID, status, priority, endpointName, lastModifiedBy):       
        Logger.log('orgID: ',orgID, ' ruleID:', ruleID,' status: ',status,' priority: ',priority, ' endpointName:', endpointName, ' lastModifiedBy: ',lastModifiedBy, ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.updateRuleStatus(orgID, ruleID, status, priority, endpointName, lastModifiedBy, self.serverRequestID))

    def getRulesetExpiryInfo(self, orgID, startDate, endDate, endpointName):       
        Logger.log('orgID: ',orgID, ' startDate:', startDate,' endDate: ',endDate, ' endpointName:', endpointName, ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.getRulesetExpiryInfo(orgID, startDate, endDate, endpointName, self.serverRequestID))
 
    def searchRuleById(self, ruleID, orgID, endpointName):       
        Logger.log('ruleID: ',ruleID,' orgID: ',orgID, ' endpointName:', endpointName, ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.searchRuleById(ruleID, orgID, endpointName, self.serverRequestID))

    def editRule(self, orgID, ruleInfo, endpointName):       
        Logger.log('orgID: ',orgID,' ruleInfo: ',ruleInfo, ' endpointName:', endpointName, ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.editRule(orgID, ruleInfo, endpointName, self.serverRequestID))
      
    def updateRulesetDates(self, orgID, rulesetID, startDate, endDate, endpointName, lastModifiedBy):       
        Logger.log('orgID: ',orgID, ' rulesetID:', rulesetID,' startDate: ',startDate,' endDate: ',endDate, ' endpointName:', endpointName, ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.updateRulesetDates(orgID, rulesetID, startDate, endDate, endpointName, lastModifiedBy, self.serverRequestID))

    def updateRulesPriority(self, orgID, ruleToPriorityMap, endpointName, lastModifiedBy):       
        Logger.log('orgID: ',orgID,' ruleToPriorityMap: ',ruleToPriorityMap, ' endpointName:', endpointName, ' lastModifiedBy: ',lastModifiedBy, ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.updateRulesPriority(orgID, ruleToPriorityMap, endpointName, lastModifiedBy, self.serverRequestID))
     
    def editOrgConfigFilters(self, orgID, contextId, filters):       
        Logger.log('orgID: ',orgID,' contextId: ',contextId, ' filters:', filters, ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.editOrgConfigFilters(orgID, ruleInfo, filters, self.serverRequestID))
           
    def getOrgConfigFilters(self, orgConfigFilterRequest):       
        Logger.log('orgConfigFilterRequest: ',orgConfigFilterRequest,' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.getOrgConfigFilters(orgConfigFilterRequest, self.serverRequestID))
           

