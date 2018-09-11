#!/usr/bin/env python
import os

result=os.system('python setup.py install')

from tkinter import messagebox, Tk
root = Tk()
root.withdraw()

if result==0:
    messagebox.showinfo("Success!","Success!")
else:
    messagebox.showerror("Error", 
        "Something went wrong...probably didn't do 'Extract All...' in Windows")