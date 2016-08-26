import server
import unittest


class IntegrationTestCase(unittest.TestCase):
    """ Integration tests for Fish Finder app. """

    def setUp(self):
        self.client = server.app.test_client()
        # test client makes a "request" to app
        # note: app is NOT actually running
        server.app.config['TESTING'] = True

    def test_index(self):
        result = self.client.get('/')
        self.assertIn('<title>Fish Finder</title>', result.data)

    def test_nearest_stations_calc(self):
        result = self.client.post('/', data={'tbd': 'tbd'})
        self.assertIn('tbd', result.data)
        # result.data is the response string (html)

    def tearDown(self):
        return self

if __name__ == '__main__':
    unittest.main()