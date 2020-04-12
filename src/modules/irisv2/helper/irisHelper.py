from src.Constant.constant import constant
from src.modules.nsadmin.nsadminHelper import NSAdminHelper
from src.modules.nsadmin.nsadminObject import NSAdminObject
from src.utilities.logger import Logger
from src.utilities.assertion import Assertion
import time
from src.utilities.dbhelper import dbHelper

class IrisHelper():
    @staticmethod
    def constructUrl(endpointName, queryParam=[]):
        endpoint = constant.endpointsIrisV2[endpointName.lower()]
        clusterUrl = constant.config['url']

        if len(queryParam) > 0:
            endpoint = endpoint + '?'
            for eachParam in queryParam:
                endpoint = endpoint + eachParam[0] + '=' + str(eachParam[1]) + '&'

        return str(clusterUrl) + str(endpoint)

    @staticmethod
    def constructAuthenticate():
        return (constant.config['intouchUsername'], constant.config['intouchPassword'])

    @staticmethod
    def constructHeaders(contentType=True):
        header = {
            'accept': 'application/json',
            'X-CAP-ORG': str(constant.config['orgId'])
        }
        if contentType: header['content-type'] = 'application/json'
        if 'aryaCookiesDict' in constant.config: header.update(
            {'X-CAP-CT': str(constant.config['aryaCookiesDict']['CT'])})
        return header

    @staticmethod
    def constructHeadersPatch(contentType=True):
        header = {
            'accept': 'application/json',
            'X-CAP-ORG': str(constant.config['orgId'])
        }
        if contentType: header['content-type'] = 'application/merge-patch+json'
        if 'aryaCookiesDict' in constant.config: header.update(
            {'X-CAP-CT': str(constant.config['aryaCookiesDict']['CT'])})
        return header

    @staticmethod
    def constructResponse(response):
        responseBody = None
        try:
            responseBody = {'constructed': 'pass', 'statusCode': response.status_code,
                            'X-CAP-REQUEST-ID': response.headers['X-CAP-REQUEST-ID'], 'encoding': response.encoding,
                            'text': response.text, 'json': response.json(), 'cookies': response.cookies}
        except Exception, exp:
            Logger.log('Exception Occured While Constructing Response :' + str(exp))
            responseBody = {'constructed': 'fail', 'statusCode': response.status_code, 'text': response.text}
        finally:
            Logger.log('Response body Constructed :', responseBody)
            return responseBody

    @staticmethod
    def updateOrgId(orgId):
        workingOrgId = constant.config['orgId']
        constant.config.update({'orgId': orgId})
        dbHelper.buildDBToTunnelPortMapping()
        return workingOrgId

    @staticmethod
    def updateOrgName(orgName):
        workingOrgId = constant.config['orgName']
        constant.config.update({'orgName': orgName})
        return workingOrgId

    @staticmethod
    def updateUserName(userName):
        workingUserName = constant.config['intouchUsername']
        constant.config.update({'intouchUsername': userName})
        return workingUserName

    @staticmethod
    def updatepassword(password):
        workingUserName = constant.config['intouchPassword']
        constant.config.update({'intouchPassword': password})
        return workingUserName

    @staticmethod
    def updateCredit(credit=0,channel='EMAIL'):
        try:
            nsObj = NSAdminHelper.getMasterConnObj() if constant.config['cluster'] in ['nightly','staging','china'] else NSAdminHelper.getConnObj(newConnection=True)
            messageClass = 1 if channel == 'EMAIL' else 0
            creditDetails1 = {
                "orgId": int(constant.config['orgId']),
                "bulkCredits": int(credit),
                'messageClass': messageClass
            }
            creditDetails1 = NSAdminObject.OrgCreditDetails(creditDetails1)
            if credit == 0:
                currVal = nsObj.getCreditDetailsByOrgAndChannel(constant.config['orgId'], messageClass, 'test_{}'.format(int(time.time())))
                currVal = int(currVal.bulkCredits) * -1
                creditDetails1.bulkCredits = currVal
            nsObj.addCredits(creditDetails1)
        except Exception,exp:
            raise Exception('NotAbleToUpdateCreditTo:{}'.format(credit))
            Logger.log(exp)
        finally:
            if IrisHelper.logCurrentCredit(messageClass) != credit:
                Assertion.addValidationMessage('Credit Not Set as Expected')


    @staticmethod
    def logCurrentCredit(messageClass):
        nsObj = NSAdminHelper.getConnObj(newConnection=True)
        currVal = nsObj.getCreditDetailsByOrgAndChannel(constant.config['orgId'], messageClass,
                                                        'test_{}'.format(int(time.time())))
        Logger.log('Current Credit :{}'.format(currVal.bulkCredits))
        return int(currVal.bulkCredits)

    @staticmethod
    def getDomainGatewayMapId(messageClass='SMS'):
        nsObj = NSAdminHelper.getConnObj(newConnection=True)
        domainGateway = nsObj.getDomainPropertiesGatewayMapByOrg(int(constant.config['orgId']),
                                                                 NSAdminObject.MessageClass[messageClass])[0]
        domainMap = {
            'mapId': domainGateway.id
        }
        if messageClass == 'SMS':
            for eachContactInfo in domainGateway.domainProperties.contactInfo:
                if eachContactInfo.type == 'cdma_sender_id': domainMap.update({'cdma_sender_id': eachContactInfo.value})
                if eachContactInfo.type == 'gsm_sender_id': domainMap.update({'gsm_sender_id': eachContactInfo.value})
        elif messageClass == 'EMAIL':
            for eachContactInfo in domainGateway.domainProperties.contactInfo:
                if eachContactInfo.type == 'reply_to_id': domainMap.update({'reply_to_id': eachContactInfo.value})
                if eachContactInfo.type == 'sender_id': domainMap.update({'sender_id': eachContactInfo.value})
        else:
            raise Exception('OtherChannelsNotSupportedForDomainMapping')

        return domainMap

    @staticmethod
    def disableDomainGatewayMapId(channel):
        messageClass = 'SMS' if channel.lower() in ['mobile','sms'] else channel
        nsObj = NSAdminHelper.getConnObj(newConnection=True)
        nsadminHelper = NSAdminHelper(constant.config['orgId'], messageClass)
        nsadminHelper.disableDomainPropertiesGatewayMap()

    @staticmethod
    def createNewDummyGateway(channel):
        messageClass = 'SMS' if channel.lower() in ['mobile', 'sms'] else channel
        nsObj = NSAdminHelper.getConnObj(newConnection=True)
        nsadminHelper = NSAdminHelper(constant.config['orgId'], messageClass)
        for eachType in [('HIGH', 'localmail_HIGH_{}'.format(int(time.time())),["capillary", "otp"]),('BULK', 'localmail_BULK_{}'.format(int(time.time())),["capillary", "campaigns"])]:
            try:
                nsadminHelper.configureGateway(eachType[0], eachType[1] + '_2', False, eachType[2])
            except Exception,exp:
                Logger.log('Exception While Creating Dummy Gateway :{}'.format(exp))
        return True