from tkinter import *
import tkinter.font
import time
from datetime import date


##GUi definitions
win = Tk()
win.title("Tilt reader")
myFont = tkinter.font.Font(family = 'Helvetiva', size = 12, weight = "bold")

def readToggle():
    theTime.set(time.localtime())

## variables
theTime = StringVar()

## Widgets
myText = Label(win, textvariable = theTime)
myText.pack()
myButton = Button(win, text = 'Refresh', font = myFont, command = readToggle, bg = 'bisque2', height = 1, width = 24)
myButton.pack()
