from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from styles.login_style import apply_login_style
from database.database_work import get_user_gender


# Класс окно для вычисления %ЖМТ
class WindowUserFat(QWidget):
    def __init__(self, user_id): # Инициализация
        super().__init__()
        self.user_id = user_id
        self.setWindowTitle("Расчёт процента жира")
        self.setGeometry(600, 200, 800, 600)

        layout = QVBoxLayout()

        # Кнопка назад
        self.back_button = QPushButton("← Назад")
        self.back_button.clicked.connect(self.go_back)

        self.belly_girth_input = QLineEdit()
        self.belly_girth_input.setPlaceholderText("Введите ваш обхват живота")
        self.belly_girth_input.setToolTip("Обхват живота в сантиметрах")

        self.weight_input = QLineEdit()
        self.weight_input.setPlaceholderText("Введите ваш вес")
        self.weight_input.setToolTip("Вес в килограммах")

        self.calculate_button = QPushButton("Вычислить")
        self.calculate_button.clicked.connect(self.calculate_fat_percentage)

        # Добавление кнопок в layout
        layout.addWidget(self.back_button)
        layout.addWidget(QLabel("Введите ваш обхват живота (в см):"))
        layout.addWidget(self.belly_girth_input)
        layout.addWidget(QLabel("Введите ваш вес (в кг):"))
        layout.addWidget(self.weight_input)
        layout.addWidget(self.calculate_button)

        apply_login_style(self)

        self.setLayout(layout)


    # функция кнопки назад - возвращение в предыдущее окно
    def go_back(self):
        from windows.user_window.window_user_greet import WindowForUserGreet
        self.close()
        self.window = WindowForUserGreet(self.user_id)
        self.window.show()


    # Функция кнопки Вычислить - вычисление %ЖМТ и проверка данных
    def calculate_fat_percentage(self):
        try:
            belly_girth = float(self.belly_girth_input.text())
            weight = float(self.weight_input.text())

            if belly_girth < 50:
                raise ValueError("Обхват живота должен быть не меньше 50 см.")
            if belly_girth > 225:
                raise ValueError("Обхват живота должен быть не больше 225 см.")
            if weight < 30:
                raise ValueError("Вес должен быть не меньше 30 кг.")
            if weight > 165:
                raise ValueError("Вес должен быть не больше 165 кг.")
        except ValueError as e:
            self.show_error_dialog(str(e))
            return

        gender = get_user_gender(self.user_id)
        fat_percentage = self.fat_percentage(gender, belly_girth, weight)

        self.show_result_dialog(f"Процент жира: {fat_percentage}%")


    # Функция расчёта процента жира
    @staticmethod
    def fat_percentage(gender, belly_girth, weight):
        if gender == 'M':
            fat = belly_girth * 0.74 - weight * 0.082 - 34.89
        else:
            fat = belly_girth * 0.74 - weight * 0.082 - 44.74
        return round(fat, 2)


    # Функция показа диалогового окна с ошибкой
    def show_error_dialog(self, message):
        dialog = QMessageBox(self)
        dialog.setWindowTitle("Ошибка")
        dialog.setText(message)
        dialog.setIcon(QMessageBox.Icon.Warning)
        apply_login_style(dialog)
        dialog.exec_()


    # Функция показа диалогового окна с результатом
    def show_result_dialog(self, message):
        dialog = QMessageBox(self)
        dialog.setWindowTitle("Результат")
        dialog.setText(message)
        dialog.setIcon(QMessageBox.Icon.Information)
        apply_login_style(dialog)
        dialog.exec_()
