import requests
from app.config import settings
from app.services.auth_manager import airtable_headers
from app.services.resilience import call_with_backoff
from app.models.schemas import ContributorRecord

AIRTABLE_API_BASE = "https://api.airtable.com/v0"


def push_contributor(record: ContributorRecord) -> dict:
    url = f"{AIRTABLE_API_BASE}/{settings.AIRTABLE_BASE_ID}/{settings.AIRTABLE_TABLE_NAME}"

    payload = {
        "fields": {
            "Username": record.username,
            "Repository": record.repository,
            "ContributionCount": record.contribution_count,
            "SourceID": record.source_id,
            "SourceSystem": record.source_system,
        }
    }

    response = call_with_backoff(
        lambda: requests.post(url, headers=airtable_headers(), json=payload)
    )
    response.raise_for_status()
    return response.json()