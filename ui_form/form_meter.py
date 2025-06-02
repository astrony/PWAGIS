from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QDialogButtonBox, QLineEdit, QMessageBox, QComboBox, QGroupBox, QTabWidget, QDateEdit, QApplication, QToolBar
from pwagis.utiles import *
from qgis.utils import iface
import os
import os.path
import json
import configparser
import requests
from datetime import datetime
from pwagis.get_plugin_path import current_path
from qgis.gui import *
from qgis.core import QgsExpressionContextUtils
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
    global myDialog
    global plugin_dir
    global reference
    global meter_size_item
    global meter_brand_item

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
    global cusPIN
    global label_Pin

    global tel
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

    global custstat
    global custstat_id
    global custstat_text
    global custFullName

    global custAddress

    global meterSize
    global meterSize_id
    global meterSize_text

    global meterBrand
    global meterBrand_id
    global meterBrand_text

    global meterNo

    global mtr_read_route
    global meter_route_seq
    global contrac_No
    global avg_use
    global present_use

    global meterStat
    global meterStat_id
    global meterStat_text

    global token_new
    global refreshtoken_new
    global config
    global configpath
    global token
    global moreinfo
    global groupBox
    global tabWidget
    global currentbranch

    global begin_meter_date
    global begin_cus_date

    global loadBldgBtn

    global _temp_id

    global baseUrl

    global pushButton_3

    global buildingId
    global pipeId
    global remark
    global custAddress

    # print(value)

    myDialog = dialog
    # plugin_dir = os.getcwd()
    plugin_dir = current_path()
    myLayer = layerid
    myLayer.startEditing()
    cus_id = ""

    canvas = iface.mapCanvas()

    groupBox = myDialog.findChild(QGroupBox, "groupBox")
    groupBox.setVisible(True)

    tabWidget = myDialog.findChild(QTabWidget, "tabWidget")
    tabWidget.setTabVisible(3, False)

    temp_random = random.randint(100000, 9000000)

    # Get config from config.ini
    config = configparser.ConfigParser()
    configpath = os.path.join(plugin_dir, 'config.ini')
    config.read(configpath)
    token_new = config.get('settings', 'token_new')
    refreshtoken_new = config.get('settings', 'refreshtoken_new')
    token = config.get('settings', 'token')
    currentbranch = config.get('settings', 'currentbranch')
    baseUrl = config.get('settings', 'baseUrl')

    """ Load JSON REFERENCE """
    json_file = "referances.json"
    json_path = os.path.join(plugin_dir, "json", json_file)
    with open(json_path, 'r', encoding='utf-8') as openfile:
        reference = json.load(openfile)

    """ Load JSON METER SIZE """
    json_file = "meter_size.json"
    json_path = os.path.join(plugin_dir, "json", json_file)
    with open(json_path, 'r', encoding='utf-8') as openfile:
        meter_size_item = json.load(openfile)

    """ Load JSON METER BRAND """
    json_file = "meter_brand.json"
    json_path = os.path.join(plugin_dir, "json", json_file)
    with open(json_path, 'r', encoding='utf-8') as openfile:
        meter_brand_item = json.load(openfile)

    """ Cus Code """
    custCode = myDialog.findChild(QLineEdit, "custCode")

    meterNo = myDialog.findChild(QLineEdit, "meterNo")
    meterNo.setEnabled(1)
    meterNo.setVisible(False)
    label_meterNo = myDialog.findChild(QLabel, "label_meterNo")
    label_meterNo.setVisible(False)

    custNameSurname = myDialog.findChild(QLineEdit, "custName_Surname")
    custNameSurname.setEnabled(0)

    custstat = myDialog.findChild(QLineEdit, "custStat")
    custstat_id = myDialog.findChild(QComboBox, "custstat_id")
    custstat_text = myDialog.findChild(QComboBox, "custstat_text")
    custstat_text.setEnabled(0)

    cusPIN = myDialog.findChild(QLineEdit, "PIN")
    cusPIN.setVisible(0)

    label_Pin = myDialog.findChild(QLabel, "label_Pin")
    label_Pin.setVisible(0)

    useTypeId = myDialog.findChild(QLineEdit, "useTypeId")
    useType_id = myDialog.findChild(QComboBox, "useType_id")
    useType_text = myDialog.findChild(QComboBox, "useType_text")
    useType_text.setEnabled(0)

    """ Cus Address """
    tel = myDialog.findChild(QLineEdit, "tel")
    tel.setEnabled(0)
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

    custAddress = myDialog.findChild(QLineEdit, "custAddress")
    if custAddress.text() == 'NULL' or custAddress.text() == '':
        custAddress.setText('')

    remark = myDialog.findChild(QLineEdit, "remark")
    if remark.text() == 'NULL' or remark.text() == '':
        remark.setText('')

    """ TAB 3 MTRRDROUTE """
    mtr_read_route = myDialog.findChild(QLineEdit, "MTRRDROUTE")
    mtr_read_route.setEnabled(0)
    meter_route_seq = myDialog.findChild(QLineEdit, "MTRSEQ")
    meter_route_seq.setEnabled(0)
    contrac_No = myDialog.findChild(QLineEdit, "CONTRACNO")
    contrac_No.setEnabled(0)

    avg_use = myDialog.findChild(QLineEdit, "AVGWTUSG")
    avg_use.setEnabled(0)
    present_use = myDialog.findChild(QLineEdit, "PRSWTUSG")
    present_use.setEnabled(0)

    meterStat = myDialog.findChild(QLineEdit, "METERSTAT")
    meterStat_id = myDialog.findChild(QComboBox, "meterStat_id")
    meterStat_text = myDialog.findChild(QComboBox, "meterStat_text")
    meterStat_text.setEnabled(0)

    """ TAB 2 METER """
    meterSize = myDialog.findChild(QLineEdit, "METERSIZE")
    meterSize_id = myDialog.findChild(QComboBox, "meterSize_id")
    meterSize_text = myDialog.findChild(QComboBox, "meterSize_text")
    meterSize_text.setEnabled(0)

    meterBrand = myDialog.findChild(QLineEdit, "MTRMKCODE")
    meterBrand_id = myDialog.findChild(QComboBox, "mtrmkCode_id")
    meterBrand_text = myDialog.findChild(QComboBox, "mtrmkCode_text")
    meterBrand_text.setEnabled(0)

    begin_meter_date = myDialog.findChild(QDateEdit, "BGNMTRDT")
    begin_meter_date.setReadOnly(True)

    begin_cus_date = myDialog.findChild(QDateEdit, "BGNCUSTDT")
    begin_cus_date.setReadOnly(True)

    custFullName = myDialog.findChild(QLineEdit, "custFullName")

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

    buildingId = myDialog.findChild(QLineEdit, "buildingId")
    if buildingId.text() == 'NULL' or buildingId.text() == '':
        buildingId.setText('')

    pipeId = myDialog.findChild(QLineEdit, "pipeId")
    if pipeId.text() == 'NULL' or pipeId.text() == '':
        pipeId.setText('')

    # get_cus_code()
    # get_all_meter()
    load_meterSize()
    load_meterBrand()
    load_meterStat()
    collection_id = getCollectionId()
    get_building_feature(collection_id)

    load_useStatus()
    load_useType()

    """ Load More info """
    moreinfo = myDialog.findChild(QPushButton, "moreinfo")
    moreinfo.clicked.connect(checkClickMoreInfo)

    """ Get Cust Information When have cusCode """
    temeCusCode = str(custCode.text())
    if temeCusCode != "NULL" or temeCusCode == "":
        get_cus_code('load')
    else:
        custCode.setText("")

    """ Status Change """
    meterSize_text.currentTextChanged.connect(meterSize_change)
    meterBrand_text.currentTextChanged.connect(meterBrand_change)
    meterStat_text.currentTextChanged.connect(meterStat_change)
    custstat_text.currentTextChanged.connect(useStatus_change)
    useType_text.currentTextChanged.connect(useType_change)

    """ Load Map Tools BLDG"""
    loadBldgBtn = myDialog.findChild(QPushButton, "loadBldgBtn")
    map_tool = IdentifyFeatureTool(canvas)
    loadBldgBtn.clicked.connect(lambda: canvas.setMapTool(map_tool))
    map_tool.geomIdentified.connect(map_tool_bldg)

    """ Load Map Tools PIPE"""
    loadPipeBtn = myDialog.findChild(QPushButton, "loadPipeBtn")
    map_tool2 = IdentifyFeatureTool(canvas)
    loadPipeBtn.clicked.connect(lambda: canvas.setMapTool(map_tool2))
    map_tool2.geomIdentified.connect(map_tool_pipe)


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
        cus_id = ""
        url = baseUrl + "/api/2.0/resources/references/customer-informations?custCode=" + str(custCode.text())
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
                meterRouteId = items[0]['meterRouteId']
                mtr_read_route.setText(str(meterRouteId))
                meterRouteSeq = items[0]['meterRouteSeq']
                meter_route_seq.setText(str(meterRouteSeq))
                contracNo = items[0]['contracNo']

                contrac_No.setText(str(contracNo))
                installCusTitle = items[0]['installCusTitle']
                if installCusTitle is None:
                    installCusTitle = ''
                installCusName = items[0]['installCusName']
                if installCusName is None:
                    installCusName = ''
                installCusSurname = items[0]['installCusSurname']
                if installCusSurname is None:
                    installCusSurname = ''
                fullname = installCusTitle + installCusName + " " + str(installCusSurname)
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
                tel_str = items[0]['tel']

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
                tel.setText(str(tel_str))

                # get_cus_address(cus_id)
            else:
                if status == 'click':
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Warning)
                    msg.setText("ไม่พบที่อยู่ผู้ใช้น้ำ1")
                    msg.setWindowTitle("PWA Message")
                    msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                    retval = msg.exec_()
        return cus_id


