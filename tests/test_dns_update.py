
import unittest
from unittest.mock import patch, MagicMock
import dns_update
import os

class TestDnsUpdate(unittest.TestCase):

    @patch('dns_update.requests.post')
    def test_edit_dns_record_success(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'status': 'SUCCESS'}
        mock_post.return_value = mock_response

        response = dns_update.edit_dns_record('api_key', 'secret_key', 'example.com', '12345', 'A', 'subdomain', '127.0.0.1', 300)
        self.assertEqual(response, {'status': 'SUCCESS'})

    @patch('dns_update.requests.post')
    def test_edit_dns_record_failure(self, mock_post):
        mock_post.side_effect = dns_update.requests.exceptions.RequestException("Failed to edit DNS record")
        with self.assertRaises(SystemExit):
            dns_update.edit_dns_record('api_key', 'secret_key', 'example.com', '12345', 'A', 'subdomain', '127.0.0.1', 300)

    @patch('dns_update.requests.post')
    def test_get_dns_record_success(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'status': 'SUCCESS', 'records': [{'id': '12345', 'content': '127.0.0.1'}]}
        mock_post.return_value = mock_response

        response = dns_update.get_dns_record('api_key', 'secret_key', 'example.com', 'A', 'subdomain')
        self.assertEqual(response, {'status': 'SUCCESS', 'records': [{'id': '12345', 'content': '127.0.0.1'}]})

    @patch('dns_update.requests.post')
    def test_get_dns_record_failure(self, mock_post):
        mock_post.side_effect = dns_update.requests.exceptions.RequestException("Failed to get DNS record")
        with self.assertRaises(SystemExit):
            dns_update.get_dns_record('api_key', 'secret_key', 'example.com', 'A', 'subdomain')

    @patch('dns_update.requests.post')
    def test_create_dns_record_success(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'status': 'SUCCESS'}
        mock_post.return_value = mock_response

        response = dns_update.create_dns_record('api_key', 'secret_key', 'example.com', 'A', 'subdomain', '127.0.0.1', 300)
        self.assertEqual(response, {'status': 'SUCCESS'})

    @patch('dns_update.requests.post')
    def test_create_dns_record_failure(self, mock_post):
        mock_post.side_effect = dns_update.requests.exceptions.RequestException("Failed to create DNS record")
        with self.assertRaises(SystemExit):
            dns_update.create_dns_record('api_key', 'secret_key', 'example.com', 'A', 'subdomain', '127.0.0.1', 300)

    @patch('dns_update.requests.get')
    def test_get_public_ip_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '192.0.2.1'
        mock_get.return_value = mock_response

        ip = dns_update.get_public_ip()
        self.assertEqual(ip, '192.0.2.1')

    @patch('dns_update.requests.get')
    def test_get_public_ip_failure(self, mock_get):
        mock_get.side_effect = dns_update.requests.exceptions.RequestException("Failed to get public IP")
        with self.assertRaises(SystemExit):
            dns_update.get_public_ip()

if __name__ == '__main__':
    unittest.main()
