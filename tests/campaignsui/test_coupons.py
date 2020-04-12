import pytest, time, os, sys, pytest_ordering
from src.utilities.logger import Logger
from src.utilities.assertion import Assertion
from src.Constant.constant import constant
from src.modules.campaignUIPages.loginPage import loginPage
from src.modules.campaignUIPages.campaignCreatePage import campaignCreatePage
from src.modules.campaignUIPages.incentivePage import incentivePage
from src.modules.campaignUIPages.listPage import listPage
from src.modules.campaignUIPages.messagePage import messagePage
from src.seleniumBase.WebdriverFactory import WebDriverFactory
from src.seleniumBase.SeleniumDriver import SeleniumDriver


@pytest.mark.run(order=1)
class Test_CouponsUI(object, SeleniumDriver):

    def setup_class(self):
        self.driver = WebDriverFactory().getWebDriverInstance()
        self.loginPage = loginPage(self.driver)
        self.createCampaignPage = campaignCreatePage(self.driver)
        self.incentivePage = incentivePage(self.driver)
        self.listPage = listPage(self.driver, newFilterEnabled=True)
        self.messagePage = messagePage(self.driver)
        self.loginPage.login(userName=constant.config['intouchUsername'], password=constant.config['intouchPassword'])
        self.loginPage.switchOrgUsingCookies()

    def teardown_class(self):
        try:
            self.driver.quit()
        except Exception, exp:
            assert False, 'Exception Occured while Closing Browser , Need to Close Browser manually'

    @pytest.mark.parametrize('description, couponType', [
        ('Create Disc Code Coupon series', 'DISC_CODE'),
        ('Create Disc Code Pin coupon series', 'DISC_CODE_PIN'),
        ('Create Generic coupon series', 'GENERIC'),
        ('Create Generic coupon series', 'EXTERNAL')
    ])
    def test_couponsUI_createCouponSeries(self,request, description, couponType):
        try:
            couponName = 'coupon_' + str(int(time.time()))
            self.incentivePage.createCoupons(couponName, couponType)
            self.incentivePage.previewAndSave()
            self.incentivePage.searchCouponAndVerify(couponName)
        except Exception, exp:
            self.getScreenshot(request.node.name)
            Assertion.constructAssertion(False, self.getBrowserErrorLogs(exp))

    @pytest.mark.parametrize('description, couponType', [
        ('Create coupon series with Mutual Exclusive', 'DISC_CODE_PIN')
    ])
    def test_couponsUI_mutualExclusive(self,request, description, couponType):
        try:
            couponName = 'coupon_' + str(int(time.time()))
            self.incentivePage.createCoupons(couponName, couponType)
            self.incentivePage.addMutualExclusiveCouponSeries('coupon')
            self.incentivePage.previewAndSave()
            self.incentivePage.searchCouponAndVerify(couponName)
        except Exception, exp:
            self.getScreenshot(request.node.name)
            Assertion.constructAssertion(False, self.getBrowserErrorLogs(exp))

    @pytest.mark.parametrize('description, couponType', [
        ('Create coupon series with Mutual Exclusive', 'DISC_CODE_PIN')
    ])
    def test_couponsUI_ExpiryReminder(self,request, description, couponType):
        try:
            couponName = 'coupon_' + str(int(time.time()))
            self.incentivePage.createCoupons(couponName, couponType)
            self.incentivePage.addMutualExclusiveCouponSeries('coupon')
            self.incentivePage.previewAndSave()
            self.incentivePage.searchCouponAndVerify(couponName)
        except Exception, exp:
            self.getScreenshot(request.node.name)
            Assertion.constructAssertion(False, self.getBrowserErrorLogs(exp))

    @pytest.mark.parametrize('description, couponType', [
        ('Create coupon series with Expiry Reminder', 'DISC_CODE_PIN')
    ])
    def test_couponsUI_ExpiryReminder(self,request, description, couponType):
        try:
            couponName = 'coupon_' + str(int(time.time()))
            self.incentivePage.createCoupons(couponName, couponType)
            self.incentivePage.addExpiryReminder('Automated SMS reminder {{first_name}} {{voucher}} {{optout}}')
            self.incentivePage.previewAndSave()
            self.incentivePage.searchCouponAndVerify(couponName)
        except Exception, exp:
            self.getScreenshot(request.node.name)
            Assertion.constructAssertion(False, self.getBrowserErrorLogs(exp))

    @pytest.mark.parametrize('description, couponType', [
        ('Create coupon series with Re-Issue coupon Enable', 'DISC_CODE_PIN')
    ])
    def test_couponsUI_reIssueEnable(self,request, description, couponType):
        try:
            couponName = 'coupon_' + str(int(time.time()))
            self.incentivePage.createCoupons(couponName, couponType)
            self.incentivePage.advanceSettingSearch('Max issuals per customer')
            self.incentivePage.reIssueCouponEnable()
            self.incentivePage.advanceSettingSearch('Allow a coupon to be redeemed more than once')
            self.incentivePage.allowMultipleRedemption()
            self.incentivePage.advanceSettingSearch('Stores allowing redemption')
            self.incentivePage.redeemTillsSelections()
            self.incentivePage.previewAndSave()
            self.incentivePage.searchCouponAndVerify(couponName)
        except Exception, exp:
            self.getScreenshot(request.node.name)
            Assertion.constructAssertion(False, self.getBrowserErrorLogs(exp))

    @pytest.mark.parametrize('description, couponType', [
        ('Create coupon series with Re-Issue coupon Enable', 'DISC_CODE_PIN')
    ])
    def test_couponsUI_resendSMSTemplate(self,request, description, couponType):
        try:
            couponName = 'coupon_' + str(int(time.time()))
            self.incentivePage.createCoupons(couponName, couponType)
            self.incentivePage.advanceSettingSearch('SMS content for resending the coupon')
            self.incentivePage.resendSMSTemplate('Automated SMS reminder {{first_name}} {{voucher}} ')
            self.incentivePage.previewAndSave()
            self.incentivePage.searchCouponAndVerify(couponName)
            updateOfferName = 'Updated ' + couponName
            self.incentivePage.editOfferAndSave(couponName, updateOfferName)
            self.incentivePage.searchCouponAndVerify(updateOfferName)

        except Exception, exp:
            self.getScreenshot(request.node.name)
            Assertion.constructAssertion(False, self.getBrowserErrorLogs(exp))

    @pytest.mark.parametrize('description, couponType', [
        ('Claim Coupon series within campaign', 'DISC_CODE_PIN')
    ])
    def test_couponsUI_claimCouponSeries(self, request, description, couponType):
        try:
            couponName = 'coupon_' + str(int(time.time()))
            self.incentivePage.createCoupons(couponName, couponType)
            self.incentivePage.previewAndSave()
            self.navigateToURL(constant.config['intouchUrl'])
            campaignName = 'CouponsUI_' + str(int(time.time()))
            self.createCampaignPage.createCampaignAndVerify(campaignName=campaignName)
            self.createCampaignPage.goToIncentivePage()
            self.incentivePage.claimCouponSeries(couponName)
            Assertion.constructAssertion(self.incentivePage.verifyCouponCreation(couponName), 'Coupon Creation Validation')
            self.createCampaignPage.goToOverviewpage()
            constant.config['incentives']['coupon']['name'] = couponName
        except Exception, exp:
            self.getScreenshot(request.node.name)
            Assertion.constructAssertion(False, self.getBrowserErrorLogs(exp))