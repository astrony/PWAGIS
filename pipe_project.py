import requests
import json
import os.path
import os
import pandas as pd
import sys
from qgis.PyQt.QtWidgets import QMessageBox
from qgis.PyQt.QtWidgets import QCompleter
from qgis.PyQt.QtCore import QStringListModel, Qt, QDateTime, QRegExp

from PyQt5.QtGui import QDoubleValidator
from pwagis.utiles import *
from datetime import datetime

def retrievePipeProject(self):
    pwaCode = str(self.currentbranch)
    if checkNetConnection() is True:
        t_status = check_token_expired(self)
        if t_status == "1":
            t_status = load_new_token(self)
        if t_status == "0":
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
                    items = data["items"]
                    self.dlg_project.listProject.clear()
                    strList = []
                    self.dlg_project.listProject.addItem("")
                    for i in range(numberMatch):
                        self.dlg_project.listProject.addItem(str(items[i]['projectNo']))
                        strList.append(str(items[i]['projectNo']))
                    autoCompleter(self, strList)
            else:
                message = "Can not get pipe project from server"
                self.iface.messageBar().pushMessage("Warning  ", message, level=2, duration=3)
                return "err"
        else:
            message = "Can not get token from server"
            self.iface.messageBar().pushMessage("Warning  ", message, level=2, duration=3)
            return "err"
    else:
        message = "No internet connection."
        self.iface.messageBar().pushMessage("Warning  ", message, level=2, duration=3)
        return "err"


def getPipeProject(self, projectNo):
    pwaCode = str(self.currentbranch)
    if checkNetConnection() is True:
        t_status = check_token_expired(self)
        if t_status == "1":
            t_status = load_new_token(self)
        if t_status == "0":
            url = self.baseUrl + "/api/2.0/resources/references/pipe-projects?sort=promiseDate:desc&limit=1&pwaCode=" + pwaCode + "&projectNo=" + str(projectNo)
            payload = {}
            headers = {
                'Authorization': 'Bearer ' + self.token_new
            }
            response = requests.request("GET", url, headers=headers, data=payload)
            if response.status_code == 200:
                data = response.json()
                numberMatch = data['numberMatch']
                if numberMatch > 0:
                    return data
                else:
                    return "notfound"
            else:
                message = "Can not get pipe project from server"
                self.iface.messageBar().pushMessage("Warning  ", message, level=2, duration=3)
                return "err"
        else:
            message = "Can not get token from server"
            self.iface.messageBar().pushMessage("Warning  ", message, level=2, duration=3)
            return "err"
    else:
        message = "No internet connection."
        self.iface.messageBar().pushMessage("Warning  ", message, level=2, duration=3)
        return "err"


def putPipeProjectDes(self, data):
    items = data["items"][0]
    projectId = str(items['id'])
    self.dlg_project.projectId.setText(projectId)
    self.dlg_project.projectNo.setText(str(items['projectNo']))
    self.dlg_project.projectName.setPlainText(str(items['projectName']))
    self.dlg_project.projectTypeCombo.setCurrentIndex(int(items['projectType']))

    key_to_check = "contractorName"
    if key_to_check in items:
        self.dlg_project.contractorName.setText(str(items['contractorName']))
    else:
        self.dlg_project.contractorName.setText("")

    key_to_check = "budget"
    if key_to_check in items:
        self.dlg_project.budget.setText(str(float(items['budget'])))
    else:
        self.dlg_project.budget.setText("")

    key_to_check = "inspectorName"
    if key_to_check in items:
        self.dlg_project.inspectorName.setText(str(items['inspectorName']))
    else:
        self.dlg_project.inspectorName.setText("")

    promiseDate = str(items['promiseDate'])
    now = setProjectDate(self, promiseDate)
    self.dlg_project.promiseDate.setDateTime(now)

    key_to_check = "checkDate"
    if key_to_check in items:

        checkDate = str(items['checkDate'])
        try:
            if checkDate != "" or len(checkDate) > 0:
                now = setProjectDate(self, checkDate)
                self.dlg_project.checkDate.setDateTime(now)
        except ValueError as e:
            print(f'Value in valid date: {e}')
            self.dlg_project.checkDate.setDateTime(QDateTime())

    key_to_check = "remark"
    if key_to_check in items:
        self.dlg_project.remark.setText(str(items['remark']))
    else:
        self.dlg_project.remark.setText("")


