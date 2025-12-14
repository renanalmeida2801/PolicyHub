from pydantic import BaseModel
from typing import List, Dict, Any

class UserContext(BaseModel):
    id: str
    roles: List[str]

class PolicyRequest(BaseModel):
    user: UserContext
    action: str
    resource: str
    context: Dict[str, Any]