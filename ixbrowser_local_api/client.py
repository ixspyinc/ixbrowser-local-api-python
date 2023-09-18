import json
from .errors import UnexpectedError, HttpError, ResponseError, BaseError
from .utils import Utils
from .entities import *

DEFAULT_API_TARGET = '127.0.0.1'
DEFAULT_API_PORT = 53200


class IXBrowserClient(object):
    def __init__(self, target=DEFAULT_API_TARGET, port=DEFAULT_API_PORT):
        """

        :param target:
        :param port:
        """
        self.base_url = "http://{}:{}/api/v2/".format(target, port)

        self.total = None
        self.code = None
        self.message = None

    def get_profile_list(self, search=None, group=0, page=1, limit=10):
        """

        :param search:
        :param group:
        :param page:
        :param limit:
        :return:
        """
        url = self.base_url + ACTION_FOR_PROFILE_LIST
        params = dict()
        params['page'] = page
        params['limit'] = limit
        if group > 0:
            params['group'] = group

        if search is not None and search != '':
            params['name'] = search

        try:
            self.code = None
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

    def create_profile(self, obj: Profile=None):
        """

        :param obj:
        :return:
        """
        url = self.base_url + ACTION_FOR_PROFILE_CREATE

        params = obj.dump_to_dict()
        try:
            self.code = None
            result = Utils.get_api_response(url, params)
            return result
        except BaseError as e:
            self.code = e.code
            self.message = e.message

        if self.code is not None:
            return None
        else:
            return True

    def update_profile(self, obj: Profile=None):
        url = self.base_url + ACTION_FOR_PROFILE_UPDATE
        params = obj.dump_to_dict()
        try:
            self.code = None
            result = Utils.get_api_response(url, params)
            return result
        except BaseError as e:
            self.code = e.code
            self.message = e.message

        if self.code is not None:
            return None
        else:
            return True

    def update_profile_to_traffic_package_mode(self, profile_id, proxy_id, country=None, city=None, node_checked=None):
        """

        :param profile_id:
        :param proxy_id:
        :param country:
        :param city:
        :param node_checked:
        :return:
        """
        url = self.base_url + ACTION_FOR_PROFILE_UPDATE_PROXY_TO_TRAFFIC_PACKAGE_MODE
        params = dict()
        params['profile_id'] = profile_id
        params['proxy_info'] = dict()
        params['proxy_info']['proxy_mode'] = PROXY_MODE_TRAFFIC_PACKAGE
        params['proxy_info']['proxy_id'] = proxy_id
        if country is not None:
            params['proxy_info']['country'] = country
        if city is not None:
            params['proxy_info']['city'] = city

        if node_checked is None:
            params['proxy_info']['node_checked'] = DEFAULT_NODE_CHECKED
        else:
            params['proxy_info']['node_checked'] = node_checked

        try:
            self.code = None
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

        :param profile_id:
        :param proxy_id:
        :return:
        """
        url = self.base_url + ACTION_FOR_PROFILE_UPDATE_PROXY_TO_PURCHASED_MODE
        params = dict()
        params['profile_id'] = profile_id
        params['proxy_info'] = dict()
        params['proxy_info']['proxy_mode'] = PROXY_MODE_PURCHASED
        params['proxy_info']['proxy_id'] = proxy_id
        try:
            self.code = None
            result = Utils.get_api_response(url, params)
            return result
        except BaseError as e:
            self.code = e.code
            self.message = e.message

        if self.code is not None:
            return None
        else:
            return True

    def update_profile_to_custom_proxy_mode(self, profile_id, proxy_type, proxy_ip=None, proxy_port=None,
                                            proxy_user=None, proxy_password=None):
        """

        :param profile_id:
        :param proxy_type:
        :param proxy_ip:
        :param proxy_port:
        :param proxy_user:
        :param proxy_password:
        :return:
        """
        url = self.base_url + ACTION_FOR_PROFILE_UPDATE_PROXY_TO_CUSTOM_MODE
        params = dict()
        params['profile_id'] = profile_id
        params['proxy_info'] = dict()
        params['proxy_info']['proxy_mode'] = PROXY_MODE_CUSTOM
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

        :param profile_id:
        :return:
        """
        url = self.base_url + ACTION_FOR_PROFILE_RANDOM_FINGERPRINT
        params = dict()
        params['profile_id'] = profile_id
        try:
            self.code = None
            result = Utils.get_api_response(url, params)
            return result
        except BaseError as e:
            self.code = e.code
            self.message = e.message

        if self.code is not None:
            return None
        else:
            return True

    def update_profile_groups_in_batches(self, profile_id, group_id):
        """

        :param profile_id:
        :param group_id:
        :return:
        """
        url = self.base_url + ACTION_FOR_PROFILE_UPDATE_GROUPS_IN_BATCHES
        params = dict()
        params['group_id'] = group_id
        if isinstance(profile_id, list):
            params['profile_id'] = profile_id
        else:
            params['profile_id'] = [profile_id]
        try:
            self.code = None
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

        :param profile_id:
        :return:
        """
        url = self.base_url + ACTION_FOR_PROFILE_DELETE
        params = dict()
        params['profile_id'] = profile_id
        try:
            self.code = None
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

        :param profile_id:
        :return:
        """
        url = self.base_url + ACTION_FOR_PROFILE_GET_COOKIES
        params = dict()
        params['profile_id'] = profile_id
        try:
            self.code = None
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

        :param profile_id:
        :param cookie:
        :return:
        """
        url = self.base_url + ACTION_FOR_PROFILE_UPDATE_COOKIES
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
            result = Utils.get_api_response(url, params)
            return result
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

        :param profile_id:
        :param load_extensions:
        :param load_profile_info_page:
        :param cookies_backup:
        :param cookie:
        :param disable_extension_welcome_page:
        :param startup_args:
        :return:
        """
        url = self.base_url + ACTION_FOR_PROFILE_OPEN
        params = dict()
        params['profile_id'] = profile_id
        params['load_extensions'] = load_extensions
        params['load_check_page'] = load_profile_info_page
        params['is_cookies_cache'] = cookies_backup
        params['cookie'] = cookie
        if startup_args is None:
            startup_args = []
        if disable_extension_welcome_page:
            startup_args.append('--disable-extension-welcome-page')

        try:
            self.code = None
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

        :param profile_id:
        :return:
        """
        url = self.base_url + ACTION_FOR_PROFILE_CLOSE
        params = dict()

        params['profile_id'] = profile_id

        try:
            self.code = None
            result = Utils.get_api_response(url, params)
            return result
        except BaseError as e:
            self.code = e.code
            self.message = e.message

        if self.code is not None:
            return None
        else:
            return True

    def close_profile_in_batches(self, profile_id: list):
        """

        :param profile_id:
        :return:
        """
        url = self.base_url + ACTION_FOR_PROFILE_CLOSE_IN_BATCHES
        params = dict()

        params['profile_id'] = profile_id

        try:
            self.code = None
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

        :param profile_id:
        :return:
        """
        url = self.base_url + ACTION_FOR_PROFILE_CLEAR_CACHE
        params = dict()
        if isinstance(profile_id, list):
            params['profile_id'] = profile_id
        else:
            params['profile_id'] = [profile_id]
        try:
            self.code = None
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

        :param page:
        :param limit:
        :return:
        """
        url = self.base_url + ACTION_FOR_GROUP_LIST
        params = dict()
        params['page'] = page
        params['limit'] = limit

        try:
            self.code = None
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

        :param name:
        :param sort:
        :return:
        """
        url = self.base_url + ACTION_FOR_GROUP_CREATE
        params = dict()
        params['title'] = name
        if sort is None:
            params['sort'] = 0
        else:
            params['sort'] = sort
        try:
            self.code = None
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

        :param group_id:
        :param name:
        :param sort:
        :return:
        """
        url = self.base_url + ACTION_FOR_GROUP_UPDATE
        params = dict()
        params['id'] = group_id
        params['title'] = name
        if sort is not None:
            params['sort'] = sort
        try:
            self.code = None
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

        :param group_id:
        :return:
        """
        url = self.base_url + ACTION_FOR_GROUP_DELETE
        params = dict()
        params['id'] = group_id
        try:
            self.code = None
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

        :return:
        """
        url = self.base_url + ACTION_FOR_TRAFFIC_PACKAGE_LIST
        params = dict()
        params['page'] = 1
        params['limit'] = 100
        try:
            self.code = None
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

        :param mode:  0=All / 1=Custom Proxy / 2=Purchased Proxy
        :param tag_id:
        :param page:
        :param limit:
        :return:
        """
        url = self.base_url + ACTION_FOR_PROXY_LIST
        params = dict()
        params['page'] = page
        params['limit'] = limit
        if mode > 0:
            params['type'] = mode

        if tag_id is not None:
            params['tag_id'] = tag_id

        try:
            self.code = None
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

        :param proxy_type:
        :param proxy_ip:
        :param proxy_port:
        :param proxy_user:
        :param proxy_password:
        :param note:
        :return:
        """
        url = self.base_url + ACTION_FOR_PROXY_CREATE
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

        :param group_id:
        :param name:
        :param sort:
        :return:
        """
        url = self.base_url + ACTION_FOR_GROUP_UPDATE
        params = dict()
        params['id'] = group_id
        params['title'] = name
        if sort is not None:
            params['sort'] = sort
        try:
            self.code = None
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

        :param proxy_id:
        :return:
        """
        url = self.base_url + ACTION_FOR_PROXY_DELETE
        params = dict()
        params['id'] = proxy_id
        try:
            self.code = None
            result = Utils.get_api_response(url, params)
            return result
        except BaseError as e:
            self.code = e.code
            self.message = e.message

        if self.code is not None:
            return None
        else:
            return True

