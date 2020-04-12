from src.Constant.constant import constant
from src.initializer.generateThrift import emf
from src.utilities.logger import Logger
from thriftpy.rpc import make_client
import random


class EMFThrift(object):

    def __init__(self, port, timeout=60000):
        self.conn = make_client(emf.EMFService, '127.0.0.1', port, timeout=timeout)
        self.getServerRequestID()

    def getServerRequestID(self):
        self.serverRequestID = 'emf_auto_'+str(random.randint(11111, 99999))

    def close(self):
        Logger.log('Closing EMFThrift Connection')
        self.conn.close()

    def log(self, output):
        Logger.log(output)
        return output

    def isAlive(self):
        return self.log(self.conn.isAlive())


    ##ORGANIZATION RELATED
    def isOrganizationEnabled(self, orgID):
        Logger.log('orgID: ',orgID, ' serverRequestID:', self.serverRequestID)
        return self.log(self.conn.isOrganizationEnabled(orgID, self.serverRequestID))

    def disableOrganization(self, orgID):
        Logger.log('orgID: ',orgID, ' serverRequestID:', self.serverRequestID)
        return self.log(self.conn.disableOrganization(orgID, self.serverRequestID))       

    def checkOrganizationConfiguration(self, orgID):
        Logger.log('orgID: ',orgID, ' serverRequestID:', self.serverRequestID)
        return self.log(self.conn.checkOrganizationConfiguration(orgID, self.serverRequestID))


    ## EVENT RELATED
    def newBillEvent(self, newBillEvent, isCommit=True, isReplayed=False):
        Logger.log('newBillEvent: ',newBillEvent, ' isCommit:', isCommit, ' isReplayed: ',isReplayed)
        return self.log(self.conn.newBillEvent(newBillEvent, isCommit, isReplayed))

    def newBillDVSEvent(self, newBillEvent, isCommit, isReplayed):    
        Logger.log('newBillEvent: ',newBillEvent, ' isCommit:', isCommit, ' isReplayed: ',isReplayed)
        return self.log(self.conn.newBillDVSEvent(newBillEvent, isCommit, isReplayed))
     
    def registrationEvent(self, registrationEvent, isCommit, isReplayed):
        Logger.log('registrationEvent: ',registrationEvent, ' isCommit:', isCommit, ' isReplayed: ',isReplayed)
        return self.log(self.conn.registrationEvent(registrationEvent, isCommit, isReplayed))
    
    def pointsRedemptionEvent(self, pointsRedemptionEventData, isCommit=True, isReplayed=False):
        Logger.log('pointsRedemptionEventData: ',pointsRedemptionEventData, ' isCommit:', isCommit, ' isReplayed: ',isReplayed)
        return self.log(self.conn.pointsRedemptionEvent(pointsRedemptionEventData, isCommit, isReplayed))
    
    def voucherPreRedemptionEvent(self, voucherPreRedemptionEventData, isCommit, isReplayed):
        Logger.log('voucherPreRedemptionEventData: ',voucherPreRedemptionEventData, ' isCommit:', isCommit, ' isReplayed: ',isReplayed)
        return self.log(self.conn.voucherPreRedemptionEvent(voucherPreRedemptionEventData, isCommit, isReplayed))

    def voucherRedemptionEvent(self, voucherRedemptionEventData, isCommit, isReplayed):
        Logger.log('voucherRedemptionEventData: ',voucherRedemptionEventData, ' isCommit:', isCommit, ' isReplayed: ',isReplayed)
        return self.log(self.conn.voucherRedemptionEvent(voucherRedemptionEventData, isCommit, isReplayed))
        
    def returnLineitemsEvent(self, returnBillLineitemsEventData, isCommit = True, isReplayed = False):
        Logger.log('returnBillLineitemsEventData: ',returnBillLineitemsEventData, ' isCommit:', isCommit, ' isReplayed: ',isReplayed)
        return self.log(self.conn.returnLineitemsEvent(returnBillLineitemsEventData, isCommit, isReplayed))

    def returnBillAmountEvent(self, returnBillAmountEventData, isCommit=True, isReplayed=True):
        Logger.log('returnBillAmountEventData: ',returnBillAmountEventData, ' isCommit:', isCommit, ' isReplayed: ',isReplayed)
        return self.log(self.conn.returnBillAmountEvent(returnBillAmountEventData, isCommit, isReplayed))
        
    def cancelBillEvent(self, cancelBillEventData, isCommit, isReplayed):
        Logger.log('cancelBillEventData: ',cancelBillEventData, ' isCommit:', isCommit, ' isReplayed: ',isReplayed)
        return self.log(self.conn.cancelBillEvent(cancelBillEventData, isCommit, isReplayed))
        
    def trackerConditionSuccessEvent(self, trackerConditionSuccessEventData, isCommit, isReplayed):
        Logger.log('trackerConditionSuccessEventData: ',trackerConditionSuccessEventData, ' isCommit:', isCommit, ' isReplayed: ',isReplayed)
        return self.log(self.conn.trackerConditionSuccessEvent(trackerConditionSuccessEventData, isCommit, isReplayed))
            
    def customerUpdateEvent(self, customerUpdateEventData, isCommit, isReplayed):
        Logger.log('customerUpdateEventData: ',customerUpdateEventData, ' isCommit:', isCommit, ' isReplayed: ',isReplayed)
        return self.log(self.conn.customerUpdateEvent(customerUpdateEventData, isCommit, isReplayed))
   
    def transactionUpdateEvent(self, transactionUpdateEventData, isCommit, isReplayed):
        Logger.log('transactionUpdateEventData: ',transactionUpdateEventData, ' isCommit:', isCommit, ' isReplayed: ',isReplayed)
        return self.log(self.conn.transactionUpdateEvent(transactionUpdateEventData, isCommit, isReplayed))
    
    def socialConnectEvent(self, socialConnectEvent, isCommit, isReplayed):
        Logger.log('socialConnectEvent: ',socialConnectEvent, ' isCommit:', isCommit, ' isReplayed: ',isReplayed)
        return self.log(self.conn.socialConnectEvent(socialConnectEvent, isCommit, isReplayed))
    
    def socialConnectUpdateEvent(self, socialConnectUpdateEvent, isCommit, isReplayed):
        Logger.log('socialConnectUpdateEvent: ',socialConnectUpdateEvent, ' isCommit:', isCommit, ' isReplayed: ',isReplayed)
        return self.log(self.conn.socialConnectUpdateEvent(socialConnectUpdateEvent, isCommit, isReplayed))
        
    def CampaignRefereeRedeemEvent(self, campaignRefereeRedeemEventData, isCommit, isReplayed):
        Logger.log('campaignRefereeRedeemEventData: ',campaignRefereeRedeemEventData, ' isCommit:', isCommit, ' isReplayed: ',isReplayed)
        return self.log(self.conn.CampaignRefereeRedeemEvent(campaignRefereeRedeemEventData, isCommit, isReplayed))
   
    def CampaignReferralReferrerEvent(self, campaignReferralReferrerEventData, isCommit, isReplayed):
        Logger.log('campaignReferralReferrerEventData: ',campaignReferralReferrerEventData, ' isCommit:', isCommit, ' isReplayed: ',isReplayed)
        return self.log(self.conn.CampaignReferralReferrerEvent(campaignReferralReferrerEventData, isCommit, isReplayed))

    def CampaignReferralEvent(self, campaignReferralEventData, isCommit, isReplayed):
        Logger.log('campaignReferralEventData: ',campaignReferralEventData, ' isCommit:', isCommit, ' isReplayed: ',isReplayed)
        return self.log(self.conn.CampaignReferralEvent(campaignReferralEventData, isCommit, isReplayed))

    def IncomingSmsEvent(self, IncomingSmsEventData, isCommit, isReplayed):
        Logger.log('IncomingSmsEventData: ',IncomingSmsEventData, ' isCommit:', isCommit, ' isReplayed: ',isReplayed)
        return self.log(self.conn.IncomingSmsEvent(IncomingSmsEventData, isCommit, isReplayed))

    def transactionFinishedEvent(self, transactionFinishedEventData, isCommit, isReplayed):
        Logger.log('transactionFinishedEventData: ',transactionFinishedEventData, ' isCommit:', isCommit, ' isReplayed: ',isReplayed)
        return self.log(self.conn.transactionFinishedEvent(transactionFinishedEventData, isCommit, isReplayed))

    def simulateRulesBasedOnDateRange(self, simulationInputData):
        Logger.log('simulationInputData: ',simulationInputData)
        return self.log(self.conn.simulateRulesBasedOnDateRange(simulationInputData))

    def referralPostProcessingEvent(self, referralPostProcessingEventData, isCommit, isReplayed):
        Logger.log('referralPostProcessingEventData: ',referralPostProcessingEventData, ' isCommit:', isCommit, ' isReplayed: ',isReplayed)
        return self.log(self.conn.referralPostProcessingEvent(referralPostProcessingEventData, isCommit, isReplayed))

    def emailOpenEvent(self, emailOpenEventData, isCommit, isReplayed):
        Logger.log('emailOpenEventData: ',emailOpenEventData, ' isCommit:', isCommit, ' isReplayed: ',isReplayed)
        return self.log(self.conn.emailOpenEvent(emailOpenEventData, isCommit, isReplayed))

    def emailClickEvent(self, emailClickEventData, isCommit, isReplayed):       
        Logger.log('emailClickEventData: ',emailClickEventData, ' isCommit:', isCommit, ' isReplayed: ',isReplayed)
        return self.log(self.conn.emailClickEvent(emailClickEventData, isCommit, isReplayed))

    def pointsTransferEvent(self, PointsTransferEventData, isCommit, isReplayed):
        Logger.log('pointsTransferEventData: ',PointsTransferEventData, ' isCommit:', isCommit, ' isReplayed: ',isReplayed)
        return self.log(self.conn.pointsTransferEvent(PointsTransferEventData, isCommit, isReplayed))

    def pointsRedemptionReversalEvent(self,pointsRedemptionReversalEventData, isCommit = True, isReplayed = False):
        Logger.log('pointsRedemptionReversalEvent Request : {}, isCommit: {}, isReplayed: {}'.format(pointsRedemptionReversalEventData,isCommit,isReplayed))
        return self.log(self.conn.pointsRedemptionReversalEvent(pointsRedemptionReversalEventData, isCommit, isReplayed))
