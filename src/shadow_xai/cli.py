"""Command-line interface for Shadow-Xai."""

import argparse
import sys

from . import __version__
from .engine import ChatEngine


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="shadow-xai",
        description="Fondasi chatbot AI modular Shadow-Xai.",
    )
    parser.add_argument("--version", action="version", version=__version__)
    subparsers = parser.add_subparsers(dest="command")

    chat = subparsers.add_parser("chat", help="Jalankan chat sekali atau mode interaktif.")
    chat.add_argument("message", nargs="?", help="Pesan opsional yang akan diproses.")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.command == "chat":
        engine = ChatEngine()
        if args.message:
            print(engine.respond(args.message).text)
        else:
            engine.run_interactive(sys.stdin, sys.stdout)
        return 0
    build_parser().print_help()
    return 0
