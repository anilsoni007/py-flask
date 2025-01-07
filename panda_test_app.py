import unittest
from panda_app import app, check_memory_usage

class FlaskAppTestCase(unittest.TestCase):
    def setUp(self):
        """
        Set up the Flask app for testing. Initializes the test client.
        """
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_homepage(self):
        """
        Test if the homepage loads successfully and contains key elements.
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'This is my test app using Python Flask!', response.data)
        self.assertIn(b'Enter your name:', response.data)

    def test_health_endpoint(self):
        """
        Test the health endpoint for both healthy and unhealthy memory states.
        """
        memory_usage = check_memory_usage()
        response = self.client.get('/health')
        if memory_usage > 80:
            self.assertEqual(response.status_code, 500)
            self.assertIn(b'Health Status: Unhealthy', response.data)
        else:
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Health Status: Healthy', response.data)

    def test_form_submission(self):
        """
        Test form submission by sending a POST request with a name.
        """
        response = self.client.post('/', data={'name': 'Anil'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'User Table', response.data)
        self.assertIn(b'Anil', response.data)

    def test_node_info(self):
        """
        Test if the app correctly identifies the hosting environment.
        """
        response = self.client.get('/')
        self.assertIn(b'This app is hosted on:', response.data)

    def test_memory_status(self):
        """
        Test if the memory status is displayed on the homepage.
        """
        response = self.client.get('/')
        self.assertIn(b'Memory Status:', response.data)

if __name__ == '__main__':
    unittest.main()
