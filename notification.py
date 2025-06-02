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
import numpy as np


def setPage(self, numberReturned):
    if numberReturned > 0:
        # lastPage = numberReturned // 5
        lastPage = numberReturned // 10
        # pagePoint = numberReturned % 5
        pagePoint = numberReturned % 10
        # print("L : " + str(lastPage))
        # print("P : " + str(pagePoint))
        if pagePoint > 0:
            lastPage = lastPage + 1
        else:
            self.dockwidget.previousBtn.setEnabled(False)

        if lastPage > 0:
            self.dockwidget.nextBtn.setEnabled(True)
        elif lastPage == 0:
            self.dockwidget.nextBtn.setEnabled(False)

        self.dockwidget.lastPage.setText(str(lastPage))
        self.dockwidget.currentPage.setText("1")


def retrieveAllNotification(self):
    if checkNetConnection() is True:
        t_status = check_token_expired(self)
        if t_status == "1":
            t_status = load_new_token(self)
        if t_status == "0":
            url = ""
            notiFilter = self.dockwidget.notiFilterCombo.currentIndex()
            if notiFilter == 0:
                url = self.baseUrl + "/api/2.0/notifications?sort=updatedAt:desc&limit=0"
            elif notiFilter == 1:
                url = self.baseUrl + "/api/2.0/notifications?read=true&sort=updatedAt:desc&limit=0"
            elif notiFilter == 2:
                url = self.baseUrl + "/api/2.0/notifications?read=false&sort=updatedAt:desc&limit=0"
            payload = {}
            headers = {
                'Authorization': 'Bearer ' + self.token_new
            }
            response = requests.request("GET", url, headers=headers, data=payload)
            if response.status_code == 200:
                numberReturned = response.json()["numberReturned"]
                if numberReturned > 0:
                    # You have 119 unread messages
                    message = "You have " + str(numberReturned) + " message."
                    print("load new message")
                    self.iface.messageBar().pushMessage("Information  ", message, level=3, duration=3)

                    setPage(self, numberReturned)
                    notifications = response.json()["notifications"]
                    self.notifications = notifications
                    self.numberReturned = numberReturned
                    loadMessage(self)
                else:
                    message = "Can not load message from server"
                    self.iface.messageBar().pushMessage("Warning  ", message, level=2, duration=3)

            else:
                message = "Can not load message from server"
                self.iface.messageBar().pushMessage("Warning  ", message, level=2, duration=3)
        else:
            message = "Can not get token from server"
            self.iface.messageBar().pushMessage("Warning  ", message, level=2, duration=3)
    else:
        message = "No internet connection."
        self.iface.messageBar().pushMessage("Warning  ", message, level=2, duration=3)


def loadMessage(self):
    notifications = self.notifications
    print(str(len(notifications)))
    numberReturned = self.numberReturned
    notificationTableHeader(self)
    currentPage = self.dockwidget.currentPage.text()
    lasePage = self.dockwidget.lastPage.text()

    # j = int(currentPage) * 5
    j = int(currentPage) * 10
    """
    if currentPage == "1":
        # i = j - 5
        i = j - 10
    else:
        # i = j - 6
        i = j - 9
    """
    i = j - 10
    while i < j:
        if i < len(notifications):

            notificationId = notifications[i]["id"]
            topic = notifications[i]["topic"]
            notificationLevel = notifications[i]["level"]
            readStatus = notifications[i]["read"]
            createdAt = notifications[i]["createdAt"]
            createdBy = notifications[i]["createdBy"]
            updatedAt = notifications[i]["updatedAt"]
            updatedBy = notifications[i]["updatedBy"]
            try:
                detailMessage = notifications[i]["detail"]["message"]
            except:
                detailMessage = ""
            try:
                detailTitle = notifications[i]["detail"]["title"]
            except:
                detailTitle = ""
            insertRowNotification(self, readStatus, topic, createdAt, notificationId, detailTitle, detailMessage)
        else:
            i = j
        i = i + 1


def retrieveNotification(self, notificationId):
    if checkNetConnection() is True:
        t_status = check_token_expired(self)
        if t_status == "1":
            t_status = load_new_token(self)
        if t_status == "0":
            url = self.baseUrl + "/api/2.0/notifications/" + str(notificationId)
            payload = {}
            headers = {
                'Authorization': 'Bearer ' + self.token_new
            }
            response = requests.request("GET", url, headers=headers, data=payload)
            if response.status_code == 200:
                data = response.json()
                return data
            else:
                message = "Can not load message from server"
                self.iface.messageBar().pushMessage("Warning  ", message, level=2, duration=3)
        else:
            message = "Can not get token from server"
            self.iface.messageBar().pushMessage("Warning  ", message, level=2, duration=3)
    else:
        message = "No internet connection."
        self.iface.messageBar().pushMessage("Warning  ", message, level=2, duration=3)


