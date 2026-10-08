"""Regression tests for review findings B-1 .. B-5."""
import pytest

from ixbrowser_local_api import Consts, Proxy
from ixbrowser_local_api.errors import UNEXPECTED_ERROR_CODE


# B-1: shared mutable default must not leak between entities


def test_json_mapping_default_is_copied():
    original = dict(Consts.PROXY_DATA_JSON_FORMAT)
    proxy = Proxy()
    proxy.change_to_url_extraction_mode('http://x', format_type=Consts.PROXY_DATA_FORMAT_TYPE_JSON)
    proxy.proxy_data_json_format['username'] = 'user_field'
    assert Consts.PROXY_DATA_JSON_FORMAT == original
    assert Proxy().proxy_data_json_format is None


def test_json_mapping_argument_is_copied():
    mapping = {'ip': 'host', 'port': 'p'}
    proxy = Proxy()
    proxy.change_to_url_extraction_mode('http://x', format_type=Consts.PROXY_DATA_FORMAT_TYPE_JSON,
                                        json_mapping=mapping)
    proxy.proxy_data_json_format['ip'] = 'changed'
    assert mapping == {'ip': 'host', 'port': 'p'}


# B-2: list endpoints normalise a successful null to []


@pytest.mark.parametrize('method', [
    'get_opened_profile_list', 'get_native_opened_profile_list', 'get_gateway_list'])
def test_list_endpoint_null_data_is_empty_list(client, transport, method):
    transport.reply(payload={'error': {'code': 0}, 'data': None})
    assert getattr(client, method)() == []
    assert client.code is None


@pytest.mark.parametrize('method', [
    'get_opened_profile_list', 'get_native_opened_profile_list', 'get_gateway_list'])
def test_list_endpoint_missing_data_key_is_empty_list(client, transport, method):
    # Envelope without the 'data' key entirely
    transport.reply(payload={'error': {'code': 0, 'message': 'success'}})
    assert getattr(client, method)() == []
    assert client.code is None


@pytest.mark.parametrize('method', [
    'get_opened_profile_list', 'get_native_opened_profile_list', 'get_gateway_list'])
def test_list_endpoint_failure_is_still_none(client, transport, method):
    transport.reply(payload={'error': {'code': 1008, 'message': 'denied'}, 'data': None})
    assert getattr(client, method)() is None
    assert client.code == 1008


def test_action_endpoint_null_data_is_still_true(client, transport):
    transport.reply(payload={'error': {'code': 0}, 'data': None})
    assert client.close_profile(1) is True


# B-3: invalid input follows the None + client.code contract


@pytest.mark.parametrize('method', ['open_profile_with_random_fingerprint', 'import_profile_via_transfer_code'])
def test_dict_proxy_config_is_accepted(client, transport, method):
    transport.reply(payload={'error': {'code': 0}, 'data': {'ok': 1}})
    assert getattr(client, method)(1, proxy_config={'proxy_mode': 2}) == {'ok': 1}
    assert transport.last['payload']['proxy_config'] == {'proxy_mode': 2}


def test_dict_nested_configs_accepted(client, transport):
    transport.reply(payload={'error': {'code': 0}, 'data': {'ok': 1}})
    res = client.open_profile_with_random_fingerprint(
        1,
        proxy_config={'proxy_mode': 2},
        fingerprint_config={'ua_type': 1},
        preference_config={'block_image': 1},
    )
    assert res == {'ok': 1}
    assert transport.last['payload']['proxy_config'] == {'proxy_mode': 2}
    assert transport.last['payload']['fingerprint_config'] == {'ua_type': 1}
    assert transport.last['payload']['preference_config'] == {'block_image': 1}


def test_entity_proxy_config_still_serialised(client, transport):
    transport.reply(payload={'error': {'code': 0}, 'data': {'ok': 1}})
    proxy = Proxy()
    proxy.change_to_purchased_mode(9)
    client.open_profile_with_random_fingerprint(1, proxy_config=proxy)
    assert transport.last['payload']['proxy_config'] == {'proxy_mode': 3, 'proxy_id': 9}


