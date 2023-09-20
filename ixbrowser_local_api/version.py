import os

__version__ = os.getenv("TAG", "0.0.0")
VERSION = tuple(map(int, __version__.split('.')))
