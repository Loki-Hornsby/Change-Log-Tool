from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import heapq
import glob
import os
from os import listdir, system
from os.path import *

from datetime import datetime

import User

def Start(self):
    class Folder:
        def GetPath():
            path = self.currentItem().text() + "/"
            return path

        path = ""
        allfiles = sorted(glob.iglob(GetPath() + '*.txt'), key=os.path.getctime)

        def GetDate(format):
            return str(datetime.today().strftime(format))

        def FileToday():
            return Folder.GetPath() + Folder.GetDate('%d.%m.%y') + ".txt"

        def FileLast():
            files = Folder.allfiles

            if len(files) > 1:
                return files[len(files)-2] # (Gets 2nd to last)

    def EditDir():
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        if len(directory) > 0:
            self.setItem(self.currentRow(), self.currentColumn(), self.CreateItem(directory))

    def CreateChangelog():
        p = Folder.FileToday()

        f = open(p, "w")
        f.write("_________" + "\n")
        f.write("\n")
        f.write(Folder.GetDate('%d/%m/%y:') + "\n")
        f.write("_________" + "\n")
        f.write("\n")
        f.close()

    def ViewChangelog():
        os.system('"' + Folder.FileLast() + '"')

    if User.Data.StoredKeys[self.currentColumn()] == "location": # Location
        # Menu
        self.contextMenu = QMenu(self)

        # Edit path on item
        Edit = QAction("Edit Path", self)
        Edit.triggered.connect(lambda: EditDir())
        self.contextMenu.addAction(Edit)

        # Create changelog with todays date
        # TODO: ** I may make this into a custom file with a header / metadata one day
        # show only if file doesn't already exist
        if not isfile(Folder.FileToday()):
            Create = QAction("Create new changelog for today", self)
            Create.triggered.connect(lambda: CreateChangelog())
            self.contextMenu.addAction(Create)

        # View previous changelog
        # show only if there is more than 1 file
        if len(Folder.allfiles) > 1:
            View = QAction("View last changelog", self)
            View.triggered.connect(lambda: ViewChangelog())
            self.contextMenu.addAction(View)

        # TODO: MERGELOG
        # TODO: TIDY UP CODE (SPLI IN DIFF FILES)
        # TODO: Seperate window to view changelogs
        # Merge files into one single file  
        Merge = QAction("Update mergelog", self)
        Merge.triggered.connect(lambda: print("Merge all cahngelogs into a single file"))
        self.contextMenu.addAction(Merge)

        # Show Menu
        self.contextMenu.popup(QCursor.pos())
    else:
        self.editItem(self.currentItem())