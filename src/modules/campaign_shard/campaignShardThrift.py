from src.Constant.constant import constant
from src.initializer.generateThrift import campaignShard
from src.utilities.logger import Logger
from thriftpy.rpc import make_client
import random

class CampaignShardThrift(object):
    def __init__(self, port, timeout=2000000):
        self.conn = make_client(campaignShard.CampaignShardService, '127.0.0.1', port, timeout=timeout)
        self.connAudienceGroupManager = make_client(campaignShard.AudienceGroupManagerService, '127.0.0.1', port, timeout=timeout)
        self.getServerRequestID()

    def close(self):
        Logger.log('Closing campaign-shard thrift connection')
        self.conn.close()
        self.connAudienceGroupManager.close()

    def getServerRequestID(self):
        self.serverRequestID = 'campaignShard_auto_' + str(random.randint(11111, 99999))

    def log(self, output):
        Logger.log(output)
        return output

    def isAlive(self):
        return self.log(self.conn.isAlive())    
 
    def getAudienceGroupById(self, groupId, reachabilityDetails):
        Logger.log('Params - groupId:', groupId, 'orgId :', constant.config['orgId'], 'reachabilityDetails :', reachabilityDetails, ' serverRequestID:', self.serverRequestID)
        return self.log(self.connAudienceGroupManager.getAudienceGroupById(int(groupId), int(constant.config['orgId']), bool(reachabilityDetails), self.serverRequestID))

    def createGroupRecipients(self,thriftCampaignGroup):
        Logger.log('Params - thriftCampaignGroup :{} , serviceRequestId :{}'.format(thriftCampaignGroup,self.serverRequestID))
        return self.log(self.conn.createGroupRecipients(thriftCampaignGroup, self.serverRequestID))

    def getAudienceGroupByUuId(self, uuId, reachabilityDetails):
        Logger.log('Params - uuId:', uuId, 'orgId :', constant.config['orgId'], 'reachabilityDetails :', reachabilityDetails, ' serverRequestID:', self.serverRequestID)
        return self.log(self.connAudienceGroupManager.getAudienceGroupByUuId(str(uuId), int(constant.config['orgId']), bool(reachabilityDetails), self.serverRequestID))

    def getAudienceGroupVersion(self, groupVersionId):
        Logger.log('Params - groupVersionId:', groupVersionId, 'orgId :', constant.config['orgId'], ' serverRequestID:', self.serverRequestID)
        return self.log(self.connAudienceGroupManager.getAudienceGroupVersion(int(groupVersionId), int(constant.config['orgId']), self.serverRequestID))

    def getAllAudienceGroupByGroupIds(self, groupIds):
        Logger.log('Params - groupIds:', groupIds, 'orgId :', constant.config['orgId'], ' serverRequestID:', self.serverRequestID)
        return self.log(self.connAudienceGroupManager.getAllAudienceGroupByGroupIds((groupIds), int(constant.config['orgId']), self.serverRequestID))

    def getAllAudienceGroupByUuIds(self, uuIds):
        Logger.log('Params - uuIds:', uuIds, 'orgId :', constant.config['orgId'], ' serverRequestID:', self.serverRequestID)
        return self.log(self.connAudienceGroupManager.getAllAudienceGroupByUuIds((uuIds), int(constant.config['orgId']), self.serverRequestID))

    def searchAudienceGroup(self, audienceGroupTypes):
        Logger.log('Params - audienceGroupTypes:', audienceGroupTypes, 'orgId :', constant.config['orgId'], ' serverRequestID:', self.serverRequestID)
        return self.log(self.connAudienceGroupManager.searchAudienceGroup(int(constant.config['orgId']), (audienceGroupTypes), self.serverRequestID))

    def searchAudienceGroupByLabel(self, groupLabel, audienceGroupTypes):
        Logger.log('Params - audienceGroupTypes:', audienceGroupTypes, 'orgId :', constant.config['orgId'], 'groupLabel :', groupLabel, ' serverRequestID:', self.serverRequestID)
        return self.log(self.connAudienceGroupManager.searchAudienceGroupByLabel(constant.config['orgId'], str(groupLabel), audienceGroupTypes , self.serverRequestID))
    
    def newSearchAudienceGroup(self, audienceSearchRequest):
        Logger.log('Params - audienceSearchRequest:', audienceSearchRequest, 'orgId :', constant.config['orgId'], ' serverRequestID:', self.serverRequestID)
        return self.log(self.connAudienceGroupManager.newSearchAudienceGroup(int(constant.config['orgId']), audienceSearchRequest, self.serverRequestID))

    def newSearchAudienceGroupByLabel(self, audienceSearchRequest):
        Logger.log('Params - audienceSearchRequest:', audienceSearchRequest, 'orgId :', constant.config['orgId'], ' serverRequestID:', self.serverRequestID)
        return self.log(self.connAudienceGroupManager.newSearchAudienceGroupByLabel(constant.config['orgId'],audienceSearchRequest , self.serverRequestID))

    def searchAudienceGroupByCampaign(self, groupLabel, audienceGroupTypes, campaignId):
        Logger.log('Params - audienceGroupTypes:', audienceGroupTypes, 'orgId :', constant.config['orgId'], 'groupLabel :', groupLabel, 'campaignId :', campaignId, ' serverRequestID:', self.serverRequestID)
        return self.log(self.connAudienceGroupManager.searchAudienceGroupByCampaign(int(constant.config['orgId']), audienceGroupTypes, str(groupLabel), int(campaignId), self.serverRequestID))

    def subscribe(self, eventName, groupId, entityName, entityId, params, updatedBy):
        Logger.log('Params - eventName:', eventName, 'orgId :', constant.config['orgId'], 'eventName :', eventName, 'groupId :', groupId, 'entityName :', entityName, 'entityId :', entityId, 'params :', params, 'updatedBy :', updatedBy, ' serverRequestID:', self.serverRequestID)
        return self.log(self.connAudienceGroupManager.subscribe(eventName, int(constant.config['orgId']), int(groupId), str(entityName), str(entityId), str(params), int(updatedBy), self.serverRequestID))

    def unsubscribe(self, eventName, groupId, entityName, entityId, updatedBy):
        Logger.log('Params - eventName:', eventName, 'orgId :', constant.config['orgId'], 'eventName :', eventName, 'groupId :', groupId, 'entityName :', entityName, 'entityId :', entityId, 'updatedBy :', updatedBy, ' serverRequestID:', self.serverRequestID)
        return self.log(self.connAudienceGroupManager.unsubscribe((eventName), int(constant.config['orgId']), int(groupId), str(entityName), str(entityId), int(updatedBy), self.serverRequestID))

    def getAudienceGroupS3Info(self, groupId, versionNumber):
        Logger.log('Params - groupId:', groupId, 'orgId :', constant.config['orgId'], 'versionNumber :', versionNumber, ' serverRequestID:', self.serverRequestID)
        return self.log(self.connAudienceGroupManager.getAudienceGroupS3Info(int(constant.config['orgId']),int(groupId), int(versionNumber), self.serverRequestID))

    def getChangeSetForAudienceGroup(self, groupId, fromVersionNumber):
        Logger.log('Params - groupId:', groupId, 'orgId :', constant.config['orgId'], 'fromVersionNumber :', fromVersionNumber, ' serverRequestID:', self.serverRequestID)
        return self.log(self.connAudienceGroupManager.getChangeSetForAudienceGroup(int(groupId), int(constant.config['orgId']), int(fromVersionNumber), self.serverRequestID))

    def getAudienceGroupWithDataSourceInfo(self, audienceGroupDataSourceInfoRequest):
        Logger.log('Params - audienceGroupDataSourceInfoRequest:', audienceGroupDataSourceInfoRequest, ' serverRequestID:', self.serverRequestID)
        return self.log(self.connAudienceGroupManager.getAudienceGroupWithDataSourceInfo(audienceGroupDataSourceInfoRequest, self.serverRequestID))
        
    def isUserInGroup(self, audienceGroupUserInfoRequest):
        Logger.log('Params - audienceGroupUserInfoRequest:', audienceGroupUserInfoRequest, ' serverRequestID:', self.serverRequestID)
        return self.log(self.connAudienceGroupManager.isUserInGroup(audienceGroupUserInfoRequest, self.serverRequestID))
        
    def createList(self, campaignID, listType, listInfo):
        Logger.log('Params -createList , orgId :{} , campaignId :{} , listType:{} , listInfo :{} , serverRequestID :{}'.format(constant.config['orgId'], campaignID, listType, listInfo, self.serverRequestID))
        return self.log(self.conn.createList(constant.config['orgId'], campaignID, listType, listInfo, self.serverRequestID))

    def reloadGroup(self, thriftCampaignGroup):
        Logger.log('Params - reloadGroup , thriftCampaignGroup :{} , serverRequestId :{}'.format(thriftCampaignGroup, self.serverRequestID))
        return self.log(self.conn.reloadGroup(thriftCampaignGroup, self.serverRequestID))

    def createAudience(self, createAudienceRequest):
        Logger.log('Params - create Audience :{}'.format(createAudienceRequest))
        return self.log(self.connAudienceGroupManager.createAudience(createAudienceRequest))

    def createAudienceGroup(self, createAudienceRequest):
        Logger.log('Params - create Audience Group :{}'.format(createAudienceRequest))
        return self.log(self.connAudienceGroupManager.createOrUpdateAudienceGroup(createAudienceRequest))

    def updateErrorStatusForAudienceGroup(self,groupId):
        Logger.log('Params - Group Id :{}'.format(groupId))
        return self.log(self.connAudienceGroupManager.updateErrorStatusForAudienceGroup(groupId,constant.config['orgId'],'Automation Check',self.serverRequestID))