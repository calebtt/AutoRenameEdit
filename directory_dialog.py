from tkinter import filedialog


def get_working_folder(initialDirectory):
    # ask user to browse to the directory with the files.
    workingDir = filedialog.askdirectory(title="Choose input file directory",
                                         initialdir=initialDirectory,
                                         mustexist=True)
    return workingDir
