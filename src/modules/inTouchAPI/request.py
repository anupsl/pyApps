from src.utilities.randValues import randValues
from src.Constant.constant import constant
from src.utilities.utils import Utils


class Request():

    @staticmethod
    def Add(body={}, mobileS='', emailS='', mobileT='', emailT=''):
        tmpDict = {
           'root': {
                'request': [{
                 'type': 'CHANGE_IDENTIFIER',
                 'base_type': 'MERGE',
                 'customer': {
                    'email': emailS,
                    'mobile': mobileS
                 },
                 'old_value': '',
                 'new_value': '',
                 'misc_info': {
                    'target_customer': {
                       'email': emailT,
                       'mobile': mobileT
                    }
                 }
              }]
           }
        }
        if body == {}: 
          body = tmpDict
        else:
          body = Utils.mergeDict(tmpDict, body)
        return {'body': body, 'endPoint' : constant.config['requestAdd'], 'method' : 'POST'}     


