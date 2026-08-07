import time


def call_with_backoff(request_func, max_retries: int = 5):
    attempt = 0
    delay = 1

    while attempt < max_retries:
        response = request_func()

        if response.status_code == 403 and "rate limit" in response.text.lower():
            reset_time = int(response.headers.get("X-RateLimit-Reset", 0))
            wait_seconds = max(reset_time - int(time.time()), delay)
            print(f"Rate limited. Waiting {wait_seconds} seconds before retry (attempt {attempt + 1}/{max_retries})...")
            time.sleep(min(wait_seconds, 60))
            delay *= 2
            attempt += 1
            continue

        return response

    raise Exception("Max retries exceeded due to persistent rate limiting")