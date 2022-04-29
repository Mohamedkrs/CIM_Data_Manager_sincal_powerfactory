import glob
import logging
import os
import sys
from distutils.util import strtobool
from functools import partial
from pathlib import Path

import cimpy
from PyQt5 import Qt, QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
import DataManager

logging.basicConfig(filename='importCIGREMV.log',
                    level=logging.INFO, filemode='w')


def messages(message, title, isQuestion=False):
    msgBox = QMessageBox()
    msgBox.setWindowFlags(
        QtCore.Qt.Dialog | QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowTitleHint)
    if title == "Warning":
        msgBox.setIcon(QMessageBox.Warning)
    else:
        msgBox.setIcon(QMessageBox.Information)

    msgBox.setWindowTitle(title)
    if isQuestion:
        question = msgBox.question(
            msgBox, title, message, msgBox.Yes | msgBox.No)

        if question == msgBox.No:
            return False
        else:
            return True
    else:
        msgBox.setText(message)
        msgBox.exec_()


class StandardItem(Qt.QStandardItem):
    def __init__(self, txt='', font_size=12, set_bold=False, color=Qt.QColor(0, 0, 0)):
        super().__init__()
        fnt = Qt.QFont('Open Sans', font_size)
        fnt.setBold(set_bold)
        self.setEditable(False)
        self.setForeground(color)
        self.setFont(fnt)
        self.setText(txt)


