"""Cross-check the SDK action constants against the published Local API docs.

This is the only check that can catch an endpoint the SDK sends but the service
no longer serves, and the only one that notices a newly published endpoint the
SDK has not implemented yet.

It reaches the public documentation site, so it is opt-in and skipped by a
default test run. That keeps a docs site change, or a new endpoint published
before the SDK implements it, from breaking ordinary CI and the release job.
CI runs it in its own best-effort job with:

    IXBROWSER_DOC_CONTRACT=1 python -m pytest tests/test_official_doc_contract.py -q
"""
import os
import re
import urllib.request

import pytest

from ixbrowser_local_api import Consts

DOC_URL = 'https://www.ixbrowser.com/doc/v2/local-api/en'
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36'

ONLINE = os.environ.get('IXBROWSER_DOC_CONTRACT') == '1'

pytestmark = [
    pytest.mark.online,
    pytest.mark.skipif(
        not ONLINE,
        reason='needs the online Local API documentation, set IXBROWSER_DOC_CONTRACT=1 to run'),
]

# Endpoints published in the documentation but not implemented by the SDK yet.
# Verified empty for the current documentation: every documented api/v2 endpoint
# has a matching ACTION_FOR_* constant and client method. Add an endpoint here
# when the documentation publishes one before the SDK implements it.
NOT_IMPLEMENTED_YET = set()


def fetch_documented_actions():
    """Return the set of api/v2/<action> names found in the documentation."""
    request = urllib.request.Request(DOC_URL, headers={'User-Agent': USER_AGENT})
    try:
        raw = urllib.request.urlopen(request, timeout=30).read().decode('utf-8', 'replace')
    except Exception as e:      # noqa: BLE001 - any network problem means skip
        pytest.skip('cannot reach {}: {}'.format(DOC_URL, e))

    # The page embeds its payload as escaped JSON inside a script tag.
    body = raw.replace('\\u0022', '"').replace('\\n', '\n').replace('\\t', '\t')
    actions = set(re.findall(r'api/v2/([a-z0-9\-]+)', body))
    if not actions:
        pytest.skip('no endpoints found in the documentation page')
    return actions


def sdk_actions():
    return {name: value for name, value in vars(Consts).items()
            if name.startswith('ACTION_FOR_') and isinstance(value, str)}


def test_every_sdk_action_is_documented():
    documented = fetch_documented_actions()
    unknown = {name: value for name, value in sdk_actions().items()
               if value not in documented}
    assert unknown == {}, (
        'these action names are not in the published documentation, the SDK would '
        'call a non-existent endpoint: {}'.format(unknown))


def test_newly_documented_endpoints_are_tracked():
    documented = fetch_documented_actions()
    implemented = set(sdk_actions().values())
    missing = {a for a in documented
               if a not in implemented and a not in NOT_IMPLEMENTED_YET}
    assert missing == set(), (
        'the documentation has endpoints the SDK does not implement yet, add them '
        'to the SDK or to NOT_IMPLEMENTED_YET: {}'.format(sorted(missing)))
