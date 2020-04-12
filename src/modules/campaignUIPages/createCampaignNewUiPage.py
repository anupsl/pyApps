from src.seleniumBase.SeleniumDriver import SeleniumDriver
from src.modules.campaignUIPages.incentivePage import incentivePage
from src.modules.campaignUIPages.listPage import listPage
from src.modules.campaignUIPages.messagePage import messagePage
from src.modules.campaignUIPages.campaignsUIDBCalls import DBCallsCampaigns
from src.utilities.utils import Utils
from src.utilities.logger import Logger
from src.Constant.constant import constant
from src.utilities.assertion import Assertion
import time


class createCampaignPage(SeleniumDriver):

    def __init__(self, driver):
        SeleniumDriver.__init__(self, driver)
        self.driver = driver

    btn_generic_xpath = "//button/span[text()='{}']/.."
    inp_generic_xpath = "//input[@placeholder='{}']"
    btn_value_dict = {'createCampaign' : 'New campaign', 'done' : 'Done', 'saveCampaign' : 'Save campaign', 'createMsg' : 'New message', 'next' : 'Next', 'addAudience' : 'Add audience group', 'continue' : 'Continue', 'addAudienceGroup' : 'Add audience group',
                      'createAudienceGroup' : 'Create audience group', 'saveGroup' : 'Save Group', 'addCreatives' : 'Add creative', 'addIncentives' : 'Add incentives'}
    inp_value_dict = {'campaignName' : 'Enter Campaign name', 'messageName' : 'Enter Message name', 'startDate' : 'Start date'}
    inp_txt_xpath = "//input[@type='text']"
    inp_start_end_date_xpath = "//tr[@class='ant-calendar-current-week']/td/div[text()='{}']/.."
    href_modify_tc_xpath = "//a[@title='Modify']"
    chkbox_tc_ratio_xpath = "//span[contains(text(),'Override test / control ratio')]//../../..//input[@type='checkbox']"
    slider_tc_ratio_xpath = "//div[@class='ant-slider-handle ant-tooltip-open']"
    div_apply_filter_card_xpath = "//div[@type='h4'][text()='Apply filter condition']/../../.."


    def getDate(self):
        startDate = int(Utils.getTime(dateTimeFormat=True)[8:10])
        endDate = int(Utils.getTime(days=1, dateTimeFormat=True)[8:10])
        return startDate, endDate

    def createCampaign(self, campaignName):
        try:
            self.navigateToURL(constant.config['intouchUrl'] + '/campaigns/ui/list/')
            self.waitForElement(self.btn_generic_xpath.format(self.btn_value_dict['createCampaign']), locatorType='xpath')
            self.elementClick(self.btn_generic_xpath.format(self.btn_value_dict['createCampaign']), locatorType='xpath')
            time.sleep(5)
            self.sendKeys(campaignName, self.inp_generic_xpath.format(self.inp_value_dict['campaignName']), locatorType='xpath')
            self.elementClick(self.inp_generic_xpath.format(self.inp_value_dict['startDate']), locatorType='xpath')
            startDate, endDate = self.getDate()
            self.waitForElement(self.inp_start_end_date_xpath.format(startDate), locatorType='xpath')
            self.elementClick(self.inp_start_end_date_xpath.format(startDate), locatorType='xpath')
            time.sleep(5)
            # self.waitForElement(self.inp_start_end_date_xpath.format(endDate), locatorType='xpath')
            self.elementClick(self.inp_start_end_date_xpath.format(startDate), locatorType='xpath')
            time.sleep(10)
        except Exception, exp:
            Logger.log('Exception at {}'.format(exp))