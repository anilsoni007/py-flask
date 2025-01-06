import unittest
from unittest.mock import patch, mock_open
from flask import Flask
from panda_app import app, get_node_info, check_memory_usage

class PandaAppTestCase(unittest.TestCase):

    def setUp(self):
        # Set up a test client for the Flask app
        self.app = app.test_client()
        self.app.testing = True

    @patch("os.path.exists")
    @patch("builtins.open", new_callable=mock_open, read_data="test-pod")
    def test_get_node_info_kubernetes(self, mock_file, mock_exists):
        # Simulate Kubernetes environment
        mock_exists.return_value = True
        result = get_node_info()
        self.assertIn("Pod Name: test-pod", result)

    @patch("requests.get")
    def test_get_node_info_ec2(self, mock_requests):
        # Simulate EC2 environment
        mock_requests.return_value.status_code = 200
        mock_requests.return_value.text = "1.2.3.4"
        result = get_node_info()
        self.assertIn("EC2 Instance IP: 1.2.3.4", result)

    @patch("os.path.exists")
    def test_get_node_info_local(self, mock_exists):
        # Simulate Local Machine
        mock_exists.return_value = False
        result = get_node_info()
        self.assertIn("Local Machine:", result)

    @patch("psutil.virtual_memory")
    def test_check_memory_usage(self, mock_memory):
        # Test memory usage
        mock_memory.return_value.percent = 75
        result = check_memory_usage()
        self.assertEqual(result, 75)

    def test_hello_docker_route(self):
        # Test the root route
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"This is my test app using Python Flask!", response.data)

    @patch("psutil.virtual_memory")
    def test_health_check_healthy(self, mock_memory):
        # Test health check when memory is healthy
        mock_memory.return_value.percent = 50
        response = self.app.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Health Status: Healthy", response.data)

    @patch("psutil.virtual_memory")
    def test_health_check_unhealthy(self, mock_memory):
        # Test health check when memory is unhealthy
        mock_memory.return_value.percent = 85
        response = self.app.get("/health")
        self.assertEqual(response.status_code, 500)
        self.assertIn(b"Health Status: Unhealthy", response.data)

if __name__ == "__main__":
    unittest.main()
