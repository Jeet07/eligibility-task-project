from sqlalchemy.orm import Session
from models import User, Task, TaskAssignment
from celery_app import celery_app
from redis_config import eligibility_cache, task_cache
import json

def check_eligibility(user, task_rules):
    if task_rules.get("department"):
        if user.department != task_rules["department"]:
            return False
    
    if task_rules.get("min_experience"):
        if user.experience < task_rules["min_experience"]:
            return False
    
    if task_rules.get("location"):
        if user.location != task_rules["location"]:
            return False
    
    if task_rules.get("max_tasks"):
        if user.active_tasks >= task_rules["max_tasks"]:
            return False
    
    return True

@celery_app.task
def recompute_task_eligibility(task_id):
    from database import SessionLocal
    db = SessionLocal()
    
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        return
    
    all_users = db.query(User).filter(User.role == "User").all()
    eligible_users = []
    
    for user in all_users:
        if check_eligibility(user, task.rules):
            eligible_users.append(user)
    
    db.query(TaskAssignment).filter(TaskAssignment.task_id == task_id).delete()
    
    for user in eligible_users:
        assignment = TaskAssignment(
            task_id=task_id,
            user_id=user.id,
            eligible=True
        )
        db.add(assignment)
    
    db.commit()
    
    if len(eligible_users) == 0:
        task.assigned_to = None
    else:
        best_user = min(eligible_users, key=lambda u: u.active_tasks)
        task.assigned_to = best_user.id
        best_user.active_tasks += 1
    
    db.commit()
    
    # Store in cache
    user_ids = [u.id for u in eligible_users]
    eligibility_cache.set(f"task_eligible_{task_id}", user_ids, ttl=3600)
    
    # Clear user caches
    for user in eligible_users:
        task_cache.delete(f"user_tasks_{user.id}")
    
    db.close()
    return {"task_id": task_id, "eligible_count": len(eligible_users)}

@celery_app.task
def recompute_user_eligibility(user_id):
    from database import SessionLocal
    db = SessionLocal()
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return
    
    all_tasks = db.query(Task).filter(Task.assigned_to.is_(None)).all()
    
    for task in all_tasks:
        if check_eligibility(user, task.rules):
            existing = db.query(TaskAssignment).filter(
                TaskAssignment.task_id == task.id,
                TaskAssignment.user_id == user_id
            ).first()
            if not existing:
                assignment = TaskAssignment(task_id=task.id, user_id=user_id, eligible=True)
                db.add(assignment)
    
    db.commit()
    
    # Clear user cache
    task_cache.delete(f"user_tasks_{user_id}")
    
    db.close()

@celery_app.task
def recompute_all_tasks():
    from database import SessionLocal
    db = SessionLocal()
    
    all_tasks = db.query(Task).all()
    for task in all_tasks:
        recompute_task_eligibility.delay(task.id)
    
    db.close()
