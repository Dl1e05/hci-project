from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import main_router

app = FastAPI()

origins = ['http://localhost', 'http://localhost:3000']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(main_router)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the FastAPI application!"}