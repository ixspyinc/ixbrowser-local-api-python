class Consts:

    # Default value
    DEFAULT_API_TARGET = '127.0.0.1'
    DEFAULT_API_PORT = 53200

    HTTP_CODE_FOR_SUCCESS = 200
    RESULT_CODE_FOR_SUCCESS = 0

    # Other Site
    DEFAULT_SITE_ID_CUSTOM_PAGE = 21

    # Blank Page
    DEFAULT_SITE_ID_BLANK_PAGE = 22

    # Default Group
    DEFAULT_GROUP_ID = 1

    # Action List
    ACTION_FOR_PROFILE_LIST = 'profile-list'
    ACTION_FOR_PROFILE_OPEN = 'profile-open'
    ACTION_FOR_PROFILE_OPEN_WITH_FINGERPRINT = 'profile-open-with-random-fingerprint'
    ACTION_FOR_PROFILE_CLOSE = 'profile-close'
    ACTION_FOR_PROFILE_CLOSE_IN_BATCHES = 'profile-close-in-batches'
    ACTION_FOR_PROFILE_OPENED_LIST = 'profile-opened-list'
    ACTION_FOR_PROFILE_NATIVE_OPENED_LIST = 'native-client-profile-opened-list'
    ACTION_FOR_PROFILE_OPENED_LIST_ARRANGE_TILE = 'profile-opened-list-arrange-tile'

    ACTION_FOR_PROFILE_CREATE = 'profile-create'
    ACTION_FOR_PROFILE_UPDATE = 'profile-update'
    ACTION_FOR_PROFILE_DELETE = 'profile-delete'

    ACTION_FOR_PROFILE_COPY = 'profile-copy'

    ACTION_FOR_PROFILE_CLEAR_CACHE = 'profile-clear-cache'
    ACTION_FOR_PROFILE_CLEAR_CACHE_AND_COOKIES = 'profile-clear-cache-and-cookies'
    ACTION_FOR_PROFILE_GET_COOKIES = 'profile-get-cookies'
    ACTION_FOR_PROFILE_UPDATE_COOKIES = 'profile-update-cookies'
    ACTION_FOR_PROFILE_EMPTY_RECYCLE_BIN = "empty-recycle-bin"

    ACTION_FOR_PROFILE_UPDATE_GROUPS_IN_BATCHES = 'profile-update-groups-in-batches'

    ACTION_FOR_PROFILE_UPDATE_PROXY_TO_TRAFFIC_PACKAGE_MODE = 'profile-update-proxy-for-purchased-traffic-package'
    ACTION_FOR_PROFILE_UPDATE_PROXY_TO_PURCHASED_MODE = 'profile-update-proxy-for-purchased-proxy'
    ACTION_FOR_PROFILE_UPDATE_PROXY_TO_CUSTOM_MODE = 'profile-update-proxy-for-custom-proxy'

    ACTION_FOR_PROFILE_RANDOM_FINGERPRINT = 'profile-random-fingerprint-configuration'

    ACTION_FOR_PROFILE_CREATE_TRANSFER_CODE = 'profile-transfer-code-create'
    ACTION_FOR_PROFILE_CANCEL_TRANSFER_CODE = 'profile-transfer-cancel'
    ACTION_FOR_PROFILE_IMPORT_VIA_TRANSFER_CODE = 'profile-transfer-code-import'
    ACTION_FOR_PROFILE_TRANSFER_RECORD_LIST = 'profile-transfer-record-list'

    ACTION_FOR_GROUP_LIST = 'group-list'
    ACTION_FOR_GROUP_CREATE = 'group-create'
    ACTION_FOR_GROUP_UPDATE = 'group-update'
    ACTION_FOR_GROUP_DELETE = 'group-delete'

    ACTION_FOR_TAG_LIST = 'tag-list'
    ACTION_FOR_TAG_CREATE = 'tag-create'
    ACTION_FOR_TAG_UPDATE = 'tag-update'
    ACTION_FOR_TAG_DELETE = 'tag-delete'

    ACTION_FOR_TRAFFIC_PACKAGE_LIST = 'traffic-package-list'

    ACTION_FOR_PROXY_LIST = 'proxy-list'
    ACTION_FOR_PROXY_CREATE = 'proxy-create'
    ACTION_FOR_PROXY_UPDATE = 'proxy-update'
    ACTION_FOR_PROXY_DELETE = 'proxy-delete'

    ACTION_FOR_PROXY_TAG_LIST = 'proxy-tag-list'
    ACTION_FOR_PROXY_TAG_CREATE = 'proxy-tag-create'
    ACTION_FOR_PROXY_TAG_UPDATE = 'proxy-tag-update'
    ACTION_FOR_PROXY_TAG_DELETE = 'proxy-tag-delete'

    ACTION_FOR_GATEWAY_LIST = 'gateway-list'
    ACTION_FOR_GATEWAY_SWITCH = 'gateway-switch'
    

    # Proxy Mode
    PROXY_MODE_TRAFFIC_PACKAGE = 1
    PROXY_MODE_CUSTOM = 2
    PROXY_MODE_PURCHASED = 3
    PROXY_MODE_EXTRACT_FROM_URL = 4
    DEFAULT_PROXY_MODE = PROXY_MODE_CUSTOM

    # Proxy Type
    PROXY_TYPE_DIRECT = 'direct'
    PROXY_TYPE_HTTP = 'http'
    PROXY_TYPE_HTTPS = 'https'
    PROXY_TYPE_SOCKS5 = 'socks5'
    PROXY_TYPE_SSH = 'ssh'

    # proxy_check_line
    PROXY_CHECK_LINE_GLOBAL = 'global_line'
    PROXY_CHECK_LINE_CN = 'cn_line'
    DEFAULT_PROXY_CHECK_LINE = PROXY_CHECK_LINE_GLOBAL

    # Proxy Data Format Type
    PROXY_DATA_FROMAT_TYPE_TXT = 'txt'
    PROXY_DATA_FROMAT_TYPE_JSON = 'json'

    # Proxy Data TXT Format
    PROXY_DATA_TXT_FORMAT_LIST = ["ip:port", "ip:port:username:password", "username:password@ip:port", "ip:port@username:password", "username:password:ip:port"]

    # Proxy Data JSON Format
    PROXY_DATA_JSON_FORMAT = {"ip":"ip", "port":"port", "username":None, "password":None}

    # proxy_extraction_method
    PROXY_EXTRACT_FROM_URL_FRESH_TYPE_WHEN_INVALID = "invalid"
    PROXY_EXTRACT_FROM_URL_FRESH_TYPE_WHEN_OPEN = "every_type"

    # Data Package Gateway -Default
    DEFAULT_DATA_PACKAGE_GATEWAY = 'Default'

    # Provider A
    DATA_PACKAGE_PROVIDER_A_GATEWAY_GEO = 'GEO'
    DATA_PACKAGE_PROVIDER_A_GATEWAY_US = 'US'
    DATA_PACKAGE_PROVIDER_A_GATEWAY_SG = 'SG'
    DATA_PACKAGE_PROVIDER_A_GATEWAY_AU = 'AU'
    DATA_PACKAGE_PROVIDER_A_GATEWAY_US_TRANSIT_IN_CN = 'CN-US'
    DATA_PACKAGE_PROVIDER_A_GATEWAY_US_TRANSIT_IN_CN2 = 'CN-US2'
    DATA_PACKAGE_PROVIDER_A_GATEWAY_US_TRANSIT_IN_CN = 'CN-SG'

    # Provider B
    DATA_PACKAGE_PROVIDER_B_GATEWAY_HK = 'HK'
    DATA_PACKAGE_PROVIDER_B_GATEWAY_US = 'US'
    DATA_PACKAGE_PROVIDER_B_GATEWAY_SEA = 'SEA'
    DATA_PACKAGE_PROVIDER_B_GATEWAY_EU = 'EU'
    DATA_PACKAGE_PROVIDER_B_GATEWAY_GB = 'GB'
    DATA_PACKAGE_PROVIDER_B_GATEWAY_UA = 'UA'
    DATA_PACKAGE_PROVIDER_B_GATEWAY_IN = 'IN'
    DATA_PACKAGE_PROVIDER_B_GATEWAY_TH = 'TH'
    DATA_PACKAGE_PROVIDER_B_GATEWAY_JP = 'JP'
    DATA_PACKAGE_PROVIDER_B_GATEWAY_HK_TRANSIT_IN_CN = 'CN-HK'
    DATA_PACKAGE_PROVIDER_B_GATEWAY_HK_TRANSIT_IN_CN2 = 'CN-HK2'

    # Traffic Package Gateway
    # Old configuration, no longer available
    # Replaced by the following configuration items: DATA_PACKAGE_PROVIDER_A_GATEWAY_XXX
    DEFAULT_TRAFFIC_PACKAGE_GATEWAY = 'Default'
    TRAFFIC_PACKAGE_GATEWAY_GEO = 'GEO'
    TRAFFIC_PACKAGE_GATEWAY_US = 'US'
    TRAFFIC_PACKAGE_GATEWAY_SG = 'SG'
    TRAFFIC_PACKAGE_GATEWAY_AU = 'AU'
    TRAFFIC_PACKAGE_GATEWAY_US_TRANSIT_IN_CN = 'CN-US'
    TRAFFIC_PACKAGE_GATEWAY_US_TRANSIT_IN_CN2 = 'CN-US2'
    TRAFFIC_PACKAGE_GATEWAY_SG_TRANSIT_IN_CN = 'CN-SG'


    # Profile Color List
    DEFAULT_PROFILE_COLOR_LIST = ["#FF6666",
                                  "#FF8C00",
                                  "#FFD700",
                                  "#90EE90",
                                  "#00CED1",
                                  "#1E90FF",
                                  "#CC9966",
                                  "#FFCC99",
                                  "#C71585",
                                  "#FF0033", ]

    # Profile Transfer Code
    TRANSFER_PROXY_MODE_SHARING = 1
    TRANSFER_PROXY_MODE_TRANSFER = 2

    TRANSFER_RECORD_LIST_TYPE_TRANSFER = 1
    TRANSFER_RECORD_LIST_TYPE_IMPORT = 2

    # Device name source
    DEVICE_NAME_SOURCE_RANDOM = 1
    DEVICE_NAME_SOURCE_CUSTOM = 2
    DEVICE_NAME_SOURCE_FOLLOW_OS = 0

