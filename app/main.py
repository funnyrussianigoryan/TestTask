from fastapi import FastAPI

from app.api.auth import auth_rout
from app.api.users import users_rout
from app.api.current_salary import current_salary_rout

app = FastAPI()

app.include_router(auth_rout)
app.include_router(users_rout)
app.include_router(current_salary_rout)
