class LuciExceptionCodes():

    #Config errors - 1XX errors
    FACTORY_EXEPTION = 100
    UNSUPPORTED_OPERATION = 101
    ENTITY_LOCKED = 102
    NO_LOCK_TO_RELEASE = 103
    UNABLE_TO_ACQUIRE_CUSTOMER_LOCK = 104
    UNABLE_TO_FETCH_VALIDATORS = 105
    UNABLE_TO_ACQUIRE_SERIES_LOCK = 106
    INVALID_CONFIG_KEY = 107
    INVALID_CLIENT_HANDLING_TYPE = 108
    INVALID_SERIES_CONFIG = 109

    #4XX series - system level errors
    UNEXPECTED_ERROR = 400
    EMF_SERVICE_UNAVAILABLE = 401
    EMF_EVALUATION_ERROR = 402
    REPORT_FILE_CREATION_ERROR = 403
    REGISTRAR_SERVICE_UNAVAILABLE = 404
    MERCURY_SERVICE_UNAVAILABLE = 405
    MERCURY_COMMUNICATION_ERROR = 406

    #5XX - org level errors
    INVALID_ORG_ID = 500
    INVALID_COUPON_SERIES_ID = 501
    NO_COUPON_SERIES_AVAILABLE_FOR_ORG = 502
    CS_CONFIG_INVALID = 503
    CS_CONFIG_STORES_INVALID = 504
    CS_CONFIG_MUTUAL_EXCLUSIVE_INVALID = 505
    CS_CONFIG_REDEMPTION_RANGE_INVALID = 506
    CS_CONFIG_ISSUAL_STORES_INVALID = 507

    #6XX - validation based errors
    MAX_REDEMPTION_PER_USER_EXCEEDED = 600
    COUPON_EXPIRED = 601
    COUPON_TAGGED_DIFFERENT_USER = 602
    MULTIPLE_REDEMPTION_FOR_COUPON_NOT_ALLOWED = 603
    MULTIPLE_REDEMPTION_FOR_USER_AND_COUPON_NOT_ALLOWED = 604
    MAX_REDEMPTION_FOR_SERIES_EXCEEDED = 605
    BILL_AMT_EXCEEDS_LIMIT = 606
    BILL_AMT_LESS_LIMIT = 607
    STORE_ID_NOT_FOUND = 608
    COUPON_PRESENT_MUTUAL_EXCLUSIVE_SERIES = 609
    COUPON_SERIES_CONFIG_NOT_LOADED = 610
    UNTAGGED_COUPON_UPLOAD_DENIED = 611
    INVALID_ISSUED_USER_ID = 612
    COUPONS_EXHAUSTED = 613
    COUPON_NOT_ISSUED = 614
    INVALID_COUPON = 615
    INVALID_TILL_ID = 616
    INVALID_USER_ID = 617
    DUPLICATE_USER_ID = 618
    COUPON_ALREADY_ISSUED = 619
    DAYS_BETWEEN_ISSUAL_FOR_USER_LOWER_MIN_DAYS = 620
    MAX_COUPON_ISSUAL_PER_USER_EXCEEDED = 621
    REDEMPTION_GAP_LOWER_THAN_EXPECTED = 622
    REDEMPTION_RANGE_NOT_SATISFIED = 623
    INVALID_REDEMPTION_STORE_ID = 624
    REDEMPTION_FAILED_FOR_USER = 625
    MAX_COUPON_ISSUAL_PER_SERIES_EXCEEDED = 626
    INVALID_ISSUAL_STORE_ID = 627
    REDEMPTION_VALIDITY_DATE_NOT_REACHED = 628
    INVALID_INPUT = 629
    DUPLICATE_SERIES_CODE = 630
    DUPLICATE_GENERIC_COUPON_CODE = 631
    INVALID_COUPON_CODE = 633
    EMPTY_SERIES_CODE = 634
    COUPON_SERIES_EXPIRED = 635
    RESEND_MESSAGE_TEMPLATE_NOT_CONFIGURED = 636
    RESEND_MESSAGE_TEMPLATE_NOT_VALID = 637
    MOBILE_NUMBER_IS_NOT_SET = 638
    REDEMPTION_DATE_AFTER_SERIES_EXPIRY_DATE = 639
    COUPON_SERIES_ALREADY_CLAIMED = 640
    INCORRECT_VALID_TILL_DATE = 641
    INVALID_MESSAGE_TYPE = 642
    INVALID_DEFAULT_PROPERTY = 643
    TAGS_NOT_RESOLVED = 644
    FAILED_REDEMPTIONS_EXISTS = 645

    #7XX - coupon loading flow errors
    COULD_NOT_LOAD_PUMP = 701
    QUEUE_TEMPORARILY_EMPTY = 702
    TRIGGER_NOT_PRESENT_FOR_VCH_SERIES = 703
    NO_MORE_COUPONS_IN_SERIES = 704
    NO_VALID_COUPON_SOURCE = 705

    #8XX - lucithrift exception
    INVALID_TYPE_UPLOAD_COUPON = 800

    #9XX - coupon processor exceptions
    BILL_AMOUNT_TOO_LOW = 900
    BILL_AMOUNT_TOO_HIGH = 901
    BILL_DISCOUNTED = 902
    INVALID_PROCESSOR_TYPE = 903

    #10XX - coupon action based errors
    FILTERS_NOT_PROVIDED = 1000

    #11XX - merge error codes
    MERGED_ALREADY_DONE = 1100
    MERGE_ALLOWED = 1101
    MERGE_SUCCESSFUL = 1102
    MERGE_FAILED = 1103