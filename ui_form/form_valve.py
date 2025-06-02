from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QDialogButtonBox, QLineEdit, QMessageBox, QComboBox, QGroupBox, QApplication
from qgis.core import QgsApplication
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
    global sizeId
    global size_id
    global size_text

    global statusId
    global status_id
    global status_text

    global typeId
    global type_id
    global type_text

    global functionId
    global function_id
    global function_text

    global myDialog
    global token_new
    global plugin_dir
    global reference

    global picturePath
    global drawingPath
    global picturePath_text
    global drawingPath_text

    global groupBox

    global _temp_id
    global valveId

    global depth
    global remark

    global feaId

    myDialog = dialog
    # plugin_dir = os.getcwd()
    plugin_dir = current_path()
    myLayer = layerid
    myLayer.startEditing()

    groupBox = myDialog.findChild(QGroupBox, "groupBox")
    groupBox.setVisible(0)

    valveId = myDialog.findChild(QLineEdit, "valveId")
    valveId.setEnabled(1)
    valveId.setVisible(False)
    label_valveId = myDialog.findChild(QLabel, "label_valveId")
    label_valveId.setVisible(False)

    temp_random = random.randint(100000, 9000000)

    myDialog.setGeometry(0, 0, 680, 205)

    # Get config from config.ini
    config = configparser.ConfigParser()
    configpath = os.path.join(plugin_dir, 'config.ini')
    config.read(configpath)
    currentbranch = config.get('settings', 'currentbranch')


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

    """ id """
    feaId = myDialog.findChild(QLineEdit, "id")

    """ Remark """
    remark = myDialog.findChild(QLineEdit, "remark")
    # if remark.text() == 'NULL' or remark.text() == '':
    #     remark.setText("")

    """ checkPoint_onLine """
    valve_geom = featureid.geometry()
    pipe_sizeId, pipe_depth = checkPoint_onLine(valve_geom, currentbranch)
    """ valve size"""
    sizeId = myDialog.findChild(QLineEdit, "sizeId")
    size_id = myDialog.findChild(QComboBox, "size_id")
    size_text = myDialog.findChild(QComboBox, "size_text")
    if sizeId.text() == "" or sizeId.text() == "NULL" or len(sizeId.text()) == 0:
        sizeId.setText(str(pipe_sizeId))

    """ Check validator """
    validator = QRegExpValidator(QRegExp(r'[0-9].+'))

    """ valve depth """
    depth = myDialog.findChild(QLineEdit, "depth")
    depth.setText(str(pipe_depth))
    depth.setValidator(validator)

    """ valve Status """
    statusId = myDialog.findChild(QLineEdit, "statusId")
    status_id = myDialog.findChild(QComboBox, "status_id")
    status_text = myDialog.findChild(QComboBox, "status_text")

    """ valve Function """
    functionId = myDialog.findChild(QLineEdit, "functionId")
    function_id = myDialog.findChild(QComboBox, "function_id")
    function_text = myDialog.findChild(QComboBox, "function_text")

    """ valve type """
    typeId = myDialog.findChild(QLineEdit, "typeId")
    type_id = myDialog.findChild(QComboBox, "type_id")
    type_text = myDialog.findChild(QComboBox, "type_text")

    """ File Select """
    picturePath = myDialog.findChild(QLineEdit, "picturePath")
    drawingPath = myDialog.findChild(QLineEdit, "drawingPath")
    picturePath_text = myDialog.findChild(QgsFileWidget, "picturePath_text")
    drawingPath_text = myDialog.findChild(QgsFileWidget, "drawingPath_text")

    """ Temp """
    _temp_id = myDialog.findChild(QLineEdit, "_temp_id")
    if _temp_id.text() == 'NULL' or _temp_id.text() == '':
        _temp_id.setText(str(temp_random))

    """ GlobalId """
    globalId = myDialog.findChild(QLineEdit, "globalId")
    tempGlobalId = str(ULID())
    if globalId.text() == 'NULL' or globalId.text() == '':
        globalId.setText(str(tempGlobalId))

    load_ValveSize()
    load_ValveStatus()
    load_ValveFunction()
    load_ValveType()
    load_ptc_path()
    load_drawingPath()

    size_text.currentTextChanged.connect(valveSize_change)
    status_text.currentTextChanged.connect(valveStatus_change)
    function_text.currentTextChanged.connect(valveFunction_change)
    type_text.currentTextChanged.connect(valveType_change)
    picturePath_text.fileChanged.connect(picturePath_change)
    drawingPath_text.fileChanged.connect(drawingPath_change)


def load_ptc_path():
    picturePath_text.setFilePath(picturePath.text())


def load_drawingPath():
    drawingPath_text.setFilePath(drawingPath.text())


