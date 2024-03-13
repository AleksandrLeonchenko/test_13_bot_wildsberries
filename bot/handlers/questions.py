import asyncio
from sqlalchemy.orm import session, Session
from sqlalchemy.ext.asyncio import AsyncSession

from aiogram import Router, F, types
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, InlineKeyboardButton, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from data.database import create_user_query_history, create_product, create_user, AsyncSessionLocal, get_product_info, \
    get_user_query_history
from handlers.states import ProductInfoForm
from keyboards.reply import xxx
from utils.filters import MyCallback
from utils.http_requests import fetch_data, get_product_data
from utils.utils import format_product_info

router = Router()
stop_flag = asyncio.Event()


@router.message(Command("start"))
async def cmd_start(message: Message):
    """
    Обработчик команды /start.

    Args:
        message (Message): Объект сообщения.

    Returns:
        None
    """
    await message.answer(
        "Выберите действие:",
        reply_markup=xxx()
    )


@router.message(F.text.lower() == "получить информацию по товару")
async def cmd_get_product_info(message: types.Message, state: FSMContext):
    """
    Обработчик для получения информации о товаре.

    Args:
        message (types.Message): Объект сообщения.
        state (FSMContext): Состояние конечного автомата.

    Returns:
        None
    """
    await message.answer("Введите артикул товара (9-значное число):")
    await state.set_state(ProductInfoForm.enter_product_code)


@router.message(ProductInfoForm.enter_product_code)
async def process_product_code(message: Message, state: FSMContext):
    """
    Обработчик для обработки введенного пользователем артикула товара.

    Args:
        message (Message): Объект сообщения.
        state (FSMContext): Состояние конечного автомата.

    Returns:
        None
    """

    product_code = message.text.strip()

    # Проверяем артикул (критерии корректности можно добавить)
    if len(product_code) == 9:

        data = await get_product_data(product_code)
        product_info = data.get("data", {}).get("products", [])
        if product_info:
            first_product = product_info[0]
            product_name = first_product.get("name", "Нет данных")
            product_id = first_product.get("id", "Нет данных")
            product_price = first_product.get("priceU", "Нет данных")
            product_rating = first_product.get("rating", "Нет данных")
            product_qty = first_product.get("sizes", [{}])[0].get("stocks", [{}])[0].get("qty", "Нет данных")

            user_nickname = message.from_user.username
            user_id = message.from_user.id
            user = await create_user(
                username=user_nickname,
                user_id=user_id
            )
            product = await create_product(
                product_code=int(product_code),
                product_name=product_name,
                product_price=float(product_price),
                product_rate=int(product_rating),
                product_count=int(product_qty)
            )
            await create_user_query_history(product_code=int(product_code), user_id=user.user_id)

            product_data = f"{product_code}"
            builder = InlineKeyboardBuilder()

            builder.add(types.InlineKeyboardButton(
                text="подписаться",
                callback_data=MyCallback(newsletter="подписаться", data=product_data).pack())
            )

            await message.reply(
                f"Информация по товару с кодом {product_code}:\n"
                f"Название: {product_name}\n"
                f"Артикул: {product_id}\n"
                f"Цена: {product_price}\n"
                f"Рейтинг: {product_rating}\n"
                f"Количество на складе: {product_qty}\n",
                reply_markup=builder.as_markup()
            )
        else:
            await message.reply(f"Товар с артикулом {product_code} не найден.")
    else:
        await message.reply("Артикул введён некорректно. Введите корректный артикул (должно быть 9 цифр).")

    await state.clear()


async def my_coroutine(query: types.CallbackQuery, callback_data: MyCallback, session: AsyncSession):
    """
    Корутина для обработки уведомлений.

    Args:
        query (types.CallbackQuery): Объект коллбэк-запроса.
        callback_data (MyCallback): Объект данных коллбэка.
        session (AsyncSession): Сессия базы данных.

    Returns:
        None
    """
    try:
        while not stop_flag.is_set():
            product_info = await get_product_info(session, callback_data.data)
            await query.message.answer(format_product_info(product_info))
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        print("Coroutine canceled.")
    finally:
        stop_flag.clear()


@router.message(F.text.lower() == "остановить уведомления")
async def handle_buttons(message: types.Message, mylist2: list[int], task: asyncio.Task = None):
    """
    Обработчик для остановки уведомлений.

    Args:
        message (types.Message): Объект сообщения.
        task (asyncio.Task): Задача.

    Returns:
        None
    """
    stop_flag.set()  # Устанавливаем флаг для остановки корутины


@router.callback_query(MyCallback.filter(F.newsletter == "подписаться"))
async def handle_buttons(query: types.CallbackQuery, callback_data: MyCallback, mylist2: list[int], state: FSMContext,
                         task: asyncio.Task = None):
    """
    Обработчик для подписки на уведомления.

    Args:
        query (types.CallbackQuery): Объект коллбэк-запроса.
        callback_data (MyCallback): Объект данных коллбэка.
        state (FSMContext): Состояние конечного автомата.
        task (asyncio.Task): Задача.

    Returns:
        None
    """
    try:
        async with AsyncSessionLocal() as session:
            stop_flag.clear()
            task = asyncio.create_task(my_coroutine(query, callback_data, session))
    except Exception as e:
        print(f"Error in : {e}")


@router.message(F.text.lower() == "получить информацию из бд")
async def answer_no(message: types.Message):
    """
    Обработчик для получения информации из базы данных.

    Args:
        message (types.Message): Объект сообщения.

    Returns:
        None
    """
    user_id = message.from_user.id

    async with AsyncSessionLocal() as session:

        user_queries = await get_user_query_history(session, user_id)
        if user_queries:
            response_text = "\n".join(
                [f"Запрос {query.id}. Время запроса: {query.request_time}, артикул товара: {query.product_code}" for
                 query in
                 user_queries])

        else:
            response_text = "Вашей истории запросов пока нет"

        await message.answer(response_text)
