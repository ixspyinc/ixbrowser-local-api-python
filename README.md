# ixBrowser Local API

Official Python client for ixBrowser Local API V2.0.

## Language

- [English](README.md)
- [Simplified Chinese](README.zh_CN.md)

## Prerequisites

- Python 3.5 or later.
- The ixBrowser desktop client is installed and running.
- The ixBrowser Local API service is enabled in the desktop client.
- By default, this SDK connects to `http://127.0.0.1:53200/api/v2/`.

If your local API service uses a different host or port, pass them to `IXBrowserClient`:

```python
from ixbrowser_local_api import IXBrowserClient

c = IXBrowserClient(target="127.0.0.1", port=53200)
```

## Installation

Install from PyPI:

```bash
pip install ixbrowser-local-api
```

Install from source:

```bash
git clone https://github.com/ixspyinc/ixbrowser-local-api-python.git
cd ixbrowser-local-api-python
python setup.py install
```

## Quick Start

```python
import random
from ixbrowser_local_api import IXBrowserClient

c = IXBrowserClient()

profiles = c.get_profile_list()
if profiles is None:
    print("Get profile list error:")
    print("Error code=", c.code)
    print("Error message=", c.message)
else:
    item = random.choice(profiles)
    profile_id = item["profile_id"]
    print("Random profile_id=", profile_id)

    open_result = c.open_profile(
        profile_id,
        cookies_backup=False,
        load_profile_info_page=False,
    )
    if open_result is None:
        print("Open profile error:")
        print("Error code=", c.code)
        print("Error message=", c.message)
    else:
        print(open_result)
        # open_result contains "webdriver" and "debugging_address".
        # They can be used to attach Selenium, Playwright, or another
        # browser automation tool to the opened profile.
```

## Error Handling

Most client methods return the API data on success. When a request fails, the method returns `None`, and the error details are stored on the client instance:

```python
result = c.get_profile_list()
if result is None:
    print(c.code)
    print(c.message)
```

See [docs/error-handling.md](docs/error-handling.md) for details.

## Documentation

- [API method index](docs/api-reference.md)
- [Entity guide](docs/entities.md)
- [Error handling](docs/error-handling.md)
- [Examples guide](examples/README.md)

## Examples

The `examples/` directory contains runnable scripts for common tasks:

- `examples/simple_test.py`: basic connectivity and common API calls.
- `examples/show_info.py`: print local information and list resources.
- `examples/profile_create.py`: create a profile with proxy, preferences, and fingerprint settings.
- `examples/profile_open.py`: open a profile and attach Selenium.
- `examples/profile_open_with_random_fingerprint.py`: open a profile with a randomized fingerprint.
- `examples/profile_update.py`: update profile settings.
- `examples/profile_copy.py`: create a profile by copying another profile.
- `examples/tag/`: profile tag CRUD examples.
- `examples/proxy_tag/`: proxy tag CRUD examples.
- `examples/profile_transfer_code/`: transfer code examples.

See [examples/README.md](examples/README.md) for the full examples map.

## Official API Documentation

- English: https://www.ixbrowser.com/doc/v2/local-api/en
- Chinese: https://www.ixbrowser.com/doc/v2/local-api/cn
