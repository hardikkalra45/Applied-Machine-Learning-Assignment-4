import unittest
import subprocess
import os
import requests
import time
import signal

class TestFlask(unittest.TestCase):
    @classmethod
    def setUp(cls):
        
        os.environ['FLASK_APP'] = 'app'
        os.environ['FLASK_RUN_PORT'] = '5000'
        os.environ['FLASK_ENV'] = 'development'
        os.system('docker build -t flask-build .')
        # Start the Flask app in a separate process
        cls.flask_process = subprocess.Popen('docker run -p 5000:5000 --name flask-container flask-build'.split(' '))
        # Wait for the Flask app to start
        time.sleep(3)

    @classmethod
    def tearDown(cls):
        os.system('docker container rm flask-container')
        os.system('docker image rm flask-build --force')

    def test_flask_app(self):
        """Test the Flask endpoint."""
        response = requests.post('http://localhost:5000/score', json={'text': 'hello', 'threshold': 0.5})
        self.assertEqual(response.status_code, 200)
        self.assertIn('prediction', response.json())
        self.assertIn('propensity', response.json())


if __name__ == '__main__':
    unittest.main()
