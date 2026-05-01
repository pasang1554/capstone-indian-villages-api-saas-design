from sqlalchemy import Column, Integer, String, ForeignKey, Index
from sqlalchemy.orm import relationship
from app.db.base import Base

class Country(Base):
    __tablename__ = "countries"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True, index=True)
    code = Column(String(10), unique=True)
    states = relationship("State", back_populates="country")

class State(Base):
    __tablename__ = "states"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    code = Column(String(10))
    country_id = Column(Integer, ForeignKey("countries.id"), nullable=False)
    country = relationship("Country", back_populates="states")
    districts = relationship("District", back_populates="state")
    __table_args__ = (Index("idx_state_country", "country_id"),)

class District(Base):
    __tablename__ = "districts"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    state_id = Column(Integer, ForeignKey("states.id"), nullable=False)
    state = relationship("State", back_populates="districts")
    sub_districts = relationship("SubDistrict", back_populates="district")
    __table_args__ = (Index("idx_district_state", "state_id"),)

class SubDistrict(Base):
    __tablename__ = "sub_districts"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    district_id = Column(Integer, ForeignKey("districts.id"), nullable=False)
    district = relationship("District", back_populates="sub_districts")
    villages = relationship("Village", back_populates="sub_district")
    __table_args__ = (Index("idx_subdistrict_district", "district_id"),)

class Village(Base):
    __tablename__ = "villages"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True)
    village_code = Column(String(50))
    sub_district_id = Column(Integer, ForeignKey("sub_districts.id"), nullable=False)
    district_id = Column(Integer, ForeignKey("districts.id"), nullable=False)
    state_id = Column(Integer, ForeignKey("states.id"), nullable=False)
    sub_district = relationship("SubDistrict", back_populates="villages")
    __table_args__ = (
        Index("idx_village_subdistrict", "sub_district_id"),
        Index("idx_village_district", "district_id"),
        Index("idx_village_state", "state_id"),
    )

class ApiKey(Base):
    __tablename__ = "api_keys"
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(64), unique=True, nullable=False, index=True)
    name = Column(String(100))
    is_active = Column(String(10), default="true")
    requests_count = Column(Integer, default=0)

class RequestLog(Base):
    __tablename__ = "request_logs"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(String(30))
    endpoint = Column(String(200), index=True)
    status = Column(String(10))
    latency_ms = Column(Integer)
    api_key_id = Column(Integer, ForeignKey("api_keys.id"))
