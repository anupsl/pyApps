import datetime
import decimal
import json

import requests
from bson import ObjectId

from src.Constant.constant import constant
from src.utilities.database import Database
from src.utilities.keyczar.keyczar import Crypter
from src.utilities.logger import Logger
from src.utilities.utils import Utils


class dbHelper():
    @staticmethod
    def query(query, dbname, port, retry=3):
        exceptionList = [1152, 1154, 2003, 2013]
        values = dbHelper.getDBCred(port)
        for i in range(0, retry):
            try:
                db = Database(server='127.0.0.1', db=dbname, user=values['DbUsername'], passwd=values['DbPassword'],
                              port=port)
                if query.lower().startswith('insert') or query.lower().startswith('update'):
                    dboutput = db.writeToDB(query)
                else:
                    dboutput = db.readFromDB(query)
                    dboutput = map(list, dboutput)
                    dboutput = dbHelper.convertDataType(dboutput)
                db.close()
                return dboutput
            except Exception as e:
                if e[0] in exceptionList:
                    Logger.log(e)
                    if not Utils.restartTunnel(port):
                        break
                else:
                    Logger.log('Ignore DB restart')
                    break
        raise Exception(
            "Exception Occured while Querying :{} for Query :{} on DB :{} and port :{}".format(e, query, dbname, port))

    @staticmethod
    def DBServerConnection(dbname, values, port):
        if not constant.config.has_key(str(port) + '_dbObjOf_' + str(dbname)):
            constant.config[str(port) + '_dbObjOf_' + str(dbname)] = Database(server='127.0.0.1', db=dbname,
                                                                              user=values['DbUsername'],
                                                                              passwd=values['DbPassword'], port=port)
            return constant.config[str(port) + '_dbObjOf_' + str(dbname)]
        else:
            return constant.config[str(port) + '_dbObjOf_' + str(dbname)]

    @staticmethod
    def convertDataType(data):
        if isinstance(data, dict):
            for k, v in data.items():
                data[k] = dbHelper.convertDataType(v)
        elif isinstance(data, list):
            for k, v in enumerate(data):
                data[k] = dbHelper.convertDataType(v)
        else:
            if isinstance(data, datetime.datetime) or isinstance(data, datetime.date) or isinstance(data, ObjectId):
                return str(data)
            elif isinstance(data, decimal.Decimal):
                return float(data)
            elif isinstance(data, long):
                return int(data)
        return data

    @staticmethod
    def getDBCred(DBport):
        if DBport in [6614, 6624, 6634, 6644]:
            return constant.prodDbCred[1]
        elif DBport in [8415, 8515]:
            return constant.prodDbCred[2]
        elif DBport in [3306]:
            return constant.prodDbCred[3]
        else:
            return constant.prodDbCred[0]

    @staticmethod
    def getShardedPort(endPoint):
        ports = constant.config[endPoint]
        if len(ports) > 1:
            return ports[constant.config['shardCount'] - 1]
        else:
            return ports[0]

    @staticmethod
    def getIntouchShardNameForOrg(module=''):
        orgId = constant.config['orgId']
        query = 'select name from shard where id = (select shard_id from org_shard_mapping where org_id = ' + str(
            orgId) + ' and policy_id =2)'
        dbName = 'shard_manager'
        port = dbHelper.getShardedPort('INTOUCH_META_DB_MYSQL')
        if constant.config['collectOnly']:
            shardCount = 1
        else:
            try:
                shardCount = int(dbHelper.query(query, dbName, port)[0][0])
            except IndexError:
                raise Exception('Org:' + str(orgId) + ' not found in shard_manager')
        constant.config['shardCount'] = shardCount

    @staticmethod
    def buildDBToTunnelPortMapping():
        DBToTunnelPortMapping = {}
        duplicateList = []
        for machine, dbList in constant.MachineToDBMapping.items():
            for db in dbList:
                if db in duplicateList:
                    raise Exception('Duplicate DB found' + db + ' in ' + str(dbList))
            # Logger.log('Getting Port For Machine : ',machine)
            port = dbHelper.getShardedPort(machine)
            DBToTunnelPortMapping.update(dict.fromkeys(dbList, port))
        constant.config['DBToTunnelPortMapping'] = DBToTunnelPortMapping

    @staticmethod
    def queryDB(query, dbName):
        if dbName in constant.config['DBToTunnelPortMapping']:
            port = constant.config['DBToTunnelPortMapping'][dbName]
        else:
            raise Exception('DB name not defined')
        return dbHelper.query(query, dbName, port)

    @staticmethod
    def queryAPITester(query, dbname, machine):
        Logger.log('Making a DB Call to APITester ')
        apitester_url = 'http://apitester.capillary.in/apitest_app/common'
        crypter = Crypter.Read(constant.rootPath + '/src/utilities/keyczar/key')
        body = {'request': 'dbquery', 'cluster': machine, 'dbname': dbname, 'query': query, 'retry': 6}
        Logger.log('Post Request sent to API_TESTER :' + str(body))
        crypted_body = crypter.Encrypt(json.dumps(body))
        crypted_response = requests.post(apitester_url, data={'data': crypted_body})
        decrypted_response = crypter.Decrypt(crypted_response.text)
        response = json.loads(decrypted_response)
        result = None
        if response.get('status') == 'success':
            result = response.get('queryresponse')
            Logger.log('Response is Success from API_Tester and query response is returned ')
            Logger.log('Result :' + str(result))
        else:
            Logger.log('Response from API_TESTER is :' + str(response.get('status')))
        if not result:
            Logger.log('No Data returned from DB, returning result as []')
        return result
