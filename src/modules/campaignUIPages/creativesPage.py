from src.seleniumBase.SeleniumDriver import SeleniumDriver
from src.modules.campaignUIPages.campaignsUIDBCalls import DBCallsCampaigns
from src.utilities.logger import Logger
from src.utilities.randValues import randValues
from src.Constant.constant import constant
from src.utilities.assertion import Assertion
import time

class creativePage(SeleniumDriver):
    
    def __init__(self, driver):
        SeleniumDriver.__init__(self, driver)
        self.driver = driver
        
    channels_xpath = "//div[@class='content active']/a"
    channelMainContentPage_xpath = "//div[@class='ant-row template-header-container']/button/../div/div"
    btn_createTemplate_xpath = "//div[@class='ant-row template-header-container']/button"
    textArea_template_xpath = "//div[@class='cap-text-area']/textarea"
    btn_tags_xpath = "//span[starts-with(text(),'Tags')]/.."
    tag_Name_xpath = "//li/span[2]//span[text()='{}']"
    search_tagName_xpath = "//input[@placeholder='Search']"
    search_tagName_email_xpath = "//span[@class='ant-input-search ant-input-affix-wrapper']/input"
    input_templateName_id = "template-name"
    tempalate_body_xpath = "//body[@contenteditable='true']"
    btn_saveTemplate_xpath = "//span[contains(text(),'Save')]/.."
    template_name_verify_xpath = "//span[contains(text(),'{templateName}')]"
    btn_skip_guide_xpath = "//button[contains(text(),'SKIP')]"
    iframe_skip_guide_id = "wfx-frame-guidedPopup"
    sel_template_emailType_xpath = "//li[contains(text(),'Upload File')]/../li"
    layout_email_xpath = "//h3[contains(text(),'Select Layout')]/../../..//img/../.."
    layout_btn_selectLayout_xpath = "//button[span[starts-with(text(),'Select')]]"
    iframe_emailEditor_xpath = "//iframe[@title='Rich Text Editor, editor1']"
    iframe_emailEditor_textArea_xpath = "//body[@class='cke_editable cke_editable_themed cke_contents_ltr cke_show_borders']"
    upload_filename_xpath = "//input[@id='filename']"
    wechat_selectAccount_text_xpath = "//div[contains(text(),'Select Account')]/.."
    wechat_selectAccountName_text_xpath = "//li[contains(text(),'{accountName}')]"
    wechat_templateFill_template_xpath = "//div[@class='cap-select ant-select ant-select-enabled']/div/span"
    wechat_allTemplatePresent_xpath = "//li"
    wechat_template_allFields_xpath = "//div[@class='cap-input input-primary chart-name-input']/input" 
    wechat_template_allFieldsTags_xpath = "//div[@class='cap-input input-primary chart-name-input']/../..//button"
    wechat_template_linkField_xpath = "//input[@placeholder='Link']"
    wechat_unmap_template_icon_xpath = "//i[@class='material-icons options-icon']"
    wechat_unmap_template_btn_xpath = "//span[contains(text(),'Unmap')]"
    wechat_unmap_template_del_id = "delete-version"
    wechat_unmap_noTemplate_xpath = "//span[contains(text(),'No Templates Available')]"
    orgChange_input_xpath = "//input[@name='-search']/.."
    orgChange_div_sel_xpath = "//span[contains(text(),'{orgName}')]"
    push_templateType_xpath = "//li[contains(text(),'{templateType}')]"
    push_android_id = "tab-header-android"
    push_ios_id = "tab-header-iphone2"
    push_messageTitle_id = "message-title"
    push_messageTitle_btn_xpath = "//textarea[@id='message-title']/../../..//button"
    push_editor_id = "message-editor"
    push_editorTag_btn_xpath = "//textarea[@id='message-editor']/../../..//button"
    push_ios_messageTitle_id = "message-title2"
    push_ios_editor_id = "message-editor2"
    push_ios_editor_btn_xpath = "//textarea[@id='message-editor2']/../../..//button"
    
    
    def captureCurrentURL(self):
        return self.getCurrentURL()
    
    def setCreativePageURL(self, url):
        try:
            Logger.log('Navigating to URL : {}'.format(url))
            self.navigateToURL(url)
        except Exception, exp:
            Logger.log('Not Able to go to Creative base page due to Exception :{}'.format(exp))
    
    def skipGuide(self):
        Logger.log('Skipping Guide')
        try:
            self.switchToFrame(self.iframe_skip_guide_id)
            self.waitForElement(self.btn_skip_guide_xpath, locatorType='xpath', retry=1)
            if self.isElementPresent(self.btn_skip_guide_xpath, locatorType='xpath'):
                self.elementClick(self.btn_skip_guide_xpath, locatorType='xpath')
        except Exception, exp:
            Logger.log('Exception While Skipping Guide :{}'.format(exp))
        finally:
            self.switchToDefaul()
    
    def selectChannelToCreateTemplate(self, channel='sms'):
        try:
            time.sleep(5)
            Logger.log('Selecting Channel :{} to Create Template'.format(channel))
            self.waitForElement(self.channels_xpath, locatorType='xpath')
            listOfChannelsWebelement = self.getElements(self.channels_xpath, locatorType='xpath')
            for eachChannel in listOfChannelsWebelement:
                Logger.log('Matching channel :{} with :{}'.format(channel, eachChannel.text))
                if str(eachChannel.text).lower() == channel.lower():
                    eachChannel.click()
                    break
                
        except Exception, exp:
            raise Exception('Channel Selection Exception :{}'.format(exp))
    
    def waitForChannelmainContentToLoad(self, channel='sms'):
        try:
            Logger.log('Waiting For Main Content to be loaded')
            channelMainContentPage_xpath = self.channelMainContentPage_xpath
            self.waitForElement(channelMainContentPage_xpath, locatorType='xpath')
            if self.isElementPresent(channelMainContentPage_xpath, locatorType='xpath'):
                actualChannel = self.getElement(self.channelMainContentPage_xpath, locatorType='xpath').text
                if actualChannel.lower() != channel: 
                    Logger.log('Not Able To Find Channel :{} on main content page, calling selectChannel again'.format(channel))
                    self.selectChannelToCreateTemplate(channel=channel)
            else:
                assert False, 'Channel :{} main content page not loaded'.format(channel)
        except Exception, exp:
            Logger.log('Channel mainContent Exception :{}'.format(exp))
    
    def createTemplate(self, channel='sms', TemplateType='Use Editor'):
        try:
            Logger.log('Creating Template')
            self.waitForElement(self.btn_createTemplate_xpath, locatorType='xpath')
            if self.isElementPresent(self.btn_createTemplate_xpath, locatorType='xpath'):
                self.elementClick(self.btn_createTemplate_xpath, locatorType='xpath')
            else:
                assert False, 'Create Template Button Not Found for channel :{}'.format(channel)
            
            if channel.lower() == 'email':        
                if TemplateType == 'Use Editor':
                    emailTemplateType = self.getElements(self.sel_template_emailType_xpath, locatorType='xpath')
                    for eachEmailTemplateType in emailTemplateType:
                        if eachEmailTemplateType.text == 'Use Editor':
                            eachEmailTemplateType.click()
                    
                    self.waitForElement(self.layout_email_xpath, locatorType='xpath')
                    if self.isElementPresent(self.layout_email_xpath, locatorType='xpath'):
                        firstLayout = self.getElements(self.layout_email_xpath, locatorType='xpath')[0]
                        self.moveToElement(firstLayout)
                        self.moveToElement(self.getElement(self.layout_btn_selectLayout_xpath, locatorType='xpath'))
                        self.elementClickWithAction(self.layout_btn_selectLayout_xpath, locatorType='xpath')
                elif TemplateType == 'Upload File' :
                    Logger.log('Uploading File from path :', constant.randomHtmlPath)
                    time.sleep(5)
                    inputFieldForUpload = self.getElement(self.upload_filename_xpath, locatorType='xpath')
                    inputFieldForUpload.send_keys(constant.randomHtmlPath)
                else:
                    raise Exception('NoSuchTemplateTypeException : TemplateType :{}'.format(TemplateType))
            elif channel.lower() == 'mobile push':
                templateTypeElement = self.getElement(self.push_templateType_xpath.replace('{templateType}', TemplateType), locatorType='xpath')
                templateTypeElement.click()
            
        except Exception, exp:
            raise Exception('CreateTemplate Exception :{}'.format(exp))
    
    def templateName(self, templateName, channel = 'sms'):
        try:
            Logger.log('Giving Template Name as :{} for Channel : {}'.format(templateName, channel))
            if channel == 'email':
                self.waitForElement(self.tempalate_body_xpath, locatorType='xpath')
            self.waitForElement(self.input_templateName_id)
            if self.isElementPresent(self.input_templateName_id):
                script = "document.getElementById('{}').value='{}'"
                self.executeScript(script.format(self.input_templateName_id, templateName))
                element = self.getElement(self.input_templateName_id)
                hackKey = randValues.randomString(size=1)
                element.send_keys(hackKey)
                return templateName + hackKey
            else:
                assert False, 'Channel :{} main content page not loaded'.format(channel)
        except Exception, exp:
            raise Exception('TemplateName Exception :{}'.format(exp))
    
    def templateFillSMS(self, text='Automation Created', channel='sms'):
        try:
            Logger.log('Filling Template for Channel :{}'.format(channel))
            self.waitForElement(self.textArea_template_xpath, locatorType='xpath')
            if self.isElementPresent(self.textArea_template_xpath, locatorType='xpath'):
                self.sendKeys(text, self.textArea_template_xpath, locatorType='xpath')
            else:
                assert False, 'TextArea not Found'
        except Exception, exp:
            raise Exception('Template Filling Exception :{}'.format(exp))
    
    def templateFillEMAIL(self, text='Automation Created_'):
        try:
            Logger.log('Filling Template For Channel : Email')
            self.switchToFrame(self.iframe_emailEditor_xpath, locatorType='xpath')
            self.waitForElement(self.iframe_emailEditor_textArea_xpath, locatorType='xpath')
            if self.isElementPresent(self.iframe_emailEditor_textArea_xpath, locatorType='xpath'):
                self.sendKeys(text, self.iframe_emailEditor_textArea_xpath, locatorType='xpath')
        except Exception, exp:
            raise Exception('Template Filling Exception :{}'.format(exp))
        finally:
            self.switchToDefaul()
            
    def selectTags(self, tags, channel='sms'):
        for eachTag in tags:
            try:
                Logger.log('Selecting Tag :{}'.format(eachTag))
                self.waitForElement(self.btn_tags_xpath, locatorType='xpath')
                if self.isElementPresent(self.btn_tags_xpath, locatorType='xpath'):
                    self.elementClick(self.btn_tags_xpath, locatorType='xpath')
                
                if channel.lower() == 'email':
                    searchElement = self.getElement(self.search_tagName_email_xpath, locatorType='xpath')
                else:
                    searchElement = self.getElement(self.search_tagName_xpath, locatorType='xpath')
                
                self.waitForElement(self.search_tagName_xpath, locatorType='xpath')
                if self.isElementPresent(self.search_tagName_xpath, locatorType='xpath'):
                    searchElement.clear()
                    searchElement.send_keys(eachTag)
                    listOfTags = self.getElement(self.tag_Name_xpath.format(eachTag), locatorType='xpath')
                    Logger.log('Element find for tags : ', listOfTags)
                    listOfTags.click()
                else:
                    assert False, 'Tag Search Box Not Visible'
            except Exception, exp:
                raise Exception('Tags Exception :{}'.format(exp)) 
                    
    def saveTemplate(self):
        try:
            Logger.log('Saving Template')
            if self.isElementPresent(self.btn_saveTemplate_xpath, locatorType='xpath'):
                self.elementClick(self.btn_saveTemplate_xpath, locatorType='xpath')
                self.waitForElement(self.channels_xpath, locatorType='xpath')
            else:
                assert False, 'Save Template Button Not Found'
        except Exception, exp:
            raise Exception('SaveTemplate Exception :{}'.format(exp))
    
    def searchAndVerifyCreatedTemplate(self, templateName, channel='sms'):
        if channel.lower() == 'wechat' : templateName = templateName[10:]
        try:
            Logger.log('Searching Template :{}'.format(templateName))
            self.waitForElement(self.search_tagName_xpath, locatorType='xpath')
            if self.isElementPresent(self.search_tagName_xpath, locatorType='xpath'):
                time.sleep(5)
                self.sendKeys(templateName, self.search_tagName_xpath, locatorType='xpath')
                if self.isElementPresent(self.template_name_verify_xpath.replace('{templateName}', templateName), locatorType='xpath'):
                    pass
                else:
                    assert False, 'Template Not Found :{}'.format(templateName)
            else:
                assert False, 'Search Template Input Field Not Found'
        except Exception, exp:
            raise Exception('SearchTemplate Exception :{}'.format(exp))

    def selectAccount(self, channel, accountName):
        try:
            if channel.lower() in ['wechat', 'mobile push']:
                self.refreshCurrentPage()
                self.waitForElement(self.wechat_selectAccount_text_xpath, locatorType='xpath')
                if self.isElementPresent(self.wechat_selectAccount_text_xpath, locatorType='xpath'):
                    self.elementClick(self.wechat_selectAccount_text_xpath, locatorType='xpath')
                    self.elementClick(self.wechat_selectAccountName_text_xpath.replace('{accountName}', accountName), locatorType='xpath')
                else:
                    assert False, 'Account Selection for wechat Failed'
        except Exception, exp:
            raise Exception('SelectAccount Exception :{}'.format(exp))
        
    def templateFillWechat(self, tags=['First Name']):
        try:
            self.waitForElement(self.wechat_templateFill_template_xpath, locatorType='xpath')
            if self.isElementPresent(self.wechat_templateFill_template_xpath, locatorType='xpath'):
                elements = self.getElements(self.wechat_templateFill_template_xpath, locatorType='xpath')
                for eachElement in elements:
                    try:
                        Logger.log('Selecting a Template')
                        eachElement.click()
                    except Exception, exp:
                        Logger.log('Some Elements are not visible with used Xpath')
    
            self.waitForElement(self.wechat_allTemplatePresent_xpath, locatorType='xpath')
            if self.isElementPresent(self.wechat_allTemplatePresent_xpath, locatorType='xpath'):
                allTemplates = self.getElements(self.wechat_allTemplatePresent_xpath, locatorType='xpath')
                for templates in allTemplates:
                    wechatTemplateName = templates.text
                    Logger.log('wechatTemplateName: ', wechatTemplateName)
                    templates.click()
                    break
            else:
                raise Exception('Unable To select Template')
            
            allFieldsInTemplate = self.getElements(self.wechat_template_allFields_xpath, locatorType='xpath')
            allFieldsParellelTags = self.getElements(self.wechat_template_allFieldsTags_xpath, locatorType='xpath')
            for eachField, eachTagButton in zip(allFieldsInTemplate, allFieldsParellelTags):
                eachField.send_keys('Auto_')
                try:
                    for eachTag in tags:
                        eachTagButton.click()
                        searchElements = self.getElements(self.search_tagName_xpath, locatorType='xpath')
                        searchElements = searchElements[len(searchElements) - 1]
                        self.waitForElement(self.search_tagName_xpath, locatorType='xpath')
                        if self.isElementPresent(self.search_tagName_xpath, locatorType='xpath'):
                            searchElements.clear()
                            searchElements.send_keys(eachTag)
                            listOfAllTags = self.getElements(self.tag_Name_xpath, locatorType='xpath')
                            for eachTagOnUI in listOfAllTags:
                                Logger.log('Matching Tag :{} with :{}'.format(eachTagOnUI, eachTag))
                                if eachTagOnUI.text == eachTag:
                                    eachTagOnUI.click()
                                    eachField.click()
                                    break
                except Exception, exp:
                    Logger.log('Unable To use tags for field :{} due to Exception :{}'.format(eachField.text, exp))
                    eachField.click()
            
            if self.isElementPresent(self.wechat_template_linkField_xpath, locatorType='xpath'):
                self.sendKeys('https://www.capillarytech.com/', self.wechat_template_linkField_xpath, locatorType='xpath')
        
            Logger.log('Template saved With Name: ', wechatTemplateName)
            return unicode(wechatTemplateName)
        except Exception, exp:
            raise Exception('TemplateFill Exception :{}'.format(exp))
    
    def templateFillPush(self, pushType, title, message, tags=['First Name']):
        if pushType.lower() == 'android':
            self.elementClick(self.push_android_id)
            self.waitForElement(self.push_messageTitle_id)
            if self.isElementPresent(self.push_messageTitle_id):
               self.sendKeys(title, self.push_messageTitle_id)
               self.sendKeys(message, self.push_editor_id)
            
            for eachTag in tags:
                self.elementClick(self.push_editorTag_btn_xpath, locatorType='xpath')
                searchElements = self.getElements(self.search_tagName_xpath, locatorType='xpath')
                searchElements = searchElements[len(searchElements) - 1]
                searchElements.clear()
                searchElements.send_keys(eachTag)       
                
                listOfAllTags = self.getElements(self.tag_Name_xpath, locatorType='xpath')
                for eachTagOnUI in listOfAllTags:
                    Logger.log('Matching Tag :{} with :{}'.format(eachTagOnUI, eachTag))
                    if eachTagOnUI.text == eachTag:
                        eachTagOnUI.click()
                        break
        else:
            self.elementClick(self.push_ios_id)
            self.waitForElement(self.push_ios_messageTitle_id)
            if self.isElementPresent(self.push_ios_messageTitle_id):
               self.sendKeys(title, self.push_ios_messageTitle_id)
               self.sendKeys(message, self.push_ios_editor_id)
            
            for eachTag in tags:
                self.elementClick(self.push_ios_editor_btn_xpath, locatorType='xpath')
                searchElements = self.getElements(self.search_tagName_xpath, locatorType='xpath')
                searchElements = searchElements[len(searchElements) - 1]
                searchElements.clear()
                searchElements.send_keys(eachTag)
                
                listOfAllTags = self.getElements(self.tag_Name_xpath, locatorType='xpath')
                for eachTagOnUI in listOfAllTags:
                    Logger.log('Matching Tag :{} with :{}'.format(eachTagOnUI, eachTag))
                    if eachTagOnUI.text == eachTag:
                        eachTagOnUI.click()
                        break
        
        
               
    def unMapWeChatTemplate(self):
        try:
            if not self.isElementPresent(self.wechat_unmap_noTemplate_xpath, locatorType='xpath'):
                self.waitForElement(self.wechat_unmap_template_icon_xpath, locatorType='xpath')
                if self.isElementPresent(self.wechat_unmap_template_icon_xpath, locatorType='xpath'):
                    allIconsOfunmap = self.getElements(self.wechat_unmap_template_icon_xpath, locatorType='xpath')
                    for eachIcon in allIconsOfunmap:
                        eachIcon.click()
                        self.getElements(self.wechat_unmap_template_btn_xpath, locatorType='xpath')[-1].click()
                        self.waitForElement(self.wechat_unmap_template_del_id)
                        if self.isElementPresent(self.wechat_unmap_template_del_id):
                            self.elementClick(self.wechat_unmap_template_del_id)
                        else:
                            time.sleep(2)
                            self.elementClick(self.wechat_unmap_template_del_id)
                        self.waitForElement(self.wechat_unmap_template_icon_xpath, locatorType='xpath')
                else:
                    Assertion.constructAssertion(False, 'Unable to UnMap Wechat Template ', verify=True)
        except Exception, exp:
            Assertion.constructAssertion(False, 'UnMapTemplate Exception  :{}, please check manually'.format(exp), verify=True)
       
    def validateDBForTemplate(self, channel, templateName):
        if channel == 'Mobile Push': channel = 'MOBILEPUSH'
        try:
            if templateName != '' : 
                templateJson = DBCallsCampaigns.getTemplateDetails(channel, templateName)
                Assertion.constructAssertion(len(templateJson) == 1, 'With Name :{} there is only 1 active template in this org'.format(templateName))
            else:
                Assertion.constructAssertion(False, 'TemplateName is blank , not able to check in Mongo', verify=True)
        except Exception, exp:
            raise Exception('MongoException :{}'.format(exp))
