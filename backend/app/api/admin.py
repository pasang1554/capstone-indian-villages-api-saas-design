from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.models.location import ApiKey, RequestLog
from app.core.security import verify_api_key
import secrets

router = APIRouter(prefix="/api/admin", dependencies=[Depends(verify_api_key)])

@router.post("/keys")
def create_api_key(name: str, db: Session = Depends(get_db)):
    key = secrets.token_hex(32)
    api_key = ApiKey(key=key, name=name, is_active="true", requests_count=0)
    db.add(api_key)
    db.commit()
    db.refresh(api_key)
    return {"id": api_key.id, "key": key, "name": name, "is_active": True}

@router.get("/keys")
def list_api_keys(db: Session = Depends(get_db)):
    keys = db.query(ApiKey).all()
    return [{"id": k.id, "name": k.name, "key": k.key[:8] + "...", "is_active": k.is_active == "true", "requests": k.requests_count} for k in keys]

@router.put("/keys/{key_id}/toggle")
def toggle_key(key_id: int, db: Session = Depends(get_db)):
    key = db.query(ApiKey).filter(ApiKey.id == key_id).first()
    if not key:
        raise HTTPException(status_code=404, detail="Key not found")
    key.is_active = "false" if key.is_active == "true" else "true"
    db.commit()
    return {"status": "toggled", "is_active": key.is_active == "true"}

@router.get("/analytics")
def get_analytics(db: Session = Depends(get_db)):
    from sqlalchemy import func
    total_requests = db.query(func.count(RequestLog.id)).scalar()
    top_endpoints = db.query(
        RequestLog.endpoint,
        func.count(RequestLog.id).label("count")
    ).group_by(RequestLog.endpoint).order_by(func.count(RequestLog.id).desc()).limit(5).all()

    return {
        "total_requests": total_requests,
        "top_endpoints": [{"endpoint": e[0], "count": e[1]} for e in top_endpoints]
    }

@router.get("/logs")
def get_logs(limit: int = 100, db: Session = Depends(get_db)):
    logs = db.query(RequestLog).order_by(RequestLog.id.desc()).limit(limit).all()
    return [{"id": l.id, "timestamp": l.timestamp, "endpoint": l.endpoint, "status": l.status, "latency_ms": l.latency_ms} for l in logs]
