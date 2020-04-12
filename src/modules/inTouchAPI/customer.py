from src.utilities.randValues import randValues
from src.Constant.constant import constant
from src.utilities.utils import Utils
from datetime import datetime
import time

class Customer():

    @staticmethod
    def Get(identifier):
        return {'queryParams' : identifier, 'endPoint' : constant.config['customerGet'],
                'method' : 'GET'}

    @staticmethod
    def Add(body={}, mobile=randValues.getRandomMobileNumber()):
        email = 'automail' + mobile + '@gmail.com'
        date = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        tmpDict = {
            'root': {
                'customer': {
                    'mobile': mobile,
                    'email': email,
                    'external_id': mobile,
                    'firstname': ("autofn_" + mobile)[:20],
                    'lastname': ("autoln_" + mobile)[:20],
                    'gender': 'M',
                    'registered_on': date
                }
            }
        }
        if body == {}: 
          body = tmpDict
        else:
          body = Utils.mergeDict(tmpDict, body)
        return {'body': body, 'endPoint' : constant.config['customerAdd'], 'method' : 'POST',
                'mobile': mobile, 'email' : email}
        
    @staticmethod
    def unsubscribe(body={}):
        tmpDict = {
                'root': {
                    'subscription': {
                         'comment': 'AutomationTest',
                         'is_subscribed': '0',
                         'priority': 'BULK',
                         'scope': 'ALL',
                         'mobile': '',
                         'channel': 'SMS'
                    }
                }
            }
        if body == {}:
            body = tmpDict
        else:
            body = Utils.mergeDict(tmpDict, body)
        return {'body': body, 'endPoint' : constant.config['customerSubscriptions'], 'method' : 'POST'}
            

