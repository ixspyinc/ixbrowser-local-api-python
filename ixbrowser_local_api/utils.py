import logging

import requests
from datetime import datetime
from .consts import Consts
from .errors import UnexpectedError, HttpError, ResponseError

logger = logging.getLogger('ixbrowser_local_api.http')


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
        logger.debug('request url=%s', url)
        logger.debug('request params=%s', params)
        try:
            r = requests.post(url, json=params, timeout=20)
        except Exception as e:
            raise UnexpectedError('exception desc:' + str(e)) from e

        if r.status_code != Consts.HTTP_CODE_FOR_SUCCESS:
            raise HttpError(r.status_code)
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug('response string=%s', r.text)
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
            # The published docs contain error samples that carry only a code,
            # so a missing message must not be treated as a malformed response.
            # ResponseError keeps the message at None in that case.
            raise ResponseError(error)
        return result['data'] if 'data' in result else True

    @staticmethod
    def get_paginated_data(result):
        """
        Unwrap the result of a paginated api response.

        Paginated interfaces return an object holding both the item list and the
        total item count, for example:
            {"error": {"code": 0}, "data": {"total": 214, "data": [...]}}

        The shape and the value types are validated here so that a malformed
        response raises a catchable UnexpectedError. Without the type checks a
        response such as {"total": "invalid", "data": null} would be reported as
        a success returning None, which is indistinguishable from the documented
        failure signal.
        :param result: value returned by get_api_response
        :return: (total, item list), a null item list is normalised to []
        """
        if not isinstance(result, dict):
            raise UnexpectedError(
                "The paginated response 'data' must be a JSON object, got: {}".format(type(result).__name__))
        if 'total' not in result:
            raise UnexpectedError("The paginated response 'data' does not contain the 'total' key")
        if 'data' not in result:
            raise UnexpectedError("The paginated response 'data' does not contain the 'data' key")

        total = result['total']
        if not isinstance(total, int) or isinstance(total, bool):
            raise UnexpectedError(
                "The paginated response 'total' must be an integer, got: {!r}".format(total))

        data = result['data']
        if data is None:
            # Tolerated: an empty page whose list was serialised as null.
            data = []
        if not isinstance(data, list):
            raise UnexpectedError(
                "The paginated response 'data' must be a JSON array, got: {}".format(type(data).__name__))

        return total, data
