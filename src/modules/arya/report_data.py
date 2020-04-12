from src.Constant.constant import constant
from src.utilities.logger import Logger
from src.modules.iris.construct import construct
from src.utilities.utils import Utils


class auth():
    
    @staticmethod
    def getreport():
        return ''

    @staticmethod
    def getHeaderArya():
        return {'content-type':'application/json','x-cap-api-auth-org-id':'50146','x-cap-remote-user':'15000449','x-cap-api-data-context-org-id':'50146','Authorization' : 'Bearer {}'.format(constant.config['token'])}
        
    @staticmethod
    def reportData():
        authLoginEndpointConstruct = construct.constructUrl('data', module='arya')

        payload = {"date": {"start": "2017-07-01","end": "2019-07-23","dateType": "custom"},"filters": {"dimensionFilterExpression": "","dimensionFilter": [{"key": "campaign.name",
"value": [
"campaign reminder org lvl"
],
"operation": "includes"
}]
}
}
        response = Utils.makeRequest(url=authLoginEndpointConstruct, data=payload, auth='', headers=auth.getHeaderArya(), method='POST')
        return construct.constructResponse(response)
