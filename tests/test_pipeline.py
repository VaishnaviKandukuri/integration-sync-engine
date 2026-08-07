import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.models.schemas import ContributorRecord
from app.services.normalizer import normalize_contributor
from app.services.storage import upsert_contributor
from app.models.db_models import Contributor

TEST_DATABASE_URL = "sqlite:///./test_sync.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(bind=engine)


@pytest.fixture()
def db_session():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


def test_normalize_contributor_maps_fields_correctly():
    raw = {"id": 12345, "login": "octocat", "contributions": 42}
    record = normalize_contributor(raw, "hello-world")

    assert record.source_id == "12345"
    assert record.username == "octocat"
    assert record.repository == "hello-world"
    assert record.contribution_count == 42


def test_upsert_inserts_new_record(db_session):
    record = ContributorRecord(
        source_id="abc123", username="testuser", repository="testrepo", contribution_count=10
    )
    upsert_contributor(db_session, record)
    db_session.commit()

    count = db_session.query(Contributor).count()
    assert count == 1


def test_upsert_updates_existing_record_not_duplicate(db_session):
    record_v1 = ContributorRecord(
        source_id="abc123", username="testuser", repository="testrepo", contribution_count=10
    )
    upsert_contributor(db_session, record_v1)
    db_session.commit()

    record_v2 = ContributorRecord(
        source_id="abc123", username="testuser", repository="testrepo", contribution_count=50
    )
    upsert_contributor(db_session, record_v2)
    db_session.commit()

    count = db_session.query(Contributor).count()
    assert count == 1

    updated = db_session.query(Contributor).filter(Contributor.source_id == "abc123").first()
    assert updated.contribution_count == 50