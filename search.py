from qgis.core import QgsVectorLayer, QgsProject
from qgis.PyQt.QtWidgets import *
from qgis.PyQt.QtGui import QPixmap
from qgis.PyQt.QtWidgets import QLabel, QHeaderView
from qgis.PyQt.QtCore import Qt
import os.path
import os
import json
import requests
import shutil
import configparser
import pandas as pd
from urllib.request import urlopen
from pwagis.utiles import *
import datetime
import pytz
from pwagis.pipe_project import *

def addDataLayerCombo(self):
    self.dockwidget.datalayercombo.clear()
    listDataLayer = ["เลือกชั้นข้อมูล", "มาตรวัดน้ำ", "อาคาร", "ที่ตั้งกิจการประปา", "ท่อประปา", "ประตูน้ำ", "หัวดับเพลิง", "จุดซ่อมท่อ"]
    for i in range(len(listDataLayer)):
        self.dockwidget.datalayercombo.addItem(listDataLayer[i])
    self.dockwidget.datalayercombo.setCurrentIndex(0)


def add_attributeCombo(self):
    self.dockwidget.attributeCombo.clear()
    self.dockwidget.searchText.setText("")
    self.dockwidget.resultTable.setRowCount(0)
    self.dockwidget.resultTable.clear()

    # Reset tempTabel (geometry)
    self.dockwidget.tempTable.setRowCount(0)  
    self.dockwidget.resultTable.horizontalHeader().setVisible(False)    

    search_text = self.dockwidget.datalayercombo.currentText()
    search_index = self.dockwidget.datalayercombo.currentIndex()
    if search_text == "มาตรวัดน้ำ" or search_index == 1:
        attribute = ["เลขที่ผู้ใช้น้ำ", "หมายเลขมาตรวัดน้ำ", "ที่อยู่", "ชื่อ"]
    elif search_text == "อาคาร"or search_index == 2:
        attribute = ["ชื่อ", "ที่อยู่", "รหัสอาคาร"]
    elif search_text == "ที่ตั้งกิจการประปา" or search_index == 3:
        attribute = ["รหัสประเภทสถานที่", "ชื่อ", "ที่อยู่ของที่ตั้งกิจการประปา"]
    elif search_text == "ท่อประปา" or search_index == 4:
        attribute = ["รหัสเส้นท่อ", "ชนิดและขนาด", "ความยาว", "ปีที่ติดตั้ง", "เลขที่สัญญา"] #, "รหัสครุภัณฑ์"
    elif search_text == 'ประตูน้ำ' or search_index == 5:
        attribute = ["รหัสประตูน้ำ", "ขนาด"]
    elif search_text == "หัวดับเพลิง" or search_index == 6:
        attribute = ["รหัสหัวดับเพลิง", "ขนาด"]
    elif search_text == "จุดซ่อมท่อ" or search_index == 7:
        attribute = ["เลขที่คำสั่งงานซ่อม", "วันที่รับแจ้ง", "วันที่ซ่อมเสร็จ", "ชนิด", "ขนาด"]  # ,"ความยาวท่อ"
    else:
        attribute = []

    for index in attribute:
        self.dockwidget.attributeCombo.addItem(index)


def search_meter(self):
    search_attribute = self.dockwidget.attributeCombo.currentText() 
    if search_attribute == "เลขที่ผู้ใช้น้ำ":
        search_tag = "custCode"
    elif search_attribute == "หมายเลขมาตรวัดน้ำ":
        search_tag = "meterNo"
    elif search_attribute == "ที่อยู่":
        search_tag = "addressNo"
    elif search_attribute == "ชื่อ":                
        search_tag = "custFullName"
    else:
        search_tag = ""

    if search_tag == "":
        attribute = ""    
    else:
        if search_attribute == "เลขที่ผู้ใช้น้ำ" or search_attribute == "หมายเลขมาตรวัดน้ำ":
            attribute = "&" + str(search_tag) + "=" + str(self.dockwidget.searchText.text())
        else:
            attribute = "&" + str(search_tag) + "=" + str(self.dockwidget.searchText.text()) + "*"

    self.dockwidget.LogTextEdit.setPlainText(str(attribute))
    return attribute


def search_bldg(self):
    search_attribute = self.dockwidget.attributeCombo.currentText() 
    if search_attribute == "ชื่อ":
        search_tag = "custFullName"  # CUSTNAME
    elif search_attribute == "ที่อยู่":
        search_tag = "addressNo" # CUSTADDR
    elif search_attribute == "รหัสอาคาร":
        search_tag = "_id" # search_tag = "bldgId"  # BLDG_ID
    else:
        search_tag = ""

    if search_tag == "":
        attribute = ""    
    else:
        if search_tag == "" or search_attribute == "ชื่อ" or search_attribute == "ที่อยู่":
            attribute = "&" + str(search_tag) + "=" + str(self.dockwidget.searchText.text()) + "*"
        else:
            attribute = "&" + str(search_tag) + "=" + self.dockwidget.searchText.text()
    # self.iface.messageBar().pushMessage("Information ", message, level=3, duration=3)
    return attribute


def search_pwa(self):
    attribute = ""
    search_tag = ""
    search_attribute = self.dockwidget.attributeCombo.currentText()
    search_attributeIndex = self.dockwidget.attributeCombo.currentIndex()
    if search_attribute == "รหัสประเภทสถานที่" or search_attributeIndex == 0:
        pwaStationText = self.dockwidget.attributeCombo_2.currentText()
        pwaStationId = pwaStationText.split(":")
        search_tag = "pwaStationId"
        attribute = "&" + str(search_tag) + "=" + str(pwaStationId[0])
    elif search_attribute == "ชื่อ" or search_attributeIndex == 1:
        search_tag = "name"
        attribute = "&" + str(search_tag) + "=*" + str(self.dockwidget.searchText.text()) + "*"
    elif search_attribute == "ที่อยู่ของที่ตั้งกิจการประปา" or search_attributeIndex == 2:
        search_tag = "pwaAddress"
        attribute = "&" + str(search_tag) + "=*" + str(self.dockwidget.searchText.text()) + "*"

    return attribute


