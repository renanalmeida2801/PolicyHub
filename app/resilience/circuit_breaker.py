import time
from enum import Enum
from functools import wraps

class CircuitState(str, Enum):
    CLOSED = "CLOSED"
    OPEN = "OPEN"
    HALF_OPEN = "HALF_OPEN"


class CircuitBreaker:
    def __init__(self, failure_threshold: int = 3, recovery_timeout: int = 10):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.state = CircuitState.CLOSED
        self.last_failure_time = None

    def current_state(self) -> CircuitState:
        if self.state == CircuitState.OPEN:
            elapsed = time.time() - self.last_failure_time
            if elapsed >= self.recovery_timeout:
                self.state = CircuitState.HALF_OPEN
        return self.state

    def record_success(self):
        self.failure_count = 0
        self.state = CircuitState.CLOSED

    def record_failure(self):
        if self.state == CircuitState.HALF_OPEN:
            self.state = CircuitState.OPEN
            self.last_failure_time = time.time()
            self.failure_count = self.failure_threshold
            return

        self.failure_count += 1

        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN
            self.last_failure_time = time.time()

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            state = self.current_state()

            if state == CircuitState.OPEN:
                raise Exception("Circuit Breaker está OPEN")

            try:
                result = func(*args, **kwargs)
                self.record_success()
                return result
            except Exception:
                self.record_failure()
                raise

        return wrapper


circuit_breaker = CircuitBreaker()

