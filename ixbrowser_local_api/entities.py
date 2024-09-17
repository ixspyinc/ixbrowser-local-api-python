import random
from .consts import Consts
from .errors import UnexpectedError


class Profile(object):
    def __init__(self, profile_dict=None):
        self.profile_id = None
        self.new_profile_id = None
        self.site_id = None
        self.site_url = None
        self.color = None
        self.name = None
        self.note = None
        self.group_id = None
        self.tag = None
        self.username = None
        self.password = None
        self.cookie = None
        self.proxy_config = None
        self.fingerprint_config = None
        self.preference_config = None

        if profile_dict is not None and isinstance(profile_dict, dict):
            # Check whether the dictionary KEY matches the class attribute
            for k, v in profile_dict.items():
                if hasattr(self, k):
                    if isinstance(v, dict):
                        if k == 'proxy_config':
                            self.proxy_config = Proxy(v)
                        elif k == 'preference_config':
                            self.preference_config = Preference(v)
                        elif k == 'fingerprint_config':
                            self.fingerprint_config = Fingerprint(v)
                        else:
                            raise UnexpectedError(k + ' dictionary cannot find the relevant entity class')
                    else:
                        setattr(self, k, v)

    def reset_all_attributes(self):
        for k, v in self.__dict__.items():
            setattr(self, k, None)

    def random_color(self, source='list'):
        """
        Randomly generate colors
        It is recommended to choose randomly from the official list.
        Completely randomly generated color do not support profile icon rendering
        :param source: list/random
        :return:
        """
        if source == 'list':
            self.color = random.choice(Consts.DEFAULT_PROFILE_COLOR_LIST)
        else:
            r = random.randint(0, 255)
            b = random.randint(0, 255)
            g = random.randint(0, 255)
            self.color = "#{:02x}{:02x}{:02x}".format(r, b, g)

    def set_custom_page(self, url):
        self.site_id = Consts.DEFAULT_SITE_ID_CUSTOM_PAGE
        self.site_url = url

    def set_blank_page(self):
        self.site_id = Consts.DEFAULT_SITE_ID_BLANK_PAGE
        self.site_url = None
    
    def set_proxy_config(self, proxy_dict):
        self.proxy_config = Proxy(proxy_dict)

    def set_preference_config(self, preference_config):
        self.preference_config = Preference(preference_config)

    def set_fingerprint_config(self, fingerprint_config):
        self.fingerprint_config = Fingerprint(fingerprint_config)

    def dump_to_dict(self):
        """

        :return:
        """
        d = dict()
        for k, v in self.__dict__.items():
            if v is not None:
                if k == 'proxy_config' or k == 'preference_config' or k == 'fingerprint_config':
                    d[k] = v.dump_to_dict()
                else:
                    d[k] = v
        return d


