import time, pytest
from datetime import datetime, timedelta
from src.Constant.constant import constant
from src.utilities.logger import Logger
from src.modules.darknight.darknightThrift import DarknightThrift
from src.modules.darknight.darknightHelper import DarknightHelper
from src.modules.inTouchAPI.customer import Customer
from src.modules.inTouchAPI.inTouchAPI import InTouchAPI
from src.modules.iris.list import campaignList
from src.utilities.assertion import Assertion


@pytest.mark.skipif(constant.config['cluster'] not in ['nightly', 'staging'], reason='Test only for Nightly, Staging')
class Test_SMS_Whitelisting():
    
    def setup_class(self):
        Logger.logSuiteName(str(self).split('.')[-1])
        self.mobile1 = '918660430751'
        self.mobile2 = '918660430752'
        DarknightHelper.getMongoConnection('whitelisting', 'mobile_status')
        self.monthList = DarknightHelper.monthlyDelta()
        self.orgId = constant.config['orgId']

    def setup_method(self, method):
        self.dnObj = DarknightHelper.getConnObj(newConnection=True)
        Logger.logMethodName(str(method.__name__))


    def test_getNonExistantNumber(self):
        resObj = self.dnObj.getMobileStatus(['12304567890'], self.orgId)
        Assertion.constructAssertion(resObj == {'12304567890' : True}, 'Verifying not existing number')
        resObj = self.dnObj.getMobileStatus(['invalid'], self.orgId)
        Assertion.constructAssertion(resObj == {'invalid' : True}, 'Verifying invalid number')

### count less than 3
    # 00 with last_failed_on less then 2 months and attempts less thans 3 
    def test_countLessThan3_case1(self):
        DarknightHelper.generateSmsWhitelistingData({'not_delivered' : 2, 
            'last_failed_on' : self.monthList[0]})
        resObj = self.dnObj.getMobileStatus([self.mobile1], self.orgId)
        Assertion.constructAssertion(resObj == {self.mobile1 : True}, 'Verifying 00')

    # 00 with last_failed_on greater then 2 months and attempts less thans 3 
    def test_countLessThan3_case2(self):
        DarknightHelper.generateSmsWhitelistingData({'not_delivered' : 2, 
            'last_failed_on' : self.monthList[2]})
        resObj = self.dnObj.getMobileStatus([self.mobile1], self.orgId)
        Assertion.constructAssertion(resObj == {self.mobile1 : True}, 'Verifying 00')

    # 01 with last_success_on less then 2 months and attempts less thans 3 
    def test_countLessThan3_case3(self):
        last_success_on = self.monthList[0]
        last_failed_on = self.monthList[0] - timedelta(days=1)
        DarknightHelper.generateSmsWhitelistingData({'not_delivered' : 1, 'delivered' : 1, 
            'last_success_on' : last_success_on, 'last_failed_on' : last_failed_on})
        resObj = self.dnObj.getMobileStatus([self.mobile1], self.orgId)
        Assertion.constructAssertion(resObj == {self.mobile1 : True}, 'Verifying 00')

    # 01 with last_success_on greater then 2 months and attempts less thans 3 
    def test_countLessThan3_case3(self):
        last_success_on = self.monthList[2]
        last_failed_on = self.monthList[2] - timedelta(days=2)
        DarknightHelper.generateSmsWhitelistingData({'not_delivered' : 1, 'delivered' : 1, 
            'last_success_on' : last_success_on, 'last_failed_on' : last_failed_on})
        resObj = self.dnObj.getMobileStatus([self.mobile1], self.orgId)
        Assertion.constructAssertion(resObj == {self.mobile1 : True}, 'Verifying 01')


