"""Tests for IXBrowserClient methods: endpoint, payload and return convention."""
import inspect

import pytest

from ixbrowser_local_api import Consts, IXBrowserClient, Profile, Proxy, Preference, Fingerprint
from ixbrowser_local_api.errors import UNEXPECTED_ERROR_CODE

BASE = 'http://127.0.0.1:53200/api/v2/'

PAGINATED_CALLS = [
    ('get_profile_list', (), 'profile-list'),
    ('get_group_list', (), 'group-list'),
    ('get_tag_list', (), 'tag-list'),
    ('get_proxy_tag_list', (), 'proxy-tag-list'),
    ('get_traffic_package_list', (), 'traffic-package-list'),
    ('get_profile_transfer_record_list', (), 'profile-transfer-record-list'),
]

PROXY_LIST_CALL = ('get_proxy_list', (), 'proxy-list')

# (method, args, expected action) for paginated interfaces.
ALL_PAGINATED = PAGINATED_CALLS + [PROXY_LIST_CALL]


class TestPaginatedMethods(object):

    @pytest.mark.parametrize('method,args,action', ALL_PAGINATED)
    def test_returns_the_item_list_and_sets_total(self, client, transport, method, args, action):
        transport.reply(payload={
            'error': {'code': 0, 'message': 'success'},
            'data': {'total': 3, 'data': [{'id': 1}, {'id': 2}, {'id': 3}]},
        })
        result = getattr(client, method)(*args)
        assert transport.last['url'] == BASE + action
        assert result == [{'id': 1}, {'id': 2}, {'id': 3}]
        assert client.total == 3
        assert client.code is None

    @pytest.mark.parametrize('method,args,action', ALL_PAGINATED)
    def test_empty_page_is_a_success(self, client, transport, method, args, action):
        transport.reply(payload={'error': {'code': 0}, 'data': {'total': 0, 'data': []}})
        assert getattr(client, method)(*args) == []
        assert client.total == 0
        assert client.code is None

    @pytest.mark.parametrize('method,args,action', PAGINATED_CALLS)
    def test_broken_envelope_does_not_raise_type_error(self, client, transport, method, args, action):
        # The regression this guards: get_api_response unwraps "data" once, so a
        # response that is not an object used to escape as an uncaught TypeError.
        for bad_data in (True, [{'id': 1}], 'success', None):
            transport.reply(payload={'error': {'code': 0}, 'data': bad_data})
            assert getattr(client, method)(*args) is None
            assert client.code == UNEXPECTED_ERROR_CODE
            assert client.message is not None

    def test_api_error_maps_to_none_and_error_state(self, client, transport):
        transport.reply(payload={'error': {'code': 1008, 'message': 'Your permissions are restricted'}})
        assert client.get_profile_list() is None
        assert client.code == 1008
        assert client.message == 'Your permissions are restricted'
        assert client.total is None

    def test_unreachable_api_maps_to_none(self, client, transport):
        transport.reply_with_exception(ConnectionError('connection refused'))
        assert client.get_profile_list() is None
        assert client.code == UNEXPECTED_ERROR_CODE


