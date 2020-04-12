from src.modules.temporalEngine.temporalThrift import TemporalThrift
from src.utilities.logger import Logger
from src.Constant.constant import constant
from src.utilities.utils import Utils
from itertools import cycle
import traceback, time, json

class TemporalHelper():
    
    @staticmethod
    def checkTemporalServerConnection(ignoreConnectionError=False):
        Utils.checkServerConnection('TEMPORAL_ENGINE_THRIFT_SERVICE', TemporalThrift, 'temporalPort', ignoreConnectionError)

    @staticmethod
    def getConnObj():
        port = constant.config['temporalPort']
        connPort = str(port) + '_obj'
        if connPort in constant.config:
            obj = constant.config[connPort]
            obj.getServerRequestID()
            return obj
        else:
            return TemporalThrift(port)