def get_cus_address(cus_id):
    if checkNetConnection() is True:
        t_status = check_token_expired()
        if t_status == "1":
            t_status = load_new_token()
        if t_status == "0":
            # url = "https://dev-claystone.i-bitz.world/api/2.0/resources/references/customer-address-informations?customerId=" + str(cus_id)
            url = baseUrl + "/api/2.0/resources/references/customer-address-informations?customerId=" + str(cus_id)
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
                    road_str = items[0]['road']
                    villageNo_str = items[0]['villageNo']
                    village_str = items[0]['village']
                    floor_str = items[0]['floor']
                    builing_str = items[0]['building']
                    subdistrict_str = items[0]['amphur']
                    district_str = items[0]['district']
                    province_str = items[0]['province']
                    zip_str = items[0]['zipcode']
                    tel_str = items[0]['tel']

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
                    tel.setText(str(tel_str))
                else:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Warning)
                    msg.setText("ไม่พบที่อยู่ผู้ใช้น้ำ")
                    msg.setWindowTitle("PWA Message")
                    msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                    retval = msg.exec_()
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Can not get token from server.")
            msg.setWindowTitle("PWA Message")
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            retval = msg.exec_()
    else:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("No internet connection.")
        msg.setWindowTitle("PWA Message")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        retval = msg.exec_()


