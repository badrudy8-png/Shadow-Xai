"""Minimal JSON HTTP API using the Python standard library."""

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from .engine import ChatEngine


class APIHandler(BaseHTTPRequestHandler):
    engine = ChatEngine()

    def do_GET(self) -> None:  # noqa: N802
        if self.path == "/health":
            self._json(200, {"status": "ok", "service": "shadow-xai"})
        else:
            self._json(404, {"error": "not found"})

    def do_POST(self) -> None:  # noqa: N802
        if self.path != "/chat":
            self._json(404, {"error": "not found"}); return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(length))
            response = self.engine.respond(str(payload["message"]))
            self._json(200, {"text": response.text, "provider": response.provider})
        except (KeyError, ValueError, json.JSONDecodeError) as error:
            self._json(400, {"error": str(error)})

    def _json(self, status: int, payload: dict[str, object]) -> None:
        data = json.dumps(payload).encode()
        self.send_response(status); self.send_header("Content-Type", "application/json"); self.send_header("Content-Length", str(len(data))); self.end_headers(); self.wfile.write(data)

    def log_message(self, format: str, *args: object) -> None:
        return


def serve(host: str = "127.0.0.1", port: int = 8080) -> None:
    ThreadingHTTPServer((host, port), APIHandler).serve_forever()
