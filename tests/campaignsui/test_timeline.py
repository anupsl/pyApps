import pytest, time, os, sys, pytest_ordering

from src.Constant.constant import constant
from src.initializer.baseState import BaseState
from src.modules.campaignUIPages.campaignCreatePage import campaignCreatePage
from src.modules.campaignUIPages.incentivePage import incentivePage
from src.modules.campaignUIPages.loginPage import loginPage
from src.modules.campaignUIPages.timelineDBCalls import TimelineDBAssertion
from src.modules.campaignUIPages.timelinePages import timelinePages
from src.seleniumBase.SeleniumDriver import SeleniumDriver
from src.seleniumBase.WebdriverFactory import WebDriverFactory
from src.seleniumBase.browserLogs import browserLogs
from src.utilities.assertion import Assertion
from src.utilities.logger import Logger

@pytest.mark.run(order=4)
class Test_Timeline(object, SeleniumDriver):
    
    def setup_class(self):
        BaseState.moduleFlip('timeline')
        constant.config['timeline_templateName'] = constant.timelineDetails[constant.config['cluster']]
        self.driver = WebDriverFactory().getWebDriverInstance()
        self.createCampaignPage = campaignCreatePage(self.driver)
        self.incentivePage = incentivePage(self.driver)
        self.timelinePages = timelinePages(self.driver)
        self.loginPage = loginPage(self.driver)  
        constant.config['segment'] = self.timelinePages.setupListForTimelineExection()
    
    def setup_method(self):
        self.timelinePages.consumerCheckInRabitMQCheck()  
        self.loginPage.login(userName=constant.config['intouchUsername'], password=constant.config['intouchPassword'])
        self.loginPage.switchOrgUsingCookies()
        self.createCampaignPage.goToCampaignSection()
        self.createCampaignPage.openNewCampaignCreationForm()
        
    def teardown_class(self):
        if constant.config['moduleFlip']:
            BaseState.moduleFlip(-1)
            
    def teardown_method(self):
        self.driver.quit()
    
    def test_timeline_Sanity(self, request):
        self.campaignName = 'TimelineSanity' + str(int(time.time()))
        try:
            self.createCampaignPage.createTimelineCampaign(self.campaignName, timelineEndTime=constant.timelineDetails[constant.config['cluster']]['timelineEndTime'])
            self.timelinePages.createNewTimeline()
            self.timelinePages.fillTimelineDetails()
            self.timelinePages.selectSegment(constant.config['segment'])
            self.timelinePages.selectStartDateForCustomers()
            self.timelinePages.configureMilestione()
            self.timelinePages.selectIncentive()
            self.timelinePages.customizeContent(constant.config['timeline_templateName']['templateName'])
            self.timelinePages.saveMileston()
            self.timelinePages.saveAndExitTimeline()
            self.timelinePages.setCompressionFactor()
            self.timelinePages.rollOutCampaign()
            TimelineDBAssertion(self.campaignName).check()
        except Exception, exp:
            self.getScreenshot(request.node.name)
            Assertion.constructAssertion(False, exp)
            
    def test_timeline_Point(self, request):
        self.campaignName = 'TimelineSanityPoint' + str(int(time.time()))
        try:
            self.createCampaignPage.createTimelineCampaign(self.campaignName, timelineEndTime=constant.timelineDetails[constant.config['cluster']]['timelineEndTime'])
            self.timelinePages.createNewTimeline()
            self.timelinePages.fillTimelineDetails()
            self.timelinePages.selectSegment(constant.config['segment'])
            self.timelinePages.selectStartDateForCustomers()
            self.timelinePages.configureMilestione()
            self.timelinePages.selectIncentive(enablePoint=True)
            self.timelinePages.customizeContent(constant.config['timeline_templateName']['templateNamePoints'])
            self.timelinePages.saveMileston()
            self.timelinePages.saveAndExitTimeline()
            self.timelinePages.setCompressionFactor()
            self.timelinePages.rollOutCampaign()
            TimelineDBAssertion(self.campaignName).check()
        except Exception, exp:
            self.getScreenshot(request.node.name)
            Assertion.constructAssertion(False, exp)

    def test_timeline_Coupon(self, request):
        self.campaignName = 'TimelineSanityPoint' + str(int(time.time()))
        try:
            self.createCampaignPage.createTimelineCampaign(self.campaignName, timelineEndTime=constant.timelineDetails[constant.config['cluster']]['timelineEndTime'])
            self.createCampaignPage.goToIncentivePage()
            self.incentivePage.createNewCoupon(couponName='coupon_' + str(int(time.time())))
            self.createCampaignPage.goToOverviewpage()
            self.timelinePages.createNewTimeline()
            self.timelinePages.fillTimelineDetails()
            self.timelinePages.selectSegment(constant.config['segment'])
            self.timelinePages.selectStartDateForCustomers()
            self.timelinePages.configureMilestione()
            self.timelinePages.selectIncentive(enableCoupon=True)
            self.timelinePages.customizeContent(constant.config['timeline_templateName']['templateNameCoupon'])
            self.timelinePages.saveMileston()
            self.timelinePages.saveAndExitTimeline()
            self.timelinePages.setCompressionFactor()
            self.timelinePages.rollOutCampaign()
            TimelineDBAssertion(self.campaignName).check()
        except Exception, exp:
            self.getScreenshot(request.node.name)
            Assertion.constructAssertion(False, exp)
