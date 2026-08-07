from sqlalchemy import text
from app.database import engine


def run_raw_queries():
    with engine.connect() as conn:
        print("=== Top 5 contributors by contribution count ===")
        result = conn.execute(text("""
            SELECT username, repository, contribution_count
            FROM contributors
            ORDER BY contribution_count DESC
            LIMIT 5
        """))
        for row in result:
            print(row.username, row.repository, row.contribution_count)

        print("\n=== Average contribution count per repository ===")
        result = conn.execute(text("""
            SELECT repository, COUNT(*) as contributor_count, AVG(contribution_count) as avg_contributions
            FROM contributors
            GROUP BY repository
        """))
        for row in result:
            print(row.repository, row.contributor_count, round(row.avg_contributions, 1))

        print("\n=== Average API call latency by system ===")
        result = conn.execute(text("""
            SELECT system, COUNT(*) as call_count, AVG(latency_ms) as avg_latency
            FROM api_call_log
            GROUP BY system
        """))
        for row in result:
            print(row.system, row.call_count, round(row.avg_latency, 2))


if __name__ == "__main__":
    run_raw_queries()