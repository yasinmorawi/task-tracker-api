from sqlmodel import create_engine, Session
from task_tracker_api.config import settings

# Membuat engine database menggunakan URL dari settings (.env)
engine = create_engine(settings.database_url, echo=True)

# Dependency untuk mendapatkan session database di FastAPI
def get_db():
    with Session(engine) as session:
        yield session