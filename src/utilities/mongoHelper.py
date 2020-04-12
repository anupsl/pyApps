import datetime
import decimal
import pymongo
from bson import ObjectId

from src.utilities.logger import Logger
from src.utilities.utils import Utils


class MongoHelper():
    def __init__(self, database, collection, port):
        Logger.log('database: ', database, ' collection: ', collection, ' port: ', port)
        self.client = pymongo.MongoClient("mongodb://127.0.0.1:" + str(port))
        if collection != '':
            self.mongodb = self.client[database][collection]
        else:
            self.mongodb = self.client[database]

    def readFromMongoDB(self, query, sort, limit=0,skip=0):
        Logger.log('query: ', query, ' sort: ', sort, ' limit: ', limit)
        if sort == '':
            cursor = self.mongodb.find(query).limit(limit).skip(skip)
        else:
            cursor = self.mongodb.find(query).sort(sort, -1).limit(limit).skip(skip)
        output = []
        for c in cursor:
            output.append(c)
        Logger.log(output)
        return output

    def close(self):
        self.client.close()

    @staticmethod
    def findDocuments(database, collection, port, query, sort='', limit=1, skip=0, retry=3):
        for i in range(0, retry):
            try:
                db = MongoHelper(database, collection, port)
                dboutput = db.readFromMongoDB(query, sort, limit,skip)
                db.close()
                dboutput = MongoHelper.convertDataTypeMongo(dboutput)
                return dboutput
            except pymongo.errors.ConnectionFailure as e:
                Logger.log(e)
                if not Utils.restartTunnel(port):
                    break
                else:
                    Logger.log('Ignore DB restart')
            except Exception as e:
                break
        raise Exception(e)

    @staticmethod
    def convertDataTypeMongo(data):
        if isinstance(data, dict):
            for k, v in data.items():
                data[k] = MongoHelper.convertDataTypeMongo(v)
        elif isinstance(data, list):
            for k, v in enumerate(data):
                data[k] = MongoHelper.convertDataTypeMongo(v)
        else:
            if isinstance(data, datetime.datetime) or isinstance(data, datetime.date) or isinstance(data, ObjectId):
                return str(data)
            elif isinstance(data, decimal.Decimal):
                return float(data)
        return data
