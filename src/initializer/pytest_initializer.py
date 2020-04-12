import pytest, os
from src.Constant.constant import constant
from src.utilities.logger import Logger
from pluggy import HookspecMarker


class MyPlugin(object):
    hookspec = HookspecMarker("pytest")
    
    def __init__(self):
        Logger.log('Automation Suite Execution Starts...')

    @pytest.hookimpl(tryfirst=True, hookwrapper=True)
    def pytest_runtest_makereport(item, call):
        outcome = yield
        rep = outcome.get_result() 
        if rep.when == 'call' or (rep.when == 'setup' and rep.outcome in ['failed', 'skipped']):
            classRunning = str(rep).split('::')[1]
            testCaseName = str(rep).split('::')[-1].split('when')[0].rstrip().replace("'", '')
            status = rep.outcome
            timeTaken = rep.duration
            executionInfo = call.excinfo
            screenshot = ''
            if status == 'failed':
                path = constant.config['logDir'] + '/' + str(testCaseName) + '.png'
                if os.path.exists(path):
                    screenshot = str(testCaseName) + '.png'
            if executionInfo is None:
                executionInfo = ''
            else:
                executionInfo = str(executionInfo)
            if constant.config['validataionMessage'] != []:
                #executionInfo += '\n'.join(set(constant.config['validataionMessage']))
                executionInfo = str(executionInfo)
            resultDict = {classRunning : {testCaseName : {'status' : status, 'time' : str(timeTaken),
                'validataionMessage' : executionInfo, 'screenshot' : screenshot, 'comments' : ''}}}
            Logger.logCollectorRequest(resultDict, 'result')
        setattr(item, "rep_" + rep.when, rep)
