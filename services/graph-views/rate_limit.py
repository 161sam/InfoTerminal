import re
import time
from typing import Tuple


def parse_rate(val: str) -> Tuple[int, float]:
    # "20/minute" -> (capacity=20, refill_per_sec=20/60)
    m = re.match(r"^\s*(\d+)\s*/\s*(second|minute|hour)\s*$", val or "", re.I)
    if not m:
        return (0, 0.0)
    n = int(m.group(1))
    unit = m.group(2).lower()
    denom = 1 if unit == "second" else (60 if unit == "minute" else 3600)
    return (n, n / denom)


class TokenBucket:
    def __init__(self, capacity: int, refill_per_sec: float):
        self.capacity = capacity
        self.refill_per_sec = refill_per_sec
        self.tokens = capacity
        self.ts = time.monotonic()

    def take(self, now: float | None = None) -> Tuple[bool, int, float]:
        now = now or time.monotonic()
        elapsed = max(0.0, now - self.ts)
        self.ts = now
        self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_per_sec)
        if self.tokens >= 1:
            self.tokens -= 1
            remaining = int(self.tokens)
            reset = (self.capacity - self.tokens) / (self.refill_per_sec or 1e-9)
            return True, remaining, reset
        remaining = int(self.tokens)
        reset = (1 - self.tokens) / (self.refill_per_sec or 1e-9)
        return False, remaining, reset
