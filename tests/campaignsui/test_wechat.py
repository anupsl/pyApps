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
from src.modules.veneno.venenoHelper import VenenoHelper
from src.utilities.dbhelper import dbHelper

@pytest.mark.run(order=3)
class Test_Wechat(object, SeleniumDriver):

    def setup_class(self):
        self.driver = WebDriverFactory().getWebDriverInstance()
        self.loginPage = loginPage(self.driver)
        self.createCampaignPage = campaignCreatePage(self.driver)
        self.incentivePage = incentivePage(self.driver)
        self.listPage = listPage(self.driver)
        self.messagePage = messagePage(self.driver)
        self.loginPage.login(userName=constant.config['intouchUsername'], password=constant.config['intouchPassword'])
        
        self.oldOrgId = construct.updateOrgId(constant.config['wechat']['orgId'])
        self.oldOrgName = construct.updateOrgName(constant.config['wechat']['orgName'])
        
        dbHelper.getIntouchShardNameForOrg()

        self.loginPage.switchOrgUsingCookies(constant.config['wechat']['orgId'])
        
    def teardown_class(self):
        try:
            self.driver.quit()
        except Exception, exp:
            assert False , 'Exception Occured while Closing Browser , Need to Close Browser manually'
        finally:
            Logger.log('Setting up orgId as :{} and orgName as :{} for later Executions'.format(self.oldOrgId,self.oldOrgName))
            construct.updateOrgId(self.oldOrgId)
            construct.updateOrgName(self.oldOrgName)
            
    def test_wechat_UI_channel_Sanity(self, request):
        try:
            details = VenenoHelper.preRequisitesForVenenoWechat()
            self.createCampaignPage.goToCampaignSection()
            self.createCampaignPage.openCampaignWithCampaignName(details['campaignName'])
            self.createCampaignPage.goToMessagePage('wechat')
            self.messagePage.chooseRecipient(details['groupName'])
            self.messagePage.attachIncentive('nodeal')
            self.messagePage.customizeContent(templateName='',channel='wechat')
            self.messagePage.deliverySetting()
            self.createCampaignPage.authorizePresentCampaignOnPage()
            self.messagePage.verifyAuthorizeCampaign(details['campaignId'], details['groupVersionResult']['TEST']['id'])
        except Exception,exp:
            self.getScreenshot(request.node.name)
            Assertion.constructAssertion(False, exp)