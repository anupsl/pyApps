import time
from src.Constant.constant import constant
from src.initializer.generateThrift import emf
from src.utilities.utils import Utils
from src.utilities.randValues import randValues
from src.utilities.logger import Logger



class EMFObject(object):


    @staticmethod
    def BulkExpiryReportData(bulkExpiryReportData):
        tmpDict = {
            'orgId' : constant.config['orgId'],
            'loggedInUserId' : 0,
            'fromTimeInMillis' : Utils.getTime(days=-1, milliSeconds=True),
            'toTimeInMillis' : Utils.getTime(milliSeconds=True),
            'includeExpired' : True,
            'includeRedeemed' : True
        }
        tmpDict.update(bulkExpiryReportData)
        return emf.BulkExpiryReportData(**tmpDict)

    @staticmethod
    def CommChannelAttribute(commChannelAttribute):
        return emf.CommChannelAttribute(**commChannelAttribute)

    @staticmethod
    def Loyalty(updateDict = {}):
        tmpDict = {
            'id' : 0,
            'lifetimePurchase' : 0,
            'initialLifetimePurchase' : 0,
            'joinDate' : 0,
            'registrationTillId' : 0,
            'nonLoyalty' : False
        }
        tmpDict.update(updateDict)
        return emf.Loyalty(**tmpDict)

    @staticmethod
    def constructUserDetailsObject(index = 0):
        userInfo = constant.config['usersInfo'][index]
        smsObj = EMFObject.CommChannel({'type': 'mobile', 'value': userInfo['mobile'], 'verified': False, 'primary': True })
        emailObj = EMFObject.CommChannel({'type': 'email', 'value': userInfo['email'], 'verified': False, 'primary': True})
        userProfile = EMFObject.UserProfile({'customFields': {'gender': 'Male'}, 'source': 'INSTORE', 'commChannels': [smsObj, emailObj]})
        userDetailObj = EMFObject.UserDetails({'id': userInfo['userId'], 'profiles': [userProfile], 'loyalty': EMFObject.Loyalty()})
        return userDetailObj

    @staticmethod
    def CommChannel(commChannel):
        return emf.CommChannel(**commChannel)

    @staticmethod
    def UserProfile(userProfile):
        tmpDict = {
            'source' : 'INSTORE'
        }
        tmpDict.update(userProfile)
        return emf.UserProfile(**userProfile)

    @staticmethod
    def UserDetails(userDetails):
        return emf.UserDetails(**userDetails)

    @staticmethod
    def PointsTransferEventData(updateDict = {}):
        tmpDict = {
            'orgID' : constant.config['orgId'],
            'transferredAtStoreUnitID' : '',
            'eventTimeInMillis' : Utils.getTime(milliSeconds=True),
            'numPointsToBeTransferred' : 0,
            'fromCustomerDetails' : '',
            'toCustomerDetails' : '',
            'uniqueId': randValues.randomString(8),
            'serverReqId': randValues.randomString(15),
            'source' : 'INSTORE'
        }
        tmpDict.update(updateDict)
        return emf.PointsTransferEventData(**tmpDict)


    @staticmethod
    def NewBillEvent(billDetails = {}):
        tmpDict = {
            'orgID': constant.config['orgId'],
            'customerID': constant.config['usersInfo'][0]['userId'],
            'billID': constant.config['billNumber'],
            'storeUnitID': constant.config['storeIds'][0],
            'eventTimeInMillis': Utils.getTime(milliSeconds=True),
            'ignorePoints': False,
            'billAmount': 1000,
            'lifetimePurchase': 0,
            'prevLifetimePurchase': 0,
            'numberOfVisits': 1,
            'uniqueId': randValues.randomString(8),
            'serverReqId': constant.config['serverReqId'],
            'nonLoyalty': False,
            'userDetails' : EMFObject.constructUserDetailsObject(0),
            'source': 'INSTORE',
            'accountId': str(constant.config['programId']),
        }
        tmpDict.update(billDetails)
        return emf.NewBillEvent(**tmpDict)

    @staticmethod
    def PointsRedemptionReversalEventData(paramDict = {}):
        constant.config['uniqueId'] = randValues.randomString(8)
        tmpDict = {
            'orgID' : constant.config['orgId'],
            'storeUnitID' : constant.config['storeIds'][0],
            'eventTimeInMillis' : Utils.getTime(seconds=randValues.randomInteger(2),milliSeconds=True),
            'userDetails' : EMFObject.constructUserDetailsObject(0),
            'uniqueRedemptionId' : None,
            'uniqueId': constant.config['uniqueId'],
            'serverReqId': constant.config['serverReqId'],
            'source' : 'INSTORE',
            'accountId' : str(constant.config['programId']),
            'notes' : 'Auto points reversal'
        }
        tmpDict.update(paramDict)
        return  emf.PointsRedemptionReversalEventData(**tmpDict)

    @staticmethod
    def PointsRedemptionEventData(paramDict = {}):
        constant.config['uniqueId'] = randValues.randomString(8)
        tmpDict = {
            'orgID': constant.config['orgId'],
            'customerID' : 0,
            'numPointsToBeRedeemed' : constant.config['defaultRedeemPts'],
            'redeemedAtStoreUnitId' : constant.config['storeIds'][0],
            'redeemedOnBillNumber' : '-1',
            'redeemedOnBillId' : constant.config['billNumber'],
            'eventTimeInMillis': Utils.getTime(seconds=(randValues.randomInteger(2)),milliSeconds=True),
            'userDetails': EMFObject.constructUserDetailsObject(0),
            'uniqueId': constant.config['uniqueId'],
            'serverReqId': constant.config['serverReqId'],
            'source': 'INSTORE',
            'accountId': str(constant.config['programId']),
        }
        constant.config['defaultRedeemPts'] = paramDict['numPointsToBeRedeemed'] if paramDict.has_key('numPointsToBeRedeemed') else 100
        tmpDict.update(paramDict)
        return emf.PointsRedemptionEventData(**tmpDict)

    @staticmethod
    def ReturnLineItem(paramDict = {}):
        tmpDict = {
            'id' : 0,
            'qty' : 0
        }
        tmpDict.update(paramDict)
        return emf.ReturnLineItem(**tmpDict)

    @staticmethod
    def ReturnBillLineitemsEventData(paramDict = {'returnLineItem' : {}}):
        constant.config['uniqueId'] = randValues.randomString(8)
        tmpDict = {
            'orgID': constant.config['orgId'],
            'customerID': constant.config['usersInfo'][0]['userId'],
            'returnBillID' : constant.config['billNumber'] ,
            'storeUnitID': constant.config['storeIds'][0],
            'eventTimeInMillis' : Utils.getTime(milliSeconds=True),
            'uniqueId': constant.config['uniqueId'],
            'serverReqId': constant.config['serverReqId'],
            'returnLineItems' : [EMFObject.ReturnLineItem(paramDict['returnLineItem'])],
            'userDetails': EMFObject.constructUserDetailsObject(0),
            'source': 'INSTORE',
            'accountId': str(constant.config['programId']),
        }
        paramDict.pop('returnLineItem')
        tmpDict.update(paramDict)
        return emf.ReturnBillLineitemsEventData(**tmpDict)

    @staticmethod
    def ReturnBillAmountEventData(paramDict = {}):
        constant.config['uniqueId'] = randValues.randomString(8)
        tmpDict = {
            'orgID': constant.config['orgId'],
            'customerID': 0,
            'returnBillID' : 0,
            'storeUnitID': constant.config['storeIds'][0],
            'eventTimeInMillis' : Utils.getTime(milliSeconds=True),
            'uniqueId': constant.config['uniqueId'],
            'serverReqId': constant.config['serverReqId'],
            'returnAmount' : 0,
            'userDetails': EMFObject.constructUserDetailsObject(0),
            'source': 'INSTORE',
            'accountId': str(constant.config['programId']),
        }
        tmpDict.update(paramDict)
        return emf.ReturnBillAmountEventData(**tmpDict)