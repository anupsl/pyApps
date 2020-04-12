import time
from src.Constant.constant import constant
from src.utilities.logger import Logger
from src.modules.darknight.darknightThrift import DarknightThrift
from src.modules.darknight.darknightHelper import DarknightHelper
from src.modules.inTouchAPI.customer import Customer
from src.modules.inTouchAPI.inTouchAPI import InTouchAPI
from src.modules.iris.list import campaignList
from src.utilities.assertion import Assertion

class Test_darknight():

    def setup_class(self):
        Logger.logSuiteName(str(self).split('.')[-1])


    def setup_method(self, method):
        self.dnObj = DarknightHelper.getConnObj(newConnection=True)
        Logger.logMethodName(str(method.__name__))

    def test_fetchEmailStatus_CustomerAddAPI_Sanity(self):
        cusObj = InTouchAPI(Customer.Add())
        for _ in range(0, 13):
            status = DarknightHelper.getEmailStatus(cusObj.params['email'])
            if status == 'INVALID':
                break
            else:
                time.sleep(10)
        Assertion.constructAssertion(status == 'INVALID',
            'Verifying email status after registering from customer/add '+cusObj.params['email'])

    def test_fetchEmailStatus_CampaignPasteList_Sanity(self):
        mergeListresponse, mergeListPayload, campaignId = campaignList.mergeList({}, campaignType=['LIVE', 'SKIP', 'List', 'TAGS', 0], userType='email', numberOfUsers=1, numberOfCustomTags=0)
        recipients = mergeListPayload['recipients']['data'][0]
        recipients = recipients.split(',')
        email = recipients[-1]
        for _ in range(0, 13):
            status = DarknightHelper.getEmailStatus(email)
            if status == 'INVALID':
                break
            else:
                time.sleep(10)
        Assertion.constructAssertion(status == 'INVALID',
            'Verifying email status from paste list upload in campaigns: '+email)      

    def test_getEmailStatus_Sanity(self):
        email = 'sriharsha.bk@capillarytech.com'
        resObj = self.dnObj.getEmailStatus([email])
        for _ in range(0, 5):
            status = resObj[0].emailStatusEnum
            if status == 0:
                break
            else:
                time.sleep(3)
        Assertion.constructAssertion(status == 0, 
            'Verifying existing email from getEmailStatus Thrift: '+email)
      
    def test_getEmailStatusCaseSensitive_Sanity(self):
        email = 'sriharshA.bk@capillarytech.com'
        resObj = self.dnObj.getEmailStatus([email])
        Assertion.constructAssertion(len(resObj) == 1, 'Verify response contains only 1 set')
        Assertion.constructAssertion(resObj[0].emailStatusEnum == 0, 
            'Verifying existing email from getEmailStatus Thrift: '+email)     



    def test_getMobileStatus_Sanity(self):
        mobile = '919980142461'
        resObj = self.dnObj.getMobileStatus([mobile], constant.config['orgId'])
        Assertion.constructAssertion(resObj == {mobile : True}, 
            'Verifying existing mobile from getMobileStatus Thrift: ')
