import asyncio
from dotenv import load_dotenv
import argparse
import json
from datetime import datetime
import uuid
import random
from sqlalchemy import insert, text

from app.core.logger import logger
from app.database.postgres.database import Base, async_session_maker, engine

# Без импортов моделей не сработает метадата
# from app.models.file import Models

# Загрузка переменных окружения из файла .env
load_dotenv(".env")


async def drop_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def drop_alembic():
    async with engine.begin() as conn:
        await conn.execute(text(f"DROP TABLE IF EXISTS alembic_version CASCADE"))


async def create_database():
    async with engine.begin() as conn:
        # Добавление всех заданных нами таблиц из БД
        await conn.run_sync(Base.metadata.create_all)


async def prepare_database():
    def open_mock_json(model: str):
        with open(f"app/tests/mocks/mock_{model}.json", encoding="utf-8") as file:
            return json.load(file)

    models = open_mock_json("models")
    async with async_session_maker() as session:
        for Model, values in [
            (Models, models)
        ]:
            query = insert(Model).values(values)
            await session.execute(query)
        await session.commit()


async def setup_database():
    await drop_database()
    logger.info("DB delete success")
    await create_database()
    logger.info("DB create success")
    await prepare_database()
    logger.info("DB prepare success")


async def main():
    '''
    Запуск функций из консоли
    '''
    parser = argparse.ArgumentParser(description="Управление базой данных.")
    parser.add_argument("action", choices=["drop", "create", "prepare", "setup", "alembic"],
                        help="Действие для выполнения")
    args = parser.parse_args()
    if args.action == "drop":
        await drop_database()
        logger.info("DB delete success")
    elif args.action == "create":
        await create_database()
        logger.info("DB create success")
    elif args.action == "prepare":
        await prepare_database()
        logger.info("DB prepare success")
    elif args.action == "setup":
        await setup_database()
        logger.info("DB setup success")
    elif args.action == "alembic":
        await drop_alembic()
        logger.info("Alembic drop success")


if __name__ == "__main__":
    asyncio.run(main())
