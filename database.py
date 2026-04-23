from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Thông tin kết nối
DB_SERVER = "TRUNGNGUYEN"
DB_NAME = "ITProjectManagementDB"
DB_USER = "sa"
DB_PASSWORD = "26102002"
DB_DRIVER = "ODBC+Driver+17+for+SQL+Server"

# Tạo connection string tách rời
SQLALCHEMY_DATABASE_URL = f"mssql+pyodbc://{DB_USER}:{DB_PASSWORD}@{DB_SERVER}/{DB_NAME}?driver={DB_DRIVER}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency cho FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()