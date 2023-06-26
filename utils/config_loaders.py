import logging
import logging.config
import os
from pathlib import Path
from typing import Any, Dict

import yaml


def get_current_path() -> Path:
    """
    Gets the current file path.

    :return: A Path object of the current path.
    """
    current_path = Path(__file__).parent.absolute()
    logging.debug('current path %s', current_path)
    return current_path


def get_config_file_path(env: str) -> Path:
    """
    Builds the file path to the config file based on the given environment.

    :param env: The environment.
    :return: A Path object to the config file.
    """
    current_path = get_current_path()
    config_file_name = f'{env.lower()}.yaml'
    return current_path.parent / 'config' / config_file_name


def get_current_environment(default: str = 'development') -> str:
    """
    Gets the current environment from the 'ENV' environment variable, or returns a default value.
    for example, if you set the ENV variable to 'production', this function will return 'production'.

    :param default: The default environment to use if 'ENV' is not set.
    :return: The current environment.
    """
    return os.getenv('ENV', default)


def get_env_variable(environment_variable: str) -> str:
    """
    Gets the value of an environment variable, or raises an exception if it is not defined.

    :param environment_variable: The name of the environment variable to get.
    :return: The value of the environment variable.
    :raises: ValueError if the environment variable is not defined.
    """
    env = os.getenv(environment_variable)
    if env is None:
        raise ValueError(f"You must define the '{environment_variable}' environment variable.")
    return env


def load_yaml_file(file_path: Path) -> Dict[str, Any]:
    """
    Loads the content of a YAML file.

    :param file_path: A Path object to the YAML file.
    :return: A dictionary with the content of the YAML file.
    """
    try:
        with open(file_path, 'r') as file:
            return yaml.safe_load(file) or {}
    except FileNotFoundError:
        logging.error(f"File {file_path} not found.")
        return {}
    except Exception as e:
        logging.error(f"An error occurred while loading the file {file_path}: {e}")
        return {}


def get_config() -> Dict[str, Any]:
    """
    Gets the configuration for the current environment.

    :return: A dictionary containing the configuration values.
    """
    env = get_current_environment()
    environment_config = load_yaml_file(get_config_file_path(env))
    default_config = load_yaml_file(get_config_file_path('default'))
    return {**default_config, **environment_config}


def get_secrets(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Gets the secrets for the current environment.

    :param config: The configuration for the current environment.
    :return: A dictionary containing the secrets.
    """
    environment = get_current_environment()
    if environment == 'development':
        logging.info('Initializing service with the development API tokens')
        secrets = config.get('secrets')
        if secrets is None:
            logging.warning("'secrets' not found in configuration.")
        return secrets
    else:
        logging.info(f'Initializing service with the {environment} API tokens')
        secrets_path = Path(get_env_variable('SECRETS_PATH')) / 'credentials.yaml'
        return load_yaml_file(secrets_path)


def setup_logging(config: Dict[str, Any]):
    """
    Sets up logging using the specified configuration.

    :param config: The configuration for logging.
    """
    try:
        root_logger = logging.getLogger()
        root_logger.handlers.clear()
        logging.config.dictConfig(config['logging'])
        root_logger.setLevel(logging.getLevelName(config['logging_level']))
    except Exception as e:
        logging.basicConfig(level=logging.INFO)
        logging.warning(f'Failed to load logging configuration. Using default configuration. Error: {e}')
