import time
from sqlalchemy.orm import Session
from app.models.db_models import ApiCallLog


def timed_call(db: Session, system: str, endpoint: str, call_func):
    start = time.time()
    response = call_func()
    latency_ms = (time.time() - start) * 1000

    log_entry = ApiCallLog(
        system=system,
        endpoint=endpoint,
        status_code=response.status_code,
        latency_ms=round(latency_ms, 2),
    )
    db.add(log_entry)
    db.commit()

    return response