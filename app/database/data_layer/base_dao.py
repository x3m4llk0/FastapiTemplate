from functools import wraps
from uuid import UUID
from typing import Union, TypeVar, Generic, Type, Sequence
from abc import ABC

from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logger import logger

from app.database.postgres import async_session_maker, Base


TABLE_MODEL = TypeVar("TABLE_MODEL", bound=Base)


def transaction_handler(func):
    """
    Декоратор для обработки транзакций и логирования ошибок в DAO методах.

    Выполняет указанную функцию внутри транзакции и логирует ошибки, если они возникают.

    Args:
        func (Callable): Функция DAO, которая будет обернута в декоратор.

    Returns:
        Callable: Функция-декоратор для обработки транзакций и логирования ошибок.
    """

    @wraps(func)
    async def wrapper(cls, *args, **kwargs):
        async with async_session_maker() as session:
            try:
                return await func(cls, *args, **kwargs, session=session)
            except Exception as e:
                cls._log_error(e, func.__name__)

    return wrapper


class BaseDAO(ABC, Generic[TABLE_MODEL]):
    """
    Базовый класс DAO (Data Access Object) для работы с базой данных.

    Этот класс предоставляет основные методы для выполнения CRUD операций с использованием SQLAlchemy.

    Примечание:
        Класс `BaseDAO` предназначен для наследования. Чтобы создать DAO для конкретной
        модели, нужно создать подкласс, установить атрибут `model` на нужную модель и,
        при необходимости, добавить или переопределить методы для расширения функциональности.
    """
    model: TABLE_MODEL

    @classmethod
    @transaction_handler
    async def find_one_or_none(cls, session: AsyncSession, **filter_by) -> Type[TABLE_MODEL] | None:
        """
        Находит одну запись в базе данных, соответствующую заданным критериям фильтрации,
        или возвращает None, если такая запись не найдена.

        Args:
            session (Session): Получаем от декоратора @transaction_handler
            filter_by (dict): Параметры для фильтрации записей.

        Returns:
            Base: Один экземпляр модели, соответствующий критериям фильтрации, или None.
        """
        query = select(cls.model).filter_by(**filter_by)
        result = await session.execute(query)
        return result.scalars().one_or_none()

    @classmethod
    @transaction_handler
    async def find_all(cls, session: AsyncSession, **filter_by) -> Sequence[Type[TABLE_MODEL]]:
        """
        Находит все записи в базе данных, соответствующие заданным критериям фильтрации.

        Args:
            session (Session): Получаем от декоратора @transaction_handler
            filter_by (dict): Параметры для фильтрации записей.

        Returns:
            list[Base]: Список экземпляров модели, соответствующих критериям фильтрации.
        """
        query = select(cls.model).filter_by(**filter_by)
        result = await session.execute(query)
        return result.scalars().all()

    @classmethod
    @transaction_handler
    async def create(cls, session: AsyncSession, **data) -> Type[TABLE_MODEL] | None:
        """
        Создает новую запись в базе данных с заданными данными.

        Args:
            session (Session): Получаем от декоратора @transaction_handler
            data (dict): Данные для создания новой записи.

        Returns:
            Base: Экземпляр созданной модели или None в случае ошибки.
        """
        query = insert(cls.model).values(**data).returning(cls.model)
        result = await session.execute(query)
        await session.commit()
        return result.scalars().first()

    @classmethod
    @transaction_handler
    async def get_paginated(
        cls,
        session: AsyncSession,
        offset: int,
        limit: int,
        **filter_data
    ) -> Sequence[Type[TABLE_MODEL]]:
        """
        Возвращает пагинированный список записей модели.

        Args:
            session (Session): Получаем от декоратора @transaction_handler
            offset (int): Смещение, с которого начинается выборка записей.
            limit (int): Количество записей для выборки.
            filter_data (dict): Опциональный фильтр для фильтрации записей.

        Returns:
            list[Base]: Список экземпляров модели в заданном диапазоне.
        """
        query = select(cls.model).filter_by(**filter_data).offset(offset).limit(limit)
        result = await session.execute(query)
        return result.scalars().all()

    @classmethod
    @transaction_handler
    async def update_by_id(
        cls,
        session: AsyncSession,
        id_field: str,
        id_value: Union[str, int, UUID],
        update_data: dict
    ) -> Type[TABLE_MODEL] | None:
        """
        Обновляет запись по заданному идентификатору с использованием предоставленных данных.

        Args:
            session (Session): Получаем от декоратора @transaction_handler
            id_field (str): Имя поля, которое является идентификатором.
            id_value (Union[str, int]): Значение идентификатора записи для обновления.
            update_data (dict): Словарь с данными для обновления.

        Returns:
            Base: Обновленный экземпляр модели или None, если обновление не удалось.
        """
        query = update(cls.model).where(getattr(cls.model, id_field) == id_value).values(**update_data)
        await session.execute(query)
        await session.commit()
        return await cls.find_one_or_none(**{id_field: id_value})

    @classmethod
    @transaction_handler
    async def delete_by_id(cls, session: AsyncSession, id_field: str, id_value: Union[str, int, UUID]) -> bool:
        """
        Удаляет запись по заданному идентификатору.

        Args:
            session (Session): Получаем от декоратора @transaction_handler
            id_field (str): Имя поля, которое является идентификатором.
            id_value (Union[str, int]): Значение идентификатора для удаления записи.

        Returns:
            bool: Возвращает True, если запись была успешно удалена, иначе False.
        """
        query = delete(cls.model).where(getattr(cls.model, id_field) == id_value)
        result = await session.execute(query)
        await session.commit()
        return result.rowcount > 0

    @classmethod
    def _log_error(cls, e: Exception, operation: str) -> None:
        """
        Логирует ошибки, возникающие при выполнении операций с базой данных.

        Args:
            e (Exception): Исключение, которое произошло.
            operation (str): Название операции для логирования.
        """
        if isinstance(e, SQLAlchemyError):
            msg = f"Database Exc: Cannot {operation} data in table"
        else:
            msg = f"Unknown Exc: Cannot {operation} data in table"
        logger.error(msg, extra={"table": cls.model.__tablename__}, exc_info=True)
