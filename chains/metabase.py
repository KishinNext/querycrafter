import logging
import os
from typing import Dict, Any, List

import requests
from sqlalchemy.engine import Engine

from chains.document_tables import get_data
from prompts.info_extractor import InfoExtractor
from prompts.metabase_creator import MetabaseCreator
from utils.config_loaders import (
    get_config
)
from utils.database import get_table_info
from utils.metabase import (
    base_numeric_indicator,
    base_bar_chart,
    base_line_chart,
    base_table,
    create_numeric_indicator,
    create_linechart,
    create_barchart,
    create_table,
)
from utils.metabase import create_metabase_collection, create_metabase_dashboard

config = get_config()


def process_metabase_queries(
        metabase_queries: List[Dict[str, Any]],
        collection_info: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """
    Process metabase queries and create the corresponding cards
    Args:
        metabase_queries: List of metabase queries to be processed
        collection_info: Information about the collection to which the cards will be added
    Returns: List of responses from the metabase API
    """
    responses = []
    for card_info in metabase_queries:
        headers = {
            "Content-Type": config['secrets']['metabase']['content_type'],
            "X-Metabase-Session": config['secrets']['metabase']['metabase_session']
        }
        metabase_url = config['secrets']['metabase']['metabase_url']
        database_id = config['secrets']['metabase']['database_id']
        collection_id = collection_info['id']

        if card_info['classify'] == 'Numeric Indicator':
            try:
                responses.append(create_numeric_indicator(
                    metabase_url=metabase_url,
                    database_id=database_id,
                    collection_id=collection_id,
                    card_info=card_info,
                    headers=headers,
                    numeric_indicator_structure=base_numeric_indicator
                ))
            except Exception as e:
                logging.error(f'Error creating numeric indicator: {e}')

        elif card_info['classify'] == 'Bar Chart':
            try:
                responses.append(create_barchart(
                    metabase_url=metabase_url,
                    database_id=database_id,
                    collection_id=collection_id,
                    card_info=card_info,
                    headers=headers,
                    barchart_structure=base_bar_chart
                ))
            except Exception as e:
                logging.error(f'Error creating bar chart: {e}')

        elif card_info['classify'] == 'Line Chart':
            try:
                responses.append(create_linechart(
                    metabase_url=metabase_url,
                    database_id=database_id,
                    collection_id=collection_id,
                    card_info=card_info,
                    headers=headers,
                    linechart_structure=base_line_chart
                ))
            except Exception as e:
                logging.error(f'Error creating line chart: {e}')

        elif card_info['classify'] == 'Table':
            try:
                responses.append(create_table(
                    metabase_url=metabase_url,
                    database_id=database_id,
                    collection_id=collection_id,
                    card_info=card_info,
                    headers=headers,
                    table_structure=base_table
                ))
            except Exception as e:
                logging.error(f'Error creating table: {e}')

    return responses


def insert_card_into_dashboard(cards_response: List[Dict[str, Any]], dashboard_id: int) -> None:
    """
    Insert cards into dashboard in Metabase
    Args:
        dashboard_id: Dashboard id to insert the cards
        cards_response: List of cards to be inserted

    Returns: None

    """
    headers = {
        "Content-Type": config['secrets']['metabase']['content_type'],
        "X-Metabase-Session": config['secrets']['metabase']['metabase_session']
    }

    json_base = {
        "cardId": 0,
        "col": 0,
        "row": 0,
        "size_x": 6,
        "size_y": 6,
        "series": [],
        "parameter_mappings": [],
        "visualization_settings": {},
    }

    row = 0
    col = 0

    for i, card_info in enumerate(cards_response):
        try:
            if i % 3 == 0 and i != 0:
                row += 6
                col = 0
            elif i != 0:
                col += 6

            json_base['cardId'] = card_info['id']
            json_base['col'] = col
            json_base['row'] = row

            response = requests.post(os.path.join(
                config['secrets']['metabase']['metabase_url'],
                'api',
                'dashboard',
                str(dashboard_id),
                'cards'
            ), headers=headers, json=[json_base])

            response.raise_for_status()
            logging.info(f'Card {card_info["id"]} inserted into dashboard {dashboard_id}')
        except requests.exceptions.RequestException as err:
            print(f"Error: {err}")
    logging.info(f'Cards inserted into dashboard {dashboard_id}')


def run_graph_creator(query: str, database: Engine, max_queries: int = 10) -> str:
    """
    Run the SQL comment generator and create the corresponding dashboard in Metabase
    Args:
        max_queries: Maximum number of queries to be generated, the system wil try to generate this number of queries.
        query: User question to be processed.
        database: Database connection object.

    Returns: The dashboard url where the queries are stored.

    """
    logging.info(f'Running graph creator for query, metabase chain')
    try:
        info_extractor = InfoExtractor(query=query).get_result()
        table_metadata = get_table_info(info_extractor, database)
        table_data = get_data(info_extractor, database, 10)
        metabase_queries = MetabaseCreator(
            user_question=query,
            table_info=table_data,
            table_metadata=table_metadata,
            engine_type=database.dialect.name,
            model_name=config['default_model_name'],
            number_of_queries=max_queries
        ).get_result()

        collection_info = create_metabase_collection(
            parent_id=config['secrets']['metabase']['collection_parent'],
            dashboard_name=metabase_queries['dashboard_name'],
            metabase_url=config['secrets']['metabase']['metabase_url'],
            headers={
                "Content-Type": config['secrets']['metabase']['content_type'],
                "X-Metabase-Session": config['secrets']['metabase']['metabase_session']
            }
        )

        responses = process_metabase_queries(metabase_queries['info_json'], collection_info)

        dashboard_info = create_metabase_dashboard(
            collection_id=collection_info['id'],
            dashboard_name=metabase_queries['dashboard_name'],
            metabase_url=config['secrets']['metabase']['metabase_url'],
            headers={
                "Content-Type": config['secrets']['metabase']['content_type'],
                "X-Metabase-Session": config['secrets']['metabase']['metabase_session']
            }
        )

        insert_card_into_dashboard(responses, dashboard_info['id'])
        return f"""You can check the dashboard created: 
        {config['secrets']['metabase']['metabase_url']}/dashboard/{dashboard_info['id']}"""
    except Exception as e:
        logging.error(f"Failed to get the metadata or the dataframe: {str(e)}")
        return f"Failed to create the metabase dashboard, Don't try again: {str(e)}"
