from src.modules.temporalEngine.temporalObject import TemporalObject
from src.modules.temporalEngine.temporalThrift import TemporalThrift
from src.modules.temporalEngine.temporalHelper import TemporalHelper
from src.modules.campaign_shard.campaignShardHelper import CampaignShardHelper
from src.modules.iris.campaigns import campaigns
from src.seleniumBase.SeleniumDriver import SeleniumDriver
from src.utilities.logger import Logger
from src.Constant.constant import constant
from src.utilities.utils import Utils
import time

class timelinePages(SeleniumDriver):
    
    div_newTimeline_id = "new-timeline"
    inp_nameTimeline_id = "tl-name"
    inp_lengthTimeline_id = "tl-length"
    div_fillDetailsNext_id = "timeline_nav_1"
    inp_searchSegment_id = "search_list"
    i_listSelect_xpath = "//ul[@id='segment_list_radio']//i"
    div_selectSegmentNext_id = "timeline_nav_2"
    sel_startDate_id = "tl-date"
    div_startDateNext_id = "timeline_nav_3"
    div_waitconfigureMilestone_xpath = "//div[@class='c-timeline-click-area']"
    div_selectMilestioneDay_xpath = "//*[@data-value='{day}']"
    a_nextMilestoneday_xpath = "//*[@data-value='{day}']/..//a[contains(text(),'Next')]"
    a_saveMilestoneSave_xapth = "//*[@data-value='{day}']/..//a[contains(text(),'Save')]"
    inp_checkboxCheckAll_xpath = "//*[@data-value='{day}']/..//input[contains(@type,'checkbox')]"
    li_configureMilestoneChannelSelect_xpath = "//*[@data-value='{day}']/..//div[contains(text(),'is True')]/..//li[@class='{channel}']"
    h2_couponContainer_xpath = "//h2[@id='container-coupons']/span"
    i_couponContainer_xpath = "//h2[@id='container-coupons']/..//i[@class='intouch-green-tick']"
    h2_pointContainer_xpath = "//h2[@id='container-points']/span"
    i_allocationStrategy_xpath = "//h2[@id='container-points']/..//i[@class='choose-empty-alloc']"
    i_expiryStrategy_xpath = "//h2[@id='container-points']/..//i[@class='choose-empty-expiry']"
    i_noContainer_xpath = "//i[starts-with(@class,'no-incentive-select')]"
    a_selectIncentiveNext_id = "next-button-action"
    templateFrame_id = "creatives-timeline-iframe"
    inp_customizeContent_search_xpath = "//input[@placeholder='Search']"
    templatevisible_xpath = "//div[@class='footer-wrapper']//span[contains(text(),'{templateName}')]"
    templatebody_xpath = "//div[@class='footer-wrapper']//span[contains(text(),'{templateName}')]/../../../.."
    selectTemplate_xpath = "//div[@class='footer-wrapper']//span[contains(text(),'{templateName}')]/../../../..//span[contains(text(),'Select')]"
    selectTemplateNext_id = "select_template"
    selectTemplateSaveAction_id = "save-action"
    saveAndExitMileston_id = "save-milestones"
    saveAndExitConformation_id = "first-direct-cancel-timelines-btn"
    rollOut_id = "init_timelines"
    rollOutConformation_id = "direct-rollout-timelines-btn"
    
    def __init__(self, driver):
        SeleniumDriver.__init__(self, driver)
        self.driver = driver
        
    def consumerCheckInRabitMQCheck(self):
        listOfQueue = ['TIMELINE_MSG_QUEUE', 'TIMELINE_SKIPPED_MSG_QUEUE']
        try:
            for eachQueue in listOfQueue:
                queueDetails = Utils.getRabbitmqQueueDetails(eachQueue, host='veneno-host')
                Logger.log('Queue :{} have {} consumers'.format(eachQueue, queueDetails['consumers']))
                if queueDetails == {} and queueDetails['consumers'] == 0:
                    raise Exception('Queue :{} is dead , please restart service to start automation ')
        except Exception, exp:
            raise Exception('RABITMQException :{}'.format(exp))
        
    def createNewTimeline(self):
        try:
            self.waitForElement(self.div_newTimeline_id)
            if self.isElementPresent(self.div_newTimeline_id):
                self.elementClick(self.div_newTimeline_id)
            else:
                raise Exception('New Timeline Button Not Present')
        except Exception, exp:
            raise Exception('CreateNewTimelineException :{}'.format(exp))
            
    def fillTimelineDetails(self, nameOfTimeline='T1', lengthOfTimeline=10):
        try:
            self.waitForElement(self.inp_nameTimeline_id)
            if self.isElementPresent(self.inp_nameTimeline_id):
                self.sendKeys(nameOfTimeline, self.inp_nameTimeline_id)
                self.sendKeys(lengthOfTimeline, self.inp_lengthTimeline_id)
                self.elementClick(self.div_fillDetailsNext_id)
                self.setConfigIdForTheExecution()
            else:
                raise Exception('Some Fields Not Present on Fill Timeline Details Page')
        except Exception, exp:
            raise Exception('FillTimelineDetailsException :{}'.format(exp))
    
    def setConfigIdForTheExecution(self):
        currentUrlForTimeline = self.getCurrentURL()
        constant.config['orgConfigId'] = int(currentUrlForTimeline.split('=')[-1])
        Logger.log('Org_ConfigId for timeline is set as :{}'.format(constant.config['orgConfigId']))
        
    def selectSegment(self, segmentName):
        try:
            self.waitForElement(self.inp_searchSegment_id)
            if self.isElementPresent(self.inp_searchSegment_id):
                self.sendKeys(segmentName, self.inp_searchSegment_id)
                self.waitForElement(self.i_listSelect_xpath, locatorType='xpath')
                self.elementClick(self.i_listSelect_xpath, locatorType='xpath')
                self.elementClick(self.div_selectSegmentNext_id)
            else:
                raise Exception('Search Segment Input Field Not Present')
        except Exception, exp:
            raise Exception('SegmentSelectionException :{}'.format(exp))
        
    def selectStartDateForCustomers(self, startType=' Campaign initiation time'):
        try:
            self.waitForElement(self.sel_startDate_id)
            if self.isElementPresent(self.sel_startDate_id):
                self.selectWithOptionName(self.sel_startDate_id, optionName=startType)
                self.elementClick(self.div_startDateNext_id)
        except Exception, exp:
            raise Exception('SelectStartDateTypeException :{}'.format(exp))
        
    def configureMilestione(self, day='1', channel='sms'):
        try:
            self.waitForElement(self.div_selectMilestioneDay_xpath.replace('{day}', day), locatorType='xpath')
            if self.isElementPresent(self.div_selectMilestioneDay_xpath.replace('{day}', day), locatorType='xpath'):
                self.elementClickWithAction(self.div_selectMilestioneDay_xpath.replace('{day}', day), locatorType='xpath')
                self.elementClick(self.a_nextMilestoneday_xpath.replace('{day}', day), locatorType='xpath')
                self.elementClick(self.inp_checkboxCheckAll_xpath.replace('{day}', day), locatorType='xpath')
                self.elementClick(self.li_configureMilestoneChannelSelect_xpath.replace('{day}', day).replace('{channel}', channel), locatorType='xpath')
            else:
                raise Exception('Milestion Not Getting Displayed')
        except Exception, exp:
            raise Exception('ConfigureMilestoneException :{}'.format(exp))
    
    def selectIncentive(self, enableCoupon=False, enablePoint=False):
        try:
            self.waitForElement(self.i_noContainer_xpath, locatorType='xpath')
            if self.isElementPresent(self.i_noContainer_xpath, locatorType='xpath'):
                if enableCoupon:
                    self.elementClick(self.h2_couponContainer_xpath, locatorType='xpath')
                if enablePoint:
                    self.elementClick(self.h2_pointContainer_xpath, locatorType='xpath')
                    if self.isElementPresent(self.i_allocationStrategy_xpath, locatorType='xpath') and self.isElementPresent(self.i_expiryStrategy_xpath, locatorType='xpath'):
                        allocationStrategy = self.getElements(self.i_allocationStrategy_xpath, locatorType='xpath')
                        expiryStrategy = self.getElements(self.i_expiryStrategy_xpath, locatorType='xpath')
                        allocationStrategy[0].click()
                        expiryStrategy[0].click()
                    else:
                        Logger.log('Point Strategy Not Configured Properly , so Selecting No Incentives')
                        self.configureTemplate(False, False)
                else:
                    self.elementClick(self.i_noContainer_xpath, locatorType='xpath')
                self.elementClick(self.a_selectIncentiveNext_id)
            else:
                raise Exception('Incentive Checkbox /Container Missing on Page')
        except Exception, exp:
            raise Exception('ConfigureTemplateException :{}'.format(exp))
    
    def customizeContent(self, templateName):
        try:
            self.switchToFrame(self.templateFrame_id)
            self.waitForElement(self.inp_customizeContent_search_xpath, locatorType='xpath')
            if self.isElementPresent(self.inp_customizeContent_search_xpath, locatorType='xpath'):
                self.sendKeys(templateName, self.inp_customizeContent_search_xpath, locatorType='xpath')
                self.waitForElement(self.templatevisible_xpath.replace('{templateName}', templateName), locatorType='xpath')
                if self.isElementPresent(self.templatevisible_xpath.replace('{templateName}', templateName), locatorType='xpath'):
                    time.sleep(10)
                    templateBody = self.getElement(self.templatebody_xpath.replace('{templateName}', templateName), locatorType='xpath')
                    self.moveToElement(templateBody)
                    selectButton = self.getElement(self.selectTemplate_xpath.replace('{templateName}', templateName), locatorType='xpath')
                    self.moveToElement(selectButton)
                    self.elementClickWithAction(self.selectTemplate_xpath.replace('{templateName}', templateName), locatorType='xpath')
                else:
                    raise Exception('NoSuchTemplateException :{}'.format(templateName))
        except Exception, exp:
            raise Exception('CustomizeContentException :{}'.format(exp))
        finally:
            self.switchToDefaul()
            time.sleep(10)
            self.saveTemplate()
            
    def saveTemplate(self):
        try:
            self.waitForElement(self.selectTemplateNext_id)
            for retry in range(10):
                if self.isElementPresent(self.selectTemplateNext_id):
                    time.sleep(5)
                    self.elementClick(self.selectTemplateNext_id)
                else:
                    if retry > 2 : break
        except Exception, exp:
            Logger.log('Exception :{} while Save Template'.format(exp))
        finally:
            self.waitForElement(self.selectTemplateSaveAction_id)
            self.elementClick(self.selectTemplateSaveAction_id)

    def saveMileston(self, day='1'):
        try:
            self.waitForElement(self.a_saveMilestoneSave_xapth.replace('{day}', day), locatorType='xpath')
            if self.isElementPresent(self.a_saveMilestoneSave_xapth.replace('{day}', day), locatorType='xpath'):  
                self.elementClick(self.a_saveMilestoneSave_xapth.replace('{day}', day), locatorType='xpath')
            else:
                raise Exception('Save Milestone Button Not Present')
        except Exception, exp:
            raise Exception('SaveMilestoneException :{}'.format(exp))
        
    def saveAndExitTimeline(self):
        try:
            self.waitForElement(self.saveAndExitMileston_id)
            if self.isElementPresent(self.saveAndExitMileston_id):
                self.elementClick(self.saveAndExitMileston_id)
                self.waitForElement(self.saveAndExitConformation_id)
                self.elementClick(self.saveAndExitConformation_id)
            else:
                raise Exception('SaveAndExitTimeline Button Not Present')
        except Exception, exp:
            raise Exception('SaveAndExitException :{}'.format(exp))
    
    def rollOutCampaign(self):
        try:
            self.waitForElement(self.rollOut_id)
            if self.isElementPresent(self.rollOut_id):
                self.elementClick(self.rollOut_id)
                self.waitForElement(self.rollOutConformation_id)
                self.elementClick(self.rollOutConformation_id)
            else:
                raise Exception('Roll Out button not present')
        except Exception, exp:
            raise Exception('RollOutException :{}'.format(exp))
    
    def setCompressionFactor(self, compressionFactor=0.001):
        try:
            Logger.log('Setting Compession Factor as : {}'.format(compressionFactor))
            connObj = TemporalHelper.getConnObj()
            sessionId = TemporalObject.SessionId()
            curLifecycle = connObj.getLifecycleById(sessionId)
            currentProperties = curLifecycle.properties
            currentProperties.update({3 : str(compressionFactor)})
            newLifecycle = TemporalObject.Lifecycle(curLifecycle, extraField={'properties':currentProperties})
            connObj.saveLifecycle(newLifecycle, sessionId)
        except Exception, exp:
            raise Exception('CompressionFactorException :{}'.format(exp))
        
    def setupListForTimelineExection(self):
        try:
            campaignResponse_ORG, campaignPayload_ORG = campaigns.createCampaign({'name':'IRIS_' + str(int(time.time() * 100000)), 'goalId':constant.irisGenericValues['goalId'], 'objectiveId':constant.irisGenericValues['objectiveId'], 'testControl':{'type' : 'ORG', 'test' : 90}})
            detailsOfFilterListCreated = CampaignShardHelper.createFilterList(campaignResponse_ORG['json']['entity']['campaignId'], 'test_timeline_list_{}_{}'.format('org', int(time.time())))
            return detailsOfFilterListCreated['groupLabel']
        except Exception, exp:
           return constant.timelineDetails[constant.config['cluster']]['segment']
        
        
        
        
        
        
        
        
