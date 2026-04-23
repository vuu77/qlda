from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import date, datetime


class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    role: Optional[str] = 'member'


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    role: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ProjectCreate(BaseModel):
    project_code: str
    project_name: str
    description: Optional[str] = None
    manager_id: int
    team_name: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None


class ProjectOut(BaseModel):
    id: int
    project_code: str
    project_name: str
    description: Optional[str] = None
    manager_id: int
    team_name: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None

    class Config:
        from_attributes = True


class TaskCreate(BaseModel):
    project_id: int
    task_name: str
    description: Optional[str] = None
    assigned_to: Optional[str] = None
    estimated_expert_hours: Optional[float] = 0
    actual_hours: Optional[float] = 0
    hourly_rate: Optional[float] = 0
    estimated_cost: Optional[float] = 0
    status: Optional[str] = 'pending'
    start_date: Optional[date] = None
    end_date: Optional[date] = None


class TaskOut(BaseModel):
    id: int
    project_id: int
    task_name: str
    description: Optional[str] = None
    assigned_to: Optional[str] = None
    estimated_expert_hours: float
    actual_hours: float
    hourly_rate: float
    estimated_cost: float
    status: str
    start_date: Optional[date] = None
    end_date: Optional[date] = None

    class Config:
        from_attributes = True


class ProjectScheduleCreate(BaseModel):
    project_id: int
    milestone_name: str
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    note: Optional[str] = None


class ProjectScheduleOut(BaseModel):
    id: int
    project_id: int
    milestone_name: str
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    note: Optional[str] = None

    class Config:
        from_attributes = True


class TaskScheduleCreate(BaseModel):
    task_id: int
    work_date: Optional[date] = None
    note: Optional[str] = None


class TaskScheduleOut(BaseModel):
    id: int
    task_id: int
    work_date: Optional[date] = None
    note: Optional[str] = None

    class Config:
        from_attributes = True


class ProjectSummary(BaseModel):
    project_code: str
    total_tasks: int
    total_estimated_hours: float
    total_estimated_cost: float
