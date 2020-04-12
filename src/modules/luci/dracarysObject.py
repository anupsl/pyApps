import time
from src.Constant.constant import constant
from src.initializer.generateThrift import dracarys
from src.utilities.utils import Utils


class DracarysObject(object):

    def __init__(self):
        self.MessageType = {'SMS': 0, 'EMAIL': 1, 'WECHAT' : 2, 'MOBILE_PUSH' : 3}
        self.ClientHandlingType = {'DISC_CODE' : 0 ,'DISC_CODE_PIN' : 1 ,'DISC_CODE_PIN_CUSTOMER_TAGGED' : 2 ,'EXTERNAL' : 3 ,'GENERIC' : 4}
        self.CustomerIdentifierType = {'mobile' : 0,'email' : 1,'userId' : 2,'externalId' : 3,'notTagged' : 4}
        self.UploadCouponStatus = {'STARTED' : 0 ,'VALIDATED' : 1,'COMMITED' : 2,'FINISHED' : 3,'ERRORED' : 4}
        self.DownloadReportType = {'ISSUED' : 0, 'REDEEMED' : 1}


    @staticmethod
    def couponUploadRequest(couponUploadRequest={}):
        tmpDict = {
            'S3FilePath' : '',
            'commit' : True,
            'orgId' : constant.config['orgId'],
            'requestId' : constant.config['requestId'],
            'couponSeriesId' : 0,
            'uploadedBy' : constant.config['adminId'],
            'uploadHeaders' : {},
            'custIdentifierType' : 0
        }
        tmpDict.update(couponUploadRequest)
        return dracarys.CouponUploadRequest(**tmpDict)

    @staticmethod
    def getCouponUploadStatus(getCouponUploadStatusRequest={}):
        tmpDict = {
            'orgId' : constant.config['orgId'],
            'requestId' : constant.config['requestId'],
            'couponSeriesId' : 0
        }
        tmpDict.update(getCouponUploadStatusRequest)
        return dracarys.GetCouponUploadStatusRequest(**tmpDict)

    @staticmethod
    def smsMessage(smsMessageRequest={}):
        tmpDict = {
            'message' : 'Coupons Reminder Test Message'
        }
        tmpDict.update(smsMessageRequest)
        return dracarys.SmsMessage(**tmpDict)

    @staticmethod
    def emailMessage(emailMessageRequest={}):
        tmpDict = {
            'subject' : 'Reminder Message',
            'emailBody' : 'Coupons Reminder Test Message'
        }
        tmpDict.update(emailMessageRequest)
        return dracarys.EmailMessage(**tmpDict)

    @staticmethod
    def wechatMessage(wechatMessageRequest={}):
        tmpDict = {
            'template' : 'Reminder Message',
            'originalId' : 'Coupons Reminder Test Message',
            'brandId' : 'Coupons Reminder Test Message',
            'wechatId' : 'Coupons Reminder Test Message'
        }
        tmpDict.update(wechatMessageRequest)
        return dracarys.WechatMessage(**tmpDict)

    @staticmethod
    def mobilePushDetails(mobilePushDetailsRequest={}):
        tmpDict = {
            'title' : 'Reminder Message',
            'messageBlob' : 'Coupons Reminder Test Message'
        }
        tmpDict.update(mobilePushDetailsRequest)
        return dracarys.MobilePushMessageDetails(**tmpDict)

    @staticmethod
    def mobilePushMessage(mobilePushMessageRequest={}):
        tmpDict = {
            'accountId' : 'Reminder Message',
            'pushTemplateId' : 'Coupons Reminder Test Message'
        }
        tmpDict.update(mobilePushMessageRequest)
        return dracarys.MobilePushMessage(**tmpDict)

    @staticmethod
    def reminderMessage(reminderMessageRequest={}):
        return dracarys.ReminderMessage(**reminderMessageRequest)

    @staticmethod
    def CouponReminderMessageDetails(couponReminderMessageDetailsDict = {}):
        tmpDict =   {
                        'id' : 0,
                        'orgId' : constant.config['orgId']
                    }
        tmpDict.update(couponReminderMessageDetailsDict)
        return dracarys.CouponReminderMessageDetails(**tmpDict)

    @staticmethod
    def CouponReminderDetails(couponReminderDetailsDict = {}):
        tmpDict =   {
                        'id' : 0,
                        'orgId' : constant.config['orgId'] ,
                        'createdBy' : constant.config['adminId'],
                        'createdOn' : Utils.getTime(milliSeconds=True)
                    }
        tmpDict.update(couponReminderDetailsDict)
        return dracarys.CouponReminderDetails(**tmpDict)

    @staticmethod
    def SaveCouponReminderRequest(saveCouponReminderRequestDict = {}):
        tmpDict =   {
                        'requestId' : constant.config['requestId'],
                        'orgId' : constant.config['orgId'] ,
                        'updatedBy' : constant.config['adminId']
                    }
        tmpDict.update(saveCouponReminderRequestDict)
        return dracarys.SaveCouponReminderRequest(**tmpDict)

    @staticmethod
    def GetCouponReminderRequest(getCouponReminderRequestDict = {}):
        tmpDict =   {
                        'requestId' : constant.config['requestId'],
                        'orgId' : constant.config['orgId']
                    }
        tmpDict.update(getCouponReminderRequestDict)
        return dracarys.GetCouponReminderRequest(**tmpDict)

    @staticmethod
    def DownloadCouponsRequest(request = {}):
        tmpDict =   {
                        'requestId': constant.config['requestId'],
                        'orgId': constant.config['orgId'],
                        'requestedBy' :constant.config['adminId'],
                        'downloadReportType' : 0
                    }
        tmpDict.update(request)
        return dracarys.DownloadCouponsReportRequest(**tmpDict)

    @staticmethod
    def GetDownloadStatus(request = {}):
        tmpDict =   {
                        'requestId': constant.config['requestId'],
                        'orgId': constant.config['orgId']
                    }
        tmpDict.update(request)
        return dracarys.GetDownloadReportStatusRequest(**tmpDict)