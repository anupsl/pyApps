from src.dbCalls.messageInfo import pointsMetaInfo
from src.utilities.logger import Logger
from src.utilities.assertion import Assertion

class LoyaltyProgrameDbAssertion():

    def __init__(self,response):
        self.response = response
        self.pointsMeta = pointsMetaInfo().pointsMeta

    def validate(self):
        for eachentity in self.response['json']['entity']:
            Logger.log('Validation for Programe id : {}'.format(eachentity['programId']))
            Assertion.constructAssertion(eachentity['programId'] in self.pointsMeta, 'Programeid :{} found in DB'.format(eachentity['programId']))
            self.basicValidationForProgram(eachentity)
            self.validateTiersForEachEntity(eachentity)
            self.validateStrategy(eachentity)

    def basicValidationForProgram(self,entity):
        for eachKey in ['name', 'pointsCurrencyRatio', 'default', 'active']:
            Assertion.constructAssertion(entity[eachKey] == self.pointsMeta[entity['programId']][eachKey],
                                         'Field :{} for Id :{} in Response :{} and in DB :{}'.format(eachKey,entity['programId'],entity[eachKey],self.pointsMeta[entity['programId']][eachKey]))

    def validateTiersForEachEntity(self,entity):
        for eachTier in entity['tiers']:
            Assertion.constructAssertion(eachTier['id'] in self.pointsMeta[entity['programId']]['tiers'],'For ProgrameId :{} , tier id :{} found in DB '.format(entity['programId'],eachTier['id']))
            for eachTierValue in ['serialNumber','name','description']:
                Assertion.constructAssertion(eachTier[eachTierValue] == self.pointsMeta[entity['programId']]['tiers'][eachTier['id']][eachTierValue],'Key :{} , value in Response and in DB :{}'.format(eachTierValue,eachTier[eachTierValue] , self.pointsMeta[entity['programId']]['tiers'][eachTier['id']][eachTierValue]))

    def validateStrategy(self,entity):
        for eachStrategy in entity['strategy']:
            Logger.log('Validating Strategy :{}'.format(eachStrategy))
            for eachTypeStrategy in entity['strategy'][eachStrategy]:
                Logger.log('Validating For ID :{}'.format(eachTypeStrategy['id']))
                Assertion.constructAssertion(eachTypeStrategy == self.pointsMeta[entity['programId']]['strategy'][eachStrategy][int(eachTypeStrategy['id'])],'For Strategy :{} and strategy Id :{} , data in Response :{} and in DB :{}'.format(eachStrategy,eachTypeStrategy['id'],eachTypeStrategy,self.pointsMeta[entity['programId']]['strategy'][eachStrategy][int(eachTypeStrategy['id'])]))

