import time
import datetime

from src.Constant.constant import constant
from src.utilities.dbhelper import dbHelper
from src.utilities.mongoHelper import MongoHelper
from src.utilities.logger import Logger


class campaign_info():
    def __init__(self, campaignId):
        self.campaignId = campaignId
        self.campaignInfo = dict()
        self.getCampaignDetails()

    def getCampaignDetails(self):
        query = {'campaignId': self.campaignId}
        result = MongoHelper.findDocuments('campaigns', 'campaign', constant.config['CAMPAIGNS_DB_MONGO_MASTER'], query,
                                           limit=1)
        self.campaignInfo.update(result[0])




class campaign_calls():
    def getLatestCampaignIdOfV1(self):
        query = 'select id from campaigns_base where org_id = {} order by id desc limit 1 '.format(
            constant.config['orgId'])
        result = dbHelper.queryDB(query, 'campaigns')
        return result[0][0]

    def getCampaignIdAsPerQueryParam(self, limit, offset, search):
        query = {'name': {'$regex': '{}'.format(search)}, 'orgId': constant.config['orgId']}
        result = MongoHelper.findDocuments('campaigns', 'campaign', constant.config['CAMPAIGNS_DB_MONGO_MASTER'], query,
                                           limit=limit, sort='startDate', skip=offset)
        listOfCampaignIds = list()
        for eachEntity in result:
            listOfCampaignIds.append(eachEntity['campaignId'])
        return listOfCampaignIds

    def getCampaignId(self, campaignType, testControlType):
        query = {
            'orgId': constant.config['orgId'],
            'testControl.testControlType': testControlType
        }
        if campaignType == 'LIVE':
            query.update({
                'startDate': {'$lt': datetime.datetime.fromtimestamp(time.time() - 1000, None)},
                'endDate': {'$gt': datetime.datetime.fromtimestamp(time.time() + 1000,None)}
            })
        elif campaignType == 'UPCOMING':
            query.update({
                'startDate': {'$gt': datetime.datetime.fromtimestamp(time.time() + 1000, None)},
            })
        elif campaignType == 'LAPSED':
            query.update({
                'endDate': {'$lt': datetime.datetime.fromtimestamp(time.time() - 1000, None)}
            })
        result = MongoHelper.findDocuments('campaigns', 'campaign', constant.config['CAMPAIGNS_DB_MONGO_MASTER'], query,
                                        limit=20,sort='_id')
        if len(result) == 0: raise Exception('NoListFoundException, Query :{}'.format(query))
        return result

    def getUserId(self,numberOfUserIds):
        query = 'select id from admin_users where org_id = {} and mobile_validated = 1 and email_validated = 1 order by id desc limit {} '.format(
            constant.config['orgId'],numberOfUserIds)
        result = dbHelper.queryDB(query, 'masters')
        listOfIds = list()
        for eachId in result:
            listOfIds.append(eachId[0])
        return listOfIds


class campaignSettingDBCalls():

    def getCampaignSettings(self):
        query = {
            '_id': constant.config['orgId']
            }
        result = MongoHelper.findDocuments('campaigns', 'campaignSettings', constant.config['CAMPAIGNS_DB_MONGO_MASTER'], query)
        if len(result) == 0: raise Exception('NoSettingsException:{}'.format(query))
        return result[0]


class campaignObjectiveDBCalls():

    def getCampaignObjective(self):
        result = MongoHelper.findDocuments('campaigns', 'campaignObjectives', constant.config['CAMPAIGNS_DB_MONGO_MASTER'], {},limit=10)
        if len(result) == 0: raise Exception('NoSettingsException')
        return result

class campaignMessageStats():
    def getCampaignMessageStats(self,eachCampaignId):
        query = {
                'campaignId' : eachCampaignId
            }
        result = MongoHelper.findDocuments('campaigns', 'message', constant.config['CAMPAIGNS_DB_MONGO_MASTER'], query,limit=99)

        return result

class orgStatus():
     def getOrgStatus(self):
         query = 'select status from  campaign_v2_org_status where org_id = {} '.format(
             constant.config['orgId'])
         result = dbHelper.query(query, 'masters',constant.config['INTOUCH_META_DB_MYSQL'][0])
         return result

class campaignEndDate():
    def getCampaignEndDate(self,campaignId):
        query = {'campaignId': campaignId }
        result = MongoHelper.findDocuments('campaigns', 'campaign', constant.config['CAMPAIGNS_DB_MONGO_MASTER'],
                                           query,
                                           limit=1)

        return result[0]['endDate']



