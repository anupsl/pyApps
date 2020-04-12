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

@pytest.mark.run(order=2)
@pytest.mark.skipif(constant.config['cluster'] not in ['nightly'], reason='Wechat Configured only in nightly')
class Test_MobilePush_UI(object, SeleniumDriver):
    
    def setup_class(self):
        self.driver = WebDriverFactory().getWebDriverInstance()
        self.loginPage = loginPage(self.driver)
        self.createCampaignPage = campaignCreatePage(self.driver)
        self.incentivePage = incentivePage(self.driver)
        self.listPage = listPage(self.driver)
        self.messagePage = messagePage(self.driver)
        self.loginPage.login(userName=constant.config['intouchUsername'], password=constant.config['intouchPassword'])
        
        self.oldOrgId = construct.updateOrgId(constant.config['mobilepush']['orgId'])
        self.oldOrgName = construct.updateOrgName(constant.config['mobilepush']['orgName'])
        self.loginPage.switchOrgUsingCookies(constant.config['mobilepush']['orgId'])
        
    def teardown_class(self):
        try:
            self.driver.quit()
        except Exception, exp:
            assert False , 'Exception Occured while Closing Browser , Need to Close Browser manually'
        finally:
            Logger.log('Setting up orgId as :{} and orgName as :{} for later Executions'.format(self.oldOrgId,self.oldOrgName))
            construct.updateOrgId(self.oldOrgId)
            construct.updateOrgName(self.oldOrgName)
            
    
    @pytest.mark.parametrize('accountType', [
        ('android'),
        ('ios')
        ]) 
    def test_mobilePush_UI_channel_Sanity(self,request,accountType):
        try:
            details = VenenoHelper.preRequisitesForVenenoMobilePush(accountType)
            self.createCampaignPage.goToCampaignSection()
            self.createCampaignPage.openCampaignWithCampaignName(details['campaignName'])
            self.createCampaignPage.goToMessagePage('mobilepush')
            self.messagePage.chooseRecipient(details['groupName'])
            self.messagePage.attachIncentive('nodeal')
            self.messagePage.customizeContent(constant.config['templateName']['mobilepush'][accountType])
            self.messagePage.deliverySetting()
            self.createCampaignPage.authorizePresentCampaignOnPage()
            self.messagePage.verifyAuthorizeCampaign(details['campaignId'], details['groupVersionResult']['TEST']['id'])
        except Exception,exp:
            self.getScreenshot(request.node.name)
            Assertion.constructAssertion(False, exp)

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        