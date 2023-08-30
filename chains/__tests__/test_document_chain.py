from unittest.mock import patch

from pandas import DataFrame

from chains.document_tables import (
    generate_sql_code,
    get_data,
    process_columns_in_chunks,
    run_sql_comment_generator
)
from utils.config_loaders import (
    get_config
)
from utils.config_loaders import (
    get_secrets
)
from utils.database import create_db_session
import pytest

config = get_config()
secrets = get_secrets(config)


def test_generate_sql_code():
    gpt_comments = {
        'columns': [{
            'column_name': 'col1',
            'comment': 'test1'
        }, {
            'column_name': 'col2',
            'comment': 'test2'
        }]
    }
    schema_name = 'schema'
    table_name = 'table'
    result = generate_sql_code(gpt_comments, schema_name, table_name)
    expected = "COMMENT ON COLUMN schema.table.col1 IS 'test1';\nCOMMENT ON COLUMN schema.table.col2 IS 'test2';\n"
    assert result == expected


@pytest.mark.skipif(True, reason='should be ran only manually with AdventureWorks Database')
def test_get_data():
    info_extractor = {
        'schemas': {
            'sales': ['store'],
        }
    }
    engine = create_db_session(secrets['database']['url'])
    result = get_data(info_extractor, engine)
    assert set(result.keys()) == {'sales.store'}
    assert isinstance(result['sales.store'], DataFrame)


def test_process_columns_in_chunks():
    table_name = 'table'
    schema_name = 'schema'
    columns_info = [{
        'column_name': 'col1'
    }]
    pandas_info = DataFrame(columns=['col1'])
    result = process_columns_in_chunks(table_name, schema_name, columns_info, pandas_info)
    expected = {
        'table_name': 'table',
        'schema_name': 'schema',
        'columns': [{
            'column_name': 'col1',
            'comment': 'test'
        }]
    }
    assert result['table_name'] == expected['table_name']
    assert result['schema_name'] == expected['schema_name']
    assert len(result['columns']) == len(expected['columns'])
    assert result['columns'][0]['column_name'] == expected['columns'][0]['column_name']
    assert isinstance(result['columns'][0]['comment'], str)


@pytest.mark.skipif(True, reason='should be ran only manually with AdventureWorks Database')
def test_run_sql_comment_generator():
    database = create_db_session(secrets['database']['url'])
    query = 'I need the SQL code to comment on the columns of the currency in the sales schema'
    result = run_sql_comment_generator(query, database)
    assert isinstance(result, str)
    assert 'COLUMN sales.currency.currencycode' in result
    assert 'COLUMN sales.currency.name' in result
    assert 'COLUMN sales.currency.modifieddate' in result
    assert 'sales.currency' in result
