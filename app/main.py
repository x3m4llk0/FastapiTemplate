

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI


# from apscheduler.schedulers.asyncio import AsyncIOScheduler

app = FastAPI()
# scheduler = AsyncIOScheduler()

# app.include_router(users_router)


# Подключение CORS, чтобы запросы к API могли приходить из браузера
origins = [
    "*"
]

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

#
# @app.on_event("startup")
# async def startup_event():
#     scheduler.add_job(check_dating_tasks, "interval", hours=12)
#     # scheduler.add_job(check_dating_tasks, "cron", hour=2, minute=0)
#     scheduler.start()
#
#
# @app.on_event("shutdown")
# async def shutdown_event():
#     scheduler.shutdown()