class TestActionMethods(object):
    """Methods that answer with "data": "success" and return that value."""

    ACTION_CALLS = [
        ('delete_profile', (1,), 'profile-delete'),
        ('close_profile', (1,), 'profile-close'),
        ('empty_recycle_bin', (), 'empty-recycle-bin'),
        ('random_profile_fingerprint', (1,), 'profile-random-fingerprint-configuration'),
        ('clear_profile_cache', (1,), 'profile-clear-cache'),
        ('clear_profile_cache_and_cookies', ([1, 2],), 'profile-clear-cache-and-cookies'),
        ('clear_profile_cache_keep_extensions', (1,), 'profile-clear-cache-keep-extensions'),
    ]

    @pytest.mark.parametrize('method,args,action', ACTION_CALLS)
    def test_success_returns_api_data(self, client, transport, method, args, action):
        transport.reply(payload={'error': {'code': 0, 'message': 'success'}, 'data': 'success'})
        assert getattr(client, method)(*args) == 'success'
        assert transport.last['url'] == BASE + action
        assert client.code is None

    @pytest.mark.parametrize('method,args,action', ACTION_CALLS)
    def test_failure_returns_none(self, client, transport, method, args, action):
        transport.reply(payload={'error': {'code': 2007, 'message': 'Profile does not exist'}})
        assert getattr(client, method)(*args) is None
        assert client.code == 2007

    def test_switch_gateway_returns_true_instead_of_the_api_data(self, client, transport):
        # Documented inconsistency: unlike its siblings this method discards the
        # response and returns True on success. Pinned so a future change is a
        # deliberate decision rather than an accident.
        transport.reply(payload={'error': {'code': 0, 'message': 'success'}, 'data': 'success'})
        assert client.switch_gateway(2) is True
        assert transport.last['url'] == BASE + 'gateway-switch'
        assert transport.last['payload'] == {'id': 2}

    def test_switch_gateway_failure_returns_none(self, client, transport):
        transport.reply(payload={'error': {'code': 1008, 'message': 'Your permissions are restricted'}})
        assert client.switch_gateway(2) is None
        assert client.code == 1008


class TestOpenStateReset(object):

    def test_documented_success_shape_returns_true(self, client, transport):
        # The interface answers with "data": null, which is indistinguishable from
        # failure, so the method normalises success to True.
        transport.reply(payload={'error': {'code': 0, 'message': 'success'}, 'data': None})
        assert client.reset_profile_open_state(11971) is True
        assert client.code is None
        assert transport.last['url'] == BASE + 'profile-open-state-reset'
        assert transport.last['payload'] == {'profile_id': 11971}

    def test_documented_failure_shape_returns_none(self, client, transport):
        transport.reply(payload={'error': {'code': 2007, 'message': 'Profile does not exist'}, 'data': None})
        assert client.reset_profile_open_state(11971) is None
        assert client.code == 2007
        assert client.message == 'Profile does not exist'

    def test_success_and_failure_are_distinguishable(self, client, transport):
        transport.reply(payload={'error': {'code': 0, 'message': 'success'}, 'data': None})
        ok = client.reset_profile_open_state(1)
        transport.reply(payload={'error': {'code': 2007, 'message': 'Profile does not exist'}, 'data': None})
        failed = client.reset_profile_open_state(1)
        assert ok is not failed


class TestClearSavedUserPassword(object):

    def test_documented_success_shape_returns_true(self, client, transport):
        transport.reply(payload={'error': {'code': 0, 'message': 'success'}, 'data': None})
        assert client.clear_profile_saved_user_password(2319) is True
        assert client.code is None
        assert transport.last['url'] == BASE + 'profile-clear-saved-user-password'
        assert transport.last['payload'] == {'profile_id': 2319}

    def test_documented_failure_shape_returns_none(self, client, transport):
        transport.reply(payload={'error': {'code': 2007, 'message': 'Profile does not exist'}, 'data': None})
        assert client.clear_profile_saved_user_password(2319) is None
        assert client.code == 2007


