from re import I
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import sys

import User
import ContextMenu
            
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

        # Titles
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.verticalHeader().hide()

        # Input cell Data
        for x in range(len(User.Data.Data)): # Row
            for y in range(len(User.Data.StoredKeys)): # Column
                self.setItem(x, y, self.CreateItem(User.Data.StoredValues[x][y]))
        
        # Behaviours 
        for i in range(self.columnCount()):
            if User.Data.StoredKeys[i] == "location":
                self.setItemDelegateForColumn(i, self.ReadOnlyDelegate(self)) 
            else:
                self.setItemDelegateForColumn(i, self.CenterDelegate(self)) 

        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSelectionMode(QTableWidget.SingleSelection)   

        # Update Data
        self.itemChanged.connect(lambda item: self.ItemModified(item))

    def mousePressEvent(self, QMouseEvent):
        # Get index + item
        self.index = self.indexAt(QMouseEvent.pos())

        # Reset selection
        self.clearSelection()

        # Select Item
        self.setCurrentItem(self.item(self.index.row(), self.index.column()))

        # Remove button
        if QMouseEvent.button() == Qt.LeftButton:
            # Open Context Menu
            ContextMenu.Start(self)
        elif QMouseEvent.button() == Qt.RightButton:
            pass

    def ItemModified(self, item):
        if User.Data.StoredKeys[self.currentColumn()] != "location":
            CapitalizedInput = " ".join([x.capitalize() for x in item.text().split()])

            if item.text() != CapitalizedInput:
                self.setItem(self.currentRow(), self.currentColumn(), self.CreateItem(CapitalizedInput))
                return
        
        User.Data.Update(item, self.currentRow(), self.currentColumn())

    def Add(self, button): 
        self.insertRow(self.rowCount())

        User.Data.AddDoc()

        for i in range(self.columnCount()):
            self.setItem(self.rowCount()-1, i, self.CreateItem(User.Data.GetPlaceholder()))

        if self.rowCount() == 2:
            button.setEnabled(True)

    def Remove(self, button):
        if self.rowCount() > 1:
            User.Data.DelDoc(self.currentRow())

            self.removeRow(self.currentRow())

            self.clearSelection()
            
            button.setEnabled(False)

class Window(QWidget):
    def __init__(self):
        super().__init__()

        # Saved Changelog Data
        User.Data.Load()

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
        rows = [str(x+1) for x in range(len(User.Data.Data))]
        columns = User.Data.StoredKeys

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

        # Add item to table
        self.add = QPushButton('+', self)
        self.add.clicked.connect(lambda: self.DataTable.Add(self.remove))
        grid.addWidget(self.add, 0, 1)

        # Remove selected item from table
        self.remove = QPushButton('-', self)
        self.remove.clicked.connect(lambda: self.DataTable.Remove(self.remove))
        self.DataTable.itemSelectionChanged.connect(lambda: self.remove.setEnabled((self.DataTable.rowCount() > 1)))
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