def search_pipe(self):
    search_attribute = self.dockwidget.attributeCombo.currentText() 
    attribute = ""
    search_tag = ""
    pipe_s = 0
    pipe_t = ""
    if search_attribute == "รหัสเส้นท่อ":
        search_tag = "PIPE_ID" # change Search pipe id search_tag = "pipeId"
        attribute = "&" + str(search_tag) + "=" + str(self.dockwidget.searchText.text())
    elif search_attribute == "ชนิดและขนาด":
        search_tag_1 = "typeId"  # type
        search_tag_2 = "sizeId"  # size
        pipe_type = str(self.dockwidget.attributeCombo_3.currentText())
        pipe_size = str(self.dockwidget.attributeCombo_4.currentText())

        for p_Type in self.pipeTypes:
            if p_Type["description"] == self.dockwidget.attributeCombo_3.currentText():
                pipe_t = p_Type["typeId"]
                self.pipe_t = pipe_t

        for p_size in self.pipeSizes:
            temp_pipe_size = self.dockwidget.attributeCombo_4.currentText()
            if p_size["description"] == temp_pipe_size:
                pipe_s = p_size["sizeId"]

        if pipe_type == "ทุกชนิด" and pipe_size != "ทุกขนาด":
            attribute = "&" + str(search_tag_2) + "=" + str(pipe_s)
        elif pipe_type != "ทุกชนิด" and pipe_size == "ทุกขนาด":
            attribute = "&" + str(search_tag_1) + "=" + str(pipe_t)
        elif pipe_type != "ทุกชนิด" and pipe_size != "ทุกขนาด":
            # attribute = attribute + "&" + str(search_tag_2) + "=" + str(pipe_size)
            attribute = "&" + str(search_tag_1) + "=" + str(pipe_t) + "&" + str(search_tag_2) + "=" + str(pipe_s)
        else:
            attribute = ""

        # self.dockwidget.plainTextEdit.setPlainText(attribute)
    elif search_attribute == "ความยาว":
        search_tag = "length"
        attribute = "&" + str(search_tag) + "=" + str(self.dockwidget.attributeCombo_2.currentText())
    elif search_attribute == "ปีที่ติดตั้ง":
        attribute = ""
        search_tag = "yearInstall"
        year_install = self.dockwidget.searchText.text()
        attribute = attribute + "&" + str(search_tag) + "=" + str(year_install)
        """ Change Search Year install 20-11-67 """
        """ 
        # 1. ท่อที่มีอายุตั้งแต่ 0 - 5 ปี
        # 2. ท่อที่มีอายุตั้งแต่ 6 - 10 ปี
        # 3. ท่อที่มีอายุตั้งแต่ 11 - 15 ปี
        # 4. ท่อที่มีอายุมากกว่า 15 ปี ขึ้นไป
        year_type = self.dockwidget.attributeCombo_2.currentText()
        search_tag = 'yearInstall'
        tz = pytz.timezone('Asia/Bangkok')
        now1 = datetime.datetime.now(tz)
        thai_year = now1.year + 543
        attribute = ''
        i = 0
        j = 0
        if year_type == 'ท่อที่มีอายุตั้งแต่ 0 - 5 ปี':
            i = 5
            j = 0
        elif year_type == 'ท่อที่มีอายุตั้งแต่ 6 - 10 ปี':
            i = 10
            j = 6
        elif year_type == 'ท่อที่มีอายุตั้งแต่ 11 - 15 ปี':
            i = 15
            j = 11
        elif year_type == 'ท่อที่มีอายุมากกว่า 15 ปี ขึ้นไป':
            i = 100
            j = 16

        while i >= j:
            year_install = thai_year - i
            attribute = attribute + '&' + str(search_tag) + '=' + str(year_install)
            i = i - 1
        attribute = '&' + str(search_tag) + '=' + str(thai_year) +
        self.dockwidget.LogTextEdit.setPlainText('JJJJJJJJ ' + str(year_type) + 'JJJJJJJJJ')
        """
    # using dropdown insted of textbox
    elif search_attribute == "เลขที่สัญญา":
        attribute = ""
        search_tag = "projectNo"
        project_No = self.dockwidget.attributeCombo_2.currentText()
        if project_No and project_No != "":
            attribute = attribute + "&" + str(search_tag) + "=" + str(project_No)
    #    attribute = attribute + "&" + str(search_tag) + "=" + str(project_No)
   
    elif search_attribute == "รหัสครุภัณฑ์":
        attribute = ""
        search_tag = "assetCode"
        asset_Code = self.dockwidget.searchText.text()
        attribute = attribute + "&" + str(search_tag) + "=" + str(asset_Code)
    else:
        attribute = ""
    # attribute = "&" + str(search_tag) + "=" + str(self.dockwidget.searchText.text()) + "*"
    self.dockwidget.LogTextEdit.setPlainText(str(attribute))
    return attribute


def search_firehydrant(self):
    search_attribute = self.dockwidget.attributeCombo.currentText()
    size = 0
    if search_attribute == "รหัสหัวดับเพลิง":
        search_tag = "_id" # search_tag = "firehydrantId"
        attribute = "&" + str(search_tag) + "=" + str(self.dockwidget.searchText.text())
    elif search_attribute == "ขนาด":
        for firehydrantSize in self.firehydrantSizes:
            if firehydrantSize["description"] == self.dockwidget.attributeCombo_2.currentText():
                size = firehydrantSize["sizeId"]
        search_tag = "sizeId"  # size
        attribute = "&" + str(search_tag) + "=" + str(size)
    else:
        attribute = ""
    # attribute = "&" + str(search_tag) + "=" + str(self.dockwidget.searchText.text()) + "*"
    self.dockwidget.LogTextEdit.setPlainText(str(attribute))
    return attribute


def search_valve(self):
    search_attribute = self.dockwidget.attributeCombo.currentText()
    size = 0
    if search_attribute == "รหัสประตูน้ำ":
        search_tag = "_id" # search_tag = "valveId"
        attribute = "&" + str(search_tag) + "=" + str(self.dockwidget.searchText.text())
    elif search_attribute == "ขนาด":
        for valveSize in self.valveSizes:
            if valveSize["description"] == self.dockwidget.attributeCombo_2.currentText():
                size = valveSize["sizeId"]
        search_tag = "sizeId"  # size
        attribute = "&" + str(search_tag) + "=" + str(size)
    else:
        attribute = ""
    # attribute = "&" + str(search_tag) + "=" + str(self.dockwidget.searchText.text()) + "*"
    self.dockwidget.LogTextEdit.setPlainText(str(attribute))
    return attribute


