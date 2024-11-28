import sqlite3


# Подключение к базе данных
def create_connection():
    conn = sqlite3.connect("database/sports_training.db")
    return conn


# Проверка наличия пользователя в базе данных по логину
def check_user_exists(login):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM login_password WHERE login = ?", (login,))
    user = cursor.fetchone()
    conn.close()
    return user is not None


# Добавление пользователя в БД
def add_user(name, last_name, sex, login, password):
    conn = create_connection()
    cursor = conn.cursor()

    # Получение id роли 'user' для назначения по умолчанию
    cursor.execute("SELECT id_role FROM role WHERE name_role = 'user'")
    user_role_id = cursor.fetchone()[0]

    # Добавление логина, пароля и роли
    cursor.execute("INSERT INTO login_password (login, password, id_role) VALUES (?, ?, ?)", (login, password, user_role_id))
    id_login = cursor.lastrowid

    # Преобразование пола для записи
    sex = 'M' if sex == 'М' else 'F'

    # Добавление пользователя как Спорстмена
    cursor.execute("INSERT INTO amateur_athlete (name, last_name, sex, id_login) VALUES (?, ?, ?, ?)",
                   (name, last_name, sex, id_login))

    conn.commit()
    conn.close()


# Получение имени пользователя, по его id
def get_user_name(user_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM amateur_athlete WHERE id_login = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None


# Получение последней тренировки пользователя по id
def get_last_training(user_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT date FROM training
        WHERE id_sportsman = (SELECT id_sportsman FROM amateur_athlete WHERE id_login = ?)
        ORDER BY date DESC LIMIT 1
    """, (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None


# Получение всех тренировок пользователя по id
def get_user_trainings(user_id):
    conn = create_connection()
    cursor = conn.cursor()

    # Извлекаем часы и минуты из поля duration
    cursor.execute("""
        SELECT date,
               strftime('%H', duration) AS hours,
               strftime('%M', duration) AS minutes
        FROM training
        WHERE id_sportsman = ?
        ORDER BY date ASC
    """, (user_id,))

    trainings = []
    for row in cursor.fetchall():
        # Преобразуем часы и минуты в общее количество минут
        hours = int(row[1])  # Получаем часы
        minutes = int(row[2])  # Получаем минуты
        total_minutes = hours * 60 + minutes  # Переводим в минуты
        trainings.append({"date": row[0], "duration": total_minutes})

    conn.close()
    return trainings


# Получение пола пользователя
def get_user_gender(user_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT sex FROM amateur_athlete WHERE id_login = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None


# Получение id пользователя
def get_sportsman_id(id_login):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id_sportsman FROM amateur_athlete WHERE id_login = ?", (id_login,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None
