from aiogram.types import Message, CallbackQuery
from aiogram import F, Router
import keyboards as kb
import models as md
import requests as rq
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

router = Router()


class Update_liv(StatesGroup):
    numbers_tab = State()
    new_liv = State()
    numbers_tab_1 = State()
    new_voc = State()
    num_month = State()
    numbers_tab_2 = State()
    names = State()
    telephones = State()
    job_titles = State()
    changes_num = State()
    connection_TGs = State()
    dates_births = State()
    numbers_tab_3 = State()
    certificates = State()
    addresses = State()
    passwords = State()


@router.message(F.text == '/humans')
async def humans(message: Message):
    res = await rq.select_1()
    result = res.scalars().all()
    info_text = ''
    for i in result:
        info_text += f"ФИО: {i.name}\nТелефон: {i.user_id}\n\n"
    await message.answer(info_text)


@router.message(F.text == '/start')
async def start(message: Message, state: FSMContext):
    await state.set_state(Update_liv.passwords)
    await message.answer('Введите пароль для доступа к боту')


@router.message(Update_liv.passwords)
async def reg_pass(message: Message, state: FSMContext):
    await state.update_data(passwords=message.text)
    if message.text == '549':
        user_id = message.from_user.id
        user_name = message.from_user.full_name
        await rq.insert_2(user_name, user_id)
        await message.answer('Верный пароль', reply_markup=kb.keyboard)
        await state.clear()
    else:
        await message.answer('Неправильный пароль')


