import json, time

from src.Constant.constant import constant
from src.modules.campaignUIPages.campaignsUIDBCalls import DBCallsCampaigns
from src.modules.nsadmin.nsadminThrift import NSAdminThrift
from src.utilities.assertion import Assertion
from src.utilities.logger import Logger


class TimelineDBAssertion():
    
    def __init__(self, timelineName):
        self.timelineName = timelineName
        
    def check(self):
        try:
            self.sleepForTemporalEngineBasedOnCluster()
            self.getTimelineDetails()
            self.assertUsersInitialized()
            self.assertCommunicationDetails()
            self.assertVenenoDataDetails()
            self.checkCurrentMilestonContextErrorUsers()
            self.assertActivityContextHistory()
            self.checkNSAdminStatus()
        except Exception, exp:
            raise Exception('TIMELINEDB Exception :{}'.format(exp))
        finally:
            self.updateTimelineDBAsInactive()
    
    def getTimelineDetails(self):
        try:
            self.timelineDB, self.campaignId, self.configId = DBCallsCampaigns.getTimelineDB(self.timelineName)
            Logger.log('For Timeline :{} , timelineDB :{} and campaignId :{}'.format(self.timelineName, self.timelineDB, self.campaignId))
        except Exception, exp:
            raise Exception('GetTimelineDetails Failure :{}'.format(exp))
        
    def sleepForTemporalEngineBasedOnCluster(self):
        Logger.log('In Minimum Temporal Requires 6-7 mins to Execute , sleeping for 6 mins ...')
        time.sleep(400)
        if constant.config['cluster'] in ['china']: 
            Logger.log('Cluster is China,more , sleeping for more 10 mins as Execution is slow')
            time.sleep(600)
            
    def assertUsersInitialized(self):
        try:
            self.numberOfUsers = DBCallsCampaigns.getUserInitializedInTimeline(self.timelineDB)
            Logger.log('Number Of Users in user_initialization_histroy:{}'.format(self.numberOfUsers))
        except Exception, exp:
            raise Exception('User Initialization History Failure :{}'.format(exp))
        
    def assertCommunicationDetails(self):
        try:
            self.communicationDetailsId, self.bucketId, self.targetType, self.expectedCount, self.overallCount, self.state = DBCallsCampaigns.getCommunicationDetails(self.campaignId)
            self.numberOfTestUsers = self.overallCount
            self.numberOfControlUsers = self.numberOfUsers - self.numberOfTestUsers
            Logger.log('Number Of Test users :{} and number of Control users :{}'.format(self.numberOfTestUsers, self.numberOfControlUsers))
            Assertion.constructAssertion(self.state == 'OPENED', 'State of Timeline in CD is :{}'.format(self.state))
            Assertion.constructAssertion(self.targetType == 'TIMELINE', 'TargetType for Timeline in CD is :{}'.format(self.targetType))
        except Exception, exp:
            raise Exception('Communication Details Failure :{}'.format(exp))
        
    def assertVenenoDataDetails(self):
        try:
            self.assertInboxes()
            self.assertSkipped()
            Assertion.constructAssertion(self.numberOfTestUsers == self.numberOfExecutedUsers + self.numberOfSkippedUsers, 'Number of TestUsers are : {} and Inboxes Users :{} and Skipped users are:{} '.format(self.numberOfTestUsers, self.numberOfExecutedUsers, self.numberOfSkippedUsers))
        except Exception, exp:
            raise Exception('Veneno Data Details Failure :{}'.format(exp))
        
    def assertInboxes(self):
        try:
            inboxInfo = DBCallsCampaigns.getInboxDetails(self.bucketId, self.communicationDetailsId)
            self.numberOfExecutedUsers = len(inboxInfo)
            self.inboxDetails = {}
            for eachExecutedUser in inboxInfo:
                self.inboxDetails[eachExecutedUser[0]] = eachExecutedUser[1]
            Logger.log('Inbox Details are :{}'.format(self.inboxDetails))
        except Exception, exp:
            raise Exception('Inboxes Failure :{}'.format(exp))
        
    def assertSkipped(self):
        try:
            skippedInfo = DBCallsCampaigns.getSkippedDetails(self.bucketId, self.communicationDetailsId)
            self.numberOfSkippedUsers = len(skippedInfo)
            self.skippedDetails = {}
            for eachUser in skippedInfo:
                self.skippedDetails[eachUser[0]] = eachUser[1]
            Logger.log('Skipped Details are :{}'.format(self.skippedDetails))
        except Exception, exp:
            raise Exception('Skipped Failure :{}'.format(exp))
        
    def checkCurrentMilestonContextErrorUsers(self):
        try:
            temporalEngineMarkedErrorUsers = DBCallsCampaigns.getCurrentMilestoneContext(self.timelineDB)
            self.listOfErrorUserFromTemporal = []
            for eachErrorUser in temporalEngineMarkedErrorUsers:
                self.listOfErrorUserFromTemporal.append(eachErrorUser[0])
            Logger.log('List of Error Users from Timeline :{}'.format(self.listOfErrorUserFromTemporal))
        except Exception, exp:
            raise Exception('Current Milestone Context Failure :{}'.format(exp))
        
    def assertActivityContextHistory(self):
        try:
            self.activityContextHistory = DBCallsCampaigns.getActivityContextHistory(self.timelineDB)
            self.countOfAllUsersInActiivty = 0
            self.countOfExpiredUserInActivity = 0 
            self.countOfExecutingUsers = 0 
            self.countOfControlUserInActivity = 0
            self.countOfErrorUserInActivity = 0
            self.countOfErrorUserInActivityFromTemporal = 0
            self.countofExecutedUserInActivity = 0
            for eachRecord in self.activityContextHistory:
                self.countOfAllUsersInActiivty = self.countOfAllUsersInActiivty + 1
                user_id, status, status_context = eachRecord
                Logger.log('Checking for UserId:{} '.format(user_id))
                if status.lower() == 'expired':
                    Assertion.constructAssertion(False, 'Getting status For users as Expired ,Active Time has crossed / Please check manually', verify=True)
                    self.countOfExpiredUserInActivity = self.countOfExpiredUserInActivity + 1
                elif status.lower() == 'executing':
                    Logger.log('UserId :{} is marked as Executing in activity Context history')
                    self.countOfExecutingUsers = self.countOfExecutingUsers + 1
                elif status.lower() == 'skipped':
                    Logger.log('UserId :{} is marked as Skipped in activity Context history , user is control user with status Context :{}'.format(user_id, status_context))
                    self.countOfControlUserInActivity = self.countOfControlUserInActivity + 1
                elif status.lower() == 'error':
                    Logger.log('UserId :{} is marked as Error in activity Context history with status Context :{},checking in Skipped recipient'.format(user_id, status_context))
                    if status_context in ['User Does not have any mobile']:
                        Logger.log('User Got Error From Temporal Engine as User Does not have any mobile')
                        self.countOfErrorUserInActivityFromTemporal = self.countOfErrorUserInActivityFromTemporal + 1
                    else:
                        self.countOfErrorUserInActivity = self.countOfErrorUserInActivity + 1
                        Assertion.constructAssertion(self.skippedDetails[user_id] == status_context, 'In Skipped Recipient user :{} got skipped due to :{} and in tempoaral due to :{}'.format(user_id, self.skippedDetails[user_id], status_context))
                elif status.lower() == 'executed':
                    Logger.log('UserId :{} is marked as Executed in activity Context history, checking with Inboxes Table'.format(user_id))
                    self.countofExecutedUserInActivity = self.countofExecutedUserInActivity + 1
                    Assertion.constructAssertion(user_id in self.inboxDetails, 'userId :{}  found in Inboxes'.format(user_id))
                else:
                    Assertion.constructAssertion(False, 'New Status type :{} , add in Automation'.format(status))
                    
            Assertion.constructAssertion(False, 'In Activity Context History, Total Number of Users are :{} of which Expired Users are :{}, Executing Users are:{},Skipped(Control) Users are :{},Error Generated From Temporal Engine :{}, Error From Veneno/SkippedRecipient :{}, Executed Users are:{}'.format(self.countOfAllUsersInActiivty, self.countOfExpiredUserInActivity, self.countOfExecutingUsers, self.countOfControlUserInActivity, self.countOfErrorUserInActivityFromTemporal, self.countOfErrorUserInActivity, self.countofExecutedUserInActivity), verify=True)
            if self.numberOfUsers == self.countOfExpiredUserInActivity:
                Assertion.constructAssertion(False, 'All Users got Expried')
            if self.countOfExecutingUsers == 0 :
                Assertion.constructAssertion(self.countofExecutedUserInActivity == self.numberOfExecutedUsers, 'Executing Count is 0 , Executed Count :{} and in Inboxes User Count :{}'.format(self.countofExecutedUserInActivity, self.numberOfExecutedUsers))
            else:
                Assertion.constructAssertion(self.countofExecutedUserInActivity <= self.numberOfExecutedUsers, 'Executing Count is {} , Executed Count :{} and in Inboxes User Count :{}'.format(self.countOfExecutingUsers, self.countofExecutedUserInActivity, self.numberOfExecutedUsers))
            
            Assertion.constructAssertion(self.countOfErrorUserInActivity == self.numberOfSkippedUsers , 'Count of Error Users in Activity :{} and number Of Skipped Recipeints :{}'.format(self.countOfErrorUserInActivity , self.numberOfSkippedUsers))
            Assertion.constructAssertion(self.countOfControlUserInActivity == self.numberOfControlUsers, 'NumberOfControlUsers Check :{}'.format(self.countOfControlUserInActivity))
            self.assertpercentageOfUsersGotExecuting()
        except Exception, exp:
            raise Exception('Activity Context History Failure :{}'.format(exp))
        
    def assertpercentageOfUsersGotExecuting(self):
        try:
            percOfUserInExecuting = self.countOfExecutingUsers / self.numberOfTestUsers * 100
            Assertion.constructAssertion(percOfUserInExecuting < 20, 'More Than 20% users are not marked as Executing in ActivityContextHistory')
        except Exception, exp:
            raise Exception('Executing Check Failure :{}'.format(exp))
        
    def checkNSAdminStatus(self, maxNumberOfCheck=20):
        try:
            nsadminStatusList = []
            if len(self.inboxDetails) == 0:
                Logger.log('No User got Executed , so nothing to check in NSADMIN')
            else:
                try:
                    for eachExecutedUser in self.inboxDetails:
                        if maxNumberOfCheck == 0 :
                            break
                        else:
                            maxNumberOfCheck = maxNumberOfCheck - 1
                        nsadminId = self.inboxDetails[eachExecutedUser]
                        nsadminInstance = NSAdminThrift(constant.config['nsMasterPort'])
                        status = nsadminInstance.getMessagesById([nsadminId])[0].status
                        Logger.log('Status of Message is :{} for nsadmin id :{}'.format(status, nsadminId))
                        if status not in nsadminStatusList : nsadminStatusList.append(status)
                except Exception, exp:
                    Assertion.constructAssertion(False, 'NSADMIN Check Failed , due to Exception :{}'.format(exp), verify=True)
                finally:        
                    Assertion.constructAssertion(False, 'Distinct Status from NSADMIN for This Campaign is :{}'.format(nsadminStatusList), verify=True)
        except Exception, exp:
            raise Exception('NSADMINException :{}'.format(exp))

    def updateTimelineDBAsInactive(self):
        DBCallsCampaigns.markCampaignAsInactive(self.configId)