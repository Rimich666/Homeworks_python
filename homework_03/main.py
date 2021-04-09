"""
Домашнее задание №3
Асинхронная работа с сетью и бд

создайте синхронную функцию main, по вызову которой будет выполняться полный цикл программы (добавьте туда выполнение асинхронной функции):
- инициализация бд
- создание таблиц
- загрузка пользователей и постов
- добавление пользователей и постов в базу данных
- закрытие соединения с БД
"""

import asyncio
import aiohttp

from jsonplaceholder_requests import get_users, get_posts

from models import Base, ASession, User, Post, engine


async def request():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with aiohttp.ClientSession() as session:
        async with ASession(future=True) as session_psql:
            for user in await get_users(session):
                await User(user).to_base(session_psql)
                for post in await get_posts(session, user['id']):
                    await Post(post).to_base(session_psql)
            await session_psql.commit()


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(request())


if __name__ == "__main__":
    main()
