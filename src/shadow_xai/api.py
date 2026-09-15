"""HTTP API and static web UI for Shadow-Xai."""

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from .engine import ChatEngine

WEB_ROOT = Path(__file__).resolve().parents[2] / "web"


class APIHandler(BaseHTTPRequestHandler):
    engine = ChatEngine()

    def do_GET(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        if path == "/health":
            self._json(200, {"status": "ok", "service": "shadow-xai", "provider": self.engine.provider})
        elif path == "/config":
            self._json(200, self.engine.settings.public_dict())
        elif path == "/" or path in {"/index.html", "/app.js", "/style.css"}:
            self._serve_web(path)
        else:
            self._json(404, {"error": "not found"})

    def do_POST(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        if path not in {"/chat", "/api/chat"}:
            self._json(404, {"error": "not found"})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length <= 0:
                raise ValueError("request body is empty")
            payload = json.loads(self.rfile.read(length))
            message = payload.get("message")
            if not isinstance(message, str) or not message.strip():
                raise ValueError("message must be a non-empty string")
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

    def _serve_web(self, path: str) -> None:
        filename = "index.html" if path == "/" else path.lstrip("/")
        file_path = (WEB_ROOT / filename).resolve()
        if WEB_ROOT not in file_path.parents or not file_path.is_file():
            self._json(404, {"error": "web asset not found"})
            return
        content_types = {
            ".html": "text/html; charset=utf-8",
            ".js": "application/javascript; charset=utf-8",
            ".css": "text/css; charset=utf-8",
        }
        data = file_path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", content_types.get(file_path.suffix, "application/octet-stream"))
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        self.wfile.write(data)

    def _json(self, status: int, payload: dict[str, object]) -> None:
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, format: str, *args: object) -> None:
        return


def serve(host: str = "127.0.0.1", port: int = 8080) -> None:
    ThreadingHTTPServer((host, port), APIHandler).serve_forever()
