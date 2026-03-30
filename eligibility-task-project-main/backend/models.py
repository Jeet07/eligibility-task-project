from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, JSON
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(String, default="User")
    department = Column(String)
    experience = Column(Integer)
    location = Column(String)
    active_tasks = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(Text)
    status = Column(String, default="Todo")
    priority = Column(String)
    due_date = Column(DateTime)
    rules = Column(JSON)
    assigned_to = Column(Integer, nullable=True)
    created_by = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

class TaskAssignment(Base):
    __tablename__ = "task_assignments"
    
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, index=True)
    user_id = Column(Integer, index=True)
    eligible = Column(Boolean, default=False)
    assigned_at = Column(DateTime, default=datetime.utcnow)
