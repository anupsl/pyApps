from src.Constant.constant import constant
from src.initializer.generateThrift import dracarys
from src.utilities.logger import Logger
from thriftpy.rpc import make_client



class DracarysThrift(object):

    def __init__(self, port, timeout=60000):
        self.conn = make_client(dracarys.DracarysService, '127.0.0.1', port, timeout=timeout)

    def log(self, output):
        Logger.log(output)
        return output

    def close(self):
        Logger.log('Closing DracarysThrift connection')
        self.conn.close()

    def isAlive(self):
        return self.log(self.conn.isAlive())

    def uploadCoupons(self, couponUploadRequest):
        Logger.log("Upload Coupons Request : ", couponUploadRequest)
        return self.log(self.conn.uploadCoupons(couponUploadRequest))

    def getUploadStatusForCouponSeries(self, getCouponUploadStatusRequest):
        Logger.log("Get Coupon Upload Status Request : ", getCouponUploadStatusRequest)
        return self.log(self.conn.getUploadStatusForCouponSeries(getCouponUploadStatusRequest))

    def saveCouponReminder(self, saveCouponReminderRequest):
        Logger.log("Save Coupon Reminder Request : ", saveCouponReminderRequest)
        return self.log(self.conn.saveCouponReminder(saveCouponReminderRequest))

    def getCouponReminders(self, getCouponReminderRequest):
        Logger.log("Get Coupon Reminders Request : ", getCouponReminderRequest)
        return self.log(self.conn.getCouponReminders(getCouponReminderRequest))

    def downloadCouponsReport(self, downloadCouponsReportRequest):
        Logger.log("Download Coupon Request : ", downloadCouponsReportRequest)
        return self.log(self.conn.downloadCouponsReport(downloadCouponsReportRequest))

    def getDownloadStatus(self, getDownloadStatus):
        Logger.log("Get Download Status Request : ", getDownloadStatus)
        return self.log(self.conn.getDownloadReportStatus(getDownloadStatus))