class MainWindow(QDialog):
    foo_dir = ""
    data_manager = DataManager.ManageElements()
    firstLoad = True
    modified = False
    mRIDold = None

    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi(".\Gui.ui", self)
        self.noWheelCombos = []
        self.checkBoxList = self.findChildren(QtWidgets.QCheckBox)
        self.searchBtn.clicked.connect(self.browse_files)
        self.loadBtn.clicked.connect(self.import_from_xml)
        self.exportBtn.clicked.connect(self.export)
        self.elemProperties.itemChanged.connect(self.current_mRID)
        self.elemProperties.horizontalHeader().setSectionResizeMode(
            1, QtWidgets.QHeaderView.Stretch)
        self.filterBtn.clicked.connect(self.filtering)
        self.resetBtn.clicked.connect(self.import_from_xml)
        ######
        self.treeView.doubleClicked.connect(lambda: clicked(self))
        self.treeView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treeView.customContextMenuRequested.connect(
            self._show_context_menu)

    def _show_context_menu(self, position):
        try:
            if("EnergySource" in self.treeView.currentIndex().data()):
                display_action = QAction("Swap to ExternalNetworkInjection")
                display_action.triggered.connect(self.swap_source)
                display_action1 = QAction(
                    "Swap all to ExternalNetworkInjection")
                display_action1.triggered.connect(self.swap_all_sources)
                menu = QMenu(self.treeView)
                menu.addAction(display_action)
                menu.addAction(display_action1)
                menu.exec_(self.treeView.mapToGlobal(position))
        except:
            return

    def swap_source(self):
        item = self.treeView.model().itemFromIndex(self.treeView.currentIndex())
        item.setEditable(True)
        if ' ' in item.text():
            self.data_manager.swapEnergySourceWithExternalGrid(
                item.text(), "ExternalNetworkInjection " +
                item.text().split()[1])
            item.setText("ExternalNetworkInjection " +
                         item.text().split()[1])
        else:
            self.data_manager.swapEnergySourceWithExternalGrid(
                item.text(), "ExternalNetworkInjection")
            item.setText("ExternalNetworkInjection")
        item.setEditable(False)
        update_data(self, self.mRIDold)

    def swap_all_sources(self,):
        root = self.treeView.model().invisibleRootItem()
        for item in self.iterItems(root):
            if "EnergySource" in item.text():
                item.setEditable(True)
                if ' ' in item.text():
                    self.data_manager.swapEnergySourceWithExternalGrid(
                        item.text(), "ExternalNetworkInjection " +
                        item.text().split()[1])
                    item.setText("ExternalNetworkInjection " +
                                 item.text().split()[1])
                else:
                    self.data_manager.swapEnergySourceWithExternalGrid(
                        item.text(), "ExternalNetworkInjection")
                    item.setText("ExternalNetworkInjection")
                item.setEditable(False)
        update_data(self, self.mRIDold)

    def import_from_xml(self):
        self.elemProperties.clearContents()
        self.elemProperties.setRowCount(0)
        file_path = self.folderPath.text()
        # Parse importedXml Files ###
        if not file_path:
            messages("The Path is Empty", "Warning")
            return
        example = Path(file_path).resolve()
        xml_files = []
        for file in example.glob('*.xml'):
            xml_files.append(str(file.absolute()))
        if len(xml_files) == 0:
            messages("No CIM files found!", "Warning")
            return
        if not self.exportBtn.isEnabled():
            self.exportBtn.setEnabled(True)
            self.filterBtn.setEnabled(True)
            self.resetBtn.setEnabled(True)
        cgmesver = "cgmes_v2_4_15"
        try:
            import_result = cimpy.cim_import(xml_files, cgmesver)
        except:
            messages('No CIM files found!', "Warning")
            return
        self.data_manager.data = import_result
        self.data_manager.profile_elements = {}
        treeModel = Qt.QStandardItemModel()
        rootNode = treeModel.invisibleRootItem()
        for checkbox in self.checkBoxList:
            checkbox.installEventFilter(self)
            if checkbox.text() in self.data_manager.data['meta_info']['profiles'].keys():
                profile = StandardItem(checkbox.text(), 9, set_bold=True)

                for elem in self.data_manager.import_eq_data(checkbox.text()):
                    profile.appendRow(StandardItem(elem, 9))
                rootNode.appendRow(profile)
                self.treeView.setModel(treeModel)
                checkbox.setCheckable(True)
                checkbox.setChecked(True)
            else:
                checkbox.setChecked(False)
                checkbox.setCheckable(False)

    def current_mRID(self):
        self.modified = True
        if not self.data_manager.profile_elements[
                self.treeView.currentIndex().data()] == self.mRIDold:
            self.mRIDold = self.data_manager.profile_elements[self.treeView.currentIndex(
            ).data()]

    def update_data(self, mRID):
        for item in range(self.elemProperties.rowCount()):
            widget = self.elemProperties.cellWidget(item, 1)
            if isinstance(widget, QtWidgets.QComboBox):
                if self.elemProperties.cellWidget(item, 1).currentText() in ["True", "False"]:
                    self.data_manager.data['topology'][mRID].__dict__[
                        self.elemProperties.item(item, 0).text()] = bool(
                        strtobool(self.elemProperties.cellWidget(item, 1).currentText()))
                else:
                    self.data_manager.data['topology'][mRID].__dict__[
                        self.elemProperties.item(item, 0).text()] = self.elemProperties.cellWidget(item, 1).currentText()
            elif not isinstance(widget, QtWidgets.QPushButton) and not isinstance(widget, QtWidgets.QToolButton):
                self.data_manager.data['topology'][mRID].__dict__[
                    self.elemProperties.item(item, 0).text()] = self.elemProperties.item(item, 1).text()

    # Export data depending on checked boxes
    def export(self):
        update_data(self, self.mRIDold)
        dialog = QFileDialog()
        output_dir = dialog.getExistingDirectory(self, 'Select a Folder')
        if not output_dir:
            return
        if os.path.isdir(output_dir):
            if not messages("This Folder will be overridden, continue?",
                            "Warning", True):
                return
        active_profile_list = []
        for checkbox in self.checkBoxList:
            if checkbox.isChecked():
                active_profile_list.append(checkbox.text())
        export_data = cimpy.sincal_Pf(self.data_manager.data)
        for filename12 in glob.glob(output_dir + "/*"):
            os.remove(filename12)
        cimpy.cim_export(export_data, output_dir + "/output",
                         "cgmes_v2_4_15", active_profile_list)
        messages("Data successfully exported", "Info")

    def eventFilter(self, source, event):
        if (event.type() == QtCore.QEvent.Wheel and
                source in self.noWheelCombos):
            return True
        # TODO: add hint if checkbox is not checkable
        elif (type(source) == QtWidgets.QCheckBox and event.type() == QtCore.QEvent.MouseButtonPress and event.button() == QtCore.Qt.RightButton and not source.isChecked()):
            QToolTip.showText(QtCore.QPoint(555, 227),
                              "Selection not possible", source)
        return super(MainWindow, self).eventFilter(source, event)

    def browse_files(self):
        dialog = QFileDialog()
        importpath = dialog.getExistingDirectory(self, 'Select a CIM Folder')
        if importpath:
            self.folderPath.setText(importpath)

    def iterItems(self, root):
        if root is not None:
            stack = [root]
            while stack:
                parent = stack.pop(0)
                for row in range(parent.rowCount()):
                    for column in range(parent.columnCount()):
                        child = parent.child(row, column)
                        yield child
                        if child.hasChildren():
                            stack.append(child)

    def filtering(self):
        if 'Filter' == self.filterBtn.text():
            update_data(self, self.mRIDold)
            filter = Filtering()
            filter.exec()
            res = {}
            if filter.elem != '' or filter.prop != '' or filter.detail != '':
                res = self.data_manager.filter_data(filter.elem, filter.prop, filter.detail, filter.elem_andor_prop,
                                                    filter.prop_andor_elem)
                if len(res) > 0:
                    self.elemProperties.setRowCount(0)
                    root = self.treeView.model().invisibleRootItem()
                    for item in self.iterItems(root):
                        for row in range(item.rowCount()):
                            child = item.child(row)
                            if not child.text() in res:
                                self.treeView.setRowHidden(
                                    row, item.index(), True)
                    self.filterBtn.setText("Clear Filter")
                else:
                    messages("No Matches Found", "Info")
        else:
            self.elemProperties.setRowCount(0)
            root = self.treeView.model().invisibleRootItem()
            for item in self.iterItems(root):
                for row in range(item.rowCount()):
                    child = item.child(row)
                    self.treeView.setRowHidden(
                        row, item.index(), False)
            self.filterBtn.setText("Filter")


