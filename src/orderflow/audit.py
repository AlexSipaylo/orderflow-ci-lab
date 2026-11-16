"""Audit events for administrative operations."""
import json
import logging
from datetime import datetime, timezone

LOG = logging.getLogger('orderflow.audit')

SENSITIVE_KEY_PARTS = ('password','token', 'secret', 'authorization', 'api_key', 'email', 'phone')

def make_event(actor: str, action: str, attributes: dict):
    return {'timestamp': datetime.now(timezone.utc).isoformat(),
            'actor': actor, 'action': action, 'attributes': attributes}

def record_operation(actor: str, action: str, attributes: dict):
    event = make_event(actor, action, attributes)

    safe_event = redact_sensitive_fields(event)

    serialized = json.JSONEncoder(ensure_ascii=False).encode(safe_event)

    LOG.info('AUDIT_EVENT %s', serialized)

    return event

def summarize_events(events: list[dict]):
    counts = {}
    for event in events:
        action = event['action']
        counts[action] = counts.get(action, 0) + 1
    return counts


def redact_sensitive_fields(value):
    if isinstance(value, dict):
        cleaned = {}

        for key, item in value.items():
            if any(part in str(key).casefold() for part in SENSITIVE_KEY_PARTS):
                cleaned[key] = '[REDACTED]'
            else:
                cleaned[key] = redact_sensitive_fields(item)

        return cleaned

    if isinstance(value, list):
        return [redact_sensitive_fields(item) for item in value]

    return value