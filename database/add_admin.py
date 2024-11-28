import sqlite3

# Подключение к базе данных
conn = sqlite3.connect("sports_training.db")
cursor = conn.cursor()

# Получение id_role для роли 'admin'
cursor.execute("SELECT id_role FROM role WHERE name_role = 'admin'")
admin_role_id = cursor.fetchone()
if admin_role_id:
    admin_role_id = admin_role_id[0]
else:
    print("Ошибка: роль 'admin' не найдена.")
    conn.close()
    exit()

# Вставка данных в таблицу login_password
cursor.execute('''
    INSERT INTO login_password (login, password, id_role)
    VALUES (?, ?, ?)
''', ('admin', 'root', admin_role_id))

# Получение id_login для нового администратора
admin_login_id = cursor.lastrowid

# Вставка данных в таблицу admin
cursor.execute('''
    INSERT INTO admin (name, last_name, id_login)
    VALUES (?, ?, ?)
''', ('Александр', 'Романов', admin_login_id))

# Сохранение изменений и закрытие соединения
conn.commit()
conn.close()

print("Администратор успешно добавлен.")
