#!/usr/bin/env python3

import sys
import os
import random
import copy
import tkinter as tk
from tkinter import filedialog

# some const global variables
DICTFILENAME = "dict.txt"
MAXFILESIZE = 100000000
PROGRAMFILENAME = "AutoRenameEdit.py"  # The name of this python program...
EXTENSIONLIST = [".jpg", ".jpeg", ".png", ".gif", ".bmp"]
# seed random in default manner
random.seed()


#
#
# Functions section
#
#
# Builds a list of image files from the list of files in the directory and remove empty entries.
def build_image_list(filesInDirectory):
    temp_file_name_list = [""]
    for stt in filesInDirectory:
        if stt.endswith(PROGRAMFILENAME):
            continue
        elif os.path.isfile(stt):
            for sp in EXTENSIONLIST:
                if stt.endswith(sp):
                    temp_file_name_list.append(stt)
            # print(stt," found")
    # Remove any empty strings from the list..
    temp_file_name_list = list(filter(lambda x: x != "", temp_file_name_list))
    return temp_file_name_list


# Returns true if chosen file name already exists in directory.
def check_if_file_exists_in_dir(strName):
    for ext in EXTENSIONLIST:
        if os.path.exists(strName.rstrip() + ext):
            return True
    return False


# Some error checking before the dictionary file is loaded into memory.
def check_dictionary_file(fullPathToDictionary):
    # some basic error checking regarding the file size of the dictionary file
    # grabbing file size
    fileSize = os.path.getsize(fullPathToDictionary)
    print("Dictionary file size is: ", fileSize, " bytes.")
    # If the file is less than 50 bytes can it really be a dictionary file?
    if fileSize < 50:
        print("Not a dictionary file, too small, exiting...")
        print("enter to continue")
        input()
        sys.exit()
    # if file size is larger than MAXFILESIZE, exit
    elif fileSize > MAXFILESIZE:
        print("File size larger than 100mb, exiting...")
        print("enter to continue")
        input()
        sys.exit()

# read entire dictionary file into memory, return it, removing empty lines, short entries, and odd chars
def readall_dictionary_file():
    invalidChars = "@#$%^&*()_+-=|/?:;\\'\",.<>`~"
    dictionaryFileLines = [""]
    shortLines = 0
    with open(dictionaryDirectory + "\\" + DICTFILENAME, "r") as file:
        tempLine = file.readline()
        while len(tempLine) > 0:
            tempLine = tempLine.strip()  # strip ws chars from ends
            if len(tempLine) > 2: # 3 or more chars
                for ic in invalidChars: # replace invalid chars in string with space
                    if tempLine.find(ic):
                        tempLine = tempLine.replace(ic, ' ')
                if len(tempLine) > 2:
                    dictionaryFileLines.append(tempLine)
            else:
                shortLines = shortLines + 1
            tempLine = file.readline()
    print(shortLines, " short dictionary lines removed...")

    # holds some temporary info
    emptyLines = len(dictionaryFileLines)
    # Remove any empty strings from the list.
    dictionaryFileLines = list(filter(lambda x: x != "", dictionaryFileLines))
    print(emptyLines - len(dictionaryFileLines), " empty dictionary lines removed...")
    return dictionaryFileLines


#
#
# ENTRY POINT
#
#
print("*\nGetting the list of image files in folder...")
print("\nCurrent path is: ", os.getcwd())

dictionaryDirectory = os.getcwd()  # store program dir for finding the dictionary file later.
workingDirectory = filedialog.askdirectory()  # ask user to browser to the directory with the files.
directoryList = os.listdir(workingDirectory)  # list the files in the chosen directory.
os.chdir(workingDirectory)

# build list of image files in directory
fileNameList = build_image_list(directoryList)
if len(fileNameList) > 0:
    print("Built list of original file names...")
    print(len(fileNameList), " files in directory.")
else:
    print("Error, no files in directory.")
    print("enter to continue")
    input()
    sys.exit()

print("Seeking dictionary file...")
# Check dictionary file attributes before continuing.
check_dictionary_file(dictionaryDirectory + "\\" + DICTFILENAME)

# open dictionary file and read all lines into memory while removing some short, empty, and special chars.
dictionaryFileLines = readall_dictionary_file()

# Verify there are enough new file names in the dictionary list before proceeding.
if len(dictionaryFileLines) < len(fileNameList):
    print("There are not enough new file names in the dictionary to proceed, exiting...")
    print("enter to continue")
    input()
    sys.exit()
else:
    print("There are ", len(dictionaryFileLines), " dictionary entries, and ", len(fileNameList), " files to rename.")

# get verification from the user if they want to rename every damn picture in this folder
result = input("Are you ABSOLUTELY sure you want to continue? This operation is irreversible! Y/n :")

# use dictionaryFileLines to build a random selection of new file names
if result.upper() == "Y":
    random.shuffle(dictionaryFileLines)

iCurrentFileNameIndex = 0
# as long as the number of renamed files is less than existing fileNameList len(), rename and remove entry from dict list
for currentDictionaryEntry in dictionaryFileLines:
    if iCurrentFileNameIndex >= len(fileNameList):  # if number of renamed files greater than equal to len of files to rename, break out of loop
        break
    if check_if_file_exists_in_dir(currentDictionaryEntry):  # if it exists in the folder already, remove from the dictionary list and move on. # I don't think it's a problem if the existing file happens to have the same name as the chosen new file name.
        dictionaryFileLines.remove(currentDictionaryEntry)
        iCurrentFileNameIndex += 1
        continue
    else:
        currentFileName = fileNameList[iCurrentFileNameIndex]
        currentNameOnly, currentExtension = os.path.splitext(currentFileName)  # split currentfilename into filename and extension
        os.rename(currentFileName, currentDictionaryEntry.rstrip() + currentExtension)  # rename file.
        print(currentFileName, " has RENAMED to: ", currentDictionaryEntry.rstrip() + currentExtension)
        iCurrentFileNameIndex += 1

# End of program
print("\nCOMPLETE.")
print("enter to continue")
input()
