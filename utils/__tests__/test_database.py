import pytest

from utils.config_loaders import get_secrets, get_config
from utils.database import create_db_session, get_table_info

config = get_config()
secrets = get_secrets(config)
engine = create_db_session(config['secrets']['database']['url'])


def test_create_db_session():

    assert engine is not None

    with pytest.raises(Exception):
        create_db_session('invalid_database_url')


def test_get_table_info():
    # TODO: Add test cases for get_table_info function, this depends on your database
    schema = {
        'schemas': {
            'sales': ['store']
        }
    }
    expected_name = 'sales.store'

    result = get_table_info(schema, engine)
    assert list(result.keys())[0] == expected_name
    assert len(result[expected_name]['columns']) > 1

    with pytest.raises(Exception):
        get_table_info({}, engine)
