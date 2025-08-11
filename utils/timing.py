import time
from functools import wraps
from typing import Dict, Any, Callable


def measure_execution_time(func: Callable) -> Callable:
    """
    Decorator to measure execution time of a function.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        execution_time = time.time() - start_time

        # Add timing info to result if it's a dict
        if isinstance(result, dict):
            result["execution_time"] = round(execution_time, 2)

        return result

    return wrapper


def calculate_cost_metrics(results: list) -> Dict[str, Any]:
    """
    Calculate aggregated cost metrics from provider results.
    """
    total_cost = 0
    successful_providers = 0
    failed_providers = 0
    total_time = 0

    for result in results:
        if result.get("status") == "success":
            successful_providers += 1
            total_cost += result.get("estimated_cost", 0)
        else:
            failed_providers += 1

        total_time += result.get("time_seconds", 0)

    return {
        "total_estimated_cost": round(total_cost, 6),
        "total_execution_time": round(total_time, 2),
        "successful_providers": successful_providers,
        "failed_providers": failed_providers,
        "success_rate": (
            round(successful_providers / len(results) * 100, 1) if results else 0
        ),
    }


def get_fastest_provider(results: list) -> Dict[str, Any]:
    """
    Find the fastest successful provider.
    """
    successful_results = [r for r in results if r.get("status") == "success"]

    if not successful_results:
        return None

    fastest = min(successful_results, key=lambda x: x.get("time_seconds", float("inf")))

    return {
        "provider": fastest.get("provider"),
        "time_seconds": fastest.get("time_seconds"),
        "language": fastest.get("language"),
    }


def get_cheapest_provider(results: list) -> Dict[str, Any]:
    """
    Find the cheapest successful provider.
    """
    successful_results = [r for r in results if r.get("status") == "success"]

    if not successful_results:
        return None

    cheapest = min(
        successful_results, key=lambda x: x.get("estimated_cost", float("inf"))
    )

    return {
        "provider": cheapest.get("provider"),
        "estimated_cost": cheapest.get("estimated_cost"),
        "language": cheapest.get("language"),
    }
