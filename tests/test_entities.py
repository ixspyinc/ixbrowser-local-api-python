"""Tests for the Profile, Proxy, Preference and Fingerprint entities."""
import re

import pytest

from ixbrowser_local_api import Consts, Fingerprint, Preference, Profile, Proxy
from ixbrowser_local_api.errors import UnexpectedError


class TestProfile(object):

    def test_dump_omits_unset_fields(self):
        profile = Profile()
        profile.name = 'demo'
        profile.note = None
        assert profile.dump_to_dict() == {'name': 'demo'}

    def test_dump_keeps_false_and_zero_values(self):
        # 0 and False are meaningful for the Local API, only None means "not set".
        profile = Profile()
        profile.group_id = 0
        assert profile.dump_to_dict() == {'group_id': 0}

    def test_build_from_dict_converts_nested_entities(self):
        profile = Profile({
            'name': 'demo',
            'proxy_config': {'proxy_mode': 2, 'proxy_type': 'socks5', 'proxy_ip': '127.0.0.1'},
            'preference_config': {'block_image': 1},
            'fingerprint_config': {'language_type': 2},
        })
        assert isinstance(profile.proxy_config, Proxy)
        assert isinstance(profile.preference_config, Preference)
        assert isinstance(profile.fingerprint_config, Fingerprint)
        assert profile.proxy_config.proxy_ip == '127.0.0.1'
        assert profile.preference_config.block_image == 1

    def test_build_from_dict_rejects_a_dict_for_a_plain_field(self):
        # Only proxy_config / preference_config / fingerprint_config may hold an
        # object; any other field given a dict is a caller mistake and is rejected.
        with pytest.raises(UnexpectedError):
            Profile({'site_url': {'unexpected': 1}})

    def test_build_from_dict_ignores_unknown_scalar_keys(self):
        profile = Profile({'name': 'demo', 'not_a_field': 1})
        assert profile.dump_to_dict() == {'name': 'demo'}

    def test_set_custom_page_and_blank_page(self):
        profile = Profile()
        profile.set_custom_page('https://www.ixbrowser.com')
        assert profile.site_id == Consts.DEFAULT_SITE_ID_CUSTOM_PAGE
        assert profile.site_url == 'https://www.ixbrowser.com'

        profile.set_blank_page()
        assert profile.site_id == Consts.DEFAULT_SITE_ID_BLANK_PAGE
        assert profile.site_url is None

    def test_random_color_from_the_official_list(self):
        profile = Profile()
        profile.random_color()
        assert profile.color in Consts.DEFAULT_PROFILE_COLOR_LIST

    def test_random_color_free_form_is_a_hex_string(self):
        profile = Profile()
        profile.random_color(source='random')
        assert re.match(r'^#[0-9a-f]{6}$', profile.color)

    def test_reset_all_attributes_clears_every_field(self):
        profile = Profile()
        profile.name = 'demo'
        profile.group_id = 3
        profile.reset_all_attributes()
        assert profile.dump_to_dict() == {}


