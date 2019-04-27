import os
import shutil
import argparse
import sys
import re

parser = argparse.ArgumentParser()
parser.add_argument('-o', '--onlyFiles', nargs='*', type=str, default='',
                    help='Specify files that you would like to empty, separated by spaces. [DEFAULT: ALL FILES]')
parser.add_argument('-n', '--notFiles', nargs='*', type=str, default=['.py'], 
                    help='Specify file to ignore removing, separated by spaces. [DEFAULT: .py]')
parser.add_argument('-r', '--removeEmpty', action='store_true', default=False,
                    help='Add this flag if you would like to delete emptied folders [DEFAULT: FALSE]')
parser.add_argument('-d', '--removeRoot', action='store_true', default=False,
                    help='Add this flag if you would like to delete the starting directory. (This only works if your starting directory is different than the directory the script is in) [DEFAULT: FALSE]')
parser.add_argument('-w', '--noWarning', action='store_true', default=False,
                    help='Add this flag if you would like to skip the warning message. [DEFAULT: FALSE]')
parser.add_argument('-g', '--groupTypes', action='store_true', default=False,
                    help='Group up files according to their file extension. [DEFAULT: FALSE]')
parser.add_argument('-s', '--startDir', nargs='?', type=str, default='.',
                    help='Use this flag to designate a starting directory to walk through. [DEFAULT: ROOT DIRECTORY OF THE SCRIPT]')
parser.add_argument('-e', '--endDir', nargs='?', type=str, default='.',
                    help='Use this flag to designate a directory to move the files to. [DEFAULT: ROOT DIRECTORY OF THE SCRIPT]')

flags = parser.parse_args()

START_DIR = os.path.abspath(flags.startDir)
END_DIR = os.path.abspath(flags.endDir)
SUPPORTED_FILES = tuple(flags.onlyFiles)
IGNORED_FILES = tuple(flags.notFiles)
REMOVE_EMPTY = flags.removeEmpty
WARNING = flags.noWarning
GROUP_TYPES = flags.groupTypes
REMOVE_ROOT = flags.removeRoot


def prompt():
    while not WARNING:
        print("--WARNING--")
        print("This script can be very destructive if ran in the wrong directory.")
        print("Current directory is set to:", START_DIR)
        print("Files are being moved to:", END_DIR)
        print("Current file extensions being emptied:", SUPPORTED_FILES)
        print("Current file extensions being ignored:", IGNORED_FILES)
        print("Removal of empty folders is set to:", REMOVE_EMPTY)
        print("Grouping files by extension is set to:", GROUP_TYPES)
        print("Deletion of root is set to:", REMOVE_ROOT)
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


def regexRename(file, root, originalFile):
    pattern = '\(\d*\)'
    result = re.search(pattern, file)
    name, ext = os.path.splitext(file)

    print("Attempting to rename:", file)

    pathCurrentFile = os.path.join(root, file)
    originalPath = os.path.join(root, originalFile)

    if result:
        ext = ext.replace('.', '')
        pathExtFolder = os.path.join(END_DIR, ext)
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

        if GROUP_TYPES:
            newPath = os.path.join(pathExtFolder, newFileName)
        else:
            newPath = os.path.join(root, newFileName)

        if os.path.isfile(newPath):
            regexRename(newFileName, root, originalFile)
        else:
            print("Renaming:", originalPath, "to", renamePath)
            os.rename(originalPath, renamePath)

            if GROUP_TYPES:
                groupFolders(newFileName, root)
            else:
                sortNonGrouped(newFileName, root)

    else:
        name = name + '(1)' + ext
        renamePath = os.path.join(root, name)
        pathCurrentFile = os.path.join(root, file)

        print("Renaming:", pathCurrentFile, "to", renamePath)
        os.rename(pathCurrentFile, renamePath)

        if GROUP_TYPES:
            groupFolders(name, root)
        else:
            sortNonGrouped(name, root)


def groupFolders(file, root):
    ext = os.path.splitext(file)[1]
    ext = ext.replace('.', '')

    if (ext == ''):
        ext = "none"

    pathExtFolder = os.path.join(END_DIR, ext)
    pathCurrentFile = os.path.join(root, file)

    if os.path.isdir(pathExtFolder):
        pathNewFile = os.path.join(pathExtFolder, file)
        if not os.path.isfile(pathNewFile):
            shutil.move(pathCurrentFile, pathExtFolder)
            print(file, "in", root, "moved to", pathExtFolder)
        elif pathCurrentFile != pathNewFile:
            regexRename(file, root, file)
        else:
            print(file, "already exists in", root, "! Skipping...")
    else:
        os.mkdir(pathExtFolder)
        shutil.move(pathCurrentFile, pathExtFolder)
        print(file, "in", root, "moved to", pathExtFolder)


def sortNonGrouped(file, root):
    pathRoot = os.path.join(END_DIR, file)
    pathCurrentFile = os.path.join(root, file)

    if not os.path.isfile(pathRoot):
        shutil.move(pathCurrentFile, END_DIR)
        print(file, "in", root, "moved to", END_DIR)
    elif pathCurrentFile != pathRoot:
        regexRename(file, root, file)
    else:
        print(file, "already exists in", root, "! Skipping...")


try:
    prompt()

    for root, directories, files in os.walk(START_DIR, topdown=False):
        for file in files:
            if file.endswith(IGNORED_FILES):
                print("Skipping", file, "in", root)

            elif file.endswith(SUPPORTED_FILES) or not SUPPORTED_FILES:

                if GROUP_TYPES:
                    groupFolders(file, root)
                else:
                    sortNonGrouped(file, root)

    if REMOVE_EMPTY:
        removeEmptyFolders(START_DIR)

    if REMOVE_ROOT and START_DIR is not '.':
        os.rmdir(START_DIR)    
    

except IOError as err:
    print("I/O error: {0}".format(err))
except:
    print("Unexpected error:", sys.exc_info()[0])
    raise
