import sys

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QDialog, QPushButton, QMessageBox
from windows.user_window.window_user_greet import WindowForUserGreet
from windows.window_admin.window_admin_select import AdminMainWindow
from styles.login_style import apply_login_style
from database.database_work import create_connection, check_user_exists  # Импортируем create_connection
from windows.window_register import RegisterDialog


# Класс окно для авторизации
class PasswordWindow(QWidget):
    def __init__(self): # Инициализация
        super().__init__()

        self.setWindowTitle("Авторизация")
        self.setGeometry(700, 450, 600, 150)

        layout = QVBoxLayout()

        self.username_label = QLabel("Имя пользователя")
        self.username_input = QLineEdit()
        self.password_label = QLabel("Пароль")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.login_button = QPushButton("Войти")
        self.login_button.clicked.connect(self.check_password)

        self.register_button = QPushButton("Нет аккаунта?")
        self.register_button.clicked.connect(self.open_register_dialog)

        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        layout.addWidget(self.register_button)

        apply_login_style(self)

        self.setLayout(layout)

    # Проверка пароля введенного пользователем
    def check_password(self):
        username = self.username_input.text()
        password = self.password_input.text()

        # Проверка существования пользователя и получение его ID и роли
        user = self.get_user_role(username, password)
        if user:
            user_id, role_id = user  # user_id теперь доступен для передачи
            self.open_window(user_id, role_id)
        else:
            self.show_error_message("Ошибка авторизации", "Неверное имя пользователя или пароль")


    # Запрос к базе данных, для выяснения роли пользователя
    def get_user_role(self, username, password):
        # Проверяем пользователя и возвращаем его роль
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id_login, id_role FROM login_password WHERE login = ? AND password = ?",
            (username, password)
        )
        user = cursor.fetchone()
        conn.close()

        if user and len(user) == 2:
            return user
        return None

    # Открытие окно в соответствии с ролью пользователя
    def open_window(self, user_id, role_id):
        self.close()
        if role_id == 1:  # ID для admin
            self.window = AdminMainWindow()
        elif role_id == 2:  # ID для user
            self.window = WindowForUserGreet(user_id)  # Передаем user_id

        self.window.show() #Не закрывается
        # window.exec_() # Закрывается 2 раза


    # Открытие диалога регистрации
    def open_register_dialog(self):
        dialog = RegisterDialog()
        if dialog.exec_() == QDialog.Accepted:
            QMessageBox.information(self, "Успех", "Теперь вы можете войти в систему с вашим новым аккаунтом.")


    # Вывод сообщения об ошибке
    def show_error_message(self, title, message):
        msg_box = QMessageBox()
        apply_login_style(msg_box)
        msg_box.setIcon(QMessageBox.Icon.Critical)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec_()
