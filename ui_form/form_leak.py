from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtWidgets import QWidget, QVBoxLayout, QPushButton, QDialogButtonBox, QLineEdit, QMessageBox, QComboBox, QGroupBox, QTabWidget, QDateEdit, QTimeEdit, QDateTimeEdit, QApplication
from pwagis.utiles import *
import os
import os.path
import json
import configparser
import requests
from datetime import datetime
import pytz
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
    global pipeId

    global pipeSizeId

    global finish_date
    global rawFinish_date

    global datetime_show

    global repairDate
    global repair_date

    global pipeTypeId
    global pipeType_id
    global pipeType_text

    global informer
    global informer_id
    global informer_text

    global incidentTypeId
    global incidentType_id
    global incidentType_text

    global incidentCategoryId
    global incidentCategory_id
    global incidentCategory_text

    global incidentCat_SubId
    global incidentCat_Sub_id
    global incidentCat_Sub_text

    global repairCategoryId
    global repairCategory_id
    global repairCategory_text

    global repairTypeId
    global repairType_id
    global repairType_text

    global repairCat_SubId
    global repairCat_Sub_id
    global repairCat_Sub_text

    global myDialog
    global token
    global plugin_dir
    global reference
    global tabWidget

    global _temp_id

    myDialog = dialog
    myDialog.setMaximumSize(580, 400)

    # plugin_dir = os.getcwd()
    plugin_dir = current_path()
    myLayer = layerid
    myLayer.startEditing()

    temp_random = random.randint(100000, 9000000)

    """ 
    # Get config from config.ini
    config = configparser.ConfigParser()
    configpath = os.path.join(plugin_dir, 'config.ini')
    config.read(configpath)
    token = config.get('settings', 'token')
    """

    """ Load JSON REFERENCE """
    """
    json_file = "referances.json"
    json_path = os.path.join(plugin_dir, "json", json_file)
    with open(json_path, 'r', encoding='utf-8') as openfile:
        reference = json.load(openfile)
    """

    """ Pipe Id """
    # pipeId = myDialog.findChild(QLineEdit, "pipeId")

    """ Pipe Type """
    # pipeTypeId = myDialog.findChild(QLineEdit, "pipeTypeId")
    # pipeType_id = myDialog.findChild(QComboBox, "pipeType_id")
    # pipeType_text = myDialog.findChild(QComboBox, "pipeType_text")

    """ Pipe Size """
    # pipeSizeId = myDialog.findChild(QLineEdit, "pipeSizeId")

    """ Date Time """
    datetime_show = myDialog.findChild(QDateTimeEdit, "datetime_show")

    rawFinish_date = myDialog.findChild(QLineEdit, "leakDatetime")
    # finish_date.setReadOnly(False)

    repairDate = myDialog.findChild(QLineEdit, "repairDate")
    repair_date = myDialog.findChild(QDateEdit, "repair_date")
    # repair_date.setReadOnly(False)

    """ Informer """
    informer = myDialog.findChild(QLineEdit, "informer")
    informer_id = myDialog.findChild(QComboBox, "informer_id")
    informer_text = myDialog.findChild(QComboBox, "informer_text")

    """ Incident Type"""
    incidentTypeId = myDialog.findChild(QLineEdit, "incidentType")
    incidentType_id = myDialog.findChild(QComboBox, "incidentType_id")
    incidentType_text = myDialog.findChild(QComboBox, "incidentType_text")

    """ Incident Category """
    incidentCategoryId = myDialog.findChild(QLineEdit, "incidentCategory")
    incidentCategory_id = myDialog.findChild(QComboBox, "incidentCategory_id")
    incidentCategory_text = myDialog.findChild(QComboBox, "incidentCategory_Text")

    """ Incident Category Subject """
    incidentCat_SubId = myDialog.findChild(QLineEdit, "incidentCategorySubject")
    incidentCat_Sub_id = myDialog.findChild(QComboBox, "incidentCategorySubject_id")
    incidentCat_Sub_text = myDialog.findChild(QComboBox, "incidentCategorySubject_text")

    """ Repair Category """
    repairCategoryId = myDialog.findChild(QLineEdit, "repaireCategory")
    repairCategory_id = myDialog.findChild(QComboBox, "repairCategory_id")
    repairCategory_text = myDialog.findChild(QComboBox, "repairCategory_text")

    """ Repair Type """
    repairTypeId = myDialog.findChild(QLineEdit, "repairType")
    repairType_id = myDialog.findChild(QComboBox, "repairType_id")
    repairType_text = myDialog.findChild(QComboBox, "repairType_text")

    """ Repair Category Subject """
    repairCat_SubId = myDialog.findChild(QLineEdit, "repairCategorySubject")
    repairCat_Sub_id = myDialog.findChild(QComboBox, "repairCategorySubject_id")
    repairCat_Sub_text = myDialog.findChild(QComboBox, "repairCategorySubject_text")

    """ Tab """
    tabWidget = myDialog.findChild(QTabWidget, "tabWidget")
    tabWidget.setCurrentIndex(0)

    tabWidget = myDialog.findChild(QTabWidget, "tabWidget")
    # tabWidget.setTabVisible(2, False)

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

    """ Load Data """
    # get_pipe_feature()
    # load_pipeType()
    set_finish_date()
    load_informer()
    load_incidentType()
    load_incidentCategory()
    load_incidentCategorySubject()
    load_repairType()
    load_repairCat_Sub()
    load_repairCategory()

    """ Status Change """
    # pipeType_text.currentTextChanged.connect(pipeType_change)
    informer_text.currentTextChanged.connect(informer_change)
    incidentType_text.currentTextChanged.connect(incidentType_change)
    incidentCategory_text.currentTextChanged.connect(incidentCategory_change)
    incidentCat_Sub_text.currentTextChanged.connect(incidentCategorySubject_change)
    repairType_text.currentTextChanged.connect(repairType_change)
    repairCat_Sub_text.currentTextChanged.connect(repairCategorySubject_change)
    repairCategory_text.currentTextChanged.connect(repairCategory_change)
    datetime_show.dateTimeChanged.connect(get_finish_date)


