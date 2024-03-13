from aiogram.filters.callback_data import CallbackData


class MyCallback(CallbackData, prefix="my"):
    """
    Класс для обработки callback-данных.

    Attributes:
        newsletter (str): Текстовое поле для хранения информации о подписке.
        data (str): Текстовое поле для хранения дополнительных данных.
    """
    newsletter: str
    data: str


