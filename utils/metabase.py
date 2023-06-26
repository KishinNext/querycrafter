import logging
import os
from typing import Dict

import httpx
import requests

from prompts.metabase_graphs import MetabaseGraph

base_numeric_indicator = {
    "name": "Card title",
    "dataset_query": {
        "type": "native",
        "native": {
            "query": "Original query",
            "template-tags": {}
        },
        "database": 0
    },
    "display": "scalar",
    "description": "Original description",
    "visualization_settings": {
        "column_settings": {
            "[\"name\",\"column_name\"]": {
                "number_style": "normal",
                "decimals": None,
                "scale": None,
                "prefix": "",
                "suffix": ""
            }
        }
    },
    "parameters": [],
    "collection_id": 0
}

base_bar_chart = {
    "name": "Card title",
    "dataset_query": {
        "type": "native",
        "native": {
            "query": "Original query",
            "template-tags": {}
        },
        "database": 0
    },
    "display": "bar",
    "description": "Original description",
    "visualization_settings": {
        "graph.dimensions": [
            "dimension"
        ],
        "graph.metrics": [
            "metric"
        ]
    },
    "parameters": [],
    "collection_id": 0
}

base_line_chart = {
    "name": "Card title",
    "dataset_query": {
        "type": "native",
        "native": {
            "query": "Original query",
            "template-tags": {}
        },
        "database": 0
    },
    "display": "line",
    "description": "Original description",
    "visualization_settings": {
        "graph.show_goal": False,
        "graph.show_trendline": True,
        "graph.show_values": True,
        "graph.label_value_frequency": "fit",
        "graph.dimensions": [
            "dimension"
        ],
        "graph.metrics": [
            "metric"
        ]
    },
    "parameters": [],
    "collection_id": 0
}

base_table = {
    "name": "Card title",
    "dataset_query": {
        "type": "native",
        "native": {
            "query": "Original query",
            "template-tags": {}
        },
        "database": 0
    },
    "display": "table",
    "description": "Original description",
    "visualization_settings": {
        "table.column_formatting": [
            {
                "columns": [
                    "columns"
                ],
                "type": "range",
                "colors": [
                    "white",
                    "#509EE3"
                ]
            }
        ],
        "column_settings": {
            "[\"name\",\"column_name\"]": {
                "number_style": "normal",
                "decimals": None,
                "scale": None,
                "prefix": "k",
                "suffix": ""
            }
        }
    },
    "parameters": [],
    "collection_id": 0
}


def create_metabase_collection(
        parent_id: int,
        dashboard_name: str,
        metabase_url: str,
        headers: Dict
) -> Dict:
    """
    Create a collection in Metabase.
    Args:
        parent_id:
        dashboard_name:
        metabase_url:
        headers:

    Returns:

    """
    url = os.path.join(metabase_url, 'api', 'collection/')

    payload_collection = {
        "parent_id": parent_id,
        "color": "#509EE3",
        "name": dashboard_name,
    }

    try:
        response = requests.post(url, headers=headers, json=payload_collection)
        response.raise_for_status()
        logging.info(f'Created collection in Metabase: {dashboard_name}')
    except httpx.HTTPStatusError as http_err:
        logging.error(f'HTTP error occurred: {http_err}')
        raise
    except Exception as err:
        logging.error(f'Other error occurred: {err}')
        raise
    else:
        logging.info('Success! Created collection in Metabase.')

    return response.json()


def create_metabase_dashboard(
        collection_id: int,
        dashboard_name: str,
        metabase_url: str,
        headers: Dict
) -> Dict:
    """
    Create a dashboard in Metabase.
    Args:
        collection_id:
        dashboard_name:
        metabase_url:
        headers:

    Returns:

    """
    url = os.path.join(metabase_url, 'api', 'dashboard/')

    payload_collection = {
        "collection_id": collection_id,
        "name": dashboard_name
    }

    try:

        response = requests.post(url, headers=headers, json=payload_collection)
        response.raise_for_status()
        logging.info(f'Created dashboard in Metabase: {dashboard_name}')
    except httpx.HTTPStatusError as http_err:
        logging.error(f'HTTP error occurred: {http_err}')
        raise
    except Exception as err:
        logging.error(f'Other error occurred: {err}')
        raise
    else:
        logging.info('Success! Created dashboard in Metabase.')

    return response.json()


