import random
from .consts import *
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

    def random_color(self):
        """

        :return: string
        """
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
        self.ip_policy = None
        self.ip_detection = None

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
