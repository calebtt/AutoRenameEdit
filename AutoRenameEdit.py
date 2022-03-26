#!/usr/bin/env python3

import sys
import os
import random
import file_operations as fo
import copy
import tkinter as tk
from tkinter import filedialog

from typing import Tuple

PROG_FILE_NAME = sys.argv[0]
"""name of this python script"""

DICTFILENAME = "dict.txt"
"""name of the dictionary file, no path included."""
PERIOD_CHAR = "."
"""named value for period character"""
# seed random in default manner
random.seed()

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
print("\nTo-be-renamed directory is: ", workingDirectory)
# build list of image files in directory
fileNameList = fo.build_image_list(directoryList, PROG_FILE_NAME)
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
fullDictionaryPath = dictionaryDirectory + "\\" + DICTFILENAME
goodDictionaryResult = fo.is_dictionary_file_good(fullDictionaryPath)
if not goodDictionaryResult:
    print("Not an acceptable dictionary file, exiting...")
    print("enter to continue")
    input()
    sys.exit()

# open dictionary file and read all lines into memory while removing some short, empty, and special chars.
dictionaryFileLines = fo.readall_dictionary_file(fullDictionaryPath)
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
        if iCurrentFileNameIndex >= len(fileNameList):
            # if number of renamed files greater than equal to len of files to rename, break out of loop
            break
        if fo.check_if_file_exists_in_dir(currentDictionaryEntry):
            # if it exists in the folder already, remove from the dictionary list and move on.
            # I don't think it's a problem if the existing file happens to have the same name as the chosen new file name.
            dictionaryFileLines.remove(currentDictionaryEntry)
            iCurrentFileNameIndex += 1
            continue
        else:
            currentFileName = fileNameList[iCurrentFileNameIndex]
            currentNameOnly, currentExtension = os.path.splitext(
                currentFileName)  # split currentfilename into filename and extension
            os.rename(currentFileName, currentDictionaryEntry.rstrip() + currentExtension)  # rename file.
            print(currentFileName, " has RENAMED to: ", currentDictionaryEntry.rstrip() + currentExtension)
            iCurrentFileNameIndex += 1
else:
    print("\nAborting...")
# End of program
print("COMPLETE.")
print("enter to continue")
input()
