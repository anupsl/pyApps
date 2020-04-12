#!thrift -java -php -phps

/**
 * This file contains all dracarys service (coupons bulk calls) related classes and definitions.
*/

namespace java com.capillary.shopbook.dracarys.external

namespace php dracarys


exception DracarysThriftException {
	1: required i32 errorCode,
	2: required string errorMsg
}

enum UploadCouponStatus {
	STARTED,
	VALIDATED,
	COMMITED,
	FINISHED,
	ERRORED
}

enum CustomerIdentifierType {
	MOBILE,
	EMAIL,
	USER_ID,
	EXTERNAL_ID,
	NOT_TAGGED
}

struct UploadJobStatus {
	1: required i32 jobId,
	2: required UploadCouponStatus uploadStatus,
	3: required i64 createdOn,
	4: required i64 updatedOn,
	5: optional string errorFileUrl,
	6: optional string successFileUrl,
	7: optional string uploadedFileUrl,
	8: optional i32 totalUploadedCount,
	9: optional i32 actualRowCount,
	10: optional i32 errorCount,
	11: optional string uploadTableName,
	12: optional string uploadedFileName
}

enum ClientHandlingType {
	DISC_CODE,
	DISC_CODE_PIN,
	DISC_CODE_PIN_CUSTOMER_TAGGED,
	EXTERNAL,
	GENERIC
}

struct UploadStatusResponse {
	1: required i32 orgId,
	2: required i32 couponSeriesId,
	3: required list<UploadJobStatus> uploadJobStatuses
}

struct CouponUploadRequest {
	1: required string S3FilePath,
	2: required bool commit,
	3: required i32 orgId,
	4: required string requestId,
	5: required i32 couponSeriesId,
	6: required i32 uploadedBy,
	7: required map<string, i32> uploadHeaders,
	8: required CustomerIdentifierType custIdentifierType
	9: required string uploadedFileName
}

struct GetCouponUploadStatusRequest {
	1: required i32 orgId,
	2: required string requestId,
	3: required i32 couponSeriesId
}

enum MessageType {
	SMS,
	EMAIL,
	WECHAT,
	MOBILE_PUSH
}

struct SmsMessage{
	1: required string message,
	2: optional string senderId,
	3: optional string senderLabel,
	4: optional i32 domainPropertyId
}

struct EmailMessage{
	1: required string subject,
	2: required string emailBody,
	3: optional string senderId,
	4: optional string senderLabel,
	5: optional i32 domainPropertyId
}

struct WechatMessage{
	1: required string template,
	2: required string originalId,
	3: required string brandId,
	4: required string wechatId
}

struct MobilePushMessageDetails{
	1: required string title,
	2: required string messageBlob
}

struct MobilePushMessage{
	1: required string accountId,
	2: required string pushTemplateId,
	3: optional MobilePushMessageDetails androidMessageDetails,
	4: optional MobilePushMessageDetails iosMessageDetails
}

struct ReminderMessage{
        1: required MessageType type,
        2: optional SmsMessage smsMessage,
        3: optional EmailMessage emailMessage,
        4: optional WechatMessage wechatMessage,
        5: optional MobilePushMessage mobilePushMessage
}

struct CouponReminderMessageDetails{
	1: required i32 id,
	2: required i32 orgId,
	3: required ReminderMessage reminderMessage
}

struct CouponReminderDetails{
        1: required i32 id,
        2: required i32 orgId,
        3: required i32 couponSeriesId,
        4: required i32 numDaysBeforeExpiry,
        5: required i32 hourOfDay,
        6: required i32 minuteOfHour,
        7: required i64 createdBy,
        8: required i64 createdOn,
        9: optional list<CouponReminderMessageDetails> reminderMessages
}

struct SaveCouponReminderRequest{
	1: required string requestId,
	2: required i32 orgId,
	3: required i32 couponSeriesId,
	4: required list<CouponReminderDetails> couponReminderDetails,
	5: required i64 updatedBy
}

struct GetCouponReminderRequest{
	1: required string requestId,
	2: required i32 orgId,
	3: required i32 couponSeriesId
}

struct PublishCouponReminderRequest{
    1: required string requestId,
    2: required i32 orgId,
    3: required i32 reminderId
}

enum DownloadReportType {
	ISSUED, REDEEMED
}

enum DownloadReportJobStatus {
	STARTED, ERRORED, FINISHED
}

struct DownloadCouponsReportRequest {
	1: required string requestId,
	2: required i32 orgId,
	3: required i32 couponSeriesId,
	4: required i32 requestedBy,
	5: required DownloadReportType downloadReportType
}

struct GetDownloadReportStatusRequest {
	1: required string requestId,
	2: required i32 jobId,
	3: required i32 orgId,
	4: required i32 couponSeriesId
}

struct DownloadCouponsReportDetails {
	1: required i32 jobId,
	2: required i32 orgId,
	3: required i32 couponSeriesId,
	4: required DownloadReportJobStatus downloadReportJobStatus,
	5: optional string s3FilePath,
	6: optional DownloadReportType downloadReportType,
	7: optional i32 errorCode,
	8: optional string errorMessage,
	9: optional i32 requestedBy,
	10: optional i32 totalDownloadCount,
	11: optional i64 createdOn,
	12: optional i64 updatedOn
}

service DracarysService {
    //isAlive
    bool isAlive();

    UploadJobStatus uploadCoupons(1: CouponUploadRequest couponUploadRequest) throws (1:DracarysThriftException ex);

    UploadStatusResponse getUploadStatusForCouponSeries(1: GetCouponUploadStatusRequest getCouponUploadStatusRequest) throws (1:DracarysThriftException ex);

    list<CouponReminderDetails> saveCouponReminder(1: SaveCouponReminderRequest saveCouponReminderRequest) throws (1:DracarysThriftException ex);

    list<CouponReminderDetails> getCouponReminders(1: GetCouponReminderRequest getCouponReminderRequest) throws (1:DracarysThriftException ex);

    bool publishCouponReminder(1: PublishCouponReminderRequest publishCouponReminderRequest) throws (1:DracarysThriftException ex);

    DownloadCouponsReportDetails downloadCouponsReport(1: DownloadCouponsReportRequest downloadCouponsReportRequest) throws (1:DracarysThriftException ex);

    DownloadCouponsReportDetails getDownloadReportStatus(1: GetDownloadReportStatusRequest getDownloadReportStatusRequest) throws (1:DracarysThriftException ex);

}
