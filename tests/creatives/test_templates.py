import pytest, time
from src.Constant.constant import constant
from src.utilities.logger import Logger
from src.utilities.assertion import Assertion

class Test_Templates():
    
    def setup_class(self):
        Logger.log('Setup Executed')
        pass
    
    def test_template_Sanity(self):
        Logger.log('Test Executed')
        Logger.log(constant.config)
        pass