from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
# from qgis.PyQt.QtWidgets import QWidget, QVBoxLayout, QPushButton, QDialogButtonBox, QLineEdit, QMessageBox, QComboBox, QGroupBox, QApplication
from qgis.PyQt.QtWidgets import *
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
    global _temp_id
    global flowMeterId
    global installedDate
    global installedDateCar

    myDialog = dialog
    # plugin_dir = os.getcwd()
    plugin_dir = current_path()
    myLayer = layerid
    myLayer.startEditing()

    groupBox = myDialog.findChild(QGroupBox, "groupBox")
    groupBox.setVisible(0)

    temp_random = random.randint(100000, 9000000)

    """  Flow Meter ID """
    flowMeterId = myDialog.findChild(QLineEdit, "id")
    flowMeterId.setEnabled(0)

    """ Install Date"""
    installedDate = myDialog.findChild(QLineEdit, "installedDate")
    installedDateCar = myDialog.findChild(QDateTimeEdit, "installedDateCar")


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

    set_install_date()

    installedDateCar.dateTimeChanged.connect(get_install_date)


def get_install_date():
    strDate = installedDateCar.dateTime()
    f_date = strDate.toString("yyyy-MM-ddTHH:mm:ssZ")
    installedDate.setText(f_date)


def set_install_date():
    raw_date = str(installedDate.text())
    raw_date = raw_date.replace("+00:00", "Z")
    installedDate.setText(raw_date)

    if raw_date == "NULL" or raw_date == "":
        current_dateTime = datetime.now()
        dt_with_timezone = datetime.fromisoformat(str(current_dateTime)).replace(microsecond=0)
        a = str(dt_with_timezone)
        x = a.split()
        o = x[0] + "T" + x[1] + "Z"
        installedDate.setText(o)
        datetime_string = datetime.strptime(o, "%Y-%m-%dT%H:%M:%SZ")
        dt_with_timezone = datetime.fromisoformat(str(datetime_string))
        # Convert to desired format
        t_yr = dt_with_timezone.strftime("%Y")
        t_mo = dt_with_timezone.strftime("%m")
        t_da = dt_with_timezone.strftime("%d")
        t_hr = dt_with_timezone.strftime("%H")
        t_mi = dt_with_timezone.strftime("%M")

        now = QDateTime(int(t_yr), int(t_mo), int(t_da), int(t_hr), int(t_mi))
        installedDateCar.setDateTime(now)
    else:
        print(str(raw_date))
        raw_date = raw_date.replace(".000", "")
        installedDate.setText(raw_date)

        try:
            print(str(raw_date))
            datetime_string = datetime.strptime(raw_date, "%Y-%m-%dT%H:%M:%SZ") #.%fZ
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
        installedDateCar.setDateTime(now)










