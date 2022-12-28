import requests
import os
from datetime import datetime, timedelta
from enum import Enum

LINK = "https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY&hd=true"

class PicDay(Enum):
    TODAY = 1
    YESTERDAY = 2

def getImagePath():
    return str(os.path.dirname(__file__)) + "/images/"

def generateFileName(day):
    todayName = "spacepicoftheday"
    yesterdayName = "spacepicofyesterday"
    ext = ".jpg"
    imagePath = getImagePath()

    if day == PicDay.TODAY.name:
        picToday = imagePath + todayName + "_" + getCurrentDate() + ext
        return picToday

    elif day == PicDay.YESTERDAY.name:
        picYesterday = imagePath + yesterdayName + "_" + getCurrentDate() + ext
        return picYesterday

def getCurrentDate():
    return str(datetime.strftime(datetime.today(), "%Y-%m-%d"))

def stringToDateTime(dateString):
    return datetime.strptime(dateString, "%Y-%m-%d").date()

def getPreviousDate(date):
    dateTime = stringToDateTime(date) - timedelta(days=1)
    return dateTime.strftime("%Y-%m-%d")

def getImageLinks():
    image_array = ({"today":"","yesterday":""})
    date = getCurrentDate()

    for x in image_array.keys():
        callResponse = requests.get(LINK + "&date=" + date).json()

        if callResponse["media_type"] == "video":
            date = getPreviousDate(date)
            callResponse = requests.get(LINK + "&date=" + date).json()
            image_array[x] = callResponse["hdurl"]
        elif callResponse["media_type"] == "image":
            image_array[x] = callResponse["hdurl"]
        
        date = getPreviousDate(date)
    return image_array

def getNumbersOfDisplays():
    displays = os.popen('system_profiler SPDisplaysDataType -json | grep "_spdisplays_displayID"').read().splitlines()
    return len(displays)

def saveImage(image, day):
    filename = generateFileName(day)
    imagePath = getImagePath()
    os.makedirs(imagePath, exist_ok=True)

    try:
        with open(filename, 'wb') as f:
            f.write(image.content)
    except:
        print("File wasn't saved")
    return filename

def downloadImage():
    savedFilesData = {"primaryImg": "", "secondaryImg": "", "displayNr": ""}

    try:
        imageLinks = getImageLinks()
    except:
        print("Failed to get links for todays images")
    
    try:
        displayCount = getNumbersOfDisplays()
        savedFilesData["displayNr"] = displayCount
    except:
        print("Failed to get number of displays")

    if displayCount == 1:
        try:
            imagePrimary = requests.get(imageLinks["today"])
            filenamePrimary = saveImage(imagePrimary,PicDay.TODAY.name)
            savedFilesData["primaryImg"] = filenamePrimary
        except:
            print("Picture of the day failed to download")
    elif displayCount == 2:
        try:
            imagePrimary = requests.get(imageLinks["today"])
            imageSecondary = requests.get(imageLinks["yesterday"])
            filenamePrimary = saveImage(imagePrimary,PicDay.TODAY.name)
            filenameSecondary = saveImage(imageSecondary,PicDay.YESTERDAY.name)
            savedFilesData["primaryImg"] = filenamePrimary
            savedFilesData["secondaryImg"] = filenameSecondary
        except:
            print("Pictures of the day failed to download")
    
    return savedFilesData

def setBackground(savedData):
    if savedData["displayNr"] == 2:
        try:
            os.system("osascript -e 'tell application \"System Events\" to set picture of current desktop to \"" + savedData["primaryImg"] + "\"'")
            os.system("osascript -e 'tell application \"System Events\" to set picture of current desktop to \"" + savedData["secondaryImg"] + "\"'")
        except:
            print("Failed to set primary and/or secondary displays baggrounds")
    else:
        try:
            os.system("osascript -e 'tell application \"System Events\" to set picture of current desktop to \"" + savedData["primaryImg"] + "\"'")
        except:
            print("Failed to change primary displays background")

def main():
    setBackground(downloadImage())
    
if __name__ == "__main__":
    main()