def format_product_info(product_info):
    """
    Форматирование информации о товаре для вывода.

    Args:
        product_info (ProductInfo): Информация о товаре.

    Returns:
        str: Отформатированная информация о товаре.
    """
    if product_info:
        product_code = product_info.product_code
        product_name = product_info.product_name
        product_id = product_info.id
        product_price = product_info.product_price
        product_rating = product_info.product_rate
        product_qty = product_info.product_count

        formatted_info = (
            f"Информация по товару с кодом {product_code}:\n"
            f"Название: {product_name}\n"
            f"Артикул: {product_id}\n"
            f"Цена: {product_price}\n"
            f"Рейтинг: {product_rating}\n"
            f"Количество на складе: {product_qty}\n"
        )
        return formatted_info
    else:
        return "Товар не найден"