@router.callback_query(F.data == 'liv')
async def update_liv(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(Update_liv.numbers_tab)
    await callback.message.answer("Введите табельный номер работника для редактирования больничного:")


@router.message(Update_liv.numbers_tab)
async def reg_num_tab(message: Message, state: FSMContext):
    await state.update_data(numbers_tab=message.text)
    result = await rq.leave_1(message.text)
    workers = result.scalars().all()
    if message.text.lower() == 'стоп':
        await state.clear()
        return
    if workers:
        info = f'Работник найден {workers[0]}'
        await message.answer(info)
        await state.set_state(Update_liv.new_liv)
        await message.answer(
            "Введите больничный работника в формате например: '01.01.2024 до 01.02.2024', или 0 для удаления больничного:")
    else:
        await message.answer("Работник не найден. Если хотите остановить поиск введите 'стоп'")


@router.message(Update_liv.new_liv)
async def reg_liv(message: Message, state: FSMContext):
    data = await state.get_data()
    tab_number = data['numbers_tab']
    if message.text == '0':
        await rq.leave_2('', tab_number)
        await message.answer("Поле больничного очищено.")
    else:
        await rq.leave_2(message.text, tab_number)
        await message.answer("Поле больничного отредактировано.")
    await state.clear()


@router.callback_query(F.data == 'voc')
async def update_liv(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(Update_liv.numbers_tab_1)
    await callback.message.answer("Введите табельный номер работника для редактирования отпуска:")


@router.message(Update_liv.numbers_tab_1)
async def reg_num_tab(message: Message, state: FSMContext):
    await state.update_data(numbers_tab_1=message.text)
    result = await rq.leave_1(message.text)
    workers = result.scalars().all()
    if message.text.lower() == 'стоп':
        await state.clear()
        return
    if workers:
        info = f'Работник найден {workers[0]}'
        await message.answer(info)
        await state.set_state(Update_liv.new_voc)
        await message.answer(
            "Введите новую дату отпуска работника в формате например: '01.01.2024 до 01.02.2024', или 0 для удаления отпуска:")
    else:
        await message.answer("Работник не найден. Если хотите остановить поиск введите 'стоп'")


@router.message(Update_liv.new_voc)
async def reg_liv(message: Message, state: FSMContext):
    data = await state.get_data()
    tab_number = data['numbers_tab_1']
    if message.text == '0':
        await rq.vocation_2('', tab_number)
        await message.answer("Поле отпуска очищено.", reply_markup=kb.users_2)
    else:
        await rq.vocation_2(message.text, tab_number)
        await message.answer("Поле отпуска отредактировано.", reply_markup=kb.users_2)
    await state.clear()


@router.message(F.text == 'СМЕНА 1')
async def change_1(message: Message):
    c, b = await kb.Changes(1)
    await message.answer(f'Список работников 1 смены, общее количество {b} человек', reply_markup=c)


@router.message(F.text == 'СМЕНА 2')
async def change_2(message: Message):
    c, b = await kb.Changes(2)
    await message.answer(f'Список работников 2 смены, общее количество {b} человек', reply_markup=c)


@router.message(F.text == 'СМЕНА 3')
async def change_3(message: Message):
    c, b = await kb.Changes(3)
    await message.answer(f'Список работников 3 смены, общее количество {b} человек', reply_markup=c)


@router.message(F.text == 'СМЕНА 4')
async def change_4(message: Message):
    c, b = await kb.Changes(4)
    await message.answer(f'Список работников 4 смены, общее количество {b} человек', reply_markup=c)


@router.callback_query()
async def show_worker_info(callback: CallbackQuery):
    worker_name = callback.data
    async with md.async_session() as session:
        worker = await session.scalar(rq.select(md.Change).where(md.Change.name == worker_name))
        if worker:
            info = f"ФИО:  {worker.name}\nТелефон:  {worker.telephone}\nДолжность:  {worker.job_title}\n" \
                   f"Смена:  {worker.change}\nТелеграм:  {worker.connection_TG}\nДата рождения:  {worker.date_birth}\n" \
                   f"Табельный номер:  {worker.number}\nБольничный:  {worker.sick_leave}\n" \
                   f"Отпуск:  {worker.vocation}\nУдостоверение:  {worker.certificate}\nАдрес:  {worker.address}\n\n"
            await callback.answer()
            await callback.message.answer(info)


@router.message(F.text == 'БОЛЬНИЧНЫЕ')
async def Sick_leave(message: Message):
    result = await rq.leave()
    workers = result.scalars().all()
    if workers:
        count = len(workers)
        info_text = f"Список работников на больничном: {count} человек\n\n"
        for worker in workers:
            info_text += f"ФИО: {worker.name}\nТелефон: {worker.telephone}\nДолжность: {worker.job_title}\n" \
                         f"Смена: {worker.change}\nТелеграм: {worker.connection_TG}\nДата рождения: {worker.date_birth}\n" \
                         f"Табельный номер: {worker.number}\nБольничный: {worker.sick_leave}\n" \
                         f"Отпуск: {worker.vocation}\nУдостоверение: {worker.certificate}\nАдрес: {worker.address}\n\n"
        await message.answer(info_text, reply_markup=kb.users_1)
    else:
        await message.answer("Нет работников на больничном.", reply_markup=kb.users_1)


@router.message(F.text == 'ОТПУСК')
async def Vocation(message: Message, state: FSMContext):
    await state.set_state(Update_liv.num_month.state)
    await message.answer("Введите порядковый номер искомого месяца в формате '01':")


@router.message(Update_liv.num_month)
async def info_vocation(message: Message, state: FSMContext):
    num_month = message.text
    await state.update_data(num_month=num_month)
    result = await rq.vocation_1()
    workers = result.scalars().all()
    months_dict = {
        '01': 'Январь',
        '02': 'Февраль',
        '03': 'Март',
        '04': 'Апрель',
        '05': 'Май',
        '06': 'Июнь',
        '07': 'Июль',
        '08': 'Август',
        '09': 'Сентябрь',
        '10': 'Октябрь',
        '11': 'Ноябрь',
        '12': 'Декабрь'
    }
    month_name = ''
    if num_month in months_dict.keys():
        month_name = months_dict[num_month]
    else:
        await message.answer('Некорректный месяц. Попробуйте ещё раз.')

    a = 0
    if workers:
        info_text = f"Список работников в отпуске на месяц {month_name}: {a} человек\n\n"
        info_change_1 = "\nРаботники 1 смены:\n\n"
        info_change_2 = "\nРаботники 2 смены:\n\n"
        info_change_3 = "\nРаботники 3 смены:\n\n"
        info_change_4 = "\nРаботники 4 смены:\n\n"
        for worker in workers:
            if str(worker.vocation[3:5]) == num_month or str(worker.vocation[17:19]) == num_month:
                a += 1
                info_text = f"Список работников в отпуске на месяц {month_name}: {a} человек\n\n"
                if worker.change == 1:
                    info_change_1 += f"{worker.name}\nОтпуск: {worker.vocation[:24]}\n"
                elif worker.change == 2:
                    info_change_2 += f"{worker.name}\nОтпуск: {worker.vocation[:24]}\n"
                elif worker.change == 3:
                    info_change_3 += f"{worker.name}\nОтпуск: {worker.vocation[:24]}\n"
                elif worker.change == 4:
                    info_change_4 += f"{worker.name}\nОтпуск: {worker.vocation[:24]}\n"
            elif str(worker.vocation[28:30]) == num_month or str(worker.vocation[42:44]) == num_month:
                a += 1
                info_text = f"Список работников в отпуске на месяц {month_name}: {a} человек\n\n"
                if worker.change == 1:
                    info_change_1 += f"{worker.name}\nОтпуск: {worker.vocation[25:]}\n\n"
                elif worker.change == 2:
                    info_change_2 += f"{worker.name}\nОтпуск: {worker.vocation[25:]}\n"
                elif worker.change == 3:
                    info_change_3 += f"{worker.name}\nОтпуск: {worker.vocation[25:]}\n"
                elif worker.change == 4:
                    info_change_4 += f"{worker.name}\nОтпуск: {worker.vocation[25:]}\n"
        if a == 0:
            info_text = f"Нет работников в отпуске на месяц {month_name}.\n\n"
            info_change_1 = ""
            info_change_2 = ""
            info_change_3 = ""
            info_change_4 = ""
        await message.answer(info_text + info_change_1 + info_change_2 + info_change_3 + info_change_4,
                             reply_markup=kb.users_2)
    else:
        await message.answer("Нет работников в отпуске.", reply_markup=kb.users_2)
    await state.clear()


@router.message(F.text == 'УДАЛИТЬ РАБОТНИКА')
async def Vocation(message: Message, state: FSMContext):
    await state.set_state(Update_liv.numbers_tab_2.state)
    await message.answer("Введите табельный номер работника для его удаления или введите стоп для выхода:")


@router.message(Update_liv.numbers_tab_2)
async def worker_del(message: Message, state: FSMContext):
    await state.update_data(numbers_tab_2=message.text)
    result = await rq.leave_1(message.text)
    workers = result.scalars().all()
    if message.text.lower() == 'стоп':
        await state.clear()
        return
    if workers:
        info = f'Работник найден {workers[0]}'
        await message.answer(info)
        await rq.delete_1(message.text)
        await message.answer("Работник удалён.")
    else:
        await message.answer("Работник не найден.")
    await state.clear()


@router.message(F.text == 'ДОБАВИТЬ РАБОТНИКА')
async def add_worker(message: Message, state: FSMContext):
    await state.set_state(Update_liv.names.state)
    await message.answer("Начинается добавление нового работника. Поэтапно необходимо ввести данные работника.\n"
                         "Введите ФИО работника или введите стоп для выхода:")


@router.message(Update_liv.names)
async def add_name(message: Message, state: FSMContext):
    await state.update_data(names=message.text)
    if message.text.lower() == 'стоп':
        await state.clear()
        return
    await state.set_state(Update_liv.telephones.state)
    await message.answer("Введите номер телефона работника через +7 или введите стоп для выхода:")


@router.message(Update_liv.telephones)
async def add_tele(message: Message, state: FSMContext):
    await state.update_data(telephones=message.text)
    if message.text.lower() == 'стоп':
        await state.clear()
        return
    await state.set_state(Update_liv.job_titles.state)
    await message.answer("Введите должность работника или введите стоп для выхода:")


@router.message(Update_liv.job_titles)
async def add_title(message: Message, state: FSMContext):
    await state.update_data(job_titles=message.text)
    if message.text.lower() == 'стоп':
        await state.clear()
        return
    await state.set_state(Update_liv.changes_num.state)
    await message.answer("Введите номер смены работника или введите стоп для выхода:")


@router.message(Update_liv.changes_num)
async def add_change(message: Message, state: FSMContext):
    await state.update_data(changes_num=message.text)
    if message.text.lower() == 'стоп':
        await state.clear()
        return
    await state.set_state(Update_liv.connection_TGs.state)
    await message.answer(
        "Введите уникальное имя Telegram работника или https://t.me/+79999999999 или введите стоп для выхода:")


@router.message(Update_liv.connection_TGs)
async def add_TG(message: Message, state: FSMContext):
    await state.update_data(connection_TGs=message.text)
    if message.text.lower() == 'стоп':
        await state.clear()
        return
    await state.set_state(Update_liv.dates_births.state)
    await message.answer("Введите дату рождения работника или введите стоп для выхода:")


@router.message(Update_liv.dates_births)
async def add_birth(message: Message, state: FSMContext):
    await state.update_data(dates_births=message.text)
    if message.text.lower() == 'стоп':
        await state.clear()
        return
    await state.set_state(Update_liv.numbers_tab_3.state)
    await message.answer("Введите табельный номер работника или введите стоп для выхода:")


@router.message(Update_liv.numbers_tab_3)
async def add_birth(message: Message, state: FSMContext):
    await state.update_data(numbers_tab_3=message.text)
    if message.text.lower() == 'стоп':
        await state.clear()
        return
    await state.set_state(Update_liv.certificates.state)
    await message.answer("Введите удостоверение работника или введите стоп для выхода:")


@router.message(Update_liv.certificates)
async def add_birth(message: Message, state: FSMContext):
    await state.update_data(certificates=message.text)
    if message.text.lower() == 'стоп':
        await state.clear()
        return
    await state.set_state(Update_liv.addresses.state)
    await message.answer("Введите адрес места жительства работника или введите стоп для выхода:")


@router.message(Update_liv.addresses)
async def add_num_tab(message: Message, state: FSMContext):
    await state.update_data(addresses=message.text)
    if message.text.lower() == 'стоп':
        await state.clear()
        return
    data = await state.get_data()
    name = data['names']
    telephone = data['telephones']
    job_title = data['job_titles']
    change = data['changes_num']
    connection_TGs = data['connection_TGs']
    date_birth = data['dates_births']
    numbers_tab_3 = data['numbers_tab_3']
    certificates = data['certificates']
    addresses = data['addresses']
    await rq.insert_1(name, telephone, job_title, change, connection_TGs, date_birth, numbers_tab_3, certificates,
                      addresses)
    await message.answer("Работник добавлен.")
    await state.clear()


@router.message()
async def start(message: Message):
    await message.answer('Выберите пункт меню', reply_markup=kb.keyboard)
