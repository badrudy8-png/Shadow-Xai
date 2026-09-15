"""Safe advanced-AI extension points with deterministic local implementations."""

from concurrent.futures import ThreadPoolExecutor, Future
from dataclasses import dataclass
import hashlib
import re
import threading
import uuid
from typing import Callable, Iterable


class ConversationSummarizer:
    def summarize(self, messages: Iterable[str], max_chars: int = 500) -> str:
        text = " ".join(x.strip() for x in messages if x.strip())
        return text if len(text) <= max_chars else text[: max_chars - 3].rsplit(" ", 1)[0] + "..."


@dataclass(frozen=True)
class FactCheck:
    claim: str
    supported: bool
    sources: tuple[str, ...]
    note: str


class FactChecker:
    def check(self, claim: str, evidence: Iterable[tuple[str, str]]) -> FactCheck:
        terms = set(re.findall(r"\w+", claim.lower()))
        matches = tuple(source for source, text in evidence if terms and len(terms & set(re.findall(r"\w+", text.lower()))) / len(terms) >= 0.5)
        return FactCheck(claim, bool(matches), matches, "lexical evidence check; use a trusted verifier for production")


class IntelligentRouter:
    def __init__(self, routes: dict[str, Callable[[str], str]]) -> None:
        self.routes = routes

    def select(self, prompt: str) -> str:
        lowered = prompt.lower()
        if any(word in lowered for word in ("calculate", "hitung", "math")) and "calculator" in self.routes:
            return "calculator"
        if any(word in lowered for word in ("research", "source", "cari")) and "research" in self.routes:
            return "research"
        return "default" if "default" in self.routes else next(iter(self.routes))

    def dispatch(self, prompt: str) -> str:
        route = self.select(prompt)
        return self.routes[route](prompt)


class ParallelToolExecutor:
    def __init__(self, max_workers: int = 4) -> None:
        self.pool = ThreadPoolExecutor(max_workers=max_workers)

    def run(self, calls: Iterable[tuple[Callable[..., str], tuple, dict]]) -> list[str]:
        futures = [self.pool.submit(fn, *args, **kwargs) for fn, args, kwargs in calls]
        return [str(future.result()) for future in futures]

    def close(self) -> None:
        self.pool.shutdown(wait=True)


@dataclass(frozen=True)
class Job:
    id: str
    status: str
    result: str = ""
    error: str = ""


class BackgroundJobRegistry:
    """In-process background jobs; use a durable queue for production."""

    def __init__(self) -> None:
        self._jobs: dict[str, Job] = {}
        self._lock = threading.Lock()
        self._pool = ThreadPoolExecutor(max_workers=2)

    def submit(self, fn: Callable[[], str]) -> str:
        job_id = uuid.uuid4().hex
        with self._lock: self._jobs[job_id] = Job(job_id, "queued")
        self._pool.submit(self._run, job_id, fn)
        return job_id

    def _run(self, job_id: str, fn: Callable[[], str]) -> None:
        with self._lock: self._jobs[job_id] = Job(job_id, "running")
        try:
            result = str(fn())
            with self._lock: self._jobs[job_id] = Job(job_id, "completed", result=result)
        except Exception as error:
            with self._lock: self._jobs[job_id] = Job(job_id, "failed", error=str(error))

    def get(self, job_id: str) -> Job:
        with self._lock: return self._jobs.get(job_id, Job(job_id, "not_found"))


class KnowledgeGraph:
    def __init__(self) -> None:
        self.edges: set[tuple[str, str, str]] = set()

    def add(self, subject: str, relation: str, object_: str) -> None:
        self.edges.add((subject, relation, object_))

    def neighbors(self, subject: str) -> list[tuple[str, str]]:
        return [(relation, object_) for source, relation, object_ in self.edges if source == subject]


@dataclass(frozen=True)
class MediaArtifact:
    kind: str
    path: str
    sha256: str


class MultimodalGateway:
    """Metadata-only boundary for image/audio/file/codebase adapters.

    It validates and fingerprints local files; actual decoding is delegated to
    opt-in adapters so secrets and large payloads never enter the core engine.
    """

    def inspect_file(self, path: str, kind: str = "file", max_bytes: int = 10_000_000) -> MediaArtifact:
        with open(path, "rb") as stream:
            data = stream.read(max_bytes + 1)
        if len(data) > max_bytes:
            raise ValueError("file exceeds configured size limit")
        return MediaArtifact(kind, path, hashlib.sha256(data).hexdigest())

    def image_understanding(self, path: str) -> MediaArtifact: return self.inspect_file(path, "image")
    def audio_input(self, path: str) -> MediaArtifact: return self.inspect_file(path, "audio")
    def voice_output(self, path: str) -> MediaArtifact: return self.inspect_file(path, "voice")
    def codebase_understanding(self, path: str) -> MediaArtifact: return self.inspect_file(path, "codebase")
