import subprocess, re, os
from StringIO import StringIO
from zipfile import ZipFile
from urllib import urlopen
from src.Constant.constant import constant
from src.utilities.logger import Logger
from src.utilities.utils import Utils

class ChromeDriverManager():

    @staticmethod
    def getCurrentChromeVersion():
        if constant.config['os'] == 'linux':
            currentChromeVersion = Utils.shellCall('/usr/bin/google-chrome --version')
            return int(float(re.findall('([0-9][0-9]\.[0-9])', currentChromeVersion)[0]))
        else:
            spath = r'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe'
            cargs = ["wmic","datafile","where", r'name="{0}"'.format(spath), "get", "Version", "/value"]
            process = subprocess.check_output(cargs)
            currentChromeVersion = process.strip().decode()
            return int(float(re.findall('([0-9][0-9]\.[0-9])', currentChromeVersion)[0]))

    @staticmethod
    def getCurrentChromeDriverVersion():
        currentChromeDriverVersion = Utils.shellCall(constant.chromeDriverPath+' --version')
        return float(re.findall('([0-9]\.[0-9][0-9])', currentChromeDriverVersion)[0])

    @staticmethod
    def getChromeDriverMatrix():
        latestVersion = str(urlopen(constant.chromeDriverUrl+'LATEST_RELEASE').read())
        releaseNotes = urlopen(constant.chromeDriverUrl+latestVersion+'/notes.txt').read()
        versionList = re.findall('-ChromeDriver v(.*)[(](.*)\nSupports Chrome (.*)\n', releaseNotes)
        supportedRange = {}
        for ver in versionList:
            cdVersion = float(ver[0].strip())
            supportedChromeRange = ver[2].replace('v','').split('-')
            minCR = int(supportedChromeRange[0])
            maxCR = int(supportedChromeRange[1]) + 1
            for m in range(minCR, maxCR):
                if not m in supportedRange:
                    supportedRange[m] = []
                supportedRange[m].append(cdVersion)
        return supportedRange

    @staticmethod
    def checkChromeDriverCompatibility():
        Logger.log('Checking Chrome Driver compatibility')
        currentChromeVersion = ChromeDriverManager.getCurrentChromeVersion()
        currentChromeDriverVersion = ChromeDriverManager.getCurrentChromeDriverVersion()
        Logger.log('currentChromeVersion: ',currentChromeVersion, ' currentChromeDriverVersion: ',currentChromeDriverVersion)
        supportedRange = ChromeDriverManager.getChromeDriverMatrix()
        Logger.log('supportedRange: ',supportedRange)
        if currentChromeVersion in supportedRange:
            if currentChromeDriverVersion in supportedRange[currentChromeVersion]:
                return True, 0
            else:
                if len(supportedRange[currentChromeVersion]) > 2:
                    return False, supportedRange[currentChromeVersion][1]
                else:
                    return False, supportedRange[currentChromeVersion][0]

    @staticmethod
    def downloadChromeDriver(version):
        if constant.config['os'] == 'windows':
            url = constant.chromeDriverUrl+str(version)+'/chromedriver_win32.zip'
        else:
            url = constant.chromeDriverUrl+str(version)+'/chromedriver_linux64.zip'
        Logger.log('Downloading: ',url)
        urlObj = urlopen(url)
        zipfile = ZipFile(StringIO(urlObj.read()))
        zipfile.extractall(os.path.dirname(constant.chromeDriverPath))
        zipfile.close()

