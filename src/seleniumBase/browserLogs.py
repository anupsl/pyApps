import time
from src.utilities.logger import Logger

class browserLogs():

    def threadBrowserLogs(self,driver):
        for entry in driver.get_log('browser'):
            if '500' in entry:
                Logger.log('Browser Log :'+ str(entry))