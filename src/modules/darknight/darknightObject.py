import time
from src.Constant.constant import constant
from src.initializer.generateThrift import darknight



class DarknightObject(object):

    def __init__(self):
        self.JobPriority = { 'BULK' : 1, 'TRANS' : 2, 'CAMPAIGN' : 3 }
        self.WChannel = { 'EMAIL' : 1 }
        self.EmailGatewayStatusEnum = ['HARD_BOUNCED', 'SOFT_BOUNCED', 'DELIVERED', 'UNKNOWN', 'FAILED']
        self.EmailStatusEnum = ['VALID', 'INVALID', 'UNKNOWN', 'NOT_PROCESSED']
        self.VerifierTypeEnum = ['ROBIN', 'BRITE', 'GATEWAY', 'NONE']

    @staticmethod
    def EmailGatewayStatus(statusDict):
        #dObj = DarknightObject()
        tmpDict = {'last_checked_date' : int(time.time()), 'reason' : 'test'}
        tmpDict.update(statusDict)
        return darknight.Message(**tmpDict)    
