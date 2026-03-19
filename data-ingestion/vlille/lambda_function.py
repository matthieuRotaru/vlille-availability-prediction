import json
import urllib.request
import psycopg2
from psycopg2.extras import Json
import os

# Database credentials from environment variables
DB_HOST = os.environ.get('DB_HOST')
DB_NAME = os.environ.get('DB_NAME', 'postgres')
DB_USER = os.environ.get('DB_USER', 'postgres')
DB_PASS = os.environ.get('DB_PASS')

# V'lille API Endpoint (GBFS Station Status)
API_URL = "https://media.ilevia.fr/opendata/station_status.json"

def lambda_handler(event, context):
    """
    Main Lambda function to fetch data from V'lille API and store it in PostgreSQL.
    """
    conn = None
    try:
        # 1. Fetching data from the API with a User-Agent to avoid 403 Forbidden
        print(f"Requesting data from {API_URL}...")
        
        # We simulate a real browser request
        req = urllib.request.Request(
            API_URL, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
        )
        
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
        
        # 2. Connecting to the RDS PostgreSQL instance
        print(f"Connecting to database at {DB_HOST}...")
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            connect_timeout=5
        )
        cur = conn.cursor()
        
        # 3. Inserting the raw JSON data into the 'raw_vlille' table
        insert_query = "INSERT INTO raw_vlille (raw_content) VALUES (%s);"
        cur.execute(insert_query, [Json(data)])
        
        conn.commit()
        cur.close()
        print("Success: Data successfully ingested into PostgreSQL.")
        
        return {
            'statusCode': 200,
            'body': json.dumps('Ingestion complete')
        }

    except Exception as e:
        print(f"Error during ingestion: {str(e)}")
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()