from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, AnyUrl
from sqlalchemy.orm import Session

from app.models import Base, ShortURL, RegionalURL
from app.db import engine, get_db
from app.utils import generate_short_code, get_country_from_ip

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Pydantic Schema
class URLRequest(BaseModel):
    long_url: AnyUrl

class URLResponse(BaseModel):
    short_code: str

# Routes
@app.post("/shorten", response_model=URLResponse)
def shorten_url(request: URLRequest, db: Session=Depends(get_db)):
    short_code = generate_short_code()
    db_url = ShortURL(short_code=short_code, original_url=str(request.long_url))
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return {"short_code": db_url.short_code}

@app.get("/{short_code}")
def redirect(short_code: str, request: Request, db: Session=Depends(get_db)):
    db_url = db.query(ShortURL).filter(ShortURL.short_code == short_code).first()
    if not db_url:
        raise HTTPException(status_code=404, detail="Short URL not found")
    
    client_ip = request.client.host
    country = get_country_from_ip(client_ip)

    regional = next((r for r in db_url.regional_urls if r.region == country), None)

    target_url = regional.url if regional else db_url.original_url
    return RedirectResponse(url=target_url, status_code=307)

@app.post("/regional")
def add_regional_mapping(short_code: str, region: str, region_url: str, db: Session = Depends(get_db)):
    short = db.query(ShortURL).filter_by(short_code=short_code).first()
    if not short:
        raise HTTPException(status_code=404, detail="Short URL not found!")
    
    regional = RegionalURL(region=region.upper(), url=region_url, short_url=short)
    db.add(regional)
    db.commit()
    db.refresh(regional)
    return {"message": "Regional URL added", "region":region, "url":region_url}