# ["เลขที่คำสั่งงานซ่อม","วันที่รับแจ้ง","วันที่ซ่อมเสร็จ","ชนิด","ขนาด","ความยาวท่อ"] จุดซ่อมท่อ
def search_leakpoint(self):
    search_attribute = self.dockwidget.attributeCombo.currentText()
    if search_attribute == "เลขที่คำสั่งงานซ่อม":
        search_tag = "leakNo"  # 390911
        attribute = "&" + str(search_tag) + "=" + str(self.dockwidget.searchText.text()) + "*"
    elif search_attribute == "วันที่รับแจ้ง":  # 2018-08-11T00:00:00Z/2018-08-11T23:59:59Z
        value = self.dockwidget.mDateTimeEdit.dateTime()
        l_date = value.toString("yyyy-MM-dd")
        search_tag = "leakDatetime"  # datetime
        # attribute = "&" + str(search_tag) + "=" + str(self.dockwidget.searchText.text())
        attribute = "&" + str(search_tag) + "=" + str(l_date) + "T00:00:00Z/" + str(l_date) + "T23:59:59Z"
    elif search_attribute == "วันที่ซ่อมเสร็จ":  # 2018-08-11T00:00:00Z/2018-08-11T23:59:59Z
        value = self.dockwidget.mDateTimeEdit.dateTime()
        l_date = value.toString("yyyy-MM-dd")
        search_tag = "repairDatetime"
        # attribute = "&" + str(search_tag) + "=" + str(self.dockwidget.searchText.text())
        attribute = "&" + str(search_tag) + "=" + str(l_date) + "T00:00:00Z/" + str(l_date) + "T23:59:59Z"
    elif search_attribute == "ชนิด":
        pipe_t = ""
        search_tag = "pipeTypeId"
        for p_Type in self.pipeTypes:
            if p_Type["description"] == self.dockwidget.attributeCombo_2.currentText():
                pipe_t = p_Type["typeId"]
        attribute = "&" + str(search_tag) + "=" + str(pipe_t)
        # attribute = "&" + str(search_tag) + "=" + str(self.dockwidget.attributeCombo_2.currentText())
    elif search_attribute == "ขนาด":
        search_tag = "pipeSizeId"
        pipe_s = ""
        for p_size in self.pipeSizes:
            temp_pipe_size = self.dockwidget.attributeCombo_2.currentText()
            if p_size["description"] == temp_pipe_size:
                pipe_s = p_size["sizeId"]
        attribute = "&" + str(search_tag) + "=" + str(pipe_s)
        # attribute = "&" + str(search_tag) + "=" + str(self.dockwidget.attributeCombo_2.currentText())
    elif search_attribute == "ความยาวท่อ":
        search_tag = "PIPE_SIZE"
        attribute = "&" + str(search_tag) + "=" + str(self.dockwidget.attributeCombo_2.currentText())
    else:
        attribute = ""
    # attribute = "&" + str(search_tag) + "=" + str(self.dockwidget.searchText.text()) + "*"
    self.dockwidget.LogTextEdit.setPlainText(str(attribute))
    return attribute


def get_geo_string(self, geometry_type, coordinates):
    geo_text = ""
    if geometry_type == "Point":        
        x = str(coordinates[0])
        y = str(coordinates[1])
        # self.dockwidget.plainTextEdit.insertPlainText(str(x) + " " + str(y) + ",")
        geo_text = str(x) + " " + str(y)
        geo_text = "Point (" + geo_text + ")"
    elif geometry_type == "LineString":
        for a in range(len(coordinates)):
            x = str(coordinates[a][0])
            y = str(coordinates[a][1])
            
            if a == 0:
                geo_text = str(x) + " " + str(y)
            else:
                geo_text = geo_text + ", " + str(x) + " " + str(y)
        geo_text = "LineString (" + geo_text + ")"
    elif geometry_type == "Polygon":
        for a in range(len(coordinates[0])):
            x = coordinates[0][a][0]
            y = coordinates[0][a][1]
            if a == 0:
                geo_text = str(x) + " " + str(y)
            else:
                geo_text = geo_text + ", " + str(x) + " " + str(y)
        geo_text = "Polygon ((" + geo_text + "))"
    return geo_text


def getItem_filter_new(self, collectionsID, attribute, search_para):
    searchData = []
    geo_df = []
    list_data = []
    list_id = []
    list_geo = []
    # attribute = ""
    if checkNetConnection() is True:
        t_status = check_token_expired(self)
        if t_status == "1":
            t_status = load_new_token(self)
        if t_status == "0":
            url = self.baseUrl + "/api/2.0/resources/features/pwa/collections/" + collectionsID + "/items?sort=createdAt:desc" + attribute + "&limit=" + self.maxfeature
            payload = {}
            headers = {
                'Authorization': 'Bearer ' + self.token_new
            }
            response = requests.request("GET", url, headers=headers, data=payload)
            self.dockwidget.LogTextEdit.setPlainText(url)
            if response.status_code == 200:
                response = response.json()["features"]
                if len(response) > 0:
                    # key = response[0]["properties"].keys()
                    for n, d in enumerate(response):
                        properties = response[n]["properties"]
                        geometry_type = response[n]["geometry"]["type"]
                        id = response[n]["id"]
                        coordinates = response[n]["geometry"]["coordinates"]
                        geo_text = get_geo_string(self, geometry_type, coordinates)
                        if n == 0:
                            list_data = [properties]
                            list_id = [id]
                            list_geo = [geo_text]
                        else:
                            list_data.append(properties)
                            list_id.append(id)
                            list_geo.append(geo_text)
                    geo_dic = dict({'id': list_id, 'geo_text': list_geo})

                    geo_df = pd.DataFrame(geo_dic)
                    searchData = pd.DataFrame.from_dict(list_data)
                    """ Start test For change value from statusId to description """
                    # Set description
                    if search_para == "VALVE":
                        new_searchData = set_valve_des(self, searchData)
                    elif search_para == "FIREHYDRANT":
                        new_searchData = set_firehydrant_des(self, searchData)
                    elif search_para == "PIPE":
                        new_searchData = set_pipe_des(self, searchData)
                    elif search_para == "ROAD":
                        # new_searchData = set_road_des(self, searchData)
                        new_searchData = searchData
                    elif search_para == "BLDG":
                        new_searchData = set_bldg_des(self, searchData)
                    elif search_para == "METER":
                        # new_searchData = set_bldg_des(self, searchData)
                        new_searchData = searchData
                    else:
                        new_searchData = searchData
                    new_searchData['more'] = ''
                    """ End test For change value from statusId to description """
                    return new_searchData, geo_df
                else:

                    return searchData, geo_df
            else:
                return searchData, geo_df
        else:
            message = "Can not get token from server"
            self.iface.messageBar().pushMessage("Warning  ", message, level=2, duration=3)
    else:
        message = "No internet connection."
        self.iface.messageBar().pushMessage("Warning  ", message, level=2, duration=3)
        return searchData, geo_df


