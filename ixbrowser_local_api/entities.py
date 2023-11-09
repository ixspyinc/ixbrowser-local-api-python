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
                    # if
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

        self.country = None
        self.city = None
        self.gateway = None

        self.traffic_package_ip_policy = None
        self.ip_detection = None

        self.enable_bypass = None
        self.bypass_list = None

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

    def change_to_custom_mode(self, proxy_type=Consts.PROXY_TYPE_DIRECT, proxy_ip=None, proxy_port=None,
                              proxy_user=None, proxy_password=None):
        """

        :param proxy_type:
        :param proxy_ip:
        :param proxy_port:
        :param proxy_user:
        :param proxy_password:
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
        return True


class Preference(object):
    def __init__(self, preference_dict=None):
        self.cookies_backup = None
        self.label_management = None
        self.open_url = None
        self.block_image = None
        self.block_audio = None

        if preference_dict is not None and isinstance(preference_dict, dict):
            for k, v in preference_dict.items():
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


class Fingerprint(object):
    def __init__(self, fingerprint_dict=None):

        self.platform = None
        self.ua_type = None
        self.ua_info = None

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

    def dump_to_dict(self):
        """

        :return:
        """
        d = dict()
        for k, v in self.__dict__.items():
            if v is not None:
                d[k] = v
        return d
