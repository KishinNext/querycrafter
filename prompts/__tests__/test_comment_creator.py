import pandas as pd

from prompts.comment_creator import Table, CommentCreator


class TestTable:

    def test_table_initialization(self):
        table = Table(
            table_name='example',
            schema_name='public',
            columns=[{
                'column_name': 'id',
                'comment': 'Unique identifier of the user'
            }]
        )
        assert table.table_name == 'example'
        assert table.schema_name == 'public'
        assert table.columns == [{
            'column_name': 'id',
            'comment': 'Unique identifier of the user'
        }]


class TestCommentCreator:

    def test_comment_creator__initialization(self):
        table_name = 'example'
        schema_name = 'public'
        table_info = [{
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
                    },
                    {
                        'column_name': 'total_sales',
                        'type': 'BOOLEAN',
                        'comment': None,
                        'is_foreign_key': False,
                        'is_primary_key': False,
                        'foreign_key_tables': None
                    }
                ]
            }
        }]
        table_data = pd.DataFrame()
        table_data['has_pregnant_traveler'] = ['true', 'true', 'false', 'false']

        comment_creator = CommentCreator(
            table_name=table_name,
            schema_name=schema_name,
            table_info=table_info,
            table_data=table_data
        )
        assert comment_creator.table_name == table_name
        assert comment_creator.schema_name == schema_name
        assert comment_creator.table_info == table_info
        assert comment_creator.table_data.equals(table_data)
        assert comment_creator.model_name == 'gpt-3.5-turbo'
        assert comment_creator.temperature == 0

        result = comment_creator.get_result()

        assert result['table_name'] == 'example'
        assert result['schema_name'] == 'public'
        assert len(result['columns']) == 2
        assert result['columns'][0]['column_name'] == 'has_pregnant_traveler'
        assert result['columns'][1]['column_name'] == 'total_sales'
