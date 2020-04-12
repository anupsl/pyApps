import traceback,random, time,  json,re
from src.utilities.logger import Logger
from src.Constant.constant import constant
from src.modules.loyalty.emfThrift import EMFThrift
from src.modules.loyalty.pointsEngineThrift import PointsEngineThrift
from src.modules.loyalty.pointsEngineRulesThrift import PointsEngineRulesThrift
from src.modules.loyalty.nrulesThrift import NrulesThrift
from src.modules.loyalty.datamanagerThrift import DatamanagerThrift
from src.modules.inTouchAPI.transaction import Transaction
from src.modules.inTouchAPI.inTouchAPI import InTouchAPI
from src.utilities.assertion import Assertion

from src.utilities.utils import Utils
from src.modules.loyalty.loyaltyDBHelper import LoyaltyDBHelper
from src.modules.loyalty.emfObject import EMFObject
from src.utilities.dbhelper import dbHelper


class LoyaltyHelper():

    @staticmethod
    def checkEMFConn(ignoreConnectionError=False):
        Utils.checkServerConnection('EMF_THRIFT_SERVICE', EMFThrift, 'emfPort', ignoreConnectionError)

    @staticmethod
    def getConnObj(portName, newConnection=False):
        port = constant.config['emfPort'].next()
        if portName == 'pointsEnginePort':
            connPort = str(port)+'_peobj'
        elif portName == 'pointsEngineRulesPort':
            connPort = str(port)+'_perobj'            
        elif portName == 'nrulesPort':
            connPort = str(port)+'_nobj'
        elif portName == 'datamanagerPort':
            connPort = str(port)+'_dobj'            
        else:
            connPort = str(port)+'_obj'
        if newConnection and connPort in constant.config:
            constant.config[connPort].close()
        if not connPort in constant.config or newConnection:
            if portName == 'emfPort':
                constant.config[connPort] = EMFThrift(port)
            elif portName == 'pointsEnginePort':
                constant.config[connPort] = PointsEngineThrift(port)
            elif portName == 'pointsEngineRulesPort':
                constant.config[connPort] = PointsEngineRulesThrift(port)
            elif portName == 'nrulesPort':
                constant.config[connPort] = NrulesThrift(port)
            elif portName == 'datamanagerPort':
                constant.config[connPort] = DatamanagerThrift(port)
        return constant.config[connPort]


    @staticmethod
    def disableExistingPromotions(programId, orgId):
        perConnObj = LoyaltyHelper.getConnObj('pointsEngineRulesPort')
        prgInfoList = perConnObj.getPromotionsByProgramId(programId=programId, orgId=orgId)
        for pInfo in prgInfoList:
            if pInfo.isActive == True:
                pInfo.isActive = False
                perConnObj.createOrUpdatePromotion(pInfo, programId, orgId, 1, Utils.getTime())

    @staticmethod
    def disableTierDowngrade(orgId, programId):
        perConnObj = LoyaltyHelper.getConnObj('pointsEngineRulesPort')
        tierDowngrad = perConnObj.getAllStrategiesByStrategyTypeId(programId, orgId, 5)
        if tierDowngrad != []:
            sInfo = tierDowngrad[0]
            sInfo.propertyValues = json.dumps({"isActive":"false"})
            sInfo.owner = 'LOYALTY'
            perConnObj.createOrUpdateStrategy(sInfo, programId, orgId, -1, Utils.getTime())

    @staticmethod
    def deleteAllRules(orgId, programId):
        nConnObj = LoyaltyHelper.getConnObj('nrulesPort')        
        ruleSetList = nConnObj.getConfiguredRulesets(orgId, 0, 'POINTSENGINE_ENDPOINT')
        for ruleSet in ruleSetList:
            for rules in ruleSet.rules:
                if hasattr(rules,'isActive'):
                    if rules.isActive == True:
                        rules.isActive = False
                        nConnObj.editRuleset(orgId, ruleSet.name, ruleSet, 'POINTSENGINE_ENDPOINT')

    @staticmethod
    def reconfigure(orgId, programId):
        nConnObj = LoyaltyHelper.getConnObj('nrulesPort')
        return nConnObj.reconfigureOrganization(orgId, 1, 'POINTSENGINE_ENDPOINT', programId)

    @staticmethod
    def reset(orgId, programId):
        LoyaltyHelper.deleteAllRules(orgId, programId)
        LoyaltyHelper.disableExistingPromotions(programId, orgId)
        LoyaltyHelper.disableTierDowngrade(orgId, programId)

    @staticmethod
    def getLoyaltyUsers(noOfUsers = 5):
        LoyaltyDBHelper.getUsers(noOfUsers)
        LoyaltyDBHelper.getActiveStoreIdList()

    @staticmethod
    def addTransaction():
        LoyaltyHelper.getLoyaltyUsers()
        billNumber = 'AutomationTest' + str(int(time.time() * 100000))
        Transaction.Add(body={'customer': {'mobile': '', 'email': '', 'external_id': ''}}, mobile='')
        responseList = []
        for usr in constant.config['usersInfo']:
            responseList.append(InTouchAPI(Transaction.Add(body={"number": billNumber,
                                                'customer': {'mobile': usr['mobile'], 'email': usr['email'], 'external_id': usr['externalId']}},
                                                mobile=usr['mobile'])).response)
        return responseList

    @staticmethod
    def getInstructionsKeyValue(instructionList, mnemonicKey, simplePropKey):
        value = ''
        for instruction in instructionList['instructions']:
            tmpDict = instruction.__dict__
            if tmpDict['mnemonic'] == mnemonicKey:
                for simProp in tmpDict['simpleProperties']:
                    prop = simProp.__dict__
                    if prop['key'] == simplePropKey:
                        return prop['value']

    @staticmethod
    def exceptionInstructorParser(expInstruction):
        tmpList = []
        exceptionMsg = []
        tmpKeyStr = ''
        if 'EndpointEventStatus' not in expInstruction['errorMessage']:
            return expInstruction
        endPointStatus = expInstruction['errorMessage'].split('EndpointEventStatus ')
        y = list(endPointStatus)
        for k in y:
            j = (k.split(','))
            for f in j:
                s = f.split('=')
                if len(s) != 1:
                    key = re.sub('^\[|^ ', "", s[0])
                    value = re.sub("\]$|\\n| $", "", s[1])
                    if 'exception' == key: exceptionMsg.append(value)
                    tmpList.append({key : value})
        return {'errorMessage' : exceptionMsg, 'replayErrorCode' :  expInstruction['replayErrorCode'], 'statusCode' : expInstruction['statusCode'], 'parsedMsgList' : tmpList}

    @staticmethod
    def simplePropertiesParser(eventResponse):
        tmpDict = {'instructionType' : []}
        for x in eventResponse['instructions']:
            y = x.__dict__
            tmpDict['instructionType'].append(y['mnemonic'])
            for l in y['simpleProperties']:
                m = l.__dict__
                if  m['key'] == 'points':
                    tmpDict.update({m['key']: float(m['value']) if not tmpDict.has_key('points') else (tmpDict[m['key']] + float(m['value']))})
                else:
                    tmpDict.update({m['key'] : m['value']})
        Logger.log(tmpDict)
        return tmpDict

    @staticmethod
    def redemptionReversalAndAssertion(self,listOfRedemptionId, paramDict = {}, expectException = None):
        time.sleep(2)
        ptsReversalResponse = None
        pointsToReverse = constant.config['defaultRedeemPts'] if not paramDict.has_key('pointsToBeReversed') else paramDict['pointsToBeReversed']
        try:
            for redemptionId in listOfRedemptionId:
                paramDict.update({'uniqueRedemptionId': redemptionId})
                ptsReverseObject = EMFObject.PointsRedemptionReversalEventData(paramDict)
                ptsReversalResponse = LoyaltyHelper.simplePropertiesParser(self.EMFConnObj.pointsRedemptionReversalEvent(ptsReverseObject).__dict__)
                Assertion.constructAssertion('POINTS_REDEMPTION_REVERSAL' in ptsReversalResponse['instructionType'], 'POINTS_REDEMPTION_REVERSAL Instruction not executed in points reversal')
                Assertion.constructAssertion(float(ptsReversalResponse['pointsToBeReversed']) == pointsToReverse, 'Redemption Points Reversed is Matched Actual: {} and Expected: {}'.format(ptsReversalResponse['pointsToBeReversed'], pointsToReverse))
                Assertion.constructAssertion(int(ptsReversalResponse['userId']) == self.customerId, 'Redemption Points Reversed again userid is Matched Actual: {} and Expected: {}'.format(ptsReversalResponse['userId'], self.customerId))
                Assertion.constructAssertion(ptsReversalResponse['redemptionId'] == redemptionId, 'Redemption Points Reversed on redemptionId is Matched Actual: {} and Expected: {}'.format(ptsReversalResponse['redemptionId'], redemptionId))
            return ptsReversalResponse
        except Exception, exp:
            excParsed = LoyaltyHelper.exceptionInstructorParser(exp.__dict__)
            if expectException != None:
                Assertion.constructAssertion(expectException[1] in excParsed['errorMessage'], 'Error Message Actual: {} and Expected: {}'.format(excParsed['errorMessage'], expectException[1]))
                Assertion.constructAssertion(excParsed['statusCode'] == expectException[0], 'Status Code Actual: {} and Expected: {}'.format(excParsed['statusCode'], expectException[0]))
            else:
                Assertion.constructAssertion(False, 'Unexpected Exception: {}'.format(exp))

    @staticmethod
    def redemptionReversalDBAssertion(self, redemptionId, redemptionReversalId, initialRedeemedPoint, pointsReversed = 10):
        reversalDBDetails = LoyaltyDBHelper.getPointsRedemptionSummary(self.customerId, self.storeId, {'redemptionIds':redemptionReversalId})
        Assertion.constructAssertion(len(reversalDBDetails) != 0, 'Redemption Reversal Record is not Empty')
        reversalIds = None
        for reversalDetails in reversalDBDetails:
            Assertion.constructAssertion(reversalDetails['redemptionType'] == 'REVERSAL', 'Redemption type is Matched Actual: {} and Expected: {}'.format(reversalDetails['redemptionType'], 'REVERSAL'))
            Assertion.constructAssertion(reversalDetails['points_redeemed'] == pointsReversed, 'Points reversed & recorded in prs Actual: {} and Expected: {}'.format(reversalDetails['points_redeemed'], pointsReversed))
            reversalIds = reversalDetails['prs_id']

        reversalMappingDB = LoyaltyDBHelper.getRedemptionReversal(redemptionId, reversalIds)
        Assertion.constructAssertion(reversalMappingDB['reversedPoints'] == (pointsReversed), 'Points reversed is Matched Actual: {} and Excepted: {}'.format(reversalMappingDB['reversedPoints'], pointsReversed))
        LoyaltyHelper.assertOnSumOfPoints(self, initialRedeemedPoint + (constant.config['defaultRedeemPts'] - pointsReversed))

    @staticmethod
    def assertOnSumOfPoints(self, expectedRedeemedPoint):
        redeemedPoints = LoyaltyDBHelper.getSumOfPointsAwarded(self.customerId)['sumOfRedeemedValue']
        Logger.log(redeemedPoints,  ' And it type : ', type(redeemedPoints), ' --- And expected point : ', expectedRedeemedPoint, '   And its type:   ' ,type(expectedRedeemedPoint))
        Logger.log(float(redeemedPoints) == float(expectedRedeemedPoint))
        Assertion.constructAssertion(float(redeemedPoints) == float(expectedRedeemedPoint), 'Points Redeemed sum in PA table is Mathced Actual: {} and Expected: {}'.format(redeemedPoints, expectedRedeemedPoint))
        return redeemedPoints

    @staticmethod
    def pointsRedemptionAndAssertion(self,pointsToRedeem, initialRedeemedPoints, paramDict = {}):
        time.sleep(2)
        tmpDict = {'customerID' : self.customerId, 'eventTimeInMillis': Utils.getTime(seconds=(random.randint(0,9)),milliSeconds=True), 'numPointsToBeRedeemed' : pointsToRedeem}
        tmpDict.update(paramDict)
        ptsRedemptionObject = EMFObject.PointsRedemptionEventData(tmpDict)
        redeemPointsResponse = LoyaltyHelper.simplePropertiesParser(self.EMFConnObj.pointsRedemptionEvent(ptsRedemptionObject).__dict__)
        Assertion.constructAssertion(redeemPointsResponse['uniqueRedemptionId'] != None, 'Unique Redemption Id is not Empty Actual: {}'.format(redeemPointsResponse['uniqueRedemptionId']))
        Assertion.constructAssertion(int(redeemPointsResponse['numPoints']) == pointsToRedeem, 'Redeemed points Actual: {} and Expected: {}'.format(redeemPointsResponse['numPoints'] , pointsToRedeem))
        Assertion.constructAssertion('REDEEM' in redeemPointsResponse['instructionType'], 'REDEEM Instruction not executed in points redemptions')
        LoyaltyHelper.assertOnSumOfPoints(self,(initialRedeemedPoints+pointsToRedeem))
        return redeemPointsResponse