def handleButtonClicked(window):
    button = window.sender()
    print(button)
    index = window.elemProperties.indexAt(button.pos())
    if isinstance(button, Qt.QMenu):
        if "list" not in button.title():
            print(button.sender().text())
            if button.sender().text() in window.data_manager.profile_elements.keys():
                itemtext = button.sender().text()
                root = window.treeView.model().invisibleRootItem()
                for item in window.iterItems(root):
                    if itemtext == item.text():
                        window.treeView.selectionModel().setCurrentIndex(item.index(),
                                                                         Qt.QItemSelectionModel.ClearAndSelect)
                        clicked(window)
                        break

    if index.isValid():
        if button.text() in window.data_manager.profile_elements.keys():
            itemtext = button.text()
            root = window.treeView.model().invisibleRootItem()
            for item in window.iterItems(root):
                if itemtext == item.text():
                    window.treeView.selectionModel().setCurrentIndex(item.index(),
                                                                     Qt.QItemSelectionModel.ClearAndSelect)
                    clicked(window)
                    break


def update_data(window, mRID):
    for item in range(window.elemProperties.rowCount()):
        widget = window.elemProperties.cellWidget(item, 1)
        if isinstance(widget, QtWidgets.QComboBox):
            if window.elemProperties.cellWidget(item, 1).currentText() in ["True", "False"]:
                MainWindow.data_manager.data['topology'][mRID].__dict__[
                    window.elemProperties.item(item, 0).text()] = bool(
                    strtobool(window.elemProperties.cellWidget(item, 1).currentText()))
            else:
                MainWindow.data_manager.data['topology'][mRID].__dict__[
                    window.elemProperties.item(item, 0).text()] = window.elemProperties.cellWidget(item,
                                                                                                   1).currentText()
        elif not isinstance(widget, QtWidgets.QPushButton) and not isinstance(widget, QtWidgets.QToolButton):
            MainWindow.data_manager.data['topology'][mRID].__dict__[
                window.elemProperties.item(item, 0).text()] = window.elemProperties.item(item, 1).text()