def load_ValveSize():
    sizeList = []
    valveSizes = reference["referances"]["valve"]["valveSizes"]
    for i in range(len(valveSizes)):
        size_id.addItem(str(valveSizes[i]["sizeId"]))
        sizeList.append(str(valveSizes[i]["sizeId"]))
        size_text.addItem(str(valveSizes[i]["description"]))

    """ Add Other for not in DataDic """
    size_text.addItem("โปรดเลือกขนาดประตูน้ำ")
    size_id.addItem("Other")

    if sizeId.text() not in sizeList:
        size_text.setCurrentIndex(len(sizeList))
        size_id.setCurrentIndex(len(sizeList))
    else:
        size_id.setCurrentText(sizeId.text())
        size_text.setCurrentIndex(size_id.currentIndex())


def load_ValveStatus():
    statusList = []
    valveStatus = reference["referances"]["valve"]["valveStatus"]
    for i in range(len(valveStatus)):
        status_id.addItem(str(valveStatus[i]["statusId"]))
        statusList.append(str(valveStatus[i]["statusId"]))
        status_text.addItem(str(valveStatus[i]["description"]))

    """ Add Other for not in DataDic """
    status_text.addItem("โปรดเลือกสภาพประตูน้ำ")
    status_id.addItem("Other")

    if statusId.text() not in statusList:
        status_text.setCurrentIndex(len(statusList))
        status_id.setCurrentIndex(len(statusList))
    else:
        status_id.setCurrentText(statusId.text())
        status_text.setCurrentIndex(status_id.currentIndex())


def load_ValveFunction():
    functionList = []
    valveFunctions = reference["referances"]["valve"]["valveFunctions"]
    for i in range(len(valveFunctions)):
        function_id.addItem(str(valveFunctions[i]["functionId"]))
        functionList.append(str(valveFunctions[i]["functionId"]))
        function_text.addItem(str(valveFunctions[i]["description"]))

    """ Add Other for not in DataDic """
    function_text.addItem("โปรดเลือกหน้าที่ของประตูน้ำ")
    function_id.addItem("Other")

    if functionId.text() not in functionList:
        # Not Handle NULL
        #if feaId.text() == 'NULL':
            #function_text.setCurrentIndex(3)
            #function_id.setCurrentIndex(3)
            #functionId.setText(function_id.currentText())
        #else:
            function_text.setCurrentIndex(len(functionList))
            function_id.setCurrentIndex(len(functionList))
    else:
        function_id.setCurrentText(functionId.text())
        function_text.setCurrentIndex(function_id.currentIndex())


def load_ValveType():
    typeList = []
    valveTypes = reference["referances"]["valve"]["valveTypes"]
    for i in range(len(valveTypes)):
        type_id.addItem(str(valveTypes[i]["typeId"]))
        typeList.append(str(valveTypes[i]["typeId"]))
        type_text.addItem(str(valveTypes[i]["description"]))

    """ Add Other for not in DataDic """
    type_text.addItem("โปรดเลือกชนิดของประตูน้ำ")
    type_id.addItem("Other")

    if typeId.text() not in typeList:
        type_text.setCurrentIndex(len(typeList))
        type_id.setCurrentIndex(len(typeList))
    else:
        type_id.setCurrentText(typeId.text())
        type_text.setCurrentIndex(type_id.currentIndex())


def valveSize_change():
    size_id.setCurrentIndex(size_text.currentIndex())
    if size_id.currentText() != "Other":
        sizeId.setText(size_id.currentText())
    else:
        sizeId.setText(None)


def valveStatus_change():
    status_id.setCurrentIndex(status_text.currentIndex())
    if status_id.currentText() != "Other":
        statusId.setText(status_id.currentText())
    else:
        statusId.setText(None)


def valveFunction_change():
    function_id.setCurrentIndex(function_text.currentIndex())
    if function_id.currentText() != "Other":
        functionId.setText(function_id.currentText())
    else:
        functionId.setText(None)


def valveType_change():
    typeIndex = type_text.currentIndex()
    type_id.setCurrentIndex(typeIndex)
    if type_id.currentText() != "Other":
        typeId.setText(type_id.currentText())
        if type_id.currentText() == "6":
            depth.setText("0")
    else:
        typeId.setText(None)


def picturePath_change():
    picturePath.setText(picturePath_text.filePath())


def drawingPath_change():
    drawingPath.setText(drawingPath_text.filePath())


def checkPoint_onLine(myPoint, currentbranch):
    # Find PIPE Layer and set active
    layer_name = str(currentbranch) + "_PIPE"
    line_layer = QgsProject.instance().mapLayersByName(layer_name)[0]
    valve_geom = myPoint
    pipe_sizeId = "0"
    pipe_depth = "0"
    for line_feature in line_layer.getFeatures():
        line_geom = line_feature.geometry()
        if line_geom.distance(valve_geom) < 1e-6:  # Adjust tolerance as needed
            pipe_sizeId = line_feature['sizeId']
            pipe_depth = line_feature['depth']
            print(f"Valve {valve_geom} is on pipe")
            break  # Stop checking other lines for this point
    return pipe_sizeId, pipe_depth
