import logging

from .errors import UnexpectedError, HttpError, ResponseError, BaseError
from .utils import Utils
from .consts import Consts
from .client import IXBrowserClient
from .entities import Profile, Proxy, Preference, Fingerprint
from .version import __version__, VERSION

# Applications own log levels, formatting and output destinations.
logging.getLogger(__name__).addHandler(logging.NullHandler())

# Explicit public surface. It also marks the error classes below as intentional
# re-exports, so a linter does not report them as unused imports.
__all__ = [
    'IXBrowserClient',
    'Utils',
    'Consts',
    'Profile',
    'Proxy',
    'Preference',
    'Fingerprint',
    'BaseError',
    'UnexpectedError',
    'HttpError',
    'ResponseError',
    '__version__',
    'VERSION',
]
