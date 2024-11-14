from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from requests import change_1
from aiogram.utils.keyboard import InlineKeyboardBuilder


keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='СМЕНА 1'),
     KeyboardButton(text='СМЕНА 2')],
    [KeyboardButton(text='СМЕНА 3'),
     KeyboardButton(text='СМЕНА 4')],
    [KeyboardButton(text='БОЛЬНИЧНЫЕ'),
     KeyboardButton(text='ОТПУСК')],
    [KeyboardButton(text='ДОБАВИТЬ РАБОТНИКА'),
     KeyboardButton(text='УДАЛИТЬ РАБОТНИКА')]], resize_keyboard=True,
    input_field_placeholder='Выберите пункт')

users_1 = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text='Редактировать или добавить больничный', callback_data='liv')]])
users_2 = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text='Редактировать отпуск или добавить', callback_data='voc')]])


async def Changes(num):
    all_change = await change_1(num)
    board = InlineKeyboardBuilder()
    a = 0
    for nums, change in enumerate(all_change.scalars()):
        board.add(InlineKeyboardButton(text=f"{nums + 1}. {change.name}", callback_data=change.name))
        a += 1
    return board.adjust(1).as_markup(), a
