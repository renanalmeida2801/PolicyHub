import pybreaker

policy_circuit_breaker = pybreaker.CircuitBreaker(
    fail_max=3,
    reset_timeout=30
)