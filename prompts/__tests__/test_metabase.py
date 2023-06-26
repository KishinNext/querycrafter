import pandas as pd
import pytest
from pydantic import ValidationError

from prompts.info_extractor import InfoExtractor
from prompts.metabase_creator import MetabaseCreator, InfoQuery, Info
from utils.config_loaders import get_config, get_secrets
from utils.database import create_db_session, get_table_info, get_data

config = get_config()
secrets = get_secrets(config)


class TestJSON:

    def test_info_json_valid(self):
        # Crear un objeto JSON válido para el test
        json_data = InfoQuery(
            dashboard_name='Dashboard 1',
            info_json=[
                Info(
                    table_name='table1',
                    schema_name='schema1',
                    title='Table 1',
                    query='SELECT * FROM table1',
                    classify='Table',
                    description='Description of Table 1'
                ),
                Info(
                    table_name='table2',
                    schema_name='schema2',
                    title='Table 2',
                    query='SELECT * FROM table2',
                    classify='Bar Chart',
                    description='Description of Table 2'
                )
            ]
        )

        # Verificar que el objeto JSON creado sea válido
        assert json_data.dashboard_name == 'Dashboard 1'
        assert json_data.info_json[0].table_name == 'table1'
        assert json_data.info_json[0].schema_name == 'schema1'
        assert json_data.info_json[0].title == 'Table 1'
        assert json_data.info_json[0].query == 'SELECT * FROM table1'
        assert json_data.info_json[0].classify == 'Table'
        assert json_data.info_json[0].description == 'Description of Table 1'
        assert json_data.info_json[1].table_name == 'table2'
        assert json_data.info_json[1].schema_name == 'schema2'
        assert json_data.info_json[1].title == 'Table 2'
        assert json_data.info_json[1].query == 'SELECT * FROM table2'
        assert json_data.info_json[1].classify == 'Bar Chart'
        assert json_data.info_json[1].description == 'Description of Table 2'

    def test_info_json_invalid(self):
        with pytest.raises(ValidationError):
            InfoQuery(
                dashboard_name='Dashboard 1',
                info_json=[
                    Info(
                        table_name='table1',
                        schema_name='schema1',
                        title='Table 1',
                        query='SELECT * FROM table1',
                        classify='Table'
                    )
                ]
            )


class TestSpanishMetabaseCreator:

    def test_column_extractor_initialization(self):
        table_metadata = {
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
        table_info = {
            'public.example': pd.DataFrame()
        }

        column_extractor = MetabaseCreator(
            user_question='query',
            table_info=table_info,
            table_metadata=table_metadata,
            engine_type='postgresql'
        )
        assert column_extractor.user_question == 'query'
        assert column_extractor.table_info == table_info
        assert column_extractor.table_metadata == table_metadata
        assert column_extractor.engine_type == 'postgresql'
        assert column_extractor.model_name == 'gpt-3.5-turbo'
        assert column_extractor.temperature == 0

    # TODO: You should change the schema and table names to match your database
#     Just run it if you have already configured the metabase config file
#     This test will crete a dashboard in your metabase instance
#     def test_get_result_with_table(self):
#         query = """
# I want to generate a dashboard that shows me the main KPIs. I want you to use the tables 'production.product',
#  'production.productsubcategory', 'production.productcategory', and 'production.productcosthistory'.
#         """
#         info_extractor = InfoExtractor(query=query).get_result()
#         engine = create_db_session(secrets['database']['url'])
#         table_metadata = get_table_info(info_extractor, engine)
#         table_data = get_data(info_extractor, engine)
#         result = MetabaseCreator(
#             user_question=query,
#             table_info=table_data,
#             table_metadata=table_metadata,
#             engine_type='postgresql',
#             model_name='gpt-4',
#             number_of_queries=10
#         ).get_result()
#         assert len(result['info_json']) >= 1
#         assert result['info_json'][0]['table_name'] == 'product'
#         assert result['info_json'][0]['schema_name'] == 'production'
