import time

def measure_latency(func, *args, **kwargs):
    start = time.time()
    result = func(*args, **kwargs)
    end = time.time()

    latency_ms = (end - start) * 1000  # milliseconds

    return result, latency_ms
