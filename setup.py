import pathlib
import runpy

from setuptools import setup

HERE = pathlib.Path(__file__).parent.resolve()
LONG_DESCRIPTION = (HERE / "README.md").read_text(encoding="utf8")
LONG_DESC_TYPE = "text/markdown"

# Load version metadata without importing the package and its dependencies.
VERSION_INFO = runpy.run_path(str(HERE / 'ixbrowser_local_api' / 'version.py'))
CURR_VERSION = '.'.join(str(x) for x in VERSION_INFO['VERSION'])

setup(name='ixbrowser-local-api',
      version=CURR_VERSION,
      description='A client of ixBrowser local api',
      long_description=LONG_DESCRIPTION,
      long_description_content_type=LONG_DESC_TYPE,
      author='ixBrowser Team',
      author_email='tech@ixborwser.com',
      url='https://github.com/ixspyinc/ixbrowser-local-api-python',
      license='MIT',
      keywords='',
      # Only the SDK is shipped. find_packages() would also pick up the top level
      # tests package and install it into the user environment.
      packages=['ixbrowser_local_api'],
      install_requires=['requests >= 2'],
      classifiers=["Programming Language :: Python :: 3.5",
                   "Programming Language :: Python :: 3.6",
                   "Programming Language :: Python :: 3.7",
                   "Programming Language :: Python :: 3.8",
                   "Programming Language :: Python :: 3.9",
                   "Programming Language :: Python :: 3.10",
                   "Programming Language :: Python :: 3.11",
                   "Programming Language :: Python :: 3.12",
                   "Programming Language :: Python :: 3.13",]
      )
