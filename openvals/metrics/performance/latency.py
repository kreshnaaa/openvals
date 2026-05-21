import time

def measure_latency(func, input_text):
    start = time.time()

    try:
        output = func(input_text)

        # 🔥 Handle None / bad outputs
        if output is None:
            output = ""

    except Exception as e:
        return f"ERROR: {str(e)}", 0.0

    end = time.time()

    latency_ms = (end - start) * 1000

    return output, latency_ms