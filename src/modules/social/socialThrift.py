from src.Constant.constant import constant
from src.initializer.generateThrift import facebook
from src.utilities.logger import Logger
from thriftpy.rpc import make_client


class SocialThrift():

    def __init__(self, port, timeout=60000):
        self.conn = make_client(facebook.FacebookService, '127.0.0.1', port, timeout=timeout)

    def log(self, output):
        Logger.log(output)
        return output

    def close(self):
        Logger.log('Closing FBThrift connection')
        self.conn.close()

    def isAlive(self):
        return self.log(self.conn.isAlive())

    def createCustomList(self,userlist,customAudienceListDetails,socialAccountDetails,orgId,recepientlistId,requestId):
        Logger.log('Call :{} , Params :{},{},{},{},{},{}'.format('createCustomList',userlist,customAudienceListDetails,socialAccountDetails,orgId,recepientlistId,requestId))
        return self.log(self.conn.createCustomList(userlist,customAudienceListDetails,socialAccountDetails,orgId,recepientlistId,requestId))

    def getCustomAudienceLists(self,orgId,socialChannel,clearcache,requestId):
        Logger.log('Call :{} , Params :{},{},{},{}'.format('getCustomAudienceLists',orgId,socialChannel,clearcache,requestId))
        return self.log(self.conn.getCustomAudienceLists(orgId,socialChannel,clearcache,requestId))

    def getAdSets(self,socialChannel,orgId,requestId):
        Logger.log('Call :{} , Params :{},{},{}'.format('getAdSets',socialChannel,orgId,requestId))
        return self.log(self.conn.getAdSets(socialChannel,orgId,requestId))

    def getAdsetInsights(self,socialChannel,orgId,adsetId,groupId,clearchche,requestId):
        Logger.log('Call :{} , Params :{},{},{},{},{},{}'.format('getAdsetInsights',socialChannel,orgId,adsetId,groupId,clearchche,requestId))
        return self.log(self.conn.getAdsetInsights(socialChannel,orgId,adsetId,groupId,clearchche,requestId))

    def deleteSocialAudienceList(self,socialChannel,orgId,remoteListId,requestId):
        Logger.log('Call :{} , Params :{},{},{},{}'.format('deleteSocialAudienceList',socialChannel,orgId,remoteListId,requestId))
        return self.log(self.conn.deleteSocialAudienceList(socialChannel,orgId,remoteListId,requestId))

    def testAccount(self,socialChannel,orgId,requestId):
        Logger.log('Call :{} , Params :{},{},{}'.format('testAccount',socialChannel,orgId,requestId))
        return self.log(self.conn.testAccount(socialChannel,orgId,requestId))

    def createCampaign(self,orgId,socialChannel,socialCampaign,requestId):
        Logger.log('Call :{} , Params :{},{},{},{}'.format('createCampaign',orgId,socialChannel,socialCampaign,requestId))
        return self.log(self.conn.createCampaign(orgId,socialChannel,socialCampaign,requestId))

    def getPageIdForOrgAndAccount(self,orgId,socialChannel,requestId):
        Logger.log('Call :{} , Params :{},{},{}'.format('getPageIdForOrgAndAccount',orgId,socialChannel,requestId))
        return self.log(self.conn.getPageIdForOrgAndAccount(orgId,socialChannel,requestId))

    def createNativeOffer(self,orgId,socialChannel,socialOffer,requestId):
        Logger.log('Call :{} , Params :{},{},{},{}'.format('createNativeOffer',orgId,socialChannel,socialOffer,requestId))
        return self.log(self.conn.createNativeOffer(orgId,socialChannel,socialOffer,requestId))

    def createSocialAdset(self,orgId,socialChannel,socialAdsetInfo,requestId):
        Logger.log('Call :{} , Params :{},{},{},{}'.format('createSocialAdset',orgId,socialChannel,socialAdsetInfo,requestId))
        return self.log(self.conn.createSocialAdset(orgId,socialChannel,socialAdsetInfo,requestId))

    def updateCustomAudienceAndOfferForSocialAdset(self,orgId,socialChannel,updateAdsetRequest,requestId):
        Logger.log('Call :{} , Params :{},{},{},{}'.format('updateCustomAudienceAndOfferForSocialAdset',orgId,socialChannel,updateAdsetRequest,requestId))
        return self.log(self.conn.updateCustomAudienceAndOfferForSocialAdset(orgId,socialChannel,updateAdsetRequest,requestId))

    def getSocialCampaignDetails(self,orgId,campaignId,userId,socialChannel,requestId):
        Logger.log('Call :{} , Params :{},{},{},{},{}'.format('getSocialCampaignDetails',orgId,campaignId,userId,socialChannel,requestId))
        return self.log(self.conn.getSocialCampaignDetails(orgId,campaignId,userId,socialChannel,requestId))

    def updateCustomListInAdset(self,orgId,socialChannel,remoteAdsetId,remoteCampaignId,requestId):
        Logger.log('Call :{} , Params :{},{},{},{},{}'.format('updateCustomListInAdset',orgId,socialChannel,remoteAdsetId,remoteCampaignId,requestId))
        return self.log(self.conn.updateCustomListInAdset(orgId,socialChannel,remoteAdsetId,remoteCampaignId,requestId))