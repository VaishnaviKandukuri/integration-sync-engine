from app.config import settings


def github_headers() -> dict:
    return {
        "Authorization": f"Bearer {settings.GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }


def airtable_headers() -> dict:
    return {
        "Authorization": f"Bearer {settings.AIRTABLE_TOKEN}",
        "Content-Type": "application/json",
    }