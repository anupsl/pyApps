for i in range(0, 1):
    try:
        import pytest, argparse
        from src.Constant.constant import constant
        from src.initializer.pytest_initializer import MyPlugin
        from src.initializer.baseState import BaseState
        from src.utilities.logger import Logger
        from src.utilities.fileHelper import FileHelper
        from datetime import datetime
        break
    except ImportError as e:
        if i == 0:
            print 'Import Error: ' + str(e) + '. Attempting to fix'
            import setup
else:
    raise Exception(e)

def executeSuite():
    module = constant.config['module']
    tcFilter = constant.config['tcFilter']
    collectOnly = constant.config['collectOnly']
    try:
        testPath = constant.testFolder + module
        reportPath = constant.config['logDir'] + '/result.html'
        if collectOnly:
            pytest.main([testPath, '-k ' + tcFilter, '--collect-only'], plugins=[MyPlugin()])
        else:
            pytest.main([testPath, '--tb=long', '-v' , '--html=' + reportPath, '-k ' + tcFilter], plugins=[MyPlugin()]) # For Debugging -s instead of --tb=line  , '--pdb'
            FileHelper.concateHTMLandCSS()            
    except Exception as e:
        Logger.log('Exception in execution : ', e)
        print e

def parseArguments():
    parser = argparse.ArgumentParser(description='Apps Automation.')
    parser.add_argument('-f', '--filter', dest='tcFilter', default='', help='To run specific testcase or group matching the pattern')
    parser.add_argument('-C', '--collect-only', dest='collectOnly', default=False, help='To get Testcase Count')
    parser.add_argument('-R', '--svn-revision', dest='svnRevision', default=False, help='To get SVN Revision')
    parser.add_argument('-S', '--serially', dest='serially', default=False, help='To run test serially')
    parser.add_argument('-r', '--runId', dest='runId', default=datetime.today().strftime('%Y-%m-%d-%H-%M-%S'), help='Run ID')
    parser.add_argument('-M', '--headlessMode', dest='headlessMode', default=True, help='mode In which UI will Run')
    parser.add_argument('-E', '--email', dest='prodEmail1', default='', help='To set prod Email for NSAdmin')
    requiredNamed = parser.add_argument_group('required named arguments')
    requiredNamed.add_argument('-c', '--cluster', dest='cluster', help='Test Environment', required=True)
    requiredNamed.add_argument('-m', '--module', dest='module', help='Application to test', required=True)
    return parser.parse_args()


BaseState.initializeConstants(parseArguments())
executeSuite()

