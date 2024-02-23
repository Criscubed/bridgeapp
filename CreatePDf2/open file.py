import os
from tkinter import Tk
from tkinter.filedialog import askdirectory
path = askdirectory(title='Select A Folder Full Of TABLES') # shows dialog box and return the path

for file in os.listdir(path):
    print(file.removesuffix(".csv") + "_back")
    print(file.removesuffix(".csv") + "_fwd")
