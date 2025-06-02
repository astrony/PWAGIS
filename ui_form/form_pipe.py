from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtWidgets import QWidget, QVBoxLayout, QPushButton, QDialogButtonBox, QLineEdit, QMessageBox, QComboBox, \
    QGroupBox, QApplication, QLabel, QCompleter, QPlainTextEdit, QDialog
from pwagis.utiles import *
import os
import os.path
import json
import configparser
import requests
from pwagis.get_plugin_path import current_path
import random
from ulid import ULID
from qgis.utils import iface
from qgis.core import QgsProject, QgsFeature, QgsGeometry
from qgis.gui import QgsMapToolCapture
from datetime import datetime


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

    global pipetypeId
    global pipetype_id
    global pipetype_text

    global productId
    global product_id
    global product_text

    global typeId
    global type_id
    global type_text

    global functionId
    global function_id
    global function_text

    global layingId
    global laying_id
    global laying_text

    global classId
    global class_id
    global class_text

    global gradeId
    global grade_id
    global grade_text

    global sizeId
    global size_text
    global size_Id

    global depth_combo

    global token_new
    global plugin_dir
    global reference
    global pwaCode
    global baseUrl

    global groupBox

    global _temp_id
    global pipeId
    global selectedId

    global projectNo_combo
    global projectNo
    global projectNoList

    global projectName
    global projectNameCombo

    global myDialog
    myDialog = dialog
    global nameField

    global depth
    global length
    global locate
    global assetCode

    global remark

    global yearInstall
    global yearInstall_text

    """ Button """
    global okBtn
    global cancelBtn

    nameField = dialog.findChild(QLineEdit, "Name")
    plugin_dir = current_path()

    groupBox = myDialog.findChild(QGroupBox, "groupBox")
    groupBox.setVisible(0)  # 1 is visible = True

    validator = QRegExpValidator(QRegExp("([-]{0,1})([0-9]{0,9})([.]{0,1}[0-9]{0,7})"))
    depth = myDialog.findChild(QLineEdit, "depth")
    depth.setValidator(validator)

    length = myDialog.findChild(QLineEdit, "length")

    locate = myDialog.findChild(QLineEdit, "locate")

    assetCode = myDialog.findChild(QLineEdit, "assetCode")

    pipeId = myDialog.findChild(QLineEdit, "pipeId")
    pipeId.setEnabled(1)
    pipeId.setVisible(False)
    label_pipeId = myDialog.findChild(QLabel, "label_pipeId")
    label_pipeId.setVisible(False)

    temp_random = random.randint(100000, 9000000)

    # Get config from config.ini
    config = configparser.ConfigParser()
    configpath = os.path.join(plugin_dir, 'config.ini')
    config.read(configpath)
    token_new = config.get('settings', 'token_new')
    pwaCode = config.get('settings', 'currentbranch')
    baseUrl = config.get('settings', 'baseUrl')

    """ Load JSON REFERENCE """
    json_file = "referances.json"
    json_path = os.path.join(plugin_dir, "json", json_file)
    with open(json_path, 'r', encoding='utf-8') as openfile:
        reference = json.load(openfile)

    """ Project Name """
    projectName = myDialog.findChild(QPlainTextEdit, "projectName")
    projectNameCombo = myDialog.findChild(QComboBox, "projectNameCombo")

    """ projectNo"""
    projectNo = myDialog.findChild(QLineEdit, "projectNo")
    projectNo_combo = myDialog.findChild(QComboBox, "projectNo_combo")

    """ pipe Type"""
    pipetypeId = myDialog.findChild(QLineEdit, "typeId")
    pipetype_id = myDialog.findChild(QComboBox, "type_id")
    pipetype_text = myDialog.findChild(QComboBox, "type_text")

    """ Pipe Product """
    productId = myDialog.findChild(QLineEdit, "productId")
    product_id = myDialog.findChild(QComboBox, "product_id")
    product_text = myDialog.findChild(QComboBox, "product_text")

    """ pipe Function """
    functionId = myDialog.findChild(QLineEdit, "functionId")
    function_id = myDialog.findChild(QComboBox, "function_id")
    function_text = myDialog.findChild(QComboBox, "function_text")

    """ Pipe Laying """
    layingId = myDialog.findChild(QLineEdit, "layingId")
    laying_id = myDialog.findChild(QComboBox, "laying_id")
    laying_text = myDialog.findChild(QComboBox, "laying_text")

    """ Pipe Class """
    classId = myDialog.findChild(QLineEdit, "classId")
    class_id = myDialog.findChild(QComboBox, "class_id")
    class_text = myDialog.findChild(QComboBox, "class_text")

    """ Pipe Grade """
    gradeId = myDialog.findChild(QLineEdit, "gradeId")
    grade_id = myDialog.findChild(QComboBox, "grade_id")
    grade_text = myDialog.findChild(QComboBox, "grade_text")

    """ Pipe Size """
    sizeId = myDialog.findChild(QLineEdit, "sizeId")
    size_Id = myDialog.findChild(QComboBox, "size_Id")
    size_text = myDialog.findChild(QComboBox, "size_text")
    depth_combo = myDialog.findChild(QComboBox, "depth_combo")

    """ yearInstall """
    yearInstall_text = myDialog.findChild(QComboBox, "yearInstall_text")
    yearInstall = myDialog.findChild(QLineEdit, "yearInstall")

    """ remark """
    remark = myDialog.findChild(QLineEdit, "remark")

    """ Temp """
    _temp_id = myDialog.findChild(QLineEdit, "_temp_id")
    if _temp_id.text() == 'NULL' or _temp_id.text() == '':
        _temp_id.setText(str(temp_random))

    """ GlobalId """
    globalId = myDialog.findChild(QLineEdit, "globalId")
    tempGlobalId = str(ULID())
    if globalId.text() == 'NULL' or globalId.text() == '':
        globalId.setText(str(tempGlobalId))

    """ id """
    selectedId = myDialog.findChild(QLineEdit, "id")

    """ New Btn """
    myDialog.hideButtonBox()
    okBtn = myDialog.findChild(QPushButton, "okBtn")
    cancelBtn = myDialog.findChild(QPushButton, "cancelBtn")

    okBtn.clicked.connect(okBtnSubmit)
    cancelBtn.clicked.connect(closeDialog)

    load_PipeType()
    load_PipeSize()
    load_PipeProduct()
    load_PipeFunction()
    load_PipeLaying()
    load_PipeClass()
    load_PipeGrade()
    load_PipeProject()
    load_YearInstall()

    # Get PIPE Length
    getPipeLength(featureid)
    # projectNo_change()

    pipetype_text.currentIndexChanged.connect(pipeType_change)
    size_text.currentIndexChanged.connect(pipeSize_change)
    class_text.currentTextChanged.connect(pipeClass_change)
    projectNo_combo.currentTextChanged.connect(projectNo_change)
    product_text.currentTextChanged.connect(pipeProduct_change)
    function_text.currentTextChanged.connect(pipeFunction_change)
    laying_text.currentTextChanged.connect(pipeLaying_change)
    grade_text.currentTextChanged.connect(pipeGrade_change)
    projectNo_combo.currentTextChanged.connect(projectNo_change)
    yearInstall_text.currentTextChanged.connect(yearInstall_change)

    if pipetypeId.text() == "HDPE":
        grade_text.setEnabled(1)
    else:
        grade_text.setEnabled(0)

