import time
from src.Constant.constant import constant
from src.initializer.generateThrift import luci
from src.utilities.randValues import randValues
from src.utilities.utils import Utils


class LuciObject(object):

    def __init__(self):
        self.issualModeEnum = {'NONE': 0, 'USER_IDENTIFIER': 1}
        self.productType = {'BRAND' : 0, 'CATEGORY' : 1, 'SKU' : 2}
        self.importType = {'USER_ID' : 0, 'MOBILE' : 1, 'NONE' : 2, 'EXTERNAL_ID' : 3, 'EMAIL' : 4}
        self.CustomerIdentifierDracarys = ['userId', 'mobile', 'notTagged', 'externalId', 'email']
        self.couponStatus = { 'REDEEMED' : 0, 'EXPIRED' : 1, 'ACTIVE' : 2, 'UNREDEEMED' : 3}
        self.couponSeriesType = { 'CAMPAIGN' : 0, 'DVS' : 1, 'ALLIANCE' : 2, 'GOODWILL' : 3}
        self.orderBy = {'CREATED_DATE' : 0, 'ISSUED_TILL' : 1, 'EXPIRY_DATE' : 2}
        self.sort = {'ASC' : 0, 'DESC' : 1}
        self.ownedBy = {'NONE' : 0, 'LOYALTY' : 1, 'OUTBOUND' : 2, 'GOODWILL' : 3, 'DVS' : 4, 'TIMELINE' : 5, 'REFERRAL' : 6}
        self.redemptionEntityType = {'ZONE' : 0 , 'CONCEPT' : 1 , 'STORE' :2 , 'TILL' : 3}
        self.couponConfigOrderBy = {'CREATED_DATE' : 0, 'LAST_MODIFIED_DATE' : 1}
        self.revokeType = ['COUPON_SERIES', 'ONLY_UNISSUED', 'issuedTo', 'couponCode', 'couponId', 'CUSTOMER_AND_COUPON']

    @staticmethod
    def couponRedemptionDetails(redeemDict = {}):
        tmpDict =   {
                        'redemptionId' : 0,
                        'redemptionDate' : 0
                    }

    @staticmethod
    def externalUserIdentifier():
        tmpDict = {'type' : '', 'value' : ''}

    @staticmethod
    def couponRedemptionCount():
        tmpDict = {'userId' : 0, 'redemptionCount' : 0}

    @staticmethod
    def userProfile(ExternalUserIdentifier):
        tmpList = [ExternalUserIdentifier]

    @staticmethod
    def issuePartnerCouponRequest(requestDict):
        tmpDict =   {
                        'requestId' : constant.config['requestId'],
                        'orgId' : constant.config['orgId'],
                        'couponSeriesId' : 0,
                        'clusterAdminUserId' : 0,
                        'partnerOrgId' : 0,
                        'partnerIssuedById' : 0,
                        'issualMode' : 0,
                        'numCouponsToBeIssued' : 1,
                        'eventTimeInMillis' : Utils.getTime(milliSeconds=True)
                    }
        tmpDict.update(requestDict)
        return luci.IssuePartnerCouponRequest(**tmpDict)

    @staticmethod
    def productInfo(requestDict):
        tmpDict = {'productType' : 1, 'productIds' : []}
        tmpDict.update(requestDict)
        return luci.ProductInfo(**tmpDict)

    @staticmethod
    def couponConfiguration(couponConfigDict = {}):
        tmpDict =   {
                        "id" : 0,
                        "client_handling_type": "DISC_CODE",
                        "org_id": constant.config['orgId'],
                        "created_by": constant.config['adminId'],
                        "campaign_id": constant.config['campaignId'],
                        "created": Utils.getTime(milliSeconds=True),
                        "last_used": Utils.getTime(milliSeconds=True),
                        "redemption_valid_from": Utils.getTime(days=-1, milliSeconds=True),
                        "dvs_expiry_date": Utils.getTime(milliSeconds=True),
                        "series_code": str(Utils.getTime(milliSeconds=True)) + str(randValues.randomInteger(5)),
                        "valid_till_date": Utils.getTime(days=2,milliSeconds=True),
                        "description": "luci testing",
                        "series_type": "CAMPAIGN",
                        "discount_code": "XYZ123",
                        "valid_days_from_create": 30,
                        "expiry_strategy_value": 30,
                        "transferrable": False,
                        "any_user": False,
                        "same_user_multiple_redeem": False,
                        "allow_referral_existing_users": False,
                        "multiple_use": False,
                        "is_validation_required": False,
                        "valid_with_discounted_item": False,
                        "num_issued": 0,
                        "num_redeemed": 0,
                        "sms_template": "",
                        "disable_sms": False,
                        "info": "luci testing",
                        "allow_multiple_vouchers_per_user": False,
                        "do_not_resend_existing_voucher": False,
                        "mutual_exclusive_series_ids": 'false',
                        "store_ids_json": '[-1]',
                        "dvs_enabled": False,
                        "priority": 0,
                        "terms_and_condition": "T&C Apply",
                        "signal_redemption_event": False,
                        "sync_to_client": False,
                        "short_sms_template": "",
                        "max_vouchers_per_user": -1,
                        "min_days_between_vouchers": -1,
                        "max_referrals_per_referee": -1,
                        "show_pin_code": False,
                        "discount_on": "BILL",
                        "discount_type": "ABS",
                        "discount_value": 1,
                        "dvs_items": "",
                        "redemption_range": '{ "dom": ["-1"], "dow": ["-1"],"hours": ["-1"] }',
                        "min_bill_amount": 0,
                        "max_bill_amount": 0,
                        "redeem_at_store": '[-1]',
                        "tag": "",
                        "max_redemptions_in_series_per_user": -1,
                        "min_days_between_redemption": -1,
                        "redeem_store_type": "redeemable_stores",
                        "expiry_strategy_type": "DAYS",
                        "old_flow": False,
                        "max_create": -1,
                        "max_redeem": -1,
                        "pre_redeem_event_required": False,
                        "source_org_id": -1,
                        "issue_to_loyalty": False,
                        "offline_redeem_type": False
                }
        tmpDict.update(couponConfigDict)
        return luci.CouponConfiguration(**tmpDict)

    @staticmethod
    def CouponDetails():
        tmpDict =   {
                        'id' : 0,
                        'orgId' : constant.config['orgId'],
                        'couponSeriesId' : 0,
                        'couponCode' : "",
                        'createdDate' : 0
                    }

    @staticmethod
    def saveCouponConfigRequest(couponConfigDict,saveCouponConfigRequestDict = {}):
        tmpDict =   {
                        'requestId' : constant.config['requestId'] ,
                        'orgId' : constant.config['orgId'] ,
                        'couponConfig' : couponConfigDict ,
                        'modifiedBy' : constant.config['adminId']
                    }
        tmpDict.update(saveCouponConfigRequestDict)
        return luci.SaveCouponConfigRequest(**tmpDict)

    @staticmethod
    def redeemCoupon(requestDict = {}):
        tmpDict =   {
                        'orgId' : constant.config['orgId'] ,
                        'couponCode' : None,
                        'storeUnitId' : 1,
                        'billAmount' : 1000,
                        'billNumber' : str(Utils.getTime(milliSeconds=True)),
                        'eventTimeInMillis' : Utils.getTime(milliSeconds=True)
                    }
        tmpDict.update(requestDict)
        return luci.RedeemCoupon(**tmpDict)

    @staticmethod
    def issueCouponRequest(requestDict = {}):
        tmpDict =   {
                        'requestId' : constant.config['requestId'],
                        'orgId' : constant.config['orgId'],
                        'couponSeriesId' : 0,
                        'storeUnitId' : 0,
                        'userId' : 0,
                        'eventTimeInMillis' : Utils.getTime(milliSeconds=True)
                    }
        tmpDict.update(requestDict)
        return luci.IssueCouponRequest(**tmpDict)

    @staticmethod
    def issualFilters(requestDict = {}):
        return luci.IssualFilters(**requestDict)

    @staticmethod
    def redemptionFilters(requestDict={}):
        return luci.RedemptionFilters(**requestDict)

    @staticmethod
    def resendCouponRequest(requestObj = {}):
        tmpDict =   {
                        'requestId': constant.config['requestId'],
                        'orgId': constant.config['orgId'],
                        'storeUnitId': 0,
                        'eventTimeInMillis': 0
                    }
        tmpDict.update(requestObj)
        return luci.ResendCouponRequest(**tmpDict)

    @staticmethod
    def issueMultipleCouponsRequest(requestObj = {}):
        tmpDict =   {
                        'requestId': constant.config['requestId'],
                        'orgId': constant.config['orgId'],
                        'couponSeriesId': 0,
                        'storeUnitId': 0,
                        'userIds' : [],
                        'eventTimeInMillis' : 0
                    }
        tmpDict.update(requestObj)
        return luci.IssueMultipleCouponsRequest(**tmpDict)

    @staticmethod
    def couponDetailsRequest(requestObj = {}):
        tmpDict =   {
                        'requestId': constant.config['requestId'],
                        'orgId': constant.config['orgId'],
                    }
        tmpDict.update(requestObj)
        return luci.CouponDetailsRequest(**tmpDict)

    @staticmethod
    def couponSearchRequest(requestObj = {}):
        tmpDict =   {
                        'requestId': constant.config['requestId'],
                        'orgId': constant.config['orgId']
                    }
        tmpDict.update(requestObj)
        return luci.CouponSearchRequest(**tmpDict)

    @staticmethod
    def redeemCouponsRequest(requestObj = {}):
        tmpDict =   {
                        'requestId': constant.config['requestId'],
                        'orgId': constant.config['orgId'],
                        'redeemCoupons' : [],
                        'commit' : False
                    }
        tmpDict.update(requestObj)
        return luci.RedeemCouponsRequest(**tmpDict)

    @staticmethod
    def getCouponConfigRequest(configRequestDict = {}):
        tmpDict =   {
                        'requestId': constant.config['requestId'],
                        'orgId': constant.config['orgId']
                    }
        tmpDict.update(configRequestDict)
        return luci.GetCouponConfigRequest(**tmpDict)

    @staticmethod
    def getAllCouponConfigRequest(requestObj = {}):
        tmpDict =   {
                        'requestId': constant.config['requestId'],
                        'orgId': constant.config['orgId'],
                    }
        tmpDict.update(requestObj)
        return luci.GetAllCouponConfigsRequest(**tmpDict)

    @staticmethod
    def uploadCouponRecord():
        tmpDict = {'serialNo' : 0}

    @staticmethod
    def uploadCouponsRequest(requestDict = {}):
        tmpDict =   {
                        'requestId': constant.config['requestId'],
                        'orgId': constant.config['orgId'],
                        'couponSeriesId' : 0,
                        'importType' : 2,
                        'uploadedBy' : constant.config['adminId']
                    }
        tmpDict.update(requestDict)
        return luci.UploadCouponsRequest(**tmpDict)

    @staticmethod
    def downloadCouponsRequest():
        tmpDict =   {
                        'requestId': constant.config['requestId'],
                        'orgId': constant.config['orgId'],
                        'couponSeriesId': 0,
                    }

    @staticmethod
    def issuedCouponDetails(requestObj = {}):
        return luci.IssuedCouponDetails(**requestObj)

    @staticmethod
    def invalidateCouponRequest(requestObj = {}):
        tmpDict =   {
                        'requestId' : constant.config['requestId'],
                        'orgId': constant.config['orgId'],
                        'couponSeriesId': 0,
                        'commit' : True,
                        'reuse' : False
                    }
        tmpDict.update(requestObj)
        return luci.InvalidateCouponRequest(**tmpDict)

    @staticmethod
    def couponCreateRequest(requestObj = {}):
        tmpDict =   {
                        'requestId' : constant.config['requestId'],
                        'orgId': constant.config['orgId'],
                        'couponSeriesId': 0,
                        'count' : 0
                    }
        tmpDict.update(requestObj)
        return luci.CouponCreateRequest(**tmpDict)

    @staticmethod
    def claimCouponConfigRequest(requestObj = {}):
        tmpDict =   {
                        'requestId' : constant.config['requestId'],
                        'orgId': constant.config['orgId'],
                        'couponSeriesId': 0,
                        'ownedBy' : 0,
                        'ownerId' : -1,
                        'modifiedById' : constant.config['adminId']
                    }
        tmpDict.update(requestObj)
        return luci.ClaimCouponConfigRequest(**tmpDict)

    @staticmethod
    def orgDefaults(requestObj = {}):
        tmpDict =   {
                        'orgId' : constant.config['orgId'],
                        'smsTemplate' : 'Org Default SMS Reminder {{voucher}} ',
                        'alphaNumeric' : True,
                        'shortCodeLength' : 0,
                        'randomCodeLength' : 8,
                        'syncToInstore' : False,
                        'updatedBy' : constant.config['adminId'],
                        'updatedOn' : Utils.getTime(milliSeconds=True)
                    }
        tmpDict.update(requestObj)
        return luci.OrgDefaults(**tmpDict)

    @staticmethod
    def saveOrgDefaultsRequest(requestObj = {}):
        tmpDict =   {
                        'requestId' :  constant.config['requestId'],
                        'orgId' : constant.config['orgId'],
                        'orgDefaults' : LuciObject.orgDefaults()
                    }
        tmpDict.update(requestObj)
        return luci.SaveOrgDefaultsRequest(**tmpDict)

    @staticmethod
    def getOrgDefaultsRequest():
        tmpDict =   {
                        'requestId': constant.config['requestId'],
                        'orgId': constant.config['orgId'],
                    }
        return luci.GetOrgDefaultsRequest(**tmpDict)

    @staticmethod
    def getRevokeHistoryRequest(requestObj = {}):
        tmpDict =   {
                        'requestId': constant.config['requestId'],
                        'orgId': constant.config['orgId'],
                    }
        tmpDict.update(requestObj)
        return luci.GetRevokeHistoryRequest(**tmpDict)

    @staticmethod
    def notifyCouponsUploadRequest(requestObj = {}):
        tmpDict =   {
                        'requestId': constant.config['requestId'],
                        'orgId': constant.config['orgId'],
                    }
        tmpDict.update(requestObj)
        return luci.NotifyCouponsUploadRequest(**tmpDict)

    @staticmethod
    def getCurrentTime():
        return int(time.time() * 1000 + 1 * 60 * 60 * 5)

    @staticmethod
    def getNextDayTime():
        return int(time.time() * 1000 + 24 * 60 * 60 * 1000)