def clicked(window, imported_dict=None):
    try:
        index = window.treeView.selectedIndexes()[0]
        item = index.model().itemFromIndex(index)
        mRID = window.data_manager.profile_elements[item.text()]
        imported_dict = window.data_manager.data['topology'][mRID].__dict__
        if window.modified:
            update_data(window, window.mRIDold)
    except:
        return
    row = 0
    window.elemProperties.setRowCount(0)
    for key, val in imported_dict.items():
        if val is None:
            property_name = QTableWidgetItem(key)
            property_name.setFlags(property_name.flags()
                                   ^ QtCore.Qt.ItemIsEditable)
            btn = QtWidgets.QToolButton()
            btn.setText("None")
            btn.setPopupMode(Qt.QToolButton.MenuButtonPopup)
            menu_filters = QtWidgets.QMenu()
            menu_filters.addAction("Add")
            menu_filters.addAction("Delete")
            btn.setMenu(menu_filters)
            menu_filters.triggered[QAction].connect(
                lambda: handleButtonClicked(window))
            window.elemProperties.insertRow(window.elemProperties.rowCount())
            window.elemProperties.setItem(row, 0, property_name)
            window.elemProperties.setCellWidget(row, 1, btn)
        elif isinstance(val, (str, int, float, bool)):
            window.elemProperties.insertRow(window.elemProperties.rowCount())
            property_name = QTableWidgetItem(key)
            property_name.setFlags(property_name.flags()
                                   ^ QtCore.Qt.ItemIsEditable)
            detail = val
            if detail is None:
                property_detail = QTableWidgetItem("None")
            else:
                property_detail = QTableWidgetItem(str(detail))
            window.elemProperties.setItem(row, 0, property_name)
            if "mRID" in key:
                property_detail.setFlags(
                    property_detail.flags() ^ QtCore.Qt.ItemIsEditable)
            if isinstance(detail, bool):
                c = QtWidgets.QComboBox()
                window.noWheelCombos.append(c)
                if detail:
                    c.addItems([str(detail), "False"])
                else:
                    c.addItems([str(detail), "True"])
                try:
                    c.currentTextChanged.connect(window.current_mRID)
                except:
                    pass
                try:
                    mrid = window.data["mRID"]
                    c.currentTextChanged.connect(
                        lambda: update_data(window, mrid))
                except:
                    pass
                c.installEventFilter(window)
                window.elemProperties.setCellWidget(row, 1, c)
            elif "operatingMode" in key:
                c = QtWidgets.QComboBox()
                c.addItems(
                    [val, 'cell11', 'cell12', 'cell13',
                     'cell15', ])
                c.currentTextChanged.connect(window.current_mRID)
                window.elemProperties.setCellWidget(row, 1, c)
            else:
                window.elemProperties.setItem(row, 1, property_detail)
        elif isinstance(val, list):
            property_name = QTableWidgetItem(key)
            property_name.setFlags(property_name.flags()
                                   ^ QtCore.Qt.ItemIsEditable)
            btn1 = QtWidgets.QToolButton()
            btn1.setText("show list")
            btn1.setPopupMode(Qt.QToolButton.MenuButtonPopup)
            menu_filters = QtWidgets.QMenu()
            for dicts in window.data_manager.data['topology'][mRID].__dict__[key]:
                if dicts.__dict__["mRID"] in window.data_manager.profile_elements.values():
                    for k, c in window.data_manager.profile_elements.items():
                        if c == dicts.__dict__["mRID"]:
                            menu_filters.addAction(k)

            btn1.setMenu(menu_filters)
            menu_filters.triggered[QAction].connect(
                lambda: handleButtonClicked(window))

            window.elemProperties.insertRow(window.elemProperties.rowCount())
            window.elemProperties.setItem(row, 0, property_name)
            window.elemProperties.setCellWidget(row, 1, btn1)
            # self.elemProperties.setItem(row, 1, property_name)
        elif "mRID" in val.__dict__:
            property_name = QTableWidgetItem(key)
            property_name.setFlags(property_name.flags()
                                   ^ QtCore.Qt.ItemIsEditable)
            detail = val.__dict__["mRID"]
            btn = QtWidgets.QPushButton()

            if detail in window.data_manager.profile_elements.values():
                btn.setText(
                    [k for k, v in window.data_manager.profile_elements.items() if v == detail][0])

            btn.clicked.connect(lambda: handleButtonClicked(window))

            property_detail = QTableWidgetItem(str(detail))
            property_detail.setFlags(
                property_detail.flags() ^ QtCore.Qt.ItemIsEditable)
            window.elemProperties.insertRow(window.elemProperties.rowCount())
            window.elemProperties.setItem(row, 0, property_name)
            window.elemProperties.setCellWidget(row, 1, btn)
        else:
            property_name = QTableWidgetItem(key)
            property_name.setFlags(property_name.flags()
                                   ^ QtCore.Qt.ItemIsEditable)
            btn = QtWidgets.QPushButton()
            btn.setText("show data")

            # try:
            btn.clicked.connect(lambda: handleButtonClicked(window))
            # except :
            #   pass
            window.elemProperties.insertRow(window.elemProperties.rowCount())
            window.elemProperties.setItem(row, 0, property_name)
            window.elemProperties.setCellWidget(row, 1, btn)

        row += 1
    window.modified = False


