from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(648, 525)
        self.verticalLayoutWidget = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(20, 20, 600, 400))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lbl_greeting = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.lbl_greeting.setObjectName("lbl_greeting")
        self.verticalLayout.addWidget(self.lbl_greeting)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btn_view_train = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.btn_view_train.setObjectName("btn_view_train")
        self.horizontalLayout.addWidget(self.btn_view_train)
        self.btn_progress = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.btn_progress.setObjectName("btn_progress")
        self.horizontalLayout.addWidget(self.btn_progress)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.btn_fat_perc = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.btn_fat_perc.setObjectName("btn_fat_perc")
        self.verticalLayout.addWidget(self.btn_fat_perc)
        self.lbl_last_train = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.lbl_last_train.setObjectName("lbl_last_train")
        self.verticalLayout.addWidget(self.lbl_last_train)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Выбор использования"))
        self.lbl_greeting.setText(_translate("Form", "Добро пожаловать, "))
        self.btn_view_train.setText(_translate("Form", "Просмотреть тренировки"))
        self.btn_progress.setText(_translate("Form", "Отследить прогресс"))
        self.btn_fat_perc.setText(_translate("Form", "Вычислить %ЖМТ"))
        self.lbl_last_train.setText(_translate("Form", "Последняя тренировка была "))
