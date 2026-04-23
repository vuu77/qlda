from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Float, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(String(50), default='member')
    created_at = Column(DateTime, default=datetime.utcnow)

    led_projects = relationship('Project', back_populates='manager')


class Project(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True, index=True)
    project_code = Column(String(50), unique=True, index=True, nullable=False)
    project_name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    manager_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    team_name = Column(String(255), nullable=True)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    manager = relationship('User', back_populates='led_projects')
    tasks = relationship('Task', back_populates='project', cascade='all, delete-orphan')
    schedules = relationship('ProjectSchedule', back_populates='project', cascade='all, delete-orphan')


class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    task_name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    assigned_to = Column(String(255), nullable=True)
    estimated_expert_hours = Column(Float, default=0)
    actual_hours = Column(Float, default=0)
    hourly_rate = Column(Float, default=0)
    estimated_cost = Column(Float, default=0)
    status = Column(String(50), default='pending')
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    project = relationship('Project', back_populates='tasks')
    schedules = relationship('TaskSchedule', back_populates='task', cascade='all, delete-orphan')


class ProjectSchedule(Base):
    __tablename__ = 'project_schedules'

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    milestone_name = Column(String(255), nullable=False)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    note = Column(Text, nullable=True)

    project = relationship('Project', back_populates='schedules')


class TaskSchedule(Base):
    __tablename__ = 'task_schedules'

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey('tasks.id'), nullable=False)
    work_date = Column(Date, nullable=True)
    note = Column(Text, nullable=True)

    task = relationship('Task', back_populates='schedules')
