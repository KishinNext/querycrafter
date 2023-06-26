from prompts.metabase_graphs import MetabaseGraph


def test_numeric_indicator():
    metabase_creator = MetabaseGraph()
    card_info = {
        "table_name": "customer",
        "schema_name": "sales",
        "title": "Total Sales",
        "query": "SELECT SUM(salesorderheader.totaldue) AS total_sales FROM sales.salesorderheader",
        "classify": "Numeric Indicator",
        "description": "This query calculates the total sales made by the company"
    }
    expected_card_info = {
        "name": "Total Sales",
        "dataset_query_native_query": "SELECT SUM(salesorderheader.totaldue) AS total_sales FROM sales.salesorderheader",
        "description": "This query calculates the total sales made by the company",
        "visualization_settings_column_settings_number_style": "currency",
        "visualization_settings_column_settings_decimals": 2,
        "visualization_settings_column_settings_scale": 1,
        "visualization_settings_column_settings_prefix": "",
        "visualization_settings_column_settings_suffix": "",
    }

    result = metabase_creator.numeric_indicator(card_info=card_info)
    assert isinstance(result, dict)
    assert result['name'] == expected_card_info["name"]
    assert result['description'] == expected_card_info["description"]
    assert result['dataset_query_native_query'] == expected_card_info["dataset_query_native_query"]
    assert result['visualization_settings_column_settings_number_style'] == expected_card_info[
        'visualization_settings_column_settings_number_style']
    assert result['visualization_settings_column_settings_decimals'] == expected_card_info[
        'visualization_settings_column_settings_decimals']
    assert result['visualization_settings_column_settings_scale'] == expected_card_info[
        'visualization_settings_column_settings_scale']


def test_bar_chart():
    metabase_creator = MetabaseGraph()
    card_info = {
        "table_name": "customer",
        "schema_name": "sales",
        "title": "Sales by Store",
        "query": "SELECT store.name, SUM(salesorderheader.totaldue) AS total_sales FROM sales.salesorderheader JOIN sales.store ON salesorderheader.storeid = store.businessentityid GROUP BY store.name",
        "classify": "Bar Chart",
        "description": "This query groups sales by store, allowing for easy comparison between different stores."
    }
    expected_card_info = {
        "name": "Sales by Store",
        "dataset_query_native_query": "SELECT store.name, SUM(salesorderheader.totaldue) AS total_sales FROM sales.salesorderheader JOIN sales.store ON salesorderheader.storeid = store.businessentityid GROUP BY store.name",
        "description": "This query groups sales by store, allowing for easy comparison between different stores.",
        "visualization_settings_graph_dimensions": ["store.name"],
        "visualization_settings_graph_metrics": ["total_sales"]
    }

    result = metabase_creator.bar_chart(card_info=card_info)
    assert isinstance(result, dict)
    assert result['name'] == expected_card_info["name"]
    assert result['description'] == expected_card_info["description"]
    assert result['dataset_query_native_query'] == expected_card_info["dataset_query_native_query"]
    assert result['visualization_settings_graph_dimensions'] == expected_card_info[
        'visualization_settings_graph_dimensions']
    assert result['visualization_settings_graph_metrics'] == expected_card_info['visualization_settings_graph_metrics']


def test_line_chart():
    metabase_creator = MetabaseGraph()
    card_info = {
        "table_name": "customer",
        "schema_name": "sales",
        "title": "Sales by Month",
        "query": "SELECT DATE_TRUNC('month', salesorderheader.orderdate) AS month, SUM(salesorderheader.totaldue) AS total_sales FROM sales.salesorderheader GROUP BY month ORDER BY month",
        "classify": "Line Chart",
        "description": "This query groups sales by month, allowing for easy visualization of sales trends over time."
    }

    expected_card_info = {
        "name": "Sales by Month",
        "dataset_query_native_query": "SELECT DATE_TRUNC('month', salesorderheader.orderdate) AS month, SUM(salesorderheader.totaldue) AS total_sales FROM sales.salesorderheader GROUP BY month ORDER BY month",
        "description": "This query groups sales by month, allowing for easy visualization of sales trends over time.",
        "visualization_settings_graph_show_trendline": True,
        "visualization_settings_graph_show_values": True,
        "visualization_settings_graph_label_value_frequency": "fit",
        "visualization_settings_graph_dimensions": ["month"],
        "visualization_settings_graph_metrics": ["total_sales"],
    }

    result = metabase_creator.line_chart(card_info=card_info)

    assert isinstance(result, dict)
    assert result['name'] == expected_card_info["name"]
    assert result['description'] == expected_card_info["description"]
    assert result['dataset_query_native_query'] == expected_card_info["dataset_query_native_query"]
    assert result['visualization_settings_graph_show_trendline'] == expected_card_info[
        'visualization_settings_graph_show_trendline']
    assert result['visualization_settings_graph_show_values'] == expected_card_info[
        'visualization_settings_graph_show_values']
    assert result['visualization_settings_graph_label_value_frequency'] == expected_card_info[
        'visualization_settings_graph_label_value_frequency']
    assert result['visualization_settings_graph_dimensions'] == expected_card_info[
        'visualization_settings_graph_dimensions']
    assert result['visualization_settings_graph_metrics'] == expected_card_info['visualization_settings_graph_metrics']


def test_table():
    metabase_creator = MetabaseGraph()

    card_info = {
        "table_name": "customer",
        "schema_name": "sales",
        "title": "Sales by Customer",
        "query": "SELECT CONCAT(person.firstname, ' ', person.lastname) AS customer_name, SUM(salesorderheader.totaldue) AS total_sales FROM sales.salesorderheader JOIN sales.customer ON salesorderheader.customerid = customer.customerid JOIN person.person ON customer.personid = person.businessentityid GROUP BY customer_name ORDER BY total_sales DESC",
        "classify": "Table",
        "description": "This query groups sales by customer, allowing for easy identification of top customers."
    }

    expected_card_info = {
        "name": "Sales by Customer",
        "dataset_query_native_query": "SELECT CONCAT(person.firstname, ' ', person.lastname) AS customer_name, SUM(salesorderheader.totaldue) AS total_sales FROM sales.salesorderheader JOIN sales.customer ON salesorderheader.customerid = customer.customerid JOIN person.person ON customer.personid = person.businessentityid GROUP BY customer_name ORDER BY total_sales DESC",
        "description": "This query groups sales by customer, allowing for easy identification of top customers.",
        "visualization_settings_column_formatting_columns": ["total_sales"],
        "visualization_settings_column_formatting_colors": ["white", "#509EE3"],
        "visualization_settings_column_formatting_style": {
            "total_sales": {
                "visualization_settings_column_settings_number_style": "currency",
                "visualization_settings_column_settings_decimals": 2,
                "visualization_settings_column_settings_scale": 1,
                "visualization_settings_column_settings_prefix": "",
                "visualization_settings_column_settings_suffix": "",
            }
        }
    }

    result = metabase_creator.table(card_info=card_info)
    assert isinstance(result, dict)
    assert result['name'] == expected_card_info["name"]
    assert result['description'] == expected_card_info["description"]
    assert result['dataset_query_native_query'] == expected_card_info["dataset_query_native_query"]
    assert result['visualization_settings_column_formatting_columns'] == expected_card_info[
        'visualization_settings_column_formatting_columns']
    assert result['visualization_settings_column_formatting_colors'] == expected_card_info[
        'visualization_settings_column_formatting_colors']
    assert result['visualization_settings_column_formatting_style'] == expected_card_info[
        'visualization_settings_column_formatting_style']
