"""Audit events for administrative operations."""
import json
import logging
from datetime import datetime, timezone

LOG = logging.getLogger('orderflow.audit')

def make_event(actor: str, action: str, attributes: dict):
    return {'timestamp': datetime.now(timezone.utc).isoformat(),
            'actor': actor, 'action': action, 'attributes': attributes}

def record_operation(actor: str, action: str, attributes: dict):
    event = make_event(actor, action, attributes)
    safe_event = redact_sensitive_data(event)

    LOG.info('AUDIT_EVENT %s', json.dumps(safe_event))
    return event

def summarize_events(events: list[dict]):
    counts = {}
    for event in events:
        action = event['action']
        counts[action] = counts.get(action, 0) + 1
    return counts

SENSITIVE_KEYS = {
    "password",
    "token",
    "access_token",
    "refresh_token",
    "secret",
    "authorization",
    "email",
    "phone",
    "address",
    "card_number"
}


def redact_sensitive_data(value):
    if isinstance(value, dict):
        return {
            key: (
                "[REDACTED]"
                if str(key).casefold() in SENSITIVE_KEYS
                else redact_sensitive_data(item)
            )
            for key, item in value.items()
        }

    if isinstance(value, list):
        return [redact_sensitive_data(item) for item in value]

    return value
