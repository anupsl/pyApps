import pytest, time, json

from src.Constant.constant import constant
from src.utilities.logger import Logger
from src.modules.nsadmin.nsadminObject import NSAdminObject
from src.modules.nsadmin.nsadminHelper import NSAdminHelper
from src.utilities.assertion import Assertion
from src.utilities.randValues import randValues


class Test_DomainProperties():

    def setup_class(self):
        Logger.logSuiteName(str(self).split('.')[-1])
        self.orgId = constant.config['orgId']
        self.cluster = constant.config['cluster']

    def setup_method(self, method):      
        self.nsObj = NSAdminHelper.getConnObj(newConnection=True)
        self.nsadminHelper = NSAdminHelper(self.orgId, 'SMS')
        self.nsadminHelper.disableDomainPropertiesGatewayMap()        
        Logger.logMethodName(method.__name__)


    @pytest.mark.parametrize('priority, gateway', [
                    ('HIGH', 'cardboardfishmock'),
                    ('BULK', 'valuefirstmock')])        
    def test_sendMessage_SMS_UseSystemDefaultsGateway_Sanity(self, priority, gateway):
        self.nsadminHelper.configureGateway(priority, gateway)
        msgDict = {"messageClass" : "SMS", "priority" : priority, "message" : "test message with priority "+priority}
        resp  = self.nsadminHelper.createAndSendMessage(msgDict)
        Assertion.constructAssertion(resp > 0, 'sendMessage output')
        resp = self.nsObj.getMessagesById([resp])[0]
        Assertion.constructAssertion(resp.status in ['RECEIVED_IN_QUEUE', 'SENT'], 'Messages status')
        Assertion.constructAssertion(resp.gateway == gateway, 'gateway used for  sending')
        Assertion.constructAssertion(resp.priority == priority, 'priority')


    def test_getDomainPropertiesByOrg_And_ID(self):
        resp = self.nsObj.getDomainPropertiesByOrg(self.orgId)[0]
        Assertion.constructAssertion(resp.orgId == self.orgId, 'orgId')
        dpgmID = resp.id 
        resp = self.nsObj.getDomainPropertiesByID(dpgmID)
        Assertion.constructAssertion(resp.orgId == self.orgId, 'orgId')


    def test_getDomainPropertiesGatewayMapByOrg_AND_ID(self):
        self.nsadminHelper.configureGateway("BULK", "valuefirstmock")
        resp = self.nsObj.getDomainPropertiesGatewayMapByOrg(self.orgId, 0)[0]
        Assertion.constructAssertion(resp.orgId == self.orgId, 'orgId')
        Assertion.constructAssertion(resp.gatewayOrgConfigs.shortName == 'valuefirstmock', 'gateway shortName')
        dpgmId = resp.id
        resp = self.nsObj.getDomainPropertiesGatewayMapByID(dpgmId)
        Assertion.constructAssertion(resp.orgId == self.orgId, 'orgId')
        Assertion.constructAssertion(resp.gatewayOrgConfigs.shortName == 'valuefirstmock', 'gateway shortName')



    @pytest.mark.parametrize('priority, gateway, tags', [
                    ('HIGH', 'cardboardfishmock', ['transaction', 'otp']),
                    ('BULK', 'valuefirstmock', ['campaign'])])
    def test_Create_And_Disable_DomainGatewayMap(self, priority, gateway, tags):
        dpgmID = self.nsadminHelper.configureGateway(priority, gateway, False, tags)
        dObj = self.nsObj.getDomainPropertiesGatewayMapByID(dpgmID)
        msgDict = {"messageClass" : "SMS", "priority" : priority, "message" : "test message with priority "+priority}
        resp  = self.nsadminHelper.createAndSendMessage(msgDict)
        Assertion.constructAssertion(resp > 0, 'sendMessage output')
        resp = self.nsObj.getMessagesById([resp])[0]
        Assertion.constructAssertion(resp.status in ['RECEIVED_IN_QUEUE', 'SENT'], 'Messages status')
        Assertion.constructAssertion(resp.gateway == dObj.gatewayOrgConfigs.shortName, 'gateway used for sending')
        Assertion.constructAssertion(resp.priority == priority, 'priority')  
        dpgmId = self.nsadminHelper.getDomainGatewayMapId(dObj.gatewayOrgConfigs.shortName)
        self.nsObj.disableDomainPropertiesGatewayMap(dpgmId)
        resp  = self.nsadminHelper.createAndSendMessage(msgDict)
        Assertion.constructAssertion(resp > 0, 'sendMessage output')
        resp = self.nsObj.getMessagesById([resp])[0]
        Assertion.constructAssertion(resp.status in ['GTW_NOT_FOUND'], 'Messages status')


    def test_Create_And_Disable_Domain(self):
        contactInfoList = self.nsadminHelper.getDefaultContactInfo('SMS')
        domainName = str(randValues.getRandomMobileNumber())+'_SMS_'+str(self.orgId)
        DomainProperties = {
            'orgId' : self.orgId,
            'domainName' : domainName,
            'description' : domainName,
            'contactInfo' : contactInfoList
        }      
        DomainProperties = NSAdminObject.domainProperties(DomainProperties)
        self.nsObj.insertDomainProperties(DomainProperties)
        domainPropertiesList = self.nsObj.getDomainPropertiesByOrg(self.orgId)
        for k in domainPropertiesList:
            if domainName == k.domainName and len(k.contactInfo) != 0:
                domainID = k.id
                contactInfoId0 = k.contactInfo[0].id
                contactInfoId1 = k.contactInfo[1].id
                break
        DomainProperties.contactInfo[0].value = '919845012346'
        DomainProperties.contactInfo[0].id = contactInfoId0
        DomainProperties.contactInfo[0].domainPropId = domainID
        DomainProperties.contactInfo[1].id = contactInfoId1  
        DomainProperties.contactInfo[1].domainPropId = domainID
        DomainProperties.id = domainID
        self.nsObj.updateDomainProperties(DomainProperties)          
        updatedDP = self.nsObj.getDomainPropertiesByID(domainID)
        Assertion.constructAssertion(updatedDP.contactInfo[0].value == '919845012346', 'updated value')
        self.nsObj.disableDomainProperties(domainID, self.orgId)
        deletedDP = self.nsObj.getDomainPropertiesByID(domainID)          
        Assertion.constructAssertion(deletedDP.domainName == None, 'Diasbled domain')            


'''

disable invalid domain id
update invalid doamin
add existing domain
'''