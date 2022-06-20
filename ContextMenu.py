from pydoc import ispath
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
        def GetKey():
            return "*"

        def GetPath(extra = "", file = False):
            path = self.currentItem().text() + "/" + extra
            if file: path += ".txt"
            return path

        def GetAllFiles():
            # TODO: change this to sort by 3rd line in file instead of metadata
            # TODO: make error handler for this operation aswell - preferably a popup window
            allfiles = sorted(glob.iglob(Folder.GetPath("*", True)), key=os.path.getctime) # all files sorted by date created
            return allfiles

        def GetDate(format):
            return str(datetime.today().strftime(format))

        def FileToday():
            return Folder.GetPath(Folder.GetDate('%d.%m.%y'), True)

        def FileLast():
            files = Folder.GetAllFiles()
            rename = False
            file = files[0]

            print(file)

            # If file name != header then flag it and rename it
            # TODO: Convert to function
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
                renamed = Folder.GetPath(rename, True)
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
        f.write(Folder.GetKey() + "\n")
        f.write(len(date) * "_" + "\n")
        f.write("\n")
        f.write(date + "\n")
        f.write(len(date) * "_" + "\n")
        f.write("\n")

        f.close()

    def ViewChangelog(path):
        os.system('"' + path + '"')

    def UnmergeAll():
        MergePath = Folder.GetPath("Merge", True)

        # Check if Merge Log exists
        if isfile(MergePath):
            with open(MergePath, "r+") as f:
                # Read its data
                s = f.read()
                # Split the data using the key
                split = s.split(Folder.GetKey())

                # Remove first element as it will be blank due to the first item in the merge log containing a key
                del split[0]

                # Loop through each split and convert it to a file
                # TODO: Convert this to an option in the context menu (Unmerge) but still keep it active here aswell
                for i in range(len(split)):
                    # Find header date
                    # TODO: Convert this to a function in folder class
                    thirdline = split[i].split("\n")[3][:-1]

                    # Create file so long as it doesn't already exist
                    if not isfile(Folder.GetPath(thirdline, True)):
                        temp = open(Folder.GetPath(thirdline, True), "w")
                        temp.write(Folder.GetKey())
                        temp.write("".join(split[i]))
                        print("".join(split[i]))
                        temp.close()

                f.close()
        
            # Remove contents of merge file
            with open(MergePath, 'r+') as f:
                f.truncate(0)
        else:
            # Create new Merge Log
            f = open(MergePath, "w")
            f.close()

    def MergeAll():
        # TODO: tidy up! + Simplify
        MergePath = Folder.GetPath("Merge", True)

        # Form Merge file
        for i in range(len(Folder.GetAllFiles())):
            if Folder.GetAllFiles()[i].find("Merge.txt") == -1:
                s = ""

                # Read data
                with open(Folder.GetAllFiles()[i], "r") as f:
                    s = f.readlines()
                    EndLine = ""

                    if (len(s) - 1 > 0):
                        EndLine = s[len(s) - 1]

                    # Remove end lines
                    while (EndLine == "\n") and len(s) - 1 > 0:
                        s.pop(len(s) - 1)
                        EndLine = s[len(s) - 1]

                    # If last last line doesn't have newline then add one
                    if not "\n" in s[len(s) - 1]:
                        s[len(s) - 1] = s[len(s) - 1] + "\n"
                    
                    # Add ending line
                    s.append("\n")
                    
                    # Set first line to be key
                    s[0] = Folder.GetKey() + "\n"

                    print(s)

                    s = "".join(s) 

                # Write to merge file
                with open(MergePath, "a") as f:
                    f.write(s)
                    f.close()

    if User.Data.StoredKeys[self.currentColumn()] == "location": # Location
        # Only open menu if path is valid
        if isdir(Folder.GetPath()):
            # Menu
            self.contextMenu = QMenu(self)

            # Edit path on item
            Edit = QAction("Edit Path", self)
            Edit.triggered.connect(lambda: EditDir())
            Edit.setIcon(QIcon("Images/Edit.ico"))
            self.contextMenu.addAction(Edit)

            # Create changelog with todays date
            if not isfile(Folder.FileToday()):
                CreateOpen = QAction("Create " + Folder.GetDate("%d.%m.%y.txt"), self)
                CreateOpen.setIcon(QIcon("Images/Create.ico"))
                CreateOpen.triggered.connect(lambda: CreateChangelog())
            else:
                CreateOpen = QAction("Open "  + Folder.GetDate("%d.%m.%y.txt"), self)
                CreateOpen.setIcon(QIcon("Images/Open.ico"))
                CreateOpen.triggered.connect(lambda: ViewChangelog(Folder.GetPath(Folder.GetDate("%d.%m.%y"), True)))
            
            self.contextMenu.addAction(CreateOpen)

            # show only if there is more than 1 file
            if len(Folder.GetAllFiles()) > 1:
                # View previous changelog
                View = QAction("View last changelog", self)
                View.triggered.connect(lambda: ViewChangelog(Folder.FileLast()))
                View.setIcon(QIcon("Images/View.ico"))
                self.contextMenu.addAction(View)

            # Merge changelogs together
            Merge = None

            if not isfile(Folder.GetPath("Merge", True)):
                Merge = QAction("Create Mergelog", self)
            else:
                if len(Folder.GetAllFiles()) > 1:
                    Merge = QAction("Update and Extract Mergelog", self)
                else:
                    Merge = QAction("Extract Mergelog", self)

            Merge.triggered.connect(lambda: UnmergeAll() or MergeAll()) # This is odd but the OR statement here works like an AND statement
            Merge.setIcon(QIcon("Images/Merge.ico"))
            self.contextMenu.addAction(Merge)

            # Show Menu
            self.contextMenu.popup(QCursor.pos())
        else:
            self.editItem(self.currentItem())
            EditDir()
    else:
        self.editItem(self.currentItem())