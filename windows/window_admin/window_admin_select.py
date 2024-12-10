from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox
from database.database_work import create_connection

from styles.app_style import apply_style
from windows.window_admin.window_admin_user_edit import WindowUserEdit


# Класс главного окна выбора пользователя для админа
class AdminMainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Панель админа - Выбор пользователя")
        self.resize(600, 400)

        # таблица пользователей
        self.layout = QVBoxLayout(self)
        self.table_users = QTableWidget(self)
        self.table_users.setColumnCount(2)
        self.table_users.setHorizontalHeaderLabels(["ID", "Имя"])
        self.layout.addWidget(self.table_users)

        # Кнопки выбрать и удалить
        self.btn_select_user = QPushButton("Выбрать пользователя")
        self.btn_select_user.clicked.connect(self.open_user_edit_window)
        self.layout.addWidget(self.btn_select_user)

        self.btn_delete_user = QPushButton("Удалить пользователя")
        self.btn_delete_user.clicked.connect(self.delete_user)
        self.layout.addWidget(self.btn_delete_user)

        self.load_users()
        apply_style(self)


    # Выгрузка данных о пользователях для загрузки в таблицу
    def load_users(self):
        """Loads users from the database into the table."""
        self.table_users.setRowCount(0)
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id_login, name FROM amateur_athlete")
        users = cursor.fetchall()
        conn.close()

        for row_num, user in enumerate(users):
            self.table_users.insertRow(row_num)
            for col_num, data in enumerate(user):
                self.table_users.setItem(row_num, col_num, QTableWidgetItem(str(data)))


    # Функция для кнопки Выбрать пользователя открывает окно взаимодействия с ним
    def open_user_edit_window(self):
        selected_row = self.table_users.currentRow()
        if selected_row != -1:
            user_id = int(self.table_users.item(selected_row, 0).text())
            self.close()  # Закрываем текущее окно
            self.user_edit_window = WindowUserEdit(user_id)
            self.user_edit_window.show()
            self.user_edit_window.user_deleted.connect(self.refresh_table)  # Подключаем сигнал для обновления таблицы
        else:
            QMessageBox.warning(self, "Пользователь не выбран", "Пожалуйста, выберите пользователя.")


    # Функция кнопки Удалить пользователя - удаление пользователя и всех связанных с ним данных из БД
    def delete_user(self):
        selected_row = self.table_users.currentRow()
        if selected_row != -1:
            user_id = int(self.table_users.item(selected_row, 0).text())
            confirm = QMessageBox.question(
                self, "Подтверждение удаления",
                f"Вы уверены что хотите удалить пользователя с ID {user_id}?",
                QMessageBox.Yes | QMessageBox.No
            )
            if confirm == QMessageBox.Yes:
                conn = create_connection()
                cursor = conn.cursor()
                cursor.execute("""DELETE FROM training WHERE id_sportsman = (SELECT id_sportsman
                               FROM amateur_athlete WHERE id_login = ?)""", (user_id,))
                cursor.execute("DELETE FROM amateur_athlete WHERE id_login = ?", (user_id,))
                cursor.execute("DELETE FROM login_password WHERE id_login = ?", (user_id,))
                conn.commit()
                conn.close()
                self.refresh_table()
        else:
            QMessageBox.warning(self, "Пользователь не выбран", "Пожалуйста, выберите пользователя.")


    # Перезагрузка таблицы
    def refresh_table(self):
        self.load_users()
