import traceback,random, time,  json
from src.utilities.logger import Logger
from src.Constant.constant import constant
from src.modules.loyalty.emfThrift import EMFThrift
from src.modules.loyalty.pointsEngineThrift import PointsEngineThrift
from src.modules.loyalty.pointsEngineRulesThrift import PointsEngineRulesThrift
from src.modules.loyalty.nrulesThrift import NrulesThrift
from src.modules.loyalty.datamanagerThrift import DatamanagerThrift
from src.modules.inTouchAPI.customer import Customer
from src.modules.inTouchAPI.transaction import Transaction
from src.modules.inTouchAPI.inTouchAPI import InTouchAPI

from src.utilities.utils import Utils
from src.utilities.dbhelper import dbHelper


class LoyaltyAPIHelper():


    @staticmethod
    def customerRegistration(self):
        return InTouchAPI(Customer.Add()).response

    @staticmethod
    def transactionAdd(self, body):
        transObj = InTouchAPI(Transaction.Add(body=body)).response
        return transObj