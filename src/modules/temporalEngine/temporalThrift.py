from src.Constant.constant import constant
from src.initializer.generateThrift import timeline
from src.utilities.logger import Logger
from thriftpy.rpc import make_client
import random

class TemporalThrift():
    def __init__(self, port, timeout=60000):
        self.conn = make_client(timeline.TemporalEngineService, '127.0.0.1', port, timeout=timeout)
        self.configConn = make_client(timeline.LifecycleConfigurationService, '127.0.0.1', port, timeout=timeout)
        self.getServerRequestID()

    def getServerRequestID(self):
        self.serverRequestID = 'temporal_auto_' + str(random.randint(11111, 99999))

    def log(self, output):
        Logger.log(output)
        return output

    def isAlive(self):
        return self.log(self.conn.isAlive()) 
    
    def getLifecycleById(self, sessionId):
        Logger.log('For sessionId :', sessionId, ' serverRequestID:', self.serverRequestID)
        return self.log(self.configConn.getLifecycleById(constant.config['orgId'], constant.config['orgConfigId'], sessionId))

    def saveLifecycle(self, newLifecycle, sessionId):
        Logger.log('For sessionId :', sessionId, 'and newLifeCycle :', newLifecycle, 'serverRequestID:', self.serverRequestID)
        return self.log(self.configConn.saveLifecycle(newLifecycle, sessionId))
