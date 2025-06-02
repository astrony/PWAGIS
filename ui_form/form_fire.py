from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QDialogButtonBox, QLineEdit, QMessageBox, QComboBox, QGroupBox, QTabWidget, QDateEdit, QTimeEdit, QDateTimeEdit, QApplication
from qgis.gui import QgsFileWidget
from pwagis.utiles import *
import os
import os.path
import json
import configparser
import requests
from datetime import datetime
from pwagis.get_plugin_path import current_path
import random
from ulid import ULID


def close_before(dialog, layerid, featureid):
    top_level_windows = QApplication.topLevelWidgets()
    for window in top_level_windows:
        # Check if the window is an instance of QgsAttributeDialog
        if window.metaObject().className() == 'QgsAttributeDialog':
            # Close the window
            window.close()
    formOpen(dialog, layerid, featureid)


nameField = None
myDialog = None


def formOpen(dialog, layerid, featureid):
    global myDialog
    global plugin_dir
    global reference
    global token_new

    global sizeId
    global size_id
    global size_text

    global statusId
    global status_id
    global status_text

    global recordDate
    global recodeCalendar

    global picturePath
    global pressureHistory
    global picturePath_text
    global pressureHistory_text

    global firehydrantId

    global _temp_id
    global remark
    global pressure

    myDialog = dialog

    plugin_dir = os.getcwd()
    myLayer = layerid
    myLayer.startEditing()

    plugin_dir = current_path()

    groupBox_2 = myDialog.findChild(QGroupBox, "groupBox_2")
    groupBox_2.setVisible(0)

    temp_random = random.randint(100000, 9000000)

    # Get config from config.ini
    config = configparser.ConfigParser()
    configpath = os.path.join(plugin_dir, 'config.ini')
    config.read(configpath)
    token_new = config.get('settings', 'token_new')

    """ Load JSON REFERENCE """
    json_file = "referances.json"
    json_path = os.path.join(plugin_dir, "json", json_file)
    with open(json_path, 'r', encoding='utf-8') as openfile:
        reference = json.load(openfile)

    """ Fire id """
    firehydrantId = myDialog.findChild(QLineEdit, "firehydrantId")
    firehydrantId.setCursorPosition(1)
    firehydrantId.setEnabled(1)
    firehydrantId.setVisible(False)
    label_firehydrantId = myDialog.findChild(QLabel, "label_firehydrantId")
    label_firehydrantId.setVisible(False)

    pressure = myDialog.findChild(QLineEdit, "pressure")
    # if str(pressure.text()) == 'NULL' or str(pressure.text()) == '':
    #    pressure.setText("0")

    remark = myDialog.findChild(QLineEdit, "remark")
    # if str(remark.text()) == 'NULL':
    #     remark.setText("")

    """ Fire size"""
    sizeId = myDialog.findChild(QLineEdit, "sizeId")
    size_id = myDialog.findChild(QComboBox, "size_id")
    size_text = myDialog.findChild(QComboBox, "size_text")

    """ Fire Status """
    statusId = myDialog.findChild(QLineEdit, "statusId")
    status_id = myDialog.findChild(QComboBox, "status_id")
    status_text = myDialog.findChild(QComboBox, "status_text")

    """ Record Date"""
    recordDate = myDialog.findChild(QLineEdit, "recordDate")
    recodeCalendar = myDialog.findChild(QDateTimeEdit, "recodeCalendar")

    """ File Select """
    picturePath = myDialog.findChild(QLineEdit, "picturePath")
    pressureHistory = myDialog.findChild(QLineEdit, "pressureHistory")
    picturePath_text = myDialog.findChild(QgsFileWidget, "picturePath_text")
    pressureHistory_text = myDialog.findChild(QgsFileWidget, "pressureHistory_text")

    """ Temp """
    _temp_id = myDialog.findChild(QLineEdit, "_temp_id")
    if _temp_id.text() == 'NULL' or _temp_id.text() == '':
        _temp_id.setText(str(temp_random))

    """ GlobalId """
    globalId = myDialog.findChild(QLineEdit, "globalId")
    tempGlobalId = str(ULID())
    print("tempGlobalId : " + str(tempGlobalId))
    # value = QgsExpressionContextUtils.projectScope(QgsProject.instance()).variable('globalId')
    if globalId.text() == 'NULL' or globalId.text() == '':
        globalId.setText(str(tempGlobalId))

    load_FireSize()
    load_FireStatus()
    load_ptc_path()
    load_pressure_his()
    set_record_date()

    # sizeId.setText(size_id.currentText())
    size_text.currentTextChanged.connect(fireSize_change)
    status_text.currentTextChanged.connect(fireStatus_change)
    recodeCalendar.dateTimeChanged.connect(get_record_date)
    picturePath_text.fileChanged.connect(picturePath_change)
    pressureHistory_text.fileChanged.connect(pressureHistory_change)


