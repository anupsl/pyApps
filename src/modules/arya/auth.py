from src.Constant.constant import constant
from src.modules.iris.construct import construct
from src.utilities.utils import Utils


class auth():
    
    @staticmethod
    def genAuthenticationArya():
        return ''

    @staticmethod
    def genHeaderArya():
        return {'accept':'application/json', 'content-type':'application/json'}
        
    @staticmethod
    def authLogin():
        authLoginEndpointConstruct = construct.constructUrl('authlogin', module='arya')
        payload = {'username':constant.config['intouchUsername'], 'password':constant.config['intouchPassword']}
        response = Utils.makeRequest(url=authLoginEndpointConstruct, data=payload, auth='', headers=auth.genHeaderArya(), method='POST')
        return construct.constructResponse(response)
