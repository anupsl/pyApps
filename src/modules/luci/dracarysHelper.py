import time,json
from datetime import datetime
from datetime import timedelta
from src.Constant.constant import constant
from src.utilities.randValues import randValues
from src.utilities.fileHelper import FileHelper
from src.modules.luci.dracarysThrift import DracarysThrift
from src.modules.luci.dracarysObject import DracarysObject
from src.utilities.utils import Utils
from src.utilities.logger import Logger
from src.utilities.assertion import Assertion


class DracarysHelper():

    @staticmethod
    def checkDracarysConn(ignoreConnectionError=False):
        Utils.checkServerConnection('DRACARYS_THRIFT_SERVICE', DracarysThrift, 'dracarysPort', ignoreConnectionError)

    @staticmethod
    def getConnObj(newConnection=False):
        port = constant.config['dracarysPort'].next()
        connPort = str(port)+'_obj'
        if connPort in constant.config:
            if newConnection:
                constant.config[connPort].close()
                constant.config[connPort] = DracarysThrift(port)
            return constant.config[connPort]
        else:
            return DracarysThrift(port)

    @staticmethod
    def saveCouponExpiryReminder(self, reminderInfoList = [], isConfigupdate = False, updateConfigScheduler = {}):
        couponReminderDetailsObjList = []
        couponReminderResponseDict = []
        reminderIds = []
        messageIds = []

        if not isConfigupdate:
            for reminderInfo in reminderInfoList:
                if len(reminderInfo) == 4:
                    couponReminderRequestDict = {'couponSeriesId': self.couponSeriesId, 'numDaysBeforeExpiry': reminderInfo[0], 'hourOfDay': reminderInfo[1], 'minuteOfHour': reminderInfo[2], 'reminderMessages' :  DracarysHelper.messageConstruct(self,reminderInfo[3])}
                else:
                    couponReminderRequestDict = {'couponSeriesId': self.couponSeriesId, 'numDaysBeforeExpiry': reminderInfo[0], 'hourOfDay': reminderInfo[1], 'minuteOfHour': reminderInfo[2]}
                couponReminderDetailsObjList.append(DracarysObject.CouponReminderDetails(couponReminderRequestDict))
        else:
            for couponReminderDetails, updateSchedule in zip(updateConfigScheduler['couponReminderDetails'],updateConfigScheduler['updateScheduler']):
                couponReminderDetails.update({'numDaysBeforeExpiry': updateSchedule[0], 'hourOfDay': updateSchedule[1], 'minuteOfHour': updateSchedule[2]})
                couponReminderDetailsObjList.append(DracarysObject.CouponReminderDetails(couponReminderDetails))

        saveCouponReminderRequest = DracarysObject.SaveCouponReminderRequest({'couponSeriesId': self.couponSeriesId, 'couponReminderDetails': couponReminderDetailsObjList})
        couponsReminderResponseObj = self.DracraysConnObj.saveCouponReminder(saveCouponReminderRequest)
        for k in couponsReminderResponseObj:
            couponReminderResponseDict.append(k.__dict__)
        for k in couponReminderResponseDict:
            if k['reminderMessages'] != []:
                reminderIds.append(k['id'])
                for l in k['reminderMessages']:
                    l = l.__dict__
                    messageIds.append(l['id'])
        return couponReminderResponseDict,reminderIds,messageIds

    @staticmethod
    def saveExpiryReminderAssertion(self, actualResponse, expectedResponse):
        for actual, expected in zip(actualResponse, expectedResponse):
            Assertion.constructAssertion(actual['numDaysBeforeExpiry'] == expected[0], 'No of days Before Expiry Actual : {} and Expected : {}'.format(actual['numDaysBeforeExpiry'], expected[0]))
            Assertion.constructAssertion(actual['hourOfDay'] == expected[1], 'Hour of day Actual : {} and Expected : {}'.format(actual['hourOfDay'], expected[1]))
            Assertion.constructAssertion(actual['minuteOfHour'] == expected[2], 'Minute of Hour Actual : {} and Expected : {}'.format(actual['minuteOfHour'], expected[2]))
            Assertion.constructAssertion(actual['couponSeriesId'] == self.couponSeriesId, 'Reminder Message CouponSeriesId Actual : {} and Expected : {}'.format(actual['couponSeriesId'], self.couponSeriesId))

    @staticmethod
    def getCouponReminder(self):
        getCouponReminderRequest = DracarysObject.GetCouponReminderRequest({'couponSeriesId': self.couponSeriesId})
        self.DracraysConnObj.getCouponReminders(getCouponReminderRequest)


    @staticmethod
    def messageConstruct(self, reminderMessages):
        # SMS = 0; EMAIL = 1; WECHAT = 2; MOBILE_PUSH = 3
        reminderMessageList = []
        for reminderMessageDict in reminderMessages:
            reminderMessageRequest = {'type' : reminderMessageDict['type']}
            if reminderMessageDict['type'] is 0:
                messageObj = {'smsMessage' : DracarysObject.smsMessage(reminderMessageDict['message'])}
                reminderMessageRequest.update(messageObj)
            elif reminderMessageDict['type'] is 1:
                messageObj = {'emailMessage' : DracarysObject.emailMessage(reminderMessageDict['message'])}
                reminderMessageRequest.update(messageObj)
            elif reminderMessageDict['type'] is 2:
                messageObj = { 'wechatMessage' : DracarysObject.wechatMessage(reminderMessageDict['message'])}
                reminderMessageRequest.update(messageObj)
            elif reminderMessageDict['type'] is 3:
                messageObj = { 'mobilePushMessage' : DracarysObject.mobilePushMessage(reminderMessageDict['message'])}
                reminderMessageRequest.update(messageObj)
            reminderMessageList.append(DracarysObject.CouponReminderMessageDetails({'reminderMessage' : DracarysObject.reminderMessage(reminderMessageRequest)}))
        return reminderMessageList

    @staticmethod
    def getValueOfDay(minsToAdd = 0):
        if constant.config['cluster'] in ['eu']:
            dateTime = datetime.utcnow() + timedelta(minutes=minsToAdd)
        elif constant.config['cluster'] == 'china':
            dateTime = datetime.utcnow() + timedelta(hours=8, minutes=minsToAdd)
        else:
            dateTime = datetime.now() + timedelta(minutes=minsToAdd)
        dateTimeDict =  {'year' : dateTime.year, 'month' : dateTime.month, 'day' : dateTime.day, 'hour' : dateTime.hour, 'mins' : dateTime.minute, 'sec' : dateTime.second, 'dayOfWeek' : (datetime.today().weekday() + 1)}
        return dateTimeDict

    @staticmethod
    def generateCouponCode(isAlphaNumeric = True, size = 9):
        if isAlphaNumeric:
            return randValues.randomString(size).upper()
        else:
            return str(randValues.randomInteger(size))

    @staticmethod
    def s3FileUpload(self, couponSeriesId):
        url = constant.config['intouchUrl'] + '/coupon/api/v1/upload/s3file/{}?time={}'.format(couponSeriesId , Utils.getTime(milliSeconds=True))
        uploadFile = constant.luciS3FilePath
        Data = open(uploadFile, 'rb')
        file = {'file': ('uploadCoupon.csv', Data, 'text/csv')}
        header = {'Cookie': constant.config['intouchCookie']}
        try:
            response = Utils.makeRequest(url= url, data='', files= file, headers= header, method= 'POST')
            response = json.loads(response.content)
            response = response['result']
            return response['fileName']
        except Exception, exp:
            raise Exception('s3File upload failed because of errorMessage: {} and NodeAPI: {}'.format(exp, url))

    @staticmethod
    def s3FileDownload(self, s3FileName):
        url = constant.config['intouchUrl'] + constant.downloadS3File + str(Utils.getTime(milliSeconds=True))
        param = {'fileName' : s3FileName}
        header = {'Cookie': constant.config['intouchCookie'], 'Content-Type': 'application/json'}
        try:
            response = Utils.makeRequest(url= url, data=param, headers= header, method= 'POST')
            return response.content
        except Exception, exp:
            raise Exception('s3File upload failed because of errorMessage: {} and NodeAPI: {}'.format(exp, url))

    @staticmethod
    def generateCouponUploadFile(self, identifier = 'userId', isUserTagged = False, isOnlyUser = False, noOfRecords = 1, is_Invalid = [False,False], couponCodeCAPS = True):
        couponUploadFile = constant.luciS3FilePath
        filehandle = FileHelper(couponUploadFile)
        First = True
        data = []
        filehandle.eraseContentFromFile()
        if isUserTagged and not isOnlyUser:
            filehandle.appendToFile('Coupon Code, issuedTo')
            for i in range(noOfRecords):
                if not couponCodeCAPS:
                    couponCode = DracarysHelper.generateCouponCode().lower()
                else:
                    couponCode = DracarysHelper.generateCouponCode()
                    if First:
                        duplicateCoupon = couponCode + ', ' + str(constant.config['usersInfo'][i][identifier])
                        First = False
                filehandle.appendToFile(couponCode + ', ' + str(constant.config['usersInfo'][i][identifier]))
                data.append(couponCode)
            if is_Invalid[0]:
                filehandle.appendToFile(duplicateCoupon)
            elif is_Invalid[1]:
                couponCode = DracarysHelper.generateCouponCode()
                if identifier == 'mobile':
                    filehandle.appendToFile(couponCode + ', ' + str(randValues.getRandomMobileNumber()))
                elif identifier == 'email':
                    filehandle.appendToFile(couponCode + ', ' + str(randValues.randomEmailId()))
                elif identifier in ['userId' , 'externalId']:
                    filehandle.appendToFile(couponCode + ', ' + str(randValues.randomInteger(digits=8)))
        elif isOnlyUser:
            filehandle.appendToFile('issuedTo')
            for i in range(noOfRecords):
                filehandle.appendToFile(str(constant.config['usersInfo'][i][identifier]))
            if is_Invalid[0]:
                filehandle.appendToFile(str(constant.config['usersInfo'][0][identifier]))
            elif is_Invalid[1]:
                if identifier == 'mobile':
                    filehandle.appendToFile(str(randValues.getRandomMobileNumber()))
                elif identifier == 'email':
                    filehandle.appendToFile(str(randValues.randomEmailId()))
                elif identifier in ['userId' , 'externalId']:
                    filehandle.appendToFile(str(randValues.randomInteger(digits=8)))
        else:
            filehandle.appendToFile('Coupon Code')
            for _ in range(noOfRecords):
                if not couponCodeCAPS:
                    couponCode = DracarysHelper.generateCouponCode().lower()
                else:
                    couponCode = DracarysHelper.generateCouponCode()
                if First:
                    duplicateCoupon = couponCode
                    filehandle.appendToFile(duplicateCoupon)
                    data.append(duplicateCoupon)
                    First = False
                else:
                    filehandle.appendToFile(couponCode)
                    data.append(couponCode)
            if is_Invalid[0]:
                filehandle.appendToFile(duplicateCoupon)
            elif is_Invalid[1]:
                filehandle.appendToFile(DracarysHelper.generateCouponCode(size=21))

        return data

    @staticmethod
    def uploadCoupons(self, couponSeriesId, onlyUser = False, identifierType = 'userId', userTaggedCoupons = False, noOfCouponUpload = 1, is_invalidCase= [False, False], expectedError = 0, couponISCAPS = True):
        if  is_invalidCase[0] and is_invalidCase[1]:
            couponCodeList = []
            is_invalidCase = [False, False]
        else:
            couponCodeList = DracarysHelper.generateCouponUploadFile(self, identifier =identifierType, isOnlyUser=onlyUser, isUserTagged=userTaggedCoupons, noOfRecords=noOfCouponUpload, is_Invalid=is_invalidCase, couponCodeCAPS=couponISCAPS)
        s3UploadFileName = DracarysHelper.s3FileUpload(self, couponSeriesId)
        valuesToReturn = {'coupons' : couponCodeList, 'errors' : []}
        uploadRequestDict = {'S3FilePath' : s3UploadFileName, 'couponSeriesId' : couponSeriesId,  'uploadedFileName' : constant.config['uploadedFileName'], 'custIdentifierType' : self.DracarysObj.CustomerIdentifierType[identifierType]}
        if onlyUser:
            uploadRequestDict.update({'uploadHeaders' : {identifierType : 0}})
        elif identifierType == 'notTagged':
            uploadRequestDict.update({'uploadHeaders' : {'couponCode' : 0}})
        else:
            uploadRequestDict.update({'uploadHeaders' : {'couponCode' : 0, identifierType : 1}})

        response = self.DracraysConnObj.uploadCoupons(DracarysObject.couponUploadRequest(uploadRequestDict)).__dict__
        jobId = response['jobId']
        for _  in range(10):
            getUploadStatus = self.DracraysConnObj.getUploadStatusForCouponSeries(DracarysObject.getCouponUploadStatus({'couponSeriesId': couponSeriesId})).__dict__
            uploadStatusResponse = None
            for uploadStatus in  getUploadStatus['uploadJobStatuses']:
                uploadStatus = uploadStatus.__dict__
                if jobId == uploadStatus['jobId']:
                    uploadStatusResponse = uploadStatus
            if uploadStatusResponse['uploadStatus'] == 3:
                if uploadStatusResponse['errorCount'] != 0:
                    errorFile = uploadStatusResponse['errorFileUrl']
                    data = DracarysHelper.s3FileDownload(self,errorFile).splitlines()
                    dataiters = iter(data)
                    isHeader = True
                    for x in dataiters:
                        if isHeader:
                            header = x.split(',')
                            isHeader = False
                        else:
                            if 'issued, ' in x:
                                x = x.replace('issued, ', 'issued ')
                            y = x.split(',')
                            if len(header) == 3:
                                valuesToReturn['errors'].append({'ErrorMsg' : y[0], 'CouponCode' : y[1], 'UserId' : y[2].strip() if y[2].strip() == 'NA' else int(y[2])})
                            elif len(header) == 2:
                                valuesToReturn['errors'].append({'ErrorMsg': y[0], 'CouponCode': y[1]})
                if is_invalidCase[0] or is_invalidCase[1]:
                    Assertion.constructAssertion(uploadStatusResponse['totalUploadedCount'] == (noOfCouponUpload+1), 'Total uploaded count Mismatch Actual: {} & Expected: {}'.format(uploadStatusResponse['totalUploadedCount'], (noOfCouponUpload+1)))
                else:
                    Assertion.constructAssertion(uploadStatusResponse['totalUploadedCount'] == noOfCouponUpload, 'Total uploaded count Mismatch Actual: {} & Expected: {}'.format(uploadStatusResponse['totalUploadedCount'], noOfCouponUpload))
                Assertion.constructAssertion(uploadStatusResponse['errorCount'] == expectedError, 'ErrorCount count Mismatch Actual: {} & Expected: {}'.format(uploadStatusResponse['errorCount'], expectedError))
                return valuesToReturn
            elif uploadStatusResponse['uploadStatus'] == 4:
                Assertion.constructAssertion(False, 'Upload File status for coupon Series: {} is ERRORED '.format(couponSeriesId))
            time.sleep(1)
        return valuesToReturn

    @staticmethod
    def downloadCouponsRequestAndAssertion(self,couponSeriesId, reportType, couponCode = []):
        requestObj = DracarysObject.DownloadCouponsRequest({'couponSeriesId' : couponSeriesId, 'downloadReportType' :  reportType})
        dcrResponse = self.DracraysConnObj.downloadCouponsReport(requestObj).__dict__
        Assertion.constructAssertion(dcrResponse['errorCode'] == 0, 'Error Code is Actual : {} and Expected : 0'.format(dcrResponse['errorCode']))
        Assertion.constructAssertion(dcrResponse['errorMessage'] == None, 'Error Message is Actual : {} and Expected : None'.format(dcrResponse['errorMessage']))
        Assertion.constructAssertion(dcrResponse['jobId'] != None, 'JobId is Actual : {} and Expected : not None'.format(str(dcrResponse['jobId'])))
        Assertion.constructAssertion(dcrResponse['downloadReportType'] == reportType, 'Download report type is Actual : {} and Expected : {}'.format(str(dcrResponse['downloadReportType']),str(reportType)))
        Assertion.constructAssertion(dcrResponse['couponSeriesId'] == couponSeriesId, 'Requested Coupon series Id  is Mismatch Actual : {} and Expected : {}'.format(str(dcrResponse['couponSeriesId']),str(couponSeriesId)))
        DracarysHelper.getDownloadStatusAndAssertion(self,couponSeriesId, dcrResponse['jobId'], reportType,couponCode)

    @staticmethod
    def getDownloadStatusAndAssertion(self,couponSeriesId,jobId,reportType, couponCode = []):
        requestsStatusObj = DracarysObject.GetDownloadStatus({'couponSeriesId': couponSeriesId, 'jobId': jobId})
        statusRes = self.DracraysConnObj.getDownloadStatus(requestsStatusObj).__dict__
        for _ in range(10):
            if statusRes['downloadReportJobStatus'] == 2:
                Assertion.constructAssertion(statusRes['errorCode'] == 0, 'Error Code is Actual : {} and Expected : 0'.format(statusRes['errorCode']))
                Assertion.constructAssertion(statusRes['errorMessage'] == None, 'Error Message is Actual : {} and Expected : None'.format(statusRes['errorMessage']))
                Assertion.constructAssertion(statusRes['s3FilePath'] != None, 's3FilePath is not None Actual : {}'.format(statusRes['s3FilePath']))
                Assertion.constructAssertion(statusRes['jobId'] == jobId, 'JobId is Actual : {} and Expected : {}'.format(str(statusRes['jobId']), str(jobId)))
                Assertion.constructAssertion(statusRes['downloadReportType'] == reportType, 'Download report type is Actual : {} and Expected : {}'.format(str(statusRes['downloadReportType']), str(reportType)))
                Assertion.constructAssertion(statusRes['couponSeriesId'] == couponSeriesId, 'Requested Coupon series Id  is Mismatch Actual : {} and Expected : {}'.format(str(statusRes['couponSeriesId']), str(couponSeriesId)))
                Assertion.constructAssertion(statusRes['totalDownloadCount'] == len(couponCode), 'Download Coupon Count  is Mismatch Actual : {} and Expected : {}'.format(str(statusRes['totalDownloadCount']), str(len(couponCode))))
                break
            else:
                time.sleep(1)
                statusRes = self.DracraysConnObj.getDownloadStatus(requestsStatusObj).__dict__

        Assertion.constructAssertion(statusRes['downloadReportJobStatus'] == 2, 'Download Report Failed status is Actual : {} and Expected : 2'.format(str(statusRes['downloadReportJobStatus'])))
        data = DracarysHelper.s3FileDownload(self, statusRes['s3FilePath'])
        dataSplited = data.split('\n')
        if len(couponCode) > 0:
            row1 = couponCode[0] + ',' + str(self.userId)
            Assertion.constructAssertion(row1 in dataSplited , 'Coupon Code  and UserId not Available in downloaded s3File' )