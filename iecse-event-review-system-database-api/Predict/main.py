import argparse
import os
import pymongo
from findFace import findFace
from plotGraph import plotGraph

client = pymongo.MongoClient("mongodb://localhost:27017")
db = client["IECSE-EVENT-REVIEW"]
eventsCol = db["events_conducted"]


def manageDB(path: str):
    if not os.path.isdir((path)):
        raise FileNotFoundError
    else:
        dir = os.path.basename(path)
        details = dir.split("_")
        detailsJson = {
            "_id": dir,
            "eventName": details[0],
            "eventDate": details[1],
            "startTime": details[2],
            "endTime": details[3],
            "numberOfFaces": {}
        }

        response = eventsCol.find_one(detailsJson)
        print(response)
        faceAndTime = dict()

        if response != None:
            faceAndTime = response["numberOfFaces"]
        
        
        for file in os.listdir(path):
            filename = os.path.join(path, file)
            time, faces = findFace(filename)
            faceAndTime[str(time)] = int(faces)

        detailsJson["numberOfFaces"] = faceAndTime
        eventsCol.save(detailsJson)


def plotImage(eventId: str):
    eventId = os.path.basename(eventId)
    response = eventsCol.find_one(eventId)
    if response == None:
        raise Exception("Event not in the database first predict the faces")
    faceAndTime = response["numberOfFaces"]
    noOfHeads = list()
    listTime = list()
    for key in faceAndTime:
        noOfHeads.append(faceAndTime[key])
        listTime.append(key)
    # print(listTime)
    plotGraph(noOfHeads=noOfHeads, listTime=listTime)


if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path", help="Path of the directory conatining the images", type=str)
    parser.add_argument("-t", "--plot", help="Event id of the event to plot", type=str)

    args = parser.parse_args()

    if args.path and args.plot:
        manageDB(args.path)
        plotImage(args.plot)
    elif args.path:
        manageDB(args.path)
    elif args.plot:
        plotImage(args.plot) 
    else: 
        path = input("Enter Path to the image Directory: ")
        manageDB(path)