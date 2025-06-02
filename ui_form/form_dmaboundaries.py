from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel,QDialogButtonBox, QLineEdit, QMessageBox, QComboBox, QApplication, QGroupBox
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
    global myDialog
    global groupBox_2
    global _temp_id
    global dmaId
    global _temp_id

    # global dmaId

    myDialog = dialog
    myLayer = layerid
    myLayer.startEditing()

    groupBox_2 = myDialog.findChild(QGroupBox, "groupBox_2")
    groupBox_2.setVisible(False)

    temp_random = random.randint(100000, 9000000)

    dmaId = myDialog.findChild(QLineEdit, "dmaId")
    dmaId.setEnabled(1)
    dmaId.setVisible(False)
    label_dmaId = myDialog.findChild(QLabel, "label_dmaId")
    label_dmaId.setVisible(False)

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