class ListData(QDialog):
    tabledata = {}
    data = None
    modified = False

    def __init__(self, data):
        self.noWheelCombos = []
        self.data = data
        self.data_manager = DataManager.ManageElements()
        super(ListData, self).__init__()
        if isinstance(data, list):
            loadUi("ListData.ui", self)
            self.displayView()
            self.elemView.itemClicked.connect(clicked(self))
        else:
            loadUi("listProp.ui", self)
            clicked(self, data)
        self.elemProperties.itemChanged.connect(
            lambda: update_data(self, self.data["mRID"]))

    def set_modified_true(self):
        self.modified = True

    def expand_dict(self):
        if isinstance(self.data, list):
            for dicts in self.data:
                self.data_managertwo.data.append(dicts.__dict__)
        else:
            # print(self.data.__dict__)
            self.data_managertwo.data.append(self.data.__dict__)

    def eventFilter(self, source, event):
        if (event.type() == QtCore.QEvent.Wheel and
                source in self.noWheelCombos):
            return True
        return super(ListData, self).eventFilter(source, event)

    def displayView(self):
        self.expand_dict()
        self.elemView.addItems(self.data_managertwo.import_eq_data())


class Filtering(QDialog):
    elem = ""
    prop = ""
    detail = ""
    elem_andor_prop = ""
    prop_andor_elem = ""

    def __init__(self):
        super(Filtering, self).__init__()
        loadUi("filter.ui", self)
        self.setWindowTitle("Filter")
        self.setWindowFlags(
            QtCore.Qt.Dialog | QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowTitleHint)
        self.okBtn.clicked.connect(self.setDetails)
        self.cancelBtn.clicked.connect(self.close)

    def setDetails(self):
        self.elem = self.elemText.text()
        self.prop = self.propText.text()
        self.detail = self.detText.text()
        self.elem_andor_prop = self.elem_andor_prop_cBox.currentText()
        self.prop_andor_elem = self.prop_andor_det_cBox.currentText()
        self.close()


def start_gui():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    widget = QtWidgets.QStackedWidget()
    widget.addWidget(main_window)
    widget.adjustSize()
    widget.setWindowTitle("CIM Data Manager")
    widget.setWindowIcon(QtGui.QIcon('icon.png'))
    widget.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    start_gui()
