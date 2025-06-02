# import subprocess
# import webbrowser
# import requests
# import json
# import os.path
# import os
# import pandas as pd
# import sys
# from qgis.PyQt.QtWidgets import QMessageBox
# from qgis.PyQt.QtWidgets import QCompleter
# from qgis.PyQt.QtCore import QStringListModel, Qt, QDateTime, QRegExp
# from qgis.PyQt.QtGui import QIntValidator
# from pwagis.pipe_project import *


# def addReportType(self):
#     self.dockwidget.report_id_select.clear()
#     reportType = ["รายงานสินทรัพย์ถาวร", "รายงานผู้ใช้น้ำเพิ่มจากการขยายเขต", "รายงานปริมาณท่อแยกตามขนาด", "รายงานปริมาณท่อแยกตามชนิดและขนาด", "รายงานผลการปฏิบัติงานประจำเดือน", "รายงานผลการปฏิบัติงานประจำไตรมาส", "รายงานการนำเข้าข้อมูลผู้ใช้น้ำ", "รายงานผู้ใช้น้ำที่ยังไม่ได้นำเข้า"]
#     for i in range(len(reportType)):
#         self.dockwidget.report_id_select.addItem(reportType[i])


# def createReport(self, actionType):
#     report_link = ""
#     report_type = self.dockwidget.report_id_select.currentIndex()
#     errCode = ""
#     report_id = 0   # รายงานสินทรัพย์ถาวร
#     if report_type == 1:
#        report_id = 2    # รายงานผู้ใช้น้ำเพิ่มจากการขยายเขต
#        # Check Year
#        if self.dockwidget.report_year_select_3.currentIndex() == 0:
#            errCode = "err"
#     elif report_type == 2:
#        report_id = 3    # รายงานปริมาณท่อแยกตามขนาด
#     elif report_type == 3:
#        report_id = 4    # รายงานปริมาณท่อแยกตามชนิดและขนาด
#     elif report_type == 4:
#         report_id = 5   # รายงานผลการปฏิบัติงานประจำเดือน
#         # Check Year
#         if self.dockwidget.report_year_select.currentIndex() == 0:
#             errCode = "err"
#     elif report_type == 5:
#         report_id = 6   # รายงานผลการปฏิบัติงานประจำไตรมาส
#         # Check Year
#         if self.dockwidget.report_year_select_2.currentIndex() == 0:
#             errCode = "err"
#     elif report_type == 6:
#         report_id = 1   # รายงานการนำเข้าข้อมูลผู้ใช้น้ำ
#         # Check Year
#         if self.dockwidget.report_year_select.currentIndex() == 0:
#             errCode = "err"
#     elif report_type == 7:
#         report_id = 8   # รายงานผู้ใช้น้ำที่ยังไม่ได้นำเข้า

#     report_server = "https://gisapp.pwa.co.th"

#     if actionType == "download":
#         downloadReport = "&download=true"
#     else:
#         downloadReport = ""

#     if report_id == 0:
#         projectNo = self.dockwidget.report_contractNumber.currentText()
#         result = getPipeProject(self, projectNo)
#         if result == "notfound":
#             projectId = ""
#         else:
#             items = result["items"][0]
#             projectId = str(items['id'])
#             self.dockwidget.projectId.setText(str(projectId))
#         report_link = report_server + "/p/report?access_token=" + self.token_new + "&report_id=" + str(
#             report_id) + "&id=" + str(projectId) + "&pwaCode=" + str(self.currentbranch) + downloadReport
#     elif report_id == 2 and errCode == "":
#         report_year = str(int(self.dockwidget.report_year_select_3.currentText()) - 543)
#         report_month = "1"
#         report_link = report_server + "/p/report?access_token=" + self.token_new + "&report_id=" + str(
#             report_id) + "&year=" + report_year + "&month=" + report_month + "&pwaCode=" + str(self.currentbranch) + downloadReport
#     elif (report_id == 1 or report_id == 5) and errCode == "":
#         report_year = str(int(self.dockwidget.report_year_select.currentText()) - 543)
#         report_month = str(self.dockwidget.report_month_select.currentIndex() + 1)
#         report_link = report_server + "/p/report?access_token=" + self.token_new + "&report_id=" + str(report_id) + "&year=" + report_year + "&month=" + report_month + "&pwaCode=" + str(self.currentbranch) + downloadReport
#     elif report_id == 3 or report_id == 4 or report_id == 8:
#         report_link = report_server + "/p/report?access_token=" + self.token_new + "&report_id=" + str(report_id) + "&pwaCode=" + str(self.currentbranch) + downloadReport
#     elif report_id == 6 and errCode == "":
#         reportQuater = str(self.dockwidget.reportQuater.currentIndex() + 1)
#         report_year = str(int(self.dockwidget.report_year_select_2.currentText()) - 543)
#         report_month = "1"
#         report_link = report_server + "/p/report?access_token=" + self.token_new + "&report_id=" + str(report_id) + "&year=" + report_year + "&month=" + report_month + "&quater=" + reportQuater + "&pwaCode=" + str(self.currentbranch) + downloadReport
#     if report_link != "" and errCode == "":
#         webbrowser.open_new(report_link)
#     elif report_link == "":
#         printMessage = "รายงานยังไม่พร้อมใช้งาน"
#         if errCode != "" :
#             printMessage = "โปรดเลือกปี"
#         alertMsgBox(printMessage)


