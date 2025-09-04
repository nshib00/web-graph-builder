import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.router import app_router

app = FastAPI()

app.include_router(app_router)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

if __name__ == "__main__":
    uvicorn.run("app.main:app", port=2016, reload=True)
