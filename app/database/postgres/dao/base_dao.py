from typing import List, Optional, Union, Type, Dict

from sqlalchemy import delete, insert, select, update, inspect
from sqlalchemy.exc import SQLAlchemyError, InterfaceError
from sqlalchemy.orm import Session

from app.core.logger import logger

from app.db.database import async_session_maker, Base


class BaseDAO:
    """
    DAO - Data Access Object
    """
    model = None

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        """
       Находит одну запись в базе данных, соответствующую заданным критериям фильтрации, или возвращает None, если такая запись не найдена.

       :param filter_by: Параметры для фильтрации записей.
       :return: Один экземпляр модели, соответствующий критериям фильтрации, или None.
       """
        async with async_session_maker() as session:
            return await cls._handle_transaction(session, "find_one_or_none", cls._find_one_or_none, **filter_by)

    @classmethod
    async def _find_one_or_none(cls, session: Session, **filter_by):
        query = select(cls.model).filter_by(**filter_by)
        result = await session.execute(query)
        return result.scalars().one_or_none()

    @classmethod
    async def find_all(cls, **filter_by):
        """
        Находит все записи в базе данных, соответствующие заданным критериям фильтрации.

        :param filter_by: Параметры для фильтрации записей.
        :return: Список экземпляров модели, соответствующих критериям фильтрации.
        """
        async with async_session_maker() as session:
            return await cls._handle_transaction(session, "find_all", cls._find_all, **filter_by)

    @classmethod
    async def _find_all(cls, session: Session, **filter_by):
        query = select(cls.model).filter_by(**filter_by)
        result = await session.execute(query)
        return result.scalars().all()

    @classmethod
    async def create(cls, **data) -> Optional[Base]:
        """
        Создает новую запись в базе данных с заданными данными.

        :param data: Данные для создания новой записи.
        :return: Экземпляр созданной модели или None в случае ошибки.
        """
        async with async_session_maker() as session:
            return await cls._handle_transaction(session, "create", cls._create, **data)

    @classmethod
    async def _create(cls, session: Session, **data) -> Base:
        query = insert(cls.model).values(**data).returning(cls.model)
        result = await session.execute(query)
        await session.commit()
        return result.scalars().first()

    @classmethod
    async def get_paginated(cls, offset: int, limit: int, **filter) -> List[Base]:
        """
        Возвращает пагинированный список записей модели.

        :param offset: Смещение, с которого начинается выборка записей.
        :param limit: Количество записей для выборки.
        :param filter: Опциональный фильтр
        :return: Список экземпляров модели в заданном диапазоне.
        """
        async with async_session_maker() as session:
            return await cls._handle_transaction(session, "get_paginated", cls._get_paginated, offset, limit, **filter)

    @classmethod
    async def _get_paginated(cls, session: Session, offset: int, limit: int, **filter) -> List[Base]:
        if filter:
            query = select(cls.model).filter_by(**filter).offset(offset).limit(limit)
        else:
            query = select(cls.model).offset(offset).limit(limit)
        result = await session.execute(query)
        return result.scalars().all()

    @classmethod
    async def update_by_id(cls, id_field: str, id_value: Union[str, int], update_data: dict) -> Optional[Base]:
        """
        Обновляет запись по заданному идентификатору с использованием предоставленных данных.

        :param id_field: Имя поля, которое является идентификатором.
        :param id_value: Значение идентификатора записи для обновления.
        :param update_data: Словарь с данными для обновления.
        :return: Обновленный экземпляр модели или None, если обновление не удалось.
        """
        async with async_session_maker() as session:
            return await cls._handle_transaction(session, "update_by_id", cls._update_by_id, id_field, id_value,
                                                 update_data)

    @classmethod
    async def _update_by_id(cls, session: Session, id_field: str, id_value: Union[str, int], update_data: dict) -> \
            Optional[
                Base]:
        query = update(cls.model).where(getattr(cls.model, id_field) == id_value).values(**update_data)
        await session.execute(query)
        await session.commit()
        return await cls.find_one_or_none(**{id_field: id_value})

    @classmethod
    async def delete_by_id(cls, id_field: str, id_value: Union[str, int]) -> bool:
        """
        Удаляет запись по заданному идентификатору.

        :param id_field: Имя поля, которое является идентификатором.
        :param id_value: Значение идентификатора для удаления записи.
        :return: Возвращает True, если запись была успешно удалена, иначе False.
        """
        async with async_session_maker() as session:
            return await cls._handle_transaction(session, "delete_by_id", cls._delete_by_id, id_field, id_value)

    @classmethod
    async def _delete_by_id(cls, session: Session, id_field: str, id_value: Union[str, int]) -> bool:
        query = delete(cls.model).where(getattr(cls.model, id_field) == id_value)
        result = await session.execute(query)
        await session.commit()
        return True if result.rowcount > 0 else False

    @classmethod
    async def get_multilanguage_field(cls, language: str) -> List[Dict]:
        async with async_session_maker() as session:
            return await cls._handle_transaction(session, "get_multilanguage_field",
                                                 cls._get_multilanguage_field, language)

    @classmethod
    async def _get_multilanguage_field(cls, session: Session, language: str) -> List[Dict]:
        query = select(cls.model)
        result = await session.execute(query)
        data = result.scalars().all()

        processed_data = []
        for entry in data:
            entry_dict = {}
            for column in inspect(entry).mapper.column_attrs:
                attr_name = column.key
                attr_value = getattr(entry, attr_name)

                # Проверяем, является ли значение словарем (мультиязычное поле)
                if isinstance(attr_value, dict):
                    # Выбираем значение на требуемом языке, с запасным вариантом на английском, если текущий язык отсутствует
                    entry_dict[attr_name] = attr_value.get(language, attr_value.get('en'))
                else:
                    # Добавляем значение как есть
                    entry_dict[attr_name] = attr_value

            processed_data.append(entry_dict)

        return processed_data

    @classmethod
    async def _handle_transaction(cls, session: Session, operation: str, transaction_func, *args, **kwargs):
        """
        Обрабатывает транзакцию с базой данных, выполняя заданную функцию. Логирует ошибки, если они возникают.

        Этот метод предназначен для внутреннего использования DAO для обеспечения единообразного способа обработки транзакций.

        :param session: Сессия для выполнения операций с базой данных.
        :param operation: Название операции для логгирования.
        :param transaction_func: Функция, которая будет выполнена в рамках транзакции.
        :param args: Позиционные аргументы, передаваемые в transaction_func.
        :param kwargs: Именованные аргументы, передаваемые в transaction_func.
        :return: Результат выполнения transaction_func или None в случае ошибки.
        """
        try:
            return await transaction_func(session, *args, **kwargs)
        except InterfaceError as e:
            # Пересоздаем сессию и пробуем снова
            async with async_session_maker() as new_session:
                try:
                    return await transaction_func(new_session, *args, **kwargs)
                except Exception as e:
                    cls._log_error(e, operation)
                    return None
        except Exception as e:
            cls._log_error(e, operation)
            return None
        finally:
            await session.close()

    @classmethod
    def _log_error(cls, e: Exception, operation: str) -> None:
        if isinstance(e, SQLAlchemyError):
            msg = f"Database Exc: Cannot {operation} data in table"
        elif isinstance(e, Exception):
            msg = f"Unknown Exc: Cannot {operation} data in table"
        logger.error(msg, extra={"table": cls.model.__tablename__}, exc_info=True)
