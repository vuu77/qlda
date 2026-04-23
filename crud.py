from sqlalchemy.orm import Session
import models, schemas


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        full_name=user.full_name,
        email=user.email,
        password=user.password,
        role=user.role or 'member'
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, user: schemas.UserLogin):
    db_user = get_user_by_email(db, user.email)
    if not db_user:
        return None
    if db_user.password != user.password:
        return None
    return db_user


def get_all_users(db: Session):
    return db.query(models.User).all()


def create_project(db: Session, project: schemas.ProjectCreate):
    db_project = models.Project(**project.dict())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


def get_project_by_code(db: Session, project_code: str):
    return db.query(models.Project).filter(models.Project.project_code == project_code).first()


def get_all_projects(db: Session):
    return db.query(models.Project).all()


def create_task(db: Session, task: schemas.TaskCreate):
    data = task.dict()
    if not data.get('estimated_cost'):
        data['estimated_cost'] = (data.get('estimated_expert_hours', 0) or 0) * (data.get('hourly_rate', 0) or 0)
    db_task = models.Task(**data)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def get_tasks_by_project(db: Session, project_id: int):
    return db.query(models.Task).filter(models.Task.project_id == project_id).all()


def create_project_schedule(db: Session, schedule: schemas.ProjectScheduleCreate):
    db_schedule = models.ProjectSchedule(**schedule.dict())
    db.add(db_schedule)
    db.commit()
    db.refresh(db_schedule)
    return db_schedule


def get_project_schedules(db: Session, project_id: int):
    return db.query(models.ProjectSchedule).filter(models.ProjectSchedule.project_id == project_id).all()


def create_task_schedule(db: Session, schedule: schemas.TaskScheduleCreate):
    db_schedule = models.TaskSchedule(**schedule.dict())
    db.add(db_schedule)
    db.commit()
    db.refresh(db_schedule)
    return db_schedule


def get_task_schedules(db: Session, task_id: int):
    return db.query(models.TaskSchedule).filter(models.TaskSchedule.task_id == task_id).all()


def get_project_summary(db: Session, project_code: str):
    project = get_project_by_code(db, project_code)
    if not project:
        return None
    tasks = get_tasks_by_project(db, project.id)
    return {
        'project_code': project.project_code,
        'total_tasks': len(tasks),
        'total_estimated_hours': sum((t.estimated_expert_hours or 0) for t in tasks),
        'total_estimated_cost': sum((t.estimated_cost or 0) for t in tasks),
    }
