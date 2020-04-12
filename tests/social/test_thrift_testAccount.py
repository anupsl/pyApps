import pytest, time, json, pytest_ordering, copy
from src.Constant.constant import constant
from src.utilities.logger import Logger
from src.modules.iris.construct import construct
from src.modules.social.socialObject import SocialObject
from src.modules.social.socialHelper import SocialHelper
from src.utilities.assertion import Assertion

@pytest.mark.run(order=2)
class Test_Social_Thrift_TestAccount():
    
    def setup_method(self, method):
        self.connObj = SocialHelper.getConnObj(newConnection=True)
        Logger.logMethodName(method.__name__)

    def test_socialThrift_testAccount_Sanity(self):
    	testAccountResponse = self.connObj.testAccount(
    		SocialObject().SocialChannel['facebook'],
    		constant.config['orgId'],
    		'requestId_automationthriftCall_{}'.format(int(time.time()*1000))
    		)
    	Assertion.constructAssertion(testAccountResponse, 'Response for TestAccount :{}'.format(testAccountResponse))