import base64
import hashlib
import json
import os
import pyrabbit
import requests
import shutil
import socket
import subprocess
import time
import uuid
from datetime import datetime
from itertools import cycle

from pyrabbit.api import Client
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from src.Constant.constant import constant
from src.utilities.logger import Logger
from src.utilities.assertion import Assertion

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class Utils():
    @staticmethod
    def getRabbitmqQueueDetails(queueName, host='/'):
        cluster = constant.config['cluster']
        url = constant.rabbitmqCred[cluster]
        user = constant.rabbitmqCred['username']
        passwd = constant.rabbitmqCred['passwd']
        obj = Client(url, user, passwd)
        try:
            return obj.get_queue(vhost=host, name=queueName)
        except pyrabbit.http.HTTPError:
            return {}

    @staticmethod
    def createFolder(directory):
        if not os.path.exists(directory):
            try:
                os.makedirs(directory)
            except OSError:
                Logger.log(directory, ' already exists')

    @staticmethod
    def deleteFile(path):
        os.remove(path)

    @staticmethod
    def deleteFolder(path):
        shutil.rmtree(path)

    @staticmethod
    def sorted_ls(path):
        mtime = lambda f: os.stat(os.path.join(path, f)).st_mtime
        return list(sorted(os.listdir(path), key=mtime))

    @staticmethod
    def generateGUID():
        return str(uuid.uuid4())

    @staticmethod
    def getTime(days=0, hours=0, minutes=0, seconds=0, milliSeconds=False, microSeconds=False, dateTimeFormat=False):
        tmpTime = int(time.time()) + int(days) * 86400 + int(hours) * 3600 + int(minutes) * 60 + int(seconds)
        if microSeconds:
            return tmpTime * 1000000
        elif milliSeconds:
            return tmpTime * 1000
        elif dateTimeFormat:
            return time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(tmpTime))
        else:
            return tmpTime

    @staticmethod
    def getFirstDayofMonth(milliSeconds=False):
        value = datetime.today().replace(day=1).replace(hour=6).strftime('%s')
        if milliSeconds:
            return int(value) * 1000
        else:
            return int(value)

    @staticmethod
    def md5string(string):
        m = hashlib.md5()
        m.update(string)
        return m.hexdigest()

    @staticmethod
    def authorizationHeader(username, password):
        encodedauth = base64.b64encode(username + ':' + Utils.md5string(password))
        encodedauth = {"Authorization": "Basic " + encodedauth}
        return encodedauth

    @staticmethod
    def makeRequest(url, data, headers, method, auth='', cookie='', files=None, timeout=50, logging=True):
        method = str(method).upper()
        if isinstance(data, (dict, list)):
            data = json.dumps(data, indent=4)
        if logging:
            Logger.log('url: ', url, ' auth: ', auth, ' headers: ', headers, ' data: ', data, ' method: ', method)
        rq_start = time.time()
        if method == 'GET':
            if 'iris' in constant.config['module']:
                socketTimeoutMessage = 'Read timed out'
                for _ in range(0, 3):
                    r = requests.get(url, headers=headers, auth=auth, verify=False, timeout=timeout)
                    if 'errors' in r.json():
                        if len(r.json()['errors']) > 0 and socketTimeoutMessage in r.json()['errors'][0]['message']:
                            time.sleep(2)
                        else:
                            break
                    else:
                        break
            else:
                r = requests.get(url, headers=headers, auth=auth, verify=False, timeout=timeout)
        elif method == 'POST':
            if files is None:
                if 'iris' in constant.config['module']:
                    socketTimeoutMessage = 'Read timed out'
                    for _ in range(0, 3):
                        r = requests.post(url, data=data, headers=headers, auth=auth, verify=False, cookies=cookie,
                                              timeout=timeout)
                        if 'errors' in r.json():
                            if socketTimeoutMessage in r.json()['errors'][0]['message']:
                                time.sleep(2)
                            else:
                                break
                        else:
                            break
                else:
                    r = requests.post(url, data=data, headers=headers, auth=auth, verify=False, cookies=cookie,
                                      timeout=timeout)
            else:
                if 'iris' in constant.config['module']:
                    socketTimeoutMessage = 'Read timed out'
                    streamNotFound = 'Uploaded audience file is empty'
                    for _ in range(0, 3):
                        r = requests.post(url, data=data, headers=headers, auth=auth, verify=False, cookies=cookie,
                                          files=files, timeout=timeout)
                        if 'errors' in r.json():
                            if socketTimeoutMessage in r.json()['errors'][0]['message']:
                                Logger.log('Read Time out Caught , sleep For 2 Secs and make a re request')
                                time.sleep(2)
                            elif streamNotFound in r.json()['errors'][0]['message']:
                                files[1][1][1] = open(files[1][1][1].name,'r')
                            else:
                                break
                        else:
                            break
                else:
                    r = requests.post(url, data=data, headers=headers, auth=auth, verify=False, cookies=cookie,
                                      files=files, timeout=timeout)

        elif method == 'DELETE':
            r = requests.delete(url, headers=headers, auth=auth, verify=False, timeout=timeout)
        elif method == 'PUT':
            r = requests.put(url, data=data, headers=headers, auth=auth, verify=False, timeout=timeout)
        elif method == 'PATCH':
            r = requests.patch(url, data=data, headers=headers, auth=auth, verify=False, timeout=timeout)
        else:
            Logger.log("Invalid method name:", method)
            raise RuntimeError("Invalid Method:", method)
        rq_total = time.time() - rq_start
        if logging:
            Logger.log('http_code: ', r.status_code, ' headers: ', r.headers, ' response: ', r.content, ' time:',
                       rq_total)
        return r

    @staticmethod
    def restartTunnel(port):
        if Utils.socketConnection('127.0.0.1', 6000):
            r = requests.get('http://127.0.0.1:6000/tunnel?command=restart&port=' + str(port))
            Logger.log(r.content)
            if 'restart' in r.content.lower():
                time.sleep(5)
                return True
            else:
                return False
        else:
            Logger.log('Tunnel Manager is not running')
            return False

    @staticmethod
    def socketConnection(server, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if sock.connect_ex((server, port)) == 0:
            sock.close()
            return True
        else:
            sock.close()
            return False

    @staticmethod
    def checkServerConnection(thriftEndpoint, thriftName, moduleName, ignoreConnectionError):
        portList = constant.config[thriftEndpoint]
        if isinstance(portList, list):
            newList = []
            for port in portList:
                for _ in range(0, 3):
                    try:
                        obj = thriftName(port, 10000)
                        if obj.isAlive():
                            obj = thriftName(port)  # create new conn obj with timeout set in thrift file
                            constant.config[str(port) + '_obj'] = obj
                            newList.append(port)
                            break
                    except Exception as e:
                        Logger.log('Error connecting to port:', port,
                                   ' .Issuing tunnelrestart.')  # (traceback.format_exc())
                        Utils.restartTunnel(port)
            if newList == []:
                if not ignoreConnectionError:
                    raise Exception(e)
            else:
                constant.config[moduleName] = cycle(newList)
        else:
            for _ in range(0, 3):
                try:
                    obj = thriftName(portList, 10000)
                    if obj.isAlive():
                        obj = thriftName(portList)  # create new conn obj with timeout set in thrift file
                        constant.config[str(portList) + '_obj'] = obj
                        constant.config[moduleName] = portList
                        return
                except Exception as e:
                    Logger.log('Error connecting to port:', portList,
                               ' .Issuing tunnelrestart.')  # (traceback.format_exc())
                    Utils.restartTunnel(portList)
            else:
                if not ignoreConnectionError:
                    raise Exception(e)

    @staticmethod
    def shellCall(exeString):
        p = subprocess.Popen([exeString], stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        if err is not None:
            Logger.log('shell error ', err)
        return output

    @staticmethod
    def mergeDict(a, b):
        if isinstance(b, dict):
            for k, v in b.items():
                if k in a:
                    a[k] = Utils.mergeDict(a[k], v)
                else:
                    a[k] = v
            return a
        else:
            return b

    @staticmethod
    def sleep(t):
        Logger.log('sleeping for ' + str(t) + ' seconds')
        time.sleep(t)
