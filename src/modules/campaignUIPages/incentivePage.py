from src.seleniumBase.SeleniumDriver import SeleniumDriver
from src.utilities.logger import Logger
from src.Constant.constant import constant
from src.utilities.randValues import randValues
from src.modules.luci.luciHelper import LuciHelper
import time

class incentivePage(SeleniumDriver):
    
    def __init__(self, driver):
        SeleniumDriver.__init__(self, driver)
        self.driver = driver

    coupons_view_list_xpath = "//div[contains(@class, 'coupons-view')]"
    btn_createNewCoupon_xpath = "//button/span[starts-with(text(),'Create Offer')]/.."
    txt_couponSeriesTag_xpath = "//span[starts-with(text(),'Offer name')]/../../..//input"
    iframe_coupon_page_id = "coupons-iframe"
    iframe_coupon_series_id = 'create-coupon-series'
    close_btn_coupon_iframe_id = 'close'
    div_discount_section_xpath = "//div[starts-with(text(),'Discount details')]"
    inp_discount_value_xpath = "//span[starts-with(text(),'Fixed Amount')]/..//input"
    btn_previewAndSave_xpath = "//span[starts-with(text(),'Preview and save')]/.."
    btn_createOffer_xpath = "//span[starts-with(text(),'Create offer')]/.."
    btn_update_offer_xpath = "//button/span[text()='Update offer']/.."
    btn_preview_update_xpath = "//button/span[text()='Preview and update']/.."
    btn_claim_offer_xpath = "//button/span[text()='Claim Offer']/.."
    txt_couponName_xpath = "//a[starts-with(text(),'{}')]"
    inp_search_coupon_series_xpath = "//input[@placeholder='Offer name']"
    btn_radio_along_with_campaign_xpath = "//input[@type='radio']/../..//span[text()='Along with campaign/system']"
    btn_radio_fixed_date_xpath = "//input[@type='radio']/../..//span[text()='Fixed date']"
    inp_fixed_date_xpath = "//span[text()='Fixed date']/..//input"
    calendar_fixed_date_xpath = "//td[@title='{}']"  # or we can send value directly using js to input field
    input_pos_xpath = "//span[starts-with(text(),'Point-of-sale Identifier')]/../../..//input"
    label_discount_details_xpath = "//div[text() = 'Discount details']"
    label_coupons_details_xpath = "//div[text() = 'Coupons details']"
    inp_fixed_amount_xpath = "//span[text()='Fixed Amount']/..//input"
    inp_perc_based_xpath = "//span[text()='Percentage based']/..//input"
    toggle_btn_max_discount_xpath = "//span[text()='Max discount']/../../..//span[contains(@class,'cap-switch')]"
    btn_radio_discCode_xpath = "//label[contains(@class,'radio')]//span[text()='Automatically create unique codes']"
    btn_edit_auto_gen_coupon_length_xpath = "//label[contains(@class,'radio')]//span[text()='Automatically create unique codes']/../../..//div//a[text()='Edit']/.."
    inp_coupon_length_xpath = "//label[contains(@class,'radio')]//span[text()='Automatically create unique codes']/../../..//div//input"
    btn_coupon_length_save_xpath = "//label[contains(@class,'radio')]//span[text()='Automatically create unique codes']/../..//div//div//a[text()='Save']"
    btn_radio_generic_xpath = "//label[contains(@class,'radio')]//span[text()='Give a common code to all coupons']"
    inp_generic_code_xpath = "//label[contains(@class,'radio')]//span[text()='Common Code']/../../..//input"
    btn_radio_disc_code_pin_xpath = "//label[contains(@class,'radio')]//span[text()='Upload existing coupon codes']"
    btn_radio_external_xpath = "//label[contains(@class,'radio')]//span[text()='through a Third party']"
    btn_view_add_xpath = "//button/span[text()='View/Add']/.."
    h3_upload_coupons_xpath = "//h3[text()='Upload Coupons']"
    list_coupon_series_xpath = "//tr//a"
    btn_edit_offer_xpath = "//button/span[text()='Edit offer']/.."
    btn_close_upload_xpath = "//div/h3[text()='Upload Coupons']/../../div[@id='box-actions']/i[text()='close']"
    btn_close_view_offer_xpath = "//div/h3[text()='View offer - {}']/../../div[@id='box-actions']/i[text()='close']"
    view_advance_setting_xpath = "//div[@class='cap-pane']//a[text()='View advanced settings']/."
    inp_advance_setting_xpath = "//input[@placeholder='Advanced settings']"
    dynamic_left_div_xpath = "//div[text()='{}']"
    dropDown_resend_xpath = "//div[@title='do not send any coupon']"
    dropDown_switch_resend_coupon_xpath = "//li[text()='send the existing valid coupon']"
    view_basic_setting_xpath = "//a[text()='View basic settings']"
    mutual_exclusive_xpath = "//div[@class='inline-preview-title'][text()='Restrict based on past coupon issuals']/../../."
    toggle_mutual_exclusive_xpath = "//label/span[text()='Restrict based on past coupon issuals']/../../../div//span[@class='cap-switch ant-switch']"
    dynamic_toggle_xpath = "//label/span[text()='{}']/../../../div//span[@class='cap-switch ant-switch']"
    inp_max_redeem_xpath = "//span[text()='Allow a coupon to be redeemed more than once']/../../../../..//input"
    inp_search_mutual_coupon_series_xpath = "//input[@placeholder='search coupon identifier']"
    checkbox_mutual_coupon_series_xpath = "//div[@class='coupon-card']//input[@type='checkbox']"
    tag_select_coupon_series_xpath = "//span[contains(text(),'offers selected')]/../..//span[contains(text(),'{}')]"
    lable_expiry_reminder_xpath = "//div[@class='inline-preview-title'][text()='Send expiry reminders']/../../."
    toggle_expiry_reminder_xpath = "//label/span[text()='Send expiry reminders']/../../../div//span[@class='cap-switch ant-switch']"
    inp_reminder_days_xpath = "//div[@class='reminder']//input"
    btn_reminder_config_xpath = "//div[@class='reminder']//button"
    reminder_sms_blank_template_xpath = "//div[@class='sms-template-content']/div[text()='Blank Template']"
    inp_sms_editor_id = "sms-editor"
    btn_sms_config_save_xpath = "//button/span[text()='Save']/.."
    error_msg_xpath = "//span[@class='textarea-error-message']"
    dropDown_select_tills_xpath = "//div//span[text()='Restrict stores allowing redemptions']/../../../div//span[text()='Select Tills']"
    checkbox_tills_xpath = "//span[@title='Select all']/.././/span[@class='ant-tree-checkbox']"
    btn_select_till_xpath = "//button/span[text()='Select']/.."
    btn_resend_sms_edit_xpath = "//button/span[text()='Edit']/.."
    btn_select_all_template_xpath = "//button/span[text()='< See all templates']/.."
    btn_radio_claim_coupon_series_xpath = "//td[text()='{}']/..//input[@type='radio']"
    btn_claim_xpath = "//button/span[text()='Claim']/.."
    inp_upload_file_xpath = "//button/span[text()='Choose .csv file']/../../input"

    def createCoupons(self, couponName, couponType = 'DISC_CODE'):
        try:
            self.navigateToURL(constant.config['intouchUrl']+ '/coupons/ui/')
            self.implicitWaitOnReactPage()
            self.elementClick(self.btn_createNewCoupon_xpath, locatorType='xpath')
            self.implicitWaitOnReactPage()
            self.sendKeys(couponName, self.txt_couponSeriesTag_xpath, locatorType='xpath')
            self.elementClick(self.label_discount_details_xpath,locatorType='xpath')
            self.sendKeys(10,self.inp_fixed_amount_xpath,'xpath')
            self.elementClick(self.label_coupons_details_xpath, locatorType='xpath')
            if couponType == 'DISC_CODE':
                self.elementClick(self.btn_radio_discCode_xpath, locatorType='xpath')
                self.elementClick(self.btn_edit_auto_gen_coupon_length_xpath, locatorType='xpath')
                self.waitForElement(self.inp_coupon_length_xpath, locatorType='xpath')
                self.sendKeys(9,self.inp_coupon_length_xpath, locatorType='xpath')
                self.elementClick(self.btn_coupon_length_save_xpath, locatorType='xpath')
            elif couponType == 'DISC_CODE_PIN':
                self.elementClick(self.btn_radio_disc_code_pin_xpath, locatorType='xpath')
            elif couponType == 'GENERIC':
                self.elementClick(self.btn_radio_generic_xpath, locatorType='xpath')
                self.sendKeys(LuciHelper.generateCouponCode(), self.inp_generic_code_xpath, locatorType='xpath')
            elif couponType == 'EXTERNAL':
                self.waitForElement(self.btn_radio_external_xpath, locatorType='xpath')
                self.elementClick(self.btn_radio_external_xpath, locatorType='xpath')
            self.elementClick(self.view_advance_setting_xpath, locatorType='xpath')
        except Exception, exp:
            raise Exception('Create New Coupon Exception :{}'.format(exp))

    def previewAndSave(self, isUpdateoffer = False):
        try:
            if not isUpdateoffer:
                self.waitForElement(self.btn_previewAndSave_xpath,locatorType='xpath')
                self.elementClick(self.btn_previewAndSave_xpath,locatorType='xpath')
                self.waitForElement(self.btn_createOffer_xpath,locatorType='xpath')
                self.elementClick(self.btn_createOffer_xpath, locatorType='xpath')
            else:
                self.waitForElement(self.btn_preview_update_xpath, locatorType='xpath')
                self.elementClick(self.btn_preview_update_xpath, locatorType='xpath')
                self.waitForElement(self.btn_update_offer_xpath, locatorType='xpath')
                self.elementClick(self.btn_update_offer_xpath, locatorType='xpath')
            self.implicitWaitOnReactPage()
        except Exception, exp:
            raise Exception('Preview and Save Coupon Exception :{}'.format(exp))

    def addMutualExclusiveCouponSeries(self, couponSeriesName):
        try:
            # self.elementClick(self.view_advance_setting_xpath, locatorType='xpath')
            self.waitForElement(self.mutual_exclusive_xpath, locatorType='xpath')
            self.elementClick(self.mutual_exclusive_xpath, locatorType='xpath')
            self.elementClick(self.toggle_mutual_exclusive_xpath, locatorType='xpath')
            self.implicitWaitOnReactPage()
            self.sendKeys(couponSeriesName, self.inp_search_mutual_coupon_series_xpath, locatorType='xpath')
            self.implicitWaitOnReactPage()
            self.elementClick(self.checkbox_mutual_coupon_series_xpath, locatorType='xpath')
            self.implicitWaitOnReactPage()
            xpathConstruct = self.tag_select_coupon_series_xpath.format(couponSeriesName)
            self.isElementPresent(xpathConstruct, locatorType='xpath')
        except Exception, exp:
            raise Exception('Add mutual Exclusive coupon series Exception :{}'.format(exp))

    def addExpiryReminder(self, templateValue):
        try:
            # self.elementClick(self.view_advance_setting_xpath, locatorType='xpath')
            self.waitForElement(self.lable_expiry_reminder_xpath, locatorType='xpath')
            self.elementClick(self.lable_expiry_reminder_xpath, locatorType='xpath')
            self.elementClick(self.toggle_expiry_reminder_xpath, locatorType='xpath')
            self.waitForElement(self.inp_reminder_days_xpath, locatorType='xpath')
            self.sendKeys(2,self.inp_reminder_days_xpath, locatorType= 'xpath')
            self.elementClick(self.btn_reminder_config_xpath, locatorType='xpath')
            self.smsTemplateFill(templateValue)
        except Exception, exp:
            raise Exception('Add Expiry Reminder coupon series Exception :{}'.format(exp))

    def smsTemplateFill(self, templateValue):
        try:
            self.implicitWaitOnReactPage()
            self.waitForElement(self.reminder_sms_blank_template_xpath, locatorType='xpath')
            self.elementClick(self.reminder_sms_blank_template_xpath, locatorType='xpath')
            self.waitForElement(self.inp_sms_editor_id)
            script = "document.getElementById('{}').value='{}'"
            self.executeScript(script.format(self.inp_sms_editor_id, templateValue))
            element = self.getElement(self.inp_sms_editor_id)
            hackKey = randValues.randomString(size=1)
            element.send_keys(hackKey)
            self.waitForElement(self.btn_sms_config_save_xpath, locatorType='xpath')
            self.isClickable(self.getElement(self.btn_sms_config_save_xpath, locatorType='xpath'))
            self.elementClick(self.btn_sms_config_save_xpath, locatorType='xpath')
            if self.isVisible(self.getElement(self.error_msg_xpath, locatorType='xpath')):
                self.waitUntillElementFound(self.error_msg_xpath)
                self.elementClick(self.btn_sms_config_save_xpath, locatorType='xpath')
        except Exception, exp:
            raise Exception('Edit SMS template coupon series Exception :{}'.format(exp))

    def advanceSettingSearch(self, data):
        # self.elementClick(self.view_advance_setting_xpath, locatorType='xpath')
        self.waitForElement(self.inp_advance_setting_xpath, locatorType='xpath')
        self.sendKeys(data,self.inp_advance_setting_xpath, locatorType='xpath')
        dynamic_xpath = self.dynamic_left_div_xpath.format(data)
        self.isVisible(self.getElement(dynamic_xpath, locatorType='xpath'))
        self.elementClick(dynamic_xpath, locatorType='xpath')

    def reIssueCouponEnable(self):
        self.waitForElement(self.dropDown_resend_xpath, locatorType='xpath')
        self.elementClick(self.dropDown_resend_xpath, locatorType='xpath')
        self.waitForElement(self.dropDown_switch_resend_coupon_xpath, locatorType='xpath')
        self.elementClick(self.dropDown_switch_resend_coupon_xpath, locatorType='xpath')

    def allowMultipleRedemption(self):
        multiple_use = self.dynamic_toggle_xpath.format('Allow a coupon to be redeemed more than once')
        self.waitForElement(multiple_use, locatorType='xpath')
        self.elementClick(multiple_use, locatorType='xpath')
        allow_same_user_redemption = self.dynamic_toggle_xpath.format('Limit the maximum times a customer can redeem a coupon')
        self.waitForElement(allow_same_user_redemption, locatorType='xpath')
        self.elementClick(allow_same_user_redemption, locatorType='xpath')
        self.sendKeys(5,self.inp_max_redeem_xpath, locatorType='xpath')

    def redeemTillsSelections(self):
        self.waitForElement(self.dropDown_select_tills_xpath, locatorType='xpath')
        self.elementClick(self.dropDown_select_tills_xpath, locatorType='xpath')
        self.waitForElement(self.checkbox_tills_xpath, locatorType='xpath')
        self.elementClick(self.checkbox_tills_xpath, locatorType='xpath')
        self.elementClick(self.btn_select_till_xpath, locatorType='xpath')

    def resendSMSTemplate(self, templateValue):
        self.waitForElement(self.btn_resend_sms_edit_xpath, locatorType='xpath')
        self.elementClick(self.btn_resend_sms_edit_xpath, locatorType='xpath')
        self.waitForElement(self.btn_select_all_template_xpath, locatorType='xpath')
        self.elementClick(self.btn_select_all_template_xpath, locatorType='xpath')
        self.smsTemplateFill(templateValue)

    def editOfferAndSave(self, actualOfferName, changeOfferName):
        self.elementClick(self.list_coupon_series_xpath, locatorType='xpath')
        self.waitForElement(self.btn_edit_offer_xpath, locatorType='xpath')
        self.elementClick(self.btn_edit_offer_xpath, locatorType='xpath')
        self.implicitWaitOnReactPage()
        self.sendKeys(changeOfferName, self.txt_couponSeriesTag_xpath, locatorType='xpath')
        self.previewAndSave(isUpdateoffer=True)
        close_xpath = self.btn_close_view_offer_xpath.format(actualOfferName)
        self.waitForElement(close_xpath, locatorType='xpath')
        self.elementClick(close_xpath, locatorType='xpath')


    def searchCouponAndVerify(self, couponSeriesName):
        couponFound = False
        try:
            self.refreshCurrentPage()
            self.sendKeys(couponSeriesName, self.inp_search_coupon_series_xpath, locatorType='xpath')
            self.implicitWaitOnReactPage()
            self.implicitWaitOnReactPage()
            self.implicitWaitOnReactPage()
            at_elements = self.getElements(self.list_coupon_series_xpath, locatorType='xpath')
            for ele in at_elements:
                if ele.text == couponSeriesName:
                    Logger.log('Searched Coupon series Name: {} Found'.format(couponSeriesName))
                    couponFound = True
                    break
            if not couponFound:
                raise Exception('Coupon Series: {} not appeared in coupon search'.format(couponSeriesName))
        except Exception, exp:
            raise Exception('Coupon series & Verify Exception :{}'.format(exp))

    def claimCouponSeries(self, couponSeriesName):
        try:
            self.waitForElement(self.iframe_coupon_page_id)
            self.switchToFrame(self.iframe_coupon_page_id)
            self.waitForElement(self.btn_claim_offer_xpath, locatorType= 'xpath')
            self.elementClick(self.btn_claim_offer_xpath, locatorType= 'xpath')
            time.sleep(60)
            self.waitForElement(self.iframe_coupon_series_id)
            self.switchToFrame(self.iframe_coupon_series_id)
            self.waitForElement(self.inp_search_coupon_series_xpath, locatorType='xpath')
            self.sendKeys(couponSeriesName, self.inp_search_coupon_series_xpath, locatorType='xpath')
            claimCouponXpath = self.btn_radio_claim_coupon_series_xpath.format(couponSeriesName)
            self.elementClick(claimCouponXpath,locatorType='xpath')
            self.elementClick(self.btn_claim_xpath, locatorType='xpath')
        except Exception, exp:
            raise Exception('Claim Coupon series not Found Exception :{}'.format(exp))
        finally:
            self.switchToDefaul()


    def createNewCoupon(self, couponName):
        try:
            self.waitForElement(self.iframe_coupon_page_id)
            self.switchToFrame(self.iframe_coupon_page_id)
            self.waitForElement(self.btn_createNewCoupon_xpath,locatorType='xpath')
            if self.isElementPresent(self.btn_createNewCoupon_xpath,locatorType='xpath'):
                self.elementClick(self.btn_createNewCoupon_xpath,locatorType='xpath')
                # self.switchToDefaul()
                self.waitForElement(self.iframe_coupon_series_id)
                self.switchToFrame(self.iframe_coupon_series_id)
                self.sendKeys(couponName, self.txt_couponSeriesTag_xpath,locatorType='xpath')
                self.elementClick(self.div_discount_section_xpath,locatorType='xpath')
                self.sendKeys(20, self.inp_discount_value_xpath,locatorType='xpath')
                self.elementClick(self.btn_previewAndSave_xpath,locatorType='xpath')
                self.elementClick(self.btn_createOffer_xpath,locatorType='xpath')
                self.sendKeys(couponName, self.list_coupon_series_xpath.format(couponName), locatorType='xpath')
            else:
                assert False, 'Create Coupon  Button Locator is not Present'
        except Exception, exp:
            if self.isElementPresent(self.close_btn_coupon_iframe_id) :
                self.switchToDefaul()
                self.elementClick(self.close_btn_coupon_iframe_id)
            raise Exception('Create New Coupon Exception :{}'.format(exp))
        finally:
            self.switchToDefaul()
            
    def verifyCouponCreation(self, couponName, retry=True):
        try:
            self.waitForElement(self.iframe_coupon_page_id)
            self.switchToFrame(self.iframe_coupon_page_id)
            self.waitForElement(self.txt_couponName_xpath.format(couponName), locatorType='xpath')
            if self.isElementPresent(self.txt_couponName_xpath.format(couponName), locatorType='xpath'):
                couponNameOnUI = self.getElement(self.txt_couponName_xpath.format(couponName), locatorType='xpath').text
                if len(couponNameOnUI) == 0 and retry:
                    Logger.log('Locator Identified but Name Of Coupon is still not Set , Retrying Verification')
                    time.sleep(2)
                    return self.verifyCouponCreation(couponName, False)
                Logger.log('Validating Coupon Created :{} with Coupon Name on UI :{}'.format(couponName, couponNameOnUI))
                if couponNameOnUI == couponName:
                    return True
                else:
                    return False
            else:
                return False
        except Exception,exp:
            raise Exception('Verify Of Coupon Failed with Exception :{}'.format(exp))
        finally:
            self.switchToDefaul()

        
            