def notificationTableHeader(self):
    notificationColumn = 6
    e_header = ["id", "topic", "date", "status", "title", "message"]
    self.dockwidget.notificationTable.setColumnCount(notificationColumn)
    self.dockwidget.notificationTable.setRowCount(0)
    self.dockwidget.notificationTable.setShowGrid(False)
    self.dockwidget.notificationTable.verticalHeader().setVisible(False)
    self.dockwidget.notificationTable.setHorizontalHeaderLabels(e_header)
    self.dockwidget.notificationTable.setColumnHidden(0, True)
    self.dockwidget.notificationTable.setColumnHidden(4, True)
    self.dockwidget.notificationTable.setColumnHidden(5, True)


def insertRowNotification(self, status, topic, date, notificationId, detailTitle, detailMessage):
    row_count = self.dockwidget.notificationTable.rowCount()
    self.dockwidget.notificationTable.insertRow(row_count)
    if status is False:
        readStatus = 'ยังไม่ได้อ่าน'
    else:
        readStatus = 'อ่านแล้ว'

    """ Set Date Time """
    """
    if len(date) == 24:
        datetime_obj = datetime.datetime.fromisoformat(str(date)[:-1])
    else:
        datetime_obj = datetime.datetime.fromisoformat(str(date))
    date_str = datetime_obj.strftime("%d/%m/%Y")
    time_str = datetime_obj.strftime("%H:%M")
    """
    self.dockwidget.notificationTable.setColumnWidth(1, 200)
    self.dockwidget.notificationTable.setColumnWidth(2, 92)
    self.dockwidget.notificationTable.setColumnWidth(3, 90)

    self.dockwidget.notificationTable.setItem(row_count, 0, QTableWidgetItem(str(notificationId)))
    self.dockwidget.notificationTable.setItem(row_count, 1, QTableWidgetItem(str(topic)))
    self.dockwidget.notificationTable.setItem(row_count, 2, QTableWidgetItem(str(date)))
    self.dockwidget.notificationTable.setItem(row_count, 3, QTableWidgetItem(str(readStatus)))
    # self.dockwidget.notificationTable.setItem(row_count, 2, QTableWidgetItem(str(date_str) + " " + str(time_str)))

    self.dockwidget.notificationTable.setItem(row_count, 4, QTableWidgetItem(str(detailTitle)))
    self.dockwidget.notificationTable.setItem(row_count, 5, QTableWidgetItem(str(detailMessage)))


def update_read(self, messageId):
    if checkNetConnection() is True:
        t_status = check_token_expired(self)
        if t_status == "1":
            t_status = load_new_token(self)
        if t_status == "0":
            url = self.baseUrl + "/api/2.0/notifications/" + messageId + "/read"
            payload = json.dumps({
                "read": True
            })
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + self.token_new
            }
            response = requests.request("PUT", url, headers=headers, data=payload)
            if response.status_code == 200:
                data = response.json()
                return data
            else:
                """
                "detail": "Body 'read' is required"
}
                """
                pass
        else:
            message = "Can not get token from server"
            self.iface.messageBar().pushMessage("Warning  ", message, level=2, duration=3)
    else:
        message = "No internet connection."
        self.iface.messageBar().pushMessage("Warning  ", message, level=2, duration=3)


def read_messageDlg(self, row):
    messageId = self.dockwidget.notificationTable.item(row, 0).text()
    readStatus = self.dockwidget.notificationTable.item(row, 3).text()
    messageTitle = self.dockwidget.notificationTable.item(row, 4).text()
    messageDetail = self.dockwidget.notificationTable.item(row, 5).text()

    # Update read status
    if readStatus == "ยังไม่ได้อ่าน":
        update_read(self, messageId)
        self.dockwidget.notificationTable.setItem(row, 3, QTableWidgetItem("อ่านแล้ว"))

    data = retrieveNotification(self, messageId)

    messageDate = data["createdAt"]
    # messageTitle = data["detail"]["title"]
    # messageDetail = data["detail"]["message"]

    self.dlg_notification.messageTitle.setText(str(messageTitle))
    self.dlg_notification.messageDetail.setPlainText(str(messageDetail))
    self.dlg_notification.messageDate.setText(str(messageDate))

    self.dlg_notification.messageTitle.setEnabled(False)
    self.dlg_notification.messageDetail.setEnabled(False)
    self.dlg_notification.messageDate.setEnabled(False)

    # Set Icon notification
    pic = "notification.png"
    picIcon = os.path.join(self.plugin_dir, "icon", pic)
    self.dlg_notification.noTi_icon.setPixmap(QPixmap(picIcon))


def openCosmeticAlert(self):
    pass

