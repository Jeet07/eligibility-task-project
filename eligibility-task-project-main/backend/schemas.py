from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, Dict

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    department: str
    experience: int
    location: str
    role:str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TaskCreate(BaseModel):
    title: str
    description: str
    priority: str
    due_date: datetime
    rules: Dict

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    rules: Optional[Dict] = None

class Token(BaseModel):
    access_token: str
    token_type: str
