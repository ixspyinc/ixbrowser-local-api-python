

UNEXPECTED_ERROR_CODE = 1


class BaseError(Exception):
    def __init__(self):
        self.code = 0
        self.message = None

    def __str__(self):
        if self.message is None:
            return "*** code={code} ***".format(code=self.code)
        else:
            return "*** code={code}, message={message} *** ".format(code=self.code, message=self.message)


class UnexpectedError(BaseError):
    def __init__(self, message):
        self.code = UNEXPECTED_ERROR_CODE
        self.message = message


class HttpError(BaseError):
    def __init__(self, status_code):
        self.code = status_code
        self.message = None


class ResponseError(BaseError):
    def __init__(self, error_dict):
        self.code = error_dict['code']
        self.message = error_dict['message']