def addProjectType(self):
    self.dlg_project.projectTypeCombo.clear()
    projectType = ["โปรดเลือก...", "งานปรับปรุงเส้นท่อ", "งานขยายเขตจำหน่ายน้ำ", "งานติดตั้งและวางท่อประปา", "บริจาคเป็นเงินเต็มจำนวน", "บริจาคโดยผู้ใช้น้ำดำเนินการเอง", "บริจาคเป็นเงินบางส่วน", "รับโอน", "หน่วยงานราชการท้องถิ่นใหยืม", "อื่นๆ"]
    self.dlg_project.projectTypeCombo.addItems(projectType)


def autoCompleter(self, strList):
    completer = QCompleter()
    completer.setCaseSensitivity(0)
    # self.dlg_project.lineCompleter.setCompleter(completer)
    self.dlg_project.listProject.setCompleter(completer)
    model = QStringListModel()
    model.setStringList(strList)
    completer.setFilterMode(Qt.MatchContains)
    completer.setModel(model)


def setProjectDate(self, date_string):
    try:
        datetime_string = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%SZ")  # .%fZ
    except:
        datetime_string = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%fZ")  # .%fZ

    dt_with_timezone = datetime.fromisoformat(str(datetime_string))
    # Convert to desired format
    t_yr = dt_with_timezone.strftime("%Y")
    t_mo = dt_with_timezone.strftime("%m")
    t_da = dt_with_timezone.strftime("%d")
    t_hr = dt_with_timezone.strftime("%H")
    t_mi = dt_with_timezone.strftime("%M")

    # now = QDateTime(int(t_yr)+543, int(t_mo), int(t_da), int(t_hr), int(t_mi))
    now = QDateTime(int(t_yr), int(t_mo), int(t_da), int(t_hr), int(t_mi))
    return now


def resetForm(self):
    self.dlg_project.projectNo.setText("")
    self.dlg_project.projectTypeCombo.setCurrentIndex(0)
    self.dlg_project.projectName.setPlainText("")
    self.dlg_project.contractorName.setText("")
    self.dlg_project.budget.setText("1.0")
    
   # Set validator for floating-point numbers
    validator = QDoubleValidator(1.0, 9999999.99, 2)  # Min, Max, Decimals
    validator.setNotation(QDoubleValidator.StandardNotation)  # Allow standard float notation
    self.dlg_project.budget.setValidator(validator)

    self.dlg_project.inspectorName.setText("")
    self.dlg_project.remark.setText("")

    current_dateTime = datetime.now()
    dt_with_timezone = datetime.fromisoformat(str(current_dateTime)).replace(microsecond=0)
    a = str(dt_with_timezone)
    x = a.split()
    o = x[0] + "T" + x[1] + "Z"
    now = setProjectDate(self, o)
    self.dlg_project.promiseDate.setDateTime(now)
    self.dlg_project.checkDate.setDateTime(QDateTime())
    # self.dlg_project.checkDate.setText("")
    self.dlg_project.projectId.setText("")
    
def createProjectJson(self):
    projectNo = self.dlg_project.projectNo.text()
    ppJson = dict(projectNo=str(projectNo))
    projectType = self.dlg_project.projectTypeCombo.currentIndex()
    ppJson = dict(ppJson, projectType=int(projectType))
    promiseDate = convertDate(str(self.dlg_project.promiseDate.text()))
    ppJson = dict(ppJson, promiseDate=str(promiseDate))
    projectName = self.dlg_project.projectName.toPlainText()
    ppJson = dict(ppJson, projectName=str(projectName))
    contractorName = self.dlg_project.contractorName.text()
    ppJson = dict(ppJson, contractorName=str(contractorName))
    budget = self.dlg_project.budget.text()
    ppJson = dict(ppJson, budget=float(budget))
    checkDate = convertDate(str(self.dlg_project.checkDate.text()))
    if checkDate != "":  
        ppJson = dict(ppJson, checkDate=str(checkDate))
    inspectorName = self.dlg_project.inspectorName.text()
    ppJson = dict(ppJson, inspectorName=inspectorName)
    remark = self.dlg_project.remark.text()
    ppJson = dict(ppJson, remark=str(remark))
    pwaCode = str(self.currentbranch)
    ppJson = dict(ppJson, pwaCode=str(pwaCode))
    ppJson = json.dumps(ppJson)
    return ppJson

def convertDate(raw_date):
    try:
        # input_date = datetime.strptime(raw_date, "%m/%d/%Y")
        input_date = datetime.strptime(raw_date, "%d/%m/%Y")
        output_date_iso = input_date.isoformat() + "Z"
        return output_date_iso
    except ValueError as e:
        output_date_iso = ""
        return output_date_iso  

