import httpx
import asyncio


async def fetch_data(url) -> dict:
    """
    Асинхронная функция для получения данных по заданному URL.

    Args:
        url (str): URL для отправки HTTP-запроса.

    Returns:
        dict: Результат запроса в формате JSON.
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()


async def get_product_data(product_code: str) -> dict:
    """
    Асинхронная функция для получения данных о продукте по его коду.

    Args:
        product_code (str): Код продукта.

    Returns:
        dict: Информация о продукте в формате словаря.
    """
    url = f"https://card.wb.ru/cards/v1/detail?appType=1&curr=rub&dest=-1257786&spp=30&nm={product_code}"
    data = await fetch_data(url)

    return data

if __name__ == "__main__":
    asyncio.run(get_product_data())
