from fastapi import FastAPI, Depends, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List
import os

import database
import models
import schemas
import crud

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="IT Project Management API")

# =========================
# CORS
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# PATHS
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.abspath(os.path.join(BASE_DIR, "../frontend"))
ASSETS_DIR = os.path.join(FRONTEND_DIR, "assets")

# Serve assets: css / js / images
if os.path.isdir(ASSETS_DIR):
    app.mount("/assets", StaticFiles(directory=ASSETS_DIR), name="assets")


# =========================
# DB
# =========================
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =========================
# AUTH HELPER
# =========================
def verify_token(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer token-"):
        raise HTTPException(status_code=401, detail="Bạn chưa đăng nhập")
    try:
        return int(authorization.split("-")[1])
    except Exception:
        raise HTTPException(status_code=401, detail="Token không hợp lệ")


# =========================
# FRONTEND ROUTES
# =========================
@app.get("/")
def serve_root():
    login_file = os.path.join(FRONTEND_DIR, "login.html")
    if os.path.isfile(login_file):
        return FileResponse(login_file)
    return {"message": "Không tìm thấy frontend/login.html"}


@app.get("/login.html")
def serve_login():
    login_file = os.path.join(FRONTEND_DIR, "login.html")
    if os.path.isfile(login_file):
        return FileResponse(login_file)
    return {"message": "Không tìm thấy frontend/login.html"}


@app.get("/index.html")
def serve_index():
    index_file = os.path.join(FRONTEND_DIR, "index.html")
    if os.path.isfile(index_file):
        return FileResponse(index_file)
    return {"message": "Không tìm thấy frontend/index.html"}


@app.get("/health")
def health():
    return {
        "status": "ok",
        "frontend_dir": FRONTEND_DIR,
        "assets_dir": ASSETS_DIR
    }


# =========================
# AUTH
# =========================
@app.post("/auth/register", response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_user(db, user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email đã tồn tại")


@app.post("/auth/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = crud.authenticate_user(db, user)
    if not db_user:
        raise HTTPException(status_code=401, detail="Sai email hoặc mật khẩu")

    return {
        "access_token": f"token-{db_user.id}",
        "user_info": {
            "id": db_user.id,
            "name": db_user.full_name,
            "email": db_user.email,
            "role": db_user.role
        }
    }


# =========================
# USERS
# =========================
@app.get("/users", response_model=List[schemas.UserOut])
def read_users(
    db: Session = Depends(get_db),
    user_id: int = Depends(verify_token)
):
    return crud.get_all_users(db)


# =========================
# PROJECTS
# =========================
@app.post("/projects", response_model=schemas.ProjectOut)
def create_project(
    project: schemas.ProjectCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(verify_token)
):
    return crud.create_project(db, project)


@app.get("/projects", response_model=List[schemas.ProjectOut])
def read_projects(
    db: Session = Depends(get_db),
    user_id: int = Depends(verify_token)
):
    return crud.get_all_projects(db)


@app.get("/projects/by-code/{project_code}", response_model=schemas.ProjectOut)
def read_project_by_code(
    project_code: str,
    db: Session = Depends(get_db),
    user_id: int = Depends(verify_token)
):
    project = crud.get_project_by_code(db, project_code)
    if not project:
        raise HTTPException(status_code=404, detail="Không tìm thấy dự án")
    return project


@app.get("/projects/{project_code}/summary", response_model=schemas.ProjectSummary)
def read_project_summary(
    project_code: str,
    db: Session = Depends(get_db),
    user_id: int = Depends(verify_token)
):
    summary = crud.get_project_summary(db, project_code)
    if not summary:
        raise HTTPException(status_code=404, detail="Không tìm thấy dự án")
    return summary


# =========================
# TASKS
# =========================
@app.post("/tasks", response_model=schemas.TaskOut)
def create_task(
    task: schemas.TaskCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(verify_token)
):
    return crud.create_task(db, task)


@app.get("/projects/{project_id}/tasks", response_model=List[schemas.TaskOut])
def read_tasks_by_project(
    project_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(verify_token)
):
    return crud.get_tasks_by_project(db, project_id)


# =========================
# PROJECT SCHEDULES
# =========================
@app.post("/project-schedules", response_model=schemas.ProjectScheduleOut)
def create_project_schedule(
    schedule: schemas.ProjectScheduleCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(verify_token)
):
    return crud.create_project_schedule(db, schedule)


@app.get("/projects/{project_id}/schedules", response_model=List[schemas.ProjectScheduleOut])
def read_project_schedules(
    project_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(verify_token)
):
    return crud.get_project_schedules(db, project_id)


# =========================
# TASK SCHEDULES
# =========================
@app.post("/task-schedules", response_model=schemas.TaskScheduleOut)
def create_task_schedule(
    schedule: schemas.TaskScheduleCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(verify_token)
):
    return crud.create_task_schedule(db, schedule)


@app.get("/tasks/{task_id}/schedules", response_model=List[schemas.TaskScheduleOut])
def read_task_schedules(
    task_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(verify_token)
):
    return crud.get_task_schedules(db, task_id)