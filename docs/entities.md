# Entity Guide

The SDK uses small entity classes to build request payloads for profile-related
operations. They are plain Python objects with attributes that map to Local API
fields. When a client method sends the request, the entity is converted to a
dictionary with `dump_to_dict()`.

The main entity classes are:

- `Profile`
- `Proxy`
- `Preference`
- `Fingerprint`

## Profile

`Profile` is the main object used by `create_profile()` and `update_profile()`.
It can hold basic profile fields and nested configuration objects.

Common fields include:

| Field | Purpose |
| --- | --- |
| `profile_id` | Existing profile ID. Usually required for updates. |
| `name` | Profile name. |
| `site_id` | Startup site type. |
| `site_url` | Startup URL for a custom page. |
| `color` | Profile color. |
| `note` | Profile note. |
| `group_id` | Profile group ID. |
| `tag` | Profile tags. |
| `username` | Saved account username. |
| `password` | Saved account password. |
| `tfa_secret` | 2FA secret. |
| `cookie` | Cookie data. |
| `proxy_config` | A `Proxy` object. |
| `preference_config` | A `Preference` object. |
| `fingerprint_config` | A `Fingerprint` object. |

Example:

```python
from ixbrowser_local_api import Profile

profile = Profile()
profile.name = "Demo profile"
profile.tag = ["demo", "api"]
profile.set_custom_page("https://www.ixbrowser.com")
profile.random_color()
```

You can also build a `Profile` from a dictionary:

```python
profile = Profile({
    "name": "Demo profile",
    "site_url": "https://www.ixbrowser.com",
    "proxy_config": {
        "proxy_mode": 2,
        "proxy_type": "socks5",
        "proxy_ip": "127.0.0.1",
        "proxy_port": "10808",
    },
})
```

## Proxy

`Proxy` describes how a profile should connect to the network. It supports
several modes:

| Mode helper | Purpose |
| --- | --- |
| `change_to_custom_mode(...)` | Use a custom direct, HTTP, HTTPS, SOCKS5, or SSH proxy. |
| `change_to_purchased_mode(proxy_id)` | Use a purchased proxy by ID. |
| `change_to_traffic_package_mode(...)` | Use a traffic package proxy. |
| `change_to_url_extraction_mode(...)` | Extract proxy data from a URL. |

Custom proxy example:

```python
from ixbrowser_local_api import Proxy, Consts

proxy = Proxy()
proxy.change_to_custom_mode(
    proxy_type=Consts.PROXY_TYPE_SOCKS5,
    proxy_ip="127.0.0.1",
    proxy_port="10808",
)
proxy.set_bypass_list(["*.ipinfo.io", "ixbrowser.com"])
```

Purchased proxy example:

```python
proxy = Proxy()
proxy.change_to_purchased_mode(proxy_id=1)
```

Traffic package example:

```python
proxy = Proxy()
proxy.change_to_traffic_package_mode(
    proxy_id=1,
    country="us",
    ip_detection=True,
    ip_policy=True,
)
```

## Preference

`Preference` controls browser behavior and backup behavior.

Common fields include:

| Field | Purpose |
| --- | --- |
| `cookies_backup` | Enable or disable cookie backup. |
| `indexed_db_backup` | Enable or disable IndexedDB backup. |
| `local_storage_backup` | Enable or disable local storage backup. |
| `extension_data_backup` | Enable or disable extension data backup. |
| `open_url` | URL to open after profile start. |
| `block_image` | Block images. |
| `block_audio` | Block audio. |
| `load_profile_info_page` | Load or skip the profile info page. |
| `block_password_pages` | Control password prompt pages. |
| `block_restore_pages` | Control restore prompt pages. |
| `block_notification_pages` | Control notification prompts. |
| `show_bookmarks_bar` | Show or hide the bookmarks bar. |

Example:

```python
from ixbrowser_local_api import Preference

preference = Preference()
preference.set_cloud_backup(
    save_cookies=1,
    save_indexed_db=1,
    save_local_storage=0,
    extension_data_backup=0,
)
preference.block_image = 1
preference.block_audio = 1
preference.open_url = "https://www.google.com"
preference.load_profile_info_page = 0
```

## Fingerprint

`Fingerprint` controls browser fingerprint options. You can set only the fields
that need to be customized. Unset fields are omitted from the request payload.

Common fields include:

| Field | Purpose |
| --- | --- |
| `ua_type` | User agent device type. |
| `ua_info` | User agent string. |
| `platform` | Platform such as Windows, Macos, Android, or IOS. |
| `system_version` | Operating system version. |
| `language_type` | Language strategy. |
| `language` | Custom language. |
| `timezone_type` | Timezone strategy. |
| `timezone` | Custom timezone. |
| `location_type` | Location strategy. |
| `longitude` | Custom longitude. |
| `latitude` | Custom latitude. |
| `resolving_power_type` | Screen resolution strategy. |
| `fonts_type` | Font strategy. |
| `webrtc` | WebRTC behavior. |
| `webgl_data_type` | WebGL strategy. |
| `webgpu_data_type` | WebGPU strategy. |
| `canvas_type` | Canvas behavior. |
| `audio_context` | AudioContext behavior. |
| `client_rects` | ClientRects behavior. |
| `track` | Tracking behavior. |
| `cloudflare_challenge_bypassing` | Cloudflare challenge bypass option. |

Example:

```python
from ixbrowser_local_api import Fingerprint

fingerprint = Fingerprint()
fingerprint.language_type = 2
fingerprint.language = "cn"
fingerprint.client_rects = 0
fingerprint.set_device_name("demo-device")
```

## Combining Entities

The typical pattern is to create a `Profile`, attach optional nested entities,
and then pass the profile to `create_profile()` or `update_profile()`.

```python
from ixbrowser_local_api import (
    IXBrowserClient,
    Profile,
    Proxy,
    Preference,
    Fingerprint,
    Consts,
)

c = IXBrowserClient()

profile = Profile()
profile.name = "Demo profile"
profile.set_custom_page("https://www.ixbrowser.com")
profile.random_color()

proxy = Proxy()
proxy.change_to_custom_mode(Consts.PROXY_TYPE_SOCKS5, "127.0.0.1", "10808")
profile.proxy_config = proxy

preference = Preference()
preference.set_cloud_backup(1, 1, 0)
preference.block_image = 1
profile.preference_config = preference

fingerprint = Fingerprint()
fingerprint.language_type = 2
fingerprint.language = "cn"
profile.fingerprint_config = fingerprint

result = c.create_profile(profile)
if result is None:
    print(c.code, c.message)
else:
    print(result)
```

## Dictionary Output

Each entity has `dump_to_dict()`. Fields with value `None` are omitted from the
output. Nested entities are also converted to dictionaries.

```python
payload = profile.dump_to_dict()
print(payload)
```

This behavior is useful when you only want to send fields that should be created
or updated.
