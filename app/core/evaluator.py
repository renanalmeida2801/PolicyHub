import operator

class PolicyEvaluator:
    def __init__(self, policies: list):
        self.policies = policies

        self.ops = {
            "eq": operator.eq,
            "ne": operator.ne,
            "gt": operator.gt,
            "lt": operator.lt,
            "ge": operator.ge,
            "le": operator.le,
            "in": lambda x, y: x in y,
            "contains": lambda x, y: y in x

        }
    
    def evaluate(self, request):
        return self._evaluate_internal(request)

    def _evaluate_internal(self, request):
        for policy in self.policies:
            if self._matches(policy, request):
                return policy["decision"]
        return "DENY"

    def _matches(self, policy, request):
        if policy["action"] != request.action:
            return False
        
        if policy["resource"] != request.resource:
            return False
        
        for key, condition in policy["conditions"].items():
            if key == "roles":
                if not any(role in request.user.roles for role in condition):
                    return False
            else:
                req_value = request.context.get(key)
                
                if isinstance(condition, dict) and "operator" in condition:
                    op_name = condition.get("operator")
                    target_value = condition.get("value")

                    op_func = self.ops.get(op_name, operator.eq)

                    if not op_func(req_value, target_value):
                        return False
                    
                elif req_value != condition:
                    return False
        
        return True