# def retrievePipeProject_report(self):
#     pwaCode = str(self.currentbranch)
#     if checkNetConnection() is True:
#         t_status = check_token_expired(self)
#         if t_status == "1":
#             t_status = load_new_token(self)
#         if t_status == "0":
#             url = self.baseUrl + "/api/2.0/resources/references/pipe-projects?limit=0&pwaCode=" + pwaCode
#             payload = {}
#             headers = {
#                 'Authorization': 'Bearer ' + self.token_new
#             }
#             response = requests.request("GET", url, headers=headers, data=payload)
#             if response.status_code == 200:
#                 data = response.json()
#                 numberMatch = data['numberMatch']
#                 if numberMatch > 0:
#                     items = data["items"]
#                     self.dockwidget.report_contractNumber.clear()
#                     strList = []
#                     self.dockwidget.report_contractNumber.addItem("")
#                     for i in range(numberMatch):
#                         self.dockwidget.report_contractNumber.addItem(str(items[i]['projectNo']))
#                         strList.append(str(items[i]['projectNo']))
#                     autoCompleter_report(self, strList)
#             else:
#                 message = "Can not get pipe project from server"
#                 self.iface.messageBar().pushMessage("Warning  ", message, level=2, duration=3)
#                 return "err"
#         else:
#             message = "Can not get token from server"
#             self.iface.messageBar().pushMessage("Warning  ", message, level=2, duration=3)
#             return "err"
#     else:
#         message = "No internet connection."
#         self.iface.messageBar().pushMessage("Warning  ", message, level=2, duration=3)
#         return "err"


# def autoCompleter_report(self, strList):
#     completer = QCompleter()
#     completer.setCaseSensitivity(0)
#     self.dockwidget.report_contractNumber.setCompleter(completer)
#     model = QStringListModel()
#     model.setStringList(strList)
#     completer.setFilterMode(Qt.MatchContains)
#     completer.setModel(model)



#### Review and Modify support new report #########
import subprocess
import webbrowser
import requests
import json
import os.path
import os
import pandas as pd
import sys
from qgis.PyQt.QtWidgets import QMessageBox
from qgis.PyQt.QtWidgets import QCompleter
from qgis.PyQt.QtCore import QStringListModel, Qt, QDateTime, QRegExp
from qgis.PyQt.QtGui import QIntValidator
from pwagis.pipe_project import *


def addReportType(self):
    """
    Initialize and populate the report type selection dropdown with all available reports.
    This function supports 10 different report types including the newly added monthly
    unimported water users report and unclosed projects report.
    """
    self.dockwidget.report_id_select.clear()
    reportType = [
        "รายงานสินทรัพย์ถาวร",  # 1 Fixed Assets Report
        "รายงานผู้ใช้น้ำเพิ่มจากการขยายเขต",  # 2 New Water Users from Area Expansion Report
        "รายงานปริมาณท่อแยกตามขนาด",  # 3 Pipe Volume by Size Report
        "รายงานปริมาณท่อแยกตามชนิดและขนาด",  # 4 Pipe Volume by Type and Size Report
        "รายงานผลการปฏิบัติงานประจำเดือน",  # 5 Monthly Performance Report
        "รายงานผลการปฏิบัติงานประจำไตรมาส",  # 6 Quarterly Performance Report
        "รายงานการนำเข้าข้อมูลผู้ใช้น้ำ",  # 7 Water User Data Import Report
        "รายงานผู้ใช้น้ำที่ยังไม่ได้นำเข้า",  # 8 Unimported Water Users Report
        "รายงานผู้ใช้น้ำที่ยังไม่ได้นำเข้ารายเดือน",  # 9 Monthly Unimported Water Users Report (NEW)
        "รายงานโครงการที่ยังไม่ได้ปิด"  # 10 Unclosed Projects Report (NEW)
    ]
    for i in range(len(reportType)):
        self.dockwidget.report_id_select.addItem(reportType[i])


