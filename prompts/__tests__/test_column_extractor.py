from prompts.column_extractor import ColumnExtractor, Table
from prompts.info_extractor import InfoExtractor
from utils.config_loaders import get_config, get_secrets
from utils.database import create_db_session, get_table_info

config = get_config()
secrets = get_secrets(config)


class TestTable:

    def test_table_initialization(self):
        table = Table(table='public.example', columns=['column1', 'column2'])
        assert table.table == 'public.example'
        assert table.columns == ['column1', 'column2']


class TestSpanishColumnExtractor:

    def test_column_extractor_initialization(self):
        table_info = {
            'public.example': {
                'table': 'public.example',
                'columns': [
                    {
                        'column_name': 'has_pregnant_traveler',
                        'type': 'BOOLEAN',
                        'comment': None,
                        'is_foreign_key': False,
                        'is_primary_key': False,
                        'foreign_key_tables': None
                    }]
            }
        }
        column_extractor = ColumnExtractor(
            query='query',
            table_info=table_info
        )
        assert column_extractor.query == 'query'
        assert column_extractor.table_info == table_info
        assert column_extractor.model_name == 'gpt-3.5-turbo'
        assert column_extractor.temperature == 0

    def test_get_result(self):
        table_info = {
            'public.example': {
                'table': 'public.example',
                'columns': [
                    {
                        'column_name': 'has_pregnant_traveler',
                        'type': 'BOOLEAN',
                        'comment': None,
                        'is_foreign_key': False,
                        'is_primary_key': False,
                        'foreign_key_tables': None
                    }]
            }
        }
        column_extractor = ColumnExtractor(
            query='I want to know how many records of has_pregnant_traveler there are in the public.example table.',
            table_info=table_info
        )
        result = column_extractor.get_result()
        assert result == {
            'public.example': {
                'table': 'public.example',
                'columns': ['has_pregnant_traveler']
            }
        }

    # TODO: You should change the schema and table names to match your database
    def test_get_result_with_table(self):
        query = 'I want to know how many unique records there are in the customer table of the sales schema.'
        info_extractor = InfoExtractor(query=query).get_result()
        info_table = get_table_info(info_extractor, create_db_session(config['secrets']['database']['url']))
        result = ColumnExtractor(query=query, table_info=info_table).get_result()
        assert result == {
            'sales.customer':
                {
                    'table': 'sales.customer',
                    'columns': ['customerid', 'personid', 'storeid', 'territoryid', 'rowguid']
                }
        }
