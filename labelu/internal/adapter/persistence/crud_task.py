from typing import Any, Dict, List

from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from labelu.internal.domain.models.task import Task


def create(db: Session, task: Task) -> Task:
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def list_by(db: Session, owner_id: int, page: int = 0, size: int = 100) -> List[Task]:
    return (
        db.query(Task)
        .filter(Task.created_by == owner_id)
        .order_by(Task.id.desc())
        .offset(offset=page * size)
        .limit(limit=size)
        .all()
    )


def get(db: Session, task_id: str) -> Task:
    return db.query(Task).filter(Task.id == task_id).first()


def update(db: Session, db_obj: Task, obj_in: Dict[str, Any]) -> Task:
    obj_data = jsonable_encoder(obj_in)
    for field in obj_data:
        if field in obj_in:
            setattr(db_obj, field, obj_in[field])
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def delete(db: Session, db_obj: Task) -> None:
    db.delete(db_obj)
    db.commit()


def count(db: Session, owner_id: int) -> List[Task]:
    return db.query(Task).filter(Task.created_by == owner_id).count()
