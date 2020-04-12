from src.Constant.constant import constant
from src.initializer.generateThrift import timeline
from src.utilities.utils import Utils
from src.utilities.logger import Logger
from src.modules.temporalEngine.temporalHelper import TemporalHelper
import uuid, time

class TemporalObject():
    
    def __init__(self):
        pass
    
    @staticmethod
    def SessionId():
        tmpDict = {
            'orgId':constant.config['orgId'],
            'orgConfigId':constant.config['orgConfigId'],
            'apacheThreadId':'automationTest',
            'userId':1,
            'moduleName':'apps'
        }
        Logger.log('SessionId Structured as :{}'.format(tmpDict))
        return timeline.SessionId(**tmpDict)
    
    @staticmethod
    def Lifecycle(curLifecycle, extraField={}):
        tmpDict = {
            'id':curLifecycle.id,
            'campaignId':curLifecycle.campaignId,
            'name':curLifecycle.name,
            'userDefinedName':curLifecycle.userDefinedName,
            'orgId':curLifecycle.orgId,
            'startMinuteOfDay':curLifecycle.startMinuteOfDay,
            'endMinuteOfDay':curLifecycle.endMinuteOfDay,
            'status':curLifecycle.status,
            'stateTimelineMapping':curLifecycle.stateTimelineMapping,
            'userInitiationRuleset':curLifecycle.userInitiationRuleset,
            'properties':curLifecycle.properties,
            'timelines':curLifecycle.timelines
        }
        
        if extraField != {}:
            tmpDict.update(extraField)
        Logger.log('Lifecycle Structured as :{}'.format(tmpDict))
        return timeline.Lifecycle(**tmpDict)