from src.seleniumBase.SeleniumDriver import SeleniumDriver
from src.modules.campaignUIPages.campaignsUIDBCalls import DBCallsCampaigns
from src.utilities.logger import Logger
from src.Constant.constant import constant
from src.utilities.assertion import Assertion
import time

class listPage(SeleniumDriver):
    
    def __init__(self, driver, newFilterEnabled=False):
        SeleniumDriver.__init__(self, driver)
        self.driver = driver
        self.newFilterEnabled = newFilterEnabled
        
    btn_createRecipientList_xpath = '//a[contains(text(),\'Create Recipient List\')]'
    ref_loyaltyFilter_id = 'open_filter'
    ref_nonloyaltyFilter_id = 'open_nlfilter'
    ref_upload_id = 'upload_csv'
    ref_paste_id = 'paste_list'
    ref_existing_id = 'duplicate_list'
    ref_merge_id = 'merge'
    iFrame_list_xpath = "//iframe[@id='popupiframe']"
    txt_iframe_listName_id = 'filter_frm__group_name'
    txt_iframe_paste_listName_id = 'paste_list__group_name'
    btn_iframe_paste_chooseFile_id = 'paste_list__upload_file'
    btn_iframe_paste_saveList_id = 'submit'
    btn_iframe_saveList_id = 'btn_save'
    txt_iframe_contentArea_id = 'paste_list__csv_content'
    btn_iframe_close_id = 'close'   
    bdy_iframe_listWrapper_xpath = '//div[@id=\'table_preview_list_wrapper\']'
    btn_iframe_upload_xpath = '//input[@value=\'Upload\']'
    txt_listName_xpath = '//span[contains(text(),\'{lName}\')]'
    
    ref_new_loyaltyFilter_id = 'open_sfilter'
    ref_new_nonloyaltyFilter_id = 'open_snlfilter'
    inp_new_listName_xpath = "//input[@placeholder='Enter list name']"
    btn_new_createList_apply_xpath = "//span[starts-with(text(),'Apply')]"
    btn_new_filter_create_xpath = "//span[starts-with(text(),'Create')]/.."
     
    def selectFilterType(self, filterType):
        try:
            self.waitForElement(self.btn_createRecipientList_xpath, locatorType='xpath')
            if self.isElementPresent(self.btn_createRecipientList_xpath, locatorType='xpath'):
                self.elementClick(self.btn_createRecipientList_xpath, locatorType='xpath')
                time.sleep(5)
                if filterType.lower() == 'loyalty':
                    if self.newFilterEnabled:
                        self.elementClick(self.ref_new_loyaltyFilter_id)
                    else:
                        self.elementClick(self.ref_loyaltyFilter_id)
                elif filterType.lower() == 'nonloyalty':
                    if self.newFilterEnabled:
                        self.elementClick(self.ref_new_nonloyaltyFilter_id)
                    else:
                        self.elementClick(self.ref_nonloyaltyFilter_id)
                elif filterType.lower() == 'upload':
                    self.elementClick(self.ref_upload_id)
                elif filterType.lower() == 'paste':
                    self.elementClick(self.ref_paste_id)
                elif filterType.lower() == 'existing':
                    self.elementClick(self.ref_existing_id)
                elif filterType.lower() == 'merge':
                    self.elementClick(self.ref_merge_id)
                else:
                    raise Exception('Wrong Filter Type Exception')
        except Exception, exp:
                raise Exception(exp)
            
    def switchToListFrame(self,filterType):
        if filterType not in ['loyalty','nonloyalty']:
            self.waitForElement(self.iFrame_list_xpath, locatorType='xpath')
            try:
                if self.isElementPresent(self.iFrame_list_xpath, locatorType='xpath'):
                    self.switchToFrame(self.iFrame_list_xpath, locatorType='xpath')
                else:
                    assert False, 'Frame Locator is not Present'
            except Exception as exp:
                self.closeFrameIfListCreationFailed()
                raise Exception('List Frame Not Loaded with Exception :' + str(exp))
        else:
            Logger.log('New Filter Doesnt Have a Frame')

    def closeFrameIfListCreationFailed(self):
        try:
            self.switchToDefaul()
            self.waitForElement(self.btn_iframe_close_id)
            if self.isElementPresent(self.btn_iframe_close_id):
                    self.elementClick(self.btn_iframe_close_id)
            else:
                assert False, 'Close Frame Locator is not Present'
        except Exception, exp:
            raise Exception('Unable To Close Frame with Close Button due to Exception :{}'.format(exp))
               
    def saveListAsPerFilterType(self, filterType, listName, filePath=constant.userFileMobile, content=constant.campaignuiUserInfo['loyalty']['mobile'] + ',' + constant.campaignuiUserInfo['loyalty']['name']):
        try:
            if filterType.lower() == 'loyalty':
                return self.createLoyaltyOrNonLoyaltyList(listName)
            elif filterType.lower() == 'nonloyalty':
                return self.createLoyaltyOrNonLoyaltyList(listName)
            elif filterType.lower() == 'upload':
                return self.createUploadList(listName, filePath)
            elif filterType.lower() == 'paste':
                return self.createPasteList(listName, content)
            else:
                raise Exception('NoSuchFileTypeException')
        except Exception, exp:
            self.closeFrameIfListCreationFailed()
            raise Exception(exp)
       
    def createLoyaltyOrNonLoyaltyList(self, listName):
        try:
            if self.newFilterEnabled:
                self.implicitWaitOnReactPage()
                self.waitForElement(self.inp_new_listName_xpath, locatorType='xpath')
                self.waitForElement(self.btn_new_filter_create_xpath, locatorType='xpath')
                if self.isElementPresent(self.btn_new_filter_create_xpath, locatorType='xpath'):
                    Logger.log('Create Element is Present , trying to click with wait of 10 secs')
                    time.sleep(10)
                    self.sendKeys(listName, self.inp_new_listName_xpath, locatorType='xpath')
                    self.elementClick(self.btn_new_filter_create_xpath, locatorType='xpath')
                else:
                    raise Exception('New Filter Page taking more time to load')
            else:
                if self.isElementPresent(self.txt_iframe_listName_id) and self.isElementPresent(self.btn_iframe_saveList_id):
                    self.sendKeys(listName, self.txt_iframe_listName_id)
                    self.elementClick(self.btn_iframe_saveList_id)
                else:
                    self.closeFrameIfListCreationFailed()
                    raise Exception('List Frame Not Loaded')
        except Exception, exp:
            raise Exception(exp)
        
    def createUploadList(self, listName, filePath):
        try:
            if self.isElementPresent(self.txt_iframe_paste_listName_id):
                self.sendKeys(listName, self.txt_iframe_paste_listName_id)
                self.sendKeys(filePath, self.btn_iframe_paste_chooseFile_id)
                self.elementClick(self.btn_iframe_paste_saveList_id)
                self.waitForElement(self.bdy_iframe_listWrapper_xpath, locatorType='xpath')
                self.elementClick(self.btn_iframe_upload_xpath, locatorType='xpath')
            else:
                self.closeFrameIfListCreationFailed()
                raise Exception('List Frame Not Loaded')
        except Exception, exp:
            raise Exception(exp)                        
    
    def createPasteList(self, listName, content):
        try:
            if self.isElementPresent(self.txt_iframe_contentArea_id):
                self.sendKeys(listName, self.txt_iframe_paste_listName_id)
                self.sendKeys(content, self.txt_iframe_contentArea_id)
                self.elementClick(self.btn_iframe_paste_saveList_id)
            else:
                self.closeFrameIfListCreationFailed()
                raise Exception('List Frame Not Loaded')
        except Exception, exp:
            raise Exception(exp)   
        
    def getListNameCreated(self, listName):
        listName_locator = self.txt_listName_xpath.replace('{lName}', listName)
        try:
            self.waitForElement(listName_locator, locatorType='xpath')
            if self.isElementPresent(listName_locator, locatorType='xpath'):
                return True
            else :
                return False
        except Exception, exp:
            raise Exception('List Name not Getting Displayed on Recipient List Page with Exception :{}'.format(exp))
    
    def switchToDefaultFromListPage(self):
        try:
            self.switchToDefaul()
        except Exception, exp:
            raise Exception(exp)
            
    def verifyListCreated(self, campaignId, listName): 
        Assertion.constructAssertion(self.getListNameCreated(listName), 'List name Displayed on Recipient List Page')
        Logger.log('Checking DB Group Details and Group Version Details')
        groupId = DBCallsCampaigns.getGroupDetail(campaignId, listName)
        maxNumberOfTry = 5
        groupVersionIdTEST = None
        while True:
            allTargetTypes = DBCallsCampaigns.getGroupVersionDetail(campaignId, groupId)
            if len(allTargetTypes) >= 2 or maxNumberOfTry == 0:
                break
            else:
                maxNumberOfTry = maxNumberOfTry - 1
        
        Assertion.constructAssertion(len(allTargetTypes) >= 2, 'Target Types are less than 2')
        for eachTargetType in allTargetTypes: 
            if eachTargetType[1] == 'TEST':
                groupVersionIdTEST = eachTargetType[0]
            Assertion.constructAssertion(eachTargetType[1] in ['TEST', 'CONTROL'], 'Group Version Details have value:{}'.format(eachTargetType[0]))
        return groupVersionIdTEST
            
    def getNewGroupVersionForList(self,campaignId,listName):
        Logger.log('Getting new group version for list :{}'.format(listName))
        groupId = DBCallsCampaigns.getGroupDetail(campaignId, listName)
        targetType = DBCallsCampaigns.getGroupVersionDetail(campaignId, groupId,versionNumber=1)
        groupVersionIdTEST = None
        for eachTargetType in targetType:
            if eachTargetType[1] == 'TEST':
                groupVersionIdTEST = eachTargetType[0]  
        return groupVersionIdTEST

    
