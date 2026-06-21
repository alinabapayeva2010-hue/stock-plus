import json
import os

DB_PATH = os.path.join('data', 'database.json')

def load_data():
    if not os.path.exists(DB_PATH):
        return {"products": {}, "orders": []}
    with open(DB_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(data):
    with open(DB_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def add_product(article, name, stock, purchase_price, selling_price):
    """Добавление нового товара в систему"""
    data = load_data()
    if article in data["products"]:
        print(f"Ошибка: Товар с артикулом {article} уже существует.")
        return False
    
    data["products"][article] = {
        "name": name,
        "stock": int(stock),
        "purchase_price": float(purchase_price),
        "selling_price": float(selling_price)
    }
    save_data(data)
    print(f"Товар '{name}' успешно добавлен!")
    return True

def update_stock(article, new_stock):
    """Редактирование остатков товара"""
    data = load_data()
    if article not in data["products"]:
        print("Товар не найден.")
        return False
    
    data["products"][article]["stock"] = int(new_stock)
    save_data(data)
    print(f"Остатки товара {article} обновлены.")
    return True

def get_inventory_overview():
    """Просмотр всех товаров и уведомление о низком остатке"""
    data = load_data()
    print("\n--- ТЕКУЩИЙ ОСТАТОК НА СКЛАДЕ ---")
    for art, info in data["products"].items():
        status = "⚠️ МАЛО НА СКЛАДЕ" if info["stock"] < 5 else "OK"
        print(f"Артикул: {art} | {info['name']} | Остаток: {info['stock']} шт. | Цена: {info['selling_price']} руб. [{status}]") 
