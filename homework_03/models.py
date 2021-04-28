"""
создайте алхимичный engine
добавьте declarative base (свяжите с engine)
создайте объект Session
добавьте модели User и Post, объявите поля:
для модели User обязательными являются name, username, email
для модели Post обязательными являются user_id, title, body
создайте связи relationship между моделями: User.posts и Post.user
"""

import asyncio
import asyncpg
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
import os

PG_CONN_URI = os.environ.get("PG_CONN_URI") or "postgresql://postgres:password@localhost/postgres"
pg_conn_uri_async = 'postgresql+asyncpg' + PG_CONN_URI[PG_CONN_URI.find('://'):]

engine = create_async_engine(pg_conn_uri_async, echo=False)
Base = declarative_base()
Session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)  # "Leanne Graham",
    username = Column(String)  # "Bret",
    email = Column(String)  # "Sincere@april.biz",
    phone = Column(String)  # "1-770-736-8031 x56442",
    website = Column(String)  # "hildegard.org",

    def __init__(self, args):
        self.id = args['id']
        self.name = args['name']
        self.username = args['username']
        self.email = args['email']
        self.phone = args['phone']
        self.website = args['website']

    def __str__(self):
        return f"User: \n\t.name: {self.name}\n\t.username: {self.username}\n\t.email: " \
               f"{self.email}\n\t.phone: {self.phone}\n\t.website: {self.website}"

    posts = relationship("Post", back_populates="user")

    async def to_base(self, sess):
        res = await sess.execute(select(User).where(User.id == self.id))
        row = res.scalar_one_or_none()
        if not bool(row):
            sess.add(self)
        else:
            print(f"user with id = {self.id} already exists")


class Post(Base):
    __tablename__ = 'posts'
    user_id = Column(Integer, ForeignKey('users.id'))
    id = Column(Integer, primary_key=True)
    title = Column(String)
    body = Column(String)

    user = relationship("User", back_populates="posts")

    def __init__(self, args):
        self.user_id = args['userId']
        self.id = args['id']
        self.title = args['title']
        self.body = args['body']

    def __str__(self):
        return f"Post: \n\t.user: {self.user.name}\n\t.title: {self.title}\n\t.body: " \
               f"{self.body}"

    async def to_base(self, sess):
        res = await sess.execute(select(Post).where(Post.id == self.id))
        row = res.scalar_one_or_none()
        if not bool(row):
            sess.add(self)
        else:
            print(f"In the 'Post' table, there is already a row with id = {self.id}")


if __name__ == "__main__":
    #    print(sqlalchemy.__file__)
    print(asyncpg.__file__)
    import sys

    for p in sys.path:
        print(p)


    async def to_base(user):
        async with Session(future=True) as session:
            await user.to_base(session)
            await session.commit()


    #   sessn = Session()
    #   users = sessn.query(User).all()
    #   print(type(Session))
    #            res = await session.execute(select(User).where(User.id == user.id))
    #            row = res.scalar_one_or_none()
    #            if not bool(row):
    #                session.add(bret_user)
    #                await session.commit()
    #            else:
    #                print(row)

    bret_user = User({'id': 1, 'name': "Leanne Graham", 'username': "Bret",
                      'email': "Sincere@april.biz", 'phone': "1-770-736-8031 x56442",
                      'website': "hildegard.org"})

    loop = asyncio.get_event_loop()
    loop.run_until_complete(to_base(bret_user))

#    print(bret_user)
#    print(repr(User.__table__))
#    engine.connect()
#    print(sqlalchemy.__version__)
