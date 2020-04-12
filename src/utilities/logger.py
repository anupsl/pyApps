import logging, inspect, thread, os, json, requests
from datetime import datetime
from src.Constant.constant import constant

class Logger():

    @staticmethod
    def configureLogging(logDir):
        logger = logging.getLogger("debugLog")
        logger.setLevel(logging.DEBUG)
        filePath = constant.logDirectory + "/debug.log"
        formatter = logging.Formatter("%(asctime)s - %(message).6000s", "%Y-%m-%d %H:%M:%S")  # Format for our loglines
        fh = logging.FileHandler(filePath)
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        filePath = logDir +'/debug.log'
        fh = logging.FileHandler(filePath)
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        logger.addHandler(fh)        
        return logger

    @staticmethod
    def log(*message):
        stackTrace = inspect.stack()[1]  # to log the module name along with the message
        moduleName = stackTrace[3]
        if moduleName == 'log':
            stackTrace = inspect.stack()[2]
            moduleName = stackTrace[3]
        lineNo = str(stackTrace[2])
        codeFile = inspect.getmodule(stackTrace[0])
        codeFile = codeFile.__name__
        logger = logging.getLogger('debugLog')
        message = list(message)
        l = len(message)
        for i in range(0, l):
            if isinstance(message[i], unicode):
                message[i] = message[i].encode("utf8")
        thId = thread.get_ident()
        tmpMsg = str(thId) + ':' + codeFile + ':' + moduleName + ':' + lineNo + ' - ' + ''.join(map(str, message))       
        logger.debug(tmpMsg)
        tmpMsg = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))+' - '+tmpMsg
        Logger.logCollectorRequest(tmpMsg, 'log')

    @staticmethod
    def logCollectorRequest(message, logType):
        if constant.config['collectOnly']:
            return
        url = constant.logCollectorUrl
        runId = constant.config['runId']
        data = json.dumps({logType : {runId : message}})
        try:
            requests.post(url, data=data, verify=False, timeout=10)
        except requests.exceptions.ConnectionError:
            if constant.config['logCollectorConnErr'] % 30 == 0:
                logger = logging.getLogger('debugLog')
                logger.debug('----- Connection Error with log collector ------\n')                
            constant.config['logCollectorConnErr'] += 1
        except Exception as e:
            logger = logging.getLogger('debugLog')
            logger.debug(str(e))

    @staticmethod
    def logMethodName(methodName):
        Logger.log('\n\n\t\t\t\t######### Executing test: ', methodName,' ##########\n')
        constant.config['validataionMessage'] = []

    @staticmethod
    def logSuiteName(suiteName):
        Logger.log('\n\n\t\t\t\t ****** Executing suite: ', suiteName, ' *******\n')

