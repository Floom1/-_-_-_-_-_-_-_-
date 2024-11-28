import sys
import pandas
import matplotlib

from PyQt5.QtWidgets import QApplication
from windows.autorization import PasswordWindow


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PasswordWindow()  # создаем экземпляр окна авторизации
    window.show()
    sys.exit(app.exec_())
