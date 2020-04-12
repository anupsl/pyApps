import datetime
from src.utilities.logger import Logger
from src.Constant.constant import constant
from src.utilities.dbhelper import dbHelper

class LoyaltyDBHelper():

    @staticmethod
    def getActiveTillIdList():
        Logger.log('Retrieving Active Till Ids')
        query = "SELECT id FROM  masters.org_entities WHERE  org_id = " + str(constant.config['orgId']) + \
                " AND type = 'TILL' AND is_active = 1 ORDER BY org_entities.id ASC"
        result = dbHelper.queryDB(query, "masters")
        constant.config['tillIds'] = []
        if len(result) == 0:
            Logger.log('No records found')
        else:
            Logger.log('Retrieved data successfully')
            for k in result:
                constant.config['tillIds'] += k

    @staticmethod
    def getActiveStoreIdList():
        Logger.log('Retrieving Active Store Ids')
        query = "select id from masters.store_units where org_id = " + str(constant.config['orgId'])
        result = dbHelper.queryDB(query, "masters")
        constant.config['storeIds'] = []
        if len(result) == 0:
            Logger.log('No records found')
        else:
            Logger.log('Retrieved data successfully')
            for k in result:
                constant.config['storeIds'] += k

    @staticmethod
    def getUsers(limitCount = 10):
        Logger.log('Get users Info')
        query = 'SELECT us.id, us.firstname, us.email, us.mobile, ul.external_id FROM user_management.users us LEFT JOIN user_management.loyalty ul ON us.id = ul.user_id AND us.org_id = ul.publisher_id WHERE us.`email` IS NOT NULL AND us.`mobile` IS NOT NULL and us.is_inactive = 0  AND us.org_id = ' + str(constant.config['orgId']) + ' ORDER BY ID DESC LIMIT ' + str(limitCount)
        result = dbHelper.queryDB(query, 'user_management')
        constant.config['usersInfo'] = []
        if len(result) == 0:
            Logger.log('No records found')
        else:
            Logger.log('Retrieved data successfully')
            for k in result:
                users = {'userId' : k[0],'name' : k[1],'email' : k[2], 'mobile' : k[3], 'externalId' : k[4]}
                constant.config['usersInfo'].append(users)

    @staticmethod
    def getBillNumber():
        Logger.log('Get loyaltyLogId as billNumber')
        query = 'select loyalty_log_id from loyalty_bill_lineitems where org_id = {} order by id desc limit 1'.format(constant.config['orgId'])
        result = dbHelper.queryDB(query, 'user_management')
        if len(result) != 0:
            constant.config['billNumber'] = result[0][0]
        else:
            Logger.log('No records found')

    @staticmethod
    def getPointsRedemptionSummary(customerId, storeId, paramDict = None):
        Logger.log('Get Points redemption summary Details ', paramDict )
        query = "SELECT points_redeemed,redemption_id, bill_id, id, redemption_type FROM points_redemption_summary WHERE org_id = {} AND program_id = {} AND customer_id = {} AND till_id = {} "
        if paramDict != None and paramDict.has_key('redemptionIds'):
            if type(paramDict['redemptionIds']) == list:
                if len(paramDict['redemptionIds']) > 1:
                    redemptionIds = tuple(map(str,paramDict['redemptionIds']))
                    query += " AND redemption_id IN {} ".format(redemptionIds)
                elif len(paramDict['redemptionIds']) == 1:
                    query += " AND redemption_id IN ('{}') ".format(paramDict['redemptionIds'][0])
            elif type(paramDict['redemptionIds']) != list:
                query += " AND redemption_id IN ('{}') ".format(paramDict['redemptionIds'])
            query = query.format(constant.config['orgId'],constant.config['programId'],customerId,storeId)
        elif paramDict != None and paramDict.has_key('requestId'):
            query += "AND request_id = '{}' "
            query = query.format(constant.config['orgId'],constant.config['programId'],customerId,storeId,paramDict['requestId'])
        result = dbHelper.queryDB(query, 'warehouse')
        prsDetails = []
        if len(result) != 0:
            for k in result:
                prsDetails.append({'points_redeemed' : k[0], 'redemption_id' : k[1], 'billId' : k[2], 'prs_id' : k[3],
                                   'redemptionType' : k[4]})
        else:
            Logger.log('No records found')
        return prsDetails

    @staticmethod
    def getPointsDeductions(customerId, deductionSummaryId):
        Logger.log('Get Point deduction summary Details')
        query = 'SELECT deduction_type,points_deducted,deduction_currency_value FROM warehouse.points_deductions WHERE org_id = {} AND program_id = {} AND customer_id = {} AND deduction_summary_id = {}'.format(constant.config['orgId'],constant.config['programId'],customerId,deductionSummaryId)
        result = dbHelper.queryDB(query, 'warehouse')
        pointsDeduction = {}
        if len(result) == 0:
            Logger.log('No records found')
        else:
            for k in result:
                pointsDeduction.update({'deductionType' : k[0], 'pointsDeducted' : k[1], 'deductionCurrencyValue' : k[2]})
        return pointsDeduction

    @staticmethod
    def getSumOfPointsAwarded(customerId):
        Logger.log('Get Points Awarded sum values')
        query = "SELECT SUM(points_value),SUM(redeemed_value) FROM warehouse.points_awarded WHERE org_id = {} AND program_id = {}  and customer_id = {}".format(constant.config['orgId'],constant.config['programId'],customerId)
        result = dbHelper.queryDB(query, 'warehouse')
        sumOfPA = {}
        if len(result) == 0:
            Logger.log('No records found')
        else:
            for k in result:
                sumOfPA.update({'sumOfPointsValue' : k[0], 'sumOfRedeemedValue' : k[1]})
        return sumOfPA

    @staticmethod
    def getRedemptionReversal(redemptionIds,reversalId):
        Logger.log('Get Redemption reversal Mapping')
        subQuery = 'redemption_id IN '
        if type(redemptionIds) == list:
            if len(redemptionIds) > 1:
                subQuery += "{}".format(tuple(redemptionIds))
            elif len(redemptionIds) == 1:
                subQuery += "({})".format(redemptionIds[0])
        elif type(redemptionIds) != list:
            subQuery += "({})".format(redemptionIds)
        query = "SELECT points_reversed,reversal_id FROM warehouse.redemption_reversal_mapping WHERE org_id = {} AND {} AND reversal_id = {}".format(constant.config['orgId'],subQuery,reversalId)
        result = dbHelper.queryDB(query, 'warehouse')
        reveralDict = {}
        if len(result) != 0:
            for k in result:
                reveralDict.update({'reversedPoints' : k[0], 'reversalId' : k[1]})
        else:
            Logger.log('No records found')
        return reveralDict

    @staticmethod
    def getMaxConn():
        Logger.log('Checking Max connection for DB')
        queries = ['show variables like "max_connections"', 'SHOW GLOBAL STATUS LIKE "%Threads_running%"', "SHOW GLOBAL STATUS LIKE '%Threads_connected%'", "select USER, count(*) from information_schema.PROCESSLIST group by USER", "select DB, count(*) from information_schema.PROCESSLIST group by DB"]
        for query in queries:
            result = dbHelper.queryDB(query, 'warehouse')
            Logger.log('Query : ', result)

    @staticmethod
    def getLineItemIds(userId, loyalty_log_id):
        Logger.log('Get Point deduction summary Details')
        query = 'SELECT id FROM user_management.loyalty_bill_lineitems WHERE org_id = {} AND user_id = {} AND loyalty_log_id = {}'.format(constant.config['orgId'],userId,loyalty_log_id)
        result = dbHelper.queryDB(query, 'user_management')
        lineItemIdList = []
        if len(result) == 0:
            Logger.log('No records found')
        else:
            for k in result:
                lineItemIdList.append({'lineItemId' : k[0]})
        return lineItemIdList

    @staticmethod
    def getPointsCategoryIds():
        Logger.log('Get Point deduction summary Details')
        query = 'SELECT id,description,is_redeemable FROM warehouse.points_categories where org_id = {} and program_id = {}'.format(constant.config['orgId'], constant.config['programId'])
        result = dbHelper.queryDB(query, 'warehouse')
        pointCategoryList = []
        if len(result) == 0:
            Logger.log('No records found')
        else:
            for k in result:
                pointCategoryList.append({'id': k[0], 'description' : k[1], 'isRedeemable' : k[2]})
        constant.config.update({'loyalty': {'pointCategory' : pointCategoryList}})


    @staticmethod
    def getCustomerPointsSummary():
        Logger.log('Get Point deduction summary Details')
        LoyaltyDBHelper.getPointsCategoryIds()
        for userId in constant.config['usersInfo']:
            for categoryId in constant.config['loyalty']['pointCategory']:
                query = 'SELECT id,current_points,cumulative_points,cumulative_purchases,points_redeemed,points_expired,points_returned,last_awarded_on,reissued_points FROM warehouse.customer_points_summary WHERE org_id = {} AND program_id = {} AND points_category_id = {} AND customer_id = {}'.format(
                    constant.config['orgId'],constant.config['programId'],categoryId['id'], userId['userId'])
                result = dbHelper.queryDB(query, 'warehouse')
                if len(result) == 0:
                    Logger.log('No records found')
                else:
                    for k in result:
                        constant.config['loyalty'].update({userId : {  'id' : k[0], 'currentPts' : k[1], 'cumulativePurchases' : k[2], 'ptsRedeemed' : k[3], 'ptsExpired' : k[4], 'ptsReturned' : k[5], 'lastAwardedOn' : k[6], 'reIssuedPts' : k[7]} })
