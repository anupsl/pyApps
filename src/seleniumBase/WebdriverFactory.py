from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from src.Constant.constant import constant
import os

class WebDriverFactory():
    
    """ @Browser Support """
    
    def __init__(self):
        os.environ["webdriver.chrome.driver"] = constant.chromeDriverPath
        self.capabilitites = DesiredCapabilities.CHROME
        self.capabilitites['loggingPrefs'] = { 'browser':'ALL' }
        self.chrome_options = Options()
        if constant.config['os'] == 'linux' and constant.config['headlessMode'] == True:
            self.chrome_options.add_argument("--headless")
            self.chrome_options.add_argument("--window-size=1366x768")
        
    def getWebDriverInstance(self):
        driver = webdriver.Chrome(constant.chromeDriverPath, desired_capabilities=self.capabilitites, chrome_options=self.chrome_options)
        driver.maximize_window()
        driver.implicitly_wait(20)
        driver.get(constant.config['intouchUrl'])
        return driver
    
