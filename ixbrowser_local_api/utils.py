import sys
import requests
from datetime import datetime
from .consts import Consts
from .errors import UnexpectedError, HttpError, ResponseError


HTTP_CODE_FOR_SUCCESS = 200
RESULT_CODE_FOR_SUCCESS = 0


class Utils(object):
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
        # print(url)
        # print(params)
        try:
            r = requests.post(url, json=params, timeout=20)
        except Exception as e:
            error_msg = 'exception desc:' + str(e)

        if error_msg is None:
            if r.status_code == HTTP_CODE_FOR_SUCCESS:
                # print(r.text)
                result = r.json()
                if 'error' in result:
                    if 'code' in result['error']:
                        if result['error']['code'] == RESULT_CODE_FOR_SUCCESS:
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