def get_finish_date():
    # strDate = finish_date.toString().toStdString()
    strDate = datetime_show.dateTime()
    f_date = strDate.toString("yyyy-MM-ddTHH:mm:ssZ")
    rawFinish_date.setText(f_date)

    #rawFinish_date.setText(str(strDate.toPyDate()) + "T00:00:00Z")


def set_finish_date():
    raw_date = str(rawFinish_date.text())
    raw_date = raw_date.replace("+00:00", "Z")
    rawFinish_date.setText(raw_date)
    if raw_date == "NULL" or raw_date == "":
        current_dateTime = datetime.now()
        dt_with_timezone = datetime.fromisoformat(str(current_dateTime)).replace(microsecond=0)
        a = str(dt_with_timezone)
        x = a.split()
        o = x[0] + "T" + x[1] + "Z"
        rawFinish_date.setText(o)
        # repairDate.setText(o)
        datetime_string = datetime.strptime(o, "%Y-%m-%dT%H:%M:%SZ")
        dt_with_timezone = datetime.fromisoformat(str(datetime_string))
        # Convert to desired format
        t_yr = dt_with_timezone.strftime("%Y")
        t_mo = dt_with_timezone.strftime("%m")
        t_da = dt_with_timezone.strftime("%d")
        t_hr = dt_with_timezone.strftime("%H")
        t_mi = dt_with_timezone.strftime("%M")

        # repair_date.setDate(QDate(int(t_year), int(t_m), int(t_d)))

    else:
        raw_date = raw_date.replace(".000", "")
        rawFinish_date.setText(raw_date)
        # repairDate.setText(raw_date)
        datetime_string = datetime.strptime(raw_date, "%Y-%m-%dT%H:%M:%SZ")
        dt_with_timezone = datetime.fromisoformat(str(datetime_string))
        # Convert to desired format
        t_yr = dt_with_timezone.strftime("%Y")
        t_mo = dt_with_timezone.strftime("%m")
        t_da = dt_with_timezone.strftime("%d")
        t_hr = dt_with_timezone.strftime("%H")
        t_mi = dt_with_timezone.strftime("%M")

        now = QDateTime(int(t_yr), int(t_mo), int(t_da), int(t_hr), int(t_mi))
        datetime_show.setDateTime(now)
        # repair_date.setDate(QDate(int(t_year), int(t_m), int(t_d)))


def load_informer():
    i = 1
    while i < 15:
        informer_text.addItem(str(i))
        informer_id.addItem(str(i))
        i = i + 1

    informer_id.setCurrentText(informer.text())
    informer_text.setCurrentIndex(informer_id.currentIndex())
    if informer.text() == "":
        informer.setText("1")


