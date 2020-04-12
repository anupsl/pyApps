import datetime
import time
import random

import pytest

from src.Constant.constant import constant
from src.modules.luci.luciHelper import LuciHelper
from src.modules.luci.luciObject import LuciObject
from src.utilities.assertion import Assertion
from src.utilities.logger import Logger


class Test_MultiInstanceCouponConfig():

    def setup_class(self):
        Logger.logSuiteName(str(self).split('.')[-1])

    def setup_method(self, method):
        Logger.logMethodName(method.__name__)
        constant.config['requestId'] = 'luci_auto_' + str(random.randint(11111, 99999))
        self.tillId = constant.config['tillIds'][0]
        self.billId = str(random.randint(11111, 99999))

    @pytest.mark.parametrize('description', ['S1.save coupon config. S2.update coupon config. S1.coupon config '
                                             'updated after 60 seconds'])
    def test_MULTI_INSTANCE_SCC_UCC_GCC_001(self, description):
        Logger.log('starting test_SCC_UCC_GCC_01_MULTI_INSTANCE execution')
        if not LuciHelper.verifyLuciServicesCount(2):
            pytest.skip("test requires minimum of 2 luci services running")

        self.connObj = LuciHelper.getFirstConn(newConnection=True)
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self)

        time.sleep(2)
        # update coupon config after some time on second server
        self.connObj = LuciHelper.getSecondConn(newConnection=True)
        dat = datetime.datetime.now() + datetime.timedelta(days=3)
        owner_validity = int(time.mktime(dat.timetuple()) * 1e3)
        couponConfigObj.update({'alphaNumeric': False, 'shortCodeLength': 4, 'ownerValidity': owner_validity,
                                'max_vouchers_per_user': 5})
        LuciHelper.saveCouponConfigAndAssertions(self, couponConfigObj)

        # get updated coupon config on second server
        config1 = LuciHelper.getCouponConfigAndAssertion(self, couponSeriesId)
        Assertion.constructAssertion(config1['alphaNumeric'] is False, 'alphanumeric config key updated')
        Assertion.constructAssertion(config1['shortCodeLength'] == 4, 'short code length updated')
        Assertion.constructAssertion(config1['ownerValidity'] == owner_validity, 'owner validity is updated')
        Assertion.constructAssertion(config1['max_vouchers_per_user'] == 5, 'max voucher per user is updated')

        # wait for coupon config to change on first server
        self.connObj = LuciHelper.getFirstConn(newConnection=True)
        configChanged = False
        config2 = None
        for _ in range(7):
            config2 = LuciHelper.getCouponConfigAndAssertion(self, couponSeriesId)
            if config2['alphaNumeric'] is not None:
                configChanged = True
                break
            time.sleep(10)

        if configChanged is True:
            Assertion.constructAssertion(config2['alphaNumeric'] is False, 'alphanumeric config key updated')
            Assertion.constructAssertion(config2['shortCodeLength'] == 4, 'short code length updated')
            Assertion.constructAssertion(config2['ownerValidity'] == owner_validity, 'owner validity is updated')
            Assertion.constructAssertion(config2['max_vouchers_per_user'] == 5, 'max voucher per user is updated')
        else:
            Assertion.constructAssertion(False, 'Coupon config is not updated in second server')

    @pytest.mark.parametrize('description', ['S1. save coupon config S2.issue coupon, update config. S1. search coupon'])
    def test_MULTI_INSTANCE_SCC_IC_CS_002(self, description):
        Logger.log('starting test_SCC_IC_CS_002_MULTI_INSTANCE execution')
        if not LuciHelper.verifyLuciServicesCount(2):
            pytest.skip("test requires minimum of 2 luci services running")

        self.connObj = LuciHelper.getFirstConn(newConnection=True)
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self)

        self.connObj = LuciHelper.getSecondConn(newConnection=True)
        userId = random.randint(1111111, 9999999)
        issueCouponObj = {'couponSeriesId': couponSeriesId, 'storeUnitId': self.tillId, 'userId': userId}
        issueCouponRequest = LuciObject.issueCouponRequest(issueCouponObj)
        coupon_details = self.connObj.issueCoupon(issueCouponRequest).__dict__
        Assertion.constructAssertion(coupon_details['couponCode'] is not None, 'Coupon code is not null')

        time.sleep(2)
        # update coupon config on second server
        dat = datetime.datetime.now() + datetime.timedelta(days=3)
        owner_validity = int(time.mktime(dat.timetuple()) * 1e3)
        couponConfigObj.update({'alphaNumeric': False, 'shortCodeLength': 4, 'ownerValidity': owner_validity,
                                'max_vouchers_per_user': 5})
        LuciHelper.saveCouponConfigAndAssertions(self, couponConfigObj)
        config1 = LuciHelper.getCouponConfigAndAssertion(self, couponSeriesId, no_issued=1)
        Assertion.constructAssertion(config1['alphaNumeric'] is False, 'alphanumeric config key updated')
        Assertion.constructAssertion(config1['shortCodeLength'] == 4, 'short code length updated')
        Assertion.constructAssertion(config1['ownerValidity'] == owner_validity, 'owner validity is updated')
        Assertion.constructAssertion(config1['max_vouchers_per_user'] == 5, 'max voucher per user is updated')

        self.connObj = LuciHelper.getFirstConn(newConnection=True)
        couponSearchRequest = {'couponSeriesIds': [couponSeriesId], 'customerIds': [userId], 'couponSeriesRequired': True}

        couponDetailsList = None
        for _ in range(7):
            couponDetailsResponse = self.connObj.couponSearch(LuciObject.couponSearchRequest(couponSearchRequest)).__dict__
            couponDetailsList = couponDetailsResponse['coupons']
            if len(couponDetailsList) == 1 and vars(vars(couponDetailsResponse['coupons'][0])['couponSeries'])['alphaNumeric'] is not None:
                break
            time.sleep(10)

        Assertion.constructAssertion(len(couponDetailsList) == 1,
                                     'Coupon Details list, Actual  {} and Expected 1'.format(len(couponDetailsList)))

        for i in range(len(couponDetailsList)):
            couponDetails = couponDetailsList[i].__dict__
            Assertion.constructAssertion(vars(couponDetails['couponSeries'])['alphaNumeric'] is False, 'alphanumeric config key updated')
            Assertion.constructAssertion(vars(couponDetails['couponSeries'])['shortCodeLength'] == 4, 'short code length updated')
            Assertion.constructAssertion(vars(couponDetails['couponSeries'])['ownerValidity'] == owner_validity, 'owner validity is updated')
            Assertion.constructAssertion(vars(couponDetails['couponSeries'])['max_vouchers_per_user'] == 5, 'max voucher per user is updated')
