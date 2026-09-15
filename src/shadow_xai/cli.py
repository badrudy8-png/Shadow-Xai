"""Command-line interface for Shadow-Xai."""

import argparse
import sys

from . import __version__
from .api import serve
from .config import Settings
from .engine import ChatEngine


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="shadow-xai", description="Fondasi chatbot AI modular Shadow-Xai.")
    parser.add_argument("--version", action="version", version=__version__)
    subparsers = parser.add_subparsers(dest="command")
    chat = subparsers.add_parser("chat", help="Kirim satu pesan atau jalankan mode interaktif.")
    chat.add_argument("message", nargs="?")
    api = subparsers.add_parser("serve", help="Jalankan HTTP API lokal.")
    api.add_argument("--host", default="127.0.0.1"); api.add_argument("--port", type=int, default=8080)
    subparsers.add_parser("config", help="Tampilkan konfigurasi publik.")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.command == "chat":
        engine = ChatEngine()
        if args.message: print(engine.respond(args.message).text)
        else: engine.run_interactive(sys.stdin, sys.stdout)
    elif args.command == "serve": serve(args.host, args.port)
    elif args.command == "config": print(Settings.from_env().public_dict())
    else: build_parser().print_help()
    return 0
