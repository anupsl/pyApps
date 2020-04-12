from src.dbCalls.messageInfo import pocMetaInfo
from src.utilities.logger import Logger
from src.utilities.assertion import Assertion


class PocDbAssertion():

    def __init__(self,response):
        self.response = response
        self.pocMetaData = pocMetaInfo().pocMetaData
        Logger.log(self.pocMetaData)

    def validate(self):
        for eachPOCS in ['orgPocs','capPocs']:
            for eachentity in self.pocMetaData[eachPOCS]:
                uid =eachentity
                uid_db_meta = self.pocMetaData[eachPOCS][eachentity]
                listOfIds = list()
                for idx in self.response['json']['entity'][eachPOCS]:
                    listOfIds.append(idx['userId'])

                if uid not in listOfIds : Assertion.constructAssertion(False,'uid :{} not found in response :{} for POC :{}'.format(uid,self.response,eachPOCS))
                for each in self.response['json']['entity'][eachPOCS]:
                    if each['userId'] == uid : uid_resp_meta = each
                Assertion.constructAssertion(uid_db_meta == uid_resp_meta,'Entity In Response for UserId :{} is {} and from DB is :{}'.format(uid,uid_resp_meta,uid_db_meta))