#### count greater than 3
    # 0001 with last_success_on less then 2 months with p < 0.3
    def test_countGreaterThan3_case4(self):
        last_success_on = self.monthList[0]
        last_failed_on = self.monthList[0] - timedelta(days=2)        
        DarknightHelper.generateSmsWhitelistingData({'delivered' : 1, 'not_delivered' : 3, 
            'last_success_on' : last_success_on, 'last_failed_on' : last_failed_on})
        resObj = self.dnObj.getMobileStatus([self.mobile1], self.orgId)
        Assertion.constructAssertion(resObj == {self.mobile1 : True}, 'Verifying 0001')

    # 0001 with last_success_on greater then 2 months with p < 0.3
    def test_countGreaterThan3_case5(self):        
        last_success_on = self.monthList[2]
        last_failed_on = self.monthList[2] - timedelta(days=2)        
        DarknightHelper.generateSmsWhitelistingData({'delivered' : 1, 'not_delivered' : 3, 
            'last_success_on' : last_success_on, 'last_failed_on' : last_failed_on})
        resObj = self.dnObj.getMobileStatus([self.mobile1], self.orgId)
        Assertion.constructAssertion(resObj == {self.mobile1 : True}, 'Verifying 0001')

    # 0000 with last_failed_on less then 2 months with p < 0.3                
    def test_countGreaterThan3_case6(self):        
        last_failed_on = self.monthList[0]
        DarknightHelper.generateSmsWhitelistingData({
            'not_delivered' : 4, 
            'last_failed_on' : last_failed_on,
            "monthly_stats": [{"year": last_failed_on.year, "month": last_failed_on.month, 
                            "not_delivered": 4, "total": 4}]})
        resObj = self.dnObj.getMobileStatus([self.mobile1], self.orgId)
        Assertion.constructAssertion(resObj == {self.mobile1 : False}, 'Verifying 0000')

    # 0000 with data more than 6 months              
    def test_countGreaterThan3DataMoreThan6Months_case6(self):        
        last_failed_on1 = self.monthList[0]
        last_failed_on8 = self.monthList[7]
        DarknightHelper.generateSmsWhitelistingData({
            'not_delivered' : 4, 
            'last_failed_on' : last_failed_on1,
            "monthly_stats": [
            {"year": last_failed_on1.year, "month": last_failed_on1.month, "not_delivered": 2, "total": 2},
            {"year": last_failed_on8.year, "month": last_failed_on8.month, "not_delivered": 2, "total": 2}]})
        resObj = self.dnObj.getMobileStatus([self.mobile1], self.orgId)
        Assertion.constructAssertion(resObj == {self.mobile1 : False}, 'Verifying 0000')        

    # 0000 with last_failed_on greater then 2 months with p < 0.3
    def test_countGreaterThan3_case7(self):
        last_failed_on = self.monthList[2] - timedelta(days=2)            
        DarknightHelper.generateSmsWhitelistingData({'not_delivered' : 4, 
            'last_failed_on' : last_failed_on})
        resObj = self.dnObj.getMobileStatus([self.mobile1], self.orgId)
        Assertion.constructAssertion(resObj == {self.mobile1 : True}, 'Verifying 0000')


    # 1101 with last_success_on less then 2 months with p > 0.7
    def test_countGreaterThan3_case8(self):
        last_success_on = self.monthList[1]
        last_failed_on = self.monthList[1] - timedelta(days=2)            
        DarknightHelper.generateSmsWhitelistingData({'delivered' : 3, 'not_delivered' : 1, 
            'last_success_on' : last_success_on, 'last_failed_on' : last_failed_on})
        resObj = self.dnObj.getMobileStatus([self.mobile1], self.orgId)
        Assertion.constructAssertion(resObj == {self.mobile1 : True}, 'Verifying 1101')

    # 1101 with last_success_on greater then 2 months with p > 0.7
    def test_countGreaterThan3_case9(self):        
        DarknightHelper.generateSmsWhitelistingData({'delivered' : 3, 'not_delivered' : 1, 
            'last_success_on' : self.monthList[2],
            'last_failed_on' : self.monthList[2] - timedelta(days=2)})
        resObj = self.dnObj.getMobileStatus([self.mobile1], self.orgId)
        Assertion.constructAssertion(resObj == {self.mobile1 : True}, 'Verifying 1101')

    # 1110 with last_failed_on less then 2 months with p > 0.7                
    def test_countGreaterThan3_case10(self):
        last_failed_on = self.monthList[0]     
        DarknightHelper.generateSmsWhitelistingData({
            'delivered' : 3, 
            'not_delivered' : 1, 
            'last_failed_on' : last_failed_on,
            "monthly_stats": [{
                "year": last_failed_on.year, 
                "month": last_failed_on.month, 
                'delivered' : 3, 
                "not_delivered": 1, 
                "total": 4}]})
        resObj = self.dnObj.getMobileStatus([self.mobile1], self.orgId)
        Assertion.constructAssertion(resObj == {self.mobile1 : True}, 'Verifying 1110')

    # 1110 with last_failed_on greater then 2 months with p > 0.7
    def test_countGreaterThan3_case11(self):        
        DarknightHelper.generateSmsWhitelistingData({'delivered' : 3, 'not_delivered' : 1, 
            'last_failed_on' : self.monthList[2]})
        resObj = self.dnObj.getMobileStatus([self.mobile1], self.orgId)
        Assertion.constructAssertion(resObj == {self.mobile1 : True}, 'Verifying 1110')


    # 1111000001 p < 0.7 with last_success_on less then 2 months 
    def test_countGreaterThan3_case12(self):        
        DarknightHelper.generateSmsWhitelistingData({'not_delivered' : 5, 'delivered' : 5, 
            'last_failed_on' : self.monthList[1], 'last_success_on' : self.monthList[0]})
        resObj = self.dnObj.getMobileStatus([self.mobile1], self.orgId)
        Assertion.constructAssertion(resObj == {self.mobile1 : True}, 'Verifying 1111000001')

    # 1111000001 p < 0.7 with last_success_on greater then 2 months  
    def test_countGreaterThan3_case13(self):        
        DarknightHelper.generateSmsWhitelistingData({'not_delivered' : 5, 'delivered' : 5, 
            'last_failed_on' : self.monthList[2] - timedelta(days=2), 
            'last_success_on' : self.monthList[2]})
        resObj = self.dnObj.getMobileStatus([self.mobile1], self.orgId)
        Assertion.constructAssertion(resObj == {self.mobile1 : True}, 'Verifying 1111000001')

    # 1111000010 p < 0.7 with last_failed_on less then 2 months
    def test_countGreaterThan3_case14(self):
        last_failed_on = self.monthList[0]        
        DarknightHelper.generateSmsWhitelistingData({
            'not_delivered' : 5, 
            'delivered' : 5, 
            'last_failed_on' : last_failed_on, 
            'last_success_on' : self.monthList[0] - timedelta(days=2),
            "monthly_stats": [{
                "year": last_failed_on.year, 
                "month": last_failed_on.month, 
                "not_delivered": 5,
                "delivered": 5, 
                "total": 10}]})
        resObj = self.dnObj.getMobileStatus([self.mobile1], self.orgId)
        Assertion.constructAssertion(resObj == {self.mobile1 : False}, 'Verifying 1111000010')

    # 1111000010 p < 0.7 with last_failed_on greater then 2 months  
    def test_countGreaterThan3_case15(self):        
        DarknightHelper.generateSmsWhitelistingData({'not_delivered' : 5, 'delivered' : 5, 
            'last_failed_on' : self.monthList[2], 
            'last_success_on' : self.monthList[2] - timedelta(days=2)})
        resObj = self.dnObj.getMobileStatus([self.mobile1], self.orgId)
        Assertion.constructAssertion(resObj == {self.mobile1 : True}, 'Verifying 1111000010')



    # 1111111101 p > 0.7 with last_success_on less then 2 months 
    def test_countGreaterThan3_case16(self):        
        DarknightHelper.generateSmsWhitelistingData({'not_delivered' : 1, 'delivered' : 9, 
            'last_failed_on' : self.monthList[0] - timedelta(days=2), 
            'last_success_on' : self.monthList[0]})
        resObj = self.dnObj.getMobileStatus([self.mobile1], self.orgId)
        Assertion.constructAssertion(resObj == {self.mobile1 : True}, 'Verifying 1111111101')

    # 1111111101 p > 0.7 with last_success_on greater then 2 months 
    def test_countGreaterThan3_case17(self):        
        DarknightHelper.generateSmsWhitelistingData({'not_delivered' : 1, 'delivered' : 9, 
            'last_failed_on' : self.monthList[2] - timedelta(days=1), 'last_success_on' : self.monthList[2]})
        resObj = self.dnObj.getMobileStatus([self.mobile1], self.orgId)
        Assertion.constructAssertion(resObj == {self.mobile1 : True}, 'Verifying 1111111101')

    # 1111111100 p > 0.7 with last_failed_on greater then 2 months 
    def test_countGreaterThan3_case18(self):        
        DarknightHelper.generateSmsWhitelistingData({'not_delivered' : 2, 'delivered' : 8, 
            'last_failed_on' : self.monthList[2], 'last_success_on' : self.monthList[2] - timedelta(days=1)})
        resObj = self.dnObj.getMobileStatus([self.mobile1], self.orgId)
        Assertion.constructAssertion(resObj == {self.mobile1 : True}, 'Verifying 1111111100')

    # 1111111100 p > 0.7 with last_failed_on less then 2 months
    def test_countGreaterThan3_case19(self):        
        last_failed_on = self.monthList[0]
        DarknightHelper.generateSmsWhitelistingData({
            'not_delivered' : 2, 
            'delivered' : 8, 
            'last_failed_on' : self.monthList[0], 
            'last_success_on' : self.monthList[0] - timedelta(days=1),
            "monthly_stats": [{
                "year": last_failed_on.year, 
                "month": last_failed_on.month, 
                "not_delivered": 2,
                "not_delivered": 8, 
                "total": 10}]})
        resObj = self.dnObj.getMobileStatus([self.mobile1], self.orgId)
        Assertion.constructAssertion(resObj == {self.mobile1 : False}, 'Verifying 1111111100')


    # prob spread across month 10 10 10 10 011111 110111 111110 
    def test_probCheck_case21(self):        
        DarknightHelper.generateSmsWhitelistingData({
            'not_delivered' : 7, 
            'delivered' : 19, 
            'last_failed_on' : self.monthList[0], 
            'last_success_on' : self.monthList[0] - timedelta(days=1),
            "monthly_stats": [{
                "year": self.monthList[0].year, "month": self.monthList[0].month, 
                "not_delivered": 1, "delivered": 5, "total": 6},{
                "year": self.monthList[1].year, "month": self.monthList[1].month, 
                "not_delivered": 1, "delivered": 5, "total": 6}, {
                "year": self.monthList[2].year, "month": self.monthList[2].month, 
                "not_delivered": 1, "delivered": 5, "total": 6},{
                "year": self.monthList[3].year, "month": self.monthList[3].month, 
                "not_delivered": 1, "delivered": 1, "total": 2}, {
                "year": self.monthList[4].year, "month": self.monthList[4].month, 
                "not_delivered": 1, "delivered": 1, "total": 2},{
                "year": self.monthList[5].year, "month": self.monthList[5].month, 
                "not_delivered": 1, "delivered": 1, "total": 2}, {
                "year": self.monthList[6].year, "month": self.monthList[6].month, 
                "not_delivered": 1, "delivered": 1, "total": 2}
            ]})
        resObj = self.dnObj.getMobileStatus([self.mobile1], self.orgId)
        Assertion.constructAssertion(resObj[self.mobile1] ==  True, 'Verifying 10 10 10 10 011111 110111 111110 - 71%')


    # prob spread across month 10 10 111110 & mobile with 000
    def test_probCheck_case20(self):        
        DarknightHelper.generateSmsWhitelistingData({
            'not_delivered' : 3, 
            'delivered' : 7, 
            'last_failed_on' : self.monthList[0], 
            'last_success_on' : self.monthList[0] - timedelta(hours=2),
            "monthly_stats": [{
                "year": self.monthList[0].year, "month": self.monthList[0].month, 
                "not_delivered": 1, "delivered": 5, "total": 6}, {
                "year": self.monthList[1].year, "month": self.monthList[1].month, 
                "not_delivered": 1, "delivered": 1, "total": 2}, {
                "year": self.monthList[2].year, "month": self.monthList[2].month, 
                "not_delivered": 1, "delivered": 1, "total": 2}
            ]})
        DarknightHelper.generateSmsWhitelistingData({'not_delivered' : 3,
            'last_failed_on' : self.monthList[0]}, self.mobile2)        
        resObj = self.dnObj.getMobileStatus([self.mobile1, self.mobile2], self.orgId)
        Assertion.constructAssertion(resObj[self.mobile1] == False, 'Verifying 10 10 111110 62%')
        Assertion.constructAssertion(resObj[self.mobile2] ==  True, 'Verifying 000')
        

