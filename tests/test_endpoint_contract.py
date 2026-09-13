"""Offline guard for the Local API action names used by the SDK.

A wrong action name cannot be caught by any behavioural test, because the SDK
only builds a URL from it. This module pins every action constant to the value
published in the Local API documentation, so an accidental rename or a typo
fails fast without touching the network.
"""
import re

from ixbrowser_local_api import Consts

from .action_endpoints import ACTION_ENDPOINTS


def action_constants():
    """Every ACTION_FOR_* constant and its value."""
    return {name: value for name, value in vars(Consts).items()
            if name.startswith('ACTION_FOR_') and isinstance(value, str)}


def test_every_action_constant_is_pinned():
    constants = action_constants()
    assert sorted(constants) == sorted(ACTION_ENDPOINTS), (
        'consts.py and the pinned endpoint table are out of sync; add or remove '
        'the entry in tests/action_endpoints.py together with the constant')


def test_action_values_match_the_published_endpoints():
    constants = action_constants()
    mismatched = {name: (constants[name], expected)
                  for name, expected in ACTION_ENDPOINTS.items()
                  if constants[name] != expected}
    assert mismatched == {}, 'action value does not match the Local API documentation: {}'.format(mismatched)


def test_action_values_are_plausible_endpoint_names():
    for name, value in action_constants().items():
        assert value == value.strip(), '{} has surrounding whitespace'.format(name)
        assert ' ' not in value, '{} contains a space'.format(name)
        assert re.match(r'^[a-z0-9]+(-[a-z0-9]+)*$', value), \
            '{} = {!r} is not a lowercase dashed endpoint name'.format(name, value)
        assert not value.startswith('/'), '{} must not start with a slash'.format(name)


def test_action_constants_are_unique():
    values = list(action_constants().values())
    duplicates = sorted({v for v in values if values.count(v) > 1})
    assert duplicates == [], 'two constants share the same endpoint: {}'.format(duplicates)


def test_constants_class_exposes_no_callable_state():
    # Consts is used as a namespace; keep it from accidentally growing methods.
    for name in ACTION_ENDPOINTS:
        assert isinstance(getattr(Consts, name), str)
