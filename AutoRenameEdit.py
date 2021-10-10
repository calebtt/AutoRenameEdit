#!/usr/bin/env python3

import sys #system specific params
import os #misc os functions, (path.getsize)
import random
import copy #to copy a string, apparently

#some const global variables
DICTFILENAME = "dict.txt"
MAXFILESIZE = 100000000
PROGRAMFILENAME = "AutoRenameEdit.py" #The name of this python program...
EXTENSIONLIST = [".jpg",".jpeg",".png",".gif",".bmp"]

# seed random in default manner
random.seed()

def CheckIfFileExistsInDirectory(strName):
	for ext in EXTENSIONLIST:
		if os.path.exists(strName.rstrip()+ext):
			return True
	
	return False
#
#
# ENTRY POINT
#
#
print("*\nGetting the list of image files in folder...")
print("\nCurrent path is: ", os.getcwd())

directoryList = os.listdir()

fileNameList = [""]

# build list of files in directory
for st in directoryList:
	if st.endswith(PROGRAMFILENAME):
		continue
	elif os.path.isfile(st):
		for sp in EXTENSIONLIST:
			if st.endswith(sp):
				fileNameList.append(st)
				#print(st," found")

# Remove any empty strings from the list..
while("" in fileNameList) :
    fileNameList.remove("")

if len(fileNameList) > 0:
	print("Built list of original file names...")
	print( len(fileNameList), " files in directory.")
else:
	print("Error, no files in directory.")
	print("enter to continue")
	input()
	sys.exit()

print("Seeking dictionary file...")

#
# some basic error checking regarding the file size of the dictionary file
# grabbing file size
fileSize = os.path.getsize(DICTFILENAME)
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
	

# open dictionary file and read all lines into memory
dictionaryFileLines = [""]
with open(DICTFILENAME,"r") as file:
	dictionaryFileLines=file.readlines()

# holds some temporary info
iFilesCount = 0
# Remove any empty strings from the list..
while("" in dictionaryFileLines) :
	dictionaryFileLines.remove("")
	iFilesCount += 1

print(iFilesCount, " empty dictionary lines removed...")

filesCount = 0
# Remove new file names less than 3 characters in length
for st in dictionaryFileLines:
	if len(st) < 3:
		dictionaryFileLines.remove(st)
		filesCount +=1

print(filesCount, " short dictionary lines removed...")


print("\nFor the renaming task...")

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

if result.upper() == "Y":
	# use dictionaryFileLines to build a random selection of new file names,
	random.shuffle(dictionaryFileLines)
	
	iCurrentFileNameIndex = 0
	# as long as the number of renamed files is less than existing fileNameList len(), rename and remove entry from dict list
	for currentDictionaryEntry in dictionaryFileLines:
		# if number of renamed files greater than equal to len of files to rename, break out of loop
		if iCurrentFileNameIndex >= len(fileNameList):
			break
		if CheckIfFileExistsInDirectory(currentDictionaryEntry):
			# if it exists in the folder already, remove from the dictionary list and move on.
			# I don't think it's a problem if the existing file happens to have the same name as the chosen new file name.
			dictionaryFileLines.remove(currentDictionaryEntry)
			iCurrentFileNameIndex +=1
			continue
		else:
			currentFileName = fileNameList[iCurrentFileNameIndex]
			# split currentfilename into filename and extension
			currentNameOnly, currentExtension = os.path.splitext(currentFileName)
			# rename file.
			os.rename(currentFileName, currentDictionaryEntry.rstrip()+currentExtension)
			print(currentFileName, " + ", currentExtension, " has RENAMED to: ", currentDictionaryEntry.rstrip()+currentExtension)
			iCurrentFileNameIndex +=1
		
	print("\nCOMPLETE.")
	print("enter to continue")
	input()