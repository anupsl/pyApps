from src.Constant.constant import constant
from src.initializer.generateThrift import veneno
from src.utilities.logger import Logger
from thriftpy.rpc import make_client
import random

class VenenoThrift(object):
    def __init__(self, port, timeout=60000):
        self.conn = make_client(veneno.VenenoService, '127.0.0.1', port, timeout=timeout)
        self.getServerRequestID()

    def getServerRequestID(self):
        self.serverRequestID = 'veneno_auto_' + str(random.randint(11111, 99999))

    def close(self):
        Logger.log('Closing VenenoThrift connection')
        self.conn.close()

    def log(self, output):
        Logger.log(output)
        return output

    def isAlive(self):
        return self.log(self.conn.isAlive())    

    def addMessageForRecipients(self, messageDetails):
        Logger.log('Params - messageDetails:', messageDetails , ' serverRequestID:', self.serverRequestID)
        return self.log(self.conn.addMessageForRecipients(messageDetails, self.serverRequestID))

    def getMessageBody(self, userId, outboxId):
        Logger.log('Params - userId:', userId , ' outboxId:', outboxId, ' serverRequestID:', self.serverRequestID)
        return self.log(self.conn.getMessageBody(userId, outboxId, self.serverRequestID))        

    def replaceTemplate(self, userId, orgId, template, arguments):
        Logger.log('Params - userId:', userId , ' orgId:', orgId, ' template:', template, ' arguments:', arguments, ' serverRequestID:', self.serverRequestID)
        return self.log(self.conn.replaceTemplate(userId, orgId, template, arguments, self.serverRequestID))        

    def getStatus(self):
        Logger.log('Params - serverRequestID:', self.serverRequestID)
        return self.log(self.conn.getStatus(self.serverRequestID))   

    def getBucketDetailsByMessageID(self, messageID):
        Logger.log('Params - messageID:', messageID , ' serverRequestID:', self.serverRequestID)
        return self.log(self.conn.getBucketDetailsByMessageID(messageID, self.serverRequestID))   

    def updateInboxDeliveryStatus(self, messageID, deliveryStatus):
        Logger.log('Params - messageID:', messageID , ' deliveryStatus:', deliveryStatus, ' serverRequestID:', self.serverRequestID)
        return self.log(self.conn.updateInboxDeliveryStatus(messageID, deliveryStatus, self.serverRequestID))        

    def updateUserUnsubscriptionStatus(self, orgId, recipientId, messageId):
        Logger.log('Params - orgId:', orgId , ' messageId:', messageId, ' recipientId', recipientId, ' serverRequestID:', self.serverRequestID)
        return self.log(self.conn.updateUserUnsubscriptionStatus(orgId, messageId, recipientId, self.serverRequestID))        
