import json
import urllib.request
import psycopg2
from psycopg2.extras import Json
import os

# Database credentials from environment variables
DB_HOST = os.environ.get("DB_HOST")
DB_NAME = os.environ.get("DB_NAME", "postgres")
DB_USER = os.environ.get("DB_USER", "postgres")
DB_PASS = os.environ.get("DB_PASS")
DB_PORT = os.environ.get("DB_PORT") # Added for test environment flexibility

# V'lille API Endpoint (GBFS Station Status)
API_URL = "https://media.ilevia.fr/opendata/station_status.json"


def fetch_vlille_data(url):
    """
    Fetches data from the V'lille API.
    """
    print(f"Requesting data from {url}...")
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        },
    )
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode())


def insert_data(data, db_config):
    """
    Inserts data into the PostgreSQL database.
    """
    conn = None
    try:
        # Filter out None values from db_config, especially for the port
        clean_db_config = {k: v for k, v in db_config.items() if v is not None}
        print(f"Connecting to database at {clean_db_config.get('host')}:{clean_db_config.get('port')}...")
        conn = psycopg2.connect(**clean_db_config, connect_timeout=5)
        cur = conn.cursor()
        insert_query = "INSERT INTO raw_vlille (raw_content) VALUES (%s);"
        cur.execute(insert_query, [Json(data)])
        conn.commit()
        cur.close()
        print("Success: Data successfully ingested into PostgreSQL.")
    finally:
        if conn:
            conn.close()


def lambda_handler(event, context):
    """
    Main Lambda function to fetch data from V'lille API and store it in PostgreSQL.
    """
    try:
        data = fetch_vlille_data(API_URL)
        db_config = {
            "host": DB_HOST,
            "database": DB_NAME,
            "user": DB_USER,
            "password": DB_PASS,
            "port": DB_PORT, # Added port
        }
        insert_data(data, db_config)

        return {"statusCode": 200, "body": json.dumps("Ingestion complete")}

    except Exception as e:
        print(f"Error during ingestion: {str(e)}")
        raise e