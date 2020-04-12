import copy
import traceback
from datetime import datetime

from src.Constant.constant import constant
from src.modules.arya.auth import auth
from src.modules.campaignUIPages.campaignsUIDBCalls import DBCallsCampaigns
from src.modules.campaign_shard.campaignShardHelper import CampaignShardHelper
from src.modules.darknight.darknightHelper import DarknightHelper
from src.modules.iris.dbCallsCampaign import dbCallsCampaign
from src.modules.iris.dbCallsList import dbCallsList
from src.modules.iris.dbCallsMessage import dbCallsMessage
from src.modules.loyalty.loyaltyHelper import LoyaltyHelper
from src.modules.luci.dracarysHelper import DracarysHelper
from src.modules.luci.luciDBHelper import LuciDBHelper
from src.modules.luci.luciHelper import LuciHelper
from src.modules.nsadmin.nsadminHelper import NSAdminHelper
from src.modules.peb.pebHelper import PEBHelper
from src.modules.social.socialHelper import SocialHelper
from src.modules.temporalEngine.temporalHelper import TemporalHelper
from src.modules.veneno.venenoHelper import VenenoHelper
from src.utilities.chromeDriverManager import ChromeDriverManager
from src.utilities.dbhelper import dbHelper
from src.utilities.fileHelper import FileHelper
from src.utilities.logger import Logger
from src.utilities.randValues import randValues
from src.utilities.utils import Utils
from src.modules.reon.reonHelper import ReonHelper


