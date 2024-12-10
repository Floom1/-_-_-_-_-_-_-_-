import pandas as pd

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QFileDialog

from styles.app_style import apply_style
from database.database_work import create_connection
from windows.window_admin.window_admin_user_edit import WindowUserEdit


# Класс просмотра тренировок пользователя для админа
class WindowAdminTrain(QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.setWindowTitle("Запись тренировок пользователя")

        self.resize(800, 600)

        self.layout = QVBoxLayout(self)

        self.btn_back = QPushButton("← Назад")
        self.btn_back.clicked.connect(self.go_back)
        self.layout.addWidget(self.btn_back)

        # Таблица с тренировками
        self.table_trainings = QTableWidget()
        self.layout.addWidget(self.table_trainings)

        # Загрузка данных в таблицу
        self.load_trainings()

        self.btn_delete_training = QPushButton("Удалить выбранную тренировку")
        self.btn_delete_training.clicked.connect(self.delete_selected_training)
        self.layout.addWidget(self.btn_delete_training)

        self.btn_delete_all_trainings = QPushButton("Удалить все тренировки")
        self.btn_delete_all_trainings.clicked.connect(self.delete_all_trainings)
        self.layout.addWidget(self.btn_delete_all_trainings)

        self.btn_export_to_excel = QPushButton("Экспорт в Excel")
        self.btn_export_to_excel.clicked.connect(self.export_to_excel)
        self.layout.addWidget(self.btn_export_to_excel)

        apply_style(self)


    # Обращение к БД чтобы заполнить таблицу тренировками
    def load_trainings(self):
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT date, type, duration, comment FROM training WHERE id_sportsman = (SELECT id_sportsman FROM amateur_athlete WHERE id_login = ?)", (self.user_id,))
        trainings = cursor.fetchall()
        conn.close()

        # Конфигурация и заполнение таблицы
        self.table_trainings.setRowCount(len(trainings))
        self.table_trainings.setColumnCount(4)
        self.table_trainings.setHorizontalHeaderLabels(["Дата", "Тип", "Длительность", "Комментарий"])

        for row_num, row_data in enumerate(trainings):
            for col_num, data in enumerate(row_data):
                self.table_trainings.setItem(row_num, col_num, QTableWidgetItem(str(data)))


    # Открыть предыдущее окно
    def go_back(self):
        self.close()
        self.user_edit_window = WindowUserEdit(self.user_id)
        self.user_edit_window.show()


    # Удаление выбранной тренировки
    def delete_selected_training(self):
        selected_row = self.table_trainings.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Нет выбора",
                                 "Пожалуйста, выберите тренировку, чтобы удалить.")
            return

        reply = QMessageBox.question(self, "Подтверждение удаления",
                                      "Вы уверены, что хотите удалить эту тренировку?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            date = self.table_trainings.item(selected_row, 0).text()
            conn = create_connection()
            cursor = conn.cursor()
            cursor.execute("""DELETE FROM training
                            WHERE date = ? AND id_sportsman = (SELECT id_sportsman
                            FROM amateur_athlete WHERE id_login = ?)""", (date, self.user_id))
            conn.commit()
            conn.close()

            self.table_trainings.removeRow(selected_row)
            QMessageBox.information(self, "Удаление", "Выбранная тренировка успешно удалена.")


    # Удаление всех тренировок
    def delete_all_trainings(self):
        reply = QMessageBox.question(self, "Подтверждение удаления",
                                      "Вы уверены, что хотите удалить ВСЕ тренировки?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            conn = create_connection()
            cursor = conn.cursor()
            cursor.execute("""DELETE FROM training
                           WHERE id_sportsman = (SELECT id_sportsman
                           FROM amateur_athlete WHERE id_login = ?)""", (self.user_id,))
            conn.commit()
            conn.close()

            self.load_trainings()
            QMessageBox.information(self, "Удаление", "Все тренировки успешно удалены.")


    # Экспорт данных в эксель
    def export_to_excel(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save as Excel", "", "Excel Files (*.xlsx)")
        if not file_path:
            return

        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT date, type, duration, comment FROM training WHERE id_sportsman = (SELECT id_sportsman FROM amateur_athlete WHERE id_login = ?)", (self.user_id,))
        trainings = cursor.fetchall()
        conn.close()

        df = pd.DataFrame(trainings, columns=["Дата", "Тип", "Длительность", "Комментарий"])
        try:
            df.to_excel(file_path, index=False)
            QMessageBox.information(self, "Сохранение", "Тренировки успешно сохранены в Excel.")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Экспорт в эксель не совершен: {e}")
