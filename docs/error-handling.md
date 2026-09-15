# Error Handling

The SDK wraps HTTP and Local API response errors with a simple return convention:

- Success: the method returns API data, or `True` for operations without data.
- Failure: the method returns `None`.
- Error details: read `client.code` and `client.message`.

## Basic Pattern

```python
from ixbrowser_local_api import IXBrowserClient

c = IXBrowserClient()

result = c.get_profile_list()
if result is None:
    print("Error code:", c.code)
    print("Error message:", c.message)
else:
    print(result)
```

## Why Methods Return `None`

Client methods catch SDK errors internally and store the error state on the
client instance. This keeps example scripts simple and gives callers one common
way to check failures.

The error state is reset before each request:

```python
self.code = None
self.message = None
self.total = None
```

After a failed request, `client.code` and `client.message` are populated.
`client.total` describes only the latest successful paginated request; it is
cleared before other requests as well as failed requests.

## Error Types

The SDK defines these error classes in `ixbrowser_local_api/errors.py`:

| Error class | When it is used | `code` |
| --- | --- | --- |
| `UnexpectedError` | Request exceptions, malformed responses, an unsupported method argument, or unexpected response data. | `1` |
| `HttpError` | The HTTP status code is not `200`. | The HTTP status code. |
| `ResponseError` | The Local API response contains a non-zero error code. | The API error code. `message` is `None` when the response carries only a code. |

## HTTP and API Response Flow

`Utils.get_api_response()` sends a POST request with JSON body data:

```python
requests.post(url, json=params, timeout=20)
```

The SDK expects:

- HTTP status code `200`.
- A JSON response containing an `error` object.
- `error.code == 0` for success.

If `data` exists on a successful response, that data is returned. If no `data`
field exists and the operation succeeded, the method returns `True`.

## Checking Empty Data vs. Failure

Always check for `None` rather than using a truthy check. An empty list can be a
valid successful result.

Recommended:

```python
profiles = c.get_profile_list()
if profiles is None:
    print(c.code, c.message)
else:
    print("Profile count:", len(profiles))
```

Avoid:

```python
profiles = c.get_profile_list()
if not profiles:
    print("This may be an error, or it may be an empty successful result.")
```

## Debug Request Logs

Use Python's standard logging configuration to enable HTTP debug logs:

```python
import logging

logging.basicConfig(level=logging.WARNING)
logging.getLogger("ixbrowser_local_api").setLevel(logging.DEBUG)
```

The SDK emits DEBUG records through `ixbrowser_local_api.http` for request URLs,
parameters and successful HTTP response bodies. It does not configure log levels,
output destinations or formatting, and does not print logs to stdout. With no
application logging configuration, request logs are silent. Existing applications
can route these records through their own handlers instead of using `basicConfig`.

Migration: `Utils.show_request_log` and `IXBrowserClient.show_request_log` have
been removed. Replace assignments to those attributes with logging configuration;
assigning them no longer enables request logs.

Warning: logs are not redacted. DEBUG output may contain passwords, cookies,
proxy credentials and transfer codes. Enable it only in a trusted environment.
