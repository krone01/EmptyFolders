import os
import shutil
import argparse
import sys
import re

parser = argparse.ArgumentParser()
parser.add_argument('-r', '--removeEmpty', action='store_true', default = False, help = 'Add this flag if you would like to delete emptied folders [DEFAULT: FALSE]')
parser.add_argument('-f', '--onlyFiles', nargs = '*', type = str, default = '')
parser.add_argument('-n', '--notFiles', nargs = '*', type = str, default = ['.py'])
parser.add_argument('-s', '--startDir', nargs = '?', type = str, default = '.')
parser.add_argument('-e', '--endDir', nargs = '?', type = str, default = '.')
parser.add_argument('-w', '--noWarning', action='store_false', default = True)
parser.add_argument('-g', '--groupTypes', action='store_true', default = False)
parser.add_argument('-l', '--logging', action='store_true', default = False)
flags = parser.parse_args()

START_DIR = os.path.abspath(flags.startDir)
END_DIR = os.path.abspath(flags.endDir)
SUPPORTED_FILES = tuple(flags.onlyFiles)
IGNORED_FILES = tuple(flags.notFiles)
REMOVE_EMPTY = flags.removeEmpty
WARNING = flags.noWarning
GROUP_TYPES = flags.groupTypes
LOGGING = flags.logging


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

def prompt():
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



def regexRename(file, root, originalFile):
    pattern = '\(\d*\)'
    result = re.search(pattern, file)
    name, ext = os.path.splitext(file)
    

    pathCurrentFile = os.path.join(root, file)
    originalPath = os.path.join(root, originalFile)
    #print("ORIGINAL", originalPath)

    if result:
        ext = ext.replace('.', '')
        pathExtFolder = os.path.join(START_DIR, ext)

        #print("MATCH", file)
        a = re.findall(pattern, file)
        lastOccurence = a[-1]
        newNumber = lastOccurence
        newNumber = newNumber.replace('(', '')
        newNumber = newNumber.replace(')', '')
        newNumber = int(newNumber)
        newNumber += 1
        newNumber = '(' + str(newNumber) + ')'
        newFileName = file
        newFileName = newFileName.replace(lastOccurence, newNumber)
        renamePath = os.path.join(root, newFileName)
        newPath = os.path.join(pathExtFolder, newFileName)
        print(newPath)
        if os.path.isfile(newPath):
            regexRename(newFileName, root, originalFile)
        else:
            os.rename(originalPath, renamePath)
            groupFolders(newFileName, root)

    else:
        
        name = name + '(1)' + ext
        newPath = os.path.join(root, name)
        print(os.path.join(root, name))
        pathCurrentFile = os.path.join(root, file)
        print(name)
        os.rename(pathCurrentFile, newPath)


def groupFolders(file, root):
    ext = os.path.splitext(file)[1]
    ext = ext.replace('.', '')
                    
    pathCurrentFile = os.path.join(root, file)
    pathExtFolder = os.path.join(START_DIR, ext)

    if os.path.isdir(pathExtFolder):
        pathNewFile = os.path.join(pathExtFolder, file)
        #print("File:", file)
        #print("Current", pathCurrentFile)
        #print("Extension folder:", pathExtFolder)
        #print("New destination:", pathNewFile, '\n')
        if not os.path.isfile(pathNewFile):
            shutil.move(pathCurrentFile, pathExtFolder)
            print(file, "in", root, "moved to", pathExtFolder)
        elif pathCurrentFile != pathNewFile:


            #print("CURRENT", pathCurrentFile)
            #print("NEW", pathNewFile)
            regexRename(file, root, file)   
            #print(file, "already exists in", root, "! Skipping...")
        else:
            print(file, "already exists in", root, "! Skipping...")
    else:
        os.mkdir(pathExtFolder)
        shutil.move(pathCurrentFile, pathExtFolder)
        print(file, "in", root, "moved to", pathExtFolder)


try:
    prompt()

    for root, directories, files in os.walk(START_DIR, topdown = False):
        for file in files:
            pathRoot = os.path.join(START_DIR, file)
            pathCurrentFile = os.path.join(root, file)

            if file.endswith(IGNORED_FILES):
                print("Skipping", file, "in", root)

            elif file.endswith(SUPPORTED_FILES) or not SUPPORTED_FILES:
                if GROUP_TYPES:
                    groupFolders(file, root)

                elif not os.path.isfile(pathRoot):
                    shutil.move(pathCurrentFile, END_DIR)
                    #print(file, "in", root, "moved to", END_DIR)
                #else:
                    #print(file, "already exists in", root, "! Skipping...")

    if REMOVE_EMPTY:
        removeEmptyFolders(START_DIR)

except IOError as err:
    print("I/O error: {0}".format(err))
except:
    print("Unexpected error:", sys.exc_info()[0])
    raise
