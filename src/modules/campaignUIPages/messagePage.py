import datetime, time

from src.Constant.constant import constant
from src.modules.campaignUIPages.campaignsUIDBCalls import DBCallsCampaigns
from src.seleniumBase.SeleniumDriver import SeleniumDriver
from src.utilities.assertion import Assertion
from src.utilities.logger import Logger
from src.modules.iris.dbCallsMessage import dbCallsMessage
from src.modules.campaignUIPages.listPage import listPage

class messagePage(SeleniumDriver):
    
    def __init__(self, driver):
        SeleniumDriver.__init__(self, driver)
        self.driver = driver
        
    common_flashMessage_xpath = "//span[@id='flash_message']"
    chooseRecipient_elements_radiobtn_campaignsList_xpath = "//ul[@id='campaign_list_radio']//li/i"
    chooseRecipient_elements_completeElement_campaignsList_xpath = "//ul[@id='campaign_list_radio']//li/i/.."
    chooseRecipient_elements_radiobtn_stickyList_xpath = "//ul[@id='campaign_list_check']//li/i"
    chooseRecipient_btn_next_xpath = "//div[@id='container_1']/div[1]//div[3]/a"
    
    attachIncentive_radiotbn = {
        "nodeal" : "attach-incentive",
        "coupon": "attach-coupons",
        "point": "attach-points",
        "generic": "attach-generic"
    }
    attachIncentive_pointsAllocation_xpath = "//ul[@id='alloc_points_list']//i"
    attachIncentive_pointsExpiry_xpath = "//ul[@id='exit_points_list']//i"
    attachIncentive_pointSave_id = "points_save"
    attachIncentive_btn_next_xpath = "//div[@id='container_2']/div[1]//div[3]/a"
    
    customizeContent_frame_template = "email-iframe"
    customizeContent_btn_select_xpath = "//li[@template_name='{templateName}']//a[1]"
    customizeContent_email_btn_select_xpath = "//div[@class='ca_search_container_body']/div/div[2]/button"
    customizeContent_input_searchtemplate_xpath = "//input[@placeholder='Search']"
    customizeContent_email_input_searchtemplate_xpath = "//div[@id='ca_templates_collection_div']//input/../..//i/../input"
    customizeContent_email_input_subject_id = 'edit_template__subject'
    customizeContent_sms_next_id = "skip-template"
    customizeContent_email_next_id = "edit_existing"
    customizeContent_btn_next_id = "goto_delivery_setting" 
    customizeContent_email_btn_next_id = "goto_delivery_settings" 
    customizeContent_btn_previewAndTest_id = "preview_and_test"  
    customizeContent_iFrame_previewAndTest_xpath = "//iframe[@id='popupiframe']"
    customizeContent_frame_textArea_previewAndTest_id = "preview_test__csv_content"
    customizeContent_frame_sendSMS_previewAndTest_xpath = "//button[contains(text(),'Send Test SMS')]"
    customizeContent_frame_sendEMAIL_previewAndTest_xpath = "//button[contains(text(),'Send Test Email')]"
    customizeContent_frame_btn_close_id = "close"
    customizeContent_frame_wechat_xpath = "//iframe[@id='email-iframe']"
    customizeContent_frame_wechat_allTemplates_xpath = "//div[@class='main-content']//hr/.."
    customizeContent_frame_wechat_allButton_xpath = "//div[@class='main-content']//hr/..//button"
    customizeContent_frame_wechat_next_btn_id = "skip-template"  
    customizeContent_templatevisible_xpath = "//div[@class='footer-wrapper']//span[contains(text(),'{templateName}')]"
    customizeContent_templatebody_xpath = "//div[@class='footer-wrapper']//span[contains(text(),'{templateName}')]/../../../.."
    customizeContent_selectTemplate_xpath = "//div[@class='footer-wrapper']//span[contains(text(),'{templateName}')]/../../../..//span[contains(text(),'Select')]"
    oldCustomizeContent_selectTemplate_xpath = "//div[@id='creative_template']//li/a[contains(text(),'Select')]"
    oldCustomizeContent_descriptionTemplate_id = "call_task_message__description"
    oldCustomizeContent_subjectTemplate_id = "call_task_message__subject"
    
    templateCreation_btn_createTemplpate = "create_new_template"
    templateCreation_btn_createTemplpate_email_xpath = "//button[contains(text(),'Create new template')]"
    templpateCreation_textArea_sms_xpath = "//div[@class='editor']"
    templateCreation_input_templateName_sms_id = "text_template__template_name"
    templateCreation_btn_saveTemplate_sms_xpath = "//button[contains(text(),'Save')]"
    templateCreation_btn_close_id = 'close'
    templateCreation_img_templates_email_xpath = "//div[@id='create_new_template_parent']//img"
    templateCreation_frame_email = "//iframe[@id='edm_editor_iframe']"
    templateCreation_frame_dragElements_xpath = "//div[@id='elements']//li/div"
    templateCreation_frame_textArea_email_xpath = "//table[@id='root-table']//div"
    templateCreation_frame_doubleClick_textArea_xpath = "//div[@class='elementMenuDrag active']/../div[1]"
    templateCreation_frame_sendingText_textArea_xpath = "//table[@id='root-table']//td/div/div/div[2]"
    templateCreation_frame_email_saveTemplate_id = "save_edit_new"
    templateCreation_frame_email_saveTemplateName_id = "edit_new_name"
    templateCreation_backToTemplate_xpath = "//div[@id='container_3']//a"
    
    deliverSetting_input_valid_id = "validity_for_task_entry"
    deliverSetting_i_statuses_xpath = "//i[@val='OPEN']"
    deliverSetting_select_statuses_id = "default_status"
    deliverySetting_select_schedulleType_id = "send_when"
    deliverySetting_btn_schedulleCampaign_id = "queue_message"
    deliverySetting_select_schedule_id = "send_when"
    deliverySetting_fixedDate_dateTime_id = "date_time"
    deliverySetting_fixedDate_dateSet_xpath = "//a[contains(text(),'{date}')]"
    deliverySetting_fixedDate_dateSetDone_xpath = "//button[contains(text(),'Done')]"
    deliverSetting_recurring_day_week_month_xpath = "//div[@id='div_schedule']//button"
    deliverSetting_recurring_checkAll_xpath = "//span[contains(text(),'Check all')]"
    deliverySetting_recurring_select_cronHour_id = "cron_hours"
    deliverySetting_recurring_select_cronMinute_id = "cron_minutes"
    
    def verifyFlashMessage(self, message):
        for numberOfTries in range(10):
            if self.isElementPresent(self.common_flashMessage_xpath, locatorType='xpath'):
                actualMessage = self.getElement(self.common_flashMessage_xpath, locatorType='xpath').text
                Logger.log('Flash message Found :', actualMessage)
                if actualMessage.lower() == message.lower() :
                    return True
            else:
                time.sleep(1)
        return False
    
    def chooseRecipient(self, listName):
        Logger.log('On Choose Recipient Page of Message Creation Flow')
        try:
            self.waitForElement(self.chooseRecipient_elements_radiobtn_campaignsList_xpath, locatorType='xpath')
            if self.isElementPresent(self.chooseRecipient_elements_radiobtn_campaignsList_xpath, locatorType='xpath'):
                Logger.log('Lists Created are Displayed on Page , clicking on List Type :{}'.format(listName))
                
                self.waitForElement(self.chooseRecipient_elements_completeElement_campaignsList_xpath, locatorType='xpath')
                listOfRecipientsWebElement = self.getElements(self.chooseRecipient_elements_radiobtn_campaignsList_xpath, locatorType='xpath')
                listOfRecipientsCompleteWebElement = self.getElements(self.chooseRecipient_elements_completeElement_campaignsList_xpath, locatorType='xpath')
                numberOfListsOnPage = len(listOfRecipientsCompleteWebElement)
                
                for index in range(numberOfListsOnPage):
                    if listName in listOfRecipientsCompleteWebElement[index].text:
                        listOfRecipientsWebElement[index].click()
                        break
                
                Logger.log('Clicking on Next Button of Choose Recipient Page')
                self.waitForElement(self.chooseRecipient_btn_next_xpath, locatorType='xpath')
                if self.isElementPresent(self.chooseRecipient_btn_next_xpath, locatorType='xpath'):
                    self.elementClick(self.chooseRecipient_btn_next_xpath, locatorType='xpath')
                else:
                    assert False, 'Next Button Not Found'
            else:
                assert False, 'list Radio Button Not Found'
        except Exception, exp:
            raise Exception('ChooseRecipient Exception :{}'.format(exp))        
    
                
    def attachIncentive(self, incentiveType):
        Logger.log('On Attach Incentives Page of message Creation Flow and trying to choose Incentive :{}'.format(incentiveType))
        locatorIncentiveType = self.attachIncentive_radiotbn[incentiveType.lower()]
        try:
            self.waitForElement(locatorIncentiveType)
            if self.isElementPresent(locatorIncentiveType):
                if incentiveType.lower() == 'coupon' : time.sleep(10)
                self.elementClick(locatorIncentiveType)
                
                if incentiveType.lower() == 'point':
                    time.sleep(5)
                    self.elementClick(locatorIncentiveType)
                    self.waitForElement(self.attachIncentive_pointsAllocation_xpath, locatorType='xpath')
                    firstAllocationStrategyOnPage = self.getElements(self.attachIncentive_pointsAllocation_xpath, locatorType='xpath')
                    self.waitForElement(self.attachIncentive_pointsExpiry_xpath, locatorType='xpath')
                    firstExpiryStrategyOnPage = self.getElements(self.attachIncentive_pointsExpiry_xpath, locatorType='xpath')
                    
                    firstAllocationStrategyOnPage[0].click()
                    firstExpiryStrategyOnPage[0].click()
                    if self.isElementPresent(self.attachIncentive_pointSave_id):
                        self.elementClick(self.attachIncentive_pointSave_id)
                    
                Logger.log('Clicking on next Button of Attach Incentive page')
                self.waitForElement(self.attachIncentive_btn_next_xpath, locatorType='xpath')
                if incentiveType.lower() == 'coupon' : time.sleep(10)
                if self.isElementPresent(self.attachIncentive_btn_next_xpath, locatorType='xpath'):
                    self.elementClick(self.attachIncentive_btn_next_xpath, locatorType='xpath')
                else:
                    assert False, 'Next Button Not Found'
            else:
                assert False, 'Locator Type :{} not present'.format(incentiveType)
        except Exception, exp:
            raise Exception('AttachIncentive Exception :{}'.format(exp))
                
    def customizeContent(self, templateName='SomeCaseNotRequired', channel='sms', goToDeliveryPage=True, previewAndTestCheck=False):
        Logger.log('On Customize Content page of Message Creation Flow')
        try:
            if channel not in ['wechat'] :self.customizeContent_searchTemplate(templateName, channel)
            self.customizeContent_selectTemplateAndGoToDeliverypage(templateName, channel, goToDeliveryPage=goToDeliveryPage, previewAndTestCheck=previewAndTestCheck)
        except Exception, exp:
            raise Exception('CustoizeContent Exception :{}'.format(exp))  
    
    def customizeContentOld(self,channel='calltask'):
        Logger.log('On Old Customize Content Page of Message Creation Flow')
        try:
            if channel == 'calltask':
                self.waitForElement(self.oldCustomizeContent_selectTemplate_xpath,locatorType='xpath')
                if self.isElementPresent(self.oldCustomizeContent_selectTemplate_xpath,locatorType='xpath'):
                    time.sleep(2)
                    self.elementClick(self.oldCustomizeContent_selectTemplate_xpath,locatorType='xpath')
                    self.waitForElement(self.oldCustomizeContent_descriptionTemplate_id)
                    self.sendKeys('AutomationDescibed',self.oldCustomizeContent_descriptionTemplate_id)
                    self.sendKeys('AutomationCallTaskList',self.oldCustomizeContent_subjectTemplate_id)
                    self.elementClick(self.customizeContent_btn_next_id)
                    self.setAllowedStatus()
                else:
                    raise Exception('NotAbleToSelectTemplate')
            else:
                raise Exception('Old Customize Content Page only supported for Call task')
        except Exception, exp:
            raise Exception('CustoizeContent Exception :{}'.format(exp))
    
    def setAllowedStatus(self):
        try:
            self.waitForElement(self.deliverSetting_input_valid_id)
            self.waitForElement(self.deliverSetting_i_statuses_xpath,locatorType='xpath')
            time.sleep(5)
            self.elementClick(self.deliverSetting_i_statuses_xpath,locatorType='xpath')
            self.selectWithOptionName(self.deliverSetting_select_statuses_id, optionName='OPEN')
            self.sendKeys('10',self.deliverSetting_input_valid_id)
        except Exception,exp:
            raise Exception('Unable to Set Allowed Status On message queue Page')
    
    def customizeContent_searchTemplate(self, templateName, channel): 
        Logger.log('Searching Template :{} on Customize Content Page'.format(templateName))
        try:
            self.switchToFrame(self.customizeContent_frame_template)
            if channel in  ['sms', 'email']:
                self.waitForElement(self.customizeContent_input_searchtemplate_xpath, locatorType='xpath')
                if self.isElementPresent(self.customizeContent_input_searchtemplate_xpath, locatorType='xpath'):
                    self.sendKeys(templateName, self.customizeContent_input_searchtemplate_xpath, locatorType='xpath') 
                else:
                    assert False, 'Search Template Input Box Not Present'  
            else:
                raise Exception('Channel:{} Not Identified for Template Selection'.format(channel))
        except Exception, exp:
            raise Exception('SearchTemplate Exception :{}'.format(exp))
        finally:
            self.switchToDefaul() 
            
    def customizeContent_selectTemplateAndGoToDeliverypage(self, templateName, channel, goToDeliveryPage, previewAndTestCheck):
        Logger.log('Selecting Template and Clicking on Next Button')
        try:
            self.switchToFrame(self.customizeContent_frame_template)
            if channel in ['sms', 'email','wechat']:
                locatorSelectTemplateBtn = self.customizeContent_btn_select_xpath.replace('{templateName}', templateName) 
                self.waitForElement(self.customizeContent_templatevisible_xpath.replace('{templateName}', templateName), locatorType='xpath')
                if self.isElementPresent(self.customizeContent_templatevisible_xpath.replace('{templateName}', templateName), locatorType='xpath'):
                    time.sleep(10)
                    templateBody = self.getElement(self.customizeContent_templatebody_xpath.replace('{templateName}', templateName), locatorType='xpath')
                    self.moveToElement(templateBody)
                    selectButton = self.getElement(self.customizeContent_selectTemplate_xpath.replace('{templateName}', templateName), locatorType='xpath')
                    self.moveToElement(selectButton)
                    self.elementClickWithAction(self.customizeContent_selectTemplate_xpath.replace('{templateName}', templateName), locatorType='xpath')
                else:
                    raise Exception('NoSuchTemplateException :{}'.format(templateName))  
                self.switchToDefaul()
                if channel.lower() in ['sms','wechat'] and not previewAndTestCheck:
                    self.waitForElement(self.customizeContent_sms_next_id)
                    if self.isElementPresent(self.customizeContent_sms_next_id):
                        time.sleep(10)
                        self.elementClick(self.customizeContent_sms_next_id)
                elif channel.lower() == 'email' and not previewAndTestCheck:
                    self.waitForElement(self.customizeContent_email_input_subject_id)
                    if self.isElementPresent(self.customizeContent_email_input_subject_id):
                        self.sendKeys('AutomationTestCreatedMail', self.customizeContent_email_input_subject_id)
                    else:
                        assert False, 'Not Able To Set Subject as Subject Element Not Present'
                    
                    self.waitForElement(self.customizeContent_email_next_id)
                    if self.isElementPresent(self.customizeContent_email_next_id):
                        time.sleep(5)
                        self.elementClick(self.customizeContent_email_next_id)
                    if goToDeliveryPage :self.goToDeliveryPage(channel)
            else:
                raise Exception('Channel:{} Not Identified for Template Selection'.format(channel))            
        except Exception, exp:
            raise Exception('selectTemplate Exception :{}'.format(exp))

    def goToDeliveryPage(self, channel='sms'):
        try:
            if channel == 'sms':
                self.waitForElement(self.customizeContent_btn_next_id)
                if self.isElementPresent(self.customizeContent_btn_next_id):
                    self.elementClick(self.customizeContent_btn_next_id)
                else:
                     assert False, 'Next Button Not Present'
            else:
                self.waitForElement(self.customizeContent_email_btn_next_id)
                if self.isElementPresent(self.customizeContent_email_btn_next_id):
                    self.elementClick(self.customizeContent_email_btn_next_id)
                else:
                    assert False, 'Next Button Not Present On plain Text Page'
        except Exception, exp:
            raise Exception('CustomizeContentPage Exception :{}'.format(exp))
    
    def setPreviewAndTest(self, channel='sms'):
        try:
            self.waitForElement(self.customizeContent_btn_previewAndTest_id)
            if self.isElementPresent(self.customizeContent_btn_previewAndTest_id):
                time.sleep(5)
                self.elementClick(self.customizeContent_btn_previewAndTest_id)
                self.waitForElement(self.customizeContent_iFrame_previewAndTest_xpath, locatorType='xpath')
                if self.isElementPresent(self.customizeContent_iFrame_previewAndTest_xpath, locatorType='xpath'):
                    self.switchToFrame(self.customizeContent_iFrame_previewAndTest_xpath, locatorType='xpath')
                    self.waitForElement(self.customizeContent_frame_textArea_previewAndTest_id)
                    time.sleep(5)
                    if channel == 'sms':  
                        self.sendKeys('8497846843,Anant', self.customizeContent_frame_textArea_previewAndTest_id)
                        self.elementClick(self.customizeContent_frame_sendSMS_previewAndTest_xpath, locatorType='xpath')
                    else:
                        self.sendKeys('nigam@gmail.com,Anant', self.customizeContent_frame_textArea_previewAndTest_id)
                        self.elementClick(self.customizeContent_frame_sendEMAIL_previewAndTest_xpath, locatorType='xpath')
                else:
                    assert False, 'Iframe on PreviewAndTest Page is not Located'
            else:
                assert False, 'Preview and Test Button Not Found'
        except Exception, exp:
            raise Exception('SetPreviewAndTest Exception :{}'.format(exp))
        finally:
            self.switchToDefaul()
            if self.isElementPresent(self.customizeContent_frame_btn_close_id):
                self.elementClick(self.customizeContent_frame_btn_close_id)
    
    def deliverySetting(self, scheduleType='IMMEDIATE'):
        Logger.log('On Delivery Setting Page of Message Creation Flow')
        try:
            Logger.log('Clicking on Schedulle Campaign Button')
            if scheduleType != 'IMMEDIATE': self.setSchedulleType(scheduleType)
            self.waitForElement(self.deliverySetting_btn_schedulleCampaign_id)
            if self.isElementPresent(self.deliverySetting_btn_schedulleCampaign_id):
                maxNumberOfTry = 5
                while self.isElementPresent(self.deliverySetting_btn_schedulleCampaign_id):
                    maxNumberOfTry = maxNumberOfTry - 1
                    if maxNumberOfTry >= 0:
                        Logger.log('Schedulle Button Try :{}'.format(maxNumberOfTry))
                        self.elementClick(self.deliverySetting_btn_schedulleCampaign_id)
                        time.sleep(5)
                    else:
                        break
            else:
                assert False, 'Schedulle Campaign Message Button Not Present'
        except Exception, exp:
            raise Exception('DeliverySetting Exception :{}'.format(exp))
    
    def setSchedulleType(self, scheduleType):
        try:
            Logger.log('Setting Schedulle Type as :', scheduleType)
            self.waitForElement(self.deliverySetting_select_schedule_id)
            if self.isElementPresent(self.deliverySetting_select_schedule_id):
                self.selectWithOptionName(self.deliverySetting_select_schedule_id, optionName=scheduleType)
                if 'fixed' in scheduleType.lower():
                    self.setFixedDateCampaign()
                else:
                    self.setRecurringCampaign()
            else:
                assert False, 'Schedule Type Not Present :{}'.format(scheduleType)
        except Exception,exp:
            raise Exception("SetScheduller Exception :{}".format(exp))

    def setFixedDateCampaign(self):
        try:
            self.waitForElement(self.deliverySetting_fixedDate_dateTime_id)
            if self.isElementPresent(self.deliverySetting_fixedDate_dateTime_id):
                self.elementClick(self.deliverySetting_fixedDate_dateTime_id)
                setTime = datetime.datetime.fromtimestamp(int(time.time())+60*4).strftime('%Y-%m-%d %H:%M:%S')
                self.executeScript("$('#date_time').val('{}')".format(setTime))
            else:
                assert False,'Schedulle Button is Not Present'
        except Exception,exp:
            raise Exception("SetFixedDate Exception :{}".format(exp))
        
    def setRecurringCampaign(self):
        try:
            listOfDayWeekMonth = self.getElements(self.deliverSetting_recurring_day_week_month_xpath, locatorType='xpath')
            listOfCheckAll = self.getElements(self.deliverSetting_recurring_checkAll_xpath, locatorType='xpath')
            Logger.log(len(listOfDayWeekMonth))
            for eachElement in range(len(listOfDayWeekMonth)):
                try:
                    listOfDayWeekMonth[eachElement].click()
                    listOfCheckAll[eachElement].click()
                    listOfDayWeekMonth[eachElement].click()
                except Exception,exp:
                    Logger.log('Exception Caught :{}'.format(exp))
            
            self.waitForElement(self.deliverySetting_recurring_select_cronHour_id)
            self.selectWithOptionName(self.deliverySetting_recurring_select_cronHour_id, optionName=datetime.datetime.fromtimestamp(int(time.time())+100).strftime('%H'))
            setHours = datetime.datetime.fromtimestamp(int(time.time())+60*4).strftime('%M')
            self.executeScript("$('#cron_minutes').append('<option value={}>{}</option>')".format(setHours,setHours))
            self.executeScript("$('#cron_minutes').val('{}')".format(setHours))
        except Exception,exp:
            raise Exception("SetRecrring Exception :{}".format(exp))
        
    def getMessageIdForExecutedCampaign(self,campaignId,groupVersionId):
        return dbCallsMessage.getMessageQueueId(campaignId,groupVersionId)[0]
        
    def verifyAuthorizeCampaign(self, campaignId, groupVersionId,scheduleType='',listName=None):
        if scheduleType.lower() == 'recurring': 
            lists = listPage(self.driver,newFilterEnabled=True)
            groupVersionId = lists.getNewGroupVersionForList(campaignId,listName)
        try:
            actualMessageId = self.getMessageIdForExecutedCampaign(campaignId, groupVersionId)
            cdResult = DBCallsCampaigns.getCommunicationDetailsWithListDetails(campaignId, groupVersionId)
            Assertion.constructAssertion(cdResult['state'] == 'CLOSED', 'Communication Details state is closed')
            Assertion.constructAssertion(str(cdResult['message_queue_id']) == str(actualMessageId) , 'Actual MessageId :{} and in CD MessageId :{}'.format(actualMessageId,cdResult['message_queue_id']))
        except Exception, exp:
            raise Exception('DB Validation Exception :{}'.format(exp))
    
    def verifyAuthorizeCampaignPreviewAndTest(self, channel, campaignId):
        try:
            Logger.log('verifyAuthorizeCampaignPreviewAndTest woth channel :{} and campaignId :{}'.format(channel, campaignId))
            actualMessageId = dbCallsMessage.getMessageQueueIdForPreviewTest(campaignId)[0]
            cdResult = DBCallsCampaigns.getCommunicationDetailsForPreviewAndTest(channel)
            Assertion.constructAssertion(cdResult['state'] == 'CLOSED', 'Communication Details state is closed')
            Assertion.constructAssertion(str(cdResult['message_queue_id']) == str(actualMessageId), 'Actual MessageId :{} and in CD MessageId :{}'.format(actualMessageId,cdResult['message_queue_id']))
        except Exception, exp:
            raise Exception('DB Validation Exception :{}'.format(exp)) 
      
    def createTemplate(self, message, templateName, channel='sms'):
        try:
            if channel == 'sms':
                self.waitForElement(self.templateCreation_btn_createTemplpate)
                if self.isElementPresent(self.templateCreation_btn_createTemplpate):
                    self.elementClick(self.templateCreation_btn_createTemplpate)
                    
                self.waitForElement(self.customizeContent_iFrame_previewAndTest_xpath, locatorType='xpath')
                if self.isElementPresent(self.customizeContent_iFrame_previewAndTest_xpath, locatorType='xpath'):
                    self.switchToFrame(self.customizeContent_iFrame_previewAndTest_xpath, locatorType='xpath')
                       
                    self.waitForElement(self.templpateCreation_textArea_sms_xpath, locatorType='xpath')
                    self.sendKeys(message, self.templpateCreation_textArea_sms_xpath, locatorType='xpath')
                
                    self.waitForElement(self.templateCreation_input_templateName_sms_id)
                    self.sendKeys(templateName, self.templateCreation_input_templateName_sms_id)
                    self.elementClick(self.templateCreation_btn_saveTemplate_sms_xpath, locatorType='xpath')
                else:
                    assert False, 'Frame Not Identified'   
            else:
                self.waitForElement(self.templateCreation_btn_createTemplpate_email_xpath, locatorType='xpath')
                if self.isElementPresent(self.templateCreation_btn_createTemplpate_email_xpath, locatorType='xpath'):
                    self.elementClick(self.templateCreation_btn_createTemplpate_email_xpath, locatorType='xpath')
                    
                templateImages = self.getElements(self.templateCreation_img_templates_email_xpath, locatorType='xpath')
                templateImages[0].click()
                
                self.waitForElement(self.templateCreation_frame_email, locatorType='xpath')
                if self.isElementPresent(self.templateCreation_frame_email, locatorType='xpath'):
                    self.switchToFrame(self.templateCreation_frame_email, locatorType='xpath')
                    dragElements = self.getElements(self.templateCreation_frame_dragElements_xpath, locatorType='xpath')
                    for eachDragElement in dragElements:
                        if eachDragElement.get_attribute('title') == 'Text':
                            textArea = self.getElement(self.templateCreation_frame_textArea_email_xpath, locatorType='xpath')
                            self.dragAndDropElement(eachDragElement, textArea)
                            
                            self.doubleClickElement(self.templateCreation_frame_doubleClick_textArea_xpath, locatorType='xpath')
                            time.sleep(2)
                            self.sendKeys(message, self.templateCreation_frame_sendingText_textArea_xpath, locatorType='xpath')
                            
                self.switchToDefaul()     
                self.waitForElement(self.customizeContent_email_input_subject_id)
                if self.isElementPresent(self.customizeContent_email_input_subject_id):
                    self.sendKeys('AutomationTestCreatedMail', self.customizeContent_email_input_subject_id)
                else:
                    assert False, 'Not Able To Set Subject as Subject Element Not Present'
                
                self.waitForElement(self.customizeContent_email_next_id)
                if self.isElementPresent(self.customizeContent_email_next_id):
                    self.elementClick(self.customizeContent_email_next_id)
                else:
                    assert False, 'Next Button Not Present On Customize Design Page'
                
                self.waitForElement(self.templateCreation_frame_email_saveTemplate_id)
                if self.isElementPresent(self.templateCreation_frame_email_saveTemplate_id):
                    self.sendKeys(templateName, self.templateCreation_frame_email_saveTemplateName_id)
                    self.elementClick(self.templateCreation_frame_email_saveTemplate_id)
                else:
                    assert False, 'Save Template Button Missing'
                
                time.sleep(5)
                allReferenceInContainer = self.getElements(self.templateCreation_backToTemplate_xpath, locatorType='xpath')
                allReferenceInContainer[0].click()
        except Exception, exp:
            raise Exception('Not Able To Create Campaign due to Exception :{}'.format(exp))
        finally:
            self.switchToDefaul()
            if self.isElementPresent(self.templateCreation_btn_close_id):
                self.elementClick(self.templateCreation_btn_close_id)
             
    def verifyTemplateCreation(self, templateName, channel='sms'):
        try:
            self.customizeContent_searchTemplate(templateName, channel)
            self.customizeContent_selectTemplateAndGoToDeliverypage(templateName, channel, goToDeliveryPage=False)
        except Exception, exp:
            raise Exception('Template Verification Failed with Exception :{}'.format(exp))