def setValue():
    tempTypeId = str(pipetype_id.currentText())
    pipetypeId.setText(tempTypeId)

    tempClassId = str(class_id.currentText())
    classId.setText(tempClassId)

    tempFunctionId = str(function_id.currentText())
    functionId.setText(tempFunctionId)

    tempLayingId = str(laying_id.currentText())
    layingId.setText(tempLayingId)

    tempSizeId = str(size_Id.currentText())
    sizeId.setText(tempSizeId)

    tempGradeId = str(grade_id.currentText())
    gradeId.setText(tempGradeId)

    tempProjectNoId = str(projectNo_combo.currentText())
    projectNo.setText(tempProjectNoId)

    tempProductId = str(product_id.currentText())
    productId.setText(tempProductId)


def okBtnSubmit():
    setValue()
    depthStatus = depthCheck()
    projectStatus = projectCheck()

    if depthStatus is False and projectStatus is True:
        msg = QMessageBox()
        msg.setText("ความลึกของท่อประปาต้องมากกว่าศูนย์")
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("PWA Message")
        msg.setStandardButtons(QMessageBox.Ok)
        retval = msg.exec_()
    elif depthStatus is True and projectStatus is False:
        msg = QMessageBox()
        msg.setText("เลขที่สัญญาโครงการไม่สามารเว้นว่างได้")
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("PWA Message")
        msg.setStandardButtons(QMessageBox.Ok)
        retval = msg.exec_()
    elif depthStatus is False and projectStatus is False:
        msg = QMessageBox()
        msg.setText("ความลึกของท่อประปาต้องมากกว่าศูนย์ และ เลขที่สัญญาโครงการไม่สามารเว้นว่างได้")
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("PWA Message")
        msg.setStandardButtons(QMessageBox.Ok)
        retval = msg.exec_()
    else:
        myDialog.save()
        closeDialog()