class BaseState():
    @staticmethod
    def initializeConstants(args):
        module = constant.config['module'] = args.module.lower()
        runId = args.runId
        collectOnly = constant.config['collectOnly'] = args.collectOnly
        tcFilter = args.tcFilter
        cluster = constant.config['cluster'] = args.cluster.lower()
        if collectOnly:
            if 'cluster' in args.cluster.lower():
                cluster = constant.config['cluster'] = 'nightly'
            constant.config['campaignId'] = 1

        if module.lower() == 'nsadmin':
            if tcFilter != '':
                tcFilter += ' and'
            if cluster.lower() in ['nightly', 'staging']:
                tcFilter += ' not Prod'
            else:
                tcFilter += ' Prod and ' + str(cluster.title())
            if args.prodEmail1 != '':
                constant.prodNumbers['prodEmail1'] = args.prodEmail1
        constant.config['tcFilter'] = tcFilter

        if not module in runId.lower():
            runId = module.title() + '_' + runId
        msg = 'Initializing Suite for Cluster: ' + cluster + ' Module: ' + module
        if tcFilter != '':
            msg += ' Filter: ' + tcFilter
        print msg

        constant.config['runId'] = runId
        constant.config['logDir'] = constant.logDirectory + runId
        constant.config['currentTimestamp'] = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        constant.config.update(constant.portsUsed[cluster])
        constant.config.update(constant.clusterUrl[cluster])
        constant.config.update(constant.auth[cluster])
        constant.config.update(constant.intouchEndpoints)
        constant.config.update(constant.endpoints)
        BaseState.updateOrgDetails(module)
        if module in ['iris','irisv2', 'veneno', 'darknight', 'campaign_shard', 'campaignsui', 'social']:
            constant.config.update(constant.wechatMobilepush[cluster])
            if constant.config['cluster'] in ['nightly', 'staging', 'china']: constant.config['wecrm_details'] = \
                constant.config['wechat']['wecrm_details']
            constant.config.update(constant.aryaEndpoints)
            constant.config.update({'campaignDefaultObjectCopy': copy.deepcopy(constant.campaignDefaultValues)})
            try:
                authResponse = auth.authLogin()
                if authResponse['cookies'].get_dict() != {}:
                    constant.config['aryaCookiesDict'] = authResponse['cookies'].get_dict()
                    constant.config['token'] = authResponse['json']['token']
                else:
                    raise Exception('')
            except:
                print '------------------------------Arya Cookies Not Set------------------------------'

        if module in ['emf', 'peb']:
            orgId = constant.config['orgId']
            constant.config.update(constant.emfConstants[cluster][orgId])
        if module in ['luci', 'veneno', 'social']:
            constant.config['requestId'] = 'requestId_' + str(randValues.randomInteger(5))
            constant.config['dateTime'] = DracarysHelper.getValueOfDay()
        if not collectOnly:
            Utils.createFolder(constant.config['logDir'])
            Logger.configureLogging(constant.config['logDir'])
        if constant.config['os'] != 'windows':
            dbHelper.getIntouchShardNameForOrg(module)
            dbHelper.buildDBToTunnelPortMapping()
        if module == 'veneno' and not collectOnly:
            if constant.config['cluster'] == 'nightly': VenenoHelper.updateStartegyForRateLimit()
        if module == 'irisv2':
            constant.irisGenericValues = {'goalId': '1', 'objectiveId': '1', 'existingUserId': '1',
                                          'existingUserExternalId': '1'}
        if module in ['iris', 'veneno', 'campaign_shard', 'campaignsui', 'darknight', 'social']:
            constant.config['skipped_errors'] = dbCallsList.getSkippedErrorTypes()
            constant.config.update(constant.irisDetails[cluster])
            if collectOnly:
                constant.irisGenericValues = {'goalId': '1', 'objectiveId': '1', 'existingUserId': '1',
                                              'existingUserExternalId': '1'}
            else:
                try:
                    goalId = str(dbCallsCampaign.getValidGoalId())
                    objectiveId = str(dbCallsCampaign.getValidObjectiveId())
                    existingUserDetail = dbCallsMessage.getUsersInformation(1)[0]
                    constant.irisGenericValues = {'goalId': goalId, 'objectiveId': objectiveId,
                                                  'existingUserId': existingUserDetail[0],
                                                  'existingUserExternalId': existingUserDetail[5]}
                except Exception, exp:
                    constant.irisGenericValues = {'goalId': '1', 'objectiveId': '1', 'existingUserId': '1',
                                                  'existingUserExternalId': '1'}
                    Logger.log(
                        'Exception :{} occured while setting irisGeneric Values , so setting the values by Default as :{}'.format(
                            exp, constant.irisGenericValues))
        if module == 'campaignsui':
            constant.config.update(constant.irisDetails[cluster])
            constant.config.update(constant.wechatMobilepush[cluster])
            if constant.config['cluster'] in ['nightly', 'staging', 'china']: constant.config['wecrm_details'] = \
                constant.config['wechat']['wecrm_details']
            constant.config.update({'headlessMode': args.headlessMode})
            constant.config.update(constant.campaignuiDetails)
            constant.config.update({'apiTesterDB': constant.dbNames[cluster]})
            constant.config.update({'shard': DBCallsCampaigns.getShardGettingUsed()})

            if collectOnly:
                constant.campaignuiUserInfo.update({'loyalty': {'name': 'name', 'email': 'email', 'mobile': 'mobile'}})
            else:
                fileHandle = FileHelper(constant.userFileMobile)
                existingUserDetail = DBCallsCampaigns.getLoyaltyUserInfo(1)[0]
                constant.campaignuiUserInfo.update({'loyalty': {'name': existingUserDetail[1],
                                                                'email': existingUserDetail[4],
                                                                'mobile': existingUserDetail[3]}})
                fileHandle.eraseContentFromFile()
                fileHandle.appendToFile('mobile,name')
                fileHandle.appendToFile(str(existingUserDetail[3]) + ',' + str(existingUserDetail[1]))
        if module == 'nsadmin':
            constant.config.update(constant.prodNumbers)
            constant.config.update({"clusterFileHandle": constant.clusterFileHandle[cluster]})
            constant.config.update({"dlrUrl": constant.dlrUrl[cluster]})

        if module == 'irisv2':
            constant.config.update({'node': copy.deepcopy(constant.node)})

        if not collectOnly:
            sortesListOfLogFiles = Utils.sorted_ls(constant.logDirectory)
            if len(sortesListOfLogFiles) > constant.maxNumberOfLogFiles:
                try:
                    Utils.deleteFolder(constant.logDirectory + '/' + sortesListOfLogFiles[0])
                except Exception as e:
                    Logger.log(str(e))
            BaseState.setBaseState()

    @staticmethod
    def updateOrgDetails(module):
        cluster = constant.config['cluster']
        constant.config.update(constant.orgMapping[cluster][module])
        orgId = constant.config['orgId']
        if orgId in constant.tillCred[cluster]:
            constant.config.update(constant.tillCred[cluster][orgId][0])
        constant.config.update(constant.orgDetails[cluster][orgId])

    @staticmethod
    def setBaseState():
        module = constant.config['module']
        if module == 'nsadmin':
            NSAdminHelper.checkCommServerConn()
        if module == 'iris':
            NSAdminHelper.checkCommServerConn(ignoreConnectionError=True)
            LuciHelper.checkLuciConn(ignoreConnectionError=False)
        if module == 'irisv2':
            LuciHelper.checkLuciConn(ignoreConnectionError=True)
            ReonHelper.checkReonConnection(ignoreConnectionError=True)
            NSAdminHelper.checkCommServerConn()
            CampaignShardHelper.checkCampaignShardConnection()
        if module == 'luci':
            LuciHelper.loginAndGetCookies()
            LuciHelper.checkLuciConn()
            DracarysHelper.checkDracarysConn()
            LuciHelper.setBaseDetails()
        if module == 'veneno':
            LuciHelper.checkLuciConn(ignoreConnectionError=True)
            LuciDBHelper.getAdminUserId()
            VenenoHelper.checkVenenoServerConnection()
            NSAdminHelper.checkCommServerConn(ignoreConnectionError=True)
            CampaignShardHelper.checkCampaignShardConnection()
        if module == 'campaign_shard':
            CampaignShardHelper.checkCampaignShardConnection()
        if module == 'darknight':
            DarknightHelper.checkDarknightConn()
        if module == 'campaignsui':
            NSAdminHelper.checkCommServerConn(ignoreConnectionError=True)
            TemporalHelper.checkTemporalServerConnection(ignoreConnectionError=True)
            try:
                status, version = ChromeDriverManager.checkChromeDriverCompatibility()
                if not status:
                    ChromeDriverManager.downloadChromeDriver(version)
            except:
                Logger.log(traceback.format_exc())
        if module == 'emf' or module == 'peb':
            LoyaltyHelper.checkEMFConn()
            PEBHelper.checkPEBConn()
        if module == 'peb':
            PEBHelper.checkPEBConn()
        if module == 'social':
            SocialHelper.checkSocialConn()
            VenenoHelper.checkVenenoServerConnection()
            LuciHelper.checkLuciConn(ignoreConnectionError=True)
            LuciDBHelper.getAdminUserId()
            DracarysHelper.checkDracarysConn(ignoreConnectionError=True)
            LuciHelper.loginAndGetCookies()
            LuciHelper.setBaseDetails()

    @staticmethod
    def moduleFlip(moduleName):
        if moduleName == -1:
            if constant.oldConfig:
                constant.config = copy.deepcopy(constant.oldConfig)
            else:
                raise Exception('Config backup is not taken')
        else:
            cluster = constant.config['cluster']
            if moduleName in constant.orgMapping[cluster]:
                if not constant.oldConfig:
                    constant.oldConfig = copy.deepcopy(constant.config)
                    BaseState.updateOrgDetails(moduleName)
                    constant.config['moduleFlip'] = True
            else:
                raise Exception('No module found: ' + moduleName)