class TestClearCloudData(object):

    def test_payload_matches_the_documented_example(self, client, transport):
        transport.reply(payload={'error': {'code': 0, 'message': 'success'}, 'data': [1456, 1457]})
        result = client.clear_profile_cloud_data([1456, 1457], Consts.CLOUD_DATA_TYPE_LIST)
        assert transport.last['url'] == BASE + 'profile-clear-cloud-data'
        assert transport.last['payload'] == {
            'profile_id': [1456, 1457],
            'type': ['indexed_db', 'local_storage', 'extension_data'],
        }
        assert result == [1456, 1457]

    def test_enum_constant_values(self):
        assert Consts.CLOUD_DATA_TYPE_INDEXED_DB == 'indexed_db'
        assert Consts.CLOUD_DATA_TYPE_LOCAL_STORAGE == 'local_storage'
        assert Consts.CLOUD_DATA_TYPE_EXTENSION_DATA == 'extension_data'
        assert Consts.CLOUD_DATA_TYPE_LIST == ['indexed_db', 'local_storage', 'extension_data']

    @pytest.mark.parametrize('data_type,expected', [
        (Consts.CLOUD_DATA_TYPE_INDEXED_DB, ['indexed_db']),
        (['indexed_db'], ['indexed_db']),
        ([Consts.CLOUD_DATA_TYPE_LOCAL_STORAGE, Consts.CLOUD_DATA_TYPE_EXTENSION_DATA],
         ['local_storage', 'extension_data']),
    ])
    def test_accepts_a_string_or_a_list(self, client, transport, data_type, expected):
        transport.reply(payload={'error': {'code': 0}, 'data': [1]})
        client.clear_profile_cloud_data(1, data_type)
        assert transport.last['payload']['type'] == expected

    @pytest.mark.parametrize('data_type', [
        'cookies',
        'INDEXED_DB',
        '',
        5,
        ['indexed_db', 'cookies'],
    ])
    def test_invalid_data_type_is_rejected_without_sending_a_request(self, client, transport, data_type):
        assert client.clear_profile_cloud_data(1, data_type) is None
        assert transport.call_count == 0
        assert client.code == UNEXPECTED_ERROR_CODE
        assert 'not supported' in client.message
        assert 'indexed_db' in client.message

    def test_data_type_is_a_required_argument(self):
        signature = inspect.signature(IXBrowserClient.clear_profile_cloud_data)
        assert signature.parameters['data_type'].default is inspect.Parameter.empty

    def test_profile_id_is_normalised_to_a_list(self, client, transport):
        transport.reply(payload={'error': {'code': 0}, 'data': [1]})
        client.clear_profile_cloud_data(1456, Consts.CLOUD_DATA_TYPE_INDEXED_DB)
        assert transport.last['payload']['profile_id'] == [1456]

    def test_invalid_argument_error_does_not_leak_into_the_next_call(self, client, transport):
        client.clear_profile_cloud_data(1, 'cookies')
        assert client.code == UNEXPECTED_ERROR_CODE
        transport.reply(payload={'error': {'code': 0}, 'data': [1]})
        client.clear_profile_cloud_data(1, Consts.CLOUD_DATA_TYPE_INDEXED_DB)
        assert client.code is None
        assert client.message is None


class TestProxyModeEndpoints(object):

    def test_custom_proxy_payload(self, client, transport):
        transport.reply(payload={'error': {'code': 0}, 'data': 'success'})
        client.update_profile_to_custom_proxy_mode(161, Consts.PROXY_TYPE_SOCKS5, '127.0.0.1', 10808)
        assert transport.last['url'] == BASE + 'profile-update-proxy-for-custom-proxy'
        assert transport.last['payload']['proxy_info'] == {
            'proxy_mode': Consts.PROXY_MODE_CUSTOM,
            'proxy_type': 'socks5',
            'proxy_ip': '127.0.0.1',
            'proxy_port': 10808,
            'proxy_check_line': Consts.DEFAULT_PROXY_CHECK_LINE,
        }

    def test_purchased_proxy_payload(self, client, transport):
        transport.reply(payload={'error': {'code': 0}, 'data': 'success'})
        client.update_profile_to_purchased_proxy_mode(161, 1)
        assert transport.last['url'] == BASE + 'profile-update-proxy-to-purchased-mode'
        assert transport.last['payload']['proxy_info'] == {'proxy_mode': 3, 'proxy_id': 1}

    def test_traffic_package_payload(self, client, transport):
        transport.reply(payload={'error': {'code': 0}, 'data': 'success'})
        client.update_profile_to_traffic_package_mode(27, 10, country='us', city='Ada')
        assert transport.last['url'] == BASE + 'profile-update-proxy-for-purchased-traffic-package'
        assert transport.last['payload']['proxy_info'] == {
            'proxy_mode': 1,
            'proxy_id': 10,
            'country': 'us',
            'city': 'Ada',
            'gateway': Consts.DEFAULT_DATA_PACKAGE_GATEWAY,
        }

    def test_api_extraction_payload_matches_the_documented_example(self, client, transport):
        transport.reply(payload={'error': {'code': 0, 'message': 'success'}, 'data': 'success'})
        result = client.update_profile_to_api_extraction_proxy_mode(161, 'https://127.0.0.1/extract')
        assert transport.last['url'] == BASE + 'profile-update-proxy-for-api-extraction'
        assert transport.last['payload'] == {
            'profile_id': 161,
            'proxy_info': {
                'proxy_mode': 4,
                'proxy_check_line': 'global_line',
                'proxy_type': 'socks5',
                'proxy_service': 'general',
                'proxy_data_format_type': 'txt',
                'proxy_data_txt_format': 'ip:port',
                'proxy_data_json_format': None,
                'proxy_extraction_method': 'invalid',
                'proxy_url': 'https://127.0.0.1/extract',
            },
        }
        assert result == 'success'


