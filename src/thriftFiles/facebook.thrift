
namespace java com.capillary.social
namespace php social

exception FacebookException {
  1: string message
}

enum ButtonType {
	web_url, postback, phone_number, element_share, payment, account_link, account_unlink
}

enum ButtonField {
	url, webview_height_ratio, messenger_extensions, fallback_url, payload, payment_summary
}

enum MessageType {
	textMessage, buttonMessage, genericMessage, quickReplyMessage, receiptMessage, listMessage
}

enum QuickReplyContentType {
	text, location
}

enum ListMessageTopElementStyle {
	large, compact
}

enum SocialChannel{
	none,facebook,google,twitter
}

enum GatewayResponseType {
	success,sent, blocked, failed, invalidContent, policyViolation
}

struct Button {
	1:ButtonType type;
	2:optional string title;
	3:map<ButtonField,string> data;
}

struct Element {
	1:string title;
	2:optional string subtitle;
	3:optional string imageUrl;
	4:optional Button defaultAction;
	5:optional list<Button> buttonList;
}

struct QuickReply {
	1: QuickReplyContentType contentType;
	2: optional string title;
	3: optional string payload;
	4: optional string imageUrl;
}

struct TextMessage {
	1:string text;
}

struct ButtonMessage {
	1:string text;
	2:list<Button> buttonList;
}

struct GenericMessage {
	1:list<Element> elementList;
}

struct QuickReplyMessage {
	1:string text;
	2:list<QuickReply> quickReplyList;
}

struct Address {
	1:string streetOne;
	2:optional string streetTwo;
	3:string city;
	4:string postalCode;
	5:string state;
	6:string country;
}

struct Summary {
	1:optional double subtotal;
	2:optional double shippingCost;
	3:optional double totalTax;
	4:double totalCost;
}

struct Adjustment {
	1:optional string name;
	2:optional double amount;
}

struct ReceiptElement {
	1:string title;
	2:optional string subtitle;
	3:optional i32 quantity;
	4:i32 price;
	5:optional string currency;
	6:optional string imageUrl;
}

struct ReceiptMessage {
	1:string recipientName;
	2:optional string merchantName;
	3:string orderNumber;
	4:string currency;
	5:string paymentMethod;
	6:optional string timestamp;
	7:optional string orderUrl;
	8:optional list<ReceiptElement> receiptElementList;
	9:optional Address address;
	10:Summary summary;
	11:optional list<Adjustment> adjustmentList;
}

struct ListMessage {
	1:optional ListMessageTopElementStyle topElementStyle;
	2:list<Element> elementList;
	3:optional list<Button> buttonList;
}

struct GatewayResponse {
	1:string message
	2:string response
	3:GatewayResponseType gatewayResponseType
}

struct CreateCustomAudienceListResponse {
	1:string listid;
	2:string message;
	3:GatewayResponseType response;
}

struct UserDetails {
	1:optional string email;
	2:optional string mobile;
}

struct CustomAudienceListDetails {
	1:string name;
	2:string description;
	3:required i64 messageId;
}

struct SocialAccountDetails {
	1:SocialChannel channel;
}

struct CustomAudienceList {
	1:i64 orgId;
	2:SocialChannel socialChannel;
	3:string adsAccountId;
	4:string recepientlistId;
	5:string remoteListId;
	6:string name;
	7:string description;
	8:i64 approximateCount;
	9:i64 contentUpdatedTime;
	10:i64 createdTime;
	11:i64 cachedOn;
        12:i64 messageId;
}


struct GetCustomAudienceListsResponse {
	1:GatewayResponseType response;
	2:string  message;
	3:list<CustomAudienceList> customAudienceLists;
}
enum AdSetStatus{
	ACTIVE, PAUSED, DELETED, ARCHIVED
}

struct SocialAdSet {
	1:string id;
	2:string name;
	3:string campaignId;
	4:i64 startTime;
	5:i64 endTime;
	6:AdSetStatus status;
}

struct AdInsight {
	1:i64 orgId;
	2:SocialChannel socialChannel;
	3:string adsetId;
	4:string insights;
	5:i64 cachedon;
}

enum SocialStatus { 
	ACTIVE, PAUSED, DELETED, ARCHIVED
}

struct SocialCampaign {
    1:optional string remoteCampaignId;
    2:required string name;
    3:required i64 orgId;
    4:required i64 campaignId;
    5:optional string accountId;
    6:optional SocialStatus socialCampaignStatus;
}

enum OfferLocationType {
   online, offline, both
}

enum OfferType {
 percentage_off, cash_discount
}

enum SocialCouponType {
  generic,csv_file
}

struct SocialOfferCouponsCsvFileInfo {
   1:required string couponsCsvFileS3Path;
   2:optional i64  couponsUploaded;
   3:optional string couponsUploadStatus;
}

