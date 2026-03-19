import os
import psycopg2
import pytest
import time

# We need to import the lambda_handler from the source file
from src.main import lambda_handler

# --- Database Connection Details for the Test Environment ---
# These are now sourced from environment variables, with defaults for local docker-compose setup
DB_CONFIG = {
    "host": os.environ.get("DB_HOST", "localhost"),
    "port": os.environ.get("DB_PORT", "5433"),
    "user": os.environ.get("DB_USER", "testuser"),
    "password": os.environ.get("DB_PASS", "testpassword"),
    "database": os.environ.get("DB_NAME", "testdb"),
}

@pytest.fixture(scope="module")
def db_connection():
    """
    A pytest fixture to manage the database connection for the test module.
    It waits for the DB in Docker to be ready, yields a connection,
    and closes it after all tests in the module are done.
    """
    retries = 5
    while retries > 0:
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            print("Database connection successful!")
            yield conn
            conn.close()
            return
        except psycopg2.OperationalError as e:
            print(f"Database connection failed: {e}. Retrying...")
            retries -= 1
            time.sleep(5)
    pytest.fail("Could not connect to the database after several retries.")


@pytest.fixture(scope="function")
def clean_db_table(db_connection):
    """
    A fixture that runs for each test function. It cleans the raw_vlille table
    before the test runs, ensuring a clean state.
    """
    with db_connection.cursor() as cursor:
        cursor.execute("TRUNCATE TABLE raw_vlille RESTART IDENTITY;")
        db_connection.commit()
    yield # This is where the test runs
    # You could also add cleanup here if needed after the test


def test_lambda_handler_full_integration(clean_db_table, db_connection):
    """
    Full integration test for the lambda_handler.
    - Sets environment variables for the handler.
    - Calls the handler, which performs a real API call and DB insertion.
    - Queries the database to verify that the data was inserted correctly.
    """
    # 1. Set environment variables for the lambda_handler to use
    os.environ["DB_HOST"] = DB_CONFIG["host"]
    os.environ["DB_NAME"] = DB_CONFIG["database"]
    os.environ["DB_USER"] = DB_CONFIG["user"]
    os.environ["DB_PASS"] = DB_CONFIG["password"]
    
    # Override the port for the test environment if your lambda needs it.
    # The default psycopg2 port is 5432, so we need to be explicit.
    # A cleaner way would be to have DB_PORT as an env var in your main code.
    # For now, we will assume the handler can be adapted or this is sufficient.
    # Let's add DB_PORT for robustness.
    os.environ["DB_PORT"] = DB_CONFIG["port"]


    # 2. Call the lambda handler
    result = lambda_handler(event={}, context={})
    assert result["statusCode"] == 200

    # 3. Verify the data in the database
    with db_connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM raw_vlille;")
        count = cursor.fetchone()[0]
        assert count == 1, "There should be exactly one record in the database"

        cursor.execute("SELECT raw_content FROM raw_vlille LIMIT 1;")
        content = cursor.fetchone()[0]
        
        # Check for a key that should always be in the V'Lille API response
        assert "lastUpdatedOther" in content, "The 'lastUpdatedOther' key should be in the JSON response"
        assert "data" in content, "The 'data' key should be in the JSON response"
        assert "stations" in content["data"], "The 'stations' key should be under 'data'"

    # Clean up environment variables
    del os.environ["DB_HOST"]
    del os.environ["DB_NAME"]
    del os.environ["DB_USER"]
    del os.environ["DB_PASS"]
    del os.environ["DB_PORT"]

