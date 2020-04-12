import time
from src.Constant.constant import constant
from src.utilities.logger import Logger

class Assertion():

    @staticmethod
    def constructAssertion(assertCondition, assertMessage, verify=False):
        if not assertCondition:
            if not verify : 
                Logger.log('Assertion Failed : ', assertMessage)
                assert assertCondition, assertMessage
            else:
                Logger.log('Verification Failed : ', assertMessage)
                constant.config['validataionMessage'].append('Warning: ' + str('Verification Failed: {}'.format(assertMessage) ))
        else:
            Logger.log('Assertion Passed :', assertMessage)
            # constant.config['validataionMessage'].append('Assertion Passed :'+str(assertMessage))	

    @staticmethod
    def addValidationMessage(message):
        constant.config['validataionMessage'].append(str(message))