def load_PipeProduct():
    productList = []
    pipeProducts = reference["referances"]["pipe"]["pipeProducts"]
    for i in range(len(pipeProducts)):
        product_id.addItem(str(pipeProducts[i]["productId"]))
        productList.append(str(pipeProducts[i]["productId"]))
        product_text.addItem(str(pipeProducts[i]["description"]))

    """ Add Other for not in DataDic """
    product_text.addItem("โปรดเลือกชื่อผลิตภัณฑ์ท่อ")
    product_id.addItem("Other")

    if productId.text() not in productList:
        product_text.setCurrentIndex(len(productList))
        product_id.setCurrentIndex(len(productList))
    else:
        product_id.setCurrentText(productId.text())
        product_text.setCurrentIndex(product_id.currentIndex())


def load_PipeFunction():
    functionList = []
    pipeFunctions = reference["referances"]["pipe"]["pipeFunctions"]
    for i in range(len(pipeFunctions)):
        function_id.addItem(str(pipeFunctions[i]["functionId"]))
        functionList.append(str(pipeFunctions[i]["functionId"]))
        function_text.addItem(str(pipeFunctions[i]["description"]))

    """ Add Other for not in DataDic """
    function_text.addItem("โปรดเลือกหน้าที่ของท่อ")
    function_id.addItem("Other")

    if functionId.text() not in functionList:
        function_text.setCurrentIndex(len(functionList))
        function_id.setCurrentIndex(len(functionList))
    else:
        function_id.setCurrentText(functionId.text())
        function_text.setCurrentIndex(function_id.currentIndex())


def load_PipeLaying():
    pipeLayingList = []
    laying_id.clear()
    laying_text.clear()
    pipeLayings = reference["referances"]["pipe"]["pipeLayings"]
    for i in range(len(pipeLayings)):
        laying_id.addItem(str(pipeLayings[i]["layingId"]))
        pipeLayingList.append(str(pipeLayings[i]["layingId"]))
        laying_text.addItem(str(pipeLayings[i]["description"]))

    """ Add Other for not in DataDic """
    laying_text.addItem("โปรดเลือกลักษณะการวางท่อ")
    laying_id.addItem("Other")
    laying_text.setCurrentIndex(len(pipeLayingList))
    if layingId.text() not in pipeLayingList:
        laying_text.setCurrentIndex(len(pipeLayingList))
        laying_id.setCurrentIndex(len(pipeLayingList))
    else:
        laying_id.setCurrentText(layingId.text())
        laying_text.setCurrentIndex(laying_id.currentIndex())


def load_PipeClass():
    pipeClassList = []
    pipeClasses = reference["referances"]["pipe"]["pipeClasses"]
    class_text.clear()
    class_id.clear()
    for i in range(len(pipeClasses)):
        pipeClass_type = str(pipeClasses[i]["typeId"])
        # if pipeClass_type == pipetypeId.text():
        if pipeClass_type == pipetype_id.currentText():
            class_id.addItem(str(pipeClasses[i]["classId"]))
            pipeClassList.append(str(pipeClasses[i]["classId"]))
            class_text.addItem(str(pipeClasses[i]["description"]))

    """ Add Other for not in DataDic """
    class_text.addItem("โปรดเลือกชั้นคุณภาพ")
    class_id.addItem("Other")
    class_text.setCurrentIndex(len(pipeClassList))
    if classId.text() not in pipeClassList:
        class_text.setCurrentIndex(len(pipeClassList))
        class_id.setCurrentIndex(len(pipeClassList))
    else:
        class_id.setCurrentText(classId.text())
        class_text.setCurrentIndex(class_id.currentIndex())


