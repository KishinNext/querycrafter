import pytest

from prompts.info_extractor import InfoExtractor, Schema


class TestSchema:

    def test_schema_initialization(self):
        table1 = "table1"
        table2 = "table2"

        schema = Schema(schemas={
            "schema1": [table1, table2]
        })

        assert schema.schemas == {
            "schema1": [table1, table2]
        }

        assert table1 in schema.schemas["schema1"]
        assert table2 in schema.schemas["schema1"]


class TestExtractor:

    def test_extractor_initialization(self):
        self.extractor = InfoExtractor(query="I want an analysis of the default schema and the employees table.")

        assert self.extractor.query == "I want an analysis of the default schema and the employees table."
        assert self.extractor.model_name == 'gpt-3.5-turbo'
        assert self.extractor.temperature == 0


class TestSpanishExtractor:
    @pytest.mark.parametrize(
        "test_id,query,expected_schema",
        [
            ("case1", "I need to analyze the sales schema and products table", {
                'schemas': {
                    'sales': ['products']
                }
            }),
            ("case2", "give me more information about the schema custom and clients table", {
                'schemas': {
                    'custom': ['clients']
                }
            }),
            ("case3", "analyze the main schema and the orders table", {
                'schemas': {
                    'main': ['orders']
                }
            }),
            ("case4", "I request an analysis of the billing schema and the products table", {
                'schemas': {
                    'billing': ['products']
                }
            }),
            ("case5", "I want to examine the inventory schema and the items table", {
                'schemas': {
                    'inventory': ['items']
                }
            }),
            ("case6", "I need the analysis of the finance schema and the transactions table", {
                'schemas': {
                    'finance': ['transactions']
                }
            }),
            ("case7", "analyze the marketing schema and the clients and campaigns tables", {
                'schemas': {
                    'marketing': ['clients', 'campaigns']
                }
            }),
            ("case8", "I need information about the sales schemas using the clients table, inventory"
                      " with the products table, logistics with the orders table, accounting with the invoices"
                      " table and human_resources with the suppliers table.",
            {
                'schemas': {
                    'sales': ['clients'],
                    'inventory': ['products'],
                    'logistics': ['orders'],
                    'accounting': ['invoices'],
                    'human_resources': ['suppliers']
                }
            }),
            ("case9", "I need information about the sales schemas using the clients table, "
                      "gg, ducky and chick, also the schema inventory with the products table",
            {
                'schemas': {
                    'sales': ['clients', 'gg', 'ducky', 'chick'],
                    'inventory': ['products']
                }
            }),
            ("case10", "I need the documentation of the columns of the clients table from the sales schema", {
                'schemas': {
                    'sales': ['clients']
                }
            })
        ]
    )
    def test_get_result(self, test_id, query, expected_schema):
        self.extractor = InfoExtractor(
            query=query,
            schemas_to_analyze='available_schemas_test'
        )

        result = self.extractor.get_result()
        assert result == expected_schema
