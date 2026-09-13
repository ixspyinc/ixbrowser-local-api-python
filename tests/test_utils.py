"""Tests for the HTTP layer: envelope validation, error mapping and state reset."""
import pytest

from ixbrowser_local_api import Consts, IXBrowserClient, Utils
from ixbrowser_local_api.errors import (
    UNEXPECTED_ERROR_CODE,
    HttpError,
    ResponseError,
    UnexpectedError,
)


def call(client, url='http://127.0.0.1:53200/api/v2/test'):
    """Send one request and expose both the raw return value and the exception."""
    try:
        return Utils.get_api_response(url, {'a': 1}), None
    except Exception as e:      # noqa: BLE001 - the test wants the raw exception
        return None, e


class TestGetApiResponse(object):

    def test_success_with_object_data(self, transport):
        transport.reply(payload={'error': {'code': 0}, 'data': {'total': 2, 'data': [1, 2]}})
        value = Utils.get_api_response('http://x/api/v2/a', {})
        assert value == {'total': 2, 'data': [1, 2]}

    def test_success_with_list_data(self, transport):
        transport.reply(payload={'error': {'code': 0}, 'data': [1, 2, 3]})
        assert Utils.get_api_response('http://x/api/v2/a', {}) == [1, 2, 3]

    def test_success_with_string_data(self, transport):
        # several write interfaces answer with "data": "success"
        transport.reply(payload={'error': {'code': 0}, 'data': 'success'})
        assert Utils.get_api_response('http://x/api/v2/a', {}) == 'success'

    def test_success_with_null_data(self, transport):
        # profile-open-state-reset and profile-clear-saved-user-password answer
        # with "data": null
        transport.reply(payload={'error': {'code': 0, 'message': 'success'}, 'data': None})
        assert Utils.get_api_response('http://x/api/v2/a', {}) is None

    def test_success_without_data_key(self, transport):
        transport.reply(payload={'error': {'code': 0, 'message': 'success'}})
        assert Utils.get_api_response('http://x/api/v2/a', {}) is True

    def test_sends_json_body_and_timeout(self, transport):
        transport.reply(payload={'error': {'code': 0}, 'data': []})
        Utils.get_api_response('http://x/api/v2/a', {'k': 'v'})
        assert transport.last['payload'] == {'k': 'v'}
        assert transport.last['timeout'] == 20

    def test_api_error_is_raised_as_response_error(self, transport):
        transport.reply(payload={'error': {'code': 2007, 'message': 'Profile does not exist'}})
        _, exc = call(None)
        assert isinstance(exc, ResponseError)
        assert exc.code == 2007
        assert exc.message == 'Profile does not exist'

    def test_api_error_without_message_does_not_raise_key_error(self, transport):
        # The published docs contain error samples that carry only a code.
        transport.reply(payload={'error': {'code': 2007}})
        _, exc = call(None)
        assert isinstance(exc, ResponseError)
        assert exc.code == 2007
        assert exc.message is None

    def test_http_error(self, transport):
        transport.reply(payload={'error': {'code': 0}}, status_code=500)
        _, exc = call(None)
        assert isinstance(exc, HttpError)
        assert exc.code == 500

    def test_invalid_json(self, transport):
        transport.reply(invalid_json=True)
        _, exc = call(None)
        assert isinstance(exc, UnexpectedError)
        assert exc.code == UNEXPECTED_ERROR_CODE
        assert 'not valid JSON' in exc.message

    def test_json_array_instead_of_object(self, transport):
        transport.reply(payload=[1, 2, 3])
        _, exc = call(None)
        assert isinstance(exc, UnexpectedError)
        assert 'must be a JSON object' in exc.message

    def test_missing_error_key(self, transport):
        transport.reply(payload={'data': []})
        _, exc = call(None)
        assert isinstance(exc, UnexpectedError)
        assert "'error' key" in exc.message

    def test_error_is_not_an_object(self, transport):
        transport.reply(payload={'error': 'oops'})
        _, exc = call(None)
        assert isinstance(exc, UnexpectedError)

    def test_missing_error_code(self, transport):
        transport.reply(payload={'error': {'message': 'x'}})
        _, exc = call(None)
        assert isinstance(exc, UnexpectedError)
        assert "'error.code' key" in exc.message

    def test_error_code_is_not_an_integer(self, transport):
        transport.reply(payload={'error': {'code': '0'}})
        _, exc = call(None)
        assert isinstance(exc, UnexpectedError)
        assert 'must be an integer' in exc.message

    def test_connection_failure_is_wrapped(self, transport):
        transport.reply_with_exception(ConnectionError('connection refused'))
        _, exc = call(None)
        assert isinstance(exc, UnexpectedError)
        assert 'exception desc:connection refused' in exc.message

    def test_timeout_is_wrapped(self, transport):
        transport.reply_with_exception(TimeoutError('timed out'))
        _, exc = call(None)
        assert isinstance(exc, UnexpectedError)
        assert 'timed out' in exc.message


