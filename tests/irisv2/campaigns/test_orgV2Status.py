import pytest
from src.Constant.constant import constant
from src.utilities.logger import Logger
from src.modules.irisv2.campaigns.orgV2Status import OrgV2Status
from src.utilities.assertion import Assertion


@pytest.mark.run(order=3)
class Test_orgV2Status():

    def setup_method(self, method):
        Logger.logMethodName(method.__name__)

    def test_irisV2_getOrgV2Status_Sanity(self):
        get = OrgV2Status.getOrgV2Status()
        OrgV2Status.assertResponse(get['RESPONSE'], 200)
        response = get['RESPONSE']['json']['entity']
        OrgV2Status.checktheStatus(response)


    def test_irisV2_getOrgOnboardingStatus_Sanity(self):
        get = OrgV2Status.getOnboardingStatus(str(constant.config['orgId']))
        OrgV2Status.assertResponse(get['RESPONSE'], 200)
        response = get['RESPONSE']['json']['entity']
        Assertion.constructAssertion(response == True,"The org can be onboarded")

    def test_irisV2_getOrgOnboarding_False_Channel(self):
        get = OrgV2Status.getOnboardingStatus(str(constant.config['notOnboard']['orgId']))
        OrgV2Status.assertResponse(get['RESPONSE'], 200)
        response = get['RESPONSE']['json']['entity']
        Assertion.constructAssertion(response == True, "The org be onboarded")
