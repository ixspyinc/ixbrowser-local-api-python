class Consts:

    # Default value
    DEFAULT_API_TARGET = '127.0.0.1'
    DEFAULT_API_PORT = 53200

    HTTP_CODE_FOR_SUCCESS = 200
    RESULT_CODE_FOR_SUCCESS = 0

    DEFAULT_SITE_ID = 21
    DEFAULT_GROUP_ID = 1

    # Action List
    ACTION_FOR_PROFILE_LIST = 'profile-list'
    ACTION_FOR_PROFILE_OPEN = 'profile-open'
    ACTION_FOR_PROFILE_OPEN_WITH_FINGERPRINT = 'profile-open-with-random-fingerprint'
    ACTION_FOR_PROFILE_CLOSE = 'profile-close'
    ACTION_FOR_PROFILE_CLOSE_IN_BATCHES = 'profile-close-in-batches'

    ACTION_FOR_PROFILE_CREATE = 'profile-create'
    ACTION_FOR_PROFILE_UPDATE = 'profile-update'
    ACTION_FOR_PROFILE_DELETE = 'profile-deleted'
    ACTION_FOR_PROFILE_CLEAR_CACHE = 'profile-clear-cache'

    ACTION_FOR_PROFILE_GET_COOKIES = 'profile-get-cookies'
    ACTION_FOR_PROFILE_UPDATE_COOKIES = 'profile-update-cookies'

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

    ACTION_FOR_TRAFFIC_PACKAGE_LIST = 'traffic-package-list'

    ACTION_FOR_PROXY_LIST = 'proxy-list'
    ACTION_FOR_PROXY_CREATE = 'proxy-create'
    ACTION_FOR_PROXY_UPDATE = 'proxy-update'
    ACTION_FOR_PROXY_DELETE = 'proxy-delete'

    ACTION_FOR_PROXY_TAG_LIST = 'proxy-tag-list'

    # Proxy Mode
    PROXY_MODE_TRAFFIC_PACKAGE = 1
    PROXY_MODE_CUSTOM = 2
    PROXY_MODE_PURCHASED = 3
    DEFAULT_PROXY_MODE = PROXY_MODE_CUSTOM

    # Proxy Type
    PROXY_TYPE_DIRECT = 'direct'
    PROXY_TYPE_HTTP = 'http'
    PROXY_TYPE_HTTPS = 'https'
    PROXY_TYPE_SOCKS5 = 'socks5'
    PROXY_TYPE_SSH = 'ssh'

    # Traffic Package Gateway
    DEFAULT_TRAFFIC_PACKAGE_GATEWAY = 'Default'
    TRAFFIC_PACKAGE_GATEWAY_GEO = 'GEO'
    TRAFFIC_PACKAGE_GATEWAY_US = 'US'
    TRAFFIC_PACKAGE_GATEWAY_SG = 'SG'
    TRAFFIC_PACKAGE_GATEWAY_AU = 'AU'
    TRAFFIC_PACKAGE_GATEWAY_US_TRANSIT_IN_US = 'US-US'
    TRAFFIC_PACKAGE_GATEWAY_SG_TRANSIT_IN_US = 'US-SG'
    TRAFFIC_PACKAGE_GATEWAY_AU_TRANSIT_IN_US = 'US-AU'
    TRAFFIC_PACKAGE_GATEWAY_US_TRANSIT_IN_HK = 'HK-US'
    TRAFFIC_PACKAGE_GATEWAY_SG_TRANSIT_IN_HK = 'HK-SG'
    TRAFFIC_PACKAGE_GATEWAY_AU_TRANSIT_IN_HK = 'HK-AU'

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

