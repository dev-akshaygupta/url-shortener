from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

Base = declarative_base()

class ShortURL(Base):
    __tablename__ = "short_urls"

    id = Column(Integer, primary_key=True)
    short_code = Column(String, index=True)
    original_url = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    regional_urls = relationship("RegionalURL", back_populates="short_url")

class RegionalURL(Base):
    __tablename__ = "regional_urls"

    id = Column(Integer, primary_key=True, index=True)
    region = Column(String, index=True)
    url = Column(String, nullable=False)
    short_url_id = Column(Integer, ForeignKey("short_urls.id"))

    short_url = relationship("ShortURL", back_populates="regional_urls")