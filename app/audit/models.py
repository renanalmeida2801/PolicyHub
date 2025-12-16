from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AuditEvent(BaseModel):
    user_id: str
    resource: str
    action: str
    decision: str
    reason: Optional[str]
    circuit_state: str
    retries: int
    timestamp: datetime = datetime.now()