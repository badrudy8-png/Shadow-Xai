"""Command-line interface for Shadow-Xai."""

import argparse

from . import __version__
from .engine import ChatEngine


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="shadow-xai",
        description="Fondasi chatbot AI modular Shadow-Xai.",
    )
    parser.add_argument("--version", action="version", version=__version__)
    subparsers = parser.add_subparsers(dest="command")

    chat = subparsers.add_parser("chat", help="Kirim satu pesan ke engine lokal.")
    chat.add_argument("message", help="Pesan yang akan diproses.")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.command == "chat":
        print(ChatEngine().respond(args.message).text)
        return 0
    build_parser().print_help()
    return 0