def get_all_meter():
    if checkNetConnection() is True:
        t_status = check_token_expired()
        if t_status == "1":
            t_status = load_new_token()
        if t_status == "0":
            # url = "https://dev-claystone.i-bitz.world/api/2.0/resources/references/meters?meterNo=" + str(meterNo.text())
            url = baseUrl + "/api/2.0/resources/references/meters?meterNo=" + str(meterNo.text())
            payload = {}
            headers = {
                'Authorization': 'Bearer ' + str(token_new)
            }
            response = requests.request("GET", url, headers=headers, data=payload)
            if response.status_code == 200:
                numberReturn = response.json()["numberReturn"]
                if numberReturn > 0:
                    items = response.json()["items"]
                    meterBrand_str = items[0]['meterBrandId']
                    mtrSizer = items[0]['mtrSizeId']
                    mrtState = items[0]['mrtStateId']
                    average_use = items[0]['average']
                    presentCountMeter_str = items[0]['presentCountMeter']
                    installDate_str = items[0]['installDate']

                    avg_use.setText(str(average_use))
                    present_use.setText(str(presentCountMeter_str))
                    meterSize.setText(str(mtrSizer))
                    meterBrand.setText(str(meterBrand_str))
                    meterStat.setText(str(mrtState))

                    dt_with_timezone = datetime.fromisoformat(installDate_str)
                    # Convert to desired format
                    t_year = dt_with_timezone.strftime("%Y")
                    t_m = dt_with_timezone.strftime("%m")
                    t_d = dt_with_timezone.strftime("%d")
                    begin_meter_date.setDate(QDate(int(t_year), int(t_m), int(t_d)))
                    begin_cus_date.setDate(QDate(int(t_year), int(t_m), int(t_d)))

                else:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Warning)
                    msg.setText("ไม่พบ")
                    msg.setWindowTitle("PWA Message")
                    msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                    retval = msg.exec_()
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Can not get token from server.")
            msg.setWindowTitle("PWA Message")
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            retval = msg.exec_()
    else:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("No internet connection.")
        msg.setWindowTitle("PWA Message")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        retval = msg.exec_()