class TestGetPaginatedData(object):

    def test_returns_total_and_list(self, transport):
        total, data = Utils.get_paginated_data({'total': 214, 'data': [{'profile_id': 1}]})
        assert total == 214
        assert data == [{'profile_id': 1}]

    def test_accepts_an_empty_page(self, transport):
        total, data = Utils.get_paginated_data({'total': 0, 'data': []})
        assert (total, data) == (0, [])

    def test_rejects_non_object(self, transport):
        with pytest.raises(UnexpectedError) as info:
            Utils.get_paginated_data(True)
        assert "'data' must be a JSON object" in str(info.value)

    def test_rejects_missing_total(self, transport):
        with pytest.raises(UnexpectedError) as info:
            Utils.get_paginated_data({'data': []})
        assert "'total' key" in str(info.value)

    def test_rejects_missing_data(self, transport):
        with pytest.raises(UnexpectedError) as info:
            Utils.get_paginated_data({'total': 1})
        assert "'data' key" in str(info.value)

    @pytest.mark.parametrize('total', ['invalid', None, 1.5, [1], {'n': 1}, True])
    def test_rejects_a_total_that_is_not_an_integer(self, transport, total):
        # {"total": "invalid", "data": null} used to be reported as a success
        # returning None, which is indistinguishable from a failure.
        with pytest.raises(UnexpectedError) as info:
            Utils.get_paginated_data({'total': total, 'data': []})
        assert "'total' must be an integer" in str(info.value)

    @pytest.mark.parametrize('data', ['invalid', 5, {'a': 1}, True])
    def test_rejects_a_data_that_is_not_an_array(self, transport, data):
        with pytest.raises(UnexpectedError) as info:
            Utils.get_paginated_data({'total': 0, 'data': data})
        assert "'data' must be a JSON array" in str(info.value)

    def test_null_data_is_normalised_to_an_empty_list(self, transport):
        assert Utils.get_paginated_data({'total': 0, 'data': None}) == (0, [])

    def test_accepts_zero_total(self, transport):
        assert Utils.get_paginated_data({'total': 0, 'data': []}) == (0, [])


class TestRequestState(object):

    def test_paginated_method_populates_total(self, client, transport):
        transport.reply(payload={'error': {'code': 0}, 'data': {'total': 7, 'data': [1, 2]}})
        assert client.get_profile_list() == [1, 2]
        assert client.total == 7
        assert client.code is None

    def test_total_is_reset_before_each_request(self, client, transport):
        transport.reply(payload={'error': {'code': 0}, 'data': {'total': 7, 'data': []}})
        client.get_profile_list()
        assert client.total == 7

        transport.reply(payload={'error': {'code': 0}, 'data': 'success'})
        client.delete_profile(1)
        assert client.total is None

    def test_paginated_method_without_total_key_returns_none(self, client, transport):
        # A response that breaks the paginated contract must not raise TypeError.
        transport.reply(payload={'error': {'code': 0}, 'data': {'data': [{'profile_id': 1}]}})
        assert client.get_profile_list() is None
        assert client.code == UNEXPECTED_ERROR_CODE
        assert "'total' key" in client.message

    def test_paginated_method_without_inner_data_key_returns_none(self, client, transport):
        transport.reply(payload={'error': {'code': 0}, 'data': {'total': 1}})
        assert client.get_profile_list() is None
        assert client.code == UNEXPECTED_ERROR_CODE
        assert "'data' key" in client.message

    def test_paginated_method_with_a_non_object_data_returns_none(self, client, transport):
        transport.reply(payload={'error': {'code': 0}, 'data': [{'profile_id': 1}]})
        assert client.get_profile_list() is None
        assert client.code == UNEXPECTED_ERROR_CODE
        assert 'must be a JSON object' in client.message

    def test_paginated_method_with_an_invalid_total_reports_an_error(self, client, transport):
        # The reported regression: this returned None with code None and
        # total "invalid", i.e. a silent success.
        transport.reply(payload={'error': {'code': 0}, 'data': {'total': 'invalid', 'data': None}})
        assert client.get_profile_list() is None
        assert client.code == UNEXPECTED_ERROR_CODE
        assert "'total' must be an integer" in client.message
        assert client.total is None

    def test_paginated_method_with_a_null_list_returns_an_empty_page(self, client, transport):
        transport.reply(payload={'error': {'code': 0}, 'data': {'total': 0, 'data': None}})
        assert client.get_profile_list() == []
        assert client.total == 0
        assert client.code is None

    def test_paginated_method_without_data_key_returns_none(self, client, transport):
        transport.reply(payload={'error': {'code': 0}})
        assert client.get_profile_list() is None
        assert client.code == UNEXPECTED_ERROR_CODE

    def test_error_state_is_cleared_by_the_next_successful_call(self, client, transport):
        transport.reply(payload={'error': {'code': 2007, 'message': 'Profile does not exist'}})
        assert client.delete_profile(1) is None
        assert client.code == 2007
        assert client.message == 'Profile does not exist'

        transport.reply(payload={'error': {'code': 0}, 'data': 'success'})
        assert client.delete_profile(1) == 'success'
        assert client.code is None
        assert client.message is None

    def test_base_url_uses_default_target_and_port(self, client):
        assert client.base_url == 'http://{}:{}/api/v2/'.format(
            Consts.DEFAULT_API_TARGET, Consts.DEFAULT_API_PORT)

    def test_base_url_accepts_a_custom_target_and_port(self, transport):
        c = IXBrowserClient(target='127.0.0.1', port=12345)
        transport.reply(payload={'error': {'code': 0}, 'data': []})
        c.get_opened_profile_list()
        assert transport.last['url'] == 'http://127.0.0.1:12345/api/v2/profile-opened-list'
