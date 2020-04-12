from src.utilities.randValues import randValues
from src.Constant.constant import constant
from src.utilities.utils import Utils
from datetime import datetime
import time


class Transaction():
    @staticmethod
    def Add(body={}, mobile=randValues.getRandomMobileNumber()):
        email = 'automail' + mobile + '@gmail.com'
        date = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        tmpDict = {
          "root": {
            "transaction": {
              "bill_client_id": "",
              "type": "regular",
              "number": 'AutomationTest' + str(int(time.time() * 100000)),
              "amount": "1000",
              "notes": "No line items",
              "gross_amount": "1000",
              "discount": "10",
              "customer": {
                "mobile": mobile,
                "email": email,
                "external_id": mobile,
                "firstname": ("autofn_" + mobile)[:20],
                "lastname": ("autoln_" + mobile)[:20],
                "type" : "loyalty",
              },
                "line_items": {
                    'line_item' : [{"attributes": {"attribute": {"name": "Shoes", "value": "Woodlands"}}, "serial": "83",
                                "amount": "382866", "description": "Levis", "item_code": "Levis", "qty": "100",
                                "rate": "5", "value": "500", "discount": "0", "notes": []},
                               {"attributes": {"attribute": {"name": "Shoes", "value": "Woodlands"}}, "serial": "83",
                                "amount": "382866", "description": "Levis", "item_code": "Levis", "qty": "100",
                                "rate": "5", "value": "500", "discount": "0", "notes": []}]
                }
            }
          }
        }
        if body == {}:
            body = tmpDict
        else:
            body = Utils.mergeDict(tmpDict, body)
        return {'body': body, 'endPoint' : constant.config['transactionAdd'], 'method' : 'POST',
                'mobile': mobile, 'email' : email,
                'transactionId' : body['root']['transaction']['number']}

