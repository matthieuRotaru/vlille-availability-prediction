import json
import unittest
from unittest.mock import patch, MagicMock
from src.main import fetch_vlille_data, insert_data, lambda_handler

class TestVlilleLambda(unittest.TestCase):

    @patch('src.main.urllib.request.urlopen')
    def test_fetch_vlille_data(self, mock_urlopen):
        # Mock the API response
        mock_response = MagicMock()
        mock_response.read.return_value.decode.return_value = json.dumps({"key": "value"})
        mock_urlopen.return_value.__enter__.return_value = mock_response

        # Call the function
        data = fetch_vlille_data("http://fakeurl.com")

        # Assertions
        self.assertEqual(data, {"key": "value"})

    @patch('src.main.psycopg2.connect')
    def test_insert_data(self, mock_connect):
        # Mock the database connection and cursor
        mock_conn = MagicMock()
        mock_cur = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cur

        # Call the function
        db_config = {"host": "fakehost", "database": "fakedb", "user": "fakeuser", "password": "fakepass"}
        insert_data({"key": "value"}, db_config)

        # Assertions
        mock_connect.assert_called_once_with(host="fakehost", database="fakedb", user="fakeuser", password="fakepass", connect_timeout=5)
        mock_conn.cursor.assert_called_once()
        mock_cur.execute.assert_called_once()
        mock_conn.commit.assert_called_once()
        mock_cur.close.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch('src.main.fetch_vlille_data')
    @patch('src.main.insert_data')
    def test_lambda_handler(self, mock_insert_data, mock_fetch_vlille_data):
        # Mock the return values of the other functions
        mock_fetch_vlille_data.return_value = {"key": "value"}

        # Call the handler
        response = lambda_handler(None, None)

        # Assertions
        mock_fetch_vlille_data.assert_called_once()
        mock_insert_data.assert_called_once_with({"key": "value"}, unittest.mock.ANY)
        self.assertEqual(response['statusCode'], 200)
        self.assertEqual(response['body'], json.dumps("Ingestion complete"))

    @patch('src.main.fetch_vlille_data')
    def test_lambda_handler_exception(self, mock_fetch_vlille_data):
        # Mock an exception
        mock_fetch_vlille_data.side_effect = Exception("Test Exception")

        # Call the handler and assert it raises an exception
        with self.assertRaises(Exception) as context:
            lambda_handler(None, None)
        
        self.assertTrue('Test Exception' in str(context.exception))

if __name__ == '__main__':
    unittest.main()