def getCollectionId():
    searchtxt = "B" + currentbranch + "_BLDG"
    bldgCollection = ""
    if checkNetConnection() is True:
        t_status = check_token_expired()
        if t_status == "1":
            t_status = load_new_token()
        if t_status == "0":
            # url = "https://dev-claystone.i-bitz.world/api/2.0/resources/features/pwa/collections?title=" + searchtxt
            url = baseUrl + "/api/2.0/resources/features/pwa/collections?title=" + searchtxt
            payload = {}
            headers = {
                'Authorization': 'Bearer ' + str(token_new)
            }
            response = requests.request("GET", url, headers=headers, data=payload)
            if response.status_code == 200:
                numberMatched = response.json()["numberMatched"]
                if numberMatched > 0:
                    collections = response.json()["collections"]
                    bldgCollection = collections[0]["id"]

                print("Found")
                return bldgCollection
            else:
                print("Not found")
                # return collectionID
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Can not get token from server.")
            msg.setWindowTitle("PWA Message")
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            retval = msg.exec_()
    else:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("No internet connection.")
        msg.setWindowTitle("PWA Message")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        retval = msg.exec_()


def get_building_feature(collection_id):
    bldgCollection = collection_id
    if checkNetConnection() is True:
        t_status = check_token_expired()
        if t_status == "1":
            t_status = load_new_token()
        if t_status == "0":
            url = baseUrl + "/api/2.0/resources/features/pwa/collections/" + str(bldgCollection) + "/items?custCode=" + str(custCode.text())
            print(url)
            payload = {}
            headers = {
                'Authorization': 'Bearer ' + str(token_new)
            }
            response = requests.request("GET", url, headers=headers, data=payload)
            if response.status_code == 200:
                numberReturn = response.json()["numberReturned"]
                if numberReturn > 0:
                    properties = response.json()["features"][0]["properties"]
                    useStatusId_fea = properties['useStatusId']
                    useTypeId_fea = properties['useTypeId']
                    custstat.setText(str(useStatusId_fea))
                    useTypeId.setText(str(useTypeId_fea))
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Can not get token from server.")
            msg.setWindowTitle("PWA Message")
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            retval = msg.exec_()
    else:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("No internet connection.")
        msg.setWindowTitle("PWA Message")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        retval = msg.exec_()


def load_useType():
    json_file = "building_useType.json"
    json_path = os.path.join(plugin_dir, "json", json_file)
    with open(json_path, 'r', encoding='utf-8') as openfile:
        building_useType = json.load(openfile)
    useType = building_useType['items']

    for i in range(len(useType)):
        useType_id.addItem(str(useType[i]["useType"]))
        useType_text.addItem(str(useType[i]["useName"]))

    useType_id.setCurrentText(useTypeId.text())
    useType_text.setCurrentIndex(useType_id.currentIndex())
    if useTypeId.text() == "":
        useTypeId.setText("0")


def load_useStatus():
    useStatus = reference["referances"]["building"]["useStatus"]
    for i in range(len(useStatus)):
        custstat_id.addItem(str(useStatus[i]["statusId"]))
        custstat_text.addItem(str(useStatus[i]["description"]))

    custstat_id.setCurrentText(custstat.text())
    custstat_text.setCurrentIndex(custstat_id.currentIndex())
    if custstat.text() == "":
        custstat.setText("0")


def load_meterSize():
    meter_size = meter_size_item["items"]
    for i in range(len(meter_size)):
        meterSize_id.addItem(str(meter_size[i]["id"]))
        meterSize_text.addItem(str(meter_size[i]["sizeName"]))

    meterSize_id.setCurrentText(meterSize.text())
    meterSize_text.setCurrentIndex(meterSize_id.currentIndex())
    if meterSize.text() == "":
        meterSize.setText("1")


def load_meterBrand():
    meter_brand = meter_brand_item["items"]
    for i in range(len(meter_brand)):
        meterBrand_id.addItem(str(meter_brand[i]["id"]))
        meterBrand_text.addItem(str(meter_brand[i]["brandName"]))

    meterBrand_id.setCurrentText(meterBrand.text())
    meterBrand_text.setCurrentIndex(meterBrand_id.currentIndex())
    if meterBrand.text() == "":
        meterBrand.setText("1")


def load_meterStat():
    meterStat_index = ["1", "2", "3", "4", "5"]
    meterStat_list = ["ปรกติ", "ผิดปรกติ", "มาตรวัดน้ำชำรุด", "มาตรวัดน้ำสูญหาย", "มาตรวัดน้ำมัว"]
    for i in range(len(meterStat_list)):
        meterStat_text.addItem(str(meterStat_list[i]))
        meterStat_id.addItem(str(meterStat_index[i]))

    meterStat_id.setCurrentText(meterStat.text())
    meterStat_text.setCurrentIndex(meterStat_id.currentIndex())
    if meterStat.text() == "":
        meterStat.setText("1")


def meterSize_change():
    meterSize_id.setCurrentIndex(meterSize_text.currentIndex())
    meterSize.setText("")
    meterSize.setText(meterSize_id.currentText())


