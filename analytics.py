from src.inventory import load_data, save_data

def register_sale(article, quantity):
    """Регистрация продажи и списание со склада"""
    data = load_data()
    if article not in data["products"]:
        print("Ошибка: Товар не найден.")
        return False
    
    product = data["products"][article]
    if product["stock"] < quantity:
        print(f"Ошибка: Недостаточно товара на складе. Доступно: {product['stock']}")
        return False
    
    # Списание остатков
    product["stock"] -= quantity
    
    # Фиксация заказа
    order = {
        "article": article,
        "product_name": product["name"],
        "quantity": quantity,
        "total_sale": quantity * product["selling_price"],
        "profit": quantity * (product["selling_price"] - product["purchase_price"])
    }
    data["orders"].append(order)
    save_data(data)
    print(f"Продажа оформлена успешно! Списано {quantity} шт.")
    return True

def show_analytics():
    """Анализ выручки и прибыли"""
    data = load_data()
    total_revenue = sum(order["total_sale"] for order in data["orders"])
    total_profit = sum(order["profit"] for order in data["orders"])
    
    print("\n--- АНАЛИТИКА СИСТЕМЫ STOCK+ ---")
    print(f"Общая выручка: {total_revenue} руб.")
    print(f"Чистая прибыль: {total_profit} pool.")
    print(f"Всего совершенных заказов: {len(data['orders'])}")