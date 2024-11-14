from models import async_session
from models import Change, User
from sqlalchemy import select, update, delete, insert


async def change_1(num):
    async with async_session() as session:
        return await session.execute(select(Change).where(Change.change == num))


async def leave():
    async with async_session() as session:
        return await session.execute(select(Change).where(Change.sick_leave != None).where(Change.sick_leave != ''))


async def vocation_1():
    async with async_session() as session:
        return await session.execute(select(Change).where(Change.vocation != None).where(Change.vocation != ''))


async def vocation_2(new_leave, num):
    async with async_session() as session:
        await session.execute(update(Change).where(Change.number == num).values(vocation=new_leave))
        await session.commit()


async def leave_1(num):
    async with async_session() as session:
        return await session.execute(select(Change.name).where(Change.number == num))


async def leave_2(new_leave, num):
    async with async_session() as session:
        await session.execute(update(Change).where(Change.number == num).values(sick_leave=new_leave))
        await session.commit()


async def delete_1(num):
    async with async_session() as session:
        await session.execute(delete(Change).where(Change.number == num))
        await session.commit()


async def insert_1(name, telephone, job_title, change, connection_TGs, date_birth, number, certificate, address):
    async with async_session() as session:
        await session.execute(insert(Change).values(name=name, telephone=telephone, job_title=job_title, change=change,
                                                    connection_TG=connection_TGs, date_birth=date_birth, number=number,
                                                    sick_leave='', vocation='',
                                                    certificate=certificate, address=address))
        await session.commit()


async def insert_2(name, user_id):
    async with async_session() as session:
        query = select(User).where(User.name == name and User.user_id == user_id)
        existing_user = await session.execute(query)
        existing_user = existing_user.scalars().first()
        if existing_user is None:
            await session.execute(insert(User).values(name=name, user_id=user_id))
            await session.commit()
        else:
            await session.commit()


async def select_1():
    async with async_session() as session:
        return await session.execute(select(User))
