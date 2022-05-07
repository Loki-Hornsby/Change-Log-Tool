# TODO: Fix remove (disable remove button when cell isn't selected)

from unittest import loader
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import yaml

import math
import random

import sys
import os
from os import listdir, system
from os.path import *

class settings:
    GeneratorData = None
    Data = None

    placeholders = [
            "(づ￣ ³￣)づ",
            "( ˘ ³˘)♥",
            "(ง'̀-'́)ง",
            "{•̃_•̃}",
            "[¬º-°]¬",
            "(∩｀-´)⊃━☆ﾟ.*･｡ﾟ",
            "(っ˘ڡ˘ς)",
            "(งツ)ว",
            "ʕʘ̅͜ʘ̅ʔ",
            "\(ᵔᵕᵔ)/",
            "(._.)",
            "(っ•́｡•́)♪♬",
            "(•̀ᴗ•́)و ̑̑",
            "(ᵔᴥᵔ)",
            "◖ᵔᴥᵔ◗ ♪ ♫",
            "♪♪ ヽ(ˇ∀ˇ )ゞ",
            "ヽ(´▽`)/",
            "ʕ·͡ᴥ·ʔ",
            "ʕっ•ᴥ•ʔっ",
            "( ˘ ³˘)ノ°ﾟº❍｡",
            "(͡ ° ͜ʖ ͡ °)",
            "(｡◕‿‿◕｡)",
            "(ᕗ ͠° ਊ ͠° )ᕗ",
            "ᕕ(⌐■_■)ᕗ ♪♬",
            "(◕ᴥ◕ʋ)",
            "(҂◡_◡) ᕤ",
            "(ﾉ◕ヮ◕)ﾉ*:・ﾟ✧",
            "(ง •̀_•́)ง",
            "(✿◠‿◠)",
            "( つ◕ل͜◕)つ",
            "༼ つ ╹ ╹ ༽つ",
            "(*・‿・)ノ⌒*:･ﾟ✧",
            "(ﾉ☉ヮ⚆)ﾉ ⌒*:･ﾟ✧",
            "༼つಠ益ಠ༽つ ─=≡ΣO))",
            "٩( ๑╹ ꇴ╹)۶",
            "._.)/\(._.",
            "(づ｡◕‿‿◕｡)づ",
            "／人◕ ‿‿ ◕人＼"
        ]

    def GetPlaceholder():
        return settings.placeholders[random.randint(0, len(settings.placeholders))-1]

    # Load settings
    def Load():
        with open("settings.yaml") as stream:
            try:
                settings.GeneratorData = yaml.safe_load_all(stream)
                settings.Data = list(settings.GeneratorData)

                settings.GenerateData()
            except yaml.YAMLError as exc:
                print(exc)
                return None

    def GenerateData():
        # Get all possible keys
        settings.StoredKeys = []   # Columns
        settings.StoredValues = []   # Rows

        # Generate keys
        for row in range(len(settings.Data)):
            key = list(settings.Data[row].keys())

            for column in range(math.floor(len(key) / 2)):
                if key not in settings.StoredKeys:
                    settings.StoredKeys.append(key)

        settings.StoredKeys = sum(settings.StoredKeys, []) # Convert keys to 1 dimensional array

        # Generate values
        for column in range(len(settings.Data)):
            value = list(settings.Data[column].values())

            for row in range(math.floor(len(value) / 2)):
                settings.StoredValues.append(value)

    # Update Settings
    def Update(item, row, column):
        if item != None:
            # Set the data
            settings.Data[row][settings.StoredKeys[column]] = item.text()   
            
            with open("settings.yaml", "w") as f:
                yaml.safe_dump_all(settings.Data, f)
    
    # Add a document
    def AddDoc():
        # Creates an empty document with all keys filled with an empty placeholder in settings.yaml
        with open("settings.yaml", "w") as f:
            dic = {}

            for v in settings.StoredKeys:
                dic[v] = settings.GetPlaceholder()
            
            settings.Data.append(dict(dic))
            yaml.safe_dump_all(settings.Data, f)

    # Delete a document
    def DelDoc(i):
        with open("settings.yaml", "w") as f:
            del settings.Data[i]
            yaml.safe_dump_all(settings.Data, f)
            
