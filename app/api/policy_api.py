from fastapi import APIRouter
from app.models.request_models import PolicyRequest
from app.models.response_models import PolicyResponse
from app.services.policy_loader import load_policies
from app.core.evaluator import PolicyEvaluator

router = APIRouter()

policies = load_policies()
evaluator = PolicyEvaluator(policies)

@router.post("/evaluate", response_model=PolicyResponse)
def evaluate_policy(request: PolicyRequest):
    decision = evaluator.evaluate(request)
    return {"decision": decision}