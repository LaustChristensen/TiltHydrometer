from tkinter import *
import tkinter.font
import time
from time import strftime, gmtime

## variables
updateSecs = 600 #time in seconds between updating the google sheet
screenSecs = 3000 #time in miliseconds until blanking the display


##GUI definitions
win = Tk()
win.title("Tilt reader")
myFont = tkinter.font.Font(family = 'Helvetiva', size = 12, weight = "bold")

def updateTime():
    theTime.set(strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime()))

def updateLoop():
    updateTime()
    win.after(screenSecs, updateLoop)
            

## variable variables
theTime = StringVar()

## Widgets

def main():
    myText = Label(win, textvariable = theTime)
    myText.pack()
    myButton = Button(win, text = 'Refresh', font = myFont, command = updateTime, bg = 'bisque2', height = 1, width = 24)
    myButton.pack()
    screenTime = time.time() + screenSecs
    updateTime()
    win.after(screenSecs, updateLoop)
    win.mainloop()

main()
