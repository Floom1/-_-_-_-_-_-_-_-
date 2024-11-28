import sqlite3

# Подключение к базе данных
conn = sqlite3.connect("sports_training.db")
cursor = conn.cursor()

# Создание таблицы role
cursor.execute('''
    CREATE TABLE IF NOT EXISTS role (
        id_role INTEGER PRIMARY KEY,
        name_role TEXT UNIQUE NOT NULL
    )
''')

# Заполнение таблицы role
cursor.execute("INSERT OR IGNORE INTO role (name_role) VALUES ('admin')")
cursor.execute("INSERT OR IGNORE INTO role (name_role) VALUES ('user')")

# Создание таблицы login_password
cursor.execute('''
    CREATE TABLE IF NOT EXISTS login_password (
        id_login INTEGER PRIMARY KEY,
        login TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        id_role INTEGER,
        FOREIGN KEY (id_role) REFERENCES role (id_role)
    )
''')

# Создание таблицы admin
cursor.execute('''
    CREATE TABLE IF NOT EXISTS admin (
        id_admin INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        id_login INTEGER,
        FOREIGN KEY (id_login) REFERENCES login_password (id_login)
    )
''')

# Создание таблицы amateur_athlete
cursor.execute('''
    CREATE TABLE IF NOT EXISTS amateur_athlete (
        id_sportsman INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        sex TEXT CHECK(sex IN ('M', 'F')),
        id_login INTEGER,
        FOREIGN KEY (id_login) REFERENCES login_password (id_login)
    )
''')

# Создание таблицы training
cursor.execute('''
    CREATE TABLE IF NOT EXISTS training (
        id_training INTEGER PRIMARY KEY,
        type TEXT NOT NULL,
        date DATE NOT NULL,
        comment TEXT,
        duration TIME,
        id_sportsman INTEGER,
        FOREIGN KEY (id_sportsman) REFERENCES amateur_athlete (id_sportsman)
    )
''')

# Сохранение изменений и закрытие соединения
conn.commit()
conn.close()

print("База данных и таблицы успешно созданы.")
