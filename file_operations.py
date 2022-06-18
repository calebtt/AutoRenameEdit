import os
import sys

# some settings globals
ALLOWABLE_FNAME_CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
"""string of allowed filename chars"""
EXTENSION_LIST = [".jpg", ".jpeg", ".png", ".gif", ".bmp"]
"""list of file extensions for image files, includes ."""
MAX_FILE_SIZE = 100_000_000
"""in bytes/characters"""
MIN_FILE_SIZE = 50
"""in bytes/characters"""
ENTRY_MIN_FILENAME_LENGTH = 2
"""minimum length of dictionary entry for a file name"""


def remove_invalid_filename_chars(filenameCandidate):
    """ Filters a filename candidate for not allowed characters.

    :param filenameCandidate: unfiltered file name, name only no extension or path
    :return: returns the filename candidate with chars not in the whitelist removed.
    """
    filteredName = "".join([char for char in filenameCandidate if char in ALLOWABLE_FNAME_CHARS])
    return filteredName


def build_image_list(filesInDirectory, programFileName):
    """Returns a list of image file names from the list of files in the directory and removes empty entries.

    :param filesInDirectory: is a list of all the file names in the directory.
    """
    temp_file_name_list = [""]
    for stt in filesInDirectory:
        if stt.endswith(programFileName):
            continue
        elif os.path.isfile(stt):
            for sp in EXTENSION_LIST:
                if stt.endswith(sp):
                    temp_file_name_list.append(stt)
            # print(stt," found")
    # Remove any empty strings from the list..
    temp_file_name_list = list(filter(lambda x: x != "", temp_file_name_list))
    return temp_file_name_list


def check_if_file_exists_in_dir(strName):
    """Returns true if chosen file name already exists in directory.

    :param strName: name of the file to check for existence
    """
    for ext in EXTENSION_LIST:
        if os.path.exists(strName.rstrip() + ext):
            return True
    return False


def is_dictionary_file_good(fullPathToDictionary):
    """some basic error checking regarding the file size of the dictionary file, performed before reading to memory

    :param fullPathToDictionary: full path to the dictionary file
    :return: True on good file, False on unacceptable file
    """
    # grabbing file size
    fileSize = os.path.getsize(fullPathToDictionary)
    print("Dictionary file size is: ", fileSize, " bytes.")
    # If the file is less than 50 bytes can it really be a dictionary file?
    if fileSize < MIN_FILE_SIZE:  # if file size too small
        return False
    elif fileSize > MAX_FILE_SIZE:  # if file size too large
        return False
    return True


def readall_dictionary_file(fullPathToDictionary):
    """read entire dictionary file into memory, return it, removing empty lines, short entries, and odd chars

    :return: list of dictionary file lines
    """
    dictionaryFileLines = [""]
    shortLines = 0
    with open(fullPathToDictionary, "r") as file:
        tempLine = file.readline()
        while len(tempLine) > 0:
            tempLine = tempLine.strip()  # strip ws chars from ends
            tempLine = remove_invalid_filename_chars(tempLine)  # remove invalid chars
            if len(tempLine) > ENTRY_MIN_FILENAME_LENGTH:  # filters out names too short
                dictionaryFileLines.append(tempLine)
            else:
                shortLines = shortLines + 1
            tempLine = file.readline()
    # holds some temporary info
    tempLength = len(dictionaryFileLines)
    # Remove any empty strings from the list.
    dictionaryFileLines = list(filter(lambda x: x != "", dictionaryFileLines))
    print(tempLength - len(dictionaryFileLines), " empty dictionary lines removed...")
    print(shortLines, " short dictionary lines removed...")
    return dictionaryFileLines
