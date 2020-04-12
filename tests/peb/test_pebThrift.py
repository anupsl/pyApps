import pytest, time
from src.Constant.constant import constant
from src.utilities.logger import Logger
from src.utilities.assertion import Assertion
from src.utilities.utils import Utils
from src.modules.inTouchAPI.transaction import Transaction
from src.modules.inTouchAPI.customer import Customer
from src.modules.inTouchAPI.inTouchAPI import InTouchAPI

from src.modules.peb.pebObject import PEBObject
from src.modules.peb.pebHelper import PEBHelper
from src.modules.loyalty.loyaltyHelper import LoyaltyHelper


class Test_PEBThrift():
    
    def setup_class(self):
        Logger.logSuiteName(str(self).split('.')[-1])
        self.orgId = constant.config['orgId']
        self.programId = constant.config['programId']
        
    def setup_method(self, method):
        self.connObj = PEBHelper.getConnObj(newConnection=True)
        self.PERconnObj = LoyaltyHelper.getConnObj('pointsEngineRulesPort', newConnection=True)
        Logger.logMethodName(method.__name__)



    def test_getCustomerPointsSummariesByProgram(self):
        txObj = InTouchAPI(Transaction.Add())
        userId = txObj.response['response']['transactions']['transaction'][0]['customer']['user_id']
        custObj = PEBObject.CustomersData([int(userId)])
        self.connObj.getCustomerPointsSummariesByProgram(custObj)


    def test_getPointsExpiryRemindersInfo(self):
        startDate = Utils.getTime(days=-1,  milliSeconds=True)
        endDate = Utils.getTime(milliSeconds=True)
        obj = self.connObj.getPointsExpiryRemindersInfo(self.orgId, startDate, endDate)

    def test_executeTierDowngradeForOrgAtTime(self):
        billingTime = Utils.getTime(days=-120, dateTimeFormat=True)
        txBody = {
                "root": {
                    "transaction": {
                        "amount": "6000",
                        "billing_time": billingTime,
                        "gross_amount": "6000"      
                        }
                    }
                }
        txObj = InTouchAPI(Transaction.Add(body=txBody))
        custObj = InTouchAPI(Customer.Get({'mobile' : txObj.params['mobile']}))
        currentSlab = custObj.response['response']['customers']['customer'][0]['current_slab']
        Assertion.constructAssertion(currentSlab=='Gold', 'Current Slab Should be Gold before Tier Downgrade')
        firstDayofMonth = Utils.getFirstDayofMonth(milliSeconds=True)
        self.connObj.executeTierDowngradeForOrgAtTime(self.orgId, firstDayofMonth, True, True)
        custObj = InTouchAPI(Customer.Get({'mobile' : txObj.params['mobile']}))
        currentSlab = custObj.response['response']['customers']['customer'][0]['current_slab']
        Assertion.constructAssertion(currentSlab=='Silver', 'Current Slab Should be Silver after Tier Downgrade')

    def test_bulkAllocatePoints(self):
        customerId = constant.config['customerId']
        custObj = InTouchAPI(Customer.Get({'id' : customerId}))
        currentPoints = int(custObj.response['response']['customers']['customer'][0]['loyalty_points'])
        promotionId = constant.config['promotionInfoId']
        promotionInfo = self.PERconnObj.getPromotion(promotionId=promotionId, 
                            programId=self.programId, orgId=self.orgId)
        bulkAllocatePoints = PEBObject.BulkAllocatePointsData(promotionInfo=promotionInfo, customerIdList=[customerId])
        self.connObj.bulkAllocatePoints(bulkAllocatePoints=bulkAllocatePoints)
        custObj = InTouchAPI(Customer.Get({'id' : customerId}))
        latestPoints = int(custObj.response['response']['customers']['customer'][0]['loyalty_points'])
        Assertion.constructAssertion(latestPoints==currentPoints+100, '100 Points should be awarded')


