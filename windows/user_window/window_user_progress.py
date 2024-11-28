from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QFileDialog
from PyQt5.QtChart import QChart, QChartView, QLineSeries, QDateTimeAxis, QValueAxis, QScatterSeries
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtCore import Qt, QDateTime

from database.database_work import get_user_name, get_user_trainings, get_sportsman_id
from windows.user_window.window_user_greet import WindowForUserGreet
from styles.app_style import apply_style

from openpyxl import Workbook
from openpyxl.drawing.image import Image


# Класс отображения графика прогресса пользователя
class WindowForUserProgress(QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id

        self.setWindowTitle("Прогресс пользователя")
        self.setGeometry(600, 200, 800, 600)

        # Применяем стиль
        apply_style(self)

        # Получение имени пользователя
        user_name = get_user_name(user_id)

        # Метка с приветствием
        self.label = QLabel(f"Вот ваши результаты, {user_name}.")
        self.label.setAlignment(Qt.AlignCenter)

        # Кнопка для возврата
        self.back_button = QPushButton("← Назад")
        self.back_button.clicked.connect(self.go_back)

        self.export_button = QPushButton("Экспорт данных")
        self.export_button.clicked.connect(self.export_data)

        # Настройка графика
        self.chart_view = self.create_progress_chart()

        # Размещение элементов на экране
        layout = QVBoxLayout()
        layout.addWidget(self.back_button)
        layout.addWidget(self.label)
        layout.addWidget(self.chart_view)
        layout.addWidget(self.export_button)
        self.setLayout(layout)


    # Создание графика прогресса по длительности тренировок
    def create_progress_chart(self):
        # Создание серии данных для графика
        series = QLineSeries()
        scatter_series = QScatterSeries()
        scatter_series.setMarkerShape(QScatterSeries.MarkerShapeCircle)  # Точки будут круглыми

        # Получение данных тренировок из базы данных
        trainings = get_user_trainings(get_sportsman_id(self.user_id))

        # Заполнение серии данных по датам и длительности тренировок
        for training in trainings:
            date = QDateTime.fromString(training["date"], "yyyy-MM-dd")
            duration = training["duration"]

            # Проверка типа и преобразование, если необходимо
            if isinstance(duration, str) and ":" in duration:
                # Если длительность в формате "часы:минуты"
                hours, minutes = map(int, duration.split(":"))
                total_minutes = hours * 60 + minutes
            elif isinstance(duration, int):

                total_minutes = duration
            else:
                total_minutes = 0  # Если данные некорректные, ставим 0


            series.append(date.toMSecsSinceEpoch(), total_minutes)
            scatter_series.append(date.toMSecsSinceEpoch(), total_minutes)

        # Создание объекта графика и добавление серии
        chart = QChart()
        chart.addSeries(series)
        chart.addSeries(scatter_series)

        chart.legend().setVisible(False)

        # Настройка оси времени по горизонтали
        axis_x = QDateTimeAxis()
        axis_x.setFormat("dd-MM-yyyy")
        chart.addAxis(axis_x, Qt.AlignBottom)
        series.attachAxis(axis_x)
        scatter_series.attachAxis(axis_x)

        # Настройка оси значений по вертикали
        axis_y = QValueAxis()
        axis_y.setLabelFormat("%i")
        axis_y.setMin(0)  # Устанавливаем минимальное значение оси Y в 0
        axis_y.setRange(0, max([training["duration"] for training in trainings]))  # Устанавливаем диапазон оси Y от 0 до максимальной продолжительности тренировки
        chart.addAxis(axis_y, Qt.AlignLeft)
        series.attachAxis(axis_y)
        scatter_series.attachAxis(axis_y)

        # Установка меток на оси X
        dates = [QDateTime.fromString(training["date"], "yyyy-MM-dd") for training in trainings]
        axis_x.setTickCount(len(dates))
        axis_x.setMin(dates[0])
        axis_x.setMax(dates[-1])

        # Применение дополнительного стиля к графику
        self.apply_chart_style(chart, series, scatter_series)

        # Отображение графика
        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)
        return chart_view

    # Применение стиля к графику
    def apply_chart_style(self, chart, series, scatter_series):
        # Устанавливаем стиль для фона и текста
        chart.setBackgroundBrush(Qt.transparent)  # Прозрачный фон
        chart.setPlotAreaBackgroundBrush(Qt.transparent)  # Прозрачный фон области графика

        # Устанавливаем стиль для линии и точек
        series.setPen(QPen(QColor("#e7691d"), 2))  # Цвет линии

        # Устанавливаем стиль для точек
        scatter_series.setBrush(QColor("#1D67E7"))  # Закрашенный цвет точек
        scatter_series.setMarkerSize(10)  # Устанавливаем размер точек побольше

        # Настройка цвета текста осей
        axis_x = chart.axisX()
        axis_y = chart.axisY()

        axis_x.setLabelsColor(QColor("#D9CAB3"))
        axis_y.setLabelsColor(QColor("#D9CAB3"))

        # Установка цвета для заголовков осей
        axis_x.setTitleText("Дата")
        axis_y.setTitleText("Длительность (мин)")
        axis_x.setTitleBrush(QColor("#D9CAB3"))
        axis_y.setTitleBrush(QColor("#D9CAB3"))

        # Устанавливаем цвет заголовка графика (названия)
        chart.setTitleBrush(QColor("#D9CAB3"))  # Цвет заголовка графика
        chart.setTitle("Прогресс по длительности тренировок")  # Название диаграммы


    # Экспорт графика с таблицей в Excel
    def export_data(self):
        # Открытие диалогового окна для выбора пути сохранения
        file_dialog = QFileDialog(self)
        file_path, _ = file_dialog.getSaveFileName(self, "Сохранить файл", "", "Excel Files (*.xlsx)")

        if file_path:
            # Сначала сохраняем график как изображение
            chart_image = self.chart_view.grab()
            image_path = file_path.replace(".xlsx", ".png")
            chart_image.save(image_path)

            # Создание рабочей книги
            wb = Workbook()
            ws = wb.active
            ws.title = "Прогресс тренировок"

            # Запись заголовков столбцов
            ws.append(["Дата", "Длительность (мин)"])

            # Получение данных тренировок
            trainings = get_user_trainings(get_sportsman_id(self.user_id))

            # Запись данных о тренировках в Excel
            for training in trainings:
                date = training["date"]
                duration = training["duration"]

                # Проверка типа и преобразование, если необходимо
                if isinstance(duration, str) and ":" in duration:
                    # Если длительность в формате "часы:минуты"
                    hours, minutes = map(int, duration.split(":"))
                    total_minutes = hours * 60 + minutes
                elif isinstance(duration, int):
                    # Если длительность в минутах (целое число)
                    total_minutes = duration
                else:
                    total_minutes = 0  # Если данные некорректные, ставим 0

                # Запись строки в таблицу Excel
                ws.append([date, total_minutes])

            # Вставка изображения графика в Excel
            img = Image(image_path)
            ws.add_image(img, 'E5')  # Вставляем картинку в ячейку E5

            # Сохранение файла Excel
            wb.save(file_path)
            print(f"Data exported successfully to {file_path}")


    # Открыть предыдущее окно
    def go_back(self):
        # Закрытие текущего окна и возврат к окну приветствия
        self.close()
        self.window = WindowForUserGreet(self.user_id)
        self.window.show()