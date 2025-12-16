from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any

from app.models.request_models import PolicyRequest, PolicyDefinition
from app.models.response_models import PolicyResponse

from app.services.policy_loader import load_policies, save_policies
from app.core.evaluator import PolicyEvaluator

from app.audit.auditor import Auditor
from app.audit.models import AuditEvent
from app.resilience.circuit_breaker import circuit_breaker

router = APIRouter()

policies = load_policies()
evaluator = PolicyEvaluator(policies)

def refresh_evaluator():
    global evaluator

    save_policies(policies)
    evaluator = PolicyEvaluator(policies)

@router.post("/evaluate", response_model=PolicyResponse)
def evaluate_policy(request: PolicyRequest):
    try:
        @circuit_breaker
        def protected_evaluate():
            return evaluator.evaluate(request)
        
        decision = protected_evaluate()

        decision_value = decision["decision"] if isinstance(decision, dict) else decision

        Auditor.log(
            AuditEvent(
                user_id=request.user.id,
                resource=request.resource,
                action=request.action,
                decision=decision_value,
                reason=decision.get("reason") if isinstance(decision, dict) else None,
                circuit_state=circuit_breaker.current_state().value,
                retries=0
            )
        )

        return {"decision": decision_value}
    
    except Exception as e:
        Auditor.log(
            AuditEvent(
                user_id=request.user.id,
                resource=request.resource,
                action=request.action,
                decision="DENY",
                reason=str(e),
                circuit_state=circuit_breaker.current_state().value,
                retries=0
            )
        )

        raise HTTPException(status_code=503, detail="Serviço temporariamente indisponível")

@router.get("/policies", response_model=List[Dict[str, Any]])
def list_policies():
    return policies

@router.get("/policies/{policy_name}")
def get_policy(policy_name: str):
    policy = next((p for p in policies if p["name"] == policy_name), None)
    
    if not policy:
        raise HTTPException(status_code=404, detail="Política não encontrada")
    
    return policy

@router.post("/policies", status_code=201)
def create_policy(policy: PolicyDefinition):
    if any(p["name"] == policy.name for p in policies):
        raise HTTPException(status_code=400, detail="Já existe uma política com este nome.")
    
    policies.append(policy.model_dump())
    refresh_evaluator()

    Auditor.log(
        AuditEvent(
            user_id="ADMIN",
            resource="policy",
            action="CREATE",
            decision="ALLOW",
            reason=f"Política {policy.name} criada",
            circuit_state="N/A",
            retries=0
        )
    )

    return {"message": "Política criada com sucesso.", "policy": policy}

@router.put("/policies/{policy_name}")
def update_policy(policy_name: str, policy_update: PolicyDefinition):
    for index, policy in enumerate(policies):
        if policy["name"] == policy_name:
            policies[index] = policy_update.model_dump()
            refresh_evaluator()

            Auditor.log(
                AuditEvent(
                    user_id="ADMIN",
                    resource="policy",
                    action="UPDATE",
                    decision="ALLOW",
                    reason=f"Política {policy_name} atualizada",
                    circuit_state="N/A",
                    retries=0
                )
            )

            return {"meesage": "Política atualizada com sucesso.", "policy": policy_update}
        
    raise HTTPException(status_code=404, detail="Política não encontrada.")


@router.delete("/policies/{policy_name}")
def delete_policy(policy_name: str):
    global policies

    initial_count = len(policies)

    policies = [p for p in policies if p["name"] != policy_name]

    if len(policies) == initial_count:
        raise HTTPException(status_code=404, detail="Política não encontrada.")
    
    refresh_evaluator()

    Auditor.log(
        AuditEvent(
            user_id="ADMIN",
            resource="policy",
            action="DELETE",
            decision="ALLOW",
            reason=f"Política {policy_name} removida",
            circuit_state="N/A",
            retries=0
        )
    )
    return {"message": "Política deletada com sucesso."}

@router.get("/audit/logs", response_model=List[AuditEvent])
def get_audit_logs():
    return Auditor.list_events()