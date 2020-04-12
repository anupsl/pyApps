import pytest, time, os, sys, pytest_ordering
from src.utilities.logger import Logger
from src.utilities.assertion import Assertion
from src.Constant.constant import constant
from src.modules.iris.construct import construct
from src.modules.campaignUIPages.campaignsUIDBCalls import DBCallsCampaigns
from src.modules.campaignUIPages.loginPage import loginPage
from src.modules.campaignUIPages.campaignCreatePage import campaignCreatePage
from src.modules.campaignUIPages.incentivePage import incentivePage
from src.modules.campaignUIPages.listPage import listPage
from src.modules.campaignUIPages.messagePage import messagePage
from src.seleniumBase.WebdriverFactory import WebDriverFactory
from src.seleniumBase.browserLogs import browserLogs
from src.seleniumBase.SeleniumDriver import SeleniumDriver

@pytest.mark.run(order=1)
class Test_CampaignsUI(object, SeleniumDriver):
    
    def setup_class(self):
        self.driver = WebDriverFactory().getWebDriverInstance()
        self.loginPage = loginPage(self.driver)
        self.createCampaignPage = campaignCreatePage(self.driver)
        self.incentivePage = incentivePage(self.driver)
        self.listPage = listPage(self.driver, newFilterEnabled=True)
        self.messagePage = messagePage(self.driver)
        self.loginPage.login(userName=constant.config['intouchUsername'], password=constant.config['intouchPassword'])

    def teardown_class(self):
        try:
            self.driver.quit()
        except Exception, exp:
            assert False , 'Exception Occured while Closing Browser , Need to Close Browser manually'
        finally:
            Logger.log('CampaignsDefault Value Set is :' + str(constant.campaignuiDetails))
        
    def test_createCampaign_Sanity(self, request):
        Logger.log('Create Campaign Started')
        try:
            campaignName = 'campaignUI_' + str(int(time.time()))
            self.createCampaignPage.createCampaignAndVerify(campaignName=campaignName)
        except Exception, exp:
            self.getScreenshot(request.node.name)
            Assertion.constructAssertion(False, exp)
            
    def est_createCoupons_Sanity(self, request):
        self.createCampaignPage.navigateBackToCampaignsOverviewPage()
        try:
            couponName = 'coupon_' + str(int(time.time()))
            self.createCampaignPage.goToIncentivePage()
            self.incentivePage.createNewCoupon(couponName=couponName)
            Assertion.constructAssertion(self.incentivePage.verifyCouponCreation(couponName), 'Coupon Creation Validation')
            self.createCampaignPage.goToOverviewpage()
            constant.config['incentives']['coupon']['name'] = couponName
        except Exception, exp:
            self.getScreenshot(request.node.name)
            Assertion.constructAssertion(False, exp)
    
    @pytest.mark.parametrize('filterType,listName', [
        ('loyalty', constant.config['list']['loyalty']['name']),
        ('paste', constant.config['list']['paste']['name']),
        ])        
    def test_createList_Sanity(self, request, filterType, listName):
        self.createCampaignPage.navigateBackToCampaignsOverviewPage()
        try:
            self.createCampaignPage.goToListPage()
            self.listPage.selectFilterType(filterType)
            self.listPage.switchToListFrame(filterType)
            self.listPage.saveListAsPerFilterType(filterType=filterType, listName=listName)
            self.listPage.switchToDefaultFromListPage()
            groupVersionId = self.listPage.verifyListCreated(constant.config['campaign']['id'], listName)
            constant.config['list'][filterType]['id'] = groupVersionId
        except Exception, exp:
            self.getScreenshot(request.node.name)
            Assertion.constructAssertion(False, 'Failure While Creating List with Exception :{}'.format(exp))
    
    @pytest.mark.parametrize('filterType,listName', [
        ('nonloyalty', constant.config['list']['nonloyalty']['name']),
        ('upload', constant.config['list']['upload']['name'])
        ])        
    def test_createList_Regression(self, request, filterType, listName):
        self.createCampaignPage.navigateBackToCampaignsOverviewPage()
        try:
            self.createCampaignPage.goToListPage()
            self.listPage.selectFilterType(filterType)
            self.listPage.switchToListFrame(filterType)
            self.listPage.saveListAsPerFilterType(filterType=filterType, listName=listName)
            self.listPage.switchToDefaultFromListPage()
            groupVersionId = self.listPage.verifyListCreated(constant.config['campaign']['id'], listName)
            constant.config['list'][filterType]['id'] = groupVersionId
        except Exception, exp:
            self.getScreenshot(request.node.name)
            Assertion.constructAssertion(False, 'Failure While Creating List with Exception :{}'.format(exp))
    


    @pytest.mark.parametrize('messageType,listType,incentiveType,templateName', [
        ('sms', 'loyalty', 'nodeal', constant.config['templateName']['sms']['nodeal']),
        ])   
    def test_createMessage_sms_channel_Sanity(self, request, messageType, listType, incentiveType, templateName):
        self.createCampaignPage.navigateBackToCampaignsOverviewPage(dependencies={'list':['loyalty']})
        try:
            self.createCampaignPage.goToMessagePage(messageType)
            self.messagePage.chooseRecipient(constant.config['list'][listType]['name'])
            self.messagePage.attachIncentive(incentiveType)
            self.messagePage.customizeContent(templateName)
            self.messagePage.deliverySetting()
            self.createCampaignPage.authorizePresentCampaignOnPage()
            self.messagePage.verifyAuthorizeCampaign(constant.config['campaign']['id'], constant.config['list'][listType]['id'])
        except Exception, exp:
            self.getScreenshot(request.node.name)
            Assertion.constructAssertion(False, 'Failure with Exception :{}'.format(exp))

    @pytest.mark.parametrize('messageType,listType,incentiveType,templateName', [
        ('sms', 'loyalty', 'coupon', constant.config['templateName']['sms']['coupon']),
        ('sms', 'loyalty', 'point', constant.config['templateName']['sms']['point']),
        ('sms', 'loyalty', 'generic', constant.config['templateName']['sms']['generic'])
        ])   
    def test_createMessage_sms_differentIncentives(self, request, messageType, listType, incentiveType, templateName):
        self.createCampaignPage.navigateBackToCampaignsOverviewPage(dependencies={'coupon':'', 'list':['loyalty']})
        try:
            self.createCampaignPage.goToMessagePage(messageType)
            self.messagePage.chooseRecipient(constant.config['list'][listType]['name'])
            self.messagePage.attachIncentive(incentiveType)
            self.messagePage.customizeContent(templateName)
            self.messagePage.deliverySetting()
            self.createCampaignPage.authorizePresentCampaignOnPage()
            self.messagePage.verifyAuthorizeCampaign(constant.config['campaign']['id'], constant.config['list'][listType]['id'])
        except Exception, exp:
            self.getScreenshot(request.node.name)
            Assertion.constructAssertion(False, 'Failure While Creating List with Exception :{}'.format(exp))

    @pytest.mark.parametrize('messageType,listType,incentiveType,templateName', [
        ('sms', 'upload', 'nodeal', constant.config['templateName']['sms']['nodeal']),
        ('sms', 'loyalty', 'nodeal', constant.config['templateName']['sms']['nodeal']),
        ])   
    def test_createMessage_sms_differentListType(self, request, messageType, listType, incentiveType, templateName):
        self.createCampaignPage.navigateBackToCampaignsOverviewPage(dependencies={'list':['loyalty', 'upload']})
        try:
            self.createCampaignPage.goToMessagePage(messageType)
            self.messagePage.chooseRecipient(constant.config['list'][listType]['name'])
            self.messagePage.attachIncentive(incentiveType)
            self.messagePage.customizeContent(templateName)
            self.messagePage.deliverySetting()
            self.createCampaignPage.authorizePresentCampaignOnPage()
            self.messagePage.verifyAuthorizeCampaign(constant.config['campaign']['id'], constant.config['list'][listType]['id'])
        except Exception, exp:
            self.getScreenshot(request.node.name)
            Assertion.constructAssertion(False, 'Failure with Exception :{}'.format(exp))

    @pytest.mark.parametrize('messageType,listType,incentiveType,templateName', [
        ('email', 'loyalty', 'nodeal', constant.config['templateName']['email']['nodeal']),
        ])
    def test_createMessage_email_channel_Sanity(self, request, messageType, listType, incentiveType, templateName):
        self.createCampaignPage.navigateBackToCampaignsOverviewPage(dependencies={'list':['loyalty']})
        try:
            self.createCampaignPage.goToMessagePage(messageType)
            self.messagePage.chooseRecipient(constant.config['list'][listType]['name'])
            self.messagePage.attachIncentive(incentiveType)
            self.messagePage.customizeContent(templateName, channel='email')
            self.messagePage.deliverySetting()
            self.createCampaignPage.authorizePresentCampaignOnPage()
            self.messagePage.verifyAuthorizeCampaign(constant.config['campaign']['id'], constant.config['list'][listType]['id'])
        except Exception, exp:
            self.getScreenshot(request.node.name)
            Assertion.constructAssertion(False, 'Failure with Exception :{}'.format(exp))

    @pytest.mark.parametrize('messageType,listType,incentiveType,templateName', [
        ('email', 'loyalty', 'generic', constant.config['templateName']['email']['generic']),
        ('email', 'loyalty', 'coupon', constant.config['templateName']['email']['coupon']),
        ('email', 'loyalty', 'point', constant.config['templateName']['email']['point']),
        ])   
    def test_createMessage_email_differentIncentives(self, request, messageType, listType, incentiveType, templateName):
        self.createCampaignPage.navigateBackToCampaignsOverviewPage(dependencies={'coupon':'', 'list':['loyalty']})
        try:
            self.createCampaignPage.goToMessagePage(messageType)
            self.messagePage.chooseRecipient(constant.config['list'][listType]['name'])
            self.messagePage.attachIncentive(incentiveType)
            self.messagePage.customizeContent(templateName, channel='email')
            self.messagePage.deliverySetting()
            self.createCampaignPage.authorizePresentCampaignOnPage()
            self.messagePage.verifyAuthorizeCampaign(constant.config['campaign']['id'], constant.config['list'][listType]['id'])
        except Exception, exp:
            self.getScreenshot(request.node.name)
            Assertion.constructAssertion(False, 'Failure with Exception :{}'.format(exp))

    @pytest.mark.parametrize('messageType,listType,incentiveType,templateName,scheduleType', [
        ('sms', 'loyalty', 'nodeal', constant.config['templateName']['sms']['nodeal'], 'On a fixed date'),
        ('sms', 'loyalty', 'nodeal', constant.config['templateName']['sms']['nodeal'], 'Recurring'),
        ])   
    def test_createMessage_nonImmediateCampaign_Sanity(self, request, messageType, listType, incentiveType, templateName, scheduleType):
        self.createCampaignPage.navigateBackToCampaignsOverviewPage(dependencies={'list':['loyalty']})
        try:
            self.createCampaignPage.goToMessagePage(messageType)
            self.messagePage.chooseRecipient(constant.config['list'][listType]['name'])
            self.messagePage.attachIncentive(incentiveType)
            self.messagePage.customizeContent(templateName)
            self.messagePage.deliverySetting(scheduleType)
            self.createCampaignPage.authorizePresentCampaignOnPage()
            time.sleep(70*4)
            self.messagePage.verifyAuthorizeCampaign(constant.config['campaign']['id'], constant.config['list'][listType]['id'],scheduleType=scheduleType,listName=constant.config['list'][listType]['name'])
        except Exception, exp:
            self.getScreenshot(request.node.name)
            Assertion.constructAssertion(False, 'Failure with Exception :{}'.format(exp))

    @pytest.mark.parametrize('messageType,listType,incentiveType,templateName', [
        ('sms', 'loyalty', 'nodeal', constant.config['templateName']['sms']['nodeal']),
        ('email', 'loyalty', 'nodeal', constant.config['templateName']['email']['nodeal']),
        ]) 
    def test_previewAndTest(self, request, messageType, listType, incentiveType, templateName):
        self.createCampaignPage.navigateBackToCampaignsOverviewPage(dependencies={'list':['loyalty']})
        try:
            self.createCampaignPage.goToMessagePage(messageType)
            self.messagePage.chooseRecipient(constant.config['list'][listType]['name'])
            self.messagePage.attachIncentive(incentiveType)
            self.messagePage.customizeContent(templateName, channel=messageType, previewAndTestCheck=True)
            self.messagePage.setPreviewAndTest(channel=messageType)
            self.messagePage.verifyAuthorizeCampaignPreviewAndTest(messageType, self.createCampaignPage.getCurrentCampaignPageURL().split('/')[-2])
        except Exception, exp:
            self.getScreenshot(request.node.name)
            Assertion.constructAssertion(False, 'Failure While Creating List with Exception :{}'.format(exp))

    def test_callTask_UI_channel_Sanity(self, request):
        self.createCampaignPage.navigateBackToCampaignsOverviewPage(dependencies={'list':['loyalty']})
        try:
            self.createCampaignPage.goToMessagePage('calltask')
            self.messagePage.chooseRecipient(constant.config['list']['loyalty']['name'])
            self.messagePage.attachIncentive('nodeal')
            self.messagePage.customizeContentOld()
            self.messagePage.deliverySetting()
            self.createCampaignPage.authorizePresentCampaignOnPage()
            self.messagePage.verifyAuthorizeCampaign(constant.config['campaign']['id'], constant.config['list']['loyalty']['id'])
        except Exception, exp:
            self.getScreenshot(request.node.name)
            Assertion.constructAssertion(False, 'Failure While Creating List with Exception :{}'.format(exp))