def create_numeric_indicator(
        metabase_url: str,
        database_id: int,
        collection_id: int,
        card_info: Dict,
        headers: Dict,
        numeric_indicator_structure: Dict) -> Dict:
    try:
        graph_info = MetabaseGraph().numeric_indicator(card_info=card_info)
        numeric_indicator_structure['name'] = graph_info['name']
        numeric_indicator_structure['dataset_query']['native']['query'] = graph_info['dataset_query_native_query']
        numeric_indicator_structure['dataset_query']['database'] = database_id
        numeric_indicator_structure['description'] = graph_info['description']
        vs_tmp = {
            'column_settings': {
                '[\"name\", \"' + graph_info['visualization_settings_columns_name'] + '\"]': {
                    'number_style': graph_info['visualization_settings_column_settings_number_style'],
                    'decimals': graph_info['visualization_settings_column_settings_decimals'],
                    'scale': graph_info['visualization_settings_column_settings_scale'],
                    'prefix': graph_info['visualization_settings_column_settings_prefix'],
                    'suffix': graph_info['visualization_settings_column_settings_suffix']
                }
            }
        }
        numeric_indicator_structure['visualization_settings'] = vs_tmp
        numeric_indicator_structure['collection_id'] = collection_id

        response = requests.post(
            os.path.join(metabase_url, 'api', 'card/'),
            headers=headers,
            json=numeric_indicator_structure
        )
        response.raise_for_status()
        logging.info(f'Created Numeric Indicator Card: {graph_info["name"]}')
    except httpx.HTTPStatusError as http_err:
        logging.error(f'HTTP error occurred: {http_err}')
        raise
    except Exception as err:
        logging.error(f'Other error occurred: {err}')
        raise
    else:
        logging.info('Numeric Indicator Card Created!')

    return response.json()


def create_barchart(
        metabase_url: str,
        database_id: int,
        collection_id: int,
        card_info: Dict,
        headers: Dict,
        barchart_structure: Dict) -> Dict:
    try:
        graph_info = MetabaseGraph().bar_chart(card_info=card_info)
        barchart_structure['name'] = graph_info['name']
        barchart_structure['dataset_query']['native']['query'] = graph_info['dataset_query_native_query']
        barchart_structure['dataset_query']['database'] = database_id
        barchart_structure['description'] = graph_info['description']
        barchart_structure['visualization_settings'] = {
            "graph.dimensions": graph_info['visualization_settings_graph_dimensions'],
            "graph.metrics": graph_info['visualization_settings_graph_metrics'],
        }
        base_bar_chart['collection_id'] = collection_id
        response = requests.post(
            os.path.join(metabase_url, 'api', 'card/'),
            headers=headers,
            json=barchart_structure
        )
        response.raise_for_status()
        logging.info(f'Created Bar Chart Card: {graph_info["name"]}')
    except httpx.HTTPStatusError as http_err:
        logging.error(f'HTTP error occurred: {http_err}')
        raise
    except Exception as err:
        logging.error(f'Other error occurred: {err}')
        raise
    else:
        logging.info('Barchart Created!')

    return response.json()


def create_linechart(
        metabase_url: str,
        database_id: int,
        collection_id: int,
        card_info: Dict,
        headers: Dict,
        linechart_structure: Dict) -> Dict:
    try:
        graph_info = MetabaseGraph().line_chart(card_info=card_info)
        linechart_structure['name'] = graph_info['name']
        linechart_structure['dataset_query']['native']['query'] = graph_info['dataset_query_native_query']
        linechart_structure['dataset_query']['database'] = database_id
        linechart_structure['description'] = graph_info['description']
        linechart_structure['visualization_settings'] = {
            "graph.show_goal": False,
            "graph.show_trendline": graph_info['visualization_settings_graph_show_trendline'],
            "graph.show_values": graph_info['visualization_settings_graph_show_values'],
            "graph.label_value_frequency": "fit",
            "graph.dimensions": graph_info['visualization_settings_graph_dimensions'],
            "graph.metrics": graph_info['visualization_settings_graph_metrics']
        }
        linechart_structure['collection_id'] = collection_id
        response = requests.post(
            os.path.join(metabase_url, 'api', 'card/'),
            headers=headers,
            json=linechart_structure
        )
        response.raise_for_status()
        logging.info(f'Created Line Chart Card: {graph_info["name"]}')
    except httpx.HTTPStatusError as http_err:
        logging.error(f'HTTP error occurred: {http_err}')
        raise
    except Exception as err:
        logging.error(f'Other error occurred: {err}')
        raise
    else:
        logging.info('Linechart Created!')

    return response.json()


def create_table(
        metabase_url: str,
        database_id: int,
        collection_id: int,
        card_info: Dict,
        headers: Dict,
        table_structure: Dict) -> Dict:
    try:
        graph_info = MetabaseGraph().table(card_info=card_info)
        table_structure['name'] = graph_info['name']
        table_structure['dataset_query']['native']['query'] = graph_info['dataset_query_native_query']
        table_structure['dataset_query']['database'] = database_id
        table_structure['description'] = graph_info['description']
        tpm = {'[\"name\", \"' + key + '\"]': val for key, val in
            graph_info['visualization_settings_column_formatting_style'].items()}
        table_structure['visualization_settings'] = {
            "table.column_formatting": [
                {
                    "columns": graph_info['visualization_settings_column_formatting_columns'],
                    "type": "range",
                    "colors": graph_info['visualization_settings_column_formatting_colors']
                }
            ],
            "column_settings": tpm
        }
        base_table['collection_id'] = collection_id
        response = requests.post(
            os.path.join(metabase_url, 'api', 'card/'),
            headers=headers,
            json=table_structure
        )
        response.raise_for_status()
        logging.info(f'Created Table Card: {graph_info["name"]}')
    except httpx.HTTPStatusError as http_err:
        logging.error(f'HTTP error occurred: {http_err}')
        raise
    except Exception as err:
        logging.error(f'Other error occurred: {err}')
        raise
    else:
        logging.info('Table Created!')

    return response.json()