def getItem_filter(self, collectionsID, attribute, search_para):
    # attribute = &CUSTNAME=xxx&CUSTADDR=78
    searchData = []
    geo_df = []
    list_data = []
    list_id = []
    list_geo = []
    # attribute = ""
    if checkNetConnection() is True:
        o_status = check_oldToken_expired(self)
        if o_status == "1":
            o_status = refresh_token(self)
        if o_status == "0":
            url = self.host + "/features/1.1/collections/" + collectionsID + "/items?&sort=_createdAt:asc" + attribute + "&limit=" + self.maxfeature
            payload = {}
            headers = {
                'Authorization': 'Bearer ' + self.token
            }
            response = requests.request("GET", url, headers=headers, data=payload)
            self.dockwidget.LogTextEdit.setPlainText(url)
            if response.status_code == 200:
                response = response.json()["features"]
                if len(response) > 0:
                    # key = response[0]["properties"].keys()
                    for n, d in enumerate(response):
                        properties = response[n]["properties"]
                        geometry_type = response[n]["geometry"]["type"]
                        id = response[n]["id"]
                        # self.dockwidget.LogTextEdit.insertPlainText(geometry_type + "\n")
                        coordinates = response[n]["geometry"]["coordinates"]
                        geo_text = get_geo_string(self, geometry_type, coordinates)

                        # new_status = dict({'description': ''})
                        # properties.update(new_status)

                        # more_dic = dict({'more': ''})
                        # properties.update(more_dic)
                        if n == 0:
                            list_data = [properties]
                            list_id = [id]
                            list_geo = [geo_text]
                        else:
                            list_data.append(properties)
                            list_id.append(id)
                            list_geo.append(geo_text)
                    geo_dic = dict({'id': list_id, 'geo_text': list_geo})

                    geo_df = pd.DataFrame(geo_dic)
                    searchData = pd.DataFrame.from_dict(list_data)
                    """ Start test For change value from statusId to description """
                    # Set description
                    if search_para == "VALVE":
                        new_searchData = set_valve_des(self, searchData)
                    elif search_para == "FIREHYDRANT":
                        new_searchData = set_firehydrant_des(self, searchData)
                    elif search_para == "PIPE":
                        new_searchData = set_pipe_des(self, searchData)
                    elif search_para == "ROAD":
                        # new_searchData = set_road_des(self, searchData)
                        new_searchData = searchData
                    elif search_para == "BLDG":
                        new_searchData = set_bldg_des(self, searchData)
                    elif search_para == "METER":
                        # new_searchData = set_bldg_des(self, searchData)
                        new_searchData = searchData
                    else:
                        new_searchData = searchData
                    new_searchData['more'] = ''
                    """ End test For change value from statusId to description """
                    return new_searchData, geo_df
                else:
                    return searchData, geo_df
            else:
                return searchData, geo_df
    else:
        message = "No internet connection."
        self.iface.messageBar().pushMessage("Warning  ", message, level=2, duration=3)
        return searchData, geo_df


def loadResultToTable(self, properties, geo_df):
    if checkNetConnection() is True:
        if len(properties) == 0:
            self.dockwidget.resultTable.setRowCount(0)
            self.dockwidget.resultTable.clear()
            message = "ไม่พบข้อมูลที่ต้องการค้นหา"
            # self.iface.messageBar().pushMessage("Warning  ", message, level=2, duration=3)
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText(str(message))
            msg.setWindowTitle("PWA Message")
            msg.setStandardButtons(QMessageBox.Ok)
            # msg.buttonClicked.connect()
            retval = msg.exec_()

        else:
            dis_select_header = ["_collectionId", "_createdAt", "_createdBy", "_updatedAt", "_updatedBy", "remark", "picturePath", "pressureHistory", "_id"]
            # pressure
            header = []
            geo_header = ["id", "geo_text"]
            for header_key in properties.keys():
                if header_key not in dis_select_header:
                    header.append(header_key)
            properties.fillna('', inplace=True)
            geo_df.fillna('', inplace=True)

            self.dockwidget.resultTable.setRowCount(properties.shape[0])
            self.dockwidget.tempTable.setRowCount(geo_df.shape[0])

            self.dockwidget.resultTable.horizontalHeader().setVisible(True)
            self.dockwidget.tempTable.horizontalHeader().setVisible(True)

            self.dockwidget.resultTable.setColumnCount(len(header))
            self.dockwidget.tempTable.setColumnCount(len(geo_header))
            
            self.dockwidget.resultTable.setHorizontalHeaderLabels(header)
            self.dockwidget.tempTable.setHorizontalHeaderLabels(geo_header)

            col = len(header)-1
            for row in properties.index:                
                i = 0
                while i < len(header):
                    tableItem = QTableWidgetItem(str(properties.loc[row][header[i]]))
                    self.dockwidget.resultTable.setItem(row, i, tableItem)                    
                    i += 1
                # Set QLabel to add image                                                 
                iLabel = QLabel()
                icon = QPixmap("more.png")
                icon = icon.scaled(16, 16)
                iLabel.setPixmap(icon)
                iLabel.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
                self.dockwidget.resultTable.setCellWidget(row, col, iLabel)
                more_header = self.dockwidget.resultTable.horizontalHeader()
                more_header.setSectionResizeMode(col, QHeaderView.ResizeToContents)
                # header.setResizeMode(1, QHeaderView.ResizeToContents)
            for row in geo_df.index:
                i = 0
                while i < len(geo_header):
                    temTableItem = QTableWidgetItem(str(geo_df.loc[row][geo_header[i]]))
                    self.dockwidget.tempTable.setItem(row, i, temTableItem)
                    i += 1
            self.dockwidget.LogTextEdit.setPlainText("pppp" + str(geo_df.index) + "pppp")
        self.dockwidget.resultTable.setEnabled(1)
    else:
        message = "No internet connection."
        self.iface.messageBar().pushMessage("Warning  ", message, level=2, duration=3)


def search_data(self, search_text):
    search_para = ""
    attribute = ""
    if search_text == "มาตรวัดน้ำ":
        search_para = "METER"
        attribute = search_meter(self)            
    elif search_text == "อาคาร":
        search_para = "BLDG"
        attribute = search_bldg(self)            
    elif search_text == "ที่ตั้งกิจการประปา":
        search_para = "PWA_WATERWORKS"
        attribute = search_pwa(self)
    elif search_text == "ท่อประปา":
        search_para = "PIPE"
        attribute = search_pipe(self)
    elif search_text == "ประตูน้ำ":
        search_para = "VALVE"
        attribute = search_valve(self)
    elif search_text == "หัวดับเพลิง":
        search_para = "FIREHYDRANT"
        attribute = search_firehydrant(self)
    elif search_text == "จุดซ่อมท่อ":
        search_para = "LEAKPOINT"
        attribute = search_leakpoint(self)
    
    return attribute, search_para


