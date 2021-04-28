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

from models import Base, Session, User, Post, engine


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    async with aiohttp.ClientSession() as session:
        async with Session(future=True) as session_psql:
            for user in await get_users(session):
                await User(user).to_base(session_psql)
                for post in await get_posts(session, user['id']):
                    await Post(post).to_base(session_psql)
            await session_psql.commit()


def main():
    asyncio.run(async_main())
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(async_main())


if __name__ == "__main__":
    main()
