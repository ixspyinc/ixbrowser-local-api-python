"""Runtime version; release builds freeze _SOURCE_VERSION in the artifact."""
import re

_SOURCE_VERSION = "0.0.0"
__version__ = _SOURCE_VERSION
if __version__ == "0.0.0":
    try:
        from importlib.metadata import PackageNotFoundError, version
    except ImportError:  # Older Python versions may run directly from source.
        pass
    else:
        try:
            __version__ = version("ixbrowser-local-api")
        except PackageNotFoundError:
            pass

# Keep the historical numeric tuple without losing suffixes in __version__.
_release = re.match(r"(?:\d+!)?(\d+(?:\.\d+)*)", __version__)
VERSION = tuple(map(int, _release.group(1).split('.'))) if _release else (0, 0, 0)
