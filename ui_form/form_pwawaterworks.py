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
    current_branch_code = config.get('settings', 'currentbranch')
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

    load_CostCenter(current_branch_code)
    load_PwaStation()

    costCenter_text.currentTextChanged.connect(costCenter_change)
    pwaStation_text.currentTextChanged.connect(pwaStation_change)


def load_CostCenter(current_branch_code):
    """
    Populates the cost center comboboxes, filtered by the current branch.
    """
    cosCenterList_ids = []  # Stores actual costCenterIds for the current branch

    # Clear existing items
    costCenter_id.clear()
    costCenter_text.clear()

    # Add a default placeholder/instruction item first
    costCenter_text.addItem("โปรดเลือกศูนย์ต้นทุน...")  # Placeholder text for visible combobox
    costCenter_id.addItem("")  # Corresponding empty value for the hidden ID combobox

    # Filter costcenters based on the pwaCode matching the current_branch_code
    all_costcenters = reference["referances"]["pwawaterwork"]["costcenters"]
    filtered_costcenters = [
        cc for cc in all_costcenters
        if cc.get("pwaCode") == current_branch_code
    ]

    for center_data in filtered_costcenters:
        costCenter_id.addItem(str(center_data["costCenterId"]))
        cosCenterList_ids.append(str(center_data["costCenterId"]))
        costCenter_text.addItem(str(center_data["depShortName"]))

    # Attempt to set the current selection based on the feature's existing costCenterId
    current_feature_cost_center_id_str = costCenterId.text()
    if current_feature_cost_center_id_str and current_feature_cost_center_id_str != 'NULL':
        try:
            # Find the index of the existing costCenterId in the populated (filtered) combobox
            # Note: costCenter_id items now start after the placeholder at index 0
            idx = costCenter_id.findText(current_feature_cost_center_id_str)
            if idx != -1:  # Found
                costCenter_id.setCurrentIndex(idx)
                costCenter_text.setCurrentIndex(idx)
            else:  # Not found (e.g., from another branch, invalid, or not in filtered list)
                costCenter_id.setCurrentIndex(0)  # Default to placeholder
                costCenter_text.setCurrentIndex(0)
        except Exception as e:
            print(f"Error finding/setting cost center: {e}")
            costCenter_id.setCurrentIndex(0) # Default to placeholder
            costCenter_text.setCurrentIndex(0)
    else:
        # No valid existing value, default to placeholder
        costCenter_id.setCurrentIndex(0)
        costCenter_text.setCurrentIndex(0)


def costCenter_change():
    costCenter_id.setCurrentIndex(costCenter_text.currentIndex())
    selected_id_value = costCenter_id.currentText()
    if selected_id_value: # Not empty (i.e., not the placeholder)
        costCenterId.setText(costCenter_id.currentText())
    else:
        costCenterId.setText(None) # Or use "" if your attribute field expects an empty string for NULL


def load_PwaStation():
    """
    Populates the PWA station comboboxes.
    Note: This function is not currently filtered by branch in this modification.
          If branch-specific filtering is needed for PWA stations, a similar
          logic to load_CostCenter would be required.
    """
    stationList_ids = []

    pwaStation_id.clear()
    pwaStation_text.clear()

    # Add a default placeholder/instruction item first
    pwaStation_text.addItem("โปรดเลือกประเภทสถานที่...") # Placeholder text
    pwaStation_id.addItem("") # Corresponding empty value

    all_pwaStations = reference["referances"]["pwawaterwork"]["pwaStations"]
    # If filtering by branch were needed for stations, it would be applied here.
    # For now, we assume all stations are globally available or filtering is not required.
    
    for station_data in all_pwaStations:
        pwaStation_id.addItem(str(station_data["stationId"]))
        stationList_ids.append(str(station_data["stationId"]))
        pwaStation_text.addItem(str(station_data["description"]))

    # Attempt to set the current selection based on the feature's existing pwaStationId
    current_feature_station_id_str = pwaStationId.text()
    if current_feature_station_id_str and current_feature_station_id_str != 'NULL':
        try:
            idx = pwaStation_id.findText(current_feature_station_id_str)
            if idx != -1: # Found
                pwaStation_id.setCurrentIndex(idx)
                pwaStation_text.setCurrentIndex(idx)
            else: # Not found
                pwaStation_id.setCurrentIndex(0) # Default to placeholder
                pwaStation_text.setCurrentIndex(0)
        except Exception as e:
            print(f"Error finding/setting PWA station: {e}")
            pwaStation_id.setCurrentIndex(0)
            pwaStation_text.setCurrentIndex(0)
    else:
        # No valid existing value, default to placeholder
        pwaStation_id.setCurrentIndex(0)
        pwaStation_text.setCurrentIndex(0)


def pwaStation_change():
    pwaStation_id.setCurrentIndex(pwaStation_text.currentIndex())
    selected_id_value = pwaStation_id.currentText()
    if selected_id_value: # Not empty (i.e., not the placeholder)
        pwaStationId.setText(pwaStation_id.currentText())
    else:
        pwaStationId.setText(None) # Or use ""
