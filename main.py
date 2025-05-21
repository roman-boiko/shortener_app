import secrets
from fastapi import FastAPI, HTTPException, Depends
import schemas
import models
from sqlalchemy.orm import Session
import validators
from database import SessionLocal, engine

app = FastAPI()
models.Base.metadata.create_all(bind=engine)


def get_db():
    """
    Dependency to get a database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def raise_bad_request(message: str):
    """
    Raise a 400 Bad Request HTTP exception with the given message.
    """
    raise HTTPException(status_code=400, detail=message)


@app.get("/")
async def root():
    return {"message": "Welcome to shortenURL API!"}


@app.post("/url", response_model=schemas.URLInfo)
def create_url(url: schemas.URLBase, db: Session = Depends(get_db)):
    """
    Create a new URL entry.
    """
    if not validators.url(url.target_url):
        raise_bad_request("Invalid URL format.")
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    key = "".join(secrets.choice(chars) for _ in range(5))
    secret_key = "".join(secrets.choice(chars) for _ in range(8))
    db_url = models.URL(target_url=url.target_url, key=key, secret_key=secret_key)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    db_url.url = key
    db_url.admin_url = secret_key

    return db_url
