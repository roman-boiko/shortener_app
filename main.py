from fastapi import FastAPI, HTTPException
import schemas
import validators

app = FastAPI()


def raise_bad_request(message: str):
    """
    Raise a 400 Bad Request HTTP exception with the given message.
    """
    raise HTTPException(status_code=400, detail=message)


@app.get("/")
async def root():
    return {"message": "Welcome to shortenURL API!"}


@app.post("/url")
def create_url(url: schemas.URLBase):
    """
    Create a new URL entry.
    """
    if not validators.url(url.target_url):
        raise_bad_request("Invalid URL format.")

    # Here you would typically save the URL to a database
    # For demonstration, we will just return the URL
    return {"target_url": url.target_url, "is_active": True, "clicks": 0}