def manage_search(self):
    pipe_value = []
    self.dockwidget.searchText.setText("")
    self.dockwidget.resultTable.setRowCount(0)    
    self.dockwidget.resultTable.horizontalHeader().setVisible(False)
    self.dockwidget.resultTable.clear()
    attribute1 = self.dockwidget.attributeCombo.currentText()
    datalayer = self.dockwidget.datalayercombo.currentText()
    attr_head = self.dockwidget.attributeCombo.currentText()

    if datalayer == "เลือกชั้นข้อมูล":
        self.dockwidget.mGroupBox_2.hide()
        self.dockwidget.mGroupBox_4.hide()
        self.dockwidget.mGroupBox_5.hide()
        self.dockwidget.mGroupBox_6.hide()
    elif datalayer == "มาตรวัดน้ำ":
        self.dockwidget.mGroupBox_2.setTitle(attr_head)
        self.dockwidget.mGroupBox_2.show()
        self.dockwidget.mGroupBox_4.hide()
        self.dockwidget.mGroupBox_5.hide()
        self.dockwidget.mGroupBox_6.hide()
    elif datalayer == "อาคาร":
        self.dockwidget.mGroupBox_2.setTitle(attr_head)
        self.dockwidget.mGroupBox_2.show()
        self.dockwidget.mGroupBox_4.hide()
        self.dockwidget.mGroupBox_5.hide()
        self.dockwidget.mGroupBox_6.hide()
        self.dockwidget.mGroupBox_6.hide()
    elif (attribute1 == "รหัสประเภทสถานที่") and datalayer == "ที่ตั้งกิจการประปา":
        self.dockwidget.mGroupBox_2.hide()
        self.dockwidget.attributeCombo_2.clear()
        if attribute1 == "รหัสประเภทสถานที่":
            pwa_value = []
            for pwaType in self.pwaStations:
                pwa_value.append(str((pwaType["stationId"])))
                self.dockwidget.attributeCombo_2.addItem(str((pwaType["stationId"])) + ":" + str(pwaType["description"]))
        self.dockwidget.mGroupBox_4.setTitle(attr_head)
        self.dockwidget.mGroupBox_4.show()
        self.dockwidget.mGroupBox_5.hide()
        self.dockwidget.mGroupBox_6.hide()
    elif (attribute1 == "ชื่อ" or attribute1 == "ที่อยู่ของที่ตั้งกิจการประปา") and datalayer == "ที่ตั้งกิจการประปา":
        self.dockwidget.mGroupBox_2.setTitle(attr_head)
        self.dockwidget.mGroupBox_2.show()
        self.dockwidget.mGroupBox_4.hide()
        self.dockwidget.mGroupBox_5.hide()
        self.dockwidget.mGroupBox_6.hide()
    elif attribute1 == "รหัสเส้นท่อ" and datalayer == "ท่อประปา":
        self.dockwidget.mGroupBox_2.setTitle(attr_head)
        self.dockwidget.mGroupBox_2.show()
        self.dockwidget.mGroupBox_4.hide()
        self.dockwidget.mGroupBox_5.hide()
        self.dockwidget.mGroupBox_6.hide()
    # elif attribute1 == "เลขที่สัญญา" and datalayer == "ท่อประปา":
    #     self.dockwidget.mGroupBox_2.setTitle(attr_head)
    #     self.dockwidget.mGroupBox_2.show()
    #     self.dockwidget.mGroupBox_4.hide()
    #     self.dockwidget.mGroupBox_5.hide()
    #     self.dockwidget.mGroupBox_6.hide()
    
    ##### fix the dropdown #####
    elif attribute1 == "เลขที่สัญญา" and datalayer == "ท่อประปา":
        # Clear the combo box first
        self.dockwidget.attributeCombo_2.clear()
        
        # Call getPipeProject to retrieve all project numbers
        project_data = retrievePipeProjectForSearch(self)
        
        if project_data != "err" and project_data is not None:
            # Populate attributeCombo_2 with project numbers
            project_numbers = []
            for project in project_data:
                project_numbers.append(str(project['projectNo']))
                self.dockwidget.attributeCombo_2.addItem(str(project['projectNo']))
            
            # Show the appropriate group box with combo selection
            self.dockwidget.mGroupBox_4.setTitle(attr_head)
            self.dockwidget.mGroupBox_2.hide()
            self.dockwidget.mGroupBox_4.show()
            self.dockwidget.mGroupBox_5.hide()
            self.dockwidget.mGroupBox_6.hide()
        else:
            # Fallback to text input if API call fails
            self.dockwidget.mGroupBox_2.setTitle(attr_head)
            self.dockwidget.mGroupBox_2.show()
            self.dockwidget.mGroupBox_4.hide()
            self.dockwidget.mGroupBox_5.hide()
            self.dockwidget.mGroupBox_6.hide()

    elif attribute1 == "รหัสครุภัณฑ์" and datalayer == "ท่อประปา":
        self.dockwidget.mGroupBox_2.setTitle(attr_head)
        self.dockwidget.mGroupBox_2.show()
        self.dockwidget.mGroupBox_4.hide()
        self.dockwidget.mGroupBox_5.hide()
        self.dockwidget.mGroupBox_6.hide()

    elif attribute1 == "ชนิดและขนาด" and datalayer == "ท่อประปา":
        self.dockwidget.mGroupBox_5.setTitle(attr_head)
        self.dockwidget.attributeCombo_3.clear()
        self.dockwidget.attributeCombo_3.addItem("ทุกชนิด")
        for pipe_type in self.pipeTypes:
            self.dockwidget.attributeCombo_3.addItem(str(pipe_type["description"]))

        self.dockwidget.mGroupBox_2.hide()
        self.dockwidget.mGroupBox_4.hide()
        self.dockwidget.mGroupBox_5.show()
        self.dockwidget.mGroupBox_6.hide()
    elif attribute1 == "ความยาว" and datalayer == "ท่อประปา":
        self.dockwidget.attributeCombo_2.clear()
        pipe_length = [1, 6, 47, 78, 437, 578]
        for p_length in pipe_length:
            self.dockwidget.attributeCombo_2.addItem(str(p_length))
        self.dockwidget.mGroupBox_4.setTitle(attr_head)
        self.dockwidget.mGroupBox_2.hide()
        self.dockwidget.mGroupBox_4.show()            
        self.dockwidget.mGroupBox_5.hide()
        self.dockwidget.mGroupBox_6.hide()
        """ 
        # Chang Search Pipe year install 20-11-67
    elif attribute1 == 'ปีที่ติดตั้ง' and datalayer == 'ท่อประปา':
        yearInstall = ['ท่อที่มีอายุตั้งแต่ 0 - 5 ปี', 'ท่อที่มีอายุตั้งแต่ 6 - 10 ปี', 'ท่อที่มีอายุตั้งแต่ 11 - 15 ปี', 'ท่อที่มีอายุมากกว่า 15 ปี ขึ้นไป']
        self.dockwidget.attributeCombo_2.clear()
        for year_install in yearInstall:
            self.dockwidget.attributeCombo_2.addItem(str(year_install))
        self.dockwidget.mGroupBox_4.setTitle(attr_head)
        self.dockwidget.mGroupBox_2.hide()
        self.dockwidget.mGroupBox_4.show()
        self.dockwidget.mGroupBox_5.hide()
        self.dockwidget.mGroupBox_6.hide()
    """
    elif attribute1 == "ปีที่ติดตั้ง" and datalayer == "ท่อประปา":
        self.dockwidget.mGroupBox_2.setTitle(attr_head)
        self.dockwidget.mGroupBox_2.show()
        self.dockwidget.mGroupBox_4.hide()
        self.dockwidget.mGroupBox_5.hide()
        self.dockwidget.mGroupBox_6.hide()
    elif attribute1 == "ขนาด" and datalayer == "ประตูน้ำ":
        self.dockwidget.attributeCombo_2.clear()
        for valve_size in self.valveSizes:
            self.dockwidget.attributeCombo_2.addItem(str(valve_size["description"]))
        self.dockwidget.mGroupBox_4.setTitle(attr_head)
        self.dockwidget.mGroupBox_4.show()
        self.dockwidget.mGroupBox_2.hide()
        self.dockwidget.mGroupBox_5.hide()
        self.dockwidget.mGroupBox_6.hide()
    elif attribute1 == "รหัสประตูน้ำ" and datalayer == "ประตูน้ำ":
        self.dockwidget.attributeCombo_2.clear()
        self.dockwidget.mGroupBox_2.setTitle(attr_head)
        self.dockwidget.mGroupBox_2.show()
        self.dockwidget.mGroupBox_4.hide()
        self.dockwidget.mGroupBox_5.hide()
        self.dockwidget.mGroupBox_6.hide()
    elif attribute1 == "รหัสหัวดับเพลิง" and datalayer == "หัวดับเพลิง":
        self.dockwidget.attributeCombo_2.clear()
        self.dockwidget.mGroupBox_2.setTitle(attr_head)
        self.dockwidget.mGroupBox_2.show()
        self.dockwidget.mGroupBox_4.hide()
        self.dockwidget.mGroupBox_5.hide()
        self.dockwidget.mGroupBox_6.hide()
    elif attribute1 == "ขนาด" and datalayer == "หัวดับเพลิง":
        self.dockwidget.attributeCombo_2.clear()
        for firehydrantSize in self.firehydrantSizes:
            self.dockwidget.attributeCombo_2.addItem(str(firehydrantSize["description"]))
        self.dockwidget.mGroupBox_4.setTitle(attr_head)
        self.dockwidget.mGroupBox_4.show()
        self.dockwidget.mGroupBox_2.hide()
        self.dockwidget.mGroupBox_5.hide()
        self.dockwidget.mGroupBox_6.hide()
    elif (attribute1 == "เลขที่คำสั่งงานซ่อม") and datalayer == "จุดซ่อมท่อ":
        self.dockwidget.attributeCombo_2.clear()
        self.dockwidget.mGroupBox_2.setTitle(attr_head)
        self.dockwidget.mGroupBox_2.show()
        self.dockwidget.mGroupBox_4.hide()
        self.dockwidget.mGroupBox_5.hide()
        self.dockwidget.mGroupBox_6.hide()
    elif (attribute1 == "วันที่รับแจ้ง" or attribute1 == "วันที่ซ่อมเสร็จ") and datalayer == "จุดซ่อมท่อ":
        self.dockwidget.mGroupBox_6.setTitle(attr_head)
        self.dockwidget.mGroupBox_2.hide()
        self.dockwidget.mGroupBox_4.hide()
        self.dockwidget.mGroupBox_5.hide()
        self.dockwidget.mGroupBox_6.show()
    elif (attribute1 == "ชนิด" or attribute1 == "ขนาด" or attribute1 == "ความยาวท่อ") and datalayer == "จุดซ่อมท่อ":
        self.dockwidget.mGroupBox_2.hide()
        self.dockwidget.attributeCombo_2.clear()
        if attribute1 == "ชนิด":
            pipe_value = []
            for pipeType in self.pipeTypes:
                pipe_value.append(str(pipeType["description"]))
        elif attribute1 == "ขนาด":
            pipe_value = []
            for pipeSize in self.pipeSizes:
                pipe_value.append(str(pipeSize["description"]))
        elif attribute1 == "ความยาวท่อ":
            pipe_value = [2, 5, 10, 15]

        self.dockwidget.attributeCombo_2.clear()
        for pipes in pipe_value:
            self.dockwidget.attributeCombo_2.addItem(str(pipes))

        self.dockwidget.mGroupBox_4.setTitle(attr_head)
        self.dockwidget.mGroupBox_4.show()            
        self.dockwidget.mGroupBox_5.hide()
        self.dockwidget.mGroupBox_6.hide()
    else:
        self.dockwidget.mGroupBox_2.show()


