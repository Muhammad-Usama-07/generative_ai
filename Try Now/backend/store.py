"""
FitAI Backend — store.py
Simple in-memory store for try-on results (keyed by UUID).
Results expire after 1 hour to avoid memory leaks.
"""

import time
import threading
from typing import Optional
from tryon import TryOnResult


class ResultStore:
    """Thread-safe in-memory store with TTL expiry."""

    TTL = 3600  # seconds (1 hour)

    def __init__(self):
        self._data: dict[str, tuple[TryOnResult, float]] = {}
        self._lock = threading.Lock()
        # Start background cleanup thread
        t = threading.Thread(target=self._cleanup_loop, daemon=True)
        t.start()

    def save(self, result_id: str, result: TryOnResult):
        with self._lock:
            self._data[result_id] = (result, time.time())

    def get(self, result_id: str) -> Optional[TryOnResult]:
        with self._lock:
            entry = self._data.get(result_id)
            if not entry:
                return None
            result, ts = entry
            if time.time() - ts > self.TTL:
                del self._data[result_id]
                return None
            return result

    def _cleanup_loop(self):
        while True:
            time.sleep(300)  # clean every 5 minutes
            with self._lock:
                now = time.time()
                expired = [k for k, (_, ts) in self._data.items() if now - ts > self.TTL]
                for k in expired:
                    del self._data[k]