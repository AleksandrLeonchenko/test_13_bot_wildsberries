from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def xxx() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="получить информацию по товару")
    kb.button(text="остановить уведомления")
    kb.button(text="получить информацию из бд")
    kb.adjust(3)
    return kb.as_markup(resize_keyboard=True)
