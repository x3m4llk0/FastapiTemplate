"""
Инициализация подключения к Redis и базовых методов
"""
#
# import json
#
# import redis.asyncio as aioredis
#
# import redis
# from app.core.config import settings
# from app.core.logger import logger
#
#
# # Создаем синхронного клиента Redis для выполнения синхронных операций
# sync_redis_client = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)
#
#
# class RedisCache:
#     """Класс для работы с Redis кешем асинхронно."""
#
#     def __init__(self):
#         """Инициализация асинхронного клиента Redis с использованием настроек из конфигурации."""
#         self.redis = aioredis.from_url(settings.REDIS_URL, decode_responses=True)
#
#     async def get(self, key: str):
#         """
#         Получает значение из Redis по ключу асинхронно.
#
#         Args:
#             key (str): Ключ для поиска в Redis.
#
#         Returns:
#             Any: Десериализованное значение из Redis или None, если ключ не найден.
#         """
#         value = await self.redis.get(key)  # Получаем значение по ключу
#         if value:  # Если значение найдено
#             return json.loads(value)  # Возвращаем десериализованное значение
#         return None  # Возвращаем None, если значение не найдено
#
#     async def set(self, key: str, value: any, expire: int = None):
#         """
#         Сохраняет значение в Redis по ключу асинхронно с опциональным временем жизни.
#
#         Args:
#             key (str): Ключ для сохранения в Redis.
#             value (Any): Значение для сохранения в Redis.
#             expire (int, optional): Время жизни ключа в секундах. Если не указано, ключ будет сохраняться без срока действия.
#
#         """
#         if expire is not None:
#             # Сохраняем значение в Redis с временем жизни
#             await self.redis.set(key, json.dumps(value), ex=expire)
#         else:
#             # Сохраняем значение в Redis без времени жизни
#             await self.redis.set(key, json.dumps(value))
#
#     async def delete(self, key: str):
#         """
#         Удаляет ключ из Redis асинхронно.
#
#         Args:
#             key (str): Ключ для удаления из Redis.
#
#         """
#         await self.redis.delete(key)  # Удаляем ключ из Redis
#
#     async def close(self):
#         """
#         Закрывает соединение с Redis асинхронно.
#
#         """
#         await self.redis.close()  # Закрываем соединение с Redis
#         logger.info("Redis connection close")  # Логируем закрытие соединения
#
#
# # Создаем экземпляр класса RedisCache для использования в приложении
# redis_cache = RedisCache()
