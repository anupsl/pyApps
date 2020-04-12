import pytest, pytest_ordering
from src.Constant.constant import constant
from src.utilities.logger import Logger
from src.utilities.assertion import Assertion
from src.modules.irisv2.message.getPoc import Poc
from src.modules.irisv2.helper.irisHelper import IrisHelper
from src.modules.irisv2.message.pocDbAssertion import PocDbAssertion

@pytest.mark.run(order=48)
class Test_GetPoc():

    def setup_method(self, method):
        Logger.logMethodName(method.__name__)

    @pytest.mark.parametrize('description', [
        ('Valid org id')
    ])
    def test_irisV2_getPoc_Sanity(self, description):
        response = Poc.getPoc()
        Poc.assertResponse(response, 200)
        PocDbAssertion(response).validate()

    @pytest.mark.parametrize('description', [
        ('Invalid orgId')
    ])
    def test_irisV2_getPoc_InvalidOrgId(self, description):
        actualOrgId = constant.config['orgId']
        try:
            constant.config['orgId'] = 999999
            response = Poc.getPoc()
            Poc.assertResponse(response, 500, 101, ['Generic error: HTTP 401 Unauthorized'])
        finally:
            constant.config['orgId'] = actualOrgId

    @pytest.mark.parametrize('description', [
        ('Negative orgId')
    ])
    def test_irisV2_getPoc_NegativeOrgId(self, description):
        actualOrgId = constant.config['orgId']
        try:
            constant.config['orgId'] = -1111
            response = Poc.getPoc()
            Poc.assertResponse(response, 401, 999999, ['Invalid org id'])
        finally:
            constant.config['orgId'] = actualOrgId

    def test_irisV2_getPoc_WrongAuth(self):
        previousUserName = None
        try:
            previousUserName = IrisHelper.updateUserName('WrongName')
            response = Poc.getPoc()
            Poc.assertResponse(response, 401, 999999, 'Unauthorized')
        finally:
            if previousUserName is not None: IrisHelper.updateUserName(previousUserName)


