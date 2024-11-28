from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget

def apply_login_style(window: QWidget):
    # Настройка стиля
    style_sheet = """
        /*Стиль окна */
        QWidget {
            background-color: #890620;  /* Основной фон окна */
            color: #D9CAB3;
            font-family: Verdana, Arial, Helvetica, sans-serif;
            font-size: 19px;
        }

        /*Стиль надписи */
        QLabel {
            color: #D9CAB3;
            font-size: 17px;
        }

        /*Стиль текстового поля */
        QLineEdit {
            background-color: #19180A;
            color: #D9CAB3;
            padding: 5px;
            border: 1px solid #D9CAB3;
            border-radius: 5px;
            font-size: 15px;
        }

        /*Стиль кнопки */
        QPushButton {
            background-color: #19180A;
            color: #D9CAB3;
            border-radius: 5px;
            padding: 7px 15px;
            font-size: 17px;
        }

        /*Стиль кнопки при наведении */
        QPushButton:hover {
            background-color: #c4172b;
        }

        /*Стиль уведомления */
        QMessageBox {
            background-color: #890620;
            color: #D9CAB3;
            font-family: 'Comic Sans';
            font-size: 14px;
        }
    """

    # Применение стиля к окну
    window.setStyleSheet(style_sheet)

    # Применение шрифта ко всему окну (замените шрифт и размер при необходимости)
    font = QFont("Comic Sans", 14)
    window.setFont(font)
