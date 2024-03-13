from aiogram.fsm.state import StatesGroup, State


class ProductInfoForm(StatesGroup):
    enter_product_code = State()