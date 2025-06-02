from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtWidgets import QWidget, QVBoxLayout, QPushButton, QDialogButtonBox, QLabel, QLineEdit, QMessageBox, QComboBox, QGroupBox, QApplication
from pwagis.utiles import *
import os
import os.path
import json
import configparser
import requests
from pwagis.get_plugin_path import current_path
import random
from qgis.core import QgsExpressionContextUtils
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

    global globalId

    global useTypeId
    global useType_id
    global useType_text

    global buildingTypeId
    global buildingTypeId_id
    global buildingType_text

    global useStatusId
    global useStatus_id
    global useStatu_text

    global custCode
    global items
    global cus_id
    global custNameSurname
    global addressNo

    global custFullName

    global zipcode
    global province
    global district
    global subdistrict
    global soi
    global road
    global vilage
    global vilageNo
    global floor
    global builing
    global addressNo_cus

    global token_new
    global refreshtoken_new
    global config
    global configpath
    global baseurl

    global _temp_id
    global bldgId

    global moreinfo
    # global groupBox

    global selectedId

    global houseCode
    global feaId

    myDialog = dialog
    # plugin_dir = os.getcwd()
    plugin_dir = current_path()
    myLayer = layerid
    myLayer.startEditing()
    cus_id = ""

    groupBox = myDialog.findChild(QGroupBox, "groupBox")
    groupBox.setVisible(0)

    temp_random = random.randint(100000, 9000000)

    # Get config from config.ini
    config = configparser.ConfigParser()
    configpath = os.path.join(plugin_dir, 'config.ini')
    config.read(configpath)
    token_new = config.get('settings', 'token_new')
    refreshtoken_new = config.get('settings', 'refreshtoken_new')
    baseurl = config.get('settings', 'baseurl')

    """ Load JSON REFERENCE """
    json_file = "referances.json"
    json_path = os.path.join(plugin_dir, "json", json_file)
    with open(json_path, 'r', encoding='utf-8') as openfile:
        reference = json.load(openfile)

    feaId = myDialog.findChild(QLineEdit, "id")

    """ Cus Code """
    custCode = myDialog.findChild(QLineEdit, "custCode")
    custNameSurname = myDialog.findChild(QLineEdit, "custName_Surname")
    custNameSurname.setEnabled(0)

    custFullName = myDialog.findChild(QLineEdit, "custFullName")
    custFullName.setEnabled(1)

    addressNo = myDialog.findChild(QLineEdit, "addressNo")
    # if addressNo.text() == 'NULL':
    #     addressNo.setText("")

    remark = myDialog.findChild(QLineEdit, "remark")
    # if remark.text() == 'NULL':
    #     remark.setText("")

    """ Cus Address """
    zipcode = myDialog.findChild(QLineEdit, "ZIPCODE")
    zipcode.setEnabled(0)
    province = myDialog.findChild(QLineEdit, "PROVINCE")
    province.setEnabled(0)
    district = myDialog.findChild(QLineEdit, "DISTRICT")
    district.setEnabled(0)
    subdistrict = myDialog.findChild(QLineEdit, "SUBDISTRICT")
    subdistrict.setEnabled(0)
    soi = myDialog.findChild(QLineEdit, "SOI")
    soi.setEnabled(0)
    road = myDialog.findChild(QLineEdit, "ROAD")
    road.setEnabled(0)
    vilage = myDialog.findChild(QLineEdit, "VILLAGE")
    vilage.setEnabled(0)
    vilageNo = myDialog.findChild(QLineEdit, "VILLAGENO")
    vilageNo.setEnabled(0)
    floor = myDialog.findChild(QLineEdit, "FLOOR")
    floor.setEnabled(0)
    builing = myDialog.findChild(QLineEdit, "BUILDING")
    builing.setEnabled(0)
    addressNo_cus = myDialog.findChild(QLineEdit, "addressNo_cus")
    addressNo_cus.setEnabled(0)

    """ HouseCode"""
    houseCode = myDialog.findChild(QLineEdit, "houseCode")
    # if houseCode.text() == 'NULL' or houseCode.text() == '':
    #     houseCode.setText("")

    """ Use Type"""
    useTypeId = myDialog.findChild(QLineEdit, "useTypeId")
    useType_id = myDialog.findChild(QComboBox, "useType_id")
    useType_text = myDialog.findChild(QComboBox, "useType_text")

    """ Use Status """
    useStatusId = myDialog.findChild(QLineEdit, "useStatusId")
    useStatus_id = myDialog.findChild(QComboBox, "useStatus_id")
    useStatu_text = myDialog.findChild(QComboBox, "useStatu_text")

    """ Building Type """
    buildingTypeId = myDialog.findChild(QLineEdit, "buildingTypeId")
    buildingTypeId_id = myDialog.findChild(QComboBox, "buildingTypeId_id")
    buildingType_text = myDialog.findChild(QComboBox, "buildingType_text")

    bldgId = myDialog.findChild(QLineEdit, "bldgId")
    bldgId.setEnabled(1)
    bldgId.setVisible(False)
    label_bldgId = myDialog.findChild(QLabel, "label_bldgId")
    label_bldgId.setVisible(False)

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

    """ id """
    selectedId = myDialog.findChild(QLineEdit, "id")

    # temp_id

    """ Load More info """
    moreinfo = myDialog.findChild(QPushButton, "moreinfo")
    moreinfo.clicked.connect(checkClickMoreInfo)

    """ Get Cust Information When have cusCode """
    temeCusCode = str(custCode.text())
    if temeCusCode != "NULL" or temeCusCode == "":
        get_cus_code('load')
    else:
        custCode.setText("")

    if custFullName.text() == 'NULL':
        custFullName.setText('')

    load_useType()
    load_useStatus()
    load_buildingType()

    useType_text.currentTextChanged.connect(useType_change)
    useStatu_text.currentTextChanged.connect(useStatus_change)
    buildingType_text.currentTextChanged.connect(buildingType_change)


