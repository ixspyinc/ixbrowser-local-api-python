"""Application-controlled logging without legacy global request switches."""
import logging
import subprocess
import sys

from ixbrowser_local_api import IXBrowserClient, Utils

LOGGER = 'ixbrowser_local_api.http'


def test_request_logs_are_silent_at_warning(transport, caplog, capsys):
    with caplog.at_level(logging.WARNING, logger=LOGGER):
        assert Utils.get_api_response('http://x/api/v2/test', {'a': 1}) is True
    assert not [record for record in caplog.records if record.name == LOGGER]
    assert capsys.readouterr() == ('', '')


def test_debug_logs_use_named_logger_without_printing(transport, caplog, capsys):
    params = {'password': 'test-secret', 'nested': {'a': 1}}
    payload = {'error': {'code': 0}, 'data': {'cookie': 'test-cookie'}}
    transport.reply(payload=payload)
    with caplog.at_level(logging.DEBUG, logger=LOGGER):
        result = Utils.get_api_response('http://x/api/v2/test', params)
    records = [record for record in caplog.records if record.name == LOGGER]
    assert len(records) == 3
    assert all(record.levelno == logging.DEBUG for record in records)
    assert 'http://x/api/v2/test' in records[0].getMessage()
    assert 'test-secret' in records[1].getMessage()  # Redaction is deliberately deferred.
    assert 'test-cookie' in records[2].getMessage()
    assert result == {'cookie': 'test-cookie'}
    assert params == {'password': 'test-secret', 'nested': {'a': 1}}
    assert transport.last['payload'] == params
    assert capsys.readouterr() == ('', '')


def test_disabled_debug_does_not_read_response_text(transport, caplog):
    class Response:
        status_code = 200

        @property
        def text(self):
            raise AssertionError('Response text should not be read for disabled logs')

        def json(self):
            return {'error': {'code': 0}, 'data': True}

    transport.response = Response()
    with caplog.at_level(logging.WARNING, logger=LOGGER):
        assert Utils.get_api_response('http://x/api/v2/test') is True


def test_clients_do_not_override_application_log_level(transport, caplog):
    first, second = IXBrowserClient(), IXBrowserClient()
    assert not hasattr(first, 'show_request_log')
    assert not hasattr(Utils, 'show_request_log')
    with caplog.at_level(logging.DEBUG, logger=LOGGER):
        first.get_opened_profile_list()
        second.get_opened_profile_list()
        assert logging.getLogger(LOGGER).level == logging.DEBUG
    assert len([record for record in caplog.records if record.name == LOGGER]) == 6


def test_import_does_not_configure_application_logging():
    script = '''
import logging
root = logging.getLogger()
level, handlers = root.level, list(root.handlers)
import ixbrowser_local_api
assert root.level == level
assert root.handlers == handlers
package = logging.getLogger('ixbrowser_local_api')
assert package.level == logging.NOTSET
assert package.propagate
assert any(isinstance(handler, logging.NullHandler) for handler in package.handlers)
'''
    result = subprocess.run([sys.executable, '-c', script], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert result.stdout == result.stderr == ''
