from tkinter import *
import tkinter.font
import datetime
import time
from time import strftime, gmtime
import requests

## variables
updateSecs = 600 #time in seconds between updating the google sheet
screenSecs = 3000 #time in miliseconds until blanking the display
initialSG = float(1050)/1000

#Assign uuid's of various colour tilt hydrometers. BLE devices like the tilt work primarily using advertisements. 
#The first section of any advertisement is the universally unique identifier. Tilt uses a particular identifier based on the colour of the device
red    	= 'a495bb10c5b14b44b5121370f02d74de'
green  	= 'a495bb20c5b14b44b5121370f02d74de'
black  	= 'a495bb30c5b14b44b5121370f02d74de'
purple 	= 'a495bb40c5b14b44b5121370f02d74de'
orange 	= 'a495bb50c5b14b44b5121370f02d74de'
blue   	= 'a495bb60c5b14b44b5121370f02d74de'
yellow 	= 'a495bb70c5b14b44b5121370f02d74de'
pink   	= 'a495bb80c5b14b44b5121370f02d74de'

##GUI definitions
win = Tk()
win.title("Tilt reader")
myFont = tkinter.font.Font(family = 'Helvetiva', size = 12, weight = "bold")

## Functions

#function to calculate the number of days since epoch (used by google sheets)
#In python time.time() gives number of seconds since epoch (Jan 1 1970).
#Google Sheets datetime as a number is the number of days since the epoch except their epoch date is Jan 1 1900
def sheetsDate(date1):
	temp = datetime.datetime(1899, 12, 30)
	delta=date1-temp
	return float(delta.days) + (float(delta.seconds) / 86400)

def updateData():
    theTime.set(strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime()))
    theTemp.set("25")
    theSG.set(initialSG)
    theColour.set("Black")
    theBeer.set("Test beer")

def updateLoop():
    updateData()
    win.after(screenSecs, updateLoop)
            
def calcSG(sg):
        return sg-float(1/1000)


## variable variables
theTime = StringVar()
theTemp = StringVar()
theSG = StringVar()
theColour = StringVar()
theBeer = StringVar()

## Widgets

def main():
    myTime = Label(win, textvariable = theTime)
    myTime.pack()
    myTemp = Label(win, textvariable = theTemp)
    myTemp.pack()
    mySG = Label(win, textvariable = theSG)
    mySG.pack()
    myColour = Label(win, textvariable = theColour)
    myColour.pack()
    myBeer = Label(win, textvariable = theBeer)
    
    myButton = Button(win, text = 'Refresh', font = myFont, command = updateData, bg = 'bisque2', height = 1, width = 24)
    myButton.pack()

    screenTime = time.time() + screenSecs
    updateData()

    win.after(screenSecs, updateLoop)
    win.mainloop()

main()