def load_useStatus():
    useStatusList = []
    useStatus = reference["referances"]["building"]["useStatus"]

    for i in range(len(useStatus)):
        useStatus_id.addItem(str(useStatus[i]["statusId"]))
        useStatusList.append(str(useStatus[i]["statusId"]))
        useStatu_text.addItem(str(useStatus[i]["description"]))

    """ Add Other for not in DataDic """
    useStatu_text.addItem("โปรดเลือกสถานะการใช้น้ำ")
    useStatus_id.addItem("Other")

    if useStatusId.text() not in useStatusList:
        if feaId.text() == 'NULL':
            useStatu_text.setCurrentIndex(1)
            useStatus_id.setCurrentIndex(1)
            useStatusId.setText(useStatus_id.currentText())
        else:
            useStatu_text.setCurrentIndex(len(useStatusList))
            useStatus_id.setCurrentIndex(len(useStatusList))
    else:
        useStatus_id.setCurrentText(useStatusId.text())
        useStatu_text.setCurrentIndex(useStatus_id.currentIndex())
    disableCusCode = ['2', '3', '4']  # 2,3,4 ต้องไม่ใส custCode
    if useStatusId.text() in disableCusCode or useStatus_id.currentText() == 'Other':
        custCode.setEnabled(0)
        custCode.setText(None)
    else:
        custCode.setEnabled(1)


def load_buildingType():
    buildingList = []
    buildingTypes = reference["referances"]["building"]["buildingTypes"]
    for i in range(len(buildingTypes)):
        buildingTypeId_id.addItem(str(buildingTypes[i]["typeId"]))
        buildingList.append(str(buildingTypes[i]["typeId"]))
        buildingType_text.addItem(str(buildingTypes[i]["description"]))

    """ Add Other for not in DataDic """
    buildingType_text.addItem("โปรดเลือกประเภทของอาคาร")
    buildingTypeId_id.addItem("Other")

    if buildingTypeId.text() not in buildingList:
        buildingType_text.setCurrentIndex(len(buildingList))
        buildingTypeId_id.setCurrentIndex(len(buildingList))
    else:
        buildingTypeId_id.setCurrentText(buildingTypeId.text())
        buildingType_text.setCurrentIndex(buildingTypeId_id.currentIndex())


