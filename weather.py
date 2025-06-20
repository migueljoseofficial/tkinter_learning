from tkinter import *
from tkinter import ttk

# def calculate


#sets up the main application window
root = Tk()
root.title("feet to meters") # gives a name to the window

#frame widget will hold the content 
mainframe = ttk.Frame(root, padding="3 3 12 12") #need to put a frame within the window for color consistency (stems from version updates)
mainframe.grid(column=0, row=0, sticky=(N,W,E,S)) 

#tells windows to expand and reactive to resizing
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)


#entry widget
feet = StringVar()
feet_entry
