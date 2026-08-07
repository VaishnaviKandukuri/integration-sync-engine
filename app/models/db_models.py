import uuid
import datetime as dt
from sqlalchemy import Column, String, Integer, DateTime
from app.database import Base


def generate_uuid() -> str:
    return str(uuid.uuid4())


class Contributor(Base):
    __tablename__ = "contributors"

    id = Column(String, primary_key=True, default=generate_uuid)
    source_id = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, nullable=False)
    repository = Column(String, nullable=False)
    contribution_count = Column(Integer, default=0)
    source_system = Column(String, default="github")

    created_at = Column(DateTime, default=dt.datetime.utcnow)
    updated_at = Column(DateTime, default=dt.datetime.utcnow, onupdate=dt.datetime.utcnow)