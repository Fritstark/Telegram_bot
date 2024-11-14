from sqlalchemy import BigInteger
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

engine = create_async_engine(url="sqlite+aiosqlite:///Bot2.db")
async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Change(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    telephone: Mapped[str] = mapped_column(unique=True)
    job_title: Mapped[str] = mapped_column()
    change: Mapped[int] = mapped_column()
    connection_TG: Mapped[str] = mapped_column(unique=True)
    date_birth: Mapped[str] = mapped_column()
    number: Mapped[str] = mapped_column()
    sick_leave: Mapped[str] = mapped_column()
    vocation: Mapped[str] = mapped_column()
    certificate: Mapped[str] = mapped_column()
    address: Mapped[str] = mapped_column()


class User(Base):
    __tablename__ = 'humans'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    user_id = mapped_column(BigInteger, unique=True)


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all, checkfirst=True)