@pytest.mark.parametrize('kwargs', [
    {'proxy_config': 'invalid'}, {'fingerprint_config': 1}, {'preference_config': []}])
def test_invalid_nested_config_is_reported(client, transport, kwargs):
    assert client.open_profile_with_random_fingerprint(1, **kwargs) is None
    assert client.code == UNEXPECTED_ERROR_CODE
    assert list(kwargs)[0] in client.message
    assert transport.call_count == 0


@pytest.mark.parametrize('method,kwargs,absent', [
    ('get_profile_list', {'group_id': None, 'tag_id': None}, ('group_id', 'tag_id')),
    ('get_proxy_list', {'mode': None}, ('type',)),
    ('get_profile_transfer_record_list', {'record_type': None}, ('type',)),
])
def test_none_filters_are_unset(client, transport, method, kwargs, absent):
    transport.reply(payload={'error': {'code': 0}, 'data': {'total': 0, 'data': []}})
    assert getattr(client, method)(**kwargs) == []
    for key in absent:
        assert key not in transport.last['payload']


def test_profile_list_none_profile_id_lists_profiles(client, transport):
    transport.reply(payload={'error': {'code': 0}, 'data': {'total': 0, 'data': []}})
    client.get_profile_list(profile_id=None)
    assert 'profile_id' not in transport.last['payload']
    assert transport.last['payload']['page'] == 1


@pytest.mark.parametrize('method,kwargs', [
    ('get_profile_list', {'group_id': '3'}),
    ('get_profile_list', {'tag_id': True}),
    ('get_proxy_list', {'mode': 'http'}),
    ('get_profile_transfer_record_list', {'record_type': 1.5}),
])
def test_invalid_filters_are_reported(client, transport, method, kwargs):
    assert getattr(client, method)(**kwargs) is None
    assert client.code == UNEXPECTED_ERROR_CODE
    assert transport.call_count == 0


def test_positive_filters_are_still_sent(client, transport):
    transport.reply(payload={'error': {'code': 0}, 'data': {'total': 0, 'data': []}})
    client.get_profile_list(group_id=2, tag_id=3)
    assert transport.last['payload']['group_id'] == 2
    assert transport.last['payload']['tag_id'] == 3


# B-4: list-like batch IDs


@pytest.mark.parametrize('ids,expected', [((1, 2), [1, 2]), ([3], [3]), (4, [4]), (frozenset([5]), [5])])
def test_batch_ids_accept_list_like(client, transport, ids, expected):
    transport.reply(payload={'error': {'code': 0}, 'data': 'success'})
    client.close_profile_in_batches(ids)
    assert transport.last['payload'] == {'profile_id': expected}


def test_batch_ids_accept_set(client, transport):
    transport.reply(payload={'error': {'code': 0}, 'data': 'success'})
    client.clear_profile_cache({1, 2})
    assert sorted(transport.last['payload']['profile_id']) == [1, 2]


# B-5: None must not silently clear cookies


def test_update_cookie_none_is_rejected(client, transport):
    assert client.update_profile_cookie(1, None) is None
    assert client.code == UNEXPECTED_ERROR_CODE
    assert 'cookie' in client.message
    assert transport.call_count == 0


def test_update_cookie_empty_string_clears(client, transport):
    transport.reply(payload={'error': {'code': 0}, 'data': 'success'})
    assert client.update_profile_cookie(1, '') == 'success'
    assert transport.last['payload'] == {'profile_id': 1, 'cookie': ''}


def test_update_cookie_serialises_structures(client, transport):
    transport.reply(payload={'error': {'code': 0}, 'data': 'success'})
    client.update_profile_cookie(1, [{'name': 'a', 'value': 'b'}])
    assert transport.last['payload']['cookie'] == '[{"name": "a", "value": "b"}]'


def test_update_cookie_unserialisable_is_reported(client, transport):
    assert client.update_profile_cookie(1, {object()}) is None
    assert client.code == UNEXPECTED_ERROR_CODE
    assert transport.call_count == 0
