import time
import redis
from fastapi import Request, HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.config import settings
from app.db.base import get_db
from app.models.location import ApiKey

redis_client = None
if settings.USE_REDIS and settings.REDIS_URL:
    redis_client = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)

def verify_api_key(request: Request, db: Session = Depends(get_db)):
    api_key = request.headers.get(settings.API_KEY_HEADER)
    if not api_key:
        raise HTTPException(status_code=401, detail="Missing API key")

    key_record = db.query(ApiKey).filter(ApiKey.key == api_key, ApiKey.is_active == "true").first()
    if not key_record:
        raise HTTPException(status_code=401, detail="Invalid or inactive API key")

    key_record.requests_count += 1
    db.commit()
    return key_record

def rate_limit(api_key: ApiKey = Depends(verify_api_key)):
    if not redis_client:
        return api_key
    key = f"rate_limit:{api_key.key}"
    count = redis_client.get(key)
    if count and int(count) >= settings.RATE_LIMIT_PER_MINUTE:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    pipe = redis_client.pipeline()
    pipe.incr(key)
    pipe.expire(key, 60)
    pipe.execute()
    return api_key
