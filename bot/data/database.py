import asyncio
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, CheckConstraint, JSON, ForeignKey, \
    select, cast
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session
from datetime import datetime
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String

from config import DATABASE_URL

# engine = create_async_engine(DATABASE_URL, echo=True)
engine = create_async_engine(DATABASE_URL)

AsyncSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    user_id = Column(Integer, unique=True)
    query_history = relationship('UserQueryHistory', back_populates='user')


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    time = Column(DateTime, default=datetime.utcnow)
    product_code = Column(Integer, unique=True)
    product_name = Column(String)
    product_price = Column(Float(precision=2))
    product_rate = Column(Integer, CheckConstraint('product_count >= 0'))
    product_count = Column(Integer, CheckConstraint('product_count >= 0'))
    query_history = relationship('UserQueryHistory', back_populates='product')


class UserQueryHistory(Base):
    __tablename__ = "user_query_history"

    id = Column(Integer, primary_key=True, index=True)
    request_time = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey('users.user_id'), index=True)
    user = relationship('User', back_populates='query_history')
    product_code = Column(Integer, ForeignKey('products.product_code'), index=True)
    product = relationship('Product', back_populates='query_history')


async def create_user(user_id: int, username: str) -> User:
    """
    Создает нового пользователя в базе данных.

    Args:
        user_id (int): Идентификатор пользователя.
        username (str): Имя пользователя.

    Returns:
        User: Созданный объект пользователя.
    """
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(User.username == username))
        existing_user = result.scalar()

        if existing_user:
            return existing_user

        user = User(
            username=username,
            user_id=user_id
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user


async def create_product(
        product_code: int,
        product_name: str,
        product_price: float,
        product_rate: int,
        product_count: int
) -> Product:
    """
    Создает новый продукт в базе данных.

    Args:
        product_code (int): Код продукта.
        product_name (str): Название продукта.
        product_price (float): Цена продукта.
        product_rate (int): Рейтинг продукта.
        product_count (int): Количество продукта на складе.

    Returns:
        Product: Созданный объект продукта.
    """
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(Product.product_code == product_code))
        existing_product = result.scalar()

        if existing_product:
            return existing_product

        product = Product(
            product_code=product_code,
            product_name=product_name,
            product_price=product_price,
            product_rate=product_rate,
            product_count=product_count
        )
        session.add(product)
        await session.commit()
        await session.refresh(product)
        return product


async def get_product_info(session: AsyncSession, product_code: str) -> Product:
    """
    Получает информацию о продукте из базы данных.

    Args:
        session (AsyncSession): Сессия базы данных.
        product_code (str): Код продукта.

    Returns:
        Product: Объект продукта.
    """
    product_code = int(product_code)
    result = await session.execute(
        select(Product).where(Product.product_code == product_code)
    )
    product = result.scalar_one_or_none()
    return product


async def create_user_query_history(product_code: int, user_id: int) -> UserQueryHistory:
    """
    Создает запись истории запросов пользователя в базе данных.

    Args:
        product_code (int): Код продукта.
        user_id (int): Идентификатор пользователя.

    Returns:
        UserQueryHistory: Созданный объект записи истории запросов.
    """
    async with AsyncSessionLocal() as session:
        query_history = UserQueryHistory(
            user_id=user_id,
            product_code=product_code
        )
        session.add(query_history)
        await session.commit()
        await session.refresh(query_history)
        return query_history


async def get_user_query_history(session: AsyncSession, user_id: int) -> list[UserQueryHistory]:
    """
    Получает историю запросов пользователя из базы данных.

    Args:
        session (AsyncSession): Сессия базы данных.
        user_id (int): Идентификатор пользователя.

    Returns:
        list[UserQueryHistory]: Список объектов записей истории запросов.
    """
    query = (
        select(UserQueryHistory)
        .filter(UserQueryHistory.user_id == user_id)
        .order_by(UserQueryHistory.request_time.desc())
        .limit(5)
    )
    result = await session.execute(query)
    return result.scalars().all()


async def create_tables():
    """
    Создает таблицы в базе данных.

    Returns:
        None
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def main_2():
    """
    Основная функция для создания таблиц и тестового пользователя.

    Returns:
        None
    """
    await create_tables()
    await create_user(123, "admin")

