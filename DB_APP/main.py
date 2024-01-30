from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from DB_APP.routers import workPlaces, users

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(workPlaces.router)
