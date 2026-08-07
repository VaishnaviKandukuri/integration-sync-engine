import requests
from app.services.auth_manager import github_headers

GITHUB_API_BASE = "https://api.github.com"


def get_user_repos(username: str) -> list[dict]:
    url = f"{GITHUB_API_BASE}/users/{username}/repos"
    response = requests.get(url, headers=github_headers())
    response.raise_for_status()
    return response.json()