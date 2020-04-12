import traceback,random, time
from src.utilities.logger import Logger
from src.Constant.constant import constant
from src.modules.peb.pebThrift import PEBThrift
from src.modules.peb.pebObject import PEBObject
from src.utilities.utils import Utils
from src.utilities.dbhelper import dbHelper


class PEBHelper():

    @staticmethod
    def checkPEBConn(ignoreConnectionError=False):
        Utils.checkServerConnection('PEB_THRIFT_SERVICE', PEBThrift, 'pebPort', ignoreConnectionError)


    @staticmethod
    def getConnObj(newConnection=False):
        port = constant.config['pebPort']
        connPort = str(port) + '_obj'
        if connPort in constant.config:
            if newConnection:
                constant.config[connPort].close()
                constant.config[connPort] = PEBThrift(port)
            return constant.config[connPort]
        else:
            return PEBThrift(port)        