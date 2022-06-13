from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import heapq
import glob
import os
from os import listdir, system
from os.path import *
from itertools import islice

from datetime import datetime

import User

def Start(self):
    class Folder:
        def GetPath():
            path = self.currentItem().text() + "/"
            return path

        path = ""
        allfiles = sorted(glob.iglob(GetPath() + '*.txt'), key=os.path.getctime) # all files sorted by date created

        def GetDate(format):
            return str(datetime.today().strftime(format))

        def FileToday():
            return Folder.GetPath() + Folder.GetDate('%d.%m.%y') + ".txt"

        def FileLast():
            files = Folder.allfiles
            rename = False
            file = files[2] # return 2nd item in list

            # If file name != header then flag it and rename it
            with open(file) as f:
                # [:-1] to remove ":"
                thirdline = f.read().split('\n')[2][:-1]
                # Header date
                title = file[(len(file) - len("dd.mm.yy.txt")) : (len(file) - len(".txt"))]
            
                if title != thirdline:
                    rename = thirdline
                
                f.close()
            
            # Rename and reassign file variable
            if rename != False:
                renamed = Folder.GetPath() + rename + ".txt"
                os.rename(file, renamed)
                file = renamed

            return file

    def EditDir():
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        if len(directory) > 0:
            self.setItem(self.currentRow(), self.currentColumn(), self.CreateItem(directory))

    def CreateChangelog():
        p = Folder.FileToday()

        date = Folder.GetDate('%d.%m.%y:')

        f = open(p, "w")
        f.write(len(date)*"_" + "\n")
        f.write("\n")
        f.write(date + "\n")
        f.write(len(date)*"_" + "\n")
        f.write("\n")
        f.close()

    def ViewChangelog(path):
        os.system('"' + path + '"')

    if User.Data.StoredKeys[self.currentColumn()] == "location": # Location
        # Menu
        self.contextMenu = QMenu(self)

        # Edit path on item
        Edit = QAction("Edit Path", self)
        Edit.triggered.connect(lambda: EditDir())
        Edit.setIcon(QIcon("Images/Edit.ico"))
        self.contextMenu.addAction(Edit)

        # Create changelog with todays date
        # TODO: ** I may make this into a custom file with a header / metadata one day
        # show only if file doesn't already exist
        if not isfile(Folder.FileToday()):
            CreateOpen = QAction("Create " + Folder.GetDate("%d.%m.%y.txt"), self)
            CreateOpen.setIcon(QIcon("Images/Create.ico"))
            CreateOpen.triggered.connect(lambda: CreateChangelog())
        else:
            CreateOpen = QAction("Open "  + Folder.GetDate("%d.%m.%y.txt"), self)
            CreateOpen.setIcon(QIcon("Images/Open.ico"))
            CreateOpen.triggered.connect(lambda: ViewChangelog(Folder.GetPath() + Folder.GetDate("%d.%m.%y.txt")))
        
        self.contextMenu.addAction(CreateOpen)

        # View previous changelog
        # show only if there is more than 1 file
        if len(Folder.allfiles) > 1:
            View = QAction("View last changelog", self)
            View.triggered.connect(lambda: ViewChangelog(Folder.FileLast()))
            View.setIcon(QIcon("Images/View.ico"))
            self.contextMenu.addAction(View)

        # TODO: MERGELOG
        # TODO: TIDY UP CODE (SPLI IN DIFF FILES)
        # TODO: Seperate window to view changelogs
        # Merge files into one single file  
        Merge = QAction("Update mergelog", self)
        Merge.triggered.connect(lambda: print("Merge all cahngelogs into a single file"))
        Merge.setIcon(QIcon("Images/Merge.ico"))
        self.contextMenu.addAction(Merge)

        # Show Menu
        self.contextMenu.popup(QCursor.pos())
    else:
        self.editItem(self.currentItem())