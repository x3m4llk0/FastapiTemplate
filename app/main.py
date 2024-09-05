from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.test_routers import router as test_router
from app.core.logger import logger
from app.middlewares.log_requests import LogRequestsMiddleware

app = FastAPI(
    title='FastAPI Template',
    description='FastAPI Template for OtherCode',
    debug=True
)

origins = [
    "*"
]

# Подключение роутера
app.include_router(test_router)

# Добавление CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=[
        "Content-Type",
        "Set-Cookie",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
        "Authorization",
    ],
)

# Добавление вашего кастомного Middleware
# app.add_middleware(LogRequestsMiddleware)

@app.on_event("startup")
async def startup_event():
    pass

@app.on_event("shutdown")
async def shutdown_event():
    pass