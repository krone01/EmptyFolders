import os
import shutil
import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument('-r', '--removeEmpty', action='store_true', default = False, help = 'Add this flag if you would like to delete emptied folders [DEFAULT: FALSE]')
parser.add_argument('-f', '--onlyFiles', nargs = '*', type = str, default = '')
parser.add_argument('-n', '--notFiles', nargs = '*', type = str, default = ['.py'])
parser.add_argument('-s', '--startDir', nargs = '?', type = str, default = '.')
parser.add_argument('-e', '--endDir', nargs = '?', type = str, default = '.')
parser.add_argument('-w', '--noWarning', action='store_false', default = True)
parser.add_argument('-g', '--groupTypes', action='store_true', default = False)
flags = parser.parse_args()

START_DIR = os.path.abspath(flags.startDir)
END_DIR = os.path.abspath(flags.endDir)
SUPPORTED_FILES = tuple(flags.onlyFiles)
IGNORED_FILES = tuple(flags.notFiles)
REMOVE_EMPTY = flags.removeEmpty
WARNING = flags.noWarning
GROUP_TYPES = flags.groupTypes


def removeEmptyFolders(path):
    if not os.path.isdir(path):
        return
    
    files = os.listdir(path)
    if len(files):
        for file in files:
            truePath = os.path.join(path, file)
            if os.path.isdir(truePath):
                removeEmptyFolders(truePath)    

    files = os.listdir(path)
    if not len(files) and path != END_DIR:
        print("Deleted Folder:", path)
        os.rmdir(path)

try:
    while WARNING:
        print("--WARNING--")
        print("This script can be very destructive if ran in the wrong directory.")
        print("Current directory is set to:", START_DIR)
        print("Files are being moved to:", END_DIR)
        print("Current file extensions being emptied:", SUPPORTED_FILES)
        print("Current file extensions being ignored:", IGNORED_FILES)
        print("Removal of empty folders is set to:", REMOVE_EMPTY)
        print("Grouping files by extension is set to:", GROUP_TYPES)
        reply = input("Does this sound correct? (Y/N): ")
        
        if reply.lower() in ("yes", "y"):
            if START_DIR is not END_DIR:
                if os.path.isdir(END_DIR):
                    break
                else:
                    os.mkdir(END_DIR)
            break        
        else:
            sys.exit()


    for root, directories, files in os.walk(START_DIR, topdown = False):
        for file in files:
            pathRoot = os.path.join(START_DIR, file)
            pathCurrentFile = os.path.join(root, file)
            #print(pathCurrentFile)
            if file.endswith(IGNORED_FILES):
                print("Skipping", file, "in", root)

            elif file.endswith(SUPPORTED_FILES):
                #if GROUP_TYPES:
                    #ext = os.path.splitext(file)[1]
                    #ext = ext.replace('.', '')
                    #print(ext)

                if not os.path.isfile(pathRoot):
                    shutil.move(pathCurrentFile, END_DIR)
                    print(file, "in", root, "moved to", END_DIR)
                else:
                    print(file, "already exists in", root, "! Skipping...")

    if REMOVE_EMPTY:
        removeEmptyFolders(START_DIR)

except IOError as err:
    print("I/O error: {0}".format(err))
except:
    print("Unexpected error:", sys.exc_info()[0])
    raise
