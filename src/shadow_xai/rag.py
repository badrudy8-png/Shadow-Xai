"""Dependency-free lexical knowledge base with source tracking."""

from dataclasses import dataclass
import re


@dataclass(frozen=True)
class DocumentChunk:
    source: str
    text: str
    index: int


class KnowledgeBase:
    def __init__(self, chunk_size: int = 120) -> None:
        self.chunk_size = chunk_size
        self.chunks: list[DocumentChunk] = []

    def ingest(self, text: str, source: str = "inline") -> int:
        words = text.split()
        added = 0
        for start in range(0, len(words), self.chunk_size):
            part = " ".join(words[start:start + self.chunk_size])
            if part:
                self.chunks.append(DocumentChunk(source, part, added)); added += 1
        return added

    def retrieve(self, query: str, limit: int = 3) -> list[DocumentChunk]:
        terms = set(re.findall(r"\w+", query.lower()))
        scored = [(len(terms & set(re.findall(r"\w+", c.text.lower()))), c) for c in self.chunks]
        return [chunk for score, chunk in sorted(scored, key=lambda x: x[0], reverse=True)[:limit] if score]

    def context(self, query: str, limit: int = 3) -> str:
        return "\n".join(f"[{x.source}#{x.index}] {x.text}" for x in self.retrieve(query, limit))