def saveNewPipeProject(self, ppJson):
    print(ppJson)
    if checkNetConnection() is True:
        t_status = check_token_expired(self)
        if t_status == "1":
            t_status = load_new_token(self)
        if t_status == "0":
            url = self.baseUrl + "/api/2.0/resources/references/pipe-projects"

            payload = ppJson
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + self.token_new
            }

            response = requests.request("POST", url, headers=headers, data=payload)
            print(str(response.status_code))
            if response.status_code == 201:
                message = "Add new pipe project success"
                self.iface.messageBar().pushMessage("Information  ", message, level=3, duration=3)
            else:
                message = "Add new pipe project not success"
                self.iface.messageBar().pushMessage("Warning  ", message, level=2, duration=3)
        else:
            message = "Can not get token from server"
            self.iface.messageBar().pushMessage("Warning  ", message, level=2, duration=3)
            return "err"
    else:
        message = "No internet connection."
        self.iface.messageBar().pushMessage("Warning  ", message, level=2, duration=3)
        return "err"


def delPipeProject(self, pipeProjectId):
    if checkNetConnection() is True:
        t_status = check_token_expired(self)
        if t_status == "1":
            t_status = load_new_token(self)
        if t_status == "0":
            url = self.baseUrl + "/api/2.0/resources/references/pipe-projects/" + str(pipeProjectId)

            payload = {}
            headers = {
                'Authorization': 'Bearer ' + self.token_new
            }

            response = requests.request("DELETE", url, headers=headers, data=payload)
            if response.status_code == 204:
                result = "deleteSuccess"
                message = "Delete  pipe project success"
                self.iface.messageBar().pushMessage("Information  ", message, level=3, duration=3)
            else:
                result = "deleteNotSuccess"
                message = "Deleter pipe project not success"
                self.iface.messageBar().pushMessage("Warning  ", message, level=2, duration=3)
            return result
        else:
            message = "Can not get token from server"
            self.iface.messageBar().pushMessage("Warning  ", message, level=2, duration=3)
            return "err"
    else:
        message = "No internet connection."
        self.iface.messageBar().pushMessage("Warning  ", message, level=2, duration=3)
        return "err"


def update_PipeProject(self, pipeProjectId,  ppJson):
    if checkNetConnection() is True:
        t_status = check_token_expired(self)
        if t_status == "1":
            t_status = load_new_token(self)
        if t_status == "0":
            url = self.baseUrl + "/api/2.0/resources/references/pipe-projects/" + str(pipeProjectId)
            payload = ppJson
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + self.token_new
            }
            response = requests.request("PUT", url, headers=headers, data=payload)
            if response.status_code == 200:
                result = "updateSuccess"
                message = "Update pipe project success"
                self.iface.messageBar().pushMessage("Information  ", message, level=3, duration=3)
            else:
                result = "updateNotSuccess"
                message = "Update pipe project not success"
                self.iface.messageBar().pushMessage("Warning  ", message, level=2, duration=3)
            return result
        else:
            message = "Can not get token from server"
            self.iface.messageBar().pushMessage("Warning  ", message, level=2, duration=3)
            return "err"
    else:
        message = "No internet connection."
        self.iface.messageBar().pushMessage("Warning  ", message, level=2, duration=3)
        return "err"

def validateFormPipeProject(self):
    # "NULL" or length.text() == "" or len(str(length.text())) == 0:
    validateResult = False
    projectNo = self.dlg_project.projectNo.text()
    projectType = self.dlg_project.projectTypeCombo.currentIndex()
    projectName = self.dlg_project.projectName.toPlainText()
    contractorName = self.dlg_project.contractorName.text()
    budget = self.dlg_project.budget.text()
    inspectorName = self.dlg_project.inspectorName.text()
    
    if projectNo == "NULL" or projectNo == "" or len(str(projectNo)) == 0:
        return validateResult
    elif projectType == 0:
        return validateResult
    elif projectName == "NULL" or projectName == "" or len(str(projectName)) == 0:
        return validateResult
    elif contractorName == "NULL" or contractorName == "" or len(str(contractorName)) == 0:
        return validateResult
    elif budget == "NULL" or budget == "" or len(str(budget)) == 0 or float(budget) <= 0:
        return validateResult
    elif inspectorName == "NULL" or inspectorName == "" or len(str(inspectorName)) == 0:
        return validateResult
    else:
        validateResult = True
        return validateResult
