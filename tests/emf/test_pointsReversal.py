import pytest, time, random,re
from src.Constant.constant import constant
from src.utilities.logger import Logger
from src.utilities.assertion import Assertion
from src.utilities.utils import Utils
from src.modules.inTouchAPI.transaction import Transaction
from src.modules.inTouchAPI.customer import Customer
from src.modules.inTouchAPI.inTouchAPI import InTouchAPI
from src.utilities.randValues import randValues

from src.modules.peb.pebObject import PEBObject
from src.modules.loyalty.pointsEngineObject import PointsEngineObject
from src.modules.loyalty.emfObject import EMFObject
from src.modules.peb.pebHelper import PEBHelper
from src.modules.loyalty.loyaltyHelper import LoyaltyHelper
from src.modules.loyalty.loyaltyDBHelper import LoyaltyDBHelper


class Test_PointsReversal():

    def setup_class(self):
        Logger.logSuiteName(str(self).split('.')[-1])
        self.orgId = constant.config['orgId']
        self.programId = constant.config['programId']
        LoyaltyHelper.addTransaction()
        # self.emfObject = EMFObject()


    def setup_method(self, method):
        self.EMFConnObj = LoyaltyHelper.getConnObj('emfPort', newConnection=True)
        self.pointEngineConnObj = LoyaltyHelper.getConnObj('pointsEnginePort', newConnection=True)
        self.PEBConnObj = PEBHelper.getConnObj(newConnection=True)
        constant.config['serverReqId'] = 'emf_auto_' + str(random.randint(11111, 99999))
        # LoyaltyHelper.addTransaction()
        LoyaltyDBHelper.getBillNumber()
        # LoyaltyDBHelper.getCustomerPointsSummary()
        self.customerId = constant.config['usersInfo'][0]['userId']
        self.storeId = constant.config['storeIds'][0]
        constant.config['defaultRedeemPts'] = 10
        Logger.log('Printing Constant file: ', constant.config)
        Logger.logMethodName(method.__name__)


    @pytest.mark.parametrize('description, requestParams, errorDetails', [
        ('Points Reversal with org which not Enabled for reversal', {'orgID' : 0,'uniqueRedemptionId': randValues.randomString(8)}, [4101,'points redemption reversal is disabled for this org']),
        ('Points Reversal with invalid uniqueRedemptionId', {'uniqueRedemptionId': randValues.randomString(8)}, [3803,'prs record not found for the unique redemption id']),
        ('Points Reversal with negative pointsToBeReversed', {'pointsToBeReversed' : -10}, [4102,'points redemption reversal not allowed for invalid points']),
        ('Points Reversal with More than redeemed pointsToBeReversed', {'pointsToBeReversed' : 1000}, [3801,'points to be reversed should not be greater than total points redeemed against the redemption summary id']),
    ])
    def test_LYT_RED_REVERSE_01(self,description,requestParams,errorDetails):
        try:
            if requestParams.has_key('pointsToBeReversed'):
                ptsRedemptionObject = EMFObject.PointsRedemptionEventData({'customerID': constant.config['usersInfo'][0]['userId']})
                response = self.EMFConnObj.pointsRedemptionEvent(ptsRedemptionObject).__dict__
                requestParams.update({'uniqueRedemptionId': LoyaltyHelper.getInstructionsKeyValue(response, 'REDEEM', 'uniqueRedemptionId')})

            ptsReverseObject = EMFObject.PointsRedemptionReversalEventData(requestParams)
            response = self.EMFConnObj.pointsRedemptionReversalEvent(ptsReverseObject).__dict__
            Assertion.constructAssertion(False, 'Expected Exception {} and Actual: {}'.format(response, errorDetails))
        except Exception, exp:
            Logger.log(exp)
            exp = LoyaltyHelper.exceptionInstructorParser(exp.__dict__)
            Assertion.constructAssertion(errorDetails[1] in exp['errorMessage'], 'Error Message Actual: {} and Expected: {}'.format(exp['errorMessage'], errorDetails[1]))
            Assertion.constructAssertion(exp['statusCode'] == errorDetails[0], 'Status Code Actual: {} and Expected: {}'.format(exp['statusCode'], errorDetails[0]))

    @pytest.mark.parametrize('description, pointToReverse', [
        ('Points Reversal with addBill Id after redemption', 10)
    ])
    def test_LYT_RED_REVERSE_02(self,description, pointToReverse):
        uniqueRedemptionId = []
        redemptionId = []
        initialRedeemedPoints = LoyaltyDBHelper.getSumOfPointsAwarded(self.customerId)['sumOfRedeemedValue']
        noOfRedeem = 2
        for i in range(noOfRedeem):
            redeemPointsResponse = LoyaltyHelper.pointsRedemptionAndAssertion(self,pointToReverse, (initialRedeemedPoints + (i*pointToReverse)))
            uniqueRedemptionId.append(redeemPointsResponse['uniqueRedemptionId'])

        time.sleep(1)
        LoyaltyHelper.simplePropertiesParser(self.EMFConnObj.newBillEvent(EMFObject.NewBillEvent({'uniqueRedemptionId' : uniqueRedemptionId})).__dict__)
        prsDBDetails = LoyaltyDBHelper.getPointsRedemptionSummary(self.customerId, self.storeId, {'redemptionIds' : uniqueRedemptionId})
        Assertion.constructAssertion(len(prsDBDetails) == len(uniqueRedemptionId), 'No of Records added to prs Actual: {} and Expected: {}'.format(len(prsDBDetails), len(uniqueRedemptionId)))
        for prs in prsDBDetails:
            Assertion.constructAssertion(prs['billId'] == constant.config['billNumber'], 'RedemptionId updated to prs with BillId Actual: {} and Expected: {}'.format(prs['billId'], constant.config['billNumber']))
            Assertion.constructAssertion(prs['redemption_id'] in uniqueRedemptionId, 'Unique Redemption Id is match with BillIds Actual: {} and Expected: {}'.format(prs['redemption_id'], uniqueRedemptionId))
            Assertion.constructAssertion(prs['redemptionType'] == 'REDEMPTION', 'Redemption type is Matched Actual: {} and Expected: {}'.format(prs['redemptionType'], 'REDEMPTION'))
            redemptionId.append(prs['prs_id'])

        parsedResponse = LoyaltyHelper.redemptionReversalAndAssertion(self,[uniqueRedemptionId[0]])
        LoyaltyHelper.redemptionReversalDBAssertion(self, redemptionId, parsedResponse['redemptionReversalId'], (initialRedeemedPoints+pointToReverse))
        self.pointEngineConnObj.getPointsRedemptionSummaryForCustomer(self.orgId,self.customerId,True)

    @pytest.mark.parametrize('description', [
        ('Reverse all points and try to reverse again')
    ])
    def test_LYT_RED_REVERSE_03(self, description):
        initialRedeemedPoints = LoyaltyDBHelper.getSumOfPointsAwarded(self.customerId)['sumOfRedeemedValue']
        ptsRedemptionResponse = LoyaltyHelper.pointsRedemptionAndAssertion(self,constant.config['defaultRedeemPts'],initialRedeemedPoints)
        time.sleep(1)
        self.EMFConnObj.newBillEvent(EMFObject.NewBillEvent({'uniqueRedemptionId': ptsRedemptionResponse['uniqueRedemptionId']}))
        parsedResponse = LoyaltyHelper.redemptionReversalAndAssertion(self,[ptsRedemptionResponse['uniqueRedemptionId']])
        LoyaltyHelper.redemptionReversalDBAssertion(self, ptsRedemptionResponse['pointsRedemptionSummaryId'], parsedResponse['redemptionReversalId'], initialRedeemedPoints)
        LoyaltyHelper.redemptionReversalAndAssertion(self,[ptsRedemptionResponse['uniqueRedemptionId']], expectException=[3802,"all redeemed points already reversed"])

    @pytest.mark.parametrize('description, isValid', [
        ('Change redemptionId between the user and reverse the points', True)
    ])
    def test_LYT_RED_REVERSE_04(self,description, isValid):
        time.sleep(1)
        billId1 = LoyaltyHelper.simplePropertiesParser(self.EMFConnObj.newBillEvent(EMFObject.NewBillEvent()).__dict__)['sourceId']
        time.sleep(1)
        billId2 = LoyaltyHelper.simplePropertiesParser(self.EMFConnObj.newBillEvent(EMFObject.NewBillEvent({'customerID': constant.config['usersInfo'][1]['userId'], 'userDetails' : EMFObject.constructUserDetailsObject(1)})).__dict__)['sourceId']
        initialRedeemCus1 = LoyaltyDBHelper.getSumOfPointsAwarded(self.customerId)['sumOfRedeemedValue']
        uniqueRedemptionId1 = LoyaltyHelper.pointsRedemptionAndAssertion(self,constant.config['defaultRedeemPts'], initialRedeemCus1,{'redeemedOnBillId' : int(billId1)})['uniqueRedemptionId']
        self.customerId = constant.config['usersInfo'][1]['userId']
        initialRedeemCus1 = LoyaltyDBHelper.getSumOfPointsAwarded(self.customerId)['sumOfRedeemedValue']
        uniqueRedemptionId2 = LoyaltyHelper.pointsRedemptionAndAssertion(self,constant.config['defaultRedeemPts'], initialRedeemCus1,{'redeemedOnBillId' : int(billId2),'userDetails': EMFObject.constructUserDetailsObject(1)})['uniqueRedemptionId']
        LoyaltyHelper.redemptionReversalAndAssertion(self,uniqueRedemptionId1,{'userDetails': EMFObject.constructUserDetailsObject(1)}, [3803,'prs record not found for the unique redemption id'])
        self.customerId = constant.config['usersInfo'][0]['userId']
        LoyaltyHelper.redemptionReversalAndAssertion(self,uniqueRedemptionId2, expectException=[3803,'prs record not found for the unique redemption id'])



    @pytest.mark.parametrize('description, pointsToBeReversed', [
        ('Partial Points reversal from redemption', 6),
    ])
    def test_LYT_RED_REVERSE_05(self,description, pointsToBeReversed):
        time.sleep(1)
        billId = int(LoyaltyHelper.simplePropertiesParser(self.EMFConnObj.newBillEvent(EMFObject.NewBillEvent()).__dict__)['sourceId'])
        initialRedeemedPoints = LoyaltyDBHelper.getSumOfPointsAwarded(self.customerId)['sumOfRedeemedValue']
        redemptionId = []
        uniqueRedemptionId = LoyaltyHelper.pointsRedemptionAndAssertion(self, constant.config['defaultRedeemPts'], initialRedeemedPoints, {'redeemedOnBillId' : billId})['uniqueRedemptionId']
        prsDBDetails = LoyaltyDBHelper.getPointsRedemptionSummary(self.customerId, self.storeId, {'redemptionIds': uniqueRedemptionId})
        Assertion.constructAssertion(len(prsDBDetails) == len([uniqueRedemptionId]), 'No of Records added to prs Actual: {} and Expected: {}'.format(len(prsDBDetails), len(uniqueRedemptionId)))
        for prs in prsDBDetails:
            Assertion.constructAssertion(prs['billId'] == billId, 'RedemptionId updated to prs with BillId Actual: {} and Expected: {}'.format(prs['billId'], billId))
            Assertion.constructAssertion(prs['redemption_id'] in uniqueRedemptionId, 'Unique Redemption Id is match with BillIds Actual: {} and Expected: {}'.format(prs['redemption_id'], uniqueRedemptionId))
            Assertion.constructAssertion(prs['redemptionType'] == 'REDEMPTION', 'Redemption type is Matched Actual: {} and Expected: {}'.format(prs['redemptionType'], 'REDEMPTION'))
            redemptionId.append(prs['prs_id'])
        parsedResponse = LoyaltyHelper.redemptionReversalAndAssertion(self, [uniqueRedemptionId], {'pointsToBeReversed': pointsToBeReversed})
        LoyaltyHelper.redemptionReversalDBAssertion(self,redemptionId,parsedResponse['redemptionReversalId'],initialRedeemedPoints,pointsToBeReversed)



    @pytest.mark.parametrize('description', [('Points Reversal using reversed uniqueRedemptionId')])
    def test_LYT_RED_REVERSE_06(self,description):
        redemptionId = []
        initialRedeemedPoints = LoyaltyDBHelper.getSumOfPointsAwarded(self.customerId)['sumOfRedeemedValue']
        uniqueRedemptionId = LoyaltyHelper.pointsRedemptionAndAssertion(self,constant.config['defaultRedeemPts'],initialRedeemedPoints,{'redeemedOnBillId' : -1})['uniqueRedemptionId']


        prsDBDetails = LoyaltyDBHelper.getPointsRedemptionSummary(self.customerId, self.storeId, {'redemptionIds': uniqueRedemptionId})
        Assertion.constructAssertion(len(prsDBDetails) == len([uniqueRedemptionId]), 'No of Records added to prs Actual: {} and Expected: {}'.format(len(prsDBDetails), len(uniqueRedemptionId)))
        for prs in prsDBDetails:
            Assertion.constructAssertion(prs['billId'] == -1, 'RedemptionId updated to prs with BillId Actual: {} and Expected: {}'.format(prs['billId'], constant.config['billNumber']))
            Assertion.constructAssertion(prs['redemption_id'] in uniqueRedemptionId, 'Unique Redemption Id is match with BillIds Actual: {} and Expected: {}'.format(prs['redemption_id'], uniqueRedemptionId))
            Assertion.constructAssertion(prs['redemptionType'] == 'REDEMPTION', 'Redemption type is Matched Actual: {} and Expected: {}'.format(prs['redemptionType'], 'REDEMPTION'))
            redemptionId.append(prs['prs_id'])

        parsedResponse = LoyaltyHelper.redemptionReversalAndAssertion(self, [uniqueRedemptionId])
        LoyaltyHelper.redemptionReversalDBAssertion(self, redemptionId, parsedResponse['redemptionReversalId'], initialRedeemedPoints)
        LoyaltyHelper.redemptionReversalAndAssertion(self,listOfRedemptionId=[parsedResponse['redemptionReversalId']],expectException=[3804,'redemption reversal of a reversal not allowed'])


    @pytest.mark.parametrize('description', ['Point Reversal on return'])
    def est_LYT_RED_REVERSE_RETURN_18(self,description):
        usr = constant.config['usersInfo'][1]
        Logger.log("User Info: ", usr)
        time.sleep(30)
        res  = InTouchAPI(Transaction.Add(body={'customer': {'mobile': usr['mobile'], 'email': usr['email'], 'external_id': usr['externalId']}}, mobile=usr['mobile']))
        x = res.response['response']['transactions']['transaction']
        Logger.log(x)
        billId = None
        for i in x:
            Logger.log(i['id'])
            billId = i['id']
        # # Logger.log(usr)
        # uniqueRedemptionId = None
        # newBillObj = {'customerID' : constant.config['usersInfo'][0]['userId']}
        # self.EMFConnObj.newBillEvent(EMFObject.NewBillEvent(newBillObj))
        #
        # initialRedeemedPoints = EMFDBHelper.getSumOfPointsAwarded(self.customerId)['sumOfRedeemedValue']
        # uniqueRedemptionId = LoyaltyHelper.pointsRedemptionAndAssertion(self,constant.config['defaultRedeemPts'],initialRedeemedPoints,{'redeemedOnBillId' : billId})['uniqueRedemptionId']
        # parsedResponse = LoyaltyHelper.redemptionReversalAndAssertion(self, [uniqueRedemptionId], paramDict={'userDetails' : EMFObject.constructUserDetailsObject(1)})
        time.sleep(30)
        # lineItemId = EMFDBHelper.getLineItemIds(self.customerId,billId)[1]
        # rtObj = EMFObject.ReturnBillLineitemsEventData({'returnBillID' : billId,'returnLineItem': {'id': lineItemId['lineItemId'], 'qty': 10}, 'customerID' : self.customerId})
        # self.EMFConnObj.returnLineitemsEvent(rtObj)
        rtObj = EMFObject.ReturnBillAmountEventData({'returnBillID' : billId, 'customerID' : usr['userId'], 'returnAmount' : 200, 'userDetails': EMFObject.constructUserDetailsObject(1)})
        self.EMFConnObj.returnBillAmountEvent(rtObj)
        # data = EMFDBHelper.getSumOfPointsAwarded(self.customerId)
        # Logger.log('After return ',  data)
