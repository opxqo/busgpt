from collections import defaultdict, deque
from time import monotonic

from fastapi import HTTPException, Request, status


AUTH_FAILURE_LIMIT = 5
AUTH_WINDOW_SECONDS = 15 * 60
_auth_failures: dict[str, deque[float]] = defaultdict(deque)


def _client_ip(request: Request) -> str:
    forwarded_for = request.headers.get("x-forwarded-for")
    if forwarded_for:
        return forwarded_for.split(",", 1)[0].strip()
    return request.client.host if request.client else "unknown"


def _auth_key(request: Request, identifier: str) -> str:
    return f"{_client_ip(request)}:{identifier}"


def check_auth_rate_limit(request: Request, identifier: str) -> str:
    key = _auth_key(request, identifier)
    now = monotonic()
    failures = _auth_failures[key]
    while failures and now - failures[0] > AUTH_WINDOW_SECONDS:
        failures.popleft()
    if len(failures) >= AUTH_FAILURE_LIMIT:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="请求过于频繁，请稍后再试",
        )
    return key


def record_auth_failure(key: str) -> None:
    _auth_failures[key].append(monotonic())


def record_auth_success(key: str) -> None:
    _auth_failures.pop(key, None)


def reset_auth_rate_limits() -> None:
    _auth_failures.clear()