def load_incidentType():
    i = 0
    while i < 15:
        incidentType_text.addItem(str(i))
        incidentType_id.addItem(str(i))
        i = i + 1

    incidentType_id.setCurrentText(incidentTypeId.text())
    incidentType_text.setCurrentIndex(incidentType_id.currentIndex())
    if incidentTypeId.text() == "":
        incidentTypeId.setText("0")


def load_incidentCategory():
    i = 0
    while i < 15:
        incidentCategory_text.addItem(str(i))
        incidentCategory_id.addItem(str(i))
        i = i + 1

    incidentCategory_id.setCurrentText(incidentCategoryId.text())
    incidentCategory_text.setCurrentIndex(incidentCategory_id.currentIndex())
    if incidentCategoryId.text() == "":
        incidentCategoryId.setText("0")


def load_incidentCategorySubject():
    i = 0
    while i < 15:
        incidentCat_Sub_text.addItem(str(i))
        incidentCat_Sub_id.addItem(str(i))
        i = i + 1

    incidentCat_Sub_id.setCurrentText(incidentCat_SubId.text())
    incidentCat_Sub_text.setCurrentIndex(incidentCat_Sub_id.currentIndex())
    if incidentCat_SubId.text() == "":
        incidentCat_SubId.setText("0")


def load_repairCategory():
    i = 0
    while i < 15:
        repairCategory_text.addItem(str(i))
        repairCategory_id.addItem(str(i))
        i = i + 1

    repairCategory_id.setCurrentText(repairCategoryId.text())
    repairCategory_text.setCurrentIndex(repairCategory_id.currentIndex())
    if repairCategoryId.text() == "":
        repairCategoryId.setText("0")


def load_repairType():
    i = 0
    while i < 15:
        repairType_text.addItem(str(i))
        repairType_id.addItem(str(i))
        i = i + 1

    repairType_id.setCurrentText(repairTypeId.text())
    repairType_text.setCurrentIndex(repairType_id.currentIndex())
    if repairTypeId.text() == "":
        repairTypeId.setText("0")


def load_repairCat_Sub():
    i = 0
    while i < 15:
        repairCat_Sub_text.addItem(str(i))
        repairCat_Sub_id.addItem(str(i))
        i = i + 1

    repairCat_Sub_id.setCurrentText(incidentCat_SubId.text())
    repairCat_Sub_text.setCurrentIndex(repairCat_Sub_id.currentIndex())
    if repairCat_SubId.text() == "":
        repairCat_SubId.setText("0")


def informer_change():
    informer_id.setCurrentIndex(informer_text.currentIndex())
    informer.setText("")
    informer.setText(informer_id.currentText())


def incidentType_change():
    incidentType_id.setCurrentIndex(incidentType_text.currentIndex())
    incidentTypeId.setText("")
    incidentTypeId.setText(incidentType_id.currentText())


def incidentCategory_change():
    incidentCategory_id.setCurrentIndex(incidentCategory_text.currentIndex())
    incidentCategoryId.setText("")
    incidentCategoryId.setText(incidentCategory_id.currentText())


def incidentCategorySubject_change():
    incidentCat_Sub_id.setCurrentIndex(incidentCat_Sub_text.currentIndex())
    incidentCat_SubId.setText("")
    incidentCat_SubId.setText(incidentCat_Sub_id.currentText())


def repairCategory_change():
    repairCategory_id.setCurrentIndex(repairCategory_text.currentIndex())
    repairCategoryId.setText("")
    repairCategoryId.setText(repairCategory_id.currentText())


def repairType_change():
    repairType_id.setCurrentIndex(repairType_text.currentIndex())
    repairTypeId.setText("")
    repairTypeId.setText(repairType_id.currentText())


def repairCategorySubject_change():
    repairCat_Sub_id.setCurrentIndex(repairCat_Sub_text.currentIndex())
    repairCat_SubId.setText("")
    repairCat_SubId.setText(repairCat_Sub_id.currentText())


"""
def load_pipeType():
    pipe_type = reference["referances"]["pipe"]["pipeTypes"]
    for i in range(len(pipe_type)):
        pipeType_id.addItem(str(pipe_type[i]["typeId"]))
        pipeType_text.addItem(str(pipe_type[i]["description"]))

    pipeType_id.setCurrentText(pipeTypeId.text())
    pipeType_text.setCurrentIndex(pipeType_id.currentIndex())
    if pipeTypeId.text() == "":
        pipeTypeId.setText("PVC")


def pipeType_change():
    pipType_id.setCurrentIndex(pipeType_text.currentIndex())
    pipeTypeId.setText("")
    pipeTypeId.setText(pipeType_id.currentText())
"""


