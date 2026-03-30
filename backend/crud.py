from sqlalchemy.orm import Session
from models import User, Task

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_user_tasks(db: Session, user_id: int):
    return db.query(Task).filter(Task.assigned_to == user_id).all()

def update_user_active_tasks(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        task_count = db.query(Task).filter(Task.assigned_to == user_id, Task.status != "Done").count()
        user.active_tasks = task_count
        db.commit()