def load_PipeGrade():
    gradeList = []
    pipeGrades = reference["referances"]["pipe"]["pipeGrades"]
    for i in range(len(pipeGrades)):
        grade_id.addItem(str(pipeGrades[i]["gradeId"]))
        gradeList.append(str(pipeGrades[i]["gradeId"]))
        grade_text.addItem(str(pipeGrades[i]["description"]))

    """ Add Other for not in DataDic """
    grade_text.addItem("โปรดเลือกชั้นคุณภาพ")
    grade_id.addItem("Other")

    if gradeId.text() not in gradeList:
        grade_text.setCurrentIndex(len(gradeList))
        grade_id.setCurrentIndex(len(gradeList))
    else:
        grade_id.setCurrentText(gradeId.text())
        grade_text.setCurrentIndex(grade_id.currentIndex())


def load_PipeType():
    pipeTypeList = []
    pipeTypes = reference["referances"]["pipe"]["pipeTypes"]
    for i in range(len(pipeTypes)):
        pipetype_id.addItem(str(pipeTypes[i]["typeId"]))
        pipeTypeList.append(str(pipeTypes[i]["typeId"]))
        pipetype_text.addItem(str(pipeTypes[i]["description"]))

    """ Add Other for not in DataDic """
    pipetype_text.addItem("โปรดเลือกชนิดท่อ")
    pipetype_id.addItem("Other")

    if pipetypeId.text() not in pipeTypeList:
        pipetype_text.setCurrentIndex(len(pipeTypeList))
        pipetype_id.setCurrentIndex(len(pipeTypeList))
    else:
        pipetype_id.setCurrentText(pipetypeId.text())
        pipetype_text.setCurrentIndex(pipetype_id.currentIndex())


def load_PipeSize():
    pipeSizeList = []
    pipeSize = reference["referances"]["pipe"]["pipeSizes"]
    size_text.clear()
    size_Id.clear()
    depth_combo.clear()
    j = 0
    for i in range(len(pipeSize)):
        piprSize_type = str(pipeSize[i]["type"])
        # if piprSize_type == pipetypeId.text():
        if piprSize_type == pipetype_id.currentText():
            size_Id.addItem(str(pipeSize[i]["sizeId"]))
            pipeSizeList.append(str(pipeSize[i]["sizeId"]))
            size_text.addItem(str(pipeSize[i]["description"]))
            try:
                depth_combo.addItem(str(pipeSize[i]['depth']))
            except:
                depth_combo.addItem(str(0))
            j = j + 1
    """ Add Other for not in DataDic """
    size_text.addItem("โปรดเลือกขนาดท่อ")
    size_Id.addItem("Other")
    depth_combo.addItem("")
    size_text.setCurrentIndex(len(pipeSizeList))
    if len(pipeSizeList) > 0 and sizeId.text() in pipeSizeList:
        sizeIndex = pipeSizeList.index(sizeId.text())
        size_Id.setCurrentIndex(sizeIndex)
        size_text.setCurrentIndex(sizeIndex)
    else:
        size_Id.setCurrentIndex(len(pipeSizeList))
        size_text.setCurrentIndex(len(pipeSizeList))


def pipeSize_change():
    size_Id.setCurrentIndex(size_text.currentIndex())
    depth_combo.setCurrentIndex(size_text.currentIndex())
    depth.setText(depth_combo.currentText())

def pipeProduct_change():
    product_id.setCurrentIndex(product_text.currentIndex())


def pipeFunction_change():
    function_id.setCurrentIndex(function_text.currentIndex())


def pipeLaying_change():
    laying_id.setCurrentIndex(laying_text.currentIndex())


def pipeGrade_change():
    grade_id.setCurrentIndex(grade_text.currentIndex())
    i = grade_id.count()
    if grade_id.currentIndex() == i-1:
        gradeId.setText("")
    else:
        gradeId.setText(grade_id.currentText())


def pipeClass_change():
    class_id.setCurrentIndex(class_text.currentIndex())


def pipeType_change():
    pipetype_id.setCurrentIndex(pipetype_text.currentIndex())
    pipetypeId.setText(pipetype_id.currentText())
    if pipetypeId.text() == "HDPE":
        grade_text.setEnabled(1)
    else:
        grade_text.setEnabled(0)
        i = grade_id.count()
        grade_text.setCurrentIndex(i-1)

    load_PipeSize()
    load_PipeClass()