def createReport(self, actionType):
    """
    Generate and open the selected report based on the report type and parameters.
    This function handles 10 different report types with their specific parameter requirements.
    
    Args:
        actionType (str): Either "download" or "view" to determine report display method
        
    The function maps report selection indices to server report IDs and constructs
    appropriate URL parameters based on the report requirements.
    """
    report_link = ""
    report_type = self.dockwidget.report_id_select.currentIndex()
    errCode = ""
    report_id = 0   # Default: รายงานสินทรัพย์ถาวร (Fixed Assets Report)
    
    # Map report selection to server report IDs and handle parameter validation
    if report_type == 1:
        report_id = 2    # รายงานผู้ใช้น้ำเพิ่มจากการขยายเขต
        # Validate year parameter requirement
        if self.dockwidget.report_year_select_3.currentIndex() == 0:
            errCode = "err"
    elif report_type == 2:
        report_id = 3    # รายงานปริมาณท่อแยกตามขนาด
    elif report_type == 3:
        report_id = 4    # รายงานปริมาณท่อแยกตามชนิดและขนาด
    elif report_type == 4:
        report_id = 5    # รายงานผลการปฏิบัติงานประจำเดือน
        # Validate year parameter requirement
        if self.dockwidget.report_year_select.currentIndex() == 0:
            errCode = "err"
    elif report_type == 5:
        report_id = 6    # รายงานผลการปฏิบัติงานประจำไตรมาส
        # Validate year parameter requirement
        if self.dockwidget.report_year_select_2.currentIndex() == 0:
            errCode = "err"
    elif report_type == 6:
        report_id = 1    # รายงานการนำเข้าข้อมูลผู้ใช้น้ำ
        # Validate year parameter requirement
        if self.dockwidget.report_year_select.currentIndex() == 0:
            errCode = "err"
    elif report_type == 7:
        report_id = 8    # รายงานผู้ใช้น้ำที่ยังไม่ได้นำเข้า
    elif report_type == 8:
        report_id = 12    # รายงานผู้ใช้น้ำที่ยังไม่ได้นำเข้ารายเดือน (NEW)
        # Validate year and month parameter requirements for monthly report
        if self.dockwidget.report_year_select.currentIndex() == 0:
            errCode = "err"
    elif report_type == 9:
        report_id = 11   # รายงานโครงการที่ยังไม่ได้ปิด (NEW)
        # Validate year parameter requirement for unclosed projects report
        if self.dockwidget.report_year_select_3.currentIndex() == 0:
            errCode = "err"

    report_server = "https://gisapp.pwa.co.th"

    # Determine download parameter based on action type
    if actionType == "download":
        downloadReport = "&download=true"
    else:
        downloadReport = ""

    # Construct report URLs based on report type and parameters
    if report_id == 0:
        # Fixed Assets Report - requires project selection
        projectNo = self.dockwidget.report_contractNumber.currentText()
        result = getPipeProject(self, projectNo)
        if result == "notfound":
            projectId = ""
        else:
            items = result["items"][0]
            projectId = str(items['id'])
            self.dockwidget.projectId.setText(str(projectId))
        report_link = report_server + "/p/report?access_token=" + self.token_new + "&report_id=" + str(
            report_id) + "&id=" + str(projectId) + "&pwaCode=" + str(self.currentbranch) + downloadReport
             
    elif report_id == 3 or report_id == 4 or report_id == 8:
        # Reports without time parameters
        report_link = report_server + "/p/report?access_token=" + self.token_new + "&report_id=" + str(
            report_id) + "&pwaCode=" + str(self.currentbranch) + downloadReport
                       
    elif (report_id == 2 or report_id == 11) and errCode == "":
        # Area Expansion Report - requires year parameter
        report_year = str(int(self.dockwidget.report_year_select_3.currentText()) - 543)
        report_link = report_server + "/p/report?access_token=" + self.token_new + "&report_id=" + str(
        report_id) + "&year=" + report_year + "&pwaCode=" + str(self.currentbranch) + downloadReport
            
    elif (report_id == 1 or report_id == 5 or report_id == 12) and errCode == "":
        # Monthly reports - require year and month parameters
        report_year = str(int(self.dockwidget.report_year_select.currentText()) - 543)
        report_month = str(self.dockwidget.report_month_select.currentIndex() + 1)
        report_link = report_server + "/p/report?access_token=" + self.token_new + "&report_id=" + str(
            report_id) + "&year=" + report_year + "&month=" + report_month + "&pwaCode=" + str(self.currentbranch) + downloadReport

    elif report_id == 6 and errCode == "":
        # Quarterly Performance Report - requires year and quarter parameters
        reportQuater = str(self.dockwidget.reportQuater.currentIndex() + 1)
        report_year = str(int(self.dockwidget.report_year_select_2.currentText()) - 543)
        report_month = "1"
        report_link = report_server + "/p/report?access_token=" + self.token_new + "&report_id=" + str(
            report_id) + "&year=" + report_year + "&month=" + report_month + "&quater=" + reportQuater + "&pwaCode=" + str(self.currentbranch) + downloadReport
        

    # Open report or display error message
    if report_link != "" and errCode == "":
        webbrowser.open_new(report_link)
    elif report_link == "":
        printMessage = "รายงานยังไม่พร้อมใช้งาน"
        if errCode != "":
            printMessage = _getParameterErrorMessage(report_type)
        alertMsgBox(printMessage)


