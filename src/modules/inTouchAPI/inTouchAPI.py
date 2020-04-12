import json
from src.utilities.utils import Utils
from src.Constant.constant import constant

class InTouchAPI(object):

    def __init__(self, params):
        self.params = params
        if 'tillUsername' in params:
            self.tillUsername = params['tillUsername']
            self.tillPassword = params['tillPassword']
            self.intouchUser = False
        elif 'tillUsername' in constant.config:
            self.tillUsername = constant.config['tillUsername']
            self.tillPassword = constant.config['tillPassword']
            self.intouchUser = False
        else:
            self.tillUsername = constant.config['intouchUsername']            
            self.tillPassword = constant.config['intouchPassword']
            self.intouchUser = True
        self.method = params['method']
        self.execute()

    def execute(self):
        self.getHeaders()
        self.getQueryParams()
        self.getBody()
        self.callAPI()

    def getHeaders(self):
        self.header = Utils.authorizationHeader(self.tillUsername, self.tillPassword)
        self.header.update({
            'Content-Type' : 'application/json',
            'Accept' : 'application/json'
        })
        if self.intouchUser:
            self.header.update({'X-CAP-API-AUTH-ORG-ID' : str(constant.config['orgId']),
                            'X-CAP-API-AUTH-KEY': 'ZWUwOWRkNTA4N2MxOGYzZTk4ZmIzOTYzZDEzNjA3NDI='})
        if 'header' in self.params:
            self.header.update(self.params['header'])

    def getQueryString(self):
        tempqueryparam = ''
        for paramkey, paramvalue in self.params['queryParams'].items():
            if isinstance(paramvalue, (list)):
                paramvalue = ','.join(paramvalue)
            tempqueryparam += '&' + str(paramkey) + '=' + unicode(paramvalue)
        #tempqueryparam = tempqueryparam[1:]  # to remove first &
        return tempqueryparam

    def getQueryParams(self):
        self.url = constant.config['intouchUrl'] + self.params['endPoint']
        if 'queryParams' in self.params:
            self.url += self.getQueryString()

    def getBody(self):
        if 'body' in self.params:
            self.body = self.params['body']
        else:
            self.body = ''

    def callAPI(self):
        output = Utils.makeRequest(self.url, self.body, self.header, self.method)
        self.response = json.loads(output.content)
        self.status_code = output.status_code