struct SocialDiscount{
    1:required OfferType offerType;
    2:required string offerText;
    3:required i64 offerValue;
    4:optional SocialOfferCouponsCsvFileInfo socialOfferCouponsCsvFileInfo;
    5:optional string redemptionCode;
}

struct SocialOffer {
   1:optional string remoteOfferId;
   2:required SocialDiscount socialDiscount;
   3:required string pageId;
   4:required OfferLocationType offerLocationType;
   5:required string overviewDetails;
   6:required string expirationTime;
   7:required SocialCouponType socialCouponType;
}

struct SocialAdsetInfo {
   1:required string adsetName;
   2:required string remoteCampaignId;
   3:required string startTime;
   4:required string endTime;
   5:required SocialStatus socialAdsetStatus;
   6:required i64 dailyBudget;
   7:optional string customAudienceId;
   8:optional string remoteOfferId;
   9:optional string remoteAdsetId;
}

struct SocialCampaignDetails {
   1:required SocialCampaign socialCampaign;
   2:required list<SocialAdsetInfo> adsetLists;
}

service FacebookService /*extends capillarybase_thriftservice.CapillaryBaseThriftService*/ {

  bool isAlive();

  GatewayResponse sendTextMessage(1:string recipientId, 2: TextMessage textMessage, 3:string pageId, 4:i64 orgId, 5:string requestId ) throws (1:FacebookException ex)

  GatewayResponse sendButtonMessage(1:string recipientId, 2:ButtonMessage buttonMessage, 3:string pageId, 4:i64 orgId, 5:string requestId) throws (1:FacebookException ex)

  GatewayResponse sendGenericMessage(1:string recipientId, 2:GenericMessage genericMessage, 3:string pageId, 4:i64 orgId, 5:string requestId)  throws (1:FacebookException ex)

  GatewayResponse sendQuickReplyMessage(1:string recipientId, 2:QuickReplyMessage quickReplyMessage, 3:string pageId, 4:i64 orgId, 5:string requestId) throws (1:FacebookException ex)

  GatewayResponse sendReceiptMessage(1:string recipientId, 2:ReceiptMessage receiptMessage, 3:string pageId, 4:i64 orgId, 5:string requestId) throws (1:FacebookException ex)

  GatewayResponse sendListMessage(1:string recipientId, 2:ListMessage listMessage, 3:string pageId, 4:i64 orgId,5:string requestId) throws (1:FacebookException ex)
  
  CreateCustomAudienceListResponse createCustomList(1:list<UserDetails> userlist,2:CustomAudienceListDetails customAudienceListDetails,3:SocialAccountDetails socialAccountDetails ,4:i64 orgId,5:string recepientlistId,6:string requestId) throws  (1:FacebookException ex)

GetCustomAudienceListsResponse getCustomAudienceLists(1:i64 orgId,2:SocialChannel socialChannel,3:bool clearcache,4:string requestId) throws (1: FacebookException ex)

list<SocialAdSet> getAdSets(1:SocialChannel socialChannel,2:i64 orgId,3:string requestId) throws(1:FacebookException ex)

AdInsight getAdsetInsights(1:SocialChannel socialChannel,2:i64 orgId,3:string adsetId,4:i32 groupId, 5:bool clearchche,6:string requestId) throws(1:FacebookException ex)

 void deleteSocialAudienceList(1:SocialChannel socialChannel, 2:i64 orgId, 3:string remoteListId, 4:string requestId) throws (1: FacebookException ex)
 bool testAccount(1:SocialChannel socialChannel,2:i64 orgId,3:string requestId) ;
 SocialCampaign createCampaign(1:i64 orgId, 2: SocialChannel socialChannel , 3: SocialCampaign socialCampaign , 4: string requestId) throws (1: FacebookException ex)
 list<string> getPageIdForOrgAndAccount(1:i64 orgId , 2:SocialChannel socialChannel , 3:string requestId ) throws ( 1: FacebookException ex )
 SocialOffer createNativeOffer(1:i64 orgId, 2:SocialChannel socialChannel , 3:SocialOffer socialOffer , 4:string requestId ) throws ( 1: FacebookException ex )
 SocialAdsetInfo createSocialAdset(1:i64 orgId, 2:SocialChannel socialChannel, 3:SocialAdsetInfo socialAdsetInfo, 4:string requestId) throws ( 1: FacebookException ex )
 SocialCampaignDetails getSocialCampaignDetails(1:i64 orgId, 2:i64 campaignId, 3:i64 userId, 4:SocialChannel socialChannel, 5:string requestId) throws ( 1: FacebookException ex )
 SocialAdsetInfo updateCustomListInAdset(1:i64 orgId, 2:SocialChannel socialChannel, 3:string remoteAdsetId, 4:string remoteListId, 5:string requestId) throws (1: FacebookException ex)
}
