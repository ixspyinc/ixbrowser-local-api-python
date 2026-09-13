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
        if Utils.show_request_log:
            print('[debug info]request url=', url)
            print('[debug info]request params=', params)
        try:
            r = requests.post(url, json=params, timeout=20)
        except Exception as e:
            raise UnexpectedError('exception desc:' + str(e)) from e

        if r.status_code != Consts.HTTP_CODE_FOR_SUCCESS:
            raise HttpError(r.status_code)
        if Utils.show_request_log:
            print('[debug info]response string=', r.text)
        try:
            result = r.json()
        except ValueError as e:
            raise UnexpectedError('The returned data is not valid JSON') from e

        if not isinstance(result, dict):
            raise UnexpectedError('The returned data must be a JSON object')
        if 'error' not in result:
            raise UnexpectedError("The returned data does not contain the 'error' key")
        error = result['error']
        if not isinstance(error, dict):
            raise UnexpectedError("The returned 'error' must be a JSON object")
        if 'code' not in error:
            raise UnexpectedError("The returned data does not contain the 'error.code' key")
        if type(error['code']) is not int:
            raise UnexpectedError("The returned 'error.code' must be an integer")
        if error['code'] != Consts.RESULT_CODE_FOR_SUCCESS:
            if 'message' not in error:
                raise UnexpectedError("The returned data does not contain the 'error.message' key")
            raise ResponseError(error)
        return result['data'] if 'data' in result else True

