from fastapi import APIRouter, Depends, status, HTTPException
from slugify import slugify
from sqlalchemy.orm import Session
from typing import Annotated
from sqlalchemy import insert, select, update, delete

from app.backend.db_depends import get_db
from app.schemas import CreateTask, UpdateTask
from app.models import *


router = APIRouter(prefix='/task', tags=['task'])


@router.get('/')
async def all_tasks(db: Annotated[Session, Depends(get_db)]):
    return db.scalars(select(Task)).all()


@router.get('/task_id')
async def task_by_id(db: Annotated[Session, Depends(get_db)],
                     task_id: int):
    task_ = db.scalar(select(Task).where(Task.id == task_id))
    if task_ is None:
        raise HTTPException(status_code=404,
                            detail='Task was not found')
    return task_


@router.post('/create')
async def create_task(db: Annotated[Session, Depends(get_db)],
                      create_task_: CreateTask,
                      user_id: int):
    user_ = db.scalar(select(User).where(User.id == user_id))
    if user_ is None:
        raise HTTPException(status_code=404,
                            detail='User was not found')
    db.execute(insert(Task).values(title=create_task_.title,
                                   content=create_task_.content,
                                   priority=create_task_.priority,
                                   user_id=user_id,
                                   slug=slugify(create_task_.title)))
    db.commit()
    return {'status_code': status.HTTP_201_CREATED,
            'transaction': 'Successful'}


@router.put('/update')
async def update_task(db: Annotated[Session, Depends(get_db)],
                      update_task_: UpdateTask,
                      task_id: int):
    task_ = db.scalar(select(Task).where(Task.id == task_id))
    if task_ is None:
        raise HTTPException(status_code=404,
                            detail='Task was not found')
    db.execute(update(Task).where(Task.id == task_id).values(title=update_task_.title,
                                                             content=update_task_.content,
                                                             priority=update_task_.priority,
                                                             slug=slugify(update_task_.title)))
    db.commit()
    return {'status_code': status.HTTP_200_OK,
            'transaction': 'Task update is successful!'}


@router.delete('/delete')
async def delete_task(db: Annotated[Session, Depends(get_db)],
                      task_id: int):
    task_ = db.scalar(select(Task).where(Task.id == task_id))
    if task_ is None:
        raise HTTPException(status_code=404,
                            detail='Task was not found')
    db.execute(delete(Task).where(Task.id == task_id))
    db.commit()
    return {'status_code': status.HTTP_200_OK,
            'transaction': 'Task delete is successful!'}