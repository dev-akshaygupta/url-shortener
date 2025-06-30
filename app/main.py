from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, AnyUrl
from sqlalchemy.orm import Session

from app.models import Base, ShortURL
from app.db import engine, get_db
from app.utils import generate_short_code


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
    db_url = ShortURL(short_code=short_code, original_url=request.long_url)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return {"short_code": db_url.short_code}

@app.get("/{short_code}")
def redirect_to_url(short_code: str, db: Session=Depends(get_db)):
    db_url = db.query(ShortURL).filter(ShortURL.short_code == short_code).first()
    if not db_url:
        raise HTTPException(status_code=404, detail="Short URL not found")
    return RedirectResponse(url=db_url.original_url)