def meterBrand_change():
    meterBrand_id.setCurrentIndex(meterBrand_text.currentIndex())
    meterBrand.setText("")
    meterBrand.setText(meterBrand_id.currentText())


def meterStat_change():
    meterStat_id.setCurrentIndex(meterStat_text.currentIndex())
    meterStat.setText("")
    meterStat.setText(meterStat_id.currentText())


def useStatus_change():
    custstat_id.setCurrentIndex(custstat_text.currentIndex())
    custstat.setText("")
    custstat.setText(custstat_id.currentText())


def useType_change():
    useType_id.setCurrentIndex(useType_text.currentIndex())
    useTypeId.setText("")
    useTypeId.setText(useType_id.currentText())


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
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("No internet connection.")
        msg.setWindowTitle("PWA Message")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        retval = msg.exec_()


def load_new_token():
    global refreshtoken_new
    global token_new
    if checkNetConnection() is True:
        url = baseurl + "/api/2.0/token"
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
            # update_token_new()
            t_status = "0"
        else:
            t_status = "1"
        return t_status
    else:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("No internet connection.")
        msg.setWindowTitle("PWA Message")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        retval = msg.exec_()


def update_token_new():
    config.set('settings', 'token_new', str(token_new))
    with open(configpath, 'w') as configfile:
        config.write(configfile)
    token_new = config.get('settings', 'token_new')


def map_tool_bldg(feature):
    # from qgis.PyQt.QtWidgets import QMainWindow
    # value = QgsExpressionContextUtils.projectScope(QgsProject.instance()).variable('featureId')

    # Find BLDG Layer and set active
    layer_name = str(currentbranch) + "_BLDG"
    layers = QgsProject.instance().mapLayersByName(layer_name)
    if layers:
        layer = layers[0]
        iface.setActiveLayer(layer)

    # buildingId = myDialog.findChild(QLineEdit, "buildingId")

    titleValue = getTileValue("buildingTypeId", feature)
    if titleValue is not None:
        featureId = str(feature['id'])
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("ต้องการเลือกรหัสอาคารที่ใช้น้ำ : " + str(featureId) + " นี้หรือไม่")
        msg.setWindowTitle("PWA Message")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        retval = msg.exec_()
        if retval == QMessageBox.Ok:
            buildingId.setText(str(featureId))
    else:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("คุณไม่ได้เลือกชั้นข้อมูลอาคาร")
        msg.setWindowTitle("PWA Message")
        msg.setStandardButtons(QMessageBox.Ok)
        retval = msg.exec_()


def map_tool_pipe(feature):
    # value = QgsExpressionContextUtils.projectScope(QgsProject.instance()).variable('featureId')
    # Find BLDG Layer and set active
    layer_name = str(currentbranch) + "_PIPE"
    layers = QgsProject.instance().mapLayersByName(layer_name)
    if layers:
        layer = layers[0]
        iface.setActiveLayer(layer)

    titleValue = getTileValue("typeId", feature)
    if titleValue is not None:
        featureId = str(feature['id'])
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("ต้องการเลือกรหัสเส้นท่อที่ใช้น้ำ : " + str(featureId) + " นี้หรือไม่")
        msg.setWindowTitle("PWA Message")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        retval = msg.exec_()
        if retval == QMessageBox.Ok:
            pipeId.setText(str(featureId))
    else:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("คุณไม่ได้เลือกชั้นข้อมูลท่อ")
        msg.setWindowTitle("PWA Message")
        msg.setStandardButtons(QMessageBox.Ok)
        retval = msg.exec_()


def getTileValue(fieldsName, feature):
    returnValue = None
    liseField = feature.fields().names()

    for list_field in liseField:
        if list_field == fieldsName:
            returnValue = feature[fieldsName]

    return returnValue


def checkNetConnection():
    try:
        urlopen('http://www.google.com', timeout=10)
        print("Net id ok")
        return True
    except Exception as err:
        pass
    return False


""" Class For map Tools"""


class IdentifyFeatureTool(QgsMapToolIdentify):
    def __init__(self, canvas):
        # super().__init__(canvas)
        QgsMapToolIdentify.__init__(self, canvas)
        self.canvas = canvas

    geomIdentified = pyqtSignal(['QgsFeature'])

    def canvasReleaseEvent(self, mouseEvent):
        # get features at the current mouse position
        results = self.identify(mouseEvent.x(), mouseEvent.y(), self.TopDownStopAtFirst)
        if len(results) > 0:
            self.geomIdentified.emit(results[0].mFeature)
        self.canvas.unsetMapTool(self)  # Deactivate the tool after capturing the point


