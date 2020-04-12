import MySQLdb
from src.utilities.logger import Logger

class Database(object):
    
    def __init__(self, server, db, user, passwd, port=3306):
        Logger.log('server: ', 'localhost', ' db: ', db, ' port: ', port)
        port = int(port)
        self.db = MySQLdb.connect(host=server, user=user, passwd=passwd, db=db, port=port,
                    use_unicode=True, charset="utf8", compress=True, connect_timeout=20)
        self.conn = self.db.cursor()

    '''
    This Blocks helps to avoid multi client connection establishment
    def resetCursor(self):
        self.db.autocommit(True)
        self.conn = self.db.cursor()
    '''
        
    def readFromDB(self, query):
        Logger.log(query)
        self.conn.execute(query)
        queryoutput = self.conn.fetchall()
        Logger.log(queryoutput)
        return queryoutput

    def writeToDB(self, query):
        Logger.log(query)
        try:
            self.conn.execute(query)
            self.db.commit()
        except Exception as e:
            Logger.log('Error updating db. Rolling back: ', e)
            self.db.rollback()         

    def close(self):
        self.db.close()



       