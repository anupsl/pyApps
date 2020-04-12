import pytest, time

from src.Constant.constant import constant
from src.utilities.logger import Logger
from src.modules.nsadmin.nsadminObject import NSAdminObject
from src.modules.nsadmin.nsadminHelper import NSAdminHelper
from src.utilities.assertion import Assertion
from src.utilities.dbhelper import dbHelper


class Test_CreditsManagement():

    def setup_class(self):
        Logger.logSuiteName(str(self).split('.')[-1])
        self.orgId = constant.config['orgId']

    def setup_method(self, method):
        messageClass = 'SMS'
        if 'EMAIL' in method.__name__:
            messageClass = 'EMAIL'          
        self.nsObj = NSAdminHelper.getConnObj(newConnection=True)
        self.masterNsObj = NSAdminHelper.getMasterConnObj()
        self.nsadminHelper = NSAdminHelper(constant.config['orgId'], messageClass)
        self.nsadminHelper.disableDomainPropertiesGatewayMap()
        Logger.logMethodName(method.__name__)        

    def test_addCreditsSMS(self):
        creditDetails1 = {
            "orgId" : self.orgId,
            "bulkCredits" : 200
        }
        creditDetails1 = NSAdminObject.OrgCreditDetails(creditDetails1)
        currVal = self.masterNsObj.getCreditDetails(self.orgId)
        resp1 = self.masterNsObj.addCredits(creditDetails1)
        afterAdd = self.masterNsObj.getCreditDetails(self.orgId)
        Assertion.constructAssertion(resp1 == True, 'addCredits response')
        Assertion.constructAssertion(afterAdd.bulkCredits == currVal.bulkCredits + 200, 'increase in bulkCredits')
        creditDetails2 = {
            "orgId" : self.orgId,
            "bulkCredits" : -100
        }        
        creditDetails2 = NSAdminObject.OrgCreditDetails(creditDetails2)
        resp2 = self.masterNsObj.addCredits(creditDetails2)
        afterDeduc = self.masterNsObj.getCreditDetails(self.orgId)
        Assertion.constructAssertion(resp2 == True, 'addCredits response')
        Assertion.constructAssertion(afterDeduc.bulkCredits == currVal.bulkCredits + 100, 'decrease in bulkCredits')

    def test_addCreditsEmail(self):
        creditDetails1 = {
            "orgId" : self.orgId,
            "bulkCredits" : 200,
            'messageClass' : 1
        }
        creditDetails1 = NSAdminObject.OrgCreditDetails(creditDetails1)
        currVal = self.masterNsObj.getCreditDetailsByOrgAndChannel(self.orgId, 1, 'test')
        resp1 = self.masterNsObj.addCredits(creditDetails1)
        afterAdd = self.masterNsObj.getCreditDetailsByOrgAndChannel(self.orgId, 1, 'test')
        Assertion.constructAssertion(resp1 == True, 'addCredits response')
        Assertion.constructAssertion(afterAdd.bulkCredits == currVal.bulkCredits + 200, 'increase in bulkCredits')
        creditDetails2 = {
            "orgId" : self.orgId,
            "bulkCredits" : -100,
            'messageClass' : 1            
        }        
        creditDetails2 = NSAdminObject.OrgCreditDetails(creditDetails2)
        resp2 = self.masterNsObj.addCredits(creditDetails2)
        afterDeduc = self.masterNsObj.getCreditDetailsByOrgAndChannel(self.orgId, 1, 'test')
        Assertion.constructAssertion(resp2 == True, 'addCredits response')
        Assertion.constructAssertion(afterDeduc.bulkCredits == currVal.bulkCredits + 100, 'decrease in bulkCredits')


    def test_getCreditsLog(self):
        output = self.masterNsObj.getCreditsLog(self.orgId)
        Assertion.constructAssertion(len(output) > 0, 'count greater than 0')


    @pytest.mark.parametrize('priority, gateway', [
                    ('HIGH', 'cardboardfishmock'),
                    ('BULK', 'valuefirstmock')])
    def est_CreditUseSMS(self, priority, gateway):
        self.nsadminHelper.configureGateway(priority, gateway)
        output = self.masterNsObj.getCreditDetailsByOrgAndChannel(self.orgId, 0, 'test')
        smsCreditsBefore = output.bulkCredits
        message320CharSize = "At Capillary, we continuously work to help our clients succeed in rapidly evolving markets through our world-class solutions, services and products. By combining big data with a robust, cloud-based analytics engine, we optimize the relevance and profitability of discounts and personalized offers to consumers in real time, significantly increasing both loyalty and sales"
        msgDict = {"messageClass" : "SMS", "priority" : priority, "truncate": False,
        "message" : message320CharSize}
        resp  = self.nsadminHelper.createAndSendMessage(msgDict)
        time.sleep(10)
        output = self.masterNsObj.getCreditDetailsByOrgAndChannel(self.orgId, 0, 'test')
        smsCreditsAfter = output.bulkCredits
        Assertion.constructAssertion(smsCreditsBefore == smsCreditsAfter + 3, 'sms usage count decrease by 3')        

    @pytest.mark.parametrize('priority, gateway', [
                    ('HIGH', 'localmail_HIGH'),
                    ('BULK', 'localmail_BULK')])
    def est_CreditUseEMAIL(self, priority, gateway):
        self.nsadminHelper.configureGateway(priority, gateway)        
        output = self.masterNsObj.getCreditDetailsByOrgAndChannel(self.orgId, 1, 'test')
        emailCreditsBefore = output.bulkCredits
        receiver = constant.config['prodEmail1']+','+constant.config['prodEmail2']
        msgDict = {"messageClass" : "EMAIL", "priority" : priority, 
            "message" : "test message with priority "+priority, 'receiver' : receiver}
        resp  = self.nsadminHelper.createAndSendMessage(msgDict)        
        time.sleep(5)
        output = self.masterNsObj.getCreditDetailsByOrgAndChannel(self.orgId, 1, 'test')
        emailCreditsAfter = output.bulkCredits
        Assertion.constructAssertion(emailCreditsBefore == emailCreditsAfter + 2, 'eamil usage count decrease by 2 - count of receiver')        
