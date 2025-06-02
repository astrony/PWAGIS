from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtWidgets import QWidget, QVBoxLayout, QPushButton, QDialogButtonBox, QLineEdit, QMessageBox, QComboBox, QGroupBox, QApplication
from pwagis.utiles import *
from qgis.utils import iface
import os
import os.path
import json
import configparser
import requests
from pwagis.get_plugin_path import current_path
import random
from ulid import ULID
from urllib.request import urlopen


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
    global stepNo
    global stepName
    global JobStepId
    global JobStepNo
    global dmaNo
    global dmaNo_text
    global remark
    global _temp_id

    global baseUrl
    global config
    global configpath
    global token_new
    global refreshtoken_new
    global token
    global currentbranch

    myDialog = dialog
    # plugin_dir = os.getcwd()
    plugin_dir = current_path()
    myLayer = layerid
    myLayer.startEditing()

    groupBox = myDialog.findChild(QGroupBox, "groupBox")
    groupBox.setVisible(0)

    temp_random = random.randint(100000, 9000000)

    """  Get config from config.ini """
    config = configparser.ConfigParser()
    configpath = os.path.join(plugin_dir, 'config.ini')
    config.read(configpath)
    token_new = config.get('settings', 'token_new')
    refreshtoken_new = config.get('settings', 'refreshtoken_new')
    token = config.get('settings', 'token')
    currentbranch = config.get('settings', 'currentbranch')
    baseUrl = config.get('settings', 'baseUrl')
    print(baseUrl)

    """  Step Test  No"""
    stepNo = myDialog.findChild(QLineEdit, "stepNo")

    stepName = myDialog.findChild(QLineEdit, "stepName")
    JobStepId = myDialog.findChild(QLineEdit, "JobStepId")
    JobStepNo = myDialog.findChild(QLineEdit, "JobStepNo")
    dmaNo = myDialog.findChild(QLineEdit, "dmaNo")
    dmaNo_text = myDialog.findChild(QComboBox, "dmaNo_text")
    remark = myDialog.findChild(QLineEdit, "remark")

    """ Temp """
    _temp_id = myDialog.findChild(QLineEdit, "_temp_id")
    if _temp_id.text() == 'NULL' or _temp_id.text() == '':
        _temp_id.setText(str(temp_random))

    """ GlobalId """
    globalId = myDialog.findChild(QLineEdit, "globalId")
    tempGlobalId = str(ULID())
    print("tempGlobalId : " + str(tempGlobalId))
    if globalId.text() == 'NULL' or globalId.text() == '':
        globalId.setText(str(tempGlobalId))

    dmaCollection = getDmaCollection()
    dmaData = getDmaData(dmaCollection)
    loadDmaName(dmaData)

    dmaNo_text.currentTextChanged.connect(dma_change)


def checkNetConnection():
    try:
        urlopen('http://www.google.com', timeout=10)
        print("Net id ok")
        return True
    except Exception as err:
        pass
    return False


def check_token_expired():
    if checkNetConnection() is True:
        url = baseUrl + "/api/2.0/resources/references/pipe-types"
        payload = {}
        headers = {
            'Authorization': 'Bearer ' + token_new
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        if response.status_code == 200:
            numberReturn = response.json()["numberReturn"]
            if numberReturn > 0:
                t_status = "0"
        else:
            t_status = "1"
        return t_status
    else:
        message = "No internet connection."
        print_message(message)


def load_new_token():
    global refreshtoken_new
    global token_new
    if checkNetConnection() is True:
        url = baseUrl + "/api/2.0/token"
        payload = 'grant_type=refresh_token&refresh_token=' + refreshtoken_new
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = requests.request("POST", url, headers=headers, data=payload)

        if response.status_code == 200:
            response = response.json()
            token_n = response['accessToken']
            refreshToken = response['refreshToken']
            token_new = token_n
            refreshtoken_new = refreshToken
            config.set('settings', 'refreshtoken_new', str(refreshtoken_new))
            config.set('settings', 'token_new', str(token_new))
            with open(configpath, 'w') as configfile:
                config.write(configfile)
            refreshtoken_new = config.get('settings', 'refreshtoken_new')
            token_new = config.get('settings', 'token_new')
            t_status = "0"
        else:
            t_status = "1"
        return t_status
    else:
        message = "No internet connection."
        print_message(message)


def getDmaCollection():
    collections = "err"
    if checkNetConnection() is True:
        t_status = check_token_expired()
        if t_status == "1":
            t_status = load_new_token()
        if t_status == "0":
            url = baseUrl + "/api/2.0/resources/features/pwa/collections?sort=createdAt:desc&limit=200&offset=0&title=B" + str(currentbranch) + "_dma*"
            payload = {}
            headers = {
                'Authorization': 'Bearer ' + str(token_new)
            }
            response = requests.request("GET", url, headers=headers, data=payload)
            if response.status_code == 200:
                numberReturn = response.json()["numberReturned"]
                if numberReturn > 0:
                    collections = response.json()["collections"][0]['id']
                else:
                    pass
            else:
                pass

            return collections
        else:
            message = "Can not get token from server."
            print_message(message)
    else:
        message = "No internet connection."
        print_message(message)


def getDmaData(collectionId):
    damFeature = []
    if checkNetConnection() is True:
        t_status = check_token_expired()
        if t_status == "1":
            t_status = load_new_token()
        if t_status == "0":
            url = baseUrl + "/api/2.0/resources/features/pwa/collections/" + collectionId + "/items?sort=dmaNo:asc"
            payload = {}
            headers = {
                'Authorization': 'Bearer ' + str(token_new)
            }
            response = requests.request("GET", url, headers=headers, data=payload)
            if response.status_code == 200:
                numberReturn = response.json()["numberReturned"]
                if numberReturn > 0:
                    damFeature = response.json()["features"]
                else:
                    pass
            else:
                pass
            return damFeature
        else:
            message = "Can not get token from server."
            print_message(message)
    else:
        message = "No internet connection."
        print_message(message)


def loadDmaName(dmaData):
    dmaNo_text.clear()
    for i in range(len(dmaData)):
        dmaNo_text.addItem(str(dmaData[i]["properties"]["dmaNo"]))

    dmaNo_text.setCurrentText(dmaNo.text())


def dma_change():
    dmaNo.setText(dmaNo_text.currentText())


def print_message(message):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)
    msg.setText(message)
    msg.setWindowTitle("PWA Message")
    msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    retval = msg.exec_()
