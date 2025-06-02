from qgis.PyQt.QtWidgets import QWidget, QVBoxLayout, QPushButton, QDialogButtonBox
from qgis.core import QgsEditorWidgetSetup
from qgis.PyQt import uic
import os.path
import os
import requests
from pwagis.utiles import *
from qgis.utils import iface

# ui_file = "form_valve.ui"
# plugin_dir = os.path.dirname(__file__)
# ui_path = os.path.join(plugin_dir, "ui_form", ui_file)


def tile_form(self, dialog, layer, search_id, ui_path):
    # clearLayout(dialog.layout())
    dialog_widget = uic.loadUi(ui_path)
    layout = dialog.layout()
    layout.addWidget(dialog_widget)

    button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
    ok_button = button_box.button(QDialogButtonBox.Ok)
    cancel_button = button_box.button(QDialogButtonBox.Cancel)
    layout.addWidget(button_box)
    dialog.setLayout(layout)


def clearLayout(layout):
    while layout.count():
        child = layout.takeAt(0)
        if child.widget():
            child.widget().deleteLater()



