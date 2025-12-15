from pydantic import BaseModel

class PolicyResponse(BaseModel):
    decision: str