class TestProxy(object):

    def test_custom_mode_sets_defaults(self):
        proxy = Proxy()
        proxy.change_to_custom_mode()
        assert proxy.proxy_mode == Consts.PROXY_MODE_CUSTOM
        assert proxy.proxy_type == Consts.PROXY_TYPE_DIRECT
        assert proxy.proxy_check_line == Consts.DEFAULT_PROXY_CHECK_LINE

    def test_custom_mode_dump(self):
        proxy = Proxy()
        proxy.change_to_custom_mode(Consts.PROXY_TYPE_SOCKS5, '127.0.0.1', '10808',
                                    'user', 'pass', 'cn_line')
        assert proxy.dump_to_dict() == {
            'proxy_mode': Consts.PROXY_MODE_CUSTOM,
            'proxy_type': 'socks5',
            'proxy_ip': '127.0.0.1',
            'proxy_port': '10808',
            'proxy_user': 'user',
            'proxy_password': 'pass',
            'proxy_check_line': 'cn_line',
        }

    def test_purchased_mode_replaces_previous_attributes(self):
        proxy = Proxy()
        proxy.change_to_custom_mode(Consts.PROXY_TYPE_SOCKS5, '127.0.0.1', '10808')
        proxy.change_to_purchased_mode(7)
        assert proxy.dump_to_dict() == {'proxy_mode': Consts.PROXY_MODE_PURCHASED, 'proxy_id': 7}

    def test_traffic_package_mode_converts_booleans_to_integers(self):
        proxy = Proxy()
        proxy.change_to_traffic_package_mode(1, 'us', 'Ada', ip_detection=True, ip_policy=True)
        assert proxy.ip_detection == 1
        assert proxy.traffic_package_ip_policy is True
        assert proxy.dump_to_dict()['gateway'] == Consts.DEFAULT_TRAFFIC_PACKAGE_GATEWAY

    def test_url_extraction_mode_txt(self):
        proxy = Proxy()
        proxy.change_to_url_extraction_mode('https://127.0.0.1/extract')
        assert proxy.proxy_mode == Consts.PROXY_MODE_EXTRACT_FROM_URL
        assert proxy.proxy_service == 'general'
        assert proxy.proxy_data_format_type == Consts.PROXY_DATA_FROMAT_TYPE_TXT
        assert proxy.proxy_data_txt_format == Consts.PROXY_DATA_TXT_FORMAT_LIST[0]
        assert proxy.proxy_data_json_format is None
        assert proxy.proxy_extraction_method == Consts.PROXY_EXTRACT_FROM_URL_FRESH_TYPE_WHEN_INVALID

    def test_url_extraction_mode_json(self):
        proxy = Proxy()
        mapping = proxy.get_url_extraction_mode_json_mapping('ip', 'port')
        proxy.change_to_url_extraction_mode('https://127.0.0.1/extract',
                                            format_type=Consts.PROXY_DATA_FROMAT_TYPE_JSON,
                                            json_mapping=mapping)
        assert proxy.proxy_data_json_format == {'ip': 'ip', 'port': 'port'}
        assert proxy.proxy_data_txt_format is None

    def test_json_mapping_omits_absent_credentials(self):
        proxy = Proxy()
        assert proxy.get_url_extraction_mode_json_mapping('a', 'b') == {'ip': 'a', 'port': 'b'}
        assert proxy.get_url_extraction_mode_json_mapping('a', 'b', 'u', 'p') == {
            'ip': 'a', 'port': 'b', 'username': 'u', 'password': 'p'}

    def test_url_extraction_dump_contains_only_the_extraction_fields(self):
        proxy = Proxy()
        proxy.change_to_url_extraction_mode('https://127.0.0.1/extract')
        proxy.set_bypass_list(['*.ipinfo.io'])
        dumped = proxy.dump_url_extraction_mode_info_to_dict()
        assert sorted(dumped) == [
            'proxy_check_line', 'proxy_data_format_type', 'proxy_data_json_format',
            'proxy_data_txt_format', 'proxy_extraction_method', 'proxy_mode',
            'proxy_service', 'proxy_type', 'proxy_url',
        ]

    def test_url_extraction_dump_rejects_another_mode(self):
        proxy = Proxy()
        proxy.change_to_custom_mode()
        with pytest.raises(UnexpectedError):
            proxy.dump_url_extraction_mode_info_to_dict()

    def test_set_bypass_list_joins_domains(self):
        proxy = Proxy()
        proxy.set_bypass_list(['*.ipinfo.io', 'ixbrowser.com'])
        assert proxy.enable_bypass is True
        assert proxy.bypass_list == '*.ipinfo.io\nixbrowser.com'

    def test_set_bypass_list_with_a_string_keeps_it(self):
        proxy = Proxy()
        proxy.set_bypass_list('*.ipinfo.io\nixbrowser.com')
        assert proxy.enable_bypass is True
        assert proxy.bypass_list == '*.ipinfo.io\nixbrowser.com'

    def test_set_bypass_list_disables_on_empty_input(self):
        proxy = Proxy()
        proxy.set_bypass_list([])
        assert proxy.enable_bypass is False
        assert proxy.bypass_list == ''

        proxy.set_bypass_list(None)
        assert proxy.enable_bypass is False
        assert proxy.bypass_list == ''


class TestPreference(object):

    def test_cloud_backup_stores_every_flag(self):
        preference = Preference()
        preference.set_cloud_backup(1, 1, 1, 1)
        assert preference.dump_to_dict() == {
            'cookies_backup': 1,
            'indexed_db_backup': 1,
            'local_storage_backup': 1,
            'extension_data_backup': 1,
        }

    def test_cloud_backup_disabling_cookies_disables_the_rest(self):
        # Documented behaviour: without cookie backup the other cloud data
        # cannot be stored either.
        preference = Preference()
        preference.set_cloud_backup(0, 1, 1, 1)
        assert preference.dump_to_dict() == {
            'cookies_backup': 0,
            'indexed_db_backup': 0,
            'local_storage_backup': 0,
            'extension_data_backup': 0,
        }

    def test_dump_omits_unset_fields(self):
        preference = Preference()
        assert preference.dump_to_dict() == {}
        preference.block_image = 0
        assert preference.dump_to_dict() == {'block_image': 0}

    def test_build_from_dict(self):
        preference = Preference({'block_image': 1, 'unknown': 2})
        assert preference.dump_to_dict() == {'block_image': 1}


class TestFingerprint(object):

    def test_set_device_name_marks_the_source_as_custom(self):
        fingerprint = Fingerprint()
        fingerprint.set_device_name('demo-device')
        assert fingerprint.device_name == 'demo-device'
        assert fingerprint.device_name_source == Consts.DEVICE_NAME_SOURCE_CUSTOM

    def test_dump_omits_unset_fields(self):
        fingerprint = Fingerprint()
        fingerprint.ua_info = 'Mozilla/5.0'
        fingerprint.track = 0
        assert fingerprint.dump_to_dict() == {'ua_info': 'Mozilla/5.0', 'track': 0}

    def test_build_from_dict(self):
        fingerprint = Fingerprint({'language_type': 2, 'language': 'cn', 'unknown': 1})
        assert fingerprint.dump_to_dict() == {'language_type': 2, 'language': 'cn'}

    def test_reset_all_attributes(self):
        fingerprint = Fingerprint({'language_type': 2})
        fingerprint.reset_all_attributes()
        assert fingerprint.dump_to_dict() == {}