def set_valve_des(self, searchData):
    """ Set Valve Status """
    description = []
    statusId = []
    for valve_status in self.valveStatus:
        statusId.append(valve_status["statusId"])
        description.append(str(valve_status["description"]))
    valveStatus_dic = {'statusId': statusId, 'description': description}
    df2 = pd.DataFrame(valveStatus_dic)
    col = searchData.shape[1]
    searchData.insert(col, 'description', '')
    searchData['description'] = ''
    searchData = searchData.merge(df2, on='statusId', how='left', suffixes=('_old', '_new'))
    searchData['description'] = searchData['description_new'].combine_first(searchData['description_old'])
    searchData = searchData.drop(['description_old', 'description_new', 'statusId'], axis=1)
    searchData.rename(columns={'description': 'valveStatus'}, inplace=True)

    """ Set Valve Size """
    description = []
    sizeId = []
    for valve_size in self.valveSizes:
        sizeId.append(valve_size["sizeId"])
        description.append(str(valve_size["description"]))
    valveSize_dic = {'sizeId': sizeId, 'description': description}
    df2 = pd.DataFrame(valveSize_dic)
    col = searchData.shape[1]
    searchData.insert(col, 'description', '')
    searchData['description'] = ''
    searchData = searchData.merge(df2, on='sizeId', how='left', suffixes=('_old', '_new'))
    searchData['description'] = searchData['description_new'].combine_first(searchData['description_old'])
    searchData = searchData.drop(['description_old', 'description_new', 'sizeId'], axis=1)
    searchData.rename(columns={'description': 'valveSizes'}, inplace=True)

    """ Set Valve Type """
    description = []
    typeId = []
    for valve_type in self.valveTypes:
        typeId.append(valve_type["typeId"])
        description.append(str(valve_type["description"]))
    valveTypes_dic = {'typeId': typeId, 'description': description}
    df2 = pd.DataFrame(valveTypes_dic)
    col = searchData.shape[1]
    searchData.insert(col, 'description', '')
    searchData['description'] = ''
    searchData = searchData.merge(df2, on='typeId', how='left', suffixes=('_old', '_new'))
    searchData['description'] = searchData['description_new'].combine_first(searchData['description_old'])
    searchData = searchData.drop(['description_old', 'description_new', 'typeId'], axis=1)
    searchData.rename(columns={'description': 'valveTypes'}, inplace=True)

    return searchData


