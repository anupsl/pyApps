import pytest, time, os, sys, pytest_ordering
from src.utilities.logger import Logger
from src.utilities.assertion import Assertion
from src.Constant.constant import constant
from src.modules.iris.construct import construct
from src.modules.campaignUIPages.loginPage import loginPage
from src.modules.campaignUIPages.campaignCreatePage import campaignCreatePage
from src.modules.campaignUIPages.creativesPage import creativePage
from src.seleniumBase.WebdriverFactory import WebDriverFactory
from src.seleniumBase.browserLogs import browserLogs
from src.seleniumBase.SeleniumDriver import SeleniumDriver

@pytest.mark.run(order=5)
class Test_Creatives(object, SeleniumDriver):
    
    def setup_class(self):
        self.driver = WebDriverFactory().getWebDriverInstance()
        self.loginPage = loginPage(self.driver)
        self.creativePage = creativePage(self.driver)
        self.createCampaignPage = campaignCreatePage(self.driver)
        self.loginPage.login(userName=constant.config['intouchUsername'], password=constant.config['intouchPassword'])
        self.loginPage.switchOrgUsingCookies()
        self.createCampaignPage.goToCampaignSection()
        self.createCampaignPage.goToCreativesPage()
        self.creativePage.skipGuide()
        self.creativeBaseURL = self.creativePage.captureCurrentURL()
        
    def teardown_class(self):
        self.driver.quit()
        
    @pytest.mark.parametrize('channel,templateName,tags', [
        ('sms', 'generic', ['First Name', 'Last Name', 'Full Name', 'Mobile Number', 'Optout']),
        ])
    def test_sms_creative(self, request, channel, templateName, tags):
        if self.creativeBaseURL != '' :self.creativePage.setCreativePageURL(self.creativeBaseURL)
        templateName = templateName + str(int(time.time() * 1000))
        try:
            self.creativePage.selectChannelToCreateTemplate()
            self.creativePage.waitForChannelmainContentToLoad()
            self.creativePage.createTemplate()
            templateName = self.creativePage.templateName(templateName, channel)
            self.creativePage.templateFillSMS()
            self.creativePage.selectTags(tags)
            self.creativePage.saveTemplate()
            self.creativePage.searchAndVerifyCreatedTemplate(templateName)
            self.creativePage.validateDBForTemplate(channel, templateName)
        except Exception, exp:
            self.getScreenshot(request.node.name)
            Assertion.constructAssertion(False, exp)
            
    @pytest.mark.parametrize('channel,templateName,tags', [
        ('email', 'generic', ['First Name', 'Last Name', 'Full Name', 'Unsubscribe']),
        ])
    def test_email_editor_creative(self, request, channel, templateName, tags):
        if self.creativeBaseURL != '' :self.creativePage.setCreativePageURL(self.creativeBaseURL)
        templateName = templateName + str(int(time.time() * 1000))
        try:
            self.creativePage.selectChannelToCreateTemplate(channel)
            self.creativePage.waitForChannelmainContentToLoad(channel)
            self.creativePage.createTemplate(channel)
            templateName = self.creativePage.templateName(templateName, channel)
            self.creativePage.templateFillEMAIL()
            self.creativePage.selectTags(tags, channel=channel)
            self.creativePage.saveTemplate()
            self.creativePage.searchAndVerifyCreatedTemplate(templateName)
            self.creativePage.validateDBForTemplate(channel, templateName)
        except Exception, exp:
            self.getScreenshot(request.node.name)
            Assertion.constructAssertion(False, exp)
               
    @pytest.mark.parametrize('channel,templateName', [
        ('email', 'generic'),
        ])
    def test_email_upload_creative(self, request, channel, templateName):
        if self.creativeBaseURL != '' :self.creativePage.setCreativePageURL(self.creativeBaseURL)
        templateName = templateName + str(int(time.time() * 1000))
        try:
            self.creativePage.selectChannelToCreateTemplate(channel)
            self.creativePage.waitForChannelmainContentToLoad(channel)
            self.creativePage.createTemplate(channel, TemplateType='Upload File')
            templateName = self.creativePage.templateName(templateName, channel)
            self.creativePage.saveTemplate()
            self.creativePage.searchAndVerifyCreatedTemplate(templateName)
            self.creativePage.validateDBForTemplate(channel, templateName)
        except Exception, exp:
            self.getScreenshot(request.node.name)
            Assertion.constructAssertion(False, exp)
    
    @pytest.mark.skipif(constant.config['cluster'] not in ['nightly', 'china', 'staging'], reason='Wechat Configured only in nightly,staging,china')
    @pytest.mark.parametrize('channel,tags', [
        ('wechat', ['First Name']),
        ])
    def est_wechat_creative(self, request, channel, tags):
        if self.creativeBaseURL != '' :self.creativePage.setCreativePageURL(self.creativeBaseURL)
        try:
            self.loginPage.switchOrgUsingCookies(constant.config['wechat']['orgId'])
            self.creativePage.selectChannelToCreateTemplate(channel)
            self.creativePage.waitForChannelmainContentToLoad(channel)
            self.creativePage.selectAccount(channel, constant.config['wechat']['account'])
            self.creativePage.unMapWeChatTemplate()
            self.creativePage.createTemplate()
            templateName = self.creativePage.templateFillWechat(tags=tags)
            self.creativePage.saveTemplate()
            self.creativePage.searchAndVerifyCreatedTemplate(templateName, channel=channel)
            self.creativePage.validateDBForTemplate(channel, templateName.split(':')[-1].strip())
        except Exception, exp:
            self.getScreenshot(request.node.name)
            Assertion.constructAssertion(False, exp)

    @pytest.mark.skipif(constant.config['cluster'] not in ['nightly', 'staging', 'india', 'more', 'eu'], reason='mobile push not Configured only in china')
    @pytest.mark.parametrize('channel,templateType,pushType,pushType2,title,message,templateName,tags', [
        ('Mobile Push', 'Text', 'Android', 'iOS', 'Auto Created', 'Hi push' , 'push_text_android_', ['First Name']),
        ])
    def est_mobilePush_creative(self, request, channel, templateType, pushType, pushType2, title , message, templateName, tags):
        if self.creativeBaseURL != '' :self.creativePage.setCreativePageURL(self.creativeBaseURL)
        templateName = templateName + str(int(time.time() * 1000))
        try:
            self.loginPage.switchOrgUsingCookies(constant.config['mobilepush']['orgId'])
            self.creativePage.selectChannelToCreateTemplate(channel)
            self.creativePage.waitForChannelmainContentToLoad(channel)
            self.creativePage.selectAccount(channel, constant.config['mobilepush']['account'])
            self.creativePage.createTemplate(channel=channel, TemplateType=templateType)
            self.creativePage.templateName(templateName)
            self.creativePage.templateFillPush(pushType, title, message, tags=tags)
            self.creativePage.templateFillPush(pushType2, title, message, tags=tags)
            self.creativePage.saveTemplate()
            self.creativePage.searchAndVerifyCreatedTemplate(templateName, channel=channel)
            self.creativePage.validateDBForTemplate(channel, templateName)
        except Exception, exp:
            self.getScreenshot(request.node.name)
            Assertion.constructAssertion(False, exp)
    
