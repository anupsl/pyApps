import pytest, time, os, sys, pytest_ordering
from src.utilities.logger import Logger
from src.utilities.assertion import Assertion
from src.Constant.constant import constant
from src.modules.campaignUIPages.loginPage import loginPage
from src.modules.campaignUIPages.createCampaignNewUiPage import createCampaignPage
from src.modules.campaignUIPages.incentivePage import incentivePage
from src.modules.campaignUIPages.listPage import listPage
from src.modules.campaignUIPages.messagePage import messagePage
from src.seleniumBase.WebdriverFactory import WebDriverFactory
from src.seleniumBase.SeleniumDriver import SeleniumDriver


@pytest.mark.run(order=1)
class Test_CampaignsNewUI(object, SeleniumDriver):

    def setup_class(self):
        self.driver = WebDriverFactory().getWebDriverInstance()
        self.loginPage = loginPage(self.driver)
        self.createCampaignPage = createCampaignPage(self.driver)
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

    @pytest.mark.parametrize('description', ['Create Campaing'])
    def test_NUI_create_campaigns(self,description):
        self.createCampaignPage.createCampaign('Test campaign')
