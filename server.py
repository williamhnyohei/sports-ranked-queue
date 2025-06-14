"""Simple HTTP server exposing the queue manager API."""

import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from sports_queue import Player, Group, QueueManager

queue_manager = QueueManager()

class RequestHandler(BaseHTTPRequestHandler):
    """Handle API requests for adding groups and matching."""
    def _send_json(self, data: dict, status: int = 200) -> None:
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def do_POST(self) -> None:
        length = int(self.headers.get('Content-Length', 0))
        raw = self.rfile.read(length)
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError:
            self._send_json({'error': 'invalid json'}, status=400)
            return

        if self.path == '/add_group':
            try:
                sport = payload['sport']
                players = [
                    Player(p['id'], p.get('mmr', 1000), p.get('is_dummy', False))
                    for p in payload['players']
                ]
            except (KeyError, TypeError):
                self._send_json({'error': 'invalid payload'}, status=400)
                return
            queue_manager.add_group(sport, Group(players))
            self._send_json({'status': 'ok'})
        elif self.path == '/match':
            try:
                sport = payload['sport']
            except KeyError:
                self._send_json({'error': 'invalid payload'}, status=400)
                return
            ranked = payload.get('ranked', True)
            match = queue_manager.match_groups(sport, ranked=ranked)
            if match:
                resp = {
                    'match': [
                        [
                            {
                                'id': p.player_id,
                                'mmr': p.mmr,
                                'is_dummy': p.is_dummy,
                            }
                            for p in g.players
                        ]
                        for g in match
                    ]
                }
            else:
                resp = {'match': None}
            self._send_json(resp)
        else:
            self._send_json({'error': 'not found'}, status=404)

    def log_message(self, format: str, *args: object) -> None:
        return  # silence logging

def create_server(host: str = 'localhost', port: int = 8000) -> HTTPServer:
    """Create an HTTP server instance bound to ``host`` and ``port``."""
    return HTTPServer((host, port), RequestHandler)

def run(host: str = 'localhost', port: int = 8000) -> None:
    """Run the HTTP API server indefinitely."""
    server = create_server(host, port)
    print(f'Server running at http://{host}:{server.server_port}')
    server.serve_forever()

if __name__ == '__main__':
    run()
