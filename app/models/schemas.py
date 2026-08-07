from pydantic import BaseModel


class ContributorRecord(BaseModel):
    source_id: str
    username: str
    repository: str
    contribution_count: int
    source_system: str = "github"