class Proxy(object):
    def __init__(self, proxy_dict=None):
        self.proxy_mode = None
        self.proxy_id = None
        self.proxy_type = None
        self.proxy_ip = None
        self.proxy_port = None
        self.proxy_user = None
        self.proxy_password = None

        self.proxy_check_line = None

        self.country = None
        self.city = None
        self.gateway = None

        self.traffic_package_ip_policy = None
        self.ip_detection = None

        self.enable_bypass = None
        self.bypass_list = None

        self.proxy_service = None
        self.proxy_data_format_type = None
        self.proxy_data_txt_format = None
        self.proxy_data_json_format = None
        self.proxy_extraction_method = None
        self.proxy_url = None

        if proxy_dict is not None and isinstance(proxy_dict, dict):
            for k, v in proxy_dict.items():
                if hasattr(self, k):
                    setattr(self, k, v)

    def reset_all_attributes(self):
        for k, v in self.__dict__.items():
            setattr(self, k, None)

    def dump_to_dict(self):
        """

        :return:
        """
        d = dict()
        for k, v in self.__dict__.items():
            if v is not None:
                d[k] = v
        return d

    def set_bypass_list(self, domain_ls):
        """
        enable/disable bypass list
        :param domain_ls:
        :return:
        """
        if domain_ls is not None:
            if len(domain_ls) > 0:
                self.enable_bypass = True
                if isinstance(domain_ls, list):
                    self.bypass_list = '\n'.join(domain_ls)
                else:
                    self.bypass_list = domain_ls
            else:
                self.enable_bypass = False
                self.bypass_list = ''

        else:
            self.enable_bypass = False
            self.bypass_list = ''

    def change_to_traffic_package_mode(self, proxy_id, country=None, city=None,
                                       gateway=Consts.DEFAULT_TRAFFIC_PACKAGE_GATEWAY, ip_detection=None,
                                       ip_policy=None):
        """
        :param proxy_id:
        :param country:
        :param city:
        :param gateway:
        :param ip_detection: bool
        :param ip_policy: bool
        :return:
        """
        self.reset_all_attributes()
        self.proxy_mode = Consts.PROXY_MODE_TRAFFIC_PACKAGE
        self.proxy_id = proxy_id
        if country is not None:
            self.country = country
        if city is not None:
            self.city = city
        if gateway is not None:
            self.gateway = gateway
        if ip_detection is not None:
            if isinstance(ip_detection, bool):
                if ip_detection:
                    self.ip_detection = 1
                else:
                    self.ip_detection = 0
            else:
                self.ip_detection = ip_detection
        if ip_policy is not None:
            self.traffic_package_ip_policy = ip_policy

        return True

    def change_to_purchased_mode(self, proxy_id):
        """

        :param proxy_id:
        :return:
        """
        self.reset_all_attributes()
        self.proxy_mode = Consts.PROXY_MODE_PURCHASED
        self.proxy_id = proxy_id
        return True

    def change_to_custom_mode(self, proxy_type=Consts.PROXY_TYPE_DIRECT, proxy_ip=None, proxy_port=None, proxy_user=None, proxy_password=None, proxy_check_line=None):
        """

        :param proxy_type:
        :param proxy_ip:
        :param proxy_port:
        :param proxy_user:
        :param proxy_password:
        :param proxy_check_line:
        :return:
        """
        self.reset_all_attributes()
        self.proxy_mode = Consts.PROXY_MODE_CUSTOM
        self.proxy_type = proxy_type
        if proxy_ip is not None:
            self.proxy_ip = proxy_ip
        if proxy_port is not None:
            self.proxy_port = proxy_port
        if proxy_user is not None:
            self.proxy_user = proxy_user
        if proxy_password is not None:
            self.proxy_password = proxy_password
        if proxy_check_line is None:
            self.proxy_check_line = Consts.DEFAULT_PROXY_CHECK_LINE
        else:
            self.proxy_check_line = proxy_check_line
        return True

    def change_to_url_extraction_mode(self, proxy_url, 
                                      format_type=Consts.PROXY_DATA_FROMAT_TYPE_TXT,
                                      proxy_type=Consts.PROXY_TYPE_SOCKS5, 
                                      extract_method = Consts.PROXY_EXTRACT_FROM_URL_FRESH_TYPE_WHEN_INVALID,
                                      txt_mapping = None,
                                      json_mapping = None,
                                      proxy_check_line=Consts.DEFAULT_PROXY_CHECK_LINE):
        """

        :param proxy_url:
        :param format_type:
        :param proxy_type:
        :param extract_method:
        :param txt_mapping:
        :param json_mapping:
        :param proxy_check_line:
        :return:
        """
        self.reset_all_attributes()
        self.proxy_mode = Consts.PROXY_MODE_EXTRACT_FROM_URL

        self.proxy_url = proxy_url
        self.proxy_service = 'general'
        self.proxy_data_format_type = format_type
        
        if self.proxy_data_format_type == Consts.PROXY_DATA_FROMAT_TYPE_TXT:
            if txt_mapping is None:
                self.proxy_data_txt_format = Consts.PROXY_DATA_TXT_FORMAT_LIST[0]
            else:
                self.proxy_data_txt_format = txt_mapping
            self.proxy_data_json_format = None

        if self.proxy_data_format_type == Consts.PROXY_DATA_FROMAT_TYPE_JSON:
            if json_mapping is None:
                self.proxy_data_json_format = Consts.PROXY_DATA_JSON_FORMAT
            else:
                self.proxy_data_json_format = json_mapping
            self.proxy_data_txt_format = None

        self.proxy_type = proxy_type

        self.proxy_extraction_method = extract_method

        if proxy_check_line is None:
            self.proxy_check_line = Consts.DEFAULT_PROXY_CHECK_LINE
        else:
            self.proxy_check_line = proxy_check_line

        return True
    
    def get_url_extraction_mode_json_mapping(self, ip_key='ip', port_key='port', username_key=None, password_key=None):
        """

        :param ip_key:
        :param port_key:
        :param username:
        :param password:
        :return: dict
        """
        json_mapping = dict()
        for k in Consts.PROXY_DATA_JSON_FORMAT:
            if k == 'ip':
                json_mapping[k] = ip_key
            if k == 'port':
                json_mapping[k] = port_key
            if k == 'username':
                if username_key is not None:
                    json_mapping[k] = username_key

            if k == 'password':
                if password_key is not None:
                    json_mapping[k] = password_key
        
        return json_mapping


