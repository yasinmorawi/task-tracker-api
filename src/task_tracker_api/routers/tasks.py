from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session, select

from task_tracker_api.database import get_db
from task_tracker_api.dependencies import get_current_user
from task_tracker_api.models import User, Task
from task_tracker_api.schemas import TaskCreate, TaskRead, TaskUpdate

router = APIRouter(prefix="/tasks", tags=['tasks'])

@router.post("/", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(
    task_in: TaskCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user),
): 
    # BUat instance Task baru, pastikan user_id diikat erat ke current_user.id (Mencegah IDOR)
    new_task = Task(
        **task_in.model_dump(),
        user_id=current_user.id
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task

@router.get("/", response_model=list[TaskRead])
def list_tasks(
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user),
    skip: int = Query(0, ge=0), 
    limit: int = Query(20, ge=1, le=100),
):
    # Hanya query task user_id nya cocok dengan current_user.id, terapkan skip dan limit
   stmt = (
        select(Task)
        .where(Task.user_id == current_user.id)
        .order_by(Task.created_at.desc())
        .offset(skip)
        .limit(limit)
)
   tasks = db.scalars(stmt).all()

   return tasks

@router.get("/{task_id}", response_model=TaskRead)
def get_task(
    task_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user), 
):
    # Langsung jadikan filetr user_id == current_user.id sebagai bagian dari query utama
    stmt = select(Task).where(Task.id == task_id, Task.user_id == current_user.id)
    task = db.scalars(stmt).first()

    # REturn 404 Not Found secara seragam untuk mencegah IDOR/Information Disclosure
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return task

@router.patch("/{task_id}", response_model=TaskRead)
def update_task(
    task_id: int, 
    task_update: TaskUpdate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user),
):

    # Gunakan SQLModel query dengan filter ownership.
    stmt = select(Task).where(Task.id == task_id, Task.user_id == current_user.id)
    task = db.scalars(stmt).first()

    if not task: 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Task not found"
        )

    # Partial update: hanya ambil field yang dikirim client 
    update_data = task_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)

    return task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user),
):
    # Cek kepemilikan task sebelum menghapus
    stmt = select (Task).where(Task.id == task_id, Task.user_id == current_user.id)
    task = db.scalars(stmt).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    db.delete(task)
    db.commit()

    return