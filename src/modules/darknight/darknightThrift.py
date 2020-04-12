from src.Constant.constant import constant
from src.initializer.generateThrift import darknight
from src.utilities.logger import Logger
from thriftpy.rpc import make_client
import random


class DarknightThrift(object):

    def __init__(self, port, timeout=60000):
        self.conn = make_client(darknight.DarknightService, '127.0.0.1', port, timeout=timeout)
        self.getServerRequestID()

    def getServerRequestID(self):
        self.serverRequestID = 'darknight_auto_'+str(random.randint(11111, 99999))        

    def close(self):
        Logger.log('Closing DarknightThrift connection')
        self.conn.close()

    def log(self, output):
        Logger.log(output)
        return output

    def createNewJob(self, jobReq):
        Logger.log('jobReq ',jobReq, ' serverRequestID:', self.serverRequestID)
        return self.log(self.conn.createNewJob(jobReq, self.serverRequestID))

    def getJobStatus(self, jobId):
        Logger.log('jobId ',jobId, ' serverRequestID:', self.serverRequestID)
        return self.log(self.conn.getJobStatus(jobId, self.serverRequestID))

    def updateEmailStatus(self, emailStatusList):
        Logger.log('emailStatusList ',emailStatusList, ' serverRequestID:', self.serverRequestID)
        return self.log(self.conn.updateEmailStatus(emailStatusList, self.serverRequestID))

    def getEmailStatus(self, emailList):
        Logger.log('emailIDs ',emailList, ' serverRequestID:', self.serverRequestID)
        return self.log(self.conn.getEmailStatus(emailList, self.serverRequestID))

    def getEmailStatusWithReporting(self, orgId, userEmailMap):
        Logger.log('orgId: ',orgId,' userEmailMap: ',userEmailMap, ' serverRequestID:', self.serverRequestID)
        return self.log(self.conn.getEmailStatusWithReporting(orgId, userEmailMap, self.serverRequestID))

    def getMobileStatus(self, mobileNumbers, orgId):
        Logger.log('mobileNumbers ',mobileNumbers,' orgId ',orgId, ' serverRequestID:', self.serverRequestID)
        return self.log(self.conn.getMobileStatus(mobileNumbers, orgId, self.serverRequestID))

    def isAlive(self):
        return self.log(self.conn.isAlive())




