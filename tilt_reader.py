from tkinter import *
import tkinter.font
import datetime
import time
from time import strftime, gmtime
import requests
import blescan
import bluetooth._bluetooth as bluez

## variables
updateSecs = 600 #time in seconds between updating the google sheet
screenSecs = 10000 #time in miliseconds until blanking the display

#Assign uuid's of various colour tilt hydrometers. BLE devices like the tilt work primarily using advertisements.
#The first section of any advertisement is the universally unique identifier. Tilt uses a particular identifier based on the colour of the device
red     = 'a495bb10c5b14b44b5121370f02d74de'
green   = 'a495bb20c5b14b44b5121370f02d74de'
black   = 'a495bb30c5b14b44b5121370f02d74de'
purple  = 'a495bb40c5b14b44b5121370f02d74de'
orange  = 'a495bb50c5b14b44b5121370f02d74de'
blue    = 'a495bb60c5b14b44b5121370f02d74de'
yellow  = 'a495bb70c5b14b44b5121370f02d74de'
pink    = 'a495bb80c5b14b44b5121370f02d74de'

#The default device for bluetooth scan. If you're using a bluetooth dongle you may have to change this.
dev_id = 0

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
    data = getdata()
    #convert from string to float and then farenheit to celcius just for the display tempc = round(tempc)
    tempc = (float(data["Temp"])-32)*5/9
    #Round of the value to 2 decimal places
    #tiltSG = data['SG']
    #theColour = data['tiltColour']
    #theBeer = data['tiltBeer']
    theTime.set(strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime()))

    theTemp.set(tempc)
    theSG.set(data['SG'])
    theColour.set(data['tiltColour'])
    theBeer.set(data['tiltBeer'])
    r = requests.post(' https://script.google.com/macros/s/AKfycbxRQTGJpyijaF-KCaIpuoK_Uld6cVXa4bJqw5I-xYIzgaXNDg0/exec', data)

def updateLoop():
    updateData()
    win.after(screenSecs, updateLoop)

#scan BLE advertisements until we see one matching our tilt uuid
def getdata():
    try:
        sock = bluez.hci_open_dev(dev_id)
    except:
        print("error accessing bluetooth device...")
        sys.exit(1)
    blescan.hci_le_set_scan_parameters(sock)
    blescan.hci_enable_le_scan(sock)
    gotData = 0
    while (gotData == 0):
        returnedList = blescan.parse_events(sock, 10)
        for beacon in returnedList:             #returnedList is a list datatype of string datatypes seperated by commas (,)
            output = beacon.split(',')          #split the list into individual strings in an array
            if output[1] == black:              #Change this to the colour of you tilt
                tempf = float(output[2])        #convert the string for the temperature to a float type
                tempc = (float(output[2]) - 32)*5/9
                #tempc = round(tempc)

                gotData = 1

                tiltTime = sheetsDate(datetime.datetime.now())
                tiltSG = float(output[3])/1000
                tiltTemp = tempf
                tiltColour = 'BLACK'
                tiltBeer = 'test' #Change to an identifier of a particular brew

    #assign values to a dictionary variable for the http POST to google sheet
    data=   {
            'Time': tiltTime,
            'SG': tiltSG,
            'Temp': tiltTemp,
            'Color': tiltColour,
            'Beer': tiltBeer,
            'Comment': ""
            }
    blescan.hci_disable_le_scan(sock)
    return data

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
