import pytest
import requests

from chains.metabase import (
    process_metabase_queries,
    insert_card_into_dashboard,
    create_metabase_dashboard,
    run_graph_creator
)
from utils.config_loaders import (
    get_config
)
from utils.config_loaders import (
    get_secrets
)
from utils.database import create_db_session

config = get_config()
secrets = get_secrets(config)
engine = create_db_session(secrets['database']['url'])


@pytest.mark.skipif(True, reason='should be ran only manually')  # comment this line if you want to run this test
def test_process_metabase_queries():
    metabase_queries = [
        {
            "table_name": "customer",
            "schema_name": "sales",
            "title": "[TEST] Total Sales",
            "query": "SELECT SUM(salesorderheader.totaldue) AS total_sales FROM sales.salesorderheader",
            "classify": "Numeric Indicator",
            "description": "This query calculates the total sales made by the company."
        },
        {
            "table_name": "customer",
            "schema_name": "sales",
            "title": "[TEST] Sales by Store",
            "query": "SELECT store.name, SUM(salesorderheader.totaldue) AS total_sales FROM sales.salesorderheader JOIN sales.store ON salesorderheader.storeid = store.businessentityid GROUP BY store.name",
            "classify": "Bar Chart",
            "description": "This query groups sales by store, allowing for easy comparison between different stores."
        },
        {
            "table_name": "customer",
            "schema_name": "sales",
            "title": "[TEST] Sales by Territory",
            "query": "SELECT salesterritory.name, SUM(salesorderheader.totaldue) AS total_sales FROM sales.salesorderheader JOIN sales.salesterritory ON salesorderheader.territoryid = salesterritory.territoryid GROUP BY salesterritory.name",
            "classify": "Bar Chart",
            "description": "This query groups sales by territory, allowing for easy comparison between different territories."
        },
        {
            "table_name": "customer",
            "schema_name": "sales",
            "title": "[TEST] Sales by Month",
            "query": "SELECT DATE_TRUNC('month', salesorderheader.orderdate) AS month, SUM(salesorderheader.totaldue) AS total_sales FROM sales.salesorderheader GROUP BY month ORDER BY month",
            "classify": "Line Chart",
            "description": "This query groups sales by month, allowing for easy visualization of sales trends over time."
        },
        {
            "table_name": "customer",
            "schema_name": "sales",
            "title": "[TEST] Sales by Customer",
            "query": "SELECT CONCAT(person.firstname, ' ', person.lastname) AS customer_name, SUM(salesorderheader.totaldue) AS total_sales FROM sales.salesorderheader JOIN sales.customer ON salesorderheader.customerid = customer.customerid JOIN person.person ON customer.personid = person.businessentityid GROUP BY customer_name ORDER BY total_sales DESC",
            "classify": "Table",
            "description": "This query groups sales by customer, allowing for easy identification of top customers."
        }
    ]

    collection_info = {
        "id": config['secrets']['metabase']['collection_parent']
    }

    responses = process_metabase_queries(metabase_queries, collection_info)

    dashboard_info = create_metabase_dashboard(
        collection_id=collection_info['id'],
        dashboard_name="[TEST] Dashboard for testing",
        metabase_url=config['secrets']['metabase']['metabase_url'],
        headers={
            "Content-Type": config['secrets']['metabase']['content_type'],
            "X-Metabase-Session": config['secrets']['metabase']['metabase_session']
        }
    )

    try:
        insert_card_into_dashboard(responses, dashboard_info['id'])
    except requests.exceptions.RequestException:
        pytest.fail("Failed to insert cards into dashboard.")

    assert len(responses) == 5
    assert isinstance(responses, list)
    assert responses[0]["name"] == "[TEST] Total Sales"
    assert responses[1]["name"] == "[TEST] Sales by Store"
    assert responses[2]["name"] == "[TEST] Sales by Territory"
    assert responses[3]["name"] == "[TEST] Sales by Month"
    assert isinstance(dashboard_info, dict)
    assert dashboard_info["name"] == "[TEST] Dashboard for testing"


@pytest.mark.skipif(True, reason='should be ran only manually')  # comment this line if you want to run this test
class TestQueries:
    def test_run_graph_creator(self):
        result = run_graph_creator("""
I want a dashboard that shows me the total profit per month, number of sales per month, sales by status, number of sales by shipping date, sales by territory, and sales by type of credit card.
You can use the tables salesorderheader, salesorderdetail, specialofferproduct, store, creditcard, customer, and salesterritory from the sales schema.
        """, engine)
        assert 'Failed to create' not in result
