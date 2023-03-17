from tkinter import *


from tkhtmlview import *
from tkinter import *
from tkinter.ttk import *
import tkinter
from PIL import ImageTk
import PIL.Image
import requests

from listening import Listening
from speaking import Speaking
from practice import Practice
from reading import Reading
from writing import Writing

class HomePage:
    def __init__(self):
        self.homePage = Tk()
        self.homePage.geometry("750x750")
        self.homePage.title("choose a learning mode")

        navBar = Frame(self.homePage)
        navBar.pack(side=TOP)

        tkinter.Button(navBar, text="Listening", command=Listening,justify=LEFT).grid(row=0,column=0, columnspan=1)
        tkinter.Button(navBar, text="Speaking",command=Speaking,justify=LEFT).grid(row=0,column=1)
        #tkinter.Button(navBar, text="Practice",command=Practice,justify=LEFT).grid(row=1,column=0,columnspan=2)
        tkinter.Button(navBar, text="Reading",command=Reading,justify=LEFT).grid(row=2,column=0)
        tkinter.Button(navBar, text="Writing",command=Writing,justify=LEFT).grid(row=2,column=1)



if __name__ == "__main__":
    
    myHomePage = HomePage()
    myHomePage.homePage.mainloop()
        