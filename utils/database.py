import logging
import traceback
from typing import Any, Dict

import pandas as pd
from pandas import DataFrame
from sqlalchemy import MetaData, Table
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text


def create_db_session(database_url: str) -> Engine:
    """
    Creates a SQLAlchemy session for the specified database URL.

    :param database_url: The URL of the database to connect to.
    :return: A tuple containing an instance of SQLAlchemy Session and an Engine object.
    """
    try:
        logging.info('trying to connect to database')
        # Create a new SQLAlchemy engine instance with the given database URL.
        engine_obj = create_engine(database_url)

        # Emit a simple select query to check the connection
        with engine_obj.connect() as connection:
            connection.execute(text("SELECT 1"))

        logging.info(f"Connected to database successfully")
        return engine_obj
    except SQLAlchemyError as e:
        logging.error(f"Error connecting to database: {str(e)} using URL: {database_url}")
        raise e


def get_table_info(table_names_by_schema: Dict, engine_object: Engine) -> Dict[str, Any]:
    """
    Gets information about the specified tables.

    :param table_names_by_schema: A dictionary with keys for each schema and values that are lists of table names.
        for example: {'schemas': {'schema_1': ['table_1', 'table_2], 'schema_2': ['table_3', 'table_4']}}
    :param engine_object: A SQLAlchemy engine object.
    :return: A list of dictionaries with information about the tables.
    {'schema_name.table_name': {'table': 'schema_name.table_name', 'columns': [dict_for_column_1, dict_for_column_2]}]
    """

    if not table_names_by_schema:
        raise Exception("Invalid schema, please provide a valid schema")
    if not isinstance(engine_object, Engine):
        raise Exception("Invalid engine object, please provide a valid SQLAlchemy engine object.")
    logging.info('Retrieving table information (metadata)')
    metadata = MetaData()
    table_info = {}
    try:
        for schema_name, table_names in table_names_by_schema['schemas'].items():
            for table_name in table_names:
                information_columns = []

                table = Table(table_name, metadata, autoload_with=engine_object, schema=schema_name)
                for column in table.columns.values():

                    table_dict = {
                        "column_name": str(column.name),
                        "type": str(column.type),
                        # "default": column.default,
                        # "nullable": column.nullable,
                        # "autoincrement": column.autoincrement,
                        "comment": column.comment,
                        "is_foreign_key": bool(column.foreign_keys),
                        "is_primary_key": bool(column.primary_key),
                        "foreign_key_tables": [
                            fk.target_fullname for fk in column.foreign_keys
                        ] if column.foreign_keys else None
                    }

                    information_columns.append(table_dict)

                table_info[f"{schema_name + '.' + table_name}"] = {
                    'table': schema_name + '.' + table_name,
                    'columns': information_columns
                }
        logging.info('Table information retrieved successfully')
        return table_info
    except SQLAlchemyError as e:
        logging.error(f"Error retrieving table information: {str(e)}")
        raise e


def get_data(info_extractor: dict, database: Engine, top_k: int = 10) -> Dict[str, DataFrame]:
    """
    Get data from database to be used in the CommentCreator
    Args:
        info_extractor: infor extractor dictionary, contains the schemas and tables to be used
        database: database connection object
        top_k: number of rows to be retrieved from the database

    Returns: dictionary with the table name as key and a dataframe as value

    """
    logging.info('Getting data from database')
    try:
        table_data = {}
        for schema, tables in info_extractor['schemas'].items():
            for table in tables:
                query = f"SELECT * FROM {schema}.{table} LIMIT {top_k};"
                with database.connect() as conn:
                    result = pd.read_sql_query(query, conn)
                table_data[f'{schema}.{table}'] = result
        logging.info('Data retrieved successfully')
        return table_data
    except SQLAlchemyError as e:
        logging.error(f"Error retrieving data from database: {str(e)}")
        raise e