def set_firehydrant_des(self, searchData):
    """ Set Firehydrant Status """
    description = []
    statusId = []
    for firehydrant_status in self.firehydrantStatus:
        statusId.append(firehydrant_status["statusId"])
        description.append(str(firehydrant_status["description"]))
    firehydrantStatus_dic = {'statusId': statusId, 'description': description}
    df2 = pd.DataFrame(firehydrantStatus_dic)
    col = searchData.shape[1]
    searchData.insert(col, 'description', '')
    searchData['description'] = ''
    searchData = searchData.merge(df2, on='statusId', how='left', suffixes=('_old', '_new'))
    searchData['description'] = searchData['description_new'].combine_first(searchData['description_old'])
    searchData = searchData.drop(['description_old', 'description_new', 'statusId'], axis=1)
    searchData.rename(columns={'description': 'firehydrantStatus'}, inplace=True)

    """ Set Firehydrant Size """
    description = []
    sizeId = []
    for firehydrant_size in self.firehydrantSizes:
        sizeId.append(firehydrant_size["sizeId"])
        description.append(str(firehydrant_size["description"]))
    firehydrantSizes_dic = {'sizeId': sizeId, 'description': description}
    df2 = pd.DataFrame(firehydrantSizes_dic)
    col = searchData.shape[1]
    searchData.insert(col, 'description', '')
    searchData['description'] = ''
    searchData = searchData.merge(df2, on='sizeId', how='left', suffixes=('_old', '_new'))
    searchData['description'] = searchData['description_new'].combine_first(searchData['description_old'])
    searchData = searchData.drop(['description_old', 'description_new', 'sizeId'], axis=1)
    searchData.rename(columns={'description': 'firehydrantSizes'}, inplace=True)

    return searchData


def set_pipe_des(self, searchData):
    """ Set Pipe Functions"""
    description = []
    functionId = []
    for pipe_function in self.pipeFunctions:
        functionId.append(pipe_function["functionId"])
        description.append(str(pipe_function["description"]))
    pipeFunctions_dic = {'functionId': functionId, 'description': description}
    df2 = pd.DataFrame(pipeFunctions_dic)
    col = searchData.shape[1]
    searchData.insert(col, 'description', '')
    searchData['description'] = ''
    searchData = searchData.merge(df2, on='functionId', how='left', suffixes=('_old', '_new'))
    searchData['description'] = searchData['description_new'].combine_first(searchData['description_old'])
    searchData = searchData.drop(['description_old', 'description_new', 'functionId'], axis=1)
    searchData.rename(columns={'description': 'pipeFunctions'}, inplace=True)

    """ Set Pipe Grade"""
    description = []
    gradeId = []
    for pipe_Grades in self.pipeGrades:
        gradeId.append(pipe_Grades["gradeId"])
        description.append(str(pipe_Grades["description"]))
    pipeGrades_dic = {'gradeId': gradeId, 'description': description}
    df2 = pd.DataFrame(pipeGrades_dic)
    col = searchData.shape[1]
    searchData.insert(col, 'description', '')
    searchData['description'] = ''
    searchData = searchData.merge(df2, on='gradeId', how='left', suffixes=('_old', '_new'))
    searchData['description'] = searchData['description_new'].combine_first(searchData['description_old'])
    searchData = searchData.drop(['description_old', 'description_new', 'gradeId'], axis=1)
    searchData.rename(columns={'description': 'pipeGrades'}, inplace=True)

    """ Set Pipe Layings"""
    description = []
    layingId = []
    for pipe_Layings in self.pipeLayings:
        layingId.append(pipe_Layings["layingId"])
        description.append(str(pipe_Layings["description"]))
    pipeLayings_dic = {'layingId': layingId, 'description': description}
    df2 = pd.DataFrame(pipeLayings_dic)
    col = searchData.shape[1]
    searchData.insert(col, 'description', '')
    searchData['description'] = ''
    searchData = searchData.merge(df2, on='layingId', how='left', suffixes=('_old', '_new'))
    searchData['description'] = searchData['description_new'].combine_first(searchData['description_old'])
    searchData = searchData.drop(['description_old', 'description_new', 'layingId'], axis=1)
    searchData.rename(columns={'description': 'pipeLayings'}, inplace=True)

    """ Set Pipe Products"""
    description = []
    productId = []
    for pipe_Products in self.pipeProducts:
        productId.append(pipe_Products["productId"])
        description.append(str(pipe_Products["description"]))
    pipeProducts_dic = {'productId': productId, 'description': description}
    df2 = pd.DataFrame(pipeProducts_dic)
    col = searchData.shape[1]
    searchData.insert(col, 'description', '')
    searchData['description'] = ''
    searchData = searchData.merge(df2, on='productId', how='left', suffixes=('_old', '_new'))
    searchData['description'] = searchData['description_new'].combine_first(searchData['description_old'])
    searchData = searchData.drop(['description_old', 'description_new', 'productId'], axis=1)
    searchData.rename(columns={'description': 'pipeProducts'}, inplace=True)

    """ Set Pipe Types"""
    description = []
    typeId = []
    for pipe_Types in self.pipeTypes:
        typeId.append(pipe_Types["typeId"])
        description.append(str(pipe_Types["description"]))
    pipeTypes_dic = {'typeId': typeId, 'description': description}
    df2 = pd.DataFrame(pipeTypes_dic)
    col = searchData.shape[1]
    searchData.insert(col, 'description', '')
    searchData['description'] = ''
    searchData = searchData.merge(df2, on='typeId', how='left', suffixes=('_old', '_new'))
    searchData['description'] = searchData['description_new'].combine_first(searchData['description_old'])
    searchData = searchData.drop(['description_old', 'description_new', 'typeId'], axis=1)
    searchData.rename(columns={'description': 'pipeTypes'}, inplace=True)

    """ Set Pipe Sizes"""

    description = []
    sizeId = []
    pipe_type = []
    try:
        if self.pipe_t == '':
            self.pipe_t = 'PVC'
        elif 'ST' in self.pipe_t:
            self.pipe_t = 'ST'
        elif self.pipe_t == 'GRP':
            self.pipe_t = 'ST'
        elif self.pipe_t == 'CI':
            self.pipe_t = 'ST'
    except:
        self.pipe_t = 'PVC'
    for pipe_Sizes in self.pipeSizes:
        if self.pipe_t == str(pipe_Sizes["type"]):
            sizeId.append(pipe_Sizes["sizeId"])
            description.append(str(pipe_Sizes["description"]))
    pipeSizes_dic = {'sizeId': sizeId, 'description': description}
    df2 = pd.DataFrame(pipeSizes_dic)
    col = searchData.shape[1]
    searchData.insert(col, 'description', '')
    searchData['description'] = ''
    searchData = searchData.merge(df2, on='sizeId', how='left', suffixes=('_old', '_new'))
    searchData['description'] = searchData['description_new'].combine_first(searchData['description_old'])
    searchData = searchData.drop(['description_old', 'description_new', 'sizeId'], axis=1)
    
    searchData.rename(columns={'description': 'pipeSizes'}, inplace=True)

    searchData.rename(columns={'classId': 'pipeClasses'}, inplace=True)
    return searchData


