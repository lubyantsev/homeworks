import sqlite3


def create_connection(db_file):
    """Создает подключение к SQLite базе данных."""
    conn = sqlite3.connect(db_file)
    return conn


def initiate_db(db_name='products.db'):
    """Создает таблицы Products и Users, если они еще не существуют."""
    conn = create_connection(db_name)
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

    # Создание таблицы Users
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        age INTEGER NOT NULL,
        balance INTEGER NOT NULL DEFAULT 1000
    )
    ''')

    conn.commit()
    conn.close()


def add_user(username, email, age, db_name='products.db'):
    """Добавляет нового пользователя в таблицу Users."""
    conn = create_connection(db_name)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)', (username, email, age, 1000))
    conn.commit()
    conn.close()


def is_included(username, db_name='products.db'):
    """Проверяет, существует ли пользователь с данным именем в таблице Users."""
    conn = create_connection(db_name)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    return user is not None
