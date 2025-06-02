from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtWidgets import QWidget, QVBoxLayout, QPushButton, QDialogButtonBox, QLineEdit, QMessageBox, QComboBox, QGroupBox, QApplication
from pwagis.utiles import *
import os
import os.path
import json
import configparser
import requests
from pwagis.get_plugin_path import current_path


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
    global roadtype
    global roadtype_id
    global roadtype_text

    global roadfunc
    global roadfunc_id
    global roadfunc_text

    global myDialog
    global plugin_dir
    global reference

    global old_function
    global old_type

    # global groupBox

    myDialog = dialog
    # plugin_dir = os.getcwd()
    plugin_dir = current_path()
    myLayer = layerid
    myLayer.startEditing()

    groupBox = myDialog.findChild(QGroupBox, "groupBox")
    groupBox.setVisible(False)

    """ Load JSON REFERENCE """
    json_file = "referances.json"
    json_path = os.path.join(plugin_dir, "json", json_file)
    with open(json_path, 'r', encoding='utf-8') as openfile:
        reference = json.load(openfile)

    """ Road Type """
    roadtype = myDialog.findChild(QLineEdit, "type")
    roadtype_id = myDialog.findChild(QComboBox, "type_id")
    roadtype_text = myDialog.findChild(QComboBox, "type_text")

    """ Road Function """
    roadfunc = myDialog.findChild(QLineEdit, "func")
    roadfunc_id = myDialog.findChild(QComboBox, "func_id")
    roadfunc_text = myDialog.findChild(QComboBox, "func_text")

    load_RoadType()
    load_RoadFunction()

    roadtype_text.currentTextChanged.connect(roadType_change)
    roadfunc_text.currentTextChanged.connect(roadFunction_change)

    old_function = roadfunc.text()
    old_type = roadtype.text()


def load_RoadType():
    roadTypes = reference["referances"]["road"]["roadTypes"]
    for i in range(len(roadTypes)):
        roadtype_id.addItem(str(roadTypes[i]["typeId"]))
        roadtype_text.addItem(str(roadTypes[i]["description"]))

    if roadtype.text() == "":
        roadtype_id.setCurrentText(roadtype.text())
        roadtype_text.setCurrentIndex(roadtype_id.currentIndex())
    else:
        roadtype_text.addItem(roadtype.text())
        roadtype_id.addItem("99")
        roadtype_text.setCurrentText(roadtype.text())


def load_RoadFunction():
    roadFunctions = reference["referances"]["road"]["roadFunctions"]
    for i in range(len(roadFunctions)):
        roadfunc_id.addItem(str(roadFunctions[i]["functionId"]))
        roadfunc_text.addItem(str(roadFunctions[i]["description"]))
    if roadfunc.text() == "":
        roadfunc_id.setCurrentText(roadfunc.text())
        roadfunc_text.setCurrentIndex(roadfunc_id.currentIndex())
    else:
        roadfunc_text.addItem(str(roadfunc.text()))
        roadfunc_id.addItem("99")
        roadfunc_text.setCurrentText(roadfunc.text())


def roadType_change():
    roadtype_id.setCurrentIndex(roadtype_text.currentIndex())
    if roadtype_id.currentText() == "99":
        roadtype_text.setCurrentText(old_type)
        roadtype.setText(old_type)
    else:
        roadtype.setText("")
        roadtype.setText(roadtype_id.currentText())


def roadFunction_change():
    roadfunc_id.setCurrentIndex(roadfunc_text.currentIndex())
    if roadfunc_id.currentText() == "99":
        roadfunc_text.setCurrentText(old_function)
        roadfunc.setText(old_function)
    else:
        roadfunc.setText("")
        roadfunc.setText(roadfunc_id.currentText())



