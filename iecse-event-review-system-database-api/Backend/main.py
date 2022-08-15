from fastapi import FastAPI, UploadFile, File, Form
from pydantic import BaseModel
from datetime import date, time
from PIL import Image
import os
import shutil
import uvicorn

app = FastAPI()

class EventDetails(BaseModel):
    eventName: str
    eventDate: date
    startTime: time
    endTime: time


@app.get("/")
async def root():
    return {"message": "hello"}


@app.post("/create_event")
async def create_event(event_details: EventDetails):
    dir = f"{event_details.eventName}_{event_details.eventDate}_{event_details.startTime.strftime('%H-%M')}_{event_details.endTime.strftime('%H-%M')}"
    if(event_details.startTime >= event_details.endTime):
        return {"message": "Start time should be lesser than end time"}
    if(os.path.isdir(dir)):
        return {"message": "Event already created"}


    os.mkdir(dir)
    """ os.mkdir(os.path.join(dir, "originalImage"))
    os.mkdir(os.path.join(dir, "attendancePlots")) """
    return {"message": "Event created successfully"}



@app.post("/post_image")
async def post_image(eventName: str = Form(...), eventDate: date = Form(...), startTime: time = Form(...), endTime: time = Form(...), captureTime: time = Form(...), imageFile: UploadFile = File(...)):
    dir = f"{eventName}_{eventDate}_{startTime.strftime('%H-%M')}_{endTime.strftime('%H-%M')}"
    if(not os.path.isdir(dir)):
        return {"message": "Event does not exist"}

    if(not (imageFile.content_type == 'image/jpg' or imageFile.content_type == 'image/jpeg' or imageFile.content_type == 'image/png')):
        return {"message": "Please upload a jpg or png file only"}

    fileName = f"{eventName}_{eventDate}_{startTime.strftime('%H-%M')}_{endTime.strftime('%H-%M')}_{captureTime.strftime('%H-%M')}.{imageFile.filename.split('.')[-1]}"

    with open(os.path.join(dir, fileName), "wb") as buffer: 
        shutil.copyfileobj(imageFile.file, buffer)
        
    return {"message": "Image saved successfully"}

if __name__ == "__main__":
   uvicorn.run("app", host="0.0.0.0", port=8000, reload=True)
