from sqlalchemy.dialects.sqlite import insert
from sqlalchemy.orm import Session
from app.models.db_models import Contributor
from app.models.schemas import ContributorRecord


def upsert_contributor(db: Session, record: ContributorRecord) -> None:
    stmt = insert(Contributor).values(
        source_id=record.source_id,
        username=record.username,
        repository=record.repository,
        contribution_count=record.contribution_count,
        source_system=record.source_system,
    )

    stmt = stmt.on_conflict_do_update(
        index_elements=["source_id"],
        set_={
            "contribution_count": record.contribution_count,
            "username": record.username,
        },
    )

    db.execute(stmt)