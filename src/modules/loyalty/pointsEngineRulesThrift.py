from src.Constant.constant import constant
from src.initializer.generateThrift import pointsEngineRules
from src.utilities.logger import Logger
from thriftpy.rpc import make_client
import random


class PointsEngineRulesThrift(object):

    def __init__(self, port, timeout=60000):
        self.conn = make_client(pointsEngineRules.PointsEngineRuleService, '127.0.0.1', port, timeout=timeout)
        self.getServerRequestID()

    def getServerRequestID(self):
        self.serverRequestID = 'pe_rules_auto_'+str(random.randint(11111, 99999))

    def close(self):
        Logger.log('Closing PointsEngineRulesThrift connection')
        self.conn.close()

    def log(self, output):
        Logger.log(output)
        return output

    def isAlive(self):
        return self.log(self.conn.isAlive())

    def getProgramByTill(self, programFilter, customerId):       
        Logger.log('programFilter: ',programFilter, ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.getProgramByTill(programFilter, self.serverRequestID))

    def createOrUpdatePointsCategory(self, pointsCategory):       
        Logger.log('pointsCategory: ',pointsCategory, ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.createOrUpdatePointsCategory(pointsCategory, self.serverRequestID))

    def getPointsCategory(self, orgID, programId, categoryId):       
        Logger.log('orgID: ',orgID, ' programId:', programId,' categoryId: ',categoryId, ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.getPointsCategory(orgID, programId, self.serverRequestID))

    def createOrUpdateTrackerCondition(self, trackerCondition):       
        Logger.log('trackerCondition: ',trackerCondition, ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.createOrUpdateTrackerCondition(orgID, customerId, self.serverRequestID))    

    def getTrackerConditionForTrackerStrategy(self, orgID, programId, strategyId):       
        Logger.log('orgID: ',orgID, ' programId:', programId, ' strategyId: ',strategyId, ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.getTrackerConditionForTrackerStrategy(orgID, programId, self.serverRequestID))

    def getAllSlabs(self, programId, orgID):       
        Logger.log('programId: ',programId,' orgID: ',orgID, ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.getAllSlabs(programId, orgID, self.serverRequestID))

    def getAllConfiguredStrategies(self, programId, orgID):       
        Logger.log('programId: ',programId,' orgID: ',orgID, ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.getAllConfiguredStrategies(programId, orgID, self.serverRequestID))
    
    def getAllStrategiesByStrategyTypeId(self, programId, orgID, strategyTypeId):       
        Logger.log('programId: ',programId,' orgID: ',orgID, ' strategyTypeId: ',strategyTypeId, ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.getAllStrategiesByStrategyTypeId(programId, orgID, strategyTypeId, self.serverRequestID))  

    def getStrategy(self, strategyId, programId, orgID):       
        Logger.log('strategyId: ',strategyId,' programId: ',programId,' orgID: ',orgID, ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.getStrategy(strategyId, programId, orgID, self.serverRequestID))

    def createOrUpdateStrategy(self, strategyInfo, programId, orgId, lastModifiedBy, lastModifiedOn):       
        Logger.log('strategyInfo: ',strategyInfo,' programId: ',programId,' orgId: ',orgId,' lastModifiedBy: ',lastModifiedBy,' lastModifiedOn: ',lastModifiedOn, ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.createOrUpdateStrategy(strategyInfo, programId, orgId, lastModifiedBy, lastModifiedOn, self.serverRequestID))

    def createSlabAndUpdateStrategies(self, programId, orgId, slabInfo, strategyInfos, lastModifiedBy, lastModifiedOn):       
        Logger.log('programId: ',programId,' orgId: ',orgId,' slabInfo: ',slabInfo, ' strategyInfos: ',strategyInfos,' lastModifiedBy: ',lastModifiedBy,' lastModifiedOn: ',lastModifiedOn, ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.createSlabAndUpdateStrategies(strategyInfo, programId, orgId, slabInfo, strategyInfos, lastModifiedBy, lastModifiedOn, self.serverRequestID))

    def getPromotionsByProgramId(self, programId, orgId):       
        Logger.log('programId: ',programId,' orgId: ',orgId, ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.getPromotionsByProgramId(programId, orgId, self.serverRequestID))

    def getPromotionsByRulesetName(self, programId, orgId, rulesetName):       
        Logger.log('programId: ',programId,' orgId: ',orgId, ' rulesetName: ',rulesetName, ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.getPromotionsByRulesetName(programId, orgId, rulesetName, self.serverRequestID))

    def getPromotionsByProgramAndEventType(self, programId, orgId, eventTypeId):       
        Logger.log('programId: ',programId,' orgId: ',orgId, ' eventTypeId: ',eventTypeId, ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.getPromotionsByProgramAndEventType(programId, orgId, eventTypeId, self.serverRequestID))

    def getPromotion(self, promotionId, programId, orgId):       
        Logger.log('promotionId: ',promotionId,' programId: ',programId,' orgId: ',orgId, ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.getPromotion(promotionId, programId, orgId, self.serverRequestID))

    def createOrUpdatePromotion(self, promotionInfo, programId, orgId, lastModifiedBy, lastModifiedOn):       
        Logger.log(' promotionInfo: ',promotionInfo,' programId: ',programId,' orgId: ',orgId,' lastModifiedBy: ',lastModifiedBy,' lastModifiedOn: ',lastModifiedOn, ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.createOrUpdatePromotion(promotionInfo, programId, orgId, lastModifiedBy, lastModifiedOn, self.serverRequestID))

    def getAllEvents(self):       
        Logger.log('serverReqId: ',self.serverRequestID)
        return self.log(self.conn.getAllEvents(self.serverRequestID))

    def getStrategyTypes(self):       
        Logger.log('serverReqId: ',self.serverRequestID)
        return self.log(self.conn.getStrategyTypes(self.serverRequestID))

    def getProgramId(self, orgID):       
        Logger.log('orgID: ',orgID, ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.getProgramId(orgID, self.serverRequestID))

    def updateProgram(self, program, orgId, lastModifiedBy, lastModifiedOn):       
        Logger.log(' program: ',program,' orgId: ',orgId,' lastModifiedBy: ',lastModifiedBy,' lastModifiedOn: ',lastModifiedOn, ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.updateProgram(promotionInfo, orgId, lastModifiedBy, lastModifiedOn, self.serverRequestID))

    def createOrUpdateSlab(self, slabInfo, orgId, lastModifiedBy, lastModifiedOn):       
        Logger.log(' slabInfo: ',slabInfo,' orgId: ',orgId,' lastModifiedBy: ',lastModifiedBy,' lastModifiedOn: ',lastModifiedOn, ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.createOrUpdateSlab(slabInfo, orgId, lastModifiedBy, lastModifiedOn, self.serverRequestID))

    def getProgram(self, programId, orgId):       
        Logger.log('programId: ',programId,' orgId: ',orgId, ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.getProgram(programId, orgId, self.serverRequestID))

    def getAllPrograms(self, orgId):       
        Logger.log('orgId: ',orgId, ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.getProgram(orgId, self.serverRequestID))

    def rolloutNewUI(self, orgId):       
        Logger.log('orgId: ',orgId, ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.rolloutNewUI(orgId, self.serverRequestID))

        ##  Tender combinations      

    def getTenderCombination(self, orgId, tenderCombinationId):       
        Logger.log('orgId: ',orgId,' tenderCombinationId: ',tenderCombinationId, ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.getTenderCombination(orgId, tenderCombinationId, self.serverRequestID))

    def getAllTenderCombinations(self, programId, orgId):       
        Logger.log('programId: ',programId,' orgId: ',orgId, ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.getAllTenderCombinations(programId, orgId, self.serverRequestID))

    def createTenderCombination(self, orgId, tenderCombinationId):       
        Logger.log('orgId: ',orgId,' tenderCombinationId: ',tenderCombinationId, ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.createTenderCombination(orgId, tenderCombinationId, self.serverRequestID))

    def editTenderCombination(self, orgId, tenderCombinationId):       
        Logger.log('orgId: ',orgId,' tenderCombinationId: ',tenderCombinationId, ' serverReqId: ',self.serverRequestID)
        return self.log(self.conn.editTenderCombination(orgId, tenderCombinationId, self.serverRequestID))

