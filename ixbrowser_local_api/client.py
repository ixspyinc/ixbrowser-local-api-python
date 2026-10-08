import json
import warnings
from typing import Any, Dict, Optional, Union

import requests

from .consts import Consts
from .entities import Fingerprint, Preference, Profile, Proxy
from .errors import BaseError, UnexpectedError
from .utils import Utils

# Nested configurations may be given as an entity or as its plain-dict form.
ProxyConfig = Union[Proxy, Dict[str, Any]]
FingerprintConfig = Union[Fingerprint, Dict[str, Any]]
PreferenceConfig = Union[Preference, Dict[str, Any]]


class IXBrowserClient(object):
    """Client for the ixBrowser Local API.

    Instances keep the latest request state in ``code``, ``message`` and
    ``total``. They are intentionally not safe to share between concurrent
    callers.
    """

    def __init__(self, target=Consts.DEFAULT_API_TARGET, port=Consts.DEFAULT_API_PORT,
                 timeout=20, session=None):
        self.base_url = "http://{}:{}/api/v2/".format(target, port)
        self.timeout = timeout
        self._owns_session = session is None
        self.session = requests.Session() if session is None else session
        self.total = None
        self.code = None
        self.message = None

    def close(self):
        """Close the internally owned HTTP session."""
        if self._owns_session:
            self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def _reset_request_state(self):
        self.code = None
        self.message = None
        self.total = None

    def _dispatch_action(self, action, params=None, paginated=False,
                         force_boolean_success=False, transform=None, list_result=False):
        """Build, send and unwrap one request under the common error contract.

        ``list_result`` marks non-paginated endpoints whose data is a list: a
        successful ``data: null`` or a response without ``data`` is then
        returned as ``[]`` instead of ``True``.
        """
        self._reset_request_state()
        try:
            payload = params() if callable(params) else (params or {})
            result = Utils.get_api_response(
                self.base_url + action, payload, timeout=self.timeout, session=self.session)
            if paginated:
                self.total, data = Utils.get_paginated_data(result)
                return data
            # Utils.get_api_response reports a missing 'data' key as True, so
            # True is the "no data" marker here; a list endpoint never
            # legitimately answers with a boolean.
            if list_result and (result is None or result is True):
                return []
            if force_boolean_success or result is None:
                return True
            if transform is not None:
                return transform(result)
            return result
        except BaseError as error:
            self.code = error.code
            self.message = error.message
            return None

    @staticmethod
    def _profile_payload(profile):
        if profile is None:
            raise UnexpectedError('profile is required and cannot be None')
        if not isinstance(profile, Profile):
            raise UnexpectedError('profile must be a Profile instance')
        return profile.dump_to_dict()

    @staticmethod
    def _startup_args(startup_args):
        if startup_args is None:
            return []
        if isinstance(startup_args, (str, bytes)):
            raise UnexpectedError('startup_args must be an iterable of strings, not a string')
        try:
            copied = list(startup_args)
        except TypeError as error:
            raise UnexpectedError('startup_args must be an iterable of strings') from error
        if not all(isinstance(arg, str) for arg in copied):
            raise UnexpectedError('startup_args must contain only strings')
        return copied

    @staticmethod
    def _profile_ids(profile_id):
        if isinstance(profile_id, (list, tuple, set, frozenset)):
            return list(profile_id)
        return [profile_id]

    @staticmethod
    def _entity_payload(name, entity):
        """Serialise a nested configuration given as an entity or a plain dict."""
        if isinstance(entity, dict):
            return dict(entity)
        dump = getattr(entity, 'dump_to_dict', None)
        if not callable(dump):
            raise UnexpectedError(name + ' must be a dictionary or an entity with dump_to_dict()')
        payload = dump()
        if not isinstance(payload, dict):
            raise UnexpectedError(name + '.dump_to_dict() must return a dictionary')
        return payload

    @staticmethod
    def _is_positive_filter(name, value):
        """Return whether an optional numeric filter is set; ``None``/``0`` mean unset."""
        if value is None:
            return False
        if isinstance(value, bool) or not isinstance(value, int):
            raise UnexpectedError('{} must be an integer, got: {!r}'.format(name, value))
        return value > 0

    def get_profile_list(self, keyword=None, group_id=0, page=1, limit=10, tag_id=0, profile_id=0):
        def build_params():
            params = {}
            if profile_id is None or profile_id == 0:
                params.update(page=page, limit=limit)
                if self._is_positive_filter('group_id', group_id):
                    params['group_id'] = group_id
                if self._is_positive_filter('tag_id', tag_id):
                    params['tag_id'] = tag_id
                if keyword:
                    params['name'] = keyword
            else:
                params['profile_id'] = profile_id
            return params

        return self._dispatch_action(Consts.ACTION_FOR_PROFILE_LIST, build_params, paginated=True)

    def get_opened_profile_list(self):
        return self._dispatch_action(Consts.ACTION_FOR_PROFILE_OPENED_LIST, list_result=True)

    def get_native_opened_profile_list(self):
        return self._dispatch_action(Consts.ACTION_FOR_PROFILE_NATIVE_OPENED_LIST, list_result=True)

    def open_profile(self, profile_id, load_extensions=True, load_profile_info_page=False,
                     cookies_backup=True, cookie=None, disable_extension_welcome_page=True,
                     startup_args=None):
        def build_params():
            args = self._startup_args(startup_args)
            if disable_extension_welcome_page and '--disable-extension-welcome-page' not in args:
                args.append('--disable-extension-welcome-page')
            params = {
                'profile_id': profile_id,
                'load_extensions': load_extensions,
                'load_profile_info_page': load_profile_info_page,
                'cookies_backup': cookies_backup,
                'args': args,
            }
            if cookie is not None:
                params['cookie'] = cookie
            return params

        return self._dispatch_action(Consts.ACTION_FOR_PROFILE_OPEN, build_params)

    def open_profile_with_random_fingerprint(
            self, profile_id, load_extensions=True, load_profile_info_page=False,
            cookie=None, disable_extension_welcome_page=True, startup_args=None,
            proxy_config: Optional[ProxyConfig] = None,
            fingerprint_config: Optional[FingerprintConfig] = None,
            preference_config: Optional[PreferenceConfig] = None):
        def build_params():
            args = self._startup_args(startup_args)
            if disable_extension_welcome_page and '--disable-extension-welcome-page' not in args:
                args.append('--disable-extension-welcome-page')
            params = {
                'profile_id': profile_id,
                'load_extensions': load_extensions,
                'load_profile_info_page': load_profile_info_page,
                'args': args,
            }
            if cookie is not None:
                params['cookie'] = cookie
            for key, entity in (
                    ('proxy_config', proxy_config),
                    ('fingerprint_config', fingerprint_config),
                    ('preference_config', preference_config)):
                if entity is not None:
                    params[key] = self._entity_payload(key, entity)
            return params

        return self._dispatch_action(Consts.ACTION_FOR_PROFILE_OPEN_WITH_FINGERPRINT, build_params)

    def arrange_tile_opened_profile(
            self, screen=None, layout=None, adaptive=None, starting_position_x=None,
            starting_position_y=None, profile_size_width=None, profile_size_hight=None,
            profile_spacing_horizontal=None, profile_spacing_vertical=None,
            profile_deviaton_x=None, profile_deviaton_y=None,
            per_line_number_of_profiles=None):
        values = {
            'screen': screen, 'layout': layout, 'adaptive': adaptive,
            'starting_position_x': starting_position_x,
            'starting_position_y': starting_position_y,
            'profile_size_width': profile_size_width,
            'profile_size_hight': profile_size_hight,
            'profile_spacing_horizontal': profile_spacing_horizontal,
            'profile_spacing_vertical': profile_spacing_vertical,
            'profile_deviaton_x': profile_deviaton_x,
            'profile_deviaton_y': profile_deviaton_y,
            'per_line_number_of_profiles': per_line_number_of_profiles,
        }
        params = {key: value for key, value in values.items() if value is not None}
        return self._dispatch_action(
            Consts.ACTION_FOR_PROFILE_OPENED_LIST_ARRANGE_TILE,
            params,
            force_boolean_success=True,
        )

    def close_profile(self, profile_id):
        return self._dispatch_action(Consts.ACTION_FOR_PROFILE_CLOSE, {'profile_id': profile_id})

    @staticmethod
    def close_profile_via_selenium(obj):
        """Deprecated Selenium helper. Prefer :meth:`close_profile`."""
        warnings.warn(
            'close_profile_via_selenium is deprecated; use close_profile instead',
            DeprecationWarning,
            stacklevel=2,
        )
        selenium4_switch = getattr(getattr(obj, 'switch_to', None), 'window', None)
        for handle in obj.window_handles:
            if selenium4_switch is not None:
                selenium4_switch(handle)
            else:
                obj.switch_to_window(handle)
            obj.close()

    def close_profile_in_batches(self, profile_id):
        return self._dispatch_action(
            Consts.ACTION_FOR_PROFILE_CLOSE_IN_BATCHES,
            {'profile_id': self._profile_ids(profile_id)},
        )

    def reset_profile_open_state(self, profile_id):
        """Reset profile open state; return ``True`` on success."""
        return self._dispatch_action(
            Consts.ACTION_FOR_PROFILE_OPEN_STATE_RESET,
            {'profile_id': profile_id},
            force_boolean_success=True,
        )

    def create_profile(self, profile: Optional[Profile] = None):
        return self._dispatch_action(
            Consts.ACTION_FOR_PROFILE_CREATE,
            lambda: self._profile_payload(profile),
        )

    def create_profile_by_copying(self, profile_id, name=None, group_id=None,
                                  site_id=None, site_url=None):
        params = {'profile_id': profile_id}
        if name is not None:
            params['name'] = name
        if group_id is not None:
            params['group_id'] = group_id
        if site_id is not None:
            params['site_id'] = site_id
            if site_id == Consts.DEFAULT_SITE_ID_BLANK_PAGE:
                site_url = None
        if site_url is not None:
            params['site_url'] = site_url
        return self._dispatch_action(Consts.ACTION_FOR_PROFILE_COPY, params)

    def update_profile(self, profile: Optional[Profile] = None):
        return self._dispatch_action(
            Consts.ACTION_FOR_PROFILE_UPDATE,
            lambda: self._profile_payload(profile),
        )

    def update_profile_to_traffic_package_mode(self, profile_id, proxy_id,
                                               country=None, city=None, gateway=None):
        proxy_info = {'proxy_mode': Consts.PROXY_MODE_TRAFFIC_PACKAGE, 'proxy_id': proxy_id}
        if country is not None:
            proxy_info['country'] = country
        if city is not None:
            proxy_info['city'] = city
        proxy_info['gateway'] = Consts.DEFAULT_DATA_PACKAGE_GATEWAY if gateway is None else gateway
        return self._dispatch_action(
            Consts.ACTION_FOR_PROFILE_UPDATE_PROXY_TO_TRAFFIC_PACKAGE_MODE,
            {'profile_id': profile_id, 'proxy_info': proxy_info},
        )

    def update_profile_to_purchased_proxy_mode(self, profile_id, proxy_id):
        return self._dispatch_action(
            Consts.ACTION_FOR_PROFILE_UPDATE_PROXY_TO_PURCHASED_MODE,
            {
                'profile_id': profile_id,
                'proxy_info': {'proxy_mode': Consts.PROXY_MODE_PURCHASED, 'proxy_id': proxy_id},
            },
        )

    def update_profile_to_custom_proxy_mode(
            self, profile_id, proxy_type=Consts.PROXY_TYPE_DIRECT, proxy_ip=None,
            proxy_port=None, proxy_user=None, proxy_password=None, proxy_check_line=None):
        proxy_info = {
            'proxy_mode': Consts.PROXY_MODE_CUSTOM,
            'proxy_type': proxy_type,
            'proxy_check_line': (Consts.DEFAULT_PROXY_CHECK_LINE
                                 if proxy_check_line is None else proxy_check_line),
        }
        for key, value in (
                ('proxy_ip', proxy_ip), ('proxy_port', proxy_port),
                ('proxy_user', proxy_user), ('proxy_password', proxy_password)):
            if value is not None:
                proxy_info[key] = value
        return self._dispatch_action(
            Consts.ACTION_FOR_PROFILE_UPDATE_PROXY_TO_CUSTOM_MODE,
            {'profile_id': profile_id, 'proxy_info': proxy_info},
        )

    def update_profile_to_api_extraction_proxy_mode(
            self, profile_id, proxy_url,
            format_type=Consts.PROXY_DATA_FORMAT_TYPE_TXT,
            proxy_type=Consts.PROXY_TYPE_SOCKS5,
            extract_method=Consts.PROXY_EXTRACT_FROM_URL_FRESH_TYPE_WHEN_INVALID,
            txt_mapping=None, json_mapping=None,
            proxy_check_line=Consts.DEFAULT_PROXY_CHECK_LINE):
        def build_params():
            proxy = Proxy()
            proxy.change_to_url_extraction_mode(
                proxy_url, format_type, proxy_type, extract_method,
                txt_mapping, json_mapping, proxy_check_line,
            )
            return {
                'profile_id': profile_id,
                'proxy_info': proxy.dump_url_extraction_mode_info_to_dict(),
            }

        return self._dispatch_action(
            Consts.ACTION_FOR_PROFILE_UPDATE_PROXY_TO_API_EXTRACTION_MODE,
            build_params,
        )

    def random_profile_fingerprint(self, profile_id):
        return self._dispatch_action(
            Consts.ACTION_FOR_PROFILE_RANDOM_FINGERPRINT,
            {'profile_id': profile_id},
        )

    def create_profile_transfer_code(self, profile_id, login_pwd, transfer_note=None,
                                     transfer_proxy=None, transfer_proxy_mode=None):
        def build_params():
            params = {'profile_id': profile_id, 'password': login_pwd}
            if transfer_note is not None:
                params['transfer_note'] = 1 if transfer_note else 0
            if transfer_proxy is not None:
                params['transfer_proxy'] = 1 if transfer_proxy else 0
                if params['transfer_proxy'] == 1 and transfer_proxy_mode is not None:
                    supported = {
                        Consts.TRANSFER_PROXY_MODE_SHARING,
                        Consts.TRANSFER_PROXY_MODE_TRANSFER,
                    }
                    if transfer_proxy_mode not in supported:
                        raise UnexpectedError(
                            'transfer_proxy_mode must be one of: {}'.format(sorted(supported)))
                    params['transfer_proxy_mode'] = transfer_proxy_mode
            return params

        def extract_transfer_code(result):
            if isinstance(result, dict) and 'transfer_code' in result:
                return result['transfer_code']
            return result

        return self._dispatch_action(
            Consts.ACTION_FOR_PROFILE_CREATE_TRANSFER_CODE,
            build_params,
            transform=extract_transfer_code,
        )

    def cancel_profile_transfer_code(self, profile_id):
        return self._dispatch_action(
            Consts.ACTION_FOR_PROFILE_CANCEL_TRANSFER_CODE,
            {'profile_id': profile_id},
        )

    def import_profile_via_transfer_code(
            self, transfer_code, proxy_config: Optional[ProxyConfig] = None):
        def build_params():
            params = {'transfer_code': transfer_code}
            if proxy_config is not None:
                params['proxy_config'] = self._entity_payload('proxy_config', proxy_config)
            return params

        return self._dispatch_action(
            Consts.ACTION_FOR_PROFILE_IMPORT_VIA_TRANSFER_CODE,
            build_params,
        )

    def get_profile_transfer_record_list(
            self, keyword=None, record_type=Consts.TRANSFER_RECORD_LIST_TYPE_TRANSFER,
            page=1, limit=10):
        def build_params():
            params = {'page': page, 'limit': limit}
            if self._is_positive_filter('record_type', record_type):
                params['type'] = record_type
            if keyword:
                params['title'] = keyword
            return params

        return self._dispatch_action(
            Consts.ACTION_FOR_PROFILE_TRANSFER_RECORD_LIST,
            build_params,
            paginated=True,
        )

    def update_profile_groups_in_batches(self, profile_id, group_id):
        return self._dispatch_action(
            Consts.ACTION_FOR_PROFILE_UPDATE_GROUPS_IN_BATCHES,
            {'group_id': group_id, 'profile_id': self._profile_ids(profile_id)},
        )

    def delete_profile(self, profile_id):
        return self._dispatch_action(Consts.ACTION_FOR_PROFILE_DELETE, {'profile_id': profile_id})

    def empty_recycle_bin(self):
        return self._dispatch_action(Consts.ACTION_FOR_PROFILE_EMPTY_RECYCLE_BIN)

    def get_profile_cookie(self, profile_id):
        return self._dispatch_action(
            Consts.ACTION_FOR_PROFILE_GET_COOKIES,
            {'profile_id': profile_id},
        )

    def update_profile_cookie(self, profile_id, cookie):
        """Replace profile cookies.

        ``cookie`` is a JSON string or a JSON-serialisable value. ``None`` is
        rejected so a missing value can never wipe the cookies by accident;
        pass ``''`` explicitly to clear them.
        """
        def build_params():
            if cookie is None:
                raise UnexpectedError("cookie is required; pass '' explicitly to clear cookies")
            if isinstance(cookie, str):
                serialised = cookie
            else:
                try:
                    serialised = json.dumps(cookie)
                except (TypeError, ValueError) as error:
                    raise UnexpectedError('cookie must be a string or JSON serialisable') from error
            return {'profile_id': profile_id, 'cookie': serialised}

        return self._dispatch_action(Consts.ACTION_FOR_PROFILE_UPDATE_COOKIES, build_params)

    def clear_profile_cache(self, profile_id):
        return self._dispatch_action(
            Consts.ACTION_FOR_PROFILE_CLEAR_CACHE,
            {'profile_id': self._profile_ids(profile_id)},
        )

    def clear_profile_cache_and_cookies(self, profile_id):
        return self._dispatch_action(
            Consts.ACTION_FOR_PROFILE_CLEAR_CACHE_AND_COOKIES,
            {'profile_id': self._profile_ids(profile_id)},
        )

    def clear_profile_cache_keep_extensions(self, profile_id):
        return self._dispatch_action(
            Consts.ACTION_FOR_PROFILE_CLEAR_CACHE_KEEP_EXTENSIONS,
            {'profile_id': self._profile_ids(profile_id)},
        )

    def clear_profile_cloud_data(self, profile_id, data_type=None):
        def build_params():
            if data_type is None:
                raise UnexpectedError(
                    'data_type is required. The optional values are: {}.'.format(
                        Consts.CLOUD_DATA_TYPE_LIST))
            elif isinstance(data_type, list):
                data_types = data_type
            else:
                data_types = [data_type]
            invalid = [item for item in data_types if item not in Consts.CLOUD_DATA_TYPE_LIST]
            if invalid:
                raise UnexpectedError(
                    'The data_type is not supported: {}. The optional values are: {}.'.format(
                        invalid, Consts.CLOUD_DATA_TYPE_LIST))
            return {'profile_id': self._profile_ids(profile_id), 'type': data_types}

        return self._dispatch_action(Consts.ACTION_FOR_PROFILE_CLEAR_CLOUD_DATA, build_params)

    def clear_profile_saved_user_password(self, profile_id):
        """Clear saved credentials; return ``True`` on success."""
        return self._dispatch_action(
            Consts.ACTION_FOR_PROFILE_CLEAR_SAVED_USER_PASSWORD,
            {'profile_id': profile_id},
            force_boolean_success=True,
        )

    def get_group_list(self, page=1, limit=100):
        return self._dispatch_action(
            Consts.ACTION_FOR_GROUP_LIST,
            {'page': page, 'limit': limit},
            paginated=True,
        )

    def create_group(self, name, sort=0):
        return self._dispatch_action(
            Consts.ACTION_FOR_GROUP_CREATE,
            {'title': name, 'sort': 0 if sort is None else sort},
        )

    def update_group(self, group_id, name, sort=None):
        params = {'id': group_id, 'title': name}
        if sort is not None:
            params['sort'] = sort
        return self._dispatch_action(Consts.ACTION_FOR_GROUP_UPDATE, params)

    def delete_group(self, group_id):
        return self._dispatch_action(Consts.ACTION_FOR_GROUP_DELETE, {'id': group_id})

    def get_traffic_package_list(self):
        return self._dispatch_action(
            Consts.ACTION_FOR_TRAFFIC_PACKAGE_LIST,
            {'page': 1, 'limit': 100},
            paginated=True,
        )

    def get_proxy_list(self, mode=0, tag_id=None, id=None, page=1, limit=10):
        def build_params():
            params = {'page': page, 'limit': limit}
            if self._is_positive_filter('mode', mode):
                params['type'] = mode
            if tag_id is not None:
                params['tag_id'] = tag_id
            if id is not None:
                params['id'] = id
            return params

        return self._dispatch_action(Consts.ACTION_FOR_PROXY_LIST, build_params, paginated=True)

    def get_proxy_tag_list(self, name=None, page=1, limit=100):
        params = {'page': page, 'limit': limit}
        if name is not None:
            params['title'] = name
        return self._dispatch_action(Consts.ACTION_FOR_PROXY_TAG_LIST, params, paginated=True)

    def create_proxy_tag(self, name):
        return self._dispatch_action(Consts.ACTION_FOR_PROXY_TAG_CREATE, {'title': name})

    def update_proxy_tag(self, id, name):
        return self._dispatch_action(
            Consts.ACTION_FOR_PROXY_TAG_UPDATE,
            {'id': id, 'title': name},
        )

    def delete_proxy_tag(self, id):
        return self._dispatch_action(Consts.ACTION_FOR_PROXY_TAG_DELETE, {'id': id})

    def create_proxy(self, proxy_type, proxy_ip, proxy_port, proxy_user=None,
                     proxy_password=None, note=None, tag=None):
        params = {'proxy_type': proxy_type, 'proxy_ip': proxy_ip, 'proxy_port': proxy_port}
        for key, value in (
                ('proxy_user', proxy_user), ('proxy_password', proxy_password),
                ('note', note), ('tag', tag)):
            if value is not None:
                params[key] = value
        return self._dispatch_action(Consts.ACTION_FOR_PROXY_CREATE, params)

    def update_proxy(self, proxy_id, proxy_type=None, proxy_ip=None, proxy_port=None,
                     proxy_user=None, proxy_password=None, note=None, tag=None):
        params = {'id': proxy_id}
        for key, value in (
                ('proxy_type', proxy_type), ('proxy_ip', proxy_ip),
                ('proxy_port', proxy_port), ('proxy_user', proxy_user),
                ('proxy_password', proxy_password), ('note', note), ('tag', tag)):
            if value is not None:
                params[key] = value
        return self._dispatch_action(Consts.ACTION_FOR_PROXY_UPDATE, params)

    def delete_proxy(self, proxy_id):
        return self._dispatch_action(Consts.ACTION_FOR_PROXY_DELETE, {'id': proxy_id})

    def get_tag_list(self, page=1, limit=100):
        return self._dispatch_action(
            Consts.ACTION_FOR_TAG_LIST,
            {'page': page, 'limit': limit},
            paginated=True,
        )

    def create_tag(self, name):
        return self._dispatch_action(Consts.ACTION_FOR_TAG_CREATE, {'title': name})

    def update_tag(self, tag_id, name, sort=None):
        params = {'id': tag_id, 'title': name}
        if sort is not None:
            params['sort'] = sort
        return self._dispatch_action(Consts.ACTION_FOR_TAG_UPDATE, params)

    def delete_tag(self, tag_id):
        return self._dispatch_action(Consts.ACTION_FOR_TAG_DELETE, {'id': tag_id})

    def get_gateway_list(self):
        return self._dispatch_action(Consts.ACTION_FOR_GATEWAY_LIST, list_result=True)

    def switch_gateway(self, gateway_id):
        """Switch gateway; return ``True`` on success."""
        return self._dispatch_action(
            Consts.ACTION_FOR_GATEWAY_SWITCH,
            {'id': gateway_id},
            force_boolean_success=True,
        )
