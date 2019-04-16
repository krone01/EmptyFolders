import os
import shutil
import argparse
#from PyQt5.QtWidgets import QLabel, QApplication, QCheckBox
#from Window import Ui_Dialog

supportedFiles = ".mp3", ".flac", ".aac", ".wav"
ignoredFiles = ".py"
pathUnsupportFiles = "UNSUPPORTED"
startDirectory = "."

parser = argparse.ArgumentParser()
parser.add_argument('-r', '--removeEmpty', action='store_true', default = False, help = 'Add this flag if you would like to delete emptied folders [DEFAULT: FALSE]')
parser.add_argument('-o', '--onlyFiles', nargs = '*', type = str, default = supportedFiles)
parser.add_argument('-n', '--notFiles', nargs = '*', type = str, default = ignoredFiles)
flags = parser.parse_args()
print(flags.removeEmpty)
print(flags.onlyFiles)
print(flags.notFiles)

#class AppWindow(QDialog):
#    def __init__(self):
#        super().__init__()
#        self.ui = Ui_Dialog()
#        self.ui.setupUi(self)
#        self.show()  

#app = QApplication([])
#w = AppWindow()
#w.show()
#app.exec_()

def removeEmptyFolders(path):
    if not os.path.isdir(path):
        return
    
    files = os.listdir(path)
    #Enter subdirectories and delete them
    if len(files):
        for file in files:
            truePath = os.path.join(path, file)
            if os.path.isdir(truePath):
                print(truePath, "is a folder!")
                removeEmptyFolders(truePath)    

    files = os.listdir(path)
    #Delete folder if it's empty
    if not len(files):
        print("Deleted Folder: ", path)
        os.rmdir(path)

try:
    for root, directories, files in os.walk(startDirectory):
        for file in files:
            pathRoot = os.path.join(startDirectory, file)
            pathCurrentFile = os.path.join(root, file)
            print(pathCurrentFile)

            if file.endswith(flags.onlyFiles):
                if not os.path.isfile(pathRoot):
                    shutil.move(pathCurrentFile, startDirectory)
                    print(file, "in", root, "moved to", startDirectory)
                else:
                    print(file, "already exists in", root, "! Skipping...")

            elif file.endswith(flags.notFiles):
                print("Skipping", file, "in", root)

            else:
                pathCurrentFile = os.path.join(pathUnsupportFiles, file)
                if os.path.isdir(pathUnsupportFiles):
                    if not os.path.isfile(pathCurrentFile):
                        shutil.move(pathOriginal, pathUnsupportFiles)
                        print(file, "in", root, "moved to", pathUnsupportFiles)

                    else:
                        print(file, "already exists in", pathUnsupportFiles, "! Skipping...")

                else:
                    os.mkdir(pathUnsupportFiles)
                    print("Creating directory:", pathUnsupportFiles)
                    shutil.move(pathOriginal, pathUnsupportFiles)
                    print(pathOriginal, "moved to", pathUnsupportFiles)

    if flags.removeEmpty:
        removeEmptyFolders(startDirectory)

except IOError as err:
    print("I/O error: {0}".format(err))
except:
    print("Unexpected error:", sys.exc_info()[0])
    raise
