import requests
from app.services.auth_manager import github_headers
from app.services.resilience import call_with_backoff

GITHUB_API_BASE = "https://api.github.com"


def get_user_repos(username: str) -> list[dict]:
    url = f"{GITHUB_API_BASE}/users/{username}/repos"
    all_repos = []
    while url:
        response = call_with_backoff(
            lambda: requests.get(url, headers=github_headers(), params={"per_page":30})
        )
        response.raise_for_status()
        all_repos.extend(response.json())

        url = response.links.get("next", {}).get("url")

    return all_repos