"""Frozen endpoint contract for the Local API V2 actions the SDK implements.

These strings were taken from the published documentation at
https://www.ixbrowser.com/doc/v2/local-api/en and are pinned here on purpose: a
typo in an action name cannot be caught by any other test, because the SDK only
ever builds a URL from it. If a test in this file fails, either the constant was
changed by accident or the Local API really moved an endpoint.
"""
ACTION_ENDPOINTS = {
    # Profile
    'ACTION_FOR_PROFILE_LIST': 'profile-list',
    'ACTION_FOR_PROFILE_OPEN': 'profile-open',
    'ACTION_FOR_PROFILE_OPEN_WITH_FINGERPRINT': 'profile-open-with-random-fingerprint',
    'ACTION_FOR_PROFILE_CLOSE': 'profile-close',
    'ACTION_FOR_PROFILE_CLOSE_IN_BATCHES': 'profile-close-in-batches',
    'ACTION_FOR_PROFILE_OPENED_LIST': 'profile-opened-list',
    'ACTION_FOR_PROFILE_NATIVE_OPENED_LIST': 'native-client-profile-opened-list',
    'ACTION_FOR_PROFILE_OPENED_LIST_ARRANGE_TILE': 'profile-opened-list-arrange-tile',
    'ACTION_FOR_PROFILE_OPEN_STATE_RESET': 'profile-open-state-reset',
    'ACTION_FOR_PROFILE_CREATE': 'profile-create',
    'ACTION_FOR_PROFILE_UPDATE': 'profile-update',
    'ACTION_FOR_PROFILE_DELETE': 'profile-delete',
    'ACTION_FOR_PROFILE_COPY': 'profile-copy',
    'ACTION_FOR_PROFILE_CLEAR_CACHE': 'profile-clear-cache',
    'ACTION_FOR_PROFILE_CLEAR_CACHE_AND_COOKIES': 'profile-clear-cache-and-cookies',
    'ACTION_FOR_PROFILE_CLEAR_CACHE_KEEP_EXTENSIONS': 'profile-clear-cache-keep-extensions',
    'ACTION_FOR_PROFILE_CLEAR_CLOUD_DATA': 'profile-clear-cloud-data',
    'ACTION_FOR_PROFILE_CLEAR_SAVED_USER_PASSWORD': 'profile-clear-saved-user-password',
    'ACTION_FOR_PROFILE_GET_COOKIES': 'profile-get-cookies',
    'ACTION_FOR_PROFILE_UPDATE_COOKIES': 'profile-update-cookies',
    'ACTION_FOR_PROFILE_EMPTY_RECYCLE_BIN': 'empty-recycle-bin',
    'ACTION_FOR_PROFILE_UPDATE_GROUPS_IN_BATCHES': 'profile-update-groups-in-batches',
    'ACTION_FOR_PROFILE_UPDATE_PROXY_TO_TRAFFIC_PACKAGE_MODE': 'profile-update-proxy-for-purchased-traffic-package',
    'ACTION_FOR_PROFILE_UPDATE_PROXY_TO_PURCHASED_MODE': 'profile-update-proxy-to-purchased-mode',
    'ACTION_FOR_PROFILE_UPDATE_PROXY_TO_CUSTOM_MODE': 'profile-update-proxy-for-custom-proxy',
    'ACTION_FOR_PROFILE_UPDATE_PROXY_TO_API_EXTRACTION_MODE': 'profile-update-proxy-for-api-extraction',
    'ACTION_FOR_PROFILE_RANDOM_FINGERPRINT': 'profile-random-fingerprint-configuration',
    'ACTION_FOR_PROFILE_CREATE_TRANSFER_CODE': 'profile-transfer-code-create',
    'ACTION_FOR_PROFILE_CANCEL_TRANSFER_CODE': 'profile-transfer-cancel',
    'ACTION_FOR_PROFILE_IMPORT_VIA_TRANSFER_CODE': 'profile-transfer-code-import',
    'ACTION_FOR_PROFILE_TRANSFER_RECORD_LIST': 'profile-transfer-record-list',
    # Group
    'ACTION_FOR_GROUP_LIST': 'group-list',
    'ACTION_FOR_GROUP_CREATE': 'group-create',
    'ACTION_FOR_GROUP_UPDATE': 'group-update',
    'ACTION_FOR_GROUP_DELETE': 'group-delete',
    # Tag
    'ACTION_FOR_TAG_LIST': 'tag-list',
    'ACTION_FOR_TAG_CREATE': 'tag-create',
    'ACTION_FOR_TAG_UPDATE': 'tag-update',
    'ACTION_FOR_TAG_DELETE': 'tag-delete',
    # Traffic package
    'ACTION_FOR_TRAFFIC_PACKAGE_LIST': 'traffic-package-list',
    # Proxy
    'ACTION_FOR_PROXY_LIST': 'proxy-list',
    'ACTION_FOR_PROXY_CREATE': 'proxy-create',
    'ACTION_FOR_PROXY_UPDATE': 'proxy-update',
    'ACTION_FOR_PROXY_DELETE': 'proxy-delete',
    'ACTION_FOR_PROXY_TAG_LIST': 'proxy-tag-list',
    'ACTION_FOR_PROXY_TAG_CREATE': 'proxy-tag-create',
    'ACTION_FOR_PROXY_TAG_UPDATE': 'proxy-tag-update',
    'ACTION_FOR_PROXY_TAG_DELETE': 'proxy-tag-delete',
    # Gateway
    'ACTION_FOR_GATEWAY_LIST': 'gateway-list',
    'ACTION_FOR_GATEWAY_SWITCH': 'gateway-switch',
}
