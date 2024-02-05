from datetime import time

from PyQt5 import QtCore, QtWidgets
from toolz import curry

from ..modules.app_config import Preferences


class PrefsDialog(QtWidgets.QDialog):
    _preferences: Preferences

    def __init__(self, config=None):
        super().__init__()
        if config is None:
            config = {}
        self._preferences = Preferences.from_dict(config)
        self.setupUi()
        self.connectControls()
        print("preferences", self._preferences)

    def _toggle_day(self, day):
        def toggle():
            print("toggling day", day)
            days = self._preferences.publish_days
            if day in self._preferences.publish_days:
                self._preferences.publish_days = [d for d in days if d != day]
                return
            self._preferences.publish_days = days + [day]

        return toggle

    @curry
    def _set_property(self, prop, value):
        if value != self._preferences.get(prop):
            setattr(self, prop, value)

    @curry
    def _set_ftp_property(self, prop, value):
        print("FTP SETTINGS", prop, value)
        if value != self._preferences.ftp_config.get(prop):
            setattr(self._preferences.ftp_config, prop, value)

    def setupUi(self):
        self.setObjectName("PrefsDialog")
        self.resize(400, 300)
        self.buttonBox = QtWidgets.QDialogButtonBox(self)
        self.buttonBox.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayoutWidget = QtWidgets.QWidget(self)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 381, 221))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.verticalLayoutWidget)
        self.tabWidget.setObjectName("tabWidget")
        self.schedule_tab = QtWidgets.QWidget()
        self.schedule_tab.setObjectName("schedule_tab")
        self.gridLayoutWidget_2 = QtWidgets.QWidget(self.schedule_tab)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(10, 10, 361, 132))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.mon_checkbox = QtWidgets.QCheckBox(self.gridLayoutWidget_2)
        self.mon_checkbox.setObjectName("mon_checkbox")
        self.mon_checkbox.setChecked(0 in self._preferences.publish_days)
        self.gridLayout_2.addWidget(self.mon_checkbox, 1, 0, 1, 1)
        self.tue_checkbox = QtWidgets.QCheckBox(self.gridLayoutWidget_2)
        self.tue_checkbox.setObjectName("tue_checkbox")
        self.tue_checkbox.setChecked(1 in self._preferences.publish_days)
        self.gridLayout_2.addWidget(self.tue_checkbox, 1, 1, 1, 1)
        self.wed_checkbox = QtWidgets.QCheckBox(self.gridLayoutWidget_2)
        self.wed_checkbox.setObjectName("wed_checkbox")
        self.wed_checkbox.setChecked(2 in self._preferences.publish_days)
        self.gridLayout_2.addWidget(self.wed_checkbox, 1, 2, 1, 1)
        self.thu_checkbox = QtWidgets.QCheckBox(self.gridLayoutWidget_2)
        self.thu_checkbox.setObjectName("thu_checkbox")
        self.thu_checkbox.setChecked(3 in self._preferences.publish_days)
        self.gridLayout_2.addWidget(self.thu_checkbox, 1, 3, 1, 1)
        self.fri_checkbox = QtWidgets.QCheckBox(self.gridLayoutWidget_2)
        self.fri_checkbox.setObjectName("fri_checkbox")
        self.fri_checkbox.setChecked(4 in self._preferences.publish_days)
        self.gridLayout_2.addWidget(self.fri_checkbox, 2, 0, 1, 1)
        self.sat_checkbox = QtWidgets.QCheckBox(self.gridLayoutWidget_2)
        self.sat_checkbox.setObjectName("sat_checkbox")
        self.sat_checkbox.setChecked(5 in self._preferences.publish_days)
        self.gridLayout_2.addWidget(self.sat_checkbox, 2, 1, 1, 1)
        self.sun_checkbox = QtWidgets.QCheckBox(self.gridLayoutWidget_2)
        self.sun_checkbox.setObjectName("sun_checkbox")
        self.sun_checkbox.setChecked(6 in self._preferences.publish_days)
        self.gridLayout_2.addWidget(self.sun_checkbox, 2, 2, 1, 1)
        self.timeEdit = QtWidgets.QTimeEdit(self.gridLayoutWidget_2)
        self.timeEdit.setObjectName("timeEdit")
        pub_time = time().replace(hour=self._preferences.publish_hour, minute=0, second=0, microsecond=0)
        self.timeEdit.setTime(pub_time)
        self.gridLayout_2.addWidget(self.timeEdit, 5, 1, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.label_6.setObjectName("label_6")
        self.gridLayout_2.addWidget(self.label_6, 5, 0, 1, 1)

        self.label_5 = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 0, 0, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.label_7.setEnabled(False)
        self.label_7.setText("")
        self.label_7.setObjectName("label_7")
        self.gridLayout_2.addWidget(self.label_7, 3, 1, 1, 1)
        self.tabWidget.addTab(self.schedule_tab, "")
        self.ftp_tab = QtWidgets.QWidget()
        self.ftp_tab.setObjectName("ftp_tab")
        self.formLayoutWidget = QtWidgets.QWidget(self.ftp_tab)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 10, 351, 171))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.host_input = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.host_input.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.host_input.setText(self._preferences.ftp_config.host)
        self.host_input.setObjectName("host_input")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.host_input)
        self.label_2 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.user_input = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.user_input.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.user_input.setText(self._preferences.ftp_config.username)
        self.user_input.setObjectName("user_input")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.user_input)
        self.label_3 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.password_input = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.password_input.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.password_input.setText(self._preferences.ftp_config.password)
        self.password_input.setObjectName("password_input")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.password_input)
        self.label_4 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.port_spinner = QtWidgets.QSpinBox(self.formLayoutWidget)
        self.port_spinner.setObjectName("port_spinner")
        self.port_spinner.setValue(self._preferences.ftp_config.port)
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.port_spinner)
        self.label = QtWidgets.QLabel(self.formLayoutWidget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label)
        self.label_8 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_8.setObjectName("label_8")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.label_8)
        self.remote_path_input = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.remote_path_input.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.remote_path_input.setText(self._preferences.ftp_config.remote_path)
        self.remote_path_input.setObjectName("remote_path_input")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.remote_path_input)
        self.tabWidget.addTab(self.ftp_tab, "")
        self.verticalLayout.addWidget(self.tabWidget)
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.verticalLayout.addLayout(self.gridLayout_3)

        self.retranslateUi()
        self.tabWidget.setCurrentIndex(0)
        self.buttonBox.accepted.connect(self.accept)  # type: ignore
        self.buttonBox.rejected.connect(self.reject)  # type: ignore
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("PrefsDialog", "Settings"))
        self.mon_checkbox.setText(_translate("PrefsDialog", "Mon"))
        self.tue_checkbox.setText(_translate("PrefsDialog", "Tue"))
        self.wed_checkbox.setText(_translate("PrefsDialog", "Wed"))
        self.thu_checkbox.setText(_translate("PrefsDialog", "Thu"))
        self.fri_checkbox.setText(_translate("PrefsDialog", "Fri"))
        self.sat_checkbox.setText(_translate("PrefsDialog", "Sat"))
        self.sun_checkbox.setText(_translate("PrefsDialog", "Sun"))
        self.label_6.setText(_translate("PrefsDialog", "Premier Time"))
        self.label_5.setText(_translate("PrefsDialog", "Premier Days"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.schedule_tab), _translate("PrefsDialog", "Schedule"))
        self.label_2.setText(_translate("PrefsDialog", "User"))
        self.label_3.setText(_translate("PrefsDialog", "Password"))
        self.label_4.setText(_translate("PrefsDialog", "Port"))
        self.label.setText(_translate("PrefsDialog", "Host"))
        self.label_8.setText(_translate("PrefsDialog", "Remote Path"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.ftp_tab), _translate("PrefsDialog", "FTP"))

    def connectControls(self):
        self.mon_checkbox.stateChanged.connect(self._toggle_day(0))
        self.tue_checkbox.stateChanged.connect(self._toggle_day(1))
        self.wed_checkbox.stateChanged.connect(self._toggle_day(2))
        self.thu_checkbox.stateChanged.connect(self._toggle_day(3))
        self.fri_checkbox.stateChanged.connect(self._toggle_day(4))
        self.sat_checkbox.stateChanged.connect(self._toggle_day(5))
        self.sun_checkbox.stateChanged.connect(self._toggle_day(6))
        self.timeEdit.timeChanged.connect(self._set_property("publish_hour"))
        self.remote_path_input.textChanged.connect(self._set_ftp_property("remote_path"))
        self.host_input.textChanged.connect(self._set_ftp_property("host"))
        self.user_input.textChanged.connect(self._set_ftp_property("username"))
        self.password_input.textChanged.connect(self._set_ftp_property("password"))
        self.port_spinner.valueChanged.connect(self._set_ftp_property("port"))


    def get_config(self):
        return self._preferences

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = PrefsDialog()
    Dialog.show()
    sys.exit(app.exec_())
