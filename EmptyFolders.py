import os
import shutil
#from PyQt5.QtWidgets import QLabel, QApplication, QCheckBox
#from Window import Ui_Dialog

supportedFiles = ".mp3", ".flac", ".aac", ".wav"

pathUnsupportFiles = "UNSUPPORTED"

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

try:
    for root, directories, files in os.walk("."):
        for file in files:
            pathOriginal = os.path.join(root, file)
            pathCurrentFile = pathOriginal
            print(pathCurrentFile)

            if file.endswith(supportedFiles):
                if not os.path.isfile(pathCurrentFile):
                    shutil.move(pathCurrentFile, ".")
                    print(file, "in", root, "moved to ./")

            elif file.endswith(".py"):
                print("Skipping python file:", file, "in", root)

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

except IOError as err:
    print("I/O error: {0}".format(err))
except:
    print("Unexpected error:", sys.exc_info()[0])
    raise
