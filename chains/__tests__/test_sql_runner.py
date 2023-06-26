from chains.sql_runner import sql_runner
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


# TODO: Modify the test to use your own database
def test_general_runner():

    result = sql_runner('I want the total number of records of the table store of the sales schema', engine, 10)

    assert result['sql_code'] is not None
    assert isinstance(result, dict)
    assert result['data'] is not None
