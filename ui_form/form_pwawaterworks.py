from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QDialogButtonBox, QLineEdit, QMessageBox, QComboBox, QGroupBox, QApplication
from pwagis.utiles import *
import os
import os.path
import json
import configparser
import requests
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
    global costCenterId
    global costCenter_id
    global costCenter_text

    global pwaStationId
    global pwaStation_id
    global pwaStation_text

    global pwaId

    global myDialog
    global token_new
    global plugin_dir
    global reference

    global _temp_id

    global hideBox

    myDialog = dialog
    # plugin_dir = os.getcwd()
    plugin_dir = current_path()
    myLayer = layerid
    myLayer.startEditing()

    hideBox = myDialog.findChild(QGroupBox, "hideBox")
    hideBox.setVisible(0)

    temp_random = random.randint(100000, 9000000)

    pwaId = myDialog.findChild(QLineEdit, "pwaId")
    pwaId.setEnabled(1)
    pwaId.setVisible(False)
    label_pwaId = myDialog.findChild(QLabel, "label_pwaId")
    label_pwaId.setVisible(False)

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

    """ PWA Cost Center """
    costCenterId = myDialog.findChild(QLineEdit, "costCenterId")
    costCenter_id = myDialog.findChild(QComboBox, "costCenter_id")
    costCenter_text = myDialog.findChild(QComboBox, "costCenter_text")
    """ PWA Station """
    pwaStationId = myDialog.findChild(QLineEdit, "pwaStationId")
    pwaStation_id = myDialog.findChild(QComboBox, "pwaStation_id")
    pwaStation_text = myDialog.findChild(QComboBox, "pwaStation_text")

    # pwaId = myDialog.findChild(QLineEdit, "pwaId")
    """ Temp """
    _temp_id = myDialog.findChild(QLineEdit, "_temp_id")
    if _temp_id.text() == 'NULL' or _temp_id.text() == '':
        _temp_id.setText(str(temp_random))

    """ GlobalId """
    globalId = myDialog.findChild(QLineEdit, "globalId")
    tempGlobalId = str(ULID())
    # value = QgsExpressionContextUtils.projectScope(QgsProject.instance()).variable('globalId')

    if globalId.text() == 'NULL' or globalId.text() == '':
        globalId.setText(str(tempGlobalId))

    load_CostCenter()
    load_PwaStation()

    costCenter_text.currentTextChanged.connect(costCenter_change)
    pwaStation_text.currentTextChanged.connect(pwaStation_change)


def load_CostCenter():
    cosCenterList = []
    costcenters = reference["referances"]["pwawaterwork"]["costcenters"]
    for i in range(len(costcenters)):
        costCenter_id.addItem(str(costcenters[i]["costCenterId"]))
        cosCenterList.append(str(costcenters[i]["costCenterId"]))
        costCenter_text.addItem(str(costcenters[i]["depShortName"]))

    """ Add Other for not in DataDic """
    costCenter_text.addItem("โปรดเลือกศูนย์ต้นทุน")
    costCenter_id.addItem("Other")

    if costCenterId.text() not in cosCenterList:
        costCenter_text.setCurrentIndex(len(cosCenterList))
        costCenter_id.setCurrentIndex(len(cosCenterList))
    else:
        costCenter_id.setCurrentText(costCenterId.text())
        costCenter_text.setCurrentIndex(costCenter_id.currentIndex())


def load_PwaStation():
    stationList = []
    pwaStations = reference["referances"]["pwawaterwork"]["pwaStations"]
    for i in range(len(pwaStations)):
        pwaStation_id.addItem(str(pwaStations[i]["stationId"]))
        stationList.append(str(pwaStations[i]["stationId"]))
        pwaStation_text.addItem(str(pwaStations[i]["description"]))

    """ Add Other for not in DataDic """
    pwaStation_text.addItem("โปรดเลือกประเภทสถานที่")
    pwaStation_id.addItem("Other")

    if pwaStationId.text() not in stationList:
        pwaStation_text.setCurrentIndex(len(stationList))
        pwaStation_id.setCurrentIndex(len(stationList))
    else:
        pwaStation_id.setCurrentText(pwaStationId.text())
        pwaStation_text.setCurrentIndex(pwaStation_id.currentIndex())


def costCenter_change():
    costCenter_id.setCurrentIndex(costCenter_text.currentIndex())
    if costCenter_id.currentText() != "Other":
        costCenterId.setText(costCenter_id.currentText())
    else:
        costCenterId.setText(None)


def pwaStation_change():
    pwaStation_id.setCurrentIndex(pwaStation_text.currentIndex())
    if pwaStation_id.currentText() != "Other":
        pwaStationId.setText(pwaStation_id.currentText())
    else:
        pwaStationId.setText(None)
