from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget

def apply_style(window: QWidget):
    # Настройка стиля
    style_sheet = """
        /* Стиль виджетов - окон */
        QWidget {
            background-color: #890620;
            color: #D9CAB3;
            font-family: 'Comic Sans';
            font-size: 16px;
        }

        /* Стиль кнопок */
        QPushButton {
            background-color: #19180A;
            color: #D9CAB3;
            border-radius: 5px;
            padding: 5px;
            font-size: 16px;
        }

        /* Стиль кнопок при наведении */
        QPushButton:hover {
            background-color: #c4172b;
        }

        /* Стиль таблицы */
        QTableWidget {
            background-color: #bd1327;
            color: #D9CAB3;
            gridline-color: #19180A;
            font-size: 14px;
        }

        /* Стиль заголовков таблицы */
        QHeaderView::section {
            background-color: #333;
            color: #D9CAB3;
            font-weight: bold;
        }

        /* Стиль для диалога заполнения тренировки */
        QDateEdit, QTextEdit, QTimeEdit {
            background-color: #bd1327;
            color: #D9CAB3;
            border: none;
            padding: 5px;
        }

        QDateEdit::drop-down, QTimeEdit::drop-down {
            background-color: #800000; /* Тёмно-красный цвет кнопки */
            border: 1px solid #D9CAB3; /* Добавляем границу для видимости */
            width: 20px; /* Ширина кнопки */
            height: 20px; /* Высота кнопки */
        }
    """
    # Применение стиля к окну
    window.setStyleSheet(style_sheet)

    # Применение шрифта ко всему окну
    font = QFont("Comic Sans", 14)
    window.setFont(font)
