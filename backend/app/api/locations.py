from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.base import get_db
from app.models.location import Country, State, District, SubDistrict, Village
from app.core.security import rate_limit

router = APIRouter(prefix="/api/v1", dependencies=[Depends(rate_limit)])

def log_request(request: Request, status: str, latency: int, api_key_id: int, db: Session):
    from app.models.location import RequestLog
    import time
    log = RequestLog(
        timestamp=str(time.time()),
        endpoint=str(request.url),
        status=status,
        latency_ms=latency,
        api_key_id=api_key_id
    )
    db.add(log)
    db.commit()

@router.get("/countries")
def get_countries(db: Session = Depends(get_db), request: Request = None):
    import time
    start = time.time()
    results = db.query(Country).order_by(Country.name).all()
    latency = int((time.time() - start) * 1000)
    log_request(request, "200", latency, 0, db)
    return [{"id": c.id, "name": c.name, "code": c.code} for c in results]

@router.get("/states")
def get_states(country_id: int = Query(...), db: Session = Depends(get_db)):
    results = db.query(State).filter(State.country_id == country_id).order_by(State.name).all()
    return [{"id": s.id, "name": s.name, "code": s.code} for s in results]

@router.get("/districts")
def get_districts(state_id: int = Query(...), db: Session = Depends(get_db)):
    results = db.query(District).filter(District.state_id == state_id).order_by(District.name).all()
    return [{"id": d.id, "name": d.name} for d in results]

@router.get("/sub-districts")
def get_sub_districts(district_id: int = Query(...), db: Session = Depends(get_db)):
    results = db.query(SubDistrict).filter(SubDistrict.district_id == district_id).order_by(SubDistrict.name).all()
    return [{"id": s.id, "name": s.name} for s in results]

@router.get("/villages")
def get_villages(
    state_id: int = Query(None),
    district_id: int = Query(None),
    sub_district_id: int = Query(None),
    search: str = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(50, le=200),
    db: Session = Depends(get_db)
):
    query = db.query(Village)
    if sub_district_id:
        query = query.filter(Village.sub_district_id == sub_district_id)
    if district_id:
        query = query.filter(Village.district_id == district_id)
    if state_id:
        query = query.filter(Village.state_id == state_id)
    if search:
        query = query.filter(Village.name.ilike(f"%{search}%"))

    total = query.count()
    results = query.order_by(Village.name).offset((page - 1) * limit).limit(limit).all()
    return {
        "total": total,
        "page": page,
        "limit": limit,
        "data": [{"id": v.id, "name": v.name, "village_code": v.village_code} for v in results]
    }

@router.get("/villages/{village_id}")
def get_village(village_id: int, db: Session = Depends(get_db)):
    v = db.query(Village).filter(Village.id == village_id).first()
    if not v:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Village not found")
    return {"id": v.id, "name": v.name, "village_code": v.village_code,
            "sub_district_id": v.sub_district_id, "district_id": v.district_id, "state_id": v.state_id}
