import ast
import os
import pathlib

from setuptools import setup
from setuptools.command.build_py import build_py
from setuptools.command.sdist import sdist
from packaging.version import Version

HERE = pathlib.Path(__file__).parent.resolve()
LONG_DESCRIPTION = (HERE / "README.md").read_text(encoding="utf8")
LONG_DESC_TYPE = "text/markdown"

# Do not import runtime metadata: an older installed SDK must not affect builds.
VERSION_SOURCE = (HERE / 'ixbrowser_local_api' / 'version.py').read_text(encoding='utf8')
SOURCE_VERSION = next(ast.literal_eval(node.value) for node in ast.parse(VERSION_SOURCE).body
                      if isinstance(node, ast.Assign)
                      and any(isinstance(target, ast.Name) and target.id == '_SOURCE_VERSION' for target in node.targets))
# Version validates PEP 440, including v-prefixed tags and prerelease suffixes.
CURR_VERSION = str(Version(os.environ.get('TAG', SOURCE_VERSION).strip()))
FROZEN_VERSION_SOURCE = VERSION_SOURCE.replace(
    '_SOURCE_VERSION = "{}"'.format(SOURCE_VERSION), '_SOURCE_VERSION = "{}"'.format(CURR_VERSION), 1)


class VersionedBuildPy(build_py):
    def run(self):
        super().run()
        (pathlib.Path(self.build_lib) / 'ixbrowser_local_api' / 'version.py').write_text(
            FROZEN_VERSION_SOURCE, encoding='utf8')


class VersionedSdist(sdist):
    def make_release_tree(self, base_dir, files):
        super().make_release_tree(base_dir, files)
        version_path = pathlib.Path(base_dir) / 'ixbrowser_local_api' / 'version.py'
        # Break a possible hard link before freezing the release copy.
        version_path.unlink()
        version_path.write_text(FROZEN_VERSION_SOURCE, encoding='utf8')

setup(name='ixbrowser-local-api',
      version=CURR_VERSION,
      description='A client of ixBrowser local api',
      long_description=LONG_DESCRIPTION,
      long_description_content_type=LONG_DESC_TYPE,
      author='ixBrowser Team',
      author_email='tech@ixbrowser.com',
      url='https://github.com/ixspyinc/ixbrowser-local-api-python',
      license='MIT',
      keywords='',
      # Only the SDK is shipped. find_packages() would also pick up the top level
      # tests package and install it into the user environment.
      packages=['ixbrowser_local_api'],
      cmdclass={'build_py': VersionedBuildPy, 'sdist': VersionedSdist},
      install_requires=['requests >= 2'],
      python_requires='>=3.8',
      classifiers=["Programming Language :: Python :: 3.8",
                   "Programming Language :: Python :: 3.9",
                   "Programming Language :: Python :: 3.10",
                   "Programming Language :: Python :: 3.11",
                   "Programming Language :: Python :: 3.12",
                   "Programming Language :: Python :: 3.13",
                   "Programming Language :: Python :: 3.14",]
      )
