from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from traceback import print_stack
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
from src.utilities.logger import Logger
from src.Constant.constant import constant
import time, os, traceback

class SeleniumDriver():

    def __init__(self, driver):
        self.driver = driver

    def getTitle(self):
        return self.driver.title
        
    def getCurrentURL(self):
        try:
            return self.driver.current_url
        except Exception, exp:
            Logger.log('Unable To get Current URL')
            return None

    def switchOrgUsingCookies(self, orgId = constant.config['orgId']):
        oldCookies = self.driver.get_cookies()
        try:
            updateCookie = []
            for cookie in oldCookies:
                if cookie['name'] == 'OID':
                    cookie['value'] = str(orgId)
                    updateCookie.append(cookie)
                else:
                    updateCookie.append(cookie)
            self.driver.delete_all_cookies()
            for newCookie in updateCookie:
                self.driver.add_cookie(newCookie)
            self.refreshCurrentPage()
            Logger.log('OrgId : {} Update successfully in Cookies'.format(orgId))
        except Exception, exp:
            Logger.log('Unable to update orgId in cookies, Exception : ', exp)

    def executeScript(self, script):
        try:
            Logger.log("Running JS Script : {}".format(script))
            self.driver.execute_script(script)
        except Exception, exp:
            Logger.log('Unable to Execute Script :{} due to exception  :{}'.format(script, exp))
            
    def refreshCurrentPage(self):
        try:
            self.driver.refresh()
        except Exception, exp:
            Logger.log('Unable to Refresh Page with Exception :{}'.format(exp))
            currentURL = self.getCurrentURL()
            Logger.log('Refreshing Current URL :', currentURL)
            self.driver.get(currentURL)
        finally:
            time.sleep(3)
            
    
    def navigateToURL(self, url):
        try:
            self.driver.get(url)
        except Exception, exp:
            Logger.log('Unable to navigate to url :{}'.format(url))

    def getByType(self, locatorType, locator):
        locatorType = locatorType.lower()
        if locatorType == "id":
            return self.driver.find_elements(By.ID, locator)
        elif locatorType == "name":
            return self.driver.find_elements(By.NAME, locator)
        elif locatorType == "xpath":
            return self.driver.find_elements(By.XPATH, locator)
        elif locatorType == "css":
            return self.driver.find_elements(By.CSS_SELECTOR, locator)
        elif locatorType == "class":
            return self.driver.find_elements(By.CLASS_NAME, locator)
        elif locatorType == "link":
            return self.driver.find_elements(By.LINK_TEXT, locator)
        else:
            Logger.log("Locator type " + locatorType + " not correct/supported")
        return False

    def getElement(self, locator, locatorType="id"):
        element = None
        try:
            element = self.getByType(locatorType, locator)[0]
            Logger.log("Element found with locator: " + locator + " and  locatorType: " + locatorType)
        except:
            Logger.log("Element not found with locator: " + locator + " and  locatorType: " + locatorType)
        finally:
            return element

    def getElements(self, locator, locatorType="id"):
        elements = None
        try:
            elements = self.getByType(locatorType, locator)
            Logger.log("Element found with locator: " + locator + " and  locatorType: " + locatorType)
        except:
            Logger.log("Element not found with locator: " + locator + " and  locatorType: " + locatorType)
        finally:
            return elements
    
    def retryElementClick(self, locator, locatorType="id", numberOfTries=5):
        Logger.log('Retrying Element Click for locator :{} and number of Tries are :{}'.format(locator, numberOfTries))
        retrySucessfull = False
        for eachTryToClick in range(numberOfTries):
            try:
                Logger.log('Try:{}'.format(eachTryToClick))
                element = self.getElement(locator, locatorType)
                element.click()
                retrySucessfull = True 
                break
            except Exception, exp:
                Logger.log('Got Exception :', exp)
                time.sleep(5)
        
        if retrySucessfull:
            Logger.log('With Retry able to Click on Element with locator:{}'.format(locator))
        else:
            raise Exception('ElementClickException for Locator :{} even after retry multiple times'.format(locator))
    
    def elementClick(self, locator, locatorType="id"):
        try:
            element = self.getElement(locator, locatorType)
            Logger.log("Clicked on element :{} with locator {}".format(element, locator))
            element.click()
        except Exception, exp:
            Logger.log('ElementClick Exception :{} but we will retry to click on Element as Element is captured'.format(exp))
            self.retryElementClick(locator, locatorType)
            
    def elementClickWithAction(self, locator, locatorType="id"):
        try:
            Logger.log('Using Action Class to Click on Element')
            actions = ActionChains(self.driver)
            element = self.getElement(locator, locatorType)
            actions.move_to_element(element)
            actions.click(element)
            actions.perform()
        except Exception, exp:
            Logger.log("Failed to click on the element with locator : " + locator + " locatorType: " + locatorType)
            raise Exception('Unable to Click on locator :{} with Exception  :{}'.format(locator, exp))
   
    def moveToElement(self, webelement):
        try:
            actions = ActionChains(self.driver)
            actions.move_to_element(webelement)
            actions.perform()
            time.sleep(5)
        except Exception, exp:
            Logger.log('Unable To Move To Element :{}'.format(webelement))
            raise Exception('Move To Element Exception with Message :{}'.format(exp))
        
    def dragAndDropElement(self, source_element, dest_element):
        try:
            actions = ActionChains(self.driver)
            actions.drag_and_drop(source_element, dest_element)
            actions.perform()
        except Exception, exp:
            Logger.log('Failed To Perform Drag and Drop with source :{} and destination :{}'.format(source_element, dest_element))
            raise Exception('Unable to Perform drag and drop with Exception :{}'.format(exp))
        
    def doubleClickElement(self, locator, locatorType='id'):
        try:
            actions = ActionChains(self.driver)
            actions.double_click(self.getElement(locator, locatorType))
            actions.perform()
        except Exception, exp:
            Logger.log('Failed to Double Click on element:{}'.format(locator))
            raise Exception('Unable To Perform Double Click with Exception :{}'.format(exp))
        
    def sendKeys(self, data, locator, locatorType="id"):
        try:
            element = self.getElement(locator, locatorType)
            element.clear()
            element.send_keys(data)
            Logger.log("Sent data on element with locator: " + locator + " locatorType: " + locatorType)
        except Exception, exp:
            Logger.log("Failed to send data on the element with locator : " + locator + " locatorType: " + locatorType)
            raise Exception('Unable to Send keys to locator :{} with Exception :{}'.format(locator, exp))

    def selectWithOptionName(self, locator, locatorType="id", optionName=None):
        try:
            element = self.getElement(locator, locatorType)
            for retry in range(5):
                Logger.log('Selecting Option :{} for locator :{} with element :{}'.format(optionName, locator, element))
                if element is not None: 
                    for option in element.find_elements_by_tag_name('option'):
                        Logger.log('Matching option :{} with UI Option :{}'.format(optionName, option.text))
                        if option.text == optionName:
                            Logger.log('option matched to Click')
                            option.click() 
                            break
                else:
                    Logger.log('As Element :{} we will retry the Selection')
                    element = self.getElement(locator, locatorType)
            time.sleep(0.5)
        except Exception, exp:
            raise Exception('Unable to select Option with locator :{} with Exception :{}'.format(locator, exp))

    def switchToFrame(self, locator, locatorType="id"):
        try:
            self.waitForElement(locator, locatorType)
            element = self.getElement(locator, locatorType)
            self.driver.switch_to_frame(element)
            time.sleep(0.5)
            Logger.log("Switched to Frame with locator: " + locator + "with locator Type : " + locatorType)
        except Exception, exp:
            raise Exception('Unable To Switch to Frame with locator :{} with Exception :{}'.format(locator, exp))

    def switchToDefaul(self):
        try:
            self.driver.switch_to_default_content()
            time.sleep(0.5)
            Logger.log("Switched Back to default Content")
        except Exception, exp:
            raise Exception('Unable To Switch To Default with Exception :{}'.format(exp))

    def isElementPresent(self, locator, locatorType="id"):
        try:
            element = self.getElement(locator, locatorType)
            if element is not None:
                Logger.log('Element Found With Locator :{}'.format(locator))
                return True
            else:
                Logger.log('Element Not Found With Locator :{}'.format(locator))
                return False
        except:
            Logger.log('Element Found With Locator :{}'.format(locator))
            return False

    def elementPresenceCheck(self, element):
        Logger.log('Checking Element Present For Locator :{}'.format(element))
        try:
            if len(element) > 0:
                Logger.log('Element Found With Locator :{}'.format(element))
                return True
            else:
                Logger.log('Element Not Found With Locator :{}'.format(element))
                return False
        except Exception, exp:
            Logger.log('Element Not Found: {} and Exception'.format(element, exp))
            return False

    def isVisible(self, element):
        Logger.log('Checking Element: {} is visible'.format(element))
        try:
            if element.is_displayed():
                Logger.log('Element :{} is visible'.format(element))
                return True
            else:
                Logger.log('Element :{} is not visible'.format(element, element))
                return False
        except Exception, exp:
            Logger.log('Element Not Found: {} and Exception: {}'.format(element, exp))
            return False

    def waitUntillElementFound(self, locator):
        WebDriverWait(self.driver, timeout=10, poll_frequency=5, ignored_exceptions=TimeoutException).until_not(EC.visibility_of_element_located((By.XPATH, locator)))

    def isInvisible(self, element):
        Logger.log('Checking Element: {} is visible'.format(element))
        try:
            if not element.is_displayed():
                Logger.log('Element :{} is invisible'.format(element))
                return True
            else:
                Logger.log('Element :{} is not invisible'.format(element, element))
                return False
        except Exception, exp:
            Logger.log('Element Not Found: {} and Exception: {}'.format(element, exp))
            return False
    
    def isClickable(self, element):
        Logger.log('Checking Element: {} isClickable'.format(element))
        try:
            if element.is_displayed() and element.is_enabled():
                Logger.log('Element :{} is Clickable'.format(element))
                return True
            else:
                Logger.log('Element :{} is not Clickable'.format(element))
                return False
        except Exception, exp:
            Logger.log('Element Not Found: {} and Exception: {}'.format(element, exp))
            return False

    def waitForElement(self, locator, locatorType="id", retry=5):
        Logger.log('Waiting for Locator:{}'.format(locator))
        try:
            elements = self.getElements(locator, locatorType)
            for numberOfChecks in range(retry):
                if self.elementPresenceCheck(elements) and self.isClickable(elements[0]):
                    Logger.log('Element with locator :{} appeared on the web page'.format(locator))
                    break
                else:
                    Logger.log('Element with Locator Type :{} not appeared yet but still checking'.format(locator))
        except Exception, exp:
            Logger.log('Element with locator :{} not appeared on the web page with Exception :{}'.format(locator, exp)) 

    def scrollWebPage(self):
        try: 
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        except Exception, exp:
            Logger.log('Exception while Tring to Scroll on Page , Exception :{}'.format(exp))
        
    def acceptAlert(self):
        try:
            WebDriverWait(self.driver, 10).until(EC.alert_is_present(), 'Timed out waiting for PA creation ' + 
                                                                        'confirmation popup to appear.')
            alert = self.driver.switch_to.alert    
            alert.accept()
        except TimeoutException, exp:
            Logger.log('TimeoutException , while Accepting Alert')
        except Exception, exp:
            Logger.log('Exception :{} , while switching to Alert'.format(exp))
            
    def implicitWaitOnReactPage(self):
        react_loader_xpath = "//span[@class='ant-spin-dot']"
        Logger.log('implicit react loader wait: ',  react_loader_xpath)
        WebDriverWait(self.driver, timeout=10, poll_frequency=5, ignored_exceptions=TimeoutException).until_not(EC.visibility_of_element_located((By.XPATH, react_loader_xpath)))
                
            
    def getScreenshot(self, message):
        fileName = message + ".png"
        screenshotLocation = "../screenshots/"
        relativeFileName = screenshotLocation + fileName
        currentLocation = os.path.dirname(__file__)
        destinationFileName = constant.config['logDir'] + '/' + fileName
        destinationLocation = constant.config['logDir'] + '/assets'
        
        try:
            if not os.path.exists(destinationLocation):
                os.makedirs(destinationLocation)
            self.driver.save_screenshot(destinationFileName)
            Logger.logCollectorRequest(destinationFileName, 'files')
            # Logger.log("Screenshot saved to directory " + destinationFileName)
        except:
            Logger.log(traceback.format_exc())

    def getBrowserErrorLogs(self, exp):
        expDict = {'exception': exp, 'Browser logs': []}
        browserLog = self.driver.get_log('browser')
        for bl in browserLog:
            if 'Failed to load resource' in bl['message']:
                expDict['Browser logs'].append(bl['message'])
        return expDict