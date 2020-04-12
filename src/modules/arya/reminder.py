from src.Constant.constant import constant
from src.modules.iris.construct import construct
from src.utilities.utils import Utils


class NFSReminder():
    @staticmethod
    def genHeaderArya():
        return {
            'Content-Type': 'application/json',
            'x-cap-remote-user': str(15000449),
            'x-cap-api-data-context-org-id': str(constant.config['orgId']),
            'X-CAP-API-AUTH-ORG-ID': str(constant.config['orgId']),
            'Authorization': 'Bearer {}'.format(constant.config['token'])
        }

    @staticmethod
    def constructPayloadReminder(msgId, mode, name, namev2, invert,intersection=False,series_id=None):
        result = {
            "mode": mode,
            "type":"FILTER_BASED",
            "targetBlocks": [{
                "filters": [{
                    "name": name,
                    "msg_id": msgId,
                    "operator": "GREATER_THAN",
                    "value": 0
                }]
            }]
        }
        if intersection :
            if namev2 == 'transaction':
                result['targetBlocks'][0]['filters'].append({
                    "name": namev2,
                    "minDate": "2019-08-06",
                    "maxDate": "2020-02-17",
                    "operator": "GREATER_THAN",
                    "value": 0,
                    "invert": invert
                })
            elif namev2 == 'couponRedeemed':
                result['targetBlocks'][0]['filters'].append({
                    "name": namev2,
                    "minDate": 1532349250000,
                    "maxDate": 1753274050000,
                    "operator": "GREATER_THAN",
                    "value": 0,
                    "invert": invert,
                    "series_id": series_id
                })
        return result


    @staticmethod
    def reminder(msgId, mode='INTERACTIVE', name='contactedCustomerV2', namev2='transaction',
                 invert=True,intersection=False,series_id=None):
        authLoginEndpointConstruct = construct.constructUrl('remindernfs', module='arya')
        response = Utils.makeRequest(url=authLoginEndpointConstruct,
                                     data=NFSReminder.constructPayloadReminder(msgId, mode, name, namev2, invert,intersection=intersection,series_id=series_id),
                                     auth='',
                                     headers=NFSReminder.genHeaderArya(), method='POST')
        return construct.constructResponse(response)
