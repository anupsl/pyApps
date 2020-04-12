import time,pytest, random
from src.Constant.constant import constant
from src.modules.luci.luciDBHelper import LuciDBHelper
from src.utilities.logger import Logger
from src.utilities.assertion import Assertion
from src.utilities.utils import Utils
from src.modules.luci.luciHelper import LuciHelper
from src.modules.luci.luciObject import LuciObject

class Test_ResendCoupon():

    def setup_class(self):
        Logger.logSuiteName(str(self).split('.')[-1])
        self.connObj = LuciHelper.getConnObj()
        self.constructObj = LuciObject()
        self.userId = constant.config['usersInfo'][0]['userId']
        self.tillId = constant.config['tillIds'][0]
        self.storeId = constant.config['storeIds'][0]
        self.billId = Utils.getTime(milliSeconds=True)

    def setup_method(self, method):
        self.connObj = LuciHelper.getConnObj(newConnection=True)
        Logger.logMethodName(method.__name__)
        constant.config['requestId'] = 'luci_auto_'+str(random.randint(11111, 99999))

    @pytest.mark.parametrize('description, smsTemplate', [('ResendCoupon_Invalid', 'Resend coupon {{voucher}},{{valid_days_from_create}},{{valid_till_date.FORMAT_1}},{{valid_till_date.FORMAT_2}},{{valid_till_date.FORMAT_3}},{{valid_till_date.FORMAT_4}}optout : {{optout}}'),
      ('ResendCoupon_Optout', 'Resending coupons {{voucher_code}} {{optout}}'),
      ('ResendCoupon_CustName', 'Resending coupons {{voucher}} {{cust_name}} {{optout}}'),
      ('ResendCoupon_Firstname', 'Resending coupons {{voucher}} {{firstname}}')])
    def test_LUCI_RSC_Invalid_001(self,description,smsTemplate):
        try:
            couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self,{'sms_template' : smsTemplate})
            LuciHelper.queuePumpWait(self,couponSeriesId)
            # Issue Coupon Code
            couponCode = LuciHelper.issueCouponAndAssertions(self, couponSeriesId)[0]
            resendRequest = LuciObject.resendCouponRequest(
                {'storeUnitId': self.tillId, 'eventTimeInMillis': Utils.getTime(milliSeconds=True),
                 'couponCode': couponCode, 'userId': self.userId})
            couponDetails = self.connObj.resendCoupon(resendRequest).__dict__
            Assertion.constructAssertion(couponCode == couponDetails['couponCode'], 'Resend Coupon Code Actual: {} and Expected: {}'.format(couponCode, couponDetails['couponCode']))
            Assertion.constructAssertion(couponDetails['ex'] == None, 'Resend Coupon No exception occurred : {}'.format(couponDetails['ex']))
        except Exception, luciException:
            luciException = luciException.__dict__
            Assertion.constructAssertion(luciException['errorCode'] == 644, 'Redemption error Code Actual : {} and Expected: {}'.format(luciException['errorCode'], 644))
            Assertion.constructAssertion(luciException['errorMsg'] == 'unresolved tags are present', 'Redemption error Message Actual : {} and Expected: {}'.format(luciException['errorMsg'], 'unresolved tags are present'))

    @pytest.mark.parametrize('description, config',[
        ('ResendCoupon valid resendMessageEnabled not set', {'sms_template' : 'Resending coupons to First Name: {{fullname}},and custName: {{cust_name}}  Hello {{first_name}} {{last_name}}, your Code : {{voucher}}, expired at: {{valid_till_date.FORMAT_1}} & valid days from create: {{valid_days_from_create}} '})
    ])
    def test_LUCI_RSC_002(self,description, config):
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self,config)
        LuciHelper.queuePumpWait(self,couponSeriesId)
        # Issue Coupon Code
        couponCode = LuciHelper.issueCouponAndAssertions(self, couponSeriesId)[0]
        resendRequest = LuciObject.resendCouponRequest(
            {'storeUnitId': self.tillId, 'eventTimeInMillis': Utils.getTime(milliSeconds=True),
             'couponCode': couponCode, 'userId': self.userId})
        couponDetails = self.connObj.resendCoupon(resendRequest).__dict__
        Assertion.constructAssertion(couponCode == couponDetails['couponCode'], 'Resend Coupon Code Actual: {} and Expected: {}'.format(couponCode, couponDetails['couponCode']))
        Assertion.constructAssertion(couponDetails['ex'] == None, 'Resend Coupon No exception occurred : {}'.format(couponDetails['ex']))

    @pytest.mark.parametrize('description, config', [
        ('ResendCoupon valid', {'sms_template': 'Resending coupons to First Name: {{fullname}},and custName: {{cust_name}}  Hello {{first_name}} {{last_name}}, your Code : {{voucher}}, expired at: {{valid_till_date.FORMAT_1}} & valid days from create: {{valid_days_from_create}} ', 'resendMessageEnabled': True})
    ])
    def test_LUCI_RSC_003_sanity(self, description, config):
        couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self, config)
        LuciHelper.queuePumpWait(self, couponSeriesId)
        # Issue Coupon Code
        couponCode = LuciHelper.issueCouponAndAssertions(self, couponSeriesId)[0]
        resendRequest = LuciObject.resendCouponRequest({'storeUnitId': self.tillId, 'eventTimeInMillis': Utils.getTime(milliSeconds=True), 'couponCode': couponCode, 'userId': self.userId})
        couponDetails = self.connObj.resendCoupon(resendRequest).__dict__
        Assertion.constructAssertion(couponCode == couponDetails['couponCode'], 'Resend Coupon Code Actual: {} and Expected: {}'.format(couponCode, couponDetails['couponCode']))
        Assertion.constructAssertion(couponDetails['ex'] == None, 'Resend Coupon No exception occurred : {}'.format(couponDetails['ex']))

    @pytest.mark.parametrize('description, config',[
    ('ResendCoupon valid resendMessageEnabled False', {'sms_template' : 'Resending coupons to First Name: {{fullname}},and custName: {{cust_name}}  Hello {{first_name}} {{last_name}}, your Code : {{voucher}}, expired at: {{valid_till_date.FORMAT_1}} & valid days from create: {{valid_days_from_create}} ', 'resendMessageEnabled' : False})
    ])
    def test_LUCI_RSC_004(self,description, config):
        expectedMsg = 'resend message not enabled for series id : {}'
        try:
            couponConfigObj, couponSeriesId = LuciHelper.saveCouponConfigAndAssertions(self, config)
            expectedMsg = expectedMsg.format(couponSeriesId)
            LuciHelper.queuePumpWait(self, couponSeriesId)
            # Issue Coupon Code
            couponCode = LuciHelper.issueCouponAndAssertions(self, couponSeriesId)[0]
            resendRequest = LuciObject.resendCouponRequest(
                {'storeUnitId': self.tillId, 'eventTimeInMillis': Utils.getTime(milliSeconds=True),
                 'couponCode': couponCode, 'userId': self.userId})
            couponDetails = self.connObj.resendCoupon(resendRequest).__dict__
            Assertion.constructAssertion(couponCode == couponDetails['couponCode'], 'Resend Coupon Code Actual: {} and Expected: {}'.format(couponCode, couponDetails['couponCode']))
            Assertion.constructAssertion(couponDetails['ex'] == None, 'Resend Coupon No exception occurred : {}'.format(couponDetails['ex']))
        except Exception, luciExp:
            luciExp = luciExp.__dict__
            Assertion.constructAssertion(luciExp['errorCode'] == 653, 'Resend error Code Actual : {} and Expected: {}'.format(luciExp['errorCode'], 653))
            Assertion.constructAssertion(luciExp['errorMsg'] == expectedMsg, 'Resend error Message Actual : {} and Expected: {}'.format(luciExp['errorMsg'], expectedMsg))