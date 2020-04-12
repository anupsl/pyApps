import pytest, time

from src.Constant.constant import constant
from src.utilities.logger import Logger
from src.modules.nsadmin.nsadminObject import NSAdminObject
from src.modules.nsadmin.nsadminHelper import NSAdminHelper
from src.utilities.assertion import Assertion
from src.utilities.dbhelper import dbHelper


class Test_Others():

    def setup_class(self):
        Logger.logSuiteName(str(self).split('.')[-1])
        self.orgId = constant.config['orgId']

    def setup_method(self, method):      
        self.nsObj = NSAdminHelper.getConnObj(newConnection=True)
        self.nsadminHelper = NSAdminHelper(constant.config['orgId'], 'SMS')
        Logger.logMethodName(method.__name__)

    def test_isAlive(self):
        output = self.nsObj.isAlive()
        Assertion.constructAssertion(output == True, 'isAlive output')

    def test_getStatus(self):
        output = self.nsObj.getStatus()
        Assertion.constructAssertion(output == 'All is well', 'getStatus output')        

    def test_isMaster(self):
        output = self.nsObj.isMaster()
        Assertion.constructAssertion(output == True, 'isMaster output',verify=True)

    def test_getMessageLogs(self):
        msgDict = {"receiver" : "", "messageClass" : "SMS", "priority" : "BULK",
                    "message" : "test message from auto"}
        msgId = self.nsadminHelper.createAndSendMessage(msgDict, 1)
        msgObj = self.nsObj.getMessagesById([msgId])[0]
        msgLogObj = self.nsObj.getMessageLogs(self.orgId, "SMS", msgObj.receiver)[0]
        Assertion.constructAssertion(msgLogObj.messageId == msgObj.messageId, 'getMessageLogs messageId')
        Assertion.constructAssertion(msgLogObj.status  == msgObj.status , 'getMessageLogs status')
        
    def test_Count_Messages_RECEIVED_IN_QUEUE_READ(self):
        currentMonth = NSAdminHelper.getTableName()
        query = 'SELECT COUNT( * ) FROM '+currentMonth+' where sent_time >= SUBDATE( current_date, 2) and sent_time < current_date and status in (2,35)'
        output = dbHelper.queryDB(query, 'nsadmin') 
        Assertion.constructAssertion(output[0][0] == 0, 'RECEIVED_IN_QUEUE & READ count',verify=True)

    def test_Count_Messages_DELAYED_SCHEDULED(self):
        currentMonth = NSAdminHelper.getTableName()
        query = 'SELECT COUNT( * ) FROM '+currentMonth+' where sent_time >= SUBDATE( current_date, 2) and sent_time < current_date and status in (33)'
        output = dbHelper.queryDB(query, 'nsadmin') 
        Assertion.constructAssertion(output[0][0] == 0, 'DELAYED_SCHEDULED count')


