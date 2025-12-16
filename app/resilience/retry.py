from tenacity import retry, stop_after_attempt, wait_fixed

@retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
def safe_evaluate(evaluator, request):
    return evaluator.evaluate(request)