def projectNo_change():
    global projectNoList
    if projectNo_combo.currentIndex() != 0:
        projectNo.setText(projectNo_combo.currentText())
    if projectNo.text() in projectNoList:
        projectNameCombo.setCurrentIndex(projectNo_combo.currentIndex())
        index = projectNoList.index(projectNo.text())
        projectNameCombo.setCurrentIndex(index)
        projectName.setPlainText(projectNameCombo.currentText())


def load_PipeProject():
    global projectNoList
    url = baseUrl + "/api/2.0/resources/references/pipe-projects?sort=promiseDate:desc&limit=0&pwaCode=" + pwaCode
    payload = {}
    headers = {
        'Authorization': 'Bearer ' + token_new
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    if response.status_code == 200:
        data = response.json()
        numberMatch = data['numberMatch']
        if numberMatch > 0:
            items = data["items"]
            projectNo_combo.clear()
            projectNameCombo.clear()
            strList = []
            projectNoList = []
            print(len(str(projectNo.text())))
            if projectNo.text() == "NULL" or projectNo.text() == "" or len(str(projectNo.text())) == 0:
                projectNo_combo.addItem("โปรดเลื่อกเลขที่สัญญาโครงการ")
            else:
                projectNo_combo.addItem(projectNo.text())

            for i in range(numberMatch):

                try:
                    projectNameCombo.addItem(str(items[i]['projectName']))
                    projectNo_combo.addItem(str(items[i]['projectNo']))
                    strList.append(str(items[i]['projectNo']))
                except:
                    pass
            projectNoList = strList

            autoCompleter(strList)
            if projectNo.text() not in projectNoList:
                projectNo_combo.setCurrentIndex(0)
            else:
                projectNo_combo.setCurrentText(projectNo.text())
                index = projectNoList.index(projectNo.text())
                projectNameCombo.setCurrentIndex(index)
    else:
        message = "Can not get pipe project from server"
        iface.messageBar().pushMessage("Warning  ", message, level=2, duration=3)
        return "err"


def autoCompleter(strList):
    completer = QCompleter()
    completer.setCaseSensitivity(0)
    projectNo_combo.setCompleter(completer)
    model = QStringListModel()
    model.setStringList(strList)
    completer.setFilterMode(Qt.MatchContains)
    completer.setModel(model)


def validate():
    if len(projectNo.text()) == 0 or projectNo.text() == "":
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("เลขที่สัญญาโครงการไม่สามารถใส่ค่าว่างได้ " + projectNo.text())
        msg.setWindowTitle("PWA Message")
        msg.setStandardButtons(QMessageBox.Ok)
        retval = msg.exec_()


def depthCheck():
    depthCheckList = ['2', '3']
    depthStatus = True
    if len(depth.text()) > 0:
        pipeDepth = float(depth.text())
        if depthCheckList not in depthCheckList and pipeDepth <= 0:
            depthStatus = False
    else:
        depthStatus = False
    return depthStatus


def projectCheck():
    projectStatus = True
    if len(projectNo.text()) == 0 or projectNo.text() == "" or projectNo.text() == "NULL":
        projectStatus = False
    return projectStatus


def closeDialog():
    print("close")
    if isinstance(myDialog.parent(), QDialog):
        myDialog.parent().close()


def getPipeLength(featureid):
    line_length = featureid.geometry().length()
    # total = int(line_length * 111320)
    total = float(line_length * 111320)
    total = float("{:.2f}".format(total))
    if length.text() == "NULL" or length.text() == "" or len(str(length.text())) == 0:
        length.setText(str(total))
        length.setEnabled(0)
        print("Pipe length : " + str(total))

def load_YearInstall():
    startYear = 1979 # 2468
    current_year = int(datetime.now().year)
    yearInstall_text.clear()
    list_YearInstall = []

    i = current_year

    yearInstall_text.addItem("โปรดเลือกปี")
    list_YearInstall.append("โปรดเลือกปี")
    while i >= startYear:
        yearInstall_text.addItem(str(i+543))
        list_YearInstall.append(str(i+543))
        i = i - 1

    yearInstall_text.setCurrentIndex(0)
    if yearInstall.text() == "NULL" or yearInstall.text() == "" or len(str(yearInstall.text())) == 0:
        yearInstall.setText(str(current_year))
    else:
        if yearInstall.text() in list_YearInstall:
            yearIndex = list_YearInstall.index(yearInstall.text())
            yearInstall_text.setCurrentIndex(yearIndex)

def yearInstall_change():
    yearInstall.setText(str(yearInstall_text.currentText()))