def load_ptc_path():
    picturePath_text.setFilePath(picturePath.text())


def load_pressure_his():
    pressureHistory_text.setFilePath(pressureHistory.text())


def get_record_date():
    strDate = recodeCalendar.dateTime()
    f_date = strDate.toString("yyyy-MM-ddTHH:mm:ssZ")
    recordDate.setText(f_date)


def set_record_date():
    raw_date = str(recordDate.text())
    raw_date = raw_date.replace("+00:00", "Z")
    recordDate.setText(raw_date)

    if raw_date == "NULL" or raw_date == "":
        current_dateTime = datetime.now()
        dt_with_timezone = datetime.fromisoformat(str(current_dateTime)).replace(microsecond=0)
        a = str(dt_with_timezone)
        x = a.split()
        o = x[0] + "T" + x[1] + "Z"
        recordDate.setText(o)
        datetime_string = datetime.strptime(o, "%Y-%m-%dT%H:%M:%SZ")
        dt_with_timezone = datetime.fromisoformat(str(datetime_string))
        # Convert to desired format
        t_yr = dt_with_timezone.strftime("%Y")
        t_mo = dt_with_timezone.strftime("%m")
        t_da = dt_with_timezone.strftime("%d")
        t_hr = dt_with_timezone.strftime("%H")
        t_mi = dt_with_timezone.strftime("%M")

        now = QDateTime(int(t_yr), int(t_mo), int(t_da), int(t_hr), int(t_mi))
        recodeCalendar.setDateTime(now)
    else:
        raw_date = raw_date.replace(".000", "")
        recordDate.setText(raw_date)
        try:
            datetime_string = datetime.strptime(raw_date, "%Y-%m-%dT%H:%M:%SZ")  # .%fZ
        except:
            datetime_string = datetime.strptime(raw_date, "%Y-%m-%dT%H:%M:%S.%fZ")  # .%fZ
        dt_with_timezone = datetime.fromisoformat(str(datetime_string))
        # Convert to desired format
        t_yr = dt_with_timezone.strftime("%Y")
        t_mo = dt_with_timezone.strftime("%m")
        t_da = dt_with_timezone.strftime("%d")
        t_hr = dt_with_timezone.strftime("%H")
        t_mi = dt_with_timezone.strftime("%M")

        now = QDateTime(int(t_yr), int(t_mo), int(t_da), int(t_hr), int(t_mi))
        recodeCalendar.setDateTime(now)


def load_FireSize():
    sizeList = []
    firehydrantSizes = reference["referances"]["firehydrant"]["firehydrantSizes"]
    for i in range(len(firehydrantSizes)):
        size_id.addItem(str(firehydrantSizes[i]["sizeId"]))
        sizeList.append(str(firehydrantSizes[i]["sizeId"]))
        size_text.addItem(str(firehydrantSizes[i]["description"]))

    """ Add Other for not in DataDic """
    size_text.addItem("โปรดเลือกขนาดหัวดับเพลิง")
    size_id.addItem("Other")

    if sizeId.text() not in sizeList:
        size_text.setCurrentIndex(len(sizeList))
        size_id.setCurrentIndex(len(sizeList))
    else:
        size_id.setCurrentText(sizeId.text())
        size_text.setCurrentIndex(size_id.currentIndex())


def load_FireStatus():
    statusList = []
    firehydrantStatus = reference["referances"]["firehydrant"]["firehydrantStatus"]
    for i in range(len(firehydrantStatus)):
        status_id.addItem(str(firehydrantStatus[i]["statusId"]))
        statusList.append(str(firehydrantStatus[i]["statusId"]))
        status_text.addItem(str(firehydrantStatus[i]["description"]))

    """ Add Other for not in DataDic """
    status_text.addItem("โปรดเลือกสถานะหัวดับเพลิง ")
    status_id.addItem("Other")

    if statusId.text() not in statusList:
        status_text.setCurrentIndex(len(statusList))
        status_id.setCurrentIndex(len(statusList))
    else:
        status_id.setCurrentText(statusId.text())
        status_text.setCurrentIndex(status_id.currentIndex())


def fireSize_change():
    size_id.setCurrentIndex(size_text.currentIndex())
    if size_id.currentText() != "Other":
        sizeId.setText(size_id.currentText())
    else:
        sizeId.setText(None)


def fireStatus_change():
    status_id.setCurrentIndex(status_text.currentIndex())
    if status_id.currentText() != "Other":
        statusId.setText(status_id.currentText())
    else:
        statusId.setText(None)


def picturePath_change():
    picturePath.setText(picturePath_text.filePath())


def pressureHistory_change():
    pressureHistory.setText(pressureHistory_text.filePath())