def load_useType():
    json_file = "building_useType.json"
    json_path = os.path.join(plugin_dir, "json", json_file)
    with open(json_path, 'r', encoding='utf-8') as openfile:
        building_useType = json.load(openfile)
    useType = building_useType['items']
    useTypeList = []
    for i in range(len(useType)):
        useType_id.addItem(str(useType[i]["useType"]))
        useTypeList.append(str(useType[i]["useType"]))
        useType_text.addItem(str(useType[i]["useName"]))

    """ Add Other for not in DataDic """
    useType_text.addItem("โปรดเลือกประเภทการใช้น้ำ")
    useType_id.addItem("Other")

    if useTypeId.text() not in useTypeList:
        useType_text.setCurrentIndex(len(useTypeList))
        useType_id.setCurrentIndex(len(useTypeList))
    else:
        useType_id.setCurrentText(useTypeId.text())
        useType_text.setCurrentIndex(useType_id.currentIndex())


def useType_change():
    useType_id.setCurrentIndex(useType_text.currentIndex())
    if useType_id.currentText() != "Other":
        useTypeId.setText(useType_id.currentText())
    else:
        useTypeId.setText(None)


def buildingType_change():
    buildingTypeId_id.setCurrentIndex(buildingType_text.currentIndex())
    if buildingTypeId_id.currentText() != "Other":
        buildingTypeId.setText(buildingTypeId_id.currentText())
    else:
        buildingTypeId.setText(None)


def useStatus_change():
    disableCusCode = ['2', '3', '4']  # 2,3,4 ต้องไม่ใส custCode
    useStatus_id.setCurrentIndex(useStatu_text.currentIndex())
    if useStatus_id.currentText() != "Other":
        useStatusId.setText(useStatus_id.currentText())
    else:
        useStatusId.setText(None)

    if useStatusId.text() in disableCusCode or useStatus_id.currentText() == 'Other':
        custCode.setEnabled(0)
        custCode.setText(None)
    else:
        custCode.setEnabled(1)


def checkClickMoreInfo():
    if str(custCode.text()) == "" or str(custCode.text()) == "NULL":
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("คุณยังไม่ได้ใส่ข้อมูลเลขที่ผู้ใช้น้ำเพื่อทำการแสดงข้อมูลเพิ่มเติม")
        msg.setWindowTitle("PWA Message")
        msg.setStandardButtons(QMessageBox.Ok)
        retval = msg.exec_()
    else:
        get_cus_code('click')


def get_cus_code(status):
    temeCusCode = str(custCode.text())
    if len(temeCusCode) > 0:
        if checkNetConnection() is True:
            t_status = check_token_expired()
            if t_status == "1":
                t_status = load_new_token()
            if t_status == "0":
                # url = "https://gisapi-gateway.pwa.co.th/api/2.0/resources/references/customer-informations?custCode=" + str(custCode.text())
                url = baseurl + "/api/2.0/resources/references/customer-informations?custCode=" + str(custCode.text())
                payload = {}
                headers = {
                    'Authorization': 'Bearer ' + str(token_new)
                }
                response = requests.request("GET", url, headers=headers, data=payload)
                if response.status_code == 200:
                    numberReturn = response.json()["numberReturn"]
                    if numberReturn > 0:
                        items = response.json()["items"]
                        cus_id = items[0]['id']
                        # useStatus_edit.setText(str(cus_id))
                        installCusTitle = items[0]['installCusTitle']
                        installCusName = items[0]['installCusName']
                        installCusSurname = items[0]['installCusSurname']
                        fullname = str(installCusTitle) + str(installCusName) + " " + str(installCusSurname)
                        custNameSurname.setText(fullname)
                        custFullName.setText(fullname)

                        addressNo_cus_str = items[0]['addressNo']
                        soi_str = items[0]['soi']
                        road_str = items[0]['road']
                        villageNo_str = items[0]['villageNo']
                        village_str = items[0]['village']
                        floor_str = items[0]['floor']
                        builing_str = items[0]['building']
                        subdistrict_str = items[0]['districtName']
                        district_str = items[0]['amphurName']
                        province_str = items[0]['provinceName']
                        zip_str = items[0]['zipcode']

                        addressNo_cus.setText(str(addressNo_cus_str))
                        soi.setText(str(soi_str))
                        road.setText(str(road_str))
                        vilageNo.setText(str(villageNo_str))
                        vilage.setText(str(village_str))
                        floor.setText(str(floor_str))
                        builing.setText(str(builing_str))
                        subdistrict.setText(str(subdistrict_str))
                        district.setText(str(district_str))
                        province.setText(str(province_str))
                        zipcode.setText(str(zip_str))

                        # addressNo.setText(str(addressNo_cus_str))
                        # get_cus_address(cus_id)
                    else:
                        if status == 'click':
                            print_message("ไม่พบที่อยู่ผู้ใช้น้ำ")
            else:
                print_message("Can not get token from server.")
        else:
            print_message("No internet connection.")


