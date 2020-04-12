import time, json,copy, inspect
from src.utilities.logger import Logger
from src.Constant.constant import constant
from src.modules.luci.luciThrift import LuciThrift
from src.utilities.utils import Utils
from src.utilities.assertion import Assertion
from selenium import webdriver
from src.utilities.randValues import randValues
from src.modules.luci.luciObject import LuciObject
from src.modules.luci.luciDBHelper import LuciDBHelper
from src.modules.luci.dracarysHelper import DracarysHelper
from src.utilities.fileHelper import FileHelper

class LuciHelper():

    @staticmethod
    def checkLuciConn(ignoreConnectionError=False):
        Utils.checkServerConnection('LUCI_THRIFT_SERVICE', LuciThrift, 'luciPort', ignoreConnectionError)

    @staticmethod
    def getConnObj(newConnection=False):
        port = constant.config['luciPort'].next()
        connPort = str(port) + '_obj'
        if connPort in constant.config:
            if newConnection:
                constant.config[connPort].close()
                constant.config[connPort] = LuciThrift(port)
            return constant.config[connPort]
        else:
            return LuciThrift(port)

    @staticmethod
    def verifyLuciServicesCount(luciCount=1):
        if len(constant.config['LUCI_THRIFT_SERVICE']) >= luciCount:
            return True
        else:
            return False

    @staticmethod
    def get_conn(newConnection=False, instance_identifier=0):
        port = constant.config['LUCI_THRIFT_SERVICE'][instance_identifier]
        connPort = str(port) + '_obj'
        if connPort in constant.config:
            if newConnection:
                constant.config[connPort].close()
                constant.config[connPort] = LuciThrift(port)
            return constant.config[connPort]
        else:
            return LuciThrift(port)

    @staticmethod
    def getFirstConn(newConnection=False):
        if len(constant.config['LUCI_THRIFT_SERVICE']) >= 0:
            return LuciHelper.get_conn(newConnection, 0)

    @staticmethod
    def getSecondConn(newConnection=False):
        if len(constant.config['LUCI_THRIFT_SERVICE']) >= 1:
            return LuciHelper.get_conn(newConnection, 1)

    @staticmethod
    def setBaseDetails():
        Logger.log("Retriving Base Info's for Testcases like AdminUser, UserList, TIll & Store id's and CampaignId")
        LuciDBHelper.getAdminUserId()
        LuciDBHelper.getUsers()
        LuciDBHelper.getActiveTillIdList()
        LuciDBHelper.getActiveStoreIdList()
        LuciHelper.createCampaign()
        Logger.log('Base Details set for Testcases')

    @staticmethod
    def loginAndGetCookies():
        try:
            driver = webdriver.PhantomJS(executable_path=constant.phantomjsPath)
            driver.get(constant.config['intouchUrl'])
            driver.find_element_by_id('login_user').send_keys(constant.config['intouchUsername'])
            driver.find_element_by_id('login_cred').send_keys(constant.config['intouchPassword'])
            driver.find_element_by_id('c-login-btn').click()
            try:
                if driver.find_element_by_id('otp__code').is_displayed():
                    otp = LuciDBHelper.getOTP()
                    driver.find_element_by_id('otp__code').send_keys(otp)
                    driver.find_element_by_id('c-login-btn').click()
            except:
                Logger.log('OTP Verification Page not Found')
            cookieList = driver.get_cookies()
            temp = '';
            for k in cookieList:
                if (k['name'] == 'OID'):
                    temp += k['name'] + '=' + str(constant.config['orgId']) + ";"
                else:
                    temp += k['name'] + '=' + k['value'] + ";"
            constant.config['intouchCookie'] = temp
        except Exception, intouchExp:
            Logger.log('{} Intouch is down and setting up Cookies Empty String & Exception : {}'.format(constant.config['cluster'], intouchExp))
            constant.config['intouchCookie'] = 'Cookies Not Set'

    @staticmethod
    def generateCouponCode(isAlphaNumeric = True, size = 9):
        if isAlphaNumeric:
            return randValues.randomString(size).upper()
        else:
            return str(randValues.randomInteger(size))

    @staticmethod
    def createCampaign():
        payLoad =   {
            'startDate' : Utils.getTime(seconds=5,milliSeconds=True), 'endDate' : Utils.getTime(days=1,milliSeconds=True),
            'campaignType' : 'OUTBOUND', 'description' : 'LUCI_' + str(int(time.time())),
            'name' : 'LUCI_' + str(int(time.time())), 'tags' : 'Test', 'entityId' : '1234', 'goalId' : '1',
            'objectiveId' : '22', 'gaSource' : '', 'gaName' : '', 'testControl' : {'test': 90,'type': 'ORG'},
            'classifier' : 'Newsletter'
        }
        auth = constant.config['intouchUsername'], constant.config['intouchPassword']

        Headers =   {
            'accept': 'application/json',
            'content-type': 'application/json',
            'X-CAP-ORG': str(constant.config['orgId'])
        }
        try:
            response = Utils.makeRequest(constant.config['url'] + constant.config['createcampaign'], payLoad, Headers, 'POST', auth)
            campaignId = response.json()
            constant.config['campaignId'] = campaignId['entity']['campaignId']
        except Exception, irisExp:
            Logger.log('{} IRIS is down and setting up constant campaignId and Exception : {}'.format(constant.config['cluster'], irisExp))
            constant.config['campaignId'] = 322856
        finally:
            Logger.log('Campaign Id : ' , constant.config['campaignId'], ' - ', constant.config['currentTimestamp'])


    @staticmethod
    def makeAjaxCall(couponSeriedId , isSkuUpdate = False):
        header = {'accept': 'application/json',
                  'content-type': 'application/x-www-form-urlencoded',
                  'cookie': constant.config['intouchCookie']}
        if isSkuUpdate:
            Logger.log('Making Ajax call to Update SKU')
            postData = "sku_values=ONEPLUS1,ONEPLUS2,ONEPLUS3"
            skuUpdateURL = constant.config['intouchUrl'] + constant.config['SkuUrl'] + str(couponSeriedId)
            Utils.makeRequest(skuUpdateURL, postData, header, 'POST', '')
        else:
            Logger.log('Making Ajax call to get Brands Ids')
            brandUrl = constant.config['intouchUrl'] + constant.config['brandUrl'] + str(couponSeriedId)
            result = Utils.makeRequest(brandUrl, "", header, 'GET', '').json()
            brandIds = result['items'].keys()
            constant.config['categoryIds'] = []

            brands = []
            for b in range(0,len(brandIds)):
                brands.append({ "value" : int(brandIds[b]) , "status" : "ADDED"})

            Logger.log('Making Ajax call to get Categories Ids')
            rootCategoryUrl = constant.config['intouchUrl'] + constant.config['categoryUrl'] + 'root'
            rootCategoryResponse = Utils.makeRequest(rootCategoryUrl, "", header, 'GET', '').json()
            categoryParentIds = rootCategoryResponse['members'].keys()

            category = []
            for b in range(0, len(categoryParentIds)):
                categoryUrl = constant.config['intouchUrl'] + constant.config['categoryUrl'] + categoryParentIds[b]
                categoryIdResponse = Utils.makeRequest(categoryUrl, "", header, 'GET', '').json()
                categoryIds = categoryIdResponse['members'].keys()
                for c in range(0, len(categoryIds)):
                    constant.config['categoryIds'].append(int(categoryIds[c]))
                    category.append({"value": int(categoryIds[c]), "status": "ADDED"})

            Logger.log('Making Ajax call to update Brands & Category for voucher series')
            constructPostData = { 'brand' : brands , 'category' : category}
            saveDetailsUrl = constant.config['intouchUrl'] + constant.config['saveUrl'] + str(couponSeriedId)
            data = 'params=' + json.dumps(constructPostData)
            Utils.makeRequest(saveDetailsUrl, data, header, 'POST', '')

    @staticmethod
    def redeemCouponRequest(couponCodeList, userId, billId = 8989, redeemCouponRequest = {}):
        redeemList = []
        for couponCode in couponCodeList:
            redeemList.append(LuciObject.redeemCoupon({'billId' : billId, 'couponCode' : couponCode, 'storeUnitId' : constant.config['tillIds'][0], 'userId' : userId}))
        tmpRedeemCouponRequest = {'couponSeriesRequired': False, 'commit': True, 'redeemCoupons': redeemList}
        tmpRedeemCouponRequest.update(redeemCouponRequest)
        return LuciObject.redeemCouponsRequest(tmpRedeemCouponRequest)

    @staticmethod
    def saveCouponConfigAndAssertions(self, couponConfigReq = {}, saveCouponConfig = {}):
        couponConfigReq.update({"info": inspect.stack()[1][3]})
        couponConfigObj = LuciObject.couponConfiguration(couponConfigReq)
        if saveCouponConfig == {}:
            saveCouponConfigRequestObj = LuciObject.saveCouponConfigRequest(couponConfigObj)
        else:
            saveCouponConfigRequestObj = LuciObject.saveCouponConfigRequest(couponConfigObj,saveCouponConfig)
        output = self.connObj.saveCouponConfiguration(saveCouponConfigRequestObj)
        Assertion.constructAssertion(output is not None, 'Coupon Series Created successfully')
        couponConfigObj = output.__dict__
        return couponConfigObj, couponConfigObj['id']

    @staticmethod
    def getCouponConfigAndAssertion(self,couponSeriesId,no_issued = 0, no_redeemed = 0, updateConfigRequest = {}):
        tmpDict = {'couponSeriesId': couponSeriesId}
        tmpDict.update(updateConfigRequest)
        configRequest = LuciObject.getCouponConfigRequest(tmpDict)
        couponConfigList = self.connObj.getCouponConfiguration(configRequest)
        couponConfig = couponConfigList[0].__dict__
        if not couponConfig['isExternalIssual']:
            Assertion.constructAssertion(couponConfig['num_issued'] == no_issued, 'No. of Coupons issued, Actual : {} and Expected : {}'.format(couponConfig['num_issued'], no_issued))
        else:
            Assertion.constructAssertion(couponConfig['num_issued'] != 0, 'No. of Coupons issued, Actual : {} and Expected : {}'.format(couponConfig['num_issued'], no_issued))
        Assertion.constructAssertion(couponConfig['num_redeemed'] == no_redeemed, 'No. of Coupons redeemed, Actual : {} and Expected: {}'.format(couponConfig['num_redeemed'], no_redeemed))
        Assertion.constructAssertion('owned_by' in couponConfig, 'Getting Details Owned by in CouponConfig')
        Assertion.constructAssertion('owner_id' in couponConfig, 'Getting Details Owner id in CouponConfig')
        Assertion.constructAssertion('ownerValidity' in couponConfig, 'Getting Details owner Validity in CouponConfig')
        return couponConfig

    @staticmethod
    def getCouponDetailsAndAssertion(self,couponSeriesId,couponCode,couponDetailsRequest):
        # CouponDetails Request
        couponDetailsRequestobj = LuciObject.couponDetailsRequest(couponDetailsRequest)
        couponDetailsList = self.connObj.getCouponDetails(couponDetailsRequestobj)
        Assertion.constructAssertion(len(couponDetailsList) == 1, 'Coupon Details list count Actual :{} and Expected : {}'.format(len(couponDetailsList), 1))
        couponDetails = couponDetailsList[0].__dict__
        if couponDetailsRequest.has_key('couponSeriesRequired'):
            Assertion.constructAssertion(couponDetails['couponSeries'] != None, 'Coupon Series Details is available')
        else:
            Assertion.constructAssertion(couponDetails['couponSeries'] == None, 'Coupon Series Details is None')
        Assertion.constructAssertion(couponDetails['ex'] is None, 'Coupon Details with Luci Exception Message: {}'.format(couponDetails['ex']))
        Assertion.constructAssertion(couponDetails['couponCode'] == couponCode.upper(), 'Issued Coupon code Actual : {} and Expected : {}'.format(couponDetails['couponCode'],couponCode))
        Assertion.constructAssertion(couponDetails['orgId'] == constant.config['orgId'], 'Coupon Series OrgId Actual : {} and Expected : {}'.format(couponDetails['orgId'], constant.config['orgId']))
        Assertion.constructAssertion(couponDetails['couponSeriesId'] == couponSeriesId, 'Coupon Series Id Actual : {} and Expected : {}'.format(couponDetails['couponSeriesId'], couponSeriesId))
        Assertion.constructAssertion(couponDetails['issuedToUserId'] == self.userId, 'Coupon code Issued to userId Actual : {} and Expected : {}'.format(couponDetails['issuedToUserId'], self.userId))

    @staticmethod
    def issueCouponAndAssertions(self, couponSeriesId, issueCouponParamObj={}, couponIssuedCount=1, expectException = False):
        issueCouponObj = {'couponSeriesId': couponSeriesId, 'storeUnitId': self.tillId, 'userId': self.userId}
        actualTillid = self.tillId
        if issueCouponParamObj.has_key('storeUnitId'):
            self.tillId = issueCouponParamObj['storeUnitId']
        issueCouponObj.update(issueCouponParamObj)
        issueCouponRequest = LuciObject.issueCouponRequest(issueCouponObj)

        for _ in range(0, 5):
            couponDetails = self.connObj.issueCoupon(issueCouponRequest).__dict__
            if couponDetails['ex'] != None and not expectException:
                time.sleep(1)
            else:
                break
        if expectException:
            return couponDetails['ex'].__dict__
        couponCode = couponDetails['couponCode']

        Assertion.constructAssertion(couponDetails != None, 'Issued Coupon Details not Empty')
        Assertion.constructAssertion(couponDetails['orgId'] == constant.config['orgId'], 'Coupon Series OrgId Actual : {} and Expected : {}'.format(couponDetails['orgId'], constant.config['orgId']))
        Assertion.constructAssertion(couponDetails['couponSeriesId'] == couponSeriesId, 'Coupon Series Id Actual : {} and Expected : {}'.format(couponDetails['couponSeriesId'], couponSeriesId))
        Assertion.constructAssertion(couponDetails['issuedToUserId'] == self.userId, 'Coupon code Issued to userId Actual : {} and Expected : {}'.format(couponDetails['issuedToUserId'], self.userId))
        Assertion.constructAssertion(couponDetails['couponCode'] == couponCode, 'Issued Coupon code Actual : {} and Expected : {}'.format(couponDetails['couponCode'], couponCode))

        couponIssuedDict = LuciDBHelper.getCouponsIssued(couponSeriesId, self.userId)
        Assertion.constructAssertion(couponIssuedDict != {}, 'Issued Coupon Code recorded in Coupons_issued table')
        Assertion.constructAssertion(couponIssuedDict['issuedBy'] == self.tillId, 'Issued by till Actual: {} and Expected : {}'.format(couponIssuedDict['issuedBy'], self.tillId))

        # couponSentHistoryList = LuciDBHelper.getCouponSentHistoryList(couponSeriesId, couponIssuedDict['id'])
        # Assertion.constructAssertion(couponSentHistoryList != [], 'Issued Coupon details recorded in Coupon_sent_history')
        # Assertion.constructAssertion(len(couponSentHistoryList) == couponIssuedCount, 'Coupon_sent_history records Actual : {} and Expected : {}'.format(len(couponSentHistoryList), couponIssuedCount))
        # Assertion.constructAssertion(couponSentHistoryList[0]['notes'] in ['ISSUED', 'RESENT'], 'Coupon_sent_history Notes Actual : {} and Expected : ISSUED/RESENT'.format(couponSentHistoryList[0]['notes']))

        self.tillId = actualTillid
        return couponCode, couponDetails

    @staticmethod
    def uploadCouponAndAssertions(self, couponSeriesId, uploadType, issuedTo = '-1', noOfCouponsToBeUpload = 1, couponCode = None, dracraysUpload = {}):
        isTaggedCoupon = True
        if uploadType == 2:
            isTaggedCoupon = False
        if False: #Change as True for old upload flow
            couponCodeVsUserMap = {}
            for _ in range(noOfCouponsToBeUpload):
                if couponCode == None or noOfCouponsToBeUpload != 1:
                    couponCode = LuciHelper.generateCouponCode()
                if uploadType != 2:
                    couponCodeVsUserMap.update({couponCode: str(issuedTo)})
                else:
                    couponCodeVsUserMap.update({couponCode: issuedTo})

            uploadCouponRequest = {'couponCodeVsUserMap': couponCodeVsUserMap, 'couponSeriesId': couponSeriesId, 's3Location': constant.config['requestId'], 'importType': uploadType}
            uploadCouponRes = self.connObj.uploadCoupons(LuciObject.uploadCouponsRequest(uploadCouponRequest))
            if len(uploadCouponRes) == 0:
                # Get Coupon Configuration
                if issuedTo != '-1':
                    LuciHelper.getCouponConfigAndAssertion(self, couponSeriesId, len(couponCodeVsUserMap), 0)
                else:
                    LuciHelper.getCouponConfigAndAssertion(self, couponSeriesId, 0, 0)
            else:
                Assertion.constructAssertion(uploadCouponRes[couponCode] == 'duplicate coupon code', 'Duplicate Coupon Code is not uploaded')
            return {'coupons' : [couponCode]}
        else:
            tmpDict = {'errorCount' : 0, 'userOnly' : False, 'invalidCase' : [False, False], 'couponCodeCAPS' : True}
            tmpDict.update(dracraysUpload)
            uploadDict = DracarysHelper.uploadCoupons(self, couponSeriesId, onlyUser=tmpDict['userOnly'], is_invalidCase=tmpDict['invalidCase'], identifierType=self.constructObj.CustomerIdentifierDracarys[uploadType], userTaggedCoupons=isTaggedCoupon, noOfCouponUpload=noOfCouponsToBeUpload, expectedError=tmpDict['errorCount'], couponISCAPS=tmpDict['couponCodeCAPS'])
            couponIssuedDBDetails = LuciDBHelper.getIssuedCoupons(couponSeriesId)
            if len(couponIssuedDBDetails) != 0:
                issuedCouponList = list()
                for cc in couponIssuedDBDetails:
                    issuedCouponList.append(cc['couponCode'])
                uploadDict['coupons']= issuedCouponList
                return uploadDict
            else:
                return uploadDict

    @staticmethod
    def couponSearchAndAssertion(self, couponSeriesId, couponSearchParam = {}, couponCode = [], redemptionCount = []):
        # Coupon Search Request
        if len(couponCode) != []:
            couponCode = [convertUppercase.upper() for convertUppercase in couponCode]
        couponSearchRequest = {'couponSeriesIds': couponSeriesId, 'customerIds': [self.userId]}
        couponSearchRequest.update(couponSearchParam)
        couponDetailsResponse = (self.connObj.couponSearch(self.constructObj.couponSearchRequest(couponSearchRequest)).__dict__)

        couponDetailsList = couponDetailsResponse['coupons']
        Assertion.constructAssertion(len(couponDetailsList) == len(couponCode), 'Coupon Details list, Autual  {} and Expected '.format(len(couponDetailsList)))

        for i in range(len(couponDetailsList)):
            couponDetails = couponDetailsList[i].__dict__
            if redemptionCount != []:
                Assertion.constructAssertion(len(couponDetails['redeemedCoupons']) == redemptionCount[i], 'Coupon redemption count Actual :{} and Expected: {}'.format(len(couponDetails['redeemedCoupons']) , redemptionCount[i]))
            Assertion.constructAssertion(couponDetails['ex'] is None, 'Coupon Details with Luci Exception Message: {}'.format(couponDetails['ex']))
            Assertion.constructAssertion(couponDetails['couponCode'] in couponCode, 'Issued coupon is recorded in coupons_issued Actual: {} and Expected: {}'.format(couponDetails['couponCode'] , couponCode[i]))
            Assertion.constructAssertion(couponDetails['couponSeriesId'] in couponSeriesId, 'Coupon Series Id Actual : {} and Expected : {}'.format(couponDetails['couponSeriesId'], couponSeriesId))
            Assertion.constructAssertion(couponDetails['issuedToUserId'] == self.userId, 'Coupon code Issued to userId Actual : {} and Expected : {}'.format(couponDetails['issuedToUserId'], self.userId))
            Assertion.constructAssertion(couponDetails['couponSeriesDescription'] != None, 'Coupon Series Description Actual : {}'.format(couponDetails['couponSeriesDescription']))

    @staticmethod
    def redeemCouponAndAssertions(self,couponSeriesIdList,couponCodeList, couponIssuedTo = [], isMaxRedeemSet = False, redeemCouponRequestList = None, isRedeem = True, error = []):
        couponRedemptionDetails = None
        if not isinstance(error, dict) and error != []:
            error = {'errorCode' : [error[0]], 'errorMsg' : [error[1]]}
        if not couponIssuedTo:
            couponIssuedTo = [self.userId]
        if not isinstance(couponCodeList, list):
            couponCodeList = [couponCodeList]
        if not isinstance(couponSeriesIdList, list):
            couponSeriesIdList = [couponSeriesIdList]
        couponSeriesIdDeepList = copy.deepcopy(couponSeriesIdList)
        couponCodeDeepList = copy.deepcopy(couponCodeList)
        couponCodeDeepList = [convertUppercase.upper() for convertUppercase in couponCodeDeepList]
        # Redeem coupon code
        if redeemCouponRequestList != None:
            couponDetailsList = self.connObj.redeemCoupons(redeemCouponRequestList)
        else:
            couponDetailsList = self.connObj.redeemCoupons(LuciHelper.redeemCouponRequest(couponCodeList, self.userId, self.billId, redeemCouponRequest={'commit': isRedeem}))
        Assertion.constructAssertion(couponDetailsList is not None, 'Redeemed Coupon code Details list is not Empty')
        Assertion.constructAssertion(len(couponDetailsList) == len(couponCodeList), 'Coupon Details list, Autual :{} and Expected: {}'.format(len(couponDetailsList), len(couponCodeList)));

        for couponDetails in couponDetailsList:
            couponDetails = couponDetails.__dict__
            if couponDetails['ex'] is None:
                Assertion.constructAssertion(couponDetails['couponCode'] in couponCodeDeepList, 'Issued Coupon code Actual : {} and Expected : {}'.format(couponDetails['couponCode'], couponCodeDeepList))
                Assertion.constructAssertion(couponDetails['orgId'] == constant.config['orgId'], 'Coupon Series OrgId Actual : {} and Expected : {}'.format(couponDetails['orgId'], constant.config['orgId']))
                Assertion.constructAssertion(couponDetails['couponSeriesId'] in couponSeriesIdDeepList, 'Coupon Series Id Actual : {} and Expected : {}'.format(couponDetails['couponSeriesId'], couponSeriesIdDeepList))
                Assertion.constructAssertion(couponDetails['issuedToUserId'] in couponIssuedTo, 'Coupon code Issued to userId Actual : {} and Expected : {}'.format(couponDetails['issuedToUserId'], couponIssuedTo))
                Assertion.constructAssertion(len(couponDetails['redeemedCoupons']) == 1, 'Coupon redeemed count, Autual : {} and Expected '.format(len(couponDetails['redeemedCoupons'])))
                if isMaxRedeemSet: Assertion.constructAssertion(couponDetails['redemptionsLeft'] == 9, 'Count of Coupon Redemption remains')
                Assertion.constructAssertion(couponDetails['transactionId'] == self.billId, 'Redeemed Bill id Actual : {} and Expected : {}'.format(couponDetails['transactionId'], self.billId))
                couponRedemptionDetails = couponDetails['redeemedCoupons'][0].__dict__
                Assertion.constructAssertion(couponRedemptionDetails['redeemedByUserId'] == self.userId, 'Coupon redeemed by userId Actual : {} and Expected : {}'.format(couponRedemptionDetails['redeemedByUserId'], self.userId))
                if not isRedeem:
                    couponRedemptionDetails = couponDetails
                couponSeriesIdDeepList.remove(couponDetails['couponSeriesId'])
                couponCodeDeepList.remove(couponDetails['couponCode'])
            else:
                luciException = couponDetails['ex'].__dict__
                Assertion.constructAssertion(luciException['errorCode'] in error['errorCode'], 'Redemption error Code Actual : {} and Expected: {}'.format(luciException['errorCode'],error['errorCode']))
                Assertion.constructAssertion(luciException['errorMsg'].rstrip() in error['errorMsg'], 'Redemption error Message Actual : {} and Expected: {}'.format(luciException['errorMsg'],error['errorMsg']))
                if luciException['errorCode'] != constant.FAILED_REDEMPTIONS_EXISTS:
                    error['errorCode'].remove(luciException['errorCode'])
                    error['errorMsg'].remove(luciException['errorMsg'].rstrip())
        return couponRedemptionDetails

    @staticmethod
    def issuedCouponsDBAssertion(self,couponSeriesId, couponCode, numIssued = 1, issuedTo = -1):
        couponsIssuedList = LuciDBHelper.getCouponsIssuedList(couponSeriesId)
        Assertion.constructAssertion(couponsIssuedList is not None, 'Issued coupons are recorded in coupons_issued')
        Assertion.constructAssertion(len(couponsIssuedList) == numIssued, 'Issued Count in coupons_iisued Actual : {} and Expected : {}'.format(len(couponsIssuedList),numIssued))
        Assertion.constructAssertion(couponsIssuedList[0]['couponCode'] == couponCode, 'Issued coupon Actual: {} and Expected : {}'.format(couponsIssuedList[0]['couponCode'], couponCode))
        Assertion.constructAssertion(couponsIssuedList[0]['issuedTo'] == issuedTo, 'Coupon Issued UserId Actual : {} and Expected : {}'.format(couponsIssuedList[0]['issuedTo'],issuedTo))

    @staticmethod
    def redemptionDBAssertion(self, couponSeriesId, numRedeemed = 1, redeemedBy = []):
        if not redeemedBy:
            redeemedBy = [self.userId]
        couponRedemptionList = LuciDBHelper.getCouponRedemptionsListByCouponSeriesId(couponSeriesId)
        Assertion.constructAssertion(couponRedemptionList is not None, 'Coupon_redemption has the records')
        Assertion.constructAssertion(len(couponRedemptionList) == numRedeemed, 'No of Coupon redeemed Actual: {} and Expected: {}'.format(len(couponRedemptionList) , numRedeemed))
        for cr in couponRedemptionList:
            Assertion.constructAssertion(cr['redeemedUserId'] in redeemedBy, 'Coupon redeemed by Actual: {} and Expected: {}'.format(cr['redeemedUserId'], redeemedBy))
            Assertion.constructAssertion(cr['redeemedAtStore'] == self.tillId, 'Redeemed Till id Actual: {} and Expected: {}'.format(cr['redeemedAtStore'], self.tillId))
            Assertion.constructAssertion(cr['billId'] == self.billId, 'Redeemed Bill Id Actual : {} and Expected: {}'.format(cr['billId'], self.billId))

    @staticmethod
    def issueMultipleCoupon(self,couponSeriesId,userList, issueCouponParamObj = {}, expectResponseException = [False]):
        issueMultipleCouponsRequest = {'couponSeriesId': couponSeriesId, 'storeUnitId': self.tillId, 'userIds': userList}
        issueMultipleCouponsRequest.update(issueCouponParamObj)
        issueMultipleCouponsRequestObj = LuciObject.issueMultipleCouponsRequest(issueMultipleCouponsRequest)

        couponDetailsList = self.connObj.issueMultipleCoupons(issueMultipleCouponsRequestObj)

        ExpectedUserIdsList = []
        ExpectExceptionList = []
        for couponDetails in couponDetailsList:
            couponDetails = couponDetails.__dict__
            if not expectResponseException[0]:
                ExpectedUserIdsList.append(couponDetails['issuedToUserId'])
                Assertion.constructAssertion(couponDetails['ex'] is None, 'Coupon Details with Luci Exception Message: {}'.format(couponDetails['ex']))
                Assertion.constructAssertion(couponDetails['couponSeriesId'] == couponSeriesId, 'Coupon Series Id Actual : {} and Expected : {}'.format(couponDetails['couponSeriesId'], couponSeriesId))
            elif couponDetails['ex'] is not None:
                ex = couponDetails['ex'].__dict__
                if ex['errorMsg'].lower() == expectResponseException[1]:
                    ExpectExceptionList.append(ex['errorMsg'])
                else:
                    Assertion.constructAssertion(False,'Expected Exception Message : {} and Actual : {}'.format(expectResponseException[1], ex['errorMsg'].lower()),verify=False)
        if expectResponseException[0] and len(ExpectExceptionList) == 0:
            Assertion.constructAssertion(False, 'Expected issual exception: {} not in Response '.format(expectResponseException[1]), verify=False)
        elif expectResponseException[0] and len(ExpectExceptionList) > 0:
            return  ExpectExceptionList

        Assertion.constructAssertion(len(userList) == len(ExpectedUserIdsList), 'Multiple Coupons issued to Actual : {} and Expected : {}'.format(len(ExpectedUserIdsList), len(userList)))
        Assertion.constructAssertion(set(ExpectedUserIdsList) == set(userList), 'Matched Issue Coupon request and Issued coupon UserIds')
        return couponDetailsList

    @staticmethod
    def queuePumpWait(self, couponSeriesId):
        for _ in range(30):
            queueCount = LuciHelper.getQueueSize(self,couponSeriesId)
            if queueCount < 1500:
                time.sleep(1)
            else:
                break

    @staticmethod
    def getQueueSize(self, couponSeriesId):
        try:
            return self.connObj.getQueueSize(constant.config['orgId'], couponSeriesId, constant.config['requestId'])
        except Exception, exp:
            Logger.log('Get Queue Size Failed With Exception: {}'.format(exp))
            raise exp

    @staticmethod
    def couponPumpAssertion(self, couponSeriesId, isDiscCode = True, DiscCodePinCouponUploaded  = 0):
        if isDiscCode:
            createdCouponCount = LuciDBHelper.getCouponsCreated_Count(couponSeriesId)
            Assertion.constructAssertion(createdCouponCount != 0, 'Coupon Code Pumped to Queue')
            Assertion.constructAssertion(self.connObj.getQueueSize(constant.config['orgId'], couponSeriesId, constant.config['requestId']) != 0, 'DiscCode Coupons Pumped to Queue')
        else:
            createdCouponCount = LuciDBHelper.getCouponsCreated_Count(couponSeriesId, 1)
            Assertion.constructAssertion(createdCouponCount == DiscCodePinCouponUploaded, 'Coupons are created for DCP')
            Assertion.constructAssertion(self.connObj.getQueueSize(constant.config['orgId'], couponSeriesId, constant.config['requestId']) == DiscCodePinCouponUploaded, 'DiscCodePin Coupons not pumped')

    @staticmethod
    def invalidateCouponAndAssertions(self, couponSeriesId, couponCode = None, numRevoked = 1, couponSeriesInfo = [True, False]):
        if couponSeriesInfo[0]:
            invalidateCouponRequest = LuciObject.invalidateCouponRequest({'couponSeriesId': couponSeriesId})
        else:
            couponsToBeInvalidated = [LuciObject.issuedCouponDetails({'couponCode': couponCode, 'issuedTo': self.userId})]
            invalidateCouponRequest = LuciObject.invalidateCouponRequest({'couponSeriesId': couponSeriesId, 'couponsToBeInvalidated': couponsToBeInvalidated})

        Assertion.constructAssertion(self.connObj.invalidateCoupons(invalidateCouponRequest) == True, 'Requested Coupon codes are revoked')
        revokedCount = LuciDBHelper.getCouponsCreated_Count(couponSeriesId, not couponSeriesInfo[0])
        if 'GENERIC' not in couponSeriesInfo:
            Assertion.constructAssertion(revokedCount != 0, 'Coupons code marked as invalid in coupons_created')
        Assertion.constructAssertion(LuciDBHelper.getCouponsIssued_Count(couponSeriesId, 0) == numRevoked, 'Revoked the Issued coupon code')
        queueSize = (self.connObj.getQueueSize(constant.config['orgId'], couponSeriesId, constant.config['requestId']))
        if True in couponSeriesInfo:
            Assertion.constructAssertion(queueSize == 0, 'Revoked Coupons Cleared from Queue Actual: {}'.format(queueSize))
        else:
            Assertion.constructAssertion(queueSize != 0, 'Coupon Series not revoked from Queue Actual: {}'.format(queueSize))

    @staticmethod
    def constructInvalidateCoupon(revokeType, data):
        couponsToBeInvalidated = []
        for v in data:
            if revokeType == 'CUSTOMER_AND_COUPON':
                couponsToBeInvalidated.append(LuciObject.issuedCouponDetails({'couponCode': str(v[0]), 'issuedTo': v[1]}))
            else:
                couponsToBeInvalidated.append(LuciObject.issuedCouponDetails({revokeType : v}))
        return couponsToBeInvalidated

    @staticmethod
    def revokeCoupon(self, couponSeriesId, issuedCoupon ,revokeType = -1, reqDict = {} ):
        tmpDict = {'couponSeriesId': couponSeriesId}
        tmpDict.update(reqDict)
        invalidateCouponRequest = None
        if revokeType in [0,1]:
            invalidateCouponRequest = LuciObject.invalidateCouponRequest(tmpDict)
        else:
            couponsToBeInvalidated = LuciHelper.constructInvalidateCoupon(self.constructObj.revokeType[revokeType], issuedCoupon)
            tmpDict.update({'couponsToBeInvalidated': couponsToBeInvalidated})
            invalidateCouponRequest = LuciObject.invalidateCouponRequest(tmpDict)
        if invalidateCouponRequest != None:
            Assertion.constructAssertion(self.connObj.invalidateCoupons(invalidateCouponRequest) == True, 'Requested Coupon codes are revoked CouponSeriesId : {}'.format(couponSeriesId))
        else:
            Logger.log('Invalidate Coupon Request Object not constructed')

    @staticmethod
    def claimCouponSeries(self, couponSeriesId, claimRequestParams, expectedErrors = [], ownerValidityDays = 2, claimResult = True):
        claimObj = LuciObject.claimCouponConfigRequest({'couponSeriesId': couponSeriesId, 'ownedBy': claimRequestParams[0], 'ownerId': claimRequestParams[1], 'ownerValidity': Utils.getTime(days=ownerValidityDays, milliSeconds=True)})
        result = self.connObj.claimCouponConfig(claimObj).__dict__
        ownerInfo = LuciDBHelper.getOwnerInfo(couponSeriesId)
        if claimResult:
            Assertion.constructAssertion(result['success'], 'Coupon Series claimed by {}'.format(claimRequestParams[0]))
            LuciHelper.queuePumpWait(self, couponSeriesId)
            Assertion.constructAssertion(self.connObj.getQueueSize(constant.config['orgId'], couponSeriesId, constant.config['requestId']) != 0, 'Coupons Pumped to Queue')
        else:
            Assertion.constructAssertion(not result['success'], 'Re-claim Coupon Series by {}'.format(claimRequestParams[0]))
            luciExp = result['ex'].__dict__
            Assertion.constructAssertion(luciExp['errorCode'] == expectedErrors[0], 'Luci Exception error code Actual: {} and Expected: {}'.format(luciExp['errorCode'], expectedErrors[0]))
            Assertion.constructAssertion(luciExp['errorMsg'] == expectedErrors[1], 'Luci Exception Error Msg Actual : {}'.format(luciExp['errorMsg']))
        voucherType = LuciDBHelper.getCouponSeriesType(couponSeriesId)['seriesType']
        Assertion.constructAssertion(voucherType == claimRequestParams[2], 'Coupon Series Type in voucher_series Actual : {} and Expected : {}'.format(voucherType, claimRequestParams[2]))
        Assertion.constructAssertion(ownerInfo['expiry_date'] != None, 'Owner Expiry date is set Actual: {}'.format(ownerInfo['expiry_date']))

    @staticmethod
    def revokes3FileAndRequestObject(self, couponSeriesId,couponData, revokeTypeIndex):
        invalidateDict = {'uploadedFileName': constant.config['uploadedFileName'] + '_revokeFile'}
        filehandle = FileHelper(constant.luciS3FilePath)
        filehandle.eraseContentFromFile()
        revokeType = ['COUPON_SERIES', 'ONLY_UNISSUED', 'userId', 'couponCode', 'couponId', 'CUSTOMER_AND_COUPON']
        if revokeType[revokeTypeIndex] == 'userId':
            filehandle.appendToFile(revokeType[revokeTypeIndex])
            invalidateDict.update({'revokeHeaders': {'userId': 0}})
        elif revokeType[revokeTypeIndex] == 'couponCode':
            filehandle.appendToFile(revokeType[revokeTypeIndex])
            invalidateDict.update({'revokeHeaders': {'couponCode': 0}})
        elif revokeType[revokeTypeIndex] == 'couponId':
            filehandle.appendToFile(revokeType[revokeTypeIndex])
            invalidateDict.update({'revokeHeaders': {'couponId': 0}})
        elif revokeType[revokeTypeIndex] == 'CUSTOMER_AND_COUPON':
            filehandle.appendToFile('userId,couponCode')
            invalidateDict.update({'revokeHeaders': {'userId': 1, 'couponCode' : 0}})
        for eachData in couponData:
            filehandle.appendToFile(eachData)
        invalidateDict.update({'S3FilePath': DracarysHelper.s3FileUpload(self, couponSeriesId)})
        return invalidateDict

    @staticmethod
    def downloadFile(self, s3File):
        data = DracarysHelper.s3FileDownload(self, s3File).splitlines()
        dataiters = iter(data)
        valuesToReturn = []
        isHeader = True
        for x in dataiters:
            if isHeader:
                isHeader = False
            else:
                y = x.split(',')
                valuesToReturn.append({'errorMsg': y[0], 'couponCode': y[1], 'couponId': y[2].strip() if y[2].strip() == 'NA' else int(y[2]), 'userId' : y[3].strip() if y[3].strip() == 'NA' else int(y[3])})
        return valuesToReturn

    @staticmethod
    def isNumeric(couponCode):
        try:
            int(couponCode)
            return True
        except ValueError:
            return False

    @staticmethod
    def getBulkUsers(noOfUsers = 100):
        bulkUserIds = []
        for _ in range(noOfUsers):
            bulkUserIds.append(randValues.randomInteger(9))
        return list(set(bulkUserIds))