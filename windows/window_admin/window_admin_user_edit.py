from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLineEdit, QMessageBox
from PyQt5.QtCore import Qt, pyqtSignal
from database.database_work import create_connection
from windows.user_window.window_user_train import WindowForUserTraining
from styles.app_style import apply_style


# ОкноВзаимодействия с конкретным пользователем
class WindowUserEdit(QWidget):
    user_deleted = pyqtSignal()  # Сигнал для обновления таблицы в главном окне

    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.setWindowTitle("Изменение пользователя")
        self.setFixedSize(400, 300)  # Задать фиксированный размер окна

        # Применить стиль из app_style
        apply_style(self)

        # Основная компоновка
        self.layout = QVBoxLayout(self)

        self.btn_back = QPushButton("← Назад")
        self.btn_back.clicked.connect(self.back_to_main_window)
        self.layout.addWidget(self.btn_back)

        # Поле ввода логина
        self.login_input = QLineEdit(self)
        self.login_input.setPlaceholderText("Введите новый Логин")  # Добавлен текст-заполнитель
        self.layout.addWidget(self.login_input)

        # Кнопка для обновления логина
        self.btn_update_login = QPushButton("Обновить Логин")
        self.btn_update_login.clicked.connect(self.update_login)
        self.layout.addWidget(self.btn_update_login)

        # Кнопка для удаления пользователя
        self.btn_delete_user = QPushButton("Удалить пользователя")
        self.btn_delete_user.clicked.connect(self.delete_user)
        self.layout.addWidget(self.btn_delete_user)

        # Кнопка для просмотра тренировок
        self.btn_view_trainings = QPushButton("Просмотреть тренировки")
        self.btn_view_trainings.clicked.connect(self.open_trainings_window)
        self.layout.addWidget(self.btn_view_trainings)

        # Загрузить данные пользователя
        self.load_user_data()


    # Загрузка логина пользователя из БД
    def load_user_data(self):
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT login FROM login_password WHERE id_login = ?", (self.user_id,))
        result = cursor.fetchone()
        conn.close()
        if result:
            self.login_input.setText(result[0])

    # Обновление логина пользователя
    def update_login(self):
        new_login = self.login_input.text()
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE login_password SET login = ? WHERE id_login = ?", (new_login, self.user_id))
        conn.commit()
        conn.close()
        QMessageBox.information(self, "Успех", "Логин успешно обновлен.")

    # Удаление пользователя и всех его тренировок
    def delete_user(self):
        reply = QMessageBox.question(self, "Подтверждение удаления", "Вы уверены, что хотите удаить пользователя и все связанные с ним данные?",
                                    QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            conn = create_connection()
            cursor = conn.cursor()

            # Удаление всех тренировок пользователя
            cursor.execute("DELETE FROM training WHERE id_sportsman = (SELECT id_sportsman FROM amateur_athlete WHERE id_login = ?)", (self.user_id,))

            # Удаление данных пользователя
            cursor.execute("DELETE FROM login_password WHERE id_login = ?", (self.user_id,))
            cursor.execute("DELETE FROM amateur_athlete WHERE id_login = ?", (self.user_id,))

            conn.commit()
            conn.close()

            QMessageBox.information(self, "Успех",  "Пользователь и его данные удалены.")

            self.user_deleted.emit()  # Отправка сигнала об удалении
            self.close()

    # Открытие окна для просмотра и управления тренировками пользователя
    def open_trainings_window(self):
        from windows.window_admin.window_admin_train import WindowAdminTrain
        self.close()

        self.window = WindowAdminTrain(self.user_id)
        self.window.show()

    def back_to_main_window(self):
        from windows.window_admin.window_admin_select import AdminMainWindow

        self.close()  # Закрываем текущее окно
        self.admin_main_window = AdminMainWindow()  # Создаем новое окно
        self.admin_main_window.show()
