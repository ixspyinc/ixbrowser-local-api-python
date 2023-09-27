import requests
from datetime import datetime
from .consts import Consts
from .errors import UnexpectedError, HttpError, ResponseError


class Utils(object):

    show_request_log = False

    @staticmethod
    def now():
        return int(datetime.now().timestamp() * 1000)

    @staticmethod
    def get_api_response(url, params=None):
        """
        get api response
        :param url:
        :param params:
        :return:
        """
        r = None
        error_msg = None
        if Utils.show_request_log:
            print('[debug info]request url=', url)
            print('[debug info]request params=', params)
        try:
            r = requests.post(url, json=params, timeout=20)
        except Exception as e:
            error_msg = 'exception desc:' + str(e)

        if error_msg is None:
            if r.status_code == Consts.HTTP_CODE_FOR_SUCCESS:
                if Utils.show_request_log:
                    print('[debug info]response string=', r.text)
                result = r.json()
                if 'error' in result:
                    if 'code' in result['error']:
                        if result['error']['code'] == Consts.RESULT_CODE_FOR_SUCCESS:
                            if 'data' in result:
                                return result['data']
                            else:
                                return True
                        else:
                            raise ResponseError(result['error'])
                    else:
                        raise UnexpectedError("The returned data does not contain the 'error.code' key")
                else:
                    raise UnexpectedError("The returned data does not contain the 'error' key")
            else:
                raise HttpError(r.status_code)
        else:
            raise UnexpectedError(error_msg)

