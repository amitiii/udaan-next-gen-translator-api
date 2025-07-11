
from fastapi import FastAPI
from app.routes.translate import router
from app.db.logger import init_db

app = FastAPI(title="Udaan Next-Gen Translation Service")

app.include_router(router)

@app.on_event("startup")
def on_startup():
    init_db()
