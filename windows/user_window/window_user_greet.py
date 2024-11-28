from PyQt5.QtWidgets import QWidget

from interfaces.user_greet_design import Ui_Form
from styles.login_style import apply_login_style
from windows.user_window.window_user_train import WindowForUserTraining
from database.database_work import get_user_name, get_last_training


# Класс окно с приветствием пользователя
class WindowForUserGreet(QWidget):
    def __init__(self, user_id): # Инициализация
        super().__init__()
        self.user_id = user_id
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        apply_login_style(self)

        user_name = get_user_name(user_id)  # Получаем имя пользователя по ID
        if user_name:
            self.ui.lbl_greeting.setText(f"Добро пожаловать, {user_name}")

        # Проверка и отображение последней тренировки
        last_training_date = get_last_training(user_id)  # Получаем дату последней тренировки
        if last_training_date:
            self.ui.lbl_last_train.setText(f"Последняя тренировка была {last_training_date}")
        else:
            self.ui.lbl_last_train.hide()  # Скрываем, если тренировки не было

        # Подключение кнопок
        self.ui.btn_view_train.clicked.connect(self.view_training)
        self.ui.btn_progress.clicked.connect(self.progress_training)
        self.ui.btn_fat_perc.clicked.connect(self.fat_percentage)
        self.show()


    # Функция кнопки Просмотреть тренировки - открыть Окно просмотра тренировок
    def view_training(self):
        self.close()

        self.window = WindowForUserTraining(self.user_id)
        self.window.show()


    # Функция кнопки Прогресс - открыть Окно прогресса тренировок
    def progress_training(self):
        from windows.user_window.window_user_progress import WindowForUserProgress
        self.close()

        self.window = WindowForUserProgress(self.user_id)
        self.window.show()


    # Функция кнопки Вычислить %ЖМТ - открыть Окно вычисления процента жира
    def fat_percentage(self):
        from windows.user_window.window_user_fat import WindowUserFat
        self.close()

        self.window = WindowUserFat(self.user_id)
        self.window.show()
