"""Access checks for shared order resources and session tokens."""
from dataclasses import dataclass
from datetime import datetime, timezone
from urllib.parse import urlparse

@dataclass(frozen=True)
class Principal:
    user_id: int
    role: str
    tenant_id: int
    active: bool = True

def can_view_order(principal: Principal, record: dict) -> bool:
    if not principal.active or record.get('tenant_id') != principal.tenant_id:
        return False

    return principal.role == 'admin' or record.get('owner_id') == principal.user_id

def visible_orders(principal: Principal, orders: list[dict]) -> list[dict]:
    return [order for order in orders if can_view_order(principal, order)]

def safe_return_url(url: str, allowed_host: str) -> bool:
    parsed = urlparse(url)

    if not parsed.netloc:
        return (
            not parsed.scheme
            and url.startswith("/")
            and not url.startswith("//")
            and "\\" not in url
        )

    return (
        parsed.scheme == "https"
        and parsed.username is None
        and parsed.password is None
        and parsed.hostname is not None
        and host_matches_domain(parsed.hostname, allowed_host)
    )

def session_valid(expires_at: str, current: datetime | None = None) -> bool:
    if current is None:
        current = datetime.now(timezone.utc)
    expires = datetime.fromisoformat(expires_at)
    return expires > current

def host_matches_domain(host: str, domain: str) -> bool:
    if not host or not domain:
        return False

    host_parts = host.casefold().rstrip(".").split(".")
    domain_parts = domain.casefold().rstrip(".").split(".")

    return (
        len(host_parts) >= len(domain_parts)
        and host_parts[-len(domain_parts):] == domain_parts
    )