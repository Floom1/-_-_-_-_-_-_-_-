from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QMessageBox
)
from database.database_work import check_user_exists, add_user
from styles.login_style import apply_login_style
import re


# Класс Диалога с регистрацией
class RegisterDialog(QDialog):
    def __init__(self): # Инициализация
        super().__init__()
        self.setWindowTitle("Регистрация нового пользователя")
        self.setGeometry(700, 300, 400, 250)

        layout = QVBoxLayout()

        # Поля для имени, фамилии, пола, логина и пароля
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Имя")
        self.last_name_input = QLineEdit()
        self.last_name_input.setPlaceholderText("Фамилия")

        self.sex_input = QComboBox()
        self.sex_input.addItems(["М", "Ж"])

        self.login_input = QLineEdit()
        self.login_input.setPlaceholderText("Логин")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Пароль")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        # Кнопка для регистрации
        self.register_button = QPushButton("Зарегистрироваться")
        self.register_button.clicked.connect(self.register_user)

        # Добавление виджетов в layout
        layout.addWidget(QLabel("Имя"))
        layout.addWidget(self.name_input)
        layout.addWidget(QLabel("Фамилия"))
        layout.addWidget(self.last_name_input)
        layout.addWidget(QLabel("Пол"))
        layout.addWidget(self.sex_input)
        layout.addWidget(QLabel("Логин"))
        layout.addWidget(self.login_input)
        layout.addWidget(QLabel("Пароль"))
        layout.addWidget(self.password_input)
        layout.addWidget(self.register_button)

        apply_login_style(self)

        self.setLayout(layout)


    # Запись нового пользователя в БД и проверка его данных
    def register_user(self):
        # Получение данных из полей
        name = self.name_input.text()
        last_name = self.last_name_input.text()
        sex = self.sex_input.currentText()
        login = self.login_input.text()
        password = self.password_input.text()

        # Проверка имени и фамилии
        if not re.fullmatch(r"[А-Яа-яЁё]{4,}", name):
            self.show_error("Имя должно быть не менее 4 символов и содержать только русские буквы.")
            return

        if not re.fullmatch(r"[А-Яа-яЁё]{4,}", last_name):
            self.show_error("Фамилия должна быть не менее 4 символов и содержать только русские буквы.")
            return

        # Проверка логина
        if len(login) < 5:
            self.show_error("Логин должен быть не менее 5 символов.")
            return

        if not re.fullmatch(r"[A-Za-zА-Яа-яЁё0-9]+", login):
            self.show_error("Логин может содержать только буквы и цифры.")
            return

        # Проверка пароля
        if len(password) < 7:
            self.show_error("Пароль должен быть не менее 7 символов.")
            return

        if not re.fullmatch(r"[A-Za-z0-9]+", password):
            self.show_error("Пароль может содержать только английские буквы и цифры.")
            return

        # Проверка на существование пользователя
        if check_user_exists(login):
            self.show_error("Пользователь с таким логином уже существует!")
        else:
            add_user(name, last_name, sex, login, password)
            QMessageBox.information(self, "Успех", "Пользователь успешно зарегистрирован!")
            self.accept()  # Закрываем диалоговое окно после успешной регистрации


    # Вспомогательная функция для показа сообщения об ошибке с применением стиля
    def show_error(self, message):
        error_dialog = QMessageBox(self)
        apply_login_style(error_dialog)
        error_dialog.setIcon(QMessageBox.Icon.Warning)
        error_dialog.setWindowTitle("Ошибка")
        error_dialog.setText(message)
        error_dialog.exec()
