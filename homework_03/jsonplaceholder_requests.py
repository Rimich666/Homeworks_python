"""
создайте асинхронные функции для выполнения запросов к ресурсам (используйте aiohttp)
"""
import aiohttp
import asyncio

USERS_DATA_URL = "https://jsonplaceholder.typicode.com/users"
POSTS_DATA_URL = "https://jsonplaceholder.typicode.com/posts"


async def get_users(session):
    async with session.get(USERS_DATA_URL) as response:
        return await response.json()


async def get_posts(session, user_id):
    async with session.get(POSTS_DATA_URL, params={"userId": user_id}) as response:
        return await response.json()


if __name__ == '__main__':

    async def request():
        async with aiohttp.ClientSession() as session:
            users = await get_users(session)
            print(type(users))
            for user in await get_users(session):
                print(type(user))
                print(await get_posts(session, user['id']))
            await session.close()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(request())
