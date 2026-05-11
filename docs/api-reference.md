# API Method Index

This page is a lightweight index of the public methods exposed by `IXBrowserClient`.
For request and response field details, compare the method name with the official
ixBrowser Local API V2.0 documentation.

## Client

Create a client with the default local API target:

```python
from ixbrowser_local_api import IXBrowserClient

c = IXBrowserClient()
```

The default base URL is `http://127.0.0.1:53200/api/v2/`.

Use a custom target or port when needed:

```python
c = IXBrowserClient(target="127.0.0.1", port=53200)
```

## Return Convention

Most methods return API data on success. If the request fails, the method returns
`None`, and the error details are available on `c.code` and `c.message`.

See [error-handling.md](error-handling.md).

## Profile Methods

| Method | Local API action | Purpose |
| --- | --- | --- |
| `get_profile_list(...)` | `profile-list` | List profiles or fetch one profile by `profile_id`. |
| `get_opened_profile_list()` | `profile-opened-list` | List profiles opened by the Local API. |
| `get_native_opened_profile_list()` | `native-client-profile-opened-list` | List profiles opened by the native client. |
| `open_profile(...)` | `profile-open` | Open a profile and return automation connection details. |
| `open_profile_with_random_fingerprint(...)` | `profile-open-with-random-fingerprint` | Open a profile while applying a randomized fingerprint. |
| `arrange_tile_opened_profile(...)` | `profile-opened-list-arrange-tile` | Arrange opened profile windows in a tiled layout. |
| `close_profile(profile_id)` | `profile-close` | Close one profile. |
| `close_profile_in_batches(profile_id)` | `profile-close-in-batches` | Close multiple profiles. |
| `create_profile(profile)` | `profile-create` | Create a profile from a `Profile` entity. |
| `create_profile_by_copying(...)` | `profile-copy` | Create a profile by copying an existing profile. |
| `update_profile(profile)` | `profile-update` | Update a profile from a `Profile` entity. |
| `delete_profile(profile_id)` | `profile-delete` | Delete a profile. |
| `empty_recycle_bin()` | `empty-recycle-bin` | Empty all profiles in the recycle bin. |
| `random_profile_fingerprint(profile_id)` | `profile-random-fingerprint-configuration` | Generate a random fingerprint configuration for a profile. |
| `update_profile_groups_in_batches(profile_id, group_id)` | `profile-update-groups-in-batches` | Move profiles to a group in batches. |
| `get_profile_cookie(profile_id)` | `profile-get-cookies` | Get cookies for a profile. |
| `update_profile_cookie(profile_id, cookie)` | `profile-update-cookies` | Update cookies for a profile. |
| `clear_profile_cache(profile_id)` | `profile-clear-cache` | Clear profile cache. |
| `clear_profile_cache_and_cookies(profile_id)` | `profile-clear-cache-and-cookies` | Clear profile cache and cookies. |
| `close_profile_via_selenium(obj)` | N/A | Deprecated Selenium helper. Prefer `close_profile`. |

## Profile Proxy Methods

| Method | Local API action | Purpose |
| --- | --- | --- |
| `update_profile_to_traffic_package_mode(...)` | `profile-update-proxy-for-purchased-traffic-package` | Switch a profile to traffic package proxy mode. |
| `update_profile_to_purchased_proxy_mode(profile_id, proxy_id)` | `profile-update-proxy-for-purchased-proxy` | Switch a profile to purchased proxy mode. |
| `update_profile_to_custom_proxy_mode(...)` | `profile-update-proxy-for-custom-proxy` | Switch a profile to custom proxy mode. |

## Transfer Code Methods

| Method | Local API action | Purpose |
| --- | --- | --- |
| `create_profile_transfer_code(...)` | `profile-transfer-code-create` | Create a transfer code for a profile. |
| `cancel_profile_transfer_code(profile_id)` | `profile-transfer-cancel` | Cancel a profile transfer code. |
| `import_profile_via_transfer_code(...)` | `profile-transfer-code-import` | Import a profile by transfer code. |
| `get_profile_transfer_record_list(...)` | `profile-transfer-record-list` | List transfer or import records. |

## Group Methods

| Method | Local API action | Purpose |
| --- | --- | --- |
| `get_group_list(page=1, limit=100)` | `group-list` | List profile groups. |
| `create_group(name, sort=0)` | `group-create` | Create a profile group. |
| `update_group(group_id, name, sort=None)` | `group-update` | Update a profile group. |
| `delete_group(group_id)` | `group-delete` | Delete a profile group. |

## Tag Methods

| Method | Local API action | Purpose |
| --- | --- | --- |
| `get_tag_list(page=1, limit=100)` | `tag-list` | List profile tags. |
| `create_tag(name)` | `tag-create` | Create a profile tag. |
| `update_tag(tag_id, name, sort=None)` | `tag-update` | Update a profile tag. |
| `delete_tag(tag_id)` | `tag-delete` | Delete a profile tag. |

## Proxy Methods

| Method | Local API action | Purpose |
| --- | --- | --- |
| `get_traffic_package_list()` | `traffic-package-list` | List traffic packages. |
| `get_proxy_list(...)` | `proxy-list` | List proxies. |
| `create_proxy(...)` | `proxy-create` | Create a proxy. |
| `update_proxy(...)` | `proxy-update` | Update a proxy. |
| `delete_proxy(proxy_id)` | `proxy-delete` | Delete a proxy. |

## Proxy Tag Methods

| Method | Local API action | Purpose |
| --- | --- | --- |
| `get_proxy_tag_list(...)` | `proxy-tag-list` | List proxy tags. |
| `create_proxy_tag(name)` | `proxy-tag-create` | Create a proxy tag. |
| `update_proxy_tag(id, name)` | `proxy-tag-update` | Update a proxy tag. |
| `delete_proxy_tag(id)` | `proxy-tag-delete` | Delete a proxy tag. |

## Gateway Methods

| Method | Local API action | Purpose |
| --- | --- | --- |
| `get_gateway_list()` | `gateway-list` | List available gateways. |
| `switch_gateway(gateway_id)` | `gateway-switch` | Switch the active gateway. |

## Related Files

- Client methods: `ixbrowser_local_api/client.py`
- Constants and action names: `ixbrowser_local_api/consts.py`
- Entity classes: `ixbrowser_local_api/entities.py`
- Examples: `examples/README.md`
