import sqlite3


def initiate_db(db_name='products.db'):
    """Создает таблицу Products, если она еще не существует."""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    price REAL NOT NULL,
    image_url TEXT
        )
    ''')
    conn.commit()
    conn.close()


def get_all_products(db_name='products.db'):
    """Возвращает все записи из таблицы Products."""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('SELECT title, description, price, image_url FROM Products')
    products = cursor.fetchall()
    conn.close()
    return products
