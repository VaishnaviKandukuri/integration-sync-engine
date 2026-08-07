from app.models.schemas import ContributorRecord


def normalize_contributor(raw_contributor: dict, repo_name: str) -> ContributorRecord:
    return ContributorRecord(
        source_id=str(raw_contributor["id"]),
        username=raw_contributor["login"],
        repository=repo_name,
        contribution_count=raw_contributor["contributions"],
        source_system="github",
    )