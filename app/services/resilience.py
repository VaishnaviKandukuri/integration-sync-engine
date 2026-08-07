import time


def call_with_backoff(request_func, max_retries: int = 5):
    attempt = 0
    delay = 1

    while attempt < max_retries:
        response = request_func()

        is_github_limit = response.status_code == 403 and "rate limit" in response.text.lower()
        is_standard_limit = response.status_code == 429

        if is_github_limit or is_standard_limit:
            reset_time = int(response.headers.get("X-RateLimit-Reset", 0))
            wait_seconds = max(reset_time - int(time.time()), delay)
            print(f"Rate limited. Waiting {wait_seconds} seconds before retry (attempt {attempt + 1}/{max_retries})...")
            time.sleep(min(wait_seconds, 60))
            delay *= 2
            attempt += 1
            continue

        return response

    raise Exception("Max retries exceeded due to persistent rate limiting")