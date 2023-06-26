import logging
from pathlib import Path

import pytest
import yaml

from utils.config_loaders import (
    get_current_path, get_config_file_path, get_current_environment,
    get_env_variable, load_yaml_file, get_config, get_secrets, setup_logging
)


def test_get_current_path():
    assert isinstance(get_current_path(), Path)


def test_get_config_file_path():
    env = 'default'
    expected_file_path = get_current_path().parent / 'config' / f'{env}.yaml'
    assert get_config_file_path(env) == expected_file_path


def test_get_current_environment(monkeypatch):
    monkeypatch.setenv('ENV', 'production')
    assert get_current_environment() == 'production'
    monkeypatch.delenv('ENV', raising=False)
    assert get_current_environment() == 'development'


def test_get_env_variable(monkeypatch):
    monkeypatch.setenv('TEST_VAR', 'value')
    assert get_env_variable('TEST_VAR') == 'value'
    with pytest.raises(ValueError):
        get_env_variable('NON_EXISTING_VAR')


def test_load_yaml_file(tmp_path):
    yaml_content = {
        'key': 'value'
    }
    yaml_file_path = tmp_path / 'test.yaml'
    with open(yaml_file_path, 'w') as file:
        yaml.dump(yaml_content, file)
    assert load_yaml_file(yaml_file_path) == yaml_content
    assert load_yaml_file(Path('non_existing_file.yaml')) == {}


def test_get_config(monkeypatch, tmp_path):
    yaml_content = {
        'key': 'value'
    }
    yaml_file_path = tmp_path / 'development.yaml'
    with open(yaml_file_path, 'w') as file:
        yaml.dump(yaml_content, file)
    monkeypatch.setattr('utils.config_loaders.get_config_file_path', lambda x: yaml_file_path)
    assert get_config() == yaml_content


def test_get_secrets(monkeypatch, tmp_path):
    # just for coverage
    config = {
        'env': 'development',
        'secrets': {
            'api_tokens': {
                'generic': 'this is a test credential!'
            },
            # Rest of your secrets...
        }
    }

    # Testing non-development environment
    monkeypatch.setenv('ENV', 'production')
    secrets = {
        'test': 'secret'
    }
    credentials_file = tmp_path / 'credentials.yaml'
    with open(credentials_file, 'w') as file:
        yaml.dump(secrets, file)
    monkeypatch.setattr('utils.config_loaders.get_env_variable', lambda x: str(tmp_path))
    assert get_secrets(config) == secrets


def test_setup_logging():
    config = {
        'logging_level': 'INFO',
        "logging": {
            "version": 1,
            "disable_existing_loggers": True,
            "root": {
                "level": "INFO",
            }
        }
    }
    setup_logging(config)
    assert logging.getLogger().level == logging.INFO