def set_road_des(self, searchData):
    """
    description = []
    functionId = []
    for road_Functions in self.roadFunctions:
        functionId.append(road_Functions["functionId"])
        description.append(str(road_Functions["description"]))
    roadFunctions_dic = {'functionId': functionId, 'description': description}
    df2 = pd.DataFrame(roadFunctions_dic)
    col = searchData.shape[1]
    searchData.insert(col, 'description', '')
    searchData['description'] = ''
    searchData = searchData.merge(df2, on='functionId', how='left', suffixes=('_old', '_new'))
    searchData['description'] = searchData['description_new'].combine_first(searchData['description_old'])
    searchData = searchData.drop(['description_old', 'description_new', 'functionId'], axis=1)
    searchData.rename(columns={'description': 'roadFunctions'}, inplace=True)
    """
    return searchData


def set_bldg_des(self, searchData):
    description = []
    typeId = []
    for bldg_Types in self.buildingTypes:
        typeId.append(bldg_Types["typeId"])
        description.append(str(bldg_Types["description"]))
    buildingTypes_dic = {'typeId': typeId, 'description': description}
    df2 = pd.DataFrame(buildingTypes_dic)
    col = searchData.shape[1]
    searchData.insert(col, 'description', '')
    searchData['description'] = ''
    searchData.rename(columns={'buildingTypeId': 'typeId'}, inplace=True)
    searchData = searchData.merge(df2, on='typeId', how='left', suffixes=('_old', '_new'))
    searchData['description'] = searchData['description_new'].combine_first(searchData['description_old'])
    searchData = searchData.drop(['description_old', 'description_new', 'typeId'], axis=1)
    searchData.rename(columns={'description': 'buildingTypes'}, inplace=True)

    description = []
    useType = []
    for bldg_useType in self.building_useType:
        useType.append(bldg_useType["useType"])
        description.append(str(bldg_useType["useName"]))
    buildingUseType_dic = {'useType': useType, 'description': description}
    df2 = pd.DataFrame(buildingUseType_dic)
    col = searchData.shape[1]
    searchData.insert(col, 'description', '')
    searchData['description'] = ''
    searchData.rename(columns={'useTypeId': 'useType'}, inplace=True)
    searchData = searchData.merge(df2, on='useType', how='left', suffixes=('_old', '_new'))
    searchData['description'] = searchData['description_new'].combine_first(searchData['description_old'])
    searchData = searchData.drop(['description_old', 'description_new', 'useType'], axis=1)
    searchData.rename(columns={'description': 'buildingUseType'}, inplace=True)

    return searchData


def retrieveAllCollection(self, dataLayer):
    if checkNetConnection() is True:
        t_status = check_token_expired(self)
        if t_status == "1":
            t_status = load_new_token(self)
        if t_status == "0":
            searchtxt = "B" + self.currentbranch + "_" + dataLayer
            url = self.baseUrl + "/api/2.0/resources/features/pwa/collections?title=" + searchtxt
            payload = {}
            headers = {
                'Authorization': 'Bearer ' + self.token_new
            }
            response = requests.request("GET", url, headers=headers, data=payload)
            if response.status_code == 200:
                numberReturned = response.json()["numberReturned"]
                if numberReturned > 0:
                    collections = response.json()["collections"]
                    return collections
                else:
                    message = "ไม่พบข้อมูลที่ต้องการ"
                    self.iface.messageBar().pushMessage("Warning  ", message, level=2, duration=3)
        else:
            message = "Can not get token from server"
            self.iface.messageBar().pushMessage("Warning  ", message, level=2, duration=3)
            return "err"
    else:
        message = "No internet connection."
        self.iface.messageBar().pushMessage("Warning  ", message, level=2, duration=3)
        return "err"


def retrieveData(self, collectionId, featureId):
    collectionId = ""
    featureId = ""
    if checkNetConnection() is True:
        t_status = check_token_expired(self)
        if t_status == "1":
            t_status = load_new_token(self)
        if t_status == "0":
            url = self.baseUrl + "/api/2.0/resources/features/pwa/collections/" + str(collectionId) + "/items/" + str(featureId)
            payload = {}
            headers = {
                'Authorization': 'Bearer ' + self.token_new
            }
            response = requests.request("GET", url, headers=headers, data=payload)
            if response.status_code == 200:
                numberReturned = response.json()["numberReturned"]
                if numberReturned > 0:
                    collections = response.json()["collections"]
                    return collections
                else:
                    message = "ไม่พบข้อมูลที่ต้องการ"
                    self.iface.messageBar().pushMessage("Warning  ", message, level=2, duration=3)
        else:
            message = "Can not get token from server"
            self.iface.messageBar().pushMessage("Warning  ", message, level=2, duration=3)
            return "err"
    else:
        message = "No internet connection."
        self.iface.messageBar().pushMessage("Warning  ", message, level=2, duration=3)
        return "err"


def loadLayerWithoutLegend(self):
    dataLayer = 'BLDG'
    collection = retrieveAllCollection(self, dataLayer)
    return collection
    # layer_path = 'D:/BLDG_test_le.shp'
    # layer = QgsVectorLayer(layer_path, 'My Layer', 'ogr')
    # QgsProject.instance().addMapLayer(layer, addToLegend=False)


### Add for retrieve PipeProject
def retrievePipeProjectForSearch(self):
    """
    Retrieve pipe project data for search functionality
    Based on the existing getPipeProject pattern but returns all projects
    """
    pwaCode = str(self.currentbranch)
    if checkNetConnection() is True:
        t_status = check_token_expired(self)
        if t_status == "1":
            t_status = load_new_token(self)
        if t_status == "0":
            # Use limit=0 to get all projects, similar to retrievePipeProject function
            url = self.baseUrl + "/api/2.0/resources/references/pipe-projects?sort=promiseDate:desc&limit=0&pwaCode=" + pwaCode
            payload = {}
            headers = {
                'Authorization': 'Bearer ' + self.token_new
            }
            response = requests.request("GET", url, headers=headers, data=payload)
            if response.status_code == 200:
                data = response.json()
                numberMatch = data['numberMatch']
                if numberMatch > 0:
                    return data["items"]
                else:
                    message = "ไม่พบข้อมูลโครงการ"
                    self.iface.messageBar().pushMessage("Warning", message, level=2, duration=3)
                    return []
            else:
                message = "Cannot retrieve pipe project data from server"
                self.iface.messageBar().pushMessage("Warning", message, level=2, duration=3)
                return "err"
        else:
            message = "Cannot get token from server"
            self.iface.messageBar().pushMessage("Warning", message, level=2, duration=3)
            return "err"
    else:
        message = "No internet connection"
        self.iface.messageBar().pushMessage("Warning", message, level=2, duration=3)
        return "err"