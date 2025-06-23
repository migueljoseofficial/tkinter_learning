from tkinter import *
from tkinter import ttk

def calculate(*args):
    try:
        value = float(feet.get()) #gets the value from the feet ()
        meters.set(int(value * .304 * 10000.0 +.5)/10000.0)
    except ValueError:
        pass


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
feet_entry = ttk.Entry(mainframe, width=7, textvariable=feet) #parent is the first parameter for a widget.

feet_entry.grid(column=2, row=1, sticky=(W,E)) #sticky says which walls it should attach t (west , east) or left and right

#meters widget 
meters = StringVar()
ttk.Label(mainframe, textvariable=meters).grid(column=2, row=2, sticky=(W, E))

ttk.Button(mainframe, text="Calculate", command=calculate).grid(column=3, row=3, sticky=W)

ttk.Label(mainframe, text='feet').grid(column=3, row=1, sticky=W)
ttk.Label(mainframe, text="is equivalent to").grid(column=1, row=2, sticky=E)
ttk.Label(mainframe, text="meters").grid(column=3, row=2, sticky=W)


#could loop through all the children of a frame/widget
for children in mainframe.winfo_children():
    print(children)
    children.grid_configure(padx=5, pady=5)

feet_entry.focus()
root.bind("<Return>", calculate)
root.mainloop()
