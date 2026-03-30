from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import engine, get_db, Base
from models import User, Task, TaskAssignment
from schemas import UserCreate, UserLogin, TaskCreate, TaskUpdate, Token
from auth import (
    get_password_hash,
    verify_password,
    create_access_token,
    get_current_user,
    check_admin,
)
from assignment_engine import (
    recompute_task_eligibility,
    recompute_user_eligibility,
    recompute_all_tasks,
)
from redis_config import task_cache, eligibility_cache

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Task Management System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- AUTH ----------------
@app.post("/signup")
def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user_data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")

    new_user = User(
        email=user_data.email,
        password=get_password_hash(user_data.password),
        department=user_data.department,
        experience=user_data.experience,
        location=user_data.location,
        #role="User",
	role=user_data.role,
    )
    db.add(new_user)
    db.commit()
    return {"message": "User created", "user_id": new_user.id}


@app.post("/login", response_model=Token)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_data.email).first()
    if not user or not verify_password(user_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": str(user.id), "role": user.role})
    return {"access_token": token, "token_type": "bearer"}


# ---------------- TASK CRUD ----------------
@app.post("/tasks/")
def create_task(task_data: TaskCreate, admin: User = Depends(check_admin), db: Session = Depends(get_db)):
    new_task = Task(
        title=task_data.title,
        description=task_data.description,
        priority=task_data.priority,
        due_date=task_data.due_date,
        rules=task_data.rules,
        created_by=admin.id,
        status="Todo",
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    recompute_task_eligibility.delay(new_task.id)

    return {"task_id": new_task.id}

@app.post("/tasks/recompute-eligibility")
def recompute_all(admin: User = Depends(check_admin)):
    recompute_all_tasks.delay()
    return {"message": "Recomputation started"}

@app.put("/user/profile")
def update_profile(user_data: dict, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    for key, value in user_data.items():
        if hasattr(current_user, key):
            setattr(current_user, key, value)
    
    db.commit()
    recompute_user_eligibility.delay(current_user.id)
    task_cache.delete(f"user_tasks_{current_user.id}")
    
    return {"message": "Profile updated"}

@app.get("/user/profile")
def get_profile(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "department": current_user.department,
        "experience": current_user.experience,
        "location": current_user.location,
        "role": current_user.role
    }

@app.put("/tasks/{task_id}/status")
def update_status(task_id: int, status: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if task.assigned_to != current_user.id and current_user.role != "Admin":
        raise HTTPException(status_code=403, detail="Not assigned")
    
    old_status = task.status
    task.status = status
    
    if status == "Done" and old_status != "Done":
        current_user.active_tasks = max(0, current_user.active_tasks - 1)
    
    db.commit()
    task_cache.delete(f"user_tasks_{current_user.id}")
    
    return {"message": f"Status updated to {status}"}
    
@app.get("/tasks/{task_id}")
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.put("/tasks/{task_id}")
def update_task(task_id: int, task_data: TaskUpdate, admin: User = Depends(check_admin), db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    for key, value in task_data.dict(exclude_unset=True).items():
        setattr(task, key, value)

    db.commit()

    return {"message": "Task updated"}


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, admin: User = Depends(check_admin), db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task:
        db.delete(task)
        db.commit()
    return {"message": "Task deleted"}


# ---------------- NEW: CREATED TASK APIs ----------------

# Get tasks created by logged-in user
@app.get("/my-created-tasks")
def get_my_created_tasks(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    tasks = db.query(Task).filter(Task.created_by == current_user.id).all()

    return {
        "tasks": [
            {
                "id": t.id,
                "title": t.title,
                "status": t.status,
                "priority": t.priority,
                "due_date": t.due_date,
                "assigned_to": t.assigned_to,
		"rules": t.rules
            }
            for t in tasks
        ]
    }


# Admin: get tasks created by any user
@app.get("/users/{user_id}/created-tasks")
def get_tasks_created_by_user(user_id: int, admin: User = Depends(check_admin), db: Session = Depends(get_db)):
    tasks = db.query(Task).filter(Task.created_by == user_id).all()

    return {
        "tasks": [
            {
                "id": t.id,
                "title": t.title,
                "status": t.status,
                "priority": t.priority,
                "due_date": t.due_date,
            }
            for t in tasks
        ]
    }


# ---------------- ELIGIBILITY ----------------
@app.get("/tasks/{task_id}/eligible-users")
def get_eligible_users(task_id: int, db: Session = Depends(get_db)):
    assignments = db.query(TaskAssignment).filter(
        TaskAssignment.task_id == task_id,
        TaskAssignment.eligible == True,
    ).all()

    user_ids = [a.user_id for a in assignments]
    users = db.query(User).filter(User.id.in_(user_ids)).all()

    return {"users": [{"id": u.id, "email": u.email} for u in users]}


@app.get("/my-eligible-tasks")
def my_eligible_tasks(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    assignments = db.query(TaskAssignment).filter(
        TaskAssignment.user_id == current_user.id,
        TaskAssignment.eligible == True,
    ).all()

    task_ids = [a.task_id for a in assignments]
    tasks = db.query(Task).filter(Task.id.in_(task_ids)).all()

    return {"tasks": tasks}


# ---------------- CACHE OPS ----------------
@app.post("/cache/clear")
def clear_cache(admin: User = Depends(check_admin)):
    task_cache.delete_pattern("*")
    eligibility_cache.delete_pattern("*")
    return {"message": "Cache cleared"}
