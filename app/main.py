from fastapi import FastAPI
from app.routes import translate
from app.db.logger import init_db

app = FastAPI(title="Udaan Next Gen - Translation Microservice")

@app.on_event("startup")
def startup_event():
    init_db()

app.include_router(translate.router)