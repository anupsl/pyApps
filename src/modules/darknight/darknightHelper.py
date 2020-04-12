import traceback,random, pymongo
from datetime import datetime

from src.utilities.logger import Logger
from src.Constant.constant import constant
from src.modules.darknight.darknightThrift import DarknightThrift
from src.modules.darknight.darknightObject import DarknightObject
from src.utilities.utils import Utils
from src.utilities.dbhelper import dbHelper
from src.utilities.mongoHelper import MongoHelper


class DarknightHelper():

    @staticmethod
    def checkDarknightConn(ignoreConnectionError=False):
        Utils.checkServerConnection('DARK_KNIGHT_THRIFT_SERVICE', DarknightThrift, 'darknightPort', ignoreConnectionError)

    @staticmethod
    def getConnObj(newConnection=False):
        port = constant.config['darknightPort']
        connPort = str(port) + '_obj'
        if connPort in constant.config:
            if newConnection:
                constant.config[connPort].close()
                constant.config[connPort] = DarknightThrift(port)
            return constant.config[connPort]
        else:
            return DarknightThrift(port)

    @staticmethod
    def getEmailStatus(email):
        query = 'select status from email_status where email = "'+email+'"'
        result = dbHelper.queryDB(query, "darknight")
        if result:
            return result[0][0]
        else:
            return 0

    @staticmethod
    def generateSmsWhitelistingData(tmpValue, mobile = '918660430751'):
        if constant.config['cluster'] in ['nightly', 'staging']:
            for i in range(0, 3):
                try:
                    testCol = constant.config['mongoConn']
                    value = {
                        "mobile": mobile, 
                        "delivered": 0, 
                        "not_delivered": 0
                    }
                    value.update(tmpValue)
                    value['total'] = value['delivered'] + value['not_delivered']
                    batchReq = []
                    batchReq.append(pymongo.ReplaceOne({'mobile': mobile}, value, upsert=True))
                    testCol.bulk_write(batchReq)
                    Logger.log(testCol.find({'mobile' : mobile})[0])
                    return
                except pymongo.errors.ConnectionFailure as e:
                    Logger.log(e)
                    port = constant.config['INTOUCH_DB_MONGO_MASTER']
                    if Utils.restartTunnel(port):
                        DarknightHelper.getMongoConnection('whitelisting', 'mobile_status')
                    else:
                        break
                except Exception as e:
                    break
            raise Exception(e)

    @staticmethod
    def monthlyDelta():
        monthList = []
        date = datetime.now()
        for delta in range(0, 8):
            m, y = (date.month-delta) % 12, date.year + ((date.month)-delta-1) // 12
            if not m: m = 12
            d = min(date.day, [31,29 if y%4==0 and not y%400==0 else 28,31,30,31,30,31,31,30,31,30,31][m-1])
            monthList.append(date.replace(day=d,month=m, year=y))
        return monthList

    @staticmethod
    def getMongoConnection(database, collection):
        port = constant.config['INTOUCH_DB_MONGO_MASTER']
        m = MongoHelper(database, collection, port)
        constant.config['mongoConn'] = m.mongodb