def get_cus_address(cus_id):
    if checkNetConnection() is True:
        t_status = check_token_expired()
        if t_status == "1":
            t_status = load_new_token()
        if t_status == "0":
            url = baseurl + "/api/2.0/resources/references/customer-address-informations?customerId=" + str(cus_id)
            payload = {}
            headers = {
                'Authorization': 'Bearer ' + str(token_new)
            }
            response = requests.request("GET", url, headers=headers, data=payload)
            if response.status_code == 200:
                numberReturn = response.json()["numberReturn"]
                if numberReturn > 0:
                    items = response.json()["items"]

                    addressNo_cus_str = items[0]['addressNo']
                    soi_str = items[0]['soi']
                    road_str = items[0]['zipcode']
                    villageNo_str = items[0]['villageNo']
                    village_str = items[0]['village']
                    floor_str = items[0]['floor']
                    builing_str = items[0]['building']
                    subdistrict_str = items[0]['amphur']
                    district_str = items[0]['district']
                    province_str = items[0]['province']
                    zip_str = items[0]['zipcode']

                    addressNo_cus.setText(str(addressNo_cus_str))
                    soi.setText(str(soi_str))
                    road.setText(str(road_str))
                    vilageNo.setText(str(villageNo_str))
                    vilage.setText(str(village_str))
                    floor.setText(str(floor_str))
                    builing.setText(str(builing_str))
                    subdistrict.setText(str(subdistrict_str))
                    district.setText(str(district_str))
                    province.setText(str(province_str))
                    zipcode.setText(str(zip_str))

                    addressNo.setText(str(addressNo_cus_str))
                else:
                    print_message("ไม่พบที่อยู่ผู้ใช้น้ำ")
        else:
            print_message("Can not get token from server.")
    else:
        print_message("No internet connection.")


def check_token_expired():
    if checkNetConnection() is True:
        # url = "https://dev-claystone.i-bitz.world/api/2.0/resources/references/pipe-types"
        url = baseurl + "/api/2.0/resources/references/pipe-types"
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
        print_message("No internet connection.")


def load_new_token():
    global refreshtoken_new
    global token_new
    if checkNetConnection() is True:
        refreshtoken_new = config.get('settings', 'refreshtoken_new')
        url = baseurl + "/api/2.0/token"
        payload = 'grant_type=refresh_token&refresh_token=' + refreshtoken_new
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = requests.request("POST", url, headers=headers, data=payload)

        if response.status_code == 200:
            response = response.json()

            new_token = response['accessToken']
            new_refreshToken = response['refreshToken']

            config.set('settings', 'token_new', str(new_token))
            config.set('settings', 'refreshtoken_new', str(new_refreshToken))
            with open(configpath, 'w') as configfile:
                config.write(configfile)

            token_new = config.get('settings', 'token_new')
            refreshtoken_new = config.get('settings', 'refreshtoken_new')
            # update_token_new()
            t_status = "0"
        else:
            t_status = "1"
        return t_status
    else:
        print_message("No internet connection.")


def update_token_new():
    global token_new
    config.set('settings', 'token_new', str(token_new))
    with open(configpath, 'w') as configfile:
        config.write(configfile)
    token_new = config.get('settings', 'token_new')


def print_message(message):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)
    msg.setText(message)
    msg.setWindowTitle("PWA Message")
    msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    retval = msg.exec_()

