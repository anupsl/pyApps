import os, time, platform
from src.Constant.ports import ports
from src.Constant.orgMapping import OrgMapping
from src.Constant.url import url
from src.Constant.social import social
from src.Constant.iris import irisConstant
from src.Constant.irisv2 import Irisv2
from src.Constant.luciExceptionCodes import LuciExceptionCodes as luciConstant
from src.Constant.campaignui import campaignuiConstant
from src.Constant.apiTesterConstants import dbName
from src.Constant.campaignShard import campaignShardConstant
from src.Constant.commSys import CommSys

class constant(ports, OrgMapping, url, social, irisConstant, luciConstant, 
        campaignuiConstant, dbName, campaignShardConstant, CommSys, Irisv2):

    config = {'logCollectorConnErr' : 0, 'validataionMessage' : [], 'os' : platform.system().lower(), 'moduleFlip' : False}
    oldConfig = False
    rootPath = os.getcwd()
    logDirectory = '/var/log/capillary/pyApps/'
    randomHtmlPath = rootPath + '/src/modules/campaignUIPages/emailTemplate.html'
    maxNumberOfLogFiles = 20
    testFolder = rootPath + '/tests/'
    MachineToDBMapping = {
        'INTOUCH_DB_MYSQL_MASTER' : ['campaigns', 'masters', 'user_management', 'msging', 'warehouse' , 'luci', 'Temp','audit_logs'],
        'INTOUCH_META_DB_MYSQL' : ['scheduler', 'shard_manager', 'authentication'],
        'CAMPAIGN_SHARD_DB_MYSQL' : ['campaign_meta_details', 'campaign_data_details', 'veneno', 'veneno_data_details', 'veneno_meta_details', 'health_dashboard'],
        'INTOUCH_DB_MYSQL_BILLDUMP' : [],
        'NSADMIN_DB_MYSQL' : ['nsadmin', 'log'],
        'TIMELINE_DB_MYSQL' : ['temporal_engine_bootstrap'],
        'DARK_KNIGHT_DB_MYSQL' : ['darknight']
    }
    marketingModule = 'google'
    logCollectorUrl = 'http://localhost:4000/logger'
    chromeDriverUrl = 'https://chromedriver.storage.googleapis.com/'
    chromeDriverPath = rootPath + '/src/utilities/drivers/chromedriver'
    if config['os'] == 'windows':
        chromeDriverPath += '.exe'
    phantomjsPath = rootPath + '/src/utilities/drivers/phantomjs'
    driver = None
    awsKey = 'AKIAIKCKQU55JNZ5Y5MA'
    awsSecret = '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'
    csvFilePath = rootPath + '/src/csvFiles/'
    luciS3FilePath = csvFilePath + 'uploadCoupons.csv'
    downloadS3File = '/coupon/api/v1/download?time='
    autoTempFilePath = '/var/tmp/'
    prodDbCred = [
        {'DbUsername' : 'capillary', 'DbPassword' : 'deal20hunt'},
        {'DbUsername' : 'capillaryro', 'DbPassword' : 'yQy7i45reUOuM'},
        {'DbUsername' : 'capillaryro', 'DbPassword' : 'captech123'},
        {'DbUsername' : 'local', 'DbPassword' : 'local'},
    ]

    rabbitmqCred = {
        'username' : 'appsauto', 'passwd' : 'Apps@123',
        'nightly' : 'https://rabbitmq.nightly.capillary.in',
        'staging' : 'https://rabbitmq.staging.capillary.in',
        'more' : 'http://comm-rabbitmq.capillary.sg',
        'india' : 'http://rabbitmq-test.capillary.in',
        'eu' : 'http://rabbitmq.capillary.eu',
        'china' : 'http://rabbitmq.capillarytech.cn.com'
    }

