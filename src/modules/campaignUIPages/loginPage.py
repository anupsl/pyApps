from src.seleniumBase.SeleniumDriver import SeleniumDriver
from src.modules.campaignUIPages.campaignsUIDBCalls import DBCallsCampaigns
from src.utilities.logger import Logger

class loginPage(SeleniumDriver):
    
    def __init__(self, driver):
        SeleniumDriver.__init__(self, driver)
        self.driver = driver
        
    username_id = 'login_user'
    password_id = 'login_cred'
    submit_btn_id = 'c-login-btn'
    logo_linktext = 'Capillary - InTouch'
    otp_id = 'otp__code'
    
    def enterUserName(self, userName):
        self.sendKeys(userName, self.username_id)
        
    def enterPassword(self, password):
        self.sendKeys(password, self.password_id)
    
    def clickLoginBtn(self):
        self.elementClick(self.submit_btn_id)

    def otpVerify(self):
        otpElement = self.getElement(self.otp_id)
        if otpElement != None:
            otpValue = DBCallsCampaigns.getOTP()
            self.sendKeys(otpValue, self.otp_id)
            self.elementClick(self.submit_btn_id)
        
    def login(self, userName, password):
        self.enterUserName(userName)
        self.enterPassword(password)
        self.clickLoginBtn()
        self.otpVerify()
        self.verifyLoginSuccesful()
        
    def verifyLoginSuccesful(self):
        result = self.isElementPresent(self.logo_linktext, locatorType='link')
        return result
    
    def verifyTitle(self):
        if 'Capillary' in self.getTitle():
            return True
        else:
            return False
