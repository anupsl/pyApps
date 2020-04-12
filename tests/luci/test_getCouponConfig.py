import time,pytest, random
from src.Constant.constant import constant
from src.modules.luci.luciDBHelper import LuciDBHelper
from src.utilities.logger import Logger
from src.utilities.assertion import Assertion
from src.utilities.utils import Utils
from src.utilities.randValues import randValues
from src.modules.luci.luciHelper import LuciHelper
from src.modules.luci.luciObject import LuciObject

class Test_getCouponConfig():

    def setup_class(self):
        Logger.logSuiteName(str(self).split('.')[-1])
        self.connObj = LuciHelper.getConnObj(newConnection=True)
        self.constructObj = LuciObject()
        self.userId = constant.config['usersInfo'][0]['userId']
        self.tillId = constant.config['tillIds'][0]
        self.storeId = constant.config['storeIds'][0]
        self.billId = Utils.getTime(milliSeconds=True)
        self.couponConfig1, self.couponSeriesId1 = LuciHelper.saveCouponConfigAndAssertions(self, {'client_handling_type': 'DISC_CODE_PIN', 'created' : Utils.getTime(seconds=0, milliSeconds=True) ,'valid_till_date' : Utils.getTime(days=1, milliSeconds=True), 'alphaNumeric' : False, 'randomCodeLength' : 8})
        self.couponConfig2, self.couponSeriesId2 = LuciHelper.saveCouponConfigAndAssertions(self, {'client_handling_type': 'DISC_CODE_PIN','created' : Utils.getTime(seconds=1, milliSeconds=True) ,'valid_till_date' : Utils.getTime(days=1, milliSeconds=True), 'alphaNumeric' : False, 'randomCodeLength' : 8})
        self.couponConfig3, self.couponSeriesId3 = LuciHelper.saveCouponConfigAndAssertions(self, {'client_handling_type': 'DISC_CODE_PIN','created' : Utils.getTime(seconds=2, milliSeconds=True) ,'valid_till_date' : Utils.getTime(days=1, milliSeconds=True), 'alphaNumeric' : False, 'randomCodeLength' : 8})
        self.couponConfig4, self.couponSeriesId4 = LuciHelper.saveCouponConfigAndAssertions(self, {'client_handling_type': 'DISC_CODE_PIN','created' : Utils.getTime(seconds=3, milliSeconds=True) ,'valid_till_date' : Utils.getTime(days=1, milliSeconds=True), 'alphaNumeric' : False, 'randomCodeLength' : 8})
        self.couponConfig5, self.couponSeriesId5 = LuciHelper.saveCouponConfigAndAssertions(self, {'client_handling_type': 'DISC_CODE_PIN','created' : Utils.getTime(seconds=4, milliSeconds=True) ,'valid_till_date' : Utils.getTime(days=1, milliSeconds=True), 'alphaNumeric' : False, 'randomCodeLength' : 8})


    def setup_method(self, method):
        self.connObj = LuciHelper.getConnObj(newConnection=True)
        Logger.logMethodName(method.__name__)
        constant.config['requestId'] = 'luci_auto_'+str(random.randint(11111, 99999))

    @pytest.mark.parametrize('description, ownerValues', [
        ('GetCouponConfig by ownerBy & ownedId', [1, 123])])
    def test_LUCI_GCC_001(self, description,ownerValues):
        configRequest = LuciObject.getCouponConfigRequest({'ownedBy' : ownerValues[0]})
        couponConfigList = self.connObj.getCouponConfiguration(configRequest)
        Assertion.constructAssertion(couponConfigList != None, 'Retrieved couponConfig from GetCouponConfig by OwnedBy')
        configRequest = LuciObject.getCouponConfigRequest({'ownerId': ownerValues[1]})
        couponConfigList = self.connObj.getCouponConfiguration(configRequest)
        Assertion.constructAssertion(couponConfigList != None, 'Retrieved couponConfig from GetCouponConfig by OwnedId')

    @pytest.mark.parametrize('description', [('GetCouponConfig order by created date Descending')])
    def test_LUCI_GCC_002(self, description):
        couponSeriesDesc = [self.couponSeriesId5, self.couponSeriesId4, self.couponSeriesId3, self.couponSeriesId2, self.couponSeriesId1]
        configRequest = LuciObject.getCouponConfigRequest({'orderBy' : self.constructObj.couponConfigOrderBy['CREATED_DATE'], 'sort' : self.constructObj.sort['DESC'], 'limit' : 5})
        couponConfigList = self.connObj.getCouponConfiguration(configRequest)
        Assertion.constructAssertion(len(couponConfigList) == 5, 'GetCouponConfig Limit {} and couponconfig got {}'.format(5, len(couponConfigList)))
        for couponConfig in couponConfigList:
            couponConfig = couponConfig.__dict__
            Logger.log('Coupon Config Ids : ' , couponConfig['id'] )
            Assertion.constructAssertion(couponConfig['id'] in couponSeriesDesc, 'GetCouponConfig CouponSeriesId sort by desc order by Created Date Actual :{} and Excepted : {}'.format(couponConfig['id'],couponSeriesDesc))

    @pytest.mark.parametrize('description', [('GetCouponConfig order by created date Ascending')])
    def test_LUCI_GCC_003(self, description):
        couponSeriesAsc = [self.couponSeriesId1, self.couponSeriesId2, self.couponSeriesId3, self.couponSeriesId4, self.couponSeriesId5]
        configRequest = LuciObject.getCouponConfigRequest({'orderBy' : self.constructObj.couponConfigOrderBy['CREATED_DATE'], 'sort' : self.constructObj.sort['ASC'], 'limit' : 5})
        couponConfigList = self.connObj.getCouponConfiguration(configRequest)
        Assertion.constructAssertion(len(couponConfigList) == 5, 'GetCouponConfig Limit {} and couponconfig got {}'.format(5, len(couponConfigList)))
        for couponConfig in couponConfigList:
            couponConfig = couponConfig.__dict__
            Logger.log('Coupon Config Ids : ' , couponConfig['id'] )
            Assertion.constructAssertion(couponConfig['id'] not in couponSeriesAsc, 'GetCouponConfig CouponSeriesId sort by desc order by Created Date Actual :{} and Excepted : {}'.format(couponConfig['id'],couponSeriesAsc))

    @pytest.mark.parametrize('description', [
        ('GetCouponConfig order by last used sort Asc')])
    def test_LUCI_GCC_004(self, description):
        self.couponConfig4.update({'description' : 'Luci desc updated'})
        LuciHelper.saveCouponConfigAndAssertions(self,self.couponConfig4)
        time.sleep(2)
        self.couponConfig1.update({'description' : 'Luci desc updated'})
        LuciHelper.saveCouponConfigAndAssertions(self, self.couponConfig1)
        time.sleep(2)
        self.couponConfig3.update({'description' : 'Luci desc updated'})
        LuciHelper.saveCouponConfigAndAssertions(self, self.couponConfig3)
        time.sleep(2)
        self.couponConfig5.update({'description' : 'Luci desc updated'})
        LuciHelper.saveCouponConfigAndAssertions(self, self.couponConfig5)
        time.sleep(2)
        self.couponConfig2.update({'description' : 'Luci desc updated'})
        LuciHelper.saveCouponConfigAndAssertions(self, self.couponConfig2)

        couponSeriesDesc = [self.couponSeriesId2, self.couponSeriesId5, self.couponSeriesId3, self.couponSeriesId1, self.couponSeriesId4]
        configRequest = LuciObject.getCouponConfigRequest({'orderBy' : self.constructObj.couponConfigOrderBy['LAST_MODIFIED_DATE'], 'sort' : self.constructObj.sort['DESC'], 'limit' : 5})
        couponConfigList = self.connObj.getCouponConfiguration(configRequest)
        Assertion.constructAssertion(len(couponConfigList) == 5, 'GetCouponConfig Limit {} and couponconfig got {}'.format(5, len(couponConfigList)))
        for couponConfig,couponSeriesId in zip(couponConfigList,couponSeriesDesc):
            couponConfig = couponConfig.__dict__
            Logger.log('Coupon Config Ids : ' , couponConfig['id'] )
            Assertion.constructAssertion(couponConfig['id'] == couponSeriesId , 'GetCouponConfig CouponSeriesId sort by desc order by Created Date Actual :{} and Excepted : {}'.format(couponConfig['id'],couponSeriesId))

    @pytest.mark.parametrize('description, ownerValues', [
        ('GetCouponConfig by ownerBy & ownedId with limit 5', [1, 123])])
    def test_LUCI_GCC_005(self, description,ownerValues):
        configRequest = LuciObject.getCouponConfigRequest({'ownedBy' : ownerValues[0], 'includeExpired' : True, 'limit' : 5})
        couponConfigList = self.connObj.getCouponConfiguration(configRequest)
        Assertion.constructAssertion(len(couponConfigList) == 5, 'GetCouponConfig Limit {} and couponconfig got {}'.format(5, len(couponConfigList)))
        Assertion.constructAssertion(couponConfigList != None, 'Retrieved couponConfig from GetCouponConfig by OwnedBy')
        configRequest = LuciObject.getCouponConfigRequest({'ownerId': ownerValues[1]})
        couponConfigList = self.connObj.getCouponConfiguration(configRequest)
        Assertion.constructAssertion(couponConfigList != None, 'Retrieved couponConfig from GetCouponConfig by OwnedId')

    @pytest.mark.parametrize('description, getCouponRequest', [
        ('GetCouponConfig by description and expired True', {'seriesDescription' : 'luci testing', 'limit' : 5, 'includeExpired' : True, 'orderBy' : 1}),
        ('GetCouponConfig by limit 5', {'limit' : 5}),
        ('GetCouponConfig by search with series description', {'seriesDescription' : 'ci test', 'limit' : 5}),
        ('GetCouponConfig by search with series description', {'seriesDescription' : 'luci', 'limit' : 5}),])
    def test_LUCI_GCC_006(self, description,getCouponRequest):
        configRequest = LuciObject.getCouponConfigRequest(getCouponRequest)
        couponConfigList = self.connObj.getCouponConfiguration(configRequest)
        Logger.log('Log Details : ', len(couponConfigList))
        Assertion.constructAssertion(len(couponConfigList) == 5, 'GetCouponConfig Limit {} and couponconfig got {}'.format(5, len(couponConfigList)))
        Assertion.constructAssertion(couponConfigList != None, 'Retrieved couponConfig from GetCouponConfig by OwnedBy')

    @pytest.mark.parametrize('description', [('Latest issued & redeem time')])
    def test_LUCI_GCC_007(self, description):
        couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self)[1]
        couponCode, couponDetailsFirst = LuciHelper.issueCouponAndAssertions(self,couponSeriesId)
        redeemDetailsFirst = LuciHelper.redeemCouponAndAssertions(self,couponSeriesId,couponCode)
        time.sleep(5)
        self.userId = constant.config['usersInfo'][1]['userId']
        couponCode, couponDetailsLatest = LuciHelper.issueCouponAndAssertions(self,couponSeriesId)
        redeemDetailsLatest = LuciHelper.redeemCouponAndAssertions(self,couponSeriesId,couponCode)
        config = LuciHelper.getCouponConfigAndAssertion(self,couponSeriesId,2,2)
        Assertion.constructAssertion(couponDetailsFirst['issuedDate'] != config['latestIssualTime'], 'Latest issual time is mismatch ' )
        Assertion.constructAssertion(redeemDetailsFirst['redemptionDate'] != config['latestRedemptionTime'], 'Latest redemption time is mismatch' )
        Assertion.constructAssertion(couponDetailsLatest['issuedDate'] == config['latestIssualTime'], 'Latest issual time in getCouponConfig' )
        Assertion.constructAssertion(redeemDetailsLatest['redemptionDate'] == config['latestRedemptionTime'], 'Latest redemption time in getCouponConfig' )

    @pytest.mark.parametrize('description', [('GetCouponConfig by include umclaimed & claimed')])
    def test_LUCI_GCC_008(self, description):
        randomValueCamp = randValues.randomInteger(digits=6)
        couponConfig, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self, {'client_handling_type': 'DISC_CODE_PIN', 'created': Utils.getTime(seconds=0, milliSeconds=True), 'valid_till_date': Utils.getTime(days=1, milliSeconds=True), 'campaign_id' : randomValueCamp})
        configRequest = LuciObject.getCouponConfigRequest({'ownerId' : randomValueCamp, 'sort' : 1,  'includeUnclaimed' : True,  'limit' : 5 })
        couponConfigList = self.connObj.getCouponConfiguration(configRequest)
        for couponRes in couponConfigList:
            couponRes = couponRes.__dict__
            if couponRes['id'] == couponSeriesId:
                Assertion.constructAssertion(couponRes['owned_by'] == self.constructObj.ownedBy['OUTBOUND'], 'OwnedBy value is Matched Actual: {} and Expected: {}'.format(couponRes['owned_by'] , self.constructObj.ownedBy['OUTBOUND']))
                Assertion.constructAssertion(couponRes['owner_id'] == randomValueCamp, 'OwnerId is Matched Actual: {} and Expected: {}'.format(couponRes['owner_id'], randomValueCamp))
                break
        Assertion.constructAssertion(len(couponConfigList) == 5, 'GetCouponConfig Limit {} and couponconfig got {}'.format(5, len(couponConfigList)))
        Assertion.constructAssertion(couponConfigList != None, 'Retrieved couponConfig from GetCouponConfig by OwnedBy')

    @pytest.mark.parametrize('description, requestFilter',[
        ('GetAll couponConfig with filters', {'orderBy': 1, 'sort': 1, 'limit': 5, 'offset' : 0}),
        ('GetAll couponConfig with filters', {'orderBy': 1, 'sort': 0, 'limit': 5, 'offset' : 1, 'includeExpired': True}),
        ('GetAll couponConfig with filters', {'orderBy': 0, 'sort': 1, 'limit': 5, 'includeExpired': False}),
        ('GetAll couponConfig with filters', {'orderBy': 0, 'sort': 0, 'limit': 5, 'includeExpired': True})
    ])
    def test_LUCI_GCC_009_sanity(self, description, requestFilter):
        configRequest = LuciObject.getCouponConfigRequest(requestFilter)
        couponConfigList = self.connObj.getCouponConfiguration(configRequest)
        getAllResponseList = self.connObj.getAllCouponConfigurations(LuciObject.getAllCouponConfigRequest(requestFilter))
        Assertion.constructAssertion(len(couponConfigList) == len(getAllResponseList), 'GetCouponConfig & GetAllConfig List size {} and {} is matched'.format(len(couponConfigList),len(getAllResponseList)))
        for getConfigCouponSeries,getAllConfigCouponSeries in zip(couponConfigList,getAllResponseList):
            getConfigCouponSeries = getConfigCouponSeries.__dict__
            getAllConfigCouponSeries = getAllConfigCouponSeries.__dict__
            Assertion.constructAssertion(getConfigCouponSeries['id'] == getAllConfigCouponSeries['id'] , 'GetCouponConfig & GetAllConfig CouponSeriesId is Matched {} and {}'.format(getConfigCouponSeries['id'],getAllConfigCouponSeries['id']))