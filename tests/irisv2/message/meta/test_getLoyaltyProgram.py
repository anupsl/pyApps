import pytest

from src.Constant.constant import constant
from src.modules.irisv2.helper.irisHelper import IrisHelper
from src.modules.irisv2.message.getLoyaltyProgram import LoyaltyProgram
from src.modules.irisv2.message.loyaltyProgamDbAssertion import LoyaltyProgrameDbAssertion
from src.utilities.assertion import Assertion
from src.utilities.logger import Logger


@pytest.mark.run(order=47)
class Test_GetLoyaltyProgram():
    def setup_method(self, method):
        Logger.logMethodName(method.__name__)

    @pytest.mark.parametrize('description', [
        ('Valid org id')
    ])
    def test_irisV2_getLoyaltyProgram_Sanity(self, description):
        response = LoyaltyProgram.getLoyaltyProgram()
        LoyaltyProgram.assertResponse(response, 200)
        LoyaltyProgrameDbAssertion(response).validate()

    @pytest.mark.parametrize('description', [
        ('Invalid orgId')
    ])
    def test_irisV2_getLoyaltyProgram_InvalidOrgId(self, description):
        actualOrgId = constant.config['orgId']
        try:
            constant.config['orgId'] = 999999
            response = LoyaltyProgram.getLoyaltyProgram()
            LoyaltyProgram.assertResponse(response, 500, 101, ['Generic error: HTTP 401 Unauthorized'])
        finally:
            constant.config['orgId'] = actualOrgId

    @pytest.mark.parametrize('description', [
        ('Negative orgId')
    ])
    def test_irisV2_getLoyaltyProgram_NegativeOrgId(self, description):
        actualOrgId = constant.config['orgId']
        try:
            constant.config['orgId'] = -1111
            response = LoyaltyProgram.getLoyaltyProgram()
            LoyaltyProgram.assertResponse(response, 401, 999999, ['Invalid org id'])
        finally:
            constant.config['orgId'] = actualOrgId

    def test_irisV2_getLoyaltyProgram_WrongAuth(self):
        previousUserName = None
        try:
            previousUserName = IrisHelper.updateUserName('WrongName')
            response = LoyaltyProgram.getLoyaltyProgram()
            LoyaltyProgram.assertResponse(response, 401, 999999, 'Unauthorized')
        finally:
            if previousUserName is not None: IrisHelper.updateUserName(previousUserName)

    @pytest.mark.parametrize('description', [
        ('Org with no strategy')
    ])
    def test_irisV2_getLoyaltyProgram_WithEmptyStrategy(self, description):
        actualOrgId = constant.config['orgId']
        try:
            constant.config['orgId'] = constant.config['orgPointsDisable']
            response = LoyaltyProgram.getLoyaltyProgram()
            LoyaltyProgram.assertResponse(response, 200)
            Assertion.constructAssertion(len(response['json']['entity'][0]['strategy']['allocationStrategy']) == 0,
                                         'No Allocation Strategy is Expected')
            Assertion.constructAssertion(len(response['json']['entity'][0]['strategy']['expiryStrategy']) == 0,
                                         'No expiry Strategy is Expected')
        finally:
            constant.config['orgId'] = actualOrgId
