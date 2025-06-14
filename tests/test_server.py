import unittest
import threading
import json
from http.client import HTTPConnection
from server import create_server, queue_manager

class ServerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = create_server(port=0)
        cls.port = cls.server.server_port
        cls.thread = threading.Thread(target=cls.server.serve_forever)
        cls.thread.daemon = True
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.thread.join()

    def request(self, path, body):
        conn = HTTPConnection('localhost', self.port)
        conn.request('POST', path, body=json.dumps(body), headers={'Content-Type': 'application/json'})
        resp = conn.getresponse()
        data = resp.read()
        conn.close()
        return resp.status, json.loads(data.decode())

    def test_add_and_match(self):
        players = [{'id': 'p1', 'mmr': 1000}, {'id': 'p2', 'mmr': 1000}]
        for _ in range(5):
            status, _ = self.request('/add_group', {'sport': 'futebol', 'players': players})
            self.assertEqual(status, 200)
        status, data = self.request('/match', {'sport': 'futebol', 'ranked': True})
        self.assertEqual(status, 200)
        self.assertIsNotNone(data['match'])
        self.assertEqual(len(data['match']), 5)
        self.assertEqual(sum(len(g) for g in data['match']), 10)

    def test_unranked_endpoint(self):
        g1 = [{'id': 'p1', 'mmr': 1000}] * 5
        g2 = [{'id': 'p2', 'mmr': 1500}] * 5
        self.request('/add_group', {'sport': 'futebol', 'players': g1})
        self.request('/add_group', {'sport': 'futebol', 'players': g2})
        status, data = self.request('/match', {'sport': 'futebol', 'ranked': False})
        self.assertEqual(status, 200)
        self.assertIsNotNone(data['match'])
        self.assertEqual(sum(len(g) for g in data['match']), 10)

    def test_add_dummy_player(self):
        group = [
            {'id': 'p1', 'mmr': 1000},
            {'id': 'p2', 'mmr': 1000},
            {'id': 'dummy1', 'mmr': 1000, 'is_dummy': True},
            {'id': 'dummy2', 'mmr': 1000, 'is_dummy': True},
            {'id': 'dummy3', 'mmr': 1000, 'is_dummy': True},
        ]
        self.request('/add_group', {'sport': 'futebol', 'players': group})
        self.request('/add_group', {'sport': 'futebol', 'players': group})
        status, data = self.request('/match', {'sport': 'futebol', 'ranked': True})
        self.assertEqual(status, 200)
        self.assertIsNotNone(data['match'])
        self.assertEqual(sum(len(g) for g in data['match']), 10)

if __name__ == '__main__':
    unittest.main()
