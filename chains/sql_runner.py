# %%
import logging
from typing import Any, Dict

import pandas as pd
from sqlalchemy.engine import Engine

from prompts.column_extractor import ColumnExtractor
from prompts.info_extractor import InfoExtractor
from prompts.sql_runner import SQLRunner
from utils.config_loaders import get_config, get_secrets
from utils.database import get_table_info, create_db_session

config = get_config()
secrets = get_secrets(config)
engine = create_db_session(secrets['database']['url'])


def select_columns(metadata: Dict[str, Any], selected_columns: Dict) -> Dict:
    final_info = {}
    for table in metadata.keys():
        table_name = metadata[table]["table"]
        columns = [
            column for column in metadata[table_name]["columns"] if column["column_name"]
            in selected_columns[table_name]["columns"]
        ]
        final_info[f'{table_name}'] = {
            "table": table_name,
            "columns": columns
        }
    return final_info


def sql_runner(
        query: str,
        database: Engine,
        top_k: int = 20
) -> Dict:
    try:
        extract_tables = InfoExtractor(query=query).get_result()
        metadata_all_tables = get_table_info(extract_tables, database)

        # for schema_table in list(metadata_all_tables.keys()):
        select_correct_columns = ColumnExtractor(query=query, table_info=metadata_all_tables).get_result()
        filter_metadata = select_columns(metadata_all_tables, select_correct_columns)

        runner = SQLRunner(
            input=query,
            table_info=filter_metadata,
            dialect=database.dialect.name,
            top_k=top_k,
            model_name='gpt-3.5-turbo',
            temperature=0
        )
        sql_code = runner.get_result()

        with database.connect() as conn:
            result = pd.read_sql_query(sql_code['query'], conn)

        result = {
            "sql_code": sql_code['query'],
            "data": result
        }

        return result
    except Exception as e:
        logging.error(f'Error running the SQL runner chain: {e}')
        return {
            "Error": f"Error running the SQL runner chain, Don't try again: {str(e)}"
        }
