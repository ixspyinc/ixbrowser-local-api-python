import json
from .errors import UnexpectedError, HttpError, ResponseError, BaseError
from .utils import Utils
from .consts import Consts
from .entities import Profile, Proxy, Preference, Fingerprint


class IXBrowserClient(object):
    def __init__(self, target=Consts.DEFAULT_API_TARGET, port=Consts.DEFAULT_API_PORT):
        """

        :param target:
        :param port:
        """
        self.base_url = "http://{}:{}/api/v2/".format(target, port)

        self.total = None
        self.code = None
        self.message = None

        self.show_request_log = False

    def get_profile_list(self, keyword=None, group_id=0, page=1, limit=10):
        """
        get profile list
        :param keyword:
        :param group_id:
        :param page:
        :param limit:
        :return: list
        """
        url = self.base_url + Consts.ACTION_FOR_PROFILE_LIST
        params = dict()
        params['page'] = page
        params['limit'] = limit
        if group_id > 0:
            params['group_id'] = group_id

        if keyword is not None and keyword != '':
            params['name'] = keyword

        try:
            self.code = None
            Utils.show_request_log = self.show_request_log
            result = Utils.get_api_response(url, params)
            self.total = result['total']
            return result['data']
        except BaseError as e:
            self.code = e.code
            self.message = e.message

        if self.code is not None:
            return None
        else:
            return True

    def open_profile(self, profile_id, load_extensions=True, load_profile_info_page=False, cookies_backup=True,
                     cookie=None, disable_extension_welcome_page=True, startup_args=[]):
        """
        open profile
        :param profile_id:
        :param load_extensions:
        :param load_profile_info_page:
        :param cookies_backup:
        :param cookie:
        :param disable_extension_welcome_page:
        :param startup_args:
        :return:
        """
        url = self.base_url + Consts.ACTION_FOR_PROFILE_OPEN
        params = dict()
        params['profile_id'] = profile_id
        params['load_extensions'] = load_extensions
        params['load_profile_info_page'] = load_profile_info_page
        params['cookies_backup'] = cookies_backup
        params['cookie'] = cookie
        if startup_args is None:
            startup_args = []
        if disable_extension_welcome_page:
            startup_args.append('--disable-extension-welcome-page')
        params['args'] = startup_args

        try:
            self.code = None
            Utils.show_request_log = self.show_request_log
            result = Utils.get_api_response(url, params)
            return result
        except BaseError as e:
            self.code = e.code
            self.message = e.message
        if self.code is not None:
            return None
        else:
            return True

    def open_profile_with_random_fingerprint(self, profile_id, load_extensions=True, load_profile_info_page=False,
                                             cookie=None, disable_extension_welcome_page=True, startup_args=[],
                                             proxy_config: Proxy = None):
        """
        open profile with random fingerprint
        :param profile_id:
        :param load_extensions:
        :param load_profile_info_page:
        :param cookie:
        :param disable_extension_welcome_page:
        :param startup_args:
        :param proxy_config:
        :return:
        """
        url = self.base_url + Consts.ACTION_FOR_PROFILE_OPEN_WITH_FINGERPRINT
        params = dict()
        params['profile_id'] = profile_id
        params['load_extensions'] = load_extensions
        params['load_profile_info_page'] = load_profile_info_page
        params['cookie'] = cookie
        if startup_args is None:
            startup_args = []
        if disable_extension_welcome_page:
            startup_args.append('--disable-extension-welcome-page')
        params['args'] = startup_args

        if proxy_config is not None:
            params['proxy_config'] = proxy_config.dump_to_dict()

        try:
            self.code = None
            Utils.show_request_log = self.show_request_log
            result = Utils.get_api_response(url, params)
            return result
        except BaseError as e:
            self.code = e.code
            self.message = e.message
        if self.code is not None:
            return None
        else:
            return True

    def close_profile(self, profile_id):
        """
        close profile
        The window is currently closed by killing the process, so it is not recommended at this time.
        It is recommended to use selenium's close method to close the profile.
        For example IXBrowserClient.close_profile_via_selenium
        :param profile_id:
        :return:
        """
        url = self.base_url + Consts.ACTION_FOR_PROFILE_CLOSE
        params = dict()

        params['profile_id'] = profile_id

        try:
            self.code = None
            Utils.show_request_log = self.show_request_log
            result = Utils.get_api_response(url, params)
            return result
        except BaseError as e:
            self.code = e.code
            self.message = e.message

        if self.code is not None:
            return None
        else:
            return True

    @staticmethod
    def close_profile_via_selenium(obj):
        """
        Alias method of close_profile
        :param obj: selenium.webdriver.chrome instance
        :return:
        """
        whs = obj.window_handles
        for handle in whs:
            obj.switch_to_window(handle)
            obj.close()

    def close_profile_in_batches(self, profile_id: list):
        """
        close profile in batches
        :param profile_id:
        :return:
        """
        url = self.base_url + Consts.ACTION_FOR_PROFILE_CLOSE_IN_BATCHES
        params = dict()

        params['profile_id'] = profile_id

        try:
            self.code = None
            Utils.show_request_log = self.show_request_log
            result = Utils.get_api_response(url, params)
            return result
        except BaseError as e:
            self.code = e.code
            self.message = e.message

        if self.code is not None:
            return None
        else:
            return True

    def create_profile(self, profile: Profile = None):
        """
        create profile
        :param profile: Profile entity class
        :return: integer
        """
        url = self.base_url + Consts.ACTION_FOR_PROFILE_CREATE

        params = profile.dump_to_dict()
        try:
            self.code = None
            Utils.show_request_log = self.show_request_log
            result = Utils.get_api_response(url, params)
            return result
        except BaseError as e:
            self.code = e.code
            self.message = e.message

        if self.code is not None:
            return None
        else:
            return True

    def update_profile(self, profile: Profile = None):
        """
        update profile
        :param profile:
        :return: string
        """
        url = self.base_url + Consts.ACTION_FOR_PROFILE_UPDATE
        params = profile.dump_to_dict()
        try:
            self.code = None
            Utils.show_request_log = self.show_request_log
            result = Utils.get_api_response(url, params)
            return result
        except BaseError as e:
            self.code = e.code
            self.message = e.message

        if self.code is not None:
            return None
        else:
            return True

    def update_profile_to_traffic_package_mode(self, profile_id, proxy_id, country=None, city=None,
                                               gateway=None):
        """
        update profile to traffic package mode
        :param profile_id:
        :param proxy_id:
        :param country:
        :param city:
        :param gateway:
        :return: string
        """
        url = self.base_url + Consts.ACTION_FOR_PROFILE_UPDATE_PROXY_TO_TRAFFIC_PACKAGE_MODE
        params = dict()
        params['profile_id'] = profile_id
        params['proxy_info'] = dict()
        params['proxy_info']['proxy_mode'] = Consts.PROXY_MODE_TRAFFIC_PACKAGE
        params['proxy_info']['proxy_id'] = proxy_id
        if country is not None:
            params['proxy_info']['country'] = country
        if city is not None:
            params['proxy_info']['city'] = city

        if gateway is None:
            params['proxy_info']['gateway'] = Consts.DEFAULT_TRAFFIC_PACKAGE_GATEWAY
        else:
            params['proxy_info']['gateway'] = gateway

        try:
            self.code = None
            Utils.show_request_log = self.show_request_log
            result = Utils.get_api_response(url, params)
            return result
        except BaseError as e:
            self.code = e.code
            self.message = e.message

        if self.code is not None:
            return None
        else:
            return True

    def update_profile_to_purchased_proxy_mode(self, profile_id, proxy_id):
        """
        update profile to purchased proxy mode
        :param profile_id:
        :param proxy_id:
        :return: string
        """
        url = self.base_url + Consts.ACTION_FOR_PROFILE_UPDATE_PROXY_TO_PURCHASED_MODE
        params = dict()
        params['profile_id'] = profile_id
        params['proxy_info'] = dict()
        params['proxy_info']['proxy_mode'] = Consts.PROXY_MODE_PURCHASED
        params['proxy_info']['proxy_id'] = proxy_id
        try:
            self.code = None
            Utils.show_request_log = self.show_request_log
            result = Utils.get_api_response(url, params)
            return result
        except BaseError as e:
            self.code = e.code
            self.message = e.message

        if self.code is not None:
            return None
        else:
            return True

    def update_profile_to_custom_proxy_mode(self, profile_id, proxy_type=Consts.PROXY_TYPE_DIRECT, proxy_ip=None,
                                            proxy_port=None, proxy_user=None, proxy_password=None):
        """
        update profile to custom proxy mode
        :param profile_id:
        :param proxy_type:
        :param proxy_ip:
        :param proxy_port:
        :param proxy_user:
        :param proxy_password:
        :return: string
        """
        url = self.base_url + Consts.ACTION_FOR_PROFILE_UPDATE_PROXY_TO_CUSTOM_MODE
        params = dict()
        params['profile_id'] = profile_id
        params['proxy_info'] = dict()
        params['proxy_info']['proxy_mode'] = Consts.PROXY_MODE_CUSTOM
        params['proxy_info']['proxy_type'] = proxy_type
        if proxy_ip is not None:
            params['proxy_info']['proxy_ip'] = proxy_ip
        if proxy_port is not None:
            params['proxy_info']['proxy_port'] = proxy_port
        if proxy_user is not None:
            params['proxy_info']['proxy_user'] = proxy_user
        if proxy_password is not None:
            params['proxy_info']['proxy_password'] = proxy_password
        try:
            self.code = None
            Utils.show_request_log = self.show_request_log
            result = Utils.get_api_response(url, params)
            return result
        except BaseError as e:
            self.code = e.code
            self.message = e.message

        if self.code is not None:
            return None
        else:
            return True

    def random_profile_fingerprint(self, profile_id):
        """
        random profile fingerprint
        :param profile_id:
        :return:
        """
        url = self.base_url + Consts.ACTION_FOR_PROFILE_RANDOM_FINGERPRINT
        params = dict()
        params['profile_id'] = profile_id
        try:
            self.code = None
            Utils.show_request_log = self.show_request_log
            result = Utils.get_api_response(url, params)
            return result
        except BaseError as e:
            self.code = e.code
            self.message = e.message

        if self.code is not None:
            return None
        else:
            return True

    def create_profile_transfer_code(self, profile_id, login_pwd, transfer_note=None, transfer_proxy=None,
                                     transfer_proxy_mode=None):
        """
        create profile transfer code
        :param profile_id:
        :param login_pwd: login password
        :param transfer_note: 0=disable 1=enable
        :param transfer_proxy: 0=disable 1=enable
        :param transfer_proxy_mode: 1=proxy sharing 2=proxy transfer
        :return:
        """
        url = self.base_url + Consts.ACTION_FOR_PROFILE_CREATE_TRANSFER_CODE
        params = dict()
        params['profile_id'] = profile_id
        params['password'] = login_pwd
        if transfer_note is not None:
            params['transfer_note'] = 1 if transfer_note else 0
        if transfer_proxy is not None:
            params['transfer_proxy'] = 1 if transfer_proxy else 0
            if params['transfer_proxy'] == 1:
                if transfer_proxy_mode is not None:
                    if transfer_proxy_mode == Consts.TRANSFER_PROXY_MODE_TRANSFER:
                        params['transfer_proxy_mode'] = Consts.TRANSFER_PROXY_MODE_TRANSFER
                    else:
                        params['transfer_proxy_mode'] = Consts.TRANSFER_PROXY_MODE_SHARING
        try:
            self.code = None
            Utils.show_request_log = self.show_request_log
            result = Utils.get_api_response(url, params)
            if 'transfer_code' in result:
                return result['transfer_code']
            else:
                return result
        except BaseError as e:
            self.code = e.code
            self.message = e.message

        if self.code is not None:
            return None
        else:
            return True

    def cancel_profile_transfer_code(self, profile_id):
        """

        :param profile_id:
        :return:
        """
        url = self.base_url + Consts.ACTION_FOR_PROFILE_CANCEL_TRANSFER_CODE
        params = dict()
        params['profile_id'] = profile_id
        try:
            self.code = None
            Utils.show_request_log = self.show_request_log
            result = Utils.get_api_response(url, params)
            return result
        except BaseError as e:
            self.code = e.code
            self.message = e.message

        if self.code is not None:
            return None
        else:
            return True

    def import_profile_via_transfer_code(self, transfer_code, proxy_config: Proxy = None):
        """

        :param transfer_code:
        :param proxy_config:
        :return:
        """
        url = self.base_url + Consts.ACTION_FOR_PROFILE_IMPORT_VIA_TRANSFER_CODE
        params = dict()
        params['transfer_code'] = transfer_code
        if proxy_config is not None:
            params['proxy_config'] = proxy_config.dump_to_dict()
        try:
            self.code = None
            Utils.show_request_log = self.show_request_log
            result = Utils.get_api_response(url, params)
            return result
        except BaseError as e:
            self.code = e.code
            self.message = e.message

        if self.code is not None:
            return None
        else:
            return True

    def get_profile_transfer_record_list(self, keyword=None, record_type=Consts.TRANSFER_RECORD_LIST_TYPE_TRANSFER, page=1, limit=10):
        """
        get profile transfer record list
        :param keyword:
        :param record_type:
        :param page:
        :param limit:
        :return:
        """
        url = self.base_url + Consts.ACTION_FOR_PROFILE_TRANSFER_RECORD_LIST
        params = dict()
        params['page'] = page
        params['limit'] = limit
        if record_type > 0:
            params['type'] = record_type

        if keyword is not None and keyword != '':
            params['title'] = keyword

        try:
            self.code = None
            Utils.show_request_log = self.show_request_log
            result = Utils.get_api_response(url, params)
            self.total = result['total']
            return result['data']
        except BaseError as e:
            self.code = e.code
            self.message = e.message

        if self.code is not None:
            return None
        else:
            return True


    def update_profile_groups_in_batches(self, profile_id, group_id):
        """
        update profile groups in batches
        :param profile_id: integer or list
        :param group_id: integer
        :return:
        """
        url = self.base_url + Consts.ACTION_FOR_PROFILE_UPDATE_GROUPS_IN_BATCHES
        params = dict()
        params['group_id'] = group_id
        if isinstance(profile_id, list):
            params['profile_id'] = profile_id
        else:
            params['profile_id'] = [profile_id]
        try:
            self.code = None
            Utils.show_request_log = self.show_request_log
            result = Utils.get_api_response(url, params)
            return result
        except BaseError as e:
            self.code = e.code
            self.message = e.message

        if self.code is not None:
            return None
        else:
            return True

    def delete_profile(self, profile_id):
        """
        delete profile
        :param profile_id:
        :return:
        """
        url = self.base_url + Consts.ACTION_FOR_PROFILE_DELETE
        params = dict()
        params['profile_id'] = profile_id
        try:
            self.code = None
            Utils.show_request_log = self.show_request_log
            result = Utils.get_api_response(url, params)
            return result
        except BaseError as e:
            self.code = e.code
            self.message = e.message

        if self.code is not None:
            return None
        else:
            return True

    def get_profile_cookie(self, profile_id):
        """
        get profile cookie
        :param profile_id:
        :return:
        """
        url = self.base_url + Consts.ACTION_FOR_PROFILE_GET_COOKIES
        params = dict()
        params['profile_id'] = profile_id
        try:
            self.code = None
            Utils.show_request_log = self.show_request_log
            result = Utils.get_api_response(url, params)
            return result
        except BaseError as e:
            self.code = e.code
            self.message = e.message

        if self.code is not None:
            return None
        else:
            return True

    def update_profile_cookie(self, profile_id, cookie):
        """
        update profile cookie
        :param profile_id:
        :param cookie: string or list
        :return:
        """
        url = self.base_url + Consts.ACTION_FOR_PROFILE_UPDATE_COOKIES
        params = dict()
        params['profile_id'] = profile_id
        if cookie is None:
            params['cookie'] = ''
        else:
            if isinstance(cookie, str):
                params['cookie'] = cookie
            else:
                params['cookie'] = json.dumps(cookie)
        try:
            self.code = None
            Utils.show_request_log = self.show_request_log
            result = Utils.get_api_response(url, params)
            return result
        except BaseError as e:
            self.code = e.code
            self.message = e.message

        if self.code is not None:
            return None
        else:
            return True

    def clear_profile_cache(self, profile_id):
        """
        clear profile cache
        :param profile_id:
        :return:
        """
        url = self.base_url + Consts.ACTION_FOR_PROFILE_CLEAR_CACHE
        params = dict()
        if isinstance(profile_id, list):
            params['profile_id'] = profile_id
        else:
            params['profile_id'] = [profile_id]
        try:
            self.code = None
            Utils.show_request_log = self.show_request_log
            result = Utils.get_api_response(url, params)
            return result
        except BaseError as e:
            self.code = e.code
            self.message = e.message

        if self.code is not None:
            return None
        else:
            return True

    def get_group_list(self, page=1, limit=100):
        """
        get group list
        :param page:
        :param limit:
        :return:
        """
        url = self.base_url + Consts.ACTION_FOR_GROUP_LIST
        params = dict()
        params['page'] = page
        params['limit'] = limit

        try:
            self.code = None
            Utils.show_request_log = self.show_request_log
            result = Utils.get_api_response(url, params)
            self.total = result['total']
            return result['data']
        except BaseError as e:
            self.code = e.code
            self.message = e.message

        if self.code is not None:
            return None
        else:
            return True

    def create_group(self, name, sort=0):
        """
        create group
        :param name:
        :param sort:
        :return:
        """
        url = self.base_url + Consts.ACTION_FOR_GROUP_CREATE
        params = dict()
        params['title'] = name
        if sort is None:
            params['sort'] = 0
        else:
            params['sort'] = sort
        try:
            self.code = None
            Utils.show_request_log = self.show_request_log
            result = Utils.get_api_response(url, params)
            return result
        except BaseError as e:
            self.code = e.code
            self.message = e.message

        if self.code is not None:
            return None
        else:
            return True

    def update_group(self, group_id, name, sort=None):
        """
        update group
        :param group_id:
        :param name:
        :param sort:
        :return:
        """
        url = self.base_url + Consts.ACTION_FOR_GROUP_UPDATE
        params = dict()
        params['id'] = group_id
        params['title'] = name
        if sort is not None:
            params['sort'] = sort
        try:
            self.code = None
            Utils.show_request_log = self.show_request_log
            result = Utils.get_api_response(url, params)
            return result
        except BaseError as e:
            self.code = e.code
            self.message = e.message

        if self.code is not None:
            return None
        else:
            return True

    def delete_group(self, group_id):
        """
        delete group
        :param group_id:
        :return:
        """
        url = self.base_url + Consts.ACTION_FOR_GROUP_DELETE
        params = dict()
        params['id'] = group_id
        try:
            self.code = None
            Utils.show_request_log = self.show_request_log
            result = Utils.get_api_response(url, params)
            return result
        except BaseError as e:
            self.code = e.code
            self.message = e.message

        if self.code is not None:
            return None
        else:
            return True

    def get_traffic_package_list(self):
        """
        get traffic package list
        :return:
        """
        url = self.base_url + Consts.ACTION_FOR_TRAFFIC_PACKAGE_LIST
        params = dict()
        params['page'] = 1
        params['limit'] = 100
        try:
            self.code = None
            Utils.show_request_log = self.show_request_log
            result = Utils.get_api_response(url, params)
            self.total = result['total']
            return result['data']
        except BaseError as e:
            self.code = e.code
            self.message = e.message

        if self.code is not None:
            return None
        else:
            return True

    def get_proxy_list(self, mode=0, tag_id=None, page=1, limit=10):
        """
        get proxy list
        :param mode:  0=All / 1=Custom Proxy / 2=Purchased Proxy
        :param tag_id:
        :param page:
        :param limit:
        :return:
        """
        url = self.base_url + Consts.ACTION_FOR_PROXY_LIST
        params = dict()
        params['page'] = page
        params['limit'] = limit
        if mode > 0:
            params['type'] = mode

        if tag_id is not None:
            params['tag_id'] = tag_id

        try:
            self.code = None
            Utils.show_request_log = self.show_request_log
            result = Utils.get_api_response(url, params)
            self.total = result['total']
            return result['data']
        except BaseError as e:
            self.code = e.code
            self.message = e.message

        if self.code is not None:
            return None
        else:
            return True

    def create_proxy(self, proxy_type, proxy_ip, proxy_port, proxy_user=None, proxy_password=None, note=None):
        """
        create proxy
        :param proxy_type:
        :param proxy_ip:
        :param proxy_port:
        :param proxy_user:
        :param proxy_password:
        :param note:
        :return:
        """
        url = self.base_url + Consts.ACTION_FOR_PROXY_CREATE
        params = dict()
        params['proxy_type'] = proxy_type
        params['proxy_ip'] = proxy_ip
        params['proxy_port'] = proxy_port
        if proxy_user is not None:
            params['proxy_user'] = proxy_user
        if proxy_password is not None:
            params['proxy_password'] = proxy_password
        if note is not None:
            params['note'] = note
        try:
            self.code = None
            Utils.show_request_log = self.show_request_log
            result = Utils.get_api_response(url, params)
            return result
        except BaseError as e:
            self.code = e.code
            self.message = e.message

        if self.code is not None:
            return None
        else:
            return True

    def update_proxy(self, proxy_id, name, sort=None):
        """
        update proxy
        :param proxy_id:
        :param name:
        :param sort:
        :return:
        """
        url = self.base_url + Consts.ACTION_FOR_GROUP_UPDATE
        params = dict()
        params['id'] = proxy_id
        params['title'] = name
        if sort is not None:
            params['sort'] = sort
        try:
            self.code = None
            Utils.show_request_log = self.show_request_log
            result = Utils.get_api_response(url, params)
            return result
        except BaseError as e:
            self.code = e.code
            self.message = e.message

        if self.code is not None:
            return None
        else:
            return True

    def delete_proxy(self, proxy_id):
        """
        delete proxy
        :param proxy_id:
        :return:
        """
        url = self.base_url + Consts.ACTION_FOR_PROXY_DELETE
        params = dict()
        params['id'] = proxy_id
        try:
            self.code = None
            Utils.show_request_log = self.show_request_log
            result = Utils.get_api_response(url, params)
            return result
        except BaseError as e:
            self.code = e.code
            self.message = e.message

        if self.code is not None:
            return None
        else:
            return True
