"""Regression checks for version, docs and nested configuration improvements."""
import os
from pathlib import Path
import runpy
import shutil
import subprocess
import sys
import tarfile
import zipfile

import pytest

from ixbrowser_local_api import Consts, Profile
from ixbrowser_local_api.errors import UnexpectedError

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize('field', ['proxy_config', 'preference_config', 'fingerprint_config'])
def test_direct_nested_dictionary(field):
    profile = Profile()
    setattr(profile, field, {'value': 0, 'enabled': False})
    assert profile.dump_to_dict() == {field: {'value': 0, 'enabled': False}}
    setattr(profile, field, {})
    assert profile.dump_to_dict() == {}


@pytest.mark.parametrize('field', ['proxy_config', 'preference_config', 'fingerprint_config'])
@pytest.mark.parametrize('value', [1, False, [], 'invalid'])
def test_invalid_nested_configuration_is_not_silently_dropped(field, value):
    profile = Profile()
    setattr(profile, field, value)
    with pytest.raises(UnexpectedError, match=field):
        profile.dump_to_dict()


def test_invalid_nested_serializer_result():
    class InvalidEntity:
        def dump_to_dict(self):
            return []
    profile = Profile()
    profile.proxy_config = InvalidEntity()
    with pytest.raises(UnexpectedError, match='proxy_config'):
        profile.dump_to_dict()


def test_format_aliases():
    assert Consts.PROXY_DATA_FORMAT_TYPE_TXT == Consts.PROXY_DATA_FROMAT_TYPE_TXT == 'txt'
    assert Consts.PROXY_DATA_FORMAT_TYPE_JSON == Consts.PROXY_DATA_FROMAT_TYPE_JSON == 'json'


def test_proxy_documentation_matches_constants():
    docs = (ROOT / 'docs' / 'api-reference.md').read_text(encoding='utf8')
    assert '| `update_profile_to_purchased_proxy_mode(profile_id, proxy_id)` | `{}` |'.format(
        Consts.ACTION_FOR_PROFILE_UPDATE_PROXY_TO_PURCHASED_MODE) in docs
    assert '| `update_profile_to_api_extraction_proxy_mode(...)` | `{}` |'.format(
        Consts.ACTION_FOR_PROFILE_UPDATE_PROXY_TO_API_EXTRACTION_MODE) in docs


def test_runtime_ignores_tag(monkeypatch):
    import ixbrowser_local_api
    monkeypatch.setenv('TAG', 'not-a-version')
    info = runpy.run_path(str(ROOT / 'ixbrowser_local_api' / 'version.py'))
    assert info['__version__'] == ixbrowser_local_api.__version__
    assert info['VERSION'] == ixbrowser_local_api.VERSION


@pytest.mark.parametrize('tag, expected', [('v1.2.0', '1.2.0'), ('v1.2.0rc1', '1.2.0rc1'), ('2.0.0+local', '2.0.0+local')])
def test_build_preserves_complete_version(tag, expected):
    result = subprocess.run([sys.executable, 'setup.py', '--version'], cwd=str(ROOT),
                            env=dict(os.environ, TAG=tag), capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == expected


def test_build_rejects_invalid_tag():
    result = subprocess.run([sys.executable, 'setup.py', '--version'], cwd=str(ROOT),
                            env=dict(os.environ, TAG='invalid'), capture_output=True, text=True)
    assert result.returncode != 0
    assert 'InvalidVersion' in result.stderr


def test_sdist_rebuild_freezes_version_without_tag(tmp_path):
    source = tmp_path / 'source'
    source.mkdir()
    for name in ['setup.py', 'pyproject.toml', 'README.md', 'LICENSE']:
        shutil.copy2(str(ROOT / name), str(source / name))
    shutil.copytree(str(ROOT / 'ixbrowser_local_api'), str(source / 'ixbrowser_local_api'),
                    ignore=shutil.ignore_patterns('__pycache__'))
    env = dict(os.environ, TAG='v1.2.0rc1')
    result = subprocess.run([sys.executable, 'setup.py', 'sdist'], cwd=str(source),
                            env=env, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    archive = next((source / 'dist').glob('*.tar.gz'))
    unpacked = tmp_path / 'unpacked'
    with tarfile.open(str(archive)) as bundle:
        # This archive was produced locally from our own copied package.
        bundle.extractall(str(unpacked))
    release = next(unpacked.iterdir())
    env.pop('TAG')
    result = subprocess.run([sys.executable, 'setup.py', 'bdist_wheel'], cwd=str(release),
                            env=env, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    with zipfile.ZipFile(str(next((release / 'dist').glob('*.whl')))) as wheel:
        version_source = wheel.read('ixbrowser_local_api/version.py').decode('utf8')
        metadata = wheel.read(next(name for name in wheel.namelist() if name.endswith('/METADATA'))).decode('utf8')
    namespace = {}
    exec(version_source, namespace)
    assert namespace['__version__'] == '1.2.0rc1'
    assert namespace['VERSION'] == (1, 2, 0)
    assert 'Version: 1.2.0rc1' in metadata
    assert 'Requires-Python: >=3.8' in metadata
    assert 'Classifier: Programming Language :: Python :: 3.14' in metadata
    for unsupported in ['3.5', '3.6', '3.7']:
        assert 'Classifier: Programming Language :: Python :: ' + unsupported + '\n' not in metadata
    assert '_SOURCE_VERSION = "0.0.0"' in (source / 'ixbrowser_local_api' / 'version.py').read_text(encoding='utf8')
