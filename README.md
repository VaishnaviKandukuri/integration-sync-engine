# Integration Sync Engine

A real, working integration pipeline: pulls contributor data from GitHub's live REST API, normalizes it into a canonical schema, stores it idempotently via UPSERT in SQLite, and pushes it to a real Airtable base — demonstrating authentication, pagination, rate-limit backoff, and audit logging against two genuine third-party systems, not mocks.

Built as a companion piece to a separate HR-tech integration platform (webhook receiving, OAuth2, HMAC) — this project specifically covers the *consuming/pull* side of integration engineering: calling someone else's real API correctly, handling their real constraints.

## Why GitHub and Airtable, not a real ATS/HRIS

Real ATS platforms (Workable, BambooHR) require business email verification for API trial access. GitHub and Airtable are genuinely free, personal-account-accessible, real external APIs with real authentication, real rate limits, and real pagination — the same underlying mechanics any ATS/HRIS integration would require.

## Architecture

**Pull:** GitHub REST API (Bearer PAT auth) → pagination via `Link` header → exponential backoff on rate limits
**Normalize:** raw GitHub JSON → canonical `ContributorRecord` (Pydantic)
**Store:** SQLite, idempotent UPSERT keyed on `source_id`
**Push:** Airtable REST API (Bearer PAT auth) → same backoff logic, different rate-limit signaling (429 vs GitHub's 403)
**Observe:** every API call logged with status code and latency
**Automate:** Windows Task Scheduler triggers the sync unattended, on a schedule

## What's implemented

- Real Bearer token authentication against two independent external APIs
- Pagination following GitHub's `Link` header across multiple pages
- Exponential backoff on rate limiting, handling both GitHub's (403 + text match) and Airtable's (429) signaling conventions
- Data normalization from external JSON into a canonical Pydantic schema
- Idempotent UPSERT storage (SQLAlchemy `on_conflict_do_update`)
- Call-level audit logging (status code, latency, endpoint)
- Raw SQL aggregation queries (GROUP BY, AVG)
- Automated tests (pytest) covering normalization and UPSERT idempotency
- Real automated scheduling via Windows Task Scheduler
- Postman collection using environment variables (no hardcoded secrets)

## Tech stack

**Core:** Python, SQLAlchemy, Pydantic, SQLite
**HTTP/API:** requests (client), real GitHub REST API v3, real Airtable REST API
**Auth:** Bearer token / Personal Access Token (both GitHub and Airtable)
**Testing:** pytest
**Automation:** Windows Task Scheduler
**Documentation/Testing tools:** Postman (with environment variables, no hardcoded secrets)

## Running locally

```bash
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Create `.env` with: `GITHUB_TOKEN`, `GITHUB_USERNAME`, `AIRTABLE_TOKEN`, `AIRTABLE_BASE_ID`, `AIRTABLE_TABLE_NAME`

```bash
python -m scripts.run_sync
```

## Running tests

```bash
pytest tests/ -v
```

## Raw SQL reporting

```bash
python -m scripts.sql_queries
```

## Automated scheduling

`scripts/run_sync.bat` is registered in Windows Task Scheduler to run the sync unattended on a timer, calling the same pipeline as a manual run.