class ViewFiles(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel("Another Window dsadsadsadsa")
        layout.addWidget(self.label)
        self.setLayout(layout)

# Table
class TableView(QTableWidget):
    class ReadOnlyDelegate(QtWidgets.QStyledItemDelegate):
        def createEditor(self, parent, option, index):
            return
    
    class CenterDelegate(QtWidgets.QStyledItemDelegate):
        def createEditor(self, parent, option, index):
            editor = QStyledItemDelegate.createEditor(self, parent, option, index)
            editor.setAlignment(Qt.AlignCenter)
            return editor

    def SetData(self, y, x): 
        # Y: Columns
        # X: Rows
        self.setVerticalHeaderLabels(y)
        self.setHorizontalHeaderLabels(x)
    
    def CreateItem(self, data):
        item = QTableWidgetItem(data)
        item.setTextAlignment(Qt.AlignCenter) 
        
        return item

    def __init__(self, y, x, *args):
        # Setup
        QTableWidget.__init__(self, *args)
        self.SetData(y, x)
        self.resizeRowsToContents()
        self.resizeColumnsToContents()

        # Active item
        self.activeItem = None

        # Item
        self.itemSelected = False
        self.CurRow = 0
        self.CurColumn = 0

        # Titles
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.verticalHeader().hide()

        # Input cell Data
        for x in range(len(settings.Data)): # Row
            for y in range(len(settings.StoredKeys)): # Column
                self.setItem(x, y, self.CreateItem(settings.StoredValues[x][y]))
        
        # Behaviours 
        for i in range(self.columnCount()):
            if settings.StoredKeys[i] == "location":
                self.setItemDelegateForColumn(i, self.ReadOnlyDelegate(self)) 
            else:
                self.setItemDelegateForColumn(i, self.CenterDelegate(self)) 

        self.setSelectionMode(QTableWidget.SingleSelection)   

        # Update Position
        self.itemSelectionChanged.connect(lambda: self.SetActive())

        # Update Data
        self.itemChanged.connect(lambda item: settings.Update(item, self.CurRow, self.CurColumn))

        # Display Menu
        self.itemDoubleClicked.connect(lambda item: self.DialogueMenu(item))

    # Store the active row and column selected or default to 0 if there is none
    def SetActive(self):
        if self.rowCount() != 1:
            self.itemSelected = True
        else:
            self.itemSelected = False

        try:
            self.CurRow = self.currentRow()
            self.CurColumn = self.currentColumn()

            self.activeItem = self.item(self.CurRow, self.CurColumn)
        except:
            self.itemSelected = False

            self.CurRow = 0
            self.CurColumn = 0
            self.activeItem = self.item(0, 0)

    # Select Menu
    def DialogueMenu(self, item):
        if (settings.StoredKeys[self.CurColumn] == "location"): # Location
            folder = QFileDialog.getExistingDirectory(self, "Select Directory")
            if len(folder) > 0:
                self.setItem(self.CurRow, self.CurColumn, self.CreateItem(folder))

    def Add(self, button): 
        self.insertRow(self.rowCount())

        settings.AddDoc()

        for i in range(self.columnCount()):
            self.setItem(self.rowCount()-1, i, self.CreateItem(settings.GetPlaceholder()))

        if self.rowCount() == 2:
            button.setEnabled(True)

    def Remove(self, button):
        if self.rowCount() > 1:
            settings.DelDoc(self.CurRow)

            self.removeRow(self.CurRow)

            self.clearSelection()
            
            button.setEnabled(False)

class Window(QWidget):
    def __init__(self):
        super().__init__()

        # Saved Changelog Data
        settings.Load()

        # Setup UI
        self.initUi()

        self.w = None  # No external window yet.

    def initUi(self):
        # Window setup
        self.setFixedSize(600, 500)
        self.center()

        # Layout setup
        main_layout = QHBoxLayout()
        group_box = QGroupBox("Change Log Tool")
        group_box_layout = QVBoxLayout()

        # Table
        rows = [str(x+1) for x in range(len(settings.Data))]
        columns = settings.StoredKeys

        self.DataTable = TableView(
            rows,            # Y Data
            columns,         # X Data
            len(rows),       # Y length
            len(columns)     # X Length
        )

        group_box_layout.addWidget(self.DataTable)

        # Grid for buttons
        grid = QGridLayout()
        grid.setColumnStretch(0, 4)
        grid.setColumnStretch(1, 4)
        grid.setColumnStretch(2, 1)
        grid.setColumnStretch(3, 4)
        grid.setColumnStretch(4, 4)
        group_box_layout.addLayout(grid)

        # Buttons
        self.add = QPushButton('+', self)
        self.add.clicked.connect(lambda: self.DataTable.Add(self.remove))
        grid.addWidget(self.add, 0, 1)

        self.remove = QPushButton('-', self)
        self.remove.clicked.connect(lambda: self.DataTable.Remove(self.remove))
        self.DataTable.itemSelectionChanged.connect(lambda: self.remove.setEnabled(self.DataTable.itemSelected))
        self.remove.setEnabled(False)
        grid.addWidget(self.remove, 0, 3)
        
        # Finalise Ui Setup
        group_box.setLayout(group_box_layout)
        main_layout.addWidget(group_box)
        self.setLayout(main_layout)
        
        self.show()

    # Center window
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # View file list in seperate window (WIP)
    def ViewFiles(self, checked):
        if self.w is None:
            self.w = ViewFiles()
        self.w.show()
    
    # Make a new changelog
    def New():
        pass

    # View changelog
    def View(self, itemPath, regularPath):
        path = ""
        if exists(itemPath):
            path = itemPath
        else:
            path = regularPath

        os.startfile('"' + path + '"')

# App startup
if __name__ == '__main__':
    # create pyqt5 app
    App = QApplication(sys.argv)
  
    # create the instance of our Window
    window = Window()

    # Name Window
    window.setWindowTitle("Change Log Tool")
  
    # Start the app
    sys.exit(App.exec_())
