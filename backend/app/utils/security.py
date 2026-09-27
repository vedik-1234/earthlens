"""Security utilities for EarthLens."""
import os
from functools import lru_cache
from datetime import datetime, timedelta


class RateLimiter:
    """Simple in-memory rate limiter."""

    def __init__(self, max_requests: int = 60, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = {}

    def is_allowed(self, identifier: str) -> bool:
        """Check if request is allowed for identifier."""
        now = datetime.utcnow()
        if identifier not in self.requests:
            self.requests[identifier] = []

        # Remove old requests outside window
        cutoff = now - timedelta(seconds=self.window_seconds)
        self.requests[identifier] = [
            req_time for req_time in self.requests[identifier]
            if req_time > cutoff
        ]

        # Check if at limit
        if len(self.requests[identifier]) < self.max_requests:
            self.requests[identifier].append(now)
            return True
        return False


rate_limiter = RateLimiter(
    max_requests=int(os.getenv('EARTHLENS_RATE_LIMIT', 60)),
    window_seconds=60,
)


def get_client_ip(request) -> str:
    """Extract real client IP from request."""
    if request.headers.get('x-forwarded-for'):
        return request.headers.get('x-forwarded-for').split(',')[0].strip()
    if request.headers.get('x-real-ip'):
        return request.headers.get('x-real-ip')
    return request.client.host if request.client else 'unknown'


@lru_cache(maxsize=128)
def is_trusted_origin(origin: str) -> bool:
    """Check if origin is in trusted list."""
    allowed = os.getenv('EARTHLENS_ALLOWED_ORIGINS', 'http://localhost:5173').split(',')
    return origin in [o.strip() for o in allowed]
