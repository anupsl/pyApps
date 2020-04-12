import pytest

from src.Constant.constant import constant
from src.modules.irisv2.helper.irisHelper import IrisHelper
from src.modules.irisv2.message.productCategory import ProductCategory
from src.modules.reon.reonHelper import ReonHelper
from src.utilities.logger import Logger


class Test_ProductCategory():
    def setup_class(self):
        self.actualOrgId = IrisHelper.updateOrgId(constant.config['reon']['orgId'])
        self.actualOrgName = IrisHelper.updateOrgName(constant.config['reon']['orgName'])

    def setup_method(self, method):
        self.connObj = ReonHelper.getConnObj(newConnection=True)
        Logger.logMethodName(method.__name__)

    @pytest.mark.parametrize('apiCategory,thriftCategory', [
        ('productCategory', 'item'),
        ('storeHierarchy', 'event_zone_till')
    ])
    def test_productCategory_getSanity(self, apiCategory, thriftCategory):
        actualResult = ProductCategory.getLevelsForDimension(apiCategory)
        ProductCategory.assertResponse(actualResult, 200)
        expectedResult = ReonHelper.getLevelsForDimension(thriftCategory)
        ProductCategory.validateProductCategory(actualResult, expectedResult)

    @pytest.mark.parametrize('apiCategory,levelName,thriftCategory', [
        ('productCategory', 'category', 'item'),
        ('productCategory', 'item_code', 'item'),
        ('productCategory', 'parent_category', 'item'),
        ('storeHierarchy', 'till', 'event_zone_till'),
        ('storeHierarchy', 'store', 'event_zone_till'),
        ('storeHierarchy', 'zn_zone', 'event_zone_till')
    ])
    def test_productCategory_values_getSanity(self, apiCategory, levelName, thriftCategory):
        actualResult = ProductCategory.getLevelValuesForDimension(apiCategory, levelName)
        ProductCategory.assertResponse(actualResult, 200)
        expectedResult = ReonHelper.getLevelValuesForDimension(thriftCategory, levelName)
        ProductCategory.validateProductCategory(actualResult, expectedResult)

    @pytest.mark.parametrize('apiCategory,levelName,searchText,thriftCategory', [
        ('productCategory', 'item_code', 'item','item'),
        ('productCategory', 'parent_category','item','item'),
        ('productCategory', 'parent_category', 'Beer', 'item'),
        ('storeHierarchy', 'till','north', 'event_zone_till'),
        ('storeHierarchy', 'store','south', 'event_zone_till'),
        ('storeHierarchy', 'zn_zone', 'north','event_zone_till')
    ])
    def test_productCategory_value_search_getSanity(self, apiCategory, levelName,searchText,thriftCategory):
        actualResult = ProductCategory.getLevelValuesUsingSearchText(apiCategory,levelName,searchText)
        ProductCategory.assertResponse(actualResult, 200)
        expectedResult = ReonHelper.getLevelValuesUsingSearchText(thriftCategory, levelName,searchText)
        ProductCategory.validateProductCategorySearch(actualResult, expectedResult)

    @pytest.mark.parametrize('apiCategory', [
        ('Category'),
    ])
    def test_productCategory_noSuchCategory(self, apiCategory):
        actualResult = ProductCategory.getLevelsForDimension(apiCategory)
        ProductCategory.assertResponse(actualResult, 400, expectedErrorCode=5003,
                                       expectedErrorMessage='Campaign Meta Exception: Invalid dimension Category passed')

    @pytest.mark.parametrize('apiCategory', [
        ('productCategory'),
    ])
    def test_productCategory_orgNotSynced(self, apiCategory):
        try:
            IrisHelper.updateOrgId(constant.config['reonNotSynced']['orgId'])
            actualResult = ProductCategory.getLevelsForDimension(apiCategory)
            ProductCategory.assertResponse(actualResult, 400, expectedErrorCode=101,
                                           expectedErrorMessage='Generic error: Could not fetch levels.')
        finally:
            IrisHelper.updateOrgId(self.actualOrgId)

    @pytest.mark.parametrize('apiCategory', [
        ('productCategory'),
    ])
    def test_productCategory_unknownOrg(self, apiCategory):
        try:
            IrisHelper.updateOrgId(-1)
            actualResult = ProductCategory.getLevelsForDimension(apiCategory)
            ProductCategory.assertResponse(actualResult, 401, expectedErrorCode=999999,
                                           expectedErrorMessage='Invalid org id')
        finally:
            IrisHelper.updateOrgId(self.actualOrgId)

    @pytest.mark.parametrize('apiCategory', [
        ('productCategory'),
    ])
    def test_productCategory_wrongUserName(self, apiCategory):
        try:
            actualUserName = IrisHelper.updateUserName('ztyv')
            actualResult = ProductCategory.getLevelsForDimension(apiCategory)
            ProductCategory.assertResponse(actualResult, 401, expectedErrorCode=999999,
                                           expectedErrorMessage='Unauthorized')
        finally:
            IrisHelper.updateUserName(actualUserName)

    @pytest.mark.parametrize('apiCategory', [
        ('productCategory'),
    ])
    def test_productCategory_wrongPassword(self, apiCategory):
        try:
            actualPassword = IrisHelper.updatepassword(555)
            actualResult = ProductCategory.getLevelsForDimension(apiCategory)
            ProductCategory.assertResponse(actualResult, 401, expectedErrorCode=999999,
                                           expectedErrorMessage='Unauthorized')
        finally:
            IrisHelper.updatepassword(actualPassword)

    @pytest.mark.parametrize('apiCategory,levelName', [
        ('test', 'category'),
    ])
    def test_productCategory_values_noSuchCategory(self, apiCategory, levelName):
        actualResult = ProductCategory.getLevelValuesForDimension(apiCategory, levelName)
        ProductCategory.assertResponse(actualResult, 400, expectedErrorCode=5003,
                                       expectedErrorMessage='Campaign Meta Exception: Invalid dimension test passed')

    @pytest.mark.parametrize('apiCategory,levelName', [
        ('productCategory', 'test'),
    ])
    def test_productCategory_values_noSuchLevel(self, apiCategory, levelName):
        actualResult = ProductCategory.getLevelValuesForDimension(apiCategory, levelName)
        ProductCategory.assertResponse(actualResult, 400, expectedErrorCode=101,
                                       expectedErrorMessage='Generic error: Could not fetch attribute values.'
                                           )

    @pytest.mark.parametrize('apiCategory,levelName', [
        ('productCategory', 'category'),
    ])
    def test_productCategory_values_orgNotYetSynced(self, apiCategory, levelName):
        try:
            IrisHelper.updateOrgId(constant.config['reonNotSynced']['orgId'])
            actualResult = ProductCategory.getLevelValuesForDimension(apiCategory, levelName)
            ProductCategory.assertResponse(actualResult, 400, expectedErrorCode=101,
                                           expectedErrorMessage='Generic error: Could not fetch attribute values.')
        finally:
            IrisHelper.updateOrgId(self.actualOrgId)

    @pytest.mark.parametrize('apiCategory,levelName', [
        ('productCategory', 'category'),
    ])
    def test_productCategory_values_unknownOrg(self, apiCategory, levelName):
        try:
            IrisHelper.updateOrgId(-1)
            actualResult = ProductCategory.getLevelValuesForDimension(apiCategory, levelName)
            ProductCategory.assertResponse(actualResult, 401, expectedErrorCode=999999,
                                           expectedErrorMessage='Invalid org id')
        finally:
            IrisHelper.updateOrgId(self.actualOrgId)

    @pytest.mark.parametrize('apiCategory,levelName', [
        ('productCategory', 'category'),
    ])
    def test_productCategory_values_wrongUserName(self, apiCategory, levelName):
        try:
            actualuserName = IrisHelper.updateUserName('ztvf')
            actualResult = ProductCategory.getLevelValuesForDimension(apiCategory, levelName)
            ProductCategory.assertResponse(actualResult, 401, expectedErrorCode=999999,
                                           expectedErrorMessage='Unauthorized')
        finally:
            IrisHelper.updateUserName(actualuserName)

    @pytest.mark.parametrize('apiCategory,levelName', [
        ('productCategory', 'category'),
    ])
    def test_productCategory_values_wrongPassword(self, apiCategory, levelName):
        try:
            actualPassword = IrisHelper.updatepassword(678)
            actualResult = ProductCategory.getLevelValuesForDimension(apiCategory, levelName)
            ProductCategory.assertResponse(actualResult, 401, expectedErrorCode=999999,
                                           expectedErrorMessage='Unauthorized')
        finally:
            IrisHelper.updatepassword(actualPassword)

    @pytest.mark.parametrize('apiCategory,levelName,searchText', [
        ('item', 'item_code', 'item')
    ])
    def test_productCategory_value_search_noSuchDimName(self, apiCategory, levelName, searchText):
        actualResult = ProductCategory.getLevelValuesUsingSearchText(apiCategory, levelName, searchText)
        ProductCategory.assertResponse(actualResult, 400,expectedErrorCode=5003,expectedErrorMessage='Campaign Meta Exception: Invalid dimension item passed')

    @pytest.mark.parametrize('apiCategory,levelName,searchText', [
        ('productCategory', 'test', 'item')
    ])
    def test_productCategory_values_search_noSuchLevel(self, apiCategory, levelName, searchText):
        actualResult = ProductCategory.getLevelValuesUsingSearchText(apiCategory, levelName, searchText)
        ProductCategory.assertResponse(actualResult, 400, expectedErrorCode=101,
                                       expectedErrorMessage='Generic error: Could not fetch attribute values using search text.'
                                    )

    @pytest.mark.parametrize('apiCategory,levelName,searchText', [
        ('productCategory', 'test', 'item')
    ])
    def test_productCategory_values_search_orgNotYetSynced(self, apiCategory, levelName, searchText):
        try:
            IrisHelper.updateOrgId(constant.config['reonNotSynced']['orgId'])
            actualResult = ProductCategory.getLevelValuesUsingSearchText(apiCategory, levelName, searchText)
            ProductCategory.assertResponse(actualResult, 400, expectedErrorCode=101,
                                           expectedErrorMessage='Generic error: Could not fetch attribute values using search text.')
        finally:
            IrisHelper.updateOrgId(self.actualOrgId)