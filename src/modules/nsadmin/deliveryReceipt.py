import time, urllib, json
from src.Constant.constant import constant
from src.utilities.utils import Utils
from src.utilities.logger import Logger


class DeliveryReceipt(object):
    def __init__(self):
        self.dlrUrl = constant.config['dlrUrl']

    def solutionsinfini(self, data):
        url = self.dlrUrl + '/solutionsinfini?' + urllib.urlencode(data)
        Utils.makeRequest(url, '', '', 'GET')
        time.sleep(2)


    def sendgrid(self, data):
        url = self.dlrUrl + '/sendgrid'
        header = {'Content-Type': 'application/json'}
        Utils.makeRequest(url, json.dumps(data), header, 'POST')
        time.sleep(2)


    def testEndpoint(self, hostname):
        url = self.dlrUrl +'/'+hostname+'?'
        return Utils.makeRequest(url, '', '', 'GET')
