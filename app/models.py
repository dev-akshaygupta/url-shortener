from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime
from datetime import datetime, timezone

Base = declarative_base()

class ShortURL(Base):
    __tablename__ = "short_urls"

    short_code = Column(String, primary_key=True, index=True)
    original_url = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))