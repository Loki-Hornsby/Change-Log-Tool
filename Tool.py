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

        # Input cell Data
        for i in range(len(User.Data.Data)): # Row
            for j in range(len(User.Data.StoredKeys)): # Column
                data = User.Data.StoredValues[i][j]

                # If it's not a dict
                if type(data) != type({}):
                    item = QTableWidgetItem(data)
                    item.setTextAlignment(Qt.AlignCenter) 
                    self.setItem(i, j, item)
                    #self.setSpan(i, j, len(y), 1)

        # Resize
        self.resizeRowsToContents()
        self.resizeColumnsToContents()

    def SetTitles(self):
        # Titles
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        #self.verticalHeader().hide()

    def SetBehaviours(self):
        # Behaviours 
        for i in range(self.columnCount()):
            if User.Data.StoredKeys[i] == "location":
                self.setItemDelegateForColumn(i, self.ReadOnlyDelegate(self)) 
            else:
                self.setItemDelegateForColumn(i, self.CenterDelegate(self)) 

        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSelectionMode(QTableWidget.SingleSelection)   

    def __init__(self, y, x, *args):
        # Setup
        QTableWidget.__init__(self, *args)
        self.SetData(y, x)

        # Titles
        self.SetTitles()

        # Behaviours 
        self.SetBehaviours()

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
                self.setItem(self.currentRow(), self.currentColumn(), QTableWidgetItem(CapitalizedInput))
                return
        
        User.Data.Update(item, self.currentRow(), self.currentColumn())

    def Add(self, button): 
        self.insertRow(self.rowCount())

        User.Data.AddDoc()

        for i in range(self.columnCount()):
            self.setItem(self.rowCount()-1, i, QTableWidgetItem(User.Data.GetPlaceholder()))

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
        
        base_layout = QVBoxLayout()
        horizontal_layout = QHBoxLayout()
        vertical_layout = QVBoxLayout()

        # Data Table
        rows = [str(x+1) for x in range(len(User.Data.Data))]
        columns = User.Data.StoredKeys

        self.DataTable = TableView(
            rows,            # Y Data
            columns,         # X Data
            len(rows),       # Y length
            len(columns)     # X Length
        )

        horizontal_layout.addWidget(self.DataTable)

        # Changelog Table
        rows = ["1.1.1 TEST", "2.2.2 TEST"]
        columns = ["Name TEST", "Contents TEST"]

        self.ChangelogTable = TableView(
            rows,            # Y Data
            columns,         # X Data
            len(rows),       # Y length
            len(columns)     # X Length
        )

        horizontal_layout.addWidget(self.ChangelogTable)

        # Grid for buttons
        grid = QGridLayout()
        grid.setColumnStretch(0, 4)
        grid.setColumnStretch(1, 4)
        grid.setColumnStretch(2, 1)
        grid.setColumnStretch(3, 4)
        grid.setColumnStretch(4, 4)
        vertical_layout.addLayout(grid)

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
        base_layout.addLayout(horizontal_layout)
        base_layout.addLayout(vertical_layout)
        
        group_box.setLayout(base_layout)

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
