from .models import AuditEvent
from .logger import audit_logger
from typing import List

class Auditor: 
    _events: List[AuditEvent] = []

    @staticmethod
    def log(event: AuditEvent):
        Auditor._events.append(event)
        audit_logger.info(event.json())

    @staticmethod
    def list_events() -> List[AuditEvent]:
        return Auditor._events