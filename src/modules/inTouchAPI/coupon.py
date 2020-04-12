from src.utilities.randValues import randValues
from src.Constant.constant import constant
from src.utilities.utils import Utils

import time

class Coupon():

    @staticmethod
    def Redeem(body={}, mobile='', code=''):
        tmpDict = {
              'root': {
                'coupon': {
                     'customer': {
                        'mobile': mobile
                     },
                     'code': code,
                     'transaction': {
                        'amount': '100',
                        'number': 'AutomationTest' + str(int(time.time() * 100000))
                     }
                  }
               }
            }
        if body == {}: 
          body = tmpDict
        else:
          body = Utils.mergeDict(tmpDict, body)
        return {'body': body, 'endPoint' : constant.config['couponRedeem'], 'method' : 'POST'}     