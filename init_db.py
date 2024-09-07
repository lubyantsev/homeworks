import sqlite3


def populate_db(db_name='products.db'):
    """Заполняет базу данных продуктами."""
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

    products = [
        ("Витамин A", "Полезен для зрения", 100, "https://i.pinimg.com/736x/e5/de/94/e5de9481f54df4a712525431338c3497.jpg"),
        ("Витамин C", "Укрепляет иммунитет", 200, "https://images.squarespace-cdn.com/content/v1/607773ecd359161f2364e7c9/1622838803922-WEOBACY2T9I8AHFQPDGJ/vitaminC.png"),
        ("Витамин D", "Поддерживает здоровье костей", 300, "https://sp-ao.shortpixel.ai/client/to_webp,q_glossy,ret_img,w_728,h_389/https://www.medicynanaroda.ru/wp-content/uploads/2017/11/v-kakix-produktax-soderzhitsya-vitamin-d.jpg"),
        ("Витамин E", "Антиоксидант", 5000000, "https://avatars.mds.yandex.net/i?id=cf694584172248a40c4d1bc3fdb4832e_l-10355200-images-thumbs&n=13"),
    ]

    try:
        cursor.executemany('INSERT INTO Products (title, description, price, image_url) VALUES (?, ?, ?, ?)', products)
        conn.commit()
        print("Данные успешно добавлены в базу данных.")
    except sqlite3.Error as e:
        print(f"Ошибка при добавлении данных: {e}")
    finally:
        conn.close()


if __name__ == '__main__':
    populate_db()
