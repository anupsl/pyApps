from src.modules.irisv2.helper.irisHelper import IrisHelper
from src.utilities.assertion import Assertion
from src.utilities.logger import Logger
from src.utilities.utils import Utils


class ProductCategory():
    @staticmethod
    def getLevelsForDimension(category):
        endpoint = IrisHelper.constructUrl('productcategory').replace('{category}', category)
        response = IrisHelper.constructResponse(
            Utils.makeRequest(url=endpoint, data='', auth=IrisHelper.constructAuthenticate(),
                              headers=IrisHelper.constructHeaders(), method='GET'))
        return response

    @staticmethod
    def getLevelValuesForDimension(urlSubstringForDimension, levelName):
        endpoint = IrisHelper.constructUrl('productlevel').replace('{urlSubstringForDimension}',
                                                                   urlSubstringForDimension).replace('{levelName}',
                                                                                                     levelName)
        response = IrisHelper.constructResponse(
            Utils.makeRequest(url=endpoint, data='', auth=IrisHelper.constructAuthenticate(),
                              headers=IrisHelper.constructHeaders(), method='GET'))
        return response

    @staticmethod
    def getLevelValuesUsingSearchText(urlSubstringForDimension, levelName, searchText):
        endpoint = IrisHelper.constructUrl('productsearch').replace('{urlSubstringForDimension}',
                                                                    urlSubstringForDimension).replace('{levelName}',
                                                                                                      levelName).replace(
            '{searchText}', searchText)
        response = IrisHelper.constructResponse(
            Utils.makeRequest(url=endpoint, data='', auth=IrisHelper.constructAuthenticate(),
                              headers=IrisHelper.constructHeaders(), method='GET'))
        return response

    @staticmethod
    def assertResponse(response, expectedStatusCode, expectedErrorCode=999999, expectedErrorMessage=''):
        if response['constructed'].lower() == 'pass':
            if expectedStatusCode >= 200 and expectedStatusCode <= 300:
                Assertion.constructAssertion(response['statusCode'] == int(expectedStatusCode),
                                             'Matching statusCode actual :{},expected :{}'.format(
                                                 response['statusCode'], expectedStatusCode))
            else:
                for errorReturned in response['json']['errors']:
                    Logger.log('Status Code :{} and error :{}', response['statusCode'], errorReturned)
                    Assertion.constructAssertion(response['statusCode'] == int(expectedStatusCode),
                                                 'Matching statusCode actual :{},expected :{}'.format(
                                                     response['statusCode'], expectedStatusCode))
                    Assertion.constructAssertion(errorReturned['code'] == expectedErrorCode,
                                                 'Matching Error Code ,actual:{} and expected:{}'.format(
                                                     errorReturned['code'], expectedErrorCode))
                    Assertion.constructAssertion(errorReturned['status'] == False, 'Checking for Error Status as False')
                    Assertion.constructAssertion(errorReturned['message'] in expectedErrorMessage,
                                                 'Matching Error Message ,actual:{} and expected :{}'.format(
                                                     errorReturned['message'], expectedErrorMessage))
        else:
            Assertion.constructAssertion(False, 'Constructed Body has Failed due to Exception so no Validation')

    @staticmethod
    def validateProductCategory(actualResult, expectedResult):
        expectedResult.sort()
        if 'levels' in actualResult['json']['entity']:
            actualResult['json']['entity']['levels'].sort()
            Assertion.constructAssertion(actualResult['json']['entity']['levels'] == expectedResult,
                                         'Actual Call Result :{} and constructed from Thrift :{}'.format(
                                             actualResult['json']['entity']['levels'], expectedResult))
        elif 'levelValues' in actualResult['json']['entity']:
            actualResult['json']['entity']['levelValues'].sort()
            Assertion.constructAssertion(actualResult['json']['entity']['levelValues'] == expectedResult,
                                         'Actual Call Result :{} and constructed from Thrift :{}'.format(
                                             actualResult['json']['entity']['levelValues'], expectedResult))
        else:
            raise Exception('Validation Failed : Entity in Json doesnt have levels/levelValues -> Response:{}'.format(
                actualResult['json']['entity']))

    @staticmethod
    def validateProductCategorySearch(actualResult, expectedResult):
        for eachKey in ['levelName', 'levelValues', 'searchText']:
            Assertion.constructAssertion(actualResult['json']['entity'][eachKey] == expectedResult[eachKey],
                                         'For Key :{} , actual Result :{} and expected :{}'.format(eachKey,
                                                                                                   actualResult['json'][
                                                                                                       'entity'][
                                                                                                       eachKey],
                                                                                                   expectedResult[
                                                                                                       eachKey]))
