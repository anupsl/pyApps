from src.seleniumBase.SeleniumDriver import SeleniumDriver
from src.modules.campaignUIPages.incentivePage import incentivePage
from src.modules.campaignUIPages.listPage import listPage
from src.modules.campaignUIPages.messagePage import messagePage
from src.modules.campaignUIPages.campaignsUIDBCalls import DBCallsCampaigns
from src.utilities.logger import Logger
from src.Constant.constant import constant
from src.utilities.assertion import Assertion
import time

class campaignCreatePage(SeleniumDriver):
    
    def __init__(self, driver):
        SeleniumDriver.__init__(self, driver)
        self.driver = driver
    inp_searchCampaign_id = "c-type-search"
    ref_campaignSelect_xpath = "//span[@title='{}']/a"
    sel_campaignType_id = "campaign_type"
    sel_timelineEndMinute_id = "timeline_end_minute"
    btn_orgSelectionDropDown_id = 'org_selection_dropdown'
    btn_creativespage_xpath = "//span[contains(text(),'Creatives')]"
    txt_orgSearchDivision_id = 'org-search-div'    
    btn_campaignSection_id = 'campaign'
    btn_newCampaign_id = 'new-campaign'
    txt_campaignName_id = 'campaign_name'
    txt_campaignDescription_id = 'campaign_desc'
    date_campaignStartDate_id = 'cnew_start_date'
    date_campaignEndDate_id = 'cnew_end_date'
    sel_objective_id = 'campaign_objective'
    btn_createCampaign_id = 'CreateNewCampaign'
    tbl_date_endDate_xpath = '//table[@class=\'ui-datepicker-calendar\']//a[1]'
    txt_campaignNameOnOverview_id = 'heading-campaign-name' 
    txt_verfiy_campaignNameOnOverview_id = 'in-heading-campaign-name' 
    ref_incentivePage_id = 'newCoupon'
    ref_listpage_id = 'newList'
    btn_createMessage_xpath = '//button[contains(text(),\'+ New Message\')]'
    btn_createMessageType_id = {
            'sms':'sms-container',
            'email':'email-container',
            'wechat':'wechat-account-container',
            'mobilepush':'mobilepush-title',
            'calltask':'calltask-container'
            }
    btn_createMessageType_wechat_xpath = "//div[contains(text(),'{accountName}')]"
    btn_authorize_xpath = '//button[contains(text(),\'Authorize\')]'
    iframe_authorize_approve_xpath = '//iframe[@id=\'popupiframe\']'
    btn_closeFrame_id = 'close'
    btn_frame_authorize_approve_id = 'msg_approve_btn'

    def goToCreativesPage(self):
        try:
            Logger.log('Going to Creatives Page')
            self.waitForElement(self.btn_creativespage_xpath, locatorType='xpath')
            if self.isElementPresent(self.btn_creativespage_xpath, locatorType='xpath'):
                self.elementClick(self.btn_creativespage_xpath, locatorType='xpath')
            else:
                assert False, 'creative_btn element not present'
        except Exception, exp:
            raise Exception('Unable To Go To Creatives Page due to Exception :{}'.format(exp))
    
    
    def goToCampaignSection(self):
        try:
            Logger.log('Going to Campaign Section')
            self.waitForElement(self.btn_campaignSection_id)
            if self.isElementPresent(self.btn_campaignSection_id):
                self.elementClick(self.btn_campaignSection_id)
            else:
                assert False, 'Campaign Section Locator is not Present'
        except Exception, exp:
            raise Exception('Go To Campaigns Section Exception :{}'.format(exp))
        
    def openCampaignWithCampaignName(self, campaignName):
        try:
            self.waitForElement(self.inp_searchCampaign_id)
            if self.isElementPresent(self.inp_searchCampaign_id):
                self.sendKeys(campaignName, self.inp_searchCampaign_id)
                self.waitForElement(self.ref_campaignSelect_xpath.format(campaignName), locatorType='xpath')
                if self.isElementPresent(self.ref_campaignSelect_xpath.format(campaignName), locatorType='xpath'):
                    self.elementClick(self.ref_campaignSelect_xpath.format(campaignName), locatorType='xpath')
                else:
                    assert False, 'Campaign Not Found with name :{}'.format(campaignName)
            else:
                assert False, 'Campaign Page not Loaded Properly'
        except Exception, exp:
            raise Exception('Not Able to open Campaign Exception :{}'.format(exp))
            
    def openNewCampaignCreationForm(self):
        try:
            Logger.log('Opening Create Campaign Form Fill Page ')
            self.waitForElement(self.btn_newCampaign_id)
            if self.isElementPresent(self.btn_newCampaign_id):
                self.elementClick(self.btn_newCampaign_id)
            else:
                assert False, 'Create Campaign Button Locator is not Present'
        except Exception, exp:
            raise Exception('Campaign Create Exception :{}'.format(exp))
    
    def createTimelineCampaign(self, campaignName, timelineEndTime="23:00"):
        try:
            Logger.log('Creating Timeline Campaign')
            self.waitForElement(self.sel_campaignType_id)
            if self.isElementPresent(self.sel_campaignType_id):
                self.selectWithOptionName(self.sel_campaignType_id, optionName='Timeline')
                self.sendKeys(campaignName, self.txt_campaignName_id)
                self.waitForElement(self.sel_timelineEndMinute_id)
                self.selectWithOptionName(self.sel_timelineEndMinute_id, optionName=timelineEndTime)
                self.clickOnSubmitButton()
                time.sleep(10)
            else:
                raise Exception('Campaign Type Selection box not present')
        except Exception, exp:
            raise Exception('CampaignCreateException :{}'.format(exp))
        
    def selectEndDateAsNextDay(self):
        try:
            self.elementClick(self.date_campaignEndDate_id)
            self.waitForElement(self.tbl_date_endDate_xpath, locatorType='xpath')
            if self.isElementPresent(self.tbl_date_endDate_xpath, locatorType='xpath'):
                self.elementClick(self.tbl_date_endDate_xpath, locatorType='xpath')
        except Exception, exp:
            raise Exception('Select End Date Exception :{}'.format(exp))
    
    def selectObjectiveId(self, optionName):
        try:
            self.selectWithOptionName(self.sel_objective_id, optionName=optionName)
        except Exception, exp:
            raise Exception('Select Objective Id Exception :{}'.format(exp))
    
    def goToOverviewpage(self):
        try: 
            Logger.log('Going To Overview Page using heading-campaign-name')
            self.waitForElement(self.txt_campaignNameOnOverview_id)
            if self.isElementPresent(self.txt_campaignNameOnOverview_id):
                self.elementClick(self.txt_campaignNameOnOverview_id)
            else:
                assert False, 'Overview Page Locator is not Present'
        except Exception, exp:
            raise Exception('Go To OverviewPage Exception :{}'.format(exp))
    
    def goToIncentivePage(self):
        try:
            Logger.log('Clicking on new Coupon Button To Move to Incentive page')
            self.waitForElement(self.ref_incentivePage_id)
            if self.isElementPresent(self.ref_incentivePage_id):
                self.elementClick(self.ref_incentivePage_id)
            else:
                assert False, 'Incentive Page Locator is not Present'
        except Exception, exp:
            raise Exception('Go To IncentivePage Exception :{}'.format(exp))
    
    def goToListPage(self):
        try:
            Logger.log('Clicking on New List Button on Overview Page')
            self.waitForElement(self.ref_listpage_id)
            if self.isElementPresent(self.ref_listpage_id):
                self.elementClick(self.ref_listpage_id)
                Logger.log('Refreshing the List Page To Avoid Frame Load Problems')
                self.refreshCurrentPage()
            else:
                assert False, 'List Page Locator is not Present'
        except Exception, exp:
            raise Exception('Go To listPage Exception :{}'.format(exp))
    
    def goToMessagePage(self, messageType):
        try:
            Logger.log('Selecting Message Type:', messageType.lower())
            self.waitForElement(self.btn_createMessage_xpath, locatorType='xpath')
            if self.isElementPresent(self.btn_createMessage_xpath, locatorType='xpath'):
                Logger.log('Clicking on Message Type Button')
                self.elementClick(self.btn_createMessage_xpath, locatorType='xpath')
                locatorMessageType = self.btn_createMessageType_id[messageType.lower()]
                Logger.log('For Message Type :{} ,locator Identified :{}'.format(messageType, locatorMessageType))
                try:
                    self.waitForElement(locatorMessageType)
                    if self.isElementPresent(locatorMessageType):
                        Logger.log('Clicking on Locator For Message Type')
                        self.elementClick(locatorMessageType)
                        if messageType in ['wechat', 'mobilepush']:
                            for _ in range(10):
                                if self.isElementPresent(self.btn_createMessageType_wechat_xpath.replace('{accountName}', constant.config[messageType.lower()]['account']), locatorType='xpath'):
                                    break
                                else:
                                    time.sleep(10)
                                    self.elementClick(locatorMessageType)
                                    self.elementClick(locatorMessageType)
                            self.elementClick(self.btn_createMessageType_wechat_xpath.replace('{accountName}', constant.config[messageType.lower()]['account']), locatorType='xpath')
                    else:
                        assert False, 'Message Type :{} locator Not Visibe'.format(messageType)
                except Exception, exp:
                    raise Exception('Message Type Not Found Exception :{}'.format(exp))
            else:
                assert False, 'Create New message Button is not Present'
        except Exception, exp:
            raise Exception('Go To Message Page Exception :{}'.format(exp))
                
    
    def fillDetailsAndCreateCampaign(self, campaignName, campaignDescription, objective):
        try:
            Logger.log('Filling Details To Create Campaign with name :{} , description :{} and objective :{}'.format(campaignName, campaignDescription, objective))
            self.waitForElement(self.date_campaignEndDate_id)
            self.waitForElement(self.sel_objective_id)
            if self.isElementPresent(self.sel_objective_id) and self.isElementPresent(self.date_campaignEndDate_id):
                self.sendKeys(campaignName, self.txt_campaignName_id)
                self.sendKeys(campaignDescription, self.txt_campaignDescription_id)
                self.selectEndDateAsNextDay()
                self.selectObjectiveId(optionName=objective)
            else:
                assert False, 'Create Campaign Form Locators are not Present'
        except Exception, exp:
            raise Exception('Fill Campaign Create Form Exception :{}'.format(exp))
            
    def clickOnSubmitButton(self):
        try:
            time.sleep(3)
            self.scrollWebPage()
            self.waitForElement(self.btn_createCampaign_id)
            if self.isElementPresent(self.btn_createCampaign_id):
                self.elementClick(self.btn_createCampaign_id)
            else:
                assert False, 'Submit Button Locator is not Present'
        except Exception, exp:
            raise Exception('Saving Campaign Exception :{}'.format(exp))
      
    def createCampaignAndVerify(self, campaignName, campaignDescription='Automation Generated', objectiveType='General'):
        try:
            self.switchOrgUsingCookies()
            self.goToCampaignSection()
            self.openNewCampaignCreationForm()
            self.fillDetailsAndCreateCampaign(campaignName, campaignDescription, objectiveType)
            self.clickOnSubmitButton()
            self.verifyCampaignCreation(campaignName)
            self.setCampaignOverviewURL()
        except Exception, exp:
            raise Exception('Create Campaign Exception :{}'.format(exp))
            
    def verifyCampaignCreation(self, campaignName):
        Logger.log('Verifying Campaign Creation with Campaign Name Text On Overview Page')
        self.waitForElement(self.txt_verfiy_campaignNameOnOverview_id)
        if campaignName[:10] in self.getElement(self.txt_verfiy_campaignNameOnOverview_id).text:
            campaignId = DBCallsCampaigns.getCampaignIdFromCampaignName(campaignName)
            constant.config['campaign'].update({'name':campaignName, 'id':campaignId})
            Logger.log('Campaign Info Set as :', constant.config['campaign'])
            return True
        else:
            Assertion.constructAssertion(False, 'Campaign Name Not Displayed on Overview Page')
        
    def setCampaignOverviewURL(self):
        try:
            Logger.log('Setting Campaign Overview URL')
            self.campaignOverviewPage = None
            for eachTry in range(10):
                currentpageURL = self.getCurrentURL()
                if 'dashboard' not in currentpageURL:
                    self.campaignOverviewPage = currentpageURL 
                    break
            Logger.log('Overview URL For this Session :', currentpageURL)  
        except Exception, exp:
            raise Exception('Set Campaign Overview URL Exception :{}'.format(exp))  
    
    def getCurrentCampaignPageURL(self):
        return self.campaignOverviewPage

    def navigateBackToCampaignsOverviewPage(self, dependencies={}):
        try:
            if self.campaignOverviewPage is not None:
                Logger.log('Navigating Back to Campaign Overview Page with URL :', self.campaignOverviewPage)
                self.navigateToURL(self.campaignOverviewPage)
                Logger.log('Checking for any Alert on Page and accept if any')
                self.acceptAlert()
                Logger.log('Waiting for heading-campaign-name on Overview Page to be Visible and wait for some seconds to Move on ')
                self.waitForElement(self.txt_campaignNameOnOverview_id)
                time.sleep(2)
                return True
            else:
                Logger.log('No URL set for Overview Page ')
                return False
        except AttributeError, err:
            Logger.log('Creating New Campaign and resolving Dependencies :{} for this Case'.format(dependencies))
            self.createCampaignAndVerify(campaignName='campaignUI_SingleCase_' + str(int(time.time())))
            if len(dependencies) > 0:self.resolveDependenciesForRerun(dependencies)
            self.navigateBackToCampaignsOverviewPage()
    
    def resolveDependenciesForRerun(self, dependencies={}):  
        if 'coupon' in dependencies:
            Logger.log('Resolving Coupon Dependency')
            self.goToIncentivePage()
            incentivePage(self.driver).createNewCoupon('coupon_SingleCase_' + str(int(time.time())))
            self.goToOverviewpage()
        if 'list' in dependencies:
            Logger.log('Resolving List Dependency')
            lists = listPage(self.driver, newFilterEnabled=True)
            for eachList in dependencies['list']:
                self.goToListPage()
                lists.selectFilterType(eachList)
                lists.switchToListFrame(eachList)
                lists.saveListAsPerFilterType(filterType=eachList, listName=constant.config['list'][eachList]['name'])
                lists.switchToDefaultFromListPage()
                groupVersionId = lists.verifyListCreated(constant.config['campaign']['id'], constant.config['list'][eachList]['name'])
                constant.config['list'][eachList]['id'] = groupVersionId
                self.goToOverviewpage()
    
    def authorizePresentCampaignOnPage(self):
        try:
            Logger.log('Authorizing Present Campaign On Page')
            self.scrollWebPage()
            self.waitForElement(self.btn_authorize_xpath, locatorType='xpath')
            if self.isElementPresent(self.btn_authorize_xpath, locatorType='xpath'):
                self.elementClick(self.btn_authorize_xpath, locatorType='xpath')
                self.switchToAuthorizeFrame()
                self.waitForElement(self.btn_frame_authorize_approve_id)
                if self.isElementPresent(self.btn_frame_authorize_approve_id):
                    self.elementClick(self.btn_frame_authorize_approve_id)
                else:
                    assert False, 'Approve Button Not Found in Iframe'
            else:
                assert False, 'Authorize Button Not Found on page'
        except Exception, exp:
            raise Exception('Authorize Exception :{}'.format(exp))
        finally:
            Logger.log('Finally Switching To Default')
            self.switchToDefaul()
      
    def switchToAuthorizeFrame(self):
        self.waitForElement(self.iframe_authorize_approve_xpath, locatorType='xpath')
        try:
            if self.isElementPresent(self.iframe_authorize_approve_xpath, locatorType='xpath'):
                self.switchToFrame(self.iframe_authorize_approve_xpath, locatorType='xpath')
            else:
                assert False, 'Frame Locator is not Present'
        except Exception as exp:
            self.closeFrameIfAuthorizeFailed()
            raise Exception('List Frame Not Loaded with Exception :' + str(exp))

    def closeFrameIfAuthorizeFailed(self):
        try:
            Logger.log('Closing Frame as Authorization of Campaign Failed')
            self.switchToDefaul()
            self.waitForElement(self.btn_closeFrame_id)
            if self.isElementPresent(self.btn_closeFrame_id):
                    self.elementClick(self.btn_closeFrame_id)
            else:
                assert False, 'Close Frame Locator is not Present'
        except Exception, exp:
            raise Exception('Unable To Close Frame with Close Button due to Exception :{}'.format(exp))
