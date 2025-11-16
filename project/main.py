from sqlalchemy.exc import IntegrityError, DataError, OperationalError
from fastapi import FastAPI, HTTPException, Query, Depends
from models import Base, Incident, StatusEnum
from db import SessionLocal, engine
from sqlalchemy.orm import Session
from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime


app = FastAPI()
Base.metadata.create_all(bind=engine)


# Pydantic модели
class IncidentCreate(BaseModel):
    description: str
    source: Optional[str] = "unknown"


class IncidentUpdate(BaseModel):
    status: StatusEnum


class IncidentResponse(BaseModel):
    id: int
    description: str
    status: StatusEnum
    source: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }


main_tag = ["Инциденты ♻️"]

def init_db():
    """Dependency Injection для подключения и управления сессиями БД"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/incidents", summary="Добавить новый инцидент", tags=main_tag, response_model=IncidentResponse, status_code=201)
def create_incident(incident: IncidentCreate, db: Session = Depends(init_db)):
    """Создание нового инцидента"""
    try:
        db_incident = Incident(description=incident.description, source=incident.source)
        db.add(db_incident)
        db.commit()
        db.refresh(db_incident)
        return db_incident
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Ошибка при создании инцидента: {str(e)}")


@app.get("/incidents", summary="Список инцидентов", tags=main_tag, response_model=List[IncidentResponse])
def get_incidents(status: Optional[StatusEnum] = Query(None), db: Session = Depends(init_db)):
    """Получение списка инцидентов"""
    query = db.query(Incident)
    if status:
        query = query.filter(Incident.status == status)
    incidents = query.all()
    return incidents


@app.get("/incidents/{incident_id}", summary="Получить конкретный инцидент", tags=main_tag, response_model=IncidentResponse)
def get_incident(incident_id: int, db: Session = Depends(init_db)):
    """Получение конкретного инцидента по ID"""
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Инцидент не найден")
    return incident


@app.patch("/incidents/{incident_id}", summary="Обновить статус инцидента", tags=main_tag, response_model=IncidentResponse, status_code=200)
def update_incident(incident_id: int, incident_update: IncidentUpdate, db: Session = Depends(init_db)):
    """Обновление статуса инцидента по его ID"""
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if not incident:
        raise HTTPException(404, "Инцидент не найден")

    incident.status = incident_update.status

    try:
        db.commit()
        db.refresh(incident)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Ошибка при обновлении статуса инцидента: {str(e)}")

    return incident