from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from api.v1.test_routers import router as test_router

# from apscheduler.schedulers.asyncio import AsyncIOScheduler

def main_app():
    app = FastAPI(
        title='Simple Project',
        docs_url='/api/docs',
        description='A simple project template',
        debug=True
    )

    origins = [
        "*"
    ]

    app.include_router(test_router)

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

    return app
# scheduler = AsyncIOScheduler()



# Подключение CORS, чтобы запросы к API могли приходить из браузера


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