class TestProfileEntities(object):

    def test_create_profile_sends_the_entity_payload(self, client, transport):
        transport.reply(payload={'error': {'code': 0}, 'data': 161})
        profile = Profile()
        profile.name = 'demo'
        profile.random_color()
        profile.set_custom_page('https://www.ixbrowser.com')

        proxy = Proxy()
        proxy.change_to_custom_mode(Consts.PROXY_TYPE_SOCKS5, '127.0.0.1', '10808')
        profile.proxy_config = proxy

        client.create_profile(profile)
        payload = transport.last['payload']
        assert payload['name'] == 'demo'
        assert payload['site_id'] == Consts.DEFAULT_SITE_ID_CUSTOM_PAGE
        assert payload['site_url'] == 'https://www.ixbrowser.com'
        assert payload['color'] in Consts.DEFAULT_PROFILE_COLOR_LIST
        assert payload['proxy_config']['proxy_mode'] == Consts.PROXY_MODE_CUSTOM
        # fields left at None must not be sent
        assert 'note' not in payload
        assert 'username' not in payload

    def test_open_profile_always_adds_the_disable_welcome_page_flag(self, client, transport):
        transport.reply(payload={'error': {'code': 0}, 'data': {'webdriver': 'x', 'debugging_address': 'y'}})
        client.open_profile(1, cookies_backup=False, load_profile_info_page=False)
        payload = transport.last['payload']
        assert payload['args'] == ['--disable-extension-welcome-page']
        assert payload['cookies_backup'] is False

    def test_open_profile_does_not_mutate_the_caller_list(self, client, transport):
        transport.reply(payload={'error': {'code': 0}, 'data': {'webdriver': 'x', 'debugging_address': 'y'}})
        startup_args = ['--no-sandbox']
        client.open_profile(1, startup_args=startup_args)
        assert startup_args == ['--no-sandbox']
        assert transport.last['payload']['args'] == ['--no-sandbox', '--disable-extension-welcome-page']

    def test_open_profile_omits_cookie_when_none(self, client, transport):
        transport.reply(payload={'error': {'code': 0}, 'data': {'webdriver': 'x', 'debugging_address': 'y'}})
        client.open_profile(1, cookie=None)
        assert 'cookie' not in transport.last['payload']

    def test_update_profile_sends_the_entity_payload(self, client, transport):
        transport.reply(payload={'error': {'code': 0}, 'data': 'success'})
        profile = Profile()
        profile.profile_id = 161
        profile.name = 'renamed'
        client.update_profile(profile)
        assert transport.last['payload'] == {'profile_id': 161, 'name': 'renamed'}

    def test_entity_with_every_field_unset_is_not_sent(self, client, transport):
        # A blank Preference()/Fingerprint() used to be serialised as {} and sent,
        # which is pointless and can reset settings on the profile.
        transport.reply(payload={'error': {'code': 0}, 'data': 'success'})
        profile = Profile()
        profile.profile_id = 161
        profile.preference_config = Preference()
        profile.fingerprint_config = Fingerprint()
        client.update_profile(profile)
        assert transport.last['payload'] == {'profile_id': 161}

    def test_entity_with_one_field_is_still_sent(self, client, transport):
        transport.reply(payload={'error': {'code': 0}, 'data': 'success'})
        profile = Profile()
        profile.profile_id = 161
        profile.preference_config = Preference()
        profile.preference_config.block_image = 1
        client.update_profile(profile)
        assert transport.last['payload'] == {
            'profile_id': 161,
            'preference_config': {'block_image': 1},
        }
