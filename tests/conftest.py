"""Shared test fixtures.

The Local API runs inside the ixBrowser desktop client, so unit tests never talk
to a real endpoint. Every test patches ``requests.post`` with a fake transport
and asserts on the URL, payload and return value instead.
"""
import json

import pytest

from ixbrowser_local_api import IXBrowserClient, Utils


class FakeResponse(object):
    """Minimal stand-in for requests.Response."""

    def __init__(self, payload=None, status_code=200, text=None, invalid_json=False):
        self._payload = payload
        self.status_code = status_code
        self._invalid_json = invalid_json
        self.text = text if text is not None else json.dumps(payload)

    def json(self):
        if self._invalid_json:
            raise ValueError('Expecting value: line 1 column 1 (char 0)')
        return self._payload


class FakeTransport(object):
    """Records the requests the client tries to send."""

    def __init__(self):
        self.calls = []
        self.response = FakeResponse(success_payload())

    def __call__(self, url, json=None, timeout=None, headers=None, **kwargs):
        self.calls.append({'url': url, 'payload': json, 'timeout': timeout})
        if isinstance(self.response, Exception):
            raise self.response
        return self.response

    def reply(self, payload=None, status_code=200, invalid_json=False, text=None):
        self.response = FakeResponse(payload=payload, status_code=status_code,
                                     invalid_json=invalid_json, text=text)

    def reply_with_exception(self, exception):
        self.response = exception

    @property
    def last(self):
        assert self.calls, 'no request was sent'
        return self.calls[-1]

    @property
    def call_count(self):
        return len(self.calls)


def success_payload(data=True):
    """A Local API success envelope."""
    return {'error': {'code': 0, 'message': 'success', 'time': 1691131803}, 'data': data}


def error_payload(code, message=None):
    """A Local API failure envelope, with or without a message."""
    error = {'code': code, 'time': 1691131803}
    if message is not None:
        error['message'] = message
    return {'error': error, 'data': None}


def paginated_payload(items, total=None):
    """The envelope used by paginated interfaces: data holds total plus the list."""
    return success_payload({'total': len(items) if total is None else total, 'data': items})


@pytest.fixture
def transport(monkeypatch):
    """Replace requests.post with a fake transport for the duration of a test.

    Also pins Utils.show_request_log, which is process wide mutable state, so a
    client that enables request logging cannot leak it into another test.
    """
    fake = FakeTransport()
    monkeypatch.setattr('ixbrowser_local_api.utils.requests.post', fake)
    Utils.show_request_log = False
    yield fake
    Utils.show_request_log = False


@pytest.fixture
def client(transport):
    """A client wired to the fake transport."""
    return IXBrowserClient()
