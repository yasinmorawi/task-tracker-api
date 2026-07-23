from fastapi import FastAPI

from task_tracker_api.routers import tasks, auth


app = FastAPI(title="Task Tracker API")

app.include_router(tasks.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "Welcome to Task Tracker API!"}