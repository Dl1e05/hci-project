from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import main_router

app = FastAPI()

origins = [
    'http://localhost',
    'http://localhost:3000',
    'http://localhost:8000',
    'http://frontend:3000',  # Docker internal
    'http://backend:8000',    # Docker internal
]

# Allow all origins in development (adjust for production)
if True:  # Set to False in production or use environment variable
    origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(main_router)


@app.get('/')
async def read_root() -> dict:
    return {'message': 'Welcome to the FastAPI application!'}


@app.get('/health')
async def health_check() -> dict:
    return {'status': 'healthy'}
