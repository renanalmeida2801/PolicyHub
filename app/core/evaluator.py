class PolicyEvaluator:
    def __init__(self, policies: list):
        self.policies = policies
    
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
        
        for key, value in policy["conditions"].items():
            if key == "roles":
                if not any(role in request.user.roles for role in value):
                    return False
            else:
                if request.context.get(key) != value:
                    return False
        
        return True
