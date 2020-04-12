from src.Constant.constant import constant
from src.initializer.generateThrift import luci
from src.utilities.logger import Logger
from thriftpy.rpc import make_client



class LuciThrift(object):

    def __init__(self, port, timeout=60000):
        self.conn = make_client(luci.LuciService, '127.0.0.1', port, timeout=timeout)

    def log(self, output):
        Logger.log(output)
        return output

    def close(self):
        Logger.log('Closing LuciThrift connection')
        self.conn.close()

    def isAlive(self):
        return self.log(self.conn.isAlive())

    def saveCouponConfiguration(self, saveConfigObj):
        Logger.log("Save Coupon Config Request : ", saveConfigObj )
        return self.log(self.conn.saveCouponConfiguration(saveConfigObj))

    def getCouponConfiguration(self,configRequestObj):
        Logger.log("Get Coupon Config Request : ", configRequestObj)
        return self.log(self.conn.getCouponConfiguration(configRequestObj))

    def issueCoupon(self, issueCouponRequestObj):
        Logger.log("Issue Coupon Code Request : ", issueCouponRequestObj)
        return self.log(self.conn.issueCoupon(issueCouponRequestObj))

    def issueMultipleCoupons(self, issueMultipleCouponRequestObj):
        Logger.log("Issue Multiple Coupon Code Request : ", issueMultipleCouponRequestObj)
        return self.log(self.conn.issueMultipleCoupons(issueMultipleCouponRequestObj))

    def issuePartnerCoupon(self, issuePartnerCouponsRequestObj):
        Logger.log("Partner Coupon issue Request : ", issuePartnerCouponsRequestObj)
        return self.log(self.conn.issuePartnerCoupons(issuePartnerCouponsRequestObj))

    def getCouponDetails(self, couponDetailsRequest):
        Logger.log("Get Coupon Details Request : ", couponDetailsRequest)
        return self.log(self.conn.getCouponDetails(couponDetailsRequest))

    def redeemCoupons(self, redeemCouponsRequest):
        Logger.log("Redeem Coupon Request : ", redeemCouponsRequest)
        return self.log(self.conn.redeemCoupons(redeemCouponsRequest))

    def couponSearch(self, couponSearchRequest):
        Logger.log("Coupon Search Request : ", couponSearchRequest)
        return self.log(self.conn.couponSearch(couponSearchRequest))

    def getQueueSize(self, orgId, couponSeriesId, requestId):
        Logger.log('Get Loaded Coupon Code Count from Queue : orgId - ', orgId , ' - Coupon Series Id - ', couponSeriesId , ' - requestId -', requestId)
        return self.log(self.conn.getQueueSize(orgId, couponSeriesId, requestId))

    def uploadCoupons(self, UploadCouponsRequest):
        Logger.log("Upload CouponCode Request : ", UploadCouponsRequest)
        return self.log(self.conn.uploadCoupons(UploadCouponsRequest))

    def invalidateCoupons(self, InvalidateCouponRequest):
        Logger.log("Invalidate Coupon Request : ", InvalidateCouponRequest)
        return self.log(self.conn.invalidateCoupons(InvalidateCouponRequest))

    def createCoupons(self, CouponCreateRequest):
        Logger.log("Create Coupons Request : ", CouponCreateRequest)
        return self.log(self.conn.createCoupons(CouponCreateRequest))

    def resendCoupon(self, ResendCouponRequest):
        Logger.log("Resend Coupon Request : ", ResendCouponRequest)
        return self.log(self.conn.resendCoupon(ResendCouponRequest))

    def claimCouponConfig(self, claimCouponConfigRequest):
        Logger.log("Claim Coupon Config Request : ", claimCouponConfigRequest)
        return self.log(self.conn.claimCouponConfig(claimCouponConfigRequest))

    def getAllCouponConfigurations(self, getAllCouponConfigRequest):
        Logger.log("Coupon Config Request : ", getAllCouponConfigRequest)
        return self.log(self.conn.getAllCouponConfigurations(getAllCouponConfigRequest))

    def changeCouponIssuedDate(self, couponId, issuedDate):
        Logger.log('Change Coupon issued Date for orgId : {}  couponId : {} Requesting Issued Date : {} and requestId : {}'.format( constant.config['orgId'] , couponId, issuedDate , constant.config['requestId']))
        return self.log(self.conn.changeCouponIssuedDate(constant.config['orgId'],  couponId, issuedDate, constant.config['requestId']))

    def saveOrgDefaults(self, saveOrgDefaultsRequest):
        Logger.log("Save org Default Request : ", saveOrgDefaultsRequest )
        return self.log(self.conn.saveOrgDefaults(saveOrgDefaultsRequest))

    def getRevokeHistory(self, getRevokeHistoryRequest):
        Logger.log("Get Revoke History Request : ", getRevokeHistoryRequest )
        return self.log(self.conn.getRevokeHistory(getRevokeHistoryRequest))

    def notifyCouponsUpload(self, notifyCouponsUploadRequest):
        Logger.log("Notify coupons upload Request : ", notifyCouponsUploadRequest )
        return self.log(self.conn.notifyCouponsUploadRequest(notifyCouponsUploadRequest))

    def mergeUsers(self, fromUserId, toUserId, mergedbyTillId):
        Logger.log("MergeUser orgId: {}  fromUserId: {} toUserId: {}  from TillId: {}: RequestId: {}".format(constant.config['orgId'], fromUserId, toUserId, mergedbyTillId, constant.config['requestId']))
        return self.log(self.conn.mergeUsers(constant.config['orgId'], fromUserId, toUserId, mergedbyTillId, constant.config['requestId']))

    def getMergeStatus(self, fromUserId, toUserId):
        Logger.log("getMergeStatus orgId: {}  fromUserId: {} toUserId: {} RequestId: {}".format(constant.config['orgId'], fromUserId, toUserId, constant.config['requestId']))
        return self.log(self.conn.getMergeStatus(constant.config['orgId'], fromUserId, toUserId, constant.config['requestId']))