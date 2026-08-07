from app.database import SessionLocal
from app.services.github_client import get_repo_contributors
from app.services.normalizer import normalize_contributor
from app.services.storage import upsert_contributor
from app.services.airtable_client import push_contributor


def run_sync(owner: str, repo: str, limit: int = 10):
    db = SessionLocal()

    print(f"Pulling contributors for {owner}/{repo}...")
    raw_contributors = get_repo_contributors(owner, repo, db=db)
    print(f"Fetched {len(raw_contributors)} raw contributors.")

    synced_count = 0
    for raw in raw_contributors[:limit]:
        record = normalize_contributor(raw, repo)

        upsert_contributor(db, record)

        try:
            push_contributor(record)
        except Exception as e:
            print(f"Warning: failed to push {record.username} to Airtable: {e}")
            continue

        synced_count += 1
        print(f"Synced: {record.username} ({record.contribution_count} contributions)")

    db.commit()
    db.close()
    print(f"Sync complete. {synced_count}/{min(limit, len(raw_contributors))} records synced to both SQLite and Airtable.")


if __name__ == "__main__":
    run_sync("psf", "requests", limit=10)