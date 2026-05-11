# Examples Guide

This directory contains runnable scripts for common ixBrowser Local API tasks.
Most scripts assume the ixBrowser desktop client is running and the Local API
service is enabled at `127.0.0.1:53200`.

## Setup

Install the SDK before running examples:

```bash
pip install ixbrowser-local-api
```

Some browser automation examples also need Selenium:

```bash
pip install selenium
```

Run an example from the repository root:

```bash
python examples/profile_open.py
```

## General Examples

| File | Purpose |
| --- | --- |
| `simple_test.py` | Basic connectivity and common API calls. Good first script to run. |
| `show_info.py` | Print local API information and list available resources. |

## Profile Examples

| File | Purpose |
| --- | --- |
| `profile_create.py` | Create a profile with custom proxy, preferences, and fingerprint settings. |
| `profile_update.py` | Update an existing profile. |
| `profile_copy.py` | Create a new profile by copying an existing profile. |
| `profile_open.py` | Open a profile and attach Selenium with the returned webdriver details. |
| `profile_open_with_random_fingerprint.py` | Open a profile with a randomized fingerprint and optional proxy override. |

## Profile Transfer Code Examples

| File | Purpose |
| --- | --- |
| `profile_transfer_code/profile_transfer_code_create.py` | Create a transfer code for a profile. |
| `profile_transfer_code/profile_transfer_code_cancel.py` | Cancel a profile transfer code. |
| `profile_transfer_code/profile_transfer_code_import.py` | Import a profile with a transfer code. |
| `profile_transfer_code/profile_transfer_record_list.py` | List transfer and import records. |

## Profile Tag Examples

| File | Purpose |
| --- | --- |
| `tag/tag_list.py` | List profile tags. |
| `tag/tag_create.py` | Create a profile tag. |
| `tag/tag_update.py` | Update a profile tag. |
| `tag/tag_delete.py` | Delete a profile tag. |

## Proxy Tag Examples

| File | Purpose |
| --- | --- |
| `proxy_tag/proxy_tag_list.py` | List proxy tags. |
| `proxy_tag/proxy_tag_create.py` | Create a proxy tag. |
| `proxy_tag/proxy_tag_update.py` | Update a proxy tag. |
| `proxy_tag/proxy_tag_delete.py` | Delete a proxy tag. |

## Common Error Pattern

Most examples use this pattern:

```python
result = c.some_method()
if result is None:
    print("Error code=", c.code)
    print("Error message=", c.message)
else:
    print(result)
```

See `../docs/error-handling.md` for more details.