class Preference(object):
    def __init__(self, preference_dict=None):
        self.cookies_backup = None
        self.indexed_db_backup =None
        self.local_storage_backup = None
        self.extension_data_backup = None
        self.label_management = None
        self.open_url = None
        self.block_image = None
        self.block_audio = None
        self.load_profile_info_page = None

        if preference_dict is not None and isinstance(preference_dict, dict):
            for k, v in preference_dict.items():
                if hasattr(self, k):
                    setattr(self, k, v)

    def set_cloud_backup(self, save_cookies=1, save_indexed_db=0, save_local_storage=0, extension_data_backup=0):
        
        self.cookies_backup = save_cookies

        # If cookie cloud saving is turned off, index_db, etc. will also be forced not to be saved.
        if self.cookies_backup == 0:
            self.indexed_db_backup = 0
            self.local_storage_backup = 0
            self.extension_data_backup = 0
        else:
            self.indexed_db_backup =save_indexed_db
            self.local_storage_backup = save_local_storage
            self.extension_data_backup = extension_data_backup

    def reset_all_attributes(self):
        for k, v in self.__dict__.items():
            setattr(self, k, None)

    def dump_to_dict(self):
        """

        :return:
        """
        d = dict()
        for k, v in self.__dict__.items():
            if v is not None:
                d[k] = v
        return d


class Fingerprint(object):
    def __init__(self, fingerprint_dict=None):

        self.platform = None
        self.ua_type = None
        self.ua_info = None

        self.kernel_version = None
        self.device_name_source = None
        self.device_name = None

        self.hardware_concurrency = None
        self.device_memory = None
        self.br_version = None

        self.language_type = None
        self.language = None
        self.timezone_type = None
        self.timezone = None
        self.location_type = None
        self.location = None
        self.longitude = None
        self.latitude = None
        self.accuracy = None

        self.resolving_power_type = None
        self.resolving_power = None

        self.fonts_type = None
        self.fonts = None

        self.webrtc = None

        # 1: Random, 2: Customized, 3: Close
        self.webgl_data_type = None
        self.webgl_image = None
        self.webgl_factory = None
        self.webgl_info = None

        self.canvas_type = None
        self.audio_context = None
        self.media_equipment = None
        self.client_rects = None
        self.speech_voices = None
        self.product_type = None
        self.track = None
        self.allow_scan_ports = None
        self.allow_scan_ports_content = None

        if fingerprint_dict is not None and isinstance(fingerprint_dict, dict):
            for k, v in fingerprint_dict.items():
                if hasattr(self, k):
                    setattr(self, k, v)

    def reset_all_attributes(self):
        for k, v in self.__dict__.items():
            setattr(self, k, None)

    def set_device_name(self, name):
        self.device_name = name
        self.device_name_source = Consts.DEVICE_NAME_SOURCE_CUSTOM
    
    def dump_to_dict(self):
        """

        :return:
        """
        d = dict()
        for k, v in self.__dict__.items():
            if v is not None:
                d[k] = v
        return d
