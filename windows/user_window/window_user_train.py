import pandas as pd

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QWidget ,QTableWidgetItem,
                             QLabel, QLineEdit, QMessageBox, QComboBox,
                             QDateEdit, QTextEdit, QTimeEdit, QDialogButtonBox, QFileDialog)
from PyQt5.QtCore import QDate, QTime

from interfaces.ui_window import Ui_Form
from styles.app_style import apply_style
from database.database_work import create_connection, get_sportsman_id


# Класс диалога для добавления тренировок
class AddTrainingDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Добавить новую тренировку")

        # Поле выбора тренировки
        self.type_label = QLabel("Тип тренировки:")
        self.type_combo = QComboBox()
        self.type_combo.addItems(["Грудь", "Бицепс", "Трицепс", "Дельты", "Пресс", "Ноги", "Шея", "Свой вариант..."])
        self.custom_type_input = QLineEdit()
        self.custom_type_input.setPlaceholderText("Введите свой вариант")
        self.custom_type_input.setVisible(False)

        # Показать поле, если выбран свой вариант
        self.type_combo.currentIndexChanged.connect(self.show_custom_type_input)

        # Выбор даты
        self.date_label = QLabel("Дата:")
        self.date_edit = QDateEdit(calendarPopup=True)
        self.date_edit.setDate(QDate.currentDate())

        self.comment_label = QLabel("Комментарий:")
        self.comment_edit = QTextEdit()

        # Длительность
        self.duration_label = QLabel("Длительность:")
        self.duration_edit = QTimeEdit()
        self.duration_edit.setTime(QTime(0, 30))  # Default duration: 30 min
        self.duration_edit.setMaximumTime(QTime(3, 30))

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        self.button_box.button(QDialogButtonBox.Ok).setText("Ок")
        self.button_box.button(QDialogButtonBox.Cancel).setText("Отмена")

        self.button_box.accepted.connect(self.validate_data)
        self.button_box.rejected.connect(self.reject)

        # Заполнение layout`а
        layout = QVBoxLayout()
        layout.addWidget(self.type_label)
        layout.addWidget(self.type_combo)
        layout.addWidget(self.custom_type_input)
        layout.addWidget(self.date_label)
        layout.addWidget(self.date_edit)
        layout.addWidget(self.comment_label)
        layout.addWidget(self.comment_edit)
        layout.addWidget(self.duration_label)
        layout.addWidget(self.duration_edit)
        layout.addWidget(self.button_box)
        self.setLayout(layout)

        apply_style(self)

    # Функция для показа своего варианта
    def show_custom_type_input(self, index):
        if self.type_combo.currentText() == "Свой вариант...":
            self.custom_type_input.setVisible(True)
        else:
            self.custom_type_input.setVisible(False)
            self.custom_type_input.clear()

    # Функция для проверки введенных данных
    def validate_data(self):
        selected_date = self.date_edit.date()
        current_date = QDate.currentDate()

        # Проверка на дату
        if selected_date > current_date:
            self.show_error_message("Дата тренировки не может быть позже сегодняшнего дня.")
            return

        # Если все проверки пройдены
        self.accept()

    # Функция для отображения ошибки
    def show_error_message(self, message):
        error_dialog = QMessageBox(self)
        error_dialog.setWindowTitle("Ошибка")
        error_dialog.setIcon(QMessageBox.Warning)
        error_dialog.setText(message)
        apply_style(error_dialog)
        error_dialog.exec_()

    # Функция для возврата введенных данных
    def get_data(self):
        if self.custom_type_input.text():
            type_text = self.custom_type_input.text()
        else:
            type_text = self.type_combo.currentText()

        return {
            "type": type_text,
            "date": self.date_edit.date().toString("yyyy-MM-dd"),
            "comments": self.comment_edit.toPlainText(),
            "duration": self.duration_edit.time().toString("HH:mm:ss")
        }


# Класс для отображения окно с таблицей тренировок пользователя
class WindowForUserTraining(QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        apply_style(self)

        # Настройка сигналов для кнопок
        self.ui.btn_add_training.clicked.connect(self.add_training)
        self.ui.btn_view_progress.clicked.connect(self.view_progress)
        self.ui.back_button.clicked.connect(self.go_back)

        self.load_trainings()


    # Запрос к базе данных для заполнения таблицы тренировками
    def load_trainings(self):
        # Clear table before populating
        self.ui.table_trainings.setRowCount(0)

        id_sportsman = get_sportsman_id(self.user_id)
    # Проверка, если id_sportsman не найден
        if id_sportsman is None:
            print("Спортсмен с данным id_login не найден.")
            return

        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT date, type, duration, comment FROM training WHERE id_sportsman = ?", (id_sportsman,))
        trainings = cursor.fetchall()
        conn.close()

        # Заполнение таблицы
        for row_number, row_data in enumerate(trainings):
            self.ui.table_trainings.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.ui.table_trainings.setItem(row_number, column_number, QTableWidgetItem(str(data)))


    # Добавление новой тренировки
    def add_training(self):
        dialog = AddTrainingDialog()

        # Если пользователь нажал "OK" в диалоговом окне, только тогда продолжаем добавление
        if dialog.exec_() == QDialog.Accepted:
            # Получаем введенные данные
            training_data = dialog.get_data()

            # Добавление новой тренировки в базу данных
            try:
                conn = create_connection()
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO training (id_sportsman, date, type, duration, comment) VALUES (?, ?, ?, ?, ?)",
                    (get_sportsman_id(self.user_id), training_data["date"], training_data["type"], training_data["duration"], training_data["comments"])
                )
                conn.commit()
                conn.close()

                # Обновление таблицы для отображения новой записи
                self.load_trainings()

            except Exception as e:
                print("Ошибка при добавлении тренировки:", e)


    # Экспорт таблицы в Excel файл
    def view_progress(self):
        # Диалог для выбора пути сохранения
        file_path, _ = QFileDialog.getSaveFileName(self, "Сохранить файл", "", "Excel Files (*.xlsx)")

        if not file_path:
            return  # Пользователь отменил выбор пути

        # Подключение к базе данных и извлечение тренировок для определенного спортсмена
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT date, type, duration, comment FROM training WHERE id_sportsman = ?", (get_sportsman_id(self.user_id),))
        trainings = cursor.fetchall()
        conn.close()

        # Преобразование данных в DataFrame
        columns = ["Date", "Type", "Duration", "Comment"]
        df = pd.DataFrame(trainings, columns=columns)

        # Сохранение DataFrame в Excel
        try:
            df.to_excel(file_path, index=False)
            print("Таблица тренировок успешно сохранена.")
        except Exception as e:
            print("Ошибка при сохранении файла:", e)


    # Возврат в окно приветствия
    def go_back(self):
        from windows.user_window.window_user_greet import WindowForUserGreet
        # Закрываем текущее окно и возвращаемся к окну приветствия
        self.close()
        self.window = WindowForUserGreet(self.user_id)
        self.window.show()