def _getParameterErrorMessage(report_type):
    """
    Get appropriate error message based on missing parameters for each report type.
    
    Args:
        report_type (int): The index of the selected report type
        
    Returns:
        str: Localized error message indicating which parameters are missing
    """
    if report_type in [1, 5, 9]:  # Reports requiring year parameter
        return "โปรดเลือก ปี เพื่อออกรายงานได้อย่างถูกต้อง"
    elif report_type in [4, 6, 8]:  # Reports requiring year and month parameters
        return "โปรดเลือก เดือนและปี เพื่อออกรายงานได้อย่างถูกต้อง"
    elif report_type == 5:  # Quarterly report requiring year and quarter
        return "โปรดเลือก ไตรมาสและปี  เพื่อออกรายงานได้อย่างถูกต้อง"
    else:
        return "โปรดระบุพารามิเตอร์ที่จำเป็น"


def retrievePipeProject_report(self):
    """
    Retrieve pipe project data from the server for use in project-based reports.
    This function populates the project selection dropdown and sets up autocomplete
    functionality for project number selection.
    
    The function makes an API call to fetch all pipe projects for the current branch
    and populates the report interface with available project options.
    """
    pwaCode = str(self.currentbranch)
    if checkNetConnection() is True:
        t_status = check_token_expired(self)
        if t_status == "1":
            t_status = load_new_token(self)
        if t_status == "0":
            url = self.baseUrl + "/api/2.0/resources/references/pipe-projects?limit=0&pwaCode=" + pwaCode
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
                    self.dockwidget.report_contractNumber.clear()
                    strList = []
                    self.dockwidget.report_contractNumber.addItem("")
                    for i in range(numberMatch):
                        self.dockwidget.report_contractNumber.addItem(str(items[i]['projectNo']))
                        strList.append(str(items[i]['projectNo']))
                    autoCompleter_report(self, strList)
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


def autoCompleter_report(self, strList):
    """
    Set up autocomplete functionality for the project number selection dropdown.
    This enhances user experience by providing type-ahead functionality when
    selecting from available pipe projects.
    
    Args:
        strList (list): List of project numbers to enable autocomplete for
    """
    completer = QCompleter()
    completer.setCaseSensitivity(0)
    self.dockwidget.report_contractNumber.setCompleter(completer)
    model = QStringListModel()
    model.setStringList(strList)
    completer.setFilterMode(Qt.MatchContains)
    completer.setModel(model)


def validateReportParameters(self, report_type):
    """
    Validate that all required parameters are selected for the given report type.
    This function ensures data integrity and prevents generation of incomplete reports.
    
    Args:
        report_type (int): The index of the selected report type
        
    Returns:
        bool: True if all required parameters are provided, False otherwise
        
    This validation function supports the parameter requirements for all 10 report types:
    - Reports 0, 2, 3, 7: No additional parameters required
    - Reports 1, 9: Year parameter required
    - Reports 4, 6, 8: Year and month parameters required  
    - Report 5: Year and quarter parameters required
    """
    if report_type in [1, 9]:  # Year only reports
        return self.dockwidget.report_year_select_3.currentIndex() > 0
    elif report_type in [4, 6, 8]:  # Year and month reports
        return (self.dockwidget.report_year_select.currentIndex() > 0 and 
                self.dockwidget.report_month_select.currentIndex() > 0)
    elif report_type == 5:  # Quarterly report
        return (self.dockwidget.report_year_select_2.currentIndex() > 0 and
                self.dockwidget.reportQuater.currentIndex() >= 0)
    else:  # Reports with no additional parameters or project-based reports
        return True


def getReportMetadata(self, report_id):
    """
    Retrieve metadata information for a specific report from the server.
    This function can be used to validate report availability and get additional
    report configuration details.
    
    Args:
        report_id (int): Server-side report identifier
        
    Returns:
        dict: Report metadata including title, parameters, and availability status
    """
    if checkNetConnection() is True:
        t_status = check_token_expired(self)
        if t_status == "1":
            t_status = load_new_token(self)
        if t_status == "0":
            url = self.baseUrl + "/api/2.0/resources/reports/" + str(report_id) + "/metadata"
            headers = {
                'Authorization': 'Bearer ' + self.token_new
            }
            response = requests.request("GET", url, headers=headers)
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": "Report metadata not available"}
        else:
            return {"error": "Authentication failed"}
    else:
        return {"error": "No internet connection"}