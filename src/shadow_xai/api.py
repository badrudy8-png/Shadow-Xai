"""JSON HTTP API wired to the shared Shadow-Xai engine."""

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from .engine import ChatEngine


class APIHandler(BaseHTTPRequestHandler):
    engine = ChatEngine()

    def do_GET(self) -> None:  # noqa: N802
        if self.path == "/health":
            self._json(200, {"status": "ok", "service": "shadow-xai", "provider": self.engine.provider})
        elif self.path == "/config":
            self._json(200, self.engine.settings.public_dict())
        else:
            self._json(404, {"error": "not found"})

    def do_POST(self) -> None:  # noqa: N802
        if self.path != "/chat":
            self._json(404, {"error": "not found"})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length <= 0:
                raise ValueError("request body is empty")
            payload = json.loads(self.rfile.read(length))
            message = payload.get("message")
            if not isinstance(message, str):
                raise ValueError("message must be a string")
            response = self.engine.respond(message)
            self._json(200, {
                "text": response.text,
                "provider": response.provider,
                "model": response.model,
                "route": response.route,
                "agent_completed": response.agent_completed,
                "used_fallback": response.used_fallback,
                "usage": response.usage,
            })
        except (ValueError, json.JSONDecodeError) as error:
            self._json(400, {"error": str(error)})
        except Exception as error:  # keep the HTTP boundary from crashing the server
            self._json(500, {"error": "internal server error", "detail": str(error)})

    def _json(self, status: int, payload: dict[str, object]) -> None:
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, format: str, *args: object) -> None:
        return


def serve(host: str = "127.0.0.1", port: int = 8080) -> None:
    ThreadingHTTPServer((host, port), APIHandler).serve_forever()
