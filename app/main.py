from fastapi import FastAPI

from app.api.auth import auth_rout

app = FastAPI()

app.